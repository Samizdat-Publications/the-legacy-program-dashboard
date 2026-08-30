# The Program — working instructions

**Read this before touching anything.** It is the authoritative entry point. Where any
other document in this repo disagrees with this file, this file wins and the other one is
stale — several of them are, and they are named in §8.

**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private), branch `master`.
It is its own repository. `PROJECT.md` says it lives inside the-vanishing; that is no
longer true.

**Owner:** Stewart.

**Do not trust any figure in this file, or in any other document here.** Run
`python3 tools/state_snapshot.py --gate` — it derives every number from source and runs
the gate. The counts below are a sanity anchor, not a source of truth.

**Starting a fresh session?** Read `notes/HANDOFF-2026-08-30.md` after this. **It is the current
one.** `notes/HANDOFF-2026-08-29-MAPS.md` is the brief it answers and all three of its builds
are now done: the map inversion, the patents tab and the FOIA layer.
`notes/HANDOFF-2026-08-29.md` is superseded and accurate only on what it lists as done.

`notes/HANDOFF-2026-08-27-shell.md` is the last SHELL handoff and is still accurate on the
shell: it is usable and both panels fold on a curve in both directions. Its statement that
the image register is at 12 is stale — it is 13 and at its ceiling
(`notes/IMAGE-CEILING-2026-08-28.md`). **The DEPLOY is still outstanding and a cloud session
cannot run it** — there is no Cloudflare token in the environment, and `master` carries a
`<title>` fix that is committed and not yet deployed. `notes/SHELL-2026-08-27.md`,
`notes/SHELL-DOCK-2026-08-27.md` and `notes/DRAWERS-2026-08-27.md` are that day's working
records, in that order. `notes/HANDOFF-2026-08-26-UX.md` is still the best statement of the
original diagnosis; its §4 priority list is done.

**The lesson from 27 August is about process, not code: an unmerged PR is invisible to the
next session.** PR #5 held the whole of 26 August -- the authored chip labels, the denial
adjudication, the corrected §3 below, Design's shell response -- and sat as an open draft
while `master` stayed far behind. A session cut from `master` began blind and re-derived
what was already written down. Merge before handing off.
`notes/HANDOFF-2026-08-26-packed.md` is the previous one and is still accurate on the packed
layout and the pipeline. Two earlier handoffs from 25 August are **superseded** and should be read
as record only: `notes/HANDOFF-2026-08-25-audit.md` (still accurate on the source audit, but
its open list is stale -- the packed layout is built and the highlights are signed off) and
`notes/HANDOFF-2026-08-25-claude-code.md` (says 18 verify checks when there are 38, and
lists finished work as pending).

---

## 1. What this is

A research board mapping the alleged legacy UAP recovery and reverse-engineering
programme, 1944–2026. Single self-contained HTML file, no server, no runtime deps.
**Self-contained is now literally true and was not before 26 August 2026** — the
typeface came from `fonts.googleapis.com` on a render-blocking `<link>` inherited from
the parent board, and first paint waited on it. `notes/FIRST-PAINT-2026-08-26.md`.

| | |
|---|---|
| nodes | 964 (279 people · 685 entities) |
| hand-written sourced edges | 2,172 |
| tiered claims | 4,614 — T1 2,855 · T2 1,257 · T3 502 |
| edge tiers | T1 1,389 · T2 584 · T3 199 |
| unique source URLs | 2,941 |
| dead citations | 0 |
| timeline events | 872 |
| views | 9 — Network map, Program map, Patents, Timeline, Geography, Case files, Analysis, The cover-up, Search, Report |
| primary map | the force-directed full graph, all 964 nodes. **Inverted 29 August 2026** |
| program map (L0) | 110 nodes, all with dossiers, on the PROGRAM tab |
| map layout | Design's packed cells: 7 bands x 5 columns, 110 chips at one size |
| links drawn at rest | 103 of 326, by the model's own budget |
| FOIA layer | 17 requests linked to 121 open questions across 42 nodes, none filed |
| built artifact | `dist/the-program.html`, 15.6 MB |
| gate | 52 verify checks + 40 audit re-derivations + 46 runtime + 31 canvas + 15 analyst assertions, all self-tested |

Regenerate these numbers rather than trusting them; they move every research pass:
`python3 tools/state_snapshot.py`.

---

## 2. THE ONE RULE THAT NEVER BENDS

**No invented sources, URLs, document numbers or quotes. Ever, anywhere, including in
mockup copy, placeholder text and example data.**

If you need a placeholder, mark it unmistakably as one. If you cannot verify a citation,
say so and leave it out. This rule has no exceptions and no "just for now" case.

Corollaries that have already cost real time:

- **AARO is not a neutral source.** Claims sourced to `aaro.mil` or `defense.gov` cap at
  **Tier 2** unless the claim is about *what they said*.
- **An image URL is a sourcing claim.** `data/l0-images.json` is empty on purpose. A record
  there asserts an image exists at a URL under a licence. That needs verification, not a
  plausible-looking guess.
- **Two agents agreeing is not corroboration when they share a method.** Two independent
  research passes both "corrected" a statutory citation that was already right, and the
  correction had to be reverted.

---

## 3. How to build and check

Run from the repo root. **Order matters** — later stages consume earlier output.

```
python3 tools/merge.py
python3 tools/regrade.py
python3 tools/merge.py
python3 tools/build_l0.py
python3 tools/build_design_extract.py
node    tools/build_l0_layout.mjs
python3 tools/build_dashboard.py
```

Then the gate:

```
python3 tools/state_snapshot.py --gate       # state + the whole gate below, in one command
python3 tools/verify.py                      # 52 checks
python3 tools/verify.py --self-test          # every check shown rejecting bad input
node    tools/capture_strip.js               # writes tools/runtime-strip.txt from a real DOM
python3 tools/audit_independent.py           # 40 checks, deliberately independent
node    tools/runtime_check.js               # 28 DOM assertions in a real browser
node    tools/test_packed_layout.js          # 30 assertions read back out of the canvas
node    tools/test_packed_layout.js --self-test
node    tools/test_scripted_analyst.mjs      # 15 branch assertions
python3 tools/verify.py --idempotent         # slow: builds twice, requires identical output
```

And, separately, because it asserts nothing and cannot fail:

```
node    tools/look.js                        # screenshots the map -> dist/shots/
```

The four browser steps need the board served over HTTP -- `file://` does not work for a
13MB page. Run `node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899
--silent &` first, or point `BOARD_URL` at wherever you are serving it. `--gate` checks
whether anything is serving it and **names the skip** rather than reporting a failure that
has nothing to do with the board.

**`test_packed_layout.js` reads the canvas, and that is the point.** It drives the **PROGRAM**
tab, not NETWORK — the two maps swapped roles on 29 August; see §9. The map is drawn with
`ctx.` calls, so for six sessions the standing assumption was that a cloud session could not
verify it -- `runtime_check.js` asserts through text nodes and there are none. `getImageData`
has no such problem. The check aims the camera at each of the 110 chips in turn and samples
the pixel at that chip's own class rule, against coordinates `data/l0-layout-model.json`
states independently. It found two defects on the day it was written that reading the source
did not: see `notes/PACKED-LAYOUT-BUILD-2026-08-25.md`.

**Run `capture_strip.js` BEFORE `audit_independent.py`, every time.** Six of the audit's
checks compare the figures a reader actually sees against an independent re-derivation, and
they read those figures out of `tools/runtime-strip.txt`. That file is a capture, not a
source. A stale one makes the audit report a defect that is not there: on 25 August a
capture left over from a different build reported the duplicate collapse as two count
errors, and cost a handoff two findings that did not exist.

**All of these must be green before a push.** `--idempotent` is the one that catches a
whole class of bug: any pass that reads its own previous output back in.

### Where you are running

This project is worked on from three places:

| | can build & test | can push | can **look** at the dashboard |
|---|---|---|---|
| **cloud session** (web) | yes | yes, via the GitHub connection | **yes — `node tools/look.js`** |
| **local Claude Code** | yes | yes | yes |
| Stewart, by hand | yes | yes | yes |

**That row said "no" until 26 August 2026, and it was wrong.** Chromium is installed,
the board serves over HTTP, `page.screenshot()` writes a PNG and a session can open a
PNG. `notes/PACKED-LAYOUT-COST-2026-08-25.md` built a whole cost argument on the "no",
and `CLAUDE.md` §9 carried "no human being has seen it rendered" as the top priority for
a day while the means to look sat installed. It is the same shape as the `getImageData`
assumption in §5, one rung further out.

```
node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
node tools/look.js                 # sweeps four viewport sizes -> dist/shots/
```

`tools/look.js` is a **camera, not a check**. It asserts nothing and cannot fail. It
sweeps sizes because what the board does with its room changes across them: whether the
control row wraps onto the era heads, whether the fit clears the 0.62 label threshold,
how much of the window the dossier takes. Measured on 27 August, the control row is 25px
tall at 2560 and 149px at 1366.

> The reason given here until 27 August was that the map had **two opening states** --
> fitted, or 1:1 in the corner below the label threshold. It has one now: fitted, at
> every width, drawing real chips. Cell mode became an explicit opt the same day, so no
> fit can land a reader in the count matrix. `notes/SHELL-2026-08-27.md`.

**What is still true is the discipline.** Looking is now available, so use it — but
report what you actually saw and nothing more. Two limits worth naming:

- The captures are taken at `deviceScaleFactor: 2` and a PNG viewed scaled-to-fit shows
  small text **larger** than a 1x monitor does. Judge arrangement freely; do not certify
  the legibility of the smallest labels from a screenshot.
- A screenshot is one state. "The labels no longer overlap" is a claim about every state,
  and writing it from one capture is the same failure as a check that passes while broken.

Where you have not looked, still say "built, gate green, unverified on screen".

### Windows notes — for commands you hand Stewart, not for your own shell

A cloud session runs Linux and should use `python3` and forward slashes for itself.
This section applies only to commands written **for Stewart to paste**. He runs
**PowerShell 5.1**:

- `&&` is a **syntax error**. One command per line.
- **Always include the `cd`, quoted, in EVERY block — not just the first one on the
  page, and not just in documents.** This applies to commands written in chat as much
  as to `DEPLOY.md`. He pastes one block into whatever terminal is open; a block that
  assumes the previous block's working directory is a block that fails. It has already
  cost a session: `npx wrangler secret put` run from `C:\Users\stewa`, no config in
  scope, nothing to attach a secret to, and the error message named none of that.
  ```
  cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
  python tools\verify.py
  ```
- The interpreter may be `python`, not `python3`. Check once, then be consistent.
- The repo path contains **three spaces**. This has already broken a build script that used
  `new URL(...).pathname`, which percent-encodes them. Use `fileURLToPath`.

---

## 4. Working agreements with Stewart

- **EVERY terminal command he is asked to run must be a complete copy-paste block that starts
  with its own `cd`.** He does not read terminal commands and should not have to. Never write
  "from the repo root", never assume the previous block's directory, never hand him a bare
  command. One block, `cd` first, one command per line, nothing to work out. This has been
  corrected three times — 26 August 2026 — and each time it was in CHAT rather than in a
  document, which is why §3's version was not enough on its own.
- **COMMIT AND PUSH OFTEN. This is the default, not a courtesy.** Stewart, 29 August 2026:
  *"unless there's some reason not to, save our work after any big changes... especially if I
  ask for a session handoff."* Push after each substantial change rather than batching to the
  end of a session: a finished research pass, a working build, a note worth keeping. **A
  handoff request is an explicit instruction to commit and push first**, before writing
  anything about what happens next.
  The reason is not tidiness, it is that this project has paid for the alternative twice.
  PR #5 held a whole day's work as an open draft and the next session started blind and
  re-derived it. On 29 August a session spent roughly forty minutes re-deriving the Sheehy
  material that the previous session had already pushed, because nobody ran `git fetch`.
  A cloud container is reclaimed without warning and uncommitted work goes with it.
  The corollary, and it is the one that actually bites: **`git fetch --all` BEFORE reading a
  handoff, not after.** A handoff that says work is uncommitted may simply be wrong.
- **Clamp responses.** What you did, why, what you need from him. Detail goes in a repo note,
  not in chat.
- **No em dashes** in prose written for him. Tables are preferred over long lists. Charts get
  data labels.
- **Adversarial review does NOT apply to this project. Stop offering it here.** It exists for
  Stewart's employer work products — it recreates handing a deliverable to a reviewer, who looks for
  certain things, then to JD, who looks for others. This board has no Jess and no JD; its
  equivalent is the gate, which already runs every time. Offering the audit here reads as not
  understanding what the audit is for. (Told twice: 26 August 2026.)
- **He cannot read JSON.** When a JSON file needs his decision, render it as a table in chat
  and let him edit by line.
- **Never paste the GitHub token into chat.** It lives in `.gh-token`, gitignored.
- **Size must never encode importance** anywhere in the visual language. The largest node is
  AARO, which this board treats as implicated, not authoritative. Position is available;
  size is not.

---

## 5. The failure mode this repo keeps hitting

Stated four times in the notes in four different costumes. It is the single most useful
thing to internalise before working here:

> **A check that has never been shown to fail is indistinguishable from a broken one.**

Concrete instances, all real:

- `canvasInk` reported zero ink on a visibly drawing canvas and had never once fired.
- Six of six new verify checks were born broken and silently passing, because the poisoned
  fixture was built from a source that already contained the thing being tested for.
- A programmatic overflow test returned zero while the dossier panel visibly clipped every
  line at both edges — the panel fitted its element, and the element did not fit its grid
  track.
- The scripted-analyst test passed while **six of seven** suggestion chips routed to the
  wrong branch, because it asserted only that a long answer came back with valid commands.
  A check that cannot name the branch it expected cannot detect a wrong one.

- The packed layout's first cut pinned the band and column labels to the viewport and did
  not clip the map out from under them. Six chips rendered *beneath* the column-head plate
  at about 12% opacity. Nothing in the source said so; the pixels did.

**Therefore: every check you add must be demonstrated rejecting the input it must reject.**
`verify.py --self-test` enforces this and will flag any check that lacks a poison.

**And poison the page, not just the predicate.** Nine of `test_packed_layout.js`'s poisons
corrupt the probe object, which proves each predicate rejects bad input and nothing more --
a probe that always returned the expected colour would pass all nine. The tenth moves every
chip 60px on the real page while the expectation stays put, and requires the match to
collapse. It does: 29 of 110. That is the difference between a check that is self-tested and
a check that is *known to be looking at the thing*.

And its sibling rule: **reading the source is not verification.** Three times on 25 August a
check agreed with the implementation and a screenshot disagreed. For anything visual, look
at it -- and where you cannot look, find the channel that reads what actually rendered. On
this board that turned out to be `getImageData`, and the assumption that it was impossible
survived six sessions unexamined.

---

## 6. Two grading systems, and do not confuse them

They share three colours, which is a known weakness in the design.

- **Claim tiers 1-3 — evidence strength. 1 is strongest.** Ammunition grading. T1 documented,
  T2 a named person on the record, T3 stated inference. T3 is flagged by the file rather than
  by a critic, and is where research goes next.
- **Node tiers A/B/C — proximity to the programme.** Not credibility. A Tier A node carrying
  only T3 claims is not a contradiction; it is the definition of where to look next.

---

## 7. Where things are

```
data/the-program.json        6.9MB  the full board          } over GitHub's ~1MB
data/l0-model.json           5.7MB  map model + dossiers    } API read cap: they
dist/the-program.html         13MB  the built dashboard     } read as ABSENT
data/design-extract.json     285KB  purpose-built, readable — hand this to Design
data/l0-layout-model.json    461KB  Design's layout output
data/l0-highlights.json             14 editorial start-here flags, signed off
data/l0-images.json                 image register, 13 records, at its ceiling
data/foia-links.json                GENERATED node -> FOIA request linkage. Do not hand-edit
research/patents-view.json          the PATENTS tab's content, authored and gate-checked
research/observables-view.json      the five observables, standalone so a later surface reuses them
research/dossiers/                  per-node research
research/_authority.json            12 offices, each naming its instrument
research/_removed.json              approved removals + alias map
tools/                              the pipeline and the gate
tools/patents_patches.py            the PATENTS view. A renderer; its content is the two files above
tools/build_foia_links.py           derives data/foia-links.json from the letters. Runs inside the build
tools/make_drawing_thumbs.mjs       display derivatives for the patent sheets. Run by hand, output committed
notes/                              every session's findings and mistakes
ref/the-vanishing-v2.html           the parent board. build_dashboard.py patches THIS.
```

**The 1MB read cap is trap #7 and it has bitten twice.** A tracked, pushed, present file
over 1MB reads as *absent* to anything using the GitHub API. When briefing Claude Design,
cite `data/design-extract.json` and never the big three.

---

## 8. Stale documents — do not trust these

Fixed on 24 August but listed so you know the pattern:

- `PROJECT.md` — said the repo lives inside the-vanishing. It does not.
- `README.md` — carried counts from an earlier research wave.
- `TESTING-CHECKLIST.md` — asserted the no-key analyst was "already working as designed".
  It was answering questions about a different project entirely.
- `SESSION-HANDOFF.md` — dated 13 August, written *into* the session that ended on the 24th.
  Superseded by this file plus `notes/ANALYST-NOKEY-2026-08-24.md`.
- `WAVE3_QUEUE.md`, `CLAUDE-DESIGN-PROMPT.md` — historical. Useful as record, not as
  instruction.
- `notes/PACKED-LAYOUT-COST-2026-08-25.md` — **superseded in part, 26 August 2026.** Its
  layout description holds; its "what I cannot verify" table does not. It assumed a cloud
  session could not see the rendered board, which was the same wrong belief §3 carried.

**General principle: this board was built by porting a shell from a sibling project. Assume
every inherited surface is answering about the wrong project until someone has read it.**
Two were found on 24 August by accident, while looking for something else.

**And the sweep has a blind spot: it only ever looked at prose.** The 25 August pass
diffed prose string literals and found 177 survivors. It never read `<head>`, where three
inherited `<link>` tags sat pointing at Google — one of them render-blocking. Anything the
browser FETCHES is an inherited surface too. `verify.py` now asserts the built page fetches
nothing at runtime, so that specific hole is closed; the general lesson is that "inherited
surface" includes markup, not just copy.

---

## 9. What is next, in priority order

> **0. DONE, 25 August 2026.** `origin/claude/status-update-bewtdk` was merged into this
> line with Stewart's approval. `research/` did not conflict; both hand-edited tools
> auto-merged; every generated file was resolved by rebuilding. The two "genuine audit
> failures" the handoff reported were neither genuine nor failures -- both came from a
> stale `tools/runtime-strip.txt` captured off a different build. See
> `notes/AUDIT-STRIP-2026-08-25.md`. `tools/capture_strip.js` now generates that file.

> **DONE, 29-30 August 2026: THE MAP INVERSION, THE PATENTS TAB AND THE FOIA LAYER.**
> All three builds from `notes/HANDOFF-2026-08-29-MAPS.md`. Records:
> `notes/MAP-INVERSION-2026-08-29.md`, `notes/PATENTS-TAB-BUILD-2026-08-29.md`,
> `notes/FOIA-LAYER-2026-08-29.md`.
>
> | | |
> |---|---|
> | **The two maps swapped roles** | NETWORK is the force-directed full graph, primary. PROGRAM is Design's packed map, its own tab, always the whole map. Stewart's call after using the live board, and the sign-off `l0_patches.py` had waited for since 25 August — arriving in the opposite direction from what was built. |
> | **The patents tab** | Third in the rail. Content authored in `research/patents-view.json` and `research/observables-view.json`, not in the renderer. |
> | **The FOIA layer** | An open question names the request that would close it. Derived from the letters, which are derived from `REQUEST-QUEUE.md`. |
>
> **Three things a next session must not undo.**
>
> 1. **`tools/test_packed_layout.js` drives the PROGRAM tab.** It was navigated, not
>    weakened — all 31 assertions, every threshold and every poison intact. If it goes red,
>    fix the map, not the check.
> 2. **The particle rule now governs the default surface.** `l0_patches.py` ~2418: a particle
>    draws only on the SELECTED node's edges, running away from the reader, never along the
>    time axis. That was Design's ruling on a fallback; the inversion promoted it to the first
>    thing every reader sees. `e.pair.flip` must never steer a particle again.
> 3. **Content for the patents tab and the FOIA layer lives in data, not in a renderer.**
>    Both are gate-checked — every quotation against the transcript it cites, every request
>    against a question that is actually open. A string typed into `patents_patches.py` is a
>    string nothing checks.
>
> **Still open, and it is Design's:** the inversion **reverses Design's spec** — the packed
> layout was theirs, built to it, with 31 canvas assertions behind it, and it is now a
> secondary tab. They should see it. `notes/MAP-INVERSION-2026-08-29.md` §9 has the two
> questions worth their time.

> **DONE, 27 August 2026. THE SHELL. Kept as record — read `notes/HANDOFF-2026-08-26-UX.md`
> for the original diagnosis.**
> The data work is done and gated. What is left is that **the board is hard to use**, reported
> by Stewart from the live site on 26 August 2026 with screenshots. He is right on every point,
> and the four causes are located in the source, not guessed:
>
> | | where | what |
> |---|---|---|
> | **A** | `tools/l0_patches.py:253` | `L0_LABEL_DROP = 0.62` does **two jobs**: "labels off" AND "collapse to counts". Fit at 1920 lands at 0.608, so **FIT shows the count matrix instead of the map**. Split it: keep 0.62 for labels, add `L0_CELL_MODE = 0.30` for the collapse |
> | **B** | `tools/l0_patches.py:2568` | the dossier dock is `innerWidth * 0.5`. At 1920 the map gets under 40% of the window, so AUTO correctly re-fits it to 0.29x, which reads as broken |
> | **C** | `tools/l0_patches.py:2004` | `focus()` forces `view.k >= 1.15`, so a START HERE pick drops a first-time reader **inside** the map. It should CEDE and fit -- `showOnMap()` already does exactly that |
> | **D** | `.l0panel` | the node popover has no awareness of the measured `PAD.t`, so it prints over the crumb and the era heads |
>
> **A is the smallest change with the biggest effect and should go first.** When you split the
> constant, **re-read** the five canvas checks that drive `v.k = 0.45` to reach dense mode --
> at 0.45 that is no longer dense and they will pass while testing nothing. Aim them at
> `L0_CELL_MODE`, not at a literal.
>
> **Stewart proposed swapping the analyst and dossier docks** (analyst to the right rail,
> dossier to the full-width bottom strip). Endorsed, and for shape as much as for space: the
> dossier is prose and wants width, the analyst is a transcript and wants a column.
> **Do not build it without a mockup screenshotted at 1366 / 1920 / 2560 and shown to Stewart.**
> The last three layout changes built directly were all wrong on the first cut.
>
> **The tooling answer is `tools/walk.js`**, not a download: Playwright and Chromium are
> already installed. A camera, not a check, on the `look.js` contract -- click every control,
> screenshot each state, and record console errors, overlapping interactive rects, clipped
> text, map scale and map share of window into `dist/shots/walk/REPORT.md`. The overlap and
> occupancy records are the two that catch what Stewart is seeing, and no current check looks
> at more than the one state it was written for.

> **DONE, 26 August 2026: the two editorial decisions are answered and built.** Kept as
> record. Note that the answer to question 1 is what created UX defect A above -- cell mode
> and label-drop were answered with the same constant.
> ~~LOOK AT THE MAP~~ **DONE, 26 August 2026** — and the reason it sat undone is that §3's
> table said a cloud session could not. It can. `notes/LOOKING-2026-08-26.md` is the record.
> Four defects were found and fixed in the first pass, two of which no check could have
> stated: two of the five era column heads drawn underneath the DOM control row at every
> viewport size, and the absent-link cross printed on top of its own chip's label. A
> twelfth canvas assertion, `head-row-clear`, guards the first; its page poison moves the
> real control row back onto the labels and requires the clearance to collapse.
>
> **What is left is not a build task. Two questions for Stewart:**
>
> 1. **The whole map fits with labels only above about 1944px of window width.** On a
>    1920 screen it misses by 24px, opens at 1:1 showing three of seven bands, and the one
>    control that shows the whole map (OVERVIEW) is below the label threshold and so draws
>    110 anonymous rectangles. Reclaiming 24px from `geo.gutter` flips it. Lowering
>    `L0_LABEL_DROP` does not, honestly: 0.62 already admits a 5.9px label.
> 2. ~~**Label truncation at ~37 characters.**~~ **DONE.** All 110 L0 nodes now carry a `short`
>    and none of them exceeds 37 characters, so the truncation problem is closed. Verified
>    28 August 2026 by reading `data/l0-model.json` rather than by trusting this file.
>
> `disclosure` holding 3 nodes reads as deliberate on screen rather than broken — it is the
> last row of a descending order. Worth Stewart's eye, not a change from here.
>
> **UPDATE, 26 August 2026.** Question 1 is answered and built: below the label threshold
> the chips collapse and every cell prints its count, so OVERVIEW is the occupancy matrix
> rather than 110 anonymous rectangles. The 24px gutter question is therefore much less
> urgent — a 1920 screen now gets a readable whole-map view either way. Question 2 is
> ANSWERED IN FULL: labels middle-truncate so the distinguishing tail survives, and all 110
> `short` values are now authored.
>
> **All seventeen of Claude Design's checks now exist**, along with four this build added.
> See `notes/DESIGN-CONFORMANCE-2026-08-26.md` for the item-by-item state and for the five
> things that are genuinely left, none of which is code.


1. ~~**The COVER-UP view still carries the sibling board's skeptical record.**~~ **DONE,
   25 August 2026.** Three inherited surfaces found and removed, only one of which was
   the COVER-UP view. See `notes/INHERITED-SURFACES-2026-08-25.md`. Two gate checks now
   guard the class: `every edge type has a caption written for this board` and
   `no parent-board editorial content ships`.

2. ~~**Sweep every remaining inherited surface.**~~ **DONE, 25 August 2026.** Done by
   construction rather than by grep: diffing prose string literals between
   `ref/the-vanishing-v2.html` and the built file showed 177 that survived the port
   verbatim. Five rendered as false copy, and the analyst system prompt was inherited
   whole -- including a HARD RULE naming the axes **S, P and I** when this board scores
   on **C, A and D**. All fixed; `notes/INHERITED-SURFACES-2026-08-25.md` has the list.
   Three gate checks guard the class now, the third being
   `the analyst system prompt describes this board`. **Re-run the literal diff after any
   change to `ref/`** -- it is four lines of Python and it found what six sessions of
   reading did not.

3. ~~**The last 23 unsourced edges are an ACCESS problem, not a research problem.**~~
   **DONE, 25 August 2026, and the diagnosis was wrong.** They were not an access
   problem. `norm_source()` in `merge.py` silently discarded any source written as a
   bare string, and 732 sources across `research/` went that way -- 236 unique URLs, 76
   of which reached the board by no other route. Several sat on exactly those 23 edges,
   so a previous pass recorded them as UNSOURCED and went hunting for citations that
   were already in the file. **All 2,159 edges now carry a source.**

   That fix then exposed something worse, and it is the reason to read
   `notes/EDGE-TIERS-2026-08-25.md` before touching tiers: `remediate_tiers()` walks
   people and entities, and **edges were never in it**. Edge `claimTier` was whatever
   the research authored, merged by `min()`, audited by nothing, while rendering to the
   reader as "Tier 1 - documented". 93 edges held that grade on a Wikipedia article, a
   YouTube video or a blogspot post. 91 are now Tier 2; two gained the real document.
   A self-tested gate check and `edge_tiers` in the golden manifest stop it recurring.

   **The access facts in `notes/SOURCING-2026-08-25.md` still hold and still matter.**
   `web.archive.org` is unreachable from this environment entirely, so the board's many
   Wayback URLs cannot be verified from here and the usual fallback for a 403 does not
   exist. `govinfo.gov`, `archive.org` (including `archive.org/details/DTIC_*`, the
   Defense Technical Information Center mirror), `theblackvault.com` and `irp.fas.org`
   all answer. `dia.mil` and `aaro.mil` refuse curl but serve WebFetch. The govinfo
   search API answers with `DEMO_KEY` and rate-limits after roughly a dozen queries.

4. ~~**`data/l0-highlights.json` needs Stewart's sign-off.**~~ **DONE, 25 August 2026.**
   He kept all fourteen and cut none. `_status` in the file records it. The cap is 16, so
   two slots remain. The table stays live at
   https://claude.ai/code/artifact/ecc7053d-63f5-4d6b-9de4-8e101048671e — if the flags ever
   change, republish that same URL rather than building a new one. The flags now reach the
   built page as well: `L0DATA.highlights` was read by the analyst's "where do I start"
   branch and had never been written, and `merge_packed` writes it.
5. ~~**Implement Design's packed-cell layout and edge budget** in `tools/l0_patches.py`.~~
   **DONE, 25 August 2026.** Stewart approved the comp and asked for the build with all
   three options on. `notes/PACKED-LAYOUT-BUILD-2026-08-25.md` is the record.

   110 chips at one size, 7 bands by measured mean C, 4 eras plus NO DATE, 103 of 326 links
   at rest, 14 start-here pointers, 3 absent-link crosses. Everything already on the surface
   stayed: tier dashes, directional denials, tick counts, the ledger, both registers, the
   FULL GRAPH fallback. **The one thing nobody has done is look at it on a screen.**

   Two things to know before touching it again:

   - **The geometry is merged in `build_dashboard.py`, not `build_l0.py`**, because
     `build_l0_layout.mjs` runs between them. Merging it upstream would read a later stage's
     output from the *previous* build — the exact bug `--idempotent` exists to catch, and it
     would pass on build one.
   - **The gutter and head row are frozen chrome**, held in screen space and pan-clamped,
     not drawn in world space like the comp. The comp is one static full-view; the map pans.
     `clampView()` must be called from every place the camera moves. Miss one and the map
     opens right and then drifts, which is worse than never clamping.
6. ~~**Add Design's nine checks** from §5 of their response, each self-tested.~~ **DONE,
   25 August 2026.** All nine, each demonstrated rejecting the exact input Design named
   in the "must reject" column. They assert against `data/l0-layout-model.json`, which
   is a build product on disk rather than something embedded in the page, so they get
   their own poison channel in `--self-test`: `_LAYOUT_OVERRIDE`, the same pattern as
   the analyst check's `BREAK=1`. Note the model is generated but **not yet rendered** -
   the checks guard the spec, and item 5 is still to build against it.
7. **The image sourcing pass** for `data/l0-images.json`. Federal works are the strongest
   candidates (17 U.S.C. 105) but must trace to a `.gov` original, not an aggregator.
   Witnesses default to the class letter — a private person who testified has not licensed
   their likeness.

   **The RENDER half is built and tested, 26 August 2026** — it was being deferred under the
   same heading for no reason that survived examination. The stated reason, "a render branch
   with no data is untested code", is the argument for testing it, not for leaving it
   unwritten; leaving it unwritten meant whoever finally populated the register, after the
   hardest and least reversible research on this board, would be the one to find out whether
   the renderer worked. Five canvas assertions now exercise it against injected fixtures,
   including **the two treatments swapped**, because `photoKind` is load-bearing: a portrait
   may be cropped to a circle and **a seal may not** — a cropped seal is a different mark,
   and several carry statutory restrictions on alteration stricter than copyright. A verify
   check guards the register itself, because a malformed record does not error, it simply
   fails to clear and falls back to the class letter, which looks exactly like never having
   tried. `notes/IMAGE-TILE-2026-08-26.md`.

   **The register reached its ceiling on 28 August 2026 at 13 of 39 institutions**, and the
   remaining 26 are a finding rather than a backlog: no mark exists, or the mark is a wordmark
   that cannot survive an 11px square, or the body is private, foreign, or not an organisation
   at all. `notes/IMAGE-CEILING-2026-08-28.md` lists all three categories by node and says what
   would actually move it. **Do not re-run a Commons sweep expecting a different answer** --
   the searches for OUSDI, ISOO and House Oversight returned intelligence-law syllabi,
   conference photographs containing identifiable faces, and a scan of a redacted document.

   **The unattended rule is LIFTED, 27 August 2026, by Stewart:** *"licensing is for me to
   deal with on my end. You're just collecting the pictures for our project."* A session
   may collect and register candidate images without stopping for approval. What does not
   change is §2: an image URL is a sourcing claim, so every record must name a URL that has
   been opened and a licence basis that has been read. Collecting is unattended; inventing
   is still forbidden, and `clearance: "ask"` with the reason recorded is the honest state
   for anything unresolved rather than a guess in either direction.
8. **`notes/REQUEST-QUEUE.md`** — 35 logged actions, and the FOIA queue.
9. ~~**TESTING-CHECKLIST.md §12 source spot-checks**~~ **DONE for the mechanical half,
   25 August 2026.** `tools/spot_check.py` asserts that every claim quoting a phrase of
   four or more words has that phrase in the document it cites -- 604 claims qualify.
   **No fabricated source was found.** 278 of the 283 adjudicable claims quote their
   source correctly; five real citation defects were found and fixed and eight rotted
   `gov.br` URLs repointed. `notes/SPOT-CHECK-2026-08-25.md`.
   **The aaro.mil block is now done too:** all 24 quotes against the FY2025 and FY2023
   annual reports and HRR Volume I verify, fetched with WebFetch and adjudicated
   mechanically via `tools/spot_cache_put.py`. Two misquotes were found there and fixed,
   one of which mattered -- AAWSAP's purpose was quoted as assessing "long-range
   aerospace threats" where the HRR says "long-term and over-the-horizon foreign
   advanced aerospace threats".

   **`python3 tools/spot_check.py --links` is the other half:** a parallel HEAD sweep of
   every cited URL, 1,324 of them, in minutes. It asks whether the citation still
   reaches a document at all rather than whether the quote is right. **The board now
   has zero dead citations.** Four were found dead and repaired on 25 August. Only 404
   and 410 count as dead; everything else non-200 is the host refusing this caller and
   is labelled as such in the output. **The probe is a ranged GET, not a HEAD, and must
   stay that way** -- a blogspot post that answers HEAD with 200 and GET with 404 sat
   undetected until it was changed. Re-run it after any research wave -- link rot is silent and the board carries
   a lot of it.

   **What is left is item 10.** The tool is deliberately not in the build gate -- it
   depends on the network, and a check that fails because a host is throttling is a
   check people learn to ignore.

10. ~~**181 claims cite a DIA reading-room URL that no longer resolves.**~~ **ALL 46
    REPAIRED, 25 August 2026.** DIA renumbered its reading room and the old
    `FileId/1700xx/` ids now render the INDEX rather than a document -- `FileId/999999999/`
    returns the same page, so DIA falls back silently and a stale citation looks live.
    Every repair was verified by opening the document and reading its own title page,
    document number and page count, never by trusting a listing.

    **The last three were settled by the board's own claims rather than by their quoted
    text**, which is worth remembering next time: matching on the quote was hopeless
    because `170051`'s quote is the header common to all four Contract Status Briefs.
    The claims date the briefings, and only one brief bears each date. `170052` needed a
    further step because DIA released the 8 May 2009 briefing twice; the board cites
    `237616`, the fuller of the two at 12 pages against 11. `170018` was never a document
    citation at all -- its Tier 2 claim is about what the reading room LISTS, so it now
    points at the reading room.

    `tools/spot_cache_put.py` is the tool for this class: it puts a WebFetch-obtained
    file into `spot_check.py`'s cache so verification stays a substring test rather than
    a model's opinion. See `notes/SPOT-CHECK-2026-08-25.md`.
