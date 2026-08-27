# The dock was a proportion doing a measure's job

**27 August 2026, second shell pass.** Follows `notes/SHELL-2026-08-27.md`. Two defects,
both in the state a reader reaches by selecting a node, which is the state Stewart's
original complaint came from and the one the first pass did not look at.

---

## 1. The register printed on the controls

`.l0reg` was pinned at `top:44px`. The control row it has to clear is measured.

The constant cleared a single-line strip by 9px and nothing else, so it read as correct
for exactly as long as nobody opened the dossier. Measured with a path open and a node
selected:

| window | control row | register covered it by |
|---|---|---|
| 2560 | 56px | 22px |
| 1920 | 87px | 53px |
| 1600 | 87px | 53px |
| 1366 | 118px | 84px |

And it covered them **from above**: `.l0reg` is z-index 5 against `.l0head`'s 4.

This is the era-head bug one layer up. That one was the canvas painting *under* the
buttons; this is the DOM stacking *over* them. Same cause both times, and the third
instance in this file of a constant standing in for something that varies.

**`.l0ledger` was never the culprit, and the reason is the fix.** It clamps to
`PAD.t + 6` in script rather than to a number in a stylesheet. `measureHead` now
publishes the measured reserve as `--l0-ctl` and `--l0-pad-t`, so CSS and canvas read
one value and the next overlay has something true to pin to.

---

## 2. The dock was half the viewport, and that was never right

`setDockOpen` used `Math.max(560, innerWidth * 0.5)`. Measured at 11.5px IBM Plex Mono
with a 6.9px advance, taken off the resolved face rather than assumed:

| window | dock | chars per line | map share |
|---|---|---|---|
| 1366 | 683 | 95 | 37% |
| 1600 | 800 | 112 | 37% |
| 1920 | 960 | 135 | 39% |
| 2560 | 1280 | **182** | 42% |

Comfortable measure is 45 to 75 characters and about 90 is the ceiling for sustained
reading. Every size busted it, and **the bigger the monitor the worse the dossier read**,
which is backwards. The panel was not wide because the prose needed it. It was wide
because a proportion was doing a measure's job.

That is also the measurable half of Stewart's report on 26 August: *"the right bar
expands to half the screen, you never actually get to see the full map."* Both halves of
that sentence have the same cause.

Capping at 640:

| window | dock | chars per line | map share |
|---|---|---|---|
| 1366 | 640 | 89 | 40% |
| 1600 | 640 | 89 | 47% |
| 1920 | 640 | 89 | 56% |
| 2560 | 640 | 89 | 67% |

Both surfaces win, which is why this is **not** the analyst/dossier swap and does not
need it. The swap stays deferred and may now be unnecessary.

A side effect worth recording: a narrower dock leaves the map wider, so the control row
wraps less. `head-row-clear` went from measuring a 149/87/56/25px row to an 87/56/56/25px
one at the same four widths.

---

## 3. What was NOT changed, and why

**Selecting a node still does not re-fit the board.** `focus()` sets `camMode = 'held'`
and remembers `focusId` so a later box change re-centres rather than re-fits. That looks
like the bug and is not: the comment records that re-fitting was tried and produced
**k=0.289 at a 1920 window, with the node nominally on screen and nothing on it
readable.** At 758px of room you cannot both keep a readable scale and show the whole
board, so the trade is deliberate. Capping the dock widens the room instead, which is the
only move that improves both sides.

**The node tooltip was left alone.** `.l0tip` is z-index 8 and would print over the
controls, but it is positioned at `my + 14` — always *below* the cursor — and chips only
exist below `PAD.t`, so it cannot reach the head band at any realistic window. Adding a
clamp would have been a guard that can never be shown firing, which is the thing §5 of
`CLAUDE.md` warns about. Recorded here so the next session does not re-derive it.

---

## 4. Checks

Two, both self-tested, both poisoning **the page** rather than the predicate.

| check | poison | result |
|---|---|---|
| `overlay-clears-controls` | puts `top:44px` back on the live page | 0px becomes 22px |
| `dossier-measure-capped` | puts half-the-viewport back | 89 chars becomes 112 |

`dossier-measure-capped` asserts a **floor as well as a cap**: a dock that collapsed to
nothing would sail through a cap-only check while making the dossier unreadable.

Gate: verify 46 + self-test, capture_strip, audit 40, runtime 28, canvas 29 + every
poison, analyst 15, `--idempotent`. All green.

**Not seen on a real monitor.** Captured headless at 1366 / 1600 / 1920 / 2560.
