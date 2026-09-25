"""Duplicate-candidate finder for data/the-program.json (redesign phase 4, task 2).

Reads the merged board and writes the candidate pairs and clusters to
tools/topics/DUPLICATE-CANDIDATES.json (or --out PATH). It changes nothing else.
It found the 103 clusters reviewed in notes/plans/P4-dedupe-decisions.md; the 25
MERGE clusters there are research/_removed.json aliases now, and re-running this on
the merged board is how a later pass sees whether any duplicate is still open.
A cluster here is a CANDIDATE: the decision on each is a reading of the records,
and the reviewed KEEP-SEPARATE list is expected to keep appearing.

Signals, each computed only between nodes of the SAME class (people only against people):
  jaccard   label-token Jaccard >= 0.6 after normalisation
  urls      2+ shared source URLs (node sources + claim sources), counting only URLs
            cited by at most URL_DF_MAX nodes, so a report cited everywhere does not pair
            every node that cites it
  ident     a distinctive identifier (GAO number, RG, U.S.C. cite, Pub. L., EO, H.R./S.,
            DIRD, NDAA section, DOPSR case, FOIA case ...) that appears in the LABEL of one
            node and the label or desc of the other, and in at most IDENT_DF_MAX nodes
  id_jaccard  the same Jaccard over the id's hyphen tokens
  jaccard_date  label Jaccard 0.34-0.6 AND the same full date (e.g. '24 June 2009') in
            label/sub/desc head; catches twins titled differently (the Reid letter pair)
  rare_url  label Jaccard 0.25-0.6 AND a non-Wayback URL cited by exactly these two nodes
  desc_jaccard  annotation only (templated descs make it useless as a trigger)
  xclass    (entities only) label Jaccard >= 0.8 across different classes, flagged so a
            reviewer can see a misfiled twin; never merged on this alone
A pair is STRONG if it has any non-URL signal, or url_overlap (shared/min) >= 0.5.
Clusters: connected components over the label-type signals (L clusters), then separately
over the strong URL-only pairs (U clusters: co-citation, reviewed in bulk). Weak URL-only
pairs are listed but not clustered.

Usage: python tools/topics/find_duplicates.py [--out PATH]
"""
import json, re, sys, os, itertools, collections, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else
       os.path.join(ROOT, "tools", "topics", "DUPLICATE-CANDIDATES.json"))
URL_DF_MAX = 8
IDENT_DF_MAX = 6
JAC = 0.6
DESC_JAC = 0.45

STOP = set("""the of and a an us u s in on for to at by with from its it
into as or re""".split())
ABBR = {
    "dod": ["defense", "department"], "doe": ["energy", "department"],
    "usaf": ["air", "force"], "af": ["air", "force"], "usn": ["navy"],
    "dept": ["department"], "natl": ["national"], "intl": ["international"],
    "cia": ["cia"], "dia": ["dia"], "govt": ["government"], "gov": ["government"],
    "rpt": ["report"], "prog": ["program"], "programme": ["program"],
    "ndaa": ["ndaa"], "fy": ["fy"], "sec": ["section"], "vol": ["volume"],
    "i": ["1"], "ii": ["2"], "iii": ["3"], "jr": [], "sr": [], "dr": [], "gen": [],
    "col": [], "lt": [], "maj": [], "capt": [], "adm": [], "sen": [], "rep": [],
}


def norm_tokens(label, drop_initials=False):
    s = unicodedata.normalize("NFKD", label or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("u.s.", " ").replace("'s", "")
    toks = re.split(r"[^a-z0-9]+", s)
    out = []
    for t in toks:
        if not t or t in STOP:
            continue
        if t in ABBR:
            out.extend(ABBR[t])
            continue
        if drop_initials and len(t) == 1 and t.isalpha():
            continue
        out.append(t)
    return set(out)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


IDENT_RES = [
    ("gao", r"GAO[/-]?[A-Z]{2,6}[- ]?\d{2}[- ]\d{1,4}"),
    ("rg", r"\bRG\s?\d{2,3}\b|Record Group\s\d{2,3}"),
    ("usc", r"\b\d{1,2}\s?U\.?S\.?C\.?\s?(?:§\s?)?\d{2,5}[a-z]?\b"),
    ("publaw", r"Pub(?:lic|\.)\s?L(?:aw|\.)\s?(?:No\.\s?)?\d{2,3}[-–]\d{1,4}"),
    ("eo", r"(?:E\.?O\.?|Executive Order)\s?\d{5}"),
    ("bill", r"\b(?:H\.\s?R\.|S\.)\s?\d{2,5}\b"),
    ("ndaa", r"NDAA\s?(?:for\s)?(?:FY|Fiscal Year)\s?\d{2,4}[^.;]{0,30}?(?:Sec(?:tion|\.)?\s?\d{3,4})"),
    ("sec", r"\bSec(?:tion|\.)\s?\d{4}\b"),
    ("dopsr", r"DOPSR\s(?:case\s)?\d{2,4}-\d{2,5}"),
    ("dird", r"DIRD[^,.;]{0,6}\b\d{1,2}\b"),
    ("docnum", r"\b[A-Z]{2,6}-\d{2,4}-\d{2,5}\b"),
    ("fileid", r"FileId/\d{5,7}"),
    ("mj12", r"MJ-?12|Majestic[- ]12"),
]


def idents(text):
    found = set()
    for kind, rx in IDENT_RES:
        for m in re.finditer(rx, text or "", flags=re.I):
            v = re.sub(r"[\s§.\-–/]+", "", m.group(0).upper())
            v = v.replace("RECORDGROUP", "RG").replace("EXECUTIVEORDER", "EO").replace("PUBLICLAW", "PUBL")
            found.add(f"{kind}:{v}")
    return found


def urls_of(n):
    out = set()
    for s in n.get("sources") or []:
        if isinstance(s, dict) and s.get("url"):
            out.add(s["url"].strip().rstrip("/").lower())
        elif isinstance(s, str) and s.startswith("http"):
            out.add(s.strip().rstrip("/").lower())
    for c in n.get("claims") or []:
        src = c.get("source")
        srcs = src if isinstance(src, list) else [src]
        for s in srcs:
            if isinstance(s, dict) and s.get("url"):
                out.add(s["url"].strip().rstrip("/").lower())
            elif isinstance(s, str) and s.startswith("http"):
                out.add(s.strip().rstrip("/").lower())
    return out


def main():
    d = json.load(open(os.path.join(ROOT, "data", "the-program.json"), encoding="utf-8"))
    nodes = {}
    for n in d["people"]:
        nodes[n["id"]] = dict(n, _kind="person", _cls="person")
    for n in d["entities"]:
        nodes[n["id"]] = dict(n, _kind="entity", _cls=n.get("cls"))
    deg = collections.Counter()
    for e in d["edges"]:
        deg[e["a"]] += 1
        deg[e["b"]] += 1

    tok = {i: norm_tokens(n.get("label"), drop_initials=(n["_kind"] == "person")) for i, n in nodes.items()}
    urls = {i: urls_of(n) for i, n in nodes.items()}
    udf = collections.Counter(u for s in urls.values() for u in s)
    lab_id = {i: idents(n.get("label")) for i, n in nodes.items()}
    all_id = {i: idents(" ".join([n.get("label") or "", n.get("desc") or "", n.get("narrative") or "" if isinstance(n.get("narrative"), str) else ""])) for i, n in nodes.items()}
    idf = collections.Counter(x for s in all_id.values() for x in s)

    idtok = {i: set(t for t in i.split("-") if t and t not in STOP) for i in nodes}
    dtok = {i: norm_tokens(n.get("desc") if isinstance(n.get("desc"), str) else (n.get("narrative") if isinstance(n.get("narrative"), str) else "")) for i, n in nodes.items()}
    DATE = re.compile(r"\b(\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|\d{4}-\d{2}-\d{2})\b")
    def _fd(n):
        head = (n.get("desc") or "")[:300] if isinstance(n.get("desc"), str) else ""
        return set(DATE.findall(" ".join(str(n.get(k) or "") for k in ("label", "sub")) + " " + head))
    fdates = {i: _fd(n) for i, n in nodes.items()}
    by_cls = collections.defaultdict(list)
    for i, n in nodes.items():
        by_cls[n["_cls"]].append(i)

    pairs = {}

    def add(a, b, sig, val):
        k = tuple(sorted((a, b)))
        pairs.setdefault(k, {})[sig] = val

    for cls, ids in by_cls.items():
        for a, b in itertools.combinations(sorted(ids), 2):
            j = jaccard(tok[a], tok[b])
            if j >= JAC:
                add(a, b, "jaccard", round(j, 3))
            shared = sorted(u for u in urls[a] & urls[b] if udf[u] <= URL_DF_MAX)
            if len(shared) >= 2:
                add(a, b, "urls", shared)
                small = min(len(urls[a]), len(urls[b])) or 1
                add(a, b, "url_overlap", round(len(shared) / small, 3))
            ij = jaccard(idtok[a], idtok[b])
            if ij >= JAC:
                add(a, b, "id_jaccard", round(ij, 3))
            dj = jaccard(dtok[a], dtok[b])
            if dj >= DESC_JAC and min(len(dtok[a]), len(dtok[b])) >= 15:
                add(a, b, "desc_jaccard", round(dj, 3))
            if 0.34 <= j < JAC and (fdates[a] & fdates[b]):
                add(a, b, "jaccard_date", {"jaccard": round(j, 3), "dates": sorted(fdates[a] & fdates[b])})
            rare = sorted(u for u in urls[a] & urls[b] if udf[u] == 2 and "web.archive.org" not in u)
            if rare and 0.25 <= j < JAC:
                add(a, b, "rare_url", {"jaccard": round(j, 3), "urls": rare})
            ida = {x for x in lab_id[a] & all_id[b] if idf[x] <= IDENT_DF_MAX}
            idb = {x for x in lab_id[b] & all_id[a] if idf[x] <= IDENT_DF_MAX}
            if ida | idb:
                add(a, b, "ident", sorted(ida | idb))
    ents = [i for i, n in nodes.items() if n["_kind"] == "entity"]
    for a, b in itertools.combinations(sorted(ents), 2):
        if nodes[a]["_cls"] != nodes[b]["_cls"]:
            j = max(jaccard(tok[a], tok[b]), jaccard(idtok[a], idtok[b]))
            if j >= 0.8:
                add(a, b, "xclass", round(j, 3))

    # connected components
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def strong(sig):
        # desc_jaccard is an annotation, never a reason on its own: the DIRD and
        # location descs are templated and pair every member of the series.
        if set(sig) - {"urls", "url_overlap", "desc_jaccard"}:
            return True
        return sig.get("url_overlap", 0) >= 0.5
    weak = {k: v for k, v in pairs.items() if not strong(v)}
    pairs = {k: v for k, v in pairs.items() if strong(v)}
    LABELISH = {"jaccard", "id_jaccard", "ident", "xclass", "jaccard_date", "rare_url"}
    lab_pairs = {k: v for k, v in pairs.items() if set(v) & LABELISH}
    url_pairs = {k: v for k, v in pairs.items() if not (set(v) & LABELISH)}

    def components(prs):
        parent.clear()
        for a, b in prs:
            parent[find(a)] = find(b)
        comps = collections.defaultdict(set)
        for a, b in prs:
            comps[find(a)].add(a)
            comps[find(b)].add(b)
        return sorted(comps.values(), key=lambda s: sorted(s)[0])

    def mk(members, prs, kind):
        return {
            "kind": kind,
            "members": [{
                "id": i, "cls": nodes[i]["_cls"], "label": nodes[i].get("label"),
                "tier": nodes[i].get("tier"),
                "date": nodes[i].get("date") or [nodes[i].get("dateStart"), nodes[i].get("dateEnd")],
                "edges": deg[i], "claims": len(nodes[i].get("claims") or []),
                "sources": len(nodes[i].get("sources") or []),
            } for i in sorted(members)],
            "pairs": [{"a": a, "b": b, "signals": prs[(a, b)]} for (a, b) in sorted(prs) if a in members],
        }

    clusters = [mk(m, lab_pairs, "label") for m in components(lab_pairs)]
    # URL-only pairs whose two ends already sit together in a label cluster add nothing.
    in_lab = {}
    for k, c in enumerate(clusters):
        for m in c["members"]:
            in_lab[m["id"]] = k
    url_pairs = {k: v for k, v in url_pairs.items() if not (k[0] in in_lab and in_lab.get(k[0]) == in_lab.get(k[1]))}
    clusters += [mk(m, url_pairs, "url-only") for m in components(url_pairs)]
    for k, c in enumerate(clusters, 1):
        c["cluster"] = ("L" if c["kind"] == "label" else "U") + f"{k:02d}"
    json.dump({"_params": {"jaccard": JAC, "url_df_max": URL_DF_MAX, "ident_df_max": IDENT_DF_MAX,
                           "nodes": len(nodes), "strong_pairs": len(pairs), "weak_url_only_pairs": len(weak), "clusters": len(clusters), "strong_rule": "any non-URL signal, or url_overlap (shared/min url count) >= 0.5"},
               "clusters": clusters,
               "weak_url_only_pairs": [{"a": a, "b": b, "labels": [nodes[a].get("label"), nodes[b].get("label")],
                                        "cls": nodes[a]["_cls"], "signals": v} for (a, b), v in sorted(weak.items())]},
              open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(pairs), "strong pairs", len(weak), "weak url-only pairs", len(clusters), "clusters")
    for c in clusters:
        print(c["cluster"], " | ".join(f"{m['id']}[{m['cls'][:4]},{m['edges']}e]" for m in c["members"]))
        for p in c["pairs"]:
            print("     ", p["a"], "~", p["b"], {k: (v if not isinstance(v, list) else len(v)) for k, v in p["signals"].items()})


if __name__ == "__main__":
    main()
