# Design brief: a new shell for The Program (2 September 2026)

This brief is self-contained. Everything you need is in this file and the files it
names, all on the `master` branch of `Samizdat-Publications/the-legacy-program-dashboard`.
Three of the board's data files are over GitHub's 1 MB API read cap and will read as
absent; do not try to open `data/the-program.json`, `data/l0-model.json` or
`dist/the-program.html`. `data/design-extract.json` (285 KB) is the readable extract of
the data and it is the one to open.

## What the board is

A research board on the alleged US programme for recovering and reverse-engineering
non-human craft, 1944 to now, built as a single self-contained web page. It is a
sourced graph: every node carries claims graded by evidence strength (Tier 1 documented,
Tier 2 a named person on the record, Tier 3 stated inference), every edge is hand-written
and sourced, and contradictions between what witnesses said and what the record shows are
recorded as findings. Its owner wants to share it with research friends as a tool.

| Figure | Value |
|---|---|
| nodes | 1,027: 300 people, 727 entities across institution, program, document, event, location, legislation, domain |
| sourced edges | 2,348, in 12 types (institutional, custody, funding, denial, witness-chain, programmatic, investigative, legislative, research, temporal, behavioral, geographic) |
| claims | 5,120: Tier 1 3,214, Tier 2 1,394, Tier 3 512 |
| timeline events | 912, in four strands: program, witness, oversight, cover-up |
| the program map | 125 nodes above a floor of six distinct neighbours, each with a written dossier; 7 bands by measured custody proximity, 5 eras |
| start-here flags | 14, signed off by the owner |
| entry paths | custody 46 nodes, denial 39, foreign 11, mechanism 10, money 7, witness 7 |
| patents | 5 Navy patents (US 10,144,532; 10,135,366; 10,322,827; US 2019/0058105; US 2019/0295733), 11 drawing sheets, and the prosecution file wrapper of 10,144,532 (rejections, two declarations, an appeal brief) |
| FOIA layer | 17 requests linked to 121 open questions on 42 nodes |
| analyst | a question box answered by a model that cites nodes; seven suggested questions |

## What is wrong with the current shell

The shell was written for a different, fifty-node project and patched into this one.
At 1,027 nodes:

- The default view is a force-directed graph of all 1,027 marks and 3,919 links. Labels
  are one size and chosen by available space, so at rest 17 nodes are named and the rest
  are anonymous dots. The owner's words: "a thousand dots that mean nothing".
- The one legible surface, the orthogonal program map (125 named chips, bands by era),
  is on the second tab.
- The dossier, which is the actual content, opens in a half-width dock with no URL.
  Nothing can be linked to.
- The timeline is 912 events on one axis. The patents tab is eleven thumbnails in a row.
  Analysis, Case files and Geography carry copy and computations designed for the other
  project.

Screenshots of the current program map at three widths are in
`notes/shots/2026-09-02/` (`map-1366x768-open.png`, `map-1920x1080-open.png`,
`map-2560x1440-open.png`). The 1920 capture is the best statement of what the owner
likes: orthogonal routing, one label size, era columns, band rows, cyan links with
directional marks, an amber start-here register. The current network map is not
captured because it does not survive a screenshot; the owner's description above is
accurate.

## What to design

A new shell, entity first and map second. Seven screens, each at 1366 by 768, 1920 by
1080 and 2560 by 1440, plus an interaction spec. The data does not change; the page
embeds it.

1. **Home.** Search first. One paragraph on what the board is and the sourcing rule.
   The six entry paths as cards that open threads. The 14 start-here nodes. The counts.
   The analyst's seven suggested questions. This is the first thing a friend sees from
   a shared link with no node in it.
2. **Node page** (`#/n/<id>`). The dossier as a page: label, class, tier and the three
   axes (custody proximity, access, disclosure role, 0 to 3 each), status and date; the
   narrative; claims grouped by tier, each with its source as a link; denials on the
   record; sourced connections as a list with the evidence on each edge and its type;
   the node's timeline slice; its FOIA requests and open questions; "show on the map"
   and "open the neighbourhood". This is the unit of the product and the page a link
   opens on.
3. **The map.** The orthogonal program map as the default map, at fit, all 125 names
   readable at 1920 and above. Below the label floor a cell shows a count instead of
   anonymous marks, and a click expands the cell to its members. The 875 nodes below
   the floor are reached by cells, search and pages, never drawn as unnamed dots.
   Keep: the band and era structure, one label size, orthogonal routing, the start-here
   register, links at rest by budget.
4. **The neighbourhood.** The selected node and its sourced edges at one, two or three
   hops, with the current force-graph rendering the owner likes (metro-style lines with
   animated flow along the selected node's edges, collision-tested labels). Derived
   pairs (shared employer, location, domain) drawn muted and switchable. It never draws
   the whole graph; with nothing selected it shows the start-here nodes and asks for
   one.
5. **Thread page** (`#/t/<id>`). An ordered chain of nodes with one line of evidence per
   step, a small map of just those nodes, and the timeline slice. Eight threads to
   start: the AAWSAP to AATIP to KONA BLUE lineage; the custody chain from Grusch to a
   named contractor; the money; the denial ledger; the Wilson-Davis notes; patents and
   prosecution; the missing scientists; oversight 2023 to 2026.
6. **Timeline.** Four strand lanes, eras as the outer structure, counts per era at low
   zoom, events at high zoom, scoped to the current node or thread when there is one.
7. **Patents.** One section per patent with its sheets in order, a lightbox that opens a
   sheet at reading size, the prosecution timeline from the file wrapper, and the
   maintenance-fee status. The five observables as their own section.

Also: an **evidence explorer** (the claims as a filterable table: tier, class, cluster,
source domain, denied, open question, with the FOIA request beside the question it
would close) and a **report** (a printable brief for the current node or thread with
numbered citations). Both can be simpler than the seven screens; a layout for each is
enough.

## Constraints that do not bend

- Dark ground, monospace type, the existing palette (cyan for links and confirmed
  claims, amber for claims and start-here, red for open questions and denials, the
  class colours already in use). Do not introduce gradients, glassmorphism or a hero
  metric.
- **Size never encodes importance.** The largest node on the old map was AARO, which
  the board treats as implicated, not authoritative. Position and grouping are
  available; size is not.
- **Labels are one size and chosen by space, never by rank.** A label that would have
  to be shrunk or truncated to fit is skipped. A mark that cannot be named at the
  current zoom is not drawn as an anonymous dot.
- **Nothing invented.** Mockup copy uses real node names, real claims and real figures
  from `data/design-extract.json`. Placeholders are marked as placeholders. This rule has
  no "just for the mockup" exception.
- One self-contained page, no runtime fetch except the analyst. If the patent lightbox
  needs images at reading size, say what they cost and propose the trade.
- Three viewports. At 1366 the map will not fit with labels; say what the reader gets
  instead.

## What to send back

1. The seven screens at three widths, as PNG, with the real data.
2. An interaction spec: the label and zoom rule for the map and the neighbourhood; what
   a cell expansion looks like; how a node page, the map and the neighbourhood hand off
   to each other; the URL scheme.
3. The checks you would want written against the build, in the form "must reject
   <input>", the way the previous Design response listed nine of them. The build will
   ship each one with a poison that proves it fires.
4. Anything in the current program map you would change, since that renderer survives
   the move.

Reply in a file, not in a chat message, so the build session can read it from the
repository: `notes/DESIGN-RESPONSE-SHELL-<date>.md` with the PNGs under
`notes/shots/design-<date>/`.
