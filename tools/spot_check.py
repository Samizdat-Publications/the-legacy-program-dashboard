#!/usr/bin/env python3
"""
spot_check.py — open the sources and check the board is quoting them correctly.

WHY THIS EXISTS
---------------
TESTING-CHECKLIST.md §12 asks a human to "pick five claims at random and verify
against the source", and says of a fabricated source: "stop and report immediately.
That is the one failure mode that matters." It had never been run systematically.

Five is not a sample, it is an anecdote. But most of §12 does not need a human:

  * whether the URL resolves is mechanical;
  * whether the source SAYS what the claim says is mechanical too, for the subset
    of claims that quote the document verbatim.

That subset is large. 630 claims on this board carry both a quoted phrase of four
or more words and a URL, and a quoted phrase is exactly where a fabricated source
shows itself: paraphrase can drift honestly, but a sentence in quotation marks is
either in the document or it is not.

So this checks the strongest available property: EVERY CLAIM THAT QUOTES A PHRASE
AND CITES A FETCHABLE URL MUST HAVE THAT PHRASE IN THE DOCUMENT IT CITES.

WHAT IT DOES NOT DO
-------------------
It cannot check paraphrase, and it does not try. A NOT FOUND is a finding to read,
not a verdict, and the report prints how much of the quote DID match so it can be
triaged without opening the document. UNREACHABLE is not a finding at all -- it
means this environment cannot open the host, which is a fact about the network
vantage and not about the board.

One class it cannot adjudicate at all: SCANNED FOIA RELEASES. The 38 DIRDs on
theblackvault are photocopies run through OCR, with redaction stamps sitting inside
sentences. One reads "under the Defense Intelligence Agency, l(b)(3):10 USC 424
It\dvanced Aerospace Weapon Syst..." where the board correctly quotes "under the
Defense Intelligence Agency Advanced Aerospace Weapon System Applications (AAWSA)
Program"; another prints the document's own ICOD stamp as "reDO:" and its control
number as "DIA-08-1004-00 1". Every DIRD quote in the first run reported NOT FOUND
and every one of them was the board quoting accurately. Those are grouped out of
the findings, not counted as them.

NORMALISATION, and why it is aggressive
---------------------------------------
Comparing raw strings produces false alarms, not findings. Scanned documents from
the DTIC archive double-space between words; PDFs wrap lines mid-sentence and
hyphenate across them; every source disagrees about curly versus straight quotes.
A pass that reported those as missing quotes would be worse than no pass, because
it would train the reader to ignore it. So both sides are folded down to lowercase
alphanumerics separated by single spaces before comparison.

Usage:
    python3 tools/spot_check.py                 # every checkable claim
    python3 tools/spot_check.py --sample 60     # a seeded random subset
    python3 tools/spot_check.py --host govinfo.gov
    python3 tools/spot_check.py --json out.json
"""

import argparse, json, os, random, re, subprocess, sys, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "data", "the-program.json")
CACHE = os.path.join(ROOT, "tools", ".spot-cache")
# A 403 or a 429 is usually this crawl's own rate limit rather than a policy,
# so a remembered failure must be retryable or the run poisons its own cache.
RETRY_ERRORS = False
# The eCFR versioner needs a concrete date; the most recent year end is stable
# and is what "current" resolved to when these citations were written.
ECFR_DATE = "2025-12-31"

URL_PAT = re.compile(r"https?://[^\s,;)\]<>\"]+")
# A quoted run long enough to be a real quotation rather than a scare-quoted term.
#
# The lookarounds on the straight-single-quote form are not optional. Without them
# the apostrophe in a possessive opens a quotation: "EarthTech's published citation
# list ... gives the same paper as ..." was read as a quote beginning at
# EarthTech'S and running to the next apostrophe, and the check duly reported that
# the document did not contain it. A pass that manufactures findings is worse than
# no pass, because it teaches the reader to skip the output.
QUOTE_PAT = re.compile(
    r"(?<![A-Za-z0-9])'([^']{25,400})'(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9])‘([^’]{25,400})’"
    r"|\"([^\"]{25,400})\"")
MIN_WORDS = 4


# Editorial interpolations the publisher injects INTO the middle of a sentence.
# govinfo prints statutes with page breaks and drafting notes inline, so the text
# of PL 117-263 sec. 6802 actually reads "...enactment of the Intelligence
# Authorization [[Page 136 STAT. 3590]] Act for Fiscal Year 2023...". The board
# quotes the sentence correctly and the first version of this check called it
# missing, four times over, on the strongest statutory material on the board.
INTERPOLATION = re.compile(r"\[\[Page[^\]]*\]\]|<<[^>]*>>")


def fold(s):
    """Lowercase alphanumerics, single-spaced. See NORMALISATION above."""
    s = s.replace("’", "'").replace("‘", "'")
    # The U.S. Code prints the section symbol; the board writes "Sec." for it. Both
    # are the same citation and folding punctuation away leaves "501a" against
    # "sec 501a", so three correct statutory citations read as misquotes.
    s = re.sub(r"§+", " sec ", s)
    s = INTERPOLATION.sub(" ", s)
    # Hyphenation across a line break, including the not-sign an OCR pass emits for
    # a soft hyphen: the Condon Report scan prints "con\u00ac currently".
    s = re.sub(r"[-\u00ac\u2010\u2011]\s*\n\s*", "", s)
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s)
    return " " + s.lower().strip() + " "


def contains(doc, quote):
    """Is `quote` in `doc`, allowing for an elided quote?

    A quote written with an ellipsis is deliberately not contiguous -- the board
    writes 'any requirement ... that certain information be included in a report'
    -- so requiring one substring match reports every such quote as missing. Each
    fragment must appear, and in order.
    """
    # " / " is how the board joins two lines of a title page or masthead into one
    # quotation. Like an ellipsis it marks a deliberate join, not a contiguous run.
    # Square brackets mark an editorial insertion, so their contents are by
    # definition NOT in the source. AARO's HRR prints "which was also known AATIP",
    # dropping the "as"; the board quotes it "was also known [as] AATIP", which is
    # the correct convention and more careful than the document. Matching the
    # brackets literally would report that carefulness as a misquote.
    quote = re.sub(r"\[[^\]]{0,40}\]", " ", quote)
    parts = [fold(p).strip() for p in re.split(r"\.\.\.|…|\s+/\s+", quote)]
    parts = [p for p in parts if len(p) >= 8]
    if not parts:
        return False
    at = 0
    for p in parts:
        at = doc.find(p, at)
        if at < 0:
            return _contains_squashed(doc, parts)
        at += len(p)
    return True


def _squash(s):
    return re.sub(r"\s+", "", s)


def _contains_squashed(doc, parts):
    """Second pass with every space removed.

    PDF text extraction does not reliably preserve word boundaries. AARO's FY2025
    report comes out of pypdf as "Fis cal Year 2025", "ALL-D OMAIN ANOMALY
    RESOLUTION OFFIC E" -- spaces inserted inside words -- and renders the
    line-broken compound "UAP-related" such that de-hyphenating it yields
    "uaprelated" while the correct reading is "uap related". Both are the extractor
    mangling the document, not the board misquoting it, and both are invisible to a
    space-sensitive comparison.

    Removing every space from both sides makes the test blind to that whole class.
    It is only reached after the faithful comparison has failed, and the quotes here
    are 25 characters or longer, so a spurious match across word boundaries is not a
    practical risk.
    """
    at = 0
    sdoc = _squash(doc)
    for p in parts:
        sp = _squash(p)
        at = sdoc.find(sp, at)
        if at < 0:
            return False
        at += len(sp)
    return True


def longest_prefix(doc, quote):
    """How much of the quote IS in the document, for the report.

    A bare "not found" cannot be triaged: the reader has to open the document to
    learn whether the board misquoted or the tool tripped over formatting. The
    character at which the match stops usually says which immediately.
    """
    fq = fold(quote).strip()
    lo, hi = 0, len(fq)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if fq[:mid] in doc:
            lo = mid
        else:
            hi = mid - 1
    return lo, len(fq), fq[lo:lo + 60]


def quotes_in(text):
    out = []
    for m in QUOTE_PAT.finditer(text or ""):
        for g in m.groups():
            if g and len(g.split()) >= MIN_WORDS:
                out.append(g.strip())
    return out


# archive.org/details/{id} is a catalogue page, not the document. Fetching it
# retrieves 36KB of navigation chrome in which no quotation appears, and the check
# then reports the board as misquoting a document it never opened -- including,
# on the first run, the USAF and Condon Report citations added the same night.
DETAILS = re.compile(r"^https?://(?:www\.)?archive\.org/details/([^/?#]+)")

# ecfr.gov serves its regulation text from JavaScript; a plain fetch of
# /current/title-32/.../part-117/section-117.3 returns 2KB of page furniture in
# which no regulation appears. Nine claims -- the SAP and ACCM definitions the
# board's whole custody argument rests on -- read as unverifiable because of it.
# The versioner API returns the same part as XML. A date is required and "current"
# is not accepted, so this asks for the most recent year-end.
ECFR = re.compile(r"^https?://(?:www\.)?ecfr\.gov/current/title-(\d+)/.*?/part-(\d+)")


def resolve(url):
    m = DETAILS.match(url)
    if m:
        return f"https://archive.org/download/{m.group(1)}/{m.group(1)}_djvu.txt"
    m = ECFR.match(url)
    if m:
        return (f"https://www.ecfr.gov/api/versioner/v1/full/{ECFR_DATE}/"
                f"title-{m.group(1)}.xml?part={m.group(2)}")
    return url


def fetch(url):
    """Return (kind, text). kind is 'ok' or a short reason it could not be read."""
    url = resolve(url)
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(key + ".txt"):
        return "ok", open(key + ".txt", encoding="utf-8", errors="replace").read()
    if os.path.exists(key + ".err") and not RETRY_ERRORS:
        return open(key + ".err", encoding="utf-8").read().strip(), ""

    def remember_error(reason):
        with open(key + ".err", "w", encoding="utf-8") as f:
            f.write(reason)
        return reason, ""

    raw = key + ".bin"
    r = subprocess.run(
        ["curl", "-sSL", "--max-time", "90", "-o", raw,
         "-w", "%{http_code} %{content_type}", url],
        capture_output=True, text=True)
    if r.returncode != 0:
        return remember_error(f"curl failed ({r.returncode})")
    code, _, ctype = (r.stdout.strip() + " ").partition(" ")
    if code != "200":
        return remember_error(f"HTTP {code}")

    data = open(raw, "rb").read()
    if data[:5] == b"%PDF-":
        try:
            from pypdf import PdfReader
            import io
            text = "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
        except Exception as e:
            return remember_error(f"pdf unreadable ({type(e).__name__})")
    else:
        text = data.decode("utf-8", errors="replace")
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        import html as _html
        text = _html.unescape(text)
    os.remove(raw)
    # A 200 that yields almost no text is a failed fetch wearing a success's clothes.
    # One house.gov PDF answered 168 bytes on the first pass and 531KB minutes later;
    # caching the first as a success meant six claims stayed "not found" against a
    # document that had never actually been read, and no retry flag could reach them
    # because nothing had been recorded as an error.
    if len(text.strip()) < 500:
        return remember_error(f"empty body ({len(text.strip())} chars of text)")
    with open(key + ".txt", "w", encoding="utf-8") as f:
        f.write(text)
    return "ok", text


def collect(board):
    """Every (node, claim, quote, url) the check can act on."""
    items = []
    for n in board["people"] + board["entities"]:
        for c in n.get("claims") or []:
            qs = quotes_in(c.get("text"))
            us = URL_PAT.findall(c.get("source") or "")
            if not qs or not us:
                continue
            items.append({"id": n["id"], "tier": c.get("tier"),
                          "quotes": qs, "urls": [u.rstrip(".,;") for u in us],
                          "text": (c.get("text") or "")[:160]})
    return items


def all_source_urls(board):
    """Every URL the board cites, from node sources, claim sources and edge sources.

    The quote check only ever visits URLs attached to a claim that quotes something.
    That is most of the interesting ones and none of the rest, and link rot does not
    respect the distinction: the Arquivo Nacional citations died on a `copy_of_noticias`
    staging path that the board carried in eight places, and 46 DIA reading-room ids
    stopped resolving without a single 404 to show for it.
    """
    seen = {}
    def add(u, where):
        u = u.rstrip(".,;")
        seen.setdefault(u, set()).add(where)
    for n in board["people"] + board["entities"]:
        for s in n.get("sources") or []:
            if s.get("url"):
                add(s["url"], n["id"])
        for c in n.get("claims") or []:
            for u in URL_PAT.findall(c.get("source") or ""):
                add(u, n["id"])
    for e in board.get("edges") or []:
        for s in e.get("sources") or []:
            if s.get("url"):
                add(s["url"], f"{e['a']}->{e['b']}")
    return seen


def link_sweep(board, host=None):
    """Report which cited URLs this environment cannot open, and why.

    A 403 is this network vantage, not a defect. A 404 is a dead citation and is the
    only class here that is unambiguously the board's problem.
    """
    urls = all_source_urls(board)
    if host:
        urls = {u: w for u, w in urls.items() if host in u}
    print(f"=== link sweep — {len(urls)} distinct cited URLs ===\n")
    from collections import Counter, defaultdict
    tally, dead = Counter(), defaultdict(list)
    for i, (u, where) in enumerate(sorted(urls.items()), 1):
        kind, _ = fetch(u)
        tally[kind if kind == "ok" else kind.split(" (")[0]] += 1
        if kind.startswith("HTTP 4") or kind.startswith("HTTP 5"):
            dead[kind].append((u, sorted(where)[:3]))
        if i % 100 == 0:
            print(f"  ... {i}/{len(urls)}", file=sys.stderr)
    for k, c in tally.most_common():
        print(f"  {c:5d}  {k}")
    if dead:
        print("\n  DEAD CITATIONS — a 4xx/5xx is the board's problem, unlike a 403 block:")
        for k in sorted(dead):
            for u, where in sorted(dead[k]):
                print(f"    {k}  {u[:104]}")
                print(f"           cited by {', '.join(where)}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0, help="check a seeded random subset")
    ap.add_argument("--seed", type=int, default=20260825)
    ap.add_argument("--host", help="only claims citing this host")
    ap.add_argument("--json", help="write the full result set here")
    ap.add_argument("--links", action="store_true",
                    help="sweep every cited URL for reachability instead of checking quotes")
    ap.add_argument("--retry-errors", action="store_true",
                    help="ignore remembered fetch failures (403s are often rate limits)")
    a = ap.parse_args()
    global RETRY_ERRORS
    RETRY_ERRORS = a.retry_errors

    board = json.load(open(BOARD, encoding="utf-8"))
    if a.links:
        return link_sweep(board, a.host)
    items = collect(board)
    if a.host:
        items = [i for i in items if any(a.host in u for u in i["urls"])]
    if a.sample and a.sample < len(items):
        random.Random(a.seed).shuffle(items)
        items = items[:a.sample]

    print(f"=== source spot-check — {len(items)} claims quote a document and cite a URL ===\n")
    results, tally = [], {"ok": 0, "not_found": 0, "unreachable": 0}
    for i, it in enumerate(items, 1):
        verdict, detail = None, ""
        for u in it["urls"]:
            kind, text = fetch(u)
            if kind != "ok":
                if verdict is None:
                    verdict, detail = "unreachable", f"{u} — {kind}"
                continue
            doc = fold(text)
            if any(contains(doc, q) for q in it["quotes"]):
                verdict, detail = "ok", u
                break
            got, want, rest = longest_prefix(doc, it["quotes"][0])
            verdict, detail = "not_found", u
            it["diverges"] = (f"matched {got}/{want} chars, document does not continue "
                              f"...{rest!r}" if got else "no part of the quote is present")
        results.append(dict(it, verdict=verdict, detail=detail))
        tally[verdict] = tally.get(verdict, 0) + 1
        if verdict != "ok":
            mark = "MISSING " if verdict == "not_found" else "no access"
            print(f"  {mark} {it['id']} (T{it['tier']})")
            print(f"      {detail}")
            if verdict == "not_found":
                print(f"      quoted: {it['quotes'][0][:120]!r}")
                print(f"      {it.get('diverges','')}")
        if i % 50 == 0:
            print(f"  ... {i}/{len(items)}", file=sys.stderr)

    print(f"\n  quote found in the cited document   {tally['ok']}")
    print(f"  quote NOT found                     {tally['not_found']}")
    print(f"  host unreachable from here          {tally['unreachable']}")
    if tally["not_found"]:
        from collections import Counter
        by_host = Counter(re.sub(r"^https?://(www\.)?", "", r["detail"]).split("/")[0]
                          for r in results if r["verdict"] == "not_found")
        print("\n  NOT FOUND by host — read this before treating any of it as a finding:")
        for h, c in by_host.most_common():
            note = ""
            if "theblackvault" in h or "dia.mil" in h:
                note = "  <- scanned FOIA PDFs, OCR-degraded, not adjudicable"
            elif "burlison.house.gov" in h:
                note = "  <- image-only PDF; no text layer to search"
            elif "ia800403" in h:
                note = "  <- scanned PDF"
            print(f"    {c:4d}  {h}{note}")
    checked = tally["ok"] + tally["not_found"]
    if checked:
        print(f"\n  of {checked} claims actually checkable from this environment, "
              f"{100.0 * tally['ok'] / checked:.1f}% quote their source correctly.")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1, ensure_ascii=False)
        print(f"  full results -> {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
