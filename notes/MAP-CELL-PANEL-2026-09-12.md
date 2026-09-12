# The open cell's panel, judged, 12 September 2026

`notes/HANDOFF-2026-09-04.md` section 3 item 3 left this for a human:

> `walk.js` reports 32 overlaps on `#/map?cell=oversight.3`, the open cell's rows
> over the neighbouring cell, for a human to judge.

Judged. At 1366 it is 49 overlaps, not 32. Screenshots:
`dist/shots/walk1366/07-map-cell.png` and `dist/shots/map-cell-1920.png`.

## What is actually happening

Opening a cell draws `.cell-panel`, a floating dialog listing that cell's members
with a start year, sorted by date, with an ESC close. It is positioned near the
cell and it lands on top of whichever cell is above and to the left. The 49
"overlaps" are its `a.cell-row` links sitting over other cells' chips. Nothing is
broken and nothing is mispositioned: it is a popover, it has a border, a title
and a close control, and it reads as deliberate on screen.

**The judgement is not about the overlap. It is about what the panel adds, and
that differs by mode.**

| | what the grid already shows | what the panel adds | verdict |
|---|---|---|---|
| **1366, cell mode** | the cell collapsed to "13 nodes · click to expand". No member names at all | every member, its class mark and its start year | **It earns its place.** It is the only way to see who is in the cell |
| **1920, label mode** | all 13 members drawn as labelled chips, in the cell, already readable | the same 13 names again, plus a start year each and a date sort | **Marginal.** It repeats what is on screen, and covers a neighbouring cell to do it |

At 1920 the panel for `oversight.3` covers the research band's 2017-2026 cell,
hiding "Sec. 6802, FY2023 NDAA" and "Wayne State University" among others. A
reader who opens a cell to look at it loses sight of a different one.

## What I would change, and why it is not changed here

In label mode, opening a cell could focus that cell's chips rather than opening a
panel that repeats them over a neighbour: the year and the date order are the
only things the panel adds there, and both could go on the chips or in the strip.
In cell mode the panel should stay exactly as it is.

Not changed, for the reason `CLAUDE.md` section 4 gives: **the map is Design's**,
the packed layout was built to their spec with 31 canvas assertions behind it,
and a change to how opening a cell behaves is a change to their interaction
model, not a defect fix. It also needs a mockup at 1366 and 1920 before it is
built, because the last three layout changes built directly were all wrong on the
first cut.

## What is NOT worth chasing

The overlap count itself. `walk.js` says plainly that an overlap may be a
deliberate stack, and this one is. A future session should not spend time driving
the number to zero: the number is a symptom of a popover existing, and the
question is whether the popover should exist in label mode, which is the table
above.
