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

  4. COORDINATES. Location nodes carry no coords, so GEOGRAPHY cannot plot. Fill from
     research/_places.json (the hand-built table that used to be typed into this file).

Writes research/_remediation.json, which merge.py consumes like any other domain file,
plus tools/REGRADE_REPORT.json showing every tier that moved and why.

The overlay approach matters: the research files stay untouched, so a later wave can
re-run this with different weights without anything having been destructively edited.
"""

import json, os, re, sys, subprocess
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")
PRISTINE = os.path.join(ROOT, "tools", "_pristine-board.json")
OVERLAY = os.path.join(ROOT, "research", "_remediation.json")


def pristine_board():
    """Score the research corpus, NOT the board this script previously remediated.

    This script writes research/_remediation.json, which merge.py folds into
    data/the-program.json as an authoritative overlay. If we then read that merged
    board back, every fix we already made looks like it was always there:
    `if p.get("date"): continue` skips the 40 dates recovered last run, we emit an
    overlay carrying only the 5 we can still derive, and the next merge silently
    drops the other 35. The documented rebuild sequence therefore destroyed data
    on every run — 35 dates and a tier-rank shuffle, confirmed by diffing a
    rebuild against the shipped board on 2026-08-12.

    Re-merging without the overlay makes this script a pure function of research/
    and idempotent by construction, which is what the module docstring always
    claimed it was.
    """
    env = dict(os.environ, MERGE_SKIP="_remediation", MERGE_JSON_OUT=PRISTINE)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "merge.py")],
                       env=env, stdout=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.exists(PRISTINE):
        sys.exit("regrade: pristine merge failed — refusing to score a remediated board")
    return json.load(open(PRISTINE, encoding="utf-8"))


def guard_no_data_loss(new, board):
    """Refuse to write an overlay that would drop a field from the FINAL board.

    The failure this exists to catch was silent: the build printed success, every
    patch applied, and 35 dates went to null. Loud and early beats correct-looking.

    Compare effective values (pristine value, else overlay value) rather than raw
    overlay entries. An overlay legitimately shrinks when the underlying research
    starts carrying a field itself — that is the fix working, not data loss, and a
    guard that cannot tell the two apart would just get switched off.
    """
    if not os.path.exists(OVERLAY):
        return
    try:
        old = json.load(open(OVERLAY, encoding="utf-8"))
    except Exception:
        return
    base = {n["id"]: n for n in board["people"] + board["entities"]}

    def effective(overlay, key, field):
        out = {}
        for rid, rec in base.items():
            if rec.get(field):
                out[rid] = rec[field]
        for r in overlay.get(key, []):
            if r.get(field):
                out[r["id"]] = r[field]
        return out

    lost = []
    for key in ("people", "entities"):
        for field in ("date", "coords", "tier"):
            eff_old = effective(old, key, field)
            eff_new = effective(new, key, field)
            for rid, val in eff_old.items():
                # a coordinate research/_places.json deliberately withholds, with
                # its reason, is a decision rather than a loss
                if field == "coords" and rid in WITHHELD:
                    continue
                if rid in base and not eff_new.get(rid):
                    lost.append(f"{key}/{rid}.{field} = {val!r}")
    if lost:
        print(f"\n!! REGRADE ABORTED — the new overlay drops {len(lost)} field(s) the "
              f"previous one supplied:", file=sys.stderr)
        for l in lost[:20]:
            print("     " + l, file=sys.stderr)
        if len(lost) > 20:
            print(f"     ... and {len(lost) - 20} more", file=sys.stderr)
        print("   research/_remediation.json was NOT written. This is the "
              "non-idempotency guard;\n   see pristine_board() for what it is "
              "protecting against.\n", file=sys.stderr)
        sys.exit(1)

# Target distribution. Tier A is meant to be "named in sworn testimony or primary
# documents as directly inside the program" — that is a minority position by definition.
TARGET = {"A": 0.15, "B": 0.35, "C": 0.50}

# Edge types that indicate direct program involvement rather than context.
#
# `witness-chain` was in this set until 2026-09-18 and is deliberately NOT in it now.
# The other three are documented structural relationships: who held the thing, who paid
# for it, what programme it belonged to. A witness-chain edge is not a structural fact
# about the node, it is a record that somebody SAID something about it. Weighting it x3
# for being "inside" made an accumulation of testimony read as an accumulation of
# custody. That was tolerable while witness-chain edges mostly joined documented
# witnesses to documented programmes; the hub rule adopted on 2026-09-18 (every claimant
# gets a witness-chain edge into the thing claimed about) makes it the dominant edge type
# of every claimant cluster, so the x3 weight would systematically promote claimants.
#
# The measurement that decided it, on the 1,057-node board: witness-chain edges are 61.8%
# Tier 2 or 3, against 30.0% for custody/funding/programmatic. It is by a wide margin the
# most claim-like member of a set whose whole justification is that it is structural.
# Witness-chain edges still count at x1.0 in plain degree, which is the intended reading:
# degree is allowed to mean "a lot is claimed here", never "this is true".
# Reasoning and the rejected alternative: notes/CENTRALITY-2026-09-18.md.
PROGRAM_EDGES = {"custody", "funding", "programmatic"}
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


# The coordinates live in research/_places.json since redesign phase 11: the 76
# entries that were typed here were moved there verbatim, with a record of where
# they came from (no cited source; a cited gazetteer is a phase R item). This is
# the same table read back, (lat, lon, place as written) keyed by node id.
PLACES = os.path.join(ROOT, "research", "_places.json")
with open(PLACES, encoding="utf-8") as _fh:
    _PL = json.load(_fh)
GAZETTEER = {k: (v["lat"], v["lon"], v["loc"]) for k, v in (_PL.get("places") or {}).items()}
# ids whose table coordinates were set aside, each with its reason in the file
WITHHELD = set((_PL.get("_withheld") or {}).keys())

# Single source of truth. These two scripts each having their own copy of the id
# rules is exactly how the five duplicate people got onto the board: regrade
# normalised, merge did not, and merge created the normalised id as a new node.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge import canonical_id as normalise_id, ID_MERGES  # noqa: E402


def main():
    board = pristine_board()
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
        # The 0.35 multiplier in centrality() DISCOUNTS an unsourced node; it does
        # not exclude it, and a high-degree node can still clear the top-15% cut.
        # The comment there says "cannot be Tier A"; this is where that is true.
        # verify.py asserts it on the shipped board.
        if new == "A" and not [x for x in n.get("sources", []) if x.get("url")]:
            new = "B"
        old = n.get("tier", "C")
        nid = normalise_id(n["id"])
        if new != old:
            report.append({"id": nid, "cls": n.get("cls"), "from": old, "to": new,
                           "score": round(score, 1), "rank": rank + 1,
                           "degree": deg[nid], "program_edges": prog_deg[nid],
                           "denials": denial_deg[nid]})
        rationale = (
            f"Re-graded {new} on a global pass (rank {rank+1} of {total}, score {score:.0f}). "
            f"{deg[nid]} connections, {prog_deg[nid]} of them custody/funding/programmatic"
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
    guard_no_data_loss(out, board)
    json.dump(out, open(OVERLAY, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

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
