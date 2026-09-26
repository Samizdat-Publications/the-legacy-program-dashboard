# The Program: working instructions

**Read this first. Then read `notes/STATE.md`, which says what to do now.** This file holds the rules and
the working agreements; `notes/STATE.md` holds where the repo stands; the history that used to live here
is in `notes/HISTORY-TO-2026-09-24.md`, verbatim.

**Repo:** `Samizdat-Publications/the-legacy-program-dashboard` (private), branch `master`, its own
repository. **Owner:** Stewart. **Working copy:** `C:\Users\stewa\ClaudeProjects\Missing individuals
connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders; never work there.

**The redesign (24 September 2026)** rebuilds the board from a graph into an atlas of topics in which
every link explains itself. The decision: `notes/REDESIGN-2026-09-24.md`. The work, phase by phase, with
the model and effort for each: `notes/PLAN-2026-09-24.md`. Do the phase `notes/STATE.md` names; a phase
not written out in full in the plan gets its own detailed plan in `notes/plans/` first.

**Trust no figure in any document here.** `python tools/state_snapshot.py` derives them from source.

---

## 1. What this is

A research board mapping the alleged legacy UAP recovery and reverse-engineering programme, 1944 to now.
What ships is the app in `app/`: Vite 5 and TypeScript, no framework, hash-routed, its data fetched at
runtime from `/data`, which `tools/build_app_data.py` generates from `research/` through the Python
pipeline in `tools/`. Production is **https://the-program-zxz.pages.dev** (note the `-zxz`), deployed by
`.github/workflows/deploy.yml` after a green `gate.yml` on `master`. The review site
**https://the-program-next.pages.dev** is where a build is looked at before production, deployed by hand.
The analyst's Worker in `worker/` is deployed by hand, by Stewart only.

The old single-file shell retired in phase 2 (25 September 2026); C27 to C29 carry its checks.

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
  correction had to be reverted. **This became load-bearing on 19 September 2026** when the
  triage rule widened (below). The board now carries the problem documented from both
  directions: Tal Levesque invented `thomas-castello` and mailed a hundred identical packets
  to manufacture the look of many independent sources, and the Disclosure Project's
  sixty-eight testimonies were all collected by one interviewer who cross-references his own
  witnesses to each other in editorial notes. One deliberate, one nobody intended.

### 2a. NOTABILITY IS A SECOND, PARALLEL CRITERION FOR ADMISSION (19 September 2026)

Adopted on Stewart's instruction from `research/leads/CANON-GAPS-2026-09-18.md` section 5.
Full reasoning and its obligations: `notes/TRIAGE-RULE-2026-09-19.md`.

The old rule promoted a lead to a node only when an openable primary record anchored the
claim, which is why this board carried the officials and omitted the claimants. **A person,
place, programme or event now also belongs on the board when an informed reader would expect
to find it and would read its absence as a gap in the map**, whether or not any record
vouches for what was said.

**This widens ADMISSION and changes NOTHING about GRADING.** The triage rule decides whether
a lead becomes a node. The tier decides how strong the evidence is. They are separate and
must stay separate:

- Testimony is Tier 2. It is carried at Tier 2, openly, and is not upgraded for being
  important.
- The openable anchor is **the dated artefact of the claim** (a recorded testimony, a
  broadcast, a book, a filing), NOT a record of the thing claimed. There must still be
  something that fixes WHEN the claim was made.
- The case against goes in the same node's `conflicts` and `unverified`, never elsewhere.
- Where no record exists, **the node says so in its own narrative**: "no employment, service
  or civil record has ever been produced for this person" is a finding, and beats silence.

**THE OBLIGATION THAT COMES WITH IT.** Admitting claimants admits circular reporting, so
every node admitted on notability records HOW THE CLAIM REACHED US, not only its content:
who found this person and by what route; what they had said BEFORE being contacted by an
interested party; whether they were given another witness's account first; and whether the
accounts agree on substance while diverging on detail, which reads very differently from
verbatim agreement. `michael-herrera` is the standard: its edge to the 2025 hearing carries
a note in capitals saying it is NOT a witness appearance.

---

## 3. How to build and check

```
python tools/build.py                 # the whole pipeline, in order, stopping at the first failure
python tools/gate.py                  # build, every Python check, the app build, its checks, every poison
python tools/gate.py --quick          # the same without the poison sweep, while iterating
python tools/gate.py --no-build       # check what is already built
python tools/gate.py --idempotent     # also build twice and require identical output (slow)
```

`build.py` runs merge, regrade, merge, build_foia_links, build_source_registry, build_app_data,
build_places, propose_members. Order matters: later stages consume earlier output. `gate.py` starts and
stops its own preview on 127.0.0.1:4173 (or reuses one already answering) and prints one summary table.
**All of it green before a push to `master`.** A change to `app/src` alone may use `--no-build`.

What the gate holds, and why each piece exists:

- **`verify.py`** checks the research data and what ships, and **`verify.py --self-test`** shows every
  check rejecting a poisoned input. `--update-golden` after any deliberate count change, explained in the
  commit. **`audit_independent.py`** re-derives the same facts by a deliberately different route.
- **`build_app_data.py --check`** re-derives every count in `app/public/data/index.json` from the sources
  and fails on drift. `app/public/data/` is generated AND committed, and it is reproducible across
  platforms: its fingerprint hashes content with CRLF normalised to LF and reads nothing from `.git`. So CI
  compares it with a plain `git diff --quiet`. Never add `-I` flags to that diff.
- **`check_rebuild.py`** requires the committed artifacts to equal a fresh build. It normalises the build
  date stamp on both sides and compares full bytes. **Do not "simplify" it to `git diff -I<regex>`**: some
  artifacts are a single line, so the changed line always carries the stamp and every real change would be
  swallowed.
- **`lint_no_em_dash.py`** keeps U+2014 out of `app/src`, `app/checks` and `worker/src`
  (`app/src/analyst/tools.ts` is exempt until phase 12).
- **The app's checks** (C1 to C72, with gaps), in `app/checks/run.mjs`, drive the BUILD in a real browser, not the dev
  server. Each has a **poison**: a deliberate corruption of the real page at one stop, which its check must
  be seen to fail on. `npm run check:poison` runs them all; `POISON=c21 node checks/run.mjs` runs one.
  CI shards the sweep three ways (`--all-poisons --shard k/3`).

To run the app by hand: from `app/`, `npm run build`, then as a background task
`npx vite preview --host 127.0.0.1 --port 4173 --strictPort`. Spell out the host (plain `npm run preview`
binds IPv6 only here and the checks find nothing) and keep `--strictPort` (so it fails rather than moving
to 4174, which nothing watches).

**Looking, and the blind critic** (Stewart, 25 September 2026). `node tools/look.js` is a camera, never a
check. After every phase that changes what a reader sees, run `node tools/look.js --critic --out <dir>`
(every surface at 1920, 1366 and 375 wide, at 1x) and give the shots to a separate critic agent with
`tools/critic/BRIEF.md` and NOTHING else: no code, no notes, no reasoning. It returns the five worst
problems a reader would notice. Fix them, shoot again, repeat until the worst is cosmetic; keep each
round's report in `notes/critic/`. The builder never grades its own screenshots; one shot is one state. Where nobody has looked, say "built, gate green, unverified on screen".

**Commands written for Stewart** are PowerShell 5.1: `&&` is a syntax error, so one command per line;
every block starts with its own quoted `cd`; the interpreter is `python`. The repo path has three spaces:
in Node use `fileURLToPath`, never `new URL(...).pathname`. Locally `core.autocrlf` is on, so anything that
hashes bytes must normalise CRLF.

---

## 4. Working agreements with Stewart

- **Sessions own the repo end to end** (git, merges, pushes, deploys, research and tier decisions): "You
  have full authority to make decisions" (18 September 2026); "nothing is SACRED except the dataset" (24
  September 2026). Decide, record the reasoning in a note, and tell him after. If the harness refuses a
  push to `master`, ask him in one line.
- **Every terminal command he is asked to run is a complete copy-paste block that starts with its own
  `cd`.** He does not read terminal commands. Corrected three times, each time in chat.
- **Commit and push often**, after each substantial change, not at the end. **`git fetch --all` before
  reading any handoff**, and **merge before handing off**: an unmerged branch is invisible to the next
  session (PR #5 held a whole day's work as a draft; a later session re-derived pushed work for forty
  minutes). A handoff request is an instruction to commit and push first.
- **Clamp responses**: what you did, why, what you need from him. Detail goes in a repo note. Tables over
  long lists; charts carry data labels; **no em dashes**, anywhere.
- **Adversarial review does not apply to this project.** It exists for his employer work; here the gate is
  the equivalent. Do not offer it.
- **He cannot read JSON.** When a JSON file needs his decision, render it as a table in chat.
- **Hand things to Claude Design, self-contained**: its own context, screenshots and figures; anything it
  references on `master` and under 1MB (the API reads bigger files as absent).
- **Never paste the GitHub token into chat** (`.gh-token`, gitignored).
- **Token economy** (3 September 2026): the orchestrating session does not read files over about 10 KB; an
  agent reads them and reports in under 40 lines. Fan-outs of more than five agents go through one
  coordinator. Sonnet for mechanical batches, the gate and screenshots; Opus for code, triage,
  verification and drafting. Waits are one background job, never a poll.
- **Size never encodes importance**, anywhere in the visual language. One label size (11px); labels are
  chosen by space, never shrunk or truncated; no anonymous marks.
- `data/analyst-suggestions.json` is Stewart's. When board counts move, update only the numerals in the
  chips that quote them, never the wording, and tell him.

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
  line at both edges: the panel fitted its element, and the element did not fit its grid
  track.
- The scripted-analyst test passed while **six of seven** suggestion chips routed to the
  wrong branch, because it asserted only that a long answer came back with valid commands.
  A check that cannot name the branch it expected cannot detect a wrong one.
- The (retired) map's first packed layout rendered six chips *beneath* its column-head plate
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

- **Claim tiers 1-3: evidence strength. 1 is strongest.** Ammunition grading. T1 documented,
  T2 a named person on the record, T3 stated inference. T3 is flagged by the file rather than
  by a critic, and is where research goes next.
- **Node tiers A/B/C: proximity to the programme.** Not credibility. A Tier A node carrying
  only T3 claims is not a contradiction; it is the definition of where to look next.
  Computed by forced percentile in `tools/regrade.py`, where `PROGRAM_EDGES` is the set
  weighted x3.0 for meaning *inside* rather than *adjacent*. **`witness-chain` is
  deliberately not in that set** (18 September 2026): it records that somebody made an
  assertion, not a structural fact about the node, and under the hub rule it is the
  dominant edge type of every claimant cluster. It counts at x1.0 in plain degree, so
  degree may mean "a lot is claimed here", never "this is true". Weighting the degree
  counters by each edge's `claimTier` was measured and rejected in the same pass, because
  it demotes documented nodes: `notes/CENTRALITY-2026-09-18.md` has the numbers.

---

## 7. Where things are

```
app/                         the shipped app. app/dist/ is built in CI and gitignored
app/src/pages/               one module per page; connections.ts groups a node's links
app/src/vocab.ts             edge-type names, from schema/vocab.json (the one vocabulary)
app/src/analyst/             the analyst: tools.ts (twelve tools that RUN IN THE BROWSER), client.ts
                             (the tool loop), state.ts, chips.ts, panel.ts
app/public/data/             GENERATED by build_app_data.py and COMMITTED. Never hand-edit
app/public/_headers          the deployed app's headers; _redirects maps old deep links
app/checks/run.mjs           the app checks, each with a poison
worker/                      the analyst's Worker. Deployed by hand, by Stewart
research/                    the authored data: one JSON per research pass, dossiers/, threads.json,
                             patents-view.json, observables-view.json, _corrections.json,
                             _authority.json, _removed.json, _edge_tiers.json, leads/
data/the-program.json        the merged board (over GitHub's 1MB API read cap: reads as ABSENT)
data/foia-links.json         GENERATED node to FOIA request links. Never hand-edit
data/analyst-suggestions.json  the analyst's chips, Stewart's decisions
data/l0-highlights.json      the start-here flags, signed off; l0-shorts.json authored short labels;
                             l0-images.json the image register (the l0- names outlived the map)
tools/build.py, gate.py      the build order and the one gate command
tools/merge.py, regrade.py   the pipeline's core (reads schema/); GOLDEN.json the counts verify.py holds
tools/dossiers.py            the entity dossiers (research/dossiers/) with the sourcing cap
research/_places.json        place coordinates: the board's own UNCITED table (a cited one is phase R)
tools/look.js, walk.js       the cameras
tools/analysis/              the redesign's re-runnable measurements
exports/notebooklm/          the NotebookLM export (tools/build_notebook_export.py)
notes/                       STATE.md, the plan, per-phase plans, handoffs, findings
```

---

## 8. Stale documents

`PROJECT.md`, `README.md`, `TESTING-CHECKLIST.md`, `SESSION-HANDOFF.md`, `WAVE3_QUEUE.md` and
`CLAUDE-DESIGN-PROMPT.md` are historical. Handoffs are true as of their date only; `notes/STATE.md` is
current. **This board was built by porting a sibling project's shell: assume any inherited surface
(copy, markup, anything the browser fetches) answers about the wrong project until someone has read it.**
C28 guards the known strings.

---

## 9. What is next, and what not to undo

**Next:** whatever `notes/STATE.md` names, from `notes/PLAN-2026-09-24.md`.

**Do not undo** (each cost a session to learn; the reasons are in `notes/HISTORY-TO-2026-09-24.md`):

- Anything a build computes in floating point must be identical on Windows and Linux: libm's last-ulp
  differences once produced two maps from one source and kept CI red for a day (the map and its own trig
  retired in phase 11).
- The analyst's tools run in the reader's browser, not the Worker; thinking blocks are relayed untouched
  (their signature covers their text); all tool results go back in ONE user message; `TOOLS_VERSION` lives
  in two files and a change is a deploy of both; the cited-id guard flags and never edits.
- The back button's only action is `history.back()`; `/data/*` revalidates rather than being immutable.
- A research record with no `cls` used to be dropped by `merge.py` in silence; the check that names such
  records stays.
- Recorded research decisions stay decided: the section E exclusions and section D corrections of
  `research/leads/CANDIDATES-2026-08-30.md`; the four transcript claims recorded as contradicted by the
  opened record (Michels build); `sapoc` established 5 January 1994; ATIC discontinued 1 July 1961 with FTD
  constituted the same day; the nitinol lineage carries the NOL record beside the Battelle allegation.
- `witness-chain` stays out of `PROGRAM_EDGES` in `regrade.py`; weighting the degree counters by claim
  tier was measured and rejected (`notes/CENTRALITY-2026-09-18.md`).
- `tools/spot_check.py --links` sweeps every cited URL with a ranged GET, never HEAD.
