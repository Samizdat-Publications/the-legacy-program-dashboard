# Design response: a new shell for The Program (2 September 2026)

Answers `notes/DESIGN-BRIEF-SHELL-2026-09-02.md`. Everything here was built from
`data/design-extract.json` and the three captures in `notes/shots/2026-09-02/`. The
three files over the read cap were not opened.

The mockups are a working page, not drawings: `Program Shell.dc.html` in the design
project renders every screen from the extract at the three widths, and the PNGs under
`notes/shots/design-2026-09-02/` are captures of it. Where the extract does not carry a
thing (claim text, sources, the 912 events, patents' titles and sheets, FOIA requests,
the analyst's seven questions, hand-written edge evidence), the mockup says so in
italics in square brackets. There is no invented copy.

## 0. What is in the extract and what is not

Used as real data: 125 map nodes with label, short label, class, cluster, tier A/B/C,
C/A/D axes, dates, era, roles, the 400-character `whyImplicated` opening, the direct
member list (with class and tier) and the routed list (with depth); 247 direct edges
with tier and types; 121 summarised edges with their via-members; 51 denial pairs with
their labels; the six entry paths with blurbs and counts; the distributions; the
authority list. The 14 start-here flags are not in the extract; they were read off
`map-1920x1080-open.png` (the amber numbered chips) and are listed in section 2.5 so the
build can check them against the owner's list.

Not in the extract, therefore placeholders: claim text and sources, the 912 timeline
events, the four strands, FOIA requests and open questions, the patents' titles, sheet
images and file-wrapper dates, the analyst's suggested questions, the per-edge evidence
lines, the full dossier narrative beyond 400 characters, the band rule of the current
renderer (see 4.1).

## 1. The screens

All PNGs: `notes/shots/design-2026-09-02/<nn>-<screen>-<w>x<h>.png`.

| # | Screen | 1366×768 | 1920×1080 | 2560×1440 |
|---|---|---|---|---|
| 1 | Home | `01-home-1366x768.png` | `01-home-1920x1080.png` | `01-home-2560x1440.png` |
| 2 | Node page (`#/n/aawsap`) | `02-node-…` | `02-node-…` | `02-node-…` |
| 3 | Map | `03-map-1366x768.png` (cell mode, one cell open) | `03-map-1920x1080.png` | `03-map-2560x1440.png` |
| 4 | Neighbourhood (`#/hood/aawsap`) | `04-neighbourhood-…` (1 hop) | `04-neighbourhood-…` (2 hops) | `04-neighbourhood-…` (2 hops) |
| 5 | Thread (`#/t/custody`) | `05-thread-…` | `05-thread-…` | `05-thread-…` |
| 6 | Timeline | `06-timeline-…` | `06-timeline-…` | `06-timeline-…` |
| 7 | Patents (`#/patents/10144532`) | `07-patents-…` | `07-patents-…` + `07b-patents-lightbox-1920x1080.png` | `07-patents-…` |
| + | Evidence explorer | `08-evidence-…` | `08-evidence-…` | `08-evidence-…` |
| + | Report (`#/report/n/aawsap`) | `09-report-…` | `09-report-…` | `09-report-…` |

### 1.1 Common frame

A 40 px bar: wordmark, eight routes (Home · Map · Neighbourhood · Threads · Timeline ·
Patents · Evidence · Report), the search field, and on the right the current URL
fragment and the viewport. The search field is the same control on every screen; on
Home it is repeated large. Ground `#0c1119`, panels `#121a26`, borders `#263141`, text
`#cfd8e3`, cyan `#52d3dd`, amber `#e2a93b`, red `#e2605b`. Class colours as in the
current map's chip markers (institution blue, program violet, document yellow, event
green, legislation pink, person salmon, location teal, domain grey); take the exact hex
values from the current renderer, the mockup approximates them. Type is IBM Plex Mono at
11 px for every label, 12–13 px for body, one size per role. No gradients, no hero
metric, no size encoding anywhere.

### 1.2 Home

Search first: a 52 px field. One paragraph on what the board is and the sourcing rule
(the paragraph in the mockup is written from the brief's description; the owner should
replace it with their own). The six entry paths as cards, each with the real blurb and
`total · onMap` from the extract, opening `#/t/<entry id>`. The 14 start-here nodes as
numbered amber chips in the owner's reading order. The counts table (all figures from
the brief). The analyst box with seven suggested-question slots. At 1366 the six cards go
3×2 and the right column narrows; nothing is dropped.

### 1.3 Node page `#/n/<id>`

Header: class · tier · cluster · dates, the label as an H1, the three axes as three
3-cell bars with the number beside them (position, not size), the roles as chips, then
three actions: **Show on the map**, **Open the neighbourhood**, **Report**. Below:
*Why it is on the map* (the dossier narrative), *Claims · N* grouped T1/T2/T3 each with
its source as a link on the right, *Denials on the record* (from `denialPairs`, red
rule), and the timeline slice and FOIA block. Right column: *Sourced connections* as one
row per edge with class mark, label, edge type and tier, on-map neighbours first, then
members below the floor.

- 1366: two columns (main + connections 340 px); slice and FOIA sit under the denials.
- 1920: two columns (main + connections 520 px).
- 2560: three columns; the slice and FOIA get the third.

The mockup shows AAWSAP because it is start-here 1 and carries the richest record in
the extract (59 distinct neighbours, 83 members, one denial).

### 1.4 The map

The orthogonal program map is the default map. Bands are rows (7), eras are columns (5,
including *No date*), chips are one label size (11 px), width fitted to the text, packed
left-to-right by start date within each band × era cell. Edges are orthogonal (exit
horizontally, one vertical, enter horizontally) with a 2 px end mark; the rest budget is
the 118 tier-1 direct edges with the most types, denial edges red, derived pairs amber
dashed and off by default. Start-here chips are amber with their number on the right.

- 1920: all 125 names at 11 px, row pitch 18, band gap 12, 130 links at rest.
- 2560: the same layout with row pitch 26 and wider band gaps.
- 1366: **cell mode.** The label layout needs 1,300 px of height at this width and there
  are 656. Each band × era cell shows its count and as many names as fit at 11 px in
  start-date order, then a `+N` chip. No links at rest. The capture shows the
  *Oversight × 2017-2026* cell (13 nodes) expanded. See 2.3.

### 1.5 The neighbourhood `#/hood/<id>`

The selected node in the centre, hop 1 on a ring, hop 2 in two outer columns. Ring
positions are assigned by *y*, not by angle: the ring's height is divided into label
slots of 15 px on each side, so labels never collide by construction. Lines from the
centre to hop-1: solid cyan for member edges; dashed and type-coloured for edges to map
nodes (denial red, custody/funding amber), with a dash-offset animation on the selected
node's edges. Hop-2 lines are dotted grey. Derived pairs (shared members) draw as dotted
grey and switch off with **Derived**.

- 1366: hop 1 only by default (59 nodes, 47 named at ring radius 230); hop 2 is a
  toggle.
- 1920: two hops, ring radius 300, 47 of 59 at hop 1 named, 15 of 24 at hop 2.
- 2560: two hops, ring radius 420, everything named.

Whatever is not named is not drawn; the count goes in a `+N … expand` chip under the
ring. With no node selected the screen shows the 14 start-here nodes on the ring around
an empty centre labelled *pick a node*.

### 1.6 Thread page `#/t/<id>`

Left: the ordered chain, one node per step with class mark, year, one line of evidence,
and the edge's type · tier · direct/derived. Right: a small map (the same 7 × 5 grid,
each step as its numbered chip only, orthogonal links between consecutive steps) and a
timeline slice with the steps' years. A rail of the eight threads across the top.

The eight threads, using only edges that exist in the extract:

1. **Lineage** — AAWSAP → AATIP (programmatic T1) → KONA BLUE (derived via Reid and
   Bigelow) → AARO Historical Record Vol I (investigative/programmatic T1).
2. **Custody** — House Oversight hearing 26 July 2023 → Waived SAP Notification Group
   (derived via Grusch, Luna) → 10 U.S.C. 119 (legislative T1) → KONA BLUE (behavioral
   T1) → Lockheed Skunk Works (custody T2) → Lockheed Martin (derived via Ben Rich, GAO
   accession 130581, Plant 42).
3. **Money** — DoD Agency-Wide Audit → Classified Annex (derived via Funding Channels,
   SFFAS 56) → DoD SAPCO (funding T1) → Waived SAP Notification Group (institutional T1)
   → 10 U.S.C. 119 → FY2024 NDAA sec. 1687 (legislative T1).
4. **Denials** — the 51 `denialPairs`, denier → denied, with the pair label as the
   evidence line. This thread is fully real in the mockup.
5. **Wilson-Davis** — Wilson-Davis Notes → EG&G (custody T3) → Lockheed Martin (derived)
   → AARO Historical Record Vol I (denial/temporal T1).
6. **Patents** — US 10,144,532 → US Navy (institutional T2) → UAP Task Force
   (institutional T1) → ODNI Preliminary Assessment (institutional/programmatic T1).
7. **Missing scientists** — no candidate nodes above the floor in the extract; four
   placeholder steps.
8. **Oversight 2023–2026** — Hearing 26 July 2023 → AARO (derived) → Task Force hearing
   9 Sep 2025 (denial T2) → Burlison to MITRE (investigative T3) → MITRE
   (investigative/denial T1) → UAPDA FY2027 House-adopted (legislative T3).

Where two consecutive steps have no edge in the extract the mockup prints a red
placeholder; the build must reject such a step (check C7).

### 1.7 Timeline

Four strand lanes, five era columns as the outer structure. Closed eras show one count
per lane; the open era (2017-2026 in the captures) shows year gridlines and events as
chips, packed into rows so that no two overlap; an event that cannot be placed at 11 px
is a 5 px mark until its year is opened. Scope switches (All · Node · Thread) filter to
the current node's slice or the thread's steps. The mockup uses the 125 map nodes' start
dates as stand-in events and derives strand from roles (concealment → cover-up, oversight
→ oversight, disclosure → witness, else program); the build uses the 912 events and the
board's own strands.

### 1.8 Patents

Left: five sections, one per patent, with number, title and status (only 10,144,532 has
its node in the extract; the other four titles are placeholders). The five observables as
their own list under the patents. Right: the selected patent's header (inventor,
assignee, grant date, maintenance-fee status), the sheets as a grid in order, and the
prosecution timeline from the file wrapper (filed, rejection, two declarations, appeal
brief, granted). Clicking a sheet opens the lightbox (`07b-…`): the sheet at reading
height (viewport minus 160 px), caption, prev/next, ESC. At 1366 the sheets are one row of
eleven; at 1920 and 2560 two rows of six.

**Cost of sheets at reading size.** Eleven sheets as 1600 px-tall greyscale JPEGs are
roughly 200–350 KB each, 2.5–4 MB embedded, ×1.33 as base64: the page grows by 3.5–5 MB
and the first paint waits on it. Proposed trade: embed eleven 400 px thumbnails (about
25 KB each, 0.35 MB total) for the grid, and load the reading-size sheet on demand from
`notes/…/patents/` next to the page. That is a second runtime fetch besides the analyst,
so it needs the owner's sign-off; if it is refused, embed 1000 px sheets (about 90 KB
each, 1.3 MB base64) and accept the weight.

### 1.9 Evidence explorer

Left rail of filters (tier, class, cluster, source domain, denied, open question), each a
row of chips with real counts. Table: tier · class · node · claim · source · denied ·
FOIA, the FOIA column showing the request beside the question it would close. The
mockup's rows are one per map node with its real T1 count; the build lists every claim.

### 1.10 Report

A light page (paper colours, still monospace) sized to the viewport: header line with
type, URL and generation date; title and axes; the narrative; claims by tier as a
numbered list; denials; connections in 2–3 columns; citations at the foot, numbered
superscripts in the body. Printable as-is.

## 2. Interaction spec

### 2.1 URL scheme

```
#/                         home
#/n/<id>                   node page
#/n/<id>/map               map, scrolled and centred on <id>, its edges drawn
#/n/<id>/hood              neighbourhood of <id>          (alias #/hood/<id>)
#/hood                     neighbourhood, nothing selected: start-here ring
#/map                      map at fit
#/map?cell=<band>.<era>    map with that cell expanded (cell mode) or highlighted
#/t/<id>                   thread
#/t/<id>/map               map with the thread's steps highlighted
#/timeline                 all strands, counts
#/timeline?era=<era>       one era opened
#/timeline?scope=n:<id>    scoped to a node       (or scope=t:<id> for a thread)
#/patents/<number>         patent section          ?sheet=<k> opens the lightbox
#/evidence?tier=1&cls=…&cluster=…&denied=1&open=1
#/report/n/<id>            report for a node       #/report/t/<id> for a thread
```

Ids are the board's node ids (`aawsap`, `kona-blue`); thread ids are the eight above.
Every route is shareable, and every route with a node id opens with that node's name in
the title.

### 2.2 The label rule (map and neighbourhood)

One font size, 11 px, everywhere. A label is drawn only if the whole label fits in the
space available to it at that size; nothing is truncated, abbreviated or shrunk. A mark
whose label does not fit is not drawn; it is counted, and the count is drawn instead.
Order within a cell or a ring is start date, then label; never degree, tier or
connections.

- Map, label mode: chip width = text width + 30 px (+16 for a start-here number); chips
  pack left-to-right, wrapping, within the cell's column. Row pitch starts at 20 (26 at
  2560) and steps down to 18, then the band gap down to 6, before the map gives up on
  label mode. The map is in label mode when the sum over bands of (max rows in the band ×
  pitch) fits the viewport height; otherwise it is in cell mode. Zooming below fit is
  never needed in label mode because the layout is computed for the viewport.
- Map, cell mode: band heights are proportional to the band's largest cell. A cell shows
  `N nodes`, then names that fit in start-date order, reserving 40 px at the end of the
  last row for the `+N` chip. No links at rest; selecting a chip or a cell draws its
  edges.
- Neighbourhood: ring slots are 15 px of *y* on each side. Hop-1 labels have
  (column-x − ring-radius − 26) px of room when hop 2 is on, and (half-width − radius −
  24) px when it is off; hop-2 labels have the room to the viewport edge. Anything wider
  is counted in the `+N` chip under the ring.

Zoom: the map has FIT, FIT ALL and 1:1 as today. Zooming in from fit re-runs the layout
at the new scale; the label rule still applies, so zooming in only ever adds names.
Zooming out below 0.62× switches to cell mode for the whole map, not to smaller text.

### 2.3 Cell expansion

Click a cell (or press Enter on it) → a panel anchored to the cell's bottom edge (or top
edge if it would leave the viewport), one column at ≤500 px, two columns above, listing
every member as a 20 px row: class mark, year, name, start-here number. The list is in
start-date order. The cell keeps its border in cyan while open; ESC or a click outside
closes it. Clicking a row goes to `#/n/<id>`. Only one cell is open at a time; the open
cell is in the URL (`?cell=oversight.2017-2026`) so the state is shareable.

### 2.4 Hand-offs between node page, map and neighbourhood

- Node page → **Show on the map**: `#/n/<id>/map`. The map opens at fit in the mode the
  viewport allows, scrolls so the chip is visible, gives it a white border, and draws
  all of its edges regardless of the rest budget. In cell mode the containing cell opens
  with the node's row highlighted.
- Node page → **Open the neighbourhood**: `#/n/<id>/hood`, two hops at ≥1600 px, one hop
  below.
- Map chip click → `#/n/<id>`. Map chip hover → its edges at full opacity, everything
  else dimmed to 35 %; no tooltip, the chip is already the label.
- Neighbourhood node click → `#/n/<id>`; **Show on map** → `#/n/<id>/map`; changing the
  centre keeps the hop count.
- Thread step click → `#/n/<id>`; the small map's chip click → `#/t/<id>/map`.
- Timeline event click → `#/n/<id>`. Scope chips carry the id from the page you came
  from and are visible only when there is one.
- Back always works: every state above is a hash change.

### 2.5 Start-here register

The 14 flags read off the 1920 capture, in the owner's numbering: 1 AAWSAP, 2 Waived SAP
Notification Group, 3 10 U.S.C. 119, 4 AARO Historical Record Vol I, 5 AARO, 6 The
MITRE Corporation, 7 Carve-Out Provision, 8 DoD Agency-Wide Audit, 9 Immaculate
Constellation 2024, 10 KONA BLUE, 11 The Wilson-Davis Notes, 12 UAP Disclosure Act of
2023, 13 GEIPAN, 14 Operação Prato. Amber border and the number at the chip's right
edge, on the map, in cell lists, in the thread small map, in the timeline and on Home.

## 3. Checks the build should ship, each with a poison

- **C1 must reject** a node id that appears in the page (any route, chip, thread step,
  cell list, report citation) and is not in `the-program.json`.
- **C2 must reject** a label rendered at any font size other than the one label size,
  or with `text-overflow`, an ellipsis character, or a width smaller than its text.
- **C3 must reject** a drawn mark without a rendered label in the map or the
  neighbourhood (an anonymous dot).
- **C4 must reject** any two rendered labels whose boxes intersect, on the map, in the
  neighbourhood, in the timeline or in a thread small map.
- **C5 must reject** a map layout in label mode whose height exceeds the viewport, or a
  map in cell mode at a viewport where label mode would fit.
- **C6 must reject** a cell whose displayed count differs from the number of members in
  that band × era, or a `+N` chip where N ≠ members − names drawn.
- **C7 must reject** a thread step whose pair with the previous step has no edge in
  `directEdges`, `summarised` or `denialPairs`.
- **C8 must reject** a node page claim without a source link, or a claims header whose
  T1+T2+T3 does not equal the node's claim count.
- **C9 must reject** a route in 2.1 that does not resolve, or a rendered link whose
  `href` is not a route in 2.1.
- **C10 must reject** a neighbourhood drawn with nothing selected that contains any node
  other than the 14 start-here nodes, or one that ever contains more than the selected
  node's hop-1 ∪ hop-2 ∪ hop-3 sets.
- **C11 must reject** a start-here register different from the owner's 14 ids, or a
  numbered chip whose number differs from the owner's order.
- **C12 must reject** a mark whose rendered width or height varies with degree, tier,
  connections or claims (size encoding).
- **C13 must reject** a denial row on a node page that is not in `denialPairs` for that
  node, or a `denialPairs` entry for the node that is missing from the page.
- **C14 must reject** a runtime request other than the analyst endpoint (and, if the
  owner accepts the trade in 1.8, `notes/…/patents/*`).
- **C15 must reject** a timeline event placed in the wrong era column or lane for its
  date and strand, or an opened year whose chips + marks ≠ its event count.
- **C16 must reject** any string in the page that matches the mockup's placeholder
  pattern `[… — placeholder …]` or `not in the extract`.

Poisons: for each, a fixture that changes exactly one thing (a truncated label, a shifted
chip, a step with no edge, a stray dot) and the check must fail on it and pass on the
clean build.

## 4. What to change in the current program map

The renderer survives the move; these are changes to it, not replacements.

1. **Band assignment.** The mockup approximates the band rule as "first role in the
   order reverse-engineering · retrieval · custody · funding · research · oversight ·
   disclosure"; that puts 17 in reverse-engineering and 9 in retrieval where the current
   map has 15 and 11. Whatever the real rule is, write it in the data (a `band` field per
   node) so that renderer and checks read the same thing.
2. **Fixed chip width.** The current chips are fixed-width and elide text (`Depar… of
   Defense`, `Anomal…ion Office`). Fit the chip to the text instead; it is the only way
   to keep the no-truncation rule and it frees the columns to pack two or three chips
   per row.
3. **Layout for the viewport, not for a world.** The current map lays out in a 2200 ×
   1420 world and scales it (0.74× at 1920, 0.44× at 1366), so text shrinks. Lay out at
   1:1 for the viewport and switch to cell mode when it does not fit.
4. **Cell mode** does not exist yet (the *Cells* toggle is there). It is the answer for
   1366 and for anything below the label floor.
5. **Rest budget.** 118 links at rest is right; choose them by tier and type count, not by
   endpoint degree, and colour denial edges red so the denial ledger reads on the map.
6. **Derived pairs** should be off by default and dashed amber when on; at rest they
   dominate the current map's long horizontals.
7. **The start-here panel** at bottom right can go; the numbers on the chips and the
   Home list carry it. Keep the *Start here* toggle.
8. **Vertical trunks** currently cross chips freely. Route the vertical segment in the
   inter-column gutter nearest the source (the mockup exits 10 px from the chip and
   turns there); it costs little and stops lines from running through names.
9. **Legend** to the bottom edge, one row, class colours only.
10. **Selected-node halo** (white border) and dimming of everything not connected on
    hover; the current map has neither and it is what makes 130 links readable.

## 5. Files

- `notes/DESIGN-RESPONSE-SHELL-2026-09-02.md` — this file.
- `notes/shots/design-2026-09-02/*.png` — 28 captures (9 screens × 3 widths + the
  lightbox).
- `Program Shell.dc.html` (design project) — the working mockup; loads
  `data/design-extract.json` at runtime for the mockup only. Views are hash-routed as in
  2.1 (`?w=1366|1920|2560` sets the frame).
