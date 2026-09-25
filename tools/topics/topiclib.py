"""topiclib.py: reading the topic records and resolving what they cite.

Shared by tools/build_app_data.py (which ships app/public/data/topics.json and
topics/<id>.json) and tools/topics/topic_packet.py (which prints a drafter's packet).
verify.py and audit_independent.py do NOT import this: they restate the rules by
their own routes, so a mistake here cannot be agreed with.

A topic cites claim ids (c-...) and edge ids (e-...), both minted by merge.py from
content. A claim phase 3 could not place (tools/UNPLACED-CLAIMS.json, listed on a
stub as `unplacedClaims`) is cited by the id it would carry on the node it collapsed
into: merge.claim_id(collapsedInto, text).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOPICS_DIR = os.path.join(ROOT, "research", "topics")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from merge import claim_id  # noqa: E402

TEXT_KEYS = ("lead", "summary", "record", "claimed", "contested")
STATUSES = ("draft", "drafted", "verified")


def rd(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def stub_files():
    """Sorted file names of the authored topic records (not the _ files)."""
    return sorted(f for f in os.listdir(TOPICS_DIR)
                  if f.endswith(".json") and not f.startswith("_"))


def load_topics():
    """[topic], sorted by id."""
    return sorted((rd(os.path.join(TOPICS_DIR, f)) for f in stub_files()),
                  key=lambda t: t["id"])


def load_sections():
    return rd(os.path.join(TOPICS_DIR, "_sections.json"))


def items(t):
    """[(where, item)] for every citable item: the lead and each list entry."""
    out = []
    if t.get("lead") is not None:
        out.append(("lead", t["lead"]))
    for k in TEXT_KEYS[1:]:
        for i, it in enumerate(t.get(k) or []):
            out.append(("%s[%d]" % (k, i), it))
    return out


def cited_ids(t):
    """Distinct cited ids, in first-cited order."""
    seen = []
    for _w, it in items(t):
        for c in (it.get("cite") or []) if isinstance(it, dict) else []:
            if c not in seen:
                seen.append(c)
    return seen


def unplaced(t):
    """{claim id: unplaced claim record} for the stub's unplacedClaims."""
    return {claim_id(c.get("collapsedInto"), c.get("claim") or ""): c
            for c in t.get("unplacedClaims") or []}


class Board(object):
    """The built board, indexed for resolution: nodes, claims and edges by id."""

    def __init__(self, board):
        self.nodes = {n["id"]: n for n in board["people"] + board["entities"]}
        self.claims = {}
        for n in board["people"] + board["entities"]:
            for c in n.get("claims") or []:
                if c.get("id"):
                    self.claims[c["id"]] = (n, c)
        self.edges = {e["id"]: e for e in board["edges"] if e.get("id")}


def resolve(bd, t, cid, source_row):
    """One cited id as the topic file ships it, or None when it resolves to nothing.
    source_row(text) -> the claim source object (the shape claims.json ships)."""
    up = unplaced(t)
    if cid in up:
        c = up[cid]
        n = bd.nodes.get(c.get("collapsedInto")) or {}
        return {"id": cid, "kind": "claim", "text": c.get("claim"), "tier": c.get("tier"),
                "source": source_row(c.get("source")), "node": c.get("collapsedInto"),
                "nodeLabel": n.get("label"), "unplaced": True}
    if cid in bd.claims:
        n, c = bd.claims[cid]
        return {"id": cid, "kind": "claim", "text": c.get("text"), "tier": c.get("tier"),
                "source": source_row(c.get("source")), "node": n["id"],
                "nodeLabel": n.get("label")}
    if cid in bd.edges:
        e = bd.edges[cid]
        return {"id": cid, "kind": "edge", "text": e.get("note") or "",
                "label": e.get("label") or "", "tier": e.get("claimTier"),
                "type": e.get("type"), "sources": e.get("sources") or [],
                "endpoints": [{"id": x, "label": (bd.nodes.get(x) or {}).get("label")}
                              for x in (e["a"], e["b"])]}
    return None
