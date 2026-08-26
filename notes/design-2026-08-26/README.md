# Handoff — shell: fit, focus, occlusion

**26 August 2026.** Design response to `notes/HANDOFF-2026-08-26-packed.md` and to Stewart's
three asks: a fit button, a board that fits on entry, and something for SHOW ON MAP to do
when the panels cover the map.

## What is in here

| file | what it is |
|---|---|
| `Shell Fit and Focus.dc.html` | the working study. Open it in a browser — no build, no server. |
| `support.js` | runtime the study needs. Keep it beside the HTML. |
| `data/l0-layout-model.js` | the layout model it reads (`window.L0_LAYOUT_MODEL`, `current` dataset). Unmodified. |
| `DESIGN-RESPONSE-SHELL-2026-08-26.md` | the written decisions, including the answers to the two open items in §1 of your handoff. |

Try, in this order: press FIT ALL and FIT ROOM with nothing selected (identical), click a
chip, then press SHOW ON MAP with each of CEDE / PORTHOLE / TETHER selected in the bottom
bar. Drag and wheel to see AUTO flip to HELD.

## What to port, in priority order

**1. Measure, then fit.** Every fit must run against a measured rect, never a default. This
was the study's own first bug and it presented exactly as "the map never fits": the geometry
was correct, the box it fitted into was imaginary. Measure on mount (rAF after the ref lands),
keep a ResizeObserver, and add a window-resize fallback. Same discipline as `clampView()` in
your build — every path that can change the box calls the one function.

**2. Two fit buttons that print their own scale.** FIT ROOM fits into what is left after the
panels; FIT ALL fits into the whole canvas and lets the panels cover the overlap. Printing
both scales (`0.30×` / `0.34×`) makes the cost of an open dossier a number rather than a
feeling. With nothing open they read the same, which is the point.

**3. Auto-fit on entry, released by the first gesture.** `AUTO · REFITS ON ANY PANEL MOVE`
until the first drag, wheel or pick, then `HELD · PRESS FIT TO RE-ARM`. Never move the camera
under a hand that is already moving it. Entry is the whole board; the 14 start-here flags stay
an offer inside a board the reader has already seen whole.

**4. SHOW ON MAP does one of three things.** CEDE (panels fold to labelled spines, map re-fits
to the room it gains, target outlined), PORTHOLE (layout holds, board dims except a lens on
the target), TETHER (camera only, hairline from dossier to chip). Ship CEDE as the default and
keep the choice a preference, not a mode. A folded panel keeps its label and one click
restores it.

**5. Chrome in screen space.** Band labels and era heads hold one type size at every zoom;
only cells and chips scale. This is the reason a 0.30× fit is still readable, and it extends
the frozen-gutter argument already in your build to the label sizes.

**6. The selection survives cell mode.** When the fit drops below chip legibility, the cell
holding the selection takes the amber outline and its numeral turns amber. Before that, a fit
silently lost the selected node.

**7. Small things that bite.** The selection bar carries SHOW ON MAP and CLEAR, so inset it by
the panel width and put it above both the dossier and the dim. Rest edges do not draw in cell
mode — with no chips to land on they are orphan lines across the grid; only the selection's
own links draw.

## Numbers used

Panels: dossier 392, spine 30, rail 176 / 30 collapsed, selection bar 44. Reserved chrome:
top strip 30, left gutter 118. Cell mode below `k × 205 < 84px` of chip width. Camera eases
`1-(1-t)³`, 460ms for a fit, 520ms for CEDE, 300ms for a panel.

## Not verified

`dist/the-program.html` is not in this project, so §1's "open it and say what is wrong" is
answered from the layout model and a screenshot of the live board, not from the built
artifact. Everything above was rendered and driven through at several window sizes.
