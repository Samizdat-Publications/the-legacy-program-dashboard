# -*- coding: utf-8 -*-
"""Read-only census of the-program's data model.

Reads data/the-program.json, data/l0-model.json, data/l0-layout-model.json,
app/public/data/*, research/*.json, research/dossiers/*.json and a few
side files. Writes census.json (and census_detail.json) to this script's folder.
Never writes into the repo.
"""
import collections
import glob
import json
import os
import re
import statistics
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
# Outputs go outside the repo so a run never dirties the tree (CENSUS_OUT, else system temp).
import tempfile
HERE = os.environ.get("CENSUS_OUT") or os.path.join(tempfile.gettempdir(), "the-program-census")
os.makedirs(HERE, exist_ok=True)
Counter = collections.Counter
defaultdict = collections.defaultdict


def rd(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def pct(a, b):
    return round(100.0 * a / b, 1) if b else None


def dist(vals):
    vals = sorted(vals)
    if not vals:
        return {}
    n = len(vals)
    return {"n": n, "min": vals[0], "p25": vals[int(0.25 * (n - 1))],
            "median": statistics.median(vals), "mean": round(sum(vals) / n, 2),
            "p75": vals[int(0.75 * (n - 1))], "p90": vals[int(0.9 * (n - 1))],
            "max": vals[-1], "zeros": sum(1 for v in vals if v == 0)}


def top(counter, k=30):
    return [[str(a), b] for a, b in counter.most_common(k)]


def precision_of(s):
    if not s:
        return None
    s = str(s)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return "day"
    if re.match(r"^\d{4}-\d{2}$", s):
        return "month"
    if re.match(r"^\d{4}$", s):
        return "year"
    return "other:" + s[:12]


def year_of(s):
    m = re.match(r"\s*(\d{4})", str(s or ""))
    return int(m.group(1)) if m else None


URL_RE = re.compile(r"https?://[^\s\"'<>|)\]]+")


def host_of(url):
    m = re.match(r"https?://([^/:]+)", url or "")
    if not m:
        return None
    h = m.group(1).lower()
    return h[4:] if h.startswith("www.") else h


C = {}          # the census, headline numbers
D = {}          # detail tables

board = rd("data/the-program.json")
P, E, ED, TL, EI = board["people"], board["entities"], board["edges"], board["timeline"], board["entityInfo"]
N = P + E
BY = {n["id"]: n for n in N}
ids = set(BY)
l0m = rd("data/l0-model.json")
layout = rd("data/l0-layout-model.json")["current"]
app = lambda f: rd("app/public/data/" + f)
aindex, aclaims, aedges, atl = app("index.json"), app("claims.json"), app("edges.json"), app("timeline.json")
amap, athreads, afoia, ahl, apat = app("map.json"), app("threads.json"), app("foia.json"), app("highlights.json"), app("patents.json")

C["generated"] = board["generated"]
C["counts"] = {"people": len(P), "entities": len(E), "nodes": len(N), "edges": len(ED),
               "timeline": len(TL), "entityInfo": len(EI)}

# ============================================================== NODES
cls = Counter(n["cls"] for n in N)
C["nodes_by_cls"] = dict(cls.most_common())
C["tier_by_cls"] = {c: dict(Counter(n["tier"] for n in N if n["cls"] == c)) for c in cls}
C["tier_total"] = dict(Counter(n["tier"] for n in N))
C["cluster_by_cls"] = {c: dict(Counter(n["cluster"] for n in N if n["cls"] == c).most_common()) for c in cls}
C["cluster_total"] = dict(Counter(n["cluster"] for n in N).most_common())
C["person_status"] = dict(Counter(p["status"] for p in P).most_common())
C["axes"] = {ax: {c: dict(sorted(Counter(n[ax] for n in N if n["cls"] == c).items())) for c in cls}
             for ax in ("C", "A", "D")}
C["axes_all_zero"] = sum(1 for n in N if n["C"] == 0 and n["A"] == 0 and n["D"] == 0)

# sub
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
subs_p = Counter(p["sub"] for p in P)
subs_e = Counter(e["sub"] for e in E)
slug_like_e = Counter(e["sub"] for e in E if e["sub"] and SLUG.match(e["sub"]))
slug_like_p = Counter(p["sub"] for p in P if p["sub"] and SLUG.match(p["sub"]))
C["sub"] = {
    "people_distinct": len(subs_p), "people_null_or_empty": sum(1 for p in P if not p["sub"]),
    "people_shared_by_2plus": sum(1 for v in subs_p.values() if v >= 2),
    "entities_distinct": len(subs_e), "entities_null_or_empty": sum(1 for e in E if not e["sub"]),
    "entities_shared_by_2plus_values": sum(1 for v in subs_e.values() if v >= 2),
    "entities_nodes_in_shared_values": sum(v for v in subs_e.values() if v >= 2),
    "entities_slug_like_nodes": sum(slug_like_e.values()),
    "entities_slug_like_distinct": len(slug_like_e),
    "people_slug_like_nodes": sum(slug_like_p.values()),
    "sub_len_entities": dist([len(e["sub"] or "") for e in E]),
    "sub_len_people": dist([len(p["sub"] or "") for p in P]),
}
D["sub_top_entities"] = top(subs_e, 40)
D["sub_slug_like_entities"] = top(slug_like_e, 80)
D["sub_top_people"] = top(subs_p, 15)
D["sub_slug_by_cls"] = {c: top(Counter(e["sub"] for e in E if e["cls"] == c and e["sub"] and SLUG.match(e["sub"])), 30) for c in cls if c != "person"}

# dates
pdate = Counter(precision_of(p["date"]) for p in P)
eds = Counter(precision_of(e["dateStart"]) for e in E)
ede = Counter(precision_of(e["dateEnd"]) for e in E)
C["dates"] = {
    "people_date_precision": dict(pdate), "entities_dateStart_precision": dict(eds),
    "entities_dateEnd_precision": dict(ede),
    "nodes_with_any_date": sum(1 for p in P if p["date"]) + sum(1 for e in E if e["dateStart"] or e["dateEnd"]),
    "entities_with_range": sum(1 for e in E if e["dateStart"] and e["dateEnd"]),
    "entities_by_cls_with_dateStart": {c: [sum(1 for e in E if e["cls"] == c and e["dateStart"]), cls[c]] for c in cls if c != "person"},
    "people_with_chronology": sum(1 for p in P if p["chronology"]),
    "chronology_entries": sum(len(p["chronology"]) for p in P),
    "people_with_sequenceChain": sum(1 for p in P if p["sequenceChain"]),
    "sequenceChain_entries": sum(len(p["sequenceChain"]) for p in P),
}
seqkeys = Counter(k for p in P for s in p["sequenceChain"] if isinstance(s, dict) for k in s)
C["dates"]["sequenceChain_keys"] = dict(seqkeys)
C["dates"]["sequenceChain_nondict"] = sum(1 for p in P for s in p["sequenceChain"] if not isinstance(s, dict))
C["dates"]["sequenceChain_isAnomalous_true"] = sum(1 for p in P for s in p["sequenceChain"] if isinstance(s, dict) and s.get("isAnomalous"))
# era (app rule)
ERAS = [("0", None, 1969), ("1", 1970, 1999), ("2", 2000, 2016), ("3", 2017, 2100)]


def era_of(ds):
    y = year_of(ds)
    if y is None:
        return "nd"
    for i, a, b in ERAS:
        if (a is None or y >= a) and y <= b:
            return i
    return "nd"


C["era_nodes"] = dict(Counter(n["era"] for n in aindex["nodes"]))
C["era_nodes_by_cls"] = {c: dict(Counter(n["era"] for n in aindex["nodes"] if n["cls"] == c)) for c in cls}
C["decade_nodes"] = dict(sorted(Counter((year_of(n.get("date") or n.get("dateStart")) // 10 * 10) if year_of(n.get("date") or n.get("dateStart")) else "nd" for n in N).items(), key=lambda kv: str(kv[0])))

# places
loc_nodes = [e for e in E if e["cls"] == "location"]
geo_nbrs = set()
for e in ED:
    for x, y in ((e["a"], e["b"]), (e["b"], e["a"])):
        if BY.get(y, {}).get("cls") == "location":
            geo_nbrs.add(x)
C["places"] = {
    "people_loc_string": sum(1 for p in P if p["loc"]),
    "people_locId": sum(1 for p in P if p["locId"]),
    "people_locId_resolves_to_location_cls": sum(1 for p in P if p["locId"] and BY.get(p["locId"], {}).get("cls") == "location"),
    "people_locId_distinct": len(set(p["locId"] for p in P if p["locId"])),
    "people_loc_distinct_strings": len(set(p["loc"] for p in P if p["loc"])),
    "people_instId": sum(1 for p in P if p["instId"]),
    "people_instId_distinct": len(set(p["instId"] for p in P if p["instId"])),
    "people_instId_cls": dict(Counter(BY.get(p["instId"], {}).get("cls", "MISSING") for p in P if p["instId"])),
    "entities_coords": sum(1 for e in E if e["coords"]),
    "entities_coords_by_cls": dict(Counter(e["cls"] for e in E if e["coords"])),
    "entities_locLabel": sum(1 for e in E if e["locLabel"]),
    "location_cls_nodes": len(loc_nodes),
    "location_nodes_with_coords": sum(1 for e in loc_nodes if e["coords"]),
    "nodes_adjacent_to_a_location_node": len(geo_nbrs - set(x["id"] for x in loc_nodes)),
    "nodes_with_any_place_signal": len({p["id"] for p in P if p["loc"] or p["locId"]}
                                       | {e["id"] for e in E if e["coords"] or e["locLabel"] or e["cls"] == "location"}
                                       | geo_nbrs),
}
top_loc = Counter(p["locId"] for p in P if p["locId"])
D["people_locId_top"] = top(top_loc, 20)
D["people_instId_top"] = top(Counter(p["instId"] for p in P if p["instId"]), 20)
# person domains (authored links to domain nodes)
pd = Counter(d for p in P for d in p["domains"])
C["people_domains_field"] = {
    "people_with_domains": sum(1 for p in P if p["domains"]),
    "refs": sum(pd.values()), "distinct": len(pd),
    "resolve_to_domain_cls": sum(v for d, v in pd.items() if BY.get(d, {}).get("cls") == "domain"),
    "resolve_to_other_cls": sum(v for d, v in pd.items() if d in BY and BY[d]["cls"] != "domain"),
    "dangling": sum(v for d, v in pd.items() if d not in BY),
}
D["people_domains_top"] = top(pd, 25)

# text fields
C["text"] = {
    "people_narrative_len": dist([len(p["narrative"] or "") for p in P]),
    "entities_desc_len": dist([len(e["desc"] or "") for e in E]),
    "entities_desc_under_200": sum(1 for e in E if len(e["desc"] or "") < 200),
    "tierRationale_machine_regraded": sum(1 for n in N if (n["tierRationale"] or "").startswith("Re-graded")),
    "tierRationale_other": sum(1 for n in N if not (n["tierRationale"] or "").startswith("Re-graded")),
    "people_affiliations": sum(1 for p in P if p["affiliations"]),
    "affiliation_entries": sum(len(p["affiliations"]) for p in P),
    "people_conflicts": sum(1 for p in P if p["conflicts"]),
    "conflict_entries": sum(len(p["conflicts"]) if isinstance(p["conflicts"], list) else 1 for p in P if p["conflicts"]),
    "people_unverified": sum(1 for p in P if p["unverified"]),
    "unverified_entries": sum(len(p["unverified"]) if isinstance(p["unverified"], list) else 1 for p in P if p["unverified"]),
    "people_unverified_as_string": sum(1 for p in P if isinstance(p["unverified"], str)),
    "people_unexplainedResidual": sum(1 for p in P if p["unexplainedResidual"]),
    "people_photoCredit": sum(1 for p in P if p["photoCredit"]),
    "people_age": sum(1 for p in P if p["age"] is not None),
}
dossiers = l0m["dossiers"]
C["dossiers"] = {
    "count": len(dossiers), "on_board": sum(1 for k in dossiers if k in ids),
    "by_cls": dict(Counter(BY[k]["cls"] for k in dossiers if k in BY)),
    "dossier_claims": sum(len(v.get("claims") or []) for v in dossiers.values()),
    "dossier_claim_tiers": dict(Counter(c.get("tier") for v in dossiers.values() for c in v.get("claims") or [])),
    "openQuestions": sum(len(v.get("openQuestions") or []) for v in dossiers.values()),
    "with_denialPosture": sum(1 for v in dossiers.values() if v.get("denialPosture")),
    "with_connections_prose": sum(1 for v in dossiers.values() if v.get("connections")),
    "roles": dict(Counter(r for v in dossiers.values() for r in v.get("roles") or []).most_common()),
    "roles_per_node": dict(Counter(len(v.get("roles") or []) for v in dossiers.values())),
    "dossier_nodes_on_L0": sum(1 for k in dossiers if k in {x["id"] for x in l0m["l0"]}),
}
C["entityInfo"] = {"keys": len(EI), "keys_on_board": sum(1 for k in EI if k in ids),
                   "keys_not_nodes": sorted(k for k in EI if k not in ids)}

# provenance _domains
prov = Counter(d for n in N for d in n["_domains"])
C["provenance_files_per_node"] = dist([len(n["_domains"]) for n in N])
D["provenance_nodes_per_file"] = top(prov, 120)

# ============================================================== EDGES
et = Counter(e["type"] for e in ED)
C["edges_by_type"] = dict(et.most_common())
C["edge_tier_by_type"] = {t: dict(sorted(Counter(e["claimTier"] for e in ED if e["type"] == t).items())) for t in et}
C["edge_tier_total"] = dict(sorted(Counter(e["claimTier"] for e in ED).items()))
C["edge_note"] = {
    "with_note": sum(1 for e in ED if (e["note"] or "").strip()),
    "note_len": dist([len(e["note"] or "") for e in ED]),
    "note_len_by_type_median": {t: statistics.median([len(e["note"] or "") for e in ED if e["type"] == t]) for t in et},
    "with_label": sum(1 for e in ED if (e["label"] or "").strip()),
    "label_len": dist([len(e["label"] or "") for e in ED]),
    "label_distinct": len(set(e["label"] for e in ED)),
    "with_dateStart": sum(1 for e in ED if e["dateStart"]),
    "with_dateEnd": sum(1 for e in ED if e["dateEnd"]),
    "sources_per_edge": dist([len(e["sources"]) for e in ED]),
    "edge_sources_with_url": sum(1 for e in ED for s in e["sources"] if s.get("url")),
    "edge_sources_total": sum(len(e["sources"]) for e in ED),
    "edge_sources_with_date": sum(1 for e in ED for s in e["sources"] if s.get("date")),
    "edges_with_2plus_files": sum(1 for e in ED if len(e["_domains"]) > 1),
}
# note prefixes that encode intent/meta (e.g. "INTENT: AUTHORSHIP")
intent = Counter()
for e in ED:
    m = re.match(r"^\s*([A-Z][A-Z \-/]{3,40}):", e["note"] or "")
    if m:
        intent[m.group(1).strip()] += 1
D["edge_note_caps_prefixes"] = top(intent, 30)
# cls pairs
pairs = defaultdict(Counter)
for e in ED:
    ca, cb = BY.get(e["a"], {}).get("cls", "?"), BY.get(e["b"], {}).get("cls", "?")
    pairs[e["type"]][ca + ">" + cb] += 1
D["edge_cls_pairs"] = {t: top(pairs[t], 8) for t in et}
# first word of label
fw = defaultdict(Counter)
for e in ED:
    w = re.findall(r"[A-Za-z']+", e["label"] or "")
    fw[e["type"]][(w[0].lower() if w else "")] += 1
D["label_first_word"] = {t: top(fw[t], 12) for t in et}
# parallel edges / self loops
bypair = defaultdict(list)
for e in ED:
    bypair[tuple(sorted((e["a"], e["b"])))].append(e["type"])
C["edge_structure"] = {
    "distinct_pairs": len(bypair),
    "pairs_with_2plus_edges": sum(1 for v in bypair.values() if len(v) > 1),
    "max_edges_per_pair": max(len(v) for v in bypair.values()),
    "self_loops": sum(1 for e in ED if e["a"] == e["b"]),
    "dangling": sum(1 for e in ED if e["a"] not in ids or e["b"] not in ids),
}
deg = Counter()
nb = defaultdict(set)
for e in ED:
    deg[e["a"]] += 1
    deg[e["b"]] += 1
    nb[e["a"]].add(e["b"])
    nb[e["b"]].add(e["a"])
C["degree_edge_instances"] = dist([deg.get(i, 0) for i in ids])
C["degree_distinct_neighbours"] = dist([len(nb.get(i, ())) for i in ids])
C["degree_by_cls_median"] = {c: statistics.median([len(nb.get(n["id"], ())) for n in N if n["cls"] == c]) for c in cls}
D["top_degree"] = [[i, len(nb[i]), BY[i]["cls"]] for i, _ in sorted(((i, len(v)) for i, v in nb.items()), key=lambda kv: -kv[1])[:25]]
C["denial"] = {
    "denialKind": dict(Counter(e.get("denialKind") for e in ED if e["type"] == "denial")),
    "with_denier": sum(1 for e in ED if e["type"] == "denial" and e.get("denier")),
    "nodes_touched_by_denial": len({x for e in ED if e["type"] == "denial" for x in (e["a"], e["b"])}),
}

# research-authored edge types coerced to 'programmatic'
VALID = {"institutional", "geographic", "research", "temporal", "behavioral", "programmatic",
         "investigative", "witness-chain", "custody", "funding", "denial", "legislative"}
offv, offv_files = Counter(), Counter()
research_edge_records = 0
research_keys = Counter()
ent_dropped = Counter()
ent_dropped_ids = defaultdict(list)
cluster_offvocab = Counter()
cluster_offvocab_nodes = defaultdict(set)
authored_sub = defaultdict(lambda: defaultdict(set))
authored_cls = defaultdict(set)
authored_cluster = defaultdict(set)
authored_status = defaultdict(set)
research_files = {}
VALID_CLUSTER = {"legacy", "contractor", "ffrdc", "ic", "oversight", "witness", "research", "media", "other"}
EK = {"id", "cls", "label", "cluster", "sub", "desc", "tier", "C", "A", "D", "dateStart", "dateEnd",
      "coords", "locLabel", "tierRationale", "claims", "sources", "removeClaims"}
for f in sorted(glob.glob(os.path.join(ROOT, "research", "*.json"))):
    slug = os.path.splitext(os.path.basename(f))[0]
    doc = json.load(open(f, encoding="utf-8"))
    if not isinstance(doc, dict):
        continue
    research_files[slug] = {"domain": (doc.get("domain") or doc.get("_why") or doc.get("_what") or "")[:240],
                            "people": len(doc.get("people") or []), "entities": len(doc.get("entities") or []),
                            "edges": len(doc.get("edges") or []), "timeline": len(doc.get("timeline") or []),
                            "gaps": len(doc.get("gaps") or [])}
    for x in doc.get("edges") or []:
        research_edge_records += 1
        t = x.get("type") or x.get("rel")
        if t not in VALID:
            offv[t] += 1
            offv_files[slug] += 1
    overlay = slug in ("_corrections", "_remediation")
    for kind in ("people", "entities"):
        for r in doc.get(kind) or []:
            rid = r.get("id")
            if not rid:
                continue
            if kind == "entities":
                for k in r:
                    if k not in EK:
                        ent_dropped[k] += 1
                        ent_dropped_ids[k].append(rid)
            cv = r.get("cluster")
            if cv and cv not in VALID_CLUSTER:
                cluster_offvocab[cv] += 1
                cluster_offvocab_nodes[cv].add(rid)
            if overlay:
                continue
            if r.get("sub"):
                authored_sub[rid][r["sub"]].add(slug)
            if r.get("cls"):
                authored_cls[rid].add(r["cls"])
            if cv:
                authored_cluster[rid].add(cv)
            if kind == "people" and r.get("status"):
                authored_status[rid].add(r["status"])
C["research"] = {
    "json_files": len(research_files),
    "edge_records": research_edge_records,
    "edge_offvocab_types_records": sum(offv.values()),
    "edge_offvocab_types_distinct": len(offv),
    "entity_fields_dropped_by_merge": dict(ent_dropped),
    "entity_conflicts_dropped_ids": sorted(set(ent_dropped_ids.get("conflicts", []))),
    "entity_unverified_dropped_ids": sorted(set(ent_dropped_ids.get("unverified", []))),
    "cluster_offvocab_values": dict(cluster_offvocab),
    "cluster_offvocab_distinct_nodes": len(set().union(*cluster_offvocab_nodes.values())) if cluster_offvocab_nodes else 0,
    "sub_conflicting_ids": sum(1 for rid, v in authored_sub.items() if len(v) > 1),
    "sub_conflicting_ids_entities": sum(1 for rid, v in authored_sub.items() if len(v) > 1 and BY.get(rid, {}).get("cls") != "person"),
    "sub_conflicting_ids_people": sum(1 for rid, v in authored_sub.items() if len(v) > 1 and BY.get(rid, {}).get("cls") == "person"),
    "cls_conflicting_ids": sum(1 for v in authored_cls.values() if len(v) > 1),
    "cluster_conflicting_ids": sum(1 for v in authored_cluster.values() if len(v) > 1),
    "status_conflicting_ids": sum(1 for v in authored_status.values() if len(v) > 1),
}
D["edge_offvocab_types"] = top(offv, 60)
D["edge_offvocab_files"] = top(offv_files, 20)
D["research_files"] = research_files
D["sub_conflict_examples"] = [[rid, {k: sorted(v) for k, v in vs.items()}] for rid, vs in list(authored_sub.items()) if len(vs) > 1][:12]
D["status_conflict_examples"] = [[rid, sorted(v)] for rid, v in authored_status.items() if len(v) > 1][:15]
D["cls_conflict_examples"] = [[rid, sorted(v)] for rid, v in authored_cls.items() if len(v) > 1][:15]

# ============================================================== CLAIMS
claims = [(n, c) for n in N for c in n["claims"]]
cpn = [len(n["claims"]) for n in N]
C["claims"] = {
    "total": len(claims),
    "by_tier": dict(sorted(Counter(c["tier"] for _, c in claims).items())),
    "by_cls": {k: dict(sorted(Counter(c["tier"] for n, c in claims if n["cls"] == k).items())) for k in cls},
    "per_node": dist(cpn),
    "per_node_people": dist([len(p["claims"]) for p in P]),
    "per_node_entities": dist([len(e["claims"]) for e in E]),
    "nodes_zero_claims": sum(1 for v in cpn if v == 0),
    "nodes_only_T3": sum(1 for n in N if n["claims"] and all(c["tier"] == 3 for c in n["claims"])),
    "nodes_with_T1": sum(1 for n in N if any(c["tier"] == 1 for c in n["claims"])),
    "claim_text_len": dist([len(c["text"]) for _, c in claims]),
    "app_claims_json_rows": len(aclaims),
}
# source classification
def src_url(s):
    m = URL_RE.search(s or "")
    return m.group(0).rstrip(".,;") if m else None


demoted = sum(1 for _, c in claims if "DEMOTED from Tier 1" in (c["source"] or ""))
C["claims"]["source_with_url"] = sum(1 for _, c in claims if src_url(c["source"]))
C["claims"]["source_no_url"] = len(claims) - C["claims"]["source_with_url"]
C["claims"]["source_distinct_strings"] = len(set(c["source"] for _, c in claims))
C["claims"]["source_no_attributed"] = sum(1 for _, c in claims if (c["source"] or "").lower().startswith("no attributed source"))
C["claims"]["source_demoted_marker"] = demoted
C["claims"]["source_board_bookkeeping_by_tier"] = dict(Counter(c["tier"] for _, c in claims if re.search(r"bookkeeping", c["source"] or "", re.I)))
C["claims"]["text_placeholder_no_dossier_by_tier"] = dict(Counter(c["tier"] for _, c in claims if re.search(r"no dossier written|referenced by the board", c["text"] or "", re.I)))
C["claims"]["text_mentions_board_or_node_self_by_tier"] = dict(Counter(c["tier"] for _, c in claims if re.search(r"\b(this|the) (board|node|map)\b", c["text"] or "", re.I)))
C["claims"]["source_inference_marker_by_tier"] = dict(Counter(c["tier"] for _, c in claims if re.search(r"^\s*(inference|reasoning|inferred|board inference|stated inference)", c["source"] or "", re.I)))
C["claims"]["source_internal_repo_path_by_tier"] = dict(Counter(c["tier"] for _, c in claims if re.search(r"research/|notes/|tools/", c["source"] or "")))
dom = Counter(host_of(src_url(c["source"])) for _, c in claims if src_url(c["source"]))
D["claim_source_domains_top30"] = top(dom, 30)
alldom = Counter()
for n in N:
    for s in n["sources"]:
        if s.get("url"):
            alldom[host_of(s["url"])] += 1
for e in ED:
    for s in e["sources"]:
        if s.get("url"):
            alldom[host_of(s["url"])] += 1
D["all_structured_source_domains_top30"] = top(alldom, 30)

# source-type classes (heuristic, labelled as such)
GOV = re.compile(r"\.(gov|mil)$|\.gov\.|gov\.uk$|\.gc\.ca$|\.gob\.|\.gov\.br$|senado\.leg\.br|camara\.leg\.br|nationalarchives\.gov\.uk|europa\.eu$")
ARCH = re.compile(r"theblackvault\.com|documents2\.theblackvault|archive\.org|nsarchive|fas\.org|cia\.gov/readingroom|documentcloud|muckrock|nicap\.org|project1947|bluebookarchive|cufon|majesticdocuments")
VIDEO = re.compile(r"youtube\.com|youtu\.be|vimeo|rumble|podcasts\.apple|spotify|podbean|anchor\.fm|megaphone")
WIKI = re.compile(r"wikipedia\.org|wikidata|britannica|fandom")
SCI = re.compile(r"doi\.org|arxiv\.org|nature\.com|sciencedirect|springer|mdpi|iop\.org|aps\.org|jstor|pubmed|ncbi|researchgate|scientificamerican|aiaa\.org|ieee")
SOC = re.compile(r"twitter\.com|x\.com|facebook|instagram|reddit|substack|medium\.com|threads\.net|tiktok|linkedin")
PAT = re.compile(r"patents\.google|uspto|freepatentsonline|patft|ppubs")


def src_class_url(h):
    if not h:
        return None
    if PAT.search(h):
        return "patent office/db"
    if GOV.search(h):
        return "government/military"
    if ARCH.search(h):
        return "archive/FOIA mirror"
    if VIDEO.search(h):
        return "video/podcast"
    if WIKI.search(h):
        return "encyclopedia"
    if SCI.search(h):
        return "scholarly"
    if SOC.search(h):
        return "social/newsletter"
    return "news/other web"


SPEECH = re.compile(r"\b(testimony|testified|testifies|written statement|statement to|statement,|interview|interviewed|podcast|episode|press conference|remarks|told|said|says|speech|affidavit|deposition|lecture|conference|panel|on X\b|tweet|post on|posted|livestream|broadcast|documentary|60 Minutes|NewsNation|Rogan|Jesse Michels|American Alchemy|Danny Jones|Weaponized|Coulthart|Corbell)\b", re.I)
BOOKISH = re.compile(r"\b(book|memoir|pp?\.\s*\d|ISBN|chapter|(19|20)\d\d\)|press, (19|20)\d\d|University Press)\b", re.I)
INFER = re.compile(r"^\s*(inference|reasoning|inferred|board|analysis of|comparison of|stated inference)", re.I)
IDENT = re.compile(r"GAO[/-]|CHRG-|HHRG-|CIA-RDP|U\.S\.C\.|USC\b|P\.L\.|Pub\. ?L\.|H\.R\.\s*\d|S\.\s*\d{2,4}\b|S\.Amdt|SA \d{3,4}|DoD[ID]\s*\d|DODD|DODI|DoDM|EO \d{5}|E\.O\. ?\d{5}|Executive Order \d{5}|DIA-\d|FOIA[- ]?\d|case (no\.? )?\d|\d{2}-F-\d{3,5}|DOI\s*10\.|10\.\d{4,}/|US ?Patent|Patent \d|\bUS\d{7,}|RG \d{2,3}|DEFE \d|AFR \d{2,3}-\d|ICD \d{3}|NSDD|NSDM|NSC \d|PDD|PPD-\d|CFR\b|Sec\. ?\d{3,5}|section \d{3,5}|NDAA", re.I)


def classify_source(s):
    s = s or ""
    u = src_url(s)
    if u:
        return "url:" + (src_class_url(host_of(u)) or "?")
    if s.lower().startswith("no attributed source"):
        return "none"
    if re.search(r"bookkeeping", s, re.I):
        return "bookkeeping"
    if INFER.search(s):
        return "inference/analysis"
    if IDENT.search(s):
        return "identifier (no url)"
    if SPEECH.search(s):
        return "speaker/testimony/interview (no url)"
    if BOOKISH.search(s):
        return "book/report title (no url)"
    return "named publication/other (no url)"


sc = Counter(classify_source(c["source"]) for _, c in claims)
C["claims"]["source_class_heuristic"] = dict(sc.most_common())
C["claims"]["source_class_by_tier_heuristic"] = {t: dict(Counter(classify_source(c["source"]) for _, c in claims if c["tier"] == t).most_common()) for t in (1, 2, 3)}
# speaker in claim TEXT (heuristic)
SPEAK_TXT = re.compile(r"\b(testified|testifies|stated|states|said|says|told|claimed|claims|alleged|alleges|recalled|recalls|described|describes|wrote|writes|asserted|asserts|according to|reported|reports|maintains|maintained|insisted|denied|denies)\b", re.I)
C["claims"]["text_has_speech_verb_by_tier"] = {t: [sum(1 for _, c in claims if c["tier"] == t and SPEAK_TXT.search(c["text"])), sum(1 for _, c in claims if c["tier"] == t)] for t in (1, 2, 3)}
# dates in claim text
YR = re.compile(r"\b(1[89]\d\d|20[0-2]\d)\b")
DAYDATE = re.compile(r"\b\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) (1[89]\d\d|20[0-2]\d)\b|\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2},? (1[89]\d\d|20[0-2]\d)\b")
C["claims"]["text_has_year"] = sum(1 for _, c in claims if YR.search(c["text"]))
C["claims"]["text_has_full_date"] = sum(1 for _, c in claims if DAYDATE.search(c["text"]))
C["claims"]["have_id_field"] = False
C["claims"]["have_date_field"] = False

# ------------------------------------------------ sources as objects (coordinator ask 1)
def norm_url(u):
    u = u.strip().rstrip(".,;)")
    wb = re.match(r"https?://web\.archive\.org/web/\d+[a-z_]*/(https?://.+)$", u, re.I)
    if wb:
        u = wb.group(1)
    u = re.sub(r"#.*$", "", u)
    u = re.sub(r"[?&](utm_[^=&]+|fbclid|gclid)=[^&]*", "", u)
    m = re.match(r"https?://(?:www\.)?([^/]+)(/.*)?$", u, re.I)
    if not m:
        return u.lower()
    host, path = m.group(1).lower(), (m.group(2) or "/")
    path = path.rstrip("/") or "/"
    return host + path


ID_RULES = [
    ("PL", re.compile(r"PLAW-(\d{3})publ(\d{1,3})", re.I), lambda m: "PL %s-%s" % (m.group(1), m.group(2))),
    ("USC", re.compile(r"USCODE-\d{4}-title(\d{1,2})\S*?-sec(\d{1,5}[a-z]?)", re.I), lambda m: "%s USC %s" % (m.group(1), m.group(2).lower())),
    ("USC", re.compile(r"uscode\.house\.gov/view\.xhtml\?req=granuleid:USC-prelim-title(\d{1,2})-section(\d{1,5}[a-z]?)", re.I), lambda m: "%s USC %s" % (m.group(1), m.group(2).lower())),
    ("DODI/D", re.compile(r"issuances/dod([idm])/(\d{4})(\d{2})(?:_vol\d+)?p?\.pdf", re.I), lambda m: "DOD%s %s.%s" % (m.group(1).upper(), m.group(2), m.group(3))),
    ("ICD", re.compile(r"\bICD[-_ ](\d{3})\b", re.I), lambda m: "ICD " + m.group(1)),
    ("HR", re.compile(r"BILLS-\d{3}hr(\d{1,5})", re.I), lambda m: "HR %s" % m.group(1)),
    ("S", re.compile(r"BILLS-\d{3}s(\d{1,5})", re.I), lambda m: "S %s" % m.group(1)),
    ("GAO", re.compile(r"\bGAO[/-]?((?:NSIAD|GGD|AFMD|HRD|RCED|OSI|T-NSIAD|AIMD|GAO)[-/]?\d{2}-\d{1,4}|\d{2}-\d{2,4}[A-Z]{0,2})\b", re.I), lambda m: "GAO-" + m.group(1).upper().replace("/", "-")),
    ("GAO", re.compile(r"GAOREPORTS-((?:NSIAD|GGD|AFMD|HRD|RCED)-\d{2}-\d{1,4})", re.I), lambda m: "GAO-" + m.group(1).upper()),
    ("CHRG", re.compile(r"\bCHRG-(\d{3})(hhrg|shrg|jhrg)(\d{3,6})\b", re.I), lambda m: "CHRG-%s%s%s" % (m.group(1), m.group(2).lower(), m.group(3))),
    ("HHRG", re.compile(r"\bHHRG-(\d{3})-([A-Z]{2}\d{2})(?:-(\d{8}))?", re.I), lambda m: "HHRG-%s-%s" % (m.group(1), m.group(2).upper())),
    ("CIA-RDP", re.compile(r"\bCIA-RDP[0-9A-Z]+-[0-9A-Z]+(?:-\d)?\b", re.I), lambda m: m.group(0).upper()),
    ("USC", re.compile(r"\b(\d{1,2})\s*U\.?\s?S\.?\s?C\.?\s*(?:§+\s*)?(\d{1,5}[a-z]?)", re.I), lambda m: "%s USC %s" % (m.group(1), m.group(2).lower())),
    ("PL", re.compile(r"\b(?:P\.\s?L\.|Pub(?:lic|\.)\s?L(?:aw|\.)?)\s*(?:No\.\s*)?(\d{2,3})[-\u2013](\d{1,3})\b", re.I), lambda m: "PL %s-%s" % (m.group(1), m.group(2))),
    ("HR", re.compile(r"\bH\.\s?R\.\s*(\d{1,5})\b"), lambda m: "HR %s" % m.group(1)),
    ("HR", re.compile(r"congress\.gov/bill/(\d{2,3})\w*-congress/house-bill/(\d{1,5})", re.I), lambda m: "HR %s" % m.group(2)),
    ("S", re.compile(r"(?<![.\w])S\.\s?(\d{2,4})\b"), lambda m: "S %s" % m.group(1)),
    ("S", re.compile(r"congress\.gov/bill/(\d{2,3})\w*-congress/senate-bill/(\d{1,5})", re.I), lambda m: "S %s" % m.group(2)),
    ("SAMDT", re.compile(r"\b(?:S\.\s?Amdt\.?|SA)\s*(\d{3,4})\b"), lambda m: "SAMDT %s" % m.group(1)),
    ("DODI/D", re.compile(r"\bDoD\s?([IDM])\s*(\d{4}\.\d{2}(?:-[A-Z0-9]+)?)", re.I), lambda m: "DOD%s %s" % (m.group(1).upper(), m.group(2))),
    ("DODI/D", re.compile(r"\bDOD([IDM])\s*(\d{4}\.\d{2})", re.I), lambda m: "DOD%s %s" % (m.group(1).upper(), m.group(2))),
    ("EO", re.compile(r"\b(?:E\.?O\.?|Executive Order)\s*(1\d{4})\b", re.I), lambda m: "EO %s" % m.group(1)),
    ("DIA-DIRD", re.compile(r"\bDIA-08-\d{4}-\d{3}\b", re.I), lambda m: m.group(0).upper()),
    ("FOIA-case", re.compile(r"\b(\d{2}-F-\d{3,5}(?:-[A-Z0-9]+)?)\b", re.I), lambda m: "FOIA " + m.group(1).upper()),
    ("FOIA-case", re.compile(r"\bFOIA[- ](\d{5})-(\d{4})\b", re.I), lambda m: "FOIA-%s-%s" % (m.group(1), m.group(2))),
    ("DOI", re.compile(r"\b(10\.\d{4,9}/[^\s,;\"'<>]+)", re.I), lambda m: "DOI " + m.group(1).rstrip(".)").lower()),
    ("PATENT", re.compile(r"\bUS\s?(?:Patent\s*(?:No\.\s*)?)?((?:\d{1,2},)?\d{3},\d{3}|\d{7,8})\b", re.I), lambda m: "US-PAT " + m.group(1).replace(",", "")),
    ("PATENT", re.compile(r"\bUS\s?(20\d{2})/?(\d{7})\b", re.I), lambda m: "US-PUB %s%s" % (m.group(1), m.group(2))),
    ("AFR", re.compile(r"\bAFR\s*(\d{2,3}-\d{1,3})\b", re.I), lambda m: "AFR " + m.group(1)),
    ("ICD", re.compile(r"\bICD\s*(\d{3})\b"), lambda m: "ICD " + m.group(1)),
    ("NARA-RG", re.compile(r"\b(?:RG|Record Group)\s*(\d{2,3})\b"), lambda m: "NARA RG " + m.group(1)),
    ("UK-TNA", re.compile(r"\b(DEFE|AIR|PREM|CAB)\s?(\d{1,3}/\d{1,4}(?:/\d+)?)\b"), lambda m: "TNA %s %s" % (m.group(1), m.group(2))),
    ("CFR", re.compile(r"\b(\d{1,2})\s*CFR\s*(\d{1,4}(?:\.\d+)?)", re.I), lambda m: "%s CFR %s" % (m.group(1), m.group(2))),
]


def doc_keys(text):
    """Every identifier in a source string (text and URL), normalised. Heuristic."""
    out = []
    for fam, rx, fn in ID_RULES:
        for m in rx.finditer(text or ""):
            try:
                out.append((fam, fn(m)))
            except Exception:
                pass
    # de-dup preserving order
    seen, res = set(), []
    for fam, k in out:
        if k not in seen:
            seen.add(k)
            res.append((fam, k))
    return res


def title_head(s):
    s = re.sub(r"\s*[-\u2014]+\s*DEMOTED from Tier 1.*$", "", s or "")
    h = re.split(r"[,;:]|\s[-\u2013\u2014]\s", s, maxsplit=1)[0]
    h = re.sub(r"\([^)]*\)", "", h)
    h = re.sub(r"\s+", " ", h).strip().lower()
    return h


def canonical(s):
    """(method, key): url-identifier > text-identifier > url > title head."""
    s = s or ""
    u = src_url(s)
    keys = doc_keys(s)
    if u:
        ukeys = doc_keys(u)
        if ukeys:
            return "url+id", ukeys[0][1]
        if keys:
            return "url+id", keys[0][1]
        return "url", norm_url(u)
    if keys:
        return "id", keys[0][1]
    if s.lower().startswith("no attributed source") or re.search(r"bookkeeping", s, re.I):
        return "none", None
    if INFER.search(s):
        return "inference", None
    return "head", title_head(s)


cmeth = Counter()
ckey = Counter()
ckey_by_method = {}
for _, c in claims:
    m, k = canonical(c["source"])
    cmeth[m] += 1
    if k:
        ckey[k] += 1
        ckey_by_method.setdefault(k, m)
C["sources_as_objects"] = {
    "claim_source_strings_distinct": len(set(c["source"] for _, c in claims)),
    "claims_by_normalisation_method": dict(cmeth.most_common()),
    "claims_resolved_to_canonical_doc_url_or_id": cmeth["url"] + cmeth["url+id"] + cmeth["id"],
    "claims_resolved_by_identifier_without_url": cmeth["id"],
    "canonical_docs_distinct_url_or_id": len([k for k in ckey if ckey_by_method[k] in ("url", "url+id", "id")]),
    "title_heads_distinct": len([k for k in ckey if ckey_by_method[k] == "head"]),
    "claims_title_head_only": cmeth["head"],
}
C["sources_as_objects"]["id_family_counts_in_claims"] = dict(Counter(fam for _, c in claims for fam, _k in doc_keys(c["source"])).most_common())
# top 40 canonical docs (url/id), and title heads separately
top_docs = [(k, v) for k, v in ckey.most_common() if ckey_by_method[k] in ("url", "url+id", "id")][:40]
top_heads = [(k, v) for k, v in ckey.most_common() if ckey_by_method[k] == "head"][:30]
# do those docs exist as nodes (document / legislation)?
docnodes = [e for e in E if e["cls"] in ("document", "legislation")]
evnodes = [e for e in E if e["cls"] == "event"]


def alnum(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def node_doc_index(nodes):
    strict_keys = defaultdict(set)   # identifier parsed out of the node's own label/id
    first = defaultdict(set)         # the node's FIRST source (proxy for 'this node is that document')
    anysrc = defaultdict(set)        # any source of the node cites it
    blobs = {}
    for n in nodes:
        blobs[n["id"]] = alnum(n["label"]) + "|" + alnum(n["id"])
        for fam, k in doc_keys((n["label"] or "") + " " + n["id"]):
            strict_keys[k].add(n["id"])
        for i, s in enumerate(n["sources"]):
            keys = set()
            if s.get("url"):
                keys.add(norm_url(s["url"]))
                keys |= {k for _, k in doc_keys(s["url"])}
            keys |= {k for _, k in doc_keys(s.get("name") or "")}
            for k in keys:
                anysrc[k].add(n["id"])
                if i == 0:
                    first[k].add(n["id"])
    return strict_keys, first, anysrc, blobs


dk_strict, dk_first, dk_any, dk_blob = node_doc_index(docnodes)
ev_strict, ev_first, ev_any, ev_blob = node_doc_index(evnodes)


def strict_match(k, sk, blobs):
    out = set(sk.get(k, ()))
    ak = alnum(k)
    if len(ak) >= 5 and not k.startswith(("http", "www")) and "/" not in k:
        out |= {i for i, b in blobs.items() if ak in b}
    return out


top_docs_rows = []
m_strict = m_first = m_event = 0
for k, v in top_docs:
    s1 = strict_match(k, dk_strict, dk_blob)
    f1 = dk_first.get(k, set())
    e1 = strict_match(k, ev_strict, ev_blob) | ev_first.get(k, set())
    m_strict += bool(s1)
    m_first += bool(s1 or f1)
    m_event += bool(s1 or f1 or e1)
    top_docs_rows.append({"doc": k, "claims": v, "method": ckey_by_method[k],
                          "doc_or_leg_node_strict": sorted(s1)[:4],
                          "doc_or_leg_node_first_source": sorted(f1)[:4],
                          "event_node": sorted(e1)[:3],
                          "cited_by_doc_nodes_any_source": len(dk_any.get(k, ()))})
D["top40_canonical_docs"] = top_docs_rows
D["top30_title_heads_no_url_no_id"] = [[k, v] for k, v in top_heads]
C["sources_as_objects"]["top40_docs_matched_strict_label_or_id"] = m_strict
C["sources_as_objects"]["top40_docs_matched_strict_or_first_source"] = m_first
C["sources_as_objects"]["top40_docs_matched_incl_event_nodes"] = m_event
alldocs = [k for k in ckey if ckey_by_method[k] in ("url", "url+id", "id")]
C["sources_as_objects"]["all_canonical_docs"] = len(alldocs)
C["sources_as_objects"]["all_docs_matched_strict"] = sum(1 for k in alldocs if strict_match(k, dk_strict, dk_blob))
C["sources_as_objects"]["all_docs_matched_strict_or_first_source"] = sum(1 for k in alldocs if strict_match(k, dk_strict, dk_blob) or dk_first.get(k))
C["sources_as_objects"]["all_docs_matched_incl_event_nodes"] = sum(1 for k in alldocs if strict_match(k, dk_strict, dk_blob) or dk_first.get(k) or strict_match(k, ev_strict, ev_blob) or ev_first.get(k))
C["sources_as_objects"]["claims_citing_a_matched_doc"] = sum(v for k, v in ckey.items() if k in set(alldocs) and (strict_match(k, dk_strict, dk_blob) or dk_first.get(k) or strict_match(k, ev_strict, ev_blob) or ev_first.get(k)))
C["sources_as_objects"]["document_legislation_nodes"] = len(docnodes)
C["sources_as_objects"]["singleton_docs_cited_once"] = sum(1 for k in alldocs if ckey[k] == 1)
# edges: structured sources compared
edge_src = [s for e in ED for s in e["sources"]]
edge_keys = Counter()
for s in edge_src:
    t = (s.get("name") or "") + " " + (s.get("url") or "")
    m, k = canonical(t)
    if k:
        edge_keys[(m, k)] += 1
C["sources_as_objects"]["edges"] = {
    "edge_source_objects": len(edge_src),
    "with_url": sum(1 for s in edge_src if s.get("url")),
    "with_name": sum(1 for s in edge_src if s.get("name")),
    "with_date": sum(1 for s in edge_src if s.get("date")),
    "distinct_urls": len({norm_url(s["url"]) for s in edge_src if s.get("url")}),
    "edges_all_sources_have_url": sum(1 for e in ED if e["sources"] and all(s.get("url") for s in e["sources"])),
    "canonical_docs_distinct": len({k for (m, k) in edge_keys if m in ("url", "url+id", "id")}),
}
claim_doc_keys = set(alldocs)
edge_doc_keys = {k for (m, k) in edge_keys if m in ("url", "url+id", "id")}
C["sources_as_objects"]["docs_cited_by_both_claims_and_edges"] = len(claim_doc_keys & edge_doc_keys)
node_src = [s for n in N for s in n["sources"]]
C["sources_as_objects"]["node_level_sources"] = {
    "objects": len(node_src), "with_url": sum(1 for s in node_src if s.get("url")),
    "with_date": sum(1 for s in node_src if s.get("date")),
    "distinct_urls": len({norm_url(s["url"]) for s in node_src if s.get("url")}),
}
allurls = {norm_url(s["url"]) for s in node_src + edge_src if s.get("url")} | {norm_url(src_url(c["source"])) for _, c in claims if src_url(c["source"])}
C["sources_as_objects"]["distinct_urls_anywhere_normalised"] = len(allurls)

# ============================================================== TIMELINE
C["timeline"] = {
    "total": len(TL),
    "by_strand": dict(Counter(t["strand"] for t in TL).most_common()),
    "by_precision": dict(Counter(t["precision"] for t in TL).most_common()),
    "tier_values_raw": dict(Counter(repr(t.get("tier")) for t in TL).most_common()),
    "with_node": sum(1 for t in TL if t.get("node")),
    "node_resolves": sum(1 for t in TL if t.get("node") in ids),
    "with_text": sum(1 for t in TL if t.get("text")),
    "with_label": sum(1 for t in TL if t.get("label")),
    "with_source_string": sum(1 for t in TL if t.get("source")),
    "with_sources_list": sum(1 for t in TL if t.get("sources")),
    "with_any_source": sum(1 for t in TL if t.get("source") or t.get("sources")),
    "with_entities_list": sum(1 for t in TL if t.get("entities")),
    "entities_refs": sum(len(t.get("entities") or []) for t in TL),
    "with_event_field": sum(1 for t in TL if t.get("event")),
    "with_ref_field": sum(1 for t in TL if t.get("ref")),
    "distinct_nodes_linked": len({t["node"] for t in TL if t.get("node")}),
    "events_per_linked_node": dist(list(Counter(t["node"] for t in TL if t.get("node")).values())),
}
C["timeline"]["per_decade"] = dict(sorted(Counter((year_of(t["date"]) // 10 * 10) for t in TL if year_of(t["date"])).items()))
C["timeline"]["strand_by_decade"] = {d: dict(Counter(t["strand"] for t in TL if year_of(t["date"]) and year_of(t["date"]) // 10 * 10 == d)) for d in sorted({year_of(t["date"]) // 10 * 10 for t in TL if year_of(t["date"])})}
C["timeline"]["linked_node_cls"] = dict(Counter(BY[t["node"]]["cls"] for t in TL if t.get("node") in BY))
idpref = Counter(re.split(r"[-_]", t["id"])[0] for t in TL)
D["timeline_id_prefixes"] = top(idpref, 30)
C["timeline"]["nodes_with_timeline_event_pct"] = pct(C["timeline"]["distinct_nodes_linked"], len(N))
C["timeline"]["event_cls_nodes_with_timeline_event"] = sum(1 for e in E if e["cls"] == "event" and any(t.get("node") == e["id"] for t in TL))
C["timeline"]["event_cls_nodes"] = cls["event"]
_evlabels = {(e["label"] or "").lower() for e in E if e["cls"] == "event"}
C["timeline"]["timeline_labels_matching_event_node_label"] = sum(1 for t in TL if (t.get("label") or "").lower() in _evlabels)

# ============================================================== THREADS / MAP / FOIA / PATENTS / HL
th = athreads["threads"]
steps = [s for t in th for s in t["steps"]]
C["threads"] = {"count": len(th), "steps": len(steps),
                "distinct_nodes": len({s["node"] for s in steps}),
                "nodes_covered_pct": pct(len({s["node"] for s in steps}), len(N)),
                "edge_types_used": dict(Counter((s["edge"] or {}).get("type") for s in steps if s["edge"])),
                "edge_kind": dict(Counter((s["edge"] or {}).get("kind") for s in steps if s["edge"])),
                "per_thread_steps": {t["id"]: len(t["steps"]) for t in th}}
C["L0"] = {
    "l0_nodes": len(l0m["l0"]), "counts": l0m["counts"],
    "l0_by_cls": dict(Counter(x["cls"] for x in l0m["l0"])),
    "band_distribution": dict(Counter(n["band"] for n in layout["nodes"])),
    "bands_declared": [b["id"] for b in layout["bands"]],
    "era_distribution": dict(Counter(str(n["era"]) for n in layout["nodes"])),
    "cells_nonempty": len(amap["cells"]),
    "direct_edges": len(amap["direct"]), "summarised_edges": len(amap["summarised"]),
    "entryPaths": [{"id": p["id"], "label": p["label"], "total": p["total"], "onMap": p["onMap"]} for p in amap["entryPaths"]],
    "entryPath_union_ids": len({i for p in amap["entryPaths"] for i in p["ids"]}),
    "members_covered_by_l0": len({m for x in l0m["l0"] for m in x["direct"]} | {r["id"] for x in l0m["l0"] for r in x["routed"]}),
    "authority_nodes": len(l0m["authority"]),
}
C["foia"] = {"requests": len(afoia["requests"]), "nodes": len(afoia["byNode"]),
             "questions_links": sum(len(n["questions"]) + len(n["partial"]) for r in afoia["requests"] for n in r["nodes"]),
             "status": dict(Counter(r["status"] for r in afoia["requests"])),
             "agencies": dict(Counter(r["agency"] for r in afoia["requests"]))}
C["patents"] = {"filings": len(apat["patents"]), "with_node": sum(1 for p in apat["patents"] if p.get("node")),
                "sheets": sum(len(p.get("sheets") or []) for p in apat["patents"]),
                "openQuestions": len(apat.get("openQuestions") or []),
                "observables": len((apat.get("observables") or {}).get("observables") or []) if isinstance(apat.get("observables"), dict) else None}
C["highlights"] = {"flags": len(ahl["flags"]), "ids": [f["id"] for f in ahl["flags"]]}

# gaps (tools/GAPS.json)
gaps = rd("tools/GAPS.json")
gtext = [(g["gap"] if isinstance(g["gap"], str) else (g["gap"].get("text") or "")) for g in gaps]
# node mention in text by id token or exact label (labels >= 8 chars), via token n-grams
WTOK = re.compile(r"[a-z0-9]+")
label_grams = {}
for n in N:
    lab = n["label"] or ""
    if len(lab) >= 8:
        g = tuple(WTOK.findall(lab.lower()))
        if g:
            label_grams.setdefault(g, set()).add(n["id"])
gram_lens = sorted({len(g) for g in label_grams})
IDTOK = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)+")
long_ids = {i for i in ids if len(i) >= 6}


def mentions(text):
    tl = (text or "").lower()
    hit = set()
    for t in IDTOK.findall(tl):
        if t in long_ids:
            hit.add(t)
    w = WTOK.findall(tl)
    for s in range(len(w)):
        for L in gram_lens:
            if s + L > len(w):
                break
            g = tuple(w[s:s + L])
            if g in label_grams:
                hit |= label_grams[g]
    return hit
gm = [mentions(t) for t in gtext]
C["gaps"] = {"records": len(gaps), "free_string": sum(1 for g in gaps if isinstance(g["gap"], str)),
             "structured": sum(1 for g in gaps if isinstance(g["gap"], dict)),
             "structured_with_wouldClose": sum(1 for g in gaps if isinstance(g["gap"], dict) and g["gap"].get("wouldClose")),
             "have_node_field": 0,
             "text_mentions_a_node_label_or_id": sum(1 for h in gm if h),
             "distinct_nodes_mentioned": len(set().union(*gm)) if gm else 0,
             "by_file_top": top(Counter(g["domain"] for g in gaps), 15)}

# claim text mentions of OTHER nodes (latent cross-links), heuristic, labels >= 8 chars
cross = 0
cross_pairs = set()
for n, c in claims:
    h = {x for x in mentions(c["text"]) if x != n["id"]}
    if h:
        cross += 1
        for x in h:
            cross_pairs.add(tuple(sorted((n["id"], x))))
edge_pairs = set(tuple(sorted((e["a"], e["b"]))) for e in ED)
C["claims"]["text_mentions_another_node"] = cross
C["claims"]["mention_pairs_distinct"] = len(cross_pairs)
C["claims"]["mention_pairs_not_joined_by_edge"] = len(cross_pairs - edge_pairs)

# ids
pref = Counter()
for n in N:
    m = re.match(r"^([a-z]{1,4})-", n["id"])
    pref[(n["cls"], m.group(1) if m else "(none)")] += 1
D["id_prefix_by_cls"] = [[a + ":" + b, v] for (a, b), v in sorted(pref.items(), key=lambda kv: -kv[1])[:40]]
C["ids"] = {
    "location_ids_with_l_prefix": sum(1 for e in E if e["cls"] == "location" and e["id"].startswith("l-")),
    "location_ids_total": cls["location"],
    "nonlocation_ids_with_l_prefix": sum(1 for e in E if e["cls"] != "location" and e["id"].startswith("l-")),
    "domain_ids_with_d_prefix": sum(1 for e in E if e["cls"] == "domain" and e["id"].startswith("d-")),
    "domain_ids_total": cls["domain"],
    "event_ids_with_ev_prefix": sum(1 for e in E if e["cls"] == "event" and e["id"].startswith("ev-")),
    "event_ids_total": cls["event"],
    "document_ids_with_doc_prefix": sum(1 for e in E if e["cls"] == "document" and e["id"].startswith("doc-")),
    "document_ids_total": cls["document"],
    "ids_with_year_token": sum(1 for n in N if re.search(r"(?<!\d)(19|20)\d\d(?!\d)", n["id"])),
    "removed_list": len(rd("research/_removed.json")["remove"]),
    "alias_map": len(rd("research/_removed.json")["alias"]),
    "probable_duplicates_integrity": len(rd("tools/INTEGRITY.json").get("probable_duplicate_node", [])),
}
D["probable_duplicates"] = rd("tools/INTEGRITY.json").get("probable_duplicate_node", [])

# stubs: nodes whose only provenance is a stub file
stubby = [n["id"] for n in N if set(n["_domains"]) <= {"_stubs", "_rs-stubs-known"}]
C["stub_only_nodes"] = len(stubby)
C["stub_only_by_cls"] = dict(Counter(BY[i]["cls"] for i in stubby))
C["bookkeeping_nodes"] = len({n["id"] for n, c in claims if re.search(r"bookkeeping", c["source"] or "", re.I)})

json.dump(C, open(os.path.join(HERE, "census.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(D, open(os.path.join(HERE, "census_detail.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ok", len(json.dumps(C)), len(json.dumps(D)))
