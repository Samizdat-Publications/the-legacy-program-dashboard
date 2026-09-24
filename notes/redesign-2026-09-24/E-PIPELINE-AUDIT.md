# Appendix E: the pipeline, the gate and CI, mapped for the redesign (24 September 2026)

Produced by a read-only Opus 5.5 agent for `notes/REDESIGN-2026-09-24.md`, at master `838c134`. [M]
measured from code, data or GitHub run records; [I] inferred. Nothing was built, installed or committed.

## 0. Headline findings

1. **[M] The pipeline drops authored research field by field, without a word.**
   - `merge.py` builds entity records without `conflicts`, `unverified` or `openQuestions`
     (`merge.py:465-477`). 63 entity records in 8 files carry 121 such items; 0 shipped entities have
     them (files: arv, tr3b, lazar-s4, dulce, disclosure-project, propulsion, legacy-1947-86,
     w2-places-events). Example: `app/public/data/nodes/arv-fluxliner.json`. CLAUDE.md section 2a says
     the case against a node must live in exactly those fields.
   - 62 edge records use `source`/`tier`, which merge never reads.
   - 89 edge records with unknown types are coerced to `programmatic` with no reject
     (`merge.py:522-523`): `contains` 32, `testimony` 13, `authorship` 6, others. 24 shipped edges exist
     only because of that, and regrade weights that type x3.
2. **[M] Sourcing rules apply per surface, not to the data.** Node claims and edges get them
   (`merge.py:837-1005`). The 1,811 dossier claims do not (loaded raw, `build_l0.py:558-570`), nor do
   timeline events. Of 1,331 Tier 1 dossier claims, 40 cite a secondary source and 22 cite AARO/DoD for
   an outside fact (both would be capped on a node); 50 carry no URL. Verify #45 enforces denial direction
   on the map only; the node page prints "issued here/directed here" for 22 unadjudicated edges
   (`node.ts:155`); the analyst prints every denial row, associations included, as "X denies Y"
   (`tools.ts:678`).
3. **[M] The old shell blocks production deploys** (`deploy.yml:53-70` waits on the whole workflow).
   The critical path is the app job's poison sweep. On 19 Sep (run 35430923882) C11 caught the
   label-mode regression while the old-shell job passed.
4. **[M] Dead weight.** The force-layout bake is "kept, not drawn" (`l0_patches.py:2090`) but fails the
   build on label overlaps (`build_l0.py:826-827`). `data/program-*.js` (9.1 MB) and
   `l0-layout-model.js` (555 KB) have no reader. `l0-model.json` stores dossiers twice (1.9 MB in the
   map rows, 2.2 MB under `dossiers`).
5. **[M] Tier cuts are decided by file order.** 9 nodes tie at the A/B cut, 39 at the B/C cut; stable
   sort orders them by load order. All 1,394 authored tiers in research files are overwritten.

## 1. tools/ inventory

42 code files, 26,563 lines.

| Category | Files | Lines | Bytes |
|---|---|---|---|
| (a) data pipeline | 7 | 4,150 | 213 KB |
| (b) old shell | 13 | 11,896 | 754 KB |
| (c) app | 4 | 1,802 | 78 KB |
| gate and harness | 8 | 4,352 | 215 KB |
| (d) research ops | 9 | 3,074 | 141 KB |
| (e) exports | 1 | 1,289 | 62 KB |

Outside `tools/`: `ref/the-vanishing-v2.html` (4,728 lines), `app/` (9,449 lines, `checks/run.mjs`
1,823), `worker/` (403 lines plus a 217-line test).

- (a) `merge.py` 1,375; `regrade.py` 375; `build_l0.py` 831; `build_design_extract.py` 156;
  `build_l0_layout.mjs` 987; `build_foia_links.py` 194 (called from INSIDE `build_dashboard.py`,
  lines 2497-2498); `make_stubs.py` 232 (by hand).
- (b) `build_dashboard.py` 2,598 (patches the parent board into `dist/the-program.html`, 18.6 MB);
  `l0_patches` 3,530, `network_patches` 856, `patents_patches` 546, `analyst_patches` 271;
  `precompute_layout` 124; `build_site` 81 (nothing runs it); `capture_strip` 62; `runtime_check` 1,545;
  `test_packed_layout` 1,841; `test_scripted_analyst` 114; `shoot` 87; `l0_comp.html` 241.
- (c) `build_app_data` 1,048 (writes `app/public/data`, 1,146 tracked files, 22 MB); `look` 195; `walk`
  477; `make_drawing_thumbs` 82.
- Gate: `verify` 2,976; `audit_independent` 384; `check_rebuild` 273; `state_snapshot` 339;
  `browser_env` 133; `test_browser_env` 165; `probe_browser` 64; `build.sh` 18 (stale: leaves out
  `build_app_data`).
- (d) `corpus_crosscheck` 782; `corpus_absent_groups` 189; `fetch_transcripts` 708; `fetch_podcast` 449;
  `read_transcript` 75; `export_transcripts` 155; `spot_check` 508; `spot_cache_put` 61;
  `set_repo_secret` 147.
- (e) `build_notebook_export` reads `app/public/data` and `_corrections`, writes `exports/notebooklm/`.
- Report files in tools/: read by a program: `REJECTS` (verify #55), `DUPLICATES_ACCEPTED` (#6),
  `GOLDEN` (#56). Written but never read: `INTEGRITY`, `GAPS` (265 KB), `DEMOTIONS` (260),
  `EDGE-DEMOTIONS` (100), `REGRADE_REPORT`, `REMOVED-CLAIMS` (1), `DATE-CONFLICTS` (14); all rewritten on
  every build and committed.

## 2. Build order

```
merge.py #1 -> the-program.json (+ program-*.js, tools/*.json)
regrade.py --(subprocess merge, MERGE_SKIP=_remediation, MERGE_JSON_OUT=tools/_pristine-board.json)--> research/_remediation.json
merge.py #2 -> FINAL data/the-program.json
build_l0.py -> data/l0-model.json
build_design_extract.py -> data/design-extract.json
build_l0_layout.mjs -> data/l0-layout-model.json (+ .js: no reader)
build_dashboard.py -> build_foia_links -> data/foia-links.json   (hidden edge)
                   -> precompute_layout (node) -> dist/the-program.html
build_app_data.py -> app/public/data/ (needs foia-links, so must run after build_dashboard)
app: tsc --noEmit && vite build -> app/dist -> Cloudflare Pages
build_notebook_export.py (by hand) -> exports/notebooklm/
```

Merge runs three times per build; the CI gate job builds everything three times. Authored inputs:
`research/` (104 top-level JSON files plus `dossiers/`, 33 files) and 6 authored files in `data/`
(`denial-adjudication`, `l0-highlights`, `l0-shorts`, `l0-images`, `analyst-suggestions`, the frozen
`l0-extract`), plus a letters note in `notes/` and the vendored parent board. `data/` also holds 11
generated outputs and 2 stale files nothing reads (`layout.json`, `program-meta.js`).

## 3. merge.py

**Load order** (`merge.py:372`): normal files by filename, then `_stubs` (1), `_remediation` (2),
`_corrections` (3); the name test matches anywhere in the full path. `_edge_tiers.json` has an `edges`
key, so merge ingests its 16 records as edges (all 16 match real edges today; a mistyped key would create
a phantom Tier 3 edge).

**Records:** ids canonicalised in one place (`50-60`); people and entities rebuilt into a fixed shape
(`385-513`), losing entity `conflicts`, `unverified`, `openQuestions`, `short` and `domains` without a
reject. Claims (`128-149`): unknown tiers become 3; a missing source becomes "No attributed source on
file"; all 6,047 authored claims are clean. Sources (`82-111`): bare strings accepted; no name and no URL
goes to REJECTS. Edges (`515-545`): stored undirected, keyed `a|b|type`; unknown type becomes
`programmatic`; missing `claimTier` becomes 3; `note` falls back to `summary`; singular `source`/`tier`
ignored. Timeline (`547-564`): deduped on date plus the first 50 characters of the label; unknown strand
becomes "program"; `tier` holds letters on 881 events and numbers on 165; only 219 of 1,059 events carry
any source. entityInfo (`566-580`): longest description wins.

**Same id in several files:**

| Field | Rule | Lines |
|---|---|---|
| person loc, locId, instId, sub, date, age, photoCredit, unexplainedResidual | first file by name wins | 290-293 |
| cluster, person status | default applied once after all files load (19 Sep fix) | 169-184, 326-357 |
| narrative, tierRationale, desc, edge note | longest wins | 294-296, 320-321, 535-536 |
| label | a real name beats a label equal to the id | 247-255 |
| entity dateStart/dateEnd | more precise agreeing date wins; disagreement logged to DATE-CONFLICTS | 258-285, 316-319 |
| axes C/A/D | clamped 0-3, max wins | 156-160, 235-236 |
| node tier | strongest wins, default C | 237-238 |
| edge claimTier | strongest wins, default 3 | 539 |
| sources | merged, deduplicated | 239, 540 |
| claims | added unless the same normalised text is present | 221-231 |
| person affiliations, domains, conflicts, unverified, sequenceChain | merged | 298 |
| chronology | merged on date plus first 60 characters, sorted | 299-305 |

`_corrections` replaces rather than merges (people `420-442`, entities `478-504`; entity
`dateStart`/`dateEnd` corrections are NOT applied). `_remediation` sets tier, rationale, date and coords
(`443-447, 505-509`). `_removed.json` (`592-687`) deletes nodes and edges and re-points aliases.

**Passes** (`1325-1332`): `hoist_claim_urls`; `remediate_tiers` (260 claims demoted today);
`remediate_edge_tiers`; `remediate_interested_party_edges` (100 edges logged); `integrity` (reports, never
fails); `emit` (stamps denial verdicts; an orphan verdict only warns, `1250-1255`).

**Enforced:** unknown overlay ids, empty sources, claims without text, bad chronology, unknown entity
classes (any reject fails verify #55). **Coerced silently:** edge type, strand, precision, cluster, claim
tier. **Not enforced:** person status vocabulary (dead 70, deceased 4, active 198, alive 10, plus unknown,
former, missing, fabricated, resolved), unknown fields, timeline and dossier sourcing.

**Defects measured:** claim dedupe key mismatch (`226` vs `228`) ships 4 duplicate claims (eli-crane,
anna-paulina-luna, hearing-2025-09-09, uap-nda-waiver-directive-2026); entity conflicts/unverified
dropped (63 records, 121 items); 89 edge types coerced; 33 people with conflicting dates never recorded
(robert-bigelow ships 2008-09-22 against 1996-01-01 and 2009-01-01); the `sapoc` dateStart correction is
ignored (right only because the research file was also fixed); `_edge_tiers.json` ingested as edges; 3
stray denial verdicts and 22 denials with no verdict (of 219: 142 directed, 42 association, 13
undirected, 22 none).

## 4. Tiers and the map model

- `regrade.py`: scores degree (cap 40) + 3 x custody/funding/programmatic (cap 20) + 4 x denials (cap
  10) + claim weight (cap 45) + 4C + 3A + 2D; a node without a URL source scores at 0.35x;
  `PROGRAM_EDGES` at line 131; forced 15/35/50 split (A 169, B 398, C 569); every authored tier
  discarded; also fills 36 person dates and 45 location coordinates from a 76-entry table in the script
  (`157-237`).
- `build_l0.py`: structural class or document with at least `FLOOR=6` distinct neighbours; budget 135 by
  degree then file order; highlights by right. Registers: 135 direct / 974 routed / 26 path-only / 1
  unattached. 5,370 connection rows; six entry paths from seed lists written into the code
  (`581-639`); 154 dossiers with 1,811 claims never merged into node claims and never sourcing-checked;
  written twice. Force-layout bake (`331-453`) is dead output that can stop the build. Hand-rolled sine
  and cosine for cross-platform determinism.
- `build_l0_layout.mjs`: columns are 4 eras; rows are the rarest dossier role tag (pinned rarity,
  re-pinned 19 Sep on a 3% margin); every map node needs a dossier.

## 5. The gate

**verify.py, 57 checks:**

| Group | Check line numbers | Fate when the old shell retires |
|---|---|---|
| Data integrity (10) | 67, 86, 94*, 117, 137, 161, 196, 218, 240, 2149 | survive |
| Sourcing rules (4) | 299, 361, 507, 649 | survive |
| Map model read out of the old HTML (10) | 739, 766, 800, 824, 852, 879, 902, 916, 935, 959 | survive once `_l0()` (727-737) reads `data/l0-model.json` |
| Layout model (15) | 1147-1748 | survive |
| Research views (6) | 1772, 1840, 1894, 1919, 1971, 2027 | survive once FOIA links are generated outside build_dashboard |
| Golden counts (1) | 2185 (the only check without a poison, 2791-2793) | survive |
| Old-shell rendering (11) | 265, 415, 438, 471, 523, 565, 587, 615, 664, 694, 2202 | die |

\* 94 tests the old shell's surname plate format. Of the 11 that die, 523 and 565 are already covered by
C14; 438 (parent-board wording) and 615 (analyst prompt) need app versions first. `--idempotent`
(`2233-2283`) rebuilds the old steps twice and hashes `dist/`; it must be re-pointed at
`app/public/data`.

**audit_independent.py, 41 checks:** board data 7 survive; map model re-derived from `l0-model.json` 22
survive; figures scraped from the old shell 12 die. Line 37 opens `dist/` unconditionally (guard it). Line
149 compares against `mx <= 5 or True`, always true.

**state_snapshot.py --gate** runs 10 steps (`224-241`); it does NOT run check_rebuild, the app-data check
or the app checks. Its "unique source URLs" counts distinct source strings (3,865 vs GOLDEN's 1,671).

**App checks C1 to C21**, each with a poison (see Appendix C). Header comments in `run.mjs` and
`gate.yml:10-12` still say C1-C17/C18.

**GOLDEN and check_rebuild:** GOLDEN holds 19 counts; check_rebuild blanks two build-date stamp forms and
compares full bytes of changed files, refuses to run if nothing is newer than `.git/index`, and its
printed instructions leave out build_app_data.

## 6. CI

- `gate.yml`: `gate` job (old pipeline, check_rebuild, old-shell gate) and `app` job (build_app_data +
  plain diff, Worker validators, build, preview, C1-C21, all 21 poisons, look.js). Run 35482093152 (20
  Sep): gate 9m15s (Gate step 8m09s); app 23m09s (checks 1m54s, **poisons 19m48s**). About 24 minutes
  end to end, against 7m16s on 28 Aug.
- `deploy.yml`: on gate success on master, on the exact commit; refuses if `app/dist/transcripts`
  exists; `wrangler pages deploy app/dist --project-name the-program --branch master`, about 47 s. The
  review site is by hand.
- Worker: holds the API key as a Cloudflare secret; pins model, tokens, effort, history (`index.ts:81-94`);
  relays only allowed block types and the 12 tool names; CORS for the two Pages projects and local
  ports; 20/min per IP, 60/min overall; a caller's own key skips limits; deployed by hand.

## 7. Weight and fragility

- Committed generated files: `data/` (19 files, 27 MB), `dist/the-program.html` (18.6 MB),
  `app/public/data` (22 MB). **`.git` is 568 MB, up from 146 MB on 28 Aug.**
- Unread: `program-*.js` (9.1 MB), `l0-layout-model.js`, `layout.json`, `program-meta.js`, the duplicate
  dossier copy, the `legacy` layout dataset (186 KB). `exports/notebooklm/` has 13 band files for 7
  bands; 6 are orphans the export never deletes.
- Steps sessions keep forgetting: run the pipeline before committing research; run build_app_data last;
  capture the strip before the audit; check_rebuild on a clean tree after committing; accept golden
  changes deliberately; start vite preview with `--host 127.0.0.1 --strictPort`; dossier and short label
  for every node joining the map; adjudicate every new denial edge (22 missing, nothing fails); on rebase
  conflicts in generated files take master's side and rebuild; `wrangler deploy` by hand when the Worker
  changes; written counts go stale.

**Retiring the old shell** (CLAUDE.md section 7 plus 4 couplings it does not name: FOIA links generated
inside build_dashboard; the force-layout bake exists only for the old shell; `--idempotent` hashes
`dist/`; audit line 37 reads `dist/` unconditionally). Order: (1) write the two app-side replacement
checks; (2) make FOIA links their own build step; (3) point `_l0()` and `--idempotent` at the new files,
guard the audit's read, drop its 12 checks; (4) in one commit delete the 13 old-shell tools, the parent
HTML, `dist/the-program.html` and its `BUILT` entry; (5) shrink the gate job and state_snapshot; (6)
update the docs. Size [I]: one focused session; about 16,600 lines deleted, 400-600 edited, 150-250 new.
The gate job drops from about 9 minutes to 2-3; end-to-end only drops if the poisons are split across
jobs. Main risk: the 12 dying audit checks are the only independent check of reader-visible numbers.

## 8. Recommendations

1. A typed schema with closed vocabularies; an unknown field or value is an error at load.
2. Per-field merge rules declared in that schema; fix the six merge defects.
3. Sourcing rules applied to every claim-bearing object (dossier claims, timeline, denial direction in
   the app and the analyst).
4. One build command from one declared order; regrade in-process; FOIA links as their own step;
   authored files split from generated ones.
5. A generated data contract for `app/public/data` (JSON Schema to TypeScript types and Python
   validation) and one shared vocabulary module (today the vocabulary is restated in merge,
   build_l0_layout.mjs, build_app_data, l0_patches, verify and audit).
6. Retire the old shell in one session, handling its 4 hidden couplings; drop unread files and the
   force-layout bake.
7. No build-date stamps; commit only research plus the published app data.
8. One fast gate: fold in check_rebuild and the app checks, drop duplicate runs, split the 21 poisons
   across CI jobs.
