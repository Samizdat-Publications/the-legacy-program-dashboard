"""Supporting checks for claims in the report."""
import random
from collections import Counter, defaultdict
from g import *
B = Board()
ids, adj = B.ids, B.adj
C = rd(OUT, "s3_consensus.json")["cons"]
res = {}
# 1. containment / jaccard of each hubdamp community in all and typedamp consensus
def groups(p):
    g = defaultdict(set)
    for k, v in p.items(): g[v].add(k)
    return g
H, A, T = groups(C["hubdamp"]["part"]), groups(C["all"]["part"]), groups(C["typedamp"]["part"])
rob = {}
for h in sorted(H, key=lambda x: -len(H[x])):
    ja = max(len(H[h] & A[a]) / len(H[h] | A[a]) for a in A)
    jt = max(len(H[h] & T[t]) / len(H[h] | T[t]) for t in T)
    ca = max(len(H[h] & A[a]) / len(H[h]) for a in A)
    ct = max(len(H[h] & T[t]) / len(H[h]) for t in T)
    rob[h] = (len(H[h]), round(ja, 2), round(ca, 2), round(jt, 2), round(ct, 2))
    print("H%d" % h, rob[h])
res["robust"] = rob
# 2. edge date vs endpoint dates: equal to newer / older
eq_new = eq_old = both = 0
for e in B.edges:
    y = year_of(e["dateStart"])
    ya, yb = year_of(B.nodes[e["a"]]["dateStart"]), year_of(B.nodes[e["b"]]["dateStart"])
    if y and ya and yb:
        both += 1
        if y == max(ya, yb): eq_new += 1
        if y == min(ya, yb): eq_old += 1
res["edge_year_eq_newer"] = (eq_new, both)
res["edge_year_eq_older"] = (eq_old, both)
print("edge year == newer endpoint year", eq_new, "/", both, "; == older", eq_old)
# 3. random-pair intermediates (weighted by 1/#paths) and the edge type used to enter them
top20 = set(sorted(ids, key=lambda i: -B.deg[i])[:20])
pair_types = defaultdict(list)
for e in B.edges:
    k = (e["a"], e["b"]) if e["a"] < e["b"] else (e["b"], e["a"])
    pair_types[k].append(e["t"])
rng = random.Random(4)
Sn = [i for i in ids if B.deg[i] > 0]
inter = Counter(); enter = Counter(); n = 0
for _ in range(1000):
    a, b = rng.sample(Sn, 2)
    ps = all_shortest_paths(a, b, adj, limit=200)
    if not ps: continue
    n += 1
    w = 1 / len(ps)
    for p in ps:
        for j in range(1, len(p) - 1):
            inter[p[j]] += w
            u, v = p[j - 1], p[j]
            k = (u, v) if u < v else (v, u)
            for t in pair_types[k]:
                if v in top20:
                    enter[t] += w / len(pair_types[k])
tot = sum(inter.values())
res["random_intermediates"] = [(i, round(v / n, 3), B.nodes[i]["cls"]) for i, v in inter.most_common(15)]
res["enter_top20_types"] = [(t, round(v / sum(enter.values()), 3)) for t, v in enter.most_common()]
print("pairs", n)
print("top intermediates (expected appearances per pair):", res["random_intermediates"])
print("edge types used to step INTO a top-20 hub:", res["enter_top20_types"])
# share of all intermediate appearances that are top-20 hubs
res["share_intermediates_top20"] = sum(v for i, v in inter.items() if i in top20) / tot
print("share of intermediate appearances that are top-20 hubs", res["share_intermediates_top20"])
# 4. per-pair: does AARO Vol I appear
S9 = rd(OUT, "s9_paths.json")
for r in S9["pairs"]:
    ps = r["paths"]
    print(r["a"], r["b"], "VolI in", sum(1 for p in all_shortest_paths(r["a"], r["b"], adj, limit=500) if "aaro-historical-record-vol1" in p[1:-1]), "of", r["n_paths"])
dump("s12_checks.json", res)
