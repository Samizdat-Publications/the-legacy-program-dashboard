# State of the repo

**Overwrite this file at the end of every session. Never append.** It answers one question for the next
session: where does the repo stand, and what do I do now? History lives in the dated handoffs and in
`notes/HISTORY-TO-2026-09-24.md`.

**Updated:** 25 September 2026, by the overnight session (Opus 5.5, high), after phase 5 and P5b.

| | |
|---|---|
| **Next phase** | **Phase 6: the Atlas, topic pages, the front door.** Detailed plan: `notes/plans/P6-atlas-and-topic-pages.md`. Stewart (25 September 2026) asked for the redesign to run to the end autonomously and will review at the end, so phase 6 merges on a green gate plus the blind critic's rounds rather than waiting for his look |
| After that | phases 7 to 12, then phase R (its first queue: `notes/plans/P5-research-queue.md`) |
| Master | phases 1 to 5 and P5b merged |
| Production | https://the-program-zxz.pages.dev serves master (CI deploys after a green gate) |
| The gate | `python tools/gate.py` (full), `--quick` (no poison sweep), `--no-build`, `--no-app`, `--idempotent`. CI: a gate job without a browser, an app job, and the poison sweep in three parallel shards |
| Branches worth knowing | `trial/nuclear-on-defaults`: local only, a measurement, never merge. `nuclear-2026-09-19`, `redesign/p1-*`, `redesign/p2-*`: merged, history |
| Working copy | `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`. The OneDrive copy is dead cloud placeholders |
| Waiting on Stewart | nothing blocking. At the end: the topic table (`notes/plans/P4-topic-table.md`, drafted at high effort), the redesign as a whole, the Worker redeploy from 12 September (not urgent), the public-release questions in section 10 of the redesign |

## The blind critic (Stewart, 25 September 2026)

After every phase a reader sees: `node tools/look.js --critic` shots to a separate agent with only
`tools/critic/BRIEF.md`; fix its five worst; repeat. Reports in `notes/critic/`. Round 0 (the baseline)
found phones broken everywhere (a blocker), testimony reading as documented fact, wrong connection groups,
unnamed marks and a node page that led with prose; each row is triaged to a phase there.

## What phase 5 and P5b did

| | |
|---|---|
| 93 topics, verified | drafted by 8 Opus agents from packets of the board's own claims (`tools/topics/topic_packet.py`), verified twice by 3 Opus agents re-deriving every sentence from its cites (round 1: 53 of 93 failed, mostly sentences saying more than their cites and testimony stated as fact; round 2: 7, fixed). Ten honesty checks in `verify.py` with poisons, restated in the audit |
| Coverage | 96.3% of nodes and 96.0% of people in a topic's members (floor committed); every hub of degree 30 or more in 3 or more topics |
| Shipped as data | `app/public/data/topics.json` and `topics/<id>.json` with every cite resolved; absorbed domain nodes carry `absorbedBy`. Readers see topics from phase 6 |
| What drafting found wrong in the data | `notes/plans/P5-research-queue.md`: six claims or edges that overstate their sources, a class of Tier 1 claims resting on secondary relays, and more (phase R) |
| P5b, from the critic | phones work on every surface (a two-row bar with VIEWS, stacked Home, evidence cards, list views of the map and neighbourhood; C26 sweeps every route at 375); 396 Tier 1 claims that record what was said are marked "said on the record" or "the office's own account" (C31; no tier moved); the node page's first screen shows the case against, and the board's own analysis is labelled and folded; the analyst tab covers nothing (C32); plain words and no debug chrome (C35); thread and timeline order fixes (C33, C34). Three critic rounds; round 3's worst were all later-phase items |

## What phase 4 did

| | |
|---|---|
| Stable ids | every claim (`c-` + 10 hex) and edge (`e-` + 10 hex) carries a content id, shipped in the app's data; no collisions |
| Entity resolution | 25 reviewed merges, 32 aliases (`notes/plans/P4-dedupe-decisions.md`): nodes 1,170 to 1,138; 123 claims moved to their survivors; six disagreements recorded as `conflicts`, nothing deleted; the duplicate finder is `tools/topics/find_duplicates.py` |
| The taxonomy, DRAFT | 93 topic stubs in `research/topics/`, 10 sections, 3 research gaps; proposals (`tools/topics/propose_members.py`, part of the build) cover 98.2% of nodes and 97.7% of people; all 58 domain nodes absorbed exactly once |
| Found on the way | the analyst's health check had no timeout, so a stalled Worker left the dock saying "checking" forever (now 8 seconds, then the unreachable line); the map ranks nodes with a dossier first within its budget |
| Local poison sweeps | on this Windows machine, late at night, runs died in bursts with "fetch failed" against a live preview: not reproducible in 400 direct fetches. Every one of the 30 poisons was seen when rerun alone; CI's sharded Linux sweep is the authoritative one. The harness now retries its first fetch and names the underlying error |

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
