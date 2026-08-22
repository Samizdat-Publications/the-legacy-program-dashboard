# Link health sweep, 22 August 2026

Every distinct source URL on the board was probed once: **1,198 URLs**, from node
`sources[]`, from URLs embedded in `claim.source`, and from edge `sources[]`.
Raw results in `notes/link-sweep-2026-08-22.tsv` (status<TAB>url).

## Read this before quoting any number below

**A failure here means "this session could not fetch it", not "the document is
gone."** Three things make the raw counts misleading, and all three were checked
rather than assumed:

1. **`web.archive.org` is blocked outright for this session.** All 164 Wayback
   URLs returned no connection. Re-probing serially with three-second gaps changed
   nothing, so it is not rate-limiting from the sweep's own concurrency, and
   WebFetch answers `Claude Code is unable to fetch from web.archive.org`. These
   164 carry **zero information** about whether the archives are intact.
2. **403 to a plain HTTP client is not 403 to everything.** `gao.gov` and
   `war.gov` both returned 403 in this sweep, and both served real content to
   WebFetch in this same session — the GAO NSIAD-95-187 report page and the
   Department of War biography of Michael Powers. Government and news hosts
   commonly refuse a bare client and serve a browser.
3. **YouTube's 429s are rate-limiting**, not removals.

So the honest summary is a floor, not a census.

## What was actually established

| | |
|---|---|
| Distinct URLs probed | 1,198 |
| Confirmed reachable (HTTP 200) | **763** |
| Blocked to this client (403) | 225 |
| No connection (000) | 171, of which **164 are web.archive.org** |
| Rate-limited / other (429, 202, 302, 404, 405, 406, 503) | 39 |
| Non-archive URLs confirmed reachable | 763 of 1,034 = **74%** |

Nothing here supports a claim that any specific citation has rotted, with one
exception.

## The one genuine retrieval failure

`https://irp.fas.org/dia/aatip-list.pdf` — the DIA's January 2018 list of the 38
Defense Intelligence Reference Documents, and the most-cited single URL behind the
DIRD nodes — **returns HTTP 202 with an empty body and serves no document.**

This one is diagnosable rather than ambiguous:

- The Wayback availability API reports its closest capture, of 4 August 2026, with
  `"status": "202"`. FAS was already serving the interstitial when the archive
  crawled it, so there is no good capture to fall back to.
- The DIA FOIA reading room copy returns 403.
- It is not a client problem: `https://fas.org/publication/aatip-list/`, the FAS
  article that announces the same release, returns 200 and reads normally.

**That FAS article is the better citation** and should be added alongside. It
establishes provenance in its own text — the list "was publicly released yesterday
under the Freedom of Information Act", it was "previously provided to Congress in
January 2018", it covers "a list of 38 research titles", and DIA "spent $22 million
on the activity". It does not reproduce the titles, so it does not replace the PDF
for anything title-specific.

The working retrieval path for the DIRDs themselves is The Black Vault: all 32
series-member PDFs returned 200 and were downloaded and read on 22 August.

## Where the unreachable URLs cluster

Non-archive hosts with the most URLs this client could not fetch. Treat as "needs
a browser or a mirror", not "dead":

| count | host |
|---|---|
| 50 | www.dia.mil |
| 20 | www.aaro.mil |
| 18 | www.youtube.com (429, rate limit) |
| 17 | www.congress.gov |
| 13 | thehill.com |
| 11 | www.war.gov (proven reachable via WebFetch) |
| 10 | media.defense.gov |
| 10 | www.mitre.org |
| 8 | www.esd.whs.mil |
| 8 | www.newsnationnow.com |
| 7 | www.dodig.mil |

`www.dia.mil` at 50 is the one worth attention: the AAWSAP/AATIP FOIA reading-room
entries are the custody spine of the DIRD material, and this session cannot open
any of them.

## Consequence for the sourcing backlog

This is why the remaining thin-sourcing work stalled. `congress.gov`,
`bioguide.congress.gov`, `dia.mil` and `washingtontimes.com` all refuse this
session, and the rule on this board is that a source is not added unless it has
been opened. Rather than cite URLs sight-unseen, the blocked hosts are recorded
here.

## Next

1. Re-run this sweep from a session that can reach `web.archive.org`. Until then
   the archive mirroring strategy in the wave-3 queue is unverifiable — 164
   mirrors exist and not one of them has been confirmed to work.
2. Add `https://fas.org/publication/aatip-list/` to `dird-series` alongside the
   202-ing PDF.
3. The wave-3 queue's item 2, the dead `dpo.tothestarsacademy.com` CRADA links, is
   already closed: `ttsa-army-crada` now carries the TTSA Form 1-A exhibits from
   SEC EDGAR, which is the primary record that queue item asked for.
