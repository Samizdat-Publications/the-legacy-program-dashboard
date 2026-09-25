#!/usr/bin/env python3
"""
verify.py — assert things about the board that a human would otherwise have to notice.

WHY THIS EXISTS
---------------
On 2026-08-12 a QA pass found four BROKEN-severity defects in a board that had been
"verified". Every one of them was invisible to the verification that existed:

  * 35 dates were replaced with null on every rebuild        -> valid JSON, no error
  * five people were on the board twice, one rendering
    its own slug as its display name                          -> valid nodes, no error
  * thirteen person plates read "JR., J." or "(SAM), '."      -> rendered fine, just wrong
  * the DETAIL panel stated the wrong number of classes       -> rendered fine, just false

The verification was `shoot.js`: screenshot the views, collect console errors, report
zero. That checks *that nothing threw*. None of these threw. A board can be completely
wrong and completely quiet.

Worse, the one check `shoot.js` had that could have caught something real — `canvasInk`,
meant to catch a blank canvas — was itself broken. It reported 0 ink on a canvas that was
visibly drawing, because the renderer is WebGL and `getImageData` returns empty without
`preserveDrawingBuffer`. It had never once failed, and nobody noticed, because a check
that always passes and a check that always says zero look identical from the outside.

So this file follows two rules:

  1. EVERY CHECK ASSERTS A FACT, and fails the build with a non-zero exit when the fact
     is false. Reporting is not verifying.
  2. EVERY CHECK IS ITSELF TESTED. `--self-test` feeds each check input it must reject.
     A check that cannot be shown to fail is not evidence of anything. This is the
     direct lesson of canvasInk and it is not optional.

Usage:
    python3 tools/verify.py                # assert the current build
    python3 tools/verify.py --self-test    # prove every check can fail
    python3 tools/verify.py --update-golden  # deliberately accept new counts
"""

import json, os, re, sys, subprocess, hashlib, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from merge import canonical_id  # noqa: E402

BOARD = os.path.join(ROOT, "data", "the-program.json")
GOLDEN = os.path.join(ROOT, "tools", "GOLDEN.json")

FAILURES = []
CHECKS_RUN = []


def check(name):
    """Register a check. The body returns a list of problem strings; empty means pass."""
    def deco(fn):
        CHECKS_RUN.append((name, fn))
        return fn
    return deco


# ---------------------------------------------------------------------------
# structural invariants — these are properties, not counts. They must hold at
# any size, so they never need updating as the research grows.
# ---------------------------------------------------------------------------

@check("ids are canonical")
def _ids_canonical(b):
    """Two spellings of one id put the same person on the board twice, split their
    edges and sources, and — because label falls back to the id — make the twin
    render its own slug as its name. This is exactly what happened to
    p-dylan-borland / dylan-borland."""
    bad = []
    seen = {}
    for n in b["people"] + b["entities"]:
        i = n["id"]
        if canonical_id(i) != i:
            bad.append(f"non-canonical id {i!r} (should be {canonical_id(i)!r})")
        seen.setdefault(canonical_id(i), []).append(i)
    for canon, spellings in seen.items():
        if len(spellings) > 1:
            bad.append(f"{len(spellings)} ids collapse to {canon!r}: {spellings}")
    return bad


@check("no label is its own id")
def _label_not_id(b):
    """merge.py falls back to the id when a record has no label. That fallback
    reaching the screen means a record was invented rather than merged."""
    return [f"{n['id']} displays its own slug as its name"
            for n in b["people"] + b["entities"] if n.get("label") == n["id"]]


@check("person plate names are meaningful")
def _plate_names(b):
    """The plate shows `SURNAME, F.`. A label whose last token is a generational
    suffix rendered five different people as 'JR., J.'. Reproduces the shipped
    formatter's contract rather than trusting it."""
    SUFFIX = re.compile(r"^(jr|sr|ii|iii|iv|v|phd|md|esq|ret)\.?$", re.I)
    TITLE = re.compile(r"^(dr|mr|mrs|ms|prof|maj|gen|col|lt|capt|cmdr|cdr|adm|sgt|rep|sen|hon|brig|gral|general|de|brigada|aérea)\.?$", re.I)
    bad = []
    for p in b["people"]:
        parts = re.sub(r"\([^)]*\)", " ", re.sub(r"[“”‘’\"']", "", p["label"])).split()
        while len(parts) > 1 and SUFFIX.match(parts[-1]):
            parts.pop()
        while len(parts) > 1 and TITLE.match(parts[0]):
            parts.pop(0)
        if not parts:
            bad.append(f"{p['id']}: label {p['label']!r} reduces to nothing")
            continue
        short = (parts[-1] + (", " + parts[0][0] + "." if len(parts) > 1 else "")).upper()
        if SUFFIX.match(parts[-1]) or not re.match(r"^[A-ZÀ-ž]", short):
            bad.append(f"{p['id']}: {p['label']!r} -> {short!r}")
    return bad


@check("no dangling references")
def _dangling(b):
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for e in b["edges"]:
        for side in ("a", "b"):
            if e[side] not in ids:
                bad.append(f"edge {e['a']}->{e['b']} references missing {e[side]!r}")
    for t in b.get("timeline", []):
        if t.get("node") and t["node"] not in ids:
            bad.append(f"timeline {t.get('id')} references missing node {t['node']!r}")
        if t.get("ref") and t["ref"] not in ids:
            bad.append(f"timeline {t.get('id')}.ref references missing {t['ref']!r}")
        for f in ("entities", "nodes", "refs"):
            for x in t.get(f) or []:
                if x not in ids:
                    bad.append(f"timeline {t.get('id')}.{f} references missing {x!r}")
    return bad[:40]


@check("every person back-reference resolves")
def _person_refs(b):
    """A person points at nodes through locId, instId and domains, and deriveEdges()
    turns each one into a live edge at runtime. These are references exactly as much
    as an edge endpoint is, and until this check existed nothing walked them.

    That gap shipped. When 30 location nodes were removed under the approved
    deletion list, the removal dropped the edges that touched them -- because the
    dangling check walked edge endpoints, and satisfying the gate defined the scope
    of the fix. The 31 person.locId back-references pointing at those same nodes
    survived, and the board emitted 31 geographic edges to locations that no longer
    existed. Nothing threw, and 'no dangling references' reported ok on every run."""
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for p in b["people"]:
        for f in ("locId", "instId"):
            if p.get(f) and p[f] not in ids:
                bad.append(f"person {p['id']}.{f} references missing {p[f]!r}")
        for d in p.get("domains") or []:
            if d not in ids:
                bad.append(f"person {p['id']}.domains references missing {d!r}")
    return bad[:40]


@check("no unapproved duplicate nodes")
def _duplicates(b):
    """One object recorded twice is worse than one recorded not at all: both copies
    look sourced, each holds a fraction of the evidence, and they can carry
    different tiers, so the board grades the same thing two ways at once.

    Five people were on this board twice in August. That was fixed by unifying the
    id rules for people, and nothing ever checked the entities. On 22 August the
    FY2024 NDAA sec. 1687 was here three times, the AARO FY2025 annual report three
    times, and Jesse Marcel twice -- nine groups, 19 nodes, splitting about 70 edges
    and 130 claims.

    This computes the groups from the board itself rather than reading merge.py's
    INTEGRITY.json, so it is a property of what shipped and can be self-tested.
    Pairs that genuinely are not duplicates go in tools/DUPLICATES_ACCEPTED.json
    with a reason saying what distinguishes them -- the same deliberate-acceptance
    pattern as the golden manifest. Anything unlisted fails."""
    from merge import duplicate_groups
    from collections import OrderedDict
    people = OrderedDict((n["id"], n) for n in b["people"])
    ents = OrderedDict((n["id"], n) for n in b["entities"])
    acc = os.path.join(ROOT, "tools", "DUPLICATES_ACCEPTED.json")
    ok = set()
    if os.path.exists(acc):
        for row in json.load(open(acc, encoding="utf-8")).get("accepted", []):
            ok.add(tuple(sorted([row["a"], row["b"]])))
    bad = []
    for g in duplicate_groups(people, ents):
        if tuple(sorted([g["a"], g["b"]])) not in ok:
            bad.append(f"{g['a']} and {g['b']} look like one {g.get('cls')} recorded twice "
                       f"(label overlap {g.get('overlap')}); collapse it, or record why it is "
                       f"not a duplicate in tools/DUPLICATES_ACCEPTED.json")
    return bad[:40]


@check("affiliations render as names, not ids")
def _affiliations(b):
    """affiliations is a prose field upstream and is printed verbatim. The research
    here writes node ids into it, so 54 entries reached the dossier as raw slugs:
    a reader saw 'dod-sapco' and 'skidmore-fitts-report' where a name belonged.

    The renderer now resolves an id-shaped entry to that node's label and links it,
    which keeps the graph link instead of throwing it away by rewriting to prose.
    That fix only holds for entries that name a REAL node -- an id-shaped string
    matching nothing falls through to esc() and prints the slug. So the property
    worth asserting is not 'no ids here', it is: every id-shaped entry resolves."""
    ids = {n["id"] for n in b["people"] + b["entities"]}
    slug = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    bad = []
    for p in b["people"]:
        for a in p.get("affiliations") or []:
            if isinstance(a, str) and slug.match(a) and a not in ids:
                bad.append(f"{p['id']}: affiliation {a!r} is id-shaped but names no node, "
                           f"so it prints as the raw slug")
    return bad[:40]


@check("sequence chains are renderable")
def _chain_shape(b):
    """chainHtml() reads s.date, s.event, s.source and s.isAnomalous off every step.
    All 11 chains on this board held bare node-id strings instead of step objects,
    so every one of them rendered an undefined event under an undefined date --
    including Grusch, Elizondo, Davis and Marcel, which are the most-read dossiers
    here. Nothing threw, and no count moved.

    The renderer is inherited from The Vanishing, where a chain step is an ordered,
    dated, individually sourced link. The research wrote program lineages into the
    same field. Both are legitimate objects; only one of them is what this field
    renders, and the field has to hold what the renderer reads."""
    bad = []
    for p in b["people"]:
        for i, s in enumerate(p.get("sequenceChain") or []):
            if not isinstance(s, dict):
                bad.append(f"{p['id']}: chain step {i} is a {type(s).__name__}, not a step object")
            elif not (s.get("date") and s.get("event")):
                bad.append(f"{p['id']}: chain step {i} has no date or no event")
    return bad[:40]


@check("no edge note leaks build bookkeeping")
def _edge_note_bookkeeping(b):
    """An edge note renders in the dock. A reader gets it as the board's statement of
    what the edge asserts, so it must say only that.

    Collapse re-pointing wrote its own provenance into the notes it re-pointed --
    "[Re-pointed from the collapsed duplicate `setka`, 14 Aug 2026.]" and similar.
    That is editing history, not an assertion about the world, and twelve of them
    shipped to readers. They were stripped by hand once before and came back,
    because two of the three collapse files were missed and nothing looked again.

    The provenance is not lost: it lives in research/*-collapse.json and in
    notes/DUPLICATES-2026-08-22.md, which is where a reader who wants the editing
    history should find it."""
    pat = re.compile(r"\[Re-pointed from|collapsed duplicate|Board bookkeeping", re.I)
    bad = []
    for e in b["edges"]:
        note = e.get("note") or ""
        m = pat.search(note)
        if m:
            bad.append(f"edge {e.get('a')}->{e.get('b')} ({e.get('type')}) "
                       f"note carries build bookkeeping: {m.group(0)!r}")
    return bad[:40]


@check("no Tier 1 edge rests only on a secondary source")
def _edge_tier_sourcing(b):
    """An edge's claimTier renders in the dock as "Tier 1 - documented", and the
    board's own copy calls Tier 1 "what survives a hostile audit". That is the
    same promise a claim's Tier 1 makes, and it was audited on one of the two.

    merge.py's remediate_tiers() walks people and entities. Edge claimTier was
    whatever the research authored, merged across duplicates by min() and checked
    by nothing -- so 93 edges shipped labelled "documented" whose only support was
    a Wikipedia article, a YouTube video or a blogspot post. George Knapp to Harry
    Reid, Leslie Kean to David Grusch, every UAP Gerb investigation edge on the
    board. One thread a hostile reader pulls and the grade means nothing anywhere.

    This asserts the rule the claims pass already enforces: an edge may hold Tier 1
    only if some source on it is a primary record, or if none of its sources is
    encyclopedic. It does NOT assert the interested-party rule, which does not
    survive the move from claim text to an edge note -- see remediate_edge_tiers()
    in merge.py for why that one stays a research question."""
    import re as _re
    SECONDARY = _re.compile(r"wikipedia|britannica|\bwiki\b|reddit|substack|medium\.com|"
                            r"youtube|podcast|blog|fandom", _re.I)
    PRIMARY = _re.compile(
        r"congress\.gov|govinfo\.gov|federalregister\.gov|whitehouse\.gov|"
        r"archives\.gov|presidentiallibraries\.us|ecfr\.gov|acquisition\.gov|"
        r"law\.cornell\.edu|courtlistener|\.uscourts\.gov|"
        r"gao\.gov|oversight\.house\.gov|\.senate\.gov|\.house\.gov|docs\.house\.gov|"
        r"\.mil\b|defense\.gov|war\.gov|dni\.gov|odni\.gov|cia\.gov|\.fbi\.gov|"
        r"nsa\.gov|dhs\.gov|energy\.gov|osti\.gov|lanl\.gov|sec\.gov|"
        r"usaspending\.gov|sam\.gov|fpds\.gov|fasab\.gov|foia|"
        r"nsf\.gov|nasa\.gov|cnes\.fr|patents\.google|uspto\.gov|doi\.org|"
        r"nationalarchives\.gov\.uk|\.gov\.uk|\.gc\.ca|\.gob\.cl|\.gov\.br|"
        r"leg\.br|\.gouv\.fr|legifrance|assemblee-nationale\.fr|senat\.fr|europa\.eu|"
        r"theblackvault\.com|irp\.fas\.org|archive\.org/details/DTIC_", _re.I)
    bad = []
    for e in b["edges"]:
        if e.get("claimTier") != 1:
            continue
        srcs = e.get("sources") or []
        urls = " ".join(s.get("url") or "" for s in srcs)
        named = " ".join(((s.get("name") or "") + " " + (s.get("url") or "")) for s in srcs)
        if PRIMARY.search(urls) or not SECONDARY.search(named):
            continue
        m = SECONDARY.search(named)
        bad.append(f"edge {e.get('a')}->{e.get('b')} ({e.get('type')}) is Tier 1 on "
                   f"{m.group(0)!r} with no primary record")
    return bad[:40]


_EDGE_TIERS_OVERRIDE = None


def _edge_tiers():
    """research/_edge_tiers.json, or the poisoned stand-in during --self-test."""
    if _EDGE_TIERS_OVERRIDE is not None:
        return _EDGE_TIERS_OVERRIDE
    path = os.path.join(ROOT, "research", "_edge_tiers.json")
    if not os.path.exists(path):
        return {"edges": []}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@check("no Tier 1 edge rests on an interested party asserting an external fact")
def _edge_interested_party(b):
    """CLAUDE.md section 2: claims sourced to aaro.mil or defense.gov cap at Tier 2
    unless the claim is about what they said. The rule names no carve-out for
    edges, and until 1 September 2026 it had one anyway: remediate_tiers() applied
    it to node claims and remediate_edge_tiers() explicitly did not, on the
    argument that an edge note defeats the attribution regex. The argument was
    right about the regex and wrong about the conclusion -- 82 edges rendered
    "Tier 1 - documented" with every source on an interested-party domain and no
    adjudication behind any of them, four of them the board's own inferences.

    This re-derives the rule independently of merge.py, with its own patterns. An
    edge whose EVERY source is an interested-party domain may hold Tier 1 only if
    its note attributes what the document says, or if research/_edge_tiers.json
    carries a reasoned decision for it. The file is the reviewable half; the regex
    is the mechanical half. An adjudicated edge must ship at its adjudicated tier."""
    import re as _re
    INTERESTED = _re.compile(r"aaro\.mil|(?:^|//|\.)defense\.gov|war\.gov|dvidshub|"
                             r"pentagon\.mil|\bdodcio\b", _re.I)
    ATTR = _re.compile(
        r"\b(denie[ds]|denial|declined|state[sd]|said|assert(?:s|ed)?|claim(?:s|ed)|"
        r"announced|acknowledg\w*|conclude[sd]|reported that|wrote|testified|"
        r"responded|maintains?|characteri[sz]ed|attribute[sd]?|credit(?:s|ed)?|"
        r"list(?:s|ed)?|identifie[sd]|name[sd]|reads|contains?|describe[sd]?|"
        r"print(?:s|ed)?|publishe[sd]|record(?:s|ed)?|shows?|gives?|hosts?|"
        r"disclosed|confirm(?:s|ed|ing)?|refers|treats|establishe[sd]|"
        r"disestablished|directed|signed|transmitted|links?|carries|attested|"
        r"rejects|approved|appropriated|issued|told|conducted|commits|places|"
        r"according to (?:aaro|the )?(?:dod|department of defense|pentagon))\b|"
        r"own words|'[^']{12,}'", _re.I)
    adj = {(r.get("a"), r.get("b"), r.get("type")): r
           for r in (_edge_tiers() or {}).get("edges") or []}
    bad = []
    for e in b["edges"]:
        key = (e.get("a"), e.get("b"), e.get("type"))
        if key in adj:
            want = adj[key].get("tier")
            if e.get("claimTier") != want:
                bad.append(f"edge {key[0]}->{key[1]} ({key[2]}) ships Tier "
                           f"{e.get('claimTier')} but _edge_tiers.json adjudicates {want}")
            continue
        if e.get("claimTier") != 1:
            continue
        urls = [s.get("url") or "" for s in (e.get("sources") or [])]
        if not urls or not all(INTERESTED.search(u) for u in urls):
            continue
        if ATTR.search(e.get("note") or ""):
            continue
        bad.append(f"edge {key[0]}->{key[1]} ({key[2]}) is Tier 1 on interested-party "
                   f"sources only, with a note that does not attribute and no "
                   f"adjudication in research/_edge_tiers.json")
    return bad[:40]


@check("every Tier A node rests on at least one sourced URL")
def _tier_a_sourced(b):
    """regrade.py's centrality() says 'a node with no sources cannot be Tier A' and
    then multiplies the score by 0.35, which is a discount, not an exclusion: a
    node with forty connections and full axis scores could still clear the top
    15% cut with no URL anywhere on it. regrade.py now forces such a node to B;
    this asserts the outcome on the shipped board rather than trusting the pass."""
    bad = []
    for n in b["people"] + b["entities"]:
        if n.get("tier") != "A":
            continue
        if not any((s or {}).get("url") for s in (n.get("sources") or [])):
            bad.append(f"{n['id']} is Tier A with no sourced URL")
    return bad[:40]


@check("claim tiers are valid and Tier 1 is sourced")
def _claims(b):
    """Credibility rule: no claim renders without a confidence treatment, and Tier 1
    means a primary record exists. A Tier 1 with no URL is the single most damaging
    thing this board can ship."""
    bad = []
    for n in b["people"] + b["entities"]:
        for c in n.get("claims", []):
            if c.get("tier") not in (1, 2, 3):
                bad.append(f"{n['id']}: claim with tier {c.get('tier')!r}")
            elif c["tier"] == 1 and not str(c.get("source") or "").strip():
                bad.append(f"{n['id']}: Tier 1 claim with no source")
    return bad[:40]


# ---------------------------------------------------------------------------
# the L0 program map, each check self-tested
#
# These read data/l0-model.json, the build product the app's map data is written
# from. Self-test poisons them through _L0_OVERRIDE, the same channel pattern as
# _LAYOUT_OVERRIDE below.
# ---------------------------------------------------------------------------

L0_MODEL = os.path.join(ROOT, "data", "l0-model.json")
_L0_OVERRIDE = None
_L0_CACHE = []


def _l0():
    """data/l0-model.json, or the poisoned stand-in during --self-test.

    Until 25 September 2026 this parsed the `const L0DATA = ` literal back out of
    the old single-file shell, on the principle that what shipped is the only thing
    worth asserting on. The old shell is retired and the app reads the map from
    app/public/data/, which build_app_data.py writes from this same file and checks
    with --check; so the model file is now the nearest thing to what ships."""
    if _L0_OVERRIDE is not None:
        return _L0_OVERRIDE
    if not _L0_CACHE:
        if not os.path.exists(L0_MODEL):
            return None
        with open(L0_MODEL, encoding="utf-8") as fh:
            _L0_CACHE.append(json.load(fh))
    return _L0_CACHE[0]


@check("register partition is total")
def _l0_partition(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    c = d["counts"]
    total = len(b["people"]) + len(b["entities"])
    got = c["l0"] + c["ledger"] + c["pathOnly"] + c["unattached"]
    bad = []
    if got != total:
        bad.append(f"registers sum to {got}, board has {total} nodes — "
                   f"the partition is not total, so 'nothing was left out' is false")
    # and no id may appear in two registers, or in none
    seen, dupe = {}, []
    for reg, ids in (("l0", [n["id"] for n in d["l0"]]),
                     ("pathOnly", [r["id"] for r in d["pathOnly"]]),
                     ("unattached", [r["id"] for r in d["unattached"]])):
        for i in ids:
            if i in seen:
                dupe.append(f"{i} is in both {seen[i]} and {reg}")
            seen[i] = reg
    bad += dupe[:5]
    if c["l0"] != len(d["l0"]):
        bad.append(f"counts.l0 says {c['l0']}, the l0 array holds {len(d['l0'])}")
    return bad


@check("summarised edge tier is the strongest of its underlying links")
def _l0_tier(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    pair = {}
    for e in b["edges"]:
        pair.setdefault("|".join(sorted((e["a"], e["b"]))), []).append(e)
    bad = []
    for e in d["summarised"]:
        want = 9
        for v in e["via"]:
            for end in (e["a"], e["b"]):
                for h in pair.get("|".join(sorted((end, v))), []):
                    want = min(want, h["claimTier"])
        if want != 9 and e["tier"] != want:
            bad.append(f"summarised {e['a']}~{e['b']} prints tier {e['tier']}, "
                       f"strongest underlying link is tier {want}")
        # the tick count IS the shared-member count; they cannot disagree
        if e["n"] != len(e["via"]):
            bad.append(f"summarised {e['a']}~{e['b']} claims {e['n']} shared members "
                       f"but lists {len(e['via'])}")
    return bad[:8]


@check("the shared-member gate holds and only hand-written edges are summarised")
def _l0_gate(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    hand = set()
    for e in b["edges"]:
        hand.add("|".join(sorted((e["a"], e["b"]))))
    gate = d["config"]["sharedMemberGate"]
    bad = []
    for e in d["summarised"]:
        if len(e["via"]) < gate:
            bad.append(f"summarised {e['a']}~{e['b']} has {len(e['via'])} shared "
                       f"member(s), below the gate of {gate}")
        # A rolled-up DERIVED edge would carry a count and a tier earned by nothing
        # but a shared attribute. The two must never meet in the same code path.
        for v in e["via"]:
            for end in (e["a"], e["b"]):
                if "|".join(sorted((end, v))) not in hand:
                    bad.append(f"summarised {e['a']}~{e['b']} rests on {end}~{v}, "
                               f"which is not a hand-written edge")
    return bad[:8]


@check("no routed or path-only entity emits an edge instance")
def _l0_noroutededges(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    l0ids = {n["id"] for n in d["l0"]}
    off = {r["id"] for r in d["pathOnly"]} | {r["id"] for r in d["unattached"]}
    for n in d["l0"]:
        off |= {r["id"] for r in n["routed"]}
    bad = []
    for e in d["directEdges"] + d["summarised"]:
        for end in (e["a"], e["b"]):
            if end in off:
                bad.append(f"edge {e['a']}~{e['b']} has endpoint {end}, which is "
                           f"routed or path-only and must not draw")
            elif end not in l0ids:
                bad.append(f"edge {e['a']}~{e['b']} has endpoint {end}, which is "
                           f"not on the map at all")
    # every routed row must print its intermediates, or the reader cannot audit
    # how the entity was attached
    for n in d["l0"]:
        for r in n["routed"]:
            if r["depth"] > 1 and not r.get("via"):
                bad.append(f"{r['id']} is attached to {n['id']} at depth "
                           f"{r['depth']} with no intermediates printed")
    return bad[:8]


@check("every L0 node's class bar sums to the members it lists")
def _l0_copy(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    bad = []
    # This check also asserted, until 25 September 2026, that the old shell's rail
    # carried both register controls with counts read from L0DATA.counts. That half
    # went with the old shell; the half that is about the model stays.
    for n in d["l0"]:
        listed = len(n["direct"]) + len(n["routed"])
        mixed = sum(n["mix"].values())
        if listed != mixed:
            bad.append(f"{n['id']} says {mixed} members in its class bar but lists "
                       f"{listed} rows")
    return bad[:8]


@check("every routed row names its intermediate resolvably")
def _l0_via(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    known = set(d["nodes"].keys())
    bad = []
    for n in d["l0"]:
        for r in n["routed"]:
            for v in r.get("via", []):
                # This is where JR., J. comes back. A via that does not resolve to
                # a real node id prints a label the reader cannot follow — and a
                # label truncated at the first space prints "via AARO" for a FOIA
                # memorandum and "via Kirsten" for a senator.
                if v not in known:
                    bad.append(f"{n['id']} routes {r['id']} via '{v}', which is not "
                               f"a node id")
                elif not str(d["nodes"][v][0]).strip():
                    bad.append(f"{n['id']} routes {r['id']} via {v}, which has an "
                               f"empty label")
    return bad[:8]


@check("every L0 node carries an entity dossier")
def _l0_dossier_cover(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    # The dossier is the ARGUMENT for why a node is on this map, and on this board
    # the argument is the product. A node with a member list and no argument sends
    # the reader into individual dossiers to reconstruct it themselves.
    missing = [n["id"] for n in d["l0"] if not (n.get("dossier") or {}).get("narrative")]
    if missing:
        return [f"{len(missing)} L0 node(s) have no entity dossier: {missing[:6]}"]
    return []


@check("every dossier claim is tiered and sourced")
def _l0_dossier_claims(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    bad = []
    for n in d["l0"]:
        for i, c in enumerate((n.get("dossier") or {}).get("claims", [])):
            if c.get("tier") not in (1, 2, 3):
                bad.append(f"{n['id']} claim {i} has tier {c.get('tier')!r}; "
                           f"an untiered claim is an unmarked assertion")
            if not str(c.get("source") or "").strip():
                bad.append(f"{n['id']} claim {i} has no source. This is the one "
                           f"rule that never bends.")
            if not str(c.get("text") or "").strip():
                bad.append(f"{n['id']} claim {i} has no text")
    return bad[:8]


@check("every connection row is backed by a hand-written edge")
def _l0_connections(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    hand = set()
    for e in b["edges"]:
        hand.add((e["a"], e["b"], e["type"]))
        hand.add((e["b"], e["a"], e["type"]))
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    for src, rows in (d.get("connections") or {}).items():
        for r in rows:
            # The connection layer is PROJECTED from sourced edges, never written.
            # If a row appears here with no edge behind it, something generated it,
            # and a generated connection on this board is a fabricated claim.
            if (src, r["id"], r["type"]) not in hand:
                bad.append(f"{src} -> {r['id']} ({r['type']}) has no hand-written "
                           f"edge behind it")
            if r["id"] not in ids:
                bad.append(f"{src} connects to {r['id']}, which is not a node")
    return bad[:8]


@check("structural authority is cited, and the exclusions hold")
def _l0_authority(b):
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    auth = d.get("authority") or {}
    ids = {n["id"] for n in b["people"] + b["entities"]}
    bad = []
    # Excluded on principle, not by accident: a spokesperson speaks for a decision
    # and does not make one; an FFRDC trustee advises a corporation, not a
    # compartment. The first matcher caught all four plus a set of hearings that
    # merely cited an office. If they reappear, the matcher has gone loose again.
    for x in ("susan-gough", "christopher-sherwood", "donald-kerr", "sue-gordon"):
        if x in auth:
            bad.append(f"{x} is flagged as holding structural authority; it is "
                       f"excluded by rule and the matcher has gone loose")
    for k, v in auth.items():
        if k not in ids:
            bad.append(f"{k} carries authority but is not a node")
        if not v.get("instruments"):
            bad.append(f"{k} claims authority with no instrument cited; an uncited "
                       f"authority is an assertion")
        if v.get("tense") not in ("holds", "held"):
            bad.append(f"{k} has tense {v.get('tense')!r}; a former holder's "
                       f"authority is history and must not read as live")
    return bad[:8]

# ---------------------------------------------------------------------------
# golden counts — drift detection. Not correctness; a tripwire that turns a
# silent change into a deliberate one. `--update-golden` is the only way past it.
# ---------------------------------------------------------------------------

def _l0_golden():
    """The six L0 counts GOLDEN tracks. `unattached` moving is either a research
    gain or a routing regression, and the two look identical in a diff — which is
    exactly why it needs deliberate acceptance rather than a silent update."""
    path = os.path.join(ROOT, "data", "l0-model.json")
    if not os.path.exists(path):
        return {}
    c = json.load(open(path, encoding="utf-8"))["counts"]
    return {"l0_nodes": c["l0"], "l0_edges_direct": c["directEdges"],
            "l0_edges_summarised": c["summarisedEdges"], "ledger": c["ledger"],
            "path_only": c["pathOnly"], "unattached": c["unattached"],
            "l0_with_dossier": c.get("withDossier", 0),
            "l0_dossier_claims": c.get("dossierClaims", 0),
            # Since phase 3 the node sourcing caps reach dossier claims, so their
            # tier mix is a count that moves on purpose and is held here.
            "l0_dossier_claim_tiers": _dossier_tier_mix(json.load(open(path, encoding="utf-8")))}


def _dossier_tier_mix(model):
    from collections import Counter
    doss = dict(model.get("dossiers") or {})
    for n in model.get("l0") or []:
        if n.get("dossier"):
            doss.setdefault(n["id"], n["dossier"])
    ct = Counter(c.get("tier") for d in doss.values() for c in (d or {}).get("claims") or [])
    return {str(k): ct[k] for k in (1, 2, 3)}


def measure(b):
    from collections import Counter
    cls = Counter(n["cls"] for n in b["entities"])
    tier = Counter(n.get("tier") for n in b["people"] + b["entities"])
    ctier = Counter(c["tier"] for n in b["people"] + b["entities"] for c in n.get("claims", []))
    # This counted the whole annotated source STRING, so appending a demotion note
    # to a claim minted a new "unique source URL" and the number drifted upward on
    # a pass that added no sourcing at all. Count the URLs, from the claim sources
    # and the node sources alike, which is what the name has always promised.
    urlpat = re.compile(r"https?://[^\s,;)\]<>\"]+")
    urls = set()
    for n in b["people"] + b["entities"]:
        for c in n.get("claims", []):
            urls.update(u.rstrip(".,;") for u in urlpat.findall(c.get("source") or ""))
        for sc in n.get("sources", []) or []:
            if sc.get("url"):
                urls.add(sc["url"].rstrip(".,;"))
    return {
        "people": len(b["people"]), "entities": len(b["entities"]),
        "edges": len(b["edges"]), "timeline": len(b.get("timeline", [])),
        "entity_classes": dict(sorted(cls.items())),
        "entity_tiers": dict(sorted(tier.items())),
        "claim_tiers": {str(k): v for k, v in sorted(ctier.items())},
        # Edge tiers were never in this manifest, which is part of why nobody
        # noticed they were never audited either: 93 edges printed "Tier 1 -
        # documented" on a Wikipedia article and no count moved when they did.
        "edge_tiers": {str(k): sum(1 for e in b["edges"] if e.get("claimTier") == k)
                       for k in (1, 2, 3)},
        "unique_source_urls": len(urls),
        **_l0_golden(),
        "people_with_date": sum(1 for p in b["people"] if p.get("date")),
        "locations_with_coords": sum(1 for e in b["entities"] if e.get("coords")),
        # The case against, on entities: carried since phase 3.
        "entity_case_against": {f: sum(len(e.get(f) or []) for e in b["entities"])
                                for f in ("conflicts", "unverified", "openQuestions")},
    }


# ---------------------------------------------------------------------------
# Design's nine checks, from notes/design-2026-08-24/DESIGN-RESPONSE-LAYOUT §5.
#
# They assert against data/l0-layout-model.json, which is a build product on disk,
# so they need their own poison channel: _LAYOUT_OVERRIDE, set by self_test().
# ---------------------------------------------------------------------------

LAYOUT = os.path.join(ROOT, "data", "l0-layout-model.json")
REJECTS = os.path.join(ROOT, "tools", "REJECTS.json")
_LAYOUT_OVERRIDE = None
_REJECTS_OVERRIDE = None
IMAGES = os.path.join(ROOT, "data", "l0-images.json")
_IMAGES_OVERRIDE = None


def _images():
    """The image register, or the poisoned stand-in during --self-test."""
    if _IMAGES_OVERRIDE is not None:
        return _IMAGES_OVERRIDE
    if not os.path.exists(IMAGES):
        return None
    with open(IMAGES, encoding="utf-8") as fh:
        return json.load(fh)


_PATENTS_OVERRIDE = None
_OBS_OVERRIDE = None
_FOIA_OVERRIDE = None
_THREADS_OVERRIDE = None


def _threads():
    """research/threads.json, or the poisoned stand-in during --self-test."""
    if _THREADS_OVERRIDE is not None:
        return _THREADS_OVERRIDE
    path = os.path.join(ROOT, "research", "threads.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _foia():
    """data/foia-links.json, or the poisoned stand-in during --self-test."""
    if _FOIA_OVERRIDE is not None:
        return _FOIA_OVERRIDE
    path = os.path.join(ROOT, "data", "foia-links.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _patents():
    """research/patents-view.json, or the poisoned stand-in during --self-test."""
    if _PATENTS_OVERRIDE is not None:
        return _PATENTS_OVERRIDE
    path = os.path.join(ROOT, "research", "patents-view.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _observables():
    """research/observables-view.json, or the poisoned stand-in."""
    if _OBS_OVERRIDE is not None:
        return _OBS_OVERRIDE
    path = os.path.join(ROOT, "research", "observables-view.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _flat(t):
    """Whitespace-flattened, for substring tests against a transcript.

    The wrapper transcripts are hard-wrapped at about 80 columns, so a quotation
    that is verbatim in the document still fails a naive `in` test the moment it
    crosses a line. That is not a hypothetical: the first attempt to verify the
    Sheehy quotation from a shell one-liner reported it ABSENT, because 'beyond the
    state of the possible' is broken across two lines in the letter. A check that
    reports a real quote as fabricated is worse than no check."""
    return " ".join(str(t or "").split())


def _layout():
    """The layout model, or the poisoned stand-in during --self-test."""
    if _LAYOUT_OVERRIDE is not None:
        return _LAYOUT_OVERRIDE
    if not os.path.exists(LAYOUT):
        return None
    with open(LAYOUT, encoding="utf-8") as fh:
        return json.load(fh)


def _datasets(m):
    """Both baked datasets. `current` is authoritative; `legacy` is the superseded
    96-node snapshot, kept so the editorial layer cannot be silently trimmed to the
    intersection of the two."""
    return [(k, m[k]) for k in ("current", "legacy") if isinstance(m.get(k), dict)]


@check("every chip label fits the chip it is drawn in")
def _shorts_fit(b):
    """A 205px chip at 1.0x holds about 37 monospace characters. Beyond that the
    renderer middle-truncates, which Design called a safety net rather than a
    design: `l0Fit` cannot know which half of a label matters, and it dropped the
    citation from "Sec. 6802, James M. Inhofe NDAA for FY2023 (Pub. L. 117-263)" --
    the half that identifies the statute.

    46 of 110 overflowed. They are authored in data/l0-shorts.json now, and this
    keeps them that way: a node added later with a long label fails here rather
    than quietly losing its distinguishing tail on the map.

    Two nodes sharing a short is the other failure, and it is worse than a long
    one -- "AARO Historical Record" for both Volume I and Volume II is a chip that
    names the wrong document half the time."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad, seen = [], {}
    for _, ds in _datasets(m):
        for n in (ds.get("nodes") or []):
            sh = (n.get("short") or "").strip()
            if not sh:
                bad.append(f"{n.get('id')}: no short at all")
                continue
            if len(sh) > 37:
                bad.append(f"{n.get('id')}: short is {len(sh)} chars, over the 37 the chip "
                           f"holds -- author one in data/l0-shorts.json: {sh[:50]!r}")
            if sh in seen and seen[sh] != n.get("id"):
                bad.append(f"{n.get('id')} and {seen[sh]} share the short {sh!r}; a chip that "
                           f"names two nodes names the wrong one half the time")
            seen[sh] = n.get("id")
        break        # `current` is authoritative; legacy is a superseded snapshot
    return bad[:40]


@check("nothing in the image register fails silently")
def _image_register(b):
    """`data/l0-images.json` is empty on purpose -- a record there asserts that a
    specific image exists at a specific URL under a specific licence, which is a
    sourcing claim like any other. But the register is PLUMBED, and the failure mode
    of a plumbed-and-empty channel is that the first person to fill it gets no
    feedback: `build_l0_layout.mjs` draws an image only when a record clears, and a
    record that is malformed simply does not clear. The node falls back to its class
    letter, which is a supported state and looks identical to never having tried.

    So a record that was MEANT to ship an image and does not must fail here rather
    than disappear into a legitimate-looking fallback. Every rule below is a way of
    intending to publish an image and silently not doing it -- except the credit
    rule, which is the other direction: attribution is the condition most of these
    licences are granted on, and an image that ships without it is a licensing
    problem rather than a rendering one.

    `no` and `none` records are welcome and assert nothing: recording that an image
    was found and does NOT clear is research, and deleting it means the next pass
    re-does the work."""
    reg = _images()
    if reg is None:
        return ["data/l0-images.json is missing -- the register is plumbed and must exist"]
    imgs = reg.get("images")
    if not isinstance(imgs, dict):
        return ["data/l0-images.json has no `images` object"]
    m = _layout()
    ids = set()
    if isinstance(m, dict):
        for _, ds in _datasets(m):
            for n in (ds.get("nodes") or []):
                if n.get("id"):
                    ids.add(n["id"])
    bad = []
    OKC = ("clears", "ask", "no", "none")
    for nid, r in sorted(imgs.items()):
        if not isinstance(r, dict):
            bad.append(f"{nid}: record is not an object")
            continue
        cl = r.get("clearance")
        if cl not in OKC:
            bad.append(f"{nid}: clearance {cl!r} is not one of {OKC} -- "
                       f"an unrecognised value never draws, and never says so")
            continue
        if ids and nid not in ids:
            bad.append(f"{nid}: not a node on the map, so this record can never draw")
        if cl in ("clears", "ask"):
            if not (r.get("photo") or "").strip():
                bad.append(f"{nid}: clearance {cl!r} with no `photo` -- "
                           f"claims to ship an image and has none")
            if not (r.get("photoCredit") or "").strip():
                bad.append(f"{nid}: clearance {cl!r} with no `photoCredit` -- "
                           f"attribution is the condition the licence is granted on")
        if cl == "ask" and not (r.get("note") or "").strip():
            bad.append(f"{nid}: clearance 'ask' with no `note` -- ask ships WITH its "
                       f"reason, or the doubt is resolved silently in its own favour")
        pk = r.get("photoKind")
        if pk is not None and pk not in ("portrait", "mark"):
            bad.append(f"{nid}: photoKind {pk!r} is neither 'portrait' nor 'mark' -- "
                       f"the renderer crops a portrait and must not crop a mark")
    return bad[:40]


@check("L0 degree is distinct neighbours, not edge instances")
def _dz_degree(b):
    """Design: `degree_is_distinct_neighbours`. Must reject a model baked from the
    extract's `deg` field, which counts edge INSTANCES.

    This is trap #2 in the handoff and it has already cost a session: 94 node pairs
    on this board carry more than one hand-written edge, so counting instances
    published '107 L0 nodes' when the answer was 96. A floor of 6 applied to the
    wrong quantity admits nodes that do not belong on the map at all.

    Asserts two things: every shipped node's `deg` equals the distinct-neighbour
    count recomputed from the board, and every shipped node clears the stated floor.
    It does NOT assert set equality with a naive recomputation -- build_l0 excludes
    routed and path-only entities, so the derived superset is legitimately larger."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    nb = {}
    for e in b["edges"]:
        a, z = e.get("a"), e.get("b")
        if a and z and a != z:
            nb.setdefault(a, set()).add(z)
            nb.setdefault(z, set()).add(a)
    bad = []
    for key, d in _datasets(m):
        if key != "current":
            continue            # only `current` is derived from the shipped board
        floor = (d.get("config") or {}).get("floor")
        if floor is None:
            bad.append("the layout model states no floor")
            continue
        for n in d.get("nodes") or []:
            actual = len(nb.get(n["id"], ()))
            if n.get("deg") != actual:
                bad.append(f"{n['id']}: model deg {n.get('deg')} but {actual} distinct "
                           f"neighbours on the board -- looks like edge instances")
            if actual < floor:
                bad.append(f"{n['id']} is on the map with {actual} distinct neighbours, "
                           f"below the floor of {floor}")
    return bad[:40]


@check("every layout figure recomputes from the model")
def _dz_figures(b):
    """Design: `figures_match_model`. Must reject any hand-edited figure.

    Every number quoted in the design write-up is supposed to be read out of the
    model rather than typed. A typed figure is a claim that goes stale silently --
    the same fault that put 'ENTITIES 976' in the QA checklist and sent testers to
    rebuild a board that was already correct."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        f, nodes, edges = d.get("figures") or {}, d.get("nodes") or [], d.get("edges") or []
        want = {
            "l0": len(nodes),
            "directEdges": sum(1 for e in edges if e.get("kind") == "direct"),
            "summarisedEdges": sum(1 for e in edges if e.get("kind") == "shared"),
            "drawnBeforeBudget": len(edges),
            "restDrawn": sum(1 for e in edges if e.get("rest")),
            "isolated": sum(1 for n in nodes if n.get("isolated")),
        }
        for k, v in want.items():
            if k in f and f[k] != v:
                bad.append(f"{key}.figures.{k} says {f[k]}, the model itself gives {v}")
    return bad[:40]


@check("no L0 node with a link is left without a line")
def _dz_no_bare(b):
    """Design: `no_node_without_a_line`. Must reject clause 1 shipped without clause
    2, which reaches 50 of 110 nodes and leaves 60 bare.

    The edge budget exists to stop the map being a hairball. The failure mode it
    introduces is the opposite one: a node drawn with no line at all, which reads as
    'unconnected' when it means 'its lines lost the budget'."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        for n in d.get("nodes") or []:
            if (n.get("allEdges") or 0) > 0 and (n.get("restEdges") or 0) == 0:
                bad.append(f"{key}: {n['id']} has {n['allEdges']} L0-level edges and none "
                           f"drawn at rest -- it renders bare and reads as unconnected")
    return bad[:40]


@check("absent prints as absent")
def _dz_absent(b):
    """Design: `absent_prints_as_absent`. Must reject placing an undated node in an
    era column, or an `isolated` count dropping to 0 without those nodes gaining a
    real edge.

    A node with no date and a node with no link are both facts. Hiding either one --
    by parking it in the nearest era, or by quietly reclassifying it -- turns a gap
    into a false positive."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        eras = d.get("eras") or []
        nodate = [e for e in eras if e.get("kind") == "nodate"]
        if not nodate:
            bad.append(f"{key}: no NO DATE column -- undated nodes have nowhere honest to go")
        elif not (nodate[0].get("label") or "").strip():
            bad.append(f"{key}: the NO DATE column carries no label")
        # Placement is `col`, not `era`: an undated node has era None and col "nd".
        # Asserting on `era` reads the absence of an era as a missing placement and
        # false-positives on five correctly placed nodes -- which is what the first
        # version of this check did.
        nd_ids = {e.get("id") for e in nodate}
        nd_span = {e.get("id"): (e.get("x"), (e.get("x") or 0) + (e.get("w") or 0))
                   for e in nodate}
        for n in d.get("nodes") or []:
            undated = n.get("y0") in (None, "")
            col = n.get("col")
            in_nd = col in nd_ids
            if undated and not in_nd:
                bad.append(f"{key}: {n['id']} has no dateStart but sits in column "
                           f"{col!r} rather than NO DATE")
            if in_nd and not undated:
                bad.append(f"{key}: {n['id']} is dated {n.get('y0')} but sits in NO DATE")
            if in_nd and isinstance(n.get("x"), int):
                lo, hi = nd_span.get(col, (None, None))
                if lo is not None and not (lo <= n["x"] <= hi):
                    bad.append(f"{key}: {n['id']} is assigned to NO DATE but sits at "
                               f"x={n['x']}, outside that column's {lo}-{hi}")
            if bool(n.get("isolated")) != ((n.get("allEdges") or 0) == 0):
                bad.append(f"{key}: {n['id']} isolated={n.get('isolated')} but carries "
                           f"{n.get('allEdges')} L0-level edges -- the marker and the data disagree")
    return bad[:40]


@check("chip size is not a channel")
def _dz_no_size(b):
    """Design: `no_size_channel`. Must reject any model where the set of distinct chip
    widths or heights has more than one member.

    Size is the channel a reader reads as importance without being told to. This map
    scores entities on three axes that are deliberately never summed, so a single
    size channel would collapse exactly what the axes keep apart. Every chip is the
    same size on purpose."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        nodes = d.get("nodes") or []
        if not nodes:
            continue
        ws = {n.get("w") for n in nodes}
        hs = {n.get("h") for n in nodes}
        if len(ws) != 1 or len(hs) != 1:
            bad.append(f"{key}: chips come in {len(ws)} widths and {len(hs)} heights "
                       f"({sorted(ws)[:4]} x {sorted(hs)[:4]}) -- size has become a channel")
            continue
        geo = (d.get("config") or {}).get("geo") or {}
        if geo.get("chipW") is not None and ws != {geo["chipW"]}:
            bad.append(f"{key}: chips are {ws.pop()} wide, config says {geo['chipW']}")
        if geo.get("chipH") is not None and hs != {geo["chipH"]}:
            bad.append(f"{key}: chips are {hs.pop()} tall, config says {geo['chipH']}")
    return bad[:40]


@check("layout positions are grid-derived, not force-derived")
def _dz_deterministic(b):
    """Design: `layout_is_deterministic`. Must reject a re-introduced force pass.

    `--idempotent` already builds twice and requires byte-identical output, which
    catches non-determinism across runs. This catches its cause in a single run: a
    force simulation settles on fractional coordinates and drifts outside the cell
    grid, where a packed layout emits integers inside declared bounds."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        ww, wh = d.get("worldW"), d.get("worldH")
        if not isinstance(ww, int) or not isinstance(wh, int):
            bad.append(f"{key}: world bounds are not integers ({ww}x{wh})")
            continue
        for n in d.get("nodes") or []:
            x, y = n.get("x"), n.get("y")
            if not isinstance(x, int) or not isinstance(y, int):
                bad.append(f"{key}: {n['id']} sits at ({x}, {y}) -- fractional coordinates "
                           f"mean something is settling, not packing")
            elif not (0 <= x <= ww and 0 <= y <= wh):
                bad.append(f"{key}: {n['id']} at ({x}, {y}) is outside the world {ww}x{wh}")
    return bad[:40]


@check("a denial that is not a directed act carries no denial styling")
def _dz_denialkind(b):
    """Design, answering the implementation session: a denial has three states
    because the data has three, and one undifferentiated red line was not.

        directed     issuer named        arrowhead, and later a particle
        undirected   an act, no issuer   a perpendicular bar at the midpoint
        association  not a directed act  no denial styling at all

    Eleven of thirty adjudicated edges are the third kind -- `roswell ->
    official-denial`, "four official explanations for one event"; a person and their
    own bylined article. Red is reserved for something somebody did.

    UPDATED 26 August 2026, when all 174 were adjudicated. This asserted that
    denialKind was only ever 'association' or absent -- true while `association`
    was the only verdict anyone had recorded, and false the moment the other two
    were. A check that hardcodes the state of the data rather than the RULE about
    it goes red on the work it was written to protect.

    The rule is the vocabulary and its internal consistency:
      association  not a directed act, so it must NOT name a denier
      directed     a named issuer, so it MUST name one, and that denier must be
                   one of the edge's own two ends
      undirected   an act with no attributable issuer, so it must NOT name one
    Absent still means undirected, which claims the least."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        for e in d.get("edges") or []:
            k = e.get("denialKind")
            if k is None:
                continue
            if k not in ("association", "directed", "undirected"):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} has denialKind {k!r}, "
                           f"which is not one of the three states")
            elif k == "directed":
                dn = e.get("denier")
                if not dn:
                    bad.append(f"{key}: {e.get('a')}->{e.get('b')} is 'directed' and names "
                               f"no denier -- a direction with nobody at the sharp end")
                elif dn not in (e.get("a"), e.get("b")):
                    bad.append(f"{key}: {e.get('a')}->{e.get('b')} names denier {dn!r}, "
                               f"which is neither of its own two ends")
            elif k == "undirected" and e.get("denier"):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} is 'undirected' and names a "
                           f"denier -- if the issuer is known it is directed")
            elif k == "association" and e.get("denier"):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} is an association and "
                           f"also names a denier {e.get('denier')!r}")
    return bad


@check("every field the design reads but the data withholds is in the backfill queue")
def _dz_queue(b):
    """Design's `queue_covers_every_field_read`. Must reject "this doc and the page
    disagreeing" -- the same drift class the reproduction correction fixed once.

    The queue is how the design degrades honestly instead of guessing: a field the
    renderer reads and the data does not supply has to be a NAMED TASK with a place
    to pull it from, or it is just a silent hole. Two rows were added on 26 August
    (`denialKind` and the `short` budget) because the standing rule is that any new
    field the design reads gets a row.

    Asserts every field this build reads and does not yet have is named in `gaps`,
    and that each row carries all four columns."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    rows = m.get("gaps") or []
    if not rows:
        return ["the model carries no backfill queue at all"]
    blob = " ".join(str(c) for r in rows for c in r).lower()
    bad = []
    for r in rows:
        if not isinstance(r, list) or len(r) != 4 or not all(str(c).strip() for c in r):
            bad.append(f"queue row {r[0] if r else r!r} is not four filled columns: "
                       "field, what it is, where to pull it, what the design cannot say")
    # ---- which fields the data withholds, MEASURED ---------------------------
    # This was a hardcoded list of six field names asserted to be missing. It went
    # red the moment any of them was supplied -- denialKind, denier and short all
    # landed on 26 August and the check complained about the rows being retired,
    # which is the work it exists to protect. A check that hardcodes the STATE of
    # the data rather than the RULE about it is a check with an expiry date.
    #
    # So: measure. A field is withheld when no node or edge carries it, and only
    # then does it need a row.
    ds0 = None
    for _, d0 in _datasets(m):
        ds0 = d0
        break
    nodes0 = (ds0 or {}).get("nodes") or []
    edges0 = (ds0 or {}).get("edges") or []
    dn0 = [e for e in edges0 if e.get("denial")]
    READS = {
        "denialkind": ("the three denial states",
                       any(e.get("denialKind") for e in dn0)),
        "denier":     ("which end issued a denial",
                       any(e.get("denier") for e in dn0)),
        "short":      ("a chip-length label",
                       bool(nodes0) and all((n.get("short") or "") for n in nodes0)),
        "photo":      ("the chip glyph slot's image",
                       any(n.get("photo") for n in nodes0)),
        "dateend":    ("the end of a span",
                       any(n.get("y1") is not None for n in nodes0)),
        "members":    ("the off-map neighbours",
                       bool(nodes0) and all(n.get("members") for n in nodes0)),
    }
    for key, (why, supplied) in READS.items():
        if supplied:
            continue
        alt = {"denier": "denial a/b", "dateend": "dateend"}.get(key, key)
        if key not in blob and alt.replace(" ", "") not in blob.replace(" ", ""):
            bad.append(f"the design reads `{key}` ({why}) and the data does not carry it, "
                       f"but no backfill row names it")

    # ---- and the other direction, which is how three rows went stale ---------
    # This check asserted only that a MISSING field is queued. It never asked
    # whether a QUEUED field is still missing, so via[], members[] and C/A/D sat
    # in the queue for two days after the pipeline started supplying them, and
    # the check passed the whole time because the rows were present.
    #
    # A stale row is not harmless. It is a standing instruction to redo finished
    # work, and it makes this file and the data disagree -- the same drift class
    # the row-shape half was written for. So: any row whose field the data now
    # supplies for EVERY node must be retired.
    ds = None
    for _, d in _datasets(m):
        ds = d
        break
    if ds:
        nodes = ds.get("nodes") or []
        edges = ds.get("edges") or []
        shared = [e for e in edges if e.get("kind") == "shared"]
        supplied = {
            "via[]": bool(shared) and all(e.get("via") for e in shared),
            "members[]": bool(nodes) and all(n.get("members") for n in nodes),
            "c / a / d": bool(nodes) and all(n.get("C") is not None for n in nodes),
        }
        for r in rows:
            name = str(r[0]).strip().lower()
            if supplied.get(name):
                bad.append(f"backfill row `{r[0]}` is stale: every node or edge now "
                           f"carries it. Retire the row -- a queue that lists finished "
                           f"work is an instruction to do it again")
    return bad


@check("the rarity order the board implies still matches the pin")
def _dz_rarity(b):
    """Design's `rarity_order_matches_the_pin`, the one named check that was never
    built as a gate step. The generator has always REPORTED drift in
    `figures.rarityDrift` and `state_snapshot.py` prints it; nothing failed on it.

    Two tags with near-equal counts can swap rarity rank between research passes and
    take every node carrying both with them, which moves them between BANDS -- and
    the band order is the vertical argument. `oversight` (64) and `disclosure` (61)
    are within 10% and are INVERTED on the legacy snapshot, which is the pin doing
    its job rather than failing.

    So this asserts the pin holds on the dataset that SHIPS, and that drift is
    reported rather than silently obeyed. Legacy drift is expected and is not a
    failure: CLAUDE.md is explicit that editing RARITY_PIN to silence it is wrong."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    cur = m.get("current") or {}
    f = cur.get("figures") or {}
    pin, obs = f.get("rarityPin"), f.get("rarityObserved")
    bad = []
    if not pin or not obs:
        return ["current/figures is missing rarityPin or rarityObserved"]
    if list(pin) != list(obs):
        bad.append("the shipping dataset's tag counts imply "
                   f"{list(obs)} against the pin {list(pin)} -- decide it, do not "
                   "edit RARITY_PIN to silence it")
    if f.get("rarityDrift"):
        bad.append("current reports rarityDrift " + str(f["rarityDrift"]))
    # and the drift channel itself must exist, or the report is not being made
    for key, d in _datasets(m):
        if "rarityDrift" not in (d.get("figures") or {}):
            bad.append(f"{key}: figures carries no rarityDrift, so drift is not reported at all")
    return bad


@check("denial direction is published only where the record names a denier")
def _dz_denier(b):
    """The check that was missing while 22 of 47 arrowheads pointed the wrong way.

    `motion is attested, not decorative` above guards the FLAGS -- that a denial is
    marked as one, and that no second motion flag exists. It says nothing about the
    direction, which is the actual claim the arrowhead makes, and it passed happily
    for the whole of the first build while the head was drawn at `e.b` where a/b is
    [a,b].sort(). Alphabetical order rendered as a statement about who denied whom.

    The board's raw records do not carry a consistent issuer-first convention
    either, so direction is attested ONLY where an edge names its denier. See
    notes/DENIAL-DIRECTION-2026-08-26.md.

    Asserts: a published `denier` is one of the edge's own ends, and it is named by
    at least one of the underlying denial records the edge rolls up. An edge with no
    denier is fine and is the current state of every one of them."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    bad = []
    for key, d in _datasets(m):
        for e in d.get("edges") or []:
            dnr = e.get("denier")
            if dnr is None:
                continue
            if not e.get("denial"):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} names a denier but is "
                           f"not marked as a denial")
                continue
            if dnr not in (e.get("a"), e.get("b")):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} names denier {dnr!r}, "
                           f"which is not one of its own ends")
                continue
            pairs = e.get("dn") or []
            if pairs and not any(dnr in p for p in pairs):
                bad.append(f"{key}: {e.get('a')}->{e.get('b')} names denier {dnr!r}, "
                           f"which appears in none of its {len(pairs)} denial record(s)")
    return bad


@check("motion is attested, not decorative")
def _dz_motion(b):
    """Design: `motion_only_where_attested`. Must reject a time-direction flow on
    every line.

    A particle travelling along a path reads as a claim that something moved that
    way. The board can attest exactly one such claim -- a denial, which has a
    direction because someone denied something to someone -- plus the selection
    highlight, which is the reader's own act rather than an assertion.

    Asserts the model marks denials explicitly and consistently with the edge's own
    types, and carries no second, undirected motion flag for a renderer to key on."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    banned = ("flow", "particle", "animate", "direction", "pulse")
    bad = []
    for key, d in _datasets(m):
        for e in d.get("edges") or []:
            # A summarised (`shared`) edge is a rollup of members two nodes have in
            # common. It has no relationship type of its own, so it cannot be a
            # denial and correctly carries no flag. Only typed direct edges can.
            if e.get("kind") != "direct":
                if e.get("denial"):
                    bad.append(f"{key}: summarised edge {e.get('a')}->{e.get('b')} is "
                               f"marked as a denial -- a rollup asserts no relationship")
                continue
            if "denial" not in e:
                bad.append(f"{key}: direct edge {e.get('a')}->{e.get('b')} carries no "
                           f"explicit denial flag, so a renderer cannot tell what may move")
                continue
            if bool(e["denial"]) != ("denial" in (e.get("types") or [])):
                bad.append(f"{key}: edge {e.get('a')}->{e.get('b')} is marked "
                           f"denial={e['denial']} but its types are {e.get('types')}")
            for k in banned:
                if k in e:
                    bad.append(f"{key}: edge {e.get('a')}->{e.get('b')} carries a {k!r} "
                               f"field -- motion on every line is decoration, not evidence")
    return bad[:40]


@check("highlights are a pointer, not a promotion")
def _dz_highlights(b):
    """Design: `highlights_are_a_pointer`. Must reject a flag naming an id the floor
    excluded, or flagging more than 16 of 110.

    The start-here layer is editorial. It is drawn as an offset pointer and is
    deliberately NOT a property of the record, so that pointing at AARO can never be
    mistaken for grading AARO. Two things keep that true: a flag may not carry a
    credibility field, and the layer may not grow large enough to become the map.

    The cap is 15% of the map. Unknown ids are FATAL on the dataset the flags were
    authored for and merely reported on any other, so the superseded `legacy`
    snapshot cannot kill the build and nobody is tempted to trim the editorial list
    down to the intersection of the two."""
    m = _layout()
    if not m:
        return ["data/l0-layout-model.json is missing"]
    credibility = {"tier", "C", "A", "D", "claims", "t1"}
    bad = []
    for key, d in _datasets(m):
        hl = d.get("highlights") or {}
        flags = hl.get("flags") or []
        nodes = d.get("nodes") or []
        ids = {n["id"] for n in nodes}
        cap = int(len(nodes) * 0.15)
        if len(flags) > cap:
            bad.append(f"{key}: {len(flags)} flags on a {len(nodes)}-node map exceeds the "
                       f"15% cap of {cap} -- the pointer has become the map")
        authored_for = m.get("default") or "current"
        for f in flags:
            stray = credibility & set(f)
            if stray:
                bad.append(f"{key}: flag {f.get('id')} carries {sorted(stray)} -- a flag that "
                           f"sets a credibility field is a promotion, not a pointer")
            if key == authored_for and f.get("id") not in ids:
                bad.append(f"{key}: flag names {f.get('id')!r}, which is not on the map")
    return bad[:40]


@check("the layout model stays under the read cap")
def _dz_read_cap(b):
    """Design: `model_under_read_cap`. Must reject the thing this whole correction was
    about.

    A tracked, pushed, present file over ~1MB reads as ABSENT over the GitHub read
    API. That is how a design brief came to cite figures nobody could reproduce, and
    how Claude Design correctly refused to reproduce them. The model exists at this
    size so it can be read."""
    if _LAYOUT_OVERRIDE is not None:
        raw = json.dumps(_LAYOUT_OVERRIDE)
        size = len(raw.encode("utf-8"))
    elif os.path.exists(LAYOUT):
        size = os.path.getsize(LAYOUT)
    else:
        return ["data/l0-layout-model.json is missing"]
    cap = 1_000_000
    if size > cap:
        return [f"the layout model is {size/1e6:.2f}MB, over the ~1MB read cap -- it will "
                f"read as ABSENT over the GitHub API, which is the failure this file exists "
                f"to avoid"]
    return []


@check("every FOIA request points at a question that is actually open")
def _foia_links(b):
    """The FOIA layer, and what it must not be allowed to become.

    Stewart, 29 August 2026: "The FOIA will have to happen way later but keep them
    there and ready. In fact integrate them into the board somehow." The integration
    is a chip on an open question naming the request that would close it, which turns
    the request queue from a document beside the board into part of its argument.

    That is only worth anything if the pointer is true. Three ways it can rot, and
    all three are silent:

      - a node is renamed and the letters keep the old id, so the chip stops drawing
        and the dossier looks as though no request touches it;
      - a research pass removes an open question and the indices shift underneath a
        letter written against the old numbering, so a chip points at the wrong
        question while still looking right;
      - the linkage file goes stale against the letters it was derived from.

    The third is handled by generating data/foia-links.json inside the build. This
    asserts the first two against the board that actually shipped, and asserts that
    the status stays honest: NOTHING HAS BEEN FILED, and a board that printed a
    request with no status would read as one in flight."""
    F = _foia()
    if F is None:
        return ["data/foia-links.json is missing — run python3 tools/build_foia_links.py"]
    bad = []
    # The generator records what it could not resolve rather than dropping it. If it
    # recorded anything, that is the finding.
    for nid in F.get("unresolved") or []:
        bad.append(f"the letters name node {nid!r}, which is not on this board")
    for x in F.get("outOfRange") or []:
        bad.append(f"a request points past the end of a node's open questions: {x}")

    reqs = F.get("requests") or []
    if not reqs:
        bad.append("no requests parsed out of notes/FOIA-LETTERS-2026-08-29.md, so "
                   "every dossier would render exactly as it did before the layer "
                   "existed — which is what a silently broken parser looks like")
    STATUS = {"not filed", "filed", "acknowledged", "responded", "appealed"}
    for r in reqs:
        if r.get("status") not in STATUS:
            bad.append(f"{r.get('id')}: status {r.get('status')!r} is not one the "
                       f"board knows how to draw")
        if not r.get("agency"):
            bad.append(f"{r.get('id')}: no agency, so its chip would print a bare id")
        if not (r.get("nodes") or []):
            bad.append(f"{r.get('id')}: closes nothing on the board")

    # And the linkage against the real dossiers, which is the half that rots.
    model_path = os.path.join(ROOT, "data", "l0-model.json")
    if os.path.exists(model_path):
        with open(model_path, encoding="utf-8") as fh:
            doss = (json.load(fh).get("dossiers") or {})
        for nid, rows in sorted((F.get("byNode") or {}).items()):
            d = doss.get(nid)
            if d is None:
                bad.append(f"a request points at {nid!r}, which has no dossier")
                continue
            n = len(d.get("openQuestions") or [])
            for row in rows:
                for q in (row.get("questions") or []) + (row.get("partial") or []):
                    if not (0 <= q < n):
                        bad.append(f"{row.get('request')} points at {nid} Q{q} and that "
                                   f"node has {n} open question(s)")
    return bad[:40]


@check("every patents-tab quotation is verbatim in the document it cites")
def _pat_quotes(b):
    """THE ONE RULE THAT NEVER BENDS, mechanised for the PATENTS tab.

    The tab's argument is carried by four quotations, three of them the examiner's,
    and a quotation is the highest-risk thing this board prints: it looks like
    evidence, it gets repeated, and nothing about a slightly-wrong one looks wrong.
    So every quote names the transcript it came from and this reads that file.

    It is not theoretical. The mockup signed off on 29 August is a picture, and a
    picture is not a source: its Sheehy quotation had to be checked against
    research/patents/wrapper/sheehy-letter-2017-12-15.txt before it could ship. It
    was verbatim -- but the check that established that is this one, not the eye.

    tools/spot_check.py does the same job for CLAIMS and is deliberately out of the
    gate because it depends on the network. This one is in the gate because the
    documents are transcribed in the repo: no network, no excuse.

    Whitespace is flattened on both sides. The transcripts are hard-wrapped at about
    80 columns, so a genuinely verbatim quotation crosses a line break and a naive
    substring test calls it a fabrication."""
    P = _patents()
    if P is None:
        return ["research/patents-view.json is missing and the PATENTS tab is a "
                "renderer with no content of its own"]
    bad = []
    for q in P.get("quotes") or []:
        text = _flat(q.get("text"))
        src = (q.get("source") or {}).get("name") or ""
        who = f'{q.get("speaker")} {q.get("date")}'
        if not text:
            bad.append(f"{who}: a quote with no text")
            continue
        if not src:
            bad.append(f"{who}: quoted with no source named")
            continue
        # the transcript the source names, if it names one
        m = re.search(r"(research/[\w./-]+\.txt)", src)
        if not m:
            bad.append(f"{who}: the source names no transcript in this repo, so the "
                       f"quotation cannot be checked here: {src[:80]}")
            continue
        path = os.path.join(ROOT, m.group(1))
        if not os.path.exists(path):
            bad.append(f"{who}: cites {m.group(1)}, which is not in the repo")
            continue
        with open(path, encoding="utf-8") as fh:
            doc = _flat(fh.read())
        if text not in doc:
            bad.append(f"{who}: the quotation is NOT in {m.group(1)} -- "
                       f"{text[:70]!r}")
    return bad


@check("no patents-tab quotation is edited by its own highlight")
def _pat_emphasis(b):
    """The renderer lights one phrase inside each quotation. If that phrase is not a
    substring of the quotation, the renderer drops it silently and the quote prints
    plain -- which is the safe failure, but a silent one.

    The reason this is a check and not just a guard: a highlight that does not appear
    in what it highlights is an edit to a quotation, and CLAUDE.md section 2 has no
    'just for display' case. The renderer must not be the only thing standing between
    a mistyped emphasis and the page."""
    P = _patents()
    if P is None:
        return ["research/patents-view.json is missing"]
    bad = []
    for q in P.get("quotes") or []:
        em = q.get("emphasis")
        if not em:
            continue
        if str(em) not in str(q.get("text") or ""):
            bad.append(f'{q.get("speaker")} {q.get("date")}: the highlighted phrase '
                       f'{str(em)[:50]!r} does not appear in the quotation it '
                       f'highlights')
    return bad


@check("the five observables stay Tier 2, and the mapping stays separate")
def _pat_observables(b):
    """TWO GRADES THAT MUST NEVER BE MERGED, and merging them is the easy overclaim
    this node exists to avoid.

    The TAXONOMY is Tier 2: attributed to one named former official, with no released
    government document stating the set as a set. The MAPPING is Tier 1: it is read
    off a FOIA-released Navy briefing. Print the pair as one grade and the board
    claims the government published the five observables, which it has not.

    And FOUR OF FIVE, NEVER FIVE. Sudden and instantaneous acceleration is not
    itemised as a design goal in PAX 205 -- the briefing's 'rapid acceleration
    transients' is how the machine is driven, not a claimed flight characteristic.
    research/five-observables.json records that four is the accurate figure and five
    would be the easy overclaim; this asserts the view data still says four, and
    asserts it by COUNTING the rows rather than by reading a stored number."""
    O = _observables()
    if O is None:
        return ["research/observables-view.json is missing"]
    bad = []
    if O.get("tier") != 2:
        bad.append(f"the taxonomy is graded Tier {O.get('tier')}. It is attributed to "
                   f"one named former official and no government original has been "
                   f"located, so it caps at Tier 2 (CLAUDE.md section 2)")
    obs = O.get("observables") or []
    if len(obs) != 5:
        bad.append(f"{len(obs)} observables. The set is five.")
    for m in O.get("mappings") or []:
        rows = m.get("rows") or []
        met = [r for r in rows if r.get("met")]
        if m.get("tier") != 1:
            bad.append(f"the mapping against {m.get('against')} is graded Tier "
                       f"{m.get('tier')}; it is read off a released document and is "
                       f"Tier 1, and it must not be merged with the taxonomy's grade")
        if len(rows) != len(obs):
            bad.append(f"the mapping against {m.get('against')} covers {len(rows)} of "
                       f"{len(obs)} observables; every one must be accounted for, "
                       f"including the one that is not met")
        if len(met) != 4:
            bad.append(f"the mapping against {m.get('against')} claims {len(met)} of "
                       f"{len(rows)} observables. Four is the figure the record "
                       f"supports; five is the overclaim.")
        for r in rows:
            if not r.get("met") and not r.get("why"):
                bad.append(f"{r.get('observable')} is marked NOT met with no reason "
                           f"given; an absence with no reason reads as an omission")
            if r.get("observable") not in {o.get("id") for o in obs}:
                bad.append(f"the mapping names {r.get('observable')!r}, which is not "
                           f"one of the five")
    return bad


@check("the patents tab prints what it does not have")
def _pat_absent(b):
    """`absent prints as absent`, the rule this board already gates on the map,
    applied to the file wrapper.

    The Reasons for Allowance is the examiner's own account of what reversed a
    rejection he had twice sustained. It is the single most informative document
    still outstanding on this node, and a reader who cannot see that it is missing
    will read the wrapper list as complete. So the absent papers are rows, struck
    through and marked NOT OBTAINED, and each carries the reason it is absent.

    Also asserts the filings are internally consistent: a status set that is not
    drawn from the closed vocabulary the renderer styles would print as an unstyled
    chip, and an EXPIRED filing with no expiry date states a fact it cannot support."""
    P = _patents()
    if P is None:
        return ["research/patents-view.json is missing"]
    bad = []
    W = P.get("wrapper") or {}
    if not (W.get("absent") or []):
        bad.append("the file wrapper lists nothing as absent. Every paper after "
                   "20 August 2018 is outstanding, the Reasons for Allowance among "
                   "them; a wrapper that lists only what was obtained reads as "
                   "complete")
    for a in W.get("absent") or []:
        if not a.get("why"):
            bad.append(f"{a.get('label')!r} is marked absent with no reason. "
                       f"'Not obtained' and 'does not exist' are different findings")
    KNOWN = {"GRANTED", "EXPIRED", "APPEALED", "PUBLISHED"}
    for f in P.get("filings") or []:
        for k in ("number", "application", "title", "filed"):
            if not f.get(k):
                bad.append(f"{f.get('id') or f.get('number')}: no {k}")
        st = set(f.get("status") or [])
        if not st:
            bad.append(f"{f.get('number')}: no status")
        for x in sorted(st - KNOWN):
            bad.append(f"{f.get('number')}: status {x!r} is not one the renderer "
                       f"styles, so it would print as an unmarked chip")
        if "EXPIRED" in st and not f.get("expired"):
            bad.append(f"{f.get('number')} is marked EXPIRED with no date")
        if "GRANTED" in st and not f.get("granted"):
            bad.append(f"{f.get('number')} is marked GRANTED with no grant date")
    # the drawings are named here and shipped from a directory; a named sheet with
    # no derivative renders as an empty frame, which looks like never having tried
    D = P.get("drawings") or {}
    thumbs = os.path.join(ROOT, "research", "patents", "drawings", "thumbs")
    for sh in D.get("sheets") or []:
        if not os.path.exists(os.path.join(thumbs, sh.get("file") or "")):
            bad.append(f"drawing sheet {sh.get('file')!r} is named and has no display "
                       f"derivative; run node tools/make_drawing_thumbs.mjs")
        if not sh.get("patent"):
            bad.append(f"drawing sheet {sh.get('file')!r} names no source patent")
    return bad


@check("every thread step is joined to the last by a board edge")
def _threads_joined(b):
    """research/threads.json is the THREADS page's whole content, the way
    research/patents-view.json is the PATENTS tab's. A thread is a chain a stranger
    is invited to follow, so the one thing it must never do is imply a connection
    the board does not hold: two nodes printed one above the other read as joined
    whether or not anything joins them, and the reader has no way to tell.

    APP-SPEC-2026-09-02 section 5 states the rule and Design's mockup printed a red
    placeholder wherever the extract had no edge for a pair. A placeholder in a
    mockup is honest; the same gap shipped is an invented relationship, which is
    CLAUDE.md section 2 in a costume it has not worn here before.

    So: every step names a node that exists, and every consecutive pair is joined,
    in either direction, by an edge in data/the-program.json of exactly the type and
    claimTier the step declares. A pair may instead be `derived` -- but only where
    the board holds NO direct edge at all, and then it must be one of
    data/l0-model.json's `summarised` pairs and must name that pair's own `via`
    members. Declaring `derived` over a pair that has a direct edge would let a
    thread quietly downgrade a documented link into an inferred one, and declaring a
    type or a tier the edge does not carry would let the page print a grade the
    board never awarded.

    This reads the board from disk rather than from `b`: the self-test fixture is
    two synthetic nodes with no edges, so every real thread would false-positive
    against it. The thing under test is the FILE, and its poison channel is
    _THREADS_OVERRIDE, the same pattern as _PATENTS_OVERRIDE."""
    T = _threads()
    if T is None:
        return ["research/threads.json is missing and the THREADS page is a "
                "renderer with no content of its own"]
    if not os.path.exists(BOARD):
        return ["data/the-program.json is missing, so no thread step can be checked"]
    with open(BOARD, encoding="utf-8") as fh:
        board = json.load(fh)
    ids = {n["id"] for n in board["people"] + board["entities"]}
    pairs = {}
    for e in board["edges"]:
        pairs.setdefault(frozenset((e["a"], e["b"])), []).append(e)
    summarised = {}
    lpath = os.path.join(ROOT, "data", "l0-model.json")
    if os.path.exists(lpath):
        with open(lpath, encoding="utf-8") as fh:
            for s in json.load(fh).get("summarised") or []:
                summarised[frozenset((s["a"], s["b"]))] = s

    bad = []
    seen_ids = set()
    threads = T.get("threads")
    if not threads:
        return ["research/threads.json carries no threads"]
    for t in threads:
        tid = t.get("id") or "<no id>"
        if tid in seen_ids:
            bad.append(f"{tid}: two threads share one id, so one of them is "
                       f"unreachable at #/t/{tid}")
        seen_ids.add(tid)
        for k in ("id", "label", "title", "blurb"):
            if not (t.get(k) or "").strip():
                bad.append(f"{tid}: no {k}")
        steps = t.get("steps") or []
        if not 5 <= len(steps) <= 9:
            bad.append(f"{tid}: {len(steps)} steps; a thread carries five to nine")
        for i, s in enumerate(steps):
            node = s.get("node")
            where = f"{tid} step {i + 1} ({node!r})"
            if node not in ids:
                bad.append(f"{where}: not a node on the board")
                continue
            if not (s.get("evidence") or "").strip():
                bad.append(f"{where}: no evidence line, so the step asserts a join "
                           f"and says nothing about it")
            ed = s.get("edge")
            if i == 0:
                if ed is not None:
                    bad.append(f"{where}: the first step has nothing before it and "
                               f"must carry edge: null")
                continue
            prev = steps[i - 1].get("node")
            key = frozenset((prev, node))
            direct = pairs.get(key) or []
            if ed is None:
                bad.append(f"{where}: no edge object, so nothing states how it is "
                           f"joined to {prev!r}")
                continue
            kind = ed.get("kind")
            if kind == "direct":
                if not direct:
                    bad.append(f"{where}: NOTHING on the board joins it to {prev!r}. "
                               f"The page would print the two as a chain anyway")
                    continue
                hit = [e for e in direct
                       if e.get("type") == ed.get("type")
                       and e.get("claimTier") == ed.get("tier")]
                if not hit:
                    have = sorted({f"{e.get('type')}/T{e.get('claimTier')}"
                                   for e in direct})
                    bad.append(f"{where}: declares {ed.get('type')}/T{ed.get('tier')} "
                               f"to {prev!r}; the board holds {', '.join(have)}")
            elif kind == "derived":
                if direct:
                    have = sorted({f"{e.get('type')}/T{e.get('claimTier')}"
                                   for e in direct})
                    bad.append(f"{where}: declared derived, but the board holds a "
                               f"direct edge to {prev!r} ({', '.join(have)}). A "
                               f"documented link must not print as an inferred one")
                    continue
                s2 = summarised.get(key)
                if s2 is None:
                    bad.append(f"{where}: declared derived, and {prev!r} shares no "
                               f"L0 member with it in data/l0-model.json")
                    continue
                if sorted(ed.get("via") or []) != sorted(s2.get("via") or []):
                    bad.append(f"{where}: names via {sorted(ed.get('via') or [])}; "
                               f"the model's shared members are "
                               f"{sorted(s2.get('via') or [])}")
            else:
                bad.append(f"{where}: edge kind {kind!r} is neither 'direct' nor "
                           f"'derived'")
    return bad


# ---------------------------------------------------------------------------
# redesign phase 3: the pipeline drops nothing
#
# Each of these re-derives from research/ (or from the board) what merge.py was
# changed to carry, so a regression back to dropping is a failure, not a quiet
# smaller number. Poisons: the checks that compare the research against the REAL
# board get a mutated copy of the real board (poison_realboard in self_test), the
# verb check gets a vocabulary with one verb removed (_VERB_MAP_OVERRIDE), and the
# denial report check gets the real board with one verdict stripped.
# ---------------------------------------------------------------------------

from merge import (VERB_MAP as _MERGE_VERB_MAP, VALID_EDGE as _VALID_EDGE,  # noqa: E402
                   VALID_GRADE as _VALID_GRADE, NOT_NODE_DOCUMENTS as _NOT_NODE_DOCS,
                   claim_key as _claim_key, tier1_cap_reason as _tier1_cap_reason,
                   URL_IN_SOURCE as _URL_IN_SOURCE, VALID_CLS as _VALID_CLS)

RESEARCH_DIR = os.path.join(ROOT, "research")
UNADJ = os.path.join(ROOT, "tools", "UNADJUDICATED-DENIALS.json")
_VERB_MAP_OVERRIDE = None
_RESEARCH_CACHE = []


def _research_docs():
    """Every node document under research/, as merge.py reads them."""
    if not _RESEARCH_CACHE:
        import glob
        docs = []
        for p in sorted(glob.glob(os.path.join(RESEARCH_DIR, "*.json"))):
            if os.path.basename(p) in _NOT_NODE_DOCS:
                continue
            with open(p, encoding="utf-8") as fh:
                docs.append((os.path.splitext(os.path.basename(p))[0], json.load(fh)))
        _RESEARCH_CACHE.append(docs)
    return _RESEARCH_CACHE[0]


CASE_FIELDS = ("conflicts", "unverified", "openQuestions")


def _authored_case_items():
    """{entity id: {field: [items]}}, unioned across files, collapsed ids folded into
    their survivors and removed ids dropped: what the board should carry."""
    out = {}
    for _slug, doc in _research_docs():
        for e in doc.get("entities") or []:
            if e.get("cls") not in _VALID_CLS or e.get("cls") == "person" or not e.get("id"):
                continue
            eid = canonical_id(e["id"])
            slot = out.setdefault(eid, {f: [] for f in CASE_FIELDS})
            for f in CASE_FIELDS:
                v = e.get(f)
                for x in (v if isinstance(v, list) else ([v] if v else [])):
                    if x not in slot[f]:
                        slot[f].append(x)
    rmp = os.path.join(RESEARCH_DIR, "_removed.json")
    rm = json.load(open(rmp, encoding="utf-8")) if os.path.exists(rmp) else {}
    alias = rm.get("alias") or {}
    for i in sorted(set(rm.get("remove") or [])):
        if i not in out:
            continue
        loser = out.pop(i)
        tgt = out.get(alias.get(i))
        if tgt is not None:
            for f in CASE_FIELDS:
                for x in loser[f]:
                    if x not in tgt[f]:
                        tgt[f].append(x)
    return out


@check("every authored conflict, unverified note and open question on an entity reaches the board")
def _entity_case_against(b):
    """Until phase 3 merge.py built an entity from a fixed field list that did not
    name `conflicts`, `unverified` or `openQuestions`, and 63 records' worth of the
    case against a node never reached the board: S-4, Dulce and TR-3B among them.
    This recounts them from research/ and compares node by node."""
    want = _authored_case_items()
    have = {e["id"]: e for e in b["entities"]}
    bad = []
    for eid, fields in sorted(want.items()):
        e = have.get(eid)
        if e is None:
            continue          # a rejected or unknown node: the reject check says so
        for f in CASE_FIELDS:
            got = e.get(f) or []
            got = got if isinstance(got, list) else [got]
            if len(fields[f]) != len(got):
                bad.append(f"{eid}.{f}: research carries {len(fields[f])}, the board {len(got)}")
    return bad[:40]


def _verb_map():
    return _VERB_MAP_OVERRIDE if _VERB_MAP_OVERRIDE is not None else _MERGE_VERB_MAP


@check("every authored edge verb is one of the twelve types or mapped in schema/vocab.json")
def _edge_verbs(b):
    """An authored verb outside the twelve types used to become `programmatic` in
    silence (89 records, 35 verbs). merge.py now maps each one through
    schema/vocab.json and rejects the rest; this re-reads research/ and the board
    so a verb that slips past the map, or a map row pointing at no type, or an
    edge whose type disagrees with its own authoredVerb, is a failure."""
    vm = _verb_map()
    bad = []
    for slug, doc in _research_docs():
        for x in doc.get("edges") or []:
            t = x.get("type") or x.get("rel")
            if t not in _VALID_EDGE and t not in vm:
                bad.append(f"{slug}: edge {x.get('a') or x.get('from')}->{x.get('b') or x.get('to')} "
                           f"carries the verb {t!r}, which is neither a type nor mapped")
    for v, m in sorted(vm.items()):
        if m.get("type") not in _VALID_EDGE:
            bad.append(f"schema/vocab.json maps {v!r} to {m.get('type')!r}, which is not a type")
    for e in b["edges"]:
        v = e.get("authoredVerb")
        if v and (v not in vm or vm[v]["type"] != e["type"]):
            bad.append(f"{e['a']}->{e['b']}: authoredVerb {v!r} but type {e['type']!r}")
    return bad[:40]


@check("no node carries a claim twice")
def _no_duplicate_claims(b):
    """The dedupe key was the whole text on one side and its first 120 characters on
    the other, so a long claim never matched itself and four nodes shipped one
    twice. One key now, on both sides; this asserts the result."""
    bad = []
    for n in b["people"] + b["entities"]:
        seen = set()
        for c in n.get("claims") or []:
            k = _claim_key(c.get("text"))
            if k in seen:
                bad.append(f"{n['id']}: {c.get('text', '')[:70]!r}")
            seen.add(k)
    return bad[:40]


APP_TIMELINE = os.path.join(ROOT, "app", "public", "data", "timeline.json")
APP_INDEX = os.path.join(ROOT, "app", "public", "data", "index.json")


@check("no timeline event ships a tier mixing two vocabularies")
def _timeline_tiers(b):
    """One `tier` field carried an event grade (A/B/C) and a claim tier (1/2/3, as
    ints and as strings). They are `grade` and `claimTier` now, each with its own
    vocabulary, and `tier` is not shipped: not on the board, not in the app."""
    bad = []
    rows = [("board", t) for t in b.get("timeline") or []]
    if os.path.exists(APP_TIMELINE):
        with open(APP_TIMELINE, encoding="utf-8") as fh:
            rows += [("app", t) for t in json.load(fh)]
    for where, t in rows:
        tid = t.get("id")
        if "tier" in t:
            bad.append(f"{where} {tid}: still ships `tier` {t['tier']!r}")
        if t.get("grade") is not None and t["grade"] not in _VALID_GRADE:
            bad.append(f"{where} {tid}: grade {t['grade']!r} is not A/B/C")
        ct = t.get("claimTier")
        if ct is not None and (not isinstance(ct, int) or isinstance(ct, bool) or ct not in (1, 2, 3)):
            bad.append(f"{where} {tid}: claimTier {ct!r} is not the integer 1, 2 or 3")
        if t.get("grade") is not None and ct is not None:
            bad.append(f"{where} {tid}: carries both a grade and a claim tier")
    return bad[:40]


_UNADJ_OVERRIDE = None


@check("every denial edge without a verdict is in the unadjudicated report")
def _unadjudicated_report(b):
    """tools/UNADJUDICATED-DENIALS.json lists every denial edge the adjudication has
    not reached. A report in phase 3; once phase R clears it, this check is where
    the list is required to be empty. Both directions are asserted: an edge missing
    from the list, and a listed edge that has a verdict or is gone."""
    if _UNADJ_OVERRIDE is not None:
        rep = _UNADJ_OVERRIDE
    elif os.path.exists(UNADJ):
        with open(UNADJ, encoding="utf-8") as fh:
            rep = json.load(fh)
    else:
        return ["tools/UNADJUDICATED-DENIALS.json is missing: run tools/build.py"]
    listed = {frozenset((r["a"], r["b"])) for r in rep}
    open_ = {frozenset((e["a"], e["b"])) for e in b["edges"]
             if e["type"] == "denial" and not e.get("denialKind")}
    bad = [f"denial {'/'.join(sorted(k))} has no verdict and is not in the report"
           for k in sorted(open_ - listed, key=sorted)]
    bad += [f"the report lists {'/'.join(sorted(k))}, which has a verdict or is not on the board"
            for k in sorted(listed - open_, key=sorted)]
    return bad[:40]


_EM = "\u2014"


@check("no display label carries a spaced em dash")
def _display_labels(b):
    """A spaced em dash in a label becomes " - " at build time, recorded in
    tools/DISPLAY-NORMALISED.json. Labels only: claim texts, sources and timeline
    texts may be quotations and are never touched, so they are not checked."""
    spaced = re.compile(r"\s" + _EM + r"\s")
    bad = []
    for n in b["people"] + b["entities"]:
        for f in ("label", "short"):
            if spaced.search(str(n.get(f) or "")):
                bad.append(f"node {n['id']}.{f}: {n[f]!r}")
    for e in b["edges"]:
        if spaced.search(e.get("label") or ""):
            bad.append(f"edge {e['a']}->{e['b']}: {e['label']!r}")
    for t in b.get("timeline") or []:
        if spaced.search(str(t.get("label") or "")):
            bad.append(f"timeline {t.get('id')}: {t['label']!r}")
    if os.path.exists(APP_INDEX):
        with open(APP_INDEX, encoding="utf-8") as fh:
            for r in json.load(fh)["nodes"]:
                if spaced.search(str(r.get("short") or "")):
                    bad.append(f"app index short {r['id']}: {r['short']!r}")
    return bad[:40]


@check("no Tier 1 dossier claim breaks the node-claim sourcing rules")
def _dossier_caps(b):
    """The node rule (secondary source, no attributed source, no primary URL, an
    interested party asserting an outside fact) reaches entity dossiers since phase
    3, through the same function. Re-applied here to what the model ships."""
    d = _l0()
    if d is None:
        return ["data/l0-model.json is missing: run tools/build.py"]
    doss = dict(d.get("dossiers") or {})
    for n in d.get("l0") or []:
        if n.get("dossier"):
            doss.setdefault(n["id"], n["dossier"])
    bad = []
    for nid, ds in sorted(doss.items()):
        claims = (ds or {}).get("claims") or []
        urls = " ".join(u for c in claims for u in _URL_IN_SOURCE.findall(c.get("source") or ""))
        for c in claims:
            why = _tier1_cap_reason(c, urls)
            if why:
                bad.append(f"{nid}: Tier 1 dossier claim {why}: {(c.get('text') or '')[:60]!r}")
    return bad[:40]


UNPLACED = os.path.join(ROOT, "tools", "UNPLACED-CLAIMS.json")
REMOVED_CLAIMS = os.path.join(ROOT, "tools", "REMOVED-CLAIMS.json")
_UNPLACED_OVERRIDE = None


@check("every authored claim reaches the board or is listed")
def _claims_placed(b):
    """Every claim written on any node id in research/, collapsed ids included,
    is on the board under its id or its collapse survivor (by the one claim key),
    or is named in a report that says why not: tools/UNPLACED-CLAIMS.json (an
    approved deletion, or a collapse into a d-* domain node) or
    tools/REMOVED-CLAIMS.json (a _corrections removeClaims rule). Until phase 3
    a collapse deleted the loser's claims in silence: 37 of them."""
    if _UNPLACED_OVERRIDE is not None:
        unplaced = _UNPLACED_OVERRIDE
    elif os.path.exists(UNPLACED):
        with open(UNPLACED, encoding="utf-8") as fh:
            unplaced = json.load(fh).get("claims") or []
    else:
        return ["tools/UNPLACED-CLAIMS.json is missing: run tools/build.py"]
    removed = []
    if os.path.exists(REMOVED_CLAIMS):
        with open(REMOVED_CLAIMS, encoding="utf-8") as fh:
            removed = json.load(fh)
    listed = {(u["id"], _claim_key(u.get("claim"))) for u in unplaced}
    rmp = os.path.join(RESEARCH_DIR, "_removed.json")
    alias = (json.load(open(rmp, encoding="utf-8")).get("alias") or {}) if os.path.exists(rmp) else {}
    have = {n["id"]: {_claim_key(c.get("text")) for c in n.get("claims") or []}
            for n in b["people"] + b["entities"]}
    bad = []
    for slug, doc in _research_docs():
        for n in (doc.get("people") or []) + (doc.get("entities") or []):
            if not n.get("id"):
                continue
            i = canonical_id(n["id"])
            to, hops = i, 0
            while to not in have and to in alias and hops < 8:
                to, hops = alias[to], hops + 1
            for c in n.get("claims") or []:
                t = (c.get("text") or c.get("claim")) if isinstance(c, dict) else None
                if not t:
                    continue          # a claim with no text is a merge reject
                k = _claim_key(t)
                if k in have.get(to, ()) or (i, k) in listed:
                    continue
                if any(r.get("id") == to and t.startswith(r.get("claim") or "\0")
                       for r in removed):
                    continue
                bad.append(f"{slug}: {i}" + (f" (-> {to})" if to != i else "") +
                           f": {t[:70]!r} is neither on the board nor listed")
    return bad[:40]


@check("no research record is silently dropped")
def _no_rejects(b):
    """merge.py writes every record it could not place to tools/REJECTS.json with a
    reason, and until 25 August NOTHING READ THAT FILE. The build exited 0, the gate
    passed, and the dropped research simply was not on the board.

    What that cost, discovered by looking: research/w11-statutory.json carried four
    entity records whose `cls` values were 'provision', 'statute' and 'mechanism' --
    none of which are in VALID_CLS. All four were rejected on every build since they
    were written, taking 30 claims with them, 26 of which reached the board by no
    other route. Among them the verbatim text of the 10 U.S.C. 119(e)(1) waiver
    authority, the DoDI 5205.11 paragraphs cutting professional staff out of waived
    programs, and the finding that the waiver has been exercised and the Department
    says so in a currently effective instruction. Two of the four nodes are
    start-here flags -- the first things the board tells a stranger to read.

    A typo in one field, no error anywhere, and the most load-bearing statutory
    research on the board was absent for weeks.

    This asserts the reject list is empty. If a record genuinely cannot be placed and
    that is correct, fix the record or move it out of the merged keys -- do not add an
    accepted-rejects list, because the next silent drop will hide inside it."""
    if _REJECTS_OVERRIDE is not None:
        rej = _REJECTS_OVERRIDE
    elif not os.path.exists(REJECTS):
        return []
    else:
        with open(REJECTS, encoding="utf-8") as fh:
            try:
                rej = json.load(fh)
            except ValueError:
                return ["tools/REJECTS.json is unparseable"]
    return [f"merge dropped {r.get('kind')} {r.get('id')!r}: {r.get('why')}"
            for r in rej][:40]


@check("counts match the golden manifest")
def _golden(b):
    now = measure(b)
    if not os.path.exists(GOLDEN):
        return ["tools/GOLDEN.json missing — run with --update-golden to establish it"]
    want = json.load(open(GOLDEN, encoding="utf-8"))["counts"]
    bad = []
    for k, v in want.items():
        if now.get(k) != v:
            bad.append(f"{k}: golden {v!r} -> now {now.get(k)!r}")
    return bad


# ---------------------------------------------------------------------------
# idempotency: the check that would have caught the 35 lost dates.
# ---------------------------------------------------------------------------

def _idempotent_targets():
    """Every file the build writes that a reader or a later stage consumes."""
    out = []
    appdata = os.path.join(ROOT, "app", "public", "data")
    for dirpath, _dirs, files in os.walk(appdata):
        for f in files:
            out.append(os.path.join(dirpath, f))
    for rel in ("the-program.json", "l0-model.json", "l0-layout-model.json",
                "foia-links.json"):
        out.append(os.path.join(ROOT, "data", rel))
    return sorted(out)


def check_idempotent():
    """Run the full documented pipeline twice and require identical output.

    This is the check that catches a whole CLASS of bug rather than one instance:
    any pass that reads its own previous output back in and forgets what it did.
    It is slow, so it is opt-in via --idempotent.

    The pipeline is tools/build.py, the one build order. Until 25 September 2026
    this listed the steps itself and hashed the old single-file shell; it now
    hashes every file under app/public/data, which is what the app serves, plus
    the four data/ build products the rest of the gate reads.
    """
    stamp = re.compile(rb'"generated"\s*:\s*"\d{4}-\d{2}-\d{2}"')

    def build_once():
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py")],
                           capture_output=True, cwd=ROOT)
        if r.returncode != 0:
            out = (r.stdout.decode(errors="replace") + r.stderr.decode(errors="replace"))
            return None, f"tools/build.py exited {r.returncode}: {out[-400:]}"
        # Several products carry a "generated":"YYYY-MM-DD" stamp. Hashing it makes
        # this check fail for a build that straddles midnight UTC -- a real, rare,
        # maximally confusing false failure, since nothing is actually
        # non-deterministic and a re-run passes. Neutralise the stamp, and CRLF,
        # and hash everything else.
        hashes = {}
        for path in _idempotent_targets():
            if not os.path.exists(path):
                hashes[path] = "absent"
                continue
            raw = open(path, "rb").read().replace(b"\r\n", b"\n")
            raw = stamp.sub(b'"generated":"<stamped>"', raw)
            hashes[path] = hashlib.sha256(raw).hexdigest()
        return hashes, None

    h1, err = build_once()
    if err:
        return [err]
    h2, err = build_once()
    if err:
        return [err]
    differ = sorted(os.path.relpath(p, ROOT).replace(os.sep, "/")
                    for p in set(h1) | set(h2) if h1.get(p) != h2.get(p))
    if differ:
        return [f"pipeline is NOT idempotent: {len(differ)} file(s) differ between two "
                f"consecutive builds. Something reads its own output back in."] + differ[:12]
    return []


# ---------------------------------------------------------------------------
# self-test — every check must be shown capable of failing.
# ---------------------------------------------------------------------------

def self_test():
    """Feed each check input it MUST reject. A check that passes here is broken,
    and a broken check is worse than no check because it reads as evidence."""
    # The fixture carries the real shape: eight classes and four strands.
    base = {"people": [{"id": "a-b", "cls": "person", "label": "Ann Bee", "claims": []}],
            "entities": [{"id": f"e{i}", "cls": c, "label": f"E{i}", "claims": []}
                         for i, c in enumerate(["institution", "program", "location",
                                                "domain", "legislation", "document",
                                                "event"])],
            "edges": [], "timeline": [{"strand": "program"}, {"strand": "witness"},
                                      {"strand": "oversight"}, {"strand": "coverup"}]}

    def mut(f):
        import copy
        b = copy.deepcopy(base)
        f(b)
        return b

    poisons = {
        "ids are canonical": mut(lambda b: b["people"].append(
            {"id": "p-a-b", "cls": "person", "label": "Ann Bee", "claims": []})),
        "no label is its own id": mut(lambda b: b["people"][0].update(label="a-b")),
        "person plate names are meaningful": mut(lambda b: b["people"][0].update(
            label="James R. Clapper Jr.") or b["people"][0].update(label="Jr.")),
        "no dangling references": mut(lambda b: b["edges"].append(
            {"a": "a-b", "b": "ghost", "type": "custody"})),
        "every person back-reference resolves": mut(
            lambda b: b["people"][0].update(locId="l-ghost")),
        "sequence chains are renderable": mut(
            lambda b: b["people"][0].update(sequenceChain=["a-node-id"])),
        "affiliations render as names, not ids": mut(
            lambda b: b["people"][0].update(affiliations=["some-ghost-org"])),
        "no unapproved duplicate nodes": mut(lambda b: (
            b["entities"][0].update(label="Twin Report",
                                    sources=[{"url": "https://example.gov/twin.pdf"}]),
            b["entities"].append({"id": "e-twin", "cls": b["entities"][0]["cls"],
                                  "label": "Twin Report", "claims": [],
                                  "sources": [{"url": "https://example.gov/twin.pdf"}]}))),
        "no Tier 1 edge rests only on a secondary source": mut(lambda b: b["edges"].append(
            {"a": "a-b", "b": "a-b", "type": "institutional", "claimTier": 1, "note": "x",
             "sources": [{"name": "Wikipedia - Something",
                          "url": "https://en.wikipedia.org/wiki/Something"}]})),
        # an external fact about a third party, on an aaro.mil page alone, graded
        # "documented": the exact shape of the 82 edges found on 1 September 2026
        "no Tier 1 edge rests on an interested party asserting an external fact": mut(
            lambda b: b["edges"].append(
                {"a": "a-b", "b": "e0", "type": "behavioral", "claimTier": 1,
                 "note": "Ann Bee left the office in 2023 and joined E0 as its chief technologist.",
                 "sources": [{"name": "AARO UAP Records",
                              "url": "https://www.aaro.mil/UAP-Records/"}]})),
        "no edge note leaks build bookkeeping": mut(lambda b: b["edges"].append(
            {"a": "a-b", "b": "a-b", "type": "custody",
             "note": "Asserts a thing. [Re-pointed from the collapsed duplicate `x`, 14 Aug 2026.]"})),
        "claim tiers are valid and Tier 1 is sourced": mut(lambda b: b["people"][0]["claims"].append(
            {"tier": 1, "text": "x", "source": ""})),
        # a Tier A node with no sourced URL: the 0.35 discount let one through
        "every Tier A node rests on at least one sourced URL": mut(
            lambda b: b["entities"][0].update(tier="A", sources=[{"name": "a recollection"}])),
        # the 120-character key's failure: one long claim, twice
        "no node carries a claim twice": mut(lambda b: b["people"][0]["claims"].extend(
            [{"tier": 2, "text": "A long claim " + "x" * 130, "source": "s"},
             {"tier": 2, "text": "A long claim " + "x" * 130, "source": "s"}])),
        # both vocabularies in one field, the shape of 1,076 events before phase 3
        "no timeline event ships a tier mixing two vocabularies": mut(
            lambda b: b["timeline"].extend([{"id": "t-a", "strand": "program", "tier": "A"},
                                            {"id": "t-1", "strand": "program", "tier": "1"}])),
        "no display label carries a spaced em dash": mut(
            lambda b: b["people"][0].update(label="Ann Bee \u2014 the witness")),
    }
    # Checks that compare research/ or a tools/ report against the REAL board: the
    # synthetic fixture cannot stand in for it, so each poison is a mutated copy of
    # the real board, and the clean call is the real board itself.
    def _drop_unverified(rb):
        for e in rb["entities"]:
            if e["id"] == "s-4-papoose-lake" and e.get("unverified"):
                e["unverified"] = e["unverified"][:-1]
                return
        for e in rb["entities"]:
            if e.get("unverified"):
                e["unverified"] = e["unverified"][:-1]
                return

    def _drop_open_questions(rb):
        for e in rb["entities"]:
            if e.get("openQuestions"):
                e["openQuestions"] = []
                return

    def _strip_one_verdict(rb):
        for e in rb["edges"]:
            if e["type"] == "denial" and e.get("denialKind"):
                del e["denialKind"]
                return

    def _adjudicate_one_listed(rb):
        # the other direction: an edge the report lists acquires a verdict and the
        # report is not regenerated
        rep = json.load(open(UNADJ, encoding="utf-8")) if os.path.exists(UNADJ) else []
        if not rep:
            return
        k = {rep[0]["a"], rep[0]["b"]}
        for e in rb["edges"]:
            if e["type"] == "denial" and {e["a"], e["b"]} == k:
                e["denialKind"] = "directed"

    def _drop_carried_claim(rb):
        # the pre-fix state on one node: setka-program without setka's claims
        for e in rb["entities"]:
            if e["id"] == "setka-program":
                e["claims"] = e["claims"][:7]

    def _unlist_the_domain_collapse(rb):
        # the report forgets the claims it could not place
        global _UNPLACED_OVERRIDE
        _UNPLACED_OVERRIDE = []

    poison_realboard = {
        "every authored claim reaches the board or is listed":
            [_drop_carried_claim, _unlist_the_domain_collapse],
        "every authored conflict, unverified note and open question on an entity reaches the board":
            [_drop_unverified, _drop_open_questions],
        "every denial edge without a verdict is in the unadjudicated report":
            [_strip_one_verdict, _adjudicate_one_listed],
    }
    # a vocabulary that has lost the row for the 32 `contains` edges
    poison_verbs = {
        "every authored edge verb is one of the twelve types or mapped in schema/vocab.json": [
            {k: v for k, v in _MERGE_VERB_MAP.items() if k != "contains"},
            {**_MERGE_VERB_MAP, "contains": {"type": "membership"}},
        ],
    }
    # ---- L0 fixtures. Each L0 check gets a model it MUST reject, through
    # _L0_OVERRIDE; its clean call gets L0() through the same channel.
    def L0(**kw):
        m = {"config": {"sharedMemberGate": 2},
             "counts": {"total": 8, "l0": 1, "ledger": 1, "pathOnly": 0,
                        "unattached": 6},
             "l0": [{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                     "dossier": {"narrative": "why e0 is on the map",
                                 "claims": [{"text": "x", "tier": 1, "source": "https://e"}]}}],
             "directEdges": [], "summarised": [], "pathOnly": [],
             "unattached": [{"id": "e%d" % i, "deg": 0} for i in range(1, 7)],
             "connections": {}, "authority": {},
             "nodes": {"a-b": ["Ann Bee", "person", 1, "A"],
                       **{"e%d" % i: ["E%d" % i, "institution", 0, "B"] for i in range(7)}}}
        m.update(kw)
        return m

    # a board with the hand-written edges the tier and gate poisons rest on
    l0board = mut(lambda b: b["edges"].extend([
        {"a": "e0", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "a-b", "type": "custody", "claimTier": 1},
        {"a": "e0", "b": "e2", "type": "custody", "claimTier": 1},
        {"a": "e1", "b": "e2", "type": "custody", "claimTier": 1}]))
    two_l0 = [{"id": "e0", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}},
              {"id": "e1", "direct": ["a-b", "e2"], "routed": [], "mix": {"person": 1, "institution": 1}}]

    poisons.update({
        # a summarised edge printing Tier 3 over two Tier 1 links
        "summarised edge tier is the strongest of its underlying links": l0board,
        "the shared-member gate holds and only hand-written edges are summarised": l0board,
    })
    _l0_dosn = {"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                "dossier": {"narrative": "why e0 is on the map",
                            "claims": [{"text": "x", "tier": 1, "source": "https://e"}]}}
    poison_l0 = {
        # a node on the map with no argument for why it is there
        "every L0 node carries an entity dossier":
            (L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1}}])),
        # an unsourced claim, which is the one rule that never bends
        "every dossier claim is tiered and sourced":
            (L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [], "mix": {"person": 1},
                         "dossier": {"narrative": "n",
                                     "claims": [{"text": "x", "tier": 1, "source": ""}]}}])),
        # registers that do not sum to the board
        "register partition is total":
            (L0(counts={"total": 8, "l0": 1, "ledger": 1, "pathOnly": 0, "unattached": 5})),
        "summarised edge tier is the strongest of its underlying links":
            (L0(l0=two_l0, counts={"total": 8, "l0": 2, "ledger": 1, "pathOnly": 0, "unattached": 5},
                    summarised=[{"a": "e0", "b": "e1", "n": 2, "tier": 3,
                                 "via": ["a-b", "e2"], "links": 4}])),
        # one shared member is not a summary, it is a restatement — and 420 of them
        # would have been drawn on the real board
        "the shared-member gate holds and only hand-written edges are summarised":
            (L0(l0=two_l0, counts={"total": 8, "l0": 2, "ledger": 1, "pathOnly": 0, "unattached": 5},
                    summarised=[{"a": "e0", "b": "e1", "n": 1, "tier": 1,
                                 "via": ["a-b"], "links": 2}])),
        # an edge drawn to an unattached entity
        "no routed or path-only entity emits an edge instance":
            (L0(directEdges=[{"a": "e0", "b": "e3", "n": 1, "tier": 1, "types": ["custody"]}])),
        # the class bar says two members, the ledger lists one
        "every L0 node's class bar sums to the members it lists":
            (L0(l0=[{"id": "e0", "direct": ["a-b"], "routed": [],
                         "mix": {"person": 1, "document": 1}}])),
        # the matcher going loose, plus an uncited authority claim
        "structural authority is cited, and the exclusions hold":
            (L0(authority={"susan-gough": {"authority": "x", "instruments": [],
                                               "weight": 3, "tense": "holds",
                                               "publicRecord": {"connections": 0}}})),
        # a connection row with no edge behind it: something generated it
        "every connection row is backed by a hand-written edge":
            (L0(connections={"e0": [{"id": "a-b", "type": "custody", "tier": 1,
                                         "label": "Ann Bee", "cls": "person",
                                         "dir": "out", "why": "", "note": ""}]})),
        # the JR., J. reappearance site: a via that resolves to nothing
        "every routed row names its intermediate resolvably":
            (L0(l0=[{"id": "e0", "direct": [], "mix": {},
                         "routed": [{"id": "e4", "depth": 2, "via": ["ghost"]}]}])),
        # a dossier claim graded documented on an encyclopedia entry, and one on
        # an aaro.mil page asserting a fact about somebody else
        "no Tier 1 dossier claim breaks the node-claim sourcing rules":
            (L0(dossiers={"e0": {"claims": [
                {"text": "E0 was founded in 1952.", "tier": 1,
                 "source": "https://en.wikipedia.org/wiki/E0"},
                {"text": "Ann Bee joined E0 in 2023.", "tier": 1,
                 "source": "https://www.aaro.mil/UAP-Records/ and https://www.congress.gov/x"}]}})),
    }

    # ---- Design's nine, from DESIGN-RESPONSE-LAYOUT-2026-08-24 section 5 ----------
    # Each poison is the specific input Design named in the "must reject" column.
    # These checks read a build product on disk rather than the synthetic board, so
    # they get their own channel: _LAYOUT_OVERRIDE, set around the call below.
    _real = _layout()
    # Design's checks compare the MODEL against the board it was built from, so the
    # synthetic fixture is the wrong input for them -- every L0 node would show zero
    # neighbours and the degree check would false-positive on clean data. It did,
    # the first time this ran. Give them the real board on both the poisoned and the
    # clean call; what varies between the two is the model, which is the thing under
    # test.
    _real_board = None
    if os.path.exists(BOARD):
        with open(BOARD, encoding="utf-8") as fh:
            _real_board = json.load(fh)
    _real_patents = _patents()
    _real_obs = _observables()
    _real_foia = _foia()

    def lay(mut):
        """Deep-copy the real layout model and break it one way."""
        m = copy.deepcopy(_real)
        mut(m)
        return m

    def _bloat(m):
        # the failure this whole correction was about: a model over the read cap
        m["_bloat"] = ["x" * 4096 for _ in range(300)]

    def _undated_into_an_era(m):
        for n in m["current"]["nodes"]:
            if n.get("y0") in (None, ""):
                n["col"] = 3          # parked in a real era column
                return

    def _bare_node(m):
        for n in m["current"]["nodes"]:
            if (n.get("allEdges") or 0) > 0:
                n["restEdges"] = 0    # clause 1 without clause 2
                return

    # The reject list is a build product too, and the check that reads it needs to be
    # shown failing for the same reason every other check does.
    poison_rejects = {
        "no research record is silently dropped":
            [{"kind": "entity", "id": "usc-10-119", "why": "bad cls 'statute'"}],
    }

    # The register is empty, so the check passes on an empty dict and the poison has
    # to be a record. Four ways to intend an image and silently not publish one, plus
    # the credit rule, which is a licensing failure rather than a rendering one.
    poison_shorts = {
        # Two ways a chip lies: a label too long for it, and a label shared with
        # another node. Both, so neither half of the check goes untested.
        "every chip label fits the chip it is drawn in": [
            lay(lambda m: m["current"]["nodes"][0].update(
                short="A label far longer than the thirty-seven characters a chip can hold")),
            lay(lambda m: m["current"]["nodes"][1].update(
                short=m["current"]["nodes"][0]["short"])),
        ],
    }

    poison_images = {
        "nothing in the image register fails silently": {"images": {
            # clears, and nothing to draw
            "a-b": {"clearance": "clears", "photo": "", "photoCredit": "x"},
            # ask, with the reason dropped
            "e0": {"clearance": "ask", "photo": "p.jpg", "photoCredit": "x"},
            # a seal that the renderer would be free to crop to a circle
            "e1": {"clearance": "clears", "photo": "p.jpg", "photoCredit": "x",
                   "photoKind": "logo"},
            # published with no attribution
            "e2": {"clearance": "clears", "photo": "p.jpg"},
            # a clearance word the renderer has never heard of
            "e3": {"clearance": "probably fine", "photo": "p.jpg", "photoCredit": "x"},
        }},
    }

    # THE PATENTS TAB. Its content lives in two authored files rather than in the
    # renderer, so it gets its own poison channel, the same pattern as the image
    # register's and the layout model's. Each poison is the mistake the check exists
    # to catch, not a mangled predicate.
    import copy as _copy

    def _pat(fn):
        d = _copy.deepcopy(_real_patents) if _real_patents else {}
        fn(d)
        return d

    def _obs(fn):
        d = _copy.deepcopy(_real_obs) if _real_obs else {}
        fn(d)
        return d

    def _misquote(d):
        # one word changed in a quotation. It still reads plausibly, cites the same
        # document, and is not in it.
        d["quotes"][1]["text"] = d["quotes"][1]["text"].replace(
            "the math and physics are sound", "the math and physics are unsound")

    def _stray_emphasis(d):
        d["quotes"][0]["emphasis"] = "beyond the state of the art"

    poison_patents = {} if _real_patents is None else {
        "every patents-tab quotation is verbatim in the document it cites":
            _pat(_misquote),
        "no patents-tab quotation is edited by its own highlight":
            _pat(_stray_emphasis),
        "the patents tab prints what it does not have": [
            # a wrapper that lists only what was obtained reads as complete
            _pat(lambda d: d["wrapper"].update(absent=[])),
            # EXPIRED asserted with no date behind it
            _pat(lambda d: d["filings"][0].pop("expired", None)),
            # a status the renderer does not style
            _pat(lambda d: d["filings"][2]["status"].append("PENDING")),
        ],
    }
    def _foi(fn):
        d = _copy.deepcopy(_real_foia) if _real_foia else {}
        fn(d)
        return d

    poison_foia = {} if _real_foia is None else {
        "every FOIA request points at a question that is actually open": [
            # a node renamed under a letter written against the old id
            _foi(lambda d: d["byNode"].setdefault("a-node-that-was-renamed",
                 [{"request": "F1", "agency": "NARA", "title": "x", "status": "not filed",
                   "questions": [0], "partial": []}])),
            # a research pass removed an open question and the indices shifted
            _foi(lambda d: d["byNode"]["yankee-blue"][0]["questions"].append(99)),
            # a status the board does not know how to draw
            _foi(lambda d: d["requests"][0].update(status="in progress")),
            # the parser read nothing and reported a clean run
            _foi(lambda d: d.update(requests=[])),
        ],
    }

    _real_threads = _threads()

    def _thr(fn):
        d = copy.deepcopy(_real_threads) if _real_threads else {}
        fn(d)
        return d

    def _unjoined(d):
        """The poison APP-SPEC section 5 names: a step spliced into a real thread
        with nothing on the board joining it to the step above. `aaro` and
        `harry-reid` are both real nodes and there is no edge between them, so this
        is exactly the failure the check exists to catch -- a chain that reads as a
        chain and is not one. Note it is inserted in the MIDDLE, not appended: a
        poison at the end would also be caught by the step-count bound, and then the
        join test would never have been exercised at all."""
        st = d["threads"][0]["steps"]
        st.insert(1, {"node": "aaro", "year": 2022,
                      "evidence": "spliced step with no joining edge",
                      "edge": {"type": "programmatic", "tier": 1,
                               "kind": "direct", "via": []}})
        st.pop()

    poison_threads = {} if _real_threads is None else {
        "every thread step is joined to the last by a board edge": [
            # the step that is not joined to the one above it
            _thr(_unjoined),
            # a real pair, a type the edge does not carry: the page would print a
            # relationship the board never recorded between two nodes that ARE joined
            _thr(lambda d: d["threads"][0]["steps"][1]["edge"].update(type="custody")),
            # a real pair and a real type, graded up one tier
            _thr(lambda d: d["threads"][1]["steps"][2]["edge"].update(tier=1)),
            # a documented link relabelled as an inference
            _thr(lambda d: d["threads"][0]["steps"][1]["edge"].update(
                kind="derived", via=["harry-reid"])),
            # an id that does not exist -- a rename upstream, or a typo
            _thr(lambda d: d["threads"][2]["steps"][3].update(node="dod-sapco-office")),
            # a step with no evidence line: it asserts the join and says nothing
            _thr(lambda d: d["threads"][3]["steps"][4].update(evidence="  ")),
            # a thread cut below the floor of five steps
            _thr(lambda d: d["threads"][4].update(steps=d["threads"][4]["steps"][:3])),
        ],
    }

    poison_obs = {} if _real_obs is None else {
        "the five observables stay Tier 2, and the mapping stays separate": [
            # the taxonomy promoted to the grade its mapping earned
            _obs(lambda d: d.update(tier=1)),
            # five of five: the easy overclaim
            _obs(lambda d: d["mappings"][0]["rows"][4].update(met=True)),
        ],
    }

    poison_layout = {} if _real is None else {
        # a model baked from the extract's `deg` field, which counts edge INSTANCES
        "L0 degree is distinct neighbours, not edge instances":
            lay(lambda m: m["current"]["nodes"][0].update(
                deg=(m["current"]["nodes"][0].get("deg") or 0) + 40)),
        # a hand-edited figure in the write-up
        "every layout figure recomputes from the model":
            lay(lambda m: m["current"]["figures"].update(l0=107)),
        # clause 1 shipped without clause 2 -- nodes drawn with no line at all
        "no L0 node with a link is left without a line": lay(_bare_node),
        # an undated node placed in an era column
        "absent prints as absent": lay(_undated_into_an_era),
        # more than one distinct chip size
        "chip size is not a channel":
            lay(lambda m: m["current"]["nodes"][0].update(w=260)),
        # a re-introduced force pass, which settles on fractional coordinates
        "layout positions are grid-derived, not force-derived":
            lay(lambda m: m["current"]["nodes"][0].update(x=418.37)),
        # a time-direction flow on every line
        "motion is attested, not decorative":
            lay(lambda m: [e.update(flow="time") for e in m["current"]["edges"]]),
        # a queue that has stopped naming a field the renderer reads
        # Two poisons, one per direction. A field the data withholds and the
        # queue does not name; and a row naming work the data has already done.
        "every field the design reads but the data withholds is in the backfill queue": [
            # Aimed at `photo`, which the register keeps deliberately empty, so
            # this poison stays valid for as long as that is true. It used to drop
            # the denialKind row -- and when the 174 denials were adjudicated on
            # 26 August, dropping that row became the CORRECT state and the poison
            # silently stopped poisoning. A poison aimed at a field that might get
            # filled has the same expiry date as the check it guards.
            lay(lambda m: m.__setitem__(
                "gaps", [r for r in m["gaps"] if "photo" not in str(r[0])])),
            lay(lambda m: m["gaps"].append(
                ["C / A / D", "the three scored axes per node",
                 "straight off the board records", "band order is the measured mean C"])),
        ],
        # a research pass that inverts a near-tie on the shipping dataset
        "the rarity order the board implies still matches the pin":
            lay(lambda m: m["current"]["figures"].update(
                rarityObserved=list(reversed(m["current"]["figures"]["rarityPin"])))),
        # a denier invented for an edge, naming a node that is not even on it --
        # which is what publishing a direction derived from [a,b].sort() amounts to
        "denial direction is published only where the record names a denier":
            lay(lambda m: [e.update(denier="not-an-end-of-this-edge")
                           for e in m["current"]["edges"] if e.get("denial")]),
        # a third denial state invented, or an association that also claims a denier
        "a denial that is not a directed act carries no denial styling":
            lay(lambda m: [e.update(denialKind="probably-a-denial")
                           for e in m["current"]["edges"] if e.get("denial")]),
        # a flag naming an id the floor excluded
        "highlights are a pointer, not a promotion":
            lay(lambda m: m["current"]["highlights"]["flags"].append(
                {"id": "not-on-this-map", "why": "x"})),
        # the model over the ~1MB read cap
        "the layout model stays under the read cap": lay(_bloat),
    }

    print("self-test — each check must REJECT poisoned input\n")
    ok = True
    poison_layout.update(poison_shorts)

    for name, fn in CHECKS_RUN:
        if name == "counts match the golden manifest":
            print(f"  n/a   {name} (drift tripwire, not a property)")
            continue
        if name in poison_l0:
            global _L0_OVERRIDE
            _L0_OVERRIDE = poison_l0[name]
            try:
                caught = fn(poisons.get(name, base))
            finally:
                _L0_OVERRIDE = L0()
            try:
                clean = fn(base)
            finally:
                _L0_OVERRIDE = None
        elif name in poison_realboard:
            # every poison must be rejected, and the real board must pass
            if _real_board is None:
                print(f"  FAIL  {name}: data/the-program.json missing, nothing to poison")
                ok = False
                continue
            caught = []
            for mutate in poison_realboard[name]:
                pb = copy.deepcopy(_real_board)
                global _UNPLACED_OVERRIDE
                try:
                    mutate(pb)
                    got = fn(pb)
                finally:
                    _UNPLACED_OVERRIDE = None     # a poison may set a report override
                if not got:
                    caught = []
                    print(f"  FAIL  {name} accepted its poison {mutate.__name__}")
                    break
                caught = caught + got
            clean = fn(_real_board)
        elif name in poison_verbs:
            global _VERB_MAP_OVERRIDE
            caught = []
            for vm in poison_verbs[name]:
                _VERB_MAP_OVERRIDE = vm
                try:
                    got = fn(base)
                finally:
                    _VERB_MAP_OVERRIDE = None
                if not got:
                    caught = []
                    print(f"  FAIL  {name} accepted one of its poisons")
                    break
                caught = caught + got
            clean = fn(_real_board if _real_board is not None else base)
        elif name in poison_rejects:
            global _REJECTS_OVERRIDE
            _REJECTS_OVERRIDE = poison_rejects[name]
            try:
                caught = fn(base)
            finally:
                _REJECTS_OVERRIDE = []
            clean = fn(base)
            _REJECTS_OVERRIDE = None
        elif name in poison_images:
            global _IMAGES_OVERRIDE
            _IMAGES_OVERRIDE = poison_images[name]
            try:
                caught = fn(base)
            finally:
                _IMAGES_OVERRIDE = None
            clean = fn(base)
        elif name in poison_foia:
            global _FOIA_OVERRIDE
            caught = []
            for one in poison_foia[name]:
                _FOIA_OVERRIDE = one
                try:
                    got = fn(base)
                finally:
                    _FOIA_OVERRIDE = None
                if not got:
                    caught = []
                    print(f"  FAIL  {name} accepted one of its poisons")
                    break
                caught = got
            clean = fn(base)
        elif name in poison_threads:
            # Seven poisons, one per clause: every clause a check asserts needs its
            # own, or the untested ones are indistinguishable from broken.
            global _THREADS_OVERRIDE
            caught = []
            for one in poison_threads[name]:
                _THREADS_OVERRIDE = one
                try:
                    got = fn(base)
                finally:
                    _THREADS_OVERRIDE = None
                if not got:
                    caught = []
                    print(f"  FAIL  {name} accepted one of its poisons")
                    break
                caught = got
            clean = fn(base)
        elif name in poison_patents or name in poison_obs:
            # A check may carry SEVERAL poisons and every one must be rejected;
            # one poison per check is only enough when the check asserts one thing,
            # and `the patents tab prints what it does not have` asserts three.
            global _PATENTS_OVERRIDE, _OBS_OVERRIDE
            ps = poison_patents.get(name) or poison_obs.get(name)
            if isinstance(ps, dict):
                ps = [ps]
            in_obs = name in poison_obs
            caught = []
            for one in ps:
                if in_obs:
                    _OBS_OVERRIDE = one
                else:
                    _PATENTS_OVERRIDE = one
                try:
                    got = fn(base)
                finally:
                    _PATENTS_OVERRIDE = None
                    _OBS_OVERRIDE = None
                if not got:
                    # name the poison that slipped through rather than just failing
                    caught = []
                    print(f"  FAIL  {name} accepted one of its poisons")
                    break
                caught = got
            clean = fn(base)
        elif name in poison_layout:
            global _LAYOUT_OVERRIDE
            lb = _real_board if _real_board is not None else base
            # A check may carry SEVERAL poisons, and every one must be rejected.
            # One poison per check is only enough when the check asserts one
            # thing. The backfill-queue check asserts two opposite things -- that
            # a missing field is queued, and that a queued field is still
            # missing -- and a single poison would leave whichever half it did
            # not touch untested. That is how the second half came to be absent
            # for two days in the first place.
            ps = poison_layout[name]
            if not isinstance(ps, list):
                ps = [ps]
            caught = []
            for pz in ps:
                _LAYOUT_OVERRIDE = pz
                try:
                    got = fn(lb)
                finally:
                    _LAYOUT_OVERRIDE = None
                if not got:
                    caught = []          # one poison slipped through: the check is dead
                    break
                caught = caught + got
            clean = fn(lb)
        else:
            caught = fn(poisons.get(name, base))
            clean = fn(base)
        if not caught:
            print(f"  FAIL  {name}: did NOT reject poisoned input — this check is dead")
            ok = False
        elif clean:
            print(f"  FAIL  {name}: rejects CLEAN input too ({clean[0][:70]}) — false positive")
            ok = False
        else:
            print(f"  ok    {name}: rejects bad, accepts good")
    print()
    return ok


def main():
    args = sys.argv[1:]
    if "--self-test" in args:
        return 0 if self_test() else 1

    if not os.path.exists(BOARD):
        print("data/the-program.json missing — run merge.py", file=sys.stderr)
        return 1
    b = json.load(open(BOARD, encoding="utf-8"))

    if "--update-golden" in args:
        json.dump({"note": "Deliberately accepted counts. Every change here should be "
                           "explainable in the commit message.",
                   "counts": measure(b)},
                  open(GOLDEN, "w", encoding="utf-8"), indent=1)
        print("wrote tools/GOLDEN.json")
        return 0

    print("=== verify ===")
    failed = 0
    for name, fn in CHECKS_RUN:
        problems = fn(b)
        if problems:
            failed += 1
            print(f"  FAIL  {name}  ({len(problems)})")
            for p in problems[:8]:
                print(f"          {p}")
            if len(problems) > 8:
                print(f"          ... and {len(problems)-8} more")
        else:
            print(f"  ok    {name}")

    if "--idempotent" in args:
        problems = check_idempotent()
        if problems:
            failed += 1
            print("  FAIL  pipeline is idempotent")
            for p in problems:
                print(f"          {p}")
        else:
            print("  ok    pipeline is idempotent (two full builds, identical output)")

    print()
    if failed:
        print(f"!! {failed} CHECK(S) FAILED — do not ship this build")
    else:
        print("all checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
