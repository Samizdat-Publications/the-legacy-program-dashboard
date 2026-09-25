#!/usr/bin/env python3
"""topic_packet.py: everything a phase 5 drafter may use for one topic, and nothing else.

    python tools/topics/topic_packet.py <topic-id>              print the packet (markdown)
    python tools/topics/topic_packet.py <topic-id> --out FILE   write it to FILE
    python tools/topics/topic_packet.py --all DIR               one DIR/<id>.md per topic
    python tools/topics/topic_packet.py --node <node-id>        one node in full: every
                                                                claim, the whole description

Read from the BUILT board (data/the-program.json) and the committed proposals
(research/topics/_proposals.json), never paraphrased: every claim is printed with its
id, tier, text and source exactly as the board carries it, every edge with its id,
type, tier, label, sentence and sources. A drafter cites these ids and nothing else
(notes/plans/P5-drafting-topics.md). Run tools/build.py first; a packet printed from a
stale board cites ids the gate will not find.

What goes in: the stub; its proposals above propose_members.py's threshold with their
signals, strongest first (at most MAX_CANDIDATES), and the near misses by id; the
claims of the domain nodes the topic absorbs and of its unplaced claims, with the ids
they are cited by; each candidate's label, class, dates, description, claims and case
against (conflicts, unverified notes, open questions); and every edge whose two ends
are both printed candidates or absorbed nodes.

THE SIZE LIMIT. A packet is held under LIMIT bytes by printing low-scoring candidates
in less detail, lowest first, and saying so on each one and in the table: `full`
(every claim, description to DESC_CAP characters), then `reduced` (the first
REDUCED_CLAIMS claims, a short description), then `brief` (the header and a count of
what `--node` would print). Anchors are reduced only after every other candidate is
brief, and only then are the lowest candidates dropped (listed by id and score). A
claim that is not printed can still be cited: `--node <id>` prints it with its id.

Not part of the build and not committed output: packets are working papers.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import topiclib  # noqa: E402
from topiclib import ROOT, TOPICS_DIR  # noqa: E402

BOARD = os.path.join(ROOT, "data", "the-program.json")
PROPOSALS = os.path.join(TOPICS_DIR, "_proposals.json")
VOCAB = os.path.join(ROOT, "schema", "vocab.json")
MAX_CANDIDATES = 80
LIMIT = 150_000          # bytes of UTF-8
DESC_CAP = 1500          # characters of a node's description, in full detail
DESC_SHORT = 300         # characters, in reduced detail
REDUCED_CLAIMS = 5
FULL, REDUCED, BRIEF, DROPPED = 0, 1, 2, 3
LEVEL_NAME = {FULL: "full", REDUCED: "reduced", BRIEF: "brief", DROPPED: "dropped"}


RULES = """\
## The rules (notes/plans/P5-drafting-topics.md)

- Cite ids from this packet only: claim ids (`c-...`) and edge ids (`e-...`). Every
  `lead`, `summary`, `record`, `claimed` and `contested` item cites at least one.
- Paraphrase only what the cited claims and edges say. No outside facts, no URLs.
- A quotation in double quotes must appear verbatim in a claim or edge the same item cites.
- `record` is what the documents show: each item cites at least one Tier 1 claim or
  Tier 1 edge. Testimony is Tier 2, is called testimony, and goes in `claimed`.
- The case against, and disagreements between records, go in `contested`.
- A member is included only if a cited item or an edge ties it to the topic. A cited
  claim sits on a member (or on an absorbed domain node, or is an unplaced claim
  below); a cited edge joins two members.
- At least 6 members unless the stub carries `researchGap`. `related` names topic ids.
- `questions` are open questions in the topic's own words, cite-free.
- No em dashes. Set `status` to "drafted".
- A candidate printed `reduced` or `brief` has more on the board than is shown here:
  `python tools/topics/topic_packet.py --node <id>` prints all of it, with its ids.
"""


def rd(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def dates(n):
    if n.get("cls") == "person":
        return n.get("date") or "undated"
    a, b = n.get("dateStart"), n.get("dateEnd")
    if a and b and a != b:
        return "%s to %s" % (a, b)
    return a or b or "undated"


def one_line(s):
    return " ".join(str(s or "").split())


def cap(s, n):
    s = one_line(s)
    if len(s) <= n:
        return s
    return s[:n] + " [... cut at %d characters by the packet; --node prints it all]" % n


def src_line(srcs):
    out = []
    for x in srcs or []:
        if isinstance(x, dict):
            bits = [one_line(x.get("name"))] if x.get("name") else []
            if x.get("url"):
                bits.append("<%s>" % x["url"])
            if x.get("date"):
                bits.append("(%s)" % x["date"])
            out.append(" ".join(bits) or "(empty source record)")
        else:
            out.append(one_line(x))
    return "; ".join(out) or "no source recorded"


def claim_line(c):
    return ("- `%s` Tier %s: %s  \n  Source: %s"
            % (c.get("id"), c.get("tier"), one_line(c.get("text")),
               one_line(c.get("source")) or "none recorded"))


def against_lines(n):
    out = []
    for key, head in (("conflicts", "Conflicts"), ("unverified", "Unverified"),
                      ("openQuestions", "Open questions")):
        xs = n.get(key) or []
        if xs:
            out.append("%s:" % head)
            out += ["- %s" % one_line(x if not isinstance(x, dict)
                                      else json.dumps(x, ensure_ascii=False)) for x in xs]
    return out


def node_block(k, n, score, signals, is_anchor, level=FULL, desc_cap=DESC_CAP):
    claims = n.get("claims") or []
    head = "### %s%s (`%s`)" % ("%d. " % k if k else "", one_line(n.get("label")), n["id"])
    meta = "%s, %s, node tier %s, score %s%s%s" % (
        n.get("cls"), dates(n), n.get("tier"), score, ", ANCHOR" if is_anchor else "",
        "" if level == FULL else ", printed %s" % LEVEL_NAME[level])
    lines = [head, "", meta, ""]
    if signals is not None and level != BRIEF:
        lines += ["Signals: `%s`" % json.dumps(signals, ensure_ascii=False, sort_keys=True), ""]
    if n.get("sub"):
        lines.append("Sub: %s" % one_line(n["sub"]))
    if level == BRIEF:
        ag = sum(len(n.get(k2) or []) for k2 in ("conflicts", "unverified", "openQuestions"))
        lines += ["%d claims (Tier 1: %d), %d notes against; not printed here: "
                  "`--node %s` prints them." % (len(claims),
                                               sum(1 for c in claims if c.get("tier") == 1),
                                               ag, n["id"]), ""]
        return lines
    desc = n.get("desc") or n.get("narrative")
    if desc:
        lines.append("Description: %s" % cap(desc, desc_cap if level == FULL else DESC_SHORT))
    lines.append("")
    shown = claims if level == FULL else claims[:REDUCED_CLAIMS]
    if shown:
        lines += ["Claims:"] + [claim_line(c) for c in shown]
        if len(shown) < len(claims):
            lines.append("- (%d more claims on the node, not printed: `--node %s`)"
                         % (len(claims) - len(shown), n["id"]))
    else:
        lines.append("Claims: none on the board.")
    ag = against_lines(n)
    if ag:
        lines += [""] + ag
    lines.append("")
    return lines


def edge_block(bd, e):
    la = one_line((bd.nodes.get(e["a"]) or {}).get("label"))
    lb = one_line((bd.nodes.get(e["b"]) or {}).get("label"))
    return ["- `%s` %s (`%s`) -> %s (`%s`); type %s; Tier %s; label: %s  \n"
            "  Sentence: %s  \n  Sources: %s"
            % (e.get("id"), la, e["a"], lb, e["b"], e.get("type"), e.get("claimTier"),
               one_line(e.get("label")) or "(none)",
               one_line(e.get("note")) or "(no sentence recorded for this link)",
               src_line(e.get("sources")))]


class Packet(object):
    """One topic's packet, rendered at a given level of detail per candidate."""

    def __init__(self, t, prop, bd, roles, threshold):
        self.t, self.prop, self.bd, self.roles, self.threshold = t, prop, bd, roles, threshold
        self.anchors = set(t.get("anchors") or [])
        self.absorbs = list(t.get("absorbs") or [])
        cands = sorted(prop.get("members") or [], key=lambda m: (-m[1], m[0]))
        self.cands = cands[:MAX_CANDIDATES]
        self.over_max = cands[MAX_CANDIDATES:]
        self.near = sorted(prop.get("near") or [], key=lambda m: (-m[1], m[0]))
        self.level = {m[0]: FULL for m in self.cands}
        self._blocks = {}

    def block(self, k, m):
        key = (m[0], self.level[m[0]], k)
        if key not in self._blocks:
            n = self.bd.nodes.get(m[0])
            if n is None:
                lines = ["### %d. `%s`: not on the board (stale proposals; rebuild)" % (k, m[0]), ""]
            else:
                lines = node_block(k, n, m[1], m[2], m[0] in self.anchors, self.level[m[0]])
            self._blocks[key] = "\n".join(lines)
        return self._blocks[key]

    def render(self):
        t = self.t
        sp = t.get("span") or {}
        L = ["# Topic packet: %s" % t["id"], "",
             "**%s** (kind %s, section %s, span %s to %s, focus era %s, status %s)"
             % (t.get("title"), t.get("kind"), t.get("section"), sp.get("from"), sp.get("to"),
                t.get("focusEra"), t.get("status")), "",
             "Printed by tools/topics/topic_packet.py from data/the-program.json and "
             "research/topics/_proposals.json. Everything below is the board's own text.", "",
             RULES,
             "Roles (schema/vocab.json topicRoles): " + ", ".join("`%s`" % r for r in self.roles), "",
             "## The stub", "", "```json", json.dumps(t, ensure_ascii=False, indent=1), "```", ""]
        if t.get("researchGap"):
            L += ["**Research gap:** %s" % one_line(t["researchGap"]), ""]

        kept = [m for m in self.cands if self.level[m[0]] != DROPPED]
        dropped = [m for m in self.cands if self.level[m[0]] == DROPPED] + self.over_max
        counts = {v: sum(1 for m in kept if self.level[m[0]] == v) for v in (FULL, REDUCED, BRIEF)}
        L += ["## Proposed members, strongest first", "",
              "%d candidates above the threshold of %s; %d printed (%d in full, %d reduced, "
              "%d brief)." % (len(self.prop.get("members") or []), self.threshold, len(kept),
                              counts[FULL], counts[REDUCED], counts[BRIEF]), ""]
        if counts[REDUCED] or counts[BRIEF]:
            L += ["**Cut to fit %d KB:** the lowest-scoring candidates are printed in less "
                  "detail; `--node <id>` prints any of them in full." % (LIMIT // 1000), ""]
        if dropped:
            L += ["**Left out:** %d candidates, lowest scores: %s"
                  % (len(dropped), ", ".join("`%s` (%s)" % (m[0], m[1]) for m in dropped)), ""]
        L += ["| # | id | score | printed | signals |", "|---|---|---|---|---|"]
        for k, m in enumerate(kept, 1):
            L.append("| %d | `%s` | %s | %s | %s |" % (k, m[0], m[1], LEVEL_NAME[self.level[m[0]]],
                                                      ", ".join(sorted(m[2]))))
        L.append("")
        if self.near:
            L += ["Near misses (below the threshold, not printed; a member only if a cited "
                  "item ties it in): " + ", ".join("`%s` (%s)" % (m[0], m[1]) for m in self.near), ""]

        if self.absorbs:
            L += ["## Absorbed domain nodes", "",
                  "Their claims are the topic's own and may be cited.", ""]
            for i in self.absorbs:
                n = self.bd.nodes.get(i)
                if n:
                    L += node_block(0, n, "absorbed", None, False)
        up = topiclib.unplaced(t)
        if up:
            L += ["## Unplaced claims", "",
                  "Claims phase 3 could not place on a node. Cite them by these ids.", ""]
            for cid, c in up.items():
                L.append("- `%s` Tier %s (collapsed into `%s`): %s  \n  Source: %s"
                         % (cid, c.get("tier"), c.get("collapsedInto"), one_line(c.get("claim")),
                            one_line(c.get("source"))))
            L.append("")

        L += ["## Candidates", ""]
        for k, m in enumerate(kept, 1):
            L.append(self.block(k, m))

        ends = {m[0] for m in kept} | set(self.absorbs)
        rank = {m[0]: k for k, m in enumerate(kept)}
        es = [e for e in self.bd.edges.values()
              if e["a"] in ends and e["b"] in ends and e["a"] != e["b"]]
        es.sort(key=lambda e: (min(rank.get(e["a"], 999), rank.get(e["b"], 999)),
                               max(rank.get(e["a"], 999), rank.get(e["b"], 999)), e["id"]))
        L += ["## Edges among the printed candidates and absorbed nodes (%d)" % len(es), ""]
        for e in es:
            L += edge_block(self.bd, e)
        L.append("")
        return "\n".join(L)

    def fit(self):
        """Degrade detail, lowest score first, until the packet fits. The schedule:
        non-anchors to reduced, then to brief; anchors to reduced; non-anchors
        dropped; anchors to brief."""
        md = self.render()
        order = [m[0] for m in reversed(self.cands)]          # lowest score first
        plain = [i for i in order if i not in self.anchors]
        anch = [i for i in order if i in self.anchors]
        steps = ([(i, REDUCED) for i in plain] + [(i, BRIEF) for i in plain] +
                 [(i, REDUCED) for i in anch] + [(i, DROPPED) for i in plain] +
                 [(i, BRIEF) for i in anch])
        for i, lv in steps:
            if len(md.encode("utf-8")) <= LIMIT:
                break
            self.level[i] = lv
            md = self.render()
        size = len(md.encode("utf-8"))
        if size > LIMIT:
            md += ("\n**Still over %d KB with every candidate brief or left out; the edges "
                   "are printed in full.**\n" % (LIMIT // 1000))
        return md


def packet(tid, bd, props, roles):
    """(markdown, bytes, candidates not printed in full) for one topic."""
    p = os.path.join(TOPICS_DIR, tid + ".json")
    if not os.path.exists(p):
        raise SystemExit("no topic %r in research/topics" % tid)
    t = rd(p)
    prop = (props.get("topics") or {}).get(tid) or {"members": []}
    pk = Packet(t, prop, bd, roles, (props.get("method") or {}).get("threshold"))
    md = pk.fit()
    cut = sum(1 for v in pk.level.values() if v != FULL) + len(pk.over_max)
    return md, len(md.encode("utf-8")), cut


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("topic", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--all", metavar="DIR")
    ap.add_argument("--node", metavar="ID")
    a = ap.parse_args()
    if not a.topic and not a.all and not a.node:
        ap.error("name a topic id, or --all DIR, or --node ID")
    bd = topiclib.Board(rd(BOARD))
    if a.node:
        n = bd.nodes.get(a.node)
        if n is None:
            raise SystemExit("no node %r on the board" % a.node)
        es = [e for e in bd.edges.values() if a.node in (e["a"], e["b"])]
        md = "\n".join(node_block(0, n, "n/a", None, False, FULL, desc_cap=10 ** 9)
                       + ["## Edges (%d)" % len(es), ""]
                       + [x for e in sorted(es, key=lambda e: e["id"]) for x in edge_block(bd, e)]) + "\n"
    else:
        props = rd(PROPOSALS)
        roles = [r["id"] for r in rd(VOCAB).get("topicRoles") or []]
    if a.all:
        os.makedirs(a.all, exist_ok=True)
        sizes = []
        for f in topiclib.stub_files():
            tid = f[:-5]
            md, size, cut = packet(tid, bd, props, roles)
            with open(os.path.join(a.all, tid + ".md"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(md)
            sizes.append((size, tid, cut))
        sizes.sort()
        print("wrote %d packets to %s: median %d KB, largest %s at %d KB; %d with candidates "
              "cut to fit" % (len(sizes), a.all, sizes[len(sizes) // 2][0] // 1000,
                              sizes[-1][1], sizes[-1][0] // 1000,
                              sum(1 for s in sizes if s[2])))
        return 0
    if not a.node:
        md, size, cut = packet(a.topic, bd, props, roles)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(md)
        print("wrote %s: %d bytes" % (a.out, len(md.encode("utf-8"))))
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
