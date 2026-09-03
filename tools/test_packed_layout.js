/* The packed-cell layout, checked by reading the pixels it actually drew.
 *
 * WHY THIS EXISTS
 * ---------------
 * notes/PACKED-LAYOUT-COST-2026-08-25.md said a cloud session could not verify
 * this work, and gave a table of properties with "nothing here" in the second
 * column: chips overlapping, a band clipping, labels unreadable at the opening
 * fit, the map opening on empty space. The reason given was that mountL0 draws to
 * a canvas and tools/runtime_check.js reads the DOM.
 *
 * That reason was half right. runtime_check.js cannot read a canvas because it
 * asserts through text nodes. But getImageData can, in the same headless browser,
 * and the packed layout is the one surface where that is worth the trouble --
 * every chip's position is stated in data/l0-layout-model.json, so the drawn
 * pixels can be compared against an independent statement of where they belong
 * rather than against the renderer's own opinion.
 *
 * So this file does the thing the note said could not be done, for the properties
 * where it can be done, and says plainly which ones remain out of reach:
 *
 *   caught here      chips drawn at the model's coordinates, in the model's class
 *                    colours; no chip overlapping another on screen; the opening
 *                    view landing on chips rather than on empty world; the row and
 *                    column labels surviving a pan; the edge budget at rest; all
 *                    three options on; the canvas carrying ink at all
 *   NOT caught here  whether a truncated label is still a useful label, and
 *                    whether the whole thing looks good. Those need eyes.
 *
 * Every check below has a poison in --self-test, because CLAUDE.md section 5 is
 * about this exact file's ancestor: `canvasInk` reported zero ink on a visibly
 * drawing canvas and had never once fired.
 *
 * Run it:
 *   npx http-server dist -p 8899 --silent &   # or the container copy under /opt/node22
 *   node tools/test_packed_layout.js
 *   node tools/test_packed_layout.js --self-test
 */
const { requirePlaywright, launchOptions } = require('./browser_env');
const { chromium } = requirePlaywright();
const fs = require('fs');
const zlib = require('zlib');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const URL = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';
const SELFTEST = process.argv.includes('--self-test');

/* ---- the assertions, as data ------------------------------------------------
 * Each one is a pure function of a probe taken from the page, so the SAME
 * function runs against the real probe and against a poisoned one. A check that
 * is only ever fed good input is the failure mode this repo keeps hitting; here
 * there is no second code path for it to hide in. */
const CHECKS = [
  {
    id: 'mounted',
    label: 'the program map mounts as the packed grid',
    test: p => p.hasCanvas && p.packedNodes === p.l0Nodes && p.l0Nodes > 0,
    detail: p => `canvas=${p.hasCanvas} packed=${p.packedNodes} l0=${p.l0Nodes}`,
    poison: p => ({ ...p, packedNodes: p.packedNodes - 1 }),
  },
  {
    id: 'geometry',
    label: 'every node carries a chip rect from the model',
    test: p => p.withRect === p.l0Nodes && p.distinctSizes === 1,
    detail: p => `${p.withRect}/${p.l0Nodes} with x,y,w,h · ${p.distinctSizes} chip size(s)`,
    /* Two sizes is the poison, not zero: size must never encode importance, and
       the way that rule breaks is one node quietly getting a bigger plate. */
    poison: p => ({ ...p, distinctSizes: 2 }),
  },
  {
    id: 'no-overlap',
    label: 'no chip overlaps another on screen',
    test: p => p.overlaps === 0,
    detail: p => `${p.overlaps} overlapping pairs of ${p.onScreen} on screen`,
    poison: p => ({ ...p, overlaps: 1 }),
  },
  {
    id: 'ink',
    label: 'the canvas is drawn on',
    /* An upper bound as well as a lower one. Zero ink is the historic bug; a
       canvas that is 100% ink is the other way to pass a naive version of this
       check, and it is what a single fillRect over the whole surface looks like. */
    test: p => p.inkPct >= 2 && p.inkPct <= 80,
    detail: p => `${p.inkPct}% of sampled pixels are content rather than ground`,
    poison: p => ({ ...p, inkPct: 0 }),
  },
  {
    id: 'chips-where-the-model-says',
    label: 'chips are drawn at the model coordinates, in their class colours',
    /* The load-bearing one. For each on-screen chip it samples the class rule at
       the chip's own left edge and asks whether that pixel is nearer the node's
       class colour than the chip fill. Shift the layout by a chip width and these
       samples land on band fill instead, so the count collapses. */
    test: p => p.classHits === p.classProbes && p.classUnprobed === 0
               && p.classProbes === p.l0Nodes,
    detail: p => `${p.classHits}/${p.classProbes} probes matched their class colour`
               + ` · ${p.classUnprobed} node(s) never reached by the camera`
               + (p.classMiss.length ? ' · missed ' + p.classMiss.slice(0, 6).join(' ') : ''),
    poison: p => ({ ...p, classHits: p.classProbes - 1 }),
  },
  {
    id: 'opens-on-content',
    label: 'the map opens on chips, not on empty world',
    test: p => p.openingChips >= 20 && p.labelsLegible,
    detail: p => `${p.openingChips} chips in the opening view · k=${p.k} · labels ${p.labelsLegible ? 'drawn' : 'DROPPED'}`,
    poison: p => ({ ...p, openingChips: 0 }),
  },
  {
    id: 'furniture-pinned',
    label: 'row and column labels survive a pan to the far corner',
    /* The rows are ordered by measured mean C and that order IS the argument, so
       a band label that scrolls away takes the argument with it. Panned to the
       bottom-right of a 2200x912 world, the gutter and head row must still carry
       ink -- which they only do because they are pinned to the viewport. */
    test: p => p.gutterInkPanned && p.headInkPanned,
    detail: p => `gutter=${p.gutterInkPanned} headRow=${p.headInkPanned} after pan`,
    poison: p => ({ ...p, gutterInkPanned: false }),
  },
  {
    id: 'edge-budget',
    label: 'the edges drawn at rest are the ones the model budgeted',
    test: p => p.restCount === p.restDrawnFigure && p.restCount < p.allEdges,
    detail: p => `${p.restCount} at rest vs figures.restDrawn ${p.restDrawnFigure}, of ${p.allEdges}`,
    poison: p => ({ ...p, restCount: p.allEdges }),
  },
  {
    id: 'options-on',
    label: 'the view options ship in the state Stewart signed off, each with a control',
    /* Stewart's call, 25 August 2026, having looked at the comp with all three
       on. If a later change flips a default this says so rather than letting the
       board quietly ship a different reading surface than the one signed off. */
    /* Four controls, three lit. CELLS is the fourth and it must ship OFF: it is the
       count matrix, and the whole point of 27 August is that nothing puts a reader
       there without asking. A default flip here is exactly the silent regression
       this check exists to catch. */
    test: p => p.optRest && p.optFlags && p.optLabels && p.optCells === false
               && p.optControls === 4 && p.controlsOn === 3,
    detail: p => `rest=${p.optRest} flags=${p.optFlags} labels=${p.optLabels}`
               + ` cells=${p.optCells}`
               + ` · ${p.controlsOn}/${p.optControls} controls lit`,
    poison: p => ({ ...p, optCells: true }),
  },
  {
    id: 'no-fit-lands-in-cells',
    label: 'no fit at any window size lands the reader in the count matrix',
    /* THE 27 AUGUST REGRESSION, NAILED DOWN. dense() was `view.k < 0.62` and every
       fit at a normal window lands below it, so FIT and FIT ALL both handed the
       reader a grid of numerals instead of the map. Stewart hit it on the live
       deploy twice.

       Splitting the constant would not have been enough and that is why this check
       sweeps WIDTHS rather than asserting one threshold: at 1366 the fit is 0.222,
       so a 0.30 cell-mode threshold still ambushes a laptop while looking fixed on
       a 2560 monitor. Eight states -- FIT and FIT ALL at four widths -- and cell
       mode must be off in all eight.

       `cellInkRatio` is the pixel half: bright ink at the centre of occupied cells,
       which is what a printed count looks like and what a chip row does not. The
       self-test forces cell mode on the real page and requires it to rise, so this
       is a measure demonstrated to tell the two modes apart rather than a number
       that happens to be small. */
    test: p => p.fitCellModes.length === 8
               && p.fitCellModes.every(m => m === false)
               && p.fitChipInk === true,
    detail: p => `${p.fitCellModes.filter(m => m === false).length}/8 fits drew chips`
               + ` · win ${(p.fitWinW||[]).join('/')}`
               + ` · host ${(p.fitHostW||[]).join('/')}`
               + ` · scales ${p.fitScales.map(x => x.toFixed(2)).join(' ')}`
               + ` · class-ink chips ${p.cellInkChips} vs cells ${p.cellInkCells}`,
    poison: p => ({ ...p, fitCellModes: p.fitCellModes.map((m, i) => i === 3 ? true : m) }),
  },
  {
    id: 'pointers-offset',
    label: 'start-here pointers are drawn beside chips, never on them',
    /* The flags must stay a separate layer. The moment the flag becomes a
       property of the chip it can be read as a tier, and AARO gets promoted by
       being pointed at. Probing the gutter strip to the LEFT of each flagged chip
       is how that separation is held to. */
    test: p => p.flagHits === p.flagProbes && p.flagProbes >= 3,
    detail: p => `${p.flagHits}/${p.flagProbes} flagged chips have amber ink offset to their left`
               + (p.flagMiss.length ? ' · no pointer on ' + p.flagMiss.join(' ') : ''),
    poison: p => ({ ...p, flagHits: 0 }),
  },
  {
    id: 'motion-only-where-attested',
    label: 'at rest only attested denials move, and a selection moves its own edges',
    /* THE ASSERTION CHANGED ON 27 AUGUST AND THE OLD ONE WAS A PROXY.
       It read `stillFrames === 1` -- nothing moves at rest at all. That was a
       correct proxy for exactly as long as the board had no directed denial: the
       renderer's own comment said "none yet, so none draw". The adjudication then
       landed 174 verdicts and 38 directed denials, and Design's rule is not
       "nothing moves at rest" but "a path carries a particle only if it is a
       denial or belongs to the selected node". Motion at rest became CORRECT, and
       a proxy that cannot tell correct motion from the flow-on-every-line
       treatment Design rejected is worse than no check.

       So it asserts the real property in three parts: the map moves at rest,
       it goes STILL when every denier is stripped from the page, and a selection
       moves its own edges. The middle one is the load-bearing half -- it is what
       separates "38 attested denials are moving" from "everything is drifting". */
    test: p => p.directedDenials > 0 && p.stillFrames > 1
               && p.stillFramesNoDenial === 1 && p.selectedFrames > 1,
    detail: p => `${p.directedDenials} directed denials · ${p.stillFrames} distinct frame(s)`
               + ` at ${p.attnState} with nothing selected, ${p.stillFramesNoDenial} once every`
               + ` denier is stripped, ${p.selectedFrames} with a node selected`,
    poison: p => ({ ...p, stillFramesNoDenial: 4 }),
  },
  {
    id: 'breath-touches-no-data-channel',
    label: 'the start-here breath never touches the chip stroke, which carries tier',
    /* Two channels on one property is the failure. The bloom must be able to run
       its whole cycle without the tier stroke changing colour once. */
    test: p => p.breathStrokeStates === 1 && p.breathOutlineStates > 1,
    detail: p => `over 7s the chip stroke held ${p.breathStrokeStates} colour(s) while the`
               + ` bloom outside it took ${p.breathOutlineStates}`,
    poison: p => ({ ...p, breathStrokeStates: 3 }),
  },
  {
    id: 'overview-is-never-anonymous',
    label: 'below the label threshold every occupied cell prints its count',
    /* The state this replaces drew 110 rectangles with nothing in them: no
       identity, and it hid the one thing still legible at that size. */
    test: p => p.denseCells > 0 && p.denseCellsWithInk === p.denseCells,
    detail: p => `${p.denseCellsWithInk}/${p.denseCells} occupied cells carry ink at their centre`,
    poison: p => ({ ...p, denseCellsWithInk: p.denseCells - 1 }),
  },
  {
    id: 'overview-draws-no-orphan-edges',
    label: 'the edge layer is switched off below the label threshold',
    /* Lines are anchored to chip coordinates, so with the chips gone they
       terminate at nothing and lattice over the counts the mode exists to show.
       Tested by difference: toggling LINES AT REST cannot change a single pixel
       in dense mode, and must change many at a scale where chips draw. */
    test: p => p.denseEdgeToggleInert === true && p.chipEdgeToggleLive === true,
    detail: p => `toggling LINES AT REST changes nothing in dense mode (${p.denseEdgeToggleInert})`
               + ` and does change the map where chips draw (${p.chipEdgeToggleLive})`,
    poison: p => ({ ...p, denseEdgeToggleInert: false }),
  },
  {
    id: 'denial-marks-follow-the-adjudication',
    label: 'the denial layer is drawn from the adjudication, not from edge order',
    test: p => p.denyDirected > 0 && p.denyMarksOn > 0
               && p.denyMarksAllAssoc < p.denyMarksOn * 0.25,
    detail: p => `${p.denyDirected} directed · ${p.denyUndirected} undirected · `
               + `${p.denyAssoc} association :: ${p.denyMarksOn} denial marks drawn, `
               + `${p.denyMarksAllAssoc} once every edge is told it is an association`,
    /* Poison both halves: a board with no directed denials at all, and a renderer
       that keeps drawing them after the adjudication says not to. */
    poison: p => ({ ...p, denyDirected: 0, denyMarksAllAssoc: p.denyMarksOn }),
  },
  {
    id: 'selection-survives-cell-mode',
    label: 'in cell mode the selected node still says which cell it is in',
    test: p => p.selCellHit === true && p.selCellStray === 0,
    detail: p => `${p.selCellId} · marked in its own cell=${p.selCellHit}`
               + ` · other cells marked=${p.selCellStray} (must be 0)`,
    poison: p => ({ ...p, selCellHit: false, selCellStray: 3 }),
  },
  {
    id: 'thin-bands-print-amber',
    label: 'a band under five nodes says so in amber, and a full one does not',
    /* Until 3 September 2026 the disclosure band held three nodes and this
       required a thin band to exist. The Danny Jones build took it to six, so
       no band on the current data is thin and the amber half cannot be
       exercised on the real page; the detail says so rather than pretending.
       The full-band half still asserts on every band drawn. */
    test: p => (p.thinTotal === 0 || p.thinAmber === p.thinTotal) && p.fullAmber === 0,
    detail: p => (p.thinTotal === 0 ? 'no band under five nodes on this data, amber half unexercised · '
                                    : `${p.thinAmber}/${p.thinTotal} thin bands amber · `)
               + `${p.fullAmber}/${p.fullTotal} full bands amber (must be 0)`
               + ` · ${(p.bandsInfo||[]).map(b => b.id + ':' + b.n).join(' ')}`,
    /* Poison both halves: a thin band that stayed grey (conjured when the data
       has none, so the predicate is still shown rejecting it), and amber
       bleeding onto a band that is not thin. One alone would pass on a gutter
       painted amber from top to bottom. */
    poison: p => ({ ...p, thinTotal: Math.max(1, p.thinTotal),
                    thinAmber: Math.max(1, p.thinTotal) - 1, fullAmber: 1 }),
  },
  {
    id: 'axis-type-readable-at-every-scale',
    label: 'the gutter labels do not scale away with the world',
    /* Axis chrome is drawn at an authored px size positioned at world x scale.
       Counter-scaling by 1/k is the tempting wrong fix: it inflates type against
       containers that stay at model dimensions, so it overflows its own box. */
    test: p => p.denseAxisInkRows >= 5 && p.denseAxisInkRows <= 40,
    detail: p => `the first band label's ink runs ${p.denseAxisInkRows} contiguous pixel rows at k=0.45`,
    poison: p => ({ ...p, denseAxisInkRows: 2 }),
  },
  {
    id: 'labels-truncate-in-the-middle',
    label: 'no chip label is cut off at its end',
    /* An end ellipsis loses the tail, and the tail is the distinguishing token on
       this board: volume numbers, years, Roman numerals, Sec. references. */
    test: p => p.endTrunc === 0 && p.midTrunc > 0,
    detail: p => `${p.fittedLabels} fit whole \u00b7 ${p.midTrunc} middle-truncated \u00b7 `
               + `${p.endTrunc} end-truncated`
               + (p.endTruncEx && p.endTruncEx.length ? ' :: ' + p.endTruncEx.join(' | ') : ''),
    poison: p => ({ ...p, endTrunc: 4 }),
  },
  {
    id: 'head-row-clear',
    label: 'no era column head is painted under the map controls, at any width',
    /* The eras are the horizontal argument exactly as the bands are the vertical
       one, and a head a reader cannot read takes its column's claim with it.

       THIS USED TO BE ARITHMETIC AND THE ARITHMETIC WAS WRONG.
       It compared `geo.headRow - 22 - 9` against the control row's bottom, which
       reproduced neither what the renderer reserved nor where it drew. It passed
       throughout, at one width, on a build that was overprinting: `.l0head` is
       pinned at top:10px and its height h gave a reserve of h + 20 with the label
       drawn at reserve - 22, i.e. 12px above the buttons -- but HEAD_MIN's 76px
       floor dominated whenever the row was a single line and bought accidental
       clearance. Widen the left group with an entry-path chip and open the dossier
       and the row wraps: measured, `.l0head` goes 25px -> 56 -> 87 -> 118 -> 180 ->
       255 as the window narrows. The floor stops dominating and the heads print
       through the buttons. That is the screenshot Stewart sent.

       So it reads PIXELS now, under the buttons' own rects, at four widths, with a
       path open and the dossier out -- the state that wraps hardest. `eraInkPoison`
       is the page-level half: the control row is translated 22px down onto the band
       while the canvas holds still, and the count must rise. 0 against 91 when it
       was written. */
    test: p => p.eraHeads >= 2 && p.eraInkMax === 0 && p.eraInkPoison > 0,
    detail: p => `${p.eraHeads} era heads · era ink under the controls`
               + ` ${(p.eraInkWidths||[]).join('/')} at ${(p.eraInkAt||[]).join('/')}`
               + ` · control row ${(p.eraHeadH||[]).join('/')}px tall`
               + ` · ${p.eraInkPoison} when the row is moved onto the band`,
    poison: p => ({ ...p, eraInkMax: 3 }),
  },
  {
    id: 'gutter-labels-clear-the-rail-tab',
    label: 'no band label is painted under the rail fold tab',
    /* The left-edge sibling of head-row-clear, and it went unnoticed far longer
       because it does not look like a defect. It looks like a shorter word.

       `.rail-fold` is 22px of opaque DOM pinned to the rail's right edge and
       hanging into the map. The band labels were drawn at a hard x=10 inside the
       canvas, underneath it. Measured at 1600x1000 on the build of 29 August:
       RESEARCH rendered as "SEARCH", OVERSIGHT as "ERSIGHT", and both node counts
       were eaten -- "30 nodes . mean C 0.87" read "nodes . mean C 0.87". Only two
       of seven bands, because the tab is 150px tall and centred, which is what
       makes it read as a naming quirk rather than an overlay.

       The label x is measured now, against the tab's real rect, for the reason
       PAD.t is measured: --rail-w changes when the rail folds and the tab rides
       that edge on a curve, so a constant is right in one state and wrong in the
       other. It is also clamped by what the gutter can spare, measured through the
       renderer's own ctx at the fonts bandLabels really uses -- insetting past that
       would trade a covered label for one overflowing into the chip field, which is
       the same defect pointing the other way.

       `gutterInkPoison` is the page-level half, mirroring eraInkPoison exactly: the
       real tab is widened while the canvas holds still, so the labels stay put and
       the tab laps over them. The count must rise. 0 against 132 when it was
       written, with 25px of clearance in the honest state. */
    test: p => p.gutterInk === 0 && p.gutterClear >= 0 && p.gutterInkPoison > 0,
    detail: p => `${p.gutterInk} label px under the ${p.gutterTabW}px tab`
               + ` · ${p.gutterClear}px of clearance`
               + ` · ${p.gutterInkPoison} when the tab is widened onto them`,
    poison: p => ({ ...p, gutterInk: 7 }),
  },
  {
    id: 'overlay-clears-controls',
    label: 'no DOM overlay covers the map controls, at any width',
    /* The sibling of head-row-clear, one layer up. That one guards what the canvas
       paints UNDER the buttons; this guards what the DOM stacks OVER them.

       .l0reg was pinned at `top:44px` while the control row is measured. The
       constant cleared a single-line strip by 9px and nothing else, so it looked
       correct for as long as nobody opened the dossier -- and the dossier is the
       state Stewart was in. Measured with a path open and a node selected, the
       register covered the controls by 22 / 53 / 53 / 84 px at 2560 / 1920 / 1600 /
       1366, from above.

       .l0ledger was never the culprit and the reason is worth keeping: it clamps to
       `PAD.t + 6` in script rather than to a number in a stylesheet. The fix makes
       the register do the same thing by publishing the measured reserve as
       --l0-ctl, so CSS and canvas read one value.

       requiring regOverlapPoison > 0 is what stops this passing on a page where the
       register simply never rendered: -1 is the not-found sentinel and fails both
       halves. */
    test: p => p.regOverlapMax === 0 && p.regOverlapPoison > 0
               && (p.regOverlaps || []).length === 4,
    detail: p => `register vs controls ${(p.regOverlaps||[]).join('/')}px`
               + ` at 1366/1600/1920/2560 · control row ${(p.regHeadH||[]).join('/')}px tall`
               + ` · ${p.regOverlapPoison}px with the old top:44px constant put back`,
    poison: p => ({ ...p, regOverlapMax: 12 }),
  },
  {
    id: 'dossier-measure-capped',
    label: 'the dossier stays a reading measure at every window size',
    /* The dock was `innerWidth * 0.5`, which made the panel wider the bigger the
       monitor got. Measured, the running prose ran 95 / 112 / 135 / 182 characters
       at 1366 / 1600 / 1920 / 2560, against a 45-75 comfortable band and about 90
       as the ceiling for sustained reading. So the widest monitor read worst, and
       the panel was not wide because the prose needed it -- it was wide because a
       proportion was doing a measure's job.

       This is also the measurable half of Stewart's "the right bar expands to half
       the screen, you never actually get to see the full map". Capping the dock at
       640px holds ~89 characters everywhere and returns the map to 40 / 47 / 56 /
       67 percent of the window.

       The floor matters as much as the cap: a dock that collapsed to nothing would
       pass a cap-only check while making the dossier unreadable, so the minimum is
       asserted too. The poison restores half-the-viewport on the live page and
       requires the measure to bust the ceiling. */
    test: p => p.proseCharsMax > 0 && p.proseCharsMax <= 92 && p.proseCharsMin >= 60
               && p.proseCharsPoison > 92,
    detail: p => `${(p.proseChars||[]).join('/')} chars per line`
               + ` at 1366/1600/1920/2560 · ${p.proseCharsPoison} with half-the-viewport put back`,
    poison: p => ({ ...p, proseCharsMax: 135 }),
  },
  {
    id: 'both-drawers-fold-on-a-curve',
    label: 'the rail folds and reopens on a curve, with a tab in both directions',
    /* Stewart, 27 August: "a clickable edge that, when clicked, on a curved motion
       sends the drawer back to its closed position... then I should be able to open
       the closed drawer by clicking it to expand."

       Three things have to hold and only one of them is the animation. The tab must
       exist on the OPEN state (the rail had only a toolbar button, nowhere near the
       edge a reader looks at), the collapsed spine must be clickable back open, and
       the travel between them must be interpolated rather than flipped.

       `display:none` is what the rail did before, and no easing rescues it -- which
       is why the assertion counts distinct widths instead of checking that a
       transition is declared. Measured: 12 steps closing, 15 opening, 2 with the
       transition killed. */
    test: p => p.railTabOpen === true && p.railTabClosed === false
               && p.railTabReopen === true
               && p.railClosedW === 30 && p.railOpenW > 150
               && p.railCloseSteps >= 6 && p.railOpenSteps >= 6
               && p.railPoisonSteps <= 3,
    detail: p => `tab open/closed/reopen ${p.railTabOpen}/${p.railTabClosed}/${p.railTabReopen}`
               + ` · ${p.railOpenW}px to ${p.railClosedW}px`
               + ` · ${p.railCloseSteps} closing / ${p.railOpenSteps} opening distinct widths`
               + ` · ${p.railPoisonSteps} with the transition killed`,
    poison: p => ({ ...p, railCloseSteps: 2 }),
  },
];

/* ---- the fit sweep ----------------------------------------------------------
 * Its own pass, because it is the only thing here that RESIZES the window, and a
 * resize invalidates every rect the main probe measured. Runs after it.
 *
 * Two halves. The first drives FIT and FIT ALL at four widths and asks the page
 * whether it ended up in cell mode -- eight states, because one threshold cannot
 * be checked at one width: 1366 fits at 0.222 and 2560 at 0.920, and a rule that
 * looks right on the second ambushes the first.
 *
 * The second is the pixel half, and it is deliberately geometry-free. Rather than
 * computing where a cell centre lands -- which would mean agreeing with the
 * renderer about PAD.t, the exact dependence the geo comment above warns off --
 * it counts pixels near one of the five saturated CLASS colours. Only chips draw
 * those; cells draw neutral plates and grey numerals, and the edge layer is off in
 * cell mode entirely. So the count collapsing when cell mode is forced ON is proof
 * the measure is reading the chip renderer and not a constant. */
async function fitSweep(page) {
  /* REAL ASPECT RATIOS, not four widths at one height. The first cut held height
     at 900 and the fit scale froze at 0.41 across 1600/1920/2560, because the fit
     is bound by the SHORTER axis and the height never moved -- eight states that
     were really two. These are the four common panel sizes, and their fits span
     roughly 0.33 to 0.75, which is the range that actually straddles the old 0.62
     threshold. */
  const SIZES = [[1366, 768], [1600, 900], [1920, 1080], [2560, 1440]];
  const fitCellModes = [], fitScales = [], fitHostW = [], fitWinW = [];
  for (const [w, h] of SIZES) {
    await page.setViewportSize({ width: w, height: h });
    await page.waitForTimeout(800);
    for (const sel of ['[data-fit]', '[data-fitall]']) {
      const btn = await page.$('.l0ctl ' + sel);
      if (btn) { await btn.click({ force: true }).catch(() => {}); }
      await page.waitForTimeout(600);
      const r = await page.evaluate(() => {
        const c = document.querySelector('.l0wrap');
        return { cells: !!window.__board.MAP.opt.cells,
                 k: window.__board.MAP.view.k,
                 hostW: c ? Math.round(c.getBoundingClientRect().width) : -1,
                 winW: window.innerWidth };
      });
      fitCellModes.push(r.cells); fitScales.push(r.k);
      fitHostW.push(r.hostW); fitWinW.push(r.winW);
    }
  }

  await page.setViewportSize({ width: 2000, height: 1150 });
  await page.waitForTimeout(800);
  const classInk = want => page.evaluate(async (cells) => {
    const MAP = window.__board.MAP;
    MAP.opt.cells = cells; MAP.repaint();
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    const cvs = document.querySelector('.l0wrap canvas');
    const d = cvs.getContext('2d').getImageData(0, 0, cvs.width, cvs.height).data;
    /* institution, document, programme, event/location, legislation/domain.
       The person grey is left out on purpose: it is close enough to antialiased
       type that cell numerals would score on it. */
    const CLSC = [[167,149,232],[240,210,100],[102,214,159],[127,180,232],[224,138,208]];
    let hit = 0, tot = 0;
    for (let i = 0; i < d.length; i += 4 * 29) {
      tot++;
      const r = d[i], g = d[i+1], b = d[i+2];
      for (const c of CLSC) {
        if (Math.abs(r-c[0]) + Math.abs(g-c[1]) + Math.abs(b-c[2]) <= 60) { hit++; break; }
      }
    }
    return tot ? Math.round(10000 * hit / tot) : -1;
  }, want);

  const cellInkChips = await classInk(false);
  const cellInkCells = await classInk(true);
  await page.evaluate(() => {
    window.__board.MAP.opt.cells = false; window.__board.MAP.repaint();
  });
  await page.waitForTimeout(400);

  return { fitCellModes, fitScales, fitHostW, fitWinW, cellInkChips, cellInkCells,
           /* A RATIO, not a floor. Cell mode does not fall to zero class-coloured
              ink -- measured at 25 per ten-thousand with chips against 9 without --
              because some chrome on the canvas sits inside the same tolerance. The
              claim being made is the one the numbers support: forcing cell mode on
              the real page costs most of the chip ink. A renderer that had stopped
              drawing chips entirely would flatten the two and fail here. */
           fitChipInk: cellInkChips > 0 && cellInkCells * 2 < cellInkChips };
}

/* THE MEASURE, at module scope so headSweep and the self-test run the SAME code.
 * Reads the canvas under each control's own rect. Optional shiftY translates the
 * real control row down onto the era band without repainting, which is the page
 * poison: a probe that reported 0 regardless would sail through a predicate poison
 * and fail this. */
async function eraInkUnderControls(page, shiftY) {
  return await page.evaluate(sy => {
    const ctl = document.querySelector('.l0ctl');
    const prev = ctl ? ctl.style.transform : '';
    /* PAGE POISON: move the real control row down onto the band while the canvas
       holds still. A probe that reported 0 regardless would pass the predicate
       poison below and fail this. */
    if (sy && ctl) ctl.style.transform = 'translateY(' + sy + 'px)';
    const cvs = document.querySelector('.l0wrap canvas');
    if (!cvs) return { ink: -1, headH: -1 };
    const ctx = cvs.getContext('2d');
    const hb = cvs.getBoundingClientRect();
    const dpr = cvs.width / hb.width;
    const HEAD = [141,151,164], NOTE = [92,102,114];   /* colHead, colNote */
    const near = (r,g,b,c) => Math.abs(r-c[0]) + Math.abs(g-c[1]) + Math.abs(b-c[2]) <= 26;
    let ink = 0;
    for (const el of document.querySelectorAll('.l0head button, .l0head .l0chip, .l0head .l0cam')) {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      const x0 = Math.max(0, Math.round((r.left - hb.left) * dpr));
      const y0 = Math.max(0, Math.round((r.top  - hb.top ) * dpr));
      const w  = Math.min(cvs.width  - x0, Math.round(r.width  * dpr));
      const h  = Math.min(cvs.height - y0, Math.round(r.height * dpr));
      if (w <= 0 || h <= 0) continue;
      const d = ctx.getImageData(x0, y0, w, h).data;
      for (let i = 0; i < d.length; i += 4)
        if (near(d[i],d[i+1],d[i+2],HEAD) || near(d[i],d[i+1],d[i+2],NOTE)) ink++;
    }
    const hr = document.querySelector('.l0head').getBoundingClientRect();
    if (ctl) ctl.style.transform = prev;
    return { ink, headH: Math.round(hr.height) };
  }, shiftY || 0);
}

/* THE LEFT EDGE, on exactly the pattern above and for exactly the same reason.
 *
 * `.rail-fold` is the rail's fold tab: position:fixed at the rail's right edge,
 * 22px wide, hanging INTO the map by design the way `.dock-fold` hangs into it from
 * the other side. The band labels are painted inside the canvas, and until the
 * measured inset landed they started at a hard x=10 -- straight underneath it.
 *
 * WHAT THAT LOOKED LIKE is why no check caught it for four days: not a blank
 * region, not an error, just two bands whose names had lost their first two
 * characters. RESEARCH read "SEARCH". OVERSIGHT read "ERSIGHT". Both node counts
 * went with them. Only two of seven bands were hit, because the tab is 150px tall
 * and vertically centred, so the page reads as though those rows are simply called
 * that. "SEARCH" is not a truncation a reader can decode -- it is a different word,
 * and it is the name of another view on this board.
 *
 * `the gutter labels do not scale away with the world` could never have caught it:
 * it asserts that ink is PRESENT, and ink was present. It was the wrong ink.
 *
 * The poison is the page poison from eraInkUnderControls, mirrored: widen the real
 * fold tab without repainting, so the labels stay where they are and the tab laps
 * over them. A probe that reported 0 regardless sails through a predicate poison
 * and fails this one. */
async function bandInkUnderRailTab(page, widenTo) {
  return await page.evaluate(w => {
    const tab = document.querySelector('.rail-fold');
    if (!tab) return { ink: -1, tabW: -1, clear: -1 };
    const prev = tab.style.width;
    /* PAGE POISON: widen the real tab while the canvas holds still. */
    if (w) tab.style.width = w + 'px';
    const cvs = document.querySelector('.l0wrap canvas');
    if (!cvs) { tab.style.width = prev; return { ink: -1, tabW: -1, clear: -1 }; }
    const ctx = cvs.getContext('2d');
    const hb = cvs.getBoundingClientRect();
    const tb = tab.getBoundingClientRect();
    const dpr = cvs.width / hb.width;
    /* bandLabel, bandN, and pointer for a thin band drawn amber. */
    const COLS = [[92,102,114], [59,68,79], [239,181,85]];
    const near = (r,g,b,c) => Math.abs(r-c[0]) + Math.abs(g-c[1]) + Math.abs(b-c[2]) <= 26;
    const x0 = Math.max(0, Math.round((tb.left - hb.left) * dpr));
    const y0 = Math.max(0, Math.round((tb.top  - hb.top ) * dpr));
    const ww = Math.min(cvs.width  - x0, Math.round(tb.width  * dpr));
    const hh = Math.min(cvs.height - y0, Math.round(tb.height * dpr));
    let ink = 0;
    if (ww > 0 && hh > 0) {
      const d = ctx.getImageData(x0, y0, ww, hh).data;
      for (let i = 0; i < d.length; i += 4)
        for (const c of COLS) if (near(d[i], d[i+1], d[i+2], c)) { ink++; break; }
    }
    /* How far the leftmost label ink actually sits from the tab's right edge, as a
       positive number when it is clear. Reported so the check says how much room it
       had, not merely that it had some. */
    let clear = -1;
    const scan = ctx.getImageData(0, y0, Math.min(cvs.width, Math.round(200 * dpr)),
                                  Math.max(1, hh));
    outer:
    for (let px = 0; px < scan.width; px++) {
      for (let py = 0; py < scan.height; py++) {
        const i = (py * scan.width + px) * 4;
        for (const c of COLS) if (near(scan.data[i], scan.data[i+1], scan.data[i+2], c)) {
          clear = Math.round(px / dpr - (tb.right - hb.left));
          break outer;
        }
      }
    }
    tab.style.width = prev;
    return { ink, tabW: Math.round(tb.width), clear };
  }, widenTo || 0);
}

/* ---- the head sweep ---------------------------------------------------------
 * The worst case for the control row, held for four widths: an entry path open
 * (its chip widens the left group) and a node selected (the dossier takes half the
 * window). That is the state that wraps `.l0ctl` onto two and three lines, and the
 * state Stewart was in when he screenshotted the era heads printing through the
 * buttons.
 *
 * Reads the canvas UNDER each control's own rect. The controls are DOM painted over
 * the canvas, so the map's ink is still there to find underneath -- which is exactly
 * what the reader sees through a semi-transparent button. */
async function headSweep(page) {
  const SIZES = [[1366, 768], [1600, 900], [1920, 1080], [2560, 1440]];
  const eraInkWidths = [], eraInkAt = [], eraHeadH = [];
  const measure = shiftY => eraInkUnderControls(page, shiftY);

  await page.evaluate(() => { window.__board.CMD.openPath('money'); });
  await page.waitForTimeout(1500);
  await page.evaluate(() => { window.__board.CMD.selectNode('aawsap'); });
  await page.waitForTimeout(1500);

  for (const [w, h] of SIZES) {
    await page.setViewportSize({ width: w, height: h });
    await page.waitForTimeout(900);
    const r = await measure(0);
    eraInkWidths.push(r.ink); eraInkAt.push(w); eraHeadH.push(r.headH);
  }
  /* The poison at the width that wrapped hardest of the four. */
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.waitForTimeout(900);
  const poisoned = await measure(22);

  await page.evaluate(() => {
    window.__board.CMD.clearSelection && window.__board.CMD.clearSelection();
    window.__board.CMD.clearPath && window.__board.CMD.clearPath();
  });
  await page.setViewportSize({ width: 2000, height: 1150 });
  await page.waitForTimeout(900);

  return { eraInkWidths, eraInkAt, eraHeadH,
           eraInkMax: Math.max.apply(null, eraInkWidths),
           eraInkPoison: poisoned.ink };
}

/* The DOM overlays that sit on the map, against the control row they must clear.
   headSweep guards what the CANVAS paints under the buttons; this guards what the
   DOM stacks on top of them, which is a different failure with the same cause. On
   27 August .l0reg was pinned at top:44px -- a constant that cleared a single-line
   strip by 9px and nothing else. Open the dossier so the row wraps and, measured,
   the register covered the controls by 22px at 2560, 53 at 1920 and 1600 and 84 at
   1366, from ABOVE: z-index 5 against .l0head's 4.

   The poison is page-level and is the whole point: it puts the old constant back
   on the live page by overriding --l0-ctl, and the overlap must return. A check
   that only ever sees the fixed value cannot tell a measured reserve from a lucky
   one. 0px against 53 at 1600 when it was written. */
async function overlayOverlap(page) {
  return await page.evaluate(() => {
    const q = s => { const e = document.querySelector(s); if (!e) return null;
      const r = e.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, left: r.left, right: r.right }; };
    const head = q('.l0head'), reg = q('.l0reg');
    if (!head || !reg) return { overlap: -1, headH: -1 };
    /* Vertical overlap only counts where the two also share horizontal span. */
    const across = !(reg.left >= head.right || reg.right <= head.left);
    const v = Math.max(0, Math.min(head.bottom, reg.bottom) - Math.max(head.top, reg.top));
    return { overlap: across ? Math.round(v) : 0, headH: Math.round(head.bottom - head.top) };
  });
}

/* The dossier's reading measure, in characters rather than pixels, because
   characters are what the rule is about. Half the viewport made the panel WIDER
   the bigger the monitor got, which is backwards: measured at 11.5px IBM Plex
   Mono, running prose ran 95 / 112 / 135 / 182 characters at 1366 / 1600 / 1920 /
   2560 against a 45-75 comfortable band and a ~90 ceiling. The advance is
   measured off the resolved face rather than assumed, because the whole point of
   a monospace measure is that it is knowable and this file has been bitten by
   assumed metrics before. */
async function dossierMeasure(page) {
  return await page.evaluate(() => {
    const d = document.getElementById('dock');
    if (!d) return -1;
    const ps = [...d.querySelectorAll('p')].filter(e => (e.textContent || '').length > 200);
    let widest = 0, el = null;
    for (const e of ps) { const r = e.getBoundingClientRect(); if (r.width > widest) { widest = r.width; el = e; } }
    if (!el) return -1;
    const cs = getComputedStyle(el);
    const cv = document.createElement('canvas').getContext('2d');
    cv.font = cs.fontSize + ' ' + cs.fontFamily;
    const adv = cv.measureText('M'.repeat(100)).width / 100;
    return adv > 0 ? Math.round(widest / adv) : -1;
  });
}

/* BOTH DRAWERS FOLD ON A CURVE, IN BOTH DIRECTIONS.
   The dock's slide was got right on 27 August only because it was sampled every
   frame: `.dock{transition:width}` never ran at all, and transitioning the grid
   track on an UNREGISTERED custom property gave 30px -> 762px in ONE frame with a
   140ms settle after it. Both looked like a slide in a screenshot and neither was.
   The rail then repeated the family error a third time with `display:none`, which
   is not interpolable at any duration.

   So this counts DISTINCT WIDTHS across the transition rather than trusting that a
   transition property is declared. A real eased fold produces a dozen or more; a
   discrete flip produces two. The poison sets `transition:none` on the live page
   and requires the count to collapse, which is what proves the sampler is watching
   the animation rather than reporting a constant. */
async function foldFrames(page, action) {
  return await page.evaluate(async (act) => {
    const app = document.getElementById('app');
    const read = () => parseFloat(getComputedStyle(app).getPropertyValue('--rail-w')) || 0;
    const out = [read()];
    if (act === 'fold') { const t = document.querySelector('.rail-fold'); if (t) t.click(); }
    else { const r = document.querySelector('.rail'); if (r) r.click(); }
    await new Promise(res => {
      let n = 0;
      const tick = () => { out.push(read()); if (++n < 40) requestAnimationFrame(tick); else res(); };
      requestAnimationFrame(tick);
    });
    return out;
  }, action);
}

async function railSweep(page) {
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.waitForTimeout(700);
  /* START FROM A KNOWN OPEN STATE, THROUGH THE REAL CONTROL. The sweeps before
     this one drive FIT ALL and an entry path, both of which fold the rail, so
     measuring "the fold" from whatever they left behind measures nothing.

     And it has to be a CLICK on #railbtn rather than setting S.railOpen: the board
     is wrapped in an IIFE, so S and applyChrome are module-private and unreachable
     from page.evaluate -- the same constraint runtime_check.js is built around.
     Reaching for them silently no-ops and the assertion then measures a rail that
     nothing ever opened. */
  await page.evaluate(() => {
    const app = document.getElementById('app');
    const rb = document.getElementById('railbtn');
    if (app && app.classList.contains('rail-off') && rb) rb.click();
  });
  await page.waitForTimeout(700);
  const tab = async () => await page.evaluate(() => !!document.querySelector('.rail-fold'));

  const tabWhenOpen = await tab();
  const closing = await foldFrames(page, 'fold');
  await page.waitForTimeout(500);
  const tabWhenClosed = await tab();
  const opening = await foldFrames(page, 'open');
  await page.waitForTimeout(500);
  const tabAfterReopen = await tab();

  /* PAGE POISON: kill the transition and fold again. A discrete flip must not be
     able to pass a check written to detect a slide. */
  await page.evaluate(() => {
    const st = document.createElement('style');
    st.id = 'railpoison';
    st.textContent = '#app{transition:none !important}';
    document.head.appendChild(st);
  });
  await page.waitForTimeout(300);
  const poisoned = await foldFrames(page, 'fold');
  await page.evaluate(() => {
    const st = document.getElementById('railpoison'); if (st) st.remove();
    const r = document.querySelector('.rail'); if (r) r.click();
  });
  await page.waitForTimeout(700);
  await page.setViewportSize({ width: 2000, height: 1150 });
  await page.waitForTimeout(700);

  const distinct = a => new Set(a.map(v => Math.round(v))).size;
  return {
    railTabOpen: tabWhenOpen, railTabClosed: tabWhenClosed, railTabReopen: tabAfterReopen,
    railCloseSteps: distinct(closing), railOpenSteps: distinct(opening),
    railPoisonSteps: distinct(poisoned),
    railClosedW: Math.round(closing[closing.length - 1]),
    railOpenW: Math.round(opening[opening.length - 1]),
  };
}

async function overlaySweep(page) {
  const SIZES = [[1366, 768], [1600, 900], [1920, 1080], [2560, 1440]];
  const regOverlaps = [], regHeadH = [], proseChars = [];

  await page.evaluate(() => { window.__board.CMD.openPath('money'); });
  await page.waitForTimeout(1200);
  await page.evaluate(() => { window.__board.CMD.selectNode('aawsap'); });
  await page.waitForTimeout(1200);
  await page.evaluate(() => { window.__board.CMD.showPathOnly(); });
  await page.waitForTimeout(1200);

  for (const [w, h] of SIZES) {
    await page.setViewportSize({ width: w, height: h });
    await page.waitForTimeout(900);
    const r = await overlayOverlap(page);
    regOverlaps.push(r.overlap); regHeadH.push(r.headH);
    proseChars.push(await dossierMeasure(page));
  }

  /* PAGE POISON: restore the pre-fix constant and require the overlap back. */
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.waitForTimeout(900);
  await page.evaluate(() => {
    const host = document.querySelector('.l0wrap');
    if (host) host.style.setProperty('--l0-ctl', '44px');
  });
  await page.waitForTimeout(500);
  const poisoned = await overlayOverlap(page);
  /* SECOND PAGE POISON, for the measure rather than the overlap: put the old
     half-the-viewport width back and require the line length to bust the ceiling.
     Two poisons because the two assertions guard different properties, and one
     poison proving "something went red" would leave the other untested. */
  await page.evaluate(() => {
    document.documentElement.style.setProperty('--dock-w',
      Math.round(window.innerWidth * 0.5) + 'px');
  });
  await page.waitForTimeout(500);
  const proseCharsPoison = await dossierMeasure(page);
  await page.evaluate(() => {
    document.documentElement.style.removeProperty('--dock-w');
    const host = document.querySelector('.l0wrap');
    if (host) host.style.removeProperty('--l0-ctl');
    window.__board.CMD.clearSelection && window.__board.CMD.clearSelection();
    window.__board.CMD.clearPath && window.__board.CMD.clearPath();
  });
  await page.setViewportSize({ width: 2000, height: 1150 });
  await page.waitForTimeout(900);

  return { regOverlaps, regHeadH, proseChars,
           regOverlapMax: Math.max.apply(null, regOverlaps),
           regOverlapPoison: poisoned.overlap,
           proseCharsMax: Math.max.apply(null, proseChars),
           proseCharsMin: Math.min.apply(null, proseChars),
           proseCharsPoison };
}

/* ---- probing the page ------------------------------------------------------ */
async function probe(page, opts = {}) {
  return await page.evaluate(async (o) => {
    const B = window.__board;
    const near = (px, hex, tol) => {
      const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
      return Math.abs(px[0] - r) + Math.abs(px[1] - g) + Math.abs(px[2] - b) <= tol;
    };
    const dist = (px, hex) => {
      const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
      return Math.abs(px[0] - r) + Math.abs(px[1] - g) + Math.abs(px[2] - b);
    };
    const STRIP_BG0 = '#11141a';
    const CLS = {
      institution: '#a795e8', document: '#f0d264', program: '#66d69f',
      event: '#7fb4e8', legislation: '#e08ad0', person: '#c9d2dd',
      location: '#7fb4e8', domain: '#e08ad0',
    };
    const CHIP_FILL = '#12171d', AMBER = '#efb555';

    const D = B.L0DATA, PK = D.packed || {}, MAP = B.MAP;
    /* PAGE-LEVEL POISON. The predicate poisons at the bottom of this file prove
       each test() rejects bad input. They do NOT prove the probe measures the
       right pixels -- a probe that always returned the class colour would sail
       through them, which is precisely how six verify checks were once born
       broken and silently passing.

       So: snapshot the coordinates FIRST, then shift what the renderer draws, and
       keep measuring against the snapshot. The chips move; the expectation does
       not. Anything that still reports 110/110 is not reading the canvas. */
    const ORIG = {};
    for (const n of (D.l0 || [])) ORIG[n.id] = { x: n.x, y: n.y, w: n.w, h: n.h };
    if (o.shiftX) {
      for (const n of D.l0) n.x += o.shiftX;
      if (B.MAP) B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }
    const cvs = document.querySelector('.l0wrap canvas');
    const out = {
      hasCanvas: !!cvs,
      l0Nodes: (D.l0 || []).length,
      packedNodes: 0, withRect: 0, distinctSizes: 0,
      overlaps: 0, onScreen: 0, inkPct: 0,
      classProbes: 0, classHits: 0, classUnprobed: -1, classMiss: [],
      flagProbes: 0, flagHits: 0, flagMiss: [],
      openingChips: 0, labelsLegible: false, k: 0,
      gutterInkPanned: false, headInkPanned: false,
      restCount: (PK.rest || []).length,
      restDrawnFigure: o.restDrawnFigure,
      allEdges: (D.directEdges || []).length + (D.summarised || []).length,
      optRest: false, optFlags: false, optLabels: false, optCells: null,
      optControls: 0, controlsOn: 0,
      fitCellModes: [], fitScales: [], fitChipInk: false,
      cellInkChips: -1, cellInkCells: -1,
      eraInkMax: -1, eraInkWidths: [], eraInkAt: [], eraHeadH: [], eraInkPoison: -1,
    };
    if (!cvs || !MAP) return out;

    const sizes = new Set();
    for (const n of D.l0) {
      if (n.x != null && n.y != null && n.w && n.h) { out.withRect++; sizes.add(n.w + 'x' + n.h); }
    }
    out.packedNodes = out.withRect;
    out.distinctSizes = sizes.size;

    const v = MAP.view;
    out.k = Math.round(v.k * 100) / 100;
    out.optRest = !!MAP.opt.rest; out.optFlags = !!MAP.opt.flags;
    out.optLabels = !!MAP.opt.labels; out.optCells = !!MAP.opt.cells;
    const ctrls = [...document.querySelectorAll('.l0ctl [data-opt]')];
    out.optControls = ctrls.length;
    out.controlsOn = ctrls.filter(b => b.className.indexOf('on') >= 0).length;

    const host = cvs.parentElement.getBoundingClientRect();
    const Wc = host.width, Hc = host.height;
    /* The map reserves these two strips for the row and column labels and clips
       itself out of them, so a "visible" chip means visible in the CONTENT rect.
       Counting the chrome as map is how the first cut of this file managed to
       probe six chips that the renderer had correctly refused to draw there. */
    /* PK.geo is populated by merge_packed, so this tracks the renderer's own PAD
       rather than restating it. The literals are the degenerate-model fallback and
       must never be relied on: if they ever diverge from geo, this check measures
       a different strip from the one the renderer draws and agrees with a renderer
       it is no longer describing. */
    const geo0 = PK.geo || { gutter: 148, headRow: 46 };
    const PADL = geo0.gutter, PADT = geo0.headRow;
    const rect = n => { const g = ORIG[n.id] || n;
      return { x: g.x * v.k + v.ox, y: g.y * v.k + v.oy,
               w: g.w * v.k, h: g.h * v.k }; };
    const vis = D.l0.map(n => ({ n, r: rect(n) }))
      .filter(({ r }) => r.x >= PADL && r.y >= PADT && r.x + r.w <= Wc && r.y + r.h <= Hc);
    out.onScreen = vis.length;
    out.openingChips = vis.length;
    out.labelsLegible = MAP.opt.labels && v.k >= 0.62;

    for (let i = 0; i < vis.length; i++) {
      for (let j = i + 1; j < vis.length; j++) {
        const a = vis[i].r, b = vis[j].r;
        if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h)
          out.overlaps++;
      }
    }

    const ctx = cvs.getContext('2d');
    const dpr = cvs.width / Wc;
    const px = (cx, cy) => {
      const d = ctx.getImageData(Math.round(cx * dpr), Math.round(cy * dpr), 1, 1).data;
      return [d[0], d[1], d[2]];
    };

    /* Ink means CONTENT ink. Counting any opaque pixel would score 95% on a
       canvas painted entirely in band fills with not one chip on it, which is the
       exact shape of the bug this check exists for -- `canvasInk` once reported
       zero on a drawing canvas and had never fired either way. So the grounds are
       named and excluded, and what is left is chips, edges, labels and furniture. */
    const GROUNDS = ['#141920', '#12161c', '#11141a', '#12171d'];
    let inked = 0, total = 0;
    const grid = ctx.getImageData(0, 0, cvs.width, cvs.height).data;
    for (let y = 0; y < cvs.height; y += 4) {
      for (let x = 0; x < cvs.width; x += 4) {
        const i = (y * cvs.width + x) * 4;
        total++;
        if (grid[i + 3] < 8) continue;
        const q = [grid[i], grid[i + 1], grid[i + 2]];
        if (GROUNDS.every(g => dist(q, g) > 14)) inked++;
      }
    }
    out.inkPct = total ? Math.round(inked / total * 100) : 0;

    /* The class rule runs down the chip's left edge, 3px wide at k=1. Column x is
       the border stroke, so x+1 is the first pixel of the rule itself.
       The camera is walked across the whole world in overlapping steps so that
       EVERY node gets probed, not only the ~32 that happen to be in the opening
       view. A layout bug that spares the top-left corner and wrecks the 2017-2026
       column is exactly the kind a single-viewport check waves through. */
    const FLAGS = new Set(PK.flags || []);
    const seen = new Set();
    /* Integral camera steps ON PURPOSE. At a fractional offset the chip's 3px
       class rule lands across pixel boundaries and antialiases into the chip fill,
       and the probe then measures the browser's blending rather than the
       renderer's placement. The rule being sampled is 3px wide; the check is about
       where it is, not how it resolves at a half-pixel. */
    /* The camera is aimed at each node in turn rather than swept in a grid.
       A grid sweep left 20 nodes unreached at the world's right and bottom edges
       once the frozen chrome narrowed the content rect -- and a check that quietly
       skips the far column is worse than no check, because the far column is
       2017-2026, the densest part of the board. */
    /* Unit scale for this pass, and say why rather than inherit it.
       The class rule is 3 * view.k pixels wide and the probe samples 1.5px in from
       the chip's left edge -- geometry that only lands inside the rule at k = 1.
       It used to get k = 1 for free, because the map opened at the top-left corner
       at 1:1 below the label threshold. The map now opens FITTED at every width,
       so at this viewport it opens near 0.63, the rule is under 2px wide, the
       sample falls on its antialiased edge and 90 of 110 chips "missed" their own
       colour. Nothing was wrong with the renderer; the probe was carrying an
       assumption it had never had to state. */
    const kProbe = v.k;
    v.k = 1;
    for (const target of D.l0) {
      if (seen.has(target.id)) continue;
      v.ox = Math.round((PADL + Wc) / 2 - (target.x + target.w / 2) * v.k);
      v.oy = Math.round((PADT + Hc) / 2 - (target.y + target.h / 2) * v.k);
      MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      {
        for (const n of D.l0) {
          if (seen.has(n.id)) continue;
          const r = rect(n);
          if (r.x < PADL + 2 || r.y < PADT + 2
              || r.x + r.w > Wc - 2 || r.y + r.h > Hc - 2) continue;
          seen.add(n.id);
          const want = CLS[n.cls] || CLS.person;
          const q = px(r.x + 1.5, r.y + r.h / 2);
          out.classProbes++;
          if (dist(q, want) < dist(q, CHIP_FILL)) out.classHits++;
          else out.classMiss.push(n.id + ':' + n.cls + ':' + q.join(','));
          if (FLAGS.has(n.id) && r.x > 20) {
            out.flagProbes++;
            let hit = false;
            for (let d = 4; d <= 15 && !hit; d++) {
              if (near(px(r.x - d, r.y + r.h / 2), AMBER, 90)) hit = true;
            }
            if (hit) out.flagHits++; else out.flagMiss.push(n.id);
          }
        }
      }
    }
    out.classUnprobed = D.l0.length - seen.size;
    v.k = kProbe;                       /* hand the camera back as it was found */

    /* The start-here pointer sits in the gap to the LEFT of the chip, between
       9 and 14px out. Amber there and nowhere on the chip is the separation. */

    /* Pan to the far bottom-right of the world and look again at the two strips
       the model reserves for furniture: geo.gutter on the left, geo.headRow on
       top. World-space labels would have left the viewport by now. */
    v.ox = -(PK.worldW * v.k - Wc) - 4;
    v.oy = -(PK.worldH * v.k - Hc) - 4;
    MAP.repaint();
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    /* LABEL ink specifically. The strips are painted opaque so nothing shows
       through them, which means "the strip has ink" would pass on an empty strip.
       What must be true is that TEXT is on them, so this counts only pixels that
       differ from the strip's own ground, and stays clear of the two 1px rules at
       the strip borders so a rule alone cannot carry the check. */
    const STRIP_BG = STRIP_BG0;
    const strip = (x0, y0, x1, y1) => {
      let n = 0;
      for (let y = y0; y < y1; y += 2)
        for (let x = x0; x < x1; x += 2) if (dist(px(x, y), STRIP_BG) > 30) n++;
      return n;
    };
    out.gutterInkPanned = strip(6, PADT + 2, PADL - 14, Hc - 2) > 20;
    out.headInkPanned = strip(PADL + 2, 4, Wc - 2, PADT - 14) > 20;

    /* The head strip is shared: the canvas paints the era labels on it and the
       map's own DOM controls (.l0crumb, .l0ctl) are positioned on top of it. Ink
       alone cannot see the difference -- headInkPanned above passed happily for
       the whole of the first build, while two of the five era heads were drawn
       underneath PROGRAM MAP and LINES AT REST and rendered as a smear. So
       measure the CLEARANCE: the lowest pixel any control occupies, against the
       highest pixel the era label reaches. mountL0 draws that label on the
       baseline PAD.t - 22, and 9px covers the cap height of its 9px face. */
    const wrapEl = document.querySelector('.l0wrap');
    const wrTop = wrapEl.getBoundingClientRect().top;
    let ctlBottom = 0;
    for (const el of document.querySelectorAll('.l0crumb, .l0crumb *, .l0ctl, .l0ctl *')) {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      ctlBottom = Math.max(ctlBottom, r.bottom - wrTop);
    }
    /* LABEL TRUNCATION. Design: middle, never end. "AARO Historical Record Volume 1"
       and "... Volume 2" are identical under an end ellipsis, and the tail is where
       this corpus keeps its distinguishing token. Recompute each chip's rendered
       label through the page's own l0Fit and the same font the renderer uses, then
       assert none of them ENDS in an ellipsis. */
    const probe = document.createElement('canvas').getContext('2d');
    probe.font = "400 9.5px 'IBM Plex Mono',monospace";
    let endTrunc = 0, midTrunc = 0, fitted = 0;
    const endTruncEx = [];
    const fit = B.l0Fit;
    if (typeof fit === 'function') {
      for (const n of (D.l0 || [])) {
        const raw = n.short || n.label || n.id;
        /* the room the renderer gives a label at k=1: chip minus rule, glyph, gaps
           and whatever is reserved on the right */
        let right = 5; if (n.iso) right += 13;
        const t = fit(probe, raw, (n.w - right) - (7 + 11 + 5));
        if (t === raw) fitted++;
        else if (t.endsWith('\u2026')) { endTrunc++; if (endTruncEx.length < 3) endTruncEx.push(raw); }
        else if (t.indexOf('\u2026') > 0) midTrunc++;
      }
    } else { endTrunc = -1; }
    out.endTrunc = endTrunc; out.midTrunc = midTrunc; out.fittedLabels = fitted;
    out.endTruncEx = endTruncEx;
    /* THE BREATH MUST NOT TOUCH A PROPERTY THAT CARRIES DATA. Design named the
       failure: putting the bloom on box-shadow wiped the entity-tier stroke it
       shares. Here the bloom rides an outline drawn OUTSIDE the chip, so the
       chip's own stroke -- which carries tier -- can never be part of the
       animation. Tested over a full cycle rather than at one instant: sample the
       stroke pixel and a pixel just outside it many times across 7 seconds, and
       require the stroke to be CONSTANT while the outside pixel VARIES. */
    {
      const fl = (D.l0 || []).find(n => (PK.flags || []).indexOf(n.id) >= 0);
      if (fl) {
        const r = { x: fl.x*v.k + v.ox, y: fl.y*v.k + v.oy, w: fl.w*v.k, h: fl.h*v.k };
        const sx = Math.round(r.x + r.w - 1), sy = Math.round(r.y + r.h/2);  /* on the stroke */
        const ox = Math.round(r.x + r.w + 2), oy = sy;                       /* just outside */
        const key = (x, y) => { const q = px(x, y); return q[0]+','+q[1]+','+q[2]; };
        const strokeSeen = new Set(), outSeen = new Set();
        for (let i = 0; i < 26; i++) {
          strokeSeen.add(key(sx, sy));
          outSeen.add(key(ox, oy));
          await new Promise(r2 => setTimeout(r2, 300));
        }
        out.breathStrokeStates = strokeSeen.size;
        out.breathOutlineStates = outSeen.size;
      } else { out.breathStrokeStates = -1; out.breathOutlineStates = -1; }
    }
    /* MOTION ONLY WHERE ATTESTED, tested on the rendered canvas rather than on the
       model's flags. Design's own `motion_only_where_attested` guards the FLAGS and
       passed for the whole of the first build while nothing moved at all -- a check
       that cannot tell a still canvas from a moving one cannot police motion.
       Two cases may move: a directed denial (none authored yet) and the selected
       node's own edges, which assert nothing because the reader chose the end.
       So with the breath off and nothing selected the canvas must be FROZEN, and
       selecting a node must make it move. */
    {
      const hashC = () => {
        const d = ctx.getImageData(0, 0, cvs.width, cvs.height).data;
        let h = 0;
        for (let i = 0; i < d.length; i += 4*53) h = (h*31 + d[i] + d[i+1]*3 + d[i+2]*7) >>> 0;
        return h;
      };
      const St = B.S;
      const open0 = St.l0open.slice();
      St.l0open = [];
      /* Re-query every time: renderChrome() rebuilds the control row on each click,
         so a handle taken once goes stale and its textContent stops tracking. */
      const attnBtn = () => [...document.querySelectorAll('.l0ctl button')]
        .find(x => /BREATH|ONCE|STILL/.test(x.textContent));
      for (let i = 0; i < 4; i++) {
        const bt = attnBtn();
        if (!bt || /STILL/.test(bt.textContent)) break;
        bt.click();
        await new Promise(r => setTimeout(r, 120));
      }
      out.attnState = (attnBtn() || {}).textContent || '(no control)';
      B.MAP.repaint();
      await new Promise(r => setTimeout(r, 900));
      const q = new Set();
      for (let i = 0; i < 4; i++) { q.add(hashC()); await new Promise(r => setTimeout(r, 400)); }
      out.stillFrames = q.size;
      /* THE CONTROL RUN. Motion at rest is only legitimate if the DENIAL
         ATTRIBUTION is what causes it. Strip `denier`/`denialKind` from every
         edge on the live page, repaint, and the map must go still. If it keeps
         moving without a single attested denier, what is moving is a flow on
         every line -- the treatment Design rejected outright -- and this check
         would otherwise have waved it through. */
      const dnBackup = (D.directEdges || []).map(e =>
        ({ e, denier: e.denier, kind: e.denialKind }));
      for (const r of dnBackup) { r.e.denier = null; r.e.denialKind = null; }
      B.MAP.repaint();
      await new Promise(r => setTimeout(r, 900));
      const q3 = new Set();
      for (let i = 0; i < 4; i++) { q3.add(hashC()); await new Promise(r => setTimeout(r, 400)); }
      out.stillFramesNoDenial = q3.size;
      for (const r of dnBackup) { r.e.denier = r.denier; r.e.denialKind = r.kind; }
      B.MAP.repaint();
      await new Promise(r => setTimeout(r, 500));
      out.directedDenials = (D.directEdges || []).filter(e =>
           (e.types || []).indexOf('denial') >= 0
        && e.denialKind !== 'association'
        && (e.denier === e.a || e.denier === e.b)).length;
      const first = (D.l0 || []).find(n => (n.direct || []).length > 2) || (D.l0 || [])[0];
      St.l0open = first ? [first.id] : [];
      B.MAP.repaint();
      await new Promise(r => setTimeout(r, 700));
      const q2 = new Set();
      for (let i = 0; i < 5; i++) { q2.add(hashC()); await new Promise(r => setTimeout(r, 350)); }
      out.selectedFrames = q2.size;
      St.l0open = open0;
      B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }
    out.ctlBottom = Math.round(ctlBottom);
    out.headStrip = PADT;
    out.headClear = Math.round((PADT - 22 - 9) - ctlBottom);
    out.eraHeads = (PK.eras || []).length;

    /* DENSE MODE. Design's answer to 110 anonymous rectangles is that the chips
       collapse and every occupied cell prints its count, with the edge layer
       switched off entirely -- so there are three things to see: the counts are
       there, the lattice is not, and the axis type survived.

       THESE PROBES USED TO REACH DENSE MODE BY SETTING `v.k = 0.45`, because
       dense() was `view.k < L0_LABEL_DROP`. On 27 August cell mode became an
       explicit opt flag that no scale can turn on, and at that moment every one
       of these checks would have gone on passing while measuring the CHIP
       renderer -- five checks silently testing nothing, which is CLAUDE.md
       section 5's whole subject. They set the flag now. The camera still drops to
       0.45 because the cell geometry is scale-dependent and the axis-type check
       needs a small scale to be worth anything. */
    {
      const k0 = v.k, ox0 = v.ox, oy0 = v.oy, cells0 = MAP.opt.cells;
      MAP.opt.cells = true;
      v.k = 0.45; v.ox = PADL - PADL*v.k; v.oy = PADT - PADT*v.k;
      B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const rowsN = (PK.bands || []).length;
      const rowH = (PK.worldH - PADT - 10) / rowsN;
      const occ = {};
      for (const n of D.l0) occ[n.band + '|' + n.col] = (occ[n.band + '|' + n.col] || 0) + 1;
      let cells = 0, cellsWithInk = 0;
      (PK.bands || []).forEach((b, i) => {
        for (const c of (PK.eras || [])) {
          if (!occ[b.id + '|' + c.id]) continue;
          cells++;
          const by = PADT + i*rowH;
          const cx = Math.round((c.x + c.w/2)*v.k + v.ox);
          const cy = Math.round((by + b.h/2 >= 0 ? by + rowH/2 : by)*v.k + v.oy);
          /* a box at the cell centre, where the numeral is */
          let ink = 0;
          for (let dy = -9; dy <= 9; dy += 2)
            for (let dx = -12; dx <= 12; dx += 2)
              if (dist(px(cx + dx, cy + dy), CHIP_FILL) > 26) ink++;
          if (ink >= 3) cellsWithInk++;
        }
      });
      out.denseCells = cells;
      out.denseCellsWithInk = cellsWithInk;
      /* THE EDGE LAYER, tested by difference rather than by counting ink.
         A first attempt counted non-ground pixels across the canvas and reported
         35% in dense mode against 8% with chips -- because at k=0.45 the whole
         world is on screen and the band STRIPING fills it, which is background,
         not edges. It was measuring the thing it was not looking for, loudly.
         So: toggle LINES AT REST, which is the control that governs the edge
         layer, and require the canvas to be BYTE-IDENTICAL either way. If the
         edges are genuinely not drawn, the toggle cannot change a pixel. */
      const hashCanvas = () => {
        const d = ctx.getImageData(0, 0, cvs.width, cvs.height).data;
        let h = 0;
        for (let i = 0; i < d.length; i += 4*29) h = (h*31 + d[i] + d[i+1]*3 + d[i+2]*7) >>> 0;
        return h;
      };
      const rest0 = MAP.opt.rest;
      MAP.opt.rest = true;  B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const hOn = hashCanvas();
      MAP.opt.rest = false; B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const hOff = hashCanvas();
      MAP.opt.rest = rest0;
      out.denseEdgeToggleInert = hOn === hOff;
      /* And the control is proved live at a scale where chips DO draw, so an
         inert toggle cannot pass by being broken everywhere. */
      MAP.opt.cells = false;   /* chips, genuinely -- the control is proved live here */
      v.k = 1; v.ox = 0; v.oy = 0; B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      MAP.opt.rest = true;  B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const cOn = hashCanvas();
      MAP.opt.rest = false; B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      const cOff = hashCanvas();
      MAP.opt.rest = rest0;
      out.chipEdgeToggleLive = cOn !== cOff;
      MAP.opt.cells = true;
      v.k = 0.45; v.ox = PADL - PADL*v.k; v.oy = PADT - PADT*v.k;
      B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      /* Axis type must survive: it is drawn at an authored px size positioned at
         world x scale, never scaled with the world. Measure the ink height of the
         first band label in the gutter -- 9px type leaves at least 5 rows of it. */
      const inked = y => {
        for (let x = 8; x < PADL - 14; x += 2) if (dist(px(x, y), STRIP_BG0) > 26) return true;
        return false;
      };
      let first = -1;
      for (let y = PADT; y < Hc && first < 0; y++) if (inked(y)) first = y;
      /* The CONTIGUOUS run from the first inked row, which is one label's cap
         height. A first attempt took topmost-to-bottommost across the whole gutter
         and got 337, i.e. the span of all seven labels, which would have passed
         while the type rendered at 2px. */
      let run = 0;
      if (first >= 0) { let y = first; while (y < Hc && inked(y)) { run++; y++; } }
      out.denseAxisInkRows = run;
      /* THIN BANDS PRINT AMBER. Design: keep the disclosure band, do not merge or
         pad it, but make thinness legible -- every band prints its count and under
         five prints amber, so a nearly empty row reads as an argument about the
         record rather than as a broken layout.
         Read it where it is drawn: amber ink in the gutter beside a band with
         fewer than five nodes, and NO amber beside a band with five or more. The
         second half is what makes this a check rather than a colour swatch -- an
         amber gutter everywhere would satisfy the first half alone. */
      const BB = PK.bands || [];
      const bandsInfo = BB.map(b => ({ id: b.id, n: b.n }));
      let thinAmber = 0, thinTotal = 0, fullAmber = 0, fullTotal = 0;
      /* Rows derived from the MODEL, not read off the band records: in dense mode
         -- which is where this probe runs, at k = 0.45 -- the renderer recomputes
         equal-height rows and the y/h on PK.bands are the non-dense ones. Reading
         them here put every band rectangle in the wrong place, and the check
         reported 0 of 1 thin bands amber while the amber was plainly on screen.
         worldH and the band count are both stated by the model, so this stays an
         independent statement of where a row is rather than the renderer's. */
      const bandRowH = (PK.worldH - PADT - 10) / (BB.length || 1);
      for (let bi = 0; bi < BB.length; bi++) {
        const b = BB[bi];
        const wy = PADT + bi * bandRowH;
        const y0 = Math.round(wy * v.k + v.oy),
              y1 = Math.round((wy + bandRowH) * v.k + v.oy);
        if (y1 < PADT || y0 > Hc) continue;
        let amber = false;
        for (let y = Math.max(PADT + 1, y0); y < Math.min(Hc, y1) && !amber; y++)
          for (let x = 8; x < PADL - 14; x += 2)
            if (near(px(x, y), AMBER, 100)) { amber = true; break; }
        if (b.n < 5) { thinTotal++; if (amber) thinAmber++; }
        else { fullTotal++; if (amber) fullAmber++; }
      }
      /* THE SELECTION SURVIVES CELL MODE. Select a node, stay in cell mode, and
         require cyan ink in the cell that node belongs to AND in no other cell.
         The second half is the check: cyan somewhere on a grid of 27 occupied
         cells proves nothing, and "the selection is visible" is a claim about
         WHICH cell it is in. The target cell is computed from the model's own
         band/col for the node, never from where the renderer put the ink. */
      {
        const pick = (D.l0 || []).find(n => n.band && n.col != null);
        if (pick) {
          B.S.sel = pick.id;
          MAP.repaint();
          await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
          const CYAN = '#5ed4e6';
          const bIdx = BB.findIndex(bb => bb.id === pick.band);
          let inTarget = false, inOthers = 0;
          for (let bi = 0; bi < BB.length; bi++) {
            for (const c of (PK.eras || [])) {
              const wy = PADT + bi * bandRowH;
              const x0 = Math.round((c.x + 10) * v.k + v.ox);
              const x1 = Math.round((c.x + c.w - 10) * v.k + v.ox);
              const yy0 = Math.round((wy + 10) * v.k + v.oy);
              const yy1 = Math.round((wy + bandRowH - 10) * v.k + v.oy);
              if (x1 < PADL || x0 > Wc || yy1 < PADT || yy0 > Hc) continue;
              let cyan = false;
              for (let y = Math.max(PADT + 1, yy0); y < Math.min(Hc, yy1) && !cyan; y += 2)
                for (let x = Math.max(PADL + 1, x0); x < Math.min(Wc, x1); x += 2)
                  if (near(px(x, y), CYAN, 60)) { cyan = true; break; }
              if (!cyan) continue;
              if (bi === bIdx && String(c.id) === String(pick.col)) inTarget = true;
              else inOthers++;
            }
          }
          out.selCellHit = inTarget;
          out.selCellStray = inOthers;
          out.selCellId = pick.id + '@' + pick.band + '/' + pick.col;
          B.S.sel = null;
          MAP.repaint();
          await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        }
      }
      /* THE DENIAL MARKS ARE DRIVEN BY THE ADJUDICATION.
         All 174 denial edges were read one at a time and given one of three
         states; 38 of the 47 on the map are directed, 5 undirected, 4 association.
         The map's job is to draw exactly that: an arrowhead where an issuer is
         named, a perpendicular bar where the act has no named issuer, and NOTHING
         where the edge is not a denial act.

         THIS COUNTS DRAW CALLS, NOT PIXELS, and that is a deliberate step down
         which is worth naming. Everything else in this file reads getImageData,
         because pixels are what a reader sees. Here that failed for a reason no
         amount of settling fixed: an arrowhead is a ~7px triangle at fit scale,
         the map redraws continuously, and the denial red (#e8705f) is also the
         absent-link cross colour -- so a whole-canvas colour count was dominated
         by crosses and never moved. Instrumenting ctx.fill during one repaint
         showed 1188 denial-coloured fills arriving while the pixel count sat at
         25 and called the layer dead.
         So: what this proves is that the RENDERER EMITTED the marks and that the
         adjudication is what drives them. What it does NOT prove is that they are
         visible or correctly placed -- `pointers-offset` and the screenshots carry
         that. Stated here so nobody reads more into it than it can support. */
      {
        const DENY = '#e8705f';
        const rest0 = MAP.opt.rest, lab0 = MAP.opt.labels, cells1 = MAP.opt.cells;
        const sel0 = B.S.sel, open0 = B.S.l0open;
        const k1 = v.k, ox1 = v.ox, oy1 = v.oy;
        /* CHIPS, not cells. This probe counts denial marks on EDGES, and the edge
           layer is switched off entirely in cell mode. It used to leave dense mode
           for free by raising v.k above 0.62; once cell mode stopped being a
           function of the camera that stopped working, and this check would have
           read 0 marks and called the adjudication dead. */
        MAP.opt.cells = false;
        MAP.opt.rest = true; MAP.opt.labels = true;
        B.S.sel = null; B.S.l0open = [];
        v.k = Math.max(0.63, MAP.fitScale());
        v.ox = PADL - PADL * v.k; v.oy = PADT - PADT * v.k;

        let fills = 0, strokes = 0;
        const of = ctx.fill.bind(ctx), os = ctx.stroke.bind(ctx);
        ctx.fill = function(){ if (String(ctx.fillStyle).toLowerCase() === DENY) fills++;
                               return of.apply(ctx, arguments); };
        ctx.stroke = function(){ if (String(ctx.strokeStyle).toLowerCase() === DENY) strokes++;
                                 return os.apply(ctx, arguments); };
        const settleMs = ms => new Promise(r => setTimeout(r, ms));
        MAP.repaint(); await settleMs(700);
        out.denyMarksOn = fills + strokes;

        const isDn = e => (e.types || []).indexOf('denial') >= 0;
        const saved = (D.directEdges || []).map(e => e.denialKind);
        (D.directEdges || []).forEach(e => { if (isDn(e)) e.denialKind = 'association'; });
        fills = 0; strokes = 0;
        MAP.repaint(); await settleMs(700);
        out.denyMarksAllAssoc = fills + strokes;

        ctx.fill = of; ctx.stroke = os;
        (D.directEdges || []).forEach((e, i) => { e.denialKind = saved[i]; });
        const dn = (D.directEdges || []).filter(isDn);
        out.denyDirected = dn.filter(e => e.denialKind === 'directed').length;
        out.denyUndirected = dn.filter(e => e.denialKind === 'undirected').length;
        out.denyAssoc = dn.filter(e => e.denialKind === 'association').length;
        MAP.opt.rest = rest0; MAP.opt.labels = lab0; MAP.opt.cells = cells1;
        B.S.sel = sel0; B.S.l0open = open0;
        v.k = k1; v.ox = ox1; v.oy = oy1;
        MAP.repaint(); await settleMs(300);
      }
      out.thinAmber = thinAmber; out.thinTotal = thinTotal;
      out.fullAmber = fullAmber; out.fullTotal = fullTotal;
      out.bandsInfo = bandsInfo;
      MAP.opt.cells = cells0;
      v.k = k0; v.ox = ox0; v.oy = oy0;
      B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }

    if (o.shiftX) {           /* put the board back the way it was found */
      for (const n of D.l0) n.x = ORIG[n.id].x;
      if (B.MAP) B.MAP.repaint();
    }
    return out;
  }, opts);
}

/* ---- the image tile -------------------------------------------------------
 *
 * data/l0-images.json is deliberately empty, so the real page draws 110 class
 * letters and there is no image anywhere to read pixels off. That is exactly the
 * condition under which a render branch rots: it ships, nothing exercises it, and
 * the first person to populate the register finds out whether it works.
 *
 * So the fixtures are injected. Two 16x16 PNGs in colours that appear nowhere in
 * the palette, assigned to two real map nodes, and the pixels read back:
 *
 *   the tile replaces the letter   the slot carries the fixture colour, and did
 *                                  not before injection
 *   a MARK is not cropped          this is the load-bearing one. A portrait may be
 *                                  cropped to a circle; an institutional seal may
 *                                  not, because a cropped seal is a different mark
 *                                  and several carry statutory restrictions on
 *                                  alteration stricter than copyright. Read the
 *                                  slot's CORNERS: square for a mark, empty for a
 *                                  portrait. Nothing else distinguishes them.
 *   a dead URL falls back          not a broken-image box. The class letter is a
 *                                  supported state; a grey box is not.
 *
 * Fixtures are marked as fixtures and are not sourcing claims: they are generated
 * bytes, not a photograph of anyone, and they never reach the register. */
function pngFixture(r, g, b) {
  const W = 16, H = 16;
  const raw = Buffer.alloc(H * (1 + W * 3));
  for (let y = 0; y < H; y++) {
    const row = y * (1 + W * 3);
    raw[row] = 0;
    for (let x = 0; x < W; x++) {
      raw[row + 1 + x * 3] = r; raw[row + 2 + x * 3] = g; raw[row + 3 + x * 3] = b;
    }
  }
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
    const body = Buffer.concat([Buffer.from(type, 'ascii'), data]);
    const crc = Buffer.alloc(4); crc.writeUInt32BE(zlib.crc32
      ? zlib.crc32(body) >>> 0 : crc32(body) >>> 0);
    return Buffer.concat([len, body, crc]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(H, 4);
  ihdr[8] = 8; ihdr[9] = 2; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  const png = Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(raw)),
    chunk('IEND', Buffer.alloc(0)),
  ]);
  return 'data:image/png;base64,' + png.toString('base64');
}
let _crcTable = null;
function crc32(buf) {
  if (!_crcTable) {
    _crcTable = new Int32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      _crcTable[n] = c;
    }
  }
  let c = -1;
  for (let i = 0; i < buf.length; i++) c = _crcTable[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ -1) >>> 0;
}

async function probeImages(page, fixtures, opts) {
  return await page.evaluate(async (F) => {
    const B = window.__board, D = B.L0DATA, MAP = B.MAP, PK = D.packed || {};
    const cvs = document.querySelector('.l0wrap canvas');
    if (!cvs || !MAP) return { ok: false, why: 'no canvas' };
    const ctx = cvs.getContext('2d');
    const dpr = cvs.width / cvs.getBoundingClientRect().width;
    const px = (x, y) => ctx.getImageData(Math.round(x * dpr), Math.round(y * dpr), 1, 1).data;
    const near = (p, hex, tol) => {
      const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
      return Math.abs(p[0]-r) + Math.abs(p[1]-g) + Math.abs(p[2]-b) <= (tol || 40);
    };
    const geo = PK.geo || { gutter: 148, headRow: 76 };
    const settle = () => new Promise(r =>
      requestAnimationFrame(() => requestAnimationFrame(r)));
    const wait = ms => new Promise(r => setTimeout(r, ms));

    const v = MAP.view;
    const k0 = v.k, ox0 = v.ox, oy0 = v.oy;
    const node = D.l0[0];
    const saved = { photo: node.photo, kind: node.photoKind, cl: node.photoClearance };

    /* Park the chip at a known screen position, blown up so the 11px slot is 22px
       and its corners are addressable. The whole point is to read the SHAPE of the
       drawn tile, and at the opening scale the slot is five pixels wide. */
    const K = 2, SX = geo.gutter + 30, SY = geo.headRow + 30;
    const place = () => { v.k = K; v.ox = SX - node.x*K; v.oy = SY - node.y*K; };
    const slot = () => {
      const size = 11*K, h = node.h*K;
      return { x: SX + 7*K, y: SY + (h - size)/2, size };
    };

    const read = async () => {
      place(); MAP.repaint(); await settle();
      await wait(450);                 /* the image loads and repaints itself */
      place(); MAP.repaint(); await settle();
      const s = slot();
      /* A signature of the whole slot, not two samples. The glyph is thin type and
         a single pixel through it is luck; what the fallback claim actually needs
         is that the slot comes back to EXACTLY the state it was in with no image
         at all, which a byte sum states and a sampled pixel does not. */
      const d = ctx.getImageData(Math.round(s.x*dpr), Math.round(s.y*dpr),
                                 Math.round(s.size*dpr), Math.round(s.size*dpr)).data;
      let sig = 0, ink = 0;
      for (let i = 0; i < d.length; i += 4){
        sig = (sig + d[i]*7 + d[i+1]*13 + d[i+2]*17) % 2147483647;
        if (!near([d[i], d[i+1], d[i+2]], '#12171d', 18)) ink++;
      }
      return {
        centre: [...px(s.x + s.size/2, s.y + s.size/2)],
        corner: [...px(s.x + 2, s.y + 2)],
        sig, ink,
      };
    };

    const out = { ok: true, id: node.id };
    /* before: the class letter, no image anywhere near the slot */
    node.photo = null; node.photoKind = null; node.photoClearance = null;
    let r = await read();
    out.beforeCentreIsFixture = near(r.centre, F.portraitHex) || near(r.centre, F.markHex);
    const glyphSig = r.sig, glyphInk = r.ink;
    out.glyphInk = glyphInk;

    node.photo = F.portrait;
    node.photoKind = F.swapKinds ? 'mark' : 'portrait';
    node.photoClearance = 'clears';
    r = await read();
    out.portraitCentre = near(r.centre, F.portraitHex);
    out.portraitCorner = near(r.corner, F.portraitHex);

    node.photo = F.mark;
    node.photoKind = F.swapKinds ? 'portrait' : 'mark';
    node.photoClearance = 'clears';
    r = await read();
    out.markCentre = near(r.centre, F.markHex);
    out.markCorner = near(r.corner, F.markHex);

    /* A URL that cannot resolve. The class letter is a supported state; a broken
       image box is not, and neither is an empty slot. */
    node.photo = F.deadUrl || 'https://127.0.0.1:9/there-is-no-such-image.png';
    node.photoKind = 'portrait'; node.photoClearance = 'clears';
    r = await read();
    out.deadUrlDrawsNoTile = !near(r.centre, F.portraitHex) && !near(r.centre, F.markHex);
    /* Identical to the no-image state, pixel for pixel, and carrying the letter's
       ink rather than an empty box. */
    out.deadUrlSigMatchesGlyph = r.sig === glyphSig;
    out.deadUrlInk = r.ink;
    out.deadUrlKeepsGlyph = r.sig === glyphSig && glyphInk > 0 && r.ink === glyphInk;

    node.photo = saved.photo; node.photoKind = saved.kind; node.photoClearance = saved.cl;
    v.k = k0; v.ox = ox0; v.oy = oy0;
    MAP.repaint(); await settle();
    return out;
  }, { ...fixtures, ...(opts || {}) });
}

(async () => {
  const layout = JSON.parse(fs.readFileSync(
    path.join(ROOT, 'data', 'l0-layout-model.json'), 'utf8'));
  const restDrawnFigure = layout.current.figures.restDrawn;

  const browser = await chromium.launch(launchOptions({
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  }));
  /* 2000x1150. The REASON for this size changed on 27 August and the old one is
     recorded here because it explains the shape of the file.

     It used to be load-bearing. Chips only existed above `view.k >= 0.62`, the map
     opens fitted, and a 1600x1000 window fits at 0.45 -- so the board opened as a
     grid of counts, every chip probe found nothing, and five checks went red the
     moment the fitted default landed. 2000px was the smallest round window whose
     fit cleared the threshold.

     Cell mode is now an explicit opt flag that no scale turns on, so chips draw at
     every width and none of that applies: `no-fit-lands-in-cells` asserts exactly
     that, at 1366 through 2560. The size is kept because a larger window puts more
     chips fully on screen, which the coordinate and colour probes want, not
     because anything breaks below it. */
  const page = await browser.newPage({ viewport: { width: 2000, height: 1150 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message.slice(0, 200)));

  await page.goto(URL, { waitUntil: 'load', timeout: 180000 });
  await page.waitForSelector('[data-view="CASES"]', { timeout: 120000 });
  await page.waitForTimeout(6000);

  /* THE PACKED MAP IS ITS OWN VIEW as of 29 August 2026 -- it used to be the rest
     state of NETWORK, and NETWORK is now the force-directed full graph. So this
     navigates to the new tab. That is the ONLY concession this file makes to the
     inversion: not one assertion, threshold or poison below is relaxed, because
     these 30 checks found two defects that reading the source did not, and the
     tenth poison moves every chip 60px on the real page and requires the match to
     collapse. A check weakened to accommodate a change stops being evidence that
     the change was safe.

     The entry surface still sits on top of the map until a reader picks a way in,
     and still has to be got past before there is a canvas to read. */
  await page.click('[data-view="PROGRAM"]');
  await page.waitForTimeout(2500);
  const skip = await page.$('.l0entry [data-entry-skip], .l0entry [data-skip]');
  if (skip) { await skip.click(); await page.waitForTimeout(1200); }
  else {
    await page.evaluate(() => {
      const e = document.querySelector('.l0entry');
      if (e) e.remove();
    });
  }
  await page.waitForSelector('.l0wrap canvas', { timeout: 30000 });
  await page.waitForTimeout(1500);

  /* THE GUTTER GOES FIRST, and the ordering is load-bearing in the same way the
     image tile's is. fitSweep clicks FIT ALL, and FIT ALL folds the rail to its
     spine -- which REMOVES `.rail-fold` from the document, because applyChrome owns
     the tab and only draws it on the open state. Measured after fitSweep the probe
     returns -1 for everything and the check fails while proving nothing about the
     map. Measured here it reads the rest state, which is the state a reader is
     actually in when the two band labels are covered. */
  const p = {};
  {
    const honest = await bandInkUnderRailTab(page, 0);
    const poisoned = await bandInkUnderRailTab(page, 120);
    p.gutterInk = honest.ink; p.gutterTabW = honest.tabW; p.gutterClear = honest.clear;
    p.gutterInkPoison = poisoned.ink;
  }
  Object.assign(p, await probe(page, { restDrawnFigure }));
  Object.assign(p, await fitSweep(page));
  /* The image tile is measured BEFORE headSweep, and the order is load-bearing.
     probeImages parks a chip at a known screen position and sets the camera by
     hand; headSweep resizes the window four times, and every resize fires the
     ResizeObserver that re-fits the map, which throws that camera away. Measured
     the wrong way round: three image checks went red reporting an empty chip slot
     that was in fact simply somewhere else. Every resizing pass runs last. */
  const FIX = { portrait: pngFixture(0xff, 0x00, 0xff), portraitHex: '#ff00ff',
                mark:     pngFixture(0x00, 0xff, 0x00), markHex:     '#00ff00' };
  const im = await probeImages(page, FIX);
  Object.assign(p, await headSweep(page));
  Object.assign(p, await overlaySweep(page));
  Object.assign(p, await railSweep(page));

  const hard = errs.filter(e => !/font|ERR_CONNECTION_RESET|404|favicon/i.test(e));
  const lines = [], fails = [];
  const record = (pass, label, detail) => {
    lines.push(`${pass ? 'ok  ' : 'FAIL'}  ${label}${detail ? ' :: ' + detail : ''}`);
    if (!pass) fails.push(label);
  };
  record(hard.length === 0, 'no page errors while the map is mounted',
         hard.slice(0, 2).join(' | '));
  for (const c of CHECKS) record(c.test(p), c.label, c.detail(p));

  /* The image tile, against injected fixtures -- measured above, before any pass
     that resizes the window. */
  const imgChecks = i => [
    { id: 'img-letter-is-default',
      label: 'the class letter is what draws when no image clears',
      pass: i.ok && i.beforeCentreIsFixture === false,
      detail: 'slot carries no fixture colour before injection' },
    { id: 'img-tile-replaces-letter',
      label: 'a cleared image replaces the class letter in the chip slot',
      pass: i.ok && i.portraitCentre === true,
      detail: `centre carries the fixture (${i.portraitCentre})` },
    { id: 'img-portrait-cropped',
      label: 'a portrait is cropped to a circle',
      pass: i.ok && i.portraitCentre === true && i.portraitCorner === false,
      detail: `centre=${i.portraitCentre} corner=${i.portraitCorner} (corner must be empty)` },
    { id: 'img-mark-not-cropped',
      label: 'a mark is never cropped to a circle',
      pass: i.ok && i.markCentre === true && i.markCorner === true,
      detail: `centre=${i.markCentre} corner=${i.markCorner} (corner must carry the mark)` },
    { id: 'img-dead-url-falls-back',
      label: 'an image that will not load falls back to the class letter',
      pass: i.ok && i.deadUrlDrawsNoTile === true && i.deadUrlKeepsGlyph === true,
      detail: `slot is byte-identical to the no-image state (${i.deadUrlSigMatchesGlyph}),`
            + ` carrying the letter's ${i.glyphInk} inked px, not an empty box` },
  ];
  for (const c of imgChecks(im)) record(c.pass, c.label, c.detail);

  console.log(lines.join('\n'));

  if (SELFTEST) {
    /* Every check, shown rejecting the input it exists to reject. A check that has
       never been demonstrated failing is indistinguishable from a broken one, and
       the poison is applied to the probe rather than to the page so that the SAME
       predicate is exercised both ways. */
    console.log('\n--- self-test: each check against input it must reject ---');
    let bad = 0;
    for (const c of CHECKS) {
      const poisoned = c.poison(p);
      const stillPasses = c.test(poisoned);
      console.log(`${stillPasses ? 'BROKEN' : 'ok    '}  ${c.id} rejects its poison`);
      if (stillPasses) bad++;
    }
    /* And the one that matters most, run against the real page rather than against
       a doctored object: move every chip 60px right of where the check expects it
       and require the pixel probe to notice. */
    console.log('\n--- self-test: the pixel probe against a moved layout ---');
    const shifted = await probe(page, { restDrawnFigure, shiftX: 60 });
    const noticed = !CHECKS.find(c => c.id === 'chips-where-the-model-says').test(shifted);
    console.log(`${noticed ? 'ok    ' : 'BROKEN'}  the probe reads the canvas`
      + ` :: ${shifted.classHits}/${shifted.classProbes} still matched after a 60px shift`);
    if (!noticed) bad++;

    /* And the head strip, poisoned on the page rather than in the object: put the
       control row back where it used to sit relative to the labels and require the
       clearance check to collapse. This is the defect itself, reproduced. */
    console.log('\n--- self-test: the head strip against a control row moved onto it ---');
    /* Targets .l0head, not .l0ctl. The control row used to be its own absolutely
       positioned box and this poison moved it by setting `top`; it now sits inside
       the .l0head flex row, so `top` on it does nothing and this poison silently
       stopped poisoning -- the check went on passing while proving nothing, which
       is the exact failure this whole file exists to prevent. It was caught by the
       self-test going BROKEN, which is the self-test doing its job. */
    /* AND IT MUST MEASURE, not merely disagree. An earlier version of this poison
       re-ran probe() and asked head-row-clear about the result -- but the ink
       fields come from headSweep, not from probe(), so the predicate was reading
       the -1 default and "caught" the poison no matter what the page did. It would
       have reported ok on a board that was overprinting freely. Run the real
       measure, on the moved page, and require ink to appear. */
    await page.addStyleTag({ content: '.l0head{top:44px !important}' });
    await page.waitForTimeout(500);
    const collided = await eraInkUnderControls(page, 0);
    const caught = collided.ink > 0;
    console.log(`${caught ? 'ok    ' : 'BROKEN'}  the clearance check sees a control row on the labels`
      + ` :: ${collided.ink} px of era-head ink under the buttons once the row is dropped 44px`);
    if (!caught) bad++;

    /* The image tile, poisoned ON THE PAGE. Hand each fixture the OTHER treatment
       -- the portrait drawn by the mark path and the mark by the portrait path --
       and require the two shape checks to collapse. Nothing else in the render
       distinguishes them, so a check that survives this is not reading the shape,
       and the shape is the whole licensing claim: a seal cropped to a circle is a
       different mark. */
    console.log('\n--- self-test: the image tile with the two treatments swapped ---');
    const swapped = await probeImages(page, FIX, { swapKinds: true });
    for (const id of ['img-portrait-cropped', 'img-mark-not-cropped']) {
      const c = imgChecks(swapped).find(x => x.id === id);
      console.log(`${c.pass ? 'BROKEN' : 'ok    '}  ${id} rejects the swapped treatment`
        + ` :: ${c.detail}`);
      if (c.pass) bad++;
    }
    /* And a "dead" URL that in fact resolves. The fallback claim is that the slot
       returns to exactly its no-image state; an image that loads must break that. */
    console.log('\n--- self-test: the fallback against a URL that does resolve ---');
    const alive = await probeImages(page, FIX, { deadUrl: FIX.portrait });
    const fb = imgChecks(alive).find(x => x.id === 'img-dead-url-falls-back');
    console.log(`${fb.pass ? 'BROKEN' : 'ok    '}  img-dead-url-falls-back rejects a live URL`
      + ` :: ${fb.detail}`);
    if (fb.pass) bad++;
    /* img-letter-is-default and img-tile-replaces-letter are each other's poison:
       the first asserts the slot carries no fixture colour BEFORE injection and the
       second that it does after, both read from the same run on the same chip. If
       the probe were not reading the slot, one of the two would have to fail. */

    if (bad) { console.error(`\n${bad} check(s) accept input they must reject`); process.exit(1); }
    console.log('all checks reject their poison');
  }

  await browser.close();
  if (fails.length) {
    console.error(`\n${fails.length} FAILED: ${fails.join(' | ')}`);
    process.exit(1);
  }
  console.log(`\nPACKED LAYOUT CHECK PASSED — ${lines.length} assertions`);
})().catch(e => { console.error(e); process.exit(1); });
