# Brief for Claude Design: the network map, reconsidered

**Repository:** `Samizdat-Publications/the-legacy-program-dashboard` (private), branch
`master`. **You have GitHub read access to it.** Everything this brief cites is on
`master` and is under 1MB, so you can open it.

**This brief is self-contained.** You do not need to read `CLAUDE.md` or any other
note to act on it. Read this file and the five screenshots in
`notes/design-2026-08-30-network/`. **Those five PNGs were captured on 30 August
at 964 nodes; the board is now 980 after a research pass added sixteen. The
arrangement, the density and every problem described here are unchanged — the
figures in this brief are the current ones and the screenshots are 1.7% lighter
than what you would see today.** If you want the underlying data,
`data/design-extract.json` (287KB) is purpose-built for you. **Do not try to open
`data/the-program.json`, `data/l0-model.json` or `dist/the-program.html`** — they are
7MB, 6MB and 16MB, and the GitHub API reports files that size as *absent* rather than
as too large, which has misled two sessions.

---

## 1. What the board is, in one paragraph

A research board mapping the alleged legacy UAP recovery and reverse-engineering
programme, 1944–2026. One self-contained HTML file, no server, no runtime
dependencies. **980 nodes and 2,194 hand-written, individually sourced edges**, plus
4,728 claims graded T1/T2/T3 by evidence strength. It has ten views. Two of them are
maps:

| | |
|---|---|
| **NETWORK** | the force-directed full graph, all 980 nodes. The primary view, the first thing a reader sees. **This brief is about this map.** |
| **PROGRAM** | your packed-cell layout — 112 nodes, 7 bands × 5 columns, one chip size. Its own tab. Working well and not in question here. |

The node classes and their counts:

| class | n | current mark |
|---|---|---|
| person | 286 | filled dot (plate when selected or hovered) |
| document | 202 | ring |
| institution | 167 | square |
| event | 74 | ring |
| location | 69 | ring |
| program | 68 | diamond |
| domain | 59 | dot inside a ring |
| legislation | 55 | ring |

---

## 2. What you ruled on 30 August, and what was built

You answered a brief about label density with five changes. All five shipped, gated,
in the order you specified.

1. **The map label carries the NAME only.** Date and status are dossier facts.
2. **The drawn label set is chosen by SPACE, never by rank.** Walk candidates outward
   from the pointer (or the viewport centre when it is off-canvas), compute the box at
   a fixed label size, draw it if it does not collide, otherwise **skip the node
   entirely** — never shrink, never truncate to fit.
3. **Pointer proximity, and nothing else.** Within a radius the label raises in
   priority and draws regardless of budget. Typography changes; geometry never does.
4. Warm arrival on the packed map.
5. The two map bridges as two controls.

**You were more right than you knew on 2.** You rejected greedy-by-degree outright.
The board was *already doing it*, in two places nobody had noticed: `PLATE_DEGREE`
decided which people got a plate at all — and a plate is how a person is named — and
`LABEL_DEGREE` gated entity labels directly. Both are gone. A check holds the line.

**Three further changes were made since, in response to the owner using the live
board.** They are repairs, not design:

6. **Selecting a node now names its neighbours.** It named one of ten. The renderer
   computed "connected" state and discarded it before the label pass, and the ~900
   dimmed nodes competed for the same collision boxes while drawing at 0.16 alpha.
7. **A mark never draws below 3.2 screen pixels, and the selected plate is a fixed
   screen size.** Labels were in screen space at one size; marks were still in world
   space. At 0.25× a person dot drew at 1.1px and vanished under a full-size name; at
   3.3× the plate drew 330×132 over 9px labels.
8. **Hold space to pan.** Every drag was landing on a node.

---

## 3. What the owner says now, and he is right

> I'm so torn because I like the look of this, but the nodes are just geometry with
> occasional white text, they need to be boxes like the names like DeLonge etc are or
> something. I think we really need design to think this through again.

> I also don't like the plain white labels we have everywhere, maybe they need a
> background or something.

> clicking the various filters doesn't really materially change or highlight anything.

He also said, and this is the actual commission:

> if you need it to rethink this entire map knowing what we've built and what we now
> know, let's give it the chance to redo it in a way that allows us to have this much
> data plotted without making it useless and all noise.

---

## 4. Measured facts, not impressions

Every figure below was read out of the running renderer at 1920×1080, after letting
the animation settle. Nothing here is estimated.

| | |
|---|---|
| nodes drawn | **980, always.** Nothing is ever removed from the field |
| links drawn | **3,919 pairs** |
| of those, hand-written and sourced | **2,194.** The rest are derived: shared employer, shared location, shared domain |
| labels drawn at rest | **143** of 980 |
| **nodes at full opacity at rest** | **501** |
| **nodes at 0.01 opacity at rest** | **463 — 48% of the board is invisible before the reader touches anything** |

### The filters do the opposite of filtering

This is the finding worth your attention, and it explains the owner's complaint
better than his own words did.

| state | at α ≥ 0.5 | labels drawn |
|---|---|---|
| at rest | 501 | 143 |
| after clicking **Tier A** | **956** | 214 |
| after also clicking **Deceased** | **938** | 211 |

**Clicking a filter reveals more of the board, not less.** They are additive reveals
wearing the visual language of filters. A reader who clicks "Tier A" expecting to be
left with 143 Tier A nodes is instead shown almost the entire board at once. That is
why nothing appears to happen: something does, in the direction of more noise.

### Screenshots

In `notes/design-2026-08-30-network/`, all at deviceScaleFactor 1:

| file | what it shows |
|---|---|
| `1-rest-1920.png` | the opening state. 143 labels, 463 nodes at 1% opacity |
| `2-selection-1920.png` | `tom-delonge` selected. All 10 neighbours named, 0 overlaps |
| `3-zoomed-out-1920.png` | 0.46×, 72 labels — the state where marks used to vanish |
| `4-rest-1366.png`, `5-rest-2560.png` | the same rest state at the two extremes |

---

## 5. The five questions

**Q1. What is a node, visually?** Today: a 4.5–6.5px outline in one of four shapes,
coloured by cluster, with a 9px label under some of them. The owner's instinct is
that everything should read like the person plate — a bounded object with a name in
it — rather than geometry that occasionally has text near it. A plate for all 980 is
clearly impossible at this density. What is the middle? Consider that **class is
already carried by shape and cluster by colour**, so a new treatment must not need a
third channel.

**Q2. The labels.** They are 9px `IBM Plex Mono`, `PALETTE.text` or `PALETTE.dim`,
drawn directly on the field with no background. Against a dark map crossed by
coloured edges they read as floating. A plate, a halo, a knockout, a leader line —
your call. Constraint: whatever it is gets drawn up to 215 times a frame and must not
enlarge the collision footprint enough to halve the number of labels that fit.

**A second, concrete half of the same question, observed on screen on 30 August.** Long
labels middle-truncate, and on document nodes the result can be unreadable. A GAO
document whose real title is *"GAO accession 130581 — Controls Over Classified Documents
for a Special Access Program at Lockheed Corporation"* draws on the map as:

    GAO ACCESSION 130581,CKHEED CORPORATION

The truncation keeps the head and the tail and drops the middle, which is the right
instinct and the wrong result: it produces a fragment that reads as a corrupted string
rather than a shortened name. This is not rare — the board carries 202 document nodes and
many have titles of that length; `gao-04-332`'s is longer still.

The PROGRAM map already solved this, and you specified the solution: authored short labels
in `data/l0-shorts.json`, 47 of them, none over 37 characters, with rules that forbid
introducing any fact not already in the full label. **The question for you is whether the
NETWORK map should read the same file** — which would mean authoring shorts for far more
than 112 nodes — or whether a label treatment (Q2's plate, halo or leader line) changes the
available width enough that a better truncation rule is sufficient. We have not guessed.

**Q3. Should 48% of the board be at 1% opacity at rest?** This was not a decision
anyone recorded making. It may be right — the map is legible partly *because* half of
it is suppressed — but if it is right it should be deliberate and the reader should
be able to tell what is being held back. If it is wrong, the opening state needs
rethinking, not tuning.

**Q4. What should a filter do?** Given the table in §4, we think this needs a rule,
not a fix: does a filter narrow the field (remove non-matching nodes), emphasise
within it (keep everything, raise matches), or drive the label budget (matches get
named first)? Pick one and we will make all of them obey it.

**Q5. Sourced vs derived, which the map has never said out loud.** 2,194 of 3,941
drawn links are hand-written and individually sourced; the other 1,747 are inferred
from shared attributes. Selecting DeLonge names ten neighbours while his dossier says
"2 connections", and **both are correct** — he has two sourced edges and eight derived
ones. We have made sourced neighbours draw at full strength and derived ones muted, as
an interim. Is a brightness difference enough for a distinction this load-bearing, or
does a derived link need to be a different *kind* of line?

---

## 6. Rules that do not bend

- **Size must never encode importance.** The largest node is AARO, which this board
  treats as implicated, not authoritative. Position is available; size is not.
- **No selection by rank.** Degree is global — it names the same nodes for every
  reader on every frame, which is why it may not decide who gets a name. Adjacency to
  the reader's own selection is a different thing and is allowed.
- **Skip, never shrink.** A label that must be made smaller to survive is a label the
  map does not have room for.
- **Static at rest.** With nothing selected and the pointer off-canvas the map does
  not move. Motion is a claim about direction, and on most of these 2,194 edges no
  such claim is made. Two gate checks hold this and they are not negotiable.
- **No invented sources, URLs, document numbers or quotes**, including in mockup copy
  and placeholder data. If you need a placeholder, mark it unmistakably as one.

## 7. What we need back

A written response is enough — we will build it. If you produce a comp, one static
full-view is less useful than three states: rest, one node selected, and one filter
applied. **Say explicitly which of the five questions you are answering and which you
are declining**, so nothing gets built on a guess.
