"""Node-level home stability against the consensus, and topic x era matrices."""
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
C = rd(OUT, "s3_consensus.json")["cons"]
P = rd(OUT, "s2_partitions.json")
out = {}
for v in ("all", "hubdamp"):
    cons = C[v]["part"]
    runs = P[v]["runs"]
    mem = defaultdict(list)
    for k, c in cons.items():
        mem[c].append(k)
    ns = {}
    for c, m in mem.items():
        if len(m) < 2:
            continue
        for i in m:
            fr = []
            for r in runs:
                fr.append(sum(1 for x in m if x != i and r[x] == r[i]) / (len(m) - 1))
            ns[i] = sum(fr) / len(fr)
    vals = list(ns.values())
    out[v] = {"n": len(vals), "lt05": sum(1 for x in vals if x < 0.5), "ge08": sum(1 for x in vals if x >= 0.8),
              "floating_top": sorted([i for i in ns if ns[i] < 0.5], key=lambda i: -B.deg[i])[:20]}
    print(v, out[v])

ERAS = [("0", 1969), ("1", 1999), ("2", 2016), ("3", 2100)]
def era(y):
    if not y: return "nd"
    for e, hi in ERAS:
        if y <= hi: return e
    return "nd"
cons = C["hubdamp"]["part"]
mat = defaultdict(Counter)
for e in B.edges:
    y = year_of(e["dateStart"])
    ca, cb = cons[e["a"]], cons[e["b"]]
    for c in {ca, cb}:
        mat[c][era(y)] += 1
nmat = defaultdict(Counter)
for i in ids:
    nmat[cons[i]][B.nodes[i]["era"]] += 1
print("topic x edge-era (hubdamp consensus): community: [0,1,2,3,nd] edges touching it")
rows = {}
for c in sorted(mat, key=lambda c: -sum(1 for i in ids if cons[i] == c)):
    r = [mat[c][k] for k in ("0", "1", "2", "3", "nd")]
    nr = [nmat[c][k] for k in ("0", "1", "2", "3", "nd")]
    rows[c] = {"edges_by_era": r, "nodes_by_era": nr}
    print(c, r, "nodes", nr)
out["topic_era"] = rows
dump("s11_extra.json", out)
