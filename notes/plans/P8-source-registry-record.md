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
- **One source is one document.** The union-find refuses any merge that would put two board nodes, or two
  identifiers of one family (two DTIC accessions, two volumes of DoDM 5205.07, a public law and a node
  for one of its sections), in one source. 32 unions were refused on the final build; the commonest is a
  node for a series or a section whose reviewed URL is the whole law or one volume.
- **Interested party** means the office's own: a source whose title names AARO, or whose every copy on
  file sits on AARO/DoD hosts. A released historical document the office also hosts (Blue Book Special
  Report 14 on war.gov as well as cia.gov) is that document, not the office's statement.

## The interested-party cap now reaches claims cited by name

`merge.py remediate_interested_party_claims()` applies the AARO/DoD cap through the registry. A Tier 1
claim whose every source is the office's own stays Tier 1 when it is about what the office said: the
attribution words, a claim that opens by quoting it, or the office or one of its documents as the subject
of an account verb ("AARO assessed", "the report reaffirmed"). Otherwise it is Tier 2 with the standard
demotion note, unless `tierAdjudications` records why it stands. 29 adjudications are recorded (the
establishment memorandum's administrative acts, the office's own caseload figures, the office's own
contracting and releases, and claims that report an official's words). **12 claims moved from Tier 1 to
Tier 2**; each is an outside fact the office's publication was the only authority for (who authored the
DIRDs, BAASS as prime contractor, the $22 million appropriation, what KONA BLUE was, the 2021 IC CAP,
Skunk Works aircraft). GOLDEN claim tiers moved 3,780 / 1,700 / 580 to 3,768 / 1,712 / 580.

## The fan-out

| | |
|---|---|
| Strings no URL or identifier resolved | 1,915 distinct, on 2,569 claims, read by 8 Sonnet batches (two re-run after a stall) |
| Sonnet readings | existing source 1,526; new source 202 (39 of them "same as" another string); unresolved 187 |
| Opus review, every merge of two strings | 4 reviewers. Existing: 991 accepted, 535 rejected. Same-as: 24 accepted, 15 rejected (each kept as its own source). Node URLs as copies of the node's document: 339 of 398 accepted |
| Commonest rejections | the string names two sources and the candidate is one; an outlet and a date with no date on the candidate; an article about a document offered as the document; a later edition (ICD 906 2024, JANAP 146(E)) |
| Mechanical rules on new sources | a paraphrased title is replaced by the citation as written (63); an issuer or date not in the string is dropped (27, 1) |
| Result | 4,911 of 6,060 claims resolve (81.0%, floor 0.8103), from 3,189 (52.6%) by URL and identifier alone |

A rejected reading leaves the claim unresolved, with the reviewer's reason as its `why`. Nothing was
guessed. The work files (batches, proposals, verdicts) were scratch; every decision that counts is in
`research/_source_decisions.json` with the batch and reviewer that made it.

## Deferred, on purpose

- **Strings that cite two sources** ("X; Y") resolve only by URL or identifier today; a reviewed reading
  maps a string to one source, so the reviewers rejected about 150 two-source strings. A list-valued
  decision would resolve most of them. Phase R.
- **Dossier claims** (the map model's) are not in the registry; they keep their source strings.
- **Edges** link their sources on the source page ("Links citing it") but the node page's connection rows
  still print their `{name, url}` sources as before, now with breakable addresses.
- **300 claims cite the board's own inference** ("Inference from ...") and name nothing that resolves.
  They are marked unresolved with that reason.
