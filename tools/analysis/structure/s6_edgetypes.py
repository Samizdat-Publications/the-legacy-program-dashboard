"""Section 4: edge-type structure, bridges, backbone candidates, type ablation."""
import statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
C = rd(OUT, "s3_consensus.json")["cons"]
PA, PH = C["all"]["part"], C["hubdamp"]["part"]
L0 = rd(REPO, "data", "l0-model.json")
l0ids = {n["id"] for n in L0["l0"]}
tierA = {i for i in ids if B.nodes[i]["tier"] == "A"}
top20 = set(sorted(ids, key=lambda i: -B.deg[i])[:20])
types = sorted(Counter(e["t"] for e in B.edges), key=lambda t: -sum(1 for e in B.edges if e["t"] == t))
res = {}


def intra_stats(part, es):
    """observed intra-community fraction and configuration-model expectation for an edge set."""
    if not es:
        return 0, 0
    intra = sum(1 for e in es if part[e["a"]] == part[e["b"]]) / len(es)
    dc = Counter()
    for e in es:
        dc[part[e["a"]]] += 1
        dc[part[e["b"]]] += 1
    tot = 2 * len(es)
    exp = sum((v / tot) ** 2 for v in dc.values())
    return intra, exp


rows = []
glob = Counter(e["t"] for e in B.edges)
hubedges = [e for e in B.edges if e["a"] in top20 or e["b"] in top20]
hubc = Counter(e["t"] for e in hubedges)
for t in types:
    es = [e for e in B.edges if e["t"] == t]
    ia, ea = intra_stats(PA, es)
    ih, eh = intra_stats(PH, es)
    rows.append({
        "type": t, "n": len(es), "share": len(es) / len(B.edges),
        "t23": sum(1 for e in es if e["tier"] > 1) / len(es),
        "t3": sum(1 for e in es if e["tier"] == 3) / len(es),
        "dated": sum(1 for e in es if year_of(e["dateStart"])) / len(es),
        "touch_top20": sum(1 for e in es if e["a"] in top20 or e["b"] in top20) / len(es),
        "hub_lift": (hubc[t] / len(hubedges)) / (len(es) / len(B.edges)),
        "intra_all": ia, "exp_all": ea, "intra_hub": ih, "exp_hub": eh,
        "nodes_touched": len({e["a"] for e in es} | {e["b"] for e in es}),
    })
res["types"] = rows
res["overall_intra_all"] = intra_stats(PA, B.edges)
res["overall_intra_hub"] = intra_stats(PH, B.edges)
print(f"{'type':14s} {'n':>5s} {'T2+3':>5s} {'T3':>4s} {'dated':>5s} {'top20':>5s} {'lift':>5s} {'intraA':>6s} {'intraH':>6s}")
for r in rows:
    print(f"{r['type']:14s} {r['n']:5d} {r['t23']:5.2f} {r['t3']:4.2f} {r['dated']:5.2f} {r['touch_top20']:5.2f} {r['hub_lift']:5.2f} {r['intra_all']:6.2f} {r['intra_hub']:6.2f}")
print("overall intra", res["overall_intra_all"], res["overall_intra_hub"])

# per-hub composition of top 10 hubs vs global (share)
comp = {}
for h in sorted(top20, key=lambda i: -B.deg[i]):
    c = Counter(e["t"] for e in B.edges if h in (e["a"], e["b"]))
    tot = sum(c.values())
    comp[h] = {t: round(c[t] / tot, 3) for t in c}
res["hub_composition"] = comp

# graph bridges (Tarjan), by type (simple graph; a pair joined by several edges is never a bridge)
import sys
sys.setrecursionlimit(10000)
disc, low, timer = {}, {}, [0]
bridges = []


def dfs(u, parent):
    disc[u] = low[u] = timer[0]
    timer[0] += 1
    for v in adj[u]:
        if v not in disc:
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:
                bridges.append((u, v))
        elif v != parent:
            low[u] = min(low[u], disc[v])


for i in ids:
    if i not in disc:
        dfs(i, None)
leafb = [b for b in bridges if B.deg[b[0]] == 1 or B.deg[b[1]] == 1]
nonleaf = [b for b in bridges if not (B.deg[b[0]] == 1 or B.deg[b[1]] == 1)]
btype = Counter()
for a, b in nonleaf:
    k = (a, b) if a < b else (b, a)
    for t in B.types_by_pair[k]:
        btype[t] += 1
res["bridges"] = {"total": len(bridges), "leaf": len(leafb), "nonleaf": len(nonleaf), "nonleaf_types": btype.most_common()}
print("bridges", res["bridges"])

# community-pair links: which types join the big hubdamp communities
pairlinks = defaultdict(Counter)
for e in B.edges:
    ca, cb = PH[e["a"]], PH[e["b"]]
    if ca != cb:
        k = (min(ca, cb), max(ca, cb))
        pairlinks[k][e["t"]] += 1
top_pairs = sorted(pairlinks.items(), key=lambda x: -sum(x[1].values()))[:15]
res["top_community_pairs_hub"] = [(k, sum(v.values()), v.most_common(3)) for k, v in top_pairs]
inter = Counter()
for v in pairlinks.values():
    inter.update(v)
res["inter_types_hub"] = inter.most_common()
print("top community pairs", res["top_community_pairs_hub"])


# ---- backbone candidates
def graph_of(tset):
    a2 = defaultdict(set)
    W = Counter()
    for e in B.edges:
        if e["t"] in tset:
            a2[e["a"]].add(e["b"])
            a2[e["b"]].add(e["a"])
            k = (e["a"], e["b"]) if e["a"] < e["b"] else (e["b"], e["a"])
            W[k] += 1
    for i in ids:
        a2.setdefault(i, set())
    return a2, W


def describe(tset, label, seeds=8):
    a2, W = graph_of(tset)
    touched = [i for i in ids if a2[i]]
    cc = components(touched, a2)
    g0 = cc[0] if cc else []
    # avg path in giant (sample of 200 sources)
    import random
    rng = random.Random(1)
    src = rng.sample(g0, min(200, len(g0)))
    t, c = 0, 0
    for s in src:
        d = bfs(s, a2)
        for k2, v in d.items():
            if k2 != s:
                t += v
                c += 1
    best = max((louvain(ids, W, seed=s) for s in range(seeds)), key=lambda x: x[1]) if W else ({}, 0)
    part = best[0]
    # NMI of backbone communities with full-graph hubdamp communities, on touched nodes
    nm = nmi(part, PH, touched) if touched else 0
    degs = sorted((len(a2[i]) for i in touched), reverse=True)
    top = sorted(touched, key=lambda i: -len(a2[i]))[:5]
    tot = sum(degs)
    out = {"label": label, "types": sorted(tset), "edges": sum(W.values()), "pairs": len(W), "nodes": len(touched),
           "node_share": len(touched) / N, "tierA_cov": len(tierA & set(touched)) / len(tierA),
           "l0_cov": len(l0ids & set(touched)) / len(l0ids), "components": len(cc), "giant": len(g0),
           "giant_share_of_touched": len(g0) / len(touched) if touched else 0,
           "avg_path_giant": t / c if c else 0, "Q": best[1], "ncom": len({part[i] for i in touched}) if touched else 0,
           "nmi_vs_full_hub": nm, "top5": [(i, len(a2[i])) for i in top],
           "top1pct_endpoint_share": sum(degs[:max(1, len(degs) // 100)]) / tot if tot else 0,
           "leaf_share": sum(1 for d in degs if d == 1) / len(degs) if degs else 0}
    return out


ALL = set(types)
cands = [
    ("PROGRAM_EDGES (custody, funding, programmatic)", {"custody", "funding", "programmatic"}),
    ("+ institutional", {"custody", "funding", "programmatic", "institutional"}),
    ("+ institutional + legislative", {"custody", "funding", "programmatic", "institutional", "legislative"}),
    ("structural 6 (+ research)", {"custody", "funding", "programmatic", "institutional", "legislative", "research"}),
    ("structural 6 + denial", {"custody", "funding", "programmatic", "institutional", "legislative", "research", "denial"}),
    ("all minus witness-chain, behavioral, temporal", ALL - {"witness-chain", "behavioral", "temporal"}),
    ("assertion layer only (witness-chain, behavioral, investigative, denial)", {"witness-chain", "behavioral", "investigative", "denial"}),
    ("all types", ALL),
]
res["backbones"] = []
for label, ts in cands:
    d = describe(ts, label)
    res["backbones"].append(d)
    print(f"{label}: edges {d['edges']} nodes {d['nodes']} ({d['node_share']:.0%}) tierA {d['tierA_cov']:.0%} L0 {d['l0_cov']:.0%} "
          f"comps {d['components']} giant {d['giant']} ({d['giant_share_of_touched']:.0%}) path {d['avg_path_giant']:.2f} Q {d['Q']:.3f} "
          f"ncom {d['ncom']} NMIfull {d['nmi_vs_full_hub']:.2f} leaf {d['leaf_share']:.2f} top {d['top5'][:3]}")

# ---- ablation: remove one type at a time
res["ablation"] = []
base = describe(ALL, "all", seeds=6)
for t in types:
    d = describe(ALL - {t}, f"minus {t}", seeds=6)
    iso_new = sum(1 for i in ids if B.deg[i] > 0) - d["nodes"]
    res["ablation"].append({"type": t, "nodes_lost": iso_new, "giant": d["giant"], "components": d["components"],
                            "avg_path": d["avg_path_giant"], "Q": d["Q"], "dQ": d["Q"] - base["Q"]})
    print(f"minus {t:14s}: nodes lost {iso_new:4d} giant {d['giant']:5d} comps {d['components']:3d} path {d['avg_path_giant']:.2f} Q {d['Q']:.3f} dQ {d['Q'] - base['Q']:+.3f}")
# only one type at a time: how many nodes does each type alone reach
res["single"] = []
for t in types:
    d = describe({t}, f"only {t}", seeds=3)
    res["single"].append({"type": t, "nodes": d["nodes"], "components": d["components"], "giant": d["giant"]})
dump("s6_edgetypes.json", res)
