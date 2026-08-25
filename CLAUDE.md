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

**Starting a fresh session?** Read `notes/HANDOFF-2026-08-25-claude-code.md` after this.

---

## 1. What this is

A research board mapping the alleged legacy UAP recovery and reverse-engineering
programme, 1944–2026. Single self-contained HTML file, no server, no runtime deps.

| | |
|---|---|
| nodes | 968 (279 people · 689 entities) |
| hand-written sourced edges | 2,160 |
| tiered claims | 4,431 — T1 2,596 · T2 1,342 · T3 493 |
| unique source URLs | 2,825 |
| timeline events | 858 |
| program map (L0) | 110 nodes, all with dossiers |
| built artifact | `dist/the-program.html`, 13.2 MB |

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
python3 tools/state_snapshot.py --gate  # state + the whole gate below, in one command
python3 tools/verify.py                 # 18 checks
python3 tools/verify.py --self-test     # every check shown rejecting bad input
python3 tools/audit_independent.py      # 38 checks, deliberately independent
node    tools/test_scripted_analyst.mjs # 15 branch assertions
python3 tools/verify.py --idempotent    # slow: builds twice, requires identical output
```

**All of these must be green before a push.** `--idempotent` is the one that catches a
whole class of bug: any pass that reads its own previous output back in.

### Where you are running

This project is worked on from three places and they are not interchangeable:

| | can build & test | can push | can **look** at the dashboard |
|---|---|---|---|
| **cloud session** (web) | yes | yes, via the GitHub connection | **no** |
| **local Claude Code** | yes | yes | yes |
| Stewart, by hand | yes | yes | yes |

**If you are a cloud session, you cannot see the rendered output.** That matters more here
than in most projects, because §5 below is a list of times a check said one thing and the
screen said another. Ship visual work, but **never report a visual property as verified**.
Say "built, gate green, unverified on screen" and hand Stewart the thing to look at. Writing
"confirmed the labels no longer overlap" when nothing rendered is the same failure as the
checks that passed while broken.

### Windows notes — for commands you hand Stewart, not for your own shell

A cloud session runs Linux and should use `python3` and forward slashes for itself.
This section applies only to commands written **for Stewart to paste**. He runs
**PowerShell 5.1**:

- `&&` is a **syntax error**. One command per line.
- Always include the `cd`, quoted, so the block is copy-pasteable:
  ```
  cd "C:\Users\stewa\OneDrive\Documents\Claude\Projects\Missing individuals connected to defense contractors\the-program"
  python tools\verify.py
  ```
- The interpreter may be `python`, not `python3`. Check once, then be consistent.
- The repo path contains **three spaces**. This has already broken a build script that used
  `new URL(...).pathname`, which percent-encodes them. Use `fileURLToPath`.

---

## 4. Working agreements with Stewart

- **Clamp responses.** What you did, why, what you need from him. Detail goes in a repo note,
  not in chat.
- **No em dashes** in prose written for him. Tables are preferred over long lists. Charts get
  data labels.
- **Adversarial review is opt-in.** When a deliverable is finished, ask *"Do you want to run
  adversarial review audit?"* and then **wait**. Do not run it unprompted; it burns context.
  When he says yes, act like his managers — hostile management reading it cold — and
  actually look at the output rather than reasoning about it.
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

**Therefore: every check you add must be demonstrated rejecting the input it must reject.**
`verify.py --self-test` enforces this and will flag any check that lacks a poison.

And its sibling rule: **reading the source is not verification.** Three times this session a
check agreed with the implementation and a screenshot disagreed. For anything visual, look
at it.

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
data/l0-highlights.json             14 editorial start-here flags, DRAFT
data/l0-images.json                 image register, plumbed and deliberately empty
research/dossiers/                  per-node research
research/_authority.json            12 offices, each naming its instrument
research/_removed.json              approved removals + alias map
tools/                              the pipeline and the gate
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

**General principle: this board was built by porting a shell from a sibling project. Assume
every inherited surface is answering about the wrong project until someone has read it.**
Two were found on 24 August by accident, while looking for something else.

---

## 9. What is next, in priority order

> **0. FIRST: there is an unmerged branch, `origin/claude/status-update-bewtdk`, carrying
> 19 commits of data-integrity and sourcing work that never reached `master`** — 88 broken
> references fixed, 90 unsourced Tier 1 claims cleared, nine duplicate groups collapsed, a
> 1,198-URL link sweep, ~250 edges sourced, and browser runtime verification. Neither side
> is a superset. A test merge produces only three conflicts, two of them generated files
> that resolve by rebuilding. `research/` does not conflict. Full analysis and the two
> genuine audit failures it exposes: `notes/HANDOFF-2026-08-25-claude-code.md` §2b.
> **Do not force-push. Do not resolve generated files by picking a side.**


1. **The COVER-UP view still carries the sibling board's skeptical record** — the JPL
   matched-denominator argument, the NeuroLogica entry. Same class of bug as the scripted
   analyst, different surface, not yet touched. **Start here.**
2. **Sweep every remaining inherited surface** for the same problem, systematically rather
   than by accident. The system prompt, the report view, and the insight strings are the
   likely candidates.
3. **`data/l0-highlights.json` needs Stewart's sign-off.** 14 draft flags, each with a
   stated reason. Show him a table; he cannot read JSON. Cap is 16, so there are 2 slots.
4. **Implement Design's packed-cell layout and edge budget** in `tools/l0_patches.py`.
   Design's response of 24 August confirms `mountL0` is ours end to end, so this is a direct
   build and not a patch against the parent renderer. Package in `notes/design-2026-08-24/`.
5. **Add Design's nine checks** from §5 of their response, each self-tested.
6. **The image sourcing pass** for `data/l0-images.json`. Federal works are the strongest
   candidates (17 U.S.C. 105) but must trace to a `.gov` original, not an aggregator.
   Witnesses default to the class letter — a private person who testified has not licensed
   their likeness.
7. **`notes/REQUEST-QUEUE.md`** — 35 logged actions, and the FOIA queue.
8. **TESTING-CHECKLIST.md §12 source spot-checks** — never started. 25 spot-checks have been
   done ad hoc with zero fabricated sources found, but the systematic pass is outstanding.
