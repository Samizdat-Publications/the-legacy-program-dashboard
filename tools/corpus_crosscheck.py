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
    "programme", "project", "operation", "us", "u", "s", "united", "states",
}


_ARTICLES = {"the", "of", "and", "for", "a", "an"}


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


def aliases(n):
    """The forms a transcript uses for a node that its label does not.

    On the first Michels pass (2 September 2026) two triage agents independently
    found 29 false ABSENTs in 474 rows, and every one was the same shape: the
    board's label is `Central Intelligence Agency` and the speaker said `CIA`;
    the label is `Charles E. Schumer` and the speaker said `Chuck Schumer`, which
    is the node's own id with the dash opened out. A false ABSENT is the
    expensive direction, so each node now answers to its id, to any acronym in
    parentheses in its label, and to the initials of its label's own words.
    """
    out = set()
    label = n.get("label", "") or ""
    out.add(norm(label))
    nid = n.get("id", "") or ""
    # ids carry a class prefix on this board for locations and domains (l-, d-).
    nid_words = re.sub(r"^(l|d|p)-", "", nid).replace("-", " ")
    out.add(norm(nid_words))
    for par in re.findall(r"\(([^)]{2,40})\)", label):
        out.add(norm(par))
    words = [w for w in norm(label).split() if w not in _STOP]
    if len(words) >= 2:
        acr = "".join(w[0] for w in words)
        if len(acr) >= 3:
            out.add(acr)
    # Initials over every label word except articles, so `United Kingdom
    # Ministry of Defence` answers to UKMOD (the stopword list drops `united`
    # and the strict form above yields KMD). And the initials of every run of
    # three to five consecutive words, so `DoD Nuclear Weapon Personnel
    # Reliability Program (...)` answers to PRP. Both found on the Area 52
    # triage of 2 September 2026, reported as false ABSENTs.
    loose = [w for w in norm(label).split() if w not in _ARTICLES]
    if len(loose) >= 2:
        out.add("".join(w[0] for w in loose))
    for width in (3, 4, 5):
        for i in range(0, len(loose) - width + 1):
            run = loose[i:i + width]
            # `program` is a stopword, and PRP ends in it: no stopword test here.
            if True:
                out.add("".join(w[0] for w in run))
    return {a for a in out if a}


def _singular(k):
    return tuple(w[:-1] if len(w) > 4 and w.endswith("s") else w for w in k)


# The given-name variants speakers use. Both directions are consulted, so the
# table lists the short form once. Added after the first Michels triage found
# Carl Nell, Bob Salas, Stephen Greer, Lou Elizondo and Danny Sheehan all
# reported ABSENT against nodes the board plainly carries.
NICKNAMES = {
    "bob": "robert", "bobby": "robert", "rob": "robert", "bill": "william",
    "will": "william", "chuck": "charles", "charlie": "charles", "dan": "daniel",
    "danny": "daniel", "mike": "michael", "jim": "james", "jimmy": "james",
    "steve": "steven", "stephen": "steven", "lou": "luis", "louis": "luis",
    "tom": "thomas", "dick": "richard", "rick": "richard", "ed": "edward",
    "ted": "edward", "jack": "john", "joe": "joseph", "harry": "harold",
    "hal": "harold", "carl": "karl", "greg": "gregory", "ron": "ronald",
    "sam": "samuel", "ben": "benjamin", "matt": "matthew", "chris": "christopher",
    "andy": "andrew", "drew": "andrew", "tony": "anthony", "larry": "lawrence",
    "jerry": "gerald", "jeff": "jeffrey", "ken": "kenneth", "pat": "patrick",
    "phil": "philip", "ray": "raymond", "dave": "david", "al": "albert",
    "fred": "frederick", "frank": "francis", "hank": "henry", "nick": "nicholas",
    "sean": "shaun", "jon": "jonathan", "rich": "richard", "richie": "richard",
    "bert": "albert", "walt": "walter", "gus": "augustus",
}


def _same_given(a, b):
    if a == b or _ed1(a, b):
        return True
    return NICKNAMES.get(a) == b or NICKNAMES.get(b) == a or (
        NICKNAMES.get(a) is not None and NICKNAMES.get(a) == NICKNAMES.get(b))


def build_index(board):
    nodes = []
    for n in board["people"] + board["entities"]:
        nodes.append({
            "id": n["id"],
            "label": n.get("label", ""),
            "cls": n.get("cls", ""),
            "tier": n.get("tier", ""),
            "aliases": aliases(n),
        })
    # Prose corpus: every free-text field a research pass could have written a
    # name into, keyed by node id so a hit can be attributed.
    #
    # THE FIRST VERSION READ FOUR FIELDS AND MISSED FIVE, and two independent
    # research passes caught it the expensive way -- by grepping the board
    # directly and finding names this tool had called ABSENT. Carl Sagan (in
    # claim text and timeline text), Randy Anderson (in entityInfo) and Douglas
    # Dean Johnson (13 hits) were all reported as leads the board had never
    # heard of. A false ABSENT sends someone after something already carried,
    # which is the one direction this tool must not be wrong in.
    #
    # So: everything with words in it. claims[].text is where most of the
    # board's actual assertions live, and it was not being read at all.
    prose = []
    for n in board["people"] + board["entities"]:
        for fld in ("narrative", "desc", "sub", "label", "tierRationale"):
            v = n.get(fld)
            if isinstance(v, str) and v:
                prose.append((n["id"], fld, v))
        for c in (n.get("claims") or []):
            if isinstance(c, dict) and isinstance(c.get("text"), str):
                prose.append((n["id"], "claim", c["text"]))
        for c in (n.get("chronology") or []):
            if isinstance(c, dict) and isinstance(c.get("event"), str):
                prose.append((n["id"], "chronology", c["event"]))
        for src in (n.get("sources") or []):
            if isinstance(src, dict) and isinstance(src.get("name"), str):
                prose.append((n["id"], "source", src["name"]))
    for eid, info in (board.get("entityInfo") or {}).items():
        if isinstance(info, dict):
            for fld, v in info.items():
                if isinstance(v, str) and len(v) > 20:
                    prose.append(("entityInfo." + eid, fld, v))
    for e in board["edges"]:
        for fld in ("label", "note", "desc"):
            v = e.get(fld)
            # edges are keyed a/b on this board, not s/t. The first cut used s/t,
            # so every edge hit printed its id as "None->None" -- harmless to the
            # verdict, useless to whoever has to go and look at it.
            if isinstance(v, str) and v:
                prose.append(("%s--%s" % (e.get("a"), e.get("b")), fld, v))
    for t in board["timeline"]:
        for fld in ("label", "title", "desc", "note", "text"):
            v = t.get(fld)
            if isinstance(v, str) and v:
                prose.append((t.get("id", "timeline"), fld, v))
    return nodes, prose


def _ed1(a, b):
    """True if a and b differ by at most one edit. Cheap, not Levenshtein."""
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        return sum(1 for x, y in zip(a, b) if x != y) == 1
    if la > lb:
        a, b, la, lb = b, a, lb, la
    for i in range(la + 1):          # b with one character removed
        if a == b[:i] + b[i + 1:]:
            return True
    return False


def near_spelling(ck, nk):
    """Same word count, every word within one edit, and something substantial.

    Auto-generated captions and hand-typed research notes both produce
    one-character name errors constantly -- the board writes `garry-nolan` and
    a transcript says "Gary Nolan". Treating those as two different people
    manufactures a lead out of a typo. Kept deliberately tight: same number of
    words, one edit each, and at least one word of five characters or more, so
    it cannot marry two short unrelated names.
    """
    if len(ck) != len(nk) or not ck:
        return False
    if max(len(w) for w in ck) < 5:
        return False
    diffs = 0
    for x, y in zip(ck, nk):
        if x == y:
            continue
        if not _ed1(x, y):
            return False
        diffs += 1
        if diffs > 1:
            return False
    return diffs == 1


def match_node(cand, nodes):
    ck = key(cand)
    if not ck:
        return None
    cs = set(ck)
    best = None
    cn = norm(cand)
    cks = _singular(ck)
    cn_s = _singular(tuple(cn.split()))
    for n in nodes:
        # id, parenthetical acronym, initials: the forms a speaker actually uses
        if cn in n.get("aliases", ()) or any(_singular(tuple(a.split())) == cn_s
                                             for a in n.get("aliases", ())):
            return (n, "alias")
        nk = key(n["label"])
        if not nk:
            continue
        if nk == ck or _singular(nk) == cks:
            return (n, "exact")
        # `Roswell Army Airfield` against `Roswell Army Air Field`: the same
        # letters with a space moved. Compare with spaces removed.
        if "".join(ck) == "".join(nk) or cn.replace(" ", "") in {a.replace(" ", "") for a in n.get("aliases", ())}:
            return (n, "spacing variant")
        # A person by given name and surname, where the given name is a nickname
        # or a caption spelling and the label may carry a middle name.
        if (n.get("cls") == "person" and len(ck) == 2 and len(nk) >= 2
                and len(ck[-1]) >= 4 and (ck[-1] == nk[-1] or _ed1(ck[-1], nk[-1]))
                and _same_given(ck[0], nk[0])):
            return (n, "given-name variant")
        ns = set(nk)
        # Containment, but only when the shorter side is at least two
        # discriminating words -- otherwise "brown" matches everything.
        if len(ck) >= 2 and cs <= ns:
            best = best or (n, "candidate within node")
        elif len(nk) >= 2 and ns <= cs and tuple(ck[:len(nk)]) == nk:
            # The node's words must LEAD the candidate. `Pease Air Force Base`
            # and `Spanish Air Force` both contain the key of `United States
            # Air Force` once the stopwords are gone, and both were reported
            # NODE -> usaf on 2 September 2026, which deleted two leads. A
            # false NODE is the silent direction; keep this rule to
            # `Lockheed Martin` leading `Lockheed Martin Skunk Works`.
            best = best or (n, "node within candidate")
        elif near_spelling(ck, nk):
            best = best or (n, "one character apart")
        elif (len(ck) >= 2 and len(nk) > len(ck) and max(len(w) for w in ck) >= 5
              and all(any(_ed1(x, y) for y in nk) for x in ck)
              # Short words must match exactly, one candidate word must match
              # exactly, and the surnames must be within one edit of each
              # other: `Ed Dames` was married to `James E. McDonald` (ed~e,
              # dames~james) on 2 September 2026 and the lead vanished.
              and all(len(x) >= 4 or x in nk for x in ck)
              and any(x in nk for x in ck if len(x) >= 3)
              and _ed1(ck[-1], nk[-1])):
            # "David Grush" against "David Charles Grusch": every candidate word
            # is within one edit of some label word, and the label is longer.
            # Caption spelling plus a middle name, which the plain containment
            # rule above cannot see and near_spelling refuses on word count.
            best = best or (n, "one character apart, within node")
    return best


def _prose_needles(cand):
    """The forms to look for in prose: the candidate, its nickname-expanded
    form (`Joe McMoneagle` -> `joseph mcmoneagle`), and a bare acronym of
    three letters or more, which the old four-character floor refused, so
    `FBI` came back ABSENT from a board that names the Bureau in prose."""
    needle = cand.lower().strip()
    out = []
    if re.fullmatch(r"[A-Z][A-Z0-9&]{2,5}", cand.strip()):
        out.append(("word", needle))
    if len(needle) >= 4:
        out.append(("sub", needle))
        words = needle.split()
        if len(words) == 2 and words[0] in NICKNAMES:
            out.append(("sub", NICKNAMES[words[0]] + " " + words[1]))
        # The stopword-stripped form: `US Department of State` was ABSENT while
        # `Department of State` sat in prose thirteen times (2 September 2026).
        stripped = " ".join(key(cand))
        if len(stripped) >= 8 and stripped != needle and len(stripped.split()) >= 2:
            out.append(("sub", stripped))
    return out


def match_prose(cand, prose, limit=3):
    needles = _prose_needles(cand)
    if not needles:
        return []
    hits = []
    for nid, fld, text in prose:
        low = text.lower()
        i = -1
        for kind, needle in needles:
            if kind == "word":
                m = re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", low)
                i = m.start() if m else -1
            else:
                i = low.find(needle)
            if i >= 0:
                break
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
    # The acronym and the id-as-words forms, which were the false ABSENTs of the
    # first Michels pass. Donors chosen at runtime so this cannot rot.
    acr_donor = next((n for n in nodes if re.search(r"\([A-Z]{3,}\)", n["label"])), None)
    if acr_donor:
        want(re.search(r"\(([A-Z]{3,})\)", acr_donor["label"]).group(1), "NODE",
             "the acronym in parentheses in a real label")
    else:
        fails.append("no node label carries a parenthetical acronym -- cannot test the alias channel")
    id_donor = next((n for n in nodes if n["cls"] == "person" and "-" in n["id"]
                     and norm(n["id"].replace("-", " ")) != norm(n["label"])), None)
    if id_donor:
        want(id_donor["id"].replace("-", " ").title(), "NODE", "a person id with the dash opened out")
    ini_donor = next((n for n in nodes if n["id"] in ("cia", "dia", "nsa", "nro", "doe")), None)
    if ini_donor:
        want(ini_donor["id"].upper(), "NODE", "the initials of a real label")
    # And the alias rule must not make a bare common word a node.
    office = classify(["Office"], nodes, prose)[0]
    if office["verdict"] == "NODE":
        fails.append("%-42s aliased to a node on a stopword alone (%s)" %
                     ("Office", office.get("node_label")))
    # Caption spelling plus a missing middle name must still find the node.
    if any(n["id"] == "david-grusch" for n in nodes):
        want("David Grush", "NODE", "caption spelling of a real label with a middle name")
    # A nickname for a real person node, chosen at runtime from the table.
    for n in nodes:
        if n.get("cls") != "person":
            continue
        lk = key(n["label"])
        if len(lk) >= 2 and len(lk[-1]) >= 5:
            short = next((s for s, full in NICKNAMES.items() if full == lk[0]), None)
            if short:
                want("%s %s" % (short.title(), lk[-1].title()), "NODE",
                     "a nickname for %s" % n["label"])
                # and the same nickname with an invented surname must NOT match
                want("%s Zzyzxington" % short.title(), "ABSENT",
                     "a nickname alone must not carry a wrong surname to a node")
                break
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

    # COVERAGE. The defect this tool shipped with was not a wrong verdict, it
    # was a corpus that did not include the board's own claim text. Assert the
    # index actually reaches each field family, so removing one shows up here
    # rather than as a false ABSENT in somebody's research pass.
    seen_fields = set(f for _, f, _ in prose)
    for want in ("narrative", "claim", "chronology", "source", "text"):
        if want not in seen_fields:
            fails.append("the prose index never reached any %r field" % want)
    if not any(i.startswith("entityInfo.") for i, _, _ in prose):
        fails.append("the prose index never reached entityInfo")
    # The one-edit rule must fire, and must NOT fire on two different people.
    r = classify(["Gary Nolan"], nodes, prose)[0]
    if r["verdict"] != "NODE":
        fails.append("%-42s expected NODE (board writes Garry Nolan) got %s" % ("Gary Nolan", r["verdict"]))
    # Two genuinely different surnames of the same length must stay apart.
    if near_spelling(key("Bob Green"), key("Bob Brown")):
        fails.append("the one-edit rule married two unrelated surnames")
    if near_spelling(key("Al Roe"), key("Al Doe")):
        fails.append("the one-edit rule fired with no substantial word")

    # The Area 52 triage of 2 September 2026: two false NODEs and four false
    # ABSENTs, each rule shown firing and shown refusing.
    for name, bad in (("Pease Air Force Base", "usaf"), ("Spanish Air Force", "usaf"),
                      ("Ed Dames", "james-e-mcdonald")):
        m = match_node(name, nodes)
        if m and m[0]["id"] == bad:
            fails.append("%-42s still reported NODE -> %s (a false NODE deletes a lead)" % (name, bad))
    m = match_node("Lockheed Martin Skunk Works", nodes)
    if not m:
        fails.append("the leading-words containment rule no longer matches Lockheed Martin Skunk Works")
    if match_node("David Grush", nodes) is None:
        fails.append("the caption-plus-middle-name rule no longer matches David Grush")
    for name, want_id in (("PRP", "prp-nuclear-weapon"), ("UK MOD", "uk-mod"),
                          ("Rich Dolan", "richard-dolan")):
        m = match_node(name, nodes)
        if not m or m[0]["id"] != want_id:
            fails.append("%-42s expected NODE %s got %s" % (name, want_id, m[0]["id"] if m else None))
    if match_node("QQZ", nodes):
        fails.append("the run-initials alias matched an acronym no label yields")
    r = classify(["FBI"], nodes, prose)[0]
    if r["verdict"] == "ABSENT":
        fails.append("FBI reported ABSENT; the board names the Bureau in prose")
    r = classify(["ZZQ"], nodes, prose)[0]
    if r["verdict"] != "ABSENT":
        fails.append("ZZQ, an acronym nothing carries, got %s" % r["verdict"])
    r = classify(["Joe McMoneagle"], nodes, prose)[0]
    if r["verdict"] == "ABSENT":
        fails.append("Joe McMoneagle reported ABSENT; the board writes Joseph McMoneagle")
    # Area 52 triage group 6: `Operation Moon Dust` against `Project MOON DUST`,
    # and `US Department of State` against thirteen prose mentions.
    m = match_node("Operation Moon Dust", nodes)
    if not m or m[0]["id"] != "project-moon-dust":
        fails.append("Operation Moon Dust expected NODE project-moon-dust got %s" % (m[0]["id"] if m else None))
    if match_node("Operation Zzyzx", nodes):
        fails.append("the operation/project equivalence matched an invented operation")
    r = classify(["US Department of State"], nodes, prose)[0]
    if r["verdict"] == "ABSENT":
        fails.append("US Department of State reported ABSENT; the board writes Department of State in prose")
    r = classify(["US Department of Zzyzx"], nodes, prose)[0]
    if r["verdict"] != "ABSENT":
        fails.append("US Department of Zzyzx, which nothing carries, got %s" % r["verdict"])

    # And three names that were reported ABSENT before the fix must not be now.
    for name in ("Carl Sagan", "Douglas Dean Johnson"):
        got = classify([name], nodes, prose)[0]["verdict"]
        if got == "ABSENT":
            fails.append("%-42s reported ABSENT; the board names it in prose" % name)

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
