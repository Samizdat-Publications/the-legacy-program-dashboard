# The patents tab, as a mockup and not as a build

**29 August 2026.** `CLAUDE.md` §9 says the analyst/dossier dock swap must not be built
without a mockup at 1366 / 1920 / 2560 shown to Stewart first, "because the last three layout
changes built directly were all wrong on the first cut". The patents tab is the same class of
change and gets the same treatment. **Nothing in `tools/l0_patches.py` was touched.**

**Canvas:** https://claude.ai/code/artifact/55c66b23-1605-4d6c-a8c8-b17db470c400

Working sources are in `notes/design-2026-08-29-patents-tab/` so the canvas can be re-seeded
without going back to the artifact: three `.dc.html` artboards, `canvas.json`, and a 1:1 PNG
of each. Re-seed with the `design` skill's `seed-canvas.mjs`.

---

## 1. It matches the shell rather than approximating it

Every value is lifted from `tools/l0_patches.py`, not eyeballed:

| | value | source |
|---|---|---|
| typeface | IBM Plex Mono 400/500/600 | shipped inline in the built page |
| chip | 22px high, `0 8px`, `500 9px/1`, `.10em`, uppercase | `.l0chip` |
| button | 25px high, `0 11px`, `500 8.5px`, `.13em` | `.l0ctl`, `.l0selbar button` |
| head strip | `left/right 12px`, `top 10px`, `gap 12px` | `.l0head` |
| selection bar | 44px | `.l0selbar` |
| register width | 396px | `.l0reg` |
| panel / chip / ledger grounds | `#12171d` · `#141920` · `#11141a` | throughout |
| borders | `#262e36` · `#1d242b` · `#22282f` · `#3a2f1c` | throughout |
| text ramp | `#e6e9ee` · `#b9c2cd` · `#8d97a4` · `#5c6672` | throughout |
| accent / legend / denial | `#5ed4e6` · `#efb555` · `#e8705f` | throughout |

## 2. The three widths are three layouts, not one layout scaled

| width | what it does |
|---|---|
| **1366** | The control row **wraps to two lines** — measured at 149px on the live board, and the mockup shows it wrapping rather than pretending it does not. The file-wrapper rail folds to a **30px spine**, reusing `#dock.dock-spine` exactly: rotated label, one click to restore. Quotes drop from four to two and the observables mapping collapses to a chip strip. |
| **1920** | Two columns. Filings across the top at one size, the two prosecution lanes on a shared axis, three pull quotes, the observables mapping as a two-column table, and the rail at 396px. |
| **2560** | The control row fits on one line (25px measured), so the extra height goes to content: a fourth pull quote (the China refusal), examiner and art unit on every filing card, the PAX 182 papers listed under the PAX 205 ones, and the drawings promoted out of the rail into a full-width six-up strip. |

## 3. What the tab actually argues

Not "here are five patents". The tab is built around the comparison, because that is the
strongest thing the cluster has:

- **Two prosecution lanes on one time axis.** PAX 182 runs clean — one rejection, allowed on
  prior art. PAX 205 runs contested — two rejections, a Sheehy letter, an appeal, and a grant
  whose reason is not in the file. Read together they are the finding.
- **Four pull quotes, and three of them are the examiner's.** Including the China refusal,
  which contradicts the account in circulation, and the 11 July "math and physics are sound …
  still not enabled".
- **The absent documents are drawn, not omitted.** The Reasons for Allowance appears as a
  struck row marked NOT OBTAINED, with the reason underneath. That follows the board's own
  `absent prints as absent` rule, which already has a gate check behind it. A reader should be
  able to see that the decisive document is missing rather than assume the record is complete.
- **The five observables sit on this tab, capped at Tier 2**, with the four-of-five mapping and
  the recorded gap printed next to it. Four out of five, never five.

## 4. It was looked at, not just built

Each artboard was rendered standalone at true 1:1 through Playwright and opened as a PNG, at
1366×768, 1920×1080 and 2560×1440. Three defects were found that way and fixed:

| found | fix |
|---|---|
| Quote boxes and rail cards stretched with `flex:1 1 auto`, leaving 300–500px of dead space at every width | the stretching panels now size to content; the space went to the observables mapping and the maintenance-fee finding, which are content rather than padding |
| At 2560 the observables card still left a band empty | drawings promoted out of the rail to a full-width six-up strip |
| Drawing captions ran together — `<br>` between a text node and a `<span>` inside a flex container did not break | captions wrapped in an explicit block |

Overflow was checked programmatically at all three widths: `scrollWidth`/`scrollHeight` equal
the frame exactly, so nothing clips or scrolls.

**The honest limit**, same one `CLAUDE.md` §3 records for `look.js`: these are three states,
not every state. Nothing here has been through a real browser at a real DPI on Stewart's
monitor, and the smallest labels (8px, `.13em`) should be judged there rather than from a PNG.

## 5. What is being asked

Four questions, in the order they change the build:

1. **Is the tab the right shape at all?** It leads with the comparison rather than with the
   five filings. That is a claim about what matters, and it is Stewart's call.
2. **Does the spine fold at 1366 read as deliberate?** It is the pattern the dossier already
   uses, but it is being applied to a second surface for the first time.
3. **Should the observables live on this tab?** They are a frame, not a patent. They earn the
   space through the mapping, but the tab is called PATENTS.
4. **Drawings: thumbnails or not at all?** They are drawn as labelled frames here. Putting real
   line art on a dark ground needs a treatment decision that has not been made.
