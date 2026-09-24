"""Shared loader and graph algorithms for the B-graph structural study.

Read-only on the repo. Python stdlib only. Written 24 September 2026 for
notes/REDESIGN-2026-09-24.md; the report it produced is
notes/redesign-2026-09-24/B-GRAPH-STRUCTURE.md. Run order: s1 ... s12, then make_report.py.
Outputs go OUTSIDE the repo (STRUCTURE_OUT, else <system temp>/the-program-structure) so a
run never dirties the working tree.
"""
import json, os, random, math, tempfile
from collections import defaultdict, Counter, deque

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
APPDATA = os.path.join(REPO, "app", "public", "data")
OUT = os.environ.get("STRUCTURE_OUT") or os.path.join(tempfile.gettempdir(), "the-program-structure")
os.makedirs(OUT, exist_ok=True)


def rd(*p):
    with open(os.path.join(*p), encoding="utf-8") as f:
        return json.load(f)


class Board:
    def __init__(self):
        idx = rd(APPDATA, "index.json")
        self.index = idx
        self.nodes = {n["id"]: n for n in idx["nodes"]}
        self.ids = sorted(self.nodes)
        self.edges = rd(APPDATA, "edges.json")  # a, b, t, tier, dateStart, label
        # full board edges for note / dateEnd
        self._full = None
        missing = [e for e in self.edges if e["a"] not in self.nodes or e["b"] not in self.nodes]
        assert not missing, missing[:5]
        # simple undirected adjacency and multiplicity
        self.adj = defaultdict(set)
        self.mult = Counter()
        self.types_by_pair = defaultdict(list)
        for e in self.edges:
            a, b = e["a"], e["b"]
            if a == b:
                continue
            self.adj[a].add(b)
            self.adj[b].add(a)
            k = (a, b) if a < b else (b, a)
            self.mult[k] += 1
            self.types_by_pair[k].append(e["t"])
        for i in self.ids:
            self.adj.setdefault(i, set())
        self.deg = {i: len(self.adj[i]) for i in self.ids}          # distinct neighbours
        self.edeg = Counter()                                         # edge count incl. multi
        for e in self.edges:
            self.edeg[e["a"]] += 1
            self.edeg[e["b"]] += 1

    def full(self):
        if self._full is None:
            self._full = rd(REPO, "data", "the-program.json")
        return self._full

    def label(self, i):
        n = self.nodes.get(i)
        return (n.get("short") or n.get("label") or i) if n else i


# ---------------------------------------------------------------- basic algorithms

def components(ids, adj, removed=frozenset()):
    seen, comps = set(), []
    for s in ids:
        if s in seen or s in removed:
            continue
        comp = [s]
        seen.add(s)
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if v not in seen and v not in removed:
                    seen.add(v)
                    comp.append(v)
                    dq.append(v)
        comps.append(comp)
    comps.sort(key=len, reverse=True)
    return comps


def bfs(src, adj, removed=frozenset()):
    dist = {src: 0}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v not in dist and v not in removed:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist


def all_shortest_paths(src, dst, adj, removed=frozenset(), limit=2000):
    """All shortest paths src->dst (unweighted), capped."""
    dist = {src: 0}
    preds = defaultdict(list)
    dq = deque([src])
    while dq:
        u = dq.popleft()
        if dst in dist and dist[u] >= dist[dst]:
            break
        for v in adj[u]:
            if v in removed:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                preds[v].append(u)
                dq.append(v)
            elif dist[v] == dist[u] + 1:
                preds[v].append(u)
    if dst not in dist:
        return []
    out = []

    def walk(v, acc):
        if len(out) >= limit:
            return
        if v == src:
            out.append([src] + acc[::-1])
            return
        for p in preds[v]:
            walk(p, acc + [v])
    walk(dst, [])
    return out


def count_shortest_paths(src, dst, adj, removed=frozenset()):
    dist = {src: 0}
    sigma = Counter({src: 1})
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in adj[u]:
            if v in removed:
                continue
            if v not in dist:
                dist[v] = dist[u] + 1
                dq.append(v)
            if dist[v] == dist[u] + 1:
                sigma[v] += sigma[u]
    return dist.get(dst), sigma.get(dst, 0)


def betweenness(ids, adj):
    """Exact Brandes betweenness, unweighted, undirected (each pair counted once)."""
    bc = dict.fromkeys(ids, 0.0)
    for s in ids:
        S = []
        P = defaultdict(list)
        sigma = defaultdict(int)
        sigma[s] = 1
        d = {s: 0}
        Q = deque([s])
        while Q:
            v = Q.popleft()
            S.append(v)
            for w in adj[v]:
                if w not in d:
                    d[w] = d[v] + 1
                    Q.append(w)
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)
        delta = defaultdict(float)
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s:
                bc[w] += delta[w]
    for k in bc:
        bc[k] /= 2.0
    return bc


def kcore(ids, adj):
    deg = {i: len(adj[i]) for i in ids}
    core = {}
    remaining = set(ids)
    k = 0
    buckets = defaultdict(set)
    for i in ids:
        buckets[deg[i]].add(i)
    cur = dict(deg)
    maxd = max(deg.values()) if deg else 0
    for kk in range(0, maxd + 1):
        pass
    # simple O(n^2)-ish peeling is fine at this size
    while remaining:
        mind = min(cur[i] for i in remaining)
        k = max(k, mind)
        batch = [i for i in remaining if cur[i] <= k]
        while batch:
            for i in batch:
                if i in remaining:
                    core[i] = k
                    remaining.discard(i)
                    for j in adj[i]:
                        if j in remaining:
                            cur[j] -= 1
            batch = [i for i in remaining if cur[i] <= k]
    return core


# ---------------------------------------------------------------- Louvain

def louvain(ids, wedges, seed=0, resolution=1.0, max_levels=20):
    """Weighted Louvain. wedges: dict (a,b)->w with a<b, a!=b.
    Returns (partition dict id->community int, modularity)."""
    rng = random.Random(seed)
    idx = {v: i for i, v in enumerate(ids)}
    n = len(ids)
    adj = [defaultdict(float) for _ in range(n)]
    loops = [0.0] * n
    for (a, b), w in wedges.items():
        if w <= 0:
            continue
        ia, ib = idx[a], idx[b]
        adj[ia][ib] += w
        adj[ib][ia] += w
    k = [sum(adj[i].values()) + 2 * loops[i] for i in range(n)]
    m2 = sum(k)
    if m2 == 0:
        return {v: i for i, v in enumerate(ids)}, 0.0
    member = list(range(n))  # original node -> current super node
    level = 0
    while level < max_levels:
        level += 1
        N = len(adj)
        comm = list(range(N))
        tot = list(k)
        improved = False
        order = list(range(N))
        rng.shuffle(order)
        moved = True
        passes = 0
        while moved and passes < 100:
            moved = False
            passes += 1
            for i in order:
                ci = comm[i]
                ki = k[i]
                # weights to neighbouring communities
                wc = defaultdict(float)
                for j, w in adj[i].items():
                    if j != i:
                        wc[comm[j]] += w
                tot[ci] -= ki
                best, bestgain = ci, wc.get(ci, 0.0) - resolution * tot[ci] * ki / m2
                cands = list(wc.items())
                rng.shuffle(cands)
                for c, w in cands:
                    g = w - resolution * tot[c] * ki / m2
                    if g > bestgain + 1e-12:
                        best, bestgain = c, g
                tot[best] += ki
                if best != ci:
                    comm[i] = best
                    moved = True
                    improved = True
        if not improved:
            break
        # renumber
        ren = {}
        for c in comm:
            if c not in ren:
                ren[c] = len(ren)
        comm = [ren[c] for c in comm]
        M = len(ren)
        nadj = [defaultdict(float) for _ in range(M)]
        nloops = [0.0] * M
        for i in range(N):
            nloops[comm[i]] += loops[i]
            for j, w in adj[i].items():
                if i < j:
                    if comm[i] == comm[j]:
                        nloops[comm[i]] += w
                    else:
                        nadj[comm[i]][comm[j]] += w
                        nadj[comm[j]][comm[i]] += w
        nk = [0.0] * M
        for i in range(N):
            nk[comm[i]] += k[i]
        member = [comm[s] for s in member]
        adj, loops, k = nadj, nloops, nk
        if M == N:
            break
    part = {ids[i]: member[i] for i in range(n)}
    return part, modularity(part, wedges, resolution)


def modularity(part, wedges, resolution=1.0):
    m = 0.0
    inside = Counter()
    degc = Counter()
    for (a, b), w in wedges.items():
        if w <= 0:
            continue
        m += w
        degc[part[a]] += w
        degc[part[b]] += w
        if part[a] == part[b]:
            inside[part[a]] += w
    if m == 0:
        return 0.0
    q = 0.0
    for c in degc:
        q += inside[c] / m - resolution * (degc[c] / (2 * m)) ** 2
    return q


def nmi(p1, p2, keys=None):
    """NMI (arithmetic normalisation) between two labelings over common keys."""
    if keys is None:
        keys = [k for k in p1 if k in p2]
    n = len(keys)
    if n == 0:
        return float("nan")
    c1 = Counter(p1[k] for k in keys)
    c2 = Counter(p2[k] for k in keys)
    c12 = Counter((p1[k], p2[k]) for k in keys)
    h1 = -sum(v / n * math.log(v / n) for v in c1.values())
    h2 = -sum(v / n * math.log(v / n) for v in c2.values())
    mi = 0.0
    for (a, b), v in c12.items():
        mi += v / n * math.log((v / n) / ((c1[a] / n) * (c2[b] / n)))
    if h1 + h2 == 0:
        return 1.0
    return 2 * mi / (h1 + h2)


def ari(p1, p2, keys=None):
    if keys is None:
        keys = [k for k in p1 if k in p2]
    n = len(keys)
    c12 = Counter((p1[k], p2[k]) for k in keys)
    a = Counter(p1[k] for k in keys)
    b = Counter(p2[k] for k in keys)
    comb = lambda x: x * (x - 1) / 2
    sij = sum(comb(v) for v in c12.values())
    sa = sum(comb(v) for v in a.values())
    sb = sum(comb(v) for v in b.values())
    exp = sa * sb / comb(n)
    mx = (sa + sb) / 2
    return (sij - exp) / (mx - exp) if mx != exp else 1.0


def year_of(s):
    if not s:
        return None
    s = str(s)
    try:
        y = int(s[:4])
        return y if 1000 < y < 2200 else None
    except ValueError:
        return None


def dump(name, obj):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


# ---------------------------------------------------------------- edge weightings
K0 = 10.0
ASSERT_TYPES = {"witness-chain", "behavioral", "temporal"}


def weights(B, variant, types=None):
    """Undirected pair weights. 'all': 1 per sourced edge. 'hubdamp': each edge scaled by
    1/sqrt(max(1,ka/10)*max(1,kb/10)) with k = distinct-neighbour degree. 'typedamp':
    witness-chain, behavioral, temporal edges at 0.3. types: optional whitelist of edge types."""
    w = Counter()
    for e in B.edges:
        if types is not None and e["t"] not in types:
            continue
        a, b = e["a"], e["b"]
        k = (a, b) if a < b else (b, a)
        if variant == "all":
            w[k] += 1.0
        elif variant == "hubdamp":
            ka, kb = B.deg[a], B.deg[b]
            w[k] += 1.0 / math.sqrt(max(1.0, ka / K0) * max(1.0, kb / K0))
        elif variant == "typedamp":
            w[k] += 0.3 if e["t"] in ASSERT_TYPES else 1.0
        else:
            raise ValueError(variant)
    return w
