#!/usr/bin/env python3
"""
build_l0.py — precompute the L0 program-map model, and bake its layout.

    python3 tools/build_l0.py            # -> data/l0-model.json

WHAT
----
The NETWORK view draws 970 nodes and ~3,700 edges at rest and is unreadable. This
rolls the rest state up to the level of the *program* — institutions, programs,
events, legislation and documents above a connectivity floor — and reveals
individuals only when a node is opened.

This file implements SPEC.md P1 (register partition, routing, member lists),
P2 (direct-edge aggregation), P3 (shared-member edges and the >= 2 gate) and
P8 (the L0 layout bake). It is a port of the design package's reference
generator `build-l0-data.mjs`, with one deliberate correction — see DEGREE below.

DEGREE — the correction, and why it matters
-------------------------------------------
The design package's figures say the floor produces 107 L0 nodes. Its own
generator produces 96 from the same input. The difference is what "degree" means.

`data/l0-extract.json` carries a `deg` field which is an **edge-instance count**,
not a degree: 94 of the 1,685 node pairs carry more than one hand-written edge
(up to three), so those nodes are counted two and three times over. The published
figures were computed from that field. The generator recomputes degree from a set
of distinct neighbours — and carries a comment saying it does so precisely because
a stale `deg` "silently changes the L0 set." It did.

Distinct neighbours is the correct reading, and the renderer settles it: P2
aggregates every hand-written edge on a pair into ONE drawn line. A map that draws
a pair once cannot let that pair count three times toward a *connectivity* floor.

Eleven nodes qualify only under the inflated count, among them `usaf`, which the
design README uses as its worked example of the single-member refusal. Under the
correct floor `usaf` is not on the map at all.

Corrected figures, reproducible from this file:

    L0 96 · ledger 706 · path-only 55 · unattached 113
    direct edges 170 · summarised 76 · primitives 342

DETERMINISM
-----------
Every traversal iterates nodes in **file order**. BFS attachment must be stable or
routed members drift between builds and `verify.py --idempotent` fails. There is no
use of `random` anywhere: the layout is seeded from a deterministic grid.
"""

import json, math, os, sys
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")
OUT = os.path.join(ROOT, "data", "l0-model.json")

# ---------------------------------------------------------------- configuration
FLOOR = 6                      # degree floor, in DISTINCT NEIGHBOURS (see above)
PROMOTE_DOCUMENTS = True       # documents join L0 at the same floor
ROUTE_CAP = 3                  # beyond this an entity is 'path only', not a member
SHARED_GATE = 2                # minimum shared members for a summarised edge

STRUCTURAL = ("institution", "program", "event", "legislation")

# Layout. SEP is a HALF-extent and it is anisotropic on purpose: labels are wide and
# not tall, so a circular separation either wastes vertical space or leaves horizontal
# overlaps. This is the figure that decides whether labels collide.
WORLD_W, WORLD_H = 2200, 1420
SEP_X, SEP_Y = 88, 32
MARGIN = 96
STEPS = 1300
REPULSION = 9000
SPRING_DIRECT = 0.018
SPRING_SHARED = 0.005
ANCHOR_PULL = 0.013            # named clusters get a ring anchor
CENTRE_PULL = 0.0014           # the unclustered get a deliberately weaker centring
NAMED_CLUSTERS = ["legacy", "contractor", "ffrdc", "ic", "oversight",
                  "witness", "research", "media"]

# The true label box, used only to MEASURE overlap. Separation runs on the padded
# box above; measuring on the padded box would be marking your own homework.
LABEL_W, LABEL_H = 68, 20


# ---------------------------------------------------------------- load
def load_board(path=BOARD):
    b = json.load(open(path, encoding="utf-8"))
    nodes = []
    for n in b["people"] + b["entities"]:
        claims = n.get("claims") or []
        nodes.append({
            "id": n["id"], "label": n["label"], "cls": n["cls"],
            "cluster": n.get("cluster") or "other", "tier": n.get("tier"),
            "C": n.get("C"), "A": n.get("A"), "D": n.get("D"),
            "claims": len(claims),
            "t1": sum(1 for c in claims if c.get("tier") == 1),
        })
    edges = [{"a": e["a"], "b": e["b"], "t": e["type"], "ct": e["claimTier"]}
             for e in b["edges"]]
    return nodes, edges


def adjacency(nodes, edges):
    """Distinct-neighbour adjacency, insertion-ordered for determinism.

    Also returns the per-pair edge lists, which P2 aggregates. Dangling edges are
    counted and reported rather than silently dropped: verify.py has a dangling-
    reference check, so a non-zero count here means the two disagree."""
    adj = OrderedDict((n["id"], OrderedDict()) for n in nodes)
    pair = OrderedDict()
    dangling = 0
    for e in edges:
        if e["a"] not in adj or e["b"] not in adj:
            dangling += 1
            continue
        adj[e["a"]][e["b"]] = None
        adj[e["b"]][e["a"]] = None
        k = "|".join(sorted((e["a"], e["b"])))
        pair.setdefault(k, []).append(e)
    return adj, pair, dangling


# ---------------------------------------------------------------- P1: registers
def partition(nodes, adj, pair):
    is_l0_class = lambda n: n["cls"] in STRUCTURAL or (PROMOTE_DOCUMENTS and n["cls"] == "document")
    deg = {n["id"]: len(adj[n["id"]]) for n in nodes}

    # File order, not set order. BFS attachment must be reproducible.
    l0ids = [n["id"] for n in nodes if is_l0_class(n) and deg[n["id"]] >= FLOOR]
    L0 = set(l0ids)

    depth, prev = {}, {}
    queue = list(l0ids)
    for i in queue:
        depth[i] = 0
    qi = 0
    while qi < len(queue):
        u = queue[qi]; qi += 1
        for v in adj[u]:
            if v not in depth:
                depth[v] = depth[u] + 1
                prev[v] = u
                queue.append(v)

    def route_of(nid):
        chain, cur = [], nid
        while depth[cur] > 0:
            p = prev[cur]
            chain.append(p)
            cur = p
        return chain

    members = OrderedDict((i, {"direct": [], "routed": []}) for i in l0ids)
    path_only, unattached = [], []
    for n in nodes:
        nid = n["id"]
        if nid in L0:
            continue
        dp = depth.get(nid)
        if dp == 1:
            # A member of EVERY L0 node it touches, not just the nearest one.
            for v in adj[nid]:
                if v in L0:
                    members[v]["direct"].append(nid)
        elif dp is not None and dp <= ROUTE_CAP:
            chain = route_of(nid)
            members[chain[-1]]["routed"].append(
                {"id": nid, "depth": dp, "via": chain[:-1]})
        elif dp is None:
            unattached.append(nid)
        else:
            path_only.append(nid)
    return l0ids, L0, deg, depth, prev, members, path_only, unattached, route_of


# ---------------------------------------------------------------- P2 + P3: edges
def build_edges(nodes, adj, pair, L0, depth):
    """P2 aggregates the hand-written edges on each L0-L0 pair into one drawn line.
    P3 adds a summarised line between L0 nodes that share >= SHARED_GATE members.

    Only hand-written edges reach either path. A rolled-up derived edge would carry
    a count and a tier earned by nothing but a shared attribute, which is exactly the
    credibility failure the cardinality gates were introduced to prevent."""
    direct_keys = [k for k in pair
                   if k.split("|")[0] in L0 and k.split("|")[1] in L0]
    direct = []
    for k in direct_keys:
        es = pair[k]
        a, b = k.split("|")
        direct.append({
            "a": a, "b": b, "n": len(es),
            "tier": min(e["ct"] for e in es),           # strongest tier present
            "types": list(dict.fromkeys(e["t"] for e in es)),
        })
    direct_set = set(direct_keys)

    shared = OrderedDict()
    for n in nodes:
        nid = n["id"]
        if nid in L0 or depth.get(nid) != 1:
            continue
        parents = [v for v in adj[nid] if v in L0]
        for i in range(len(parents)):
            for j in range(i + 1, len(parents)):
                k = "|".join(sorted((parents[i], parents[j])))
                if k in direct_set:
                    continue
                s = shared.setdefault(k, {"via": [], "best": 9, "links": 0})
                s["via"].append(nid)
                for p in (parents[i], parents[j]):
                    for e in pair.get("|".join(sorted((p, nid))), []):
                        s["best"] = min(s["best"], e["ct"])
                        s["links"] += 1

    summarised = []
    for k, s in shared.items():
        if len(s["via"]) < SHARED_GATE:
            continue
        a, b = k.split("|")
        summarised.append({"a": a, "b": b, "n": len(s["via"]),
                           "tier": s["best"], "links": s["links"], "via": s["via"]})
    gated_out = sum(1 for s in shared.values() if len(s["via"]) < SHARED_GATE)
    return direct, summarised, gated_out


# ---------------------------------------------------------------- P8: the bake
def bake(l0ids, node_by_id, direct, summarised):
    """A settled layout over the L0 set alone.

    This is NOT precompute_layout.py with a smaller input. That bake runs the board's
    own physics over 970 nodes with cluster wells; 49 of these 96 carry cluster
    'other', including AARO, so cluster wells cannot organise this map. The
    unclustered are placed by their edges alone.

    Separation is a HARD POSITIONAL CONSTRAINT relaxed after each integration step,
    not a velocity force. A velocity force does not clear overlaps at this density —
    it leaves them and the plates sit on top of each other. This is very likely the
    same mechanism behind the parent board's 46% wall-clamp and its overlapping
    plates."""
    cx, cy = WORLD_W / 2, WORLD_H / 2
    anchors = {}
    for i, c in enumerate(NAMED_CLUSTERS):
        a = (i / len(NAMED_CLUSTERS)) * math.tau - math.pi / 2
        anchors[c] = (cx + math.cos(a) * 760, cy + math.sin(a) * 470)

    P = [{"id": i, "cluster": node_by_id[i]["cluster"], "x": 0.0, "y": 0.0,
          "vx": 0.0, "vy": 0.0} for i in l0ids]

    # Deterministic seeding. No random(): the layout must be reproducible or the
    # idempotency gate fails and screenshots stop being citable.
    unc = [p for p in P if p["cluster"] not in anchors]
    cols = max(1, math.ceil(math.sqrt(len(unc) * 1.7))) if unc else 1
    rows = max(1, math.ceil(len(unc) / cols))
    for i, p in enumerate(unc):
        r, c = divmod(i, cols)
        p["x"] = cx + (c - (cols - 1) / 2) * 150
        p["y"] = cy + (r - (rows - 1) / 2) * 110
    for i, p in enumerate([p for p in P if p["cluster"] in anchors]):
        ax, ay = anchors[p["cluster"]]
        ang = i * 2.399                      # golden angle, so seeds never coincide
        p["x"] = ax + math.cos(ang) * 150
        p["y"] = ay + math.sin(ang) * 110

    idx = {p["id"]: i for i, p in enumerate(P)}
    springs = []
    for e in direct:
        if e["a"] in idx and e["b"] in idx:
            springs.append((idx[e["a"]], idx[e["b"]], SPRING_DIRECT))
    for e in summarised:
        if e["a"] in idx and e["b"] in idx:
            springs.append((idx[e["a"]], idx[e["b"]], SPRING_SHARED))

    n = len(P)

    def separate(passes):
        """Gauss-Seidel relaxation in label-normalised space."""
        for _ in range(passes):
            for i in range(n):
                a = P[i]
                for j in range(i + 1, n):
                    b = P[j]
                    ex = (b["x"] - a["x"]) / SEP_X
                    ey = (b["y"] - a["y"]) / SEP_Y
                    el = math.hypot(ex, ey)
                    if el >= 2:
                        continue
                    if el < 1e-4:
                        ex, ey, el = 1.0, 0.0, 1e-4
                    need = (2 - el) / 2 / el
                    mx, my = ex * need * SEP_X, ey * need * SEP_Y
                    a["x"] -= mx; a["y"] -= my
                    b["x"] += mx; b["y"] += my

    alpha = 1.0
    for _ in range(STEPS):
        for i in range(n):
            a = P[i]
            for j in range(i + 1, n):
                b = P[j]
                dx, dy = b["x"] - a["x"], b["y"] - a["y"]
                d2 = dx * dx + dy * dy or 0.01
                dd = math.sqrt(d2)
                f = REPULSION / d2
                fx, fy = dx / dd * f, dy / dd * f
                a["vx"] -= fx; a["vy"] -= fy
                b["vx"] += fx; b["vy"] += fy
        for i, j, k in springs:
            a, b = P[i], P[j]
            dx, dy = b["x"] - a["x"], b["y"] - a["y"]
            a["vx"] += dx * k; a["vy"] += dy * k
            b["vx"] -= dx * k; b["vy"] -= dy * k
        for p in P:
            an = anchors.get(p["cluster"])
            if an:
                p["vx"] += (an[0] - p["x"]) * ANCHOR_PULL
                p["vy"] += (an[1] - p["y"]) * ANCHOR_PULL
            else:
                p["vx"] += (cx - p["x"]) * CENTRE_PULL
                p["vy"] += (cy - p["y"]) * CENTRE_PULL
            p["x"] += p["vx"] * alpha; p["y"] += p["vy"] * alpha
            p["vx"] *= 0.81; p["vy"] *= 0.81
        separate(1)
        alpha = max(0.06, alpha * 0.9968)

    separate(70)
    clamped = 0
    for p in P:
        bx = min(WORLD_W - MARGIN, max(MARGIN, p["x"]))
        by = min(WORLD_H - MARGIN, max(MARGIN, p["y"]))
        if abs(bx - p["x"]) > 0.5 or abs(by - p["y"]) > 0.5:
            clamped += 1
        p["x"], p["y"] = bx, by
    # Clamping can reintroduce overlaps at the walls. Alternate until both hold.
    for _ in range(6):
        separate(12)
        for p in P:
            p["x"] = min(WORLD_W - MARGIN, max(MARGIN, p["x"]))
            p["y"] = min(WORLD_H - MARGIN, max(MARGIN, p["y"]))
    for p in P:
        p["x"], p["y"] = round(p["x"]), round(p["y"])

    overlaps = 0
    for i in range(n):
        for j in range(i + 1, n):
            if math.hypot((P[i]["x"] - P[j]["x"]) / LABEL_W,
                          (P[i]["y"] - P[j]["y"]) / LABEL_H) < 2:
                overlaps += 1
    return P, clamped, overlaps



# ---------------------------------------------------------------- entity dossiers
# These are a PARALLEL dataset, deliberately not merged into the board's nodes.
# Merging 359 sourced claims onto 25 nodes would move every claim count, every tier
# mix and the whole GOLDEN manifest, and it would mix two different kinds of object:
# a node claim is a fact about the entity, an entity dossier is the ARGUMENT for why
# that entity is on this map. They are verified separately for the same reason.
#
# They live in research/dossiers/ rather than research/ because merge.py globs
# research/*.json and expects node documents.
def load_dossiers():
    import glob
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "dossiers", "*.json"))):
        for e in json.load(open(f, encoding="utf-8")):
            d = e.get("entityDossier") or {}
            prev = out.get(e["id"])
            # A duplicate is not an error: two research passes can reach the same
            # entity. Keep the better-sourced one rather than whichever sorted last.
            if prev and len(prev.get("claims", [])) >= len(d.get("claims", [])):
                continue
            out[e["id"]] = d
    return out


# ---------------------------------------------------------------- emit
def short_label(s):
    import re
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    s = re.sub(r"\s*[-—–:]\s.*$", "", s)
    return s.strip()


def build(path=BOARD):
    nodes, edges = load_board(path)
    adj, pair, dangling = adjacency(nodes, edges)
    if dangling:
        print(f"  !! {dangling} edge(s) reference a node that does not exist",
              file=sys.stderr)

    l0ids, L0, deg, depth, prev, members, path_only, unattached, route_of = \
        partition(nodes, adj, pair)
    direct, summarised, gated_out = build_edges(nodes, adj, pair, L0, depth)

    node_by_id = {n["id"]: n for n in nodes}
    dossiers = load_dossiers()
    P, clamped, overlaps = bake(l0ids, node_by_id, direct, summarised)
    pos = {p["id"]: (p["x"], p["y"]) for p in P}

    # Denial direction. Convention CONFIRMED against the merged board: `a` issued it,
    # `b` is the subject. Sample: susan-gough -> luis-elizondo, "no assigned
    # responsibilities for AATIP". Direction is the whole instrument — undirected,
    # Grusch sits beside AARO and the distinction vanishes.
    issued, received = Counter(), Counter()
    for e in edges:
        if e["t"] == "denial":
            issued[e["a"]] += 1
            received[e["b"]] += 1

    l0 = []
    for i in l0ids:
        n = node_by_id[i]
        m = members[i]
        mix = Counter(node_by_id[x]["cls"]
                      for x in m["direct"] + [r["id"] for r in m["routed"]])
        x, y = pos[i]
        l0.append({
            "id": i, "label": n["label"], "short": short_label(n["label"]),
            "cls": n["cls"], "cluster": n["cluster"], "tier": n["tier"],
            "C": n["C"], "A": n["A"], "D": n["D"], "deg": deg[i],
            "claims": n["claims"], "t1": n["t1"], "x": x, "y": y,
            "mix": dict(mix), "di": issued[i], "dr": received[i],
            "dossier": dossiers.get(i),
            "direct": m["direct"], "routed": m["routed"],
        })

    ledger = sum(1 for n in nodes
                 if n["id"] not in L0 and depth.get(n["id"]) is not None
                 and 1 <= depth[n["id"]] <= ROUTE_CAP)
    mc = sorted(len(n["direct"]) + len(n["routed"]) for n in l0)
    xs = [p["x"] for p in P]
    ys = [p["y"] for p in P]

    out = {
        "generated": __import__("datetime").date.today().isoformat(),
        "source": os.path.relpath(path, ROOT),
        "config": {
            "floor": FLOOR, "degreeIs": "distinct neighbours",
            "documentsPromoted": PROMOTE_DOCUMENTS, "routeCap": ROUTE_CAP,
            "sharedMemberGate": SHARED_GATE,
            "world": {"w": WORLD_W, "h": WORLD_H},
            "sep": {"x": SEP_X, "y": SEP_Y}, "labelDropBelowScale": 0.62,
        },
        "counts": {
            "total": len(nodes), "l0": len(L0), "ledger": ledger,
            "pathOnly": len(path_only), "unattached": len(unattached),
            "directEdges": len(direct), "summarisedEdges": len(summarised),
            "gatedOut": gated_out,
            "primitives": len(L0) + len(direct) + len(summarised),
            "wallClampPct": round(clamped / len(P) * 100, 1),
            "labelOverlaps": overlaps,
            "membersMin": mc[0], "membersMedian": mc[len(mc) // 2],
            "membersMax": mc[-1], "inert": sum(1 for v in mc if v <= 1),
            "unclusteredL0": sum(1 for n in l0 if n["cluster"] == "other"),
            "withDossier": sum(1 for n in l0 if n.get("dossier")),
            "dossierClaims": sum(len((n["dossier"] or {}).get("claims", []))
                                 for n in l0 if n.get("dossier")),
            "extent": {"w": max(xs) - min(xs), "h": max(ys) - min(ys)},
        },
        "nodes": {n["id"]: [n["label"], n["cls"], deg[n["id"]], n["tier"]]
                  for n in nodes},
        "l0": l0, "directEdges": direct, "summarised": summarised,
        "pathOnly": sorted(
            ({"id": i, "depth": depth[i], "via": route_of(i)[:-1]} for i in path_only),
            key=lambda r: r["depth"]),
        "unattached": sorted(({"id": i, "deg": deg[i]} for i in unattached),
                             key=lambda r: r["deg"]),
    }

    # The partition must be total. Fail loudly rather than emit a file that lies —
    # "nothing was left out" has to be auditable, not asserted.
    c = out["counts"]
    total = c["l0"] + c["ledger"] + c["pathOnly"] + c["unattached"]
    if total != len(nodes):
        sys.exit(f"FATAL: register partition is {total}, expected {len(nodes)}")
    return out


def main():
    out = build()
    json.dump(out, open(OUT, "w", encoding="utf-8"), separators=(",", ":"))
    c = out["counts"]
    print(f"L0 {c['l0']} · ledger {c['ledger']} · path-only {c['pathOnly']} · "
          f"unattached {c['unattached']} · edges {c['directEdges']}+{c['summarisedEdges']} "
          f"· primitives {c['primitives']} · wall-clamp {c['wallClampPct']}% "
          f"· label overlaps {c['labelOverlaps']}")
    print(f"  extent {c['extent']['w']}x{c['extent']['h']} -> {OUT}")
    if c["labelOverlaps"]:
        sys.exit("FATAL: the bake left label overlaps; separation did not converge")


if __name__ == "__main__":
    main()
