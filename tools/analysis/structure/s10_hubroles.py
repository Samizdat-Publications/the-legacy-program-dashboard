"""Hub roles: containers (stars of satellites) vs provincial hubs vs connector hubs (Guimera-Amaral)."""
import statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
C = rd(OUT, "s3_consensus.json")["cons"]
P = C["hubdamp"]["part"]
S1 = rd(OUT, "s1_basics.json")
bc = {r["id"]: r["bc"] for r in S1["top20_betweenness"]}

mem = defaultdict(list)
for k, v in P.items():
    mem[v].append(k)
kin = {i: sum(1 for x in adj[i] if P[x] == P[i]) for i in ids}
z = {}
for c, m in mem.items():
    vals = [kin[i] for i in m]
    mu = statistics.mean(vals)
    sd = statistics.pstdev(vals) or 1.0
    for i in m:
        z[i] = (kin[i] - mu) / sd
part = {}
for i in ids:
    k = len(adj[i])
    if k == 0:
        part[i] = 0.0
        continue
    cnt = Counter(P[x] for x in adj[i])
    part[i] = 1 - sum((v / k) ** 2 for v in cnt.values())

rows = []
for i in sorted(ids, key=lambda i: -B.deg[i])[:30]:
    nb = adj[i]
    sat = sum(1 for x in nb if B.deg[x] <= 2) / len(nb)
    cnt = Counter(P[x] for x in nb)
    types = Counter(e["t"] for e in B.edges if i in (e["a"], e["b"]))
    role = ("container" if sat >= 0.5 else "connector hub" if part[i] >= 0.6 else "provincial hub")
    rows.append({"id": i, "cls": B.nodes[i]["cls"], "deg": B.deg[i], "sat_share": sat, "participation": part[i],
                 "z_within": z[i], "n_comms": len(cnt), "home": P[i], "home_share": cnt.get(P[i], 0) / len(nb),
                 "top_type": types.most_common(2), "role": role})
    print(f"{i:36s} {B.nodes[i]['cls']:11s} deg {B.deg[i]:3d} sat {sat:.2f} P {part[i]:.2f} z {z[i]:5.1f} comms {len(cnt):2d} home {cnt.get(P[i],0)/len(nb):.2f} {role:15s} {types.most_common(2)}")

# global role counts among nodes with deg >= 10 (Guimera-Amaral thresholds z>=2.5 hub; P thresholds)
roles = Counter()
for i in ids:
    if B.deg[i] < 5:
        continue
    hub = z[i] >= 2.5
    if hub:
        roles["connector hub (P>0.3)" if part[i] > 0.3 else "provincial hub (P<=0.3)"] += 1
    else:
        roles["non-hub connector (P>0.62)" if part[i] > 0.62 else "non-hub peripheral/ordinary"] += 1
print(roles)
# participation distribution for all nodes deg>=3
ps = [part[i] for i in ids if B.deg[i] >= 3]
print("median participation (deg>=3):", statistics.median(ps), "share P>0.5:", sum(1 for p in ps if p > 0.5) / len(ps))
dump("s10_hubroles.json", {"rows": rows, "roles": roles, "median_P_deg3": statistics.median(ps),
                           "share_P_gt_0.5": sum(1 for p in ps if p > 0.5) / len(ps)})
