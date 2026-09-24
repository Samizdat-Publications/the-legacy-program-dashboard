"""Consensus clustering over the Louvain runs, null-model modularity, and community profiles."""
import math, random, statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
P = rd(OUT, "s2_partitions.json")


def coassoc(runs):
    D = Counter()
    R = len(runs)
    for p in runs:
        groups = defaultdict(list)
        for k, v in p.items():
            groups[v].append(k)
        for mem in groups.values():
            mem.sort()
            for i in range(len(mem)):
                a = mem[i]
                for j in range(i + 1, len(mem)):
                    D[(a, mem[j])] += 1
    return {k: v / R for k, v in D.items()}


def consensus(runs, tau=0.5, seeds=30, max_iter=10):
    cur = runs
    for it in range(max_iter):
        D = coassoc(cur)
        W = {k: v for k, v in D.items() if v >= tau}
        new = []
        for s in range(seeds):
            p, q = louvain(ids, W, seed=1000 + s)
            new.append(p)
        agree = min(nmi(new[0], x) for x in new[1:])
        cur = new
        if agree > 0.999:
            return new[0], it + 1, agree
    return cur[0], max_iter, agree


cons = {}
for v in ("all", "hubdamp", "typedamp"):
    runs = P[v]["runs"]
    p, iters, agree = consensus(runs)
    # renumber by size
    sizes = Counter(p.values())
    ren = {c: i for i, (c, _) in enumerate(sizes.most_common())}
    p = {k: ren[x] for k, x in p.items()}
    W = weights(B, v)
    q = modularity(p, W)
    # stability of each consensus community against the raw runs
    mem = defaultdict(list)
    for k, x in p.items():
        mem[x].append(k)
    stab = {}
    for c, m in mem.items():
        if len(m) < 2:
            stab[c] = 1.0
            continue
        tot = len(m) * (len(m) - 1) / 2
        fr = []
        for r in runs:
            cnt = Counter(r[x] for x in m)
            fr.append(sum(n * (n - 1) / 2 for n in cnt.values()) / tot)
        stab[c] = sum(fr) / len(fr)
    cons[v] = {"part": p, "iters": iters, "agree": agree, "q": q, "stab": stab,
               "sizes": [len(mem[c]) for c in sorted(mem)],
               "nmi_to_ref": nmi(p, P[v]["ref"])}
    print(f"{v}: consensus iters {iters} agree {agree:.3f} Q {q:.4f} (best raw {P[v]['best_q']:.4f}); "
          f"{len(mem)} communities; sizes {cons[v]['sizes'][:25]}; NMI to best raw {cons[v]['nmi_to_ref']:.3f}")

for a in cons:
    for b in cons:
        if a < b:
            print(f"consensus NMI {a} vs {b}: {nmi(cons[a]['part'], cons[b]['part']):.3f}  ARI {ari(cons[a]['part'], cons[b]['part']):.3f}")

# ---- null model: degree-preserving rewiring of the simple graph
simple = list(B.mult.keys())


def rewire(edges, nswap, rng):
    E = [list(e) for e in edges]
    S = set(tuple(sorted(e)) for e in E)
    done = 0
    tries = 0
    while done < nswap and tries < nswap * 20:
        tries += 1
        i, j = rng.randrange(len(E)), rng.randrange(len(E))
        if i == j:
            continue
        a, b = E[i]
        c, d = E[j]
        if rng.random() < 0.5:
            c, d = d, c
        if len({a, b, c, d}) < 4:
            continue
        e1, e2 = tuple(sorted((a, d))), tuple(sorted((c, b)))
        if e1 in S or e2 in S:
            continue
        S.discard(tuple(sorted((a, b))))
        S.discard(tuple(sorted((c, d))))
        S.add(e1)
        S.add(e2)
        E[i] = [a, d]
        E[j] = [c, b]
        done += 1
    return [tuple(sorted(e)) for e in E]


rng = random.Random(11)
nullq = []
for rep in range(8):
    E2 = rewire(simple, 10 * len(simple), rng)
    W2 = {e: 1.0 for e in E2}
    best = max(louvain(ids, W2, seed=s)[1] for s in range(5))
    nullq.append(best)
Wsimple = {e: 1.0 for e in simple}
realq_simple = max(louvain(ids, Wsimple, seed=s)[1] for s in range(10))
print(f"null-model Q (degree-preserving rewiring, simple graph): mean {statistics.mean(nullq):.4f} sd {statistics.pstdev(nullq):.4f} max {max(nullq):.4f}; real simple-graph Q {realq_simple:.4f}")

dump("s3_consensus.json", {"cons": cons, "nullq": nullq, "realq_simple": realq_simple})
