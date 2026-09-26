"""The source registry as the app ships it (redesign phase 8). Called by
build_app_data.py; kept in its own module so the builder's edits stay small.

  app/public/data/sources.json        the Library: one row per registry source
  app/public/data/sources/<id>.json  one source page: its record, its claims (with
                                     the topics that cite them), the edges citing it,
                                     the nodes listing it, and the node it is

Nothing here decides anything: research/_sources.json and research/_claim_sources.json
are the decisions, written by tools/build_source_registry.py.
"""

import json
import os

import topiclib  # tools/topics is on sys.path (build_app_data.py puts it there)

SOURCES = os.path.join("research", "_sources.json")
CLAIM_SOURCES = os.path.join("research", "_claim_sources.json")


class Registry(object):
    def __init__(self, root):
        with open(os.path.join(root, SOURCES), encoding="utf-8") as f:
            self.sources = json.load(f)["sources"]
        with open(os.path.join(root, CLAIM_SOURCES), encoding="utf-8") as f:
            cs = json.load(f)
        self.by = {s["id"]: s for s in self.sources}
        self.claims = cs.get("claims") or {}
        self.unresolved = cs.get("unresolved") or {}
        self.edges = cs.get("edges") or {}
        self.nodes = cs.get("nodes") or {}

    def claim_refs(self, cid):
        """A claim's sources as every surface prints them: id, title and locator (the
        source page carries the rest). [] when unresolved."""
        out = []
        for r in self.claims.get(cid) or []:
            s = self.by.get(r["source"])
            if not s:
                continue
            out.append({"id": s["id"], "title": s["title"], "locator": r.get("locator")})
        return out

    def why_unresolved(self, cid):
        u = self.unresolved.get(cid)
        return u.get("why") if u else None


def _topics_citing(s):
    """{claim id: [(topic id, title)]} from every topic's cites."""
    out = {}
    for t in s.topics:
        for cid in topiclib.cited_ids(t):
            if cid.startswith("c-"):
                out.setdefault(cid, []).append((t["id"], t.get("title") or t["id"]))
    return out


def pages(s, reg, era_of):
    """{source id: page record}."""
    claims_of = {}
    owner = {}
    for n in s.nodes:
        for c in n.get("claims") or []:
            owner[c["id"]] = (n, c)
    for cid, rows in reg.claims.items():
        for r in rows:
            claims_of.setdefault(r["source"], []).append((cid, r.get("locator")))
    edges_of = {}
    eby = {e["id"]: e for e in s.board["edges"]}
    for eid, sids in reg.edges.items():
        for sid in sids:
            edges_of.setdefault(sid, []).append(eid)
    listed = {}
    for nid, sids in reg.nodes.items():
        for sid in sids:
            listed.setdefault(sid, []).append(nid)
    tcite = _topics_citing(s)

    def ref(i):
        n = s.byid.get(i) or {}
        return {"id": i, "label": n.get("label") or i, "cls": n.get("cls")}

    out = {}
    for src in reg.sources:
        sid = src["id"]
        rows = []
        for cid, loc in claims_of.get(sid, []):
            if cid not in owner:
                continue
            n, c = owner[cid]
            rows.append({"id": cid, "node": n["id"], "nodeLabel": n.get("label"),
                         "cls": n.get("cls"), "tier": c.get("tier"), "text": c.get("text"),
                         "sourceText": c.get("source"), "locator": loc})
        rows.sort(key=lambda r: ((r["nodeLabel"] or "").lower(), r["tier"] or 0, r["id"]))
        topics = {}
        for r in rows:
            for tid, title in tcite.get(r["id"], []):
                topics.setdefault(tid, {"id": tid, "title": title, "claims": []})["claims"].append(r["id"])
        edges = []
        for eid in sorted(set(edges_of.get(sid, []))):
            e = eby.get(eid)
            if not e:
                continue
            edges.append({"id": eid, "a": ref(e["a"]), "b": ref(e["b"]), "type": e.get("type"),
                          "label": e.get("label") or "", "claimTier": e.get("claimTier"),
                          "note": e.get("note") or ""})
        edges.sort(key=lambda r: (r["a"]["label"].lower(), r["b"]["label"].lower(), r["id"]))
        rec = dict(src)
        rec["era"] = era_of(src.get("date"))
        rec["node"] = ref(src["node"]) if src.get("node") else None
        rec["claims"] = rows
        rec["topics"] = sorted(topics.values(), key=lambda t: (-len(t["claims"]), t["title"].lower()))
        rec["edges"] = edges
        rec["listedOn"] = sorted((ref(i) for i in set(listed.get(sid, []))),
                                 key=lambda r: r["label"].lower())
        out[sid] = rec
    return out


def library(recs, meta, reg):
    """app/public/data/sources.json: the Library's rows, and the facet vocabularies."""
    rows = []
    for sid in sorted(recs):
        r = recs[sid]
        rows.append({"id": sid, "type": r["type"], "title": r["title"], "issuer": r.get("issuer"),
                     "date": r.get("date"), "era": r["era"],
                     "interestedParty": bool(r.get("interestedParty")),
                     "identifiers": r.get("identifiers") or [],
                     "claims": len(r["claims"]), "edges": len(r["edges"]),
                     "listedOn": len(r["listedOn"]),
                     "node": r["node"]["id"] if r.get("node") else None,
                     "urls": len(r.get("urls") or []), "archived": len(r.get("archived") or [])})
    return {"generated": meta["generated"], "source": meta["source"],
            "count": len(rows), "sources": rows,
            "claims": {"total": len(reg.claims) + len(reg.unresolved), "resolved": len(reg.claims)}}
