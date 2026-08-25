# The packed-cell layout, built

**25 August 2026.** `CLAUDE.md` §9 item 5 is done. Stewart signed off the comp and asked
for the build, with all three options on:

> The arrangement looks good. Obviously on our live one we have the animated lines etc that
> design gave us plus all the other stuff for how to show that screen, but layout wise this
> looks good and want all 3 options turned on.

Item 4 is done in the same pass: all fourteen start-here flags kept, none cut,
`data/l0-highlights.json` now reads SIGNED OFF instead of DRAFT.

---

## What ships

The L0 program map draws Design's packed cells. Eras across, bands down, one chip size for
everything.

| | |
|---|---|
| chips | 110, all 205 x 20, verified 1 distinct size |
| world | 2200 x 912 |
| rows | 7 bands, ordered by measured mean C, descending |
| columns | 4 eras + a NO DATE column |
| links at rest | 103 of 326, chosen by the model's rule |
| start-here pointers | 14 |
| absent-link crosses | 3 |
| options | lines at rest, start-here, labels. **All three on.** |

Everything that was already on the surface is still on it: the tier dash channel, the
directional denial arrowheads, the tick counts with the numeral overflow, the member
ledger, the two registers, the tooltip, the FULL GRAPH fallback, focus on select.

## Where the geometry comes from, and why it is merged where it is

`tools/build_l0_layout.mjs` runs **after** `build_l0.py` and **before** `build_dashboard.py`.
So the merge happens in `build_dashboard.py`, which loads `data/l0-layout-model.json` and
hands it to `l0_patches.apply(..., layout=...)`. `merge_packed()` folds it into the model.

Doing it in `build_l0.py` instead would have meant reading a later stage's output from the
*previous* build. That is the one bug class `verify.py --idempotent` exists to catch, and
it would have passed the first build and failed the second.

`merge_packed` **raises** if the two models disagree on which nodes are on the map. A
partial merge puts some chips on the grid and leaves the rest at force coordinates, which
renders as a plausible mess rather than as an error.

The force layout is not thrown away. It is kept as `fx`/`fy`, because `build_l0.py` still
reports `wallClampPct` and `labelOverlaps` about it and a number describing a layout nobody
draws is the kind of quiet lie §5 is about. Nothing reads `fx`/`fy` at runtime.

---

## The thing the cost note said could not be done

`notes/PACKED-LAYOUT-COST-2026-08-25.md` has a table of properties with **"nothing here"**
in the second column: chips overlapping, a band clipping, labels unreadable at the opening
fit, the map opening on empty space. The stated reason was that `mountL0` draws to a canvas
and `runtime_check.js` reads the DOM.

**That reason was half right.** `runtime_check.js` cannot read a canvas because it asserts
through text nodes. `getImageData` can, in the same headless browser. And the packed layout
is the one surface where it is worth the trouble, because every chip's position is stated
independently in `data/l0-layout-model.json` — so the drawn pixels can be checked against
something other than the renderer's own opinion.

`tools/test_packed_layout.js` does that. Eleven assertions, each self-tested.

| assertion | what it reads |
|---|---|
| the map mounts as the packed grid | canvas present, 110 packed nodes |
| every node carries a chip rect | `x,y,w,h` on all 110, **1 distinct size** |
| no chip overlaps another on screen | projected rects, pairwise |
| the canvas is drawn on | content pixels as a share of the surface |
| **chips are at the model coordinates, in their class colours** | **the pixels themselves** |
| the map opens on chips, not empty world | opening view, chip count and scale |
| row and column labels survive a pan | label ink in both strips after panning to the far corner |
| the edges at rest are the ones budgeted | 103, against `figures.restDrawn` |
| all three options ship on | `MAP.opt` and the three controls |
| start-here pointers are beside chips, never on them | amber ink offset left of each flagged chip |

The fifth is the load-bearing one. For each of the 110 nodes the camera is aimed at it, and
the pixel at that chip's own left class rule is sampled and asked whether it is nearer the
node's class colour than the chip fill. **110 of 110.**

### The poison that matters

Nine of the poisons corrupt the probe object, which proves each predicate rejects bad
input. That is not enough on its own: a probe that always returned the class colour would
sail through all nine. It is exactly how six verify checks were once born broken and
silently passing.

So `--self-test` has a tenth, run against the real page: **every chip is moved 60px right
while the expectation stays where it was.** If the probe is reading pixels, the match
collapses. It does: **29 of 110**, and the check requires 110.

(29 rather than 0 because a chip shifted by 60px sometimes lands on a neighbour of the same
class. That is why the check demands all 110 and not a majority.)

### What it still cannot judge

Whether a truncated label is a *useful* label, and whether the thing looks good. Those
need eyes. **Nobody has looked at this on a screen.**

---

## Two real defects the check found, both fixed

Neither was visible in the source. Both were found by reading pixels.

### 1. The pinned column head was painting over chips

The furniture — band names down the left, era heads across the top — is pinned to the
viewport rather than drawn in world space, because a band label that scrolls away takes the
argument with it: the rows are ordered by measured mean C and **that order is the claim**.

The first cut pinned the labels but did not clip anything, so panning slid chips underneath
the head plate, where they rendered at about 12% opacity. The probe reported six chips whose
class rule sampled as a dark smear: `pursue-releases`, `ttsa-army-crada`, `uap-task-force`,
`ndaa-fy2024`, `iaa-fy2024-sec-1102`, `sol-foundation`.

Fixed with **frozen chrome**. The model already reserves `geo.gutter` (148) and
`geo.headRow` (46) and the cells start outside both, so those two strips are now held in
screen space, painted opaque, and the map is clipped and pan-clamped to what is left. A
chip can no longer be under them, and the hit test refuses the strips too — a target you
cannot see is not a target.

### 2. You could pan the map off into empty world

Falling out of the same fix. `clampView()` keeps the cells filling the content rect, and it
is called from **every** place the camera moves: drag, wheel, OVERVIEW, 1:1 READ, focus,
resize. Miss one and the map opens correctly and then drifts, which is worse than never
clamping, because it only shows up after an interaction.

`fitScale()` now fits the cells into the content rect rather than the world into the
canvas. Fitting the world would scale the reserved strips down with everything else and
then reserve them again at full size on top, losing a chip row at every viewport size.

---

## Divergences, stated rather than smuggled

| | |
|---|---|
| **frozen chrome** | The comp is one static full-view at world scale. The map pans, so the furniture is pinned and the content clipped. Defect 1 above is why. |
| **class rule on the chip** | A 3px rule down the chip's left edge, in the class colour — the same device the `document` mark used along its top. The comp has no class channel. Dropping it would lose information the board deliberately added, and a hue stripe is not a size. |
| **1:1 READ opens on the corner** | A banded grid does not want to open on its middle. The old code centred at 1.0, which on a 2200x912 world opens on the middle of the funding band with no column head and no band label in view. |
| **the breadcrumb counts differently** | It read "436 objects", one number over nodes and both edge kinds. At rest the map draws 103 of 326 links, so a single total told the reader they were looking at 326. Now: nodes, links at rest, links total. All three are checked by `audit_independent`. |

## D2 is no longer bent

The point cloud drew each node's member class mix as a 74px hue-only bar under its label.
The design system forbids carrying a category in hue alone, and the comment at that function
recorded it as a rule **bent rather than met**.

A chip has no room under it and does not want one. The mix is named in words in the tooltip
and grouped by class in the ledger. Same information, without asking hue to carry it alone.

## The gate

`python3 tools/state_snapshot.py --gate` now runs the browser steps too, and **names the
skip** when nothing is serving the board rather than failing for a reason that has nothing
to do with the board.

```
verify PASS · verify --self-test PASS · capture_strip PASS · audit_independent PASS
runtime_check PASS · test_packed_layout PASS · test_packed_layout --self-test PASS
test_scripted_analyst PASS · verify --idempotent PASS
```

`audit_independent` is 38 -> **40** checks, the two new ones re-deriving the links-at-rest
figure from `l0-layout-model.json` rather than from the number the model states about
itself.

---

## What is left on this surface

1. **Look at it.** Labels truncate to about 37 characters on a board whose labels are legal
   citations and document titles. The comp showed this and it is still true. It is the
   first thing worth arguing about, and no check here can settle it.
2. **The `disclosure` band draws 3.** Design predicted it in §6 and read it as the structure
   appearing rather than a fault. It is visible and it does look thin.
3. **The lines at rest are faint** against the band fills. Pixel polish, not layout.
