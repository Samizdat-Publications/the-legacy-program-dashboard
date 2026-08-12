# The Program: Design Brief for Claude Design

**Date:** August 12, 2026
**Status:** optional. Read §0 before commissioning this — it argues for a *scoped* redesign,
not a rethink, and being wrong about that scope would cost more than it gains.

---

## 0. What this brief is, and what it deliberately is not

The Program is a working board. It was produced by taking `the-vanishing-v2.html` and doing
surgery on it: the CSS, the four-row shell, the dossier dock, the canvas renderer and every
view function carried over byte for byte, and a build script splices in a new dataset and
applies ~30 named patches.

**That inheritance is the reason it works, and most of it should not be touched.** The
design system in `design-package/DESIGN-SYSTEM.md` is good, it is internally consistent, and
the dossier dock in particular is the strongest surface in either product. A redesign that
starts from a blank page would throw away the part that is already right.

What genuinely needs design thinking is narrower and specific:

> **The Vanishing was designed for 52 nodes and tuned to stay legible at 3×.
> The Program carries 976 nodes and 1,788 hand-written edges — 17.5× the original.**

Everything that hurts on this board traces to that one sentence. The network map is the
acute case, but it is not the only one. **This brief asks for the map and the density model
to be rethought around this dataset. It does not ask for a new design language.**

If you conclude the shell or the dock should change too, say so and argue it — but the
default answer is no.

---

## 1. Read these first, in this order

| File | Why |
|---|---|
| `the-program/PROJECT.md` | What the board is and the editorial stance. Read the stance before designing anything. |
| `design-package/DESIGN-SYSTEM.md` | The parent board's design system. **This is the inheritance. Assume it holds unless you are arguing otherwise.** |
| `the-program/SCHEMA.md` | The data model, and precisely how it extends the parent's |
| `the-program/dist/the-program.html` | The board itself. Open it. Use it before designing for it. |
| `the-program/notes/DASHBOARD_PLAN.md` | What broke at scale and what was done about it, with the arithmetic |
| `the-program/TESTING-CHECKLIST.md` | The known-weak surfaces, enumerated |

---

## 2. The dataset, in the terms that matter for design

| | The Vanishing | The Program |
|---|---|---|
| Nodes | 52 | **976** |
| People | 14 | **251** |
| Node classes | 5 | **8** (+ legislation, document, event) |
| Hand-written edges | ~10 | **1,788** |
| Derived edges | low hundreds | ~1,900 after gating (18,491 ungated) |
| Timeline entries | 40 | **857** |
| Timeline strands | 3 | **4** |
| Clusters | 3 geographic | **9 functional** |
| Connection types | 8 | **12** |
| Graded claims | ~150 | **4,037** |
| Time span | ~5 years | **82 years, 1944–2026** |

Three consequences worth designing around rather than patching:

**The time span changed character.** A five-year cluster of deaths reads as a list. An
82-year institutional history has *eras*, and the argument the timeline makes is that
THE PROGRAM runs from 1944 while OVERSIGHT does not arrive until 2023. That 79-year gap is
the thesis, and the current vertical four-column layout states it only implicitly.

**Most nodes are no longer people.** 725 of 976 are institutions, documents, programs,
locations, legislation and events. The parent board's visual hierarchy puts the person plate
at the centre and everything else as a small glyph. On this board the *document* is often the
load-bearing object — `aaro-historical-record-vol1` carries 18 denials — and it currently
draws as a 5px square.

**The edges carry the argument.** On the parent board an edge said "these two shared an
employer". Here an edge says "this contractor held this material, according to sworn
testimony, and the government denied it on this date". Twelve types, each with a claim tier
and its own sources. The current strength-ramp rendering was designed when weight meant
"how many independent types" — it now competes with type, tier and direction for the same
visual channel.

---

## 3. The actual problem to solve

### 3.1 Density — the primary ask

At rest the map currently shows a **significant subgraph**: person plates earned at degree
≥5 of hand-written links (~46 of them, close to the original's 52), non-person nodes at
degree ≥4, and only edges that are either corroborated by 2+ types or belong to a sourced
type. Selecting anything restores the full neighbourhood.

It works, and it is a large improvement on the hairball it replaced. **It is also a
threshold I guessed at.** The result is legible on the right two-thirds and still crowded in
the upper-left, where the witness, oversight and IC clusters carry most of the Tier A nodes.

What would help:

- A principled model for **what a reader should see first** on a 976-node graph, rather than
  four numeric thresholds picked by trial.
- Whether **progressive disclosure by era, by cluster, or by claim tier** beats disclosure by
  degree. Degree is a proxy for importance; there may be a better one in this data.
- Whether the map should open **focused on something** — the custody chain, the witness
  chain, the current era — rather than on everything at reduced density.
- The four thresholds are `let` bindings (`PLATE_DEGREE`, `LABEL_DEGREE`, `EDGE_MIN_DEG`,
  `NODE_MIN_DEG`) and are trivially exposable as controls. **Is a density control the right
  answer, or an admission that the default is wrong?**

### 3.2 The eight classes need a visual system

Five classes had five shapes. Eight need a system rather than three more shapes bolted on —
especially since `document` and `event` are now frequently the most connected nodes.

### 3.3 Twelve edge types, each with a claim tier

An edge must currently communicate: type (12), strength (1–5), claim tier (1–3), and whether
it is derived or hand-written. That is four variables in colour, dash, width and glow. It is
over-subscribed. **Which of these actually needs to be visible at rest, and which only on
selection or hover?**

The one rule that cannot be dropped: **derived and hand-written edges must stay
distinguishable.** That separation is what stops the map inventing a relationship, and it is
credibility rule 4 in the parent design system.

### 3.4 The timeline should make its argument visible

Four strands, 857 entries, 82 years, vertical. The 79-year gap between THE PROGRAM starting
and OVERSIGHT arriving is the strongest structural claim on the board and the layout
currently leaves the reader to notice it. It also needs virtualisation.

### 3.5 Analysis and Report

ANALYSIS has four correct computed cards and then parent-board furniture underneath.
REPORT has had no review against this data at all. Both are open.

---

## 4. Constraints — these are not negotiable

1. **The build is a patch pipeline.** Divergence from the parent board lives in
   `tools/build_dashboard.py` as named patches that fail loudly by name. Any design change
   must be expressible as patches against `the-vanishing-v2.html`, or it breaks the ability
   to pull the parent board's updates. **If a change cannot be a patch, say so explicitly** —
   that is a real cost and a decision for Stewart, not a detail.
2. **The seven credibility rules in DESIGN-SYSTEM.md §8 all hold.** In particular: no claim
   renders without a confidence treatment; unsourced entities say so; derived connections
   stay separated from editorial ones; absent values print as absent, never as zero.
3. **The COVER-UP view keeps the structural role §8.2 gave counterarguments** — top-level,
   same card grammar, same density. It is filled with denials rather than skeptics because
   of the editorial stance, but it must never read as an appendix.
4. **The command surface stays complete.** Every control must be reachable from `CMD`, or
   the "operate the whole app from the chat input" requirement breaks. A new control means a
   new `CMD` action.
5. **The analyst's no-API-key state is first-class**, not an error.
6. **Single self-contained file, opened by double-click, no server.**
7. There are **no photographs** on this board. Person plates are 100px throughout. Do not
   design a portrait slot.

---

## 5. What to deliver

Same shape as the v2 brief that produced the current board:

1. A written argument for the density model, with the reasoning visible.
2. A revised network map specification: node system for eight classes, edge system for
   twelve types with tiers, and the disclosure model.
3. A revised timeline specification that makes the 79-year gap structural.
4. Whatever ANALYSIS and REPORT should be.
5. A list of the changes that **cannot** be expressed as patches against the parent board,
   with the cost stated plainly.

Prototype in a standalone file against the real data — `data/the-program.json` is the whole
board as JSON, and it is what `tools/build_dashboard.py` consumes.

---

## 6. Creative direction

### Mood
Unchanged. The board is a research instrument that a hostile reader is going to attack. It
should look like an intelligence product, not a conspiracy wall — the phosphor terminal
language, the density, the dot-leaders and the refusal to round anything off are all doing
credibility work.

### The one thing to hold on to
Every claim on this board carries a tier, and 59% of 4,037 claims rest on a primary record.
That number is the product. **The design's job is to make it impossible to read the board
without knowing which parts are documented and which are testimony** — not to make the
testimony look more documented than it is. The tiers are ammunition grading, not hedging:
Tier 1 is what survives a hostile audit, Tier 3 is where the research goes next.

A design that makes the board look more certain than its sourcing would be a failure, even
if it looked better.
