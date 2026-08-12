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
# golden counts — drift detection. Not correctness; a tripwire that turns a
# silent change into a deliberate one. `--update-golden` is the only way past it.
# ---------------------------------------------------------------------------

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
        for cmd in (["merge.py"], ["regrade.py"], ["merge.py"], ["build_dashboard.py"]):
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
