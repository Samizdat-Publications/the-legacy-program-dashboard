"""Section 5: time. Edge dating, era slicing, cross-era edges."""
import re, statistics
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
full = B.full()
TL = rd(APPDATA, "timeline.json")
C = rd(OUT, "s3_consensus.json")["cons"]
PH = C["hubdamp"]["part"]

ERAS = [("0", None, 1969, "through 1969"), ("1", 1970, 1999, "1970-1999"), ("2", 2000, 2016, "2000-2016"), ("3", 2017, 2100, "2017-2026")]


def era_of_year(y):
    if y is None:
        return "nd"
    for eid, lo, hi, _ in ERAS:
        if (lo is None or y >= lo) and y <= hi:
            return eid
    return "nd"


# full-board edges keyed for note text
fkey = {}
for e in full["edges"]:
    fkey.setdefault((e["a"], e["b"], e["type"]), []).append(e)
YEAR = re.compile(r"\b(1[6-9]\d\d|20[0-2]\d)\b")

res = {}
n = len(B.edges)
edate = [year_of(e["dateStart"]) for e in B.edges]
node_y = {i: year_of(B.nodes[i].get("dateStart")) for i in ids}
node_y_end = {i: year_of(B.nodes[i].get("dateEnd")) for i in ids}
both_nodes = [bool(node_y[e["a"]] and node_y[e["b"]]) for e in B.edges]
note_year = []
for e in B.edges:
    fe = fkey.get((e["a"], e["b"], e["t"])) or fkey.get((e["b"], e["a"], e["t"])) or []
    txt = " ".join((x.get("note") or "") + " " + (x.get("label") or "") for x in fe) + " " + (e.get("label") or "")
    note_year.append(bool(YEAR.search(txt)))
res["edges"] = n
res["edge_dated"] = sum(1 for y in edate if y)
res["both_endpoints_dated"] = sum(both_nodes)
res["edge_or_both"] = sum(1 for y, b in zip(edate, both_nodes) if y or b)
res["note_has_year"] = sum(note_year)
res["any_date_signal"] = sum(1 for y, b, t in zip(edate, both_nodes, note_year) if y or b or t)
res["no_date_signal"] = n - res["any_date_signal"]
# precision of edge dates
prec = Counter()
for e in B.edges:
    d = e["dateStart"]
    if d:
        prec[{4: "year", 7: "month", 10: "day"}.get(len(str(d)), "other")] += 1
res["edge_date_precision"] = dict(prec)
res["node_dated"] = sum(1 for i in ids if node_y[i])
res["node_dated_by_cls"] = {c: (sum(1 for i in ids if B.nodes[i]["cls"] == c and node_y[i]), sum(1 for i in ids if B.nodes[i]["cls"] == c))
                            for c in sorted({B.nodes[i]["cls"] for i in ids})}

# edge date vs endpoint dates
later, within, earlier = 0, 0, 0
lag = []
for e, y in zip(B.edges, edate):
    ya, yb = node_y[e["a"]], node_y[e["b"]]
    if y and ya and yb:
        lo, hi = min(ya, yb), max(ya, yb)
        if y > hi:
            later += 1
        elif y < lo:
            earlier += 1
        else:
            within += 1
        lag.append(y - lo)
res["edge_date_vs_nodes"] = {"after_both_starts": later, "between": within, "before_both": earlier,
                             "median_gap_from_older_endpoint": statistics.median(lag) if lag else None}

# per-era counts
res["node_era_counts"] = dict(Counter(B.nodes[i]["era"] for i in ids))
res["node_era_by_cls"] = {c: dict(Counter(B.nodes[i]["era"] for i in ids if B.nodes[i]["cls"] == c)) for c in sorted({B.nodes[i]["cls"] for i in ids})}
res["edge_era_counts"] = dict(Counter(era_of_year(y) for y in edate))
res["timeline_era_counts"] = dict(Counter(t.get("era") for t in TL))
res["timeline_with_node"] = sum(1 for t in TL if t.get("node"))
res["nodes_with_timeline"] = len({t["node"] for t in TL if t.get("node")})

# cross-era edges by node era
ce = Counter()
for e in B.edges:
    ea, eb = B.nodes[e["a"]]["era"], B.nodes[e["b"]]["era"]
    if ea == "nd" or eb == "nd":
        ce["has_nd"] += 1
    elif ea == eb:
        ce["same"] += 1
    else:
        ce["cross"] += 1
res["cross_era_by_node_era"] = dict(ce)
# edges whose edge-date era differs from the era of the OLDER endpoint (retrospective links)
retro = Counter()
for e, y in zip(B.edges, edate):
    if not y:
        continue
    ys = [x for x in (node_y[e["a"]], node_y[e["b"]]) if x]
    if not ys:
        continue
    retro["retro" if era_of_year(y) != era_of_year(min(ys)) else "same"] += 1
res["edge_era_vs_older_node_era"] = dict(retro)


# era subgraphs by EDGE date
def sub_by_edges(es):
    a2 = defaultdict(set)
    W = Counter()
    for e in es:
        a2[e["a"]].add(e["b"])
        a2[e["b"]].add(e["a"])
        k = (e["a"], e["b"]) if e["a"] < e["b"] else (e["b"], e["a"])
        W[k] += 1
    nodes = sorted(a2)
    for i in ids:
        a2.setdefault(i, set())
    cc = components(nodes, a2)
    best = max((louvain(ids, W, seed=s) for s in range(6)), key=lambda x: x[1]) if W else ({}, 0)
    comm = Counter(best[0][i] for i in nodes)
    top = sorted(nodes, key=lambda i: -len(a2[i]))[:8]
    g0 = cc[0] if cc else []
    import random
    rng = random.Random(2)
    src = rng.sample(g0, min(150, len(g0)))
    t, c = 0, 0
    for s in src:
        d = bfs(s, a2)
        for k2, v in d.items():
            if k2 != s:
                t += v
                c += 1
    # which hubdamp communities dominate
    hc = Counter(PH[i] for i in nodes)
    return {"edges": len(es), "nodes": len(nodes), "components": len(cc), "giant": len(g0),
            "giant_share": len(g0) / len(nodes) if nodes else 0, "Q": best[1],
            "communities_ge5": sum(1 for v in comm.values() if v >= 5), "avg_path": t / c if c else 0,
            "top": [(i, len(a2[i])) for i in top], "max_deg": len(a2[top[0]]) if top else 0,
            "hub_communities": hc.most_common(6)}


res["era_edge_slices"] = {}
for eid, lo, hi, lab in ERAS:
    es = [e for e, y in zip(B.edges, edate) if y and era_of_year(y) == eid]
    res["era_edge_slices"][lab] = sub_by_edges(es)
res["era_edge_slices"]["undated edges"] = sub_by_edges([e for e, y in zip(B.edges, edate) if not y])
# cumulative
res["cumulative"] = {}
for eid, lo, hi, lab in ERAS:
    es = [e for e, y in zip(B.edges, edate) if y and y <= hi]
    s = sub_by_edges(es)
    res["cumulative"][f"through {hi if hi < 2100 else 2026}"] = {k: s[k] for k in ("edges", "nodes", "components", "giant", "Q")}

# era subgraphs by NODE era (induced)
res["era_node_slices"] = {}
for eid, lo, hi, lab in ERAS + [("nd", None, None, "no date")]:
    S = {i for i in ids if B.nodes[i]["era"] == eid}
    es = [e for e in B.edges if e["a"] in S and e["b"] in S]
    s = sub_by_edges(es)
    s["era_nodes"] = len(S)
    s["isolated_in_slice"] = len(S) - s["nodes"]
    res["era_node_slices"][lab] = s

dump("s7_time.json", res)
for k, v in res.items():
    if k in ("era_edge_slices", "era_node_slices", "cumulative"):
        print(k)
        for kk, vv in v.items():
            print("   ", kk, json.dumps(vv, ensure_ascii=False)[:600])
    else:
        print(k, json.dumps(v, ensure_ascii=False))
