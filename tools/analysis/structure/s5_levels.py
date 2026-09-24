"""Cross-variant matching of communities, and resolution sweep (coarse and fine levels)."""
import statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
C = rd(OUT, "s3_consensus.json")["cons"]


def groups(p):
    g = defaultdict(set)
    for k, v in p.items():
        g[v].add(k)
    return g


A = groups(C["all"]["part"])
H = groups(C["hubdamp"]["part"])
T = groups(C["typedamp"]["part"])
print("best Jaccard match hubdamp -> all / typedamp")
match = {}
for h in sorted(H, key=lambda x: -len(H[x])):
    ja = max(((len(H[h] & A[a]) / len(H[h] | A[a]), a) for a in A))
    jt = max(((len(H[h] & T[t]) / len(H[h] | T[t]), t) for t in T))
    # containment: share of H[h] inside its best 'all' community
    ca = max(len(H[h] & A[a]) / len(H[h]) for a in A)
    match[h] = {"size": len(H[h]), "all_best": ja[1], "jacc_all": ja[0], "contain_all": ca, "type_best": jt[1], "jacc_type": jt[0]}
    print(h, len(H[h]), f"-> all C{ja[1]} J={ja[0]:.2f} contain={ca:.2f} | typedamp C{jt[1]} J={jt[0]:.2f}")

# resolution sweep on hubdamp and all
sweep = {}
for v in ("all", "hubdamp"):
    W = weights(B, v)
    for gamma in (0.25, 0.5, 1.0, 2.0, 3.0):
        runs = [louvain(ids, W, seed=s, resolution=gamma) for s in range(12)]
        ncom = [len(set(p.values())) for p, q in runs]
        big = [sum(1 for c, n in Counter(p.values()).items() if n >= 10) for p, q in runs]
        nm = [nmi(runs[i][0], runs[j][0]) for i in range(len(runs)) for j in range(i + 1, len(runs))]
        best = max(runs, key=lambda x: x[1])
        sweep[f"{v}@{gamma}"] = {"ncom_mean": statistics.mean(ncom), "big_mean": statistics.mean(big),
                                 "nmi_mean": statistics.mean(nm), "q_best": best[1],
                                 "sizes": sorted(Counter(best[0].values()).values(), reverse=True)[:30],
                                 "part": best[0]}
        print(f"{v} gamma {gamma}: communities {statistics.mean(ncom):.1f} (>=10 nodes: {statistics.mean(big):.1f}); "
              f"NMI between runs {statistics.mean(nm):.3f}; best Q {best[1]:.3f}; sizes {sweep[f'{v}@{gamma}']['sizes'][:14]}")

# describe the coarse level (hubdamp gamma 0.5 and 0.25): top members per group
for key in ("hubdamp@0.25", "hubdamp@0.5", "all@0.5"):
    p = sweep[key]["part"]
    g = groups(p)
    print("\n==", key)
    for c in sorted(g, key=lambda x: -len(g[x])):
        if len(g[c]) < 5:
            continue
        S = g[c]
        ideg = {m: sum(1 for x in adj[m] if x in S) for m in S}
        top = sorted(S, key=lambda m: -ideg[m])[:9]
        # which hubdamp consensus communities it contains
        cont = Counter(C["hubdamp"]["part"][m] for m in S).most_common(5)
        print(f"  size {len(S)}: {', '.join(top)} | hubdamp-consensus parts {cont}")

dump("s5_levels.json", {"match": match, "sweep": {k: {kk: vv for kk, vv in v.items() if kk != 'part'} for k, v in sweep.items()},
                        "coarse_hubdamp_0.5": sweep["hubdamp@0.5"]["part"], "coarse_hubdamp_0.25": sweep["hubdamp@0.25"]["part"]})
