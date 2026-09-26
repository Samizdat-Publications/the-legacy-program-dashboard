#!/usr/bin/env python3
"""claim_meta.py: who made each claim, when, and by what route (redesign phase 10, task 1).

research/_claim_meta.json is AUTHORED. It carries one row per claim in scope:

    "c-0123456789": {
        "claimant":     a node id (a person, or an institution for an office's
                        statement) or null when the speaker is not on the board,
        "speaker":      the speaker as the record names them (required when claimant
                        is null; "unnamed" when the record names nobody),
        "artefactDate": when the claim was MADE (the dated artefact of the claim),
                        YYYY, YYYY-MM or YYYY-MM-DD, or null,
        "eventDate":    when the thing claimed HAPPENED, same forms, or null,
        "route":        hearing | broadcast | interview | book | filing | press | document,
        "via":          who brought the claim to the record, as the record names them
                        (the show, the host, the committee, the outlet), or null,
        "by":           which pass wrote the row,
        "verified":     optional, which pass checked it against the claim
    }

Scope: every Tier 2 claim, and every Tier 1 claim the "said on the record" rule of
app/src/attrib.ts marks (`said` or `office`). A Tier 3 claim is the board's own
inference and has no claimant but the board.

This tool never overwrites a row a later pass wrote. `propose` fills rows the
mechanical rules settle (the "On <show>, <date>, <speaker> said" pattern, a named
speaker opening the claim, an attribution opening a claim on a person's own node)
and writes packets of the rest for the Sonnet batches; `merge` validates proposal
files and folds them in; `stats` prints coverage. verify.py holds the side-car to
its rules by its own route and does not import this file.

    python tools/claims/claim_meta.py stats
    python tools/claims/claim_meta.py propose --packets <dir> [--size 450]
    python tools/claims/claim_meta.py merge <proposal.json> [...] --by "<pass>"
    python tools/claims/claim_meta.py sample <n> --out <file>   (for verification)
"""
import argparse
import json
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOARD = os.path.join(ROOT, "data", "the-program.json")
META = os.path.join(ROOT, "research", "_claim_meta.json")
ROUTES = ("hearing", "broadcast", "interview", "book", "filing", "press", "document")
DATE_RX = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")

# ------------------------------------------------------------------ the said rule
# A port of app/src/attrib.ts saidKind(), which decides which Tier 1 claims record
# that something was SAID. Kept in step by hand; verify.py carries its own port.
OPEN = re.compile(r"""^['"‘“]?(?:Sworn\b|Under oath\b|Testif(?:ied|ies|ying)\b|In (?:sworn |his |her |their |written )?testimony\b|Stated\b|States:|Said\b|Says\b|Told\b|Tells\b|According to\b|Asked\b|Answering\b|Attributed\b|Elicited\b|Claimed\b|Claims\b|Alleged\b|Alleges\b)""", re.I)
SPEAKER = re.compile(r"""^(?:[A-Z][\w.'’&()-]*\s){0,4}(?!(?:The|A|An|Its|Their|His|Her|This|That|These|Those)\s)[A-Z][\w.'’&()-]*\s(?:said|says|stated|states|testified|testifies|told|tells|swore|alleged|alleges|claimed|claims|asserted|asserts|declared|declares|responded|replied|answered)\b""")
DOC_SUBJECT = re.compile(r"\b(?:Report|Paper|Assessment|Memo|Memorandum|Brief|Charter|Act|Volume|Document|Instruction|Directive|Manual|Order|FAQ|JANAP|Condon|NSDD|DIA-\d)")
SPEECH_SOURCE = re.compile(r"\b(?:sworn|testimony|testified|deposition|affidavit|spokes(?:man|woman|person)|(?:opening|written|prepared|emailed|joint|DoD|Navy|NASA|Pentagon|federal) statement|statement (?:for the record|to|following|by|attributed)|remarks|press conference(?! photographs)|media roundtable|media engagement)\b", re.I)
ABOUT_THE_RECORD = re.compile(r"^(?:Held\b|Official hearing record|The (?:hearing|transcript|document|record|report|letter|memo)\b|Its core|Page \d|Sole witness|Witness of record|Called as|Appeared as|Listed in|Written testimony filed)", re.I)
QUOTE_SOURCE = re.compile(r"\b(?:transcript|hearing|statement(?! of work)|interview)\b", re.I)
OFFICE_DOMAIN = re.compile(r"(^|\.)(?:aaro\.mil|defense\.gov|war\.gov)$", re.I)
OFFICE_SOURCE = re.compile(r"^(?:AARO|All-domain Anomaly Resolution Office)\b", re.I)
URL = re.compile(r"https?://\S+")


def first_host(s):
    m = re.search(r"https?://([^/?#:\s)\]]+)", s or "", re.I)
    return m.group(1).lower() if m else ""


def said_kind(tier, text, source):
    """'said', 'office' or None, exactly as attrib.ts decides it."""
    if tier != 1:
        return None
    t = text or ""
    src = source or ""
    s = URL.sub(" ", src)
    if OPEN.search(t):
        return "said"
    m = SPEAKER.search(t)
    if m and not DOC_SUBJECT.search(m.group(0)):
        return "said"
    if not ABOUT_THE_RECORD.search(t) and SPEECH_SOURCE.search(s):
        return "said"
    if re.match(r"""^['"‘“]""", t) and QUOTE_SOURCE.search(s):
        return "said"
    if OFFICE_DOMAIN.search(first_host(src)) or OFFICE_SOURCE.search(s.strip()):
        return "office"
    return None


# ------------------------------------------------------------------------ io

def rd(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def board():
    b = rd(BOARD)
    nodes = b["people"] + b["entities"]
    return b, nodes, {n["id"]: n for n in nodes}


def in_scope(nodes):
    """[(node, claim, kind)] for every claim in scope, in claim-id order."""
    out = []
    for n in nodes:
        for c in n.get("claims") or []:
            if not c.get("id"):
                continue
            t = c.get("tier")
            k = said_kind(t, c.get("text"), c.get("source"))
            if t == 2 or k:
                out.append((n, c, k or ("t2" if t == 2 else None)))
    out.sort(key=lambda x: x[1]["id"])
    return out


def load_meta():
    if not os.path.exists(META):
        return {"_what": WHAT, "_rules": RULES, "claims": {}}
    return rd(META)


def save_meta(doc):
    doc["claims"] = dict(sorted(doc["claims"].items()))
    with open(META, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


WHAT = ("Who made each claim, when, and by what route (redesign phase 10, task 1). One row per "
        "Tier 2 claim and per Tier 1 claim marked 'said on the record' or 'the office's own "
        "account'. Authored: written by tools/claims/claim_meta.py's mechanical pass and by "
        "reviewed Sonnet batches, sampled and verified by Opus; read by tools/build_app_data.py.")
RULES = [
    "claimant: the node whose word the claim rests on (a person, or an institution for an office's "
    "statement or publication). null only when that speaker is not on the board, and then `speaker` "
    "names them as the record does ('unnamed' when the record names nobody).",
    "artefactDate: when the claim was made, the date of its artefact (the hearing, the episode, the "
    "book, the filing, the article, the document). An access date is not an artefact date.",
    "eventDate: when the thing claimed happened, or null when the claim names no time.",
    "route: hearing (testimony, deposition, sworn statement, briefing on the record), broadcast (a "
    "programme, documentary, talk or livestream), interview (a published interview or podcast), book, "
    "filing (a complaint, affidavit, lawsuit, IG or FOIA filing), press (an article, press release, "
    "statement to the press, op-ed or post), document (a report, letter, memo or web page).",
    "via: who brought the claim to the record, as the record names them (the show and host, the "
    "committee, the outlet), or null. It is what the notability rule asks of a claimant: by what "
    "route the claim reached us.",
]

# ------------------------------------------------------------------- dates
MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"])}
MON3 = {k[:3]: v for k, v in MONTHS.items()}
_M = r"(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?"
D_DMY = re.compile(r"\b(\d{1,2}) " + _M + r",? (\d{4})\b")
D_MDY = re.compile(r"\b" + _M + r" (\d{1,2}),? (\d{4})\b")
D_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
D_MY = re.compile(r"\b" + _M + r",? (\d{4})\b")
D_URL = re.compile(r"/(\d{4})/(\d{2}|[A-Z][a-z]{2})/(\d{1,2})/")
D_Y = re.compile(r"\b(1[89]\d{2}|20[0-3]\d)\b")
NOT_ARTEFACT = re.compile(r"(accessed|retrieved|visited|archived|viewed)\s*(on\s*)?$", re.I)


def _mon(s):
    s = s.lower().rstrip(".")
    return MONTHS.get(s) or MON3.get(s[:3])


def _ok(y, m=None, d=None):
    y = int(y)
    if not 1800 <= y <= 2030:
        return None
    if m is None:
        return "%04d" % y
    if not 1 <= m <= 12:
        return None
    if d is None:
        return "%04d-%02d" % (y, m)
    if not 1 <= int(d) <= 31:
        return None
    return "%04d-%02d-%02d" % (y, m, int(d))


def dates_in(s, skip_access=True):
    """[(position, date string, matched text)] for every date expression, most
    precise match at each position, access dates left out."""
    s = s or ""
    found = []
    taken = []

    def add(m, v):
        if v is None:
            return
        a, b = m.span()
        if any(a < y and x < b for x, y in taken):
            return
        if skip_access and NOT_ARTEFACT.search(s[max(0, a - 16):a]):
            taken.append((a, b))
            return
        taken.append((a, b))
        found.append((a, v, m.group(0)))
    for m in D_ISO.finditer(s):
        add(m, _ok(m.group(1), int(m.group(2)), m.group(3)))
    for m in D_DMY.finditer(s):
        add(m, _ok(m.group(3), _mon(m.group(2)), m.group(1)))
    for m in D_MDY.finditer(s):
        add(m, _ok(m.group(3), _mon(m.group(1)), m.group(2)))
    for m in D_URL.finditer(s):
        mo = m.group(2)
        mo = int(mo) if mo.isdigit() else _mon(mo)
        add(m, _ok(m.group(1), mo, m.group(3)))
    for m in D_MY.finditer(s):
        add(m, _ok(m.group(2), _mon(m.group(1))))
    for m in D_Y.finditer(s):
        add(m, _ok(m.group(1)))
    found.sort()
    return found


def best_date(s):
    """The most precise date in s, the first of equal precision; None when none."""
    ds = dates_in(s)
    if not ds:
        return None
    return sorted(ds, key=lambda x: (-len(x[1]), x[0]))[0][1]


# ------------------------------------------------------------------- routes
R_HEARING = re.compile(r"\b(hearing|testimony|testified|sworn|deposition|CHRG-|transcript of|opening statement|statement for the record|written statement|Task Force|briefing)\b", re.I)
R_FILING = re.compile(r"\b(complaint|affidavit|lawsuit|court|docket|filing|petition|v\.\s|ICIG|Inspector General complaint|FOIA request)\b", re.I)
R_INTERVIEW = re.compile(r"\b(American Alchemy|podcast|interview|episode|Rogan|Danny Jones|Joe Rogan|Weaponized|Need to Know|Theories of Everything|Shawn Ryan|Lex Fridman|Coast to Coast|Merged|Project Unity)\b", re.I)
R_BROADCAST = re.compile(r"\b(NewsNation|CBS|60 Minutes|CNN|Fox News|documentary|NBC|ABC News|BBC|History Channel|livestream|YouTube|broadcast|television|TV|Symposium|conference|lecture|talk)\b", re.I)
R_BOOK = re.compile(r"\b(book|ISBN|Press, \d{4}|Books\b|Forbidden Science|Simon & Schuster|HarperCollins|Crown|Random House|St\. Martin|memoir|pp\. \d)", re.I)
R_PRESS = re.compile(r"\b(New York Times|NYT|Washington Post|Politico|The Debrief|Liberation Times|The War Zone|Daily Mail|Guardian|Reuters|Associated Press|AP\b|Axios|press release|news release|op-ed|Scientific American|article|reported|X post|tweet|statement to|Post\b|Times\b|Herald|Journal\b|Magazine|Newsweek|HuffPost|Vice|Wired|Popular Mechanics|NewsNation article|defensescoop|breakingdefense)\b", re.I)


def route_of(source, text):
    s = source or ""
    for rx, r in ((R_HEARING, "hearing"), (R_FILING, "filing"), (R_INTERVIEW, "interview"),
                  (R_BOOK, "book"), (R_BROADCAST, "broadcast"), (R_PRESS, "press")):
        if rx.search(s):
            return r
    if R_HEARING.search(text or "") and re.search(r"\btestif", text or "", re.I):
        return "hearing"
    return None


# ------------------------------------------------------------------- names
SUFFIX = {"jr", "jr.", "sr", "sr.", "ii", "iii", "iv"}
TITLES = r"(?:Rep\.|Representative|Sen\.|Senator|Dr\.|Gen\.|General|Col\.|Colonel|Lt\.|Lieutenant|Cmdr\.|Commander|Adm\.|Admiral|Maj\.|Major|Capt\.|Captain|Mr\.|Ms\.|Mrs\.|Secretary|Director|Deputy Director|Former|former|then-|Navy pilot|pilot|physicist|journalist|whistleblower)"


def name_index(nodes):
    """{surname: [person ids]}, {full name form: person id}."""
    sur, full = {}, {}
    for n in nodes:
        if n.get("cls") != "person":
            continue
        lab = re.sub(r"\s*\(.*?\)", "", n.get("label") or "")
        lab = re.sub(r"'[^']*'\s*", "", lab)  # nickname in quotes
        toks = [t for t in lab.replace(",", " ").split() if t]
        core = [t for t in toks if t.lower() not in SUFFIX]
        if not core:
            continue
        last = core[-1]
        sur.setdefault(last, set()).add(n["id"])
        full[" ".join(core)] = n["id"]
        if len(core) >= 2:
            full[core[0] + " " + last] = n["id"]
            # first name + last without middle initials
            plain = [t for t in core if not re.match(r"^[A-Z]\.$", t)]
            full[" ".join(plain)] = n["id"]
    return {k: sorted(v) for k, v in sur.items()}, full


SPEECH_V = r"(said|says|stated|states|testified|testifies|told|tells|swore|alleged|alleges|claimed|claims|asserted|asserts|declared|declares|responded|replied|answered|described|recalled|recounted|explained|added|confirmed|denied|wrote|writes|argued|argues|identified|named|called|insisted|maintained|repeated|revealed|disclosed|recounts|describes|recalls|explains|confirms|denies|acknowledged|acknowledges|conceded|concedes|put it|gave|offered|suggested|suggests)"
ON_SHOW = re.compile(r"^On (?P<show>[^,]{3,120}?), (?P<date>\d{1,2} [A-Z][a-z]+ \d{4})(?:, (?:at|from) [\d:]+(?:\s*(?:to|-)\s*[\d:]+)?)?, (?P<speaker>.{2,90}?) " + SPEECH_V + r"\b")
ON_DATE = re.compile(r"^On (?P<date>\d{1,2} [A-Z][a-z]+ \d{4}),? (?P<speaker>.{2,90}?) " + SPEECH_V + r"\b")
LEAD_SPEAKER = re.compile(r"^(?P<speaker>(?:" + TITLES + r"\s)?(?:[A-Z][\w.'’-]*\s){0,4}[A-Z][\w.'’-]*)(?:'s? (?:sworn |written |own )?(?:testimony|account|statement))?\s(?:\w+\s){0,2}" + SPEECH_V + r"\b")


def resolve_speaker(sp, sur, full, here):
    """A person id for a speaker phrase, or None. Unique surname or full name only."""
    sp = re.sub(r"^" + TITLES + r"\s+", "", sp.strip())
    sp = re.sub(r"^(?:the|a|an)\s+", "", sp, flags=re.I)
    sp = sp.strip(" ,")
    if sp in full:
        return full[sp]
    toks = sp.split()
    if not toks:
        return None
    # "Rep. Eric Burlison", "Skinwalker Ranch owner Brandon Fugal": the last two words
    for k in (3, 2):
        if len(toks) >= k and " ".join(toks[-k:]) in full:
            return full[" ".join(toks[-k:])]
    last = toks[-1].rstrip("'s").rstrip("’s")
    ids = sur.get(last) or []
    if len(ids) == 1:
        return ids[0]
    if here in ids:
        return here
    return None


def mechanical(n, c, kind, sur, full):
    """A full row when the mechanical rules settle claimant, artefact date and route;
    otherwise (None, hints)."""
    text = c.get("text") or ""
    src = c.get("source") or ""
    hints = {}
    claimant, via, adate, how = None, None, None, None
    m = ON_SHOW.match(text)
    if m:
        via = m.group("show").strip()
        adate = best_date(m.group("date"))
        claimant = resolve_speaker(m.group("speaker"), sur, full, n["id"])
        how = "on-show pattern"
    else:
        m = ON_DATE.match(text)
        if m:
            adate = best_date(m.group("date"))
            claimant = resolve_speaker(m.group("speaker"), sur, full, n["id"])
            how = "on-date pattern"
        else:
            m = LEAD_SPEAKER.match(text)
            if m and not DOC_SUBJECT.search(m.group("speaker")):
                claimant = resolve_speaker(m.group("speaker"), sur, full, n["id"])
                how = "named speaker opens the claim"
            elif OPEN.search(text) and n.get("cls") == "person":
                # "Testified that ...", "Under oath, ..." on a person's own node: the
                # subject is the node, unless another board person is named before
                # the first speech verb
                head = re.split(r"\b" + SPEECH_V + r"\b", text, maxsplit=1)[0]
                others = [i for s_, ids in sur.items() if re.search(r"\b" + re.escape(s_) + r"\b", head)
                          for i in ids if i != n["id"]]
                if not others:
                    claimant = n["id"]
                    how = "attribution opens a claim on the speaker's own node"
    if kind == "office" and claimant is None:
        host = first_host(src)
        if "aaro.mil" in host or OFFICE_SOURCE.search(URL.sub(" ", src).strip()):
            claimant, how = "aaro", "the office's own publication (aaro.mil)"
    if adate is None:
        adate = best_date(URL.sub(" ", src)) or best_date(src)
    route = route_of(src, text)
    hints = {"claimant": claimant, "artefactDate": adate, "route": route, "via": via, "how": how}
    # a mechanical row only where the rules are reliable: a hearing, an interview,
    # or the office's own publication. The rest go to review with these as hints.
    if claimant and adate and how and (route in ("hearing", "interview") or
                                       (kind == "office" and claimant == "aaro" and route)):
        # eventDate: the first date in the claim after its preamble that is not the
        # artefact date itself; null when the claim names none
        body = text[m.end():] if m else text
        ev = [d for _p, d, _t in dates_in(body, skip_access=False) if d != adate]
        row = {"claimant": claimant, "artefactDate": adate,
               "eventDate": ev[0] if ev else None, "route": route,
               "via": via, "by": "mechanical (%s)" % how}
        return row, hints
    return None, hints


# ------------------------------------------------------------------ commands

def cmd_stats(_a):
    b, nodes, byid = board()
    doc = load_meta()
    rows = doc["claims"]
    sc = in_scope(nodes)
    have = [x for x in sc if x[1]["id"] in rows]
    print("in scope: %d (T2 %d, said %d, office %d)" % (
        len(sc), sum(1 for x in sc if x[2] == "t2"), sum(1 for x in sc if x[2] == "said"),
        sum(1 for x in sc if x[2] == "office")))
    print("rows: %d of scope; stray rows: %d" % (len(have), len(set(rows) - {x[1]["id"] for x in sc})))
    by = {}
    for r in rows.values():
        k = (r.get("by") or "?").split(" (")[0].split(",")[0]
        by[k] = by.get(k, 0) + 1
    print("by pass:", by)
    print("with claimant: %d; verified: %d" % (sum(1 for r in rows.values() if r.get("claimant")),
                                               sum(1 for r in rows.values() if r.get("verified"))))
    cl = {}
    for r in rows.values():
        if r.get("claimant"):
            cl[r["claimant"]] = cl.get(r["claimant"], 0) + 1
    print("claimants: %d; with 20 or more: %s" % (
        len(cl), sorted(((k, v) for k, v in cl.items() if v >= 20), key=lambda x: -x[1])))


def cmd_propose(a):
    b, nodes, byid = board()
    sur, full = name_index(nodes)
    doc = load_meta()
    rows = doc["claims"]
    todo = []
    made = 0
    for n, c, kind in in_scope(nodes):
        cid = c["id"]
        if cid in rows and not str(rows[cid].get("by", "")).startswith("mechanical"):
            continue
        row, hints = mechanical(n, c, kind, sur, full)
        if row:
            rows[cid] = row
            made += 1
        else:
            rows.pop(cid, None)
            todo.append({"id": cid, "tier": c.get("tier"), "mark": kind, "node": n["id"],
                         "nodeLabel": n.get("label"), "nodeCls": n.get("cls"),
                         "text": c.get("text"), "source": c.get("source"),
                         "hints": {k: v for k, v in hints.items() if v}})
    save_meta(doc)
    print("mechanical rows: %d; left for review: %d" % (made, len(todo)))
    if a.packets:
        os.makedirs(a.packets, exist_ok=True)
        for f in os.listdir(a.packets):
            if f.startswith("packet-"):
                os.remove(os.path.join(a.packets, f))
        k = 0
        for i in range(0, len(todo), a.size):
            k += 1
            with open(os.path.join(a.packets, "packet-%02d.json" % k), "w", encoding="utf-8") as fh:
                json.dump(todo[i:i + a.size], fh, ensure_ascii=False, indent=1)
        print("wrote %d packets to %s" % (k, a.packets))


def validate_row(cid, r, byid):
    bad = []
    if r.get("claimant") is not None and r["claimant"] not in byid:
        bad.append("%s: claimant %r is not a node" % (cid, r["claimant"]))
    if r.get("claimant") is None and not str(r.get("speaker") or "").strip():
        bad.append("%s: no claimant and no speaker" % cid)
    for f in ("artefactDate", "eventDate"):
        v = r.get(f)
        if v is not None and not (isinstance(v, str) and DATE_RX.match(v)):
            bad.append("%s: %s %r is not YYYY, YYYY-MM or YYYY-MM-DD" % (cid, f, v))
    if r.get("route") not in ROUTES:
        bad.append("%s: route %r" % (cid, r.get("route")))
    return bad


def cmd_merge(a):
    b, nodes, byid = board()
    scope = {c["id"] for _n, c, _k in in_scope(nodes)}
    doc = load_meta()
    rows = doc["claims"]
    bad, n_in = [], 0
    for p in a.files:
        got = rd(p)
        if isinstance(got, list):
            got = {r.pop("id"): r for r in got}
        for cid, r in got.items():
            if cid not in scope:
                bad.append("%s: not in scope" % cid)
                continue
            keep = {k: r.get(k) for k in ("claimant", "speaker", "artefactDate", "eventDate", "route", "via")}
            if not keep.get("speaker"):
                keep.pop("speaker")
            if a.verify:
                old = rows.get(cid) or {}
                keep["by"] = old.get("by") or a.by
                if any(old.get(k) != keep.get(k) for k in ("claimant", "artefactDate", "eventDate", "route", "via", "speaker")):
                    keep["by"] = keep["by"] + "; corrected by " + a.by
                keep["verified"] = a.by
            else:
                keep["by"] = a.by
            e = validate_row(cid, keep, byid)
            if e:
                bad += e
                continue
            rows[cid] = keep
            n_in += 1
    save_meta(doc)
    print("merged %d rows; %d refused" % (n_in, len(bad)))
    for x in bad[:60]:
        print("  ", x)


def cmd_sample(a):
    b, nodes, byid = board()
    doc = load_meta()
    rows = doc["claims"]
    info = {c["id"]: (n, c, k) for n, c, k in in_scope(nodes)}
    cl = {}
    for cid, r in rows.items():
        if r.get("claimant"):
            cl.setdefault(r["claimant"], []).append(cid)
    heavy = sorted(k for k, v in cl.items() if len(v) >= 20)
    pick = set(cid for k in heavy for cid in cl[k])
    rest = sorted(set(rows) - pick)
    random.seed(20260926)
    pick |= set(random.sample(rest, min(len(rest), a.n)))
    out = []
    for cid in sorted(pick):
        if cid not in info:
            continue
        n, c, k = info[cid]
        out.append({"id": cid, "tier": c.get("tier"), "mark": k, "node": n["id"],
                    "nodeLabel": n.get("label"), "text": c.get("text"), "source": c.get("source"),
                    "row": rows[cid],
                    "claimantLabel": (byid.get(rows[cid].get("claimant")) or {}).get("label")})
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print("sample: %d rows (%d heavy claimants: %s)" % (len(out), len(heavy), heavy))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("stats")
    p = sp.add_parser("propose")
    p.add_argument("--packets")
    p.add_argument("--size", type=int, default=450)
    p = sp.add_parser("merge")
    p.add_argument("files", nargs="+")
    p.add_argument("--by", required=True)
    p.add_argument("--verify", action="store_true")
    p = sp.add_parser("sample")
    p.add_argument("n", type=int)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    {"stats": cmd_stats, "propose": cmd_propose, "merge": cmd_merge,
     "sample": cmd_sample}.get(a.cmd, lambda _a: ap.print_help())(a)


if __name__ == "__main__":
    main()
