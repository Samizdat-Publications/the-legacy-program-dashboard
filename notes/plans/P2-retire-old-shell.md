# Phase 2, detailed: retire the old shell, land the nuclear register, one gate command

Written 25 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 2" and a read-only map of the
couplings (an Opus agent, reported in session; its facts are folded in below with file:line). Branch
`redesign/p2-retire-old-shell`. Opus 5.5, high.

## What the map changed in the outline

- **Three surviving writers still produce old-shell files.** `merge.py:1280-1307` writes
  `data/program-{people,entities,edges,entity-info,timeline}.js`; `build_l0_layout.mjs:928-935` writes
  `data/l0-layout-model.js`. Deleting the files without the writers recreates them on the next build.
  `data/layout.json` (writer `precompute_layout.py`) and `data/program-meta.js` (no writer) just go.
- **The dossier copy inside `l0-model.json` rows stays.** `build_design_extract.py:55`, `verify.py` 902/916
  and `audit_independent.py:155-167` read `l0[].dossier`. It goes with L0 in phase 11.
- **The force-layout bake in `build_l0.py:331-453` stays too**, for the same reason: its x/y feed
  `design-extract.json` (`build_design_extract.py:59`) and its counts feed checks. Removing it is a data
  change to two generated files with nothing to show a reader; it belongs with L0's retirement (phase 11).
  Recorded here as a deliberate deferral, not an omission.
- **Verify #615's needles do not match the app's prompt** (`client.ts` says "C/A/D are custody proximity,
  access and disclosure role"). The app version is written against what the app actually sends.
- **Deleting `test_packed_layout.js` alone does not unblock the nuclear branch**: `state_snapshot.py:236-238`
  invokes it by path, GOLDEN needs updating, and the branch rewrote generated files. Take master's side on
  every generated file and rebuild.

## Tasks, in order (each ends green and committed)

### 1. The replacement checks, first (app, each with a poison on the real page)

- **C27 Home prints the board's own figures.** Every figure in Home's counts panel and prose equals a
  re-derivation from the raw files the app serves, not from `index.json.counts`: nodes, people and entities
  from `index.nodes` by class; edges from `edges.json`; claims by tier from `claims.json`; events from
  `timeline.json`; map nodes from `map.json`; threads; patents; FOIA requests. Replaces the 12
  figure-scraping checks in `audit_independent.py` (stats strip, breadcrumb, class count). Poison: change
  one digit in the counts panel.
- **C28 No parent-board wording, and the title names this board.** Across every screen the itinerary
  reaches, none of verify #438's nine strings appears in rendered text, and `document.title` names The
  Legacy Program. Poison: append one banned sentence to the Home prose.
- **C29 The analyst is briefed about this board.** Ask a question with the Worker route intercepted
  (fulfilled locally, so no tokens are spent); the request's `system` must name custody proximity, access
  and disclosure role and must carry none of #615's banned phrases. Poison: wrap `window.fetch` so the
  outgoing body says "axes S, P and I".

### 2. FOIA links as their own build step

`tools/build_foia_links.py` runs from the build order (it has its own `__main__`), before `build_app_data.py`.

### 3. Re-point what survives

- `verify.py`: `_l0()` reads `data/l0-model.json`, with an `_L0_OVERRIDE` hook for `--self-test` (the
  pattern of `_LAYOUT_OVERRIDE`). Drop the old-shell checks 265, 415, 438, 471, 523, 565, 587, 615, 664, 694,
  2202 and the markup half of 852; their app replacements are C22, C15, C28, C28, C14, C14, C14, C29, (none
  needed: the strings are the old shell's), C1/`build_app_data --check`, C19.
- `verify.py --idempotent`: run `tools/build.py` twice; hash `app/public/data/**`, `data/the-program.json`,
  `data/l0-model.json`, `data/l0-layout-model.json` (stamp blanked), `data/foia-links.json`.
- `audit_independent.py`: no `DIST`; drop the 12 old-shell checks; fix `mx <= 5 or True`.
- `check_rebuild.py`: `BUILT` loses `dist/the-program.html` and the five `.js` files; gains
  `data/foia-links.json`; its printed instructions become `python tools/build.py`.

### 4. One commit of deletions

The 13 tools (`build_dashboard.py`, `l0_patches.py`, `network_patches.py`, `patents_patches.py`,
`analyst_patches.py`, `precompute_layout.py`, `build_site.py`, `capture_strip.js`, `runtime_check.js`,
`test_packed_layout.js`, `test_scripted_analyst.mjs`, `shoot.js`, `l0_comp.html`), `ref/the-vanishing-v2.html`,
`dist/the-program.html`, `tools/runtime-strip.txt`, `data/program-*.js`, `data/l0-layout-model.js`,
`data/layout.json`, `data/program-meta.js`, and the writers in `merge.py` and `build_l0_layout.mjs`. The six
orphaned NotebookLM band files go, and the export deletes numbered files it did not write this run.

### 5. `tools/build.py` and `tools/gate.py`

- `build.py`: merge, regrade, merge, build_l0, build_design_extract, build_l0_layout.mjs,
  build_foia_links, build_app_data. Stops on the first failure.
- `gate.py`: build (unless `--no-build`), verify, verify --self-test, audit_independent,
  build_app_data --check and --self-test, check_rebuild and --self-test, lint_no_em_dash and --self-test,
  then the app: `npm run build`, a preview it starts and stops on 127.0.0.1:4173, `npm run check`, and
  unless `--quick` `npm run check:poison`. One summary table; non-zero on failure.
- `state_snapshot.py --gate` calls it. `tools/build.sh` goes.
- `gate.yml`: the gate job runs the build, `check_rebuild` and the Python checks only (no browser). The
  app job's poison sweep splits across three parallel jobs (`run.mjs --all-poisons --shard k/3`).

### 6. Merge `nuclear-2026-09-19`

Its authored changes: the new nuclear research files, `research/leads/*`, and one correction in
`research/_corrections.json` and `research/w2-retrieval-literature.json` (the Mansmann misattribution on
`malmstrom-echo-flight-1967`); master has not touched either since the branch point, so the branch's side
is taken. Every generated file: master's side, then rebuild. `data/analyst-suggestions.json`: master's
wording, numerals updated to the rebuilt counts. `verify.py --update-golden`, explained in the commit.

### 7. `CLAUDE.md` to 20 KB or less

History verbatim into `notes/HISTORY-TO-2026-09-24.md`. Keep sections 2, 2a, 5, 6 whole. Rewrite 3
around `tools/gate.py`, 7 around the new file list, 9 as a pointer to the plan and `notes/STATE.md`.
Figures by pointing at `python tools/state_snapshot.py`.

### 8. `notes/STATE.md`, memory, Stewart

## Acceptance

`python tools/gate.py` green; CI green and deployed; the seven nuclear base hubs resolve as node pages in
production; the CI gate job under 4 minutes; `CLAUDE.md` 20 KB or less.
