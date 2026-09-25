#!/usr/bin/env python3
"""
merge.py: assemble per-domain research JSON into the board, data/the-program.json.

Reads:  research/*.json   (one per domain, written by the research agents)
Writes: data/the-program.json, and the tools/*.json reports

It also wrote data/program-*.js, the old single-file shell's data shape, until that
shell was retired on 25 September 2026. Nothing read them after it.

Conservative by design: duplicate ids MERGE rather than overwrite, and nothing
is dropped silently. Unplaceable records land in tools/REJECTS.json with a reason.
"""

import json, os, re, sys, glob, unicodedata
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(ROOT, "research")
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "tools")

# --- pristine-merge mode -----------------------------------------------------
# regrade.py must be a pure function of the research corpus. If it scores a board
# that already contains its own previous overlay it reads its own output back in,
# skips the work it already did, and emits a THINNER _remediation.json than last
# time — silently destroying recovered dates on every rebuild. These two env vars
# let regrade build the board WITHOUT the overlay, to a scratch path, without
# touching data/the-program.json or the tools/*.json reports.
#
#   MERGE_SKIP=_remediation   comma-separated slugs to exclude from research/*.json
#   MERGE_JSON_OUT=<path>     write ONLY the board JSON here; emit nothing else
MERGE_SKIP = {s.strip() for s in os.environ.get("MERGE_SKIP", "").split(",") if s.strip()}
MERGE_JSON_OUT = os.environ.get("MERGE_JSON_OUT") or None

# --- id canonicalisation -----------------------------------------------------
# Different research agents wrote the same person under two ids: `p-dylan-borland`
# in one file and `dylan-borland` in another. regrade.py normalised these, but only
# inside its own overlay — so merge saw the normalised id as a NEW node, created an
# empty record for it, and fell back to the id for the display label. The board then
# carried five people twice, each pair splitting its edges and sources, with the twin
# rendering its own slug as its name ("alexandro-wiggins" instead of
# "Alexandro C. Wiggins"). Confirmed on the shipped board 2026-08-12.
#
# Canonicalisation belongs HERE, at load, because merge already merges duplicate ids
# conservatively — collapse the ids first and the existing rules union the records.
# regrade.py imports this so the two cannot drift apart again.
ID_MERGES = {"l-washington-dc": "l-dc"}
_P_PREFIX = re.compile(r"^p-[a-z]+-[a-z]")


def canonical_id(i):
    """One spelling per entity. Strips a stray `p-` prefix from person ids without
    touching genuinely p-named entities (`pogo`, `pursue-releases`, `project-sign`)."""
    if not i:
        return i
    i = str(i).strip()
    if i in ID_MERGES:
        return ID_MERGES[i]
    if _P_PREFIX.match(i):
        return i[2:]
    return i


# --- the one vocabulary --------------------------------------------------------
# schema/vocab.json holds every enumerated value this pipeline accepts (redesign
# phase 3, decision 6). These sets used to be literals here while the app kept its
# own copy of the edge types in app/src/vocab.ts; now both read one file.
SCHEMA_DIR = os.path.join(ROOT, "schema")
VOCAB = json.load(open(os.path.join(SCHEMA_DIR, "vocab.json"), encoding="utf-8"))
RESEARCH_SCHEMA = json.load(open(os.path.join(SCHEMA_DIR, "research.schema.json"),
                                 encoding="utf-8"))

VALID_CLS = {c["id"] for c in VOCAB["classes"]}
VALID_EDGE = {t["id"] for t in VOCAB["edgeTypes"]}
VALID_TIER = set(VOCAB["nodeTiers"])
VALID_CLUSTER = {c["id"] for c in VOCAB["clusters"]}
VALID_STRAND = set(VOCAB["strands"])
VALID_PRECISION = set(VOCAB["precisions"])
VALID_STATUS = set(VOCAB["personStatus"])
VALID_GRADE = set(VOCAB["timelineGrades"])
VERB_MAP = {k: v for k, v in VOCAB["authoredVerbs"].items() if not k.startswith("_")}
STRAND_ALIAS = {k: v for k, v in VOCAB["strandAliases"].items() if not k.startswith("_")}
TIER_WORDS = VOCAB["claimTierWords"]

rejects = []
schema_warnings = []      # unknown fields: warnings in phase 3, not rejects
display_normalised = []   # labels whose spaced em dash became " - " (decision 7)
unadjudicated_denials = []
unplaced_claims = []      # claims authored on an id that has no survivor to carry them
unplaced_sources = []
entity_info_keys = {"aliased": [], "dropped": [], "unplaced": []}


# --- display labels ---------------------------------------------------------------
# A spaced em dash in a DISPLAY label becomes " - ", and every change is listed in
# tools/DISPLAY-NORMALISED.json. Labels only: claim texts, source strings and
# timeline texts are never touched, because they may be verbatim quotations.
SPACED_EM_DASH = re.compile(r"\s+\u2014\s+")


def display_label(s, where, oid):
    if not isinstance(s, str) or "\u2014" not in s:
        return s
    new = SPACED_EM_DASH.sub(" - ", s)
    if new != s:
        display_normalised.append({"where": where, "id": oid, "from": s, "to": new})
    return new


# --- research.schema.json -----------------------------------------------------------
def _kind_schema(kind):
    return RESEARCH_SCHEMA["$defs"][kind]


def schema_fields(kind, rec, slug):
    """Unknown fields are WARNINGS in this phase (tools/SCHEMA-WARNINGS.json).
    Fields whose name starts with `_` are the research's own annotations."""
    known = _kind_schema(kind)["properties"]
    for f in rec:
        if f.startswith("_") or f in known:
            continue
        schema_warnings.append({"kind": kind, "file": slug, "id": rec.get("id") or
                                f"{rec.get('a') or rec.get('from')}->{rec.get('b') or rec.get('to')}",
                                "field": f})


def schema_enum(kind, field, value, rec, slug):
    """An enumerated field with a value outside schema/vocab.json is a REJECT: the
    value is recorded and not used. Absent (None) is not a value. Returns the value
    to use, or None."""
    if value is None:
        return None
    spec = _kind_schema(kind)["properties"][field]
    allowed = set()
    for ref in spec.get("x-vocab") or []:
        v = VOCAB[ref]
        if isinstance(v, dict):
            allowed |= {k for k in v if not k.startswith("_")}
        else:
            allowed |= {x["id"] if isinstance(x, dict) else x for x in v}
    allowed |= set(spec.get("x-also") or [])
    if value in allowed:
        return value
    reject(f"{kind}.{field}", rec, f"{field} {value!r} is not in schema/vocab.json ({slug})")
    return None


def reject(kind, obj, why):
    rejects.append({"kind": kind, "why": why,
                    "id": obj.get("id") or f"{obj.get('a')}->{obj.get('b')}" if isinstance(obj, dict) else str(obj)[:80]})


def norm_source(s):
    # Tolerate a bare URL string. This function already accepts `label` and `title`
    # as aliases for name and `verified` as an alias for date, and load() already
    # tolerates entityInfo written as a plain string -- a source written as just its
    # URL is the same shape of agent slip and there is no reason to discard it.
    #
    # Discarding it is what happened: 732 sources across research/ were written as
    # bare strings and dropped here without a word, 76 of them URLs that reached the
    # board by no other route. Several sat on edges a later pass then recorded as
    # UNSOURCED and went looking for citations that were already in the file.
    if isinstance(s, str):
        s = s.strip()
        if not s:
            reject("source", s, "empty string")
            return None
        s = {"url": s} if s.startswith("http") else {"name": s}
    if not isinstance(s, dict):
        reject("source", s, "not a string or an object")
        return None
    name = s.get("name") or s.get("label") or s.get("title")
    url = s.get("url")
    date = s.get("date") or s.get("verified") or None
    if not name and not url:
        # Recorded, not merely skipped: the `cls` bug of 30 August dropped seven
        # whole records in silence and `no research record is silently dropped`
        # caught it; a source or a claim that vanishes the same way is the same
        # failure one level down.
        reject("source", s, "no name and no url")
        return None
    return {"name": name or url, "url": url or "", "date": date}


def norm_sources(lst):
    out, seen = [], set()
    for s in lst or []:
        n = norm_source(s)
        if not n:
            continue
        key = (n["url"] or "").strip().lower() or n["name"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(n)
    return out


def norm_claim(c):
    if not isinstance(c, dict):
        reject("claim", c, "not an object")
        return None
    t = c.get("tier")
    if isinstance(t, str) and not t.strip().isdigit():
        t = TIER_WORDS.get(t.lower(), 3)
    try:
        t = int(t)
    except (TypeError, ValueError):
        t = 3
    if t not in (1, 2, 3):
        t = 3
    text = c.get("text") or c.get("claim")
    if not text:
        reject("claim", c, "no text")
        return None
    src = c.get("source")
    if isinstance(src, list):
        ns = norm_sources(src)
        src = "; ".join(x["name"] for x in ns) if ns else None
    return {"tier": t, "text": text, "source": src or "No attributed source on file"}


def norm_claims(lst):
    return [x for x in (norm_claim(c) for c in (lst or [])) if x]


def clamp_axis(v):
    try:
        return max(0, min(3, int(v)))
    except (TypeError, ValueError):
        return 0


# Out-of-vocabulary cluster values, counted rather than coerced in silence. The
# `_rs-*` source-set files tag `cluster` with a vocabulary of their own
# ("aaro", "aawsap-dird", "science", "legislation"), which is not a map band.
off_vocab_cluster = []


def _valid_cluster(v, owner=None, slug=None):
    """A cluster is either a real band or ABSENT. It is never defaulted here.

    This used to read `v if v in VALID_CLUSTER else "other"`, and that one
    expression was the whole defect: "other" is a real band AND the default, so
    once written into the record nothing downstream could tell the two apart.
    `merge_entity`/`merge_person` fill `cluster` only when it is falsy, so the
    first file to mention a node pinned "other" and every later authored band
    lost -- silently, because "other" is perfectly valid. 259 entities and 78
    people shipped off their authored band this way. Absence stays None until
    finalise_defaults() runs, after every file has been read."""
    if v in VALID_CLUSTER:
        return v
    if v:
        off_vocab_cluster.append({"id": owner, "file": slug, "value": v})
    return None


def norm_chron(lst, owner=None):
    out = []
    for c in lst or []:
        if not isinstance(c, dict):
            reject("chronology", {"id": owner, "entry": c}, "not an object")
            continue
        # `text` is accepted beside `event` and `label`. The first time this
        # function rejected instead of skipping (2 September 2026) it named 19
        # entries, all of Salvatore Pais's patent chronology, written with `text`
        # and absent from his dossier since they were researched.
        d, ev = c.get("date"), (c.get("event") or c.get("label") or c.get("text"))
        if not d or not ev:
            reject("chronology", {"id": owner, "entry": c}, "no date or no event")
            continue
        p = c.get("precision")
        if p not in VALID_PRECISION:
            p = ("day" if re.match(r"^\d{4}-\d{2}-\d{2}$", str(d))
                 else "month" if re.match(r"^\d{4}-\d{2}$", str(d)) else "year")
        out.append({"date": str(d), "event": ev, "precision": p})
    return sorted(out, key=lambda x: x["date"])


TIER_ORDER = {"A": 0, "B": 1, "C": 2}


def _union_lists(a, b, fields):
    for f in fields:
        merged = list(a.get(f) or [])
        for x in b.get(f) or []:
            if x not in merged:
                merged.append(x)
        a[f] = merged


def claim_key(text):
    """One claim's identity: its whole text, lower-cased, non-word characters out."""
    return re.sub(r"\W+", "", (text or "").lower())


def dedupe_claims(claims):
    out, seen = [], set()
    for c in claims:
        k = claim_key(c["text"])
        if k in seen:
            continue
        seen.add(k)
        out.append(c)
    return out


def _merge_claims(a, b):
    # The whole normalised text, not its first 120 characters: two long claims
    # that share an opening (the same document title, the same lead-in) and
    # diverge in their conclusion are two claims, and the truncated key merged
    # them in silence.
    #
    # The same key on BOTH sides (phase 3). The seen-set was built from the full
    # text while the incoming key was cut at 120 characters, so any claim longer
    # than that never matched itself and shipped twice: four nodes carried a
    # duplicate (anna-paulina-luna, eli-crane, hearing-2025-09-09,
    # uap-nda-waiver-directive-2026).
    seen = {claim_key(c["text"]) for c in a.get("claims", [])}
    for c in b.get("claims") or []:
        k = claim_key(c["text"])
        if k not in seen:
            seen.add(k)
            a.setdefault("claims", []).append(c)


def _merge_common(a, b):
    for f in ("C", "A", "D"):
        a[f] = max(clamp_axis(a.get(f)), clamp_axis(b.get(f)))
    at, bt = a.get("tier", "C"), b.get("tier", "C")
    a["tier"] = at if TIER_ORDER.get(at, 2) <= TIER_ORDER.get(bt, 2) else bt
    a["sources"] = norm_sources((a.get("sources") or []) + (b.get("sources") or []))
    _merge_claims(a, b)
    a.setdefault("_domains", [])
    for d in b.get("_domains", []):
        if d not in a["_domains"]:
            a["_domains"].append(d)


def _better_label(a, b):
    """`label` falls back to the id when a record has no name. That fallback must
    never beat a real name just because it was loaded from an earlier file — which
    is how `Dylan Borland` ended up displayed as `dylan-borland` once the duplicate
    ids were collapsed. A label identical to the id is absence, not a value."""
    av, bv = a.get("label"), b.get("label")
    rid = a.get("id")
    if ((not av) or av == rid) and bv and bv != rid:
        a["label"] = bv


def _better_date(a, b, owner=None, field=None):
    """Prefer the MORE PRECISE of two dates that agree; report two that do not.

    Dates on this board are ISO prefixes: "1947", "1948-03", "2023-07-26". The rule
    for `dateStart`/`dateEnd` was fill-if-falsy, so the FIRST file to carry a date
    won even when a later file carried the same date to the day, and the board threw
    away precision it had been given. `hearing-2023-07-26` shipped dateStart "2023":
    the node's own id knew the day and the board did not. 14 entities were doing this.

    Two dates AGREE when one is a prefix of the other AT A COMPONENT BOUNDARY, and
    then the longer one is strictly more information with nothing to decide. The
    boundary test matters: "194" is not a coarser "1947", and "2023-07-2" is not a
    coarser "2023-07-26".

    Anything else is two files disagreeing about WHEN something happened, which is a
    research question and not a merge one. Keep the first, exactly as before, and
    record it in DATE-CONFLICTS.json so the disagreement is visible instead of being
    settled by filename order. 13 entities are in that state today, including
    `geipan` at 1977 against 2005 and `yankee-blue` at 1950 against 1980."""
    if not a:
        return b
    if not b or a == b:
        return a
    short, long = (a, b) if len(a) < len(b) else (b, a)
    if long.startswith(short) and long[len(short)] == "-":
        return long
    date_conflicts.append({"id": owner, "field": field, "kept": a, "ignored": b})
    return a


def _record_person_date(a, b):
    """People keep fill-if-falsy for `date`: the first file wins, as it always has
    (phase 3 decision 4: the choice does not change). What changes is that two
    files disagreeing about WHEN is recorded in DATE-CONFLICTS.json beside the
    entity ones, instead of being settled by filename order in silence. Agreement
    is judged exactly as _better_date judges it: one date a prefix of the other at
    a component boundary is the same date at a coarser precision."""
    x, y = a.get("date"), b.get("date")
    if not x or not y or x == y:
        return
    x, y = str(x), str(y)
    short, long = (x, y) if len(x) < len(y) else (y, x)
    if long.startswith(short) and long[len(short)] == "-":
        return
    date_conflicts.append({"id": a.get("id"), "field": "date", "kept": a.get("date"),
                           "ignored": b.get("date")})


def merge_person(a, b):
    _better_label(a, b)
    _record_person_date(a, b)
    for f in ("loc", "locId", "instId", "sub", "cluster", "status",
              "date", "age", "photoCredit", "unexplainedResidual"):
        if not a.get(f) and b.get(f):
            a[f] = b[f]
    for f in ("narrative", "tierRationale"):
        if len(str(b.get(f) or "")) > len(str(a.get(f) or "")):
            a[f] = b[f]
    _merge_common(a, b)
    _union_lists(a, b, ("affiliations", "domains", "conflicts", "unverified", "sequenceChain"))
    seen = {(c["date"], c["event"][:60]) for c in a.get("chronology", [])}
    for c in b.get("chronology") or []:
        k = (c["date"], c["event"][:60])
        if k not in seen:
            seen.add(k)
            a.setdefault("chronology", []).append(c)
    a["chronology"] = sorted(a.get("chronology", []), key=lambda x: x["date"])
    return a


def merge_entity(a, b):
    _better_label(a, b)
    for f in ("cluster", "sub"):
        if not a.get(f) and b.get(f):
            a[f] = b[f]
    # NOT fill-if-falsy: a date carries precision, and the coarser one is not a
    # value to be defended just because its file sorted earlier. See _better_date.
    for f in ("dateStart", "dateEnd"):
        v = _better_date(a.get(f), b.get(f), a.get("id"), f)
        if v:
            a[f] = v
    if len(str(b.get("desc") or "")) > len(str(a.get("desc") or "")):
        a["desc"] = b["desc"]
    if not a.get("short") and b.get("short"):
        a["short"] = b["short"]
    _merge_common(a, b)
    # Unioned across files exactly as a person's are. Until phase 3 the entity
    # record was built from a fixed field list that did not name these, so 22
    # conflicts, 99 unverified notes and 18 open questions never reached the board.
    _union_lists(a, b, ENTITY_LIST_FIELDS)
    return a


# The list fields an entity carries and unions across research files.
ENTITY_LIST_FIELDS = ("conflicts", "unverified", "openQuestions", "domains")
# The fields that follow a collapsed node to its survivor.
CASE_AGAINST_FIELDS = ("conflicts", "unverified", "openQuestions")


def carry_collapsed(tgt, loser):
    """Everything the survivor would show, from the collapsed record: its claims
    (deduped by the one claim key), its sources (deduped as sources always are),
    the case against, a person's affiliations, chronology and sequence chain, and
    its provenance. Prose only where the survivor has none: the survivor's own
    `desc` or `narrative` is never replaced by the collapsed copy's. Tier, axes,
    dates, label and status stay the survivor's: those are settled on the
    survivor (and by the regrade overlay), not re-opened by a collapse."""
    tgt["claims"] = dedupe_claims(list(tgt.get("claims") or []) + list(loser.get("claims") or []))
    tgt["sources"] = norm_sources((tgt.get("sources") or []) + (loser.get("sources") or []))
    for f in ("desc", "narrative"):
        if f in loser and loser.get(f) and not tgt.get(f):
            tgt[f] = loser[f]
    lists = [f for f in CASE_AGAINST_FIELDS + ("affiliations", "sequenceChain")
             if loser.get(f)]
    _union_lists(tgt, loser, lists)
    if loser.get("chronology"):
        seen = {(c["date"], c["event"][:60]) for c in tgt.get("chronology") or []}
        for c in loser["chronology"]:
            if (c["date"], c["event"][:60]) not in seen:
                seen.add((c["date"], c["event"][:60]))
                tgt.setdefault("chronology", []).append(c)
        tgt["chronology"] = sorted(tgt["chronology"], key=lambda x: x["date"])
    for d in loser.get("_domains") or []:
        if d not in tgt.setdefault("_domains", []):
            tgt["_domains"].append(d)


def _as_list(v):
    """`conflicts` and `unverified` are authored as a list, or once in a while as a
    bare string. A string is one item, not a sequence of characters."""
    if v is None or v == "":
        return []
    return list(v) if isinstance(v, list) else [v]


def finalise_defaults(people, entities):
    """Apply the defaults for fill-if-falsy fields ONCE, after every research file
    has been read, so load order cannot decide them.

    A fill-if-falsy field is safe only while its absent-value is falsy. Every
    other field in those lists (loc, locId, instId, sub, date, age, dateStart,
    dateEnd, photoCredit, unexplainedResidual) already defaults to None and was
    never at risk. `cluster` and person `status` were the two that defaulted to a
    truthy value, and both were wrong on the shipped board.

    An overlay may also set a cluster directly, bypassing _valid_cluster, so the
    vocabulary is enforced here as well rather than only at read time."""
    fixed = {"cluster": 0, "status": 0, "coerced": 0}
    for rec in list(people.values()) + list(entities.values()):
        c = rec.get("cluster")
        if c is None:
            rec["cluster"] = "other"
            fixed["cluster"] += 1
        elif c not in VALID_CLUSTER:
            off_vocab_cluster.append({"id": rec.get("id"), "file": "overlay", "value": c})
            rec["cluster"] = "other"
            fixed["coerced"] += 1
    for rec in people.values():
        if not rec.get("status"):
            rec["status"] = "active"
            fixed["status"] += 1
        # An overlay may set status directly, bypassing schema_enum at read time.
        elif rec["status"] not in VALID_STATUS:
            reject("person.status", rec, f"status {rec['status']!r} is not in schema/vocab.json (overlay)")
    print(f"  defaults applied after merge: cluster={fixed['cluster']} "
          f"status={fixed['status']} coerced={fixed['coerced']}", file=sys.stderr)
    if off_vocab_cluster:
        bad = sorted({o["value"] for o in off_vocab_cluster})
        print(f"  {len(off_vocab_cluster)} out-of-vocabulary cluster value(s) ignored, "
              f"from {bad}", file=sys.stderr)


NOT_NODE_DOCUMENTS = {"_edge_tiers.json"}


def _removed_aliases():
    p = os.path.join(RESEARCH, "_removed.json")
    if not os.path.exists(p):
        return {}
    return json.load(open(p, encoding="utf-8")).get("alias") or {}


EI_ALIAS = _removed_aliases()


def norm_timeline(t, slug):
    """One timeline event, normalised. Returns a new dict, or None to drop it (with
    a reject recorded).

    STRAND. An authored strand outside the four lanes used to become `program` in
    silence (50 events: disclosure, mechanism, research). The mapping is declared in
    schema/vocab.json `strandAliases` now, the event keeps `authoredStrand`, and a
    strand in neither list is a reject. Absent is not a value: it defaults to
    `program` as before.

    LABEL AND NODE. Thirteen events were authored with `event` and `ref` in place of
    `label` and `node`, so they shipped with no label and joined no node page.

    TIER (phase 3 decision 5). One field carried two vocabularies: an event GRADE
    (A/B/C) and a claim TIER (1/2/3, as ints and as strings). They are two fields
    now, `grade` and `claimTier`; `tier` is not shipped."""
    t = dict(t)
    s = t.get("strand")
    if s is not None and s not in VALID_STRAND:
        if s in STRAND_ALIAS:
            t["authoredStrand"], t["strand"] = s, STRAND_ALIAS[s]
        else:
            reject("timeline.strand", t, f"strand {s!r} is not in schema/vocab.json ({slug})")
            t["strand"] = None
    if not t.get("strand"):
        t["strand"] = "program"
    p = t.get("precision")
    if p is not None and p not in VALID_PRECISION:
        reject("timeline.precision", t, f"precision {p!r} is not in schema/vocab.json ({slug})")
    if t.get("precision") not in VALID_PRECISION:
        t["precision"] = ("day" if re.match(r"^\d{4}-\d{2}-\d{2}$", str(t.get("date", "")))
                          else "year")
    if not t.get("label") and t.get("event"):
        t["label"] = t.pop("event")
    if not t.get("node") and t.get("ref"):
        t["node"] = t.pop("ref")
    if t.get("label"):
        t["label"] = display_label(t["label"], "timeline.label", t.get("id") or t.get("date"))
    if "tier" in t:
        v = t.pop("tier")
        if isinstance(v, str) and v.strip() in VALID_GRADE:
            t["grade"] = v.strip()
        elif str(v).strip() in ("1", "2", "3"):
            t["claimTier"] = int(str(v).strip())
        elif v is not None:
            reject("timeline.tier", t, f"tier {v!r} is neither a grade nor a claim tier ({slug})")
    return t

# entityInfo keys that are a research file's own metadata, not a node: dropped, and
# listed in tools/ENTITYINFO-KEYS.json. Keys starting with `_` are always metadata.
ENTITY_INFO_META = {"domain", "title", "scope", "thesis", "methodNote", "throughLine",
                    "counts"}


def load():
    people, entities, edges, timeline = OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()
    entity_info, gaps = {}, []

    # _remediation must land last: it is an authoritative overlay that OVERRIDES
    # the merge rules (which otherwise take the strongest tier and would undo a
    # deliberate demotion). _stubs lands second-to-last so real dossiers win over stubs.
    allf = glob.glob(os.path.join(RESEARCH, "*.json"))
    # research/_edge_tiers.json is not a node document: it is a list of per-edge
    # tier ADJUDICATIONS, read by load_edge_adjudications(). The glob used to take
    # its 16 records as edges as well (unsourced, unnoted, typed by the decision
    # they record), so it is named out here.
    allf = [f for f in allf if os.path.basename(f) not in NOT_NODE_DOCUMENTS]
    if MERGE_SKIP:
        allf = [f for f in allf
                if os.path.splitext(os.path.basename(f))[0] not in MERGE_SKIP]
        print(f"[pristine] excluded {sorted(MERGE_SKIP)} from the merge", file=sys.stderr)
    rank = lambda f: (3 if "_corrections" in f else 2 if "_remediation" in f else 1 if "_stubs" in f else 0, f)
    files = sorted(allf, key=rank)
    if not files:
        print("no research files in", RESEARCH, file=sys.stderr)

    for path in files:
        slug = os.path.splitext(os.path.basename(path))[0]
        try:
            doc = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            reject("file", {"id": path}, f"unparseable: {e}")
            continue

        for p in doc.get("people") or []:
            pid = canonical_id(p.get("id"))
            if not pid:
                reject("person", p, "no id")
                continue
            schema_fields("person", p, slug)
            rec = {
                "id": pid, "cls": "person",
                "label": display_label(p.get("label") or p.get("name") or pid, "node.label", pid),
                # Defaulted LATE, in finalise_defaults(). "active" is truthy and
                # merge_person fills `status` only when it is falsy, so defaulting
                # it here let the first file to mention a person pin "active" for
                # good: Harry Reid, Gerald Ford, Kenneth Arnold and Nathan Twining
                # all shipped "active" while another file said "dead".
                "status": schema_enum("person", "status", p.get("status") or None, p, slug),
                "date": p.get("date"), "age": p.get("age"),
                "loc": p.get("loc"),
                "locId": canonical_id(p.get("locId")), "instId": canonical_id(p.get("instId")),
                "sub": p.get("sub"),
                "cluster": _valid_cluster(p.get("cluster"), pid, slug),
                "tier": schema_enum("person", "tier", p.get("tier"), p, slug) or "C",
                "C": clamp_axis(p.get("C")), "A": clamp_axis(p.get("A")), "D": clamp_axis(p.get("D")),
                "domains": p.get("domains") or [],
                "narrative": p.get("narrative") or "",
                "affiliations": p.get("affiliations") or [],
                "tierRationale": p.get("tierRationale") or "",
                "chronology": norm_chron(p.get("chronology"), pid),
                "claims": norm_claims(p.get("claims")),
                "sources": norm_sources(p.get("sources")),
                "conflicts": p.get("conflicts") or [],
                "unverified": p.get("unverified") or [],
                "sequenceChain": p.get("sequenceChain") or [],
                "unexplainedResidual": p.get("unexplainedResidual"),
                "photoCredit": p.get("photoCredit"),
                "_domains": [slug],
            }
            if slug == "_corrections" and pid in people:
                # The entity side of this overlay has existed since the Condign
                # corrections. People needed it for the same reason and did not
                # have it: merge_person UNIONS domains, affiliations and
                # sequenceChain, so a wrong value cannot be removed by editing the
                # research file that introduced it -- the union pulls it back from
                # whichever other file also declares it. A correction has to be
                # able to say "this field is now exactly this", so on the
                # reference fields this overlay REPLACES rather than merges.
                tgt = people[pid]
                for f in ("label", "sub", "cluster", "tier", "status", "loc",
                          "date", "narrative", "unexplainedResidual"):
                    if p.get(f) is not None:
                        tgt[f] = rec["label"] if f == "label" else p[f]
                # membership test, not truthiness: an explicit null or [] is the
                # correction in every case where the old value should simply go.
                for f in ("locId", "instId", "domains", "affiliations", "sequenceChain"):
                    if f in p:
                        tgt[f] = rec[f]
                if p.get("sources"):
                    tgt["sources"] = norm_sources(list(p["sources"]) + tgt.get("sources", []))
                if p.get("claims"):
                    tgt["claims"] = dedupe_claims(norm_claims(p["claims"]) + tgt.get("claims", []))
            elif slug == "_remediation" and pid in people:
                tgt = people[pid]
                for f in ("tier", "tierRationale", "date", "coords"):
                    if p.get(f) is not None:
                        tgt[f] = p[f]
            elif slug in ("_corrections", "_remediation"):
                # An overlay names an id nothing else declares: a typo, or a node
                # since renamed or removed. Creating a near-empty node from the
                # correction's few fields is the wrong outcome twice over, so it is
                # rejected by name and the gate says so.
                reject("person", p, f"{slug} names an id no research file declares")
            else:
                people[pid] = merge_person(people[pid], rec) if pid in people else rec

        for e in doc.get("entities") or []:
            eid, cls = canonical_id(e.get("id")), e.get("cls")
            if not eid:
                reject("entity", e, "no id")
                continue
            if cls not in VALID_CLS or cls == "person":
                reject("entity", e, f"bad cls {cls!r}")
                continue
            schema_fields("entity", e, slug)
            rec = {
                "id": eid, "cls": cls,
                "label": display_label(e.get("label") or eid, "node.label", eid),
                "cluster": _valid_cluster(e.get("cluster"), eid, slug),
                "sub": e.get("sub"), "desc": e.get("desc") or None,
                "tier": schema_enum("entity", "tier", e.get("tier"), e, slug) or "C",
                "C": clamp_axis(e.get("C")), "A": clamp_axis(e.get("A")), "D": clamp_axis(e.get("D")),
                "dateStart": e.get("dateStart"), "dateEnd": e.get("dateEnd"),
                "coords": e.get("coords"), "locLabel": e.get("locLabel"),
                "tierRationale": e.get("tierRationale") or "",
                "claims": norm_claims(e.get("claims")),
                "sources": norm_sources(e.get("sources")),
                # Carried since phase 3 (decision 1). Before it these five were
                # read by nothing and 63 records' worth of the case against a node
                # (its conflicts and its unverified notes) never reached the board.
                "short": display_label(e.get("short"), "node.short", eid) or None,
                **{f: _as_list(e.get(f)) for f in ENTITY_LIST_FIELDS},
                "_domains": [slug],
            }
            if slug == "_corrections" and eid in entities:
                # Corrections are authoritative and may overwrite prose. They exist
                # because a claim on this board turned out not to survive a check,
                # and the record of that has to beat the merge's "longest wins" rule.
                #
                # dateStart/dateEnd joined this list in phase 3 (decision 1): a
                # correction to WHEN is as authoritative as a correction to what,
                # and it is the one field _better_date cannot settle by itself.
                tgt = entities[eid]
                for f in ("label", "desc", "sub", "cluster", "tier", "dateStart", "dateEnd"):
                    if e.get(f) is not None:
                        tgt[f] = rec["label"] if f == "label" else e[f]
                tgt["sources"] = norm_sources(list(e.get("sources") or []) + tgt.get("sources", []))
                # A correction may REMOVE claims it supersedes, but only by saying so:
                #   "removeClaims": [{"contains": "...", "tier": 1, "why": "..."}]
                # Until 2 September 2026 this line carried a hardcoded filter that
                # dropped every Tier 1 claim containing "yankee blue" on every
                # corrected entity. By then the claims it removed were the negative
                # primary findings (AFOSI's 'no records' FOIA answer, the zero-hit
                # full-text search of HRR Volume I) -- the corroboration of the
                # correction, not the error it was written to remove. A removal
                # rule that lives in code is a removal nobody can review.
                rules = [r for r in (e.get("removeClaims") or []) if isinstance(r, dict) and r.get("contains")]
                def _kept(c):
                    for r in rules:
                        if r["contains"].lower() in c["text"].lower() and r.get("tier") in (None, c["tier"]):
                            removed_claims.append({"id": eid, "why": r.get("why", ""),
                                                   "claim": c["text"][:110]})
                            return False
                    return True
                tgt["claims"] = dedupe_claims(norm_claims(e.get("claims")) +
                                              [c for c in tgt.get("claims", []) if _kept(c)])
            elif slug == "_remediation" and eid in entities:
                tgt = entities[eid]
                for f in ("tier", "tierRationale", "coords", "locLabel"):
                    if e.get(f) is not None:
                        tgt[f] = e[f]
            elif slug in ("_corrections", "_remediation"):
                reject("entity", e, f"{slug} names an id no research file declares")
            else:
                entities[eid] = merge_entity(entities[eid], rec) if eid in entities else rec

        for x in doc.get("edges") or []:
            a_ = canonical_id(x.get("a") or x.get("from"))
            b_ = canonical_id(x.get("b") or x.get("to"))
            t = x.get("type") or x.get("rel")
            if not a_ or not b_:
                reject("edge", x, "missing endpoint")
                continue
            schema_fields("edge", x, slug)
            # An authored verb outside the twelve types is MAPPED, by the table in
            # schema/vocab.json, and the edge keeps the verb. Until phase 3 every
            # such verb (89 records, 35 verbs) became `programmatic` in silence. A
            # verb the table does not name is a reject, never a coercion.
            verb = None
            if t not in VALID_EDGE:
                m = VERB_MAP.get(t)
                if not m:
                    reject("edge", x, f"edge type {t!r} is neither one of the twelve types "
                                      f"nor in schema/vocab.json authoredVerbs ({slug})")
                    continue
                verb, t = t, m["type"]
                if m.get("swap"):
                    a_, b_ = b_, a_
            key, rkey = f"{a_}|{b_}|{t}", f"{b_}|{a_}|{t}"
            if rkey in edges:
                key = rkey
            # Singular `tier` and `source` are aliases (phase 3 decision 2), not
            # noise: 62 records carry them, 15 of those URLs are on no twin, and
            # merge read only `claimTier` and `sources`. The strongest tier wins,
            # exactly as between duplicate edges, and the caps below still apply.
            tiers = [v for v in (x.get("claimTier"), x.get("tier")) if v in (1, 2, 3)]
            ct = min(tiers) if tiers else 3
            srcs = list(x.get("sources") or [])
            if x.get("source"):
                srcs += x["source"] if isinstance(x["source"], list) else [x["source"]]
            rec = {"a": a_, "b": b_, "type": t,
                   "label": display_label(x.get("label") or "", "edge.label", f"{a_}->{b_}"),
                   "claimTier": ct, "dateStart": x.get("dateStart"), "dateEnd": x.get("dateEnd"),
                   "note": x.get("note") or x.get("summary") or "",
                   "sources": norm_sources(srcs), "_domains": [slug]}
            if verb:
                rec["authoredVerb"] = verb
            # A research file may carry its own denial verdict (one does). The
            # adjudication file, applied in emit(), still has the last word.
            if t == "denial":
                for f in ("denialKind", "denier"):
                    if x.get(f):
                        rec[f] = canonical_id(x[f]) if f == "denier" else x[f]
            if key in edges:
                old = edges[key]
                if len(rec["note"]) > len(old["note"]):
                    old["note"] = rec["note"]
                if not old["label"]:
                    old["label"] = rec["label"]
                old["claimTier"] = min(old["claimTier"], rec["claimTier"])
                old["sources"] = norm_sources(old["sources"] + rec["sources"])
                for f in ("authoredVerb", "denialKind", "denier"):
                    if rec.get(f) and not old.get(f):
                        old[f] = rec[f]
                for d in rec["_domains"]:
                    if d not in old["_domains"]:
                        old["_domains"].append(d)
            else:
                edges[key] = rec

        seen_tl = {(v.get("date"), (v.get("label") or "")[:50]) for v in timeline.values()}
        for t in doc.get("timeline") or []:
            schema_fields("timeline", t, slug)
            t = norm_timeline(t, slug)
            if t is None:
                continue
            key = (t.get("date"), (t.get("label") or "")[:50])
            if key in seen_tl:
                continue
            seen_tl.add(key)
            if t.get("node"):
                t["node"] = canonical_id(t["node"])
            tid = t.get("id") or f"{slug}-{len(timeline)}"
            while tid in timeline:
                tid += "x"
            t["id"] = tid
            timeline[tid] = t

        for k, v in (doc.get("entityInfo") or {}).items():
            # A research file's own metadata written into entityInfo (its domain,
            # title, scope, a count table) is not about a node. Dropped, listed.
            if k.startswith("_") or k in ENTITY_INFO_META:
                entity_info_keys["dropped"].append({"file": slug, "key": k})
                continue
            k = canonical_id(k)
            # A collapsed node's entityInfo follows it to the survivor, as its
            # edges and timeline events do (phase 3 decision 9).
            if k in EI_ALIAS:
                entity_info_keys["aliased"].append({"file": slug, "key": k, "to": EI_ALIAS[k]})
                k = EI_ALIAS[k]
            # tolerate agents that wrote entityInfo as {id: "desc string"}
            if isinstance(v, str):
                v = {"desc": v, "sources": []}
            elif not isinstance(v, dict):
                reject("entityInfo", {"id": k}, f"unexpected type {type(v).__name__}")
                continue
            if k in entity_info:
                if len(str(v.get("desc") or "")) > len(str(entity_info[k].get("desc") or "")):
                    entity_info[k]["desc"] = v.get("desc")
                entity_info[k]["sources"] = norm_sources(
                    entity_info[k].get("sources", []) + (v.get("sources") or []))
            else:
                entity_info[k] = {"desc": v.get("desc"), "sources": norm_sources(v.get("sources"))}

        for g in doc.get("gaps") or []:
            gaps.append({"domain": slug, "gap": g})

    # ---- approved removals -------------------------------------------------
    # research/_removed.json is a deliberate, approved deletion list. It exists as
    # a file rather than as edits to the source research because a deletion should
    # be reviewable: the ids, the reason and who approved it stay in the repo.
    # Edges touching a removed node go with it, or verify.py's dangling-reference
    # check fails the build -- which is the correct behaviour and the reason this
    # is done here rather than by hand.
    rmpath = os.path.join(RESEARCH, "_removed.json")
    if os.path.exists(rmpath):
        rm = set(json.load(open(rmpath, encoding="utf-8")).get("remove") or [])
        gone = [i for i in rm if i in people or i in entities]
        # What was authored on a collapsed node goes to its survivor, like its
        # edges. Until phase 3 only the edges and timeline followed a collapse, so
        # 37 claims (all of `setka`'s Soviet programme record, five DoDD 5205.07
        # quotations on `dod-sapco-arch`, the DIRD list on `dird-collection`) and
        # their sources were deleted with the id they were written under.
        # carry_collapsed() says exactly what moves. A deletion with no alias, and
        # a collapse into a `d-*` domain node (a topic, not the thing the claim is
        # about), move nothing: those claims are listed in
        # tools/UNPLACED-CLAIMS.json rather than placed by guess.
        _alias = json.load(open(rmpath, encoding="utf-8")).get("alias") or {}
        for i in sorted(gone):
            loser = people.get(i) or entities.get(i)
            to = _alias.get(i)
            while to in _alias and to not in people and to not in entities:
                to = _alias[to]
            tgt = people.get(to) or entities.get(to)
            if not loser:
                continue
            if tgt is None or str(to).startswith("d-"):
                why = ("removed by research/_removed.json with no alias" if not to
                       else f"collapsed into {to}, which is not on the board" if tgt is None
                       else f"collapsed into the domain node {to}: a topic, not the thing "
                            f"the claim is about, so nothing is placed by guess")
                for c in loser.get("claims") or []:
                    unplaced_claims.append({"id": i, "to": to, "why": why, "tier": c["tier"],
                                            "claim": c["text"], "source": c.get("source")})
                for sc in loser.get("sources") or []:
                    unplaced_sources.append({"id": i, "to": to, "why": why,
                                             "url": sc.get("url"), "name": sc.get("name")})
                continue
            carry_collapsed(tgt, loser)
        for i in gone:
            people.pop(i, None)
            entities.pop(i, None)
        # A COLLAPSE is not a deletion: dird-collection and dird-series described
        # the same object. Where an alias exists, re-point references at the
        # survivor rather than orphaning them -- a removed node that timeline
        # events still cite is a dangling reference, and verify.py caught exactly
        # that on the first attempt at this.
        alias = json.load(open(rmpath, encoding="utf-8")).get("alias") or {}
        repointed = 0
        for t in timeline.values():
            for f in ("node", "nodeId", "ref", "entityId"):
                if t.get(f) in alias:
                    t[f] = alias[t[f]]
                    repointed += 1
            for f in ("nodes", "refs", "entityIds"):
                if isinstance(t.get(f), list) and any(x in alias for x in t[f]):
                    t[f] = [alias.get(x, x) for x in t[f]]
                    repointed += 1
        # An edge touching a COLLAPSED node is not garbage: it is a real
        # relationship recorded against the wrong copy of a node. Re-point it at the
        # survivor first, exactly as the timeline and the person back-references are
        # re-pointed, and only then drop what is left. Without this a collapse
        # silently deletes the loser's edges, which is how a duplicate ends up
        # costing evidence instead of just tidiness.
        repointed_edges = 0
        for key in list(edges.keys()):
            e = edges[key]
            na, nb = alias.get(e["a"], e["a"]), alias.get(e["b"], e["b"])
            if (na, nb) == (e["a"], e["b"]):
                continue
            edges.pop(key)
            if na == nb:
                # the collapse made both ends the same node; a self-edge is noise
                repointed_edges += 1
                continue
            e["a"], e["b"] = na, nb
            nk, rk = f"{na}|{nb}|{e['type']}", f"{nb}|{na}|{e['type']}"
            tgt = rk if rk in edges else nk
            if tgt in edges:
                old_e = edges[tgt]
                if len(e["note"]) > len(old_e["note"]):
                    old_e["note"] = e["note"]
                if not old_e["label"]:
                    old_e["label"] = e["label"]
                old_e["claimTier"] = min(old_e["claimTier"], e["claimTier"])
                old_e["sources"] = norm_sources(old_e["sources"] + e["sources"])
                for f in ("authoredVerb", "denialKind", "denier"):
                    if e.get(f) and not old_e.get(f):
                        old_e[f] = e[f]
                for dm in e["_domains"]:
                    if dm not in old_e["_domains"]:
                        old_e["_domains"].append(dm)
            else:
                edges[nk] = e
            repointed_edges += 1
        if repointed_edges:
            print(f"  re-pointed {repointed_edges} edge(s) onto collapse survivors",
                  file=sys.stderr)

        dropped = [k for k, e in edges.items() if e["a"] in rm or e["b"] in rm]
        for k in dropped:
            edges.pop(k)

        # Dropping the edges is not the whole job. A person points at nodes through
        # locId, instId and domains as well, and deriveEdges() turns every one of
        # those into a live edge at runtime -- so a back-reference to a removed node
        # is a phantom edge, not merely untidy data.
        #
        # The first version of this block swept edges only, because verify.py's
        # dangling check walked edge endpoints only. Satisfying the gate defined the
        # scope of the fix, and 31 people kept pointing at 30 removed locations while
        # the gate reported ok. The gate now walks these fields too; this sweep is
        # what keeps them clean, and an alias re-points rather than orphans exactly
        # as it does for the timeline above.
        # A denier named by a research file follows a collapse like any other id.
        for e in edges.values():
            if e.get("denier") in alias:
                e["denier"] = alias[e["denier"]]
        swept = 0
        for p_ in list(people.values()) + list(entities.values()):
            for f in ("locId", "instId"):
                if p_.get(f) in rm:
                    p_[f] = alias.get(p_[f])
                    swept += 1
            doms = [alias.get(d, d) for d in p_.get("domains") or []]
            doms = [d for i, d in enumerate(doms) if d not in rm and d not in doms[:i]]
            if doms != (p_.get("domains") or []):
                p_["domains"] = doms
                swept += 1
        if swept:
            print(f"  swept {swept} person back-reference(s) to removed nodes",
                  file=sys.stderr)
        if repointed:
            print(f"  re-pointed {repointed} reference(s) to a collapsed node",
                  file=sys.stderr)
        if gone or dropped:
            print(f"  removed {len(gone)} approved node(s) and {len(dropped)} edge(s) "
                  f"that touched them", file=sys.stderr)

    finalise_defaults(people, entities)

    # entityInfo keyed on no node. Not dropped: several are sourced prose (the
    # black-budget essays in w2-black-budget.json) that no node carries yet, and
    # they stay on the board file where they always were. Listed, so that a key
    # which is really a typo of a node id is visible rather than inert.
    for k in entity_info:
        if k not in people and k not in entities:
            entity_info_keys["unplaced"].append(k)

    return people, entities, edges, timeline, entity_info, gaps


# --------------------------------------------------------------------------
# tier remediation — runs after load, before integrity
# --------------------------------------------------------------------------

# A Tier 1 claim asserts a primary record exists. These patterns identify sources
# that are NOT primary records, however reliable they may be as reporting.
SECONDARY_PAT = re.compile(
    # 'blog' without \b: the word boundary meant this missed 'blogspot.com', and
    # 29 Tier 1 claims were cited to one blogspot host alone.
    r"wikipedia|britannica|\bwiki\b|reddit|substack|medium\.com|youtube|"
    r"podcast|blog|fandom", re.I)

# A URL that would justify Tier 1: statute, regulation, agency policy, court
# record, congressional record, archive, or an agency's own document repository.
#
# This pattern was written against the US federal record and silently treated
# every other government on earth as unsourceable. The board now carries the UK
# National Archives, Canada, Chile's DGAC, Brazil's Arquivo Nacional, the Senado
# and the Camara -- 16, 17, 13, 10 and 6 citations respectively -- and none of
# them counted. It also only credited a .mil URL when it ended in .pdf, so
# dia.mil and aaro.mil (248 and 154 citations) did not register as primary
# records even of their own statements.
#
# Two non-government hosts are included deliberately: The Black Vault and the
# FAS Intelligence Resource Program host the released FOIA PDFs themselves --
# the DIRDs and the DIA's 9 January 2018 AATIP list among them. Primacy belongs
# to the document, not to who serves it, and the alternative is that 118
# citations of actual released government records count as no source at all.
#
# Whether a URL is a primary record is a SEPARATE question from whether the body
# publishing it is disinterested. aaro.mil is a primary record OF ITS OWN
# STATEMENT and nothing more, and INTERESTED_PARTY_PAT below is what enforces
# that. Widening this pattern does not loosen that rule.
PRIMARY_URL_PAT = re.compile(
    # US federal
    r"congress\.gov|govinfo\.gov|federalregister\.gov|whitehouse\.gov|"
    r"archives\.gov|presidentiallibraries\.us|ecfr\.gov|acquisition\.gov|"
    r"law\.cornell\.edu|courtlistener|\.uscourts\.gov|"
    r"gao\.gov|oversight\.house\.gov|\.senate\.gov|\.house\.gov|docs\.house\.gov|"
    r"\.mil\b|defense\.gov|war\.gov|dni\.gov|odni\.gov|cia\.gov|\.fbi\.gov|"
    r"nsa\.gov|dhs\.gov|energy\.gov|osti\.gov|lanl\.gov|sec\.gov|"
    r"usaspending\.gov|sam\.gov|fpds\.gov|fasab\.gov|foia|"
    r"nsf\.gov|nasa\.gov|cnes\.fr|patents\.google|uspto\.gov|doi\.org|"
    # other governments, all of them already cited on this board
    r"nationalarchives\.gov\.uk|\.gov\.uk|\.gc\.ca|\.gob\.cl|\.gov\.br|"
    r"leg\.br|\.gouv\.fr|legifrance|assemblee-nationale\.fr|senat\.fr|europa\.eu|"
    # third-party hosts of released government documents.
    #
    # archive.org is NOT a primary host in general -- it serves commercially
    # published books too, and this board cites some. But archive.org/details/DTIC_*
    # is the Defense Technical Information Center archive mirror: every item there
    # carries creator "Defense Technical Information Center" and sits in the
    # `dticarchive` and `government-documents` collections. A DTIC accession scan is
    # the released document, and the rule this pattern already states is that primacy
    # belongs to the document rather than to who serves it. Without this, the USAF's
    # own 1995 Roswell report (DTIC ADA326148) and all three volumes of the Condon
    # Report (DTIC AD0680975-7) count as no primary record at all.
    r"theblackvault\.com|irp\.fas\.org|archive\.org/details/DTIC_", re.I)

demotions = []

# --- interested parties ------------------------------------------------------
# AARO, its predecessor offices and DoD public affairs are not neutral archives.
# They are participants in the thing this board documents, and multiple witnesses
# have testified that AARO under Kirkpatrick functioned to surface and neutralise
# whistleblowers rather than to investigate. Publishing on aaro.mil therefore makes
# a document a PRIMARY RECORD OF THE STATEMENT, not a primary record of the fact
# asserted in it.
#
# This is the same distinction the board already makes about denials: "a denial is
# a dated, signed, attributable statement, which makes it evidence about the
# denier." That reasoning was applied to the `denial` edge type and never applied
# to sourcing, so 123 claims were sitting at Tier 1 on the strength of an aaro.mil
# or defense.gov URL alone — the board's highest evidentiary grade, awarded to the
# interested party's own account of itself.
INTERESTED_PARTY_PAT = re.compile(
    r"aaro\.mil|(?:^|//|\.)defense\.gov|war\.gov|dvidshub|media\.defense\.gov|"
    r"pentagon\.mil|\bdodcio\b", re.I)

# A claim ABOUT what an interested party said is legitimately Tier 1 from that
# party's own publication — there, the statement IS the fact. Only claims that use
# the interested party as an authority for an external fact get capped.
# The interested-party rule caps an AARO/DoD-sourced claim at Tier 2 UNLESS the
# claim is about what they said -- because publishing a document makes it a primary
# record OF THE STATEMENT. That exemption is only as wide as this verb list, and the
# list held speech verbs only. So a claim reporting what a document LISTS, CONTAINS,
# READS or PUBLISHES did not read as attribution and was demoted anyway.
#
# 47 claims were caught that way, and they included the strongest evidence on the
# board: that HRR Volume I contains zero occurrences of the name 'Wilson' across all
# 63 pages, what its title page reads verbatim, and the file manifest of every PURSUE
# release. A full-text negative finding about a document, sourced to that document,
# is exactly what Tier 1 is for.
ATTRIBUTION_PAT = re.compile(
    r"\b(denie[ds]|denial|declined|stated|states|said|asserts?|asserted|claims|"
    r"claimed|announced|acknowledg\w*|concluded|reported that|wrote|testified|"
    r"responded|maintains?|characteri[sz]ed|"
    r"attributes?|attributed|credits?|credited|lists?|listed|identifies|identified|"
    r"names|named|reads|contains?|describes?|described|prints?|printed|publishes|"
    r"published|records?|recorded|shows?|gives?|hosts?|"
    r"according to (?:aaro|the )?(?:dod|"
    r"department of defense|pentagon))\b", re.I)


URL_IN_SOURCE = re.compile(r"https?://[^\s,;)\]<>\"]+")
DEMOTION_NOTE = re.compile(r"\s*[-\u2014]+\s*DEMOTED from Tier 1.*$", re.I)


def hoist_claim_urls(people, entities):
    """Make node.sources[] reflect the URLs the node's own claims already cite.

    The research writes the primary record straight into claim.source and often
    leaves node.sources[] empty. Everything downstream reads node.sources[]: the
    demotion pass computes has_primary from it, and the integrity report counts
    it. So 26 nodes carrying 90 Tier 1 claims registered as completely unsourced
    while every one of those 90 claims cited a real primary URL - the DIA 9 Jan
    2018 AATIP list, 10 U.S.C. 119 on uscode.house.gov, the released DIRD PDFs,
    committee pages on house.gov and senate.gov.

    Nothing here is new research and no claim gains a source it did not already
    cite. This only stops the node from disclaiming what it is standing on.
    """
    hoisted = 0
    for n in list(people.values()) + list(entities.values()):
        have = {s.get("url") for s in n.get("sources") or [] if s.get("url")}
        for c in n.get("claims") or []:
            raw = c.get("source") or ""
            for u in URL_IN_SOURCE.findall(raw):
                u = u.rstrip(".,;")
                if u in have:
                    continue
                have.add(u)
                # the source string minus its URLs and minus any demotion note is
                # the human name for the record; fall back to the host.
                name = DEMOTION_NOTE.sub("", URL_IN_SOURCE.sub("", raw))
                name = re.sub(r"\s+", " ", name).strip(" ,;-\u2014")
                if len(name) < 8:
                    name = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
                n.setdefault("sources", []).append({"name": name, "url": u, "date": None})
                hoisted += 1
    return hoisted


def tier1_cap_reason(c, urls):
    """Why a Tier 1 claim may not stay Tier 1, or None. `urls` is every URL the
    claim's owner stands on (a node's sources; a dossier's claim sources).

    One function, because the same rule now reaches two kinds of object: node
    claims here, and entity-dossier claims where build_l0.py loads them (phase 3
    decision 5). Before that the dossiers shipped 40 Tier 1 claims cited to a
    secondary source and 22 cited to AARO/DoD for an outside fact."""
    if c.get("tier") != 1:
        return None
    src = c.get("source") or ""
    if SECONDARY_PAT.search(src):
        return "cited to a secondary/encyclopedic source"
    if src.strip().lower().startswith("no attributed source"):
        return "no attributed source"
    if not PRIMARY_URL_PAT.search(urls) and SECONDARY_PAT.search(urls):
        return "node carries no primary-record URL"
    if (INTERESTED_PARTY_PAT.search(src)
            and not ATTRIBUTION_PAT.search(c.get("text") or "")):
        return ("sourced to an interested party (AARO/DoD) asserting an external "
                "fact; primary record of the statement, not of the fact")
    return None


def remediate_tiers(people, entities):
    """Demote Tier 1 claims that no primary record actually backs.

    This is the honesty pass. A Tier 1 claim is a promise that a primary record
    exists; if the only thing behind it is an encyclopedia entry or a video, the
    promise is false and the whole board becomes dismissible on that one thread.
    Demoted claims are flagged in place so they land in a re-sourcing queue
    rather than quietly disappearing.
    """
    for n in list(people.values()) + list(entities.values()):
        urls = " ".join(s.get("url", "") for s in n.get("sources", []))
        for c in n.get("claims", []):
            why = tier1_cap_reason(c, urls)
            if why:
                c["tier"] = 2
                if "needs primary" not in c["source"].lower():
                    c["source"] = f"{c['source']} — DEMOTED from Tier 1 ({why}); needs primary replacement"
                demotions.append({"id": n["id"], "why": why, "claim": c["text"][:110]})
    return demotions


edge_demotions = []
removed_claims = []   # claims a _corrections.json removeClaims rule took off the board
date_conflicts = []   # entities two files date differently, where neither is coarser


def remediate_edge_tiers(edges):
    """Apply the honesty pass to edges, which it never covered.

    An edge's claimTier renders on the board as "Tier 1 - documented" and the
    board's own copy calls Tier 1 "what survives a hostile audit". That is the
    same promise a claim's Tier 1 makes. But remediate_tiers() above walks
    people and entities only: edge claimTier is whatever the research authored,
    merged across duplicates by min() and audited by nothing. So 93 edges shipped
    labelled "documented" on the strength of a Wikipedia article, a YouTube video
    or a blogspot post and no primary record anywhere -- among them George Knapp
    to Harry Reid, Leslie Kean to David Grusch, and every UAP Gerb investigation
    edge on the board.

    Only the secondary-source rule is carried over, and deliberately so:

    - SECONDARY_PAT with no primary URL anywhere on the edge is unambiguous. An
      encyclopedia entry is not a primary record whatever it says, and this is
      exactly the rule the claims pass already enforces.

    - The interested-party rule is NOT carried over. It works on claims because
      claim text is a single assertion, so ATTRIBUTION_PAT can ask whether the
      claim is about what the interested party said. An edge's note is a
      summary of a relationship, and the same test misreads it: it would demote
      `aaro -> aaro-fy2023-annual-report`, which is an office publishing its own
      report and is a primary record by definition, along with notes phrased
      "AARO disclosed", "AARO confirms" and "AARO's own words" that are
      attribution the verb list happens not to name. 49 edges would be demoted
      that way and most of them wrongly. Capping them needs a per-edge reading,
      not a regex, so it stays a research question rather than a build rule.

    Demoted edges land in tools/EDGE-DEMOTIONS.json, beside DEMOTIONS.json, so the
    re-sourcing queue is a file rather than an annotation. The claims pass writes
    its flag into claim.source; the edge analogue would be the note, and the gate
    already holds that an edge note carries only what the edge asserts -- a
    demotion is editing history, the same category as the collapse provenance
    that was stripped out of twelve notes.
    """
    for e in edges.values():
        if e.get("claimTier") != 1:
            continue
        srcs = e.get("sources") or []
        urls = " ".join(s.get("url") or "" for s in srcs)
        named = " ".join(((s.get("name") or "") + " " + (s.get("url") or "")) for s in srcs)
        if PRIMARY_URL_PAT.search(urls) or not SECONDARY_PAT.search(named):
            continue
        why = "cited to a secondary/encyclopedic source with no primary record"
        e["claimTier"] = 2
        edge_demotions.append({"a": e["a"], "b": e["b"], "type": e["type"], "why": why,
                               "note": (e.get("note") or "")[:110],
                               "sources": [s.get("url") or s.get("name") or ""
                                           for s in e.get("sources") or []]})
    return edge_demotions


# Attribution verbs that read naturally in an EDGE note and not in a claim. The
# claims list is speech verbs; an edge note about a memorandum says the memorandum
# "establishes", "disestablished", "directed", "transmitted". Kept separate so the
# claims rule does not widen by accident.
EDGE_ATTRIBUTION_PAT = re.compile(
    r"\b(disclosed|confirm(?:s|ed|ing)?|refers|treats|conclude[sd]|establishe[sd]|disestablished|"
    r"directed|signed|transmitted|links?|carries|attested|rejects|approved|"
    r"appropriated|issued|told|conducted|commits|places)\b|"
    r"own words|'[^']{12,}'", re.I)


def _edge_key(e):
    return (e.get("a"), e.get("b"), e.get("type"))


def load_edge_adjudications():
    """research/_edge_tiers.json: per-edge decisions on the interested-party rule.

    A dict keyed by (a, b, type) -> record. Missing file means no adjudications,
    which is a valid state; a malformed file is not, and fails the build."""
    path = os.path.join(RESEARCH, "_edge_tiers.json")
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path, encoding="utf-8"))
    out = {}
    for rec in doc.get("edges") or []:
        k = (rec.get("a"), rec.get("b"), rec.get("type"))
        if not all(k) or rec.get("tier") not in (1, 2, 3) or not rec.get("why"):
            sys.exit(f"research/_edge_tiers.json: malformed record {rec!r}")
        out[k] = rec
    return out


def remediate_interested_party_edges(edges, adjudications):
    """The AARO/DoD cap, on edges, the way CLAUDE.md section 2 states it.

    Until 1 September 2026 this rule ran on node claims only, and the docstring
    above says why: a regex misreads an edge note, because an office publishing
    its own report is a primary record and no verb list says so. That reasoning
    was right about the regex and wrong about the conclusion. 82 edges sat at
    Tier 1 with every source on aaro.mil, defense.gov or war.gov and nothing had
    adjudicated any of them; four of them were the board's own domain-to-domain
    inferences wearing "documented".

    So: an edge whose EVERY source is an interested-party domain keeps Tier 1 only
    if its note attributes (the claims verb list plus EDGE_ATTRIBUTION_PAT plus a
    quoted phrase), or if a person has adjudicated it in research/_edge_tiers.json.
    Anything else is capped at Tier 2 and lands in EDGE-DEMOTIONS.json. An
    adjudication can also LOWER a tier, which is how the four inferences became
    Tier 3. verify.py re-derives this independently."""
    for e in edges.values():
        adj = adjudications.get(_edge_key(e))
        if adj:
            if e.get("claimTier") != adj["tier"]:
                edge_demotions.append({"a": e["a"], "b": e["b"], "type": e["type"],
                                       "why": "adjudicated in research/_edge_tiers.json: "
                                              + adj["why"][:120],
                                       "from": e.get("claimTier"), "to": adj["tier"]})
                e["claimTier"] = adj["tier"]
            continue
        if e.get("claimTier") != 1:
            continue
        urls = [s.get("url") or "" for s in (e.get("sources") or [])]
        if not urls or not all(INTERESTED_PARTY_PAT.search(u) for u in urls):
            continue
        note = e.get("note") or ""
        if ATTRIBUTION_PAT.search(note) or EDGE_ATTRIBUTION_PAT.search(note):
            continue
        e["claimTier"] = 2
        edge_demotions.append({"a": e["a"], "b": e["b"], "type": e["type"],
                               "why": "sourced only to an interested party (AARO/DoD) and "
                                      "the note does not attribute; adjudicate in "
                                      "research/_edge_tiers.json to restore",
                               "note": note[:110], "sources": urls})
    return edge_demotions


DUP_STOP = {"the", "of", "a", "an", "and", "for", "to", "on", "in", "act", "section",
            "sec", "us", "u", "s", "united", "states", "department", "office",
            "program", "programme", "inc", "llc", "corporation"}


def _dup_key(label):
    t = unicodedata.normalize("NFKD", label or "").lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    return frozenset(w for w in t.split() if w and w not in DUP_STOP)


def duplicate_groups(people, entities):
    """Find nodes that are probably the same thing recorded twice.

    Five people were once on this board twice, splitting their edges and their
    sources, and nothing detected it. The same failure is back in the entities:
    the FY2024 NDAA sec. 1687 is here three times, the AARO FY2025 annual report
    three times, and Jesse Marcel twice. A duplicate is worse than a missing node,
    because both copies look sourced and each carries a fraction of the evidence
    under a different tier.

    The test is deliberately narrow, to stay useful rather than noisy: same class,
    at least one shared source URL, and label token-sets that overlap by 60% after
    dropping structural words. Two genuinely distinct documents that share a title
    -- DIA-08-1011-003 and -004 are both called 'Aneutronic Fusion Propulsion' --
    will show up here, which is correct: a reader cannot tell them apart either.
    """
    import itertools
    from collections import defaultdict
    nodes = list(people.values()) + list(entities.values())
    byurl = defaultdict(list)
    for n in nodes:
        for src in n.get("sources") or []:
            if src.get("url"):
                byurl[src["url"]].append(n)
    seen, groups = set(), []
    for url, grp in byurl.items():
        if not 2 <= len(grp) <= 40:
            continue
        for a, b in itertools.combinations(grp, 2):
            if a["id"] == b["id"] or a.get("cls") != b.get("cls"):
                continue
            pair = tuple(sorted([a["id"], b["id"]]))
            if pair in seen:
                continue
            ka, kb = _dup_key(a["label"]), _dup_key(b["label"])
            if not ka or not kb:
                continue
            # A detector that cries wolf gets ignored, and then it is no detector.
            # Two labels that both carry an identifier and carry DIFFERENT ones are
            # different things, however alike the surrounding words are. That covers
            # the AARO consolidated annual reports, which are near-identical by title
            # and share a source but are three real reports (FY2023/FY2024/FY2025),
            # and the two DIRDs both titled 'Aneutronic Fusion Propulsion', which are
            # distinguished only by DIA-08-1011-003 vs -004.
            # Match bare digit runs, not \b\d{4}\b: "FY2023" has no word boundary
            # before its digits, which is exactly the case this needs to catch.
            ia = set(re.findall(r"\d{3,}", a["label"] or ""))
            ib = set(re.findall(r"\d{3,}", b["label"] or ""))
            if ia and ib and ia != ib:
                continue
            overlap = len(ka & kb) / len(ka | kb)
            if overlap >= 0.6:
                seen.add(pair)
                groups.append({"a": pair[0], "b": pair[1], "cls": a.get("cls"),
                               "overlap": round(overlap, 2), "shared_url": url})
    groups.sort(key=lambda g: (-g["overlap"], g["a"]))
    return groups


def integrity(people, entities, edges, timeline):
    ids = set(people) | set(entities)
    problems = defaultdict(list)

    dangling = defaultdict(set)
    for e in edges.values():
        for end in (e["a"], e["b"]):
            if end not in ids:
                dangling[end].add(f"{e['a']}->{e['b']}")
    for missing, refs in sorted(dangling.items(), key=lambda kv: -len(kv[1])):
        problems["dangling_edge_endpoint"].append(
            {"missing_id": missing, "ref_count": len(refs), "referenced_by": sorted(refs)[:6]})

    for e in edges.values():
        if not e["sources"]:
            problems["edge_without_source"].append(f"{e['a']}->{e['b']} ({e['type']})")
        if not e["note"]:
            problems["edge_without_note"].append(f"{e['a']}->{e['b']} ({e['type']})")

    for p in people.values():
        if len(p["sources"]) < 2:
            problems["person_thin_sourcing"].append({"id": p["id"], "sources": len(p["sources"])})
            # A node resting on one primary record and a node resting on one blog post
            # are not the same risk, and counting them together made the queue useless:
            # of the 26 that were thin after the w16 pass, nine already stood on govinfo,
            # lanl.gov, The Black Vault, doi.org or Chile's DGAC, and none stood on an
            # encyclopedic source at all. This is the number actually worth working.
            urls = " ".join(s.get("url") or "" for s in p["sources"])
            if not PRIMARY_URL_PAT.search(urls):
                problems["person_single_nonprimary_source"].append(
                    {"id": p["id"], "source": (p["sources"][0].get("url")
                                               if p["sources"] else None)})
        if not p["narrative"]:
            problems["person_without_narrative"].append(p["id"])
        if not p["tierRationale"]:
            problems["person_without_tier_rationale"].append(p["id"])
        if not p["date"]:
            problems["person_without_date"].append(p["id"])
        if p.get("instId") and p["instId"] not in ids:
            problems["person_bad_instId"].append({"id": p["id"], "instId": p["instId"]})
        if p.get("locId") and p["locId"] not in ids:
            problems["person_bad_locId"].append({"id": p["id"], "locId": p["locId"]})
        for d in p.get("domains", []):
            if d not in ids:
                problems["person_bad_domain_ref"].append({"id": p["id"], "domain": d})

    for e in entities.values():
        if not e["desc"]:
            problems["entity_without_desc"].append(e["id"])
        if not e["sources"]:
            problems["entity_without_source"].append(e["id"])

    for t in timeline.values():
        if t.get("node") and t["node"] not in ids:
            problems["timeline_bad_node_ref"].append({"id": t["id"], "node": t["node"]})

    for coll in (people, entities):
        for n in coll.values():
            urls = [s for s in n["sources"] if s.get("url")]
            for c in n.get("claims", []):
                if c["tier"] == 1 and not urls:
                    problems["tier1_claim_no_url"].append({"id": n["id"], "claim": c["text"][:90]})

    for g in duplicate_groups(people, entities):
        problems["probable_duplicate_node"].append(g)

    # Parallel edges: the same node pair joined more than once under different
    # types. An edge key is (a, b, type), so two passes describing one relationship
    # with different vocabulary each get their own edge. Where one twin is sourced
    # and noted at Tier 1 and the other sits unsourced at Tier 3, the unsourced one
    # is redundancy rather than missing research, and it inflates
    # edge_without_source with work that is already done.
    bypair = defaultdict(list)
    for e in edges.values():
        bypair[tuple(sorted([e["a"], e["b"]]))].append(e)
    for pair, group in sorted(bypair.items()):
        if len(group) < 2:
            continue
        sourced = [e for e in group if e["sources"]]
        bare = [e for e in group if not e["sources"]]
        if sourced and bare:
            problems["unsourced_edge_with_sourced_twin"].append({
                "a": pair[0], "b": pair[1],
                "unsourced": [e["type"] for e in bare],
                "sourced": [e["type"] for e in sourced]})

    deg = defaultdict(int)
    for e in edges.values():
        deg[e["a"]] += 1
        deg[e["b"]] += 1
    for n in list(people.values()) + list(entities.values()):
        if n.get("tier") == "A" and deg[n["id"]] < 3:
            problems["tierA_underconnected"].append({"id": n["id"], "degree": deg[n["id"]]})

    return problems, deg



def emit(people, entities, edges, timeline, entity_info, gaps, problems):
    os.makedirs(DATA, exist_ok=True)
    # ---- the denial adjudication ------------------------------------------
    # data/denial-adjudication.json carries a verdict for every denial edge:
    # which of the three states it is, and where the record names an issuer,
    # which END issued it. Stamped on here so every downstream stage -- build_l0,
    # the extract, the layout model, the renderer -- reads one adjudicated
    # record rather than re-deriving direction from [a,b].sort(), which is what
    # put 22 of the 47 arrowheads on the map the wrong way round.
    #
    # Keyed on the edge's own two ends in record order. A verdict whose key
    # matches no edge is an error, not a no-op: it means the research moved and
    # the adjudication did not follow, and a silently ignored verdict would leave
    # that edge reading as undirected for ever.
    adj_path = os.path.join(ROOT, "data", "denial-adjudication.json")
    if os.path.exists(adj_path):
        with open(adj_path, encoding="utf-8") as fh:
            raw_adj = (json.load(fh) or {}).get("edges") or {}
        # Verdict keys follow a collapse exactly as edges do (phase 3 decision 4).
        # Three verdicts were keyed on collapsed ids (cia-haines-1997 twice,
        # sue-gough) and matched nothing, which only ever printed a warning.
        adj = {}
        for k, r in raw_adj.items():
            ends = [EI_ALIAS.get(x, x) for x in k.split("|")]
            adj["|".join(ends)] = r
        matched = set()
        for e in edges.values():
            if e["type"] != "denial":
                continue
            r = adj.get(f"{e['a']}|{e['b']}") or adj.get(f"{e['b']}|{e['a']}")
            if not r:
                continue
            matched.add(f"{e['a']}|{e['b']}")
            e["denialKind"] = r.get("denialKind")
            if r.get("denier"):
                e["denier"] = r["denier"]
        stray = [k for k in adj if k not in matched
                 and "|".join(reversed(k.split("|"))) not in matched]
        if stray and not MERGE_JSON_OUT:
            # A hard error since phase 3. The pristine merge regrade.py runs is
            # exempt: it omits the overlay on purpose, and the real merge that
            # follows it is where this is enforced.
            sys.exit(f"merge.py: {len(stray)} denial verdict(s) in data/denial-adjudication.json "
                     f"match no edge on the board, even through research/_removed.json's "
                     f"aliases: {stray[:6]}. The research moved and the adjudication did "
                     f"not follow; re-key or remove the verdict.")

    # Every denial edge the adjudication does not reach, listed. A report in phase
    # 3; the check that reads it fails once phase R has cleared them.
    for e in edges.values():
        if e["type"] == "denial" and not e.get("denialKind"):
            unadjudicated_denials.append({"a": e["a"], "b": e["b"], "label": e.get("label") or "",
                                          "authoredVerb": e.get("authoredVerb")})
    unadjudicated_denials.sort(key=lambda r: (r["a"], r["b"]))

    # The authored chip shorts in data/l0-shorts.json are display labels too. The
    # three stages that read that register (build_l0.py, build_l0_layout.mjs,
    # build_app_data.py) apply the same rule; the record of it is kept here with
    # the rest, so tools/DISPLAY-NORMALISED.json is the one list.
    sp = os.path.join(ROOT, "data", "l0-shorts.json")
    if os.path.exists(sp):
        for k, v in sorted(((json.load(open(sp, encoding="utf-8")) or {}).get("shorts") or {}).items()):
            display_label(v, "l0-shorts.short", k)

    os.makedirs(OUT, exist_ok=True)
    from datetime import date as _d
    today = _d.today().isoformat()

    # Pristine mode: one scratch JSON, nothing else. Writing data/ here would
    # clobber the real build outputs with an un-remediated board.
    if MERGE_JSON_OUT:
        tl = sorted(timeline.values(), key=lambda t: str(t.get("date") or ""))
        os.makedirs(os.path.dirname(os.path.abspath(MERGE_JSON_OUT)), exist_ok=True)
        with open(MERGE_JSON_OUT, "w", encoding="utf-8") as f:
            json.dump({"generated": today, "people": list(people.values()),
                       "entities": list(entities.values()), "edges": list(edges.values()),
                       "timeline": tl, "entityInfo": entity_info}, f, indent=1,
                      ensure_ascii=False)
        print(f"[pristine] wrote {MERGE_JSON_OUT} only, no board, no reports",
              file=sys.stderr)
        return today

    tl = sorted(timeline.values(), key=lambda t: str(t.get("date") or ""))

    with open(os.path.join(DATA, "the-program.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": today, "people": list(people.values()),
                   "entities": list(entities.values()), "edges": list(edges.values()),
                   "timeline": tl, "entityInfo": entity_info}, f, indent=1, ensure_ascii=False)

    for fn, obj in (("INTEGRITY.json", dict(problems)), ("REJECTS.json", rejects),
                    ("GAPS.json", gaps), ("DEMOTIONS.json", demotions),
                    ("EDGE-DEMOTIONS.json", edge_demotions),
                    ("REMOVED-CLAIMS.json", removed_claims),
                    ("DATE-CONFLICTS.json", date_conflicts),
                    ("UNADJUDICATED-DENIALS.json", unadjudicated_denials),
                    ("UNPLACED-CLAIMS.json", {"claims": unplaced_claims,
                                              "sources": unplaced_sources}),
                    ("DISPLAY-NORMALISED.json", display_normalised),
                    ("SCHEMA-WARNINGS.json", schema_warnings),
                    ("ENTITYINFO-KEYS.json", entity_info_keys)):
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False)
    return today


def main():
    people, entities, edges, timeline, entity_info, gaps = load()
    hoisted = hoist_claim_urls(people, entities)
    remediate_tiers(people, entities)
    remediate_edge_tiers(edges)
    remediate_interested_party_edges(edges, load_edge_adjudications())
    problems, deg = integrity(people, entities, edges, timeline)
    today = emit(people, entities, edges, timeline, entity_info, gaps, problems)

    print(f"=== THE PROGRAM — merge {today} ===")
    print(f"people    {len(people)}")
    print(f"entities  {len(entities)}")
    by = defaultdict(int)
    for e in entities.values():
        by[e["cls"]] += 1
    for k in sorted(by, key=lambda x: -by[x]):
        print(f"    {k:12s} {by[k]}")
    print(f"edges     {len(edges)}")
    bt = defaultdict(int)
    for e in edges.values():
        bt[e["type"]] += 1
    for k in sorted(bt, key=lambda x: -bt[x]):
        print(f"    {k:14s} {bt[k]}")
    ct = defaultdict(int)
    srcs = set()
    for n in list(people.values()) + list(entities.values()):
        for c in n.get("claims", []):
            ct[c["tier"]] += 1
        for s in n.get("sources", []):
            if s.get("url"):
                srcs.add(s["url"])
    for e in edges.values():
        for s in e.get("sources", []):
            if s.get("url"):
                srcs.add(s["url"])
    print(f"claims    T1={ct[1]}  T2={ct[2]}  T3={ct[3]}  (total {sum(ct.values())})")
    print(f"unique source URLs  {len(srcs)}")
    print(f"timeline  {len(timeline)}")
    print(f"gaps      {len(gaps)}   rejects {len(rejects)}")
    print(f"hoisted URLs      {hoisted}  (claim.source -> node.sources)")
    print(f"tier-1 demotions  {len(demotions)}  (tools/DEMOTIONS.json)")
    print("\n--- integrity ---")
    for k in sorted(problems, key=lambda x: -len(problems[x])):
        print(f"  {k:32s} {len(problems[k])}")
    print("\n--- most connected ---")
    for nid, d in sorted(deg.items(), key=lambda kv: -kv[1])[:20]:
        print(f"  {d:4d}  {nid}")


if __name__ == "__main__":
    main()
