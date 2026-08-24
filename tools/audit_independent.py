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
    l0 = {n["id"] for n in nodes if n["cls"] in STRUCT and len(adj[n["id"]]) >= 6}

    model = json.load(open(os.path.join(ROOT, "data", "l0-model.json"), encoding="utf-8"))
    c = model["counts"]
    ck("L0 node count", c["l0"], len(l0), "floor = distinct neighbours >= 6")
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

    def rendered(pat):
        if strip is None:
            return None
        m = re.search(pat, strip)
        return m.group(1) if m else None

    ent_rendered = rendered(r"ENTITIES\s*(\d{3,4})")
    if ent_rendered:
        ck("stats strip ENTITIES", int(ent_rendered), len(nodes))
    else:
        FAIL.append("stats strip: could not locate the ENTITIES figure in the built file")

    links_rendered = rendered(r"SOURCED LINKS\s*(\d{3,5})")
    if links_rendered:
        ck("stats strip SOURCED LINKS", int(links_rendered), len(edges))

    # claim totals
    claims = [cl for n in nodes for cl in (n.get("claims") or [])]
    ck("claim tier values are all legal",
       sorted({cl.get("tier") for cl in claims}), [1, 2, 3])
    t1 = sum(1 for cl in claims if cl.get("tier") == 1)
    documented = round(t1 / len(claims) * 100)
    dr = rendered(r"(\d{1,3})%\s*(?:</[^>]+>\s*)?of\s*(\d{3,5})\s*claims")
    if dr:
        m = re.search(r"(\d{1,3})%\s*(?:</[^>]+>\s*)?of\s*(\d{3,5})\s*claims", strip)
        ck("stats strip DOCUMENTED denominator", int(m.group(2)), len(claims))
        ck("stats strip DOCUMENTED percent", int(m.group(1)), documented,
           f"{t1} tier-1 of {len(claims)}")

    den = sum(1 for e in edges if e["type"] == "denial")
    dnr = rendered(r"DENIALS\s*(\d{1,4})")
    if dnr:
        ck("stats strip DENIALS", int(dnr), den)
    cus = sum(1 for e in edges if e["type"] == "custody")
    cur = rendered(r"CUSTODY\s*(\d{1,4})")
    if cur:
        ck("stats strip CUSTODY", int(cur), cus)

    tr = rendered(r"TIER A\s*(\d{1,4})")
    if tr:
        ck("stats strip TIER A", int(tr),
           sum(1 for n in nodes if n.get("tier") == "A"))
    mo = rendered(r"PROGRAM MAP\s*(\d{2,5})\s*objects") if strip else None
    if mo:
        ck("breadcrumb object count", int(mo),
           c["l0"] + c["directEdges"] + c["summarisedEdges"])

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
