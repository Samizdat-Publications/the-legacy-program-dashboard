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
    return bad[:40]


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
        if e["n"] > 5:
            bad.append(f"summarised {e['a']}~{e['b']} needs {e['n']} ticks; the "
                       f"vocabulary tops out at 5 and there is no numeral case")
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
            "path_only": c["pathOnly"], "unattached": c["unattached"]}


def measure(b):
    from collections import Counter
    cls = Counter(n["cls"] for n in b["entities"])
    tier = Counter(n.get("tier") for n in b["people"] + b["entities"])
    ctier = Counter(c["tier"] for n in b["people"] + b["entities"] for c in n.get("claims", []))
    urls = {c["source"] for n in b["people"] + b["entities"]
            for c in n.get("claims", []) if c.get("source")}
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
        for cmd in (["merge.py"], ["regrade.py"], ["merge.py"],
                    ["build_l0.py"], ["build_dashboard.py"]):
            r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", cmd[0])],
                               capture_output=True, cwd=ROOT)
            if r.returncode != 0:
                return None, f"{cmd[0]} exited {r.returncode}: {r.stderr.decode()[:400]}"
        return hashlib.sha256(open(DIST, "rb").read()).hexdigest(), None

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
             "l0": [{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1}}],
             "directEdges": [], "summarised": [], "pathOnly": [],
             "unattached": [{"id": "e%d" % i, "deg": 0} for i in range(1, 7)],
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

    good_html = wrap(L0())

    # a board with the hand-written edges the tier and gate poisons rest on
    l0board = mut(lambda b: b["edges"].extend([
        {"a": "e0", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e0", "b": "e2", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "e2", "type": "custody", "claimTier": 1}]))
    two_l0 = [{"id": "e0", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}},
              {"id": "e1", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}}]

    poisons.update({
        # a summarised edge printing Tier 3 over two Tier 1 links
        "summarised edge tier is the strongest of its underlying links": l0board,
        "the shared-member gate holds and only hand-written edges are summarised": l0board,
    })
    poison_html.update({
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
