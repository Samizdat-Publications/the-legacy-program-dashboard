# State of the repo

**Overwrite this file at the end of every session. Never append.** It answers one question for the next
session: where does the repo stand, and what do I do now? History lives in the dated handoffs and in
`notes/HISTORY-TO-2026-09-24.md` (once phase 2 writes it).

**Updated:** 24 September 2026, by the phase 1 session (Opus 5.5, high effort).

| | |
|---|---|
| **Next phase** | **Phase 2: Retire the old shell, land the nuclear register, one gate command, slim `CLAUDE.md`.** Its section in `notes/PLAN-2026-09-24.md` is an outline: write its detailed plan first (superpowers:writing-plans) into `notes/plans/P2-retire-old-shell.md`, commit it, then execute. Opus 5.5 at **high**, branch `redesign/p2-retire-old-shell` |
| After that | phase 3 (the pipeline drops nothing), then phase 4 at **max**; see the plan's roadmap |
| Master | phase 1 merged: see "What phase 1 did" below |
| Production | https://the-program-zxz.pages.dev serves master (CI deploys after a green gate). Board data unchanged by phase 1: 1,136 nodes, 2,685 edges, 5,897 claims, 1,059 events |
| Branches worth knowing | `nuclear-2026-09-19`: the verified 47-witness nuclear register, parked only by the old shell's `fitChipInk`; it merges in phase 2. `trial/nuclear-on-defaults`: local only, a measurement, never merge. `redesign/p1-node-meaning`: merged, history |
| Working copy | `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders |
| The gate | until phase 2 lands `tools/gate.py`: the sequence under "How to run a phase" in the plan, plus `python tools/lint_no_em_dash.py`. **Always run the app checks as well** (`npm run check`, `npm run check:poison`). A phase that changes only `app/src` may skip the Python pipeline |
| Waiting on Stewart | nothing blocking. Optional: read Appendix T (the topic table) and change any line; the Worker redeploy from 12 September (not urgent); the public-release questions in section 10 of the redesign |

## What phase 1 did

| | |
|---|---|
| Connections on every node page | grouped by relationship under reader names (Custody, Money, Programme links, Institutional ties, Law and oversight, Research and authorship, Investigations, Testimony, Conduct, Denials, Sequence in time, Place) in three layers; one row per counterpart; each link's own sentence as text, with dates, tier and a fold-out source list. The word "member" is gone from the page and the report. `app/src/vocab.ts`, `app/src/pages/connections.ts` |
| Every authored field shown | what it is, unverified notes, denial posture, chronology plus sequence chain (deduplicated), affiliations, the node's own sources, and every open question with the FOIA request that would close it. The tier letter and cluster left the crumb and the report; the machine tier rationale left the page (still in the data for the analyst) |
| Search | reaches timeline events and the eight threads |
| Evidence | the column is "NODE DENIED" and a flagged cell reads "on the node": the flag is the node's, never the claim's. Data unchanged |
| Phones | at 760px and below the node page is one column and the bar scrolls inside itself |
| Em dashes | 69 lines removed from `app/src`, `app/checks`; `tools/lint_no_em_dash.py` (self-tested) runs in the app job of `gate.yml`. `app/src/analyst/tools.ts` stays exempt until phase 12 |
| Found by looking, fixed | a global `.cell` rule in `map.css` stacked the node page's three axis cells into one square (renamed `.acell`, guarded in C23); the "map neighbours by start date" list repeated a neighbour once per edge (now once each); new search rows for events had their label squeezed into the mark column (CSS) |
| Checks | C22 to C26, each written first, each shown failing on the old build and on its own poison. C18 now waits up to 10s for the analyst health line to settle (it read "checking" on a slow connection) |

## Known, not done (belongs to later phases)

- Node, edge and event labels in the DATA still carry em dashes; phase 3 normalises display labels.
- Chronology and sequence chain dedupe only exact date+text matches; near-duplicates (two phrasings of one
  event) remain, by design, until phase 3's integrity work.
- The event-row layout fix in search is looked at, not guarded by a check.
