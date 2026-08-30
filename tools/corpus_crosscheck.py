#!/usr/bin/env python3
"""Cross-check a list of candidate names against the board.

Reads candidate names one per line (blank lines and lines starting with # are
skipped) and reports, for each, whether the board already carries it.

Three answers, and the third is the only one that is a lead:

  NODE     a node's label or a known alias matches -> already on the board
  PROSE    no node, but the name appears in some node's narrative/desc/sub
           -> the board knows about it but has not made it a node
  ABSENT   the board has never heard of it

PROSE is the interesting middle: it means a research pass already read a source
that mentions the thing, so the question is whether it deserves promotion, not
whether it is new.

Matching is deliberately conservative on NODE (normalised exact, or containment
in either direction once normalised) and deliberately loose on PROSE (a
case-folded substring of the raw text). A loose NODE rule would report leads as
already-present, which is the expensive direction to be wrong in: it makes a
real addition invisible. A loose PROSE rule at worst costs a human ten seconds
reading the quoted context, which this prints.

Usage:
    python3 tools/corpus_crosscheck.py CANDIDATES.txt
    python3 tools/corpus_crosscheck.py CANDIDATES.txt --json OUT.json
    python3 tools/corpus_crosscheck.py --self-test
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Words that carry no discriminating power in this domain. "Air Force" alone
# must not match "Air Force Office of Special Investigations" as a NODE.
_STOP = {
    "the", "of", "and", "for", "a", "an", "inc", "llc", "corp", "corporation",
    "company", "co", "institute", "institution", "group", "office", "program",
    "programme", "project", "us", "u", "s", "united", "states",
}


def norm(s):
    """Case-fold, strip punctuation and honorifics, collapse whitespace."""
    s = s.lower()
    s = re.sub(r"\b(dr|mr|mrs|ms|prof|col|lt|gen|adm|cdr|capt|sen|rep)\.?\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def key(s):
    """Normalised form with stopwords dropped, for containment tests."""
    return tuple(w for w in norm(s).split() if w not in _STOP)


def load_board():
    with open(os.path.join(ROOT, "data", "the-program.json"), encoding="utf-8") as fh:
        return json.load(fh)


def build_index(board):
    nodes = []
    for n in board["people"] + board["entities"]:
        nodes.append({
            "id": n["id"],
            "label": n.get("label", ""),
            "cls": n.get("cls", ""),
            "tier": n.get("tier", ""),
        })
    # Prose corpus: every free-text field a research pass could have written a
    # name into, keyed by node id so a hit can be attributed.
    prose = []
    for n in board["people"] + board["entities"]:
        for fld in ("narrative", "desc", "sub", "label"):
            v = n.get(fld)
            if isinstance(v, str) and v:
                prose.append((n["id"], fld, v))
    for e in board["edges"]:
        for fld in ("label", "note", "desc"):
            v = e.get(fld)
            if isinstance(v, str) and v:
                prose.append((e.get("id") or "%s->%s" % (e.get("s"), e.get("t")), fld, v))
    for t in board["timeline"]:
        for fld in ("label", "title", "desc", "note"):
            v = t.get(fld)
            if isinstance(v, str) and v:
                prose.append((t.get("id", "timeline"), fld, v))
    return nodes, prose


def match_node(cand, nodes):
    ck = key(cand)
    if not ck:
        return None
    cs = set(ck)
    best = None
    for n in nodes:
        nk = key(n["label"])
        if not nk:
            continue
        if nk == ck:
            return (n, "exact")
        ns = set(nk)
        # Containment, but only when the shorter side is at least two
        # discriminating words -- otherwise "brown" matches everything.
        if len(ck) >= 2 and cs <= ns:
            best = best or (n, "candidate within node")
        elif len(nk) >= 2 and ns <= cs:
            best = best or (n, "node within candidate")
    return best


def match_prose(cand, prose, limit=3):
    needle = cand.lower().strip()
    if len(needle) < 4:
        return []
    hits = []
    for nid, fld, text in prose:
        low = text.lower()
        i = low.find(needle)
        if i >= 0:
            ctx = text[max(0, i - 70):i + len(needle) + 70].replace("\n", " ")
            hits.append({"id": nid, "field": fld, "context": "..." + ctx.strip() + "..."})
            if len(hits) >= limit:
                break
    return hits


# A token is worth probing on its own only if it is RARE in the board's prose.
# Length is the wrong test -- "consortium" is ten characters and appears in the
# FFRDC definition, so probing it fired a near miss on an invented name during
# the self-test. Rarity is the right one: a token in five or fewer fields
# identifies something; a token in fifty is furniture.
NEAR_DF_MAX = 5
_DF = None


def _doc_freq(prose):
    global _DF
    if _DF is None:
        _DF = {}
        for _, _, text in prose:
            for w in set(norm(text).split()):
                _DF[w] = _DF.get(w, 0) + 1
    return _DF


def distinctive(cand, prose):
    """The tokens worth probing for on their own when the full string misses.

    A full-string prose probe is exact, so "J. Robert Oppenheimer" misses a
    board that writes "Robert Oppenheimer". Reporting that as ABSENT is the
    expensive error in the other direction: it sends a researcher after
    something already carried. So every ABSENT gets a second probe, on the
    tokens rare enough to mean something, and any hit prints as a near miss
    for a human to adjudicate.

    Rarity carries the discrimination, so the length floor only has to exclude
    initials and particles -- four characters. Raising it to five drops "Reid"
    and the probe goes silent on a real surname, which the self-test catches.
    """
    df = _doc_freq(prose)
    toks = [w for w in norm(cand).split()
            if w not in _STOP and len(w) >= 4 and 0 < df.get(w, 0) <= NEAR_DF_MAX]
    toks.sort(key=lambda w: df.get(w, 0))
    return toks[:2]


def match_near(cand, prose, limit=2):
    hits = []
    for tok in distinctive(cand, prose):
        for nid, fld, text in prose:
            low = text.lower()
            i = low.find(tok)
            if i >= 0:
                ctx = text[max(0, i - 60):i + len(tok) + 60].replace("\n", " ")
                hits.append({"token": tok, "id": nid, "field": fld,
                             "context": "..." + ctx.strip() + "..."})
                break
        if len(hits) >= limit:
            break
    return hits


def classify(cands, nodes, prose):
    out = []
    for c in cands:
        m = match_node(c, nodes)
        if m:
            n, how = m
            out.append({"candidate": c, "verdict": "NODE", "how": how,
                        "node_id": n["id"], "node_label": n["label"],
                        "cls": n["cls"], "tier": n["tier"]})
            continue
        hits = match_prose(c, prose)
        if hits:
            out.append({"candidate": c, "verdict": "PROSE", "hits": hits})
        else:
            out.append({"candidate": c, "verdict": "ABSENT",
                        "near": match_near(c, prose)})
    return out


def read_candidates(path):
    cands, seen = [], set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.lower() not in seen:
                seen.add(line.lower())
                cands.append(line)
    return cands


def self_test():
    """Every branch shown rejecting the input it must reject.

    CLAUDE.md section 5: a check that has never been shown to fail is
    indistinguishable from a broken one. This tool is not in the gate, but the
    same rule applies -- a cross-check that reported ABSENT for everything
    would look exactly like a productive research pass.
    """
    board = load_board()
    nodes, prose = build_index(board)
    fails = []

    def want(cand, verdict, why):
        got = classify([cand], nodes, prose)[0]["verdict"]
        if got != verdict:
            fails.append("%-42s expected %-6s got %-6s  (%s)" % (cand, verdict, got, why))

    # A node the board certainly has.
    want("Harry M. Reid", "NODE", "a real node label, exact")
    want("Harry Reid", "NODE", "same node without the middle initial")
    # Something no source has ever named. Deliberately absurd so a future
    # research pass cannot make this test pass by accident.
    want("Zzyzx Perpetual Motion Consortium", "ABSENT", "invented, must not match")
    # The containment rule must not fire on a single common word.
    single = classify(["Brown"], nodes, prose)[0]
    if single["verdict"] == "NODE":
        fails.append("%-42s matched a node on one common word (%s)" %
                     ("Brown", single.get("node_label")))
    # An empty candidate must not match anything.
    want("", "ABSENT", "empty string")

    # The PROSE channel must be shown to fire, or it is dead code. Pick a
    # phrase out of the board's own prose at runtime rather than hardcoding
    # one, so this cannot rot into a check of a string that no longer ships.
    donor = next((t for _, f, t in prose if f == "narrative" and len(t) > 400), None)
    if donor:
        m = re.search(r"\b([A-Z][a-z]{4,})\s+([A-Z][a-z]{4,})\b", donor)
        if m and not match_node(m.group(0), nodes):
            got = classify([m.group(0)], nodes, prose)[0]["verdict"]
            if got != "PROSE":
                fails.append("%-42s expected PROSE got %s (phrase lifted from the board's own prose)"
                             % (m.group(0), got))

    # The near-miss probe must be shown to fire, or an ABSENT list silently
    # stops being adjudicable. Take a real node whose surname is rare enough
    # for the probe to fire at all, mangle it past the NODE matcher, and
    # require the surname to surface it anyway.
    #
    # The donor is chosen at runtime rather than hardcoded, and it has to be
    # rare: the first version of this test used Harry Reid, whose surname has
    # a document frequency of 121 because the board covers him heavily. The
    # probe stayed correctly silent and the test called it dead. The rule was
    # right; the fixture was wrong.
    df = _doc_freq(prose)
    donor_name = None
    for n in nodes:
        toks = [w for w in norm(n["label"]).split() if w not in _STOP and len(w) >= 4]
        if toks and 0 < df.get(toks[-1], 0) <= NEAR_DF_MAX:
            donor_name = toks[-1]
            break
    if not donor_name:
        fails.append("no node has a surname rare enough to probe -- cannot test the near-miss channel")
    else:
        mangled = "Qwertyuiop %s-Xyzzy" % donor_name.title()
        r = classify([mangled], nodes, prose)[0]
        if r["verdict"] != "ABSENT":
            fails.append("%-42s expected ABSENT got %s" % (mangled, r["verdict"]))
        elif not r.get("near"):
            fails.append("%-42s ABSENT with no near miss -- the loose probe is dead" % mangled)
    # And it must stay quiet on something genuinely unheard of.
    r = classify(["Zzyzx Perpetual Motion Consortium"], nodes, prose)[0]
    if r.get("near"):
        fails.append("near-miss probe fired on an invented name: %s" % r["near"])

    if fails:
        print("SELF-TEST FAILED")
        for f in fails:
            print("  " + f)
        return 1
    print("self-test ok: %d node index, %d prose fields" % (len(nodes), len(prose)))
    return 0


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        return self_test()
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    out_json = None
    if "--json" in args:
        out_json = args[args.index("--json") + 1]

    board = load_board()
    nodes, prose = build_index(board)
    cands = read_candidates(path)
    res = classify(cands, nodes, prose)

    order = {"ABSENT": 0, "PROSE": 1, "NODE": 2}
    res.sort(key=lambda r: (order[r["verdict"]], r["candidate"].lower()))

    counts = {"NODE": 0, "PROSE": 0, "ABSENT": 0}
    for r in res:
        counts[r["verdict"]] += 1

    print("%d candidates against %d nodes" % (len(cands), len(nodes)))
    print("  ABSENT %3d   not on the board in any form -- these are the leads" % counts["ABSENT"])
    print("  PROSE  %3d   named in board prose, not a node -- promotion questions" % counts["PROSE"])
    print("  NODE   %3d   already a node" % counts["NODE"])
    print()
    for verdict in ("ABSENT", "PROSE", "NODE"):
        rows = [r for r in res if r["verdict"] == verdict]
        if not rows:
            continue
        print("== %s (%d) ==" % (verdict, len(rows)))
        for r in rows:
            if verdict == "NODE":
                print("  %-46s -> %s  [%s %s, %s]" %
                      (r["candidate"], r["node_label"], r["cls"], r["tier"], r["how"]))
            elif verdict == "PROSE":
                print("  %s" % r["candidate"])
                for h in r["hits"]:
                    print("      %s.%s %s" % (h["id"], h["field"], h["context"][:160]))
            else:
                near = r.get("near") or []
                print("  %s%s" % (r["candidate"], "   <- NEAR MISS, adjudicate" if near else ""))
                for h in near:
                    print("      ~%s  %s.%s %s" % (h["token"], h["id"], h["field"], h["context"][:150]))
        print()

    if out_json:
        with open(out_json, "w", encoding="utf-8") as fh:
            json.dump({"counts": counts, "results": res}, fh, indent=1)
        print("wrote %s" % out_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
