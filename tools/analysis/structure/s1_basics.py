"""Sections 1 and 2: basics and the hairball effect."""
import random, statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
pairs = len(B.mult)
res = {}

# ---- basics
comps = components(ids, adj)
res["N"] = N
res["edges_multi"] = len(B.edges)
res["pairs"] = pairs
res["multi_pairs"] = sum(1 for v in B.mult.values() if v > 1)
res["density"] = 2 * pairs / (N * (N - 1))
res["mean_deg"] = 2 * pairs / N
res["components"] = [len(c) for c in comps]
res["component_members_small"] = [c for c in comps[1:]]
degs = [B.deg[i] for i in ids]
res["isolated"] = [i for i in ids if B.deg[i] == 0]
res["leaves"] = sum(1 for d in degs if d == 1)
res["leaf_share"] = res["leaves"] / N
res["deg2"] = sum(1 for d in degs if d == 2)
res["deg_le2_share"] = sum(1 for d in degs if d <= 2) / N
res["median_deg"] = statistics.median(degs)
res["max_deg"] = max(degs)
# index deg agreement
res["index_deg_mismatch"] = sum(1 for i in ids if B.nodes[i]["deg"] != B.deg[i])

# degree distribution histogram
bins = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 9), (10, 19), (20, 49), (50, 99), (100, 10**6)]
hist = []
for lo, hi in bins:
    hist.append({"bin": f"{lo}-{hi}" if hi < 10**6 else f"{lo}+", "n": sum(1 for d in degs if lo <= d <= hi)})
res["deg_hist"] = hist

# by class
bycls = defaultdict(list)
for i in ids:
    bycls[B.nodes[i]["cls"]].append(B.deg[i])
res["by_class"] = []
for c, ds in sorted(bycls.items(), key=lambda x: -len(x[1])):
    ds2 = sorted(ds)
    res["by_class"].append({"cls": c, "n": len(ds), "mean": sum(ds) / len(ds), "median": statistics.median(ds),
                            "p90": ds2[int(0.9 * (len(ds2) - 1))], "max": max(ds),
                            "leaves": sum(1 for d in ds if d == 1), "leaf_share": sum(1 for d in ds if d == 1) / len(ds),
                            "sum_deg_share": sum(ds) / sum(degs)})
# by cluster
byclu = defaultdict(list)
for i in ids:
    byclu[B.nodes[i]["cluster"]].append(B.deg[i])
res["by_cluster"] = [{"cluster": c, "n": len(ds), "mean": sum(ds) / len(ds), "median": statistics.median(ds), "max": max(ds)}
                     for c, ds in sorted(byclu.items(), key=lambda x: -len(x[1]))]
# by tier
bytier = defaultdict(list)
for i in ids:
    bytier[B.nodes[i]["tier"]].append(B.deg[i])
res["by_tier"] = [{"tier": c, "n": len(ds), "mean": sum(ds) / len(ds), "median": statistics.median(ds)}
                  for c, ds in sorted(bytier.items())]

# concentration: share of edge endpoints held by top 1%, 5%, 10% nodes
sd = sorted(degs, reverse=True)
tot = sum(sd)
res["endpoint_share_top"] = {f"top{p}pct": sum(sd[:max(1, int(N * p / 100))]) / tot for p in (1, 2, 5, 10, 20)}
# gini
cum = 0
s_asc = sorted(degs)
g = sum((2 * (i + 1) - N - 1) * d for i, d in enumerate(s_asc)) / (N * sum(s_asc))
res["deg_gini"] = g
# share of edges (pairs) that touch a top-20 hub
top = sorted(ids, key=lambda i: -B.deg[i])
top10, top20, top50 = top[:10], top[:20], top[:50]
for name, T in (("top10", set(top10)), ("top20", set(top20)), ("top50", set(top50))):
    res[f"pairs_touching_{name}"] = sum(1 for (a, b) in B.mult if a in T or b in T) / pairs

# ---- k-core
core = kcore(ids, adj)
kmax = max(core.values())
res["kcore_max"] = kmax
res["kcore_hist"] = sorted(Counter(core.values()).items())
res["kcore_top_members"] = sorted([i for i in ids if core[i] == kmax], key=lambda i: -B.deg[i])

# ---- hubs
bc = betweenness(ids, adj)
norm = (N - 1) * (N - 2) / 2
res["top20"] = []
for i in top20:
    n = B.nodes[i]
    tcount = Counter()
    for e in B.edges:
        if e["a"] == i or e["b"] == i:
            tcount[e["t"]] += 1
    res["top20"].append({"id": i, "label": n["label"], "cls": n["cls"], "cluster": n["cluster"], "tier": n["tier"],
                         "l0": n["l0"], "deg": B.deg[i], "edeg": B.edeg[i], "bc": bc[i] / norm,
                         "types": tcount.most_common(4)})
top_bc = sorted(ids, key=lambda i: -bc[i])[:20]
res["top20_betweenness"] = [{"id": i, "cls": B.nodes[i]["cls"], "deg": B.deg[i], "bc": bc[i] / norm} for i in top_bc]
res["bc_share_top10deg"] = sum(bc[i] for i in top10) / sum(bc.values())
res["bc_share_top20deg"] = sum(bc[i] for i in top20) / sum(bc.values())

# reach of hubs within 1 and 2 hops
reach = []
u1, u2 = set(), set()
for i in top10:
    d = bfs(i, adj)
    r1 = {k for k, v in d.items() if v <= 1}
    r2 = {k for k, v in d.items() if v <= 2}
    u1 |= r1
    u2 |= r2
    reach.append({"id": i, "hop1": len(r1) / N, "hop2": len(r2) / N, "cum_hop1": len(u1) / N, "cum_hop2": len(u2) / N})
res["hub_reach"] = reach

# ---- path lengths (giant component)
giant = set(comps[0])
dist_hist = Counter()
ecc = {}
tot_d = 0
cnt = 0
for s in giant:
    d = bfs(s, adj)
    ecc[s] = max(d.values())
    for t, v in d.items():
        if t != s:
            dist_hist[v] += 1
            tot_d += v
            cnt += 1
res["giant"] = len(giant)
res["avg_path"] = tot_d / cnt
res["diameter"] = max(ecc.values())
res["radius"] = min(ecc.values())
res["center"] = sorted([s for s in giant if ecc[s] == res["radius"]], key=lambda i: -B.deg[i])[:10]
res["dist_hist"] = sorted((k, v / cnt) for k, v in dist_hist.items())
res["pairs_within_2"] = sum(v for k, v in dist_hist.items() if k <= 2) / cnt
res["pairs_within_3"] = sum(v for k, v in dist_hist.items() if k <= 3) / cnt
res["pairs_within_4"] = sum(v for k, v in dist_hist.items() if k <= 4) / cnt

# share of all shortest paths (pairs) that pass through at least one of top10
# measured as: pairs whose distance increases when top10 are removed
def avg_path_without(removed):
    rem = set(removed)
    cc = components(ids, adj, rem)
    g0 = set(cc[0])
    t, c = 0, 0
    longer = 0
    disconnected = 0
    base_pairs = 0
    for s in g0:
        d = bfs(s, adj, rem)
        for k2, v in d.items():
            if k2 != s:
                t += v
                c += 1
    return cc, (t / c if c else 0)

frag = {}
for label, R in (("top10", top10), ("top20", top20), ("top50", top50), ("top10_bc", top_bc[:10]), ("top20_bc", top_bc)):
    cc, ap = avg_path_without(R)
    rem = N - len(R)
    frag[label] = {"removed": len(R), "components": len(cc), "giant": len(cc[0]), "giant_share_of_remaining": len(cc[0]) / rem,
                   "isolated_after": sum(1 for c in cc if len(c) == 1), "second": len(cc[1]) if len(cc) > 1 else 0,
                   "sizes_top8": [len(c) for c in cc[:8]], "avg_path_giant": ap}
# random baseline
rnd = random.Random(7)
for kk in (10, 20, 50):
    gs, comps_n, iso, aps = [], [], [], []
    for rep in range(20):
        R = rnd.sample(ids, kk)
        cc = components(ids, adj, set(R))
        gs.append(len(cc[0]) / (N - kk))
        comps_n.append(len(cc))
        iso.append(sum(1 for c in cc if len(c) == 1))
    frag[f"random{kk}"] = {"removed": kk, "giant_share_of_remaining_mean": sum(gs) / len(gs),
                           "components_mean": sum(comps_n) / len(comps_n), "isolated_mean": sum(iso) / len(iso)}
res["fragmentation"] = frag

# what the top-10 removal isolates: by class
cc10 = components(ids, adj, set(top10))
g10 = set(cc10[0])
cut_off = [i for i in ids if i not in g10 and i not in top10]
res["cut_by_top10_n"] = len(cut_off)
res["cut_by_top10_cls"] = Counter(B.nodes[i]["cls"] for i in cut_off).most_common()
cc20 = components(ids, adj, set(top20))
g20 = set(cc20[0])
cut20 = [i for i in ids if i not in g20 and i not in top20]
res["cut_by_top20_n"] = len(cut20)
res["cut_by_top20_cls"] = Counter(B.nodes[i]["cls"] for i in cut20).most_common()
# nodes whose ONLY neighbours are top-20 hubs (pure satellites)
sat = [i for i in ids if B.deg[i] > 0 and i not in top20 and all(j in set(top20) for j in adj[i])]
res["satellites_of_top20"] = len(sat)
res["satellites_cls"] = Counter(B.nodes[i]["cls"] for i in sat).most_common()
# leaf parents: who do the degree-1 nodes hang off?
leafpar = Counter()
for i in ids:
    if B.deg[i] == 1:
        leafpar[next(iter(adj[i]))] += 1
res["leaf_parents_top15"] = [(k, v, B.nodes[k]["cls"]) for k, v in leafpar.most_common(15)]
res["leaves_on_top20"] = sum(v for k, v in leafpar.items() if k in set(top20))

dump("s1_basics.json", res)
print(json.dumps({k: v for k, v in res.items() if k not in ("component_members_small",)}, indent=1, ensure_ascii=False)[:12000])
