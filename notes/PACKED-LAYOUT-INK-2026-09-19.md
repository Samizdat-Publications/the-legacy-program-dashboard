# For Design: `fitChipInk` no longer scales with the board

> ## CORRECTION, later the same night. THIS NOTE'S CENTRAL CLAIM WAS WRONG.
>
> Everything below was written when the check was red at chips 31 / cells 16, and it
> concluded that **"there is no route to the threshold of 33 by building more."**
>
> **That was wrong, and building more is exactly what fixed it.** Two further clusters
> landed (the Disclosure Project and the propulsion strand, then Dulce), L0 went 142 to
> 149, and the check now PASSES at **chips 29 / cells 12**, which is 24 < 29 with margin.
>
> Note what actually moved: **cell ink FELL, 16 to 12.** Chip ink also fell slightly, 31 to
> 29. The packing scale shrank as the board grew (0.76 to 0.74 at 1920), and cell-mode
> numerals lost total ink faster than chips did. The note below reasoned only about chips
> rising and never considered that cells could fall.
>
> **The error, stated plainly:** three data points with chip ink flat at 30, 31, 31 were
> read as saturation and written up as a structural impossibility. Two flat points are not
> saturation. The measurement was fine; the generalisation from it was not.
>
> **What survives, and is still worth Design's time:** the per-cell cost is real. A new
> band-and-class cell cost about +7 when the ARV cluster opened one, and it took roughly
> forty more nodes to climb back out. So the check is not broken and not unfixable, but it
> **is sensitive to first-of-kind nodes in a way that has nothing to do with what the check
> is trying to assert**, and the current pass is a margin of 5 on a sampled-pixel measure.
> The next genuinely new kind of object may well turn it red again.
>
> So the questions in section 5 still stand. Question 3 should be read as "is a ratio the
> right shape, given the two sides move independently and one of them tracks the board's
> variety rather than its size", not as "the constant is unreachable".


19 September 2026. Stewart's decision, this session: hand this to Design as a
first-of-kind case, alongside the map cell panel item already theirs in
`notes/MAP-CELL-PANEL-2026-09-12.md`.

**Nothing in `tools/test_packed_layout.js` was touched.** It carries a poison and its
regression shipped to Stewart twice. This note is a measurement and a question, not a
proposed patch.

## 1. What fails

`tools/test_packed_layout.js`, check `no-fit-lands-in-cells`. It has two halves.

**The load-bearing half PASSES and has never regressed.** 8 of 8 fits at 1366, 1600, 1920
and 2560 in both FIT and FIT ALL still draw chips. Nobody is landed in the count matrix.
That is the defect Stewart hit on the live deploy twice, and it is not back.

**The corroborating half fails.** `fitChipInk` asserts:

```js
fitChipInk: cellInkChips > 0 && cellInkCells * 2 < cellInkChips
```

Both figures are class-coloured ink per ten thousand sampled canvas pixels, measured at
2000x1150: `cellInkChips` with chips drawn, `cellInkCells` with cell mode forced. The
claim it makes, in its own comment, is "forcing cell mode on the real page costs most of
the chip ink. A renderer that had stopped drawing chips entirely would flatten the two and
fail here."

## 2. The measurement, four builds on one evening

| build | L0 nodes | chip ink | cell ink | needs `cells x 2 < chips` |
|---|---|---|---|---|
| master, before any of this | 137 | 25 | 9 | 18 < 25 **passes** |
| + ARV cluster (2 new L0 nodes, 1 NEW CELL) | 139 | 30 | **16** | 32 < 30 fails |
| + TR-3B cluster (1 new L0 node, existing cell) | 140 | **31** | 16 | 32 < 31 fails |
| + Lazar cluster (2 new L0 nodes, existing cells) | 142 | **31** | 16 | 32 < 31 fails |

## 3. What the numbers say, and what they disprove

**`notes/ARV-BUILD-2026-09-18.md` section 4 named the wrong cause, and this session
disproved it by building the fix it recommended.** That note said the `witness x program`
cell holding a single node was the problem, and that filling it would "stop it being a
single numeral". TR-3B joined that cell. **Cell ink did not move: 16 before, 16 after.**
Filling a cell does not remove its numeral. The cell was never the variable.

**Adding L0 nodes no longer buys chip ink.** The Lazar cluster added two and moved chip ink
by zero. The plausible mechanism is that the map packs into a fixed extent, so more nodes
means proportionally smaller chips and roughly constant total ink. Design will know whether
that is right; the measurement is agnostic about why.

**So the two levers behave like this:**

| lever | effect |
|---|---|
| one NEW band-and-class cell | about **+7** on the cell side |
| one extra chip | about **+1**, and lately **0** |

A new cell therefore costs roughly fourteen chips to offset, and chips have stopped paying.
**There is no route to the threshold of 33 by building more.**

## 4. The structural point, which matters more than the failing number

The hub rule Stewart adopted on 18 September says: the thing claimed about is a node, it is
the hub, and every claimant runs into it. Its entire purpose is to put **kinds of object
this board has never carried** onto the map. A claimed craft. A claimed base. A claimed
material.

Every first-of-kind opens a new band-and-class cell. Every new cell costs about +7 on a
measure whose other side has stopped growing.

**So the check is structurally opposed to the modelling rule.** TR-3B was nearly free only
because the ARV had already paid for `witness x program`. The next genuinely new kind will
be expensive again, and the canon pass has thirteen more clusters to go.

There is also a calibration reading worth putting plainly. The 2:1 ratio was set when cell
ink was 9 and chip ink 25. Cell ink grows with the number of occupied cells, which grows
with the board. Chip ink is bounded by the packing extent. Those two do not scale together,
so the constant that fitted a 137-node L0 does not fit a 142-node one, and will fit a
200-node one worse. That is a different statement from "the renderer broke", and the
evidence says the renderer did not break: the load-bearing half passes at all eight sizes.

## 5. What Design is being asked

Not "make it green". The questions are:

1. Is the packing-extent explanation for flat chip ink correct?
2. Should `fitChipInk` measure a ratio at all, given that its two sides scale differently?
   Is there a formulation that still catches "the renderer stopped drawing chips" without
   penalising the board for carrying more kinds of object?
3. If a ratio is right, what should the constant be for a board that will keep adding
   first-of-kind cells?
4. Separately, and related: **`arv-fluxliner` and `tr-3b` are in L0 and
   `s-4-papoose-lake` is not.** Two of the three hubs built under the rule are on the
   top-level map and the third is not, so the convergence the rule exists to show is
   invisible for the Lazar cluster. That is a design question about what L0 selection
   should do with hubs, and it should be answered together with the above.

## 6. What is blocked on this

Branch `arv-regrade-2026-09-18`, five commits, all gated green except this one check:

| commit | |
|---|---|
| `065f305` | ARV cluster re-graded under the new centrality rule |
| `7a1c6df` | The congressional witness pass |
| `409a84f` | TR-3B |
| `6f937fa` | Lazar / S-4 |
| `09f6cfe` | The 19 September handoff |

CI runs `test_packed_layout` and would go red, so nothing deploys until this is answered.
Stewart declined the alternative, which was excluding both hubs from L0 to force a pass,
on the grounds that it hides them from the map and defeats the rule. That judgement is
recorded here so Design knows the cheap option was considered and refused.

---

# UPDATE, 19 September 2026, afternoon. The note's mechanism no longer holds.

Written after the silent-defaults session. **Nothing in `tools/test_packed_layout.js` was
touched here either.** This is a measurement that changes what Design is being asked, not
a patch.

## 7. The nuclear cluster was re-tested on top of today's fixes, and is still red

`nuclear-2026-09-19` merged onto the silent-defaults branch, rebuilt, board 1,159 nodes
and 2,738 edges. Trial branch `trial/nuclear-on-defaults`, local only, not pushed.

| | chips | cells | needs `cells x 2 < chips` | |
|---|---|---|---|---|
| master today | 29 | 10 | 20 < 29 | passes, margin 9 |
| silent-defaults branch | 29 | 10 | 20 < 29 | passes, margin 9 |
| **+ nuclear cluster** | **29** | **18** | 36 < 29 | **fails** |

The load-bearing half still passes everywhere: 8 of 8 fits draw chips at all four widths in
both FIT and FIT ALL. Nobody is landed in the count matrix. Only `fitChipInk` fails.

**Correcting 267 nodes onto their authored map band did not move this measure at all.**
That was worth testing, since the measure is indexed on band and class, and the answer is
no: master and the fixed branch are both 29 / 10.

## 8. THE COST IS NOT NEW CELLS ANY MORE, so section 3's lever table is out of date

Section 3 says one new band-and-class cell costs about +7 on the cell side, and section 4
builds the structural argument on it: every first-of-kind object opens a cell, so the check
is opposed to the hub rule.

**That mechanism cannot be what is happening here.** The L0 budget was adopted the same day
as that note. L0 is now capped at 135 rather than being a floor that grows, so a new cluster
DISPLACES members instead of adding them. Counted directly off `data/l0-model.json`:

| | L0 nodes | distinct band-and-class cells |
|---|---|---|
| silent-defaults branch | 135 | **30** |
| + nuclear cluster | 135 | **30** |

Identical. No cell opens, and the per-cell occupancy barely moves: the largest shift is
`witness x event` from 5 to 8, and no cell changes by more than 3. Cell ink still rises from
10 to 18, an 80 per cent jump, off a distribution that is nearly the same.

So the +7-per-new-cell model explained the ARV build and does not explain this one. Under a
budgeted L0 the two levers in section 3 no longer describe the system.

## 9. What `classInk` actually measures, which is the likely answer to question 2

```js
for (let i = 0; i < d.length; i += 4 * 29) {          // every 29th pixel
  ...
  if (Math.abs(r-c[0]) + Math.abs(g-c[1]) + Math.abs(b-c[2]) <= 60) hit++;
}
return Math.round(10000 * hit / tot);
```

Three properties worth naming, because together they explain why the number does not scale
with anything editorial:

1. **It is a histogram of the WHOLE CANVAS, not of the chips.** Any pixel within Manhattan
   distance 60 of one of five class colours counts, wherever it is and whatever drew it.
2. **The colour tolerance is loose.** 60 across three channels admits a wide neighbourhood,
   including antialiasing and any tinted background near a class hue. The comment already
   concedes this for the person grey, which is excluded for exactly that reason.
3. **The camera is wherever the preceding fit sweep left it.** `classInk` runs after the
   eight-state fit loop with only a viewport resize between, and no camera reset. So the
   fraction of the canvas the map covers, and at what scale, is an input to the measure and
   is not controlled.

Point 3 is the one that matters for a ratio. The packing extent changes when the board
changes, the scale at a given fit changes with it, and the share of canvas covered changes
with both. `cellInkChips` and `cellInkCells` are then two whole-canvas histograms taken at
whatever view the board's own geometry produced, which is not a property of "are chips being
drawn".

**A concrete suggestion for question 2, offered and not built.** Both halves of the
comparison should be taken at a PINNED camera, and ideally over the map's drawn extent
rather than the whole canvas. The assertion the check's own comment states, "a renderer that
had stopped drawing chips entirely would flatten the two", is a statement about the two modes
DIFFERING, and a renderer that had stopped drawing chips would put the ratio at 1.0. The
board is at 1.61 and has never been near 1.0. Whether the right constant is 2.0, a smaller
ratio, or a difference rather than a ratio, is Design's call, but the current 2:1 is being
asked to survive changes in camera and extent that have nothing to do with the thing it is
checking.

## 10. What this changes for the queue

Question 4 of section 5 is unaffected and still open. Questions 1 to 3 should be read against
section 8 above rather than against section 3: **the board is no longer growing its L0, so
"the board carries more kinds of object" is not currently the thing moving the number.**
Something about extent, scale or canvas coverage is, and pinning the camera would say which
in one run.
