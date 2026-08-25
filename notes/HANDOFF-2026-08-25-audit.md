# Handoff — the audit session

**Written 25 August 2026** at commit `a55d67b`, branch `claude/status-update-bewtdk`,
PR #3 open and mergeable. **Supersedes `notes/HANDOFF-2026-08-25-claude-code.md`**,
which was written at 04:38 by the Cowork session before any of this and now reads
stale: it says 18 verify checks (there are 38), and it lists as pending several
things that are done.

The one thing it says that has not aged: *"Do not take any figure in any document,
including this one, as current."* Run `python3 tools/state_snapshot.py --gate`.

---

## 1. What this session actually was

It started as "merge master, then do the remaining backlog". It became an audit,
because the first fix exposed the second and so on. **Six silent failures, two of
them introduced by this session and written up rather than quietly corrected.**

Nothing here threw an error. Nothing showed up in any check. The board built cleanly
through all of it, which is why it lasted.

| # | What | Scale |
|---|---|---|
| 1 | Nothing ever read `tools/REJECTS.json` | 30 claims dropped since written, 26 absent by any route |
| 2 | `norm_source()` discarded every source written as a bare string | 732 sources, 236 unique URLs, 76 reaching the board no other way |
| 3 | Edge `claimTier` was never audited by anything | 93 edges printed "Tier 1 · documented" on a Wikipedia page or YouTube video |
| 4 | 46 DIA reading-room URLs reach the index, not a document | 181 claims cited one, none with a second copy |
| 5 | The link probe asked HEAD and believed it | one dead citation hidden behind a 200 |
| 6 | The DIA repair itself fabricated 116 citations | caught by a golden-manifest drift of one URL |

Each has its own note. Read in this order if you want the reasoning:
`SILENT-REJECTS-2026-08-25.md`, `EDGE-TIERS-2026-08-25.md`, `SPOT-CHECK-2026-08-25.md`.

**The headline finding: no invented quotation exists on this board.** 604 claims quote
a document and cite a URL; every one was opened and checked. Six real defects were
found and fixed, all of them quotation-mark or citation errors rather than invention.

---

## 2. The two failures this session caused

Both are in the notes and the PR body. They are here too, because a handoff that only
lists what went right is the exact genre this repo keeps having to correct.

**The DIA remap fabricated 116 citations.** Applying it as a string replace across
`research/` rewrote Wayback capture URLs, because a capture URL *contains* its target:
`web.archive.org/web/<ts>/https://www.dia.mil/.../FileId/170054/`. Replacing the inner
id asserts the archive holds a snapshot, at that instant, of a page that did not carry
that id then. Repaired by keying on the capture timestamp and restoring each original
path; verified zero differ from the pre-remap file.

**The link probe hid a dead citation.** It asked HEAD, which a deleted blogspot post
answers with 200 while GET returns 404. Now a ranged GET.

Both surfaced the same way: **a number moved and I could not explain it.** The golden
manifest drifted by one URL, and chasing that one found 116.

---

## 3. State you are inheriting

Green, pushed, mergeable. Working tree clean.

```
956 nodes (278 people, 678 entities) · 2,159 edges · 858 timeline events
4,513 claims: T1 2,772 / T2 1,246 / T3 495   (61% rest on a primary record)
edge tiers:   T1 1,385 / T2   575 / T3 199
2,888 unique source URLs · zero dead citations
```

**Gate: 38 verify checks, every one self-tested**, plus 38 independent audit checks,
16 runtime DOM assertions, 15 analyst branch assertions, and two-build idempotency.
Was 27 checks at the start of the session.

New tools, both deliberately **outside** the build gate because they depend on the
network:

- **`tools/spot_check.py`** — every claim quoting a phrase of four or more words must
  have that phrase in the document it cites. `--links` sweeps all 1,328 cited URLs for
  reachability. `--host`, `--sample`, `--retry-errors`.
- **`tools/spot_cache_put.py`** — puts a file fetched by any route into spot_check's
  cache, so hosts that refuse curl but serve WebFetch (dia.mil, aaro.mil) can still be
  adjudicated by substring test rather than by a model's opinion.

---

## 4. What is actually open

**One decision, and it is Stewart's:** build the packed-cell layout in `mountL0`, or
keep the comp. The model is finished and all nine of Design's checks guard it. The
blocker is real and does not go away in a cloud session — the renderer is canvas and
`runtime_check.js` reads the DOM, so nothing here can catch overlapping chips or
unreadable labels, which is most of what makes a layout good. Comp:
https://claude.ai/code/artifact/afb7293f-6051-4686-b308-b68996f50ce9

**Still waiting on him:** the highlights sign-off table,
https://claude.ai/code/artifact/ecc7053d-63f5-4d6b-9de4-8e101048671e

**Research that should not run unattended:** priority 7, image sourcing for
`data/l0-images.json`. It turns on licensing judgements about real people's
likenesses, and the register is empty on purpose.

**Clerical:** priority 8, `notes/REQUEST-QUEUE.md`, 35 logged actions and the FOIA
queue.

**The honest remainder of the sourcing work:** 9 people rest on a single non-primary
source (`person_single_nonprimary_source` in `tools/INTEGRITY.json`). None rests on an
encyclopedia — that class is empty. Several of the nine are journalists, a pseudonym,
or foreign nationals with sparse official records, and may not be improvable.

---

## 5. Five things that will save you a day

1. **A host recorded as blocked should be re-tested, not trusted.** `cbc.ca`,
   `today.wayne.edu` and `compassrosepllc.com` were all written off by earlier passes
   and all answer now. Two of this session's best results came from re-testing.
2. **The fetch routes are not symmetric.** `army.mil` refuses WebFetch and answers
   curl; `dia.mil` and `aaro.mil` do the reverse. Try both before writing a host off.
3. **Never bulk string-replace a URL across `research/`.** See §2. Exclude
   `web.archive.org` explicitly and verify with a timestamp-keyed diff against
   `git show`.
4. **An unexplained count in the golden manifest is a finding.** `--update-golden` is
   for drift you can account for.
5. **Check whether a quoted sentence is the author's or a reader comment.** The board
   had attributed a commenter's words to Kevin Randle. Found by opening the page.

And the one that is really the same lesson as all of them: **a model's summary of a
document is not the document.** The USAF biography of Maj. Gen. McCasland was
summarised in a way that dropped "for Acquisition, Technology and Logistics" — the
only phrase separating his office from the one DIA's AAWSAP refusal was addressed to,
in the same months, on a node that already links this board to *The Vanishing*.
Asking for that line character by character is what stopped a serious error.

---

## 6. Your first task

Same as the last handoff said, and it was right: **do not build anything first.**
Run the gate, read `CLAUDE.md` §9, and confirm the state above against
`state_snapshot.py` rather than against this file.

Then ask Stewart about the layout. It is the only thing blocking, and it has been
analysed, costed and comped — it needs a decision, not more analysis.
