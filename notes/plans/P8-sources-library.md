# Phase 8, detailed: sources and the Library

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 8" and the critic's findings
(60% of claims show "no url in the source"; archive URLs wrap mid-string; patent inventors never named).
Branch `redesign/p8-sources`. Opus 5.5, high. Starts after phase 7's data half is merged.

## Tasks

1. **`tools/build_source_registry.py`** proposes `research/_sources.json` from edge `sources` (structured),
   claim source strings (by URL and by identifier regexes: GAO/NSIAD numbers, CHRG hearing records, FOIA
   case numbers, CIA-RDP numbers, public laws, U.S.C. sections, DoD issuance numbers, Federal Register
   citations), and the document and legislation nodes that ARE sources. Fields: `id`, `type` (document,
   hearing record, statute, regulation, report, article, book, broadcast, transcript, web page, archive
   index), `title`, `issuer`, `date`, `identifiers`, `urls`, `archived`, `node` (the board node the source
   is, when there is one), `interestedParty`. **No URL may enter the registry that is not already in
   `research/`** (a check with a poison that plants an invented URL).
2. **`research/_claim_sources.json`**, per claim id: `[{ source, locator }]`. Exact URL or identifier
   matches are automatic. The rest: Sonnet batches propose, an Opus reviewer reviews every proposal that
   merges two different strings into one source. The original source string is always kept on the claim.
   Unresolved claims are marked unresolved, never guessed.
3. **Checks with poisons:** no registry URL absent from `research/`; every claim resolves to a source or
   is marked unresolved; the resolved share is reported and must not fall (a committed floor);
   interested-party sources keep the AARO/DoD cap (restated); P5c's bookkeeping rows stay out.
4. **The app:** claims render their source as a link to `#/s/<id>` (the source page carries the external
   URL); `#/library` with facets (type, issuer, era, interested party) and search; `#/s/<id>` shows the
   source's record, its claims grouped by topic and by node, the edges citing it, and its node. URLs wrap
   at sensible points, never mid-word unreadably. Phone width. C-checks with poisons for each page.
5. **The blind critic loop** until the worst in-scope issue is minor (`notes/critic/p8-round-N.md`).

## Acceptance

Gate green; the resolved share reported and floored; no registry URL outside `research/`; Library and
source pages live; the critic's source findings closed.
