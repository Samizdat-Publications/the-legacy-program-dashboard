# Phase 8: the source registry, how it was built and what it decided

Written 26 September 2026 by the phase 8 session (Opus 5.5). The spec is `P8-sources-library.md`.
Figures here are as of the phase's last build; `python tools/build_source_registry.py --stats`
re-derives them.

## What was built

| | |
|---|---|
| `tools/build_source_registry.py` | Reads the merged board and `research/_source_decisions.json`; writes `research/_sources.json` (the registry) and `research/_claim_sources.json` (per claim: its sources and locators, or why it has none; per edge and per node: the sources its `{name, url}` list cites). A build step, after the FOIA links and before `build_app_data`. |
| `tools/source_pages.py` | The registry as the app ships it: `app/public/data/sources.json` (the Library) and `sources/<id>.json` (one page per source). Claims in `claims.json`, node files and topic cites carry `sources` (id, title, locator) and `unresolved`. |
| App | `#/library` (facets type, issuer, era, interested party; search; three orders; 100 rows at a time), `#/s/<id>` (record, where to read it, claims by node or by topic, topics, links, nodes listing it). Claims on node pages, topics and the evidence table link their sources' pages; unresolved claims print the citation as written. LIBRARY sits under More. |
| verify.py | Six checks, each with poisons: no registry URL absent from `research/` (the corpus excludes the registry's own files); every claim resolved or marked unresolved, and the app ships exactly the map; the resolved share at or above `tools/SOURCE-RESOLVED-FLOOR.json`; interested-party sources keep the AARO/DoD cap; no bookkeeping row reaches the registry; a string-only source invents nothing. |
| app checks | C42 (the Library re-derived from `sources.json`: rows, order, every facet count), C43 (a source page against its record, its claims re-derived from `claims.json`), C44 (every claim row links exactly its sources), C45 (web addresses break only at their break points, at 1920 and 375). C9, C20, C26, C36 and C40 extended. |

## The only ways two citations become one source

1. The same URL (host lower-cased, `www.`, trailing slash and fragment ignored). A Wayback capture
   belongs to the page it captured and is listed under `archived`.
2. The same identifier: GAO numbers and accessions, CHRG hearing records, CREC granules, bill versions,
   public laws, U.S.C. sections, Statutes at Large, CFR parts, Federal Register citations, executive
   orders, DoD issuances (a stated year makes a separate edition), CIA-RDP numbers, DTIC accessions,
   FOIA case numbers, CRS reports, NARA record groups, patents and applications.
3. A URL joins an identifier when the URL carries it, or when a `{name, url}` pair's name carries exactly
   one identifier and the URL is on that identifier's own publisher, and the URL carries no different
   identifier of its own (a govinfo bill cited under a U.S.C. section stays the bill).
4. A document or legislation node whose label carries one identifier is that source.
5. Reviewed decisions (below).

## Decisions taken on the way

- **Four Tier 1 claims on interested-party sources only** (FOIA 24-F-0266, released AARO and DoD
  memoranda) stay Tier 1, adjudicated in `tierAdjudications`: each reports what the released document
  says. Before the registry, `merge.py` could not see them, because their strings name no aaro.mil URL.
- **Locators** are read only after a comma, colon or bracket that follows the identifier ("p.4",
  "Sec. 7343"); "GAO/NSIAD-95-187 and the Bolender memorandum" is prose, not a locator.
- **Titles.** A node's label; else the quoted title the citations give an identifier (never a quoted
  section, chapter or item); else, for a released document known by its number (CIA-RDP, DTIC, FOIA
  case), the name the citations give it most often; else the identifier. A URL source takes the name an
  edge or node gives it, then a claim's quoted title, then the commonest claim name, with notes about
  how it was read ("full OCR text read this session, opened ...") removed.
- **Dates** are the node's, or the date a URL path states (news paths, never `/uploads/`), or a CREC
  granule's. The `date` on a `{name, url}` pair is usually an access date and is not used.
