# State of the repo

**Overwrite this file at the end of every session. Never append.** It answers one question for the next
session: where does the repo stand, and what do I do now? History lives in the dated handoffs and in
`notes/HISTORY-TO-2026-09-24.md`.

**Updated:** 25 September 2026, by the overnight session (Opus 5.5, high), after phase 2.

| | |
|---|---|
| **Next phase** | **Phase 3: the pipeline drops nothing.** Its detailed plan is written and committed: `notes/plans/P3-pipeline-drops-nothing.md`. Branch `redesign/p3-pipeline-drops-nothing` |
| After that | phase 4 at **max** effort (stable ids, entity resolution, the taxonomy decided); see the roadmap in `notes/PLAN-2026-09-24.md` |
| Master | phases 1 and 2 merged |
| Production | https://the-program-zxz.pages.dev serves master (CI deploys after a green gate) |
| The gate | `python tools/gate.py` (full), `--quick` (no poison sweep), `--no-build`, `--no-app`, `--idempotent`. CI: a gate job without a browser, an app job, and the poison sweep in three parallel shards |
| Branches worth knowing | `trial/nuclear-on-defaults`: local only, a measurement, never merge. `nuclear-2026-09-19`, `redesign/p1-*`, `redesign/p2-*`: merged, history |
| Working copy | `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders |
| Waiting on Stewart | nothing blocking. Optional: Appendix T (the topic table) before phase 4; the Worker redeploy from 12 September (not urgent); the public-release questions in section 10 of the redesign |

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
