#!/usr/bin/env python3
"""The source registry (redesign phase 8): one record per source the board cites.

    python tools/build_source_registry.py            write research/_sources.json and
                                                     research/_claim_sources.json
    python tools/build_source_registry.py --stats    print the figures, write nothing
    python tools/build_source_registry.py --residue DIR   write the fan-out work lists
                                                     (residue-*.json) into DIR

WHAT A SOURCE IS HERE. A document, a hearing record, a statute, an article, a web
page: the thing a claim or an edge stands on. Until phase 8 the board held sources
only as strings on claims and {name, url} pairs on nodes and edges, so one GAO report
was cited under a dozen spellings and 60% of claims printed "no url in the source".

HOW A SOURCE IS FOUND, AND THE ONLY WAYS TWO CITATIONS BECOME ONE SOURCE.

  1. the same URL (normalised: host lower-cased, `www.` and a trailing slash and a
     #fragment ignored). A Wayback capture of a URL is that URL's source, carried in
     `archived`;
  2. the same identifier, read by the regexes in ID_RULES: GAO report numbers, CHRG
     hearing records, CREC granules, bill versions, public laws, U.S.C. sections,
     Statutes at Large, CFR parts, Federal Register citations, executive orders, DoD
     issuances, CIA-RDP numbers, DTIC accessions, FOIA case numbers, CRS reports, NARA
     record groups, patents and patent applications;
  3. a URL and an identifier join when the URL itself carries the identifier, or when
     a {name, url} pair's name carries exactly one identifier and the URL is on that
     identifier's own publisher (ISSUER_HOSTS);
  4. a document or legislation node whose label carries an identifier IS that source;
  5. the reviewed decisions in research/_source_decisions.json: a claim source
     string read by a Sonnet batch as naming a source already in the registry, a new
     source named only by a string, or a node's own URL that is a copy of the node's
     document. Every decision that merges two different strings carries an Opus
     reviewer's verdict; a rejected one is not applied.

Nothing else merges. A claim this does not resolve is listed in `unresolved` with the
reason, never guessed. The original source string stays on the claim.

NO URL ENTERS THE REGISTRY THAT research/ DOES NOT ALREADY HOLD. Every URL here is
read out of the merged board, which is read out of research/; verify.py re-reads the
raw research files and fails on any registry URL they do not contain.
"""

import collections
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from merge import INTERESTED_PARTY_PAT  # noqa: E402

BOARD = os.path.join(ROOT, "data", "the-program.json")
OUT_SOURCES = os.path.join(ROOT, "research", "_sources.json")
OUT_CLAIMS = os.path.join(ROOT, "research", "_claim_sources.json")
DECISIONS = os.path.join(ROOT, "research", "_source_decisions.json")

TYPES = ("document", "hearing record", "statute", "regulation", "report", "article",
         "book", "broadcast", "transcript", "web page", "archive index")

URL_RE = re.compile(r"https?://[^\s\"'<>|\]]+")
DEMOTION = re.compile(r"\s*[-—]+\s*DEMOTED from Tier 1.*$", re.I | re.S)
WAYBACK = re.compile(r"^https?://web\.archive\.org/web/(\d+)[a-z_]*/(https?://.+)$", re.I)
ARCHIVE_TODAY = re.compile(r"^https?://archive\.(?:ph|today|is|md)/", re.I)


# ------------------------------------------------------------------ URLs

def clean_url(u):
    """A URL as it sits in prose, without the punctuation that ends a sentence."""
    u = u.strip()
    while u and u[-1] in ".,;:'\"":
        u = u[:-1]
    # a closing bracket belongs to the URL only when the URL opened one
    while u.endswith(")") and u.count(")") > u.count("("):
        u = u[:-1]
    while u and u[-1] in ".,;:'\"":
        u = u[:-1]
    return u


def url_key(u):
    """The identity of a URL: the same page however it was typed."""
    m = re.match(r"^(https?)://([^/?#]+)([^#]*)", u, re.I)
    if not m:
        return u.lower()
    host = m.group(2).lower()
    if host.startswith("www."):
        host = host[4:]
    rest = m.group(3)
    if rest.endswith("/"):
        rest = rest[:-1]
    return host + rest


def unwrap(u):
    """(original URL, archived URL or None). A Wayback capture belongs to the page it
    captured; an archive.today capture has no readable original and stands alone."""
    m = WAYBACK.match(u)
    if m:
        return clean_url(m.group(2)), u
    return u, None


def host_of(u):
    m = re.match(r"^https?://([^/?#:]+)", u, re.I)
    h = m.group(1).lower() if m else ""
    return h[4:] if h.startswith("www.") else h


# ------------------------------------------------------------------ identifiers
#
# Each rule: (kind, regex, key(match) -> (id, label), type, issuer). `key` returns
# None to refuse a match. The label is how the page prints the identifier.

def _gao(m):
    office, a, b, suf = m.group(1), m.group(2), m.group(3), (m.group(4) or "")
    if office:
        office = office.rstrip("-/").upper()
        return (f"gao-{office.lower()}-{a}-{b}{suf.lower()}", f"GAO/{office}-{a}-{b}{suf.upper()}")
    return (f"gao-{a}-{b}{suf.lower()}", f"GAO-{a}-{b}{suf.upper()}")


def _dod(m):
    kind = m.group(1)
    k = {"directive": "D", "instruction": "I", "manual": "M"}.get(
        kind.split()[-1].lower(), kind[-1].upper())
    num = m.group(2)
    vol = m.group(3)
    lab = f"DoD{k} {num}" + (f", Volume {vol}" if vol else "")
    return (f"dod{k.lower()}-{num.replace('.', '-')}" + (f"-v{vol}" if vol else ""), lab)


def _pl(m):
    return (f"pl-{m.group(1)}-{int(m.group(2))}", f"Public Law {m.group(1)}-{int(m.group(2))}")


def _patent(m):
    n = re.sub(r"\D", "", m.group(1))
    if len(n) < 7:
        return None
    return (f"us-patent-{int(n)}", f"US Patent {int(n):,}")


ID_RULES = [
    ("hearing", re.compile(r"\bCHRG-(\d{3})([hsj]hrg)(\d+)\b", re.I),
     lambda m: (f"chrg-{m.group(1)}{m.group(2).lower()}{m.group(3)}",
                f"CHRG-{m.group(1)}{m.group(2).lower()}{m.group(3)}"),
     "hearing record", "U.S. Congress"),
    ("crec", re.compile(r"\bCREC-(\d{4}-\d{2}-\d{2})-pt(\d)-Pg([HSE]\d+(?:-\d+)?)", re.I),
     lambda m: (f"crec-{m.group(1)}-pt{m.group(2)}-pg{m.group(3).lower()}",
                f"Congressional Record, {m.group(1)}, page {m.group(3).upper()}"),
     "transcript", "U.S. Congress"),
    ("bill", re.compile(r"\bBILLS-(\d{3})(hr|s|hres|sres|hjres|sjres|hconres|sconres)(\d+)([a-z]{2,4})\b", re.I),
     lambda m: (f"bills-{m.group(1)}{m.group(2).lower()}{m.group(3)}{m.group(4).lower()}",
                f"BILLS-{m.group(1)}{m.group(2).lower()}{m.group(3)}{m.group(4).lower()}"),
     "document", "U.S. Congress"),
    ("plaw", re.compile(r"\bPLAW-(\d{2,3})publ(\d{1,3})\b", re.I), _pl, "statute", "U.S. Congress"),
    ("pl", re.compile(r"(?:\bP\.\s?L\.|\bPub(?:lic|\.)?\s?L(?:aws?|\.)?|\bPL)\s?(\d{2,3})[-–](\d{1,3})\b"),
     _pl, "statute", "U.S. Congress"),
    ("usc", re.compile(r"\b(\d{1,2})\s?U\.\s?S\.\s?C\.?\s?(?:§+\s?|Sec(?:tion|\.)?\s?)?(\d+[a-z]?)\b"),
     lambda m: (f"usc-{m.group(1)}-{m.group(2).lower()}", f"{m.group(1)} U.S.C. {m.group(2)}"),
     "statute", "U.S. Congress"),
    ("stat", re.compile(r"\b(\d{2,3}) Stat\.\s?(\d+)"),
     lambda m: (f"stat-{m.group(1)}-{m.group(2)}", f"{m.group(1)} Stat. {m.group(2)}"),
     "statute", "U.S. Congress"),
    ("cfr", re.compile(r"\b(\d{1,2}) C\.?F\.?R\.?\s?(?:[Pp]art |pt\. |§\s?)?(\d{1,4})\b"),
     lambda m: (f"cfr-{m.group(1)}-{m.group(2)}", f"{m.group(1)} CFR part {m.group(2)}"),
     "regulation", "Code of Federal Regulations"),
    ("fr", re.compile(r"\b(\d{2,3}) (?:FR|Fed\.\s?Reg\.) (\d{2,6})\b"),
     lambda m: (f"fr-{m.group(1)}-{m.group(2)}", f"{m.group(1)} FR {m.group(2)}"),
     "regulation", "Federal Register"),
    ("frdoc", re.compile(r"\bFederal Register Doc\.? (\d{2}-\d{4,6})\b"),
     lambda m: (f"frdoc-{m.group(1)}", f"Federal Register Doc. {m.group(1)}"),
     "regulation", "Federal Register"),
    ("eo", re.compile(r"(?:\bE\.\s?O\.|\bEO|\bExecutive Order)\s?(1\d{4})\b"),
     lambda m: (f"eo-{m.group(1)}", f"Executive Order {m.group(1)}"),
     "regulation", "The President"),
    ("dod", re.compile(r"\b(DoD[DIM]|DoD (?:Directive|Instruction|Manual))\s?(\d{4}\.\d{2})"
                       r"(?:[-, ]*(?:V|Vol\.?|Volume)\s?(\d))?"),
     _dod, "regulation", "Department of Defense"),
    ("gao", re.compile(r"\bGAO[/-]((?:[A-Z]{2,6}[-/])?)(\d{2})-(\d{2,6})([A-Z]{0,2})\b"),
     _gao, "report", "Government Accountability Office"),
    ("gaoacc", re.compile(r"\bGAO accession (\d{5,7})\b"),
     lambda m: (f"gao-accession-{m.group(1)}", f"GAO accession {m.group(1)}"),
     "document", "Government Accountability Office"),
    ("rdp", re.compile(r"\bCIA-RDP([0-9A-Z]{2,12}(?:-[0-9A-Z]{4,12})?R?[0-9A-Z]{0,16}-\d)\b", re.I),
     lambda m: (f"cia-rdp{m.group(1).lower()}", f"CIA-RDP{m.group(1).upper()}"),
     "document", "Central Intelligence Agency"),
    ("dtic", re.compile(r"\b(A[DB][A-C]?\d{6,7})\b"),
     lambda m: (f"dtic-{m.group(1).lower()}", f"DTIC {m.group(1).upper()}"),
     "document", "Defense Technical Information Center"),
    ("foia-dod", re.compile(r"\b(\d{2}-F-\d{3,5})\b"),
     lambda m: (f"foia-{m.group(1).lower()}", f"FOIA case {m.group(1).upper()}"),
     "document", "Department of Defense"),
    ("foia-dia", re.compile(r"\bFOIA-(\d{4,5})-(\d{4})\b"),
     lambda m: (f"foia-dia-{m.group(1)}-{m.group(2)}", f"DIA FOIA-{m.group(1)}-{m.group(2)}"),
     "document", "Defense Intelligence Agency"),
    ("crs", re.compile(r"\b(?:CRS\b[^;]{0,40}?|crs_external_products/[A-Z]+/PDF/|everycrsreport\.com/reports/)"
                       r"\b((?:RL|RS|R|IF|IN)\d{4,5})\b"),
     lambda m: (f"crs-{m.group(1).lower()}", f"CRS {m.group(1).upper()}"),
     "report", "Congressional Research Service"),
    ("rg", re.compile(r"\b(?:NARA,? )?(?:RG|Record Group) (\d{1,3})\b"),
     lambda m: (f"nara-rg-{m.group(1)}", f"NARA Record Group {m.group(1)}"),
     "archive index", "National Archives"),
    ("patent", re.compile(r"\bUS ?(?:Patent (?:No\.? )?)?(\d{1,2},\d{3},\d{3}|\d{7,8})(?:\s?[AB]\d)?\b"),
     _patent, "document", "U.S. Patent and Trademark Office"),
    ("patent-url", re.compile(r"patents\.google\.com/patent/US(\d{7,8})", re.I),
     _patent, "document", "U.S. Patent and Trademark Office"),
    ("uspto-app", re.compile(r"\bapplications? (\d{2}/\d{3},?\d{3})\b"),
     lambda m: (f"uspto-app-{re.sub(r'\D', '', m.group(1))}", f"US application {m.group(1)}"),
     "document", "U.S. Patent and Trademark Office"),
]

# the identifier's own publisher: a {name, url} whose name carries exactly one
# identifier joins that identifier when its URL is on one of these hosts
ISSUER_HOSTS = {
    "hearing": ("govinfo.gov", "congress.gov", "docs.house.gov"),
    "crec": ("govinfo.gov", "congress.gov"),
    "bill": ("govinfo.gov", "congress.gov"),
    "plaw": ("govinfo.gov", "congress.gov"),
    "pl": ("govinfo.gov", "congress.gov"),
    "usc": ("uscode.house.gov", "law.cornell.edu", "govinfo.gov"),
    "stat": ("govinfo.gov",),
    "cfr": ("ecfr.gov", "govinfo.gov", "law.cornell.edu"),
    "fr": ("federalregister.gov", "govinfo.gov"),
    "frdoc": ("federalregister.gov", "govinfo.gov"),
    "eo": ("federalregister.gov", "govinfo.gov", "archives.gov"),
    "dod": ("esd.whs.mil",),
    "gao": ("gao.gov",),
    "gaoacc": ("gao.gov",),
    "rdp": ("cia.gov",),
    "crs": ("congress.gov", "crsreports.congress.gov", "everycrsreport.com"),
    "patent": ("patents.google.com", "uspto.gov", "patentimages.storage.googleapis.com"),
}

# a patent or application number needs its context: "US 3,322,374" in prose is
# a patent; an unqualified seven-digit number is not
NEEDS_CONTEXT = {"dtic": re.compile(r"DTIC|archive\.org/details/DTIC", re.I),
                 "uspto-app": re.compile(r"USPTO|file wrapper|Patent", re.I)}

# statutes at large are a locator when the same segment names the public law
LOCATOR_ONLY_WITH = {"stat": ("pl", "plaw")}


def find_ids(text):
    """[(kind, id, label, type, issuer, start, end)] in text order, one per id."""
    out, seen = [], set()
    for kind, rx, key, typ, issuer in ID_RULES:
        need = NEEDS_CONTEXT.get(kind)
        if need and not need.search(text):
            continue
        for m in rx.finditer(text):
            k = key(m)
            if not k:
                continue
            if k[0] in seen:
                continue
            seen.add(k[0])
            out.append((kind, k[0], k[1], typ, issuer, m.start(), m.end()))
    out.sort(key=lambda r: r[5])
    return out


def issuer_join(u, r):
    """May a citation's one identifier `r` join the URL it is cited with? Only when
    the URL is on the identifier's own publisher, and only when the URL does not
    carry an identifier of its own that differs (a govinfo bill URL cited under a
    U.S.C. section is the bill, not the section)."""
    orig = unwrap(u)[0]
    h = host_of(orig)
    if not any(h == x or h.endswith("." + x) for x in ISSUER_HOSTS.get(r[0], ())):
        return False
    own = {x[1] for x in url_ids(orig)}
    return not own or r[1] in own


def url_ids(u):
    """Identifiers a URL itself carries (a govinfo package, a GAO asset, a CIA
    reading-room document, a DTIC scan, a Google Patents page)."""
    out = []
    m = re.search(r"/(?:pkg|details|link)/(CHRG-\d{3}[hsj]hrg\d+|CREC-[^/]+?-Pg[HSE]\d+(?:-\d+)?"
                  r"|BILLS-\d{3}[a-z]+\d+[a-z]+|PLAW-\d+publ\d+)", u, re.I)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids(m.group(1))]
    m = re.search(r"STATUTE-(\d{2,3})-Pg(\d+)", u)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids(f"{m.group(1)} Stat. {m.group(2)}")]
    m = re.search(r"gao\.gov/(?:assets|products)/(?:gao-)?([a-z]{2,6}-)?(\d{2})-(\d{2,6})([a-z]?)(?:\.pdf|$|[/?#])", u, re.I)
    if m:
        office = (m.group(1) or "").upper()
        text = f"GAO/{office}{m.group(2)}-{m.group(3)}{m.group(4).upper()}" if office else \
            f"GAO-{m.group(2)}-{m.group(3)}{m.group(4).upper()}"
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids(text)]
    m = re.search(r"cia-rdp[0-9a-z-]+-\d", u, re.I)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids(m.group(0).upper())]
    m = re.search(r"archive\.org/details/DTIC_(A[DB][A-C]?\d{6,7})", u, re.I)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids("DTIC " + m.group(1).upper())]
    m = re.search(r"patents\.google\.com/patent/US(\d{7,8})", u, re.I)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids("US " + m.group(1))]
    m = re.search(r"(?:crs_external_products/[A-Z]+/PDF/|everycrsreport\.com/reports/)((?:RL|RS|R|IF|IN)\d{4,5})", u)
    if m:
        out += [(r[0], r[1], r[2], r[3], r[4]) for r in find_ids("CRS " + m.group(1))]
    dedup, seen = [], set()
    for r in out:
        if r[1] not in seen:
            seen.add(r[1])
            dedup.append(r)
    return dedup


# ------------------------------------------------------------------ types, issuers

HOST_ISSUER = {
    "govinfo.gov": "U.S. Government Publishing Office", "congress.gov": "U.S. Congress",
    "uscode.house.gov": "U.S. Congress", "oversight.house.gov": "House Committee on Oversight",
    "docs.house.gov": "U.S. House of Representatives", "senate.gov": "U.S. Senate",
    "intelligence.senate.gov": "Senate Select Committee on Intelligence",
    "armed-services.senate.gov": "Senate Armed Services Committee",
    "armedservices.house.gov": "House Armed Services Committee",
    "aaro.mil": "AARO", "media.defense.gov": "Department of Defense",
    "defense.gov": "Department of Defense", "war.gov": "Department of Defense",
    "comptroller.war.gov": "Department of Defense", "esd.whs.mil": "Department of Defense",
    "dodig.mil": "DoD Inspector General", "dia.mil": "Defense Intelligence Agency",
    "dni.gov": "ODNI", "odni.gov": "ODNI", "archive.dni.gov": "ODNI",
    "cia.gov": "Central Intelligence Agency", "vault.fbi.gov": "FBI",
    "nro.gov": "National Reconnaissance Office", "af.mil": "U.S. Air Force",
    "navy.mil": "U.S. Navy", "army.mil": "U.S. Army", "navair.navy.mil": "U.S. Navy",
    "gao.gov": "Government Accountability Office", "archives.gov": "National Archives",
    "catalog.archives.gov": "National Archives", "history.state.gov": "Department of State",
    "ntrs.nasa.gov": "NASA", "science.nasa.gov": "NASA", "nasa.gov": "NASA",
    "smd-cms.nasa.gov": "NASA", "energy.gov": "Department of Energy", "osti.gov": "Department of Energy",
    "lanl.gov": "Los Alamos National Laboratory", "sec.gov": "SEC", "usaspending.gov": "USAspending.gov",
    "api.usaspending.gov": "USAspending.gov", "federalregister.gov": "Federal Register",
    "ecfr.gov": "Code of Federal Regulations", "law.cornell.edu": "Legal Information Institute",
    "courtlistener.com": "CourtListener", "storage.courtlistener.com": "CourtListener",
    "nsf.gov": "National Science Foundation", "ncses.nsf.gov": "National Science Foundation",
    "files.fasab.gov": "FASAB", "clinton.presidentiallibraries.us": "Clinton Presidential Library",
    "reaganlibrary.gov": "Reagan Presidential Library",
    "theblackvault.com": "The Black Vault", "documents.theblackvault.com": "The Black Vault",
    "documents2.theblackvault.com": "The Black Vault", "irp.fas.org": "Federation of American Scientists",
    "fas.org": "Federation of American Scientists", "sgp.fas.org": "Federation of American Scientists",
    "nsarchive.gwu.edu": "National Security Archive", "nsarchive2.gwu.edu": "National Security Archive",
    "archive.org": "Internet Archive", "ia800403.us.archive.org": "Internet Archive",
    "en.wikipedia.org": "Wikipedia", "en.wikisource.org": "Wikisource", "youtube.com": "YouTube",
    "nicap.org": "NICAP", "defensescoop.com": "DefenseScoop", "thedebrief.org": "The Debrief",
    "twz.com": "The War Zone", "thehill.com": "The Hill", "newsnationnow.com": "NewsNation",
    "foxnews.com": "Fox News", "nytimes.com": "The New York Times", "newyorker.com": "The New Yorker",
    "theintercept.com": "The Intercept", "vice.com": "Vice", "politico.com": "Politico",
    "washingtonpost.com": "The Washington Post", "wsj.com": "The Wall Street Journal",
    "npr.org": "NPR", "bbc.com": "BBC", "bbc.co.uk": "BBC", "cbsnews.com": "CBS News",
    "abcnews.com": "ABC News", "newsweek.com": "Newsweek", "8newsnow.com": "KLAS 8 News Now",
    "liberationtimes.com": "Liberation Times", "deseret.com": "Deseret News",
    "scientificamerican.com": "Scientific American", "nature.com": "Nature",
    "popularmechanics.com": "Popular Mechanics", "space.com": "Space.com",
    "centerforinquiry.org": "Center for Inquiry", "cdn.centerforinquiry.org": "Center for Inquiry",
    "skeptic.com": "Skeptic", "skepticalinquirer.org": "Skeptical Inquirer", "metabunk.org": "Metabunk",
    "thesolfoundation.org": "The Sol Foundation", "mitre.org": "MITRE", "rand.org": "RAND",
    "doi.org": "DOI", "arxiv.org": "arXiv", "legis.senado.leg.br": "Senado Federal (Brasil)",
    "camara.leg.br": "Camara dos Deputados (Brasil)", "gov.br": "Governo do Brasil",
    "imagem.sian.an.gov.br": "Arquivo Nacional (Brasil)", "science.gc.ca": "Government of Canada",
    "ised-isde.canada.ca": "Government of Canada", "cdn.nationalarchives.gov.uk": "The National Archives (UK)",
    "discovery.nationalarchives.gov.uk": "The National Archives (UK)",
    "sefaa.dgac.gob.cl": "DGAC Chile", "dgac.gob.cl": "DGAC Chile", "cnes-geipan.fr": "CNES GEIPAN",
    "geipan.fr": "CNES GEIPAN", "cnes.fr": "CNES", "patents.google.com": "Google Patents",
    "patentimages.storage.googleapis.com": "Google Patents", "freepatentsonline.com": "FreePatentsOnline",
    "image-ppubs.uspto.gov": "U.S. Patent and Trademark Office", "wikileaks.org": "WikiLeaks",
    "everycrsreport.com": "EveryCRSReport", "newstalkkzrg.com": "NewsTalk KZRG",
    "burlison.house.gov": "Rep. Eric Burlison", "democrats-appropriations.house.gov": "House Appropriations Committee",
    "appropriations.senate.gov": "Senate Appropriations Committee",
    "appropriations.house.gov": "House Appropriations Committee",
    "democrats-armedservices.house.gov": "House Armed Services Committee",
}

NEWS_HOSTS = {"defensescoop.com", "thedebrief.org", "twz.com", "thehill.com", "newsnationnow.com",
              "foxnews.com", "nytimes.com", "newyorker.com", "theintercept.com", "vice.com",
              "politico.com", "washingtonpost.com", "wsj.com", "npr.org", "bbc.com", "bbc.co.uk",
              "cbsnews.com", "abcnews.com", "newsweek.com", "8newsnow.com", "liberationtimes.com",
              "deseret.com", "scientificamerican.com", "popularmechanics.com", "space.com",
              "huffpost.com", "nypost.com", "baltimoresun.com", "santafenewmexican.com",
              "civilbeat.org", "cybernews.com", "meritalk.com", "aerotime.aero", "earthsky.org",
              "newstalkkzrg.com", "correiobraziliense.com.br", "cnnbrasil.com.br", "migalhas.com.br",
              "prnewswire.com", "skeptic.com", "skepticalinquirer.org", "theufochronicles.com",
              "silvarecord.com", "douglasjohnson.ghost.io", "uap-blog.com"}
BOOK_HOSTS = {"openlibrary.org", "gutenberg.org", "edition-open-sources.org"}
INDEX_PAT = re.compile(r"(Congressional-Press-Products|/UAP-Records|reading-?room/?$|FOIA-Electronic-Reading-Room/?$"
                       r"|archives\.gov/uap|/research/topics/|/collections/?$|/guide-fed-records/)", re.I)


def url_type(u):
    h = host_of(u)
    if h in ("youtube.com", "youtu.be", "m.youtube.com") or "podcast" in u.lower():
        return "broadcast"
    if INDEX_PAT.search(u):
        return "archive index"
    if h in NEWS_HOSTS or h.endswith("blogspot.com") or h.endswith("substack.com") \
            or h.endswith("medium.com") or h.endswith("wordpress.com"):
        return "article"
    if h in BOOK_HOSTS:
        return "book"
    if re.search(r"transcript", u, re.I):
        return "transcript"
    if re.search(r"\.pdf($|[?#])", u, re.I) or "archive.org/details/" in u or "archive.org/stream/" in u or "archive.org/download/" in u:
        return "document"
    return "web page"


def url_issuer(u):
    h = host_of(u)
    if h in HOST_ISSUER:
        return HOST_ISSUER[h]
    parts = h.split(".")
    for i in range(1, len(parts) - 1):
        cand = ".".join(parts[i:])
        if cand in HOST_ISSUER:
            return HOST_ISSUER[cand]
    return h


def url_date(u):
    """A date the URL's own path states (/2024/Mar/08/, /2026/05/17/), or None."""
    mon = {m: i for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                                        "sep", "oct", "nov", "dec"), 1)}
    m = re.search(r"/((?:19|20)\d{2})/([A-Za-z]{3}|\d{2})/(\d{2})/", u)
    if m:
        mm = mon.get(m.group(2).lower()) if not m.group(2).isdigit() else int(m.group(2))
        if mm and 1 <= mm <= 12:
            return f"{m.group(1)}-{mm:02d}-{m.group(3)}"
    m = re.search(r"/((?:19|20)\d{2})/(\d{2})/", u)
    if m and "/uploads/" not in u and 1 <= int(m.group(2)) <= 12:
        return f"{m.group(1)}-{m.group(2)}"
    return None


NODE_TYPE = [
    (re.compile(r"statute|authoriz|legislation|act\b|law", re.I), "statute"),
    (re.compile(r"executive-order|dod-issuance|directive|instruction|regulation", re.I), "regulation"),
    (re.compile(r"report", re.I), "report"),
    (re.compile(r"hearing", re.I), "hearing record"),
    (re.compile(r"video", re.I), "broadcast"),
]


def node_type(n):
    sub = n.get("sub") or ""
    if n.get("cls") == "legislation":
        for rx, t in NODE_TYPE[:2]:
            if rx.search(sub):
                return t
        return "statute"
    for rx, t in NODE_TYPE:
        if rx.search(sub):
            return t
    return "document"


# ------------------------------------------------------------------ union-find

class DSU:
    def __init__(self):
        self.p = {}

    def add(self, k):
        self.p.setdefault(k, k)

    def find(self, k):
        self.add(k)
        while self.p[k] != k:
            self.p[k] = self.p[self.p[k]]
            k = self.p[k]
        return k

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            # deterministic: the smaller key is the root
            if rb < ra:
                ra, rb = rb, ra
            self.p[rb] = ra


def short_hash(s, n=8):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:n]


def norm_string(s):
    s = DEMOTION.sub("", s or "")
    return re.sub(r"\s+", " ", s).strip()


def segments(s):
    """A source string split into its citations: on semicolons and on ' || '."""
    return [p.strip() for p in re.split(r";|\|\|", s) if p.strip()]


def locator_of(seg, start, end, label):
    """The rest of a citation segment after its identifier: 'p.4', 'Sec. 7343'."""
    rest = seg[end:].strip(" ,.:-–()")
    rest = URL_RE.sub("", rest).strip(" ,.;:-–")
    rest = re.sub(r"\s+", " ", rest)
    if not rest:
        return None
    return rest[:160]


# ------------------------------------------------------------------ the build

PROCESS = re.compile(r"this session|opened|downloaded|converted to text|read against|"
                     r"retrieved (?:from|via|on)|accessed|checked against|transcribed|"
                     r"^board |^inference|^derived by|^reasoning over|^cross-reference", re.I)


def claim_label(raw):
    """A claim source string as a name for the record it cites: URLs gone, and the
    notes about how it was read ("full OCR text read this session, opened ...")."""
    keep = []
    for seg in segments(URL_RE.sub(" ", raw)):
        seg = re.sub(r"(?:,\s*)+", ", ", seg).strip(" ,-–—")
        if seg and not PROCESS.search(seg):
            keep.append(seg)
    return re.sub(r"\s+", " ", "; ".join(keep)).strip()


def best_title(names):
    """A title from the names a source is cited under: a name an edge or a node
    gave it first (most often used), then a claim's name that carries a quoted
    title (the longest), then the most frequent claim name."""
    pn = [(c, n) for (k, n), c in names.items() if k == "P"]
    if pn:
        return sorted(pn, key=lambda x: (-x[0], len(x[1]), x[1]))[0][1]
    cn = [(c, n) for (k, n), c in names.items() if k == "C"]
    quoted = [n for c, n in cn if re.search(r"['‘“][^'’”]{8,}['’”]", n)]
    if quoted:
        return sorted(quoted, key=lambda n: (-len(n), n))[0]
    if cn:
        return sorted(cn, key=lambda x: (-x[0], len(x[1]), x[1]))[0][1]
    return None


def load_decisions():
    if not os.path.exists(DECISIONS):
        return {"strings": {}, "nodeUrls": {}}
    with open(DECISIONS, encoding="utf-8") as f:
        d = json.load(f)
    return {"strings": d.get("strings") or {}, "nodeUrls": d.get("nodeUrls") or {}}


def applied(dec):
    """A decision counts when it merges nothing, or when its reviewer accepted it."""
    if not dec:
        return False
    if dec.get("unresolved"):
        return True
    rv = dec.get("review")
    if dec.get("to") or dec.get("merge"):
        return bool(rv) and rv.get("verdict") == "accept"
    return True


def build(board=None, decisions=None):
    if board is None:
        with open(BOARD, encoding="utf-8") as f:
            board = json.load(f)
    if decisions is None:
        decisions = load_decisions()
    nodes = board["people"] + board["entities"]
    byid = {n["id"]: n for n in nodes}

    dsu = DSU()
    meta = collections.defaultdict(lambda: {"names": collections.Counter(), "urls": set(),
                                            "archived": set(), "idinfo": None})
    # --- every URL, with the names it is cited under
    def see_url(raw_u, name=None, standalone=True):
        u = clean_url(raw_u)
        if not re.match(r"^https?://[^/]+\.[^/]+", u):
            return None
        orig, arch = unwrap(u)
        k = "url:" + url_key(orig)
        dsu.add(k)
        m = meta[k]
        if arch:
            m["archived"].add(arch)
        else:
            m["urls"].add(orig)
        if name:
            m["names"][name] += 1
        for r in url_ids(orig):
            ik = "id:" + r[1]
            dsu.add(ik)
            meta[ik]["idinfo"] = meta[ik]["idinfo"] or r
            dsu.union(k, ik)
        return k

    def see_pair(name, url):
        """A structured {name, url}: the URL, and the identifier its name carries."""
        name = norm_string(name or "")
        urls = [url] if url else []
        urls += URL_RE.findall(name)
        label = claim_label(name)
        label = re.sub(r"^(?:Archived|Wayback snapshot of):?\s*", "", label)
        label = re.sub(r"\s*\((?:Wayback|archived)[^)]*\)\s*$", "", label, flags=re.I)
        keys = []
        for u in urls:
            k = see_url(u, ("P", label) if label and len(label) >= 4 else None)
            if k:
                keys.append((k, clean_url(u)))
        ids = find_ids(URL_RE.sub(" ", name))
        for r in ids:
            dsu.add("id:" + r[1])
            meta["id:" + r[1]]["idinfo"] = meta["id:" + r[1]]["idinfo"] or r[:5]
        if len(ids) == 1 and keys:
            r = ids[0]
            hosts = ISSUER_HOSTS.get(r[0], ())
            for k, u in keys:
                if issuer_join(u, r):
                    dsu.union(k, "id:" + r[1])
        return keys, ids

    node_keys, edge_keys = collections.defaultdict(list), collections.defaultdict(list)
    for n in nodes:
        for s in n.get("sources") or []:
            keys, ids = see_pair(s.get("name"), s.get("url"))
            node_keys[n["id"]] += [k for k, _ in keys] + ["id:" + r[1] for r in ids]
    for e in board["edges"]:
        for s in e.get("sources") or []:
            keys, ids = see_pair(s.get("name"), s.get("url"))
            edge_keys[e["id"]] += [k for k, _ in keys] + ["id:" + r[1] for r in ids]

    # --- document and legislation nodes are sources; an identifier in the label joins
    doc_nodes = [n for n in board["entities"] if n.get("cls") in ("document", "legislation")]
    for n in doc_nodes:
        k = "node:" + n["id"]
        dsu.add(k)
        ids = find_ids(n.get("label") or "")
        if len(ids) == 1:
            r = ids[0]
            dsu.add("id:" + r[1])
            meta["id:" + r[1]]["idinfo"] = meta["id:" + r[1]]["idinfo"] or r[:5]
            dsu.union(k, "id:" + r[1])
        # reviewed: the node's own URLs that are copies of the document itself
        dec = decisions["nodeUrls"].get(n["id"])
        if dec and applied(dec):
            for u in dec.get("urls") or []:
                uk = see_url(u)
                if uk:
                    dsu.union(k, uk)

    # --- claim strings
    claim_rows = []
    for n in nodes:
        for c in n.get("claims") or []:
            claim_rows.append((n["id"], c))

    per_claim = {}
    string_keys = {}
    for nid, c in claim_rows:
        raw = norm_string(c.get("source") or "")
        refs = []
        for seg in segments(raw):
            ids = find_ids(URL_RE.sub(" ", seg))
            kinds = {r[0] for r in ids}
            for r in ids:
                if r[0] in LOCATOR_ONLY_WITH and kinds & set(LOCATOR_ONLY_WITH[r[0]]):
                    continue
                ik = "id:" + r[1]
                dsu.add(ik)
                meta[ik]["idinfo"] = meta[ik]["idinfo"] or r[:5]
                refs.append((ik, locator_of(URL_RE.sub(" ", seg), r[5], r[6], r[2]), "identifier"))
            for u in URL_RE.findall(seg):
                label = claim_label(raw)
                k = see_url(u, ("C", label) if len(label) >= 8 else None)
                if k:
                    if len(ids) == 1 and issuer_join(clean_url(u), ids[0]):
                        dsu.union(k, "id:" + ids[0][1])
                    refs.append((k, None, "url"))
        dec = decisions["strings"].get(raw)
        if not refs and dec and applied(dec) and not dec.get("unresolved"):
            if dec.get("to"):
                refs.append((dec["to"], dec.get("locator"), "review"))
            elif dec.get("new"):
                sk = "str:" + short_hash(raw, 12)
                dsu.add(sk)
                string_keys[sk] = (raw, dec["new"])
                refs.append((sk, dec.get("locator"), "review"))
        per_claim[c["id"]] = (raw, refs, dec)

    # reviewed merges of one NEW string source into another (two strings, one source)
    for raw, dec in decisions["strings"].items():
        if dec.get("new") and dec.get("merge") and applied(dec):
            a = "str:" + short_hash(raw, 12)
            if a in string_keys:
                dsu.union(a, dec["merge"] if dec["merge"].startswith(("str:", "id:", "url:", "node:"))
                          else "str:" + short_hash(dec["merge"], 12))

    # --- components -> registry records
    comps = collections.defaultdict(list)
    for k in list(dsu.p):
        comps[dsu.find(k)].append(k)

    def pick_id(keys):
        ids = sorted(k for k in keys if k.startswith("id:"))
        nodes_ = sorted(k for k in keys if k.startswith("node:"))
        urls = sorted(k for k in keys if k.startswith("url:"))
        strs = sorted(k for k in keys if k.startswith("str:"))
        if ids:
            # the identifier kind that names a document most exactly wins
            order = [r[0] for r in ID_RULES]
            ids.sort(key=lambda k: (order.index(meta[k]["idinfo"][0]) if meta[k]["idinfo"] else 99, k))
            return ids[0][3:]
        if nodes_:
            return "n-" + nodes_[0][5:]
        if urls:
            h = host_of("https://" + urls[0][4:])
            slug = re.sub(r"[^a-z0-9]+", "-", h.replace("www.", "")).strip("-")[:24]
            return f"u-{slug}-{short_hash(urls[0], 8)}"
        return "t-" + strs[0][4:]

    registry, key_to_id = {}, {}
    for root, keys in comps.items():
        sid = pick_id(keys)
        for k in keys:
            key_to_id[k] = sid
        urls, archived, idents, names = set(), set(), [], collections.Counter()
        typ = issuer = date = title = node = None
        for k in keys:
            m = meta.get(k)
            if m:
                urls |= m["urls"]
                archived |= m["archived"]
                names.update(m["names"])
        idk = sorted((k for k in keys if k.startswith("id:")),
                     key=lambda k: ([r[0] for r in ID_RULES].index(meta[k]["idinfo"][0])
                                    if meta[k]["idinfo"] else 99, k))
        for k in idk:
            info = meta[k]["idinfo"]
            if info:
                idents.append(info[2])
        nk = sorted(k for k in keys if k.startswith("node:"))
        if nk:
            node = nk[0][5:]
            n = byid[node]
            title = n.get("label")
            typ = node_type(n)
            date = n.get("dateStart") or n.get("date")
            if isinstance(date, str) and not re.match(r"^\d{4}", date):
                date = None
        if idk and meta[idk[0]]["idinfo"]:
            info = meta[idk[0]]["idinfo"]
            typ = typ or info[3]
            issuer = info[4]
            if not title:
                title = info[2]
                # a quoted title printed right after the identifier, in any name
                for (_, nm), _ in names.most_common():
                    q = re.search(re.escape(info[2].split()[-1]) + r"[^'‘]{0,40}['‘]([^'’]{8,160})['’]", nm)
                    if q:
                        title = f"{info[2]}: {q.group(1).strip()}"
                        break
            if not date and info[0] == "crec":
                date = re.search(r"\d{4}-\d{2}-\d{2}", info[1]).group(0)
        sk = [k for k in keys if k.startswith("str:")]
        if sk and not title:
            raw, new = string_keys[sorted(sk)[0]]
            title = new.get("title") or raw
            typ = new.get("type")
            issuer = new.get("issuer")
            date = new.get("date")
        if urls or archived:
            u0 = sorted(urls or archived)[0]
            u0 = unwrap(u0)[0]
            if not typ:
                typ = url_type(u0)
            if not issuer:
                issuer = url_issuer(u0)
            if not date:
                date = url_date(u0)
            if not title:
                title = best_title(names) or u0
        if typ not in TYPES:
            typ = "document"
        allurls = sorted(urls) + sorted(archived)
        ip = any(INTERESTED_PARTY_PAT.search(u) for u in allurls) or \
            bool(re.match(r"^(?:AARO|All-domain Anomaly Resolution Office)\b", title or ""))
        registry[sid] = {
            "id": sid, "type": typ, "title": title, "issuer": issuer, "date": date,
            "identifiers": idents, "urls": sorted(urls), "archived": sorted(archived),
            "node": node, "interestedParty": ip,
        }

    # --- claims -> sources
    claims_out, unresolved = {}, {}
    for cid in sorted(per_claim):
        raw, refs, dec = per_claim[cid]
        rows, seen = [], set()
        for k, loc, by in refs:
            sid = key_to_id.get(k)
            if sid is None and k.startswith("id:") and k[3:] in registry:
                sid = k[3:]
            if sid is None:
                continue
            if (sid, loc) in seen:
                continue
            seen.add((sid, loc))
            rows.append({"source": sid, "locator": loc, "by": by})
        if rows:
            claims_out[cid] = rows
        else:
            if dec and dec.get("unresolved"):
                why = dec["unresolved"]
            elif not raw or raw.lower().startswith("no attributed source"):
                why = "no source recorded"
            elif re.match(r"^(?:board |the board's )?inference\b|^derived by this board|^reasoning over", raw, re.I):
                why = "the board's own inference; it names no source that resolves"
            else:
                why = "no URL or identifier, and no reviewed reading of the string"
            unresolved[cid] = {"why": why}
    # edges and nodes: the registry sources their {name, url} lists cite
    def ids_of(keys):
        return sorted({key_to_id[k] for k in keys if k in key_to_id})
    cites = {"edges": {k: ids_of(v) for k, v in sorted(edge_keys.items()) if ids_of(v)},
             "nodes": {k: ids_of(v) for k, v in sorted(node_keys.items()) if ids_of(v)}}
    return registry, claims_out, unresolved, per_claim, cites


def stats(registry, claims_out, unresolved):
    total = len(claims_out) + len(unresolved)
    by_type = collections.Counter(r["type"] for r in registry.values())
    return {"sources": len(registry), "byType": dict(sorted(by_type.items())),
            "claims": total, "resolved": len(claims_out),
            "resolvedShare": round(len(claims_out) / total, 4) if total else 0,
            "unresolvedWhy": dict(collections.Counter(u["why"] for u in unresolved.values())),
            "withNode": sum(1 for r in registry.values() if r["node"]),
            "interestedParty": sum(1 for r in registry.values() if r["interestedParty"])}


def write(registry, claims_out, unresolved, cites):
    st = stats(registry, claims_out, unresolved)
    with open(OUT_SOURCES, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"_about": "The source registry, written by tools/build_source_registry.py. "
                             "Never hand-edit: decisions go in research/_source_decisions.json.",
                   "stats": st,
                   "sources": [registry[k] for k in sorted(registry)]},
                  f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    with open(OUT_CLAIMS, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"_about": "Per claim id, the registry sources it cites, written by "
                             "tools/build_source_registry.py. A claim no rule or reviewed decision "
                             "resolves is in `unresolved` with the reason; the claim keeps its "
                             "original source string either way. `edges` and `nodes`: the "
                             "registry sources each edge's and node's {name, url} list cites.",
                   "claims": claims_out, "unresolved": unresolved,
                   "edges": cites["edges"], "nodes": cites["nodes"]},
                  f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    return st


def residue(per_claim, unresolved, registry, out_dir):
    """The fan-out's work lists: every distinct unresolved string, with its claims."""
    os.makedirs(out_dir, exist_ok=True)
    strings = collections.defaultdict(list)
    for cid, u in unresolved.items():
        raw = per_claim[cid][0]
        if u["why"].startswith("no URL"):
            strings[raw].append(cid)
    rows = [{"string": s, "claims": len(v)} for s, v in sorted(strings.items())]
    with open(os.path.join(out_dir, "residue-strings.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    cand = [{"key": ("node:" + r["node"]) if r["node"] else
             ("id:" + r["id"] if not r["id"].startswith(("u-", "t-", "n-")) else
              "url:" + url_key(unwrap((r["urls"] or r["archived"])[0])[0])),
             "title": r["title"], "type": r["type"], "issuer": r["issuer"], "date": r["date"],
             "identifiers": r["identifiers"]}
            for r in sorted(registry.values(), key=lambda r: r["id"])]
    with open(os.path.join(out_dir, "registry-candidates.json"), "w", encoding="utf-8") as f:
        json.dump(cand, f, ensure_ascii=False, indent=1)
    return len(rows)


def main(argv):
    registry, claims_out, unresolved, per_claim, cites = build()
    st = stats(registry, claims_out, unresolved)
    if "--stats" in argv:
        print(json.dumps(st, indent=1))
        return 0
    if "--residue" in argv:
        out_dir = argv[argv.index("--residue") + 1]
        n = residue(per_claim, unresolved, registry, out_dir)
        print(f"{n} distinct unresolved strings written to {out_dir}")
        return 0
    write(registry, claims_out, unresolved, cites)
    print(f"sources {st['sources']}  claims resolved {st['resolved']} of {st['claims']} "
          f"({st['resolvedShare']:.1%})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
