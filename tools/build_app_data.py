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
                                                board (one node removed), and the
                                                topic files drifting from their records

TOPICS (redesign phase 5, task 3).  research/topics/<id>.json ship as
app/public/data/topics.json (the index the Atlas reads) and topics/<id>.json (one
record each, every id it cites resolved to its claim or edge).  An absorbed domain
node's own file carries `absorbedBy: <topic id>`; phase 6 redirects its page.

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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "topics"))
import topiclib  # noqa: E402
import source_pages  # noqa: E402  (phase 8: the source registry as the app ships it)

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
VOCAB = "schema/vocab.json"
PREDICATES = "research/_predicates.json"

INPUTS = [BOARD, L0_MODEL, L0_LAYOUT, L0_HIGHLIGHTS, L0_SHORTS, FOIA_LINKS,
          PATENTS_VIEW, OBSERVABLES_VIEW, SUGGESTIONS, VOCAB, PREDICATES]

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

# Class colours and cluster names come from schema/vocab.json since phase 3, the
# one vocabulary the pipeline and the app share. The colours are the program map's
# chip markers, read off L0_CLS in the old shell's tools/l0_patches.py (retired 25
# September 2026), which is what the Design response section 1.1 points at.
def _vocab():
    with open(os.path.join(ROOT, VOCAB), "r", encoding="utf-8") as f:
        return json.load(f)


_V = _vocab()
CLASS_COLOUR = {c["id"]: c["colour"] for c in _V["classes"]}
CLUSTER_LABEL = {c["id"]: c["label"] for c in _V["clusters"]}
SPACED_EM_DASH = re.compile(r"\s+\u2014\s+")

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
    # the authored topic records and sections are inputs too (phase 5); the
    # generated _proposals.json is not, since nothing here reads it
    topic_rel = ["research/topics/" + f for f in ["_sections.json"] + topiclib.stub_files()]
    for rel in INPUTS + topic_rel:
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
        self.topics = topiclib.load_topics()
        self.sections = topiclib.load_sections()
        self.preds = load_predicates(self.board)
        self.reg = source_pages.Registry(ROOT)

    def generated(self):
        vals = [self.board.get("generated"), self.l0.get("generated"),
                rd(L0_LAYOUT).get("generated")]
        return max(v for v in vals if v)


# ------------------------------------------------------------ the predicates

PREDICATE_VOCAB = {p["id"]: p for p in _V.get("predicates") or []}
FAMILY_PHRASE = {f["id"]: f["phrase"] for f in _V.get("predicateFamilies") or []}


def load_predicates(board):
    """research/_predicates.json (redesign phase 7): {edge id: row}. A key that is
    not a live edge id is an ERROR, not a no-op: the edge's ends, type or sentence
    changed, its id with them, and it must be classified again rather than keep a
    predicate chosen for a sentence it no longer has. A predicate outside
    schema/vocab.json is an error too. An edge with no row ships a null predicate,
    which verify.py rejects."""
    doc = rd(PREDICATES).get("predicates") or {}
    live = {e.get("id") for e in board["edges"]}
    orphans = sorted(k for k in doc if k not in live)
    if orphans:
        raise SystemExit("research/_predicates.json names %d edge id(s) not on the board, "
                         "e.g. %s: re-classify those edges" % (len(orphans), orphans[:5]))
    unknown = sorted({r.get("predicate") for r in doc.values()} - set(PREDICATE_VOCAB))
    if unknown:
        raise SystemExit("research/_predicates.json uses predicate(s) not in "
                         "schema/vocab.json: %s" % unknown)
    return doc


def predicate_view(s, e, here):
    """The predicate of edge `e` as read from node `here`: its id, family, the label
    from this side, and which side this node is on. `subject` names the end the
    forward label reads from; the other end reads the inverse; a symmetric
    predicate reads one label from either end."""
    r = s.preds.get(e.get("id"))
    if not r:
        return {"predicate": None, "family": None, "verb": None, "predicateSide": None,
                "predicateShown": False}
    p = PREDICATE_VOCAB[r["predicate"]]
    if p.get("symmetric"):
        verb, side = p["forward"], "either"
    elif e[r["subject"]] == here:
        verb, side = p["forward"], "subject"
    else:
        verb, side = p["inverse"], "object"
    # The display rule (schema/vocab.json predicateRules.display, decided 26
    # September 2026): the family is the reliable unit; a predicate's own label
    # and direction show only where its confidence is high, otherwise the row
    # reads the family's neutral phrase. `predicateSide` is recorded either way.
    shown = r.get("confidence") == "high"
    if not shown:
        verb = FAMILY_PHRASE[p["family"]]
    return {"predicate": p["id"], "family": p["family"], "verb": verb, "predicateSide": side,
            "predicateShown": shown}


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
            # `by` ONLY from an adjudicated denier (phase 3 decision 5). This
            # used to fall back to end `a`, and the node page printed "issued
            # here" or "directed here" off that guess for every denial the
            # adjudication had not reached. Where no denier is named there is
            # no direction to publish, and the row says so.
            by = e.get("denier") if e.get("denier") in (e["a"], e["b"]) else None
            of = (e["b"] if by == e["a"] else e["a"]) if by else None
            row = {"by": by, "of": of, "edge": e}
            denials.setdefault(e["a"], []).append(row)
            denials.setdefault(e["b"], []).append(row)
    ix["out"], ix["in"], ix["denials"] = out, inn, denials
    ix["denied"] = set(r["of"] for rows in denials.values() for r in rows if r["of"])

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
        # a spaced em dash in a display label becomes " - " (phase 3 decision 7;
        # recorded in tools/DISPLAY-NORMALISED.json by merge.py)
        return SPACED_EM_DASH.sub(" - ", a.strip())
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
    # phase 7: the predicate and the end its forward label reads from (a or b)
    rows = [{"a": e["a"], "b": e["b"], "dateStart": e.get("dateStart"),
             "id": e.get("id"),
             "label": e.get("label") or "",
             "predicate": (s.preds.get(e.get("id")) or {}).get("predicate"),
             "shown": (s.preds.get(e.get("id")) or {}).get("confidence") == "high",
             "subject": (s.preds.get(e.get("id")) or {}).get("subject"),
             "t": e["type"],
             "tier": e.get("claimTier")}
            for e in s.board["edges"]]
    rows.sort(key=lambda r: (r["a"], r["b"], r["t"], r["label"]))
    return rows


def timeline_json(s):
    # phase 9: the section lane, the primary topic, the event's own sources, and
    # the same-day duplicates (see _timeline_extras)
    sec, top, srcs, same = _timeline_extras(s)
    rows = []
    for t in s.board["timeline"]:
        row = {
            "date": t.get("date"),
            "era": era_of(t.get("date")),
            "id": t["id"],
            "label": t.get("label"),
            "node": t.get("node"),
            "precision": t.get("precision"),
            "strand": t.get("strand"),
            "text": t.get("text"),
            # two fields, two vocabularies (phase 3 decision 5): the event's
            # grade A/B/C and a claim tier 1/2/3. `tier` is not shipped.
            "grade": t.get("grade"),
            "claimTier": t.get("claimTier"),
            "section": sec[t["id"]],
            "topic": top[t["id"]],
        }
        if srcs.get(t["id"]):
            row["sources"] = srcs[t["id"]]
        if same.get(t["id"]):
            row["sameAs"] = same[t["id"]]
        rows.append(row)
    rows.sort(key=lambda r: (r["date"] or "", r["id"]))
    return rows


TIMELINE_OTHER = "other"
_STOP = {"the", "and", "for", "of", "to", "a", "an", "is", "on", "in", "at", "by", "its", "with"}


def _norm_label(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()


def near_same_label(a, b):
    """Two labels of one node on one day name the same event when they are nearly
    the same string (difflib ratio 0.7 or more, compared with spaces removed so
    STARGATE meets STAR GATE), or when every content word of the shorter is in the
    longer and it has at least two. Measured on the board on 26 September 2026:
    36 pairs of same node, same day labels reach 0.6; the ones this rule leaves
    apart are different acts on the same day (two witnesses at one hearing)."""
    import difflib
    na, nb = _norm_label(a), _norm_label(b)
    if not na or not nb:
        return False
    if difflib.SequenceMatcher(None, na.replace(" ", ""), nb.replace(" ", "")).ratio() >= 0.7:
        return True
    ta = {w for w in na.split() if len(w) > 2 and w not in _STOP}
    tb = {w for w in nb.split() if len(w) > 2 and w not in _STOP}
    lo, hi = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    return len(lo) >= 2 and lo <= hi


def _timeline_extras(s):
    """Per event id: the section of its node's primary topic (TIMELINE_OTHER when
    the event names no node or the node is in no topic), that primary topic, the
    event's own authored sources, and, for an event that repeats another of the
    same node on the same day under a near-identical label, the id of the one
    the timeline shows. Nothing is dropped: the repeat keeps its row and its text,
    and the page prints it under the one it repeats."""
    alias = _alias()
    ai = appears_in(s.topics, alias)
    tsec = {t["id"]: t.get("section") for t in s.topics}
    sec, top, srcs = {}, {}, {}
    for t in s.board["timeline"]:
        n = alias.get(t.get("node"), t.get("node"))
        first = (ai.get(n) or [[None]])[0][0] if n else None
        top[t["id"]] = first
        sec[t["id"]] = tsec.get(first) or TIMELINE_OTHER
        rows = []
        if t.get("source"):
            rows.append({"text": str(t["source"]), "url": first_url(t["source"])})
        for x in t.get("sources") or []:
            if isinstance(x, dict):
                rows.append({"text": x.get("name") or x.get("url") or "",
                             "url": x.get("url") or first_url(x.get("name"))})
            elif x:
                rows.append({"text": str(x), "url": first_url(x)})
        srcs[t["id"]] = rows
    # union the repeats of one node on one day
    by = {}
    for t in s.board["timeline"]:
        if t.get("node") and t.get("date"):
            by.setdefault((t["node"], t["date"]), []).append(t)
    grade = {"A": 0, "B": 1, "C": 2}
    same = {}
    for evs in by.values():
        if len(evs) < 2:
            continue
        evs = sorted(evs, key=lambda e: e["id"])
        parent = list(range(len(evs)))

        def root(i):
            while parent[i] != i:
                i = parent[i]
            return i
        for i in range(len(evs)):
            for j in range(i + 1, len(evs)):
                if near_same_label(evs[i].get("label"), evs[j].get("label")):
                    parent[root(j)] = root(i)
        groups = {}
        for i in range(len(evs)):
            groups.setdefault(root(i), []).append(evs[i])
        for g in groups.values():
            if len(g) < 2:
                continue
            keep = min(g, key=lambda e: (grade.get(e.get("grade"), 3),
                                         -len(e.get("text") or ""), e["id"]))
            for e in g:
                if e is not keep:
                    same[e["id"]] = keep["id"]
    return sec, top, srcs, same


# ------------------------------------------------------ person facets (phase 9)

PERSON_FACETS = "research/_person_facets.json"
INPUTS.append(PERSON_FACETS)


def facets_json(s, meta):
    """research/_person_facets.json as the directories read it: every person's
    roles, vital status, role status and sworn-testimony facet, with the words of
    their own record each rests on. The side-car is shipped as authored; verify.py
    holds it to the closed vocabulary and requires this file to equal it."""
    doc = rd(PERSON_FACETS) if os.path.exists(os.path.join(ROOT, PERSON_FACETS)) else {}
    people = doc.get("people") or {}
    return {
        "generated": meta["generated"],
        "people": {k: {f: v[f] for f in ("roles", "vitalStatus", "roleStatus", "underOath", "basis")
                       if f in v}
                   for k, v in sorted(people.items())},
        "source": meta["source"],
        "vocab": {k: v for k, v in (_V.get("personFacets") or {}).items() if not k.startswith("_")},
    }


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
                "id": c.get("id"),
                "label": n["label"],
                "node": n["id"],
                "open": open_q,
                "source": {"domain": host_of(url),
                           "text": c.get("source"),
                           "url": url},
                # phase 8: the registry sources it resolves to, or why it does not
                "sources": s.reg.claim_refs(c.get("id")),
                "unresolved": s.reg.why_unresolved(c.get("id")),
                "text": c.get("text"),
                "tier": c.get("tier"),
            })
    rows.sort(key=lambda r: (r["node"], r["tier"] or 0, r["text"] or ""))
    return rows


def node_files(s, ix):
    """One file per node.  Returns {id: object}."""
    absorbed_by = {i: t["id"] for t in s.topics for i in (t.get("absorbs") or [])}
    dossiers = s.l0["dossiers"]
    ei = s.board.get("entityInfo", {})
    byNode = s.foia["byNode"]
    out = {}
    for n in s.nodes:
        nid = n["id"]
        ds, de = node_dates(n)
        rec = dict(n)
        rec.pop("_domains", None)
        # Provenance, the research files this node was merged from, ships as
        # `sourceFiles`. It used to ship as `domains`, which overwrote a
        # person's AUTHORED topic tags (ids of domain nodes) with file names.
        # Both reach the page now, under different names (phase 3 decision 9).
        rec["sourceFiles"] = sorted(n.get("_domains") or [])
        rec["domains"] = list(n.get("domains") or [])
        rec["dateStart"], rec["dateEnd"] = ds, de
        rec["short"] = short_of(s, n)
        rec["era"] = era_of(ds)
        lay = ix["layout"].get(nid)
        rec["band"] = lay["band"] if lay else None
        rec["l0"] = nid in ix["l0ids"]
        rec["deg"] = ix["deg"].get(nid, 0)
        rec["hl"] = ix["hl"].get(nid)
        rec["dossier"] = dossiers.get(nid)
        rec["claims"] = [dict(c, sources=s.reg.claim_refs(c.get("id")),
                              unresolved=s.reg.why_unresolved(c.get("id")))
                         for c in (n.get("claims") or [])]
        rec["entityInfo"] = ei.get(nid)

        conns = []
        for e, direction in ([(e, "out") for e in ix["out"].get(nid, [])] +
                             [(e, "in") for e in ix["in"].get(nid, [])]):
            other = e["b"] if direction == "out" else e["a"]
            o = s.byid.get(other)
            if o is None:
                continue
            conns.append({
                # phase 7: predicate, family, the label read from THIS node's side
                # (`verb`) and which side it is on (`predicateSide`)
                **predicate_view(s, e, nid),
                "claimTier": e.get("claimTier"),
                "cls": o.get("cls"),
                "dateEnd": e.get("dateEnd"),
                "dateStart": e.get("dateStart"),
                "direction": direction,
                # the spec lists `label` twice, for the neighbour and for the
                # edge; the neighbour keeps `label`, the edge takes `edgeLabel`.
                "edgeLabel": e.get("label") or "",
                # the edge's own stable id (phase 4); `id` is the neighbour's
                "edgeId": e.get("id"),
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

            def ref(i):
                return {"id": i, "label": s.byid[i]["label"] if i in s.byid else i}
            dens.append({
                # both ends in record order, always; `by`/`of` only where the
                # adjudication names the denier, and null otherwise
                "a": ref(e["a"]),
                "b": ref(e["b"]),
                "by": ref(by) if by else None,
                "claimTier": e.get("claimTier"),
                "denialKind": e.get("denialKind"),
                "edgeId": e.get("id"),
                "label": e.get("label") or "",
                "note": e.get("note") or "",
                "of": ref(of) if of else None,
                "sources": e.get("sources") or [],
            })
        dens.sort(key=lambda r: (r["a"]["id"], r["b"]["id"], r["label"]))
        rec["denials"] = dens

        rec["timeline"] = sorted(
            [{"date": t.get("date"), "id": t["id"], "label": t.get("label"),
              "precision": t.get("precision"), "strand": t.get("strand"),
              "text": t.get("text"), "grade": t.get("grade"),
              "claimTier": t.get("claimTier")}
             for t in ix["timeline"].get(nid, [])],
            key=lambda r: (r["date"] or "", r["id"]))

        reqs = byNode.get(nid, [])
        qs = sorted(set(q for r in reqs for q in (r["questions"] + r["partial"])))
        rec["foia"] = {"questions": qs, "requests": reqs}

        rec["members"] = (sorted(lay["members"], key=lambda m: m["id"])
                          if lay else None)
        # a domain node a topic absorbs (phase 5): its page becomes that topic's
        if nid in absorbed_by:
            rec["absorbedBy"] = absorbed_by[nid]
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


def vocab_json(meta):
    """schema/vocab.json, published as /data/vocab.json: the one vocabulary, for
    anything that reads the data rather than the page's own bundle (the page
    imports the same file at build time, in app/src/vocab.ts)."""
    v = {k: val for k, val in _V.items() if not k.startswith("_")}
    v["generated"], v["source"] = meta["generated"], meta["source"]
    return v


def threads_json(s, meta):
    return {"generated": meta["generated"], "source": meta["source"],
            "threads": threads_list(s)}


# ------------------------------------------------------------ topics (phase 5)

REMOVED = "research/_removed.json"


def _alias():
    p = os.path.join(ROOT, REMOVED)
    return (rd(REMOVED).get("alias") or {}) if os.path.exists(p) else {}


def _source_row(text):
    """A claim's source as claims.json ships it."""
    url = first_url(text)
    return {"domain": host_of(url), "text": text, "url": url}


def topic_record(s, bd, alias, t):
    """One topic as app/public/data/topics/<id>.json ships it: the authored record
    (fields beginning with `_` left out), the content lists present even when empty,
    members resolved through the alias map and labelled, and `cites`, every cited
    id resolved to its claim or edge. An id that resolves to nothing ships as
    {id, kind: null, missing: true}: absent prints as absent, and verify.py and
    --check both fail on it."""
    rec = {k: v for k, v in t.items() if not k.startswith("_")}
    rec.setdefault("lead", None)
    for k in ("summary", "record", "claimed", "contested", "members", "questions", "related"):
        rec.setdefault(k, [])
    mem = []
    for m in rec["members"]:
        i = alias.get(m.get("id"), m.get("id")) if isinstance(m, dict) else m
        n = s.byid.get(i) or {}
        mem.append({"id": i, "role": m.get("role") if isinstance(m, dict) else None,
                    "label": n.get("label"), "cls": n.get("cls")})
    rec["members"] = mem
    # each unplaced claim with the id a topic cites it by
    if rec.get("unplacedClaims"):
        by_text = {(c.get("collapsedInto"), c.get("claim")): k
                   for k, c in topiclib.unplaced(t).items()}
        rec["unplacedClaims"] = [dict(c, id=by_text[(c.get("collapsedInto"), c.get("claim"))])
                                 for c in rec["unplacedClaims"]]
    cites = {}
    for cid in topiclib.cited_ids(t):
        cites[cid] = (topiclib.resolve(bd, t, cid, _source_row)
                      or {"id": cid, "kind": None, "missing": True})
        if cites[cid].get("kind") == "claim" and not cites[cid].get("unplaced"):
            cites[cid]["sourceRefs"] = s.reg.claim_refs(cid)
    rec["cites"] = cites
    return rec


def topic_coverage(s, topics, alias):
    """The share of non-domain nodes, and of people, that are a member of a topic
    (the figure verify.py holds against tools/TOPIC-COVERAGE-FLOOR.json)."""
    inm = {alias.get(m.get("id"), m.get("id")) for t in topics
           for m in t.get("members") or [] if isinstance(m, dict)}
    nodes = [n for n in s.nodes if n.get("cls") != "domain"]
    people = [n for n in nodes if n.get("cls") == "person"]

    def one(xs):
        c = sum(1 for n in xs if n["id"] in inm)
        return {"covered": c, "share": round(c / len(xs), 4) if xs else 0.0,
                "total": len(xs)}
    return {"nodes": one(nodes), "people": one(people)}


def topic_counts(t):
    """The counts topics.json carries for one topic, from the authored record.
    `record`, `claimed` and `contested` (phase 6) are the items in each of the
    three blocks: the Atlas filters on contested, and prints nothing it cannot
    count here."""
    return {"cites": len(topiclib.cited_ids(t)),
            "claimed": len(t.get("claimed") or []),
            "contested": len(t.get("contested") or []),
            "members": len(t.get("members") or []),
            "questions": len(t.get("questions") or []),
            "record": len(t.get("record") or [])}


# The order an entity's topics are listed in on its page (phase 6, "Appears in"):
# the topics where it is an anchor first, then by its role in the order
# schema/vocab.json lists the roles (subject first), then by topic id.
TOPIC_ROLES = [r["id"] for r in _V.get("topicRoles") or []]


def appears_in(topics, alias):
    """node id -> [[topic id, role, 1 if the node is one of the topic's anchors
    else 0], ...], primary topic first. Membership is the topic's `members`
    after alias resolution; being an anchor only orders it."""
    by = {}
    for t in topics:
        anchors = {alias.get(a, a) for a in t.get("anchors") or []}
        for m in t.get("members") or []:
            if not isinstance(m, dict):
                continue
            i = alias.get(m.get("id"), m.get("id"))
            by.setdefault(i, []).append([t["id"], m.get("role"), 1 if i in anchors else 0])
    rank = {r: k for k, r in enumerate(TOPIC_ROLES)}
    for xs in by.values():
        xs.sort(key=lambda x: (-x[2], rank.get(x[1], len(rank)), x[0]))
    return dict(sorted(by.items()))


def topics_json(s, meta, alias):
    rows = []
    for t in s.topics:
        lead = t.get("lead")
        rows.append({
            "counts": topic_counts(t),
            "focusEra": t.get("focusEra"),
            "id": t["id"],
            "kind": t.get("kind"),
            "lead": lead.get("text") if isinstance(lead, dict) else None,
            "related": list(t.get("related") or []),
            "researchGap": bool(str(t.get("researchGap") or "").strip()),
            "section": t.get("section"),
            "span": t.get("span"),
            "status": t.get("status"),
            "title": t.get("title"),
        })
    return {
        "appearsIn": appears_in(s.topics, alias),
        "coverage": topic_coverage(s, s.topics, alias),
        "generated": meta["generated"],
        "sections": [{k: v for k, v in x.items() if not k.startswith("_")}
                     for x in sorted(s.sections.get("sections") or [],
                                     key=lambda x: x.get("order") or 0)],
        "source": meta["source"],
        "topics": rows,
    }


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
    written.append(("data/vocab.json",
                    write(os.path.join(OUT, "vocab.json"), vocab_json(meta), 1)))
    written.append(("data/facets.json",
                    write(os.path.join(OUT, "facets.json"), facets_json(s, meta), 1)))

    nd = os.path.join(OUT, "nodes")
    if os.path.isdir(nd):
        for f in os.listdir(nd):
            os.remove(os.path.join(nd, f))
    files = node_files(s, ix)
    tot = 0
    for nid, rec in sorted(files.items()):
        tot += write(os.path.join(nd, nid + ".json"), rec, 0)
    written.append(("data/nodes/*.json (%d files)" % len(files), tot))

    alias = _alias()
    written.append(("data/topics.json",
                    write(os.path.join(OUT, "topics.json"), topics_json(s, meta, alias), 1)))
    td = os.path.join(OUT, "topics")
    if os.path.isdir(td):
        for f in os.listdir(td):
            os.remove(os.path.join(td, f))
    bd = topiclib.Board(s.board)
    tot = 0
    for t in s.topics:
        tot += write(os.path.join(td, t["id"] + ".json"), topic_record(s, bd, alias, t), 1)
    written.append(("data/topics/*.json (%d files)" % len(s.topics), tot))

    # phase 8: the Library and one page per source
    recs = source_pages.pages(s, s.reg, era_of)
    written.append(("data/sources.json",
                    write(os.path.join(OUT, "sources.json"), source_pages.library(recs, meta, s.reg), 0)))
    sd = os.path.join(OUT, "sources")
    if os.path.isdir(sd):
        for f in os.listdir(sd):
            os.remove(os.path.join(sd, f))
    tot = 0
    for sid, rec in sorted(recs.items()):
        tot += write(os.path.join(sd, sid + ".json"), rec, 0)
    written.append(("data/sources/*.json (%d files)" % len(recs), tot))

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

    drift += check_topics()

    # phase 8: the Library holds exactly the registry, and every source has its page
    reg = rd(os.path.join("research", "_sources.json"))["sources"]
    lib_path = os.path.join(OUT, "sources.json")
    lib = json.load(open(lib_path, encoding="utf-8")) if os.path.exists(lib_path) else {"sources": []}
    want_ids = sorted(x["id"] for x in reg)
    have_ids = [x["id"] for x in lib.get("sources") or []]
    if have_ids != want_ids or lib.get("count") != len(want_ids):
        drift.append("  sources.json holds %d rows (count %r), the registry %d"
                     % (len(have_ids), lib.get("count"), len(want_ids)))
    gone = [i for i in want_ids if not os.path.exists(os.path.join(OUT, "sources", i + ".json"))]
    if gone:
        drift.append("  %d source pages missing, e.g. %s" % (len(gone), ", ".join(gone[:5])))

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


def check_topics(index=None, node_dir=None):
    """Re-derive the topic files from research/topics/*.json, read afresh here and
    counted by this function's own loop: the index's rows and counts, one topic file
    per record whose `cites` are exactly the ids the record cites and resolve, and
    `absorbedBy` on exactly the domain nodes a topic absorbs. `index` and `node_dir`
    are the poison channels for --self-test."""
    drift = []
    tdir = os.path.join(ROOT, "research", "topics")
    raw = {}
    for f in sorted(os.listdir(tdir)):
        if f.endswith(".json") and not f.startswith("_"):
            with open(os.path.join(tdir, f), encoding="utf-8") as fh:
                t = json.load(fh)
            raw[t["id"]] = t

    def cited(t):
        ids = []
        for k in ("lead", "summary", "record", "claimed", "contested"):
            v = t.get(k)
            for it in ([v] if isinstance(v, dict) else (v or [])):
                for c in (it.get("cite") or []) if isinstance(it, dict) else []:
                    if c not in ids:
                        ids.append(c)
        return ids

    if index is None:
        p = os.path.join(OUT, "topics.json")
        if not os.path.exists(p):
            return ["  no app/public/data/topics.json -- build first"]
        index = json.load(open(p, encoding="utf-8"))
    rows = {r["id"]: r for r in index.get("topics") or []}
    if set(rows) != set(raw):
        drift.append("  topics.json rows %d, research/topics records %d (differ: %s)"
                     % (len(rows), len(raw), ", ".join(sorted(set(rows) ^ set(raw))[:5])))
    for tid, t in sorted(raw.items()):
        r = rows.get(tid)
        if r is None:
            continue
        want = {"cites": len(cited(t)), "members": len(t.get("members") or []),
                "questions": len(t.get("questions") or [])}
        for k in ("record", "claimed", "contested"):
            want[k] = len(t.get(k) or [])
        if r.get("counts") != want:
            drift.append("  topics.json %s counts %r, re-derived %r" % (tid, r.get("counts"), want))
        if list(r.get("related") or []) != list(t.get("related") or []):
            drift.append("  topics.json %s related differs from the record" % tid)
        for k in ("status", "section", "kind", "title"):
            if r.get(k) != t.get(k):
                drift.append("  topics.json %s %s %r, record %r" % (tid, k, r.get(k), t.get(k)))
        lead = t.get("lead")
        if r.get("lead") != (lead.get("text") if isinstance(lead, dict) else None):
            drift.append("  topics.json %s lead differs from the record" % tid)
        fp = os.path.join(OUT, "topics", tid + ".json")
        if not os.path.exists(fp):
            drift.append("  topic file topics/%s.json missing" % tid)
            continue
        rec = json.load(open(fp, encoding="utf-8"))
        cites = rec.get("cites") or {}
        if rec.get("id") != tid or sorted(cites) != sorted(cited(t)):
            drift.append("  topics/%s.json: id %r, %d cites where the record cites %d"
                         % (tid, rec.get("id"), len(cites), len(cited(t))))
        gone = sorted(k for k, v in cites.items() if not v or v.get("missing"))
        if gone:
            drift.append("  topics/%s.json: %d cited ids resolve to nothing (%s)"
                         % (tid, len(gone), ", ".join(gone[:3])))
    extra = sorted(f[:-5] for f in os.listdir(os.path.join(OUT, "topics"))
                   if f.endswith(".json") and f[:-5] not in raw) \
        if os.path.isdir(os.path.join(OUT, "topics")) else []
    if extra:
        drift.append("  topic files with no record: %s" % ", ".join(extra[:5]))

    # appearsIn (phase 6): the set of (node, topic, role) is the shipped topic
    # files' members, read here from those files; the order is anchors first,
    # then role in vocab order, then topic id, checked pair by pair.
    al = _alias()
    roles = [x["id"] for x in _vocab().get("topicRoles") or []]
    want_set = set()
    anchor = set()
    for tid, t in raw.items():
        fp = os.path.join(OUT, "topics", tid + ".json")
        if not os.path.exists(fp):
            continue
        for m in json.load(open(fp, encoding="utf-8")).get("members") or []:
            want_set.add((m.get("id"), tid, m.get("role")))
        for a in t.get("anchors") or []:
            anchor.add((al.get(a, a), tid))
    ai = index.get("appearsIn") or {}
    have_set = {(n, x[0], x[1]) for n, xs in ai.items() for x in xs}
    if have_set != want_set:
        diff = sorted(have_set ^ want_set)
        drift.append("  topics.json appearsIn differs from the topic members in %d places (%s)"
                     % (len(diff), ", ".join("/".join(map(str, d)) for d in diff[:3])))
    for n, xs in sorted(ai.items()):
        keys = [(0 if (n, x[0]) in anchor else 1,
                 roles.index(x[1]) if x[1] in roles else len(roles), x[0]) for x in xs]
        flags = [x[2] for x in xs]
        if keys != sorted(keys) or flags != [1 if (n, x[0]) in anchor else 0 for x in xs]:
            drift.append("  topics.json appearsIn[%s] is not primary topic first (%s)"
                         % (n, ", ".join(x[0] for x in xs[:4])))
            break

    nd = node_dir or os.path.join(OUT, "nodes")
    want_by = {i: tid for tid, t in raw.items() for i in (t.get("absorbs") or [])}
    for f in sorted(os.listdir(nd)):
        nid = f[:-5]
        with open(os.path.join(nd, f), encoding="utf-8") as fh:
            txt = fh.read()
        if nid not in want_by and '"absorbedBy"' not in txt:
            continue
        have = json.loads(txt).get("absorbedBy")
        if have != want_by.get(nid):
            drift.append("  nodes/%s.json absorbedBy %r, the records say %r"
                         % (nid, have, want_by.get(nid)))
    return drift


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

    # The topic files (phase 5): the real index must re-derive, and three poisons
    # must not: a count that moved, a row that went missing, and an absorbed domain
    # node whose file lost its absorbedBy.
    print("self-test: the topic files against the real records")
    if check_topics():
        print("  FAIL: check_topics rejects the unpoisoned build: %s" % check_topics()[0])
        return False
    print("  pass: accepted")
    real = json.load(open(os.path.join(OUT, "topics.json"), encoding="utf-8"))

    def bump(ix):
        ix["topics"][0]["counts"]["members"] += 1

    def drop(ix):
        ix["topics"].pop()

    def lose_topic(ix):
        # a node that appears in several topics loses one of them
        n = max(ix["appearsIn"], key=lambda k: len(ix["appearsIn"][k]))
        ix["appearsIn"][n].pop()

    def reorder(ix):
        # a node's primary topic moved to the end of its list
        n = next(k for k, v in sorted(ix["appearsIn"].items())
                 if len(v) > 2 and v[0][2] == 1 and v[-1][2] == 0)
        ix["appearsIn"][n].append(ix["appearsIn"][n].pop(0))
    for what, mangle in (("a member count that moved", bump), ("a missing row", drop),
                         ("a node's topic list with one topic lost", lose_topic),
                         ("a node's topic list with its primary topic moved last", reorder)):
        ix = json.loads(json.dumps(real))
        mangle(ix)
        got = check_topics(index=ix)
        print("self-test: the topic files against %s" % what)
        if not got:
            print("  FAIL: check_topics ACCEPTED %s.  The check is broken." % what)
            return False
        print("  pass: rejected (%s)" % got[0].strip()[:80])
    absorbed = sorted(i for t in topiclib.load_topics() for i in (t.get("absorbs") or []))
    tmp = tempfile.mkdtemp(prefix="app-topics-poison-")
    try:
        for k, i in enumerate(absorbed):
            rec = json.load(open(os.path.join(OUT, "nodes", i + ".json"), encoding="utf-8"))
            if k == 0:
                rec.pop("absorbedBy", None)
            with open(os.path.join(tmp, i + ".json"), "w", encoding="utf-8") as fh:
                json.dump(rec, fh)
        got = check_topics(node_dir=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("self-test: the topic files against a domain node file without absorbedBy")
    if not got or absorbed[0] not in got[0]:
        print("  FAIL: check_topics ACCEPTED %s without absorbedBy.  The check is broken."
              % absorbed[0])
        return False
    print("  pass: rejected (%s)" % got[0].strip()[:80])

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
