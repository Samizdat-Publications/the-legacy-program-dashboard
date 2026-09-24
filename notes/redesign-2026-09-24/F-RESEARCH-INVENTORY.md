# the-program: research/ and backlog inventory

Repo: `C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`
Read only. No files in the repo were edited. Git state was read with `log`, `show`, `diff --stat`
and `merge-base --is-ancestor` only, no checkout of any branch other than the already checked out
`master`.

Master HEAD at time of audit: `838c134` "Handoff: the spine is built and on its own branch, not
parked." (2026-09-19 19:27 -0400). Working tree is clean (`git status --short` shows nothing
pending). Everything counted below is what is actually on master right now, 2026-09-24.

`research/` totals 89.2MB: 24.07MB of authored/committed JSON and MD content, plus 65.15MB in
`research/.transcripts/` (383 files), which is gitignored, cached YouTube captions, and per
`research/leads/README.md` must never be published. A second, unrelated cache, `dist/transcripts/`
(397 files, 46.09MB), also exists locally and is also gitignored; it sits outside `research/` and
is not counted in the 89.2MB.

---

## 1. research/*.json (104 top level files, 10.39MB): theme groups

Every file parsed cleanly as JSON. Counts below are per file as authored (raw contributions), not
deduplicated against the live board: the same real person or document is frequently the subject
of more than one research file, and the "wiring" passes (w6, w10 to w17) mostly add edges between
entities that already exist rather than new entities. Treat these as gross inputs, not net board
growth.

| Theme | Files | Size | people | entities | edges | timeline | gaps |
|---|---|---|---|---|---|---|---|
| AAWSAP/AATIP lineage (aawsap-aatip, w7-dirds-1..4, DIRD verification/legislative edges) | 8 | 715KB | 47 | 101 | 243 | 54 | 24 |
| Congress/oversight legislation (congress-house, congress-senate-legislation, hearing edges, witnesses-2026-09-18, _rs-legislation) | 5 | 730KB | 71 | 85 | 245 | 80 | 40 |
| IC oversight bodies (uaptf-aaro, _rs-aaro-reports, releases-2023-2026, grusch, elizondo-ttsa) | 5 | 1114KB | 79 | 118 | 353 | 171 | 61 |
| Roswell/1940s-2000s crash-retrieval history and literature (history-1940s-1960s, history-1970s-2000s, legacy-1947-86, w2-retrieval-literature, w2-places-events) | 5 | 1262KB | 76 | 137 | 342 | 178 | 61 |
| Lazar/S4 cluster, canon pass 1 (18 Sep) | 1 | 191KB | 9 | 19 | 43 | 27 | 16 |
| ARV/TR-3B cluster, canon pass 2 (18 Sep) | 2 | 267KB | 5 | 15 | 60 | 35 | 28 |
| Dulce cluster, canon pass 3 (19 Sep) | 1 | 177KB | 13 | 16 | 32 | 24 | 12 |
| Disclosure Project witnesses, canon pass 4 (19 Sep) | 1 | 220KB | 13 | 11 | 39 | 24 | 14 |
| Propulsion/antigravity documents (19 Sep, low yield) + pais-patents | 2 | 236KB | 7 | 23 | 34 | 36 | 18 |
| NSC/EO classification and covert-action spine (19 Sep) | 1 | 62KB | 0 | 11 | 24 | 9 | 6 |
| Podcast/media corpus domain files (michels, michels-c, area52, dannyjones, media-structure) | 5 | 943KB | 47 | 81 | 367 | 67 | 88 |
| Technical/agencies/black-budget/contractors/aviators (the w2 macro series, scientists-technical, primes-custody, ffrdcs, aviators-incidents) | 10 | 2744KB | 121 | 400 | 782 | 352 | 150 |
| SAP/classification/statutory wiring (w9, w11-statutory, w12 series, w13 series, w14 legal/institutional edges) | 20 | 443KB | 14 | 20 | 293 | 0 | 0 (22 findings, 13 unresolved) |
| Geographic/international wiring (Brazil, Setka; w6, w10, w11, w12, w13) | 14 | 474KB | 5 | 15 | 308 | 0 | 0 (60 unresolved) |
| Late niche wiring passes (w14 to w17: Aztec, Harvard/Raytheon, Intercept, Las Vegas/Wayne, Navy, ODNI/Peru, Roswell/Clarke, live-originals, thin-people, Wayne ETRD, w8-collapse) | 11 | 84KB | 16 | 8 | 32 | 0 | 0 |
| Board mechanics/meta (`_authority`, `_corrections`, `_remediation`, `_removed`, `_edge_tiers`, `_rs-archive-mirror`, `_rs-sap-docs`, `_rs-stubs-known`, `_stubs`) | 9 | 921KB | 467 | 1166 | 36 | 22 | 96 |
| UI/view config, not research content (`five-observables`, `observables-view`, `patents-view`, `threads`) | 4 | 55KB | 0 | 1 | 3 | 1 | 4 |

Notes on the meta group, because its numbers look wrong until explained:
- `_remediation.json` (272.9KB, 2026-09-19) carries `people: list[338]` and `entities: list[798]`,
  which is exactly the current board total (338 people + 798 entities = 1136 nodes). It is not a
  topic file; it is a whole-board mechanical pass (the kind of fix behind commit `eb9c7f2`, "267
  nodes off their band", and `a8785c8`, a thin-entity-enrichment bug that silently overwrote the
  map band 16 times).
- `_removed.json` (`remove: list[53]`, `alias: dict[21]`) matches `CANON-GAPS-2026-09-18.md`'s own
  citation of "53 removed ids and 21 aliases" exactly, so the two documents cross-check.
- `_corrections.json` (217.4KB) is 86 person-corrections and 46 entity-corrections to existing
  nodes, not new additions.

---

## 2. research/dossiers/ (33 files, 2.15MB)

154 `entityDossier` entries across 33 files, covering **153 unique node ids** (one id,
`nara-uap-collection`, has a dossier entry in two different files). Against 1136 total board
nodes, about 13.5% have a long-form dossier; the rest carry only the base node record (claims and
edges, no `entityDossier`).

Structure is uniform: each file is a JSON array of `{id, entityDossier}`. `entityDossier` always
has `whatItIs`, `whyImplicated`, `roles`, `narrative`, `claims` (array of `{text, tier, source}`),
`openQuestions`. Older batches (w4, w5, w6, w7, w9, w10, w11, w12 dossiers, Aug 2026) also carry
`denialPosture` and usually `connections`; the newer canon-pass dossiers (arv, dannyjones,
disclosure-project, lazar-s4, legacy-1947-86 partially, michels, propulsion, tr3b, all Sep 2026)
dropped `connections` and sometimes `denialPosture`, i.e. the schema was trimmed over time.

Largest contributors: the w5-batch series (12 files, 6-7 dossiers each, ~100KB each, the bulk
entity-dossier build) and w4-entity-dossiers-1..4 (4 files, 5-7 each). The 19 Sept canon-pass
dossiers are much smaller (1-4 entries each): arv (2), disclosure-project (3), lazar-s4 (2),
propulsion (4), tr3b (1).

---

## 3. research/leads/ (325 files, 8.18MB): corpus pipeline + canon audit + backlog

### 3a. File inventory by corpus prefix

| Prefix | Files | Size | What |
|---|---|---|---|
| michels | 97 | 2.75MB | Jesse Michels / American Alchemy corpus pipeline |
| dannyjones | 88 | 1.50MB | Danny Jones podcast corpus pipeline |
| area52 | 70 | 1.32MB | Area 52 podcast corpus pipeline |
| verified | 35 | 2.04MB | Promoted, confirmed findings per corpus (michels incl. C-variant, area52, dannyjones, disclosure-project, dulce, propulsion, tr3b, witnesses-2026-09-18, nuclear-witnesses, arv-mccandlish) |
| gerb | 7 | 338.9KB | UAP Gerb corpus pipeline (smallest, 35 videos) |
| CANDIDATES, BUILD*, VERIFY*, MAPPING*, TRIAGE* (dated 2026-08-30/09-02/09-03/09-18, no corpus prefix) | 26 | ~144KB | The original (first) corpus pass and per-corpus brief/handoff docs |
| README* | 2 | 6.7KB | Pipeline documentation |
| CANON-GAPS-2026-09-18.md | 1 | 76.3KB | The canon coverage audit (see 3b) |
| NSC-EO-SPINE-2026-09-19.md | 1 | 21.5KB | The NSC/classification-spine triage note (see 3c) |
| cached-transcripts.json | 1 | 4.8KB | 24 spot-checked transcript items outside the main batch pipeline |
| disclosure/dulce/propulsion denial-verdicts.json | 3 | ~2.9KB | Small claim-vs-counterclaim adjudication patches (see 3d) |

Each of the four podcast corpora (michels, area52, dannyjones, gerb) follows the same pipeline
shape: `*-candidates-NN.txt` (raw entity mentions per batch) to `*-corpus-NN.md` (batch transcript
digest) to `*-triage-N.md` (6 grouped analysis passes, A/B/C/D graded) to `verified-*-N.md`
(5-7 chunks of confirmed findings) to `*-crosscheck.json/.txt` (classified NODE / PROSE / ABSENT
against the live board) to `*-absent/group-N.tsv` (the board-has-never-heard-of-it leads, split
into 6-7 groups). `*-crosscheck.json` result counts: michels 1609, dannyjones 981, area52 895,
gerb 200.

### 3b. CANON-GAPS-2026-09-18.md: the canon audit and its 15 proposed passes

Read-only audit, 18 Sept 2026, against a 241-entry canon list (figures/places/events/documents/
orgs an informed reader would expect). Board state at that time: 1,057 nodes (from
`app/public/data/index.json`) and `data/the-program.json` at 311 people / 746 entities / 2,460
edges. Method: regex over `id`/`label`/`short`, cross-checked against `research/_removed.json`.
Result: **92 of 241 already on the board; 149 gaps** (22 Band 1 "conspicuous", 58 Band 2
"notable", 69 Band 3 "peripheral, or a mention suffices"). Section 4 of the document groups the
Band 1+2 gaps (80 entries, ~95 nodes once folds and sets are counted) into **15 numbered passes**.

Cross-checked against the current board (`data/the-program.json`, `git log`, `grep` for
representative node ids) rather than taken on faith:

| # | Pass (per CANON-GAPS doc) | Built? | Evidence |
|---|---|---|---|
| 1 | Area 51/S-4: the Lazar cluster | **Built** | `research/lazar-s4-2026-09-18.json` + dossier; commit `6f937fa`; ids `bob-lazar`, `klas-tv`, `lanl` present in `data/the-program.json` |
| 2 | The ARV thread (McCandlish, Fluxliner, Norton AFB, TR-3B as an origin note) | **Built** | `research/arv-2026-09-18.json` + `tr3b-2026-09-18.json` + dossiers; commits `065f305`, `409a84f`; ids `mark-mccandlish`, `tr-3b` present |
| 3 | Dulce and the Bennewitz affair | **Built** | `research/dulce-2026-09-19.json` + dossier; commit `e153f3e`; id `dulce-base` present |
| 4 | Disclosure Project 2001 witnesses | **Built** | `research/disclosure-project-2026-09-19.json` + dossier; commit `4ab0cbe` ("68 witnesses, graded"); id `clifford-stone` present |
| 5 | Astronauts, ministers, officials on the record | **Not built** | ids `edgar-mitchell`, `paul-hellyer`, `gordon-cooper` absent from `data/the-program.json` |
| 6 | 1947 and the MJ-12 named list | Not built | `vannevar-bush` absent |
| 7 | Blue Book, Robertson Panel, sceptics | Not built | `carl-sagan` absent |
| 8 | 1947-86 crash-claim literature and its sources | Not built | no corresponding research file exists |
| 9 | Trinity, Magenta, pre-Roswell claims | Not built | " |
| 10 | Oversight refused: Goldwater, LeMay, Blue Room | Not built | `barry-goldwater` absent |
| 11 | Contractors, ranges, custody | Not built | " |
| 12 | The media substrate (Art Bell, Rogan, Danny Jones-the-channel, King) | Not built | `art-bell`, `joe-rogan` absent |
| 13 | Modern claimants and the current fight | Partially | `michael-herrera` IS present, but via the congressional-witnesses pass (`7a1c6df`), not this cluster; `gary-mckinnon` absent |
| 14 | Allied and civil-aviation records | Not built | " |
| 15 | Antigravity research, named (Ning Li, Podkletnov, Cook, Bushman) | Not built | `ning-li`, `boyd-bushman` absent; `propulsion-2026-09-19.json` opened 4 propulsion documents but each "says less than is claimed for it" (commit `c588c8c`) and did not create these people |

So: **4 of 15 passes built and merged, 1 partial (a name that arrived by a different route), 10
not started.** Passes 1-4 are explicitly called out in the doc's own text as "the ones that answer
the owner's complaint directly", and that is exactly what got built.

Board growth from the 18-19 Sept work, confirmed against current `data/the-program.json`
(generated 2026-09-19, 338 people + 798 entities = 1136 nodes, 2685 edges, 1059 timeline events):
net **+79 nodes, +225 edges** over the 18 Sept baseline (1057 nodes, 2460 edges). Current tier mix:
people A34/B104/C200; entities A135/B294/C369.

### 3c. NSC-EO-SPINE-2026-09-19.md

A separate, unplanned gap (not one of the 15 canon passes; sourced from `notes/HANDOFF-2026-09-19
-LATE.md` item 3, "the cheapest documented gap available"). Verified 9 primary documents (NSC
charter, National Security Act of 1947, NSC 5412, NSAM 303, NSDD 159, EO 10501/11652/12036/12356,
Atomic Energy Act of 1954) and flagged 6 widely-repeated claims about them that are wrong on the
primary text (e.g. "NSAM 303 is part of the secrecy spine": false, it is a 2-sentence renaming
memo). **Built and merged**: `research/nsc-eo-spine-2026-09-19.json`, commits `40c8b58` (triage)
and `f803638` ("the spine the board was missing: eleven instruments"); ids `national-security
-council` and `nsdd-159` present on master.

### 3d. The nuclear-facility witness register: complete but NOT merged

This is the one item the task brief specifically asked to trace through git, and it is the most
important backlog finding in this audit. Sequence, from `git log`:

- `d545a79` (19 Sept) "the nuclear cluster parked on a branch rather than pushed red" - built, but
  deliberately kept off master pending a rendering fix.
- `c3c6946` reverted ALL of the 19 Sept research run from master ("the board has outgrown label
  mode at 1920") ... `8c7f98d` fixed the underlying budget problem ... `5e7050e` un-reverted,
  restoring Dulce/Disclosure-Project/propulsion/NSC-spine to master.
- `359958f`, branch `nuclear-2026-09-19` only: "The nuclear-facility witness register: 47 names,
  seven base hubs... **Canon pass 5**, and the pass Stewart asked for directly: 'we have to find a
  way to document even loose evidence like testimonies.'" 19 people, 29 entities, 77 edges, 192
  claims, 7 denial verdicts. Dossier: `research/leads/verified-nuclear-witnesses-2026-09-19.md`
  (100.6KB, already on master). New base hubs: `l-loring`, `l-wurtsmith`, `l-minot`,
  `l-ellsworth`, `l-warren`, `l-grand-forks`, `strategic-air-command`.
- Confirmed with `git merge-base --is-ancestor 359958f master`: **exit 1, false**. It is the only
  commit on `nuclear-2026-09-19` not on master. Confirmed with `git diff --stat master
  nuclear-2026-09-19`: touches almost the entire `app/public/data/` tree (a full rebuild, not an
  incremental patch).

So the sequential "pass 5" actually executed is NOT the CANON-GAPS doc's cluster 5 (astronauts/
officials); Stewart redirected it to an entirely new, non-canon-list investigation, and that
finished, verified work (47 witnesses) is sitting complete and unmerged on its own branch. Its
core finding, per the commit message: of 47 named witnesses, 26 reached the record through
contemporaneous official paper (message traffic, memoranda for record, duty logs, a Blue Book
phone log) versus 13 through a researcher's interview programme, "the one seam in the subject that
is documented rather than only attested."

### 3e. Denial-verdict backlog

Three small JSON patch files record claim-vs-counterclaim adjudications for named node pairs, not
yet folded into `_corrections.json`: `disclosure-project-denial-verdicts.json` (6 pairs, e.g.
`philip-j-klass|clifford-stone`), `dulce-denial-verdicts.json` (4 pairs), `propulsion-denial
-verdicts.json` (4 pairs). Commit `5b0b62f` found that a denial-weighting bug's "real defect was
eleven missing verdicts", so this is an active, tracked backlog category, not dead weight.

---

## 4. research/testimony/ and research/patents/

**testimony/**: one file. `elizondo-house-oversight-2024-11-13.txt` (7KB). Thin: the rest of the
subject's testimony/hearing content (Grusch, TTSA, congressional hearings, podcast testimony) is
folded into the `research/*.json` domain files and `leads/verified-*.md`, not archived here as raw
transcript text. This directory does not reflect how much testimony has actually been processed.

**patents/**: 5 patent texts (US10135366, US10144532, US10322827, US20190058105, US20190295733;
~167KB total, the 5 Navy "Pais patents"), `drawings/` (11 PNGs extracted from the filings plus a
`thumbs/` cache and a `PROVENANCE.md`, ~3MB), `wrapper/` (USPTO prosecution-history text files plus
a 26KB `drive-index.tsv`, ~80KB).

Concrete backlog in `patents/wrapper/MISSING.md`: application **15/141,270 (PAX 205)** is complete
only through 20-21 Aug 2018; missing after that are the Examiner's Answer, the **Notice of
Allowability and Reasons for Allowance** (flagged as "the single most informative document still
unobtained on this node"), the Issue Fee transmittal, and the maintenance-fee record. The document
names the exact ask: "documents dated after 20 August 2018 only... a handful of papers, not
another thirty." Three more applications, **15/431,823, 15/678,672, 15/928,703**, are "still
outstanding entirely." By contrast, application 14/807,943 (PAX 182) is complete through grant.

---

## 5. Corpora mined and queued

| Corpus | Episodes | Batches | Crosscheck results | Files/size in leads/ | Status |
|---|---|---|---|---|---|
| Jesse Michels / American Alchemy | 140 (`michels-episodes.json`, `michels-rss.json`) | 35 | 1609 | 97 files / 2.75MB | Mined; plus a "C" supplementary pass and one fresh single-video triage (`rjUdn6FklAU`, 19 Sep) outside the batch pipeline |
| Area 52 | 107 (implied; 27 batches x ~4) | 27 | 895 | 70 files / 1.32MB | Mined |
| Danny Jones | 136 (implied; 35 batches x ~4, per `dannyjones-candidates.txt.batches.tsv` reaching batch 35) | 35 | 981 | 88 files / 1.50MB | Mined |
| UAP Gerb | 35 videos | 3 corpus files (01-12/13-24/25-35) | 200 | 7 files / 338.9KB | Mined; already contributed 9 pre-existing board nodes (MITRE, NRO, Hidden Wing, Northrop/TRW, Battelle, Sandia investigations, Jan 2026 American Alchemy episode) per `leads/README.md`; plus one fresh single-video triage (`o4czWtSxGig`, 19 Sep) |
| Congressional hearings | n/a | n/a | n/a | 1 raw transcript (`testimony/`) | Only Elizondo 2024-11-13 archived as raw text; the rest lives in domain JSON, not as testimony transcripts |
| `research/.transcripts/` cache | - | - | - | 383 files / 65.15MB | Gitignored, never published; raw auto-generated YouTube captions behind all four corpus maps above; source of known caption corruption (e.g. "Holocron Engineering" was really HoloChron LLC); still-unresolved corrupted names per `leads/README.md`: "Sand Corp.", "SGA", "Eric Tabor", "Charles Ethan Ray", "Special Project Astra" |

**Queued / not yet mined**: no dedicated fifth podcast corpus exists. The actual backlog is (a)
the 10 remaining CANON-GAPS clusters (passes 5-12, 14-15, ~55-60 people/places/events, see 3b),
(b) the finished-but-unmerged nuclear-facility witness register (3d), (c) the 3 unfetched patent
applications and 1 incomplete one (4), and (d) the denial-verdict backlog (3e).

---

## 6. Surprising findings

1. **The canon-pass numbering is not stable.** CANON-GAPS-2026-09-18.md's "15 passes" (section 4)
   is a thematic cluster list. The commit log's "Canon pass N" is a separate, sequential counter
   over what actually got researched (1 Lazar, 2 ARV/TR-3B, 3 Dulce, 4 Disclosure Project, 5
   nuclear witnesses). Passes 1-4 happen to line up with clusters 1-4 of the doc; pass 5 does not
   line up with cluster 5 at all, it is a different, directly-requested investigation. Anyone
   reading "pass 5" in isolation would misidentify which content it refers to.
2. **The most recently finished research (the nuclear witness register, verified, dossiered, 47
   names) is the one thing not in production.** It was deliberately parked, then master reverted
   and un-reverted around it over 5 commits in one day (label-rendering budget at 1920 nodes), and
   it is still sitting one commit off master a week later.
3. **`_remediation.json`'s counts (338 people / 798 entities) exactly equal the live board total.**
   It is not a topical file at all, it is a whole-board sweep, and it is filed alongside 103
   genuine research passes with no marking to distinguish it at a glance.
4. **testimony/ is misleadingly thin.** One 7KB file gives no signal that testimony is in fact one
   of the best-covered categories on the board; it is just stored elsewhere.
5. **65 of the 89MB under research/ is a gitignored cache**, not authored content; the "92MB"
   figure is mostly raw YouTube captions, not research output.
