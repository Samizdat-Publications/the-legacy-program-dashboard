# Session handoff — The Program

> **SUPERSEDED, 24 August 2026.** Read `CLAUDE.md` first — it is the authoritative entry
> point and carries current counts, the build order, the gate and the priority queue.
> This file is preserved as the record of the 13 August handoff. Its counts are stale.

**Updated 13 August 2026.** Supersedes the cloud-session handoff of 12 August, which is
preserved as `notes/SESSION-HANDOFF-2026-08-12-cloud.md`. Its counts are stale; ignore them.

---

## The repo is published

**https://github.com/Samizdat-Publications/the-legacy-program-dashboard** (private)

Pushed 13 Aug 2026 by Stewart from PowerShell, `master` tracking `origin/master`.

The owner namespace is `Samizdat-Publications`. Stewart says this is simply his own account,
so treat it as personal. **If** a token or app authorisation later fails to see the repo,
check whether the namespace is actually an organisation — a fine-grained PAT scoped to a
personal account cannot see an org repo and fails silently rather than usefully. Do not
assume it is an org; just check that first if auth misbehaves.

Claude still cannot push from a Cowork session (see job zero). Until that is fixed, commit
locally and hand Stewart this to run:

```powershell
cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
git push
```

---

## Job zero — get GitHub write access, and do not accept "I can't"

**Stewart wants Claude to own all GitHub work permanently**: publishing, version control,
branches, releases, and eventually a landing page. He has been blocked on this twice and is
rightly annoyed. **Solving it is your first task, before the audit.**

What is already known, so you do not repeat the dead ends:

- He connected the **claude.ai GitHub Integration** on 13 Aug. That powers file attachment in
  Chat, Projects sync, and Claude Code *remote* sessions. **It does not expose write tools to
  a local Cowork session.** Confirmed by tool search — queries for repo/push/commit return
  Notion, Zoom and Cloudflare, no GitHub.
- `plugin:engineering:github` is a **different** thing: a plugin-provided MCP server, present
  but unauthorised. It needs its own auth.
- The sandbox has **no `gh` CLI, no `GH_TOKEN`, no credential helper**. `apt-get install`
  fails (no root); `apt-get download` + `dpkg-deb -x` works.

Things to try, roughly in order:

1. `ToolSearch` for github tools first — the plugin MCP may be authorised by the time you
   run. Do not assume from this document; **check**.
2. If not, tell Stewart to run `/mcp` in an **interactive** Claude Code session to authorise
   `plugin:engineering:github`. A non-interactive session cannot run OAuth.
3. Failing that, a **fine-grained PAT** with `contents:write` on the one repo, exported as
   `GH_TOKEN`, lets plain `git push` work over HTTPS. Least magic, most reliable. Do not ask
   him to paste a token into chat — have him set it in the environment.

**Whatever you find, write the answer into this file** so the next session does not
rediscover it. If you get write access, take over completely: he should never run a git
command again.

**Terminal commands for Stewart must always include the `cd`**, quoted, so the block is
copy-pasteable as one unit. He has asked for this explicitly.

**He runs Windows PowerShell 5.1.** `&&` is a syntax error there — *"The token '&&' is not a
valid statement separator in this version."* A bash-style one-liner was sent on 13 Aug and
failed. Put each command on its own line rather than joining with `;`, because `;` runs the
next command even when the `cd` failed and can execute in the wrong directory. Paths use
backslashes and contain spaces, so always double-quote them.

---

## Your first job after that

**Read the project files and audit for errors. Do not implement anything yet.**

Stewart is running `notes/DESIGN-BRIEF-L0-MAP.md` through Claude Design and will attach the
result when he has it. Before that lands, the board needs a clean bill of health, because
the design work will be built on top of whatever is wrong now.

Start here:

```bash
cd the-program
python3 tools/verify.py --self-test     # every check must prove it can fail
python3 tools/verify.py --idempotent    # full pipeline twice, identical output required
```

Both must pass. Then read, in order: `PROJECT.md`, `notes/QA-PASS-2026-08-12.md`,
`notes/PERF-AND-DENSITY-PLAN.md`, `SCHEMA.md`, `notes/DESIGN-BRIEF-L0-MAP.md`.

**Then audit.** The obvious place to look is §4 of `QA-PASS-2026-08-12.md`, which lists what
was never tested — roughly 80% of `TESTING-CHECKLIST.md`. The highest-value item there is
**§12 data spot-checks**, which has not been started: open real source URLs and confirm the
claim says what the source says. A fabricated source outranks every other defect on this
board, and nobody has checked yet.

The second place is anything the four commits below touched. They were verified, but by me.

---

## What this board is

A network board mapping the legacy UAP recovery and reverse-engineering program and the
modern disclosure movement, 1944–2026. It reuses *The Vanishing*'s engine, schema and design
system with a different subject. **It is a separate project and belongs in its own GitHub
repo** — it currently sits inside the scientist-tracker folder only because that was the
mounted directory.

**Current state: 970 nodes · 246 people · 724 entities · 1,786 hand-written sourced links ·
4,108 tiered claims · 858 timeline events.** Load 1.6s, **104 fps on Stewart's machine.**

### Editorial stance — read before writing anything

Built from the premise that a legacy recovery and reverse-engineering program exists and has
been concealed. The question is not *whether* but **who, where, under what authority, and
paid for how.** No balanced both-sides prose. No skeptical disclaimers.

**AARO is not a neutral authority.** Witnesses have testified that under Kirkpatrick it
functioned to surface and neutralise whistleblowers rather than investigate. It is a
participant in the concealment. As of `0ae5e89`, claims sourced to aaro.mil or defense.gov
cap at Tier 2 unless the claim is *about what they said* — publishing on aaro.mil makes a
document a primary record **of the statement**, not of the fact asserted. AARO is still the
most connected node on the board (degree 62) because it genuinely is central; it just no
longer gets to be its own best evidence.

**Never bends: no invented sources, URLs, document numbers or quotes.**

---

## What happened this session (4 commits)

| commit | what |
|---|---|
| `5c0e7c5` | Fixed 4 BROKEN data bugs found in the first QA pass |
| `9b2a12b` | `tools/verify.py` — a gate that asserts, and that tests itself |
| `ac8fce7` | Baked the layout at build time + size-aware anchors: 19.8s → 1.6s |
| `c55b67b` | Stopped the sim running every frame; wrote the L0 design |
| `0ae5e89` | AARO/DoD interested-party sourcing rule |
| `3ddc765` | The design brief |

### The four original bugs, and why they matter to you

All four were in a board that had been "verified". None of them threw an error.

1. **The documented rebuild destroyed 35 dates on every run.** `regrade.py` scored a board
   that already contained its own previous overlay, so it skipped work it had already done
   and emitted a thinner overlay each time. Fixed by scoring a pristine re-merge.
2. **Five people were on the board twice**, splitting their edges and sources, with the twin
   rendering its own slug as its name. Two scripts had two copies of the id rules.
3. **Thirteen person plates rendered meaningless names** — five different people all showed
   as `JR., J.`
4. **The DETAIL panel stated the wrong number of entity classes.**

### The lesson, which is the important part

The only verification was `shoot.js`, which collects console errors. That asks *did anything
throw?* All four answered no. **Nothing asserted that anything was true.**

Worse: `shoot.js`'s one substantive check — `canvasInk`, meant to catch a blank map —
reported 0 ink on a canvas that was visibly drawing, and had never once fired. A check that
always passes and a broken check are indistinguishable from outside.

So `tools/verify.py` has two rules, and **please keep them**:

1. Every check asserts a fact and exits non-zero when it is false.
2. **Every check is itself tested.** `--self-test` feeds each one input it must reject.

Rule 2 paid immediately — three of the first eight checks were born broken and silently
passing. That is the expected rate. **If you add a check, self-test it.**

`verify.py` passing is the definition of shippable. `tools/GOLDEN.json` is a drift tripwire
requiring deliberate `--update-golden`. It has already caught one real change.

---

## Rebuilding

```bash
python3 tools/merge.py            # research/*.json -> data/*
python3 tools/regrade.py          # tiers, dates, coords -> research/_remediation.json
python3 tools/merge.py            # re-merge so the overlay lands
python3 tools/build_dashboard.py  # data + parent board -> dist/the-program.html
python3 tools/verify.py --idempotent
```

`build_dashboard.py` prints `all patches applied` or names failures. **Never ship a build
that printed a failure.** 39 patches currently.

`ref/the-vanishing-v2.html` is a **build input and is never edited.** All divergence lives
in `tools/build_dashboard.py` as named patches, which is what keeps the two boards in sync.

---

## Things that have already cost a full build cycle

- **There are two map implementations in the file.** The legacy one is dead at runtime. A
  patch raising the layout step count was applied to the *wrong* one, and reading the source
  did not reveal it — **the profiler did.** If you change map behaviour, verify at runtime.
- **The layout is baked at build time** by `tools/precompute_layout.py`, which slices the
  simulation source out of the built HTML and runs it in Node. There is deliberately only
  one implementation of the physics. If you change the physics or anchors, the bake picks it
  up — but check the wall-clamp figure stays near **3.7%**. It was 46%, and that was the real
  cause of the overlapping plates that had been logged as a density problem.
- **Measure before optimising, and measure before believing a comment.** I guessed rendering
  was the load bottleneck. It was under 1%. It was 60% force layout and 24% file parse.

---

## Environment gotchas (this cost real time)

- **The workspace is OneDrive-synced and `rm` fails with "Operation not permitted".** git
  cannot delete its own `index.lock`, so the second commit onward fails. Fix: call
  `mcp__cowork__allow_cowork_file_delete` once, then `rm -f .git/index.lock .git/HEAD.lock`.
  You will likely need this early.
- **`/tmp` and `~/.cache` are wiped between bash calls.** Playwright and its browsers must be
  installed and *used* in a single call, or reinstalled each time. Working recipe:

```bash
cd /tmp
[ -d /tmp/node_modules/playwright ] || { npm init -y >/dev/null 2>&1; npm install playwright >/dev/null 2>&1; }
export PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-browsers
[ -d /tmp/pw-browsers ] || npx playwright install chromium >/dev/null 2>&1
[ -d /tmp/libs/root ] || { mkdir -p /tmp/libs && cd /tmp/libs && apt-get download libxdamage1 >/dev/null 2>&1 && dpkg-deb -x *.deb ./root; cd /tmp; }
export LD_LIBRARY_PATH=/tmp/libs/root/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
CH=$(find /tmp/pw-browsers -name chrome -type f | head -1)
```

  `shoot.js` needs its `require('playwright')` and `executablePath` rewritten to those paths.
- **No root.** `apt-get install` fails; `apt-get download` + `dpkg-deb -x` works.
- **Headless fps is measured under SwiftShader software rendering and is NOT a proxy for real
  fps.** Headless showed 2–10 fps for a board doing 104 fps on Stewart's machine. What *is*
  machine-independent is JS-per-frame cost — that is what caught the `sim.alpha` regression.
  **Never quote a headless fps number to Stewart as if it were his.**

---

## Outstanding, in priority order

1. **Audit (your first job).** Especially `TESTING-CHECKLIST.md` §12 source spot-checks —
   never started, outranks everything else.
2. **The L0 map**, once Design's response lands. Design is now a *legibility* brief, not a
   performance one. The hardest problem, which the brief names: **346 detail nodes (57% of
   605) attach to no L0 node** at degree ≥ 6 and would be unreachable.
3. **Defer the dossier payload** — ~6.6 MB of narrative/claims parsed as JS object literals
   at load. Emit as one JSON string literal, `JSON.parse` on first dossier open. Lower value
   now that load is 1.6s.
4. **`unique_source_urls` is slightly wrong** — it counts the annotated source string, so
   appending a DEMOTED note inflates it. Should measure the URL.
5. **Delete `canvasInk` from `shoot.js`** rather than fix it. A check nobody can trust should
   not be in the output.
6. **`notes/WANTS.md`** — craft-morphology schematics. Parked. Do not start before the L0
   work; the argument for drawing rather than generating them is in that file.
7. Update `TESTING-CHECKLIST.md` §0, which still asserts the pre-dedup counts and will now
   fail its own check.

---

## Working rules

- **Adversarial review is opt-in.** At the end of a deliverable that feels final, ask
  Stewart: *"Do you want to run adversarial review audit?"* Do not run it unprompted — it
  burns context. When he says yes, act as his managers, the management this gets turned in
  to, and pick apart anything that looks wrong or is visually broken. Actually look at the
  output.
- **Research agents write to `research/`.** Build tooling lives in `tools/` deliberately — an
  agent deleted the build directory mid-run once.
- **Stewart's stated preferences:** concise and direct, no em dashes, tables over prose for
  comparisons, complete code rather than fragments.
- Raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` before any research wave; the default
  budget was exhausted by wave 1.

## Standing decision for Stewart

`william-mccasland`, `david-grusch` and `pursue-releases` exist on **both** this board and
The Vanishing. If the two share an id space it becomes one graph with two views, which is
considerably more powerful than two graphs. Not actioned.
