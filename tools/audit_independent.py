#!/usr/bin/env python3
"""
audit_independent.py — Layer 1 of the adversarial review. Jess's pass.

DELIBERATELY DOES NOT IMPORT verify.py OR build_l0.py.

verify.py is the build gate and I wrote it. An audit that runs the author's own
checks proves the author is self-consistent, not that the deliverable is right.
This file re-derives every displayed figure from `data/the-program.json` using its
own arithmetic, then compares against the strings ACTUALLY RENDERED in
`dist/the-program.html`. Where the two disagree, the rendered value is what the
reader sees and therefore what is wrong.

Prints checks run / checks failed. A zero-failure run is demonstrated, not asserted.
"""

import json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")
DIST = os.path.join(ROOT, "dist", "the-program.html")

PASS, FAIL = [], []


def ck(name, got, want, note=""):
    if got == want:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: rendered/model {got!r} vs independently derived {want!r}"
                    + (f"  [{note}]" if note else ""))


def main():
    b = json.load(open(BOARD, encoding="utf-8"))
    html = open(DIST, encoding="utf-8").read()
    people, ents, edges = b["people"], b["entities"], b["edges"]
    nodes = people + ents

    # ---- the L0 model, re-derived from scratch --------------------------------
    # Independent reimplementation of the floor. If this disagrees with
    # data/l0-model.json, one of the two is wrong and the reader sees the model.
    adj = {n["id"]: set() for n in nodes}
    dangling = 0
    for e in edges:
        if e["a"] not in adj or e["b"] not in adj:
            dangling += 1
            continue
        adj[e["a"]].add(e["b"])
        adj[e["b"]].add(e["a"])
    ck("no dangling edges", dangling, 0)

    STRUCT = {"institution", "program", "event", "legislation", "document"}

    # The floor ALONE stopped describing L0 on 19 September 2026, when membership
    # became a BUDGET as well: the floor grew monotonically as research added edges
    # and the top-level map fell out of label mode at 1920. See build_l0.py.
    #
    # These two constants are RESTATED here on purpose and are NOT imported. This
    # file's whole value is that it re-derives the specification from scratch, so
    # that a bug in the builder cannot hide by being agreed with. Restating a rule
    # is the cost of that, and it is the point: when these disagree, one of the two
    # is wrong and the reader sees the model.
    FLOOR_A, BUDGET_A = 6, 135

    eligible = [n["id"] for n in nodes
                if n["cls"] in STRUCT and len(adj[n["id"]]) >= FLOOR_A]
    hl_path = os.path.join(ROOT, "data", "l0-highlights.json")
    hl_a = []
    if os.path.exists(hl_path):
        hl_a = [f.get("id") for f in
                (json.load(open(hl_path, encoding="utf-8")) or {}).get("flags") or []
                if isinstance(f, dict) and f.get("id")]
    if len(eligible) <= BUDGET_A:
        l0 = set(eligible)
    else:
        # Compete on degree; ties break on file order, as the builder does.
        pos = {nid: k for k, nid in enumerate(eligible)}
        ranked = sorted(eligible, key=lambda i: (-len(adj[i]), pos[i]))
        # Highlights are admitted by right, so C11 cannot be broken by growth.
        l0 = set(ranked[:BUDGET_A]) | (set(hl_a) & set(eligible))

    model = json.load(open(os.path.join(ROOT, "data", "l0-model.json"), encoding="utf-8"))
    c = model["counts"]
    ck("L0 node count", c["l0"], len(l0),
       f"floor = distinct neighbours >= {FLOOR_A}, budget = {BUDGET_A}, highlights by right")
    ck("L0 set identity", sorted(n["id"] for n in model["l0"]), sorted(l0),
       "the exact membership, not just the count")

    # BFS registers, recomputed
    depth = {i: 0 for i in l0}
    q = [n["id"] for n in nodes if n["id"] in l0]
    i = 0
    while i < len(q):
        u = q[i]; i += 1
        for v in adj[u]:
            if v not in depth:
                depth[v] = depth[u] + 1
                q.append(v)
    ledger = sum(1 for n in nodes if n["id"] not in l0 and 1 <= depth.get(n["id"], 99) <= 3)
    path_only = sum(1 for n in nodes if n["id"] not in l0 and depth.get(n["id"], 99) > 3
                    and n["id"] in depth)
    unatt = sum(1 for n in nodes if n["id"] not in depth)
    ck("ledger count", c["ledger"], ledger)
    ck("path-only count", c["pathOnly"], path_only)
    ck("unattached count", c["unattached"], unatt)
    ck("register partition sums to total",
       c["l0"] + c["ledger"] + c["pathOnly"] + c["unattached"], len(nodes),
       "the load-bearing rule: nothing may be left out")
    ck("model total equals node count", c["total"], len(nodes))

    # ---- edges: aggregation and the gate --------------------------------------
    pair = {}
    for e in edges:
        pair.setdefault("|".join(sorted((e["a"], e["b"]))), []).append(e)
    direct = [k for k in pair if all(x in l0 for x in k.split("|"))]
    ck("direct L0-L0 pair count", c["directEdges"], len(direct))

    # shared-member edges, recomputed with the >=2 gate
    shared = {}
    for n in nodes:
        if n["id"] in l0 or depth.get(n["id"]) != 1:
            continue
        par = sorted(v for v in adj[n["id"]] if v in l0)
        for x in range(len(par)):
            for y in range(x + 1, len(par)):
                k = "|".join(sorted((par[x], par[y])))
                if k in pair and all(z in l0 for z in k.split("|")):
                    continue
                shared.setdefault(k, set()).add(n["id"])
    summ = {k: v for k, v in shared.items() if len(v) >= 2}
    ck("summarised edge count", c["summarisedEdges"], len(summ),
       "gate is >= 2 shared members")
    gated = sum(1 for v in shared.values() if len(v) < 2)
    ck("gated-out count", c["gatedOut"], gated)

    # every summarised tick count must equal its shared-member count
    bad_tick = [e["id"] if isinstance(e, dict) else e for e in []]
    mism = 0
    for e in model["summarised"]:
        k = "|".join(sorted((e["a"], e["b"])))
        if k in summ and e["n"] != len(summ[k]):
            mism += 1
    ck("summarised tick counts equal shared-member counts", mism, 0)

    # tick overflow: the design said counts run 2-5. They do not any more.
    mx = max((e["n"] for e in model["summarised"]), default=0)
    ck("renderer has a tick-overflow path", "TICK_MAX" in html, mx <= 5 or True,
       f"max shared members is {mx}")
    if mx > 5 and "TICK_MAX" not in html:
        FAIL.append("tick overflow: counts exceed 5 and the renderer cannot draw it")

    # ---- dossiers -------------------------------------------------------------
    withd = sum(1 for n in model["l0"] if (n.get("dossier") or {}).get("narrative"))
    ck("every L0 node has a dossier", withd, c["l0"])
    ck("withDossier count is honest", c["withDossier"], withd)
    dc = sum(len((n.get("dossier") or {}).get("claims", [])) for n in model["l0"])
    ck("dossier claim total", c["dossierClaims"], dc)
    unsourced = sum(1 for n in model["l0"]
                    for cl in (n.get("dossier") or {}).get("claims", [])
                    if not str(cl.get("source") or "").strip())
    ck("no dossier claim is unsourced", unsourced, 0, "the one rule that never bends")
    untiered = sum(1 for n in model["l0"]
                   for cl in (n.get("dossier") or {}).get("claims", [])
                   if cl.get("tier") not in (1, 2, 3))
    ck("no dossier claim is untiered", untiered, 0)

    # ---- connections: projected, never generated ------------------------------
    hand = set()
    for e in edges:
        hand.add((e["a"], e["b"], e["type"]))
        hand.add((e["b"], e["a"], e["type"]))
    bad = 0
    rows = 0
    for src, rs in (model.get("connections") or {}).items():
        for r in rs:
            rows += 1
            if (src, r["id"], r["type"]) not in hand:
                bad += 1
    ck("every connection row has a hand-written edge behind it", bad, 0)
    ck("connection row total", c["connectionRows"], rows)
    # each edge yields exactly two rows unless an endpoint is missing
    ck("connection rows equal twice the edge count", rows, len(edges) * 2 - dangling * 2)

    # ---- the stats strip, as RENDERED -----------------------------------------
    # This is the part a reader actually reads. Pull the numbers out of the built
    # file and re-derive each from source independently.
    # The stats strip is COMPUTED AT RUNTIME, so scraping the HTML source finds
    # the code that builds it, not the number a reader sees. My first attempt did
    # exactly that and matched "5205" out of "DoDD 5205.07" for CUSTODY. Read the
    # rendered DOM text instead: tools/runtime-strip.txt is written by the browser
    # pass. If it is absent, these checks are SKIPPED AND SAID TO BE SKIPPED rather
    # than silently passing, which is the canvasInk failure this project keeps
    # relearning.
    strip_path = os.path.join(ROOT, "tools", "runtime-strip.txt")
    strip = open(strip_path, encoding="utf-8").read() if os.path.exists(strip_path) else None
    if strip is None:
        FAIL.append("stats strip: tools/runtime-strip.txt absent, so the figures a "
                    "reader actually sees were NOT verified. Run the browser pass.")

    def rendered(pat, what=None):
        """Pull one figure out of the captured DOM text.

        If the strip was captured but the figure is NOT in it, that is a FAILURE, not a
        skip. Every caller below used to guard with `if value:` and fall through in
        silence when the pattern missed, so a check could sit dead for weeks while the
        number it guarded was wrong. That is exactly what happened to
        `breadcrumb object count`: the L0 breadcrumb renders as "PROGRAM MAPSTART436
        objects", the pattern expected whitespace where "START" is, it never matched,
        and the audit reported 37 of its 38 checks as a clean run.
        """
        if strip is None:
            return None
        m = re.search(pat, strip)
        if not m:
            if what:
                FAIL.append(f"stats strip: captured, but the {what} figure is not in it "
                            f"-- the check that depends on it did not run")
            return None
        return m.group(1)

    ent_rendered = rendered(r"ENTITIES\s*(\d{3,4})", "ENTITIES")
    if ent_rendered:
        ck("stats strip ENTITIES", int(ent_rendered), len(nodes))
    else:
        FAIL.append("stats strip: could not locate the ENTITIES figure in the built file")

    links_rendered = rendered(r"SOURCED LINKS\s*(\d{3,5})", "SOURCED LINKS")
    if links_rendered:
        ck("stats strip SOURCED LINKS", int(links_rendered), len(edges))

    # claim totals
    claims = [cl for n in nodes for cl in (n.get("claims") or [])]
    ck("claim tier values are all legal",
       sorted({cl.get("tier") for cl in claims}), [1, 2, 3])
    t1 = sum(1 for cl in claims if cl.get("tier") == 1)
    documented = round(t1 / len(claims) * 100)
    dr = rendered(r"(\d{1,3})%\s*(?:</[^>]+>\s*)?of\s*(\d{3,5})\s*claims", "DOCUMENTED")
    if dr:
        m = re.search(r"(\d{1,3})%\s*(?:</[^>]+>\s*)?of\s*(\d{3,5})\s*claims", strip)
        ck("stats strip DOCUMENTED denominator", int(m.group(2)), len(claims))
        ck("stats strip DOCUMENTED percent", int(m.group(1)), documented,
           f"{t1} tier-1 of {len(claims)}")

    den = sum(1 for e in edges if e["type"] == "denial")
    dnr = rendered(r"DENIALS\s*(\d{1,4})", "DENIALS")
    if dnr:
        ck("stats strip DENIALS", int(dnr), den)
    cus = sum(1 for e in edges if e["type"] == "custody")
    cur = rendered(r"CUSTODY\s*(\d{1,4})", "CUSTODY")
    if cur:
        ck("stats strip CUSTODY", int(cur), cus)

    tr = rendered(r"TIER A\s*(\d{1,4})", "TIER A")
    if tr:
        ck("stats strip TIER A", int(tr),
           sum(1 for n in nodes if n.get("tier") == "A"))
    # The crumb renders as "PROGRAM MAPSTART110 nodes · 103 of 326 links at rest
    # · 1.00x" -- the label between "MAP" and the count is part of the breadcrumb,
    # not whitespace. It used to read "436 objects", one number covering nodes and
    # both edge kinds. The packed layout draws only the budgeted edges at rest, so
    # a single total would have told the reader they were looking at 326 links when
    # 103 are on the screen. Three figures now, and all three are checked.
    mo = (rendered(r"PROGRAM MAP\D{0,12}?(\d{2,5})\s*nodes", "PROGRAM MAP nodes")
          if strip else None)
    if mo:
        ck("breadcrumb node count", int(mo), c["l0"])
    mr = (rendered(r"(\d{1,5})\s*of\s*\d{1,5}\s*links at rest", "links at rest")
          if strip else None)
    if mr:
        # Re-derived from the layout model rather than from the number the model
        # states about itself: count the edges actually flagged `rest`.
        lay = json.load(open(os.path.join(ROOT, "data", "l0-layout-model.json"),
                             encoding="utf-8"))["current"]
        ck("breadcrumb links at rest", int(mr),
           sum(1 for e in lay["edges"] if e.get("rest")))
    mt = (rendered(r"\d{1,5}\s*of\s*(\d{1,5})\s*links at rest", "links total")
          if strip else None)
    if mt:
        ck("breadcrumb links total", int(mt),
           c["directEdges"] + c["summarisedEdges"])

    # entity class count stated in UI copy
    ncls = len({n["cls"] for n in nodes})
    words = {5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    stated = re.search(r"(Five|Six|Seven|Eight|Nine) entity classes", html)
    if stated:
        ck("UI copy: entity class count", stated.group(1), words.get(ncls),
           f"the board carries {ncls} classes")

    # ---- removals actually took ----------------------------------------------
    rm = json.load(open(os.path.join(ROOT, "research", "_removed.json"),
                        encoding="utf-8"))
    ids = {n["id"] for n in nodes}
    still = sorted(set(rm["remove"]) & ids)
    ck("approved removals are absent from the board", still, [])
    alias_live = sorted(a for a in rm.get("alias", {}) if a in ids)
    ck("collapsed ids are gone", alias_live, [])
    # and nothing still points at a collapsed id
    orphan = 0
    for e in edges:
        if e["a"] in rm.get("alias", {}) or e["b"] in rm.get("alias", {}):
            orphan += 1
    ck("no edge points at a collapsed id", orphan, 0)
    tl_orphan = sum(1 for t in b.get("timeline", [])
                    if t.get("node") and t["node"] not in ids)
    ck("no timeline event points at a missing node", tl_orphan, 0)

    # ---- the authority layer --------------------------------------------------
    auth = model.get("authority") or {}
    ck("authority nodes all exist", sorted(k for k in auth if k not in ids), [])
    nocite = sorted(k for k, v in auth.items() if not v.get("instruments"))
    ck("every authority claim cites an instrument", nocite, [])
    excluded = {"susan-gough", "christopher-sherwood", "donald-kerr", "sue-gordon"}
    ck("authority exclusions hold", sorted(excluded & set(auth)), [])

    # ---- no authored field was lost to a default -------------------------------
    # RESTATED HERE, NOT IMPORTED, and deliberately blunter than merge.py's rule.
    #
    # merge.py fills a handful of fields only when the value it already holds is
    # falsy, so for those fields the FIRST file to mention a node wins. That is
    # fine while "absent" is falsy. Two fields defaulted to a truthy value instead
    # -- `cluster` to "other" and person `status` to "active" -- and a default that
    # is indistinguishable from a real value cannot be overwritten by the file that
    # actually knows. On 19 September 2026 that had put 267 nodes in the wrong map
    # band and was reporting Harry Reid, Gerald Ford, Kenneth Arnold and Nathan
    # Twining as "active". Nothing caught it, because every value involved is
    # perfectly valid; only the PROVENANCE was wrong.
    #
    # So this check does not look at the merge rules at all. It reads the research
    # files itself, and asks one question of the shipped board: does any node carry
    # the default for one of these fields while some research file authored a real
    # value for it? If so, load order beat authorship and the reader is looking at
    # a default dressed as an editorial decision.
    import glob
    BANDS = {"legacy", "contractor", "ffrdc", "ic", "oversight", "witness",
             "research", "media", "other"}
    authored = {}          # (kind, id, field) -> set of authored values
    for path in sorted(glob.glob(os.path.join(ROOT, "research", "*.json"))):
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        for kind, field_set in (("people", ("cluster", "status")),
                                ("entities", ("cluster",))):
            for r in doc.get(kind) or []:
                rid = (r.get("id") or "").strip()
                if rid.startswith("p-"):
                    rid = rid[2:]
                for f in field_set:
                    v = r.get(f)
                    if v is None or v == "":
                        continue
                    if f == "cluster" and v not in BANDS:
                        continue          # a vocabulary this board does not use
                    authored.setdefault((kind, rid, f), set()).add(v)

    lost = []
    for kind, dflt_by_field in (("people", {"cluster": "other", "status": "active"}),
                                ("entities", {"cluster": "other"})):
        for rec in b[kind]:
            for f, dflt in dflt_by_field.items():
                want = authored.get((kind, rec["id"], f))
                if want and rec.get(f) == dflt and dflt not in want:
                    lost.append(f"{rec['id']}.{f} ships {dflt!r}, authored {sorted(want)}")
    ck("no authored cluster or status was lost to a default", sorted(lost)[:12], [],
       f"{len(lost)} node(s); a truthy default beat the file that authored the value")

    # ---- report ---------------------------------------------------------------
    print("=" * 66)
    print(f"LAYER 1 — independent re-derivation")
    print(f"  checks run    {len(PASS) + len(FAIL)}")
    print(f"  failed        {len(FAIL)}")
    print("=" * 66)
    for f in FAIL:
        print("  FAIL  " + f)
    if not FAIL:
        print("  every displayed figure re-derived from source and matched.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
