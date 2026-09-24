"""Section 3: Louvain communities, stability, and comparison with existing schemes."""
import math, statistics, sys
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
K0 = 10.0

ASSERT_TYPES = {"witness-chain", "behavioral", "temporal"}


def comb2(x):
    return x * (x - 1) / 2


def run_variant(variant):
    W = weights(B, variant)
    runs = []
    for s in range(SEEDS):
        p, q = louvain(ids, W, seed=s)
        runs.append((q, p))
    qs = [q for q, _ in runs]
    ncom = [len(set(p.values())) for _, p in runs]
    # pairwise NMI between runs (sample of pairs)
    nm = []
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            nm.append(nmi(runs[i][1], runs[j][1]))
    best_q, ref = max(runs, key=lambda x: x[0])
    # renumber reference by size
    sizes = Counter(ref.values())
    order = [c for c, _ in sizes.most_common()]
    ren = {c: i for i, c in enumerate(order)}
    ref = {k: ren[v] for k, v in ref.items()}
    # per-community stability: mean over runs of fraction of member pairs co-clustered
    members = defaultdict(list)
    for k, v in ref.items():
        members[v].append(k)
    stab = {}
    for c, mem in members.items():
        if len(mem) < 2:
            stab[c] = 1.0
            continue
        tot = comb2(len(mem))
        fr = []
        for _, p in runs:
            cnt = Counter(p[m] for m in mem)
            fr.append(sum(comb2(v) for v in cnt.values()) / tot)
        stab[c] = sum(fr) / len(fr)
    # node-level: fraction of runs where node shares a community with >=50% of its ref community
    node_stab = {}
    for c, mem in members.items():
        for m in mem:
            ok = 0
            for _, p in runs:
                same = sum(1 for x in mem if p[x] == p[m])
                if same >= 0.5 * len(mem):
                    ok += 1
            node_stab[m] = ok / len(runs)
    # overall pair stability: of pairs co-clustered in ref, mean fraction co-clustered across runs
    ref_pairs = sum(comb2(len(m)) for m in members.values())
    wsum = sum(stab[c] * comb2(len(m)) for c, m in members.items())
    # connectivity check of ref communities
    disconnected = []
    for c, mem in members.items():
        S = set(mem)
        sub = {m: {x for x in adj[m] if x in S} for m in mem}
        cc = components(mem, sub)
        if len(cc) > 1:
            disconnected.append((c, [len(x) for x in cc]))
    return {
        "variant": variant, "W": W, "runs": runs, "ref": ref, "best_q": best_q,
        "q_mean": statistics.mean(qs), "q_sd": statistics.pstdev(qs), "q_min": min(qs), "q_max": max(qs),
        "ncom_mean": statistics.mean(ncom), "ncom_min": min(ncom), "ncom_max": max(ncom),
        "nmi_runs_mean": statistics.mean(nm), "nmi_runs_min": min(nm),
        "stab": stab, "node_stab": node_stab, "pair_stability": wsum / ref_pairs,
        "disconnected": disconnected, "members": dict(members),
    }


results = {}
for v in ("all", "hubdamp", "typedamp"):
    results[v] = run_variant(v)
    r = results[v]
    print(f"{v}: Q best {r['best_q']:.4f} mean {r['q_mean']:.4f} sd {r['q_sd']:.4f}; communities {r['ncom_mean']:.1f} [{r['ncom_min']},{r['ncom_max']}]; "
          f"NMI between runs mean {r['nmi_runs_mean']:.3f} min {r['nmi_runs_min']:.3f}; ref pair stability {r['pair_stability']:.3f}; disconnected {r['disconnected']}")

# cross-variant agreement
for a in results:
    for b in results:
        if a < b:
            print(f"NMI ref {a} vs {b}: {nmi(results[a]['ref'], results[b]['ref']):.3f}  ARI {ari(results[a]['ref'], results[b]['ref']):.3f}")

# mean NMI across all run pairs between variants
for a in results:
    for b in results:
        if a < b:
            vals = [nmi(p1, p2) for _, p1 in results[a]["runs"][:10] for _, p2 in results[b]["runs"][:10]]
            print(f"mean NMI runs {a} x {b}: {statistics.mean(vals):.3f}")

# save compact
out = {}
for v, r in results.items():
    out[v] = {k: r[k] for k in ("best_q", "q_mean", "q_sd", "q_min", "q_max", "ncom_mean", "ncom_min", "ncom_max",
                               "nmi_runs_mean", "nmi_runs_min", "pair_stability", "disconnected")}
    out[v]["ref"] = r["ref"]
    out[v]["stab"] = r["stab"]
    out[v]["node_stab"] = r["node_stab"]
    out[v]["sizes"] = [len(r["members"][c]) for c in sorted(r["members"])]
    # all runs' partitions for later co-clustering use
    out[v]["runs"] = [p for _, p in r["runs"]]
    out[v]["run_q"] = [q for q, _ in r["runs"]]
dump("s2_partitions.json", out)
