# THE PROGRAM — dashboard build plan

How the v2 dashboard gets recreated for the new dataset. Written 2026-08-12 against
`the-vanishing-v2.html` (316 KB) and `design-package/DESIGN-SYSTEM.md` (36 KB), both
of which I have in full from the zip. Nothing further needed from you to build it.

---

## 1. What I'm reproducing

Everything, unchanged, unless it is listed in §3 as broken by the new data.

**Shell** — four rows, never scrolls as a whole. Top bar 46px · stats strip 46px ·
body (`rail 202px / view surface 1fr / dock 306px`) · analyst full-width at the bottom.
The view surface is the only thing that swaps between views. That constraint is what
makes the analyst able to drive the whole product, so it is preserved exactly.

**Design tokens** — carried over verbatim. `--bg:#0f1216`, the panel and line ramps,
the semantic accents, IBM Plex Mono at 11px, the phosphor bloom text-shadow, the
scanline and vignette ambient layers, the four motion tokens and three easings.
Rail 202px, dock 306px. The look does not change.

**The network map** — canvas layer order (gradient base → 44px grid → cluster wells →
edge traces → nodes → DOM callout/tooltip), dossier plates at 100×40 (132 only with a
real photograph — we have none, so 100 throughout), 3px status stripe, cluster wells as
radial gradients centred on member means, circuit-routed edges with strength.

**The dossier dock** — the second most important surface in the product. Class eyebrow,
status badge, assessment block with the three axes as 3-pip meters, unexplained residual
on a solid `--signal` border above the tabs, then DOSSIER / CHAIN / LINKS / SOURCES.
Missing values print as `NOT REPORTED` / `NOTHING RECORDED`, never blank, never zero.

**The AI Analyst** — full width at the bottom, header row + 208px transcript + suggestion
chips + input row. Action narration printing verbatim `:: selectNode("david-grusch")`
call lines in `--program` before the prose. Citation chips that drive the map. The
settings panel anchored `position:absolute; top:46px; right:15px` — *not* a centred modal,
for the documented reason that the app root sits in a transformed ancestor. Three
localStorage keys, renamed `program.apiKey` / `program.model` / `program.effort`.
The no-API-key state stays first-class: scripted replies, dashboard fully usable by hand.

**The command surface** — one `CMD` namespace, every action reachable by click too.
All sixteen existing actions keep their names and signatures.

**Credibility rules §8** — all seven. Three confidence levels with three border
treatments, no claim renders without one. Unsourced entities say
`No attributed source on file for this entity.` Derived edges stay separated from
editorial ones in the data layer. Absent values print as absent.

---

## 2. What changes because the subject changed

Mechanical substitutions, no design consequence:

| | The Vanishing | The Program |
|---|---|---|
| Axes | S · P · I | **C** custody · **A** access · **D** disclosure |
| Statuses | dead / missing / resolved | active / former / dead / disbanded / classified / denied / disputed |
| Clusters | california / new-mexico / huntsville / northeast | legacy · contractor · ffrdc · ic · oversight · witness · research · media |
| Strands | cases / oversight / skeptical | program · witness · oversight · **coverup** |
| Edge types | 8 | 12 (added custody · funding · denial · legislative) |
| Node classes | 5 | 8 (added legislation · document · event) |

The status stripe now has seven colours instead of three, and the class colour ramp
needs three more entries. Both are additive to the existing token set.

---

## 3. What the new data actually breaks

This is the part worth arguing about. The design system says the layout is
"tuned to stay legible at 3×" of 52 nodes — about 156. The Program is **911 nodes and
1,553 edges**, which is 17.5×. Five things break, and one is unfixable without a decision
from you.

### 3.1 The force layout will not run

Repulsion is `3200/d²` over every pair, with 900 steps run before first paint so the
graph opens settled. At 52 nodes that is 1,326 pairs per step — about 1.2M operations
total, imperceptible. At 911 nodes it is 414,505 pairs per step, **373 million operations
before the first frame**, then ~415k per frame forever after. The tab will hang on load
and then run at single-digit FPS.

**Fix:** replace the naive O(n²) accumulator with a **Barnes–Hut quadtree** at θ=0.9,
which takes it to O(n log n) — roughly 9,000 force evaluations per step instead of 414,000,
a 45× reduction. Run the 900 pre-paint steps in a **Web Worker** so the chrome paints
immediately, exactly as §7 specifies ("chrome paints immediately; force layout runs 900
steps off-screen"). The visual language is untouched; only the engine underneath changes.
`vanishing-graph.js` keeps its derivation, strength aggregation and edge-routing logic —
I am replacing one function, not the file.

### 3.2 249 dossier plates cannot share a canvas

A plate is 100×40. 249 of them is 996,000 px² of plate on a canvas of roughly
1,400×800 = 1,120,000 px². The plates alone would tile 89% of the surface before a single
edge is drawn. This is not a tuning problem, it is arithmetic.

**Fix — semantic zoom.** Node degree already stratifies the graph cleanly:
58 nodes have degree ≥10, 180 have degree ≥5. So:

- Nodes at **degree ≥10 render as full dossier plates** — 58 of them, which is almost
  exactly the density the original was designed around (52). *The first paint looks like
  the original dashboard.*
- Everything below renders as a **class-coloured dot** at the existing collision radii.
- Selecting a node, or expanding hops, **promotes** its neighbourhood to plates and demotes
  the rest. The promotion animates on `--t-layout`, same as a hop change.
- The threshold is a control in the rail, so "show me everything" is available — as an
  explicit choice with a visible cost, not the default.

This preserves the visual language at the density it was designed for while making the
whole graph reachable. It is the single most important decision in the port.

### 3.3 Tier A has stopped meaning anything

**553 of 911 nodes are Tier A — 61%.** Tier A is supposed to mean "named in sworn testimony
or primary documents as directly inside the program." At 61% the badge does not discriminate,
the tier filter returns almost everything, and the colour coding is noise.

This is a data problem the dashboard would merely expose. It happened because fourteen
independent agents each graded within their own domain, where their subject genuinely was
central. Nobody graded across the whole board.

**Fix:** a wave-3 re-grading pass with a hard distribution target — roughly 15% A, 35% B,
50% C — applied globally rather than per-domain, with the rationale rewritten for anything
that moves. Without this the tier system is decorative.

### 3.4 GEOGRAPHY has no coordinates

**Zero of 249 people carry `coords`.** The v2 schema dropped the field that the original
`events[]` had. There are 95 location nodes, but they are labels, not points.

**Fix, two stages:** ship the original's cluster-card treatment first (tint swatch, name,
count, dot-leader member rows, the reported-distance caveat on dashed amber) which needs no
coordinates and is what the original actually does. Then a wave-3 geocoding task adds
`coords` to the location nodes — most are named installations with published coordinates —
and the footer caveat converts from dashed amber to solid, exactly as §6.5 anticipates.

### 3.5 COUNTERARGUMENTS conflicts with the editorial stance

§8 rule 2 requires counterarguments as a top-level view with equal weight. That rule
exists because *The Vanishing* holds cases open. This board does not — you asked for a
board that presumes the program exists and treats the official record as obfuscation.

I don't think the answer is deleting the view, because its *structural* job is real: a
top-level surface, same card grammar, same density, that stops the board reading as
one-sided assertion. The answer is to change what fills it.

**Proposal: `COVERUP` — "The Cover-Up."** Same card grammar, same density, dashed amber
borders, top-level rail entry. Content is the **159 denial edges** and the `coverup`
timeline strand: every official denial with its signatory and date, every records
destruction, every documented disinformation operation, every stonewalled request. Plus
the extended `PRECEDENT` set — MKULTRA's 1973 record destruction, the NRO classified for
31 years, the 1997 CIA admission of falsified UFO explanations.

This is stronger than a counterarguments view, not weaker. It keeps the design's
credibility function — a reader can see the board engaging with the other side's actual
statements — while the framing does the work you asked for: a denial is data about the
denier. **This needs your sign-off; it is the one place I'm departing from the spec.**

### 3.6 File size

Compact, the dataset is **4.8 MB** of JSON against the original's 316 KB total. Weight is
descs (826 KB), claims (881 KB), sources (383 KB), narratives (321 KB) — all of it dossier
content the dock needs.

Options: single self-contained ~5 MB HTML matching the original's packaging (opens fine
from disk, ~300ms parse, awkward over a network); or an HTML shell plus a `program-data.js`
sibling (~350 KB shell, loads fast, but two files); or a lazy-loaded split where the graph
skeleton inlines and dossier bodies fetch on demand (fastest, breaks offline-from-disk).

**Recommendation: single file.** It matches the original's packaging, it works from a
double-click with no server, and 5 MB is unremarkable for a local artifact. I'd also emit
a ~400 KB "lite" build with the graph but truncated dossier prose, for sharing.

---

## 4. Other views at the new scale

| View | Change |
|---|---|
| **NETWORK** | Barnes–Hut + semantic zoom (§3.1, §3.2) |
| **TIMELINE** | 749 entries vs 40. Vertical three-strand layout holds — it was already designed to scroll — but needs virtualised rendering and the existing `setTimelineZoom` becomes load-bearing rather than a nicety. Strand column count goes 3 → 4. |
| **CASES** | 249 cards. Keep `repeat(auto-fill, minmax(268px,1fr))`, virtualise, default the filter to Tier A persons, add sort by axis score. |
| **ANALYSIS** | The four pattern cards become computed rather than hand-written — institutional overlap across 161 institutions, custody-chain depth, denial density per entity, claim-tier distribution per cluster. Every chart keeps its data labels. |
| **SEARCH** | Unchanged. Empty state shows first nine of 911 rather than of 52. |
| **REPORT** | Unchanged in structure, regenerated content. |
| **GEOGRAPHY** | §3.4 |
| **COUNTERARGS → COVERUP** | §3.5 |

---

## 5. Build sequence

1. **Wave 3** — data remediation (see §6), because building against data that is about to
   be re-graded wastes the build.
2. **Port the shell** — tokens, four-row grid, rail, stats strip, dock skeleton, ambient
   layers, responsive breakpoints. Verify against the original side by side.
3. **Port the map** — derivation from `vanishing-graph.js`, then swap the force accumulator
   for Barnes–Hut in a worker, then semantic zoom.
4. **Port the dock** — four tabs, assessment block, the three new node classes.
5. **Port the analyst** — CMD namespace, action narration, citation chips, settings panel.
6. **Port remaining views** in the §4 order.
7. **Screenshot diff** against the original at 1440px, 1280px, 1000px and 800px. The point
   is that it should be hard to tell which board you are looking at until you read a label.

---

## 6. Wave 3 — what can and cannot be done right now

**Blocked:** this session has spent its entire WebSearch budget (200/200), and the
TinyFish MCP server is not actually connected, so that fallback does not exist. `WebFetch`
still works, which means *fetching a known URL is fine* but *discovering an unknown one
is not*.

**Can be done now — no search required:**

- Tier re-grading to a sane distribution (§3.3) — pure analysis over existing data
- ID normalisation: strip the `p-` prefixes, merge `l-washington-dc` into `l-dc`
- The 40 missing `date` values, from chronology already in each record
- Re-sourcing demoted claims where the primary URL is already known — congress.gov bill
  text, `govinfo.gov` hearing transcripts, the AARO reports, released DIRDs
- Writing the 65 stub dossiers where the source is a known statute or agency page
- Coordinates for the location nodes (§3.4) — named installations, published figures
- Archive.org mirroring via the Wayback availability API, which is a GET

**Needs search, so it waits:** finding a hosted COMETA PDF, resolving whether the
February 2026 directives have signed instruments, TTSA's EDGAR filings, and any new
2025–26 material.

**Recommendation:** run wave 3A now, build the dashboard, then do wave 3B/4 in a fresh
session with the search budget raised. Nothing in 3B changes the dashboard's structure —
it fills in sources on nodes that already exist.
