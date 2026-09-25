#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 1a of the new shell: the runtime data contract under app/public/data/.

Writes every file in notes/APP-SPEC-2026-09-02.md section 2 from the same sources
the old pipeline uses, and copies the eleven patent drawing originals and their
thumbs to app/public/patents/.

    python tools/build_app_data.py              build
    python tools/build_app_data.py --check      re-derive every count in index.json
                                                from the sources and fail on drift
    python tools/build_app_data.py --self-test  show --check rejecting a poisoned
                                                board (one node removed)

WHAT IS DERIVED HERE AND WHAT IS COPIED
---------------------------------------
Nothing in this file invents a fact.  `band` and `era` are the L0 model's own
values, read out of data/l0-layout-model.json (`current`), which is where
tools/build_l0_layout.mjs bakes them -- rarest-role band, ERAS table for the era.
For a node the L0 model does not carry (the 902 below the floor) the band is
null, and the era is derived from the node's start year against that same era
table, which is the only rule this file applies and it is the model's table.

DENIAL DIRECTION.  notes/DENIAL-ADJUDICATION-2026-08-26.md read all 174 denial
edges one at a time and found the shipped "a issued it, b is the subject"
convention wrong on 34 of 124 directed cases -- 27 per cent.  merge.py stamps the
verdict onto the board as `denier` / `denialKind`.  So the denier here is the
edge's own `denier` where it has one, and only falls back to `a` where it does
not.  Writing `a` unconditionally would re-publish a claim the repo has already
shown to be wrong on a quarter of its cases.

DETERMINISM.  Every value written here is a function of the inputs' CONTENT and
of nothing else, so a rebuild from unchanged inputs is byte-identical on any
machine.  `generated` is the newest `generated` string among the inputs, not
today's date.  `source` hashes the input bytes with newlines normalised to LF, so
a Windows checkout with core.autocrlf=true and a Linux one agree.  Every object is
written with sorted keys.  There is no `sourceCommit`: it named whatever commit
.git/HEAD pointed at, which is a property of the checkout rather than of the data,
and it made the committed index.json unreproducible by construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "public", "data")
PAT_OUT = os.path.join(ROOT, "app", "public", "patents")

BOARD = "data/the-program.json"
L0_MODEL = "data/l0-model.json"
L0_LAYOUT = "data/l0-layout-model.json"
L0_HIGHLIGHTS = "data/l0-highlights.json"
L0_SHORTS = "data/l0-shorts.json"
FOIA_LINKS = "data/foia-links.json"
PATENTS_VIEW = "research/patents-view.json"
OBSERVABLES_VIEW = "research/observables-view.json"
THREADS = "research/threads.json"
DRAWINGS = "research/patents/drawings"
SUGGESTIONS = "data/analyst-suggestions.json"

INPUTS = [BOARD, L0_MODEL, L0_LAYOUT, L0_HIGHLIGHTS, L0_SHORTS, FOIA_LINKS,
          PATENTS_VIEW, OBSERVABLES_VIEW, SUGGESTIONS]

# The analyst's chips, one list per route kind.  app/src/analyst/chips.ts maps
# route kinds onto these nine keys and nothing else, so a key added here that
# the page does not know is a key nothing renders.
ANALYST_KEYS = ["home", "node", "map", "hood", "thread",
                "timeline", "patents", "evidence", "report"]
ANALYST_MIN = 3

ANALYST_WORKER = "https://the-program-analyst.stewartgregerson.workers.dev"

# The era table, verbatim from tools/build_l0_layout.mjs.  It is repeated here
# rather than re-invented: the ids, bounds and labels must be the model's, and
# the build asserts below that they still match data/l0-layout-model.json.
ERAS = [
    {"id": "0", "label": "THROUGH 1969", "sub": "Estimate through Blue Book",
     "start": None, "end": 1969},
    {"id": "1", "label": "1970-1999", "sub": "Post-Blue Book",
     "start": 1970, "end": 1999},
    {"id": "2", "label": "2000-2016", "sub": "AAWSAP / AATIP",
     "start": 2000, "end": 2016},
    {"id": "3", "label": "2017-2026", "sub": "Post-disclosure",
     "start": 2017, "end": 2100},
    {"id": "nd", "label": "NO DATE", "sub": "no start date recorded",
     "start": None, "end": None},
]

# Class colours, read off the current renderer (tools/build_dashboard.py line
# 543), which is what the Design response section 1.1 points at.
# Class colours: the program map's chip markers, L0_CLS in tools/l0_patches.py,
# which is what the Design response section 1.1 points at ("the current map's
# chip markers"). build_dashboard.py's PALETTE differs on document and event and
# belongs to the old network map.
CLASS_COLOUR = {
    "document": "#f0d264",
    "domain": "#e08ad0",
    "event": "#7fb4e8",
    "institution": "#a795e8",
    "legislation": "#e08ad0",
    "location": "#7fb4e8",
    "person": "#c9d2dd",
    "program": "#66d69f",
}

CLUSTER_LABEL = {
    "contractor": "Contractor",
    "ffrdc": "FFRDC",
    "ic": "Intelligence community",
    "legacy": "Legacy record",
    "media": "Media",
    "other": "Other",
    "oversight": "Oversight",
    "research": "Research",
    "witness": "Witness",
}

URL_RE = re.compile(r"https?://[^\s\"'<>|)\]]+")


# ---------------------------------------------------------------- io helpers

def rd(rel):
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as f:
        return json.load(f)


def write(path, obj, indent):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    txt = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=indent)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
        f.write("\n")
    return len(txt.encode("utf-8")) + 1


def year_of(s):
    if not s:
        return None
    m = re.match(r"\s*(\d{4})", str(s))
    return int(m.group(1)) if m else None


def era_of(datestart):
    """The model's era table, applied to a start date.  'nd' when undated."""
    y = year_of(datestart)
    if y is None:
        return "nd"
    for e in ERAS:
        if e["id"] == "nd":
            continue
        if (e["start"] is None or y >= e["start"]) and y <= e["end"]:
            return e["id"]
    return "nd"


def first_url(s):
    if not s:
        return None
    m = URL_RE.search(str(s))
    return m.group(0) if m else None


def host_of(url):
    if not url:
        return None
    m = re.match(r"https?://([^/:]+)", url)
    return m.group(1).lower() if m else None


def source_hash():
    """A content hash of the research inputs, and of nothing else.

    CROSS-PLATFORM.  The bytes are newline-normalised (CRLF -> LF) before they go
    in, and the name that goes in beside them is the forward-slash relative name
    spelled in INPUTS, never an os.path one.  Without that normalisation this
    value is a function of the CHECKOUT rather than of the content: the repo has
    no .gitattributes, so a Windows clone with core.autocrlf=true gets CRLF in
    every text input and the identical commit hashed 3c5aa769b9d2 here and
    e5835f8cdaf3 on Linux CI.  That difference turned the gate's `app` job red on
    every push over seven lines that meant nothing.

    Nothing here reads mtimes, and nothing here reads .git.  This used to return
    the short id of whatever commit .git/HEAD named, which index.json published as
    "sourceCommit" -- the same class of defect, a published value that moves when
    the content has not.  It is gone; `source` is the provenance stamp.

    THE BUILD-DATE STAMP IS NEUTRALISED TOO (25 September 2026).  merge.py and
    build_l0.py write `"generated": "<today>"` into their outputs, which are inputs
    here, so hashing the stamp made `source` a function of the DAY the pipeline ran.
    That did not matter while CI rebuilt only this step from committed inputs; it
    matters now that tools/build.py runs the whole pipeline and check_rebuild.py
    compares everything, because a commit built on one day and rebuilt in CI on the
    next would differ in seven files over nothing.  The stamp's own field,
    `generated`, is still published, and check_rebuild.py normalises it.
    """
    stamp = re.compile(rb'"generated"\s*:\s*"\d{4}-\d{2}-\d{2}"')
    h = hashlib.sha1()
    for rel in INPUTS:
        h.update(rel.encode("utf-8"))
        with open(os.path.join(ROOT, rel), "rb") as f:
            raw = f.read().replace(b"\r\n", b"\n")
        h.update(hashlib.sha1(stamp.sub(b'"generated":"<stamped>"', raw)).digest())
    return h.hexdigest()[:12]


# ------------------------------------------------------------ source loading

class Src(object):
    def __init__(self, board_rel=BOARD):
        self.board = rd(board_rel)
        self.l0 = rd(L0_MODEL)
        self.layout = rd(L0_LAYOUT)["current"]
        self.highlights = rd(L0_HIGHLIGHTS)
        self.shorts = rd(L0_SHORTS).get("shorts", {})
        # the model's `l0` list carries the full record of every node above the
        # floor, including the derived `short`; `nodes` is a compact id -> tuple map
        self.l0_short = {x["id"]: x.get("short") for x in (self.l0.get("l0") or []) if isinstance(x, dict) and x.get("id")}
        self.foia = rd(FOIA_LINKS)
        self.patents = rd(PATENTS_VIEW)
        self.observables = rd(OBSERVABLES_VIEW)
        self.threads = rd(THREADS) if os.path.exists(os.path.join(ROOT, THREADS)) else None
        self.nodes = self.board["people"] + self.board["entities"]
        self.byid = {n["id"]: n for n in self.nodes}

    def generated(self):
        vals = [self.board.get("generated"), self.l0.get("generated"),
                rd(L0_LAYOUT).get("generated")]
        return max(v for v in vals if v)


def check_era_table(layout):
    """The era table above must still be the model's.  Fails loudly if it moved."""
    want = [(str(e["id"]), e["label"]) for e in layout["eras"]]
    have = [(e["id"], e["label"]) for e in ERAS]
    if want != have:
        raise SystemExit(
            "era table drift: data/l0-layout-model.json says %r, this file says %r.\n"
            "Do not edit the constant to silence this -- the model is the authority."
            % (want, have))


# ---------------------------------------------------------------- derivation

def node_dates(n):
    """(dateStart, dateEnd).  People carry one `date`; entities carry a range."""
    if n.get("cls") == "person":
        return n.get("date"), None
    return n.get("dateStart"), n.get("dateEnd")


def build_indexes(s):
    """Everything the several outputs share, derived once."""
    ix = {}

    # degree, from the L0 model's node table: id -> [label, cls, deg, tier]
    ix["deg"] = {k: v[2] for k, v in s.l0["nodes"].items()}

    # the L0 floor
    ix["l0ids"] = set(n["id"] for n in s.l0["l0"])
    ix["layout"] = {n["id"]: n for n in s.layout["nodes"]}

    # start-here register: rank 1..14, in the authored order
    ix["hl"] = {f["id"]: i + 1 for i, f in enumerate(s.highlights["flags"])}

    # claim tier counts per node
    tiers = {}
    for n in s.nodes:
        c = [0, 0, 0]
        for cl in (n.get("claims") or []):
            t = cl.get("tier")
            if t in (1, 2, 3):
                c[t - 1] += 1
        tiers[n["id"]] = c
    ix["claimTiers"] = tiers

    # edges touching each node, and denials
    out, inn, denials = {}, {}, {}
    for e in s.board["edges"]:
        out.setdefault(e["a"], []).append(e)
        inn.setdefault(e["b"], []).append(e)
        if e.get("type") == "denial":
            by = e.get("denier") or e["a"]
            of = e["b"] if by == e["a"] else e["a"]
            row = {"by": by, "of": of, "edge": e}
            denials.setdefault(e["a"], []).append(row)
            denials.setdefault(e["b"], []).append(row)
    ix["out"], ix["in"], ix["denials"] = out, inn, denials
    ix["denied"] = set(r["of"] for rows in denials.values() for r in rows)

    # timeline by node
    tl = {}
    for t in s.board["timeline"]:
        if t.get("node"):
            tl.setdefault(t["node"], []).append(t)
    ix["timeline"] = tl

    # FOIA: which nodes have an open question linked
    ix["foiaNodes"] = set(s.foia["byNode"].keys())
    return ix


def short_of(s, n):
    """data/l0-shorts.json where authored, else the L0 model's derived short for a
    map node (build_l0.py derives one for every node above the floor and the map
    has always drawn it), else the label."""
    a = s.shorts.get(n["id"])
    if isinstance(a, str) and a.strip():
        return a.strip()
    m = getattr(s, "l0_short", {}).get(n["id"])
    if isinstance(m, str) and m.strip():
        return m.strip()
    return n["label"]


# ------------------------------------------------------------------- outputs

def index_json(s, ix, meta):
    nodes = []
    for n in s.nodes:
        ds, de = node_dates(n)
        lay = ix["layout"].get(n["id"])
        nodes.append({
            "A": n.get("A"),
            "C": n.get("C"),
            "D": n.get("D"),
            "band": lay["band"] if lay else None,
            "claims": ix["claimTiers"][n["id"]],
            "cls": n.get("cls"),
            "cluster": n.get("cluster"),
            "dateEnd": de,
            "dateStart": ds,
            # No `domains` here on purpose: the evidence explorer's "source
            # domain" filter is the source URL's host, which rides on every row
            # of claims.json, and the research-provenance domains are on
            # nodes/<id>.json.  Carrying them here cost 180 KB of index for a
            # filter that does not read them.
            "deg": ix["deg"].get(n["id"], 0),
            "era": era_of(ds),
            "hl": ix["hl"].get(n["id"]),
            "id": n["id"],
            "l0": n["id"] in ix["l0ids"],
            "label": n["label"],
            "short": short_of(s, n),
            "status": n.get("status"),
            "tier": n.get("tier"),
        })
    nodes.sort(key=lambda r: r["id"])
    return {
        "bands": [{"id": b["id"], "label": b["id"].replace("-", " ")}
                  for b in s.layout["bands"]],
        "classes": [{"colour": CLASS_COLOUR[c], "id": c, "label": c}
                    for c in sorted(CLASS_COLOUR)],
        "clusters": [{"id": c, "label": CLUSTER_LABEL.get(c, c)}
                     for c in sorted(CLUSTER_LABEL)],
        "counts": counts(s, ix),
        "eras": ERAS,
        "generated": meta["generated"],
        "nodes": nodes,
        "source": meta["source"],
    }


def counts(s, ix):
    ct = [0, 0, 0]
    for c in ix["claimTiers"].values():
        for i in range(3):
            ct[i] += c[i]
    pv = s.patents
    sheets = len(pv["drawings"]["sheets"])
    # Distinct (node, question) pairs. A question that two requests would close is
    # one open question, not two: until 25 September 2026 this summed per request
    # and Home printed 121 where the board holds 116 (check C27 re-derives it).
    fq = len({(n["node"], q) for r in s.foia["requests"] for n in r["nodes"]
              for q in n["questions"] + n["partial"]})
    return {
        "claims": {"1": ct[0], "2": ct[1], "3": ct[2]},
        "edges": len(s.board["edges"]),
        "entities": len(s.board["entities"]),
        "foia": {"nodes": len(s.foia["byNode"]),
                 "questions": fq,
                 "requests": len(s.foia["requests"])},
        "l0": len(s.l0["l0"]),
        "nodes": len(s.nodes),
        "patents": len(pv["filings"]),
        "people": len(s.board["people"]),
        "sheets": sheets,
        "threads": len(threads_list(s)),
        "timeline": len(s.board["timeline"]),
    }


def threads_list(s):
    t = s.threads
    if t is None:
        return []
    return t.get("threads", t) if isinstance(t, dict) else t


def edges_json(s):
    rows = [{"a": e["a"], "b": e["b"], "dateStart": e.get("dateStart"),
             "label": e.get("label") or "", "t": e["type"],
             "tier": e.get("claimTier")}
            for e in s.board["edges"]]
    rows.sort(key=lambda r: (r["a"], r["b"], r["t"], r["label"]))
    return rows


def timeline_json(s):
    rows = []
    for t in s.board["timeline"]:
        rows.append({
            "date": t.get("date"),
            "era": era_of(t.get("date")),
            "id": t["id"],
            "label": t.get("label"),
            "node": t.get("node"),
            "precision": t.get("precision"),
            "strand": t.get("strand"),
            "text": t.get("text"),
            "tier": t.get("tier"),
        })
    rows.sort(key=lambda r: (r["date"] or "", r["id"]))
    return rows


def claims_json(s, ix):
    rows = []
    for n in s.nodes:
        denied = n["id"] in ix["denied"]
        open_q = n["id"] in ix["foiaNodes"]
        for c in (n.get("claims") or []):
            url = first_url(c.get("source"))
            rows.append({
                "cls": n.get("cls"),
                "cluster": n.get("cluster"),
                "denied": denied,
                "label": n["label"],
                "node": n["id"],
                "open": open_q,
                "source": {"domain": host_of(url),
                           "text": c.get("source"),
                           "url": url},
                "text": c.get("text"),
                "tier": c.get("tier"),
            })
    rows.sort(key=lambda r: (r["node"], r["tier"] or 0, r["text"] or ""))
    return rows


def node_files(s, ix):
    """One file per node.  Returns {id: object}."""
    dossiers = s.l0["dossiers"]
    ei = s.board.get("entityInfo", {})
    byNode = s.foia["byNode"]
    out = {}
    for n in s.nodes:
        nid = n["id"]
        ds, de = node_dates(n)
        rec = dict(n)
        rec.pop("_domains", None)
        rec["domains"] = sorted(n.get("_domains") or [])
        rec["dateStart"], rec["dateEnd"] = ds, de
        rec["short"] = short_of(s, n)
        rec["era"] = era_of(ds)
        lay = ix["layout"].get(nid)
        rec["band"] = lay["band"] if lay else None
        rec["l0"] = nid in ix["l0ids"]
        rec["deg"] = ix["deg"].get(nid, 0)
        rec["hl"] = ix["hl"].get(nid)
        rec["dossier"] = dossiers.get(nid)
        rec["entityInfo"] = ei.get(nid)

        conns = []
        for e, direction in ([(e, "out") for e in ix["out"].get(nid, [])] +
                             [(e, "in") for e in ix["in"].get(nid, [])]):
            other = e["b"] if direction == "out" else e["a"]
            o = s.byid.get(other)
            if o is None:
                continue
            conns.append({
                "claimTier": e.get("claimTier"),
                "cls": o.get("cls"),
                "dateEnd": e.get("dateEnd"),
                "dateStart": e.get("dateStart"),
                "direction": direction,
                # the spec lists `label` twice, for the neighbour and for the
                # edge; the neighbour keeps `label`, the edge takes `edgeLabel`.
                "edgeLabel": e.get("label") or "",
                "id": other,
                "l0": other in ix["l0ids"],
                "label": o["label"],
                "note": e.get("note") or "",
                "sources": e.get("sources") or [],
                "tier": o.get("tier"),
                "type": e["type"],
            })
        conns.sort(key=lambda r: (r["id"], r["type"], r["direction"]))
        rec["connections"] = conns

        dens = []
        seen = set()
        for row in ix["denials"].get(nid, []):
            e = row["edge"]
            k = (e["a"], e["b"], e.get("label"), e.get("note"))
            if k in seen:
                continue
            seen.add(k)
            by, of = row["by"], row["of"]
            dens.append({
                "by": {"id": by, "label": s.byid[by]["label"] if by in s.byid else by},
                "claimTier": e.get("claimTier"),
                "denialKind": e.get("denialKind"),
                "label": e.get("label") or "",
                "note": e.get("note") or "",
                "of": {"id": of, "label": s.byid[of]["label"] if of in s.byid else of},
                "sources": e.get("sources") or [],
            })
        dens.sort(key=lambda r: (r["by"]["id"], r["of"]["id"], r["label"]))
        rec["denials"] = dens

        rec["timeline"] = sorted(
            [{"date": t.get("date"), "id": t["id"], "label": t.get("label"),
              "precision": t.get("precision"), "strand": t.get("strand"),
              "text": t.get("text"), "tier": t.get("tier")}
             for t in ix["timeline"].get(nid, [])],
            key=lambda r: (r["date"] or "", r["id"]))

        reqs = byNode.get(nid, [])
        qs = sorted(set(q for r in reqs for q in (r["questions"] + r["partial"])))
        rec["foia"] = {"questions": qs, "requests": reqs}

        rec["members"] = (sorted(lay["members"], key=lambda m: m["id"])
                          if lay else None)
        out[nid] = rec
    return out


def map_json(s, ix, meta):
    lay = s.layout
    lab = {}
    for e in s.board["edges"]:
        if e.get("type") == "denial" and (e.get("label") or "").strip():
            lab[tuple(sorted((e["a"], e["b"])))] = e["label"].strip()

    nodes = []
    for n in lay["nodes"]:
        b = s.byid.get(n["id"], {})
        ds, _ = node_dates(b) if b else (None, None)
        nodes.append({
            "A": n.get("A"), "C": n.get("C"), "D": n.get("D"),
            "band": n["band"], "cls": n["cls"], "cluster": n["cluster"],
            "dateStart": ds, "era": str(n["era"]) if n["era"] is not None else "nd",
            "hl": ix["hl"].get(n["id"]), "id": n["id"],
            "label": n["label"], "short": n["short"], "tier": n["tier"],
        })
    nodes.sort(key=lambda r: r["id"])

    direct, summarised, pairs = [], [], []
    for e in lay["edges"]:
        if e["kind"] == "direct":
            direct.append({"a": e["a"], "b": e["b"], "tier": e["tier"],
                           "types": sorted(e.get("types") or [])})
            if e.get("denial"):
                by = e.get("denier") or e["a"]
                of = e["b"] if by == e["a"] else e["a"]
                pairs.append({"by": by, "kind": e.get("denialKind"),
                              "label": lab.get(tuple(sorted((e["a"], e["b"])))) or "",
                              "of": of})
        else:
            summarised.append({"a": e["a"], "b": e["b"],
                               "via": sorted(e.get("via") or [])})
    direct.sort(key=lambda r: (r["a"], r["b"]))
    summarised.sort(key=lambda r: (r["a"], r["b"]))
    pairs.sort(key=lambda r: (r["by"], r["of"]))

    cells = {}
    for n in nodes:
        cells.setdefault("%s.%s" % (n["band"], n["era"]), []).append(n["id"])
    for k in cells:
        cells[k].sort()

    return {
        "bands": [{"id": b["id"], "label": b["id"].replace("-", " ")}
                  for b in lay["bands"]],
        "cells": cells,
        "denialPairs": pairs,
        "direct": direct,
        "entryPaths": [{"blurb": p["blurb"], "id": p["id"], "ids": p["ids"],
                        "label": p["label"], "onMap": p["onMap"],
                        "total": p["total"]}
                       for p in sorted(s.l0["entryPaths"], key=lambda p: p["id"])],
        "eras": ERAS,
        "generated": meta["generated"],
        "nodes": nodes,
        "source": meta["source"],
        "summarised": summarised,
    }


def patents_json(s, meta):
    pv = s.patents
    board = s.byid

    # sheets, keyed to a filing by patent number, then by publication number
    numkey = lambda x: re.sub(r"[^0-9A-Za-z]", "", str(x or "")).upper()
    by_num = {}
    for f in pv["filings"]:
        by_num[numkey(f["number"])] = f["id"]
    # One sheet, US 2017/0313446, is PAX 205 as published before the appeal.  No
    # filing row carries that publication number, so it is not attached to a
    # patent by guess: it goes to drawings.unmatchedSheets with its own caption,
    # which is what the caption already says it is.  Absent prints as absent.
    sheets = {}
    unmatched = []
    for k, sh in enumerate(pv["drawings"]["sheets"]):
        fid = by_num.get(numkey(sh["patent"]))
        m = re.search(r"_fig(\d+)\.", sh["file"])
        row = {"caption": sh["caption"], "fig": int(m.group(1)) if m else None,
               "file": sh["file"], "k": k, "patent": sh["patent"],
               "thumb": "thumbs/" + sh["file"]}
        if fid:
            sheets.setdefault(fid, []).append(row)
        else:
            unmatched.append(row)

    # prosecution, from the two comparison lanes (dated, labelled events) with
    # the file-wrapper paper of the same date attached where one was obtained.
    wrapper = pv["wrapper"]
    wfiles = {}
    for o in wrapper["obtained"]:
        if o.get("file"):
            wfiles[o["date"]] = o["file"]
    wrapper_app = wrapper["application"]
    lanes = {}
    for lane in pv["comparison"]["lanes"]:
        rows = []
        for ev in lane["events"]:
            rows.append({"date": ev["date"], "file": None, "kind": ev["kind"],
                         "label": ev["label"], "note": ev.get("note")})
        lanes[lane["filing"]] = rows

    # maintenance-fee outcome, from the `maintenance` finding's own rows
    fee = {}
    for fnd in pv["findings"]:
        for r in (fnd.get("rows") or []):
            if r.get("number") and r.get("date"):
                fee[numkey(r["number"])] = {"finding": fnd["id"],
                                            "lapsed": r["date"],
                                            "title": fnd["title"]}

    pats = []
    for f in pv["filings"]:
        nid = f["id"] if f["id"] in board else None
        n = board.get(f["id"]) or {}
        pros = lanes.get(f["id"], [])
        if f["application"] == wrapper_app:
            pros = [dict(p, file=wfiles.get(p["date"])) for p in pros]
            have = set(p["date"] for p in pros)
            for o in wrapper["obtained"]:
                if o["date"] not in have:
                    pros.append({"date": o["date"], "file": o.get("file"),
                                 "kind": "paper", "label": o["label"],
                                 "note": None})
            pros.sort(key=lambda p: (p["date"], p["label"]))
        pats.append({
            "absent": wrapper["absent"] if f["application"] == wrapper_app else [],
            "application": f["application"],
            "artUnits": f.get("artUnits"),
            "assignee": None,
            "docket": f.get("docket"),
            "examiner": f.get("examiner"),
            "expired": f.get("expired"),
            "fee": fee.get(numkey(f["number"])),
            "filed": f.get("filed"),
            "granted": f.get("granted"),
            "inventor": None,
            "node": nid,
            "number": f["number"],
            "published": f.get("published"),
            "sheets": sorted(sheets.get(f["id"], []), key=lambda r: r["k"]),
            "source": f.get("source"),
            "status": f.get("status"),
            "sub": n.get("sub"),
            "supervisor": f.get("supervisor"),
            "title": f.get("title"),
            "prosecution": pros,
        })
    pats.sort(key=lambda p: p["number"])

    return {
        "comparison": pv["comparison"],
        "drawings": {"provenance": pv["drawings"]["provenance"],
                     "standfirst": pv["drawings"]["standfirst"],
                     "treatment": pv["drawings"].get("_treatment"),
                     "unmatchedSheets": unmatched},
        "eyebrow": pv["eyebrow"],
        "findings": pv["findings"],
        "generated": meta["generated"],
        "observables": s.observables,
        "openQuestions": pv["openQuestions"] + s.observables.get("openQuestions", []),
        "patents": pats,
        "quotes": pv["quotes"],
        "source": meta["source"],
        "standfirst": pv["standfirst"],
        "title": pv["title"],
        "wrapper": wrapper,
    }


def highlights_json(s, meta):
    return {
        "cap": s.highlights.get("_cap"),
        "flags": [{"id": f["id"], "rank": i + 1, "why": f["why"]}
                  for i, f in enumerate(s.highlights["flags"])],
        "generated": meta["generated"],
        "leftOff": s.highlights.get("_considered_and_left_off", []),
        "rule": s.highlights["rule"],
        "source": meta["source"],
    }


def foia_json(s, meta):
    return {
        "byNode": s.foia["byNode"],
        "generated": meta["generated"],
        "letters": s.foia["source"],
        "requests": s.foia["requests"],
        "source": meta["source"],
        "status": s.foia["_status"],
    }


def analyst_json(s, ix, meta):
    """The chips, per route kind, from data/analyst-suggestions.json.

    Until 11 September 2026 this scraped a SUGGESTIONS literal out of
    tools/build_dashboard.py, which meant the shipped app's analyst chips were
    a by-product of the OLD shell and could not be changed without editing a
    renderer that is being retired.  They are data now.

    `shape` tells the page that `byRoute` is authoritative.  `suggestions` is
    still written, as the home list, so a reader holding a cached copy of an
    older page gets the home chips rather than none.
    """
    path = os.path.join(ROOT, SUGGESTIONS)
    try:
        raw = json.load(open(path, encoding="utf-8"))
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit("%s could not be read: %s" % (SUGGESTIONS, e))

    by_route = {}
    for key in ANALYST_KEYS:
        got = raw.get(key)
        if not isinstance(got, list):
            raise SystemExit("%s has no list for the route key %r" % (SUGGESTIONS, key))
        chips = [c for c in got if isinstance(c, str) and c.strip()]
        if len(chips) != len(got):
            raise SystemExit("%s: every chip under %r must be a non-empty string"
                             % (SUGGESTIONS, key))
        if len(chips) < ANALYST_MIN:
            raise SystemExit("%s: %r has %d chips, the floor is %d"
                             % (SUGGESTIONS, key, len(chips), ANALYST_MIN))
        by_route[key] = chips

    unknown = [k for k in raw
               if not k.startswith("_") and k not in ANALYST_KEYS]
    if unknown:
        raise SystemExit("%s carries route keys the app does not render: %s"
                         % (SUGGESTIONS, ", ".join(sorted(unknown))))

    check_chip_figures(raw, by_route, counts(s, ix))

    return {"byRoute": by_route, "generated": meta["generated"],
            "shape": "per-route", "source": meta["source"],
            "suggestions": by_route["home"], "worker": ANALYST_WORKER}


def check_chip_figures(raw, by_route, ct):
    """A chip that quotes a count is an assertion, and counts move.

    Four of the chips written on 11 September 2026 quote one -- 913 timeline
    events, 137 of 1,057 nodes on the map, 514 Tier 3 claims -- and a research
    pass that moves any of them leaves the chip quietly wrong, which is CLAUDE.md
    section 2 wearing a different hat.  So the file declares what it quotes, in
    `_figures`, and this fails the build on two things: a figure that no longer
    matches the board, and a figure no chip actually quotes, which means the chip
    was reworded and the declaration was left behind.

    Numbers are matched in both the plain and the comma-grouped spelling, because
    the chips are prose and say "1,057" where the data says 1057.
    """
    figs = raw.get("_figures")
    if figs is None:
        return
    if not isinstance(figs, dict):
        raise SystemExit("%s: _figures must be a map of count path to number" % SUGGESTIONS)

    text = " ".join(c for chips in by_route.values() for c in chips)
    wrong, unquoted = [], []
    for path, want in sorted(figs.items()):
        here = ct
        for part in path.split("."):
            if not isinstance(here, dict) or part not in here:
                raise SystemExit("%s: _figures names %r, which is not a board count"
                                 % (SUGGESTIONS, path))
            here = here[part]
        if here != want:
            wrong.append("%s is %s, the chips say %s" % (path, here, want))
        spellings = {str(want), "{:,}".format(want)}
        if not any(sp in text for sp in spellings):
            unquoted.append("%s (%s) is declared but no chip quotes it" % (path, want))
    if wrong:
        raise SystemExit(
            "%s quotes figures the board no longer carries:\n  %s\n"
            "Reword the chips and update _figures together."
            % (SUGGESTIONS, "\n  ".join(wrong)))
    if unquoted:
        raise SystemExit(
            "%s declares figures no chip quotes:\n  %s"
            % (SUGGESTIONS, "\n  ".join(unquoted)))


def threads_json(s, meta):
    return {"generated": meta["generated"], "source": meta["source"],
            "threads": threads_list(s)}


# ---------------------------------------------------------------------- copy

def copy_patents(quiet=False):
    src = os.path.join(ROOT, DRAWINGS)
    os.makedirs(os.path.join(PAT_OUT, "thumbs"), exist_ok=True)
    n = 0
    for f in sorted(os.listdir(src)):
        if f.lower().endswith(".png"):
            shutil.copyfile(os.path.join(src, f), os.path.join(PAT_OUT, f))
            n += 1
    t = 0
    for f in sorted(os.listdir(os.path.join(src, "thumbs"))):
        if f.lower().endswith(".png"):
            shutil.copyfile(os.path.join(src, "thumbs", f),
                            os.path.join(PAT_OUT, "thumbs", f))
            t += 1
    shutil.copyfile(os.path.join(src, "PROVENANCE.md"),
                    os.path.join(PAT_OUT, "PROVENANCE.md"))
    return n, t


# --------------------------------------------------------------------- build

def build(quiet=False):
    s = Src()
    check_era_table(s.layout)
    ix = build_indexes(s)
    meta = {"generated": s.generated(), "source": source_hash()}

    written = []
    written.append(("data/index.json",
                    write(os.path.join(OUT, "index.json"), index_json(s, ix, meta), 1)))
    written.append(("data/edges.json",
                    write(os.path.join(OUT, "edges.json"), edges_json(s), 0)))
    written.append(("data/timeline.json",
                    write(os.path.join(OUT, "timeline.json"), timeline_json(s), 0)))
    written.append(("data/claims.json",
                    write(os.path.join(OUT, "claims.json"), claims_json(s, ix), 0)))
    written.append(("data/map.json",
                    write(os.path.join(OUT, "map.json"), map_json(s, ix, meta), 1)))
    written.append(("data/threads.json",
                    write(os.path.join(OUT, "threads.json"), threads_json(s, meta), 1)))
    written.append(("data/patents.json",
                    write(os.path.join(OUT, "patents.json"), patents_json(s, meta), 1)))
    written.append(("data/highlights.json",
                    write(os.path.join(OUT, "highlights.json"), highlights_json(s, meta), 1)))
    written.append(("data/foia.json",
                    write(os.path.join(OUT, "foia.json"), foia_json(s, meta), 1)))
    written.append(("data/analyst.json",
                    write(os.path.join(OUT, "analyst.json"), analyst_json(s, ix, meta), 1)))

    nd = os.path.join(OUT, "nodes")
    if os.path.isdir(nd):
        for f in os.listdir(nd):
            os.remove(os.path.join(nd, f))
    files = node_files(s, ix)
    tot = 0
    for nid, rec in sorted(files.items()):
        tot += write(os.path.join(nd, nid + ".json"), rec, 0)
    written.append(("data/nodes/*.json (%d files)" % len(files), tot))

    imgs, thumbs = copy_patents()

    if not quiet:
        for name, size in written:
            print("  %-40s %9s" % (name, "{:,}".format(size)))
        print("  %-40s %9s" % ("patents/*.png", "%d originals, %d thumbs"
                               % (imgs, thumbs)))
        print("  generated %s  source %s"
              % (meta["generated"], meta["source"]))
    return written, meta


# --------------------------------------------------------------------- check

def check(board_rel=BOARD, quiet=False):
    """Re-derive every count in index.json from the sources.  Nothing here reads
    the builder's own intermediates: the board is re-opened and re-counted."""
    path = os.path.join(OUT, "index.json")
    if not os.path.exists(path):
        raise SystemExit("no app/public/data/index.json -- build first")
    built = json.load(open(path, encoding="utf-8"))
    have = built["counts"]

    b = rd(board_rel)
    nodes = b["people"] + b["entities"]
    ct = {1: 0, 2: 0, 3: 0}
    for n in nodes:
        for c in (n.get("claims") or []):
            if c.get("tier") in ct:
                ct[c["tier"]] += 1
    l0 = rd(L0_MODEL)
    foia = rd(FOIA_LINKS)
    pv = rd(PATENTS_VIEW)
    th = rd(THREADS) if os.path.exists(os.path.join(ROOT, THREADS)) else []
    th = th.get("threads", th) if isinstance(th, dict) else th
    fq = len({(x["node"], q) for r in foia["requests"] for x in r["nodes"]
              for q in x["questions"] + x["partial"]})

    want = {
        "claims": {"1": ct[1], "2": ct[2], "3": ct[3]},
        "edges": len(b["edges"]),
        "entities": len(b["entities"]),
        "foia": {"nodes": len(foia["byNode"]), "questions": fq,
                 "requests": len(foia["requests"])},
        "l0": len(l0["l0"]),
        "nodes": len(nodes),
        "patents": len(pv["filings"]),
        "people": len(b["people"]),
        "sheets": len(pv["drawings"]["sheets"]),
        "threads": len(th),
        "timeline": len(b["timeline"]),
    }

    drift = []
    for k in sorted(set(list(want) + list(have))):
        if want.get(k) != have.get(k):
            drift.append("  %-10s index.json %r  re-derived %r"
                         % (k, have.get(k), want.get(k)))

    # and the node rows themselves must be the board's nodes, exactly
    ids_built = set(r["id"] for r in built["nodes"])
    ids_board = set(n["id"] for n in nodes)
    if ids_built != ids_board:
        only_b = sorted(ids_built - ids_board)[:5]
        only_s = sorted(ids_board - ids_built)[:5]
        drift.append("  node ids differ: %d in index.json only (%s), "
                     "%d in board only (%s)"
                     % (len(ids_built - ids_board), ", ".join(only_b) or "-",
                        len(ids_board - ids_built), ", ".join(only_s) or "-"))

    # every node file must exist and carry its own id
    missing = [i for i in sorted(ids_board)
               if not os.path.exists(os.path.join(OUT, "nodes", i + ".json"))]
    if missing:
        drift.append("  %d node files missing, e.g. %s"
                     % (len(missing), ", ".join(missing[:5])))

    if drift:
        if not quiet:
            print("FAIL  app/public/data drifted from the sources:")
            for d in drift:
                print(d)
        return False
    if not quiet:
        for k in sorted(want):
            print("  %-10s %s" % (k, want[k]))
        print("OK    every count in index.json re-derives from %s and friends"
              % board_rel)
    return True


def self_test():
    """--check must reject a board with one node removed.  Shown, not asserted."""
    print("self-test: --check against the real board")
    if not check(quiet=True):
        print("  FAIL: --check rejects the unpoisoned board")
        return False
    print("  pass: accepted")

    b = rd(BOARD)
    victim = b["entities"][len(b["entities"]) // 2]["id"]
    b["entities"] = [e for e in b["entities"] if e["id"] != victim]
    tmp = tempfile.mkdtemp(prefix="app-data-poison-")
    rel = os.path.relpath(os.path.join(tmp, "poisoned.json"), ROOT)
    with open(os.path.join(tmp, "poisoned.json"), "w", encoding="utf-8",
              newline="\n") as f:
        json.dump(b, f, ensure_ascii=False)
    print("self-test: --check against a copy with node %r removed" % victim)
    ok = check(board_rel=rel, quiet=True)
    shutil.rmtree(tmp, ignore_errors=True)
    if ok:
        print("  FAIL: --check ACCEPTED the poisoned board.  The check is broken.")
        return False
    print("  pass: rejected (entities and nodes counts drift, and the node id "
          "set differs by 1)")

    # And the chip figures, both ways round: a figure the board no longer
    # carries, and a figure no chip quotes any more.  Shown, not asserted.
    raw = json.load(open(os.path.join(ROOT, SUGGESTIONS), encoding="utf-8"))
    by_route = {k: raw[k] for k in ANALYST_KEYS}
    ct = counts(Src(), build_indexes(Src()))
    if not raw.get("_figures"):
        print("  skip: data/analyst-suggestions.json declares no _figures")
    else:
        for what, mangle in (
                ("a figure the board no longer carries",
                 lambda r: {**r, "_figures": {k: v + 1 for k, v in r["_figures"].items()}}),
                ("a declared figure no chip quotes",
                 lambda r: r)):
            bad = mangle(raw)
            chips = by_route
            if what.startswith("a declared"):
                chips = {k: [re.sub(r"[0-9][0-9,]*", "N", c) for c in v]
                         for k, v in by_route.items()}
            print("self-test: the chip figures against %s" % what)
            try:
                check_chip_figures(bad, chips, ct)
            except SystemExit as e:
                print("  pass: rejected (%s)" % str(e).splitlines()[1].strip())
                continue
            print("  FAIL: check_chip_figures ACCEPTED %s.  The check is broken." % what)
            return False

    print("self-test OK")
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--board", default=BOARD,
                   help="board to re-derive from (used by --self-test)")
    a = p.parse_args()
    if a.self_test:
        sys.exit(0 if self_test() else 1)
    if a.check:
        sys.exit(0 if check(a.board) else 1)
    build()


if __name__ == "__main__":
    main()
