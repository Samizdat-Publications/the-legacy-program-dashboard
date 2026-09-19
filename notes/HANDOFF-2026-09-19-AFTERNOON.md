# Handoff, 19 September 2026, afternoon (THE CURRENT ONE)

Follows `notes/HANDOFF-2026-09-19-LATE.md`, which is still accurate on the research and on
the nuclear cluster. This session took its section 2, "the first thing the next session
should do", and the mechanism defects in its section 5a. It then triaged item 3 of its
section 6c, the NSC and the EO/statute spine, and verified nine primary documents without
building anything from them yet.

`git fetch --all` first.

---

## 1. Where things are

**Master is unchanged at `d545a79`.** Nothing was pushed to it.

**Six commits on branch `fix/silent-defaults-2026-09-19`, pushed to origin.** Gate green,
app checks 87 of 87, all 21 poisons seen by their own check, `check_rebuild.py` clean.
Board counts do not move: 338 people, 787 entities, 2,661 edges, 1,050 timeline, so
`GOLDEN.json` is untouched.

| commit | |
|---|---|
| `f89996d` | the map's fade terminates, and takes the same time on every machine |
| `eb9c7f2` | the silent-default fix: 267 nodes onto their authored band, 24 people off a wrong `status` |
| `01b6ae1` | dates stop losing precision to filename order |
| `ffc1d76` | the nuclear blocker re-measured |
| `567edb4` | this handoff |
| `40c8b58` | the NSC and 1947-1985 spine, triaged and verified, nothing built |

**IT NEEDS STEWART'S YES TO MERGE.** Merging to master deploys to production, and the
harness treats that as his call.

```
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git checkout master
git merge fix/silent-defaults-2026-09-19
git push
```

Also local and NOT pushed: `trial/nuclear-on-defaults`, one commit, the nuclear cluster
merged on top of these fixes purely to measure the blocker. It is still red. Delete it or
keep it; it is not a candidate for master.

---

## 2. The audit that was asked for, and its answer

**`tier` and the C/A/D axes are NOT affected by the silent-overwrite defect, and never
could have been.** The late handoff expected them to be, on the grounds that they "run the
identical code path". They are DEFAULTED by the identical code path and MERGED by a
different one, and that is the half that decides it: `tier` defaults to `"C"`, the weakest
value, and `_merge_common` takes the strongest; the axes default to 0 and it takes the
`max`. Neither is order-dependent.

That is an argument, so it was measured. Rebuilding with the fix moved **0** nodes on
`tier` and **0** on C, A or D.

**The audit is closed. Do not re-open it without a new mechanism.** It was still the right
thing to do first, because it is what found `status`.

---

## 3. What it found instead

Full reasoning, with the numbers: `notes/SILENT-DEFAULTS-2026-09-19.md`.

| | |
|---|---|
| **person `status`, 24 people** | The one nobody was looking at. It defaulted to `"active"`, which is truthy, on a board whose subject is people who died or disappeared. Harry Reid, Gerald Ford, Kenneth Arnold, Nathan Twining, Edward Condon, Daniel Inouye, Stanton Friedman and Paul Bennewitz all shipped `active` while a research file said `dead`. Latent rather than on screen, but the analyst reads `nodes.json` in the reader's browser and would have said "active" |
| **`cluster`, 267 nodes** | Not the sixteen found by accident. The bigger half is the silent coercion: 132 research entries carry a `cluster` that is not a band at all, because the `_rs-*` source-set files use the field as their own provenance tag. Those sort first, so a tag expressing no opinion about the map beat every file that did |
| **dates, 14 entities** | Same family, different cause. `hearing-2023-07-26` shipped `dateStart: "2023"`; the node's own id knew the day. Where one date is a prefix of the other they agree and the longer one wins; where they disagree it is a research question, kept as-is and written to `tools/DATE-CONFLICTS.json`. 13 of those, and `geipan` at 1977 against 2005 is somebody's afternoon |

The fix is to **default late**: absence stays `None` until `finalise_defaults()` runs, after
every file has been read, so load order cannot reach the decision. The guard is in Layer 1
and **restates** the rule rather than importing it, per the late handoff's own lesson, and
it is poisoned.

---

## 4. `runtime_check` is not a flake, and never was

Three sessions have recorded it as intermittent. It is an animation with no last frame.

The inherited renderer eases the camera and every node alpha with `v += (target - v) *
0.12`, once per FRAME, and nothing snaps. Two defects in one expression:

- **It never arrives.** The gap shrinks by 12 per cent a frame and reaches zero at no frame
  at all, so "at rest" was an asymptote. The map only LOOKED still once the residual fell
  under one quantisation step of the canvas.
- **Its duration is frame rate.** 0.12 a frame is the half-second fade Design specified, at
  60fps. The gate's swiftshader browser draws this 18MB page at about **11fps**, where the
  same constant takes **four seconds**. Nobody chose a four-second fade.

Measured: after a select-then-clear the alphas were still moving 4.8 seconds later; the
check samples at about 2.1s. Six of six failures became five of five passes, and the fade
now completes in 800ms and holds exactly still.

**How it surfaced is worth keeping.** The data fix turned the check red. The documented
flake was the obvious explanation and it was wrong: six consecutive failures, against three
of three passes for the same commit's shell on the same port. A data change that moved 267
nodes simply left a larger residual at the moment the check looked.

---

## 5. `_corrections.json` is healthy. The late handoff's section 5a item 1 was wrong

It said the file "loads at position 1 of 104 and filters the claims accumulated SO FAR",
and asked someone to audit which corrections ever took.

- **The load order is the opposite.** `rank` sorts `_corrections` LAST, 103rd of 103, and
  that lambda is unchanged since the initial import. What loads first is the ten OTHER
  underscore files, which is a real hazard and is the one in section 3 above.
- **53 of 53 field corrections took effect**, and the single `removeClaims` rule took.

Two entries look wrong on a first pass and are not: `missing-scientists-probe-2026` repeats
the phrase its own rule removes, because the correction replaces an unattributed assertion
with an attributed one; `uap-science-advisory-council-2026` targets an id that
`_removed.json` aliased away, and its claim is on the alias target regardless.

Whatever happened to the Mansmann correction was specific to it. **Do not re-run this
audit.**

---

## 6. The nuclear blocker, re-measured, and the note's mechanism is disproved

`notes/PACKED-LAYOUT-INK-2026-09-19.md` sections 7 to 10 carry this.

Still red with the cluster merged on top of these fixes, chips 29 against cells 18. The
load-bearing half still passes at all eight window states, so nobody is landed in the count
matrix; only the corroborating `fitChipInk` fails.

**But the cost is no longer new cells.** That note's sections 3 and 4 build the structural
argument on "one new band-and-class cell costs about +7", and the L0 BUDGET adopted the same
day caps L0 at 135, so a cluster now displaces rather than adds. Counted off
`data/l0-model.json`, the distinct band-and-class cell count is **30 with and without** the
nuclear cluster, and no cell's occupancy moves by more than 3. Cell ink still rises 10 to 18.

`classInk` is a whole-canvas colour histogram: every 29th pixel within Manhattan distance 60
of one of five class colours, over the entire canvas, taken after the fit sweep with no
camera reset. How much of the canvas the map covers, and at what scale, is therefore an
input to the measure. That is the likely answer to the note's own question 2 and it is
recorded as a suggestion, not built. **Nothing in `test_packed_layout.js` was touched.**

Also tested and negative: correcting 267 nodes onto their authored band did not move this
measure at all. Master and the fixed branch both read 29 / 10.

---

## 7. What is next

1. **Stewart merges the branch** (section 1), or says why not.
2. ~~**The NSC and EO/statute spine is TRIAGED AND VERIFIED, ready to build.**~~
   **BUILT, on its own branch `research/nsc-eo-spine-2026-09-19`, one commit `f803638`,
   pushed.** Deliberately NOT on the fixes branch, so the merge in section 1 stays simple;
   merge the fixes first, then this. Board 1,125 to 1,136 nodes, edges 2,685, timeline
   1,059, Tier 1 claims +53, GOLDEN updated. Gate green, app checks 87 of 87, all 21
   poisons, `check_rebuild` clean. None of the eleven reaches L0, so `test_packed_layout`
   is untouched and the nuclear blocker is unaffected either way.
   **One thing in that commit is yours and was changed anyway:** three chips in
   `data/analyst-suggestions.json` quote board counts in their own text and the build
   refuses to run while they are stale, so the numerals were updated (1,125 to 1,136,
   1,050 to 1,059, 573 to 578) with `_figures` to match. No chip's wording or question was
   altered. If you would rather they had been left alone, say so and they can be reverted.
   The triage that produced it:
   `research/leads/NSC-EO-SPINE-2026-09-19.md`. Nine primary documents opened, with exact
   URLs, quotes and the hosts that refused. Read its section 5 first: six widely repeated
   claims about these documents are wrong on the primary text, and three of them are ones
   this board would plausibly have written. NSAM 303 is a two-sentence renaming memo with
   no secrecy content, so it belongs on the board as a correction rather than as part of
   the spine. NSDD 159 is the find: Reagan, 18 January 1985, ordering "a separate,
   specially compartmented control and access system at the Top Secret classification
   level for all policy matters concerning covert action", one designated focal point per
   agency. That is this board's own subject, forty years earlier than it currently shows
   it. Also settled before any research was done: NSC 10/2 is already carried in substance
   by `cia-office-of-policy-coordination`, so do not build a node that re-quotes it.
3. Canon passes 6 to 15.
4. Design still owns the three items in the late handoff's section 7, with item 1 now
   better specified.
5. Small and open, from `notes/SILENT-DEFAULTS-2026-09-19.md` section 8: person `status` has
   no validated vocabulary and probably conflates vital status with role status, which is a
   data-model question rather than a merge fix; `entity.sub` has 164 conflicting authored
   values and looks like two fields sharing a name; the 132 out-of-vocabulary cluster tags
   should move to a field of their own.

---

## 8. One process note

`npm run check` failed C18 once, immediately after `npm run build` replaced `app/dist`
under the already-running `vite preview`, then passed four consecutive times. A race between
the rebuild and the preview server is the likely cause. Recorded rather than concluded: one
failure and four passes is not enough to call it either way, which is exactly the mistake
the late handoff's section 5c is about.
