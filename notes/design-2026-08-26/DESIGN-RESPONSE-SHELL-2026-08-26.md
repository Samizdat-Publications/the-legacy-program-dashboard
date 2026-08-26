# Design response — the shell: fit, focus, occlusion

**26 August 2026.** Answers Stewart's three asks (a fit button, a board that fits on entry,
and what SHOW ON MAP should do when the panels cover the board) and the two open items in
`notes/HANDOFF-2026-08-26-packed.md` §1.

Working reference: `Shell Fit and Focus.dc.html`. Geometry from `data/l0-layout-model.json`.

---

## 1. Fit is two buttons, and both print their scale

FIT ROOM fits the board into what is left of the canvas once the panels have taken theirs.
FIT ALL fits it into the whole canvas and lets the panels cover the overlap. Both print the
scale they would produce — `0.35×` and `0.37×` — so the cost of the open dossier is a number
on screen rather than a feeling. With no panels open the two numbers are identical, which is
the point: the difference *is* the occlusion.

## 2. The board fits on entry, and the first gesture releases it

On load and on every resize the map re-fits. The chip beside the buttons reads
`AUTO · REFITS ON ANY PANEL MOVE`. The first drag, wheel or pick flips it to
`HELD · PRESS FIT TO RE-ARM`. Nothing auto-moves the camera under a hand that is already
moving it, and a user who wants the whole thing back has one labelled way to get it.

Entry is therefore "here is all of it", not "here is where we think you should start". The
14 start-here flags stay available, but as an offer inside a board you have already seen
whole.

## 3. SHOW ON MAP — three choreographies, all in the study

| | what moves | best for |
|---|---|---|
| **CEDE** | panels fold to labelled spines, map re-fits to the room it just gained, target arrives outlined | a first look at where a node sits |
| **PORTHOLE** | nothing but light — layout holds, board dims except a lens on the target | keeping a paragraph and its node on screen together |
| **TETHER** | camera only — target panned into the open slot, hairline from dossier to chip | scanning several nodes in a row |

Recommended default: **CEDE**, with the choreography a preference rather than a mode. The
folded panel keeps its label and one click restores it, so ceding space costs nothing that
cannot be undone.

## 4. Two things the study fixes that are not about fit

**Chrome is drawn in screen space.** Band labels and era heads keep one type size at every
zoom; only the cells and chips scale. This is why a 0.30× fit is still readable, and it is
the same argument as the frozen gutter in the shipped build — extended to the label sizes.

**The selection survives cell mode.** A fit that drops below chip legibility used to lose the
selected node entirely. The cell it lives in now carries the amber outline and the numeral
turns amber, so "your node is in here, with 12 others" is still on screen.

---

## 5. On labels truncating at ~37 characters

Not a layout fault, and more characters is the wrong fix. A 205px chip at 1.0× holds about 37
monospace characters, and widening the chip costs a column.

- Keep the **middle cut**. `Sec. 6802, James M. Inhofe NDAA for FY2023 (Pub. L. 117-263)`
  must lose the honorific, never the citation. The 62/38 head/tail split does that.
- The chip label is an **index entry**, not a title. The test is "can I tell which node this
  is", not "can I read it". The dossier carries the full string, always untruncated.
- The remaining work is content: **author `short` per node at ≤37 characters.** 46 of 110
  exceed it today and are being cut by an algorithm that cannot know which half matters. That
  is one editorial pass, not a design change.

## 6. On the disclosure band holding 3 nodes

Keep the band. Do not merge it, do not pad it. But make thinness *legible*: every band name
prints its count, and under five it prints amber. `DISCLOSURE · 3 nodes` in amber is an
argument — the board is saying the record is thin here. `DISCLOSURE` alone next to a nearly
empty row is just a layout that looks broken.

## 7. What I did and did not verify

Rendered: the shell study above, at several sizes, with the three choreographies driven
through. Not rendered: `dist/the-program.html` — the built dashboard is not in this project,
so I cannot answer §1's "open it and say what is wrong" from the artifact itself. Everything
here is derived from the layout model and from the screenshot Stewart sent of the live board.
