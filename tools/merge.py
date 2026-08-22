#!/usr/bin/env python3
"""
merge.py — assemble per-domain research JSON into The Vanishing's JS data shape.

Reads:  research/*.json   (one per domain, written by the research agents)
Writes: data/*.js         (PEOPLE, entity arrays, PROGRAM_EDGES, ENTITY_INFO,
                           ENTITY_SOURCES, TIMELINE) + data/the-program.json

Conservative by design: duplicate ids MERGE rather than overwrite, and nothing
is dropped silently. Unplaceable records land in tools/REJECTS.json with a reason.
"""

import json, os, re, sys, glob
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
# touching data/*.js or the tools/*.json reports.
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


VALID_CLS = {"person", "institution", "program", "location", "domain",
             "legislation", "document", "event"}
VALID_EDGE = {"institutional", "geographic", "research", "temporal", "behavioral",
              "programmatic", "investigative", "witness-chain", "custody",
              "funding", "denial", "legislative"}
VALID_TIER = {"A", "B", "C"}
VALID_CLUSTER = {"legacy", "contractor", "ffrdc", "ic", "oversight", "witness",
                 "research", "media", "other"}
VALID_STRAND = {"program", "witness", "oversight", "coverup"}
VALID_PRECISION = {"day", "month", "year", "ranged"}

rejects = []


def reject(kind, obj, why):
    rejects.append({"kind": kind, "why": why,
                    "id": obj.get("id") or f"{obj.get('a')}->{obj.get('b')}" if isinstance(obj, dict) else str(obj)[:80]})


def norm_source(s):
    if not isinstance(s, dict):
        return None
    name = s.get("name") or s.get("label") or s.get("title")
    url = s.get("url")
    date = s.get("date") or s.get("verified") or None
    if not name and not url:
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
        return None
    t = c.get("tier")
    if isinstance(t, str):
        t = {"documented": 1, "sworn": 2, "reported": 2, "alleged": 3}.get(t.lower(), 3)
    try:
        t = int(t)
    except (TypeError, ValueError):
        t = 3
    if t not in (1, 2, 3):
        t = 3
    text = c.get("text") or c.get("claim")
    if not text:
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


def norm_chron(lst):
    out = []
    for c in lst or []:
        if not isinstance(c, dict):
            continue
        d, ev = c.get("date"), (c.get("event") or c.get("label"))
        if not d or not ev:
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


def _merge_claims(a, b):
    seen = {re.sub(r"\W+", "", c["text"].lower())[:120] for c in a.get("claims", [])}
    for c in b.get("claims") or []:
        k = re.sub(r"\W+", "", c["text"].lower())[:120]
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


def merge_person(a, b):
    _better_label(a, b)
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
    for f in ("cluster", "sub", "dateStart", "dateEnd"):
        if not a.get(f) and b.get(f):
            a[f] = b[f]
    if len(str(b.get("desc") or "")) > len(str(a.get("desc") or "")):
        a["desc"] = b["desc"]
    _merge_common(a, b)
    return a


def load():
    people, entities, edges, timeline = OrderedDict(), OrderedDict(), OrderedDict(), OrderedDict()
    entity_info, gaps = {}, []

    # _remediation must land last: it is an authoritative overlay that OVERRIDES
    # the merge rules (which otherwise take the strongest tier and would undo a
    # deliberate demotion). _stubs lands second-to-last so real dossiers win over stubs.
    allf = glob.glob(os.path.join(RESEARCH, "*.json"))
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
            rec = {
                "id": pid, "cls": "person",
                "label": p.get("label") or p.get("name") or pid,
                "status": p.get("status") or "active",
                "date": p.get("date"), "age": p.get("age"),
                "loc": p.get("loc"),
                "locId": canonical_id(p.get("locId")), "instId": canonical_id(p.get("instId")),
                "sub": p.get("sub"),
                "cluster": p.get("cluster") if p.get("cluster") in VALID_CLUSTER else "other",
                "tier": p.get("tier") if p.get("tier") in VALID_TIER else "C",
                "C": clamp_axis(p.get("C")), "A": clamp_axis(p.get("A")), "D": clamp_axis(p.get("D")),
                "domains": p.get("domains") or [],
                "narrative": p.get("narrative") or "",
                "affiliations": p.get("affiliations") or [],
                "tierRationale": p.get("tierRationale") or "",
                "chronology": norm_chron(p.get("chronology")),
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
                        tgt[f] = p[f]
                # membership test, not truthiness: an explicit null or [] is the
                # correction in every case where the old value should simply go.
                for f in ("locId", "instId", "domains", "affiliations", "sequenceChain"):
                    if f in p:
                        tgt[f] = rec[f]
                if p.get("sources"):
                    tgt["sources"] = norm_sources(list(p["sources"]) + tgt.get("sources", []))
                if p.get("claims"):
                    tgt["claims"] = norm_claims(p["claims"]) + tgt.get("claims", [])
            elif slug == "_remediation" and pid in people:
                tgt = people[pid]
                for f in ("tier", "tierRationale", "date", "coords"):
                    if p.get(f) is not None:
                        tgt[f] = p[f]
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
            rec = {
                "id": eid, "cls": cls, "label": e.get("label") or eid,
                "cluster": e.get("cluster") if e.get("cluster") in VALID_CLUSTER else "other",
                "sub": e.get("sub"), "desc": e.get("desc") or None,
                "tier": e.get("tier") if e.get("tier") in VALID_TIER else "C",
                "C": clamp_axis(e.get("C")), "A": clamp_axis(e.get("A")), "D": clamp_axis(e.get("D")),
                "dateStart": e.get("dateStart"), "dateEnd": e.get("dateEnd"),
                "coords": e.get("coords"), "locLabel": e.get("locLabel"),
                "tierRationale": e.get("tierRationale") or "",
                "claims": norm_claims(e.get("claims")),
                "sources": norm_sources(e.get("sources")),
                "_domains": [slug],
            }
            if slug == "_corrections" and eid in entities:
                # Corrections are authoritative and may overwrite prose. They exist
                # because a claim on this board turned out not to survive a check,
                # and the record of that has to beat the merge's "longest wins" rule.
                tgt = entities[eid]
                for f in ("label", "desc", "sub", "cluster", "tier"):
                    if e.get(f) is not None:
                        tgt[f] = e[f]
                tgt["sources"] = norm_sources(list(e.get("sources") or []) + tgt.get("sources", []))
                tgt["claims"] = norm_claims(e.get("claims")) + [c for c in tgt.get("claims", [])
                    if "yankee blue" not in c["text"].lower() or c["tier"] != 1]
            elif slug == "_remediation" and eid in entities:
                tgt = entities[eid]
                for f in ("tier", "tierRationale", "coords", "locLabel"):
                    if e.get(f) is not None:
                        tgt[f] = e[f]
            else:
                entities[eid] = merge_entity(entities[eid], rec) if eid in entities else rec

        for x in doc.get("edges") or []:
            a_ = canonical_id(x.get("a") or x.get("from"))
            b_ = canonical_id(x.get("b") or x.get("to"))
            t = x.get("type") or x.get("rel")
            if not a_ or not b_:
                reject("edge", x, "missing endpoint")
                continue
            if t not in VALID_EDGE:
                t = "programmatic"
            key, rkey = f"{a_}|{b_}|{t}", f"{b_}|{a_}|{t}"
            if rkey in edges:
                key = rkey
            ct = x.get("claimTier")
            ct = ct if ct in (1, 2, 3) else 3
            rec = {"a": a_, "b": b_, "type": t, "label": x.get("label") or "",
                   "claimTier": ct, "dateStart": x.get("dateStart"), "dateEnd": x.get("dateEnd"),
                   "note": x.get("note") or x.get("summary") or "",
                   "sources": norm_sources(x.get("sources")), "_domains": [slug]}
            if key in edges:
                old = edges[key]
                if len(rec["note"]) > len(old["note"]):
                    old["note"] = rec["note"]
                if not old["label"]:
                    old["label"] = rec["label"]
                old["claimTier"] = min(old["claimTier"], rec["claimTier"])
                old["sources"] = norm_sources(old["sources"] + rec["sources"])
                for d in rec["_domains"]:
                    if d not in old["_domains"]:
                        old["_domains"].append(d)
            else:
                edges[key] = rec

        seen_tl = {(v.get("date"), (v.get("label") or "")[:50]) for v in timeline.values()}
        for t in doc.get("timeline") or []:
            if t.get("strand") not in VALID_STRAND:
                t["strand"] = "program"
            if t.get("precision") not in VALID_PRECISION:
                t["precision"] = ("day" if re.match(r"^\d{4}-\d{2}-\d{2}$", str(t.get("date", "")))
                                  else "year")
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
            k = canonical_id(k)
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
        swept = 0
        for p_ in people.values():
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
    r"nsf\.gov|nasa\.gov|patents\.google|uspto\.gov|doi\.org|"
    # other governments, all of them already cited on this board
    r"nationalarchives\.gov\.uk|\.gov\.uk|\.gc\.ca|\.gob\.cl|\.gov\.br|"
    r"leg\.br|\.gouv\.fr|legifrance|europa\.eu|"
    # third-party hosts of released government documents
    r"theblackvault\.com|irp\.fas\.org", re.I)

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
ATTRIBUTION_PAT = re.compile(
    r"\b(denie[ds]|denial|declined|stated|states|said|asserts?|asserted|claims|"
    r"claimed|announced|acknowledg|concluded|reported that|wrote|testified|"
    r"responded|maintains?|characteri[sz]ed|according to (?:aaro|the )?(?:dod|"
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
        has_primary = bool(PRIMARY_URL_PAT.search(urls))
        for c in n.get("claims", []):
            if c["tier"] != 1:
                continue
            src = c.get("source") or ""
            why = None
            if SECONDARY_PAT.search(src):
                why = "cited to a secondary/encyclopedic source"
            elif src.strip().lower().startswith("no attributed source"):
                why = "no attributed source"
            elif not has_primary and SECONDARY_PAT.search(urls):
                why = "node carries no primary-record URL"
            elif (INTERESTED_PARTY_PAT.search(src)
                  and not ATTRIBUTION_PAT.search(c.get("text") or "")):
                why = ("sourced to an interested party (AARO/DoD) asserting an external "
                       "fact; primary record of the statement, not of the fact")
            if why:
                c["tier"] = 2
                if "needs primary" not in c["source"].lower():
                    c["source"] = f"{c['source']} — DEMOTED from Tier 1 ({why}); needs primary replacement"
                demotions.append({"id": n["id"], "why": why, "claim": c["text"][:110]})
    return demotions


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

    deg = defaultdict(int)
    for e in edges.values():
        deg[e["a"]] += 1
        deg[e["b"]] += 1
    for n in list(people.values()) + list(entities.values()):
        if n.get("tier") == "A" and deg[n["id"]] < 3:
            problems["tierA_underconnected"].append({"id": n["id"], "degree": deg[n["id"]]})

    return problems, deg


def js(v, indent=0):
    pad = "  " * indent
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ") + "'"
    if isinstance(v, list):
        if not v:
            return "[]"
        if all(isinstance(x, str) for x in v):
            inner = ", ".join(js(x) for x in v)
            if len(inner) < 100:
                return "[" + inner + "]"
        return "[\n" + ",\n".join(pad + "  " + js(x, indent + 1) for x in v) + "\n" + pad + "]"
    if isinstance(v, dict):
        items = [(k, x) for k, x in v.items() if not k.startswith("_")]
        if not items:
            return "{}"
        parts = []
        for k, x in items:
            key = k if re.match(r"^[A-Za-z_$][\w$]*$", k) else js(k)
            parts.append(f"{key}: {js(x, indent + 1)}")
        one = "{ " + ", ".join(parts) + " }"
        if len(one) < 110 and not any(isinstance(x, (list, dict)) and x for _, x in items):
            return one
        return "{\n" + ",\n".join(pad + "  " + p for p in parts) + "\n" + pad + "}"
    return js(str(v))


HEADER = """/* THE PROGRAM — {name}
   Generated by tools/merge.py from research/*.json on {date}.
   Schema: SCHEMA.md. Companion board to The Vanishing.

   Built from the premise that a legacy recovery and reverse-engineering program
   exists and has been concealed. Official denials are recorded as artifacts of
   the concealment effort, not as counterweights.
   Claim tiers: 1 documented, 2 sourced claim, 3 inference.
*/

"""


def emit(people, entities, edges, timeline, entity_info, gaps, problems):
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    from datetime import date as _d
    today = _d.today().isoformat()

    # Pristine mode: one scratch JSON, nothing else. Writing data/*.js here would
    # clobber the real build outputs with an un-remediated board.
    if MERGE_JSON_OUT:
        tl = sorted(timeline.values(), key=lambda t: str(t.get("date") or ""))
        os.makedirs(os.path.dirname(os.path.abspath(MERGE_JSON_OUT)), exist_ok=True)
        with open(MERGE_JSON_OUT, "w", encoding="utf-8") as f:
            json.dump({"generated": today, "people": list(people.values()),
                       "entities": list(entities.values()), "edges": list(edges.values()),
                       "timeline": tl, "entityInfo": entity_info}, f, indent=1,
                      ensure_ascii=False)
        print(f"[pristine] wrote {MERGE_JSON_OUT} only — no .js, no reports",
              file=sys.stderr)
        return today

    def write(fn, name, body):
        with open(os.path.join(DATA, fn), "w", encoding="utf-8") as f:
            f.write(HEADER.format(name=name, date=today))
            f.write(body)

    write("program-people.js", "PEOPLE",
          "export const PEOPLE = [\n" + ",\n".join("  " + js(p, 1) for p in people.values()) + "\n];\n")

    by_cls = defaultdict(list)
    for e in entities.values():
        by_cls[e["cls"]].append(e)
    varname = {"institution": "INSTITUTIONS", "program": "PROGRAMS", "location": "LOCATIONS",
               "domain": "DOMAINS", "legislation": "LEGISLATION", "document": "DOCUMENTS",
               "event": "EVENTS"}
    body = ""
    for cls, var in varname.items():
        body += (f"export const {var} = [\n"
                 + ",\n".join("  " + js(r, 1) for r in by_cls.get(cls, [])) + "\n];\n\n")
    body += ("export const ENTITIES = [...INSTITUTIONS, ...PROGRAMS, ...LOCATIONS, "
             "...DOMAINS, ...LEGISLATION, ...DOCUMENTS, ...EVENTS];\n")
    write("program-entities.js", "ENTITIES", body)

    write("program-edges.js", "PROGRAM_EDGES",
          "export const PROGRAM_EDGES = [\n" + ",\n".join("  " + js(e, 1) for e in edges.values()) + "\n];\n")

    write("program-entity-info.js", "ENTITY_INFO / ENTITY_SOURCES",
          "export const ENTITY_INFO = "
          + js({k: {"desc": v.get("desc")} for k, v in entity_info.items()}, 0)
          + ";\n\nexport const ENTITY_SOURCES = "
          + js({k: v.get("sources", []) for k, v in entity_info.items()}, 0) + ";\n")

    tl = sorted(timeline.values(), key=lambda t: str(t.get("date") or ""))
    write("program-timeline.js", "TIMELINE",
          "export const TIMELINE = [\n" + ",\n".join("  " + js(t, 1) for t in tl) + "\n];\n")

    with open(os.path.join(DATA, "the-program.json"), "w", encoding="utf-8") as f:
        json.dump({"generated": today, "people": list(people.values()),
                   "entities": list(entities.values()), "edges": list(edges.values()),
                   "timeline": tl, "entityInfo": entity_info}, f, indent=1, ensure_ascii=False)

    for fn, obj in (("INTEGRITY.json", dict(problems)), ("REJECTS.json", rejects),
                    ("GAPS.json", gaps), ("DEMOTIONS.json", demotions)):
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False)
    return today


def main():
    people, entities, edges, timeline, entity_info, gaps = load()
    hoisted = hoist_claim_urls(people, entities)
    remediate_tiers(people, entities)
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
