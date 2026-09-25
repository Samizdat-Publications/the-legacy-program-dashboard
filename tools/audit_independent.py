#!/usr/bin/env python3
"""
audit_independent.py — Layer 1 of the adversarial review. Jess's pass.

DELIBERATELY DOES NOT IMPORT verify.py OR build_l0.py.

verify.py is the build gate and I wrote it. An audit that runs the author's own
checks proves the author is self-consistent, not that the deliverable is right.
This file re-derives the map model's figures and the board's integrity rules from
`data/the-program.json` and the research files, using its own arithmetic, and
compares them against what `data/l0-model.json` states about itself.

It used to compare the figures RENDERED in the old single-file shell as well (the
stats strip, the breadcrumb, a class count in UI copy). That shell was retired on
25 September 2026; the app's check C27 now re-derives the figures Home prints from
the raw files the app serves, which is the same question asked of what ships.

Prints checks run / checks failed. A zero-failure run is demonstrated, not asserted.
"""

import json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")

PASS, FAIL = [], []


def ck(name, got, want, note=""):
    if got == want:
        PASS.append(name)
    else:
        FAIL.append(f"{name}: rendered/model {got!r} vs independently derived {want!r}"
                    + (f"  [{note}]" if note else ""))


def main():
    b = json.load(open(BOARD, encoding="utf-8"))
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
        # Compete on degree; ties break on file order, as the builder does. Since
        # phase 4 a node with an entity dossier outranks one without, because every
        # map node must carry one: read here straight off research/dossiers/, not
        # from the builder's model, so the rule is restated rather than agreed with.
        import glob
        with_dossier = {e.get("id") for f in glob.glob(os.path.join(ROOT, "research", "dossiers", "*.json"))
                        for e in json.load(open(f, encoding="utf-8"))
                        if (e.get("entityDossier") or {})}
        pos = {nid: k for k, nid in enumerate(eligible)}
        ranked = sorted(eligible, key=lambda i: (i not in with_dossier, -len(adj[i]), pos[i]))
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
    mism = 0
    for e in model["summarised"]:
        k = "|".join(sorted((e["a"], e["b"])))
        if k in summ and e["n"] != len(summ[k]):
            mism += 1
    ck("summarised tick counts equal shared-member counts", mism, 0)

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

    # ---- claim tiers ------------------------------------------------------------
    claims = [cl for n in nodes for cl in (n.get("claims") or [])]
    ck("claim tier values are all legal",
       sorted({cl.get("tier") for cl in claims}), [1, 2, 3])

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

    # ---- the vocabulary, restated (phase 3) -------------------------------------
    # schema/vocab.json is the one vocabulary merge.py, build_app_data.py, verify.py
    # and the app read. RESTATED here, not imported from those tools: if the file
    # drifts from what this board means by its twelve types and its person
    # statuses, the two lists disagree and this says so.
    TYPES = ["custody", "funding", "programmatic", "institutional", "legislative",
             "research", "investigative", "witness-chain", "behavioral", "denial",
             "temporal", "geographic"]
    STATUS = ["active", "dead", "former", "alive", "unknown", "deceased", "missing",
              "fabricated", "resolved"]
    vocab = json.load(open(os.path.join(ROOT, "schema", "vocab.json"), encoding="utf-8"))
    ck("schema/vocab.json names the twelve edge types, in reading order",
       [t["id"] for t in vocab["edgeTypes"]], TYPES)
    ck("schema/vocab.json names the nine person statuses in use",
       vocab["personStatus"], STATUS)
    ck("every edge on the board carries one of the twelve types",
       sorted({e["type"] for e in edges} - set(TYPES)), [])
    ck("every person status on the board is one of the nine",
       sorted({p.get("status") for p in people} - set(STATUS)), [])
    verbs = {k: v for k, v in vocab["authoredVerbs"].items() if not k.startswith("_")}
    unmapped = set()
    for path in sorted(glob.glob(os.path.join(ROOT, "research", "*.json"))):
        if os.path.basename(path) == "_edge_tiers.json":
            continue
        for x in json.load(open(path, encoding="utf-8")).get("edges") or []:
            t = x.get("type") or x.get("rel")
            if t not in TYPES and t not in verbs:
                unmapped.add(t)
    ck("every authored edge verb is a type or has a mapping", sorted(unmapped), [])
    ck("every verb mapping lands on one of the twelve types",
       sorted(k for k, v in verbs.items() if v.get("type") not in TYPES), [])
    ck("no timeline event ships the old mixed `tier` field",
       sum(1 for t in b.get("timeline", []) if "tier" in t), 0)

    # ---- report ---------------------------------------------------------------
    print("=" * 66)
    print(f"LAYER 1 — independent re-derivation")
    print(f"  checks run    {len(PASS) + len(FAIL)}")
    print(f"  failed        {len(FAIL)}")
    print("=" * 66)
    for f in FAIL:
        print("  FAIL  " + f)
    if not FAIL:
        print("  every figure re-derived from source and matched.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
