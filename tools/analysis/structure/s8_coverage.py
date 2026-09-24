"""Section 6: coverage of the board by existing curated structures."""
import os
from collections import Counter, defaultdict
from g import *

B = Board()
ids, adj = B.ids, B.adj
N = len(ids)
C = rd(OUT, "s3_consensus.json")["cons"]
PH, PA = C["hubdamp"]["part"], C["all"]["part"]
L0M = rd(REPO, "data", "l0-model.json")
TH = rd(APPDATA, "threads.json")["threads"]
HL = rd(APPDATA, "highlights.json")["flags"]
MAP = rd(APPDATA, "map.json")
TL = rd(APPDATA, "timeline.json")
FO = rd(APPDATA, "foia.json")
PAT = rd(APPDATA, "patents.json")

S = {}
thread_nodes = defaultdict(set)
for t in TH:
    for st in t["steps"]:
        if st.get("node"):
            thread_nodes[t["id"]].add(st["node"])
        ed = st.get("edge") or {}
        for v in ed.get("via") or []:
            thread_nodes[t["id"]].add(v)
S["threads"] = set().union(*thread_nodes.values())
S["highlights"] = {f["id"] for f in HL}
S["entry_paths"] = {i for ep in MAP["entryPaths"] for i in ep["ids"]}
S["l0"] = {n["id"] for n in L0M["l0"]}
dossier = set()
for i in ids:
    x = rd(APPDATA, "nodes", i + ".json")
    if x.get("dossier"):
        dossier.add(i)
S["dossier"] = dossier
S["timeline"] = {t["node"] for t in TL if t.get("node")}
S["foia"] = set(FO["byNode"].keys())
S["patents"] = {p["node"] for p in PAT["patents"] if p.get("node")}
direct = {d for n in L0M["l0"] for d in (n.get("direct") or [])}
routed = {r["id"] for n in L0M["l0"] for r in (n.get("routed") or [])}
S["l0_direct_member"] = direct
S["l0_routed_member"] = routed
for k in S:
    S[k] &= set(ids)

res = {"sizes": {k: len(v) for k, v in S.items()}, "shares": {k: len(v) / N for k, v in S.items()}}
res["thread_sizes"] = {k: len(v) for k, v in thread_nodes.items()}
res["thread_overlap_pairs"] = sum(1 for i in S["threads"] if sum(1 for v in thread_nodes.values() if i in v) > 1)

authored = S["threads"] | S["highlights"] | S["entry_paths"] | S["l0"] | S["dossier"]
res["authored_union"] = len(authored)
res["authored_plus_timeline"] = len(authored | S["timeline"])
res["authored_plus_timeline_foia_patents"] = len(authored | S["timeline"] | S["foia"] | S["patents"])
res["plus_l0_direct"] = len(authored | S["timeline"] | S["foia"] | S["patents"] | S["l0_direct_member"])
narrative = S["threads"] | S["highlights"] | S["entry_paths"]
res["narrative_union"] = len(narrative)
search_only = [i for i in ids if i not in (authored | S["timeline"] | S["foia"] | S["patents"])]
res["search_only_excl_l0members"] = len(search_only)
res["search_only_cls"] = Counter(B.nodes[i]["cls"] for i in search_only).most_common()
res["search_only_tier"] = Counter(B.nodes[i]["tier"] for i in search_only).most_common()
res["search_only_deg_median"] = sorted(B.deg[i] for i in search_only)[len(search_only) // 2] if search_only else None
res["search_only_in_l0_direct"] = sum(1 for i in search_only if i in direct)
res["search_only_in_l0_routed"] = sum(1 for i in search_only if i in routed)
strict = [i for i in search_only if i not in direct]
res["strict_search_only"] = len(strict)
res["strict_search_only_cls"] = Counter(B.nodes[i]["cls"] for i in strict).most_common()
res["strict_examples"] = sorted(strict, key=lambda i: -B.deg[i])[:25]
# tier A coverage
tierA = {i for i in ids if B.nodes[i]["tier"] == "A"}
res["tierA_in_narrative"] = len(tierA & narrative) / len(tierA)
res["tierA_in_authored"] = len(tierA & authored) / len(tierA)
res["tierA_search_only"] = sorted([i for i in tierA if i in search_only], key=lambda i: -B.deg[i])
# top-50 by degree coverage
top50 = sorted(ids, key=lambda i: -B.deg[i])[:50]
res["top50_not_in_narrative"] = [i for i in top50 if i not in narrative]
res["top50_not_in_l0"] = [i for i in top50 if i not in S["l0"]]
# persons on L0 (L0 carries no people?)
res["l0_cls"] = Counter(B.nodes[i]["cls"] for i in S["l0"]).most_common()
res["narrative_cls"] = Counter(B.nodes[i]["cls"] for i in narrative).most_common()


# coverage per community
def per_comm(part):
    g = defaultdict(list)
    for k, v in part.items():
        g[v].append(k)
    out = []
    for c in sorted(g, key=lambda x: -len(g[x])):
        m = g[c]
        out.append({"c": c, "size": len(m),
                    "threads": sum(1 for i in m if i in S["threads"]),
                    "thread_ids": sorted({t for t, v in thread_nodes.items() if v & set(m)}),
                    "l0": sum(1 for i in m if i in S["l0"]),
                    "highlights": sum(1 for i in m if i in S["highlights"]),
                    "entry": sum(1 for i in m if i in S["entry_paths"]),
                    "dossier": sum(1 for i in m if i in S["dossier"]),
                    "timeline": sum(1 for i in m if i in S["timeline"]),
                    "search_only": sum(1 for i in m if i in set(search_only))})
    return out


res["per_comm_hub"] = per_comm(PH)
res["per_comm_all"] = per_comm(PA)
dump("s8_coverage.json", res)
for k, v in res.items():
    if k.startswith("per_comm"):
        print(k)
        for r in v:
            print("   ", r)
    else:
        print(k, json.dumps(v, ensure_ascii=False)[:900])
