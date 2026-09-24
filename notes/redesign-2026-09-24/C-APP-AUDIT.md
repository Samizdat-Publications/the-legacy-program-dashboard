# Appendix C: the shipped app, mapped for the redesign (24 September 2026)

Produced by a read-only Opus 5.5 agent for `notes/REDESIGN-2026-09-24.md`. Repo at master `838c134`,
data generated 2026-09-19, fingerprint `8785b01c31ba`. Tags: [M] measured (code, data, or live in
Chromium with the viewport emulated), [I] inferred. Production serves the same data and bundle as master.

## Routes

| Route | Purpose | Data (raw / gzip) | Verdict |
|---|---|---|---|
| `#/` Home | search, 6 entry cards, 14 start-here flags, counts | index 515/60 KB + map.json 117/17 | keep the shell; 3 of 6 cards open the unfiltered map |
| `#/n/<id>` Node | record, claims, denials, timeline slice, FOIA, connections | + nodes/<id> (median 8 KB, max 121) | skeleton reusable; connections need rebuilding |
| `#/map` (+ `?cell`, `n/<id>/map`, `t/<id>/map`) | L0 grid, 7 bands x 5 eras | map.json | at its limit; replace, or let it scroll or zoom |
| `#/hood` (`/<id>`) | ring + outer columns, 1 to 3 hops | + edges.json 500/110 | good idea; hops 2 and 3 are only a roster |
| `#/t/<id>` Thread | 8 authored chains, small map, year slice | threads, map | solid, keep |
| `#/timeline` `?era` `?scope` | 4 strands x 5 eras | timeline.json 504/144 | reuse the packing; add filters and event detail |
| `#/patents/<n>` | 5 filings, sheets, prosecution | 28 KB + images | solid, keep |
| `#/evidence` `?filters` | all 5,897 claims, one value per facet | claims.json 3.9 MB / 833 KB | useful; needs node and text filters; fix "denied" |
| `#/report/n`, `/t` | printable briefs, numbered citations | node or step files | solid; the thread report has no inbound link |
| analyst dock | 12 tools that run in the browser, via the Worker (claude-opus-5) | case index 137.6k chars | the best asset: the query layer the UI lacks |

## Map mechanics

1. L0 membership: institution, program, event, legislation or document nodes with at least 6 distinct
   neighbours; top 135 by degree, plus the 14 flags by right (`build_l0.py:59, 91-97, 165-192`). People,
   locations and domains can never qualify.
2. Columns are start-date eras. A node's band (row) is its rarest role tag; bands are ordered by mean
   custody score C (`build_l0_layout.mjs:70-75, 511-552`).
3. Label mode applies only if every chip fits its column AND rows x pitch (20 down to 18) + gap (12 down to
   6) x 6 fits within viewport height minus 142 (`map/layout.ts:134-189`); otherwise cell mode (counts, "+N",
   zero lines).
4. The map is `position: fixed`, no scroll, no zoom, one 11px size, no truncation (`map.css:9-25`), so its
   capacity is exactly one screen.
5. [M] At 1920 wide, label mode holds at viewport height 1024 and drops to cell mode at 1023. 1920x950: 99
   of 135 chips, 9 of 14 flags, 0 lines. 1366x768: 56 of 135 chips, 6 of 14 flags.
6. [I] A maximised browser on a 1080p monitor gives about 900 to 970px of viewport, so most readers get
   cell mode. Label mode mostly exists in the 1920x1080 test harness.
7. Lines at rest: 118 of 267 direct pairs, chosen by tier and type (`model.ts:109-122`). Hubs get the most
   (aaro 13). Hover only re-lights lines already drawn (`render.ts:245-255`).
8. C5 asserts the mode matches an independent re-derivation at 1920x1080 and 1366x768, lowest chip above
   the legend. C11 asserts all 14 numbered flags are drawn on the map, which forces label mode at 1080
   (`run.mjs:1178-1192, 1333-1355`).

## How the node page organises connections today

- One flat list: on-map neighbours first, then below-floor, each group alphabetical by id
  (`build_app_data.py:494`).
- Each row: class mark, label, then the edge type, or the word "member" if the neighbour is off the map
  (`node.ts:244`), then the tier.
- The edge's own sentence is only a hover tooltip (`node.ts:248`). Edge sources are never shown on the page.
- There is no grouping by type, time, direction or role, and no filter.
- [M] 3,497 of 5,370 rows (65%) say "member". Hub lists run 40 to 80 rows (grusch 80, aaro 64, aawsap 61).
- 5,352 of 5,370 rows carry an edge label, and every row has a note, both hover-only. 234 rows repeat a
  neighbour; 16 nodes have 30+ rows; 118 nodes have 5+ edge types. [M-live] AARO: 64 rows, 45 of them
  "member", page height 2,477px.

## Checks that bind layout

Layout: C2 (one label size, no truncation), C3 (no unlabelled chip), C4 (no overlaps on map, ring,
timeline, small map), C5, C6 (cell counts), C10 (start-here ring), C11, C12 (equal chip size, width = text
+ 30), C15 (strand lanes x eras), C18 (closed dock covers nothing on map or hood), and C9's closed route
list (`run.mjs:1271-1285`).

Content checks worth keeping as they are: C1, C7, C8, C13, C14, C16, C19, C20, C21. Many checks bind class
names and exact wording (C8's header regex, C15's "N events", C18's status strings, and C19, which parses
em dashes in tool output).

| Check | Asserts | Kind | Line |
|---|---|---|---|
| C1 | node ids real; every screen has node links | content | 1113 |
| C2 | one label size; no ellipsis; label not narrower than its text; label inside its chip | layout | 1129 |
| C3 | no unlabelled chip; label equals the authored short; no unlabelled ring entry | layout | 1148 |
| C4 | no overlaps: map at 1920 and 1366, ring, timeline chips, small map | layout | 1162 |
| C5 | mode matches the re-derived rule; chips clear the legend | layout | 1178 |
| C6 | cell counts; +N arithmetic at 1366 | layout | 1194 |
| C7 | thread steps joined by a real edge or shared member | content | 1224 |
| C8 | every claim sourced; header tier counts match the rows (regex) | content | 1241 |
| C9 | routes resolve; every href fits the closed scheme | content + layout | 1261 |
| C10 | `#/hood` shows exactly the 14 flags; 3 hops stays in bounds | layout + content | 1304 |
| C11 | Home register order; 14 numbered chips on the map | layout + content | 1333 |
| C12 | equal heights; width = text + 30 or 46; equal marks | layout | 1357 |
| C13 | denial rows match the record | content | 1381 |
| C14 | only allowed fetches; no page errors | content | 1390 |
| C15 | timeline items in their lane and era; every event drawn | layout + content | 1414 |
| C16 | no placeholder strings | content | 1446 |
| C17 | Back button semantics | behaviour | 1457 |
| C18 | chips per route; dock on screen and covering nothing | behaviour + layout | 1515 |
| C19 | tool counts re-derive from the data; path, find, guard | content | 1588 |
| C20 | search ranking and highlighting | content | 1696 |
| C21 | thread report citations honest | content | 1743 |

## Findings

1. **The map is at its limit by construction** (one screen, no zoom, one size), not because of the data. The
   135 budget calls itself a stopgap (`build_l0.py:85-90`). It needs a different orientation surface; then
   C5/C11 stop being tied to a 1920x1080 viewport.
2. **Node connections hide their meaning.** Group by the edge types and direction, show each edge's sentence
   and sources inline, and stop replacing 65% of types with "member".
3. **A lot of the record is shown nowhere:** 664 of 780 open questions (only FOIA-linked ones render,
   `node.ts:204-215`); `unverified` notes on 213 nodes; chronology and affiliations on 243; node-level sources
   on all nodes; entityInfo (68); status, sub, whatItIs, denialPosture, the members list; edge sources; the
   text of 1,026 timeline events; 62% of claims show their citation only as a tooltip.
4. **Curated entry points reach 157 of 1,136 nodes (14%).** The entry paths' 100 node ids go unused; "Start
   from a witness" opens a map holding 0 of its 7 nodes; only 10 of 338 people are on any thread. No browse
   pages: THREADS and PATENTS each open one fixed item (`frame.ts:23-24`).
5. **Hubs dominate although size never encodes importance.** Degree decides map membership, breaks search
   ties (`search.ts:148`) and draws most lines at rest.
6. **Beyond hop 1 the neighbourhood is a roster, not a structure.** Hops 2 and 3 are a breadth-first walk over
   all edges with no type or tier filter; the hop-1 node that brings each one in (`parentOf`) is computed but
   never drawn (`hood/model.ts:151-202`). AARO at 2 hops: 46 of 61 and 84 of 228 named, 159 folded into "+N".
   167 of 219 denial edges touch a below-floor node, so most denials in the hood draw cyan, not red.
7. **The analyst's tools already do what the UI cannot:** search over events, edges and threads, facets,
   grouping and shortest paths (`tools.ts:157-371`). The UI's search promises events and finds none
   ("scandinavia" returns 0). Old `/path/a/b` links dead-end. The thread report and timeline scope have no
   inbound links.
8. **No phone layout:** at 375px the node page's main column is 0px wide; the smallest breakpoint is 1100.
   Evidence's "denied" flag is set per node, which paints 1,149 claims red (`build_app_data.py:286, 426`).

## Other measurements

- Source: 9,320 lines (7,626 TypeScript, 1,694 CSS), no framework, no runtime dependencies. `pages/pending.ts`
  (76 lines) is dead code. Map toggles, hood hop count and opened timeline years are module state, not in
  the URL.
- Search indexes nodes plus claims.json (lazy, 3.9 MB on the first keystroke); not events, edges,
  narratives, open questions, threads, patents or FOIA. Node ties broken by degree; claims ranked with tier
  dominant (C20 guards it). Only Escape works on the keyboard.
- Timeline strands: program 433, witness 207, oversight 245, coverup 174. Default view: 560 items, 123
  chips, 437 marks (78% unlabelled). No filter controls, no event detail.
- Analyst: TOOLS_VERSION 2026-09-11.1; 14 rounds; cached case index about 39k tokens; Worker model
  claude-opus-5, 16k max tokens, adaptive thinking, effort high.
- Design system: ground #14171c, text #e6e9ee, cyan #5ed4e6, amber #efb555, red #e8705f; IBM Plex Mono
  self-hosted. Colour overload: amber means T2, start-here, custody/funding AND FOIA; cyan means T1, links,
  members AND selection. Class colours collide (event/location #7fb4e8, legislation/domain #e08ad0).
- **Em dashes ship in UI strings** (`hood.ts:285`, `node.ts:218`, `notfound.ts:29`, `report.ts:76`,
  `render.ts:390`, analyst tool headers), against Stewart's standing rule; C19 parses them, so removing them
  touches that check.
- Performance: main JS 91.4 KB (32.5 KB gzip); every route loads index.json (515/60 KB) + analyst.json;
  evidence and the first search keystroke pull claims.json (3.9 MB / 833 KB). `/data` is no-cache; seven
  separate fetch caches fetch some files twice.

## Assessment

- **Solid and reusable:** the data contract and generator; router, back button, `h()`, tokens; the analyst
  tools as a query engine; reports, threads, patents; search ranking; the poison method and the nine
  content checks.
- **Brittle or over-constrained:** the one-screen map, the fixed-capacity hood, fixed-width node columns,
  checks tied to class names and wording, state outside the URL.
- **Essential constraints:** section 2 sourcing (C1, C8, C13, C14, C16, C19, C21); size never encodes
  importance (extend it to selection); the Back button.
- **Historical accidents:** the one-screen no-zoom map, "nothing may take height", C11 at 1920x1080, bands by
  rarest tag, the 135 budget.
