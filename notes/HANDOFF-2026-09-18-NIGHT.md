# Handoff, 18 September 2026, night (the current one)

Opus 5 session. It ran item 1 of `notes/HANDOFF-2026-09-18-EVENING.md` section 3, the
centrality fix, and nothing else, as that section instructed.

**Read order for the next session:** this file, then `notes/CENTRALITY-2026-09-18.md`,
then `notes/HANDOFF-2026-09-18-EVENING.md` section 4 for Stewart's job order, which is
unchanged and still governs. `git fetch --all` first.

**Why this is a new file and not an edit to the evening handoff.** That file exists only
on `leads/arv-2026-09-18`, not on master, and the branch this session built from is off
master. Editing master's `HANDOFF-2026-09-18.md` would have collided with the edit
`cde1c57` already makes to it on the ARV branch. New files do not conflict.

## 1. What landed

Built on branch `fix/centrality-2026-09-18` off master at `92b5903`, then **merged to
master and pushed on Stewart's yes, 18 September 2026**: `92b5903..e5666a7`, fast-forward,
two commits. `1a7d3e7` is the fix and the regenerated board, `e5666a7` is the CLAUDE.md
section 6 entry that records where node-tier proximity is computed and what is
deliberately not in it. CI gate run and deploy are in section 3.

| | |
|---|---|
| Code change | `tools/regrade.py`: `witness-chain` removed from `PROGRAM_EDGES`, with the reasoning as a comment, plus the rationale string that named the four edge types to readers |
| Note | `notes/CENTRALITY-2026-09-18.md`, the measurement, the decision, and the rejected lever with its numbers |
| Data | The whole pipeline re-run, `app/public/data/` regenerated, NotebookLM export regenerated |
| Gate, local | Green except `runtime_check.js`. See section 3 |
| Gate, CI | Run `35410883512` **green**, both jobs (`gate`, `app`). Deploy `35412163536` **green**. Production carries the new grades |
| `GOLDEN.json` | **Not touched, and did not need to be.** The evening handoff predicted it would move on the tier distribution lines. It does not: golden tracks counts, and this moves only tiers. `verify.py` passes unchanged |

## 2. The decision, in one table

The evening handoff offered two levers and asked for both to be sized first. They were.

| Variant | nodes moved | fall: testimony | fall: **document** | rise: document | right-way ratio |
|---|---|---|---|---|---|
| **lever 2 alone, BUILT** | 26 | 19 | **0** | 20 | **19.5** |
| lever 1 alone | 30 | 10 | **13** | 26 | 2.2 |
| lever 1 on `prog_deg` only | 17 | 5 | **8** | 13 | 1.6 |
| both, as the handoff proposed | 46 | 25 | **8** | 41 | 5.5 |

Section 3b of the evening handoff sets the failure condition: "If documented nodes are
falling, the fix is wrong." Every variant carrying claim-tier weighting fails it. Lever 2
alone is the only one that moves no document-based node down, and it is the smaller
change. **Lever 1 is rejected on measurement, not on taste**; section 4 of the note says
why the proposal is a category error rather than a bug.

The sharpest single piece of evidence: under the old rule
`podesta-delonge-mccasland-email-2016`, an email with four program edges that are all
`witness-chain`, was being promoted INTO Tier A, while `gao-nsiad-95-187`,
`ndaa-fy2024-subtitle-c`, `reid-sap-letter-2009`, `dcsa-nisp` and `mit-lincoln-laboratory`
were being demoted OUT of it. That is reversed.

`mark-mccandlish` goes A#70 to A#143 of 1,066 against a cut at 159, now below Mellon, the
UAP Task Force, 32 CFR 117 and 50 USC 3091a. He did not have to leave Tier A for the
inversion to be fixed, and forcing him out would have cost eight documented nodes.

**One judgement call is flagged for Stewart rather than buried:** `ryan-graves` leaves
Tier A. He testified under oath, but about what he saw, not about being inside a
programme. Note section 5 argues it. It is the one row worth disagreeing with, and it is
a research judgement, not a pipeline one.

## 3. The gate, and the one red check

Run as `BOARD_URL=http://127.0.0.1:8899/the-program.html python tools/state_snapshot.py
--gate`, which runs the whole gate in one command. Do not then run the individual checks;
that runs everything twice.

| Check | Result |
|---|---|
| `browser_env --self-test`, `verify`, `verify --self-test`, `capture_strip`, `audit_independent`, `test_packed_layout` (and `--self-test`), `test_scripted_analyst`, `verify --idempotent` | **PASS** |
| `runtime_check` | **FAIL(1)** `the network map is still at rest ... went quiet and then started moving again` |

This is the Windows-local failure the evening handoff section 1 records and says not to
chase. **It is not caused by this change, and that was tested directly rather than
assumed:** `dist/the-program.html` was checked out from master, so unchanged code and
unchanged data, and `runtime_check.js` failed on it with the identical message on this
machine. The change alters node tiers and touches nothing about map motion or settling.

One refinement to how the evening handoff describes it. That file calls it a flake because
it failed 7 of 7, then passed, then failed again. This session saw **three consecutive
failures and no pass** (two on the new board, one on master's), plus one run that hung
rather than finishing. So locally it currently looks closer to a consistent failure than
an intermittent one, while CI stays green. Nothing follows from that for this branch,
since master fails it too, but a session that retires the old shell should not expect the
check to pass here first. It dies with the old shell, job 6 in Stewart's order.

## 4. Next, in Stewart's order, unchanged

From `HANDOFF-2026-09-18-EVENING.md` section 4. Item 1 is now done.

| # | job | state |
|---|---|---|
| 1 | The centrality fix | **DONE and ON MASTER** at `e5666a7` |
| 2 | **TR-3B, the next witness-band hub** | **NEXT.** Brief is `research/leads/CANDIDATES-2026-09-18-ARVP.md` section B. Open Fouche's 1998 presentation and the "military documents" the arvp site links, and find the sceptical literature, BEFORE building |
| 3 | Gate ARV and TR-3B together and push both | Ask Stewart first |
| 3a | **The witness coverage pass. NEW, added 18 September on Stewart's instruction** | See section 4a below |
| 4 | The propulsion-mechanism strand, approved | `notes/PROPULSION-CLAIMS-2026-09-18.md` |
| 5 | The rest of the canon pass | audit passes 1, 3, 4, then 5 |
| 6 | Retire the old shell | Kills the `runtime_check` flake |
| 7 | Tier option C | Unchanged |

**DO THIS FIRST, before item 2 or 3: re-grade the ARV branch.** `leads/arv-2026-09-18` was
built under the OLD rule and the new rule is now on master, so that branch currently
carries node tiers computed two different ways. Per evening handoff section 3d, rebase or
rebuild it so its nodes are graded once. Its research files do not change; only pipeline
output does. Rebasing it will conflict on `app/public/data/`, which is generated: take
master's side and re-run the pipeline rather than resolving those files by hand.

The same applies to any other unmerged branch carrying board data. As of tonight that is
`leads/arv-2026-09-18` and the older `build/*` and `leads/*` branches, none of which are
in flight.

**Evening handoff section 3d asked whether the fix resolves the red check by itself. It
does not**, and this was confirmed by actually re-grading the ARV branch rather than by
inference. On the re-graded board L0 is **139**, `arv-fluxliner` is **in it** at Tier B in
cluster `witness` class `program`, and that cell **still holds exactly one node**.
Stewart's option 1, building TR-3B into that cell, remains the fix.

An earlier draft of this paragraph and of `notes/CENTRALITY-2026-09-18.md` section 6 cited
"L0 held at 137" as the evidence. That number was L0 on MASTER, which carries no ARV nodes
at all, so it was no evidence either way. Both are corrected.

## 4a. The witness coverage pass, new and from Stewart directly

**Stewart, 18 September 2026:** "I don't want this to be just about the program because
that would be incomplete without all the major whistleblowers and people who have
testified to Congress about UAP since that's some of the primary evidence we have about
the whole thing."

That is a scope instruction and it is his. It was prompted by the `ryan-graves` demotion,
but the demotion is not the problem and reversing it would have hidden the problem. The
board's coverage of congressional witnesses was already thin BEFORE this session, under
the old rule:

| Witness | State |
|---|---|
| `michael-herrera` | **absent entirely** (also audit band 1) |
| `jason-sands` | **absent entirely** |
| `alex-dietrich` | Tier C, **one** T1 claim |
| `david-fravor` | Tier B, 4 T1 claims. Was already Tier B before this session |
| `ryan-graves` | Tier B, 5 T1 claims |

Fravor at B and Dietrich at C predate the centrality fix, so testimony-based figures were
never ranking on the node-tier axis. The pass:

1. Build `michael-herrera` and `jason-sands`.
2. Enrich `alex-dietrich` and `david-fravor`.
3. **Check the whole congressional-witness roster for absentees first**, the same way
   `ben-rich` was caught in section 5: existence check by canonical id BEFORE building,
   every time, or the board gains duplicates.
4. The hearings are already the hubs and are already Tier A and on L0
   (`hearing-2023-07-26`, `hearing-2024-11-13`, `hearing-2025-09-09`), so this is
   enrichment of an existing structure, not a new surface. Witnesses join in by
   `witness-chain`, per the hub rule.

**Why this pass is safe only now.** Under the hub rule every claimant gets a
`witness-chain` edge into the thing claimed about. Under the OLD x3.0 weighting, adding
this roster would have drifted every one of these witnesses toward Tier A and "proximity
to the programme" would have collapsed into "how much testimony exists about this". The
centrality fix is what makes the expansion Stewart wants possible without destroying the
meaning of the axis.

The Graves grade is held at B, with his argument recorded in
`notes/CENTRALITY-2026-09-18.md` section 5, along with the three findings it rests on
(L0 carries no people; search ranks on claim tier, not node tier; the hearings are already
Tier A on L0) and the two honest routes if he wants the letter changed anyway.

## 5. Two corrections to the evening handoff, both found in passing

**Ben Rich already has a node.** Section 5 of that file carries him as an unbuilt
candidate, saying the board holds `lockheed-skunk-works` with no node for the man who ran
it. It holds `ben-rich`: person, Tier B, 2 claims, 3 sources, domain `primes-custody`,
edges `institutional -> lockheed-skunk-works` (T1) and `custody -> lockheed-martin` (T3).
He deserves the build, but **as an enrichment of the existing id, not a new node.** The id
comment in `regrade.py` exists because five duplicate people got onto this board exactly
that way. **The rest of section 5's named candidates were checked for existence the same
way and should be, one at a time, before each is built.**

**`dod-oig` is under-documented.** It falls to Tier C on four edges, one of which was the
Tier 2 `witness-chain` to Elizondo that used to carry the x3 multiplier. The Defense
Department's own Inspector General, on a board about oversight of concealed programmes,
should carry more than a single investigative edge to one report. That is a coverage gap
for the canon pass, not a scoring error, and the fix is right to stop hiding it behind a
testimony multiplier.

## 6. Mechanics worth keeping

- The `state_snapshot.py --gate` and `runtime_check` notes above.
- A long mechanical sequence runs better as one backgrounded shell command than as a
  subagent, which the evening handoff also found.
- `http-server` on 8899 may already be running from an earlier session; `EADDRINUSE` on
  starting a second one is harmless, since it serves `dist` from disk either way.
- This repo has CRLF working files. Anything that rewrites a tracked text file by exact
  string match must preserve the existing line endings or every line shows as changed.
