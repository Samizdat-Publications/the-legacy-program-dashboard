#!/usr/bin/env python3
"""
verify.py — assert things about the board that a human would otherwise have to notice.

WHY THIS EXISTS
---------------
On 2026-08-12 a QA pass found four BROKEN-severity defects in a board that had been
"verified". Every one of them was invisible to the verification that existed:

  * 35 dates were replaced with null on every rebuild        -> valid JSON, no error
  * five people were on the board twice, one rendering
    its own slug as its display name                          -> valid nodes, no error
  * thirteen person plates read "JR., J." or "(SAM), '."      -> rendered fine, just wrong
  * the DETAIL panel stated the wrong number of classes       -> rendered fine, just false

The verification was `shoot.js`: screenshot the views, collect console errors, report
zero. That checks *that nothing threw*. None of these threw. A board can be completely
wrong and completely quiet.

Worse, the one check `shoot.js` had that could have caught something real — `canvasInk`,
meant to catch a blank canvas — was itself broken. It reported 0 ink on a canvas that was
visibly drawing, because the renderer is WebGL and `getImageData` returns empty without
`preserveDrawingBuffer`. It had never once failed, and nobody noticed, because a check
that always passes and a check that always says zero look identical from the outside.

So this file follows two rules:

  1. EVERY CHECK ASSERTS A FACT, and fails the build with a non-zero exit when the fact
     is false. Reporting is not verifying.
  2. EVERY CHECK IS ITSELF TESTED. `--self-test` feeds each check input it must reject.
     A check that cannot be shown to fail is not evidence of anything. This is the
     direct lesson of canvasInk and it is not optional.

Usage:
    python3 tools/verify.py                # assert the current build
    python3 tools/verify.py --self-test    # prove every check can fail
    python3 tools/verify.py --update-golden  # deliberately accept new counts
"""

import json, os, re, sys, subprocess, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from merge import canonical_id  # noqa: E402

BOARD = os.path.join(ROOT, "data", "the-program.json")
DIST = os.path.join(ROOT, "dist", "the-program.html")
GOLDEN = os.path.join(ROOT, "tools", "GOLDEN.json")

FAILURES = []
CHECKS_RUN = []


def check(name):
    """Register a check. The body returns a list of problem strings; empty means pass."""
    def deco(fn):
        CHECKS_RUN.append((name, fn))
        return fn
    return deco


# ---------------------------------------------------------------------------
# structural invariants — these are properties, not counts. They must hold at
# any size, so they never need updating as the research grows.
# ---------------------------------------------------------------------------

@check("ids are canonical")
def _ids_canonical(b, html):
    """Two spellings of one id put the same person on the board twice, split their
    edges and sources, and — because label falls back to the id — make the twin
    render its own slug as its name. This is exactly what happened to
    p-dylan-borland / dylan-borland."""
    bad = []
    seen = {}
    for n in b["people"] + b["entities"]:
        i = n["id"]
        if canonical_id(i) != i:
            bad.append(f"non-canonical id {i!r} (should be {canonical_id(i)!r})")
        seen.setdefault(canonical_id(i), []).append(i)
    for canon, spellings in seen.items():
        if len(spellings) > 1:
            bad.append(f"{len(spellings)} ids collapse to {canon!r}: {spellings}")
    return bad


@check("no label is its own id")
def _label_not_id(b, html):
    """merge.py falls back to the id when a record has no label. That fallback
    reaching the screen means a record was invented rather than merged."""
    return [f"{n['id']} displays its own slug as its name"
            for n in b["people"] + b["entities"] if n.get("label") == n["id"]]


@check("person plate names are meaningful")
def _plate_names(b, html):
    """The plate shows `SURNAME, F.`. A label whose last token is a generational
    suffix rendered five different people as 'JR., J.'. Reproduces the shipped
    formatter's contract rather than trusting it."""
    SUFFIX = re.compile(r"^(jr|sr|ii|iii|iv|v|phd|md|esq|ret)\.?$", re.I)
    TITLE = re.compile(r"^(dr|mr|mrs|ms|prof|maj|gen|col|lt|capt|cmdr|cdr|adm|sgt|rep|sen|hon|brig|gral|general|de|brigada|aérea)\.?$", re.I)
    bad = []
    for p in b["people"]:
        parts = re.sub(r"\([^)]*\)", " ", re.sub(r"[“”‘’\"']", "", p["label"])).split()
        while len(parts) > 1 and SUFFIX.match(parts[-1]):
            parts.pop()
        while len(parts) > 1 and TITLE.match(parts[0]):
            parts.pop(0)
        if not parts:
            bad.append(f"{p['id']}: label {p['label']!r} reduces to nothing")
            continue
        short = (parts[-1] + (", " + parts[0][0] + "." if len(parts) > 1 else "")).upper()
        if SUFFIX.match(parts[-1]) or not re.match(r"^[A-ZÀ-ž]", short):
            bad.append(f"{p['id']}: {p['label']!r} -> {short!r}")
    return bad


@check("no dangling references")
def _dangling(b, html):
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for e in b["edges"]:
        for side in ("a", "b"):
            if e[side] not in ids:
                bad.append(f"edge {e['a']}->{e['b']} references missing {e[side]!r}")
    for t in b.get("timeline", []):
        if t.get("node") and t["node"] not in ids:
            bad.append(f"timeline {t.get('id')} references missing node {t['node']!r}")
        if t.get("ref") and t["ref"] not in ids:
            bad.append(f"timeline {t.get('id')}.ref references missing {t['ref']!r}")
        for f in ("entities", "nodes", "refs"):
            for x in t.get(f) or []:
                if x not in ids:
                    bad.append(f"timeline {t.get('id')}.{f} references missing {x!r}")
    return bad[:40]


@check("every person back-reference resolves")
def _person_refs(b, html):
    """A person points at nodes through locId, instId and domains, and deriveEdges()
    turns each one into a live edge at runtime. These are references exactly as much
    as an edge endpoint is, and until this check existed nothing walked them.

    That gap shipped. When 30 location nodes were removed under the approved
    deletion list, the removal dropped the edges that touched them -- because the
    dangling check walked edge endpoints, and satisfying the gate defined the scope
    of the fix. The 31 person.locId back-references pointing at those same nodes
    survived, and the board emitted 31 geographic edges to locations that no longer
    existed. Nothing threw, and 'no dangling references' reported ok on every run."""
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for p in b["people"]:
        for f in ("locId", "instId"):
            if p.get(f) and p[f] not in ids:
                bad.append(f"person {p['id']}.{f} references missing {p[f]!r}")
        for d in p.get("domains") or []:
            if d not in ids:
                bad.append(f"person {p['id']}.domains references missing {d!r}")
    return bad[:40]


@check("no unapproved duplicate nodes")
def _duplicates(b, html):
    """One object recorded twice is worse than one recorded not at all: both copies
    look sourced, each holds a fraction of the evidence, and they can carry
    different tiers, so the board grades the same thing two ways at once.

    Five people were on this board twice in August. That was fixed by unifying the
    id rules for people, and nothing ever checked the entities. On 22 August the
    FY2024 NDAA sec. 1687 was here three times, the AARO FY2025 annual report three
    times, and Jesse Marcel twice -- nine groups, 19 nodes, splitting about 70 edges
    and 130 claims.

    This computes the groups from the board itself rather than reading merge.py's
    INTEGRITY.json, so it is a property of what shipped and can be self-tested.
    Pairs that genuinely are not duplicates go in tools/DUPLICATES_ACCEPTED.json
    with a reason saying what distinguishes them -- the same deliberate-acceptance
    pattern as the golden manifest. Anything unlisted fails."""
    from merge import duplicate_groups
    from collections import OrderedDict
    people = OrderedDict((n["id"], n) for n in b["people"])
    ents = OrderedDict((n["id"], n) for n in b["entities"])
    acc = os.path.join(ROOT, "tools", "DUPLICATES_ACCEPTED.json")
    ok = set()
    if os.path.exists(acc):
        for row in json.load(open(acc, encoding="utf-8")).get("accepted", []):
            ok.add(tuple(sorted([row["a"], row["b"]])))
    bad = []
    for g in duplicate_groups(people, ents):
        if tuple(sorted([g["a"], g["b"]])) not in ok:
            bad.append(f"{g['a']} and {g['b']} look like one {g.get('cls')} recorded twice "
                       f"(label overlap {g.get('overlap')}); collapse it, or record why it is "
                       f"not a duplicate in tools/DUPLICATES_ACCEPTED.json")
    return bad[:40]


@check("affiliations render as names, not ids")
def _affiliations(b, html):
    """affiliations is a prose field upstream and is printed verbatim. The research
    here writes node ids into it, so 54 entries reached the dossier as raw slugs:
    a reader saw 'dod-sapco' and 'skidmore-fitts-report' where a name belonged.

    The renderer now resolves an id-shaped entry to that node's label and links it,
    which keeps the graph link instead of throwing it away by rewriting to prose.
    That fix only holds for entries that name a REAL node -- an id-shaped string
    matching nothing falls through to esc() and prints the slug. So the property
    worth asserting is not 'no ids here', it is: every id-shaped entry resolves."""
    ids = {n["id"] for n in b["people"] + b["entities"]}
    slug = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    bad = []
    for p in b["people"]:
        for a in p.get("affiliations") or []:
            if isinstance(a, str) and slug.match(a) and a not in ids:
                bad.append(f"{p['id']}: affiliation {a!r} is id-shaped but names no node, "
                           f"so it prints as the raw slug")
    return bad[:40]


@check("sequence chains are renderable")
def _chain_shape(b, html):
    """chainHtml() reads s.date, s.event, s.source and s.isAnomalous off every step.
    All 11 chains on this board held bare node-id strings instead of step objects,
    so every one of them rendered an undefined event under an undefined date --
    including Grusch, Elizondo, Davis and Marcel, which are the most-read dossiers
    here. Nothing threw, and no count moved.

    The renderer is inherited from The Vanishing, where a chain step is an ordered,
    dated, individually sourced link. The research wrote program lineages into the
    same field. Both are legitimate objects; only one of them is what this field
    renders, and the field has to hold what the renderer reads."""
    bad = []
    for p in b["people"]:
        for i, s in enumerate(p.get("sequenceChain") or []):
            if not isinstance(s, dict):
                bad.append(f"{p['id']}: chain step {i} is a {type(s).__name__}, not a step object")
            elif not (s.get("date") and s.get("event")):
                bad.append(f"{p['id']}: chain step {i} has no date or no event")
    return bad[:40]


@check("no edge note leaks build bookkeeping")
def _edge_note_bookkeeping(b, html):
    """An edge note renders in the dock. A reader gets it as the board's statement of
    what the edge asserts, so it must say only that.

    Collapse re-pointing wrote its own provenance into the notes it re-pointed --
    "[Re-pointed from the collapsed duplicate `setka`, 14 Aug 2026.]" and similar.
    That is editing history, not an assertion about the world, and twelve of them
    shipped to readers. They were stripped by hand once before and came back,
    because two of the three collapse files were missed and nothing looked again.

    The provenance is not lost: it lives in research/*-collapse.json and in
    notes/DUPLICATES-2026-08-22.md, which is where a reader who wants the editing
    history should find it."""
    pat = re.compile(r"\[Re-pointed from|collapsed duplicate|Board bookkeeping", re.I)
    bad = []
    for e in b["edges"]:
        note = e.get("note") or ""
        m = pat.search(note)
        if m:
            bad.append(f"edge {e.get('a')}->{e.get('b')} ({e.get('type')}) "
                       f"note carries build bookkeeping: {m.group(0)!r}")
    return bad[:40]


@check("every edge type has a caption written for this board")
def _explain_edge_covers(b, html):
    """explainEdge() writes the caption under every connection in every node dock.
    A type with no case falls through to 'Connected.', which reads as a caption
    rather than as a gap, so nothing looks broken and nobody goes looking.

    That is how four of this board's twelve types -- legislative, denial, custody
    and funding, 554 edges between them -- were explained with one word for as long
    as the board has existed. Custody is one of the three axes the board scores on.

    The same surface carried the parent board's meanings for two types it does
    share: behavioral was 'Both left the same category of personal item behind',
    which is a missing-person fact, and temporal was a sixty-day proximity rule.
    Both rendered confidently over edges that mean something else entirely.

    This asserts coverage, not wording: every type present in the data must have
    its own case, and no case may still carry the parent's vocabulary."""
    import re as _re
    types = {e.get("type") for e in b["edges"] if e.get("type")}
    m = _re.search(r"function explainEdge\(type, a, b\) \{.*?\n\}", html, _re.S)
    if not m:
        return ["explainEdge() is not in the built file at all"]
    blk = m.group(0)
    cases = set(_re.findall(r"case '([^']+)':", blk))
    bad = [f"edge type {t!r} has no explainEdge case, so its caption is 'Connected.'"
           for t in sorted(types - cases)]
    # the parent board's vocabulary, which must not survive here
    for phrase in ("personal item behind", "sixty days", "left everything behind",
                   "departure kit"):
        if phrase in blk:
            bad.append(f"explainEdge still carries the parent board's wording: {phrase!r}")
    return bad


@check("no parent-board editorial content ships")
def _no_parent_editorial(b, html):
    """This board was built by porting a shell from a sibling project, The Vanishing,
    which is about a cluster of missing and dead scientists. Its vocabulary kept
    surviving the port in surfaces nobody had read: the scripted analyst answered
    about JPL headcount, explainEdge captioned this board's behavioral edges with a
    fact about personal effects, and a 3KB COUNTERS array of skeptical commentary on
    that dataset shipped inside the published file, declared and referenced by
    nothing.

    None of it could throw. All of it renders, or reads, as confident and finished.

    The list grew on 25 August after a systematic sweep: diffing prose string
    literals between ref/the-vanishing-v2.html and the built file showed 177 that
    survived the port verbatim, of which five rendered as false copy -- a hardcoded
    "Fifty-two entities across five classes" heading the SEARCH view of a 956-node
    board among them.

    These strings are specific to the sibling board's subject matter and have no
    legitimate use here. Note what is deliberately NOT listed: 'Ning Li' and 'JPL'
    both appear on this board for real reasons -- the AAWSAP superconductor DIRD
    reviews Ning Li's work -- so screening on them would fire on good content."""
    banned = ("NeuroLogica", "matched denominator", "left everything behind",
              "departure kit", "the leftBehind array",
              # found by diffing prose literals against ref/the-vanishing-v2.html:
              # 177 survived the port verbatim and these five rendered as false copy
              "Fifty-two entities", "who disappeared within three months",
              "derived from the case records",
              "after April 2026 is a fact about reporting attention")
    return [f"the built file carries the parent board's {p!r}"
            for p in banned if p in html]


@check("the analyst system prompt describes this board")
def _system_prompt_is_ours(b, html):
    """SYSTEM_PROMPT() is what the model is told it is before it answers anything, and
    until 25 August it had never been checked by anything.

    It was inherited whole. It opened by calling this 'a research dashboard tracking
    deaths and disappearances of US scientists and defense-connected individuals since
    2021', which is the sibling board's mission with the name swapped -- the identical
    fault as the scripted analyst, one path over, missed because the scripted path got
    the attention.

    The costly line was HARD RULE 4: 'The three axes S, P and I are never summed.'
    This board scores every entity on C, A and D. The model held the wrong names for
    the board's primary scoring scheme, stated as a numbered hard rule, so any answer
    it gave about scoring reasoned over letters that are not here. A wrong axis name
    cannot throw; it produces fluent analysis of nothing.

    Asserts the prompt names this board's axes, and carries none of the parent's."""
    import re as _re
    m = _re.search(r"const SYSTEM_PROMPT = \(\) => `(.*?)`;", html, _re.S)
    if not m:
        return ["SYSTEM_PROMPT() is not in the built file"]
    p = m.group(1)
    bad = []
    for need in ("C (custody proximity)", "A (access level)", "D (disclosure role)"):
        if need not in p:
            bad.append(f"the system prompt never names the axis {need!r}")
    for wrong in ("axes S, P and I", "deaths and disappearances",
                  "real missing people", "who disappeared"):
        if wrong in p:
            bad.append(f"the system prompt still carries the parent board's {wrong!r}")
    return bad


@check("claim tiers are valid and Tier 1 is sourced")
def _claims(b, html):
    """Credibility rule: no claim renders without a confidence treatment, and Tier 1
    means a primary record exists. A Tier 1 with no URL is the single most damaging
    thing this board can ship."""
    bad = []
    for n in b["people"] + b["entities"]:
        for c in n.get("claims", []):
            if c.get("tier") not in (1, 2, 3):
                bad.append(f"{n['id']}: claim with tier {c.get('tier')!r}")
            elif c["tier"] == 1 and not str(c.get("source") or "").strip():
                bad.append(f"{n['id']}: Tier 1 claim with no source")
    return bad[:40]


@check("UI copy agrees with the data")
def _copy(b, html):
    """The DETAIL panel said 'Five entity classes' on a board with eight. Copy that
    states a fact about the data is data, and drifts like data."""
    bad = []
    classes = {n["cls"] for n in b["entities"]} | {"person"}
    words = {5: "Five", 8: "Eight", 9: "Nine", 12: "Twelve", 4: "Four", 3: "Three"}
    want = words.get(len(classes))
    m = re.search(r"(\w+) entity classes are clickable", html)
    if m and want and m.group(1) != want:
        bad.append(f"copy says {m.group(1)!r} entity classes; data has {len(classes)} ({want})")
    strands = {t.get("strand") for t in b.get("timeline", []) if t.get("strand")}
    m2 = re.search(r"(\w+) strands on one axis", html)
    if m2 and words.get(len(strands)) and m2.group(1) != words[len(strands)]:
        bad.append(f"copy says {m2.group(1)!r} strands; data has {len(strands)}")
    return bad


@check("the built file contains the data it claims")
def _dist(b, html):
    bad = []
    if not html:
        return ["dist/the-program.html is missing — run build_dashboard.py"]
    for needle, what in [("PROGRAM_EDGES", "edge array"), ("TIMELINE", "timeline array")]:
        if needle not in html:
            bad.append(f"built file has no {what}")
    # Exact, not a heuristic: every node in the data must be present in the artifact.
    # A count comparison was the first version of this check and it was wrong — it
    # also matched timeline ids. A check that is approximately right fails in both
    # directions and teaches you to ignore it.
    # Match the id as a quoted token rather than assuming a serialization. People are
    # emitted as `id: 'x'` and entities as `other('x', 'institution', ...)`; the first
    # version of this check knew only the former and declared all 724 entities missing.
    missing = [n["id"] for n in b["people"] + b["entities"]
               if ("'%s'" % n["id"]) not in html]
    if missing:
        bad.append(f"{len(missing)} node(s) in the data are absent from the built file: "
                   f"{missing[:5]}")
    return bad



# ---------------------------------------------------------------------------
# the L0 program map — six checks, each self-tested
#
# These validate what SHIPPED, not what a helper recomputes: the model is parsed
# back out of the built HTML. A patch that reads correctly and does not take
# effect is this board's most expensive recurring bug, and reading the source is
# how it keeps getting missed.
# ---------------------------------------------------------------------------

def _l0(html):
    """Pull the L0DATA literal back out of the built file. Returns None if absent."""
    i = html.find("const L0DATA = ")
    if i < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(html, i + len("const L0DATA = "))
        return obj
    except ValueError:
        return None


@check("register partition is total")
def _l0_partition(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    c = d["counts"]
    total = len(b["people"]) + len(b["entities"])
    got = c["l0"] + c["ledger"] + c["pathOnly"] + c["unattached"]
    bad = []
    if got != total:
        bad.append(f"registers sum to {got}, board has {total} nodes — "
                   f"the partition is not total, so 'nothing was left out' is false")
    # and no id may appear in two registers, or in none
    seen, dupe = {}, []
    for reg, ids in (("l0", [n["id"] for n in d["l0"]]),
                     ("pathOnly", [r["id"] for r in d["pathOnly"]]),
                     ("unattached", [r["id"] for r in d["unattached"]])):
        for i in ids:
            if i in seen:
                dupe.append(f"{i} is in both {seen[i]} and {reg}")
            seen[i] = reg
    bad += dupe[:5]
    if c["l0"] != len(d["l0"]):
        bad.append(f"counts.l0 says {c['l0']}, the l0 array holds {len(d['l0'])}")
    return bad


@check("summarised edge tier is the strongest of its underlying links")
def _l0_tier(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    pair = {}
    for e in b["edges"]:
        pair.setdefault("|".join(sorted((e["a"], e["b"]))), []).append(e)
    bad = []
    for e in d["summarised"]:
        want = 9
        for v in e["via"]:
            for end in (e["a"], e["b"]):
                for h in pair.get("|".join(sorted((end, v))), []):
                    want = min(want, h["claimTier"])
        if want != 9 and e["tier"] != want:
            bad.append(f"summarised {e['a']}~{e['b']} prints tier {e['tier']}, "
                       f"strongest underlying link is tier {want}")
        # the tick count IS the shared-member count; they cannot disagree
        if e["n"] != len(e["via"]):
            bad.append(f"summarised {e['a']}~{e['b']} claims {e['n']} shared members "
                       f"but lists {len(e['via'])}")
        # The design asserted shared counts run 2-5 so the five-tick vocabulary
        # never overflows. Densifying the graph made that false. The assertion
        # that still holds is that the RENDERER can represent the overflow: five
        # ticks drawn for both 5 and 18 would be a channel that silently
        # saturates, which is the same failure class as a check that always
        # passes.
        if e["n"] > 5 and "TICK_MAX" not in html:
            bad.append(f"summarised {e['a']}~{e['b']} carries {e['n']} shared "
                       f"members and the renderer has no tick-overflow path")
    return bad[:8]


@check("the shared-member gate holds and only hand-written edges are summarised")
def _l0_gate(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    hand = set()
    for e in b["edges"]:
        hand.add("|".join(sorted((e["a"], e["b"]))))
    gate = d["config"]["sharedMemberGate"]
    bad = []
    for e in d["summarised"]:
        if len(e["via"]) < gate:
            bad.append(f"summarised {e['a']}~{e['b']} has {len(e['via'])} shared "
                       f"member(s), below the gate of {gate}")
        # A rolled-up DERIVED edge would carry a count and a tier earned by nothing
        # but a shared attribute. The two must never meet in the same code path.
        for v in e["via"]:
            for end in (e["a"], e["b"]):
                if "|".join(sorted((end, v))) not in hand:
                    bad.append(f"summarised {e['a']}~{e['b']} rests on {end}~{v}, "
                               f"which is not a hand-written edge")
    return bad[:8]


@check("no routed or path-only entity emits an edge instance")
def _l0_noroutededges(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    l0ids = {n["id"] for n in d["l0"]}
    off = {r["id"] for r in d["pathOnly"]} | {r["id"] for r in d["unattached"]}
    for n in d["l0"]:
        off |= {r["id"] for r in n["routed"]}
    bad = []
    for e in d["directEdges"] + d["summarised"]:
        for end in (e["a"], e["b"]):
            if end in off:
                bad.append(f"edge {e['a']}~{e['b']} has endpoint {end}, which is "
                           f"routed or path-only and must not draw")
            elif end not in l0ids:
                bad.append(f"edge {e['a']}~{e['b']} has endpoint {end}, which is "
                           f"not on the map at all")
    # every routed row must print its intermediates, or the reader cannot audit
    # how the entity was attached
    for n in d["l0"]:
        for r in n["routed"]:
            if r["depth"] > 1 and not r.get("via"):
                bad.append(f"{r['id']} is attached to {n['id']} at depth "
                           f"{r['depth']} with no intermediates printed")
    return bad[:8]


@check("UI copy agrees with the register counts")
def _l0_copy(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    c = d["counts"]
    bad = []
    # Both registers must be REACHABLE, and their counts must be DERIVED. A
    # hard-coded number is the DETAIL-panel bug that shipped last time: it read
    # fine and was false. So assert the control exists and that the number beside
    # it comes from the model rather than from a keystroke.
    for key, attr in (("pathOnly", "path"), ("unattached", "un")):
        if 'data-l0reg="%s"' % attr not in html:
            bad.append(f"the rail has no {key} register control — the register is "
                       f"asserted in the counts but unreachable in the UI")
        if "L0DATA.counts." + key not in html:
            bad.append(f"the {key} count is not derived from L0DATA.counts; a typed "
                       f"number goes stale the moment the research moves")
    for n in d["l0"]:
        listed = len(n["direct"]) + len(n["routed"])
        mixed = sum(n["mix"].values())
        if listed != mixed:
            bad.append(f"{n['id']} says {mixed} members in its class bar but lists "
                       f"{listed} rows")
    return bad[:8]


@check("every routed row names its intermediate resolvably")
def _l0_via(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    known = set(d["nodes"].keys())
    bad = []
    for n in d["l0"]:
        for r in n["routed"]:
            for v in r.get("via", []):
                # This is where JR., J. comes back. A via that does not resolve to
                # a real node id prints a label the reader cannot follow — and a
                # label truncated at the first space prints "via AARO" for a FOIA
                # memorandum and "via Kirsten" for a senator.
                if v not in known:
                    bad.append(f"{n['id']} routes {r['id']} via '{v}', which is not "
                               f"a node id")
                elif not str(d["nodes"][v][0]).strip():
                    bad.append(f"{n['id']} routes {r['id']} via {v}, which has an "
                               f"empty label")
    return bad[:8]


@check("every L0 node carries an entity dossier")
def _l0_dossier_cover(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    # The dossier is the ARGUMENT for why a node is on this map, and on this board
    # the argument is the product. A node with a member list and no argument sends
    # the reader into individual dossiers to reconstruct it themselves.
    missing = [n["id"] for n in d["l0"] if not (n.get("dossier") or {}).get("narrative")]
    if missing:
        return [f"{len(missing)} L0 node(s) have no entity dossier: {missing[:6]}"]
    return []


@check("every dossier claim is tiered and sourced")
def _l0_dossier_claims(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    bad = []
    for n in d["l0"]:
        for i, c in enumerate((n.get("dossier") or {}).get("claims", [])):
            if c.get("tier") not in (1, 2, 3):
                bad.append(f"{n['id']} claim {i} has tier {c.get('tier')!r}; "
                           f"an untiered claim is an unmarked assertion")
            if not str(c.get("source") or "").strip():
                bad.append(f"{n['id']} claim {i} has no source. This is the one "
                           f"rule that never bends.")
            if not str(c.get("text") or "").strip():
                bad.append(f"{n['id']} claim {i} has no text")
    return bad[:8]


@check("every connection row is backed by a hand-written edge")
def _l0_connections(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    hand = set()
    for e in b["edges"]:
        hand.add((e["a"], e["b"], e["type"]))
        hand.add((e["b"], e["a"], e["type"]))
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for src, rows in (d.get("connections") or {}).items():
        for r in rows:
            # The connection layer is PROJECTED from sourced edges, never written.
            # If a row appears here with no edge behind it, something generated it,
            # and a generated connection on this board is a fabricated claim.
            if (src, r["id"], r["type"]) not in hand:
                bad.append(f"{src} -> {r['id']} ({r['type']}) has no hand-written "
                           f"edge behind it")
            if r["id"] not in ids:
                bad.append(f"{src} connects to {r['id']}, which is not a node")
    return bad[:8]


@check("structural authority is cited, and the exclusions hold")
def _l0_authority(b, html):
    d = _l0(html)
    if d is None:
        return ["the built file carries no L0 model"]
    auth = d.get("authority") or {}
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    # Excluded on principle, not by accident: a spokesperson speaks for a decision
    # and does not make one; an FFRDC trustee advises a corporation, not a
    # compartment. The first matcher caught all four plus a set of hearings that
    # merely cited an office. If they reappear, the matcher has gone loose again.
    for x in ("susan-gough", "christopher-sherwood", "donald-kerr", "sue-gordon"):
        if x in auth:
            bad.append(f"{x} is flagged as holding structural authority; it is "
                       f"excluded by rule and the matcher has gone loose")
    for k, v in auth.items():
        if k not in ids:
            bad.append(f"{k} carries authority but is not a node")
        if not v.get("instruments"):
            bad.append(f"{k} claims authority with no instrument cited; an uncited "
                       f"authority is an assertion")
        if v.get("tense") not in ("holds", "held"):
            bad.append(f"{k} has tense {v.get('tense')!r}; a former holder's "
                       f"authority is history and must not read as live")
    return bad[:8]

# ---------------------------------------------------------------------------
# golden counts — drift detection. Not correctness; a tripwire that turns a
# silent change into a deliberate one. `--update-golden` is the only way past it.
# ---------------------------------------------------------------------------

def _l0_golden():
    """The six L0 counts GOLDEN tracks. `unattached` moving is either a research
    gain or a routing regression, and the two look identical in a diff — which is
    exactly why it needs deliberate acceptance rather than a silent update."""
    path = os.path.join(ROOT, "data", "l0-model.json")
    if not os.path.exists(path):
        return {}
    c = json.load(open(path, encoding="utf-8"))["counts"]
    return {"l0_nodes": c["l0"], "l0_edges_direct": c["directEdges"],
            "l0_edges_summarised": c["summarisedEdges"], "ledger": c["ledger"],
            "path_only": c["pathOnly"], "unattached": c["unattached"],
            "l0_with_dossier": c.get("withDossier", 0),
            "l0_dossier_claims": c.get("dossierClaims", 0)}


def measure(b):
    from collections import Counter
    cls = Counter(n["cls"] for n in b["entities"])
    tier = Counter(n.get("tier") for n in b["people"] + b["entities"])
    ctier = Counter(c["tier"] for n in b["people"] + b["entities"] for c in n.get("claims", []))
    # This counted the whole annotated source STRING, so appending a demotion note
    # to a claim minted a new "unique source URL" and the number drifted upward on
    # a pass that added no sourcing at all. Count the URLs, from the claim sources
    # and the node sources alike, which is what the name has always promised.
    urlpat = re.compile(r"https?://[^\s,;)\]<>\"]+")
    urls = set()
    for n in b["people"] + b["entities"]:
        for c in n.get("claims", []):
            urls.update(u.rstrip(".,;") for u in urlpat.findall(c.get("source") or ""))
        for sc in n.get("sources", []) or []:
            if sc.get("url"):
                urls.add(sc["url"].rstrip(".,;"))
    return {
        "people": len(b["people"]), "entities": len(b["entities"]),
        "edges": len(b["edges"]), "timeline": len(b.get("timeline", [])),
        "entity_classes": dict(sorted(cls.items())),
        "entity_tiers": dict(sorted(tier.items())),
        "claim_tiers": {str(k): v for k, v in sorted(ctier.items())},
        "unique_source_urls": len(urls),
        **_l0_golden(),
        "people_with_date": sum(1 for p in b["people"] if p.get("date")),
        "locations_with_coords": sum(1 for e in b["entities"] if e.get("coords")),
    }


@check("counts match the golden manifest")
def _golden(b, html):
    now = measure(b)
    if not os.path.exists(GOLDEN):
        return ["tools/GOLDEN.json missing — run with --update-golden to establish it"]
    want = json.load(open(GOLDEN, encoding="utf-8"))["counts"]
    bad = []
    for k, v in want.items():
        if now.get(k) != v:
            bad.append(f"{k}: golden {v!r} -> now {now.get(k)!r}")
    return bad


# ---------------------------------------------------------------------------
# the no-key analyst — the only voice a reader without an API key ever hears.
# ---------------------------------------------------------------------------

@check("scripted analyst answers from the right branch")
def check_scripted_analyst(board, html):
    """Delegate to tools/test_scripted_analyst.mjs, which asserts the TOPIC TAG
    of each answer rather than its prose.

    Kept as a separate script, and shelling out rather than reimplementing:
    the function under test is JavaScript that closes over NODES and L0DATA, so
    the only honest way to test it is to run it. Reimplementing its routing in
    Python would produce a check that agrees with my reading of the code, which
    is the failure this repo keeps hitting.

    That script carries its own self-test: BREAK=1 disables the topic table and
    the run must go red. This check is exercised in self_test() the same way.
    """
    exe = os.path.join(ROOT, "tools", "test_scripted_analyst.mjs")
    if not os.path.exists(exe):
        return ["tools/test_scripted_analyst.mjs is missing"]
    env = dict(os.environ)
    r = subprocess.run(["node", exe], capture_output=True, cwd=ROOT, env=env)
    if r.returncode == 0:
        return []
    out = (r.stdout.decode() + r.stderr.decode())
    lines = [l for l in out.splitlines() if l.startswith("FAIL") or "->" in l]
    return ["scripted analyst routing: " + l.strip() for l in lines[:12]] or \
           ["scripted analyst test exited %d: %s" % (r.returncode, out[-300:])]


# ---------------------------------------------------------------------------
# idempotency — the check that would have caught the 35 lost dates.
# ---------------------------------------------------------------------------

def check_idempotent():
    """Run the full documented pipeline twice and require an identical artifact.

    This is the check that catches a whole CLASS of bug rather than one instance:
    any pass that reads its own previous output back in and forgets what it did.
    It is slow, so it is opt-in via --idempotent (and is what CI should run).
    """
    def build_once():
        # build_l0 bakes the L0 model and its layout; build_dashboard consumes it.
        # It is in the idempotency gate because a bake seeded from anything
        # non-deterministic would drift here and nowhere else.
        # build_design_extract feeds build_l0_layout, which is Design's generator
        # and is now inside the gate: a packed layout is a pure function of its
        # inputs, so if it is not byte-identical across two runs something
        # non-deterministic has crept back in.
        for cmd in (["merge.py"], ["regrade.py"], ["merge.py"],
                    ["build_l0.py"], ["build_design_extract.py"],
                    ["build_l0_layout.mjs"], ["build_dashboard.py"]):
            exe = ["node"] if cmd[0].endswith(".mjs") else [sys.executable]
            r = subprocess.run(exe + [os.path.join(ROOT, "tools", cmd[0])],
                               capture_output=True, cwd=ROOT)
            if r.returncode != 0:
                return None, f"{cmd[0]} exited {r.returncode}: {r.stderr.decode()[:400]}"
        # Both artifacts carry a "generated":"YYYY-MM-DD" stamp. Hashing it makes
        # this check fail for a build that straddles midnight UTC -- a real, rare,
        # maximally confusing false failure, since nothing is actually
        # non-deterministic and a re-run passes. Neutralise the stamp and hash
        # everything else. Verified 25 Aug: two consecutive runs are byte-identical
        # apart from this field.
        stamp = re.compile(rb'"generated"\s*:\s*"\d{4}-\d{2}-\d{2}"')
        h = hashlib.sha256()
        h.update(stamp.sub(b'"generated":"<stamped>"', open(DIST, "rb").read()))
        lm = os.path.join(ROOT, "data", "l0-layout-model.json")
        if os.path.exists(lm):
            h.update(stamp.sub(b'"generated":"<stamped>"', open(lm, "rb").read()))
        return h.hexdigest(), None

    h1, err = build_once()
    if err:
        return [err]
    h2, err = build_once()
    if err:
        return [err]
    if h1 != h2:
        return [f"pipeline is NOT idempotent: two consecutive builds differ "
                f"({h1[:12]} vs {h2[:12]}). Something reads its own output back in."]
    return []


# ---------------------------------------------------------------------------
# self-test — every check must be shown capable of failing.
# ---------------------------------------------------------------------------

def self_test():
    """Feed each check input it MUST reject. A check that passes here is broken,
    and a broken check is worse than no check because it reads as evidence."""
    good_html = ("Eight entity classes are clickable: x. Four strands on one axis. "
                 "PROGRAM_EDGES TIMELINE "
                 + " ".join("'%s'" % i for i in
                            ["a-b"] + ["e%d" % i for i in range(7)]))
    # The fixture must exercise the real shape: eight classes and four strands, or
    # the copy check silently no-ops on an unmapped count — which is precisely how
    # it failed its own self-test the first time this file was run.
    base = {"people": [{"id": "a-b", "cls": "person", "label": "Ann Bee", "claims": []}],
            "entities": [{"id": f"e{i}", "cls": c, "label": f"E{i}", "claims": []}
                         for i, c in enumerate(["institution", "program", "location",
                                                "domain", "legislation", "document",
                                                "event"])],
            "edges": [], "timeline": [{"strand": "program"}, {"strand": "witness"},
                                      {"strand": "oversight"}, {"strand": "coverup"}]}

    def mut(f):
        import copy
        b = copy.deepcopy(base)
        f(b)
        return b

    poisons = {
        "ids are canonical": mut(lambda b: b["people"].append(
            {"id": "p-a-b", "cls": "person", "label": "Ann Bee", "claims": []})),
        "no label is its own id": mut(lambda b: b["people"][0].update(label="a-b")),
        "person plate names are meaningful": mut(lambda b: b["people"][0].update(
            label="James R. Clapper Jr.") or b["people"][0].update(label="Jr.")),
        "no dangling references": mut(lambda b: b["edges"].append(
            {"a": "a-b", "b": "ghost", "type": "custody"})),
        "every person back-reference resolves": mut(
            lambda b: b["people"][0].update(locId="l-ghost")),
        "sequence chains are renderable": mut(
            lambda b: b["people"][0].update(sequenceChain=["a-node-id"])),
        "affiliations render as names, not ids": mut(
            lambda b: b["people"][0].update(affiliations=["some-ghost-org"])),
        "no unapproved duplicate nodes": mut(lambda b: (
            b["entities"][0].update(label="Twin Report",
                                    sources=[{"url": "https://example.gov/twin.pdf"}]),
            b["entities"].append({"id": "e-twin", "cls": b["entities"][0]["cls"],
                                  "label": "Twin Report", "claims": [],
                                  "sources": [{"url": "https://example.gov/twin.pdf"}]}))),
        "no edge note leaks build bookkeeping": mut(lambda b: b["edges"].append(
            {"a": "a-b", "b": "a-b", "type": "custody",
             "note": "Asserts a thing. [Re-pointed from the collapsed duplicate `x`, 14 Aug 2026.]"})),
        "claim tiers are valid and Tier 1 is sourced": mut(lambda b: b["people"][0]["claims"].append(
            {"tier": 1, "text": "x", "source": ""})),
        "UI copy agrees with the data": base,   # paired with a poisoned html below
        "the built file contains the data it claims": base,
    }
    poison_html = {"UI copy agrees with the data": "Five entity classes are clickable: x. "
                                                   "Four strands on one axis. PROGRAM_EDGES TIMELINE",
                   # present, but with every node id stripped out
                   "the built file contains the data it claims":
                       "Eight entity classes are clickable: x. Four strands on one axis. "
                       "PROGRAM_EDGES TIMELINE"}


    # ---- L0 fixtures. Each of the six L0 checks gets input it MUST reject.
    # The model is read back out of the HTML, so most poisons are HTML-side: that
    # is deliberate, because what shipped is the only thing worth asserting on.
    def L0(**kw):
        m = {"config": {"sharedMemberGate": 2},
             "counts": {"total": 8, "l0": 1, "ledger": 1, "pathOnly": 0,
                        "unattached": 6},
             "l0": [{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                     "dossier": {"narrative": "why e0 is on the map",
                                 "claims": [{"text": "x", "tier": 1, "source": "https://e"}]}}],
             "directEdges": [], "summarised": [], "pathOnly": [],
             "unattached": [{"id": "e%d" % i, "deg": 0} for i in range(1, 7)],
             "connections": {}, "authority": {},
             "nodes": {"a-b": ["Ann Bee", "person", 1, "A"],
                       **{"e%d" % i: ["E%d" % i, "institution", 0, "B"] for i in range(7)}}}
        m.update(kw)
        return m

    # Capture the base ONCE. Building the poisoned html from a good_html that had
    # already been given a model appended a SECOND L0DATA literal, and _l0 reads the
    # first — so every poison silently carried a clean model and all six checks
    # passed their self-test while asserting nothing. That is the canvasInk failure
    # exactly, reproduced in the fixture rather than the check.
    _base_html = good_html

    def wrap(model, extra=""):
        # the rail strings the copy check looks for, plus the model literal
        return (_base_html + ' data-l0reg="path" data-l0reg="un" '
                + ' L0DATA.counts.pathOnly L0DATA.counts.unattached ' + extra
                + "\nconst L0DATA = " + json.dumps(model) + ";\n")

    # The caption check reads explainEdge() out of the built file, so the CLEAN
    # fixture has to contain a real one or the check reports a false positive on
    # good input -- which is what it did the first time it ran.
    EXPLAIN_OK = ("\nfunction explainEdge(type, a, b) {\n  switch (type) {\n"
                  + "".join("    case '%s':\n      return 'x';\n" % t for t in
                            ("institutional", "geographic", "research", "temporal",
                             "behavioral", "programmatic", "investigative",
                             "witness-chain", "custody", "funding", "denial",
                             "legislative"))
                  + "    default:\n      return 'Connected.';\n  }\n}\n")

    # Same reason as EXPLAIN_OK: the system-prompt check reads the prompt out of the
    # built file, so the CLEAN fixture needs a valid one or the check false-positives
    # on good input.
    SYSPROMPT_OK = ("\nconst SYSTEM_PROMPT = () => `You are the analyst. The three axes "
                    "are C (custody proximity), A (access level) and D (disclosure role), "
                    "and they are never summed.`;\n")

    good_html = wrap(L0(), EXPLAIN_OK + SYSPROMPT_OK)

    # a board with the hand-written edges the tier and gate poisons rest on
    l0board = mut(lambda b: b["edges"].extend([
        {"a": "e0", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e0", "b": "e2", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "e2", "type": "custody", "claimTier": 1}]))
    two_l0 = [{"id": "e0", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}},
              {"id": "e1", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}}]

    poisons.update({
        # a board carrying custody edges, against html whose explainEdge lost that case
        "every edge type has a caption written for this board": l0board,
        # a summarised edge printing Tier 3 over two Tier 1 links
        "summarised edge tier is the strongest of its underlying links": l0board,
        "the shared-member gate holds and only hand-written edges are summarised": l0board,
    })
    _l0_dosn = {"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                "dossier": {"narrative": "why e0 is on the map",
                            "claims": [{"text": "x", "tier": 1, "source": "https://e"}]}}
    poison_html.update({
        # REPLACE the good prompt, never append a second one: the check reads the
        # first SYSTEM_PROMPT in the file, so an appended poison leaves the clean
        # one in front of it and the check passes while asserting nothing. That is
        # the duplicate-L0DATA trap this fixture already warns about, hit again.
        "the analyst system prompt describes this board":
            good_html.replace(SYSPROMPT_OK,
                "\nconst SYSTEM_PROMPT = () => `You are the analyst. The three "
                "axes S, P and I are never summed.`;\n"),
        "no parent-board editorial content ships":
            good_html + " NeuroLogica (Novella) on the matched denominator ",
        "every edge type has a caption written for this board":
            good_html.replace("    case 'custody':\n      return 'x';\n", "", 1),
        # a node on the map with no argument for why it is there
        "every L0 node carries an entity dossier":
            wrap(L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1}}])),
        # an unsourced claim, which is the one rule that never bends
        "every dossier claim is tiered and sourced":
            wrap(L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                         "dossier": {"narrative": "n",
                                     "claims": [{"text": "x", "tier": 1, "source": ""}]}}])),
        # registers that do not sum to the board
        "register partition is total":
            wrap(L0(counts={"total": 8, "l0": 1, "ledger": 1, "pathOnly": 0, "unattached": 5})),
        "summarised edge tier is the strongest of its underlying links":
            wrap(L0(l0=two_l0, counts={"total": 8, "l0": 2, "ledger": 1, "pathOnly": 0, "unattached": 5},
                    summarised=[{"a": "e0", "b": "e1", "n": 2, "tier": 3,
                                 "via": ["a-b", "e2"], "links": 4}])),
        # one shared member is not a summary, it is a restatement — and 420 of them
        # would have been drawn on the real board
        "the shared-member gate holds and only hand-written edges are summarised":
            wrap(L0(l0=two_l0, counts={"total": 8, "l0": 2, "ledger": 1, "pathOnly": 0, "unattached": 5},
                    summarised=[{"a": "e0", "b": "e1", "n": 1, "tier": 1,
                                 "via": ["a-b"], "links": 2}])),
        # an edge drawn to an unattached entity
        "no routed or path-only entity emits an edge instance":
            wrap(L0(directEdges=[{"a": "e0", "b": "e3", "n": 1, "tier": 1, "types": ["custody"]}])),
        # the class bar says two members, the ledger lists one
        "UI copy agrees with the register counts":
            wrap(L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [],
                         "mix": {"person": 1, "document": 1}}])),
        # the matcher going loose, plus an uncited authority claim
        "structural authority is cited, and the exclusions hold":
            wrap(L0(authority={"susan-gough": {"authority": "x", "instruments": [],
                                               "weight": 3, "tense": "holds",
                                               "publicRecord": {"connections": 0}}})),
        # a connection row with no edge behind it: something generated it
        "every connection row is backed by a hand-written edge":
            wrap(L0(connections={"e0": [{"id": "a-b", "type": "custody", "tier": 1,
                                         "label": "Ann Bee", "cls": "person",
                                         "dir": "out", "why": "", "note": ""}]})),
        # the JR., J. reappearance site: a via that resolves to nothing
        "every routed row names its intermediate resolvably":
            wrap(L0(l0=[{"id": "e0", "direct": [], "mix": {},
                         "routed": [{"id": "e4", "depth": 2, "via": ["ghost"]}]}])),
    })

    print("self-test — each check must REJECT poisoned input\n")
    ok = True
    for name, fn in CHECKS_RUN:
        if name == "counts match the golden manifest":
            print(f"  n/a   {name} (drift tripwire, not a property)")
            continue
        # The scripted-analyst check does not read the board or the HTML fixture
        # -- it runs real JavaScript in a subprocess -- so a poisoned dict proves
        # nothing about it. Its poison is BREAK=1, which disables the topic table
        # inside the function under test. Same contract as every other check:
        # show it going red, or it is not evidence.
        if name == "scripted analyst answers from the right branch":
            os.environ["BREAK"] = "1"
            try:
                caught = fn(base, good_html)
            finally:
                os.environ.pop("BREAK", None)
            clean = fn(base, good_html)
        else:
            b = poisons.get(name, base)
            html = poison_html.get(name, good_html)
            caught = fn(b, html)
            clean = fn(base, good_html)
        if not caught:
            print(f"  FAIL  {name}: did NOT reject poisoned input — this check is dead")
            ok = False
        elif clean:
            print(f"  FAIL  {name}: rejects CLEAN input too ({clean[0][:70]}) — false positive")
            ok = False
        else:
            print(f"  ok    {name}: rejects bad, accepts good")
    print()
    return ok


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        return 0 if self_test() else 1

    if not os.path.exists(BOARD):
        print("data/the-program.json missing — run merge.py", file=sys.stderr)
        return 1
    b = json.load(open(BOARD, encoding="utf-8"))
    html = open(DIST, encoding="utf-8").read() if os.path.exists(DIST) else ""

    if "--update-golden" in args:
        json.dump({"note": "Deliberately accepted counts. Every change here should be "
                           "explainable in the commit message.",
                   "counts": measure(b)},
                  open(GOLDEN, "w", encoding="utf-8"), indent=1)
        print("wrote tools/GOLDEN.json")
        return 0

    print("=== verify ===")
    failed = 0
    for name, fn in CHECKS_RUN:
        problems = fn(b, html)
        if problems:
            failed += 1
            print(f"  FAIL  {name}  ({len(problems)})")
            for p in problems[:8]:
                print(f"          {p}")
            if len(problems) > 8:
                print(f"          ... and {len(problems)-8} more")
        else:
            print(f"  ok    {name}")

    if "--idempotent" in args:
        problems = check_idempotent()
        if problems:
            failed += 1
            print("  FAIL  pipeline is idempotent")
            for p in problems:
                print(f"          {p}")
        else:
            print("  ok    pipeline is idempotent (two full builds, identical output)")

    print()
    if failed:
        print(f"!! {failed} CHECK(S) FAILED — do not ship this build")
    else:
        print("all checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
