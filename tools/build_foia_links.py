"""Derive the node -> FOIA request linkage from notes/FOIA-LETTERS-2026-08-29.md.

Stewart, 29 August 2026: "The FOIA will have to happen way later but keep them
there and ready. In fact integrate them into the board somehow."

THE LINKAGE IS ALREADY IN THE DATA and has been since the letters were written.
Every F-section carries a `**Closes on the board.**` line naming the nodes and the
numbered open questions it would close -- F1 alone names fourteen across eight nodes.
This reads those lines and turns them into `data/foia-links.json`.

GENERATED, NOT AUTHORED, and that is the whole point. The letters are themselves
generated from `notes/REQUEST-QUEUE.md` so the two cannot drift; deriving this from
the letters extends the same chain to the board. A hand-kept third copy of the
mapping is a third thing to keep in step, and this repo has already paid for that
kind of drift twice.

Run it after editing the letters:

    python tools/build_foia_links.py

It is a step of tools/build.py too, after merge (it reads data/the-program.json
and the entity dossiers through tools/dossiers.py; until phase 11 it read both out
of data/l0-model.json) and before build_app_data (which reads what it writes), so
a stale file cannot ship. It exits non-zero when a letter names a node or a question the board does
not have.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETTERS = os.path.join(ROOT, "notes", "FOIA-LETTERS-2026-08-29.md")
OUT = os.path.join(ROOT, "data", "foia-links.json")
BOARD = os.path.join(ROOT, "data", "the-program.json")

# `# F1. NARA - the RG 615 compliance register`
_HEAD = re.compile(r"^#\s+(F\d+)\.\s+(.+?)\s*$", re.M)
# `**Send to.** National Archives and Records Administration, FOIA Officer, ...`
_SEND = re.compile(r"^\*\*Send to\.\*\*\s+(.+?)\s*$", re.M)
# `**Closes on the board.** `a` Q0, Q1; `b` Q2. That is fourteen ...`
_CLOSES = re.compile(r"^\*\*Closes on the board\.\*\*\s+(.+?)\s*$", re.M)
_ID = re.compile(r"`([a-z0-9][a-z0-9-]*)`")
_Q = re.compile(r"Q(\d+)")
# A CLAIM CAN BE WEAKER THAN "CLOSES", and the letters say so in prose:
# "partially Q3", "and materially advances Q6 and Q11". Whether a request CLOSES a
# question or merely bears on it is exactly the distinction this board grades, so
# the two are kept apart rather than flattened together.
_WEAK = re.compile(r"\b(partially|materially advances|advances|bears on)\b", re.I)


def parse(text):
    """Every F-section, with the agency it goes to and what it would close."""
    heads = list(_HEAD.finditer(text))
    out = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[start:end]
        send = _SEND.search(body)
        closes = _CLOSES.search(body)
        rid, title = m.group(1), m.group(2)
        # The GAO section is prose about why it is NOT a FOIA request. It has no
        # `Closes on the board` line and must not be invented one.
        if not closes:
            continue
        line = closes.group(1)
        nodes, cur = [], None
        # Semicolons separate the clauses; a clause that names no id continues the
        # one before it, which is how "partially Q3" attaches to the node it follows.
        for seg in line.split(";"):
            m_id = _ID.search(seg)
            if m_id:
                cur = {"node": m_id.group(1), "questions": [], "partial": []}
                nodes.append(cur)
            if cur is None:
                continue
            w = _WEAK.search(seg)
            cut = w.start() if w else len(seg)
            for qm in _Q.finditer(seg):
                q = int(qm.group(1))
                (cur["partial"] if qm.start() >= cut else cur["questions"]).append(q)
        for n in nodes:
            n["partial"] = sorted(set(n["partial"]))
            n["questions"] = sorted(set(n["questions"]) - set(n["partial"]))

        # NOTHING MAY BE DROPPED IN SILENCE. The first cut of this parser matched
        # `id` followed by a run of Q-numbers and stopped at the first word it did
        # not expect -- so "partially Q3" on F3, "materially advances Q6 and Q11" on
        # F4 and "partially Q1" on F16 were read, discarded, and reported as a clean
        # parse of 117 links. That is the shape of every defect in CLAUDE.md section
        # 5: a pass that succeeds while not doing its job. So every Q-number in the
        # line is counted and the total must match what was attributed.
        seen = sum(len(n["questions"]) + len(n["partial"]) for n in nodes)
        total = len(_Q.findall(line))
        if seen != total:
            raise SystemExit(
                "build_foia_links: %s names %d question numbers and %d were "
                "attributed to a node. Something in that line is a shape this "
                "parser does not read, and dropping it silently is how a request "
                "stops closing a question nobody notices.\n  %s"
                % (rid, total, seen, line))
        # THE SHORT AGENCY COMES FROM THE HEADING, not from the postal address.
        # `**Send to.**` gives the mailing destination -- "Office of the Secretary of
        # Defense / Joint Staff FOIA Requester Service Center (FOID)" -- which is
        # what a letter needs and roughly four times what a chip on a dossier line
        # can carry. The heading already names the agency in the form a reader wants:
        # "F3. OSD - the YANKEE BLUE remand search result". Take that, and keep the
        # full destination for the chip's tooltip.
        short = re.split(r"\s+[-\u2013\u2014]\s+", title, maxsplit=1)[0].strip()
        out.append({
            "id": rid,
            "title": title,
            "agency": short,
            "sendTo": (send.group(1).strip() if send else ""),
            "status": "not filed",
            "nodes": nodes,
        })
    return out


def build():
    if not os.path.exists(LETTERS):
        raise SystemExit("build_foia_links: notes/FOIA-LETTERS-2026-08-29.md is missing")
    with open(LETTERS, encoding="utf-8") as fh:
        requests = parse(fh.read())
    if not requests:
        raise SystemExit("build_foia_links: no request sections parsed. The letters "
                         "file changed shape and this parser now reads nothing, "
                         "which would ship as 'no request closes anything'.")

    # The inverse index, which is what a dossier needs: node -> the requests that
    # would close its questions, and which ones.
    by_node = {}
    for r in requests:
        for n in r["nodes"]:
            row = by_node.setdefault(n["node"], [])
            row.append({"request": r["id"], "agency": r["agency"], "title": r["title"],
                        "sendTo": r["sendTo"], "status": r["status"],
                        "questions": n["questions"], "partial": n["partial"]})

    # WHAT RESOLVES AND WHAT DOES NOT, recorded rather than dropped. A node named in
    # a letter that is not on the board is a real finding -- either the letter names
    # something this board does not carry, or the node was renamed and the letters
    # went stale. Silently dropping it would hide both.
    #
    # A node is known when it is on the board. The question numbers index the
    # node's ENTITY DOSSIER's open questions (the node page prints them from
    # there), so a board node with no dossier has none, and any Q it is named with
    # is out of range. Until phase 11 both came out of data/l0-model.json, whose
    # `dossiers` held exactly what tools/dossiers.py loads.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import dossiers  # noqa: E402
    known, oq = set(), {}
    if os.path.exists(BOARD):
        with open(BOARD, encoding="utf-8") as fh:
            b = json.load(fh)
        known = {n["id"] for n in b["people"] + b["entities"]}
    for nid, d in dossiers.load_dossiers().items():
        oq[nid] = len(d.get("openQuestions") or [])

    unresolved, overrun = [], []
    for nid, rows in sorted(by_node.items()):
        if known and nid not in known:
            unresolved.append(nid)
            continue
        n = oq.get(nid, 0)
        for row in rows:
            for q in row["questions"] + row["partial"]:
                if q >= n:
                    overrun.append(f"{nid} Q{q} ({row['request']}) — that node has "
                                   f"{n} open question(s)")

    payload = {
        "_what": "node -> FOIA request linkage, DERIVED from notes/FOIA-LETTERS-2026-08-29.md "
                 "by tools/build_foia_links.py. Do not hand-edit: edit the letters, or "
                 "notes/REQUEST-QUEUE.md which the letters are generated from, and re-run.",
        "_status": "None of these requests has been filed. Stewart, 29 August 2026: "
                   "'The FOIA will have to happen way later but keep them there and ready.'",
        "source": "notes/FOIA-LETTERS-2026-08-29.md",
        "requests": requests,
        "byNode": by_node,
        "unresolved": sorted(set(unresolved)),
        "outOfRange": overrun,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return payload


if __name__ == "__main__":
    p = build()
    nq = sum(len(n["questions"]) + len(n["partial"])
             for r in p["requests"] for n in r["nodes"])
    print(f"  {len(p['requests'])} requests · {len(p['byNode'])} nodes · "
          f"{nq} open questions linked -> data/foia-links.json")
    if p["unresolved"]:
        print(f"  !! {len(p['unresolved'])} node id(s) named in the letters are not on "
              f"the board: {', '.join(p['unresolved'])}", file=sys.stderr)
    if p["outOfRange"]:
        print(f"  !! {len(p['outOfRange'])} question index(es) out of range:",
              file=sys.stderr)
        for x in p["outOfRange"][:10]:
            print(f"       {x}", file=sys.stderr)
    # A letter naming a node or a question the board does not have is a build
    # failure, as it was when this ran inside build_dashboard.py: a dossier would
    # point at a request that no longer closes anything.
    sys.exit(1 if (p["unresolved"] or p["outOfRange"]) else 0)
