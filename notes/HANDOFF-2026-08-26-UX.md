# HANDOFF — the shell is the problem now, not the data

**26 August 2026, end of session.** The data work is done and gated. What is left is that
**the board is hard to use**, reported by Stewart from the live site. Read this before
touching anything; the diagnoses below are from the code and are precise, not guesses.

---

## 1. Stewart's report, verbatim in substance

> "I choose something from the start menu and menus overlap, the right bar expands to half
> the screen, you never actually get to see the full map. Even clicking fit leads to the view
> where it just uses the numbers, which I want to save for only super zoomed out. I need fit
> to display the full map… nobody ever gets to see the map in its normal form and it's
> central to it, as it shows how robust our connections are."

He is right on every point. **The map is the argument and almost no reader will ever see it.**

---

## 2. Root causes, located

### A. FIT shows numbers because ONE CONSTANT DOES TWO JOBS

`tools/l0_patches.py:253`

```js
const L0_LABEL_DROP = 0.62;      /* inherited LOD rule, unchanged */
```

`dense()` is `view.k < L0_LABEL_DROP`. So the same number decides **"stop drawing labels"**
AND **"collapse every chip into a cell count"**. Measured fit scales:

| window | fit | what happens |
|---|---|---|
| 1366 | 0.222 | cells — correct, chips would be unreadable |
| 1600 | 0.452 | cells — **wrong, chips would be fine** |
| 1920 | 0.608 | cells — **wrong by 0.012** |
| 2560 | 0.920 | chips + labels — correct |

**The fix is to split the constant**, not to tune it:

```js
const L0_LABEL_DROP = 0.62;   // labels off below this
const L0_CELL_MODE  = 0.30;   // collapse to counts only below THIS
```

`dense()` becomes `view.k < L0_CELL_MODE`. Then FIT at 1600 and 1920 draws **the real map,
unlabelled** — chips, rules, edges, the whole lattice — which is what Stewart is asking for,
and the count matrix is reserved for a deliberate deep zoom-out as he wants.

**Every check that assumes one threshold must be re-read**, not just re-run: the canvas
suite has `overview-is-never-anonymous`, `overview-draws-no-orphan-edges`,
`the edge layer is switched off below the label threshold`, `axis-type-readable-at-every-scale`
and `selection-survives-cell-mode`, and several of them drive `v.k = 0.45` explicitly to reach
dense mode. At 0.45 that is no longer dense. **They will pass while testing nothing.** Point
them at `L0_CELL_MODE` (e.g. 0.25) rather than at a literal.

### B. The dossier takes half the window

`tools/l0_patches.py:2568`

```js
const wide = Math.max(560, Math.round(window.innerWidth * 0.5));
```

At 1920 that is 960px of dock. With the ~200px left rail the map gets **~760px of 1920, under
40%**. The AUTO re-fit built today then correctly re-fits into that, so the map is *whole* but
*tiny* — 0.29× — which reads as broken.

### C. Selecting a node zooms IN

`tools/l0_patches.py:2004`

```js
view.k = Math.max(view.k, 1.15);
```

`focus()` forces at least 1.15×. So the START HERE flow — the front door — takes a reader who
has never seen the board and drops them **inside** it at 1.15× with the dossier open. Stewart:
*"when I click a starting point I want it to select the relevant cells but then fit to screen."*
He is describing CEDE, which is built, but `focus()` runs instead of it.

### D. Popovers overlap the chrome

Visible in his screenshot: the node popover (`.l0panel`) sits over the crumb and the era heads.
It is `position:absolute` inside `.l0wrap` with no awareness of the head strip that `PAD.t`
now measures. It should clear `PAD.t` the same way the era labels do.

---

## 3. Stewart's proposal, and it is a good one

> "I wonder if we don't swap it out with analyst, so analyst stays on the right panel and the
> stuff currently on the right panel could be where the analyst is now, since it takes up the
> entire bottom of the screen."

**Recommend doing this.** The reasoning is not just space:

| surface | shape it wants | why |
|---|---|---|
| **dossier** | wide and short | long prose, claim rows, connection tables. Reads badly in a 960px column and well in a full-width strip |
| **analyst** | narrow and tall | a chat transcript. Reads well in a column; the current full-width bottom strip wastes most of its width on line-length nobody wants |

The swap gives the map back its width **and** puts each surface in the shape it actually
wants. The dock is already a grid column (`grid-template-columns: var(--rail-w) minmax(0,1fr)
var(--dock-w)`), so this is a shell change in `ref/the-vanishing-v2.html` plus the patches that
target `#dock`.

**Do not start this without a mockup.** Build it as a `.dc.html` artboard or a throwaway HTML
first, screenshot it at 1366 / 1920 / 2560, and put it in front of Stewart. The last three
layout changes that were built directly were all wrong on the first cut.

---

## 4. Priority order for the next session

1. **Split `L0_LABEL_DROP`.** Smallest change, biggest effect, and it alone answers "fit should
   show the map". Re-aim the five affected checks at the new constant.
2. **Stop `focus()` zooming to 1.15 from the entry surface.** A START HERE pick should CEDE:
   fold the panels, fit, outline the target. `showOnMap()` already does exactly this.
3. **Mock the analyst/dossier swap, screenshot it, show Stewart.** Then build.
4. **Make the popover clear `PAD.t`.**
5. Re-deploy and have Stewart look, because none of this is provable from here.

---

## 5. The tooling question

Stewart asked what would let a session *"click everything, see how it looks, write notes"*.

**Nothing needs downloading. Playwright and Chromium are already installed** — that is what
`tools/look.js`, `tools/runtime_check.js` and `tools/test_packed_layout.js` use. What is
missing is not a tool, it is a **harness**:

**Build `tools/walk.js`** — an exploratory crawler, a camera not a check, the same contract as
`look.js`:

- enumerate every clickable control (`[data-view]`, `.l0ctl button`, `.l0selbar button`,
  `[data-opt]`, `[data-flag]`, legend rows, chips on the canvas)
- click each one, screenshot the result into `dist/shots/walk/NN-<label>.png`
- after every click, record: console errors, **overlap of any two interactive rects**, any
  element whose text is clipped, the map scale, and how much of the window the map has
- write `dist/shots/walk/REPORT.md` — a table of state → what changed → what looks wrong

The overlap and occupancy checks are the ones that catch what Stewart sees. Today's
`the breadcrumb never prints on the map controls` proves the technique works; `walk.js` would
apply it to **every** state rather than the one state a check happens to look at.

Two things worth adding later, neither required:
- **axe-core** (`npm i -D axe-core`) — injectable, gives contrast and label findings.
- A **visual diff** baseline, so a change that moves pixels nobody asked to move is reported.

**And the honest limit, unchanged:** a screenshot is one state, and captures are at
`deviceScaleFactor: 2`, so small text reads larger than on a 1x monitor. `walk.js` widens the
coverage; it does not replace Stewart looking.

---

## 6. State at this checkpoint

Everything below is done, gated and pushed on `claude/claud-md-compacting-vs9o9j` (PR #5).

| | |
|---|---|
| gate | 46 verify · 40 audit · 28 runtime · 26 canvas, every poison biting, `--idempotent` green |
| denials | all 174 adjudicated: 124 directed, 36 association, 14 undirected. `data/denial-adjudication.json` |
| chip labels | all 46 overlong ones authored. `data/l0-shorts.json`. 0 of 110 over 37 chars |
| images | 9 of 39 institutions. `data/l0-images.json` + `assets/marks/`. Inlined as data URIs |
| backfill queue | down to **one** row (images) from nine |
| typeface | embedded; the page fetches nothing at runtime |
| live | https://the-program-zxz.pages.dev — **needs a redeploy to show today's work** |

Notes worth reading in this order: `FIRST-PAINT-2026-08-26.md`, `SHELL-FIT-2026-08-26.md`,
`DENIAL-ADJUDICATION-2026-08-26.md`, `IMAGE-SOURCING-2026-08-26.md`,
`DATE-EXTENT-2026-08-26.md`, `BACKFILL-QUEUE-2026-08-26.md`.
