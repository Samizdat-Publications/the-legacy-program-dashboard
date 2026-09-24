# -*- coding: utf-8 -*-
"""Latent-structure and edge-semantics measurements. Read-only on the repo.
Writes latent.json beside this script."""
import collections
import json
import os
import re
import statistics

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
# Outputs go outside the repo so a run never dirties the tree (CENSUS_OUT, else system temp).
import tempfile
HERE = os.environ.get("CENSUS_OUT") or os.path.join(tempfile.gettempdir(), "the-program-census")
os.makedirs(HERE, exist_ok=True)
Counter, defaultdict = collections.Counter, collections.defaultdict


def rd(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


b = rd("data/the-program.json")
P, E, ED, TL = b["people"], b["entities"], b["edges"], b["timeline"]
N = P + E
BY = {n["id"]: n for n in N}
NN = len(N)
l0m = rd("data/l0-model.json")
L = {}


def pct(a, n=NN):
    return round(100.0 * a / n, 1)


# ---------------------------------------------------------------- 1. research files as topics
OVERLAY = {"_corrections", "_remediation", "_stubs", "_edge_tiers", "_removed", "_authority", "_dird-verification",
           "_rs-stubs-known", "_rs-archive-mirror"}
MAINT = re.compile(r"^w(6-edges|8-|10-(collapse|domains|notification)|11-(final|setka|statutory)|12-(dod-house|duplicate|narrative|notification|tiera|twin|eo13526|sap-statutory|sec6802|nispom)|13-|14-|15-|16-|17-)")
# Everything else is a topical case / storyline / source-corpus file (INFERRED classification, by file name + domain string)
nodes_topics = {}
file_nodes = defaultdict(set)
for n in N:
    t = sorted(d for d in n["_domains"] if d not in OVERLAY and not MAINT.match(d))
    nodes_topics[n["id"]] = t
    for d in t:
        file_nodes[d].add(n["id"])
ntop = Counter(len(v) for v in nodes_topics.values())
L["topic_files"] = {
    "rule": "research/*.json minus overlays (_corrections, _remediation, _stubs, _edge_tiers, _removed, _authority, _dird-verification, _rs-stubs-known, _rs-archive-mirror) minus wiring/maintenance passes (w6-edges-*, w8, w10-collapse/domains/notification, w11-final/setka/statutory, most w12, w13-w17)",
    "topic_files_contributing_nodes": len(file_nodes),
    "nodes_with_1plus_topic_file": sum(1 for v in nodes_topics.values() if v),
    "nodes_with_exactly_1": ntop[1],
    "nodes_with_2plus": sum(v for k, v in ntop.items() if k >= 2),
    "nodes_with_0": ntop[0],
    "files_per_node_hist": dict(sorted(ntop.items())),
    "nodes_per_topic_file": sorted([[k, len(v)] for k, v in file_nodes.items()], key=lambda x: -x[1]),
}
L["topic_files"]["zero_topic_nodes_by_provenance"] = Counter(
    "+".join(sorted(BY[i]["_domains"]))[:60] for i, v in nodes_topics.items() if not v).most_common(12)
# edges by topic file (edges carry _domains too)
edge_topic = Counter()
edges_with_topic = 0
for e in ED:
    t = [d for d in e["_domains"] if d not in OVERLAY and not MAINT.match(d)]
    if t:
        edges_with_topic += 1
    for d in t:
        edge_topic[d] += 1
L["topic_files"]["edges_with_1plus_topic_file"] = edges_with_topic
L["topic_files"]["edges_per_topic_file_top"] = edge_topic.most_common(20)
# intra-topic cohesion: share of a file's edges whose both endpoints carry that file
coh = {}
for f, ns in file_nodes.items():
    es = [e for e in ED if f in e["_domains"]]
    if len(es) >= 15:
        coh[f] = round(sum(1 for e in es if e["a"] in ns and e["b"] in ns) / len(es), 2)
L["topic_files"]["edge_endpoint_cohesion"] = dict(sorted(coh.items(), key=lambda kv: -kv[1]))

# ---------------------------------------------------------------- 2. domain nodes as topics
dom_nodes = {e["id"] for e in E if e["cls"] == "domain"}
tag_people = defaultdict(set)
for p in P:
    for d in p["domains"]:
        tag_people[d].add(p["id"])
edge_to_domain = defaultdict(set)
for e in ED:
    for x, y in ((e["a"], e["b"]), (e["b"], e["a"])):
        if y in dom_nodes and x not in dom_nodes:
            edge_to_domain[y].add(x)
covered_people = {p["id"] for p in P if p["domains"]}
covered_any = covered_people | set().union(*edge_to_domain.values())
L["domain_topics"] = {
    "domain_nodes": len(dom_nodes),
    "people_tagged_via_domains_field": len(covered_people),
    "entities_linked_by_edge_to_a_domain_node": len({x for s in edge_to_domain.values() for x in s if BY[x]["cls"] != "person"}),
    "people_linked_by_edge_to_a_domain_node": len({x for s in edge_to_domain.values() for x in s if BY[x]["cls"] == "person"}),
    "nodes_with_any_domain_topic": len(covered_any),
    "domain_nodes_used_by_people_field": len(tag_people),
    "domain_nodes_with_edges": len(edge_to_domain),
    "per_domain": sorted([[d, BY[d]["label"][:40], len(tag_people.get(d, ())), len(edge_to_domain.get(d, ()))]
                          for d in dom_nodes], key=lambda r: -(r[2] + r[3])),
    "tags_per_tagged_person": statistics.median([len(p["domains"]) for p in P if p["domains"]]),
}

# ---------------------------------------------------------------- 3. hubs by class (cases, programmes, places)
nb = defaultdict(set)
for e in ED:
    nb[e["a"]].add(e["b"])
    nb[e["b"]].add(e["a"])


def hub_cover(cl):
    hubs = [n["id"] for n in N if n["cls"] == cl]
    cov = set()
    for h in hubs:
        cov |= nb[h]
    sizes = [len(nb[h]) for h in hubs]
    return {"hubs": len(hubs), "union_1hop": len(cov - set(hubs)), "union_1hop_people": len({x for x in cov if BY[x]["cls"] == "person"}),
            "nbhd_size_median": statistics.median(sizes) if sizes else 0, "nbhd_size_max": max(sizes) if sizes else 0,
            "hubs_with_ge5_neighbours": sum(1 for s in sizes if s >= 5)}


L["hub_cover"] = {c: hub_cover(c) for c in ("event", "program", "location", "institution", "document", "legislation")}
people_with_event = sum(1 for p in P if any(BY[x]["cls"] == "event" for x in nb[p["id"]]))
L["hub_cover"]["people_adjacent_to_an_event"] = people_with_event
L["hub_cover"]["people_adjacent_to_a_program"] = sum(1 for p in P if any(BY[x]["cls"] == "program" for x in nb[p["id"]]))
L["hub_cover"]["people_adjacent_to_event_or_program"] = sum(1 for p in P if any(BY[x]["cls"] in ("event", "program") for x in nb[p["id"]]))
# events typed by label (INFERRED): hearing / incident / release / meeting / conference / publication
EVK = [("hearing", r"hearing|testimony|briefing"), ("incident/sighting", r"incident|encounter|sighting|crash|case|intercept|landing|lights|flap|ufo|uap|video"),
       ("release/publication", r"release|publication|report|disclosure|press"), ("meeting/conference", r"meeting|conference|symposium|summit|panel|forum"),
       ("legal/admin", r"lawsuit|court|order|memo|directive|executive|decision|termination|established|creation")]
evtype = Counter()
for e in E:
    if e["cls"] != "event":
        continue
    lab = (e["label"] + " " + (e["sub"] or "")).lower()
    k = next((k for k, rx in EVK if re.search(rx, lab)), "other")
    evtype[k] += 1
L["event_nodes_by_label_keyword_INFERRED"] = dict(evtype.most_common())

# ---------------------------------------------------------------- 4. L0 containment as an existing grouping
direct_parents = defaultdict(set)
routed_parent = {}
for x in l0m["l0"]:
    for m in x["direct"]:
        direct_parents[m].add(x["id"])
    for r in x["routed"]:
        routed_parent[r["id"]] = x["id"]
l0ids = {x["id"] for x in l0m["l0"]}
npar = Counter(len(v) for v in direct_parents.values())
L["l0_containment"] = {
    "l0": len(l0ids),
    "direct_members_distinct": len(direct_parents),
    "direct_members_with_exactly_1_parent": npar[1],
    "direct_members_with_2plus_parents": sum(v for k, v in npar.items() if k >= 2),
    "direct_parent_count_hist": dict(sorted(npar.items())),
    "routed_members": len(routed_parent),
    "pathOnly": len(l0m["pathOnly"]), "unattached": len(l0m["unattached"]),
    "people_direct_members": sum(1 for i in direct_parents if BY[i]["cls"] == "person"),
    "member_count_per_l0": statistics.median([len(x["direct"]) + len(x["routed"]) for x in l0m["l0"]]),
}

# ---------------------------------------------------------------- 5. off-vocab cluster tags and slug subs
L["slug_sub_taxonomy"] = Counter(e["sub"] for e in E if re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", e["sub"] or "")).most_common(30)
L["id_families"] = Counter(re.match(r"^([a-z]+)", n["id"]).group(1) for n in E if n["cls"] in ("document", "legislation", "event")).most_common(25)

# ---------------------------------------------------------------- 6. edge label verb families (INFERRED lexicon)
FAM = [
    ("role/employment", r"\b(served|serving|serves|director|chief|head|chair(man|woman)?|member|employee|officer|staff|worked|works|employed|commander|commanded|deputy|analyst|scientist|engineer|professor|president|ceo|board|liaison|billet|assigned|posted|stationed|senior|former|appointed|nominated|hired)\b"),
    ("founding/ownership", r"\b(found(ed|er|ing)|co-?found|owns?|owned|owner|established|creat(ed|es)|formed|launched|set up|stood up)\b"),
    ("authorship/publication", r"\b(author(ed|s)?|co-?author|wrote|written|writes|publish(ed|es|er)|editor|byline|reporter|reported|broke the story|article|book|paper)\b"),
    ("testimony/statement", r"\b(testif(ied|ies|y)|testimony|sworn|witness|deposition|statement|said|says|told|claims?|claimed|alleg(es|ed)|recalled|describes?|described|interview(ed)?|account)\b"),
    ("funding/contract", r"\b(fund(ed|s|ing)?|paid|pay|appropriat\w*|contract(ed|or|s)?|award(ed)?|grant|budget|\$|money|financ\w*|invest\w*)\b"),
    ("custody/material", r"\b(held|holds|hold|custody|recover(ed|y)|retriev\w*|stor(ed|es|age)|possess\w*|transferr?(ed)?|shipped|material|specimen|debris|craft|wreckage)\b"),
    ("denial/refusal", r"\b(den(ied|ies|y|ial)|no record|refus\w*|reject\w*|dismiss\w*|debunk\w*|disput\w*|contradict\w*|rebut\w*|withheld|declin\w*)\b"),
    ("legislative act", r"\b(sponsor\w*|cosponsor\w*|introduc\w*|enact\w*|amend\w*|codif\w*|section|sec\.|statute|bill|act\b|requires|mandat\w*|law|provision|repeal\w*|vote[ds]?)\b"),
    ("investigation/review", r"\b(investigat\w*|probe|inquir\w*|review\w*|audit\w*|examin\w*|analy[sz]\w*|assess\w*|study|studied|evaluat\w*|search\w*|foia)\b"),
    ("communication/briefing", r"\b(letter|briefed|briefing|request(ed|s)?|asked|questioned|questioning|referr?(ed|al)|wrote to|memo|email|contacted|met|meeting|conversation)\b"),
    ("place/located", r"\b(located|based|site|near|headquarter\w*|facility|base|at the|in the)\b"),
    ("succession/sequence", r"\b(succeed\w*|replac\w*|preced\w*|successor|predecessor|follow\w*|cancel\w*|superseded|renamed|became|later|before|after|days|years)\b"),
    ("part-of/structure", r"\b(part of|parent|subcommittee|division|unit|component|under|within|subordinate|office of|branch|element|series|volume|annex|contains?|included)\b"),
]
fam_by_type = defaultdict(Counter)
fam_count = Counter()
edges_no_family = Counter()
multi = 0
for e in ED:
    lab = (e["label"] or "").lower()
    fs = [k for k, rx in FAM if re.search(rx, lab)]
    if len(fs) >= 2:
        multi += 1
    if not fs:
        edges_no_family[e["type"]] += 1
    for k in fs:
        fam_by_type[e["type"]][k] += 1
        fam_count[k] += 1
tcount = Counter(e["type"] for e in ED)
L["label_families"] = {
    "note": "keyword lexicon over edge LABELS; one label can hit several families (INFERRED, heuristic)",
    "labels_hitting_2plus_families": multi,
    "labels_hitting_none": sum(edges_no_family.values()),
    "by_type_top": {t: [[k, v, round(100.0 * v / tcount[t])] for k, v in fam_by_type[t].most_common(5)] for t in tcount},
    "family_spread_across_types": {k: len([t for t in tcount if fam_by_type[t][k] >= 5]) for k, _ in FAM},
    "no_family_by_type": dict(edges_no_family),
}
# where does 'testimony' land? which edge types carry testimony-family labels
L["testimony_family_edge_types"] = dict(Counter(e["type"] for e in ED if re.search(FAM[3][1], (e["label"] or "").lower())).most_common())
L["authorship_family_edge_types"] = dict(Counter(e["type"] for e in ED if re.search(FAM[2][1], (e["label"] or "").lower())).most_common())
L["funding_family_edge_types"] = dict(Counter(e["type"] for e in ED if re.search(FAM[4][1], (e["label"] or "").lower())).most_common())
L["denial_family_edge_types"] = dict(Counter(e["type"] for e in ED if re.search(FAM[6][1], (e["label"] or "").lower())).most_common())
# direction: does a->b have a consistent meaning? share of person endpoints on 'a' side, per type
dirn = {}
for t in tcount:
    es = [e for e in ED if e["type"] == t]
    pa = sum(1 for e in es if BY[e["a"]]["cls"] == "person")
    pb = sum(1 for e in es if BY[e["b"]]["cls"] == "person")
    dirn[t] = {"person_on_a": pa, "person_on_b": pb, "n": len(es)}
L["direction_person_side"] = dirn
# the geographic type: how many geographic edges actually touch a location node
L["geographic_edges_touching_location_node"] = sum(1 for e in ED if e["type"] == "geographic" and ("location" in (BY[e["a"]]["cls"], BY[e["b"]]["cls"])))
L["edges_touching_location_node_by_type"] = dict(Counter(e["type"] for e in ED if "location" in (BY[e["a"]]["cls"], BY[e["b"]]["cls"])).most_common())
L["edges_touching_domain_node_by_type"] = dict(Counter(e["type"] for e in ED if "domain" in (BY[e["a"]]["cls"], BY[e["b"]]["cls"])).most_common())
L["temporal_edges_with_both_dates"] = sum(1 for e in ED if e["type"] == "temporal" and e["dateStart"])
L["type_pair_matrix_top"] = Counter((e["type"], BY[e["a"]]["cls"], BY[e["b"]]["cls"]) for e in ED).most_common(25)

# ---------------------------------------------------------------- 7. dates on edges and time coverage
L["edge_dates"] = {
    "with_dateStart": sum(1 for e in ED if e["dateStart"]),
    "dateStart_precision": dict(Counter(("day" if re.match(r"^\d{4}-\d{2}-\d{2}$", e["dateStart"]) else "month" if re.match(r"^\d{4}-\d{2}$", e["dateStart"]) else "year" if re.match(r"^\d{4}$", e["dateStart"]) else "other") for e in ED if e["dateStart"])),
}
# ---------------------------------------------------------------- 8. person status semantics
L["person_status_vs_sub"] = Counter((p["status"], bool(re.search(r"\b(former|retired|ex-)\b", p["sub"] or "", re.I))) for p in P).most_common()
L["person_status_dead_without_death_word_in_sub"] = sum(1 for p in P if p["status"] in ("dead", "deceased") and not re.search(r"\b(died|death|d\.|deceased|\(\d{4}\s*[-\u2013]\s*\d{4}\))", (p["sub"] or "") + " " + (p["narrative"] or "")[:400], re.I))
json.dump(L, open(os.path.join(HERE, "latent.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=list)
print("ok")
