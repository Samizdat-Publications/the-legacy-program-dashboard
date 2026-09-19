# For Design: `fitChipInk` no longer scales with the board

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
