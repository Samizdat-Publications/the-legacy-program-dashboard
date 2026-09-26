#!/usr/bin/env python3
"""The entity dossiers, loaded and capped: research/dossiers/*.json as the app ships them.

Moved here verbatim from tools/build_l0.py when the L0 program map retired (redesign
phase 11, 26 September 2026). The dossiers outlived the map: build_app_data.py puts
each one on its node's file (`nodes/<id>.json`, field `dossier`), and
build_foia_links.py reads their open questions. Nothing here depends on the map.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- entity dossiers
# These are a PARALLEL dataset, deliberately not merged into the board's nodes.
# Merging 359 sourced claims onto 25 nodes would move every claim count, every tier
# mix and the whole GOLDEN manifest, and it would mix two different kinds of object:
# a node claim is a fact about the entity, an entity dossier is the ARGUMENT for why
# that entity is on this map. They are verified separately for the same reason.
#
# They live in research/dossiers/ rather than research/ because merge.py globs
# research/*.json and expects node documents.
def dossier_ids():
    """The ids research/dossiers/ carries a dossier for, without loading them."""
    import glob
    return {e["id"] for f in glob.glob(os.path.join(ROOT, "research", "dossiers", "*.json"))
            for e in json.load(open(f, encoding="utf-8"))}


def load_dossiers():
    import glob
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "dossiers", "*.json"))):
        for e in json.load(open(f, encoding="utf-8")):
            d = e.get("entityDossier") or {}
            prev = out.get(e["id"])
            # A duplicate is not an error: two research passes can reach the same
            # entity. Keep the better-sourced one rather than whichever sorted last.
            if prev and len(prev.get("claims", [])) >= len(d.get("claims", [])):
                continue
            out[e["id"]] = d
    cap_dossier_claims(out)
    return out


# The sourcing rules reach dossier claims (redesign phase 3, decision 5). A dossier
# claim graded Tier 1 makes the same promise a node claim does, and the node rule in
# merge.py (secondary source, no attributed source, no primary URL anywhere, AARO/DoD
# asserting an outside fact) had never been applied to them. Same function, not a
# copy of it; every demotion is logged to tools/REGRADE_REPORT.json beside the node
# tier moves, under `dossierDemotions`. Presentation never moves evidence: this is a
# sourcing cap, applied to what the claim cites, exactly as it is on the node.
REGRADE_REPORT = os.path.join(ROOT, "tools", "REGRADE_REPORT.json")


def cap_dossier_claims(dossiers):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from merge import tier1_cap_reason, URL_IN_SOURCE  # noqa: E402
    log = []
    for nid in sorted(dossiers):
        claims = dossiers[nid].get("claims") or []
        urls = " ".join(u for c in claims for u in URL_IN_SOURCE.findall(c.get("source") or ""))
        for c in claims:
            why = tier1_cap_reason(c, urls)
            if not why:
                continue
            c["tier"] = 2
            if "needs primary" not in (c.get("source") or "").lower():
                c["source"] = (f"{c.get('source') or ''} - DEMOTED from Tier 1 ({why}); "
                               f"needs primary replacement")
            log.append({"id": nid, "why": why, "claim": (c.get("text") or "")[:110]})
    if os.path.exists(REGRADE_REPORT):
        rep = json.load(open(REGRADE_REPORT, encoding="utf-8"))
        rep["dossierDemotions"] = log
        with open(REGRADE_REPORT, "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=1, ensure_ascii=False)
    return log
