# State of the repo

**Overwrite this file at the end of every session. Never append.** It answers one question for the next
session: where does the repo stand, and what do I do now? History lives in the dated handoffs and in
`notes/HISTORY-TO-2026-09-24.md` (once phase 2 writes it).

**Updated:** 24 September 2026, by the redesign session (Opus 5.5, max effort).

| | |
|---|---|
| **Next phase** | **Phase 1: Meaning on the node page.** It is written out in full, test-first, in `notes/PLAN-2026-09-24.md`. Use Opus 5.5 at **high** effort, in one session, on branch `redesign/p1-node-meaning` |
| After that | phase 2 (retire the old shell, land the nuclear register, one gate command, slim `CLAUDE.md`), then phase 3; see the plan's roadmap |
| Master | built on `838c134`, plus the redesign documents (a docs-only merge: the app and the data did not change) |
| Production | https://the-program-zxz.pages.dev serves master. Board generated 2026-09-19: 1,136 nodes (338 people, 798 entities), 2,685 edges, 5,897 claims (T1 3,701, T2 1,618, T3 578), 1,059 events |
| Branches worth knowing | `nuclear-2026-09-19`: the verified 47-witness nuclear register, parked only by the old shell's `fitChipInk`; it merges in phase 2. `trial/nuclear-on-defaults`: local only, a measurement, never merge. Every other branch is history |
| Working copy | `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders |
| The gate | until phase 2 lands `tools/gate.py`: the sequence under "How to run a phase" in the plan. **Always run the app checks as well** (`npm run check`, `npm run check:poison`) |
| Waiting on Stewart | nothing blocking. Optional: read Appendix T (the topic table) and change any line; the Worker redeploy from 12 September (not urgent); the public-release questions in section 10 of the redesign |

## What the 24 September session did

| | |
|---|---|
| Reconciled the OneDrive move | no stray files for this project (4,114 files identical between the two copies); memory linked across the path keys; 11 dead `cd` paths in live docs repointed |
| Measured the board | six read-only agents: data model, graph structure, app, history, pipeline, research backlog. Reports are in `notes/redesign-2026-09-24/`, and the scripts, re-runnable, in `tools/analysis/` |
| Decided the redesign | `notes/REDESIGN-2026-09-24.md` |
| Wrote the plan | `notes/PLAN-2026-09-24.md`: 12 phases plus ongoing research; phase 1 in full |
| Did not change | any research file, any app code, any check, any generated data |
