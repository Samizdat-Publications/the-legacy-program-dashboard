# -*- coding: utf-8 -*-
"""Extra measurements, then merge census.json + census_detail.json + latent.json + these
into one census.json. Read-only on the repo."""
import collections
import glob
import json
import os
import re

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
P, E, ED, TL, EI = b["people"], b["entities"], b["edges"], b["timeline"], b["entityInfo"]
N = P + E
BY = {n["id"]: n for n in N}
ids = set(BY)
edges = set(tuple(sorted((e["a"], e["b"]))) for e in ED)
nb = defaultdict(set)
for e in ED:
    nb[e["a"]].add(e["b"])
    nb[e["b"]].add(e["a"])
X = {}

# 1. person structural fields: joined by an explicit edge or latent
X["person_fields_vs_edges"] = {
    "instId_set": sum(1 for p in P if p["instId"]),
    "instId_joined_by_edge": sum(1 for p in P if p["instId"] and tuple(sorted((p["id"], p["instId"]))) in edges),
    "locId_set": sum(1 for p in P if p["locId"]),
    "locId_joined_by_edge": sum(1 for p in P if p["locId"] and tuple(sorted((p["id"], p["locId"]))) in edges),
    "domain_tags": sum(len(p["domains"]) for p in P),
    "domain_tags_joined_by_edge": sum(1 for p in P for x in p["domains"] if tuple(sorted((p["id"], x))) in edges),
    "app_reads_instId_locId_loc": False,
    "shipped_node_files_domains_field_is_provenance_not_topic_tags": True,
}
WT = re.compile(r"[a-z0-9]+")
grams = {}
for n in E:
    for lab in {n["label"], re.sub(r"\s*\([^)]*\)", "", n["label"])}:
        g = tuple(WT.findall(lab.lower()))
        if g and len(lab) >= 4:
            grams.setdefault(g, set()).add(n["id"])
    for m in re.findall(r"\(([A-Z][A-Za-z0-9&/-]{2,})\)", n["label"]):
        grams.setdefault((m.lower(),), set()).add(n["id"])
lens = sorted({len(g) for g in grams})
tot = hit = 0
pairs = set()
for p in P:
    for a in p["affiliations"]:
        tot += 1
        w = WT.findall(a.lower())
        h = set()
        for s in range(len(w)):
            for L in lens:
                if s + L > len(w):
                    break
                g = tuple(w[s:s + L])
                if g in grams:
                    h |= grams[g]
        hit += bool(h)
        pairs |= {(p["id"], x) for x in h}
X["affiliations_latent_INFERRED"] = {"strings": tot, "strings_mentioning_a_non_person_node": hit,
                                     "person_node_pairs": len(pairs),
                                     "pairs_already_edges": sum(1 for a, c in pairs if tuple(sorted((a, c))) in edges)}

# 2. places for events/programs/institutions
def adj_cls(n, c):
    return any(BY[x]["cls"] == c for x in nb[n["id"]])


X["place_links"] = {c: [sum(1 for n in N if n["cls"] == c and adj_cls(n, "location")), sum(1 for n in N if n["cls"] == c)]
                    for c in ("event", "program", "institution", "document", "person")}
X["place_links"]["events_with_coords"] = sum(1 for n in E if n["cls"] == "event" and n["coords"])
X["place_links"]["coords_source"] = "tools/regrade.py GAZETTEER (lines 157-237) written into research/_remediation.json; only location-class nodes carry coords"

# 3. claims vs timeline vs events
MON = {m: i + 1 for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                        "september", "october", "november", "december"])}
DR = re.compile(r"\b(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (1[89]\d\d|20[0-2]\d)\b")
tl_by_node = defaultdict(set)
for t in TL:
    if t.get("node"):
        tl_by_node[t["node"]].add(t["date"][:10])
alltl = {t["date"][:10] for t in TL}
dated = same = anyd = 0
for n in N:
    for c in n["claims"]:
        ds = {"%s-%02d-%02d" % (y, MON[m.lower()], int(d)) for d, m, y in DR.findall(c["text"])}
        if ds:
            dated += 1
            same += bool(ds & tl_by_node[n["id"]])
            anyd += bool(ds & alltl)
X["claims_vs_timeline"] = {"claims_with_day_date_in_text": dated, "date_matches_timeline_event_on_same_node": same,
                           "date_matches_any_timeline_event": anyd, "claims_have_date_field": False,
                           "timeline_events_have_claim_link": False}
KEYS = {"hearing-2023-07-26": r"26 July 2023|July 26, 2023|2023-07-26", "hearing-2024-11-13": r"13 November 2024|November 13, 2024",
        "hearing-2025-09-09": r"9 September 2025|September 9, 2025", "roswell-1947": r"Roswell", "nimitz-2004": r"Nimitz"}
X["event_claims_scattered"] = {k: {"claims_on_node": len(BY[k]["claims"]),
                                   "claims_elsewhere_mentioning": sum(1 for n in N for c in n["claims"] if n["id"] != k and re.search(rx, c["text"])),
                                   "nodes_elsewhere": len({n["id"] for n in N for c in n["claims"] if n["id"] != k and re.search(rx, c["text"])})}
                               for k, rx in KEYS.items()}

# 4. speaker named in source (INFERRED via unique surnames of person nodes)
WA = re.compile(r"[A-Za-z]+")
sur = Counter()
toks_of = {}
for p in P:
    t = [x for x in WA.findall(re.sub(r"\([^)]*\)|\"[^\"]*\"", "", p["label"])) if len(x) > 1]
    toks_of[p["id"]] = t
    if t:
        sur[t[-1].lower()] += 1
uniq = {t[-1].lower(): pid for pid, t in toks_of.items() if t and sur[t[-1].lower()] == 1 and len(t[-1]) >= 5}
sp = Counter()
selfsrc = Counter()
for n in N:
    for c in n["claims"]:
        s = {uniq[w.lower()] for w in WA.findall(c["source"] or "") if w.lower() in uniq}
        sp[(c["tier"], bool(s))] += 1
        if n["cls"] == "person" and n["id"] in s:
            selfsrc[c["tier"]] += 1
X["speaker_named_in_source_INFERRED"] = {"by_tier": {t: {"named": sp[(t, True)], "not_named": sp[(t, False)]} for t in (1, 2, 3)},
                                         "claims_on_person_node_sourced_to_that_person": dict(selfsrc),
                                         "method": "unique surnames (>=5 letters) of the 338 person labels found in the claim source string"}

# 5. orphaned entityInfo essays
origin = defaultdict(list)
for f in glob.glob(os.path.join(ROOT, "research", "*.json")):
    doc = json.load(open(f, encoding="utf-8"))
    if isinstance(doc, dict):
        for k in (doc.get("entityInfo") or {}):
            origin[k].append(os.path.basename(f))
X["entityInfo_orphans"] = [{"key": k, "chars": len(str((v.get("desc") if isinstance(v, dict) else v) or "")), "from": origin.get(k)}
                           for k, v in sorted(EI.items()) if k not in ids]
X["entityInfo_orphans_substantive_ge400"] = sum(1 for r in X["entityInfo_orphans"] if r["chars"] >= 400)

# 6. timeline tier vocabulary by id prefix
tt = defaultdict(Counter)
for t in TL:
    tt[re.split(r"[-_]", t["id"])[0]][repr(t.get("tier"))] += 1
X["timeline_tier_by_id_prefix"] = {k: dict(v) for k, v in tt.items()}
X["timeline_shipped_fields"] = "app/public/data/timeline.json rows carry date, era, id, label, node, precision, strand, text, tier only (build_app_data.py timeline_json lines 405-420); source/sources/entities/event/ref are not shipped"
X["edges_json_shipped_fields"] = "app/public/data/edges.json rows carry a, b, dateStart, label, t, tier only (build_app_data.py lines 396-402); note, sources and dateEnd ship only inside nodes/<id>.json connections"

# 7. notes that admit the edge vocabulary cannot say it
wk = [e for e in ED if re.search(r"no \w+ edge type|TYPED \w+|INTENT:|deliberately NOT built as|edge type is used because", e["note"])]
X["edge_notes_admitting_type_workaround"] = {"count": len(wk), "examples": [[e["type"], e["a"], e["b"], e["note"][:140]] for e in wk[:6]]}

# 8. status semantics
FORMER = re.compile(r"\b(former|retired|ex-|until \d{4}|to \d{4}|\d{4}\s*[-\u2013]\s*\d{4})\b", re.I)
X["status_semantics"] = {"vocab": dict(Counter(p["status"] for p in P)),
                         "active_with_former_or_dated_role_in_sub_INFERRED": sum(1 for p in P if p["status"] == "active" and FORMER.search(p["sub"] or "")),
                         "vital_values": ["dead", "deceased", "alive", "missing"], "role_values": ["active", "former"],
                         "editorial_values": ["fabricated", "resolved", "unknown"]}

# 9. duplicates the detector misses
X["duplicate_documents_not_flagged"] = [{"a": "gao-nsiad-95-187", "b": "gao-roswell-report-1995",
                                          "why": "both labels carry GAO/NSIAD-95-187; sources differ (gao.gov vs govinfo.gov) so merge.duplicate_groups, which requires a shared URL, does not pair them",
                                          "a_label": BY["gao-nsiad-95-187"]["label"][:80], "b_label": BY["gao-roswell-report-1995"]["label"][:80]}]

# 10. manual adjudication of the top-40 cited documents (MANUAL, by reading ids/labels)
MANUAL = {
    "PL 118-31": ("yes", "ndaa-fy2024 (+ section nodes)"),
    "10 USC 119": ("yes", "usc-10-119, usc-10-119e"),
    "CHRG-119hhrg61718": ("event only", "hearing-2025-09-09 is an event node; no document node for the transcript"),
    "DODI 5205.11": ("yes", "dodi-5205-11"),
    "CHRG-118hhrg53022": ("event only", "hearing-2023-07-26"),
    "DODD 5205.07": ("yes", "dodd-5205-07-2010, dodd-5205-07-2024"),
    "CHRG-118hhrg57440": ("event only", "hearing-2024-11-13"),
    "GAO-NSIAD-95-187": ("yes, twice", "gao-nsiad-95-187 AND gao-roswell-report-1995 (duplicate)"),
    "archive.org/stream/DisclosureProjectBriefingDocument/DisclosureProjectBriefingDocument_djvu.txt": ("yes", "disclosure-project-briefing-2001"),
    "S 2226": ("yes", "s2226-118"),
    "irp.fas.org/dia/aatip-list.pdf": ("yes", "dia-aatip-list-2019 (its own first source is a different fas.org URL)"),
    "PL 119-60": ("yes", "ndaa-fy2026"),
    "ufos-scientificresearch.blogspot.com/2019/01/back-to-those-38-defense-intelligence.html": ("no", "blog post"),
    "DODM 5205.07": ("yes", "dodm-5205-07-v1, dodm-5205-07-series (flagged probable duplicates)"),
    "PL 117-263": ("yes", "ndaa-fy2023 (carries a Board-bookkeeping placeholder claim)"),
    "ICD 906": ("yes", "icd-906"),
    "cdn.centerforinquiry.org/wp-content/uploads/sites/29/2022/09/26195512/SUN-68-Summer-2001.pdf": ("no", "CSICOP newsletter"),
    "arvp.co.uk/wp-content/uploads/2024/12/SORENSEN-1990-INTERVIEW.pdf": ("yes", "scott-sorensen-notes-1990"),
    "cdn.centerforinquiry.org/wp-content/uploads/sites/29/1993/01/22165151/p77.pdf": ("no", "Skeptical Inquirer article"),
    "50 USC 3091a": ("yes", "usc-50-3091a"),
    "ntrs.nasa.gov/api/citations/20040070788/downloads/20040070788.pdf": ("yes", "millis-tm-2004-213082"),
    "media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-CLEARED-508-COMPLIANT-HRRV1-08-MAR-2024-FINAL.PDF": ("yes", "aaro-historical-record-vol1 (URL variant)"),
    "PL 118-159": ("yes", "ndaa-fy2025"),
    "50 USC 3348": ("yes", "usc-50-3348"),
    "50 USC 3093": ("yes", "usc-50-3093"),
    "FOIA 18-F-0324": ("yes", "foia-18-f-0324"),
    "checktheevidence.com/pdf/Edgar%20Fouche%20-%201998%20Presentation%20to%20IUFOC.pdf": ("yes", "fouche-iufoc-1998"),
    "irp.fas.org/budget/index.html": ("partial", "intel-budget-disclosure-record is a collection node, not this page"),
    "aaro.mil/Portals/136/PDFs/AARO_Historical_Record_Report_Vol_1_2024.pdf": ("yes", "aaro-historical-record-vol1 (second URL variant of the same report)"),
    "intelligence.senate.gov/sites/default/files/hearings/95mkultra.pdf": ("partial", "mkultra program node exists; no node for the 1977 hearing record"),
    "checktheevidence.com/pdf/Edgar%20Fouches%20Military%20Documents.pdf": ("yes", "fouche-military-documents"),
    "EO 13526": ("yes", "eo-13526"),
    "PL 119-75": ("partial", "section nodes only (classified-annex, sec-8005-transfer, sec-8009-sap-notice)"),
    "ia800403.us.archive.org/17/items/pdfy-NRIQie2ooVehep7K/The%20Cometa%20Report%20%5BUFO%27s%20And%20Defense%20-%20What%20Should%20We%20Prepare%20For%5D.pdf": ("yes", "doc-cometa-report"),
    "US-PAT 10144532": ("yes", "pais-patent-imrd"),
    "SAMDT 797": ("yes", "samdt-797"),
    "files.fasab.gov/pdffiles/handbook_sffas_56.pdf": ("yes", "sffas-56"),
    "50 USC 3373": ("partial", "carried by ndaa-fy2022-sec-1683 (the enacting section), no node for the codified section"),
    "aaro.mil/Portals/136/PDFs/FY25%20UAP%20Annual%20Report/AARO_FY2025_Consolidated_Annual_Report_on_UAP.pdf": ("yes", "aaro-fy2025-annual-report"),
    "burlison.house.gov/sites/evo-subsites/burlison.house.gov/files/evo-media-document/memorandum_2026.pdf": ("yes", "odni-memo-es-2026-00818"),
}
C = json.load(open(os.path.join(HERE, "census.json"), encoding="utf-8"))
if "headline" in C:          # idempotent re-run
    C = C["headline"]
D = json.load(open(os.path.join(HERE, "census_detail.json"), encoding="utf-8"))
L = json.load(open(os.path.join(HERE, "latent.json"), encoding="utf-8"))
rows = []
for r in D["top40_canonical_docs"]:
    k = r["doc"]
    v = MANUAL.get(k)
    if v is None:
        v = next((MANUAL[m] for m in MANUAL if k.startswith(m[:60]) or m.startswith(k[:60])), ("unadjudicated", ""))
    rows.append({"claims": r["claims"], "doc": k, "node": v[0], "which": v[1]})
X["top40_docs_manual"] = rows
X["top40_docs_manual_tally"] = dict(Counter(r["node"] for r in rows))
out = {"_what": "Census of the-program data model, measured 2026-09-24 against master 838c134 (board generated 2026-09-19). "
                "headline = census.py; detail = census.py tables; latent = latent.py; extras = extras.py. "
                "Keys ending _INFERRED or marked heuristic are heuristics, everything else is a direct count.",
       "headline": C, "detail": D, "latent": L, "extras": X}
out["_what"] += " Em dashes quoted from repo data are replaced by ' - ' in these outputs."
json.dump(out, open(os.path.join(HERE, "census.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=list)
for fn in ("census.json", "census_detail.json", "latent.json", "edge_examples.json"):
    pth = os.path.join(HERE, fn)
    if os.path.exists(pth):
        txt = open(pth, encoding="utf-8").read()
        if chr(0x2014) in txt:
            open(pth, "w", encoding="utf-8").write(txt.replace(chr(0x2014), " - "))
print(json.dumps(X["top40_docs_manual_tally"]), X["entityInfo_orphans_substantive_ge400"], X["place_links"], X["person_fields_vs_edges"], X["affiliations_latent_INFERRED"])
