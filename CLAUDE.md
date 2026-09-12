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

**Starting a fresh session?** Read `notes/HANDOFF-2026-09-04.md` after this. **It is the
current one.** It records the cutover: the new shell in `app/` is production, deployed by
`deploy.yml` after a green gate; the back button Stewart made a condition of the cutover;
the CRLF fingerprint fix in `build_app_data.py`; the NotebookLM export; and the analyst
plan that waits on his four answers. `notes/HANDOFF-2026-09-03-EVENING.md` is the one
before it and is still accurate on the Danny Jones corpus build (board 1,027 -> 1,057),
the L0 layout fix in `build_l0.py`, the ten dead citations and the things not to undo.
`notes/HANDOFF-2026-09-03.md`, the morning one, is history: its cutover recipe has been
carried out. `notes/HANDOFF-2026-09-01.md` is still accurate on
everything it records. Then `notes/RETHINK-2026-09-02.md`: on 2 September Stewart asked for the
whole dashboard to be rethought for sharing with research friends, and that note is the
assessment, the proposal (entity first, the orthogonal map by default, the full graph only
as a scoped neighbourhood, a new shell replacing the inherited one) and the phased plan.
Its Design brief is `notes/DESIGN-BRIEF-SHELL-2026-09-02.md`; nothing in phases 1 to 5 is
built until Design's mockups are in and Stewart has signed them off. It points at `notes/AUDIT-FABLE-2026-09-01.md`, a 27-finding audit of the
whole repo with the fixes recorded in its section 2a, and at the transcript phase now
running on Stewart's machine. `notes/HANDOFF-2026-08-30-NIGHT.md` is the one before it and
is still accurate on the label fix, the OOM fix and the podcast tooling (this paragraph
pointed at the EVENING handoff for a day after NIGHT was written; the pointer is part of
the handoff). `notes/HANDOFF-2026-08-30-EVENING.md` carries the sixteen-node research pass
and the Design hand-over. `notes/HANDOFF-2026-08-30.md` is the morning brief before those
and is still accurate on the map inversion, the patents tab and the FOIA layer.
`notes/HANDOFF-2026-08-29-MAPS.md` is the brief those answer and all three of its builds
are now done. `notes/HANDOFF-2026-08-29.md` is superseded and accurate only on what it lists
as done.

`notes/HANDOFF-2026-08-27-shell.md` is the last SHELL handoff and is still accurate on the
shell: it is usable and both panels fold on a curve in both directions. Its statement that
the image register is at 12 is stale — it is 13 and at its ceiling
(`notes/IMAGE-CEILING-2026-08-28.md`). **The DEPLOY is SOLVED, 30 August 2026:**
`.github/workflows/deploy.yml` deploys on every push to `master` once the gate is green,
with the Cloudflare credential held as a repository secret that no session can read. The
live board is **https://the-program-zxz.pages.dev**. Note the `-zxz`, which Cloudflare
appended because `the-program.pages.dev` was already taken by an unrelated project.
**Since the cutover of 3 September 2026 that hostname serves the APP**: the build of
`app/`, uploaded as `app/dist`, and not the single-file old shell. The review site
**https://the-program-next.pages.dev** stays what it is: the place a build is looked at
before it goes to production. `DEPLOY.md` leads with the automatic route; the manual one
stays as the fallback and the analyst worker stays manual and Stewart's. `notes/SHELL-2026-08-27.md`,
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
programme, 1944–2026. What ships is the app in `app/`: a Vite build, hash-routed, its
data fetched at runtime from `/data`. Nothing about it is self-contained and nothing
needs to be, because it is served rather than opened from a disk.

**The single self-contained HTML file is the OLD shell**, `dist/the-program.html`, built
by `tools/build_dashboard.py`. It was the whole board until the cutover of 3 September
2026 and it is now retiring: it still builds, and the `gate` job still runs every check
against it, because it carries the bulk of the evidence over the research data and it is
the rollback if an app deploy is wrong. It is deployed nowhere. Its retirement is a
session of its own; §7 marks every file that goes with it. Its self-containment was
literally true only after 26 August 2026, because the typeface came from `fonts.googleapis.com`
on a render-blocking `<link>` inherited from the parent board, and first paint waited on
it. `notes/FIRST-PAINT-2026-08-26.md`.

| | |
|---|---|
| nodes | 1,057 (311 people · 746 entities) |
| hand-written sourced edges | 2,460 |
| tiered claims | 5,303 — T1 3,367 · T2 1,422 · T3 514 |
| edge tiers | regenerate; they moved with the 3 September build |
| unique source URLs | 3,541 |
| dead citations | 0 as of the 3 September evening sweep. Ten were found that day (nine on cufon.org, which is gone as a site) and repaired against opened documents the same evening; `notes/HANDOFF-2026-09-03-EVENING.md` section 5 |
| timeline events | 913 |
| pages | 10: Home · Node · Map (label and cell modes) · Neighbourhood · Thread · Timeline · Patents · Evidence · Report · not-found |
| primary map | the force-directed full graph, all 1,057 nodes. **Inverted 29 August 2026** |
| program map (L0) | 137 nodes, all with dossiers, on the app's Map page |
| map layout | Design's packed cells: 7 bands x 5 columns, 137 chips at one size |
| links drawn at rest | 128 of 394, by the model's own budget |
| FOIA layer | 17 requests linked to 121 open questions across 42 nodes, none filed |
| shipped artifact | `app/dist/`: `index.html`, hashed `assets/`, and `data/`, `fonts/`, `patents/` copied from `app/public/`. Gitignored and built in CI |
| old shell artifact | `dist/the-program.html`, 17,294,938 bytes. Still built, still gated, deployed nowhere |
| gate | 57 verify checks + 40 audit re-derivations + 51 runtime + 31 canvas + 20 analyst assertions over the old shell, plus the app's own C1 to C19 and all 19 poisons, all self-tested |
| analyst | live for every reader since 2 September 2026 via the Worker. **Since 11 September 2026 it has TOOLS**: twelve of them, defined and run in the reader's own browser against `/data`, so it can search, filter, count, group, trace a path and read the timeline across the whole board rather than only the page in view. It is on every route as a dock at the foot of the window, with chips per route kind. `notes/ANALYST-TOOLS-2026-09-11.md` |

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
  **Tier 2** unless the claim is about *what they said*. **This applies to edges too, since
  1 September 2026.** `merge.py` caps an edge whose every source is an interested-party
  domain unless its note attributes, and `research/_edge_tiers.json` carries the per-edge
  decisions a regex cannot make (an office publishing its own report is a primary record;
  a domain-to-domain inference is Tier 3 however official its citation). A `verify.py`
  check re-derives the rule. Before that date 82 such edges rendered "Tier 1 - documented"
  with nothing adjudicating them.
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
python3 tools/build_app_data.py
```

**`build_app_data.py` is last and it is not optional.** It writes `app/public/data/`,
which is what the shipped app reads, from the same sources everything else here reads,
and it must run after `build_dashboard.py` because it consumes `data/foia-links.json`
that the dashboard build generates. It joined this list on 3 September 2026: until then
nothing in CI ran it, so the committed data under `app/public/data/` could drift from
`research/` with the gate staying green, and after the cutover that drift is what a
reader sees. `python3 tools/build_app_data.py --check` re-derives every count in
`index.json` from the sources and fails on drift; `--self-test` shows `--check` rejecting
a board with one node removed.

**Fixed, 4 September 2026: `app/public/data/` is reproducible across platforms.** It was
not, for two reasons, and both were values that moved when the content had not. First,
`index.json` carried `"sourceCommit"`, the short id of whatever `.git/HEAD` named at build
time, so the committed copy recorded the commit BEFORE the one that shipped it. It is no
longer written at all. Second, `"source"` hashed the input files' raw bytes, and this repo
has no `.gitattributes`, so a Windows clone with `core.autocrlf=true` gets CRLF in every
text input while Linux CI gets LF: the identical commit hashed `3c5aa769b9d2` on the
machine that built the committed data and `e5835f8cdaf3` on CI, and the gate's `app` job
went red on every push over seven files by one line each plus `index.json` by two.
`source_hash()` now normalises CRLF to LF before hashing and reads nothing from `.git` and
no mtimes. `generated` was never part of this: it is the newest `generated` string among
the inputs, so it already agreed. Proven by rebuilding from an LF copy of the inputs and
diffing: all 1,067 files byte-identical. So the gate's `app` job compares with a plain
`git diff --quiet -- app/public/data/`, with no `-I` flags, and a local pipeline run no
longer leaves `index.json` dirty. `build_app_data.py` still stays out of the `Build` step
in `.github/workflows/gate.yml`, because the `app` job is where the app's data is checked
and checking it twice buys nothing.

Then the gate:

```
python3 tools/state_snapshot.py --gate       # state + the whole gate below, in one command
python3 tools/verify.py                      # 57 checks
python3 tools/verify.py --self-test          # every check shown rejecting bad input
node    tools/capture_strip.js               # writes tools/runtime-strip.txt from a real DOM
python3 tools/audit_independent.py           # 40 checks, deliberately independent
node    tools/runtime_check.js               # 28 DOM assertions in a real browser
node    tools/test_packed_layout.js          # 30 assertions read back out of the canvas
node    tools/test_packed_layout.js --self-test
node    tools/test_scripted_analyst.mjs      # 15 branch assertions
python3 tools/verify.py --idempotent         # slow: builds twice, requires identical output
python3 tools/check_rebuild.py               # committed artifacts == a fresh build
python3 tools/check_rebuild.py --self-test
```

**`check_rebuild.py` is what CI runs after rebuilding, and it exists because `git diff
--quiet` was wrong here.** Every artifact carries a build-DATE stamp, so a plain diff fails
whenever CI rebuilds on a different UTC day from the machine that built the commit — which
happened at 00:01 on 30 August. It normalises the stamp on both sides and compares full
bytes. **Do not "simplify" it to `git diff -I<regex>`**: three of these artifacts are a
single line each, so the one changed line always contains the stamp and every real change to
them would be silently ignored.

**Every command in that gate block drives the OLD shell**, `dist/the-program.html`. It is
deployed nowhere since the cutover of 3 September 2026, and these steps stay exactly as
they are until it is retired in its own session: they are still the bulk of the evidence
over the research data, and the app's checks do not yet replace them. §1 says why.

The four browser steps among them need that shell served over HTTP -- `file://` does not
work for a 17MB page. Run `node /opt/node22/lib/node_modules/http-server/bin/http-server
dist -p 8899 --silent &` first, or point `BOARD_URL` at wherever you are serving it.
`--gate` checks whether anything is serving it and **names the skip** rather than
reporting a failure that has nothing to do with the board.

### The app's own checks

Nineteen checks, C1 to C19, in `app/checks/run.mjs`. They drive the BUILD in a real
browser, not the dev server, so what they walk is what Pages would serve:

```
cd app
npm run build
npx vite preview --host 127.0.0.1 --port 4173 --strictPort    # background task
npm run check                                                 # C1 to C19
npm run check:poison                                          # all 19 poisons
POISON=c19 node checks/run.mjs                                # one poison, by name
```

**Start the preview as a background task, and spell out `--host 127.0.0.1`.** Plain
`npm run preview` binds IPv6 only here, and the checks fetch `127.0.0.1`, so they find
nothing and report the app broken when the app is fine. `--strictPort` makes it fail
loudly rather than quietly moving to 4174, which the checks would not be watching.
`APP_URL` overrides the address if you are serving it somewhere else.

**A poison is a deliberate corruption of the REAL page**, applied at one stop of the
itinerary, and the check named for it must be seen to fail on it. None of them touches a
predicate, a fixture or a probe; each changes what the browser has drawn. That is the
whole point: a check nobody has watched fail is not a check, it is a sentence. `npm run
check:poison` runs all nineteen and fails if any check survives its own poison.

And, separately, because it asserts nothing and cannot fail:

```
node    tools/look.js                        # 9 screenshots of the app -> dist/shots/
```

It reads `APP_URL` (default `http://127.0.0.1:4173`), so run it against the same preview
server as the checks. It exits 2 with a message when nothing is serving 4173.

**`test_packed_layout.js` reads the canvas, and that is the point.** It drives the **PROGRAM**
tab, not NETWORK — the two maps swapped roles on 29 August; see §9. The map is drawn with
`ctx.` calls, so for six sessions the standing assumption was that a cloud session could not
verify it -- `runtime_check.js` asserts through text nodes and there are none. `getImageData`
has no such problem. The check aims the camera at each of the 112 chips in turn and samples
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

| | can build & test | can push | can **look** at the app |
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
cd app
npm run build
npx vite preview --host 127.0.0.1 --port 4173 --strictPort    # background task
node tools/look.js                 # 9 shots of the app's screens -> dist/shots/
```

`tools/look.js` is a **camera, not a check**. It asserts nothing and cannot fail, and it
must never become a check: `app/checks/run.mjs` is the check, this is the eyes. The one
thing it exits non-zero for is a harness problem, nothing serving 4173 being the usual
one. Its sweep is one shot per surface a reader meets, plus the map a second time at
1366 wide, which Design's own note puts below the label floor. Every id in it is read out
of the data the preview is serving at run time: the node is the highest-degree node in
`index.json`, the thread the first in `threads.json`, the patent the first in
`patents.json`, so nothing in the sweep is written down by hand and goes stale.

> **It pointed at the old shell until 3 September 2026** and re-pointing it was a rewrite,
> not a config change. `BOARD_URL` is gone with the board it named: the old file's
> `[data-view]` tabs, canvas map, `.l0ctl` controls and `window.__board` have no
> equivalents here. The app is hash-routed and publishes `window.__app.map`,
> `window.__app.hood` and `window.__app.timeline` instead. `tools/walk.js` moved the same
> way and on the same day.

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
- **HAND things to Claude Design. Do not point at the repo.** §7 says "hand this to Design"
  about `data/design-extract.json` and that verb is load-bearing: a Design session starts with
  no memory of this project and reads GitHub, if at all, only when told the exact
  `owner/repo` AND the exact branch. A brief that opens "read `CLAUDE.md`, then these three
  notes" is a brief Design cannot act on, and on 30 August one was written that way and
  bounced. Every Design brief must be **self-contained** — it carries its own context, its own
  screenshots and its own figures — and anything it references must be **on `master`**, which
  means the PR is merged first. This is the unmerged-PR lesson above, wearing different
  clothes: the gate has 184 assertions and not one of them checks that a document written for
  somebody else is reachable by them.
- **Never paste the GitHub token into chat.** It lives in `.gh-token`, gitignored.
- **Token economy, agreed 3 September 2026 after a session that spent 71% of its usage on
  the orchestrator's own re-sent context.** The orchestrating session (Fable) does not read
  any file over about 10 KB; an agent reads it and returns the conclusion in under 40 lines.
  One phase per session (map; triage and verify; build and gate), each ending in a handoff
  note, or `/compact` at the boundary. Fan-outs run through one coordinator agent that
  launches its own subagents and reports once, or through the Workflow tool when Stewart
  says "use a workflow". Model ladder: Sonnet for mapping, sweeps, running the pipeline,
  gate, commits and deploys; Opus for triage, verification, builds, dossiers and any code
  change; Fable for decisions, reviewing agent output, decision lists and handoffs only.
  Waits are one background job that exits when the whole condition holds, not a poll that
  wakes the session every thirty seconds.
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
app/                                THE SHIPPED SHELL. Vite 5 + TypeScript, no framework,
                                    hash-routed on app/src/router.ts. `app/dist/` is the
                                    upload and is gitignored: CI builds it
app/public/data/                    the app's runtime data. GENERATED by build_app_data.py
                                    and COMMITTED, 1,067 files, 20MB. Do not hand-edit
app/public/_headers                 nosniff, referrer policy, cache rules. The only place
                                    the deployed app's headers are stated
app/public/_redirects               the old shell's path deep links, sent to hash routes
app/src/analyst/                    the analyst: tools.ts (the twelve tools, and they
                                    RUN IN THE BROWSER), client.ts (the tool loop and the
                                    cited-id guard), state.ts (the per-route CURRENT
                                    STATE), chips.ts, panel.ts (the dock)
data/analyst-suggestions.json       the analyst's chips, per route kind. Stewart's
                                    decisions only. build_app_data.py reads it and fails
                                    the build on a missing key or fewer than three chips
app/checks/run.mjs                  the app's gate: C1 to C19, each with a poison that
                                    damages the real page and must make its check fail
tools/build_app_data.py             writes app/public/data/ from the same sources as the
                                    rest of the pipeline. --check re-derives every count
data/the-program.json        8.6MB  the full board          } over GitHub's ~1MB
data/l0-model.json           6.5MB  map model + dossiers    } API read cap: they
dist/the-program.html       17.3MB  the OLD shell's build   } read as ABSENT
data/design-extract.json     336KB  purpose-built, readable. Hand this to Design
data/l0-layout-model.json    553KB  Design's layout output
data/l0-highlights.json             14 editorial start-here flags, signed off
data/l0-images.json                 image register, 13 records, at its ceiling
data/foia-links.json                GENERATED node -> FOIA request linkage. Do not hand-edit
research/patents-view.json          the patents content, authored and gate-checked
research/observables-view.json      the five observables, standalone so a later surface reuses them
research/threads.json               the eight authored chains behind the app's Thread pages
research/dossiers/                  per-node research
research/_authority.json            12 offices, each naming its instrument
research/_removed.json              approved removals + alias map
tools/                              the pipeline and the gate
tools/build_foia_links.py           derives data/foia-links.json from the letters. Runs inside the build
tools/make_drawing_thumbs.mjs       display derivatives for the patent sheets. Run by hand, output committed
notes/                              every session's findings and mistakes

OLD SHELL, staged for retirement. Still built, still gated, deployed nowhere:
tools/build_dashboard.py            builds dist/the-program.html by patching the file below
tools/l0_patches.py                 } the four renderers build_dashboard.py imports.
tools/network_patches.py            } The app renders all four of these surfaces
tools/patents_patches.py            } itself, from app/public/data/
tools/analyst_patches.py            }
ref/the-vanishing-v2.html           the parent board. build_dashboard.py patches THIS
tools/build_site.py                 assembled site/ for the old deploy. Nothing runs it now
```

**Retiring the old shell is a session of its own, not a delete.** `state_snapshot.py`,
`verify.py` (including `--idempotent`, which rebuilds by invoking `build_dashboard.py` by
name), `audit_independent.py`, `capture_strip.js`, `runtime_check.js`,
`test_packed_layout.js`, `test_scripted_analyst.mjs`, `precompute_layout.py`, `shoot.js`
and `check_rebuild.py`'s `BUILT` tuple all read `dist/the-program.html` or build it. A
deletion that leaves `dist/the-program.html` in `BUILT` turns `check_rebuild.py` red with
`unreadable`; the path has to leave that tuple in the same commit.

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

> **DONE, 3 September 2026: THE DANNY JONES CORPUS BUILD.** 136 episodes, mapped by
> 35 Sonnet agents across two sessions, 981 names cross-checked, six Opus triage groups,
> 36 candidates opened by six Opus verifiers, decided in
> `research/leads/CANDIDATES-2026-09-03-DANNYJONES.md`, built in
> `research/dannyjones-2026-09-03.json`: 11 people, 19 entities, 112 edges, 18
> corrections. Board 1,027 -> 1,057, claims 5,120 -> 5,303, L0 125 -> 137. Record:
> `notes/HANDOFF-2026-09-03-EVENING.md`. **Three things a next session must not undo:**
> the nitinol lineage now carries the NOL record beside the Battelle allegation (NASA
> SP-5110, NOLTR 61-75, patent filed 1 December 1961); `build_l0.py`'s layout uses its own
> `_sin`/`_cos` and `sqrt` of a sum rather than libm, because libm's last-ulp differences
> between Windows and Linux produced two different maps from one source and kept CI red
> for a whole day; and `gate.yml` uploads the rebuilt artifacts when the reproducibility
> step fails, which is the only way a Windows session can see what Linux built.

> **4 September 2026, cutover.** The new shell is production. Back button on every
> page (`app/src/history.ts`, check C17 with a poison), approved by Stewart on the review
> site; `deploy.yml` builds `app/` and deploys `app/dist`; `gate.yml` gained the `app` job;
> `_headers` and `_redirects`; `look.js` and `walk.js` re-pointed; sections 1, 3 and 7
> rewritten. Gate green at `e9d397b` once `build_app_data.py`'s fingerprint became
> content-only (CRLF-normalised bytes, no git id). NotebookLM export under
> `exports/notebooklm/`. Record: `notes/HANDOFF-2026-09-04.md`. **Do not undo:** the
> content-only fingerprint and the plain diff in the app job; `history.back()` as the
> button's only action; `/data/*` revalidating rather than immutable.

> **DONE, 2 September 2026 (afternoon): THE AREA 52 CORPUS BUILD.** 107 episodes of
> AREA52 - DEBRIEFED, transcribed, mapped by 27 Sonnet agents, cross-checked, triaged by
> six Opus agents, 35 candidates opened by seven Opus verifiers, decided in
> `research/leads/CANDIDATES-2026-09-02-AREA52.md` under Stewart's blanket approval of
> the day, built in `research/area52-2026-09-02.json`: 8 people, 22 entities, 79 edges,
> 20 timeline events, 20 gaps. Board 1,000 -> 1,027 (three duplicate pairs collapsed:
> william-moore, sue-gough, cia-haines-1997), claims 4,946 -> 5,120, L0 118 -> 125.
> **Two corrections a next session must not undo:** `sapoc` was established on 5 January
> 1994 with Deutch as chair (the November 1994 SAPOC bulletin), not on 1 July 2010; and
> ATIC was redesignated Aerospace Technical Intelligence Center in 1959 and discontinued
> on 1 July 1961 with FTD constituted the same day, so "ATIC became FTD" is wrong.
> `corpus_crosscheck.py` gained six rules the same day, each self-tested, after the
> triage agents caught false NODE verdicts (a false NODE deletes a lead). Record:
> `notes/HANDOFF-2026-09-01.md` section 9.

> **DONE, 2 September 2026: THE MICHELS CORPUS BUILD.** 140 Jesse Michels episodes
> transcribed on Stewart's machine, mapped by Sonnet subagents, triaged and verified by
> Opus subagents, decided by Stewart, built. `research/michels-2026-09-02.json`: 8 people,
> 12 entities, 76 edges, 7 timeline events, 8 gaps. Board 980 -> 1,000, claims 4,728 ->
> 4,853, L0 112 -> 118 (six nodes crossed the floor and gained dossiers in
> `research/dossiers/michels-2026-09-02-l0.json`). Record: `notes/HANDOFF-2026-09-01.md`
> section 7. **Four transcript claims are recorded as contradicted by the opened record**
> (Bluegill's date and contents, Inman and SAIC, the Church Committee's own access, Silver
> Bug's purpose); do not "fix" the nodes back toward the podcast. The build also fixed
> `tools/build_l0_layout.mjs`, whose main guard never fired on Windows and exited 0 having
> written nothing.
>
> **Same day, the section C pass.** What the 140 transcripts say about nodes the board
> already carried: six Opus verifiers, 93 attributed claims on 41 nodes in
> `research/_corrections.json`, every podcast claim at Tier 2 in the form "On <show>,
> <date>, <speaker> said". Nine Tier 1 claims came from documents opened on the way, the
> one that matters being **the Hippler letter of 16 January 1967** (nicap.org scan), now
> on `edward-condon`, `condon-committee` and `robert-low` with its disclaimer and its
> instruction in the same claim text. Seventeen named documents that were NOT opened are
> gaps in `research/michels-2026-09-02-c.json`. Claims 4,853 -> 4,946.

> **DONE, 30 August 2026: SIXTEEN NODES FROM THE VERIFIED LEADS.** Section A and section
> B of `research/leads/CANDIDATES-2026-08-30.md`, approved by Stewart. Record:
> `notes/HANDOFF-2026-08-30-EVENING.md`. Board 964 -> 980, claims 4,614 -> 4,728.
>
> **Four things a next session must not undo.**
>
> 1. **The exclusions are decisions, not gaps.** No Sarbacher-to-RDB edge, no
>    Trimble-recruited-Witten edge, no BDM-to-Northrop edge, and `sperry-rand` is
>    deliberately unattached because MacArthur has no node. Section E of the candidates
>    file says why for each. Each one looks like something missing.
> 2. **The section D corrections are load-bearing.** The Lockheed unaccounted-for total is
>    **11**, not 17 plus 46. The Moon Dust **49/17 figures are deorbit notifications
>    received, not objects recovered**. JANAP 146 carries no dollar figure; 18 U.S.C. 793
>    does. Neither Brown patent claims anti-gravity. Winterhaven contains no saucer.
> 3. **L0 went 110 -> 112.** `usaf` and `lockheed-skunk-works` crossed the floor of 6.
>    Note that §9's older text says `usaf` "is not on the map at all" under the correct
>    floor -- that was true and is now not. Both gained dossiers in
>    `research/dossiers/legacy-1947-86-l0.json`. All 31 canvas assertions still pass.
> 4. **A research record with no `cls` is dropped by `merge.py` in silence.** Seven
>    section B records were authored that way and 22 claims never reached the board while
>    every other check stayed green. `no research record is silently dropped` named all
>    seven by id. Fifth instance of §5 in these notes; do not weaken that check.

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
