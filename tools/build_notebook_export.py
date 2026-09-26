#!/usr/bin/env python3
"""
build_notebook_export.py

Renders the whole evidence board as a set of Markdown files under exports/notebooklm/,
sized and shaped for Google NotebookLM. NotebookLM accepts Markdown sources of roughly
500,000 words each and does better with many topic sized prose sources than with one
enormous one, so the board is split into seventeen files that each stand on their own:
a read me, the eight authored threads, one file per era for the nodes that carry an
entity dossier, the people, the entities, the denials, the timeline, the patents, the FOIA queue, the
corrections the records forced, and the strongest connections.

THE ONE RULE OF THIS REPO, which this script obeys:
no invented sources, URLs, document numbers or quotes. Every sentence here either comes
out of the data files or is scaffolding that describes what the data says. Every claim
keeps its tier label (1 documented, 2 a named person on the record, 3 a stated inference)
and its source string exactly as stored. Every allegation shaped claim stays flagged as
an allegation. Nothing is summarised into a stronger form than the record supports.

Two mechanical normalisations are applied to stored text and are the only edits made:
em dashes become commas (or the word "to" between two numbers), because the export must
carry no em dashes, and runs of horizontal whitespace collapse to one space. No wording
is changed, added or removed.

Reads only: app/public/data/*.json, app/public/data/nodes/*.json, research/_corrections.json.
Never reads dist/ and never reads anything transcript shaped.

PHASE 11 STOPGAP (26 September 2026). Files 02 onward were one per band of the L0
programme map, read from app/public/data/map.json. The map retired and map.json is no
longer written, so the deep files are now the nodes that carry an entity dossier (the
argument for why a node is on this board), one file per era of index.json, and "below
the map" means without a dossier. Phase 12 rebuilds this export by topic.

Usage:
    python tools/build_notebook_export.py            write the files, print word counts
    python tools/build_notebook_export.py --check    report file list and word counts only,
                                                     exit 1 if any file exceeds the cap
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "app" / "public" / "data"
NODE_DIR = DATA / "nodes"
RESEARCH = ROOT / "research"
OUT_DIR = ROOT / "exports" / "notebooklm"

WORD_CAP = 450000

EM = "\u2014"
_EM_BETWEEN_DIGITS = re.compile(r"(?<=\d)\s*" + EM + r"\s*(?=\d)")
_MULTI_SPACE = re.compile(r"[ \t]{2,}")

ALLEGATION_WORDS = (
    "alleged", "allegedly", "allegation", "allegations", "purported", "purportedly",
    "reportedly", "unsupported", "unverified", "unsubstantiated", "rumour", "rumor",
    "claimed to", "said to have", "is said to",
)

CLAIM_TIER_LONG = {
    1: "Tier 1, documented, a primary record exists",
    2: "Tier 2, a named person on the record",
    3: "Tier 3, a stated inference with the reasoning given",
}
CLAIM_TIER_SHORT = {
    1: "Tier 1 documented",
    2: "Tier 2 named person on the record",
    3: "Tier 3 stated inference",
}
NODE_TIER_LONG = {
    "A": "board tier A, named in sworn testimony or primary documents as directly inside the programme",
    "B": "board tier B, documented channel and capability, programme role indicated but not yet nailed to a primary source",
    "C": "board tier C, contextual, real and relevant, no direct programme linkage on the record yet",
}
NODE_TIER_SHORT = {"A": "board tier A", "B": "board tier B", "C": "board tier C"}
NODE_TIER_RANK = {"A": 0, "B": 1, "C": 2}

BAND_FILE_NUMBERS = ["02", "03", "04", "05", "06", "07", "08"]   # one per era now, five used

ACRONYM_RE = re.compile(r"^(?P<long>[^()]{4,140}?)\s*\((?P<ab>[A-Z][A-Za-z0-9\-/\.&]{1,15})\)\s*$")


# ---------------------------------------------------------------- text helpers

def clean(value):
    """Normalise a stored string for the export: no em dashes, no double spaces."""
    if value is None:
        return ""
    if not isinstance(value, str):
        value = str(value)
    text = _EM_BETWEEN_DIGITS.sub(" to ", value)
    text = text.replace(" " + EM + " ", ", ")
    text = text.replace(EM + " ", ", ")
    text = text.replace(" " + EM, ", ")
    text = text.replace(EM, ", ")
    text = text.replace(" ,", ",")
    while ",," in text:
        text = text.replace(",,", ",")
    text = _MULTI_SPACE.sub(" ", text)
    return text.strip()


def words(text):
    return len(text.split())


def is_allegation(text):
    low = text.lower()
    return any(w in low for w in ALLEGATION_WORDS)


def claim_tier_label(tier, text):
    try:
        tier_int = int(tier)
    except (TypeError, ValueError):
        tier_int = None
    label = CLAIM_TIER_SHORT.get(tier_int, "tier not recorded")
    if is_allegation(text):
        label += ", allegation shaped wording as stored"
    return label


def mixed_tier_label(tier):
    """Timeline and some other records carry either a claim tier or a board tier."""
    if tier is None:
        return "no tier recorded"
    if isinstance(tier, str) and tier.upper() in NODE_TIER_SHORT:
        return NODE_TIER_SHORT[tier.upper()]
    try:
        return CLAIM_TIER_SHORT[int(tier)]
    except (TypeError, ValueError, KeyError):
        return "tier recorded as " + clean(str(tier))


def source_line(source):
    """Render a source exactly as stored, whatever shape it takes."""
    if source is None:
        return "no source string on file"
    if isinstance(source, str):
        return clean(source) or "no source string on file"
    if isinstance(source, dict):
        bits = []
        name = clean(source.get("name"))
        url = clean(source.get("url"))
        date = clean(source.get("date"))
        if name:
            bits.append(name)
        if url:
            bits.append(url)
        if date:
            bits.append("dated " + date)
        return ", ".join(bits) if bits else "no source string on file"
    return clean(str(source))


def sources_sentence(sources):
    if not sources:
        return "No source on file."
    return end_stop("Sources: " + "; ".join(source_line(s) for s in sources))


def end_stop(text):
    """Close a sentence built around a stored string without doubling its full stop."""
    text = clean(text)
    if not text:
        return ""
    if text[-1] in ".!?:;":
        return text
    last = text.split()[-1] if text.split() else ""
    if last.startswith("http"):
        return text
    return text + "."


def para(text):
    text = clean(text)
    return text + "\n\n" if text else ""


def date_span(start, end):
    start = clean(start)
    end = clean(end)
    if start and end and start != end:
        return start + " to " + end
    if start:
        return start
    if end:
        return "recorded end " + end
    return "no dates recorded"


# ---------------------------------------------------------------- data loading

class Board:
    def __init__(self):
        self.index = self._load(DATA / "index.json")
        self.threads = self._load(DATA / "threads.json")
        self.timeline = self._load(DATA / "timeline.json")
        self.patents = self._load(DATA / "patents.json")
        self.foia = self._load(DATA / "foia.json")
        self.analyst = self._load_optional(DATA / "analyst.json")
        self.corrections = self._load_optional(RESEARCH / "_corrections.json")
        self.idx = {n["id"]: n for n in self.index["nodes"]}
        self.counts = self.index.get("counts", {})
        self._node_cache = {}
        self.eras = self.index["eras"]
        self.era_order = {e["id"]: i for i, e in enumerate(self.eras)}
        # The deep set (phase 11 stopgap, see the module docstring): every node that
        # carries an entity dossier, in index order. It was the L0 map's nodes.
        self.deep = [n for n in self.index["nodes"]
                     if isinstance((self.node(n["id"]) or {}).get("dossier"), dict)]
        self.map_ids = {n["id"] for n in self.deep}
        # the deep files go one per era, in the index's era order
        self.bands = [{"id": "era-" + str(e["id"]), "era": e["id"], "label": e["label"]}
                      for e in self.eras]

    @staticmethod
    def _load(path):
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _load_optional(path):
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def node(self, node_id):
        if node_id not in self._node_cache:
            path = NODE_DIR / (str(node_id) + ".json")
            self._node_cache[node_id] = self._load(path) if path.exists() else None
        return self._node_cache[node_id]

    def label(self, node_id):
        rec = self.idx.get(node_id)
        if rec:
            return clean(rec.get("label") or node_id)
        node = self.node(node_id)
        if node:
            return clean(node.get("label") or node_id)
        return clean(node_id)

    def deg(self, node_id):
        rec = self.idx.get(node_id)
        return int(rec.get("deg") or 0) if rec else 0

    def tier(self, node_id):
        rec = self.idx.get(node_id)
        return (rec.get("tier") or "C") if rec else "C"

    def cls(self, node_id):
        rec = self.idx.get(node_id)
        return clean(rec.get("cls") or "") if rec else ""

    def build_stamp(self):
        for candidate in (self.analyst, self.index):
            if candidate and candidate.get("generated"):
                stamp = clean(candidate["generated"])
                src = clean(candidate.get("source") or "")
                commit = clean(self.index.get("sourceCommit") or "")
                extra = [x for x in (src, commit) if x]
                if extra:
                    return stamp + " (board source " + ", ".join(extra) + ")"
                return stamp
        return "not recorded in the data"

    def merged_claims(self, node):
        """Node claims plus dossier claims, deduplicated on tier and text."""
        seen = set()
        out = []
        pools = [node.get("claims") or []]
        dossier = node.get("dossier")
        if isinstance(dossier, dict):
            pools.append(dossier.get("claims") or [])
        for pool in pools:
            for c in pool:
                text = clean(c.get("text"))
                if not text:
                    continue
                key = (c.get("tier"), text)
                if key in seen:
                    continue
                seen.add(key)
                out.append({"tier": c.get("tier"), "text": text, "source": c.get("source")})
        return out

    def acronyms_for(self, labels):
        found = {}
        for lab in labels:
            m = ACRONYM_RE.match(lab.strip())
            if not m:
                continue
            ab = m.group("ab")
            long = clean(m.group("long"))
            if ab.upper() != ab or len(long) < 5:
                continue
            found.setdefault(ab, long)
        return sorted(found.items())


# ---------------------------------------------------------------- doc assembly

class Doc:
    def __init__(self, basename, header, sections):
        self.basename = basename
        self.header = header
        self.sections = [s for s in sections if s and s.strip()]

    def whole(self):
        return self.header + "".join(self.sections)

    def parts(self):
        """Return [(filename, text)], splitting on section boundaries if over the cap."""
        full = self.whole()
        if words(full) <= WORD_CAP:
            return [(self.basename + ".md", full.rstrip() + "\n")]
        chunks = []
        current = []
        current_words = words(self.header)
        for section in self.sections:
            sw = words(section)
            if current and current_words + sw > WORD_CAP:
                chunks.append(current)
                current = [section]
                current_words = words(self.header) + sw
            else:
                current.append(section)
                current_words += sw
        if current:
            chunks.append(current)
        out = []
        letters = "abcdefghijklmnopqrstuvwxyz"
        for i, chunk in enumerate(chunks):
            note = ("This is part " + str(i + 1) + " of " + str(len(chunks))
                    + " of this file. The file was split because a single NotebookLM source "
                      "has a word ceiling. Load every part.\n\n")
            out.append((self.basename + "-" + letters[i] + ".md",
                        self.header + note + "".join(chunk).rstrip() + "\n"))
        return out


# ---------------------------------------------------------------- renderers

def render_read_me(b):
    counts = b.counts
    claim_counts = counts.get("claims", {})
    t1 = claim_counts.get("1", 0)
    t2 = claim_counts.get("2", 0)
    t3 = claim_counts.get("3", 0)
    total_claims = t1 + t2 + t3

    demoted = 0
    for node_id in sorted(b.idx):
        node = b.node(node_id)
        if not node:
            continue
        for c in node.get("claims") or []:
            if "DEMOTED" in (c.get("source") or ""):
                demoted += 1

    head = "# Read me first: what this board is and how to read the rest of these files\n\n"
    head += ("This is a research board about an alleged legacy programme to recover and reverse "
             "engineer non human craft, and about the modern fight to force that record into the open. "
             "Everything in these files comes out of the board's own data, with every claim carrying "
             "the tier that says how strongly it is evidenced and the source string it rests on.\n\n")

    s = []
    s.append("## What the board holds\n\n"
             + para("The board carries " + str(counts.get("nodes", 0)) + " nodes: "
                    + str(counts.get("people", 0)) + " people and " + str(counts.get("entities", 0))
                    + " entities, which are institutions, programmes, documents, events, locations, "
                      "domains and pieces of legislation. Those nodes are joined by "
                    + str(counts.get("edges", 0)) + " hand written links and carry "
                    + str(total_claims) + " tiered claims between them. "
                    + str(counts.get("timeline", 0)) + " dated events sit on the timeline, "
                    + str(len(b.deep)) + " carry an entity dossier arguing why they are here, "
                    + str(counts.get("patents", 0)) + " patents are tracked in full prosecution detail, "
                    + str(counts.get("threads", 0)) + " authored threads walk a reader through the "
                      "strongest sequences, and " + str(counts.get("foia", {}).get("requests", 0))
                    + " Freedom of Information Act requests are drafted and waiting to be filed.")
             + para("Of the claims, " + str(t1) + " are Tier 1, " + str(t2) + " are Tier 2 and "
                    + str(t3) + " are Tier 3. That split is the point of the board. It is built so "
                      "that nobody can read it without knowing which parts rest on a primary record "
                      "and which parts rest on testimony or on inference."))

    s.append("## The claim tiers, in plain words\n\n"
             + para("Every claim on this board carries a number from 1 to 3. That number is about "
                    "evidence strength and nothing else.")
             + "- **" + CLAIM_TIER_LONG[1] + ".** A document exists and has been located. The source string names it.\n"
             + "- **" + CLAIM_TIER_LONG[2] + ".** Somebody with a name said it, in testimony, in an interview or in print. The claim is evidence that they said it.\n"
             + "- **" + CLAIM_TIER_LONG[3] + ".** The board is reasoning from what it holds. The reasoning is written into the claim rather than hidden.\n\n"
             + para("When a claim is worded as an allegation rather than as an established fact, these "
                    "files say so next to the tier. That flag is generated from the wording the board "
                    "already uses, words such as alleged, reportedly, purported, unsupported and unverified."))

    s.append("## The node tiers, which are not credibility\n\n"
             + para("Nodes carry a letter, A, B or C. This is the single most misread thing on the "
                    "board, so it is worth saying slowly: the letter measures proximity to the alleged "
                    "programme, not how credible the node is. A tier C node can be entirely real and "
                    "entirely well documented. It just sits further out.")
             + "- **Tier A.** Named in sworn testimony or primary documents as directly inside the programme.\n"
             + "- **Tier B.** Documented channel and capability, programme role indicated but not yet nailed to a primary source.\n"
             + "- **Tier C.** Contextual, real and relevant, with no direct programme linkage on the record yet.\n\n"
             + para("Tiers are assigned globally rather than by the researcher who worked that subject, "
                    "and a node with no sourced URL has its score cut hard, so nothing unsourced can "
                    "hold tier A. Each node carries a written rationale showing its rank and inputs, and "
                    "those rationales are reproduced in the era files."))

    s.append("## The three axes: C, A and D\n\n"
             + para("Each node also carries three scores from 0 to 3. They are never summed, because "
                    "collapsing them destroys the information: a contractor can sit at the centre of "
                    "the custody chain and be completely absent from the disclosure fight.")
             + "- **C, custody proximity.** How close is this entity to alleged possession of recovered material or craft?\n"
             + "- **A, access level.** What special access did it hold: special access program, unacknowledged special access program, or waived unacknowledged?\n"
             + "- **D, disclosure role.** How central is it to forcing the record into the open?\n\n"
             + para("So a node written as C3 A2 D0 is deep in the custody question, holds serious "
                    "access, and plays no part in disclosure. A node written as C0 A0 D3 is a "
                    "legislator or a journalist driving the whole fight with no programme access at all."))

    s.append("## Interested parties do not get to be their own best evidence\n\n"
             + para("The All-domain Anomaly Resolution Office, AARO, and the Department of Defense "
                    "publishing domains including defense.gov are treated on this board as interested "
                    "parties. A claim sourced to them caps at Tier 2 unless the claim is about what "
                    "they said. The reasoning is simple: publishing something on aaro.mil makes that "
                    "page a primary record of the statement, not a primary record of the fact asserted "
                    "in it. AARO reporting what AARO found is testimony from a party to the dispute.")
             + para("This is not a rhetorical stance, it is enforced in the data. " + str(demoted)
                    + " claims on this board carry a source string that records the demotion in writing, "
                      "usually with the phrase DEMOTED from Tier 1 followed by the reason and a note "
                      "that a primary replacement is still needed. Those strings are reproduced "
                      "unchanged in these files.")
             + para("The mirror of that rule is that denials are kept in full and sourced, treated as "
                    "artefacts of the concealment effort rather than as counterweights to it. A denial "
                    "is a dated, signed, attributable statement, which makes it evidence about the "
                    "denier. There is a whole file of them here."))

    era_lines = "".join("- **" + clean(e["label"]) + "**: " + clean(e.get("sub") or "") + "\n" for e in b.eras)
    s.append("## The dossiers, era by era\n\n"
             + para("The " + str(len(b.deep)) + " nodes that carry an entity dossier, the written "
                    "argument for why each is on this board, are taken one file per era, by the year "
                    "the node's record starts. Files 02 to " + BAND_FILE_NUMBERS[len(b.bands) - 1]
                    + " in this set are one per era.")
             + "The eras:\n\n" + era_lines + "\n")

    acr = b.acronyms_for([clean(n.get("label") or "") for n in b.index["nodes"]])
    if acr:
        lines = "".join("- **" + ab + "**: " + long + "\n" for ab, long in acr)
        s.append("## Names in full\n\n"
                 + para("These expansions are taken from the board's own node labels. Where a file "
                        "below uses a short form, the full name is here.")
                 + lines + "\n")

    s.append("## How to use these files\n\n"
             + para("Every file stands alone. File 01 walks the eight authored threads, which are the "
                    "best single starting point because they are the sequences the board considers "
                    "strongest. Files 02 to " + BAND_FILE_NUMBERS[len(b.bands) - 1] + " are the dossier "
                    "nodes era by era and hold the deepest prose, including for each node what it is, why it is implicated, why it holds the "
                    "tier it holds and what it has denied. Files 09 and 10 are the people and the "
                    "entities that carry no dossier. File 11 is the denials, file 12 the whole "
                    "timeline, file 13 the patents, file 14 the FOIA queue, file 15 the corrections "
                    "the records forced on the board, and file 16 the strongest connections in the "
                    "whole graph told as short stories.")
             + para("If you are listening rather than reading: file 15 is the honest one. It is where "
                    "the board records the places it was wrong and what the record actually said. Any "
                    "discussion of this material that skips it is doing the easy version.")
             + para("Two mechanical notes about the text. Em dashes in the stored data have been "
                    "rendered as commas, or as the word to when they sat between two numbers, and runs "
                    "of spaces have been collapsed. No wording has been changed, added or removed.")
             + para("Generated from board build " + b.build_stamp() + "."))

    return Doc("00-read-me-first", head, s)


def render_threads(b):
    head = "# The eight threads\n\n"
    head += ("A thread is an authored walk through the board: a short chain of nodes where each step "
             "is joined to the next by a link somebody wrote down and sourced. These are the sequences "
             "the board considers its strongest, and they are the best place to start.\n\n")
    s = []
    for t in b.threads["threads"]:
        body = "## " + clean(t.get("title") or t.get("label")) + "\n\n"
        body += para("Thread name on the board: " + clean(t.get("label")) + ".")
        body += para(clean(t.get("blurb")))
        steps = t.get("steps") or []
        for i, step in enumerate(steps):
            node_id = step.get("node")
            lab = b.label(node_id)
            year = step.get("year")
            meta = []
            if year:
                meta.append("year " + str(year))
            cls = b.cls(node_id)
            if cls:
                meta.append("a " + cls)
            meta.append(NODE_TIER_SHORT.get(b.tier(node_id), "board tier not recorded"))
            body += ("**Step " + str(i + 1) + ", " + lab + "** (" + ", ".join(meta) + "). "
                     + clean(step.get("evidence")) + "\n\n")
            edge = step.get("edge")
            if edge and i > 0:
                prev = b.label(steps[i - 1].get("node"))
                join = ("The join from " + prev + " to " + lab + " is a "
                        + clean(edge.get("type") or "link") + " link, recorded as "
                        + clean(edge.get("kind") or "direct") + ", at "
                        + CLAIM_TIER_SHORT.get(edge.get("tier"), "no tier recorded") + ".")
                via = edge.get("via") or []
                if via:
                    join += " It runs through " + ", ".join(b.label(v) for v in via) + "."
                body += para(join)
        s.append(body)
    return Doc("01-the-eight-threads", head, s)


def _node_block(b, node_id, claim_cap, conn_cap, include_dossier=True):
    node = b.node(node_id)
    if not node:
        return ""
    idx = b.idx.get(node_id, {})
    lab = clean(node.get("label") or node_id)
    out = "## " + lab + "\n\n"

    facts = []
    cls = clean(node.get("cls") or "")
    if cls:
        facts.append("a " + cls + " on the board")
    facts.append(NODE_TIER_LONG.get(node.get("tier"), "no board tier recorded"))
    facts.append("dates " + date_span(node.get("dateStart"), node.get("dateEnd")))
    facts.append("axes C" + str(node.get("C", 0)) + " A" + str(node.get("A", 0)) + " D" + str(node.get("D", 0)))
    facts.append(str(idx.get("deg", node.get("deg", 0))) + " connections")
    band = clean(node.get("band") or "")
    if band:
        facts.append("in the " + band + " band")
    out += para(end_stop(lab + " is " + "; ".join(facts)))

    sub = clean(node.get("sub") or "")
    if sub:
        out += para(end_stop("In one line: " + sub))

    dossier = node.get("dossier") if include_dossier else None
    if isinstance(dossier, dict):
        if dossier.get("whatItIs"):
            out += "### What it is\n\n" + para(dossier["whatItIs"])
        if dossier.get("whyImplicated"):
            out += "### Why it is implicated\n\n" + para(dossier["whyImplicated"])
        if dossier.get("narrative"):
            out += "### The longer account\n\n" + para(dossier["narrative"])
        if dossier.get("denialPosture"):
            out += "### What it has denied\n\n" + para(dossier["denialPosture"])
        roles = dossier.get("roles") or []
        if roles:
            out += para(end_stop("Roles the board assigns it: " + ", ".join(clean(r) for r in roles)))
        oq = dossier.get("openQuestions") or []
        if oq:
            out += "### Open questions on this node\n\n"
            for q in oq:
                out += "- " + clean(q) + "\n"
            out += "\n"
    else:
        desc = clean(node.get("desc") or "")
        if desc:
            out += "### What it is\n\n" + para(desc)
        narrative = clean(node.get("narrative") or "")
        if narrative:
            out += "### The longer account\n\n" + para(narrative)
        info = node.get("entityInfo")
        if isinstance(info, dict) and info.get("desc"):
            info_text = clean(info["desc"])
            if info_text and info_text != desc:
                out += "### The board's reading\n\n" + para(info_text)
        residual = clean(node.get("unexplainedResidual") or "")
        if residual:
            out += "### What is left unexplained\n\n" + para(residual)
        conflicts = node.get("conflicts") or []
        if conflicts:
            out += "### Where the record conflicts\n\n"
            for c in conflicts:
                out += "- " + clean(c) + "\n"
            out += "\n"
        unverified = node.get("unverified") or []
        if unverified:
            out += "### Recorded as unverified\n\n"
            for c in unverified:
                out += "- " + clean(c) + "\n"
            out += "\n"
        affiliations = node.get("affiliations") or []
        if affiliations:
            out += para(end_stop("Affiliations recorded: " + ", ".join(clean(a) for a in affiliations)))

    rationale = clean(node.get("tierRationale") or "")
    if rationale:
        out += "### Why it holds its tier\n\n" + para(rationale)

    claims = b.merged_claims(node)
    if claim_cap:
        wanted = [c for c in claims if c.get("tier") in (1, 2)] if claim_cap >= 20 else list(claims)
        if not wanted:
            wanted = list(claims)
        wanted = sorted(wanted, key=lambda c: (c.get("tier") if isinstance(c.get("tier"), int) else 9, c["text"]))
        shown = wanted[:claim_cap]
        if shown:
            out += "### The claims on the record\n\n"
            for c in shown:
                out += ("- **" + claim_tier_label(c.get("tier"), c["text"]) + ".** " + c["text"]
                        + " Source: " + source_line(c.get("source")) + "\n")
            out += "\n"
            if len(wanted) > len(shown):
                out += para("A further " + str(len(wanted) - len(shown)) + " claims sit on this node "
                            "on the board and are not reproduced here.")

    conns = node.get("connections") or []
    if conn_cap and conns:
        ranked = sorted(
            conns,
            key=lambda c: (
                c.get("claimTier") if isinstance(c.get("claimTier"), int) else 9,
                NODE_TIER_RANK.get(c.get("tier"), 3),
                -b.deg(c.get("id")),
                clean(c.get("id")),
            ),
        )[:conn_cap]
        out += "### Its strongest connections\n\n"
        for c in ranked:
            other = clean(c.get("label") or c.get("id"))
            direction = "runs out to" if c.get("direction") == "out" else "comes in from"
            line = ("- " + lab + " " + direction + " **" + other + "** ("
                    + clean(c.get("cls") or "node") + ", "
                    + NODE_TIER_SHORT.get(c.get("tier"), "no board tier") + "), a "
                    + clean(c.get("type") or "link") + " link at "
                    + CLAIM_TIER_SHORT.get(c.get("claimTier"), "no tier recorded") + ". ")
            edge_label = clean(c.get("edgeLabel") or "")
            if edge_label:
                line += end_stop("The link reads: " + edge_label) + " "
            note = clean(c.get("note") or "")
            if note:
                line += note + " "
            line += sources_sentence(c.get("sources"))
            out += line.rstrip() + "\n"
        out += "\n"
        if len(conns) > conn_cap:
            out += para("It carries " + str(len(conns)) + " connections in total on the board.")

    return out


def render_band(b, band, number):
    # One era of the dossier nodes (phase 11 stopgap; this was one band of the map).
    band_id = band["id"]
    band_label = clean(band["label"])
    nodes = [n for n in b.deep if n.get("era") == band["era"]]
    nodes.sort(key=lambda n: (b.era_order.get(n.get("era"), 99), -b.deg(n["id"]), n["id"]))

    head = "# The dossiers: " + band_label + "\n\n"
    head += ("The board carries an entity dossier on " + str(len(b.deep)) + " nodes, and this file "
             "is the " + str(len(nodes)) + " whose record starts in " + band_label + ", most connected "
             "first. Each entry gives what the node is, why the board places it here, why it holds the tier it "
             "holds, what it has denied, its documented and testimonial claims with their sources, and "
             "the links that tie it to the rest of the board.\n\n")

    acr = b.acronyms_for([clean(n.get("label") or "") for n in nodes])
    if acr:
        head += "Names in full, for this file:\n\n"
        head += "".join("- **" + ab + "**: " + long + "\n" for ab, long in acr)
        head += "\n"

    s = []
    current_era = None
    for n in nodes:
        era_id = n.get("era")
        if era_id != current_era:
            current_era = era_id
            era = next((e for e in b.eras if e["id"] == era_id), None)
            if era:
                s.append("# " + clean(era["label"]) + ": " + clean(era.get("sub") or "") + "\n\n")
            else:
                s.append("# Era not recorded\n\n")
        s.append(_node_block(b, n["id"], claim_cap=25, conn_cap=15, include_dossier=True))
    return Doc(number + "-" + band_id, head, s)


def render_people(b):
    people = [n for n in b.index["nodes"]
              if n.get("cls") == "person" and n["id"] not in b.map_ids]
    people.sort(key=lambda n: (-int(n.get("deg") or 0), n["id"]))
    top = people[:120]
    head = "# The people\n\n"
    head += ("None of the " + str(len(b.deep)) + " nodes that carry an entity dossier is a person, so "
             "every one of the board's " + str(b.counts.get("people", 0)) + " people is here: "
             "witnesses, officials, legislators, contractors, scientists and journalists. This file "
             "takes the " + str(len(top)) + " with the most connections, most connected first, and "
             "gives what the board records about each of them and up to eight of their claims.\n\n")
    s = []
    for rec in top:
        s.append(_node_block(b, rec["id"], claim_cap=8, conn_cap=6, include_dossier=False))
    return Doc("09-the-people", head, s)


def render_entities(b):
    ents = [n for n in b.index["nodes"]
            if n.get("cls") != "person" and n["id"] not in b.map_ids]
    ents.sort(key=lambda n: (-int(n.get("deg") or 0), n["id"]))
    top = ents[:120]
    head = "# The entities below the floor\n\n"
    head += ("Beside the dossier nodes sit the institutions, programmes, documents, events, locations "
             "and statutes that the board holds but has written no dossier for. This file takes "
             "the " + str(len(top)) + " most connected of them, most connected first, with what the "
             "board records about each and up to eight of their claims.\n\n")
    s = []
    for rec in top:
        s.append(_node_block(b, rec["id"], claim_cap=8, conn_cap=6, include_dossier=False))
    return Doc("10-the-entities-below-the-floor", head, s)


def render_denials(b):
    seen = {}
    postures = {}
    for node_id in sorted(b.idx):
        node = b.node(node_id)
        if not node:
            continue
        dossier = node.get("dossier")
        if isinstance(dossier, dict) and dossier.get("denialPosture"):
            postures[node_id] = clean(dossier["denialPosture"])
        for d in node.get("denials") or []:
            by = d.get("by") or {}
            of = d.get("of") or {}
            if by:
                key = (by.get("id"), of.get("id"), clean(d.get("label")))
            else:
                # no adjudicated denier (phase 3): keyed on both ends, grouped
                # under None, and never given a direction
                ends = tuple(sorted(((d.get("a") or {}).get("id") or "",
                                     (d.get("b") or {}).get("id") or "")))
                key = (None, ends, clean(d.get("label")))
            seen.setdefault(key, d)

    by_denier = {}
    for key, d in seen.items():
        by_denier.setdefault(key[0], []).append(d)

    head = "# The denials\n\n"
    head += ("This board records official denials in full and sourced, treated as artefacts of the "
             "concealment effort rather than as counterweights to it, because a denial is a dated, "
             "signed, attributable statement and that makes it evidence about the denier. There are "
             + str(len(seen)) + " distinct denials here, from " + str(len(by_denier))
             + " deniers, grouped by who did the denying.\n\n")

    s = []
    for denier_id in sorted(by_denier, key=lambda x: b.label(x or "")):
        group = sorted(by_denier[denier_id],
                       key=lambda d: (clean((d.get("of") or {}).get("id")), clean(d.get("label"))))
        if denier_id is None:
            block = "## Denials whose direction is not adjudicated\n\n"
            block += para(str(len(group)) + (" denial" if len(group) == 1 else " denials")
                          + " on this board name no denier in the adjudication, so no direction "
                          "is given for them here. Each is listed by its two ends.")
            for d in group:
                a, b_ = d.get("a") or {}, d.get("b") or {}
                block += ("- **" + clean(d.get("label")) + "** Between "
                          + clean(a.get("label") or a.get("id")) + " and "
                          + clean(b_.get("label") or b_.get("id")) + ", recorded as a "
                          + clean(d.get("denialKind") or "not yet adjudicated") + " denial link at "
                          + CLAIM_TIER_SHORT.get(d.get("claimTier"), "no tier recorded") + ". ")
                note = clean(d.get("note") or "")
                if note:
                    block += note + " "
                block += sources_sentence(d.get("sources")).rstrip() + "\n"
            s.append(block + "\n")
            continue
        block = "## " + b.label(denier_id) + "\n\n"
        block += para(b.label(denier_id) + " is recorded as the denying party in " + str(len(group))
                      + (" denial" if len(group) == 1 else " denials") + " on this board.")
        posture = postures.get(denier_id)
        if posture:
            block += "### Its stated denial posture\n\n" + para(posture)
        for d in group:
            of = d.get("of") or {}
            block += ("- **Denies: " + clean(d.get("label")) + "** This is directed at "
                      + clean(of.get("label") or of.get("id")) + ", recorded as a "
                      + clean(d.get("denialKind") or "denial") + " denial at "
                      + CLAIM_TIER_SHORT.get(d.get("claimTier"), "no tier recorded") + ". ")
            note = clean(d.get("note") or "")
            if note:
                block += note + " "
            block += sources_sentence(d.get("sources")).rstrip() + "\n"
        block += "\n"
        s.append(block)
    return Doc("11-denials", head, s)


def render_timeline(b):
    events = b.timeline
    head = "# The timeline\n\n"
    head += ("Every dated event on the board, " + str(len(events)) + " of them, grouped by the era the "
             "board assigns and then by year. Each line gives the date, what happened, the node it "
             "hangs on, the strand of the story it belongs to and the tier it carries.\n\n")
    head += ("A note on tiers in this file: timeline entries carry either a claim tier, 1 to 3, or a "
             "board tier, A to C, depending on how the entry was written. Both are reproduced as "
             "stored and labelled for what they are.\n\n")

    groups = {}
    for e in events:
        groups.setdefault(e.get("era"), []).append(e)

    ordered_eras = [e["id"] for e in b.eras if e["id"] in groups]
    ordered_eras += sorted(str(k) for k in groups if k not in ordered_eras)

    s = []
    for era_id in ordered_eras:
        if era_id not in groups:
            continue
        era = next((e for e in b.eras if e["id"] == era_id), None)
        title = clean(era["label"]) if era else "Era not recorded"
        sub = clean(era.get("sub") or "") if era else ""
        block = "## " + title + (": " + sub + "\n\n" if sub else "\n\n")
        items = sorted(groups[era_id], key=lambda e: (clean(e.get("date")), clean(e.get("id"))))
        block += para(str(len(items)) + " events sit in this era.")
        current_year = None
        for e in items:
            date = clean(e.get("date"))
            year = date[:4] if date else "no year"
            if year != current_year:
                current_year = year
                block += "### " + year + "\n\n"
            node_id = e.get("node")
            node_bit = (end_stop("On the node " + b.label(node_id)) + " ") if node_id else "No node attached. "
            block += ("- **" + date + ", " + clean(e.get("label")) + ".** " + clean(e.get("text"))
                      + " " + node_bit + "Strand: " + clean(e.get("strand") or "not recorded")
                      + ". Recorded at " + mixed_tier_label(e.get("grade") or e.get("claimTier")) + ".\n")
        block += "\n"
        s.append(block)
    return Doc("12-timeline", head, s)


def render_patents(b):
    p = b.patents
    pats = p.get("patents") or []
    head = "# The patents\n\n"
    head += ("The board tracks " + str(len(pats)) + " United States patent filings in full prosecution "
             "detail, which makes them the most completely documented objects on the whole board: "
             "every one is a federal record with dates, an application number, a docket and a file "
             "wrapper. " + clean(p.get("eyebrow") or "") + ".\n\n")
    head += ("Where a field below says it is left empty in the patent data, that is exactly what the "
             "board holds: the field exists and carries no value, and nothing has been filled in for it "
             "here.\n\n")

    s = []
    for pat in sorted(pats, key=lambda x: clean(x.get("number"))):
        block = "## " + clean(pat.get("number")) + ", " + clean(pat.get("title")) + "\n\n"
        block += para(clean(pat.get("sub") or ""))
        facts = []
        facts.append("application " + (clean(pat.get("application")) or "not recorded"))
        facts.append("docket " + (clean(pat.get("docket")) or "not recorded"))
        facts.append("filed " + (clean(pat.get("filed")) or "not recorded"))
        facts.append("granted " + (clean(pat.get("granted")) or "not recorded"))
        pub = clean(pat.get("published"))
        facts.append("published " + pub if pub else "no separate publication date recorded")
        facts.append("examiner " + (clean(pat.get("examiner")) or "left empty in the patent data"))
        facts.append("supervising examiner " + (clean(pat.get("supervisor")) or "left empty in the patent data"))
        units = pat.get("artUnits") or []
        facts.append("art unit " + (", ".join(clean(u) for u in units) if units else "not recorded"))
        facts.append("inventor field " + (clean(pat.get("inventor")) or "left empty in the patent data"))
        facts.append("assignee field " + (clean(pat.get("assignee")) or "left empty in the patent data"))
        status = pat.get("status") or []
        facts.append("status " + (", ".join(clean(x) for x in status) if status else "not recorded"))
        expired = clean(pat.get("expired"))
        if expired:
            facts.append("expired " + expired)
        block += para("The record: " + "; ".join(facts) + ".")
        block += para(end_stop("Source for the file data: " + source_line(pat.get("source"))))

        fee = pat.get("fee")
        if isinstance(fee, dict):
            bits = []
            if fee.get("title"):
                bits.append(clean(fee["title"]))
            if fee.get("lapsed"):
                bits.append("lapsed " + clean(fee["lapsed"]))
            if fee.get("finding"):
                bits.append("recorded against the finding named " + clean(fee["finding"]))
            if bits:
                block += "### Fee status\n\n" + para(end_stop("; ".join(bits)))

        pros = pat.get("prosecution") or []
        if pros:
            block += "### Prosecution history\n\n"
            for step in pros:
                line = "- **" + clean(step.get("date")) + ", " + clean(step.get("label")) + ".**"
                note = clean(step.get("note") or "")
                if note:
                    line += " " + note
                kind = clean(step.get("kind") or "")
                if kind and kind != "plain":
                    line += " Recorded as a " + kind + " step."
                f = clean(step.get("file") or "")
                if f:
                    line += " File on record: " + f + "."
                block += line + "\n"
            block += "\n"

        absent = pat.get("absent") or []
        if absent:
            block += "### Documents not obtained\n\n"
            for a in absent:
                block += "- **" + clean(a.get("label")) + ".** " + clean(a.get("why")) + "\n"
            block += "\n"

        sheets = pat.get("sheets") or []
        if sheets:
            block += para(str(len(sheets)) + " drawing sheets are held for this patent, captioned "
                          + end_stop("; ".join(clean(sh.get("caption")) for sh in sheets)))

        node_id = pat.get("node")
        if node_id:
            block += "### The board nodes linked to it\n\n"
            block += para("On the board this patent is the node " + b.label(node_id) + ", "
                          + NODE_TIER_LONG.get(b.tier(node_id), "no board tier recorded") + ", with "
                          + str(b.deg(node_id)) + " connections.")
            node = b.node(node_id)
            if node:
                for c in sorted(node.get("connections") or [],
                                key=lambda c: (c.get("claimTier") if isinstance(c.get("claimTier"), int) else 9,
                                               NODE_TIER_RANK.get(c.get("tier"), 3),
                                               clean(c.get("id")))):
                    line = ("- **" + clean(c.get("label") or c.get("id")) + "** ("
                            + clean(c.get("cls") or "node") + ", "
                            + NODE_TIER_SHORT.get(c.get("tier"), "no board tier") + "), a "
                            + clean(c.get("type") or "link") + " link at "
                            + CLAIM_TIER_SHORT.get(c.get("claimTier"), "no tier recorded") + ". ")
                    if clean(c.get("edgeLabel")):
                        line += end_stop("The link reads: " + clean(c.get("edgeLabel"))) + " "
                    if clean(c.get("note")):
                        line += clean(c.get("note")) + " "
                    line += sources_sentence(c.get("sources"))
                    block += line.rstrip() + "\n"
                block += "\n"
                claims = b.merged_claims(node)
                if claims:
                    block += "### The claims on that node\n\n"
                    ordered = sorted(claims, key=lambda c: (c.get("tier") if isinstance(c.get("tier"), int) else 9, c["text"]))
                    for c in ordered[:25]:
                        block += ("- **" + claim_tier_label(c.get("tier"), c["text"]) + ".** " + c["text"]
                                  + " Source: " + source_line(c.get("source")) + "\n")
                    block += "\n"
        s.append(block)

    comp = p.get("comparison")
    if isinstance(comp, dict):
        block = "## " + clean(comp.get("title")) + "\n\n"
        block += para(clean(comp.get("standfirst") or ""))
        block += para("The board's finding, at " + CLAIM_TIER_SHORT.get(comp.get("tier"), "no tier recorded")
                      + ": " + clean(comp.get("finding") or ""))
        for lane in comp.get("lanes") or []:
            block += "### " + clean(lane.get("label") or "lane") + "\n\n"
            block += para(clean(lane.get("summary") or ""))
            for ev in lane.get("events") or []:
                if isinstance(ev, dict):
                    line = "- " + clean(ev.get("date") or "") + ", " + clean(ev.get("label") or "")
                    if clean(ev.get("note")):
                        line += ". " + clean(ev.get("note"))
                    block += line + "\n"
            block += "\n"
        s.append(block)

    findings = p.get("findings") or []
    if findings:
        block = "## The findings on the filings\n\n"
        for f in sorted(findings, key=lambda x: clean(x.get("id"))):
            block += "### " + clean(f.get("title")) + "\n\n"
            block += para("At " + CLAIM_TIER_SHORT.get(f.get("tier"), "no tier recorded") + ". "
                          + clean(f.get("text") or ""))
            if f.get("coda"):
                block += para(clean(f["coda"]))
            block += para(end_stop("Source: " + source_line(f.get("source"))))
        s.append(block)

    oq = p.get("openQuestions") or []
    if oq:
        block = "## What is still open on the patents\n\n"
        for q in oq:
            block += "- " + (clean(q.get("text")) if isinstance(q, dict) else clean(q)) + "\n"
        block += "\n"
        s.append(block)

    return Doc("13-patents", head, s)


def render_foia(b):
    f = b.foia
    reqs = f.get("requests") or []
    pairs = sum(len(n.get("questions") or []) for r in reqs for n in r.get("nodes") or [])
    head = "# The FOIA queue\n\n"
    head += ("The board carries " + str(len(reqs)) + " drafted Freedom of Information Act requests, "
             "each aimed at a specific agency and built out of the open questions already sitting on "
             "the nodes it covers, " + str(pairs) + " node and question pairings in all. "
             + clean(f.get("status") or "") + "\n\n")
    head += ("A question below is reproduced from the open questions recorded on the node the request "
             "names. Nothing here is a new question written for the export.\n\n")

    s = []
    for r in sorted(reqs, key=lambda x: clean(x.get("id"))):
        block = "## " + clean(r.get("id")) + ", " + clean(r.get("title")) + "\n\n"
        block += para(end_stop("Agency: " + (clean(r.get("agency")) or "not recorded") + ". Status: "
                               + (clean(r.get("status")) or "not recorded")))
        block += para(end_stop("Where it goes: " + (clean(r.get("sendTo")) or "not recorded")))
        node_entries = sorted(r.get("nodes") or [], key=lambda n: clean(n.get("node")))
        block += para("It covers " + str(len(node_entries))
                      + (" node" if len(node_entries) == 1 else " nodes") + " on the board: "
                      + end_stop(", ".join(b.label(n.get("node")) for n in node_entries)))
        for entry in node_entries:
            node_id = entry.get("node")
            node = b.node(node_id)
            oq = []
            if node and isinstance(node.get("dossier"), dict):
                oq = node["dossier"].get("openQuestions") or []
            block += "### " + b.label(node_id) + "\n\n"
            asked = [i for i in entry.get("questions") or [] if i < len(oq)]
            partial = [i for i in entry.get("partial") or [] if i < len(oq)]
            if asked:
                block += "What this request asks, taken from the open questions on that node:\n\n"
                for i in asked:
                    block += "- " + clean(oq[i]) + "\n"
                block += "\n"
            if partial:
                block += "Questions this request would only partly answer:\n\n"
                for i in partial:
                    block += "- " + clean(oq[i]) + "\n"
                block += "\n"
            if not asked and not partial:
                block += para("No open question text is recorded on this node for this request.")
        s.append(block)

    letters = clean(f.get("letters") or "")
    if letters:
        s.append(para("The drafted letters themselves live in the repository at " + letters + "."))
    return Doc("14-foia", head, s)


def render_corrections(b):
    c = b.corrections
    head = "# What the records corrected\n\n"
    if not c:
        return Doc("15-what-the-records-corrected",
                   head + "No corrections file was found in the repository.\n\n", [])

    head += ("This is the file that keeps the rest honest. It is the board's own record of the places "
             "where the research was wrong, thin or malformed, and what the documents actually said "
             "when somebody went and checked. Read against the confident prose in the other files, "
             "this is the correction the material deserves.\n\n")
    head += ("One thing to be clear about, because the export will not pretend otherwise: the "
             "corrections file stores the corrected value and the reasoning for it. In most cases it "
             "does not store the superseded wording, so these entries say what the record now says and "
             "why, rather than quoting what the board used to say. Where the file does carry the "
             "replaced sentence, it is quoted here in full and marked as the replaced text.\n\n")

    s = []
    why_keys = sorted(k for k, v in c.items() if k.startswith("_") and isinstance(v, str) and k != "_what")
    if why_keys:
        block = "## The reasoning, in the board's own words\n\n"
        block += para("Each of these is the written justification for one pass of corrections. They "
                      "are reproduced whole because the reasoning is the evidence.")
        for k in why_keys:
            block += "### " + k.strip("_").replace("_", " ") + "\n\n" + para(c[k])
        s.append(block)

    for section in ("people", "entities", "edges", "timeline"):
        items = c.get(section) or []
        if not items:
            continue
        block = "## Corrections to the " + section + "\n\n"
        block += para(str(len(items)) + " records in the " + section + " set were changed by what the "
                      "documents said.")
        for item in sorted(items, key=lambda x: clean(x.get("id")) if isinstance(x, dict) else clean(str(x))):
            if not isinstance(item, dict):
                continue
            block += "### " + b.label(item.get("id")) + "\n\n"
            changed = sorted(k for k in item if k not in ("id", "_replacement"))
            block += para("Fields the record forced a change to: " + ", ".join(changed) + ".")
            if "_replacement" in item:
                block += para(end_stop("The board once carried a sentence that the record replaced. The "
                                       "corrections file states: " + clean(item["_replacement"])))
            if item.get("date"):
                block += para("Its date is now set to " + clean(item["date"])
                              + ", derived from the record rather than assigned.")
            if item.get("label"):
                block += para(end_stop("Its label now reads: " + clean(item["label"])))
            if item.get("sub"):
                block += para(end_stop("Its one line summary now reads: " + clean(item["sub"])))
            if item.get("desc"):
                block += para(end_stop("Its description now reads: " + clean(item["desc"])))
            for chain_key, chain_name in (("sequenceChain", "sequence chain"), ("chronology", "chronology")):
                chain = item.get(chain_key) or []
                if chain:
                    block += "The rebuilt " + chain_name + ":\n\n"
                    for step in chain:
                        line = "- " + clean(step.get("date")) + ", " + end_stop(clean(step.get("event")))
                        if step.get("isAnomalous"):
                            line += " The board marks this step as the anomalous one."
                        src = step.get("source")
                        line += " Source: " + end_stop(source_line(src) if src else "no attributed source on file")
                        block += line + "\n"
                    block += "\n"
            affiliations = item.get("affiliations") or []
            if affiliations:
                block += para("Affiliations rewritten as prose rather than as raw identifiers: "
                              + end_stop(", ".join(clean(a) for a in affiliations)))
            claims = item.get("claims") or []
            if claims:
                block += "Claims the record added:\n\n"
                for cl in claims:
                    text = clean(cl.get("text"))
                    block += ("- **" + claim_tier_label(cl.get("tier"), text) + ".** " + text
                              + " Source: " + source_line(cl.get("source")) + "\n")
                block += "\n"
            removed = item.get("removeClaims") or []
            if removed:
                block += "Claims the record removed:\n\n"
                for cl in removed:
                    block += "- " + (clean(cl.get("text")) if isinstance(cl, dict) else clean(cl)) + "\n"
                block += "\n"
            srcs = item.get("sources") or []
            if srcs:
                block += para(end_stop("Sources added to it: " + "; ".join(source_line(x) for x in srcs)))
        s.append(block)

    gaps = c.get("gaps") or []
    if gaps:
        block = "## What is still missing\n\n"
        block += para("The corrections pass also wrote down what it could not settle. These are open "
                      "gaps, recorded rather than papered over.")
        for g in gaps:
            block += "- " + (clean(g.get("text")) if isinstance(g, dict) else clean(g)) + "\n"
        block += "\n"
        s.append(block)

    return Doc("15-what-the-records-corrected", head, s)


def render_strongest(b):
    pairs = {}
    for node_id in sorted(b.idx):
        node = b.node(node_id)
        if not node:
            continue
        for c in node.get("connections") or []:
            other = c.get("id")
            if not other:
                continue
            key = tuple(sorted((node_id, other)))
            existing = pairs.get(key)
            ct = c.get("claimTier") if isinstance(c.get("claimTier"), int) else 9
            if existing is None or ct < existing[0]:
                pairs[key] = (ct, node_id, c)

    scored = []
    for key, (ct, from_id, c) in pairs.items():
        a, bb = key
        score = (
            ct,
            NODE_TIER_RANK.get(b.tier(a), 3) + NODE_TIER_RANK.get(b.tier(bb), 3),
            -(b.deg(a) + b.deg(bb)),
            a,
            bb,
        )
        scored.append((score, from_id, c))
    scored.sort(key=lambda x: x[0])
    top = scored[:100]

    head = "# The strongest connections on the board\n\n"
    head += ("The board holds " + str(b.counts.get("edges", 0)) + " hand written links between its "
             "nodes. These are the hundred that combine the best evidenced link tier with the two "
             "best placed and most connected nodes at either end, each told as a short paragraph with "
             "the note somebody wrote when they made the link and the sources it rests on.\n\n")

    s = []
    for i, (score, from_id, c) in enumerate(top):
        to_id = c.get("id")
        other_label = clean(c.get("label") or to_id)
        block = "## " + str(i + 1) + ". " + b.label(from_id) + " and " + other_label + "\n\n"
        line = (b.label(from_id) + " (" + (b.cls(from_id) or "node") + ", "
                + NODE_TIER_SHORT.get(b.tier(from_id), "no board tier") + ", "
                + str(b.deg(from_id)) + " connections) is joined to " + other_label + " ("
                + clean(c.get("cls") or "node") + ", "
                + NODE_TIER_SHORT.get(c.get("tier"), "no board tier") + ", "
                + str(b.deg(to_id)) + " connections) by a " + clean(c.get("type") or "link")
                + " link recorded at " + CLAIM_TIER_SHORT.get(c.get("claimTier"), "no tier recorded") + ". ")
        edge_label = clean(c.get("edgeLabel") or "")
        if edge_label:
            line += end_stop("The link is labelled: " + edge_label) + " "
        dates = date_span(c.get("dateStart"), c.get("dateEnd"))
        if dates != "no dates recorded":
            line += "It is dated " + dates + ". "
        block += para(line)
        note = clean(c.get("note") or "")
        if note:
            block += para(note)
        block += para(sources_sentence(c.get("sources")))
        s.append(block)
    return Doc("16-strongest-connections", head, s)


README_TEXT = """# NotebookLM export

Generated files. Do not edit them by hand: they are rebuilt from the board's data every
time the script runs, and any edit made here is lost on the next rebuild.

## What is in here

- `00-read-me-first.md` what the board is, the tiers, the axes, how to read the rest
- `01-the-eight-threads.md` the eight authored threads, step by step
- `02` onward, the nodes that carry an entity dossier, one file per era
- `09-the-people.md` and `10-the-entities-below-the-floor.md` the most connected nodes without a dossier
- `11-denials.md` every denial, grouped by who denied it
- `12-timeline.md` every dated event, by era and year
- `13-patents.md` the five patents in full prosecution detail
- `14-foia.md` the drafted FOIA requests and the questions behind them
- `15-what-the-records-corrected.md` where the board was wrong and what the record said
- `16-strongest-connections.md` the hundred strongest links, told as short stories

## Regenerate after every board rebuild

```powershell
cd "C:\\Users\\stewa\\ClaudeProjects\\Missing individuals connected to defense contractors\\the-program"
python tools/build_notebook_export.py
python tools/build_notebook_export.py --check
```

## Load them into NotebookLM

1. Go to notebooklm.google.com and click Create new notebook.
2. Click Add source, then Upload.
3. Multi select every numbered `.md` file in this folder. Skip this README.
4. Wait for them all to finish processing, then open Audio Overview and click Customize.

## Audio Overview customize prompt

```
Take the angle that the recovery programme is real and the denials are the cover story, and
tell it that way for entertainment. Two hard rules you never break. First, whenever you lean
on a claim, say its tier out loud: Tier 1 documented, Tier 2 a named person on the record,
Tier 3 a stated inference. Say a node's board tier, A, B or C, as proximity to the programme
rather than as credibility. Second, never invent a document number, a date, a quote or a
source. If the sources do not carry it, say the record does not carry it. Anything the files
label as an allegation stays an allegation out loud. Spend real time on the corrections file:
the places the board got it wrong are the most interesting part of the story.
```
"""


# ---------------------------------------------------------------- main

def build_all(b):
    docs = [render_read_me(b), render_threads(b)]
    for number, band in zip(BAND_FILE_NUMBERS, b.bands):
        docs.append(render_band(b, band, number))
    docs.append(render_people(b))
    docs.append(render_entities(b))
    docs.append(render_denials(b))
    docs.append(render_timeline(b))
    docs.append(render_patents(b))
    docs.append(render_foia(b))
    docs.append(render_corrections(b))
    docs.append(render_strongest(b))
    files = []
    for doc in docs:
        files.extend(doc.parts())
    return files


def main():
    ap = argparse.ArgumentParser(
        description="Render the evidence board as NotebookLM Markdown sources.")
    ap.add_argument("--check", action="store_true",
                    help="report the file list and word counts only, exit 1 if any file exceeds the cap")
    args = ap.parse_args()

    board = Board()
    files = build_all(board)

    for name, text in files:
        if EM in text:
            print("ERROR: an em dash survived in " + name, file=sys.stderr)
            return 2

    over = [(n, words(t)) for n, t in files if words(t) > WORD_CAP]

    if not args.check:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for name, text in files:
            (OUT_DIR / name).write_text(text, encoding="utf-8", newline="\n")
        (OUT_DIR / "README.md").write_text(README_TEXT, encoding="utf-8", newline="\n")
        # A numbered file this run did not write is an orphan from an earlier run,
        # left behind when the band order changed and the numbers moved: six of them
        # sat in the export beside their replacements, so a notebook loaded from
        # the folder read two different band files under one number. Remove them.
        written = {name for name, _ in files}
        for stale in sorted(OUT_DIR.glob("[0-9][0-9]-*.md")):
            if stale.name not in written:
                stale.unlink()
                print("  removed stale " + stale.name)

    total_words = 0
    total_chars = 0
    print(("CHECK " if args.check else "WROTE ") + str(len(files)) + " files in " + OUT_DIR.as_posix())
    for name, text in files:
        w = words(text)
        total_words += w
        total_chars += len(text)
        flag = "  OVER CAP" if w > WORD_CAP else ""
        print("  " + name.ljust(42) + str(w).rjust(9) + " words" + flag)
    print("  " + "TOTAL".ljust(42) + str(total_words).rjust(9) + " words, "
          + str(round(total_chars / 1024 / 1024, 2)) + " MB")
    print("  word cap per file: " + str(WORD_CAP))

    if over:
        print("FAIL: " + str(len(over)) + " file(s) exceed the word cap.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
