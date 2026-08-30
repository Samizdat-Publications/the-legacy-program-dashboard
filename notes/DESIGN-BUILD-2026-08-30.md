# Claude Design's five changes, built — 30 August 2026

Design's response to `notes/DESIGN-BRIEF-2026-08-30-STANDALONE.md`, built in the order they
specified. Their ordering is load-bearing and was followed: change 1 lowers the density that
2 and 3 are judged against, and doing it later would make them unmeasurable.

Stewart approved all five, and answered open decision 2 — **absent, not disabled** — which is
Design's own position, held loosely by them.

---

## What was built

| # | change | acceptance condition, measured |
|---|---|---|
| 1 | the map label carries the NAME only | every drawn label a single line at 1920×1080 ✓ |
| 2 | the drawn set is chosen by SPACE, never by rank | **0 overlapping boxes** at full extent, mid and close ✓ |
| 3 | pointer proximity, and nothing else | pointer off-canvas → settles then holds still; pointer in → drawn set changes, **no node moves** ✓ |
| 4 | warm arrival on the packed map | opens at `L0_LABEL_DROP` exactly; cold arrival unchanged ✓ |
| 5 | the two bridges, as two different controls | forward names the count, reverse names the coordinates, absent on the other 854, selection survives the round trip ✓ |

## 1. The finding that vindicates change 2 more than Design knew

Design rejected greedy-by-degree outright — *"Do not implement this even as an interim
step"* — because ranking labels by connectivity makes prominence a function of degree, which
is `CLAUDE.md` §4's "size must never encode importance" in different clothes.

**The board was already doing it, in two places.**

- `PLATE_DEGREE = 5` decided which **people** got a plate at all, and a plate is how a person
  is named on this map. So the most-connected people were named and the rest were anonymous
  dots.
- `LABEL_DEGREE = 12` gated the **entity** labels directly:
  `if (sel || hov || near || (scale > 0.62 && (n.deg || 0) >= LABEL_DEGREE))`.

Design was not warning against a hypothetical. It was describing the shipped behaviour without
having seen the source. Both gates are gone, replaced by the space budget.

A gate check now holds the line: **the least-connected drawn node has degree 1 while the
most-connected skipped node has degree 109.** If the set were a degree ranking that could not
be true.

## 2. Three judgements beyond the letter of the spec, flagged as such

- **Labels moved to SCREEN space.** Design requires "one size at every scale". Inside the
  world transform the font scaled with the camera, so it could not be one size. The marks stay
  in world space; only the type leaves it.
- **A person at rest is a dot plus a name, exactly like an entity.** This follows from change 1
  rather than being stated by it: once the plate carries only a name, a scaled box around one
  line of screen-space type is two treatments for one job. The full plate — photo, stripe,
  date, status — draws under selection and hover. It also makes the collision problem uniform
  across all 964 nodes instead of two-tier.
- **Middle truncation** borrows the packed map's rule, not its code. `l0Fit` is inside the
  other module's closure and a second copy of a renderer's own truncation is a thing this repo
  has been bitten by.

## 3. Change 4 did NOT reach the 31 canvas assertions, and that is the finding

Design predicted it would: *"this change does reach the 31 canvas assertions, because it
changes the scale the map can open at."*

It does not. `tools/test_packed_layout.js` navigates to PROGRAM with **nothing selected**,
which is a cold arrival, and the cold arrival is deliberately unchanged. All 31 passed
untouched on the first run after the change.

So the warm arrival would have shipped with nothing looking at it. A prediction about which
check will catch a change is itself a claim, and this one was wrong in the safe direction —
the check did not need weakening, it needed a sibling. `a warm arrival opens at the label
threshold` is that sibling, and it is **aimed at `L0_LABEL_DROP`, not at 0.62**, for the
reason `CLAUDE.md` gives by example: five canvas checks drove `v.k = 0.45` to reach dense mode
and would have passed while testing nothing the moment the constant moved.

## 4. Open decision 1, resolved by measurement

`notes/FIT-SCALE-2026-08-30.md` has the detail. **0.59 was the 1600×1000 figure and 0.74 is
1920×1080**; the brief carried the first attached to the words "at 1920" while its own
screenshot showed the second. Design caught the contradiction rather than building against it.

The measurement then made their case for them. With a selection open the dossier takes 640px
and the fit collapses to **0.19× at 1366, 0.29× at 1600, 0.45× at 1920** — below the 0.62
threshold on three of four common windows. A warm arrival that simply fitted would land a
reader on 110 unlabelled rectangles. Visible in
`notes/shots/2026-08-30-design/4-warm-arrival-and-forward-bridge.png`: the toolbar reads
`FIT 0.45×` while the map is `HELD` at 0.62 with its chip labels legible.

## 5. The checks, and both poisons

Eight new runtime assertions. Two page poisons, each demonstrated collapsing the thing it
names:

| poison | effect |
|---|---|
| `POISON=labels` | collapses every published box onto one coordinate. **17,578 overlaps against 0**, and `the overlap check can see an overlap` fires |
| `POISON=bridge` | neuters the forward command. The bridge is observed not landing — `view PROGRAM, .l0wrap true` — and the demonstration passes by seeing it |

**The published box list is bound back to pixels.** `MAP.labelBoxes()` reports what the
renderer says it drew; a check that trusted that alone would pass for a renderer publishing
fiction. `a published label box has label ink in it` samples the canvas inside 24 of them:
**24 of 24 carry ink.**

Two mistakes in writing those checks, both this file's own documented failure modes:

- **The first cut sampled the wrong canvas.** The map stacks three canvases of identical
  width in `.cwrap` — a WebGL edge layer that returns null for a 2D context, and two 2D
  layers — so "the widest" picks an arbitrary one of three. It reported `0 of 24` and the
  check was right to fail. It now samples the composite the reader actually sees.
- **The stillness check did not settle first.** `runtime_check.js` already records learning
  this: the renderer eases its camera and the layout settles, so a fixed wait passes or fails
  on luck. It now requires the canvas to go quiet **and then** stay quiet, which also fails
  correctly on a map that never stops moving.

A third: `POISON=bridge` originally cascaded into the reverse-bridge assertions, because the
neutered forward control leaves the reader on PROGRAM and the reverse control lives on the
network chrome. A poison should break the thing it names and nothing else. Fixed.

## 6. Not built

- **The FOIA queue page.** Design specified it inside Report, ranked by open questions closed
  and nodes touched, and marked it do-not-build-yet pending Stewart's yes and a design pass
  against the 17 real requests. Untouched.
- **The 8px label size.** Design: do not raise it and do not certify it either, until density
  is fixed and it can be judged against a field that is not fighting itself. Untouched.
- **The cold arrival below the label threshold at 1366 and 1600.** Recorded in
  `notes/FIT-SCALE-2026-08-30.md` §4 as a question for Design, not patched here.

## 7. Gate

Green on all ten steps including `--idempotent`. 31 canvas assertions still pass unmodified.
