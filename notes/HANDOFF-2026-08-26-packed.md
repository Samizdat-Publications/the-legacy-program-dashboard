# Handoff — the packed layout shipped

**Written 25 August 2026, end of the session that built it.** This is the current handoff.
Read `CLAUDE.md` first, then this. Everything else in `notes/` is record.

---

## 1. Your first task is to look at something

The L0 program map now draws Design's packed-cell layout. It went in today, the whole gate
is green, and **nobody has seen it on a screen.**

Eleven canvas assertions say the 110 chips are exactly where `data/l0-layout-model.json`
puts them, that none overlap, that the labels and start-here pointers draw, that the row and
column names survive a pan, and that all three view options ship on. Not one of them can say
whether the thing *reads*.

Two problems the comp already showed, both still open, neither settleable by a check:

| | |
|---|---|
| labels truncate at ~37 characters | on a board whose node labels are legal citations and document titles |
| the `disclosure` band holds 3 nodes | Design predicted it in §6 and called it the structure appearing, not a fault. It still looks thin. |

If you can look: open `dist/the-program.html`, go to NETWORK, and say what is wrong. If you
are a cloud session and cannot, say so and do not pretend otherwise — `CLAUDE.md` §3 has the
table of what each environment can and cannot do, and "confirmed the labels no longer
overlap" written by something that rendered nothing is the same failure as a check that
passes while broken.

---

## 2. What this session did

Two decisions from Stewart, both acted on.

**The 14 start-here flags: all kept, none cut.** `data/l0-highlights.json` reads SIGNED OFF.
Two of the sixteen slots remain. A side effect worth knowing: `L0DATA.highlights` was read by
the analyst's "where do I start" branch and had never been written by anything.
`merge_packed` writes it now, so that branch stopped answering from an empty list.

**The packed-cell layout: built, with all three options on.** His words: *"The arrangement
looks good ... layout wise this looks good and want all 3 options turned on."* The full
record is `notes/PACKED-LAYOUT-BUILD-2026-08-25.md`. The short version:

- 110 chips, one size, 7 bands by measured mean C, 4 eras plus NO DATE, 103 of 326 links at
  rest, 14 pointers, 3 absent-link crosses.
- Everything already on the surface stayed: tier dashes, directional denial arrowheads, tick
  counts with the numeral overflow, the member ledger, both registers, the tooltip, the FULL
  GRAPH fallback, focus on select.
- Three controls — LINES AT REST, START HERE, LABELS — all on, all drivable from the chat
  input via `CMD.l0opt`.

---

## 3. Five things that will save you a day

**1. The geometry is merged in `build_dashboard.py`, not `build_l0.py`.**
`build_l0_layout.mjs` runs *between* them. Merging it upstream would mean reading a later
stage's output from the previous build — the exact bug class `verify.py --idempotent`
exists to catch, and it would have passed on build one and failed on build two.

**2. The gutter and head row are frozen chrome.** Held in screen space, painted opaque, with
the map clipped and pan-clamped to what is left. The comp is one static full-view; the map
pans, and a band label that scrolls away takes the argument with it, because the row order
*is* the claim. `clampView()` must be called from every place the camera moves: drag, wheel,
OVERVIEW, 1:1 READ, focus, resize. Miss one and the map opens correctly and then drifts,
which is worse than never clamping because it only appears after an interaction.

**3. `getImageData` works, and the assumption that it did not survived six sessions.**
The standing belief was that a cloud session could not verify the canvas map because
`runtime_check.js` reads the DOM. True of that file, false of the browser.
`tools/test_packed_layout.js` aims the camera at each of the 110 chips and samples the pixel
at that chip's own class rule. It found two real defects on the day it was written that
reading the source did not: the pinned column head painting over six chips at 12% opacity,
and a map you could pan off into empty world.

**4. Poison the page, not just the predicate.** Nine of that file's poisons corrupt the
probe object. That proves each predicate rejects bad input and nothing more — a probe that
always returned the expected colour would pass all nine. The tenth moves every chip 60px on
the real page while the expectation stays put, and requires the match to collapse. It does:
29 of 110, against a check that demands 110. Do the same for anything you add here.

**5. `state_snapshot.py --gate` now runs the browser steps.** It checks whether anything is
serving the board and **names the skip** rather than reporting a failure that has nothing to
do with the board. Start the server first:

```
node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
python3 tools/state_snapshot.py --gate
```

Nine steps, all PASS as of this handoff. It does not survive a container restart.

---

## 4. State

| | |
|---|---|
| branch | `claude/status-update-bewtdk`, PR #3 open |
| board | 956 nodes · 2,159 edges · 4,513 claims · 2,888 unique URLs · **0 dead citations** |
| map | 110 chips, packed cells, 103 of 326 links at rest |
| gate | verify 38 · audit 40 · canvas 11 · analyst 15 · idempotent — all green |
| highlights | 14, signed off |
| images register | 0 records, empty on purpose |

Do not trust that table. Run `python3 tools/state_snapshot.py --gate`.

---

## 5. What is actually open

**Beyond looking at the map**, two research items, both left undone deliberately rather
than forgotten:

1. **The image sourcing pass** (`CLAUDE.md` §9 item 7). `data/l0-images.json` is plumbed and
   empty. Federal works are the strongest candidates under 17 U.S.C. 105 but must trace to a
   `.gov` original rather than an aggregator, and witnesses default to the class letter —
   a private person who testified has not licensed their likeness. **This involves licensing
   judgements about real people's faces and should not run unattended.**
2. **`notes/REQUEST-QUEUE.md`** (item 8) — 35 logged actions and the FOIA queue.

And one metric worth a pass when there is nothing better: **9 people rest on a single
non-primary source.** `merge.py` reports it as `person_single_nonprimary_source`, split out
from the raw thin-sourcing count on purpose — chasing the raw number means padding strong
nodes to move it.

---

## 6. The standing cautions, all learned the hard way on 25 August

1. **Never bulk string-replace a URL across `research/`.** A `web.archive.org` capture URL
   *contains* its target, so replacing an inner path rewrote 116 capture URLs into assertions
   that Wayback holds snapshots it does not. That is a fabricated source in the precise sense
   `CLAUDE.md` §2 forbids, produced by the pass that exists to remove fabricated sources.
2. **The link probe is a ranged GET and must stay one.** A blogspot post answering HEAD 200
   and GET 404 hid a dead citation until it was changed.
3. **Check whether a quoted sentence is the author's or a reader comment.** The board had
   attributed a commenter's words to Kevin Randle.
4. **An unexplained count change in the golden manifest is a finding, not a formality.**
   A drift of one URL is what exposed the 116.
5. **A host recorded as blocked should be re-tested, not trusted.** `today.wayne.edu`,
   `cbc.ca` and `compassrosepllc.com` all came back. `web.archive.org` is still unreachable
   from this environment entirely.
