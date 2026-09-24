"""Section 7: shortest paths for reader-relevant pairs, and whether they tell a story."""
import heapq, math
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
top20 = set(sorted(ids, key=lambda i: -B.deg[i])[:20])
STRUCT = {"custody", "funding", "programmatic", "institutional", "legislative", "research"}

pair_edges = defaultdict(list)
for e in B.edges:
    k = (e["a"], e["b"]) if e["a"] < e["b"] else (e["b"], e["a"])
    pair_edges[k].append(e)


def elabel(u, v):
    k = (u, v) if u < v else (v, u)
    es = pair_edges[k]
    return "; ".join(f"[{e['t']} T{e['tier']}{' ' + str(e['dateStart'])[:4] if e['dateStart'] else ''}] {e['label']}" for e in es)


def etypes(u, v):
    k = (u, v) if u < v else (v, u)
    return [e["t"] for e in pair_edges[k]]


def sub_adj(tset):
    a2 = defaultdict(set)
    for e in B.edges:
        if e["t"] in tset:
            a2[e["a"]].add(e["b"])
            a2[e["b"]].add(e["a"])
    for i in ids:
        a2.setdefault(i, set())
    return a2


A_STRUCT = sub_adj(STRUCT)


def hub_penalised(src, dst, alpha=1.0):
    """Dijkstra where entering an intermediate node v costs 1 + alpha*log2(deg v)."""
    dist = {src: 0.0}
    prev = {}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            break
        if d > dist.get(u, 1e18):
            continue
        for v in adj[u]:
            c = 1.0 + (0 if v == dst else alpha * math.log2(max(2, B.deg[v])))
            nd = d + c
            if nd < dist.get(v, 1e18):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if dst not in dist:
        return None
    p = [dst]
    while p[-1] != src:
        p.append(prev[p[-1]])
    return p[::-1]


PAIRS = [
    ("Whistleblower to contractor", "david-grusch", "lockheed-skunk-works"),
    ("Programme to law", "aawsap", "uapda-2023"),
    ("1947 event to 2023 hearing", "roswell-1947", "hearing-2023-07-26"),
    ("Claimant to the official office", "bob-lazar", "aaro"),
    ("Legacy programme to modern office", "project-blue-book", "aaro"),
    ("Patents to contractor (extra)", "salvatore-pais", "lockheed-skunk-works"),
    ("Nuclear witness to the official office (extra)", "robert-salas", "aaro"),
    ("Wilson-Davis author to the contractor (extra)", "eric-davis", "lockheed-martin"),
]
out = []
lines = []
for title, a, b in PAIRS:
    d, n = count_shortest_paths(a, b, adj)
    paths = all_shortest_paths(a, b, adj, limit=200)
    inter = Counter(x for p in paths for x in p[1:-1])
    via_hub = sum(1 for p in paths if any(x in top20 for x in p[1:-1])) / len(paths) if paths else 0
    tcount = Counter(t for p in paths for u, v in zip(p, p[1:]) for t in etypes(u, v))
    d20, n20 = count_shortest_paths(a, b, adj, removed=top20 - {a, b})
    p20 = all_shortest_paths(a, b, adj, removed=top20 - {a, b}, limit=3)
    ds, ns = count_shortest_paths(a, b, A_STRUCT)
    ps = all_shortest_paths(a, b, A_STRUCT, limit=3)
    hp = hub_penalised(a, b)
    rec = {"title": title, "a": a, "b": b, "dist": d, "n_paths": n, "share_via_top20": via_hub,
           "intermediates": inter.most_common(10), "edge_types": tcount.most_common(),
           "paths": paths[:6], "no_top20": {"dist": d20, "n": n20, "paths": p20},
           "structural_only": {"dist": ds, "n": ns, "paths": ps}, "hub_penalised": hp}
    out.append(rec)
    lines.append(f"\n## {title}: {a} -> {b}")
    lines.append(f"distance {d}, {n} shortest paths, {via_hub:.0%} pass through a top-20 hub; intermediates {inter.most_common(8)}")
    lines.append(f"edge types on shortest paths {tcount.most_common()}")
    for p in paths[:4]:
        lines.append("  PATH: " + " > ".join(p))
        for u, v in zip(p, p[1:]):
            lines.append(f"     {u} -- {v}: {elabel(u, v)[:230]}")
    lines.append(f"  without top-20 hubs: dist {d20}, {n20} paths; e.g. {' > '.join(p20[0]) if p20 else 'none'}")
    if p20:
        for u, v in zip(p20[0], p20[0][1:]):
            lines.append(f"     {u} -- {v}: {elabel(u, v)[:200]}")
    lines.append(f"  structural types only: dist {ds}, {ns} paths; e.g. {' > '.join(ps[0]) if ps else 'none'}")
    if ps:
        for u, v in zip(ps[0], ps[0][1:]):
            lines.append(f"     {u} -- {v}: {elabel(u, v)[:200]}")
    lines.append(f"  hub-penalised path: {' > '.join(hp) if hp else 'none'}")
    if hp:
        for u, v in zip(hp, hp[1:]):
            lines.append(f"     {u} -- {v}: {elabel(u, v)[:200]}")

# aggregate: across all node pairs (sample), share of shortest paths that route through top-20
import random
rng = random.Random(4)
S = [i for i in ids if B.deg[i] > 0]
hits, tot = 0, 0
mid_types = Counter()
for _ in range(400):
    a, b = rng.sample(S, 2)
    ps = all_shortest_paths(a, b, adj, limit=50)
    if not ps:
        continue
    tot += 1
    if all(any(x in top20 for x in p[1:-1]) for p in ps):
        hits += 1
res_agg = {"sampled_pairs": tot, "all_shortest_paths_via_top20": hits / tot}
lines.append(f"\nRandom pairs: {hits}/{tot} ({hits / tot:.0%}) have EVERY shortest path passing through a top-20 hub")
dump("s9_paths.json", {"pairs": out, "agg": res_agg})
open(os.path.join(OUT, "s9_paths.txt"), "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
