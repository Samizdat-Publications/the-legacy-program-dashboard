"""Community profiles and crosstabs against cluster, class, era, L0 band."""
import random, statistics, sys
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
C = rd(OUT, "s3_consensus.json")["cons"]
P = rd(OUT, "s2_partitions.json")
L0M = rd(REPO, "data", "l0-model.json")
TL = rd(APPDATA, "timeline.json")

variant = sys.argv[1] if len(sys.argv) > 1 else "all"
part = C[variant]["part"]
stab = {int(k): v for k, v in C[variant]["stab"].items()}

# L0 homes
l0ids = {n["id"] for n in L0M["l0"]}
band = {i: B.nodes[i]["band"] for i in ids if B.nodes[i]["band"]}
home = defaultdict(set)
for n in L0M["l0"]:
    for d in n.get("direct") or []:
        home[d].add(n["id"])
    for r in n.get("routed") or []:
        home[r["id"]].add(n["id"])  # routed only if not direct; overlap is 0 by construction
homeband = {}
for i in ids:
    if i in l0ids:
        homeband[i] = band.get(i)
    elif home.get(i):
        cnt = Counter(band[h] for h in home[i] if h in band)
        if cnt:
            homeband[i] = cnt.most_common(1)[0][0]

# timeline by node
tl_by_node = defaultdict(list)
for t in TL:
    if t.get("node"):
        y = year_of(t.get("date"))
        if y:
            tl_by_node[t["node"]].append(y)

members = defaultdict(list)
for k, v in part.items():
    members[v].append(k)


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    return xs[min(len(xs) - 1, int(round(p * (len(xs) - 1))))]


profiles = []
for c in sorted(members, key=lambda x: -len(members[x])):
    mem = members[c]
    S = set(mem)
    ideg = {m: sum(1 for x in adj[m] if x in S) for m in mem}
    top = sorted(mem, key=lambda m: (-ideg[m], -B.deg[m]))[:10]
    cls = Counter(B.nodes[m]["cls"] for m in mem)
    clu = Counter(B.nodes[m]["cluster"] for m in mem)
    tiers = Counter(B.nodes[m]["tier"] for m in mem)
    eras = Counter(B.nodes[m]["era"] for m in mem)
    # internal and boundary edges by type
    itypes, btypes = Counter(), Counter()
    idates = []
    for e in B.edges:
        a, b = e["a"], e["b"]
        if a in S and b in S:
            itypes[e["t"]] += 1
            y = year_of(e["dateStart"])
            if y:
                idates.append(y)
        elif a in S or b in S:
            btypes[e["t"]] += 1
    nyears = []
    for m in mem:
        n = B.nodes[m]
        y0 = year_of(n.get("dateStart"))
        if y0:
            nyears.append(y0)
    tyears = [y for m in mem for y in tl_by_node.get(m, [])]
    ext = Counter()
    for m in mem:
        for x in adj[m]:
            if x not in S:
                ext[part[x]] += 1
    l0in = [m for m in mem if m in l0ids]
    hb = Counter(homeband.get(m) for m in mem if homeband.get(m))
    profiles.append({
        "id": c, "size": len(mem), "stability": stab.get(c),
        "internal_edges": sum(itypes.values()), "boundary_edges": sum(btypes.values()),
        "conductance": (sum(btypes.values()) / (2 * sum(itypes.values()) + sum(btypes.values()))) if (sum(itypes.values()) + sum(btypes.values())) else 0.0,
        "top": [(m, ideg[m], B.deg[m], B.nodes[m]["cls"]) for m in top],
        "cls": cls.most_common(), "cluster": clu.most_common(), "tier": sorted(tiers.items()),
        "era": eras.most_common(), "itypes": itypes.most_common(), "btypes": btypes.most_common(5),
        "node_year_p10_p50_p90": (pct(nyears, .1), pct(nyears, .5), pct(nyears, .9)), "n_dated_nodes": len(nyears),
        "edge_year_p10_p50_p90": (pct(idates, .1), pct(idates, .5), pct(idates, .9)),
        "timeline_year_p10_p50_p90": (pct(tyears, .1), pct(tyears, .5), pct(tyears, .9)), "n_tl": len(tyears),
        "l0_members": l0in, "home_band": hb.most_common(),
        "neighbours": ext.most_common(4),
        "members": sorted(mem, key=lambda m: -ideg[m]),
    })

# ---- crosstab / NMI
def lab(attr):
    return {i: B.nodes[i][attr] for i in ids}


def nmi_null(p, q, keys, reps=30):
    rng = random.Random(5)
    vals = [q[k] for k in keys]
    out = []
    for _ in range(reps):
        rng.shuffle(vals)
        out.append(nmi(p, dict(zip(keys, vals)), keys))
    return statistics.mean(out)


cmp = {}
for name, q in (("cluster", lab("cluster")), ("cls", lab("cls")), ("era", lab("era")), ("tier", lab("tier"))):
    cmp[name] = (nmi(part, q, ids), nmi_null(part, q, ids), ari(part, q, ids))
k_l0 = [i for i in ids if i in l0ids]
cmp["L0band_on_L0nodes"] = (nmi(part, band, k_l0), nmi_null(part, band, k_l0), ari(part, band, k_l0))
k_hb = [i for i in ids if homeband.get(i)]
cmp["L0homeband_all"] = (nmi(part, homeband, k_hb), nmi_null(part, homeband, k_hb), ari(part, homeband, k_hb))
# L0 home node (the actual L0 grouping unit), single-home nodes only
single = {i: next(iter(home[i])) for i in ids if len(home.get(i, ())) == 1}
for i in l0ids:
    single[i] = i
k_s = list(single)
cmp["L0homenode_singlehome"] = (nmi(part, single, k_s), nmi_null(part, single, k_s), ari(part, single, k_s))
# baseline: cluster vs L0 band on L0 nodes
cmp["_cluster_vs_L0band_on_L0nodes"] = (nmi(lab("cluster"), band, k_l0), None, None)
cmp["_cluster_vs_cls"] = (nmi(lab("cluster"), lab("cls"), ids), None, None)

# crosstab community x cluster (counts), community x homeband
ct_cluster = {c: dict(Counter(B.nodes[m]["cluster"] for m in members[c])) for c in members}
ct_band = {c: dict(Counter(homeband.get(m, "none") for m in members[c])) for c in members}
# purity: for each cluster, share in its largest community
purity_cluster = {}
byclu = defaultdict(list)
for i in ids:
    byclu[B.nodes[i]["cluster"]].append(part[i])
for k, v in byclu.items():
    cnt = Counter(v)
    purity_cluster[k] = (len(v), cnt.most_common(1)[0][1] / len(v), len(cnt))
byband = defaultdict(list)
for i in k_hb:
    byband[homeband[i]].append(part[i])
purity_band = {k: (len(v), Counter(v).most_common(1)[0][1] / len(v), len(set(v))) for k, v in byband.items()}

dump(f"s4_profiles_{variant}.json", {"profiles": profiles, "cmp": cmp, "ct_cluster": ct_cluster, "ct_band": ct_band,
                                      "purity_cluster": purity_cluster, "purity_band": purity_band})

for p in profiles:
    print(f"\n### C{p['id']} size {p['size']} stab {p['stability']:.2f} int {p['internal_edges']} bnd {p['boundary_edges']} cond {p['conductance']:.2f}")
    print("  top:", ", ".join(f"{m}({d}/{k})" for m, d, k, _ in p["top"]))
    print("  cls:", p["cls"][:5], " cluster:", p["cluster"][:4])
    print("  itypes:", p["itypes"][:5], " era:", p["era"])
    print("  years node", p["node_year_p10_p50_p90"], "edge", p["edge_year_p10_p50_p90"], "tl", p["timeline_year_p10_p50_p90"], p["n_tl"])
    print("  L0 members:", p["l0_members"][:14], " homeband:", p["home_band"][:4])
    print("  more members:", ", ".join(p["members"][10:40]))
print()
for k, v in cmp.items():
    print(k, v)
print("purity cluster", purity_cluster)
print("purity band", purity_band)
