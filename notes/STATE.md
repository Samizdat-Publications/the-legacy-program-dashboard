# State of the repo

**Overwrite this file at the end of every session. Never append.** It answers one question for the next
session: where does the repo stand, and what do I do now? History lives in the dated handoffs and in
`notes/HISTORY-TO-2026-09-24.md`.

**Updated:** 25 September 2026, by the overnight session (Opus 5.5, high), after phase 3.

| | |
|---|---|
| **Next phase** | **Phase 4: stable ids, entity resolution, the taxonomy.** Detailed plan: `notes/plans/P4-topics-foundations.md`; the reviewed merge list: `notes/plans/P4-dedupe-decisions.md`. The plan marks it MAX; see the plan's note on effort |
| After that | phase 5 (drafting the topics), then 6 (the Atlas, merged only after Stewart's look) |
| Master | phases 1, 2 and 3 merged |
| Production | https://the-program-zxz.pages.dev serves master (CI deploys after a green gate) |
| The gate | `python tools/gate.py` (full), `--quick` (no poison sweep), `--no-build`, `--no-app`, `--idempotent`. CI: a gate job without a browser, an app job, and the poison sweep in three parallel shards |
| Branches worth knowing | `trial/nuclear-on-defaults`: local only, a measurement, never merge. `nuclear-2026-09-19`, `redesign/p1-*`, `redesign/p2-*`: merged, history |
| Working copy | `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders |
| Waiting on Stewart | nothing blocking. Optional: Appendix T (the topic table) before phase 4; the Worker redeploy from 12 September (not urgent); the public-release questions in section 10 of the redesign |

## What phase 3 did

| | |
|---|---|
| Nothing authored is dropped | entities keep `conflicts` (30), `unverified` (140) and `openQuestions` (18); a collapsed node's claims, sources and case against follow it to its survivor (33 claims; what cannot be placed is listed in `tools/UNPLACED-CLAIMS.json`) |
| One vocabulary | `schema/vocab.json` (read by the pipeline and the app, shipped as `/data/vocab.json`) and `schema/research.schema.json`. The 35 authored edge verbs are mapped explicitly and kept as `authoredVerb`; an unmapped verb is a reject |
| Integrity fixes | 4 duplicate claims gone; 62 edges' singular `source`/`tier` read (15 URLs, 2 stronger tiers); 33 person date conflicts recorded; orphan denial verdicts resolved through aliases and now a hard error; 19 unadjudicated denials listed and printed as "direction not adjudicated" (check C30) |
| Sourcing rules everywhere | dossier claims get the node rules: 85 Tier 1 dossier claims are Tier 2. Timeline `tier` split into `grade` (A/B/C) and `claimTier` (1/2/3) |
| Display labels | 56 spaced em dashes in labels replaced by " - ", listed in `tools/DISPLAY-NORMALISED.json`; claim texts and sources untouched |
| Node tiers that moved | 16, all from edges no longer folded into `programmatic` or claims now carried; listed in the phase 3 commits. The A/B/C distribution is unchanged |

## What phase 2 did

| | |
|---|---|
| The old shell is gone | `dist/the-program.html`, the parent page it patched, and 13 tools that built or tested it: about 331,000 lines. Its independent checks were carried to the app first: C27 (Home's figures re-derived from the served files), C28 (no sibling-board wording; the title names this board), C29 (the analyst's brief names this board's axes, read from the request it sends, answered locally so no tokens are spent) |
| A real defect, found by C27 on its first run | Home said 121 open questions; the board holds 116. `build_app_data.py` counted a question twice when two FOIA requests would close it |
| One build, one gate | `tools/build.py` (merge, regrade, merge, build_l0, build_design_extract, build_l0_layout, build_foia_links, build_app_data) and `tools/gate.py`. `verify.py` 57 to 46 checks, `audit_independent.py` 41 to 29: only old-shell checks went. `--idempotent` hashes the app's data |
| The nuclear register is live | 47 witnesses, 15 people and 19 entities net, seven base hubs. GOLDEN moved with it (nodes 1,136 to 1,170, edges 2,685 to 2,762, events 1,059 to 1,076, claims T1 3,789, T2 1,684, T3 618). Three chip numerals updated, wording untouched |
| `CLAUDE.md` | 69 KB to 20 KB. The whole old file is in `notes/HISTORY-TO-2026-09-24.md` |
| Deferred, on purpose | the force-layout bake in `build_l0.py` and the dossier copy inside `l0-model.json`'s rows: both still have readers, and both go with the L0 map in phase 11 |
| Noticed, and made visible | a local poison sweep run alongside another heavy job on this machine reported 16 runs with no verdict line; run alone, they pass. The sweep now prints the exit status and the last lines of any run that dies before its verdict |
