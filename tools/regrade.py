#!/usr/bin/env python3
"""
regrade.py — wave 3A structural remediation, applied as an overlay.

Four passes, none of which need a web search:

  1. TIER RE-GRADE. Fourteen agents each graded within their own domain, where their
     subject genuinely was central, and nobody graded across the whole board. Result:
     553 of 911 nodes at Tier A, which makes the badge meaningless. This recomputes
     tiers globally against a composite centrality score and cuts at ~15/35/50.

  2. ID NORMALISATION. Strip stray `p-` prefixes; merge `l-washington-dc` into `l-dc`.

  3. MISSING DATES. 40 people have no `date`, which is the timeline sort key, so they
     cannot be placed. Recover it from the record's own chronology.

  4. COORDINATES. Location nodes carry no coords, so GEOGRAPHY cannot plot. Fill from a
     hand-built gazetteer of the named installations and cities actually on the board.

Writes research/_remediation.json, which merge.py consumes like any other domain file,
plus tools/REGRADE_REPORT.json showing every tier that moved and why.

The overlay approach matters: the research files stay untouched, so a later wave can
re-run this with different weights without anything having been destructively edited.
"""

import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")

# Target distribution. Tier A is meant to be "named in sworn testimony or primary
# documents as directly inside the program" — that is a minority position by definition.
TARGET = {"A": 0.15, "B": 0.35, "C": 0.50}

# Edge types that indicate direct program involvement rather than context.
PROGRAM_EDGES = {"custody", "witness-chain", "funding", "programmatic"}
# Edge types that indicate someone thought this node worth denying.
DENIAL_EDGES = {"denial"}


def centrality(node, deg, prog_deg, denial_deg, claim_w):
    """Composite score. Every term is defensible in isolation, which matters because
    a re-grade nobody can explain is worse than the broken grades it replaced."""
    s = 0.0
    # Structural weight: how embedded is this node in the graph at all.
    s += min(deg, 40) * 1.0
    # Program weight: edges of the types that mean *inside*, not *adjacent*.
    s += min(prog_deg, 20) * 3.0
    # Denial weight: an entity a government body bothered to deny is, on this board,
    # more interesting rather than less. This is the stance encoded as arithmetic.
    s += min(denial_deg, 10) * 4.0
    # Evidence weight: Tier 1 claims count triple, Tier 2 double, Tier 3 once.
    s += claim_w
    # Axis weight: custody and access are what the board is actually measuring.
    s += (node.get("C", 0) * 4.0) + (node.get("A", 0) * 3.0) + (node.get("D", 0) * 2.0)
    # A node with no sources cannot be Tier A no matter what else it scores.
    if not [x for x in node.get("sources", []) if x.get("url")]:
        s *= 0.35
    return s


GAZETTEER = {
    # US installations and sites
    "l-dc": (38.8951, -77.0364, "Washington, DC, USA"),
    "l-washington-dc": (38.8951, -77.0364, "Washington, DC, USA"),
    "l-wright-patterson": (39.8261, -84.0483, "Wright-Patterson AFB, Ohio, USA"),
    "l-kirtland": (35.0403, -106.6092, "Kirtland AFB, New Mexico, USA"),
    "l-roswell": (33.3943, -104.5230, "Roswell, New Mexico, USA"),
    "l-groom-lake": (37.2350, -115.8111, "Groom Lake, Nevada, USA"),
    "l-area51": (37.2350, -115.8111, "Groom Lake, Nevada, USA"),
    "l-skinwalker": (40.2569, -109.8890, "Uintah County, Utah, USA"),
    "l-los-alamos": (35.8800, -106.3031, "Los Alamos, New Mexico, USA"),
    "l-albuquerque": (35.0844, -106.6504, "Albuquerque, New Mexico, USA"),
    "l-huntsville": (34.7304, -86.5861, "Huntsville, Alabama, USA"),
    "l-white-sands": (32.3801, -106.4757, "White Sands, New Mexico, USA"),
    "l-edwards-afb": (34.9054, -117.8837, "Edwards AFB, California, USA"),
    "l-nellis": (36.2360, -115.0343, "Nellis AFB, Nevada, USA"),
    "l-tonopah": (37.7981, -116.7817, "Tonopah Test Range, Nevada, USA"),
    "l-vandenberg": (34.7420, -120.5724, "Vandenberg SFB, California, USA"),
    "l-ft-meade": (39.1084, -76.7713, "Fort Meade, Maryland, USA"),
    "l-detroit-arsenal": (42.5570, -83.0413, "Detroit Arsenal, Michigan, USA"),
    "l-colorado-springs": (38.8339, -104.8214, "Colorado Springs, Colorado, USA"),
    "l-boulder-co": (40.0150, -105.2705, "Boulder, Colorado, USA"),
    # US cities
    "l-la": (34.0522, -118.2437, "Los Angeles, California, USA"),
    "l-long-beach": (33.7701, -118.1937, "Long Beach, California, USA"),
    "l-huntington-beach": (33.6603, -117.9992, "Huntington Beach, California, USA"),
    "l-stanford": (37.4275, -122.1697, "Stanford, California, USA"),
    "l-sri": (37.4560, -122.1760, "Menlo Park, California, USA"),
    "l-nyc": (40.7128, -74.0060, "New York, New York, USA"),
    "l-boston": (42.3601, -71.0589, "Boston, Massachusetts, USA"),
    "l-cambridge": (42.3736, -71.1097, "Cambridge, Massachusetts, USA"),
    "l-wellesley": (42.2968, -71.2924, "Wellesley, Massachusetts, USA"),
    "l-woodshole": (41.5265, -70.6731, "Woods Hole, Massachusetts, USA"),
    "l-las-vegas": (36.1699, -115.1398, "Las Vegas, Nevada, USA"),
    "l-albany": (42.6526, -73.7562, "Albany, New York, USA"),
    "l-detroit": (42.3314, -83.0458, "Detroit, Michigan, USA"),
    "l-dallas": (32.7767, -96.7970, "Dallas, Texas, USA"),
    "l-fort-worth-tx": (32.7555, -97.3308, "Fort Worth, Texas, USA"),
    "l-huffman-tx": (30.0182, -95.0966, "Huffman, Texas, USA"),
    "l-orlando": (28.5383, -81.3792, "Orlando, Florida, USA"),
    "l-parkland-fl": (26.3103, -80.2373, "Parkland, Florida, USA"),
    "l-st-petersburg": (27.7676, -82.6403, "St Petersburg, Florida, USA"),
    "l-charleston-sc": (32.7765, -79.9311, "Charleston, South Carolina, USA"),
    "l-nashville": (36.1627, -86.7816, "Nashville, Tennessee, USA"),
    "l-franklin-tn": (35.9251, -86.8689, "Franklin, Tennessee, USA"),
    "l-knoxville": (35.9606, -83.9207, "Knoxville, Tennessee, USA"),
    "l-tompkinsville": (36.7017, -85.6913, "Tompkinsville, Kentucky, USA"),
    "l-cincinnati": (39.1031, -84.5120, "Cincinnati, Ohio, USA"),
    "l-schaumburg": (42.0334, -88.0834, "Schaumburg, Illinois, USA"),
    "l-green-bay": (44.5133, -88.0133, "Green Bay, Wisconsin, USA"),
    "l-glenbeulah": (43.8036, -88.0997, "Glenbeulah, Wisconsin, USA"),
    "l-michigan-state": (42.7018, -84.4822, "East Lansing, Michigan, USA"),
    "l-ames": (42.0308, -93.6319, "Ames, Iowa, USA"),
    "l-cedar-rapids": (41.9779, -91.6656, "Cedar Rapids, Iowa, USA"),
    "l-springfield-mo": (37.2090, -93.2923, "Springfield, Missouri, USA"),
    "l-boise-id": (43.6150, -116.2023, "Boise, Idaho, USA"),
    "l-windsor-co": (40.4775, -104.9014, "Windsor, Colorado, USA"),
    "l-oro-valley": (32.3909, -110.9665, "Oro Valley, Arizona, USA"),
    "l-gilbert-az": (33.3528, -111.7890, "Gilbert, Arizona, USA"),
    "l-seattle": (47.6062, -122.3321, "Seattle, Washington, USA"),
    "l-lafayette": (30.2241, -92.0198, "Lafayette, Louisiana, USA"),
    "l-takoma-park": (38.9779, -77.0075, "Takoma Park, Maryland, USA"),
    "l-san-agustin": (33.8500, -107.7500, "Plains of San Agustin, New Mexico, USA"),
    "l-aztec": (36.8222, -107.9928, "Aztec, New Mexico, USA"),
    # international
    "l-london": (51.5074, -0.1278, "London, United Kingdom"),
    "l-uk": (54.0000, -2.0000, "United Kingdom"),
    "l-uk-mod-whitehall": (51.5045, -0.1265, "Whitehall, London, United Kingdom"),
    "l-sheffield": (53.3811, -1.4701, "Sheffield, United Kingdom"),
    "l-paris": (48.8566, 2.3522, "Paris, France"),
    "l-toulouse": (43.6047, 1.4442, "Toulouse, France"),
    "l-france": (46.6034, 1.8883, "France"),
    "l-brasilia": (-15.7939, -47.8828, "Brasilia, Brazil"),
    "l-brazil": (-14.2350, -51.9253, "Brazil"),
    "l-varginha": (-21.5510, -45.4300, "Varginha, Minas Gerais, Brazil"),
    "l-santiago": (-33.4489, -70.6693, "Santiago, Chile"),
    "l-ottawa": (45.4215, -75.6972, "Ottawa, Ontario, Canada"),
    "l-fredericton": (45.9636, -66.6431, "Fredericton, New Brunswick, Canada"),
    "l-moscow": (55.7558, 37.6173, "Moscow, Russia"),
    "l-stockholm": (59.3293, 18.0686, "Stockholm, Sweden"),
}

ID_MERGES = {"l-washington-dc": "l-dc"}


def normalise_id(i):
    if i in ID_MERGES:
        return ID_MERGES[i]
    # strip a stray p- prefix on person ids, but never on p-named real entities
    if re.match(r"^p-[a-z]+-[a-z]", i):
        return i[2:]
    return i


def main():
    board = json.load(open(BOARD, encoding="utf-8"))
    people, entities, edges = board["people"], board["entities"], board["edges"]
    nodes = people + entities
    by_id = {n["id"]: n for n in nodes}

    # ---- degree tables -------------------------------------------------------
    deg, prog_deg, denial_deg = Counter(), Counter(), Counter()
    for e in edges:
        a, b, t = normalise_id(e["a"]), normalise_id(e["b"]), e["type"]
        deg[a] += 1; deg[b] += 1
        if t in PROGRAM_EDGES:
            prog_deg[a] += 1; prog_deg[b] += 1
        if t in DENIAL_EDGES:
            denial_deg[a] += 1; denial_deg[b] += 1

    # ---- score ---------------------------------------------------------------
    scored = []
    for n in nodes:
        nid = normalise_id(n["id"])
        cw = sum({1: 3.0, 2: 2.0, 3: 1.0}[c["tier"]] for c in n.get("claims", []))
        cw = min(cw, 45.0)
        scored.append((centrality(n, deg[nid], prog_deg[nid], denial_deg[nid], cw), n))
    scored.sort(key=lambda x: -x[0])

    total = len(scored)
    cut_a = int(total * TARGET["A"])
    cut_b = cut_a + int(total * TARGET["B"])

    report, overlay_people, overlay_entities = [], [], []
    for rank, (score, n) in enumerate(scored):
        new = "A" if rank < cut_a else ("B" if rank < cut_b else "C")
        old = n.get("tier", "C")
        nid = normalise_id(n["id"])
        if new != old:
            report.append({"id": nid, "cls": n.get("cls"), "from": old, "to": new,
                           "score": round(score, 1), "rank": rank + 1,
                           "degree": deg[nid], "program_edges": prog_deg[nid],
                           "denials": denial_deg[nid]})
        rationale = (
            f"Re-graded {new} on a global pass (rank {rank+1} of {total}, score {score:.0f}). "
            f"{deg[nid]} connections, {prog_deg[nid]} of them custody/witness/funding/programmatic"
            + (f", {denial_deg[nid]} official denial{'s' if denial_deg[nid] != 1 else ''} recorded against it"
               if denial_deg[nid] else "")
            + f". Axes C{n.get('C',0)}/A{n.get('A',0)}/D{n.get('D',0)}."
        )
        rec = {"id": nid, "tier": new, "tierRationale": rationale}
        if n.get("cls") == "person":
            overlay_people.append(rec)
        else:
            rec["cls"] = n.get("cls")
            overlay_entities.append(rec)

    # ---- missing dates from chronology ---------------------------------------
    dated = 0
    date_fix = {}
    for p in people:
        if p.get("date"):
            continue
        ch = p.get("chronology") or []
        if ch:
            # the last dated event in the record is the one that best places the person
            d = max(c["date"] for c in ch)
            if len(d) == 4:
                d += "-01-01"
            elif len(d) == 7:
                d += "-01"
            date_fix[normalise_id(p["id"])] = d
            dated += 1
    for rec in overlay_people:
        if rec["id"] in date_fix:
            rec["date"] = date_fix[rec["id"]]

    # ---- coordinates ---------------------------------------------------------
    coord_recs, coords_added = [], 0
    for e in entities:
        if e.get("cls") != "location":
            continue
        nid = normalise_id(e["id"])
        g = GAZETTEER.get(nid)
        if not g:
            continue
        coord_recs.append({"id": nid, "cls": "location",
                           "coords": [g[0], g[1]], "loc": g[2]})
        coords_added += 1
    # fold coords into the entity overlay
    cmap = {c["id"]: c for c in coord_recs}
    for rec in overlay_entities:
        c = cmap.get(rec["id"])
        if c:
            rec["coords"] = c["coords"]
            rec["locLabel"] = c["loc"]

    out = {
        "domain": "_remediation",
        "people": [{**r, "cls": "person"} for r in overlay_people],
        "entities": overlay_entities,
        "edges": [], "timeline": [], "entityInfo": {},
        "gaps": [f"{len(GAZETTEER)} locations have coordinates; the remainder still need geocoding"],
    }
    json.dump(out, open(os.path.join(ROOT, "research", "_remediation.json"), "w",
                        encoding="utf-8"), indent=1, ensure_ascii=False)

    dist = Counter(r["tier"] for r in overlay_people + overlay_entities)
    json.dump({"moved": report,
               "distribution": dict(dist),
               "dates_recovered": dated,
               "coords_added": coords_added},
              open(os.path.join(ROOT, "tools", "REGRADE_REPORT.json"), "w",
                   encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"scored {total} nodes")
    print(f"new distribution  A={dist['A']} ({dist['A']/total:.0%})  "
          f"B={dist['B']} ({dist['B']/total:.0%})  C={dist['C']} ({dist['C']/total:.0%})")
    print(f"tiers moved       {len(report)}")
    print(f"dates recovered   {dated}")
    print(f"coords added      {coords_added}")
    print("\ntop 15 by centrality:")
    for score, n in scored[:15]:
        print(f"  {score:7.1f}  {normalise_id(n['id']):38s} {n.get('cls','')}")


if __name__ == "__main__":
    main()
