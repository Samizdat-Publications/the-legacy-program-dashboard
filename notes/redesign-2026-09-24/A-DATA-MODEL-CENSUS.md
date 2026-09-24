# Appendix A: the data model and a census, for the redesign (24 September 2026)

Produced by a read-only Opus 5.5 agent for `notes/REDESIGN-2026-09-24.md`, on master `838c134` (board
generated 2026-09-19). The numbers are in `census-2026-09-24.json` (sections `headline`, `detail`,
`latent`, `extras`); the scripts are `tools/analysis/census/census.py`, `latent.py`, `extras.py` (run in
that order; they write to `CENSUS_OUT` or the system temp dir, never into the repo). Items marked
*(heuristic)* are lexicon or pattern estimates; everything else is a direct count.

## 1. Data dictionary

A = where authored, M = where merged or derived, S = where it ships in `app/public/data/`.

| record (n) | A | M | S | fields and vocabulary |
|---|---|---|---|---|
| person 338 | `research/*.json` people[] | `merge.py:385-455`, `_corrections`, `_remediation` | index.json, nodes/<id>.json | `status` 9 values; `date` has no fixed meaning; `loc`/`locId`/`instId` never read by the app; `domains` tags 46 `d-*` topic nodes; `sub` unique per person; `chronology` 1,316 entries; `conflicts` 102; `unverified` 213 |
| entity 798 | entities[] | `merge.py:457-513` | same | cls: document 237, institution 196, event 87, program 82, location 73, legislation 64, domain 59. `sub` 718 distinct values; `dateStart` on 698; `coords` on 45 (locations only, from a gazetteer written into `regrade.py:157-237`) |
| edge 2,685 | edges[] | `merge.py:515-545`, tier passes 877-1005 | edges.json (a, b, t, tier, label, dateStart); full rows only inside node files | 12 types; `label` and `note` free text; `claimTier`; dates; `sources[{name,url,date}]`; `denialKind`/`denier` |
| claim 5,897 | node claims[] | `merge.py:128-149`, demotion 837-869 | claims.json, node files | only `{tier, text, source}`, source a string; **no id, no date, no speaker, no document or event link** |
| timeline 1,059 | timeline[] | `merge.py:547-564` | timeline.json | 4 strands; `node` links 576 nodes; `tier` mixes A/B/C with 1/2/3; `source(s)` not shipped |
| thread 8 | `research/threads.json` | verify.py | threads.json | steps: node, year, evidence, edge type/tier; 44 nodes |
| dossier 153 | `research/dossiers/*.json` | `build_l0.py:558-570` | node `dossier` | whatItIs, whyImplicated, 8 roles, 1,797 separate claims, 805 openQuestions; no person has one |
| gap 618 | gaps[] per file | `tools/GAPS.json` | not shipped | keyed to the research file, never to a node |
| FOIA 17 | `notes/FOIA-LETTERS-2026-08-29.md` | `build_foia_links.py` | foia.json | `questions` index into `dossier.openQuestions`; 42 nodes; none filed |
| patent 5, authority 12 (23 nodes), highlight 14 | `patents-view.json`, `_authority.json`, `l0-highlights.json` | build_app_data / build_l0 | patents.json, highlights.json (authority not shipped) | |
| overlays | `_corrections` 86 people / 46 entities; `_remediation` (all nodes); `_edge_tiers` 16; denial-adjudication 200; `_removed` 53 plus 21 aliases | merge overlays | effects only | |
| L0 map | computed | `build_l0.py`, `build_l0_layout.mjs` | map.json; band, era, l0, members | 135 map nodes; 974 members; band = rarest dossier role |
| entityInfo 88 | research entityInfo{} | `merge.py:566-580` | node files | 20 keys are not node ids and never ship; **14 of them are storyline essays** |

## 2. The ten decision-relevant numbers

1. Median node has 3 distinct neighbours (people: 2). The map shows 11.9% of nodes, threads 3.9%,
   dossiers 13.1%.
2. `institutional` alone is 720 of 2,685 edges (26.8%). **2,539 distinct edge labels for 2,685 edges.**
   89 authored verbs (35 distinct: contains, testimony, authorship, amends, codifies ...) were coerced to
   `programmatic` at `merge.py:522-523`.
3. 61.8% of claims (3,643 of 5,897) have no URL; 3,865 distinct source strings; 42.8% resolve to neither a
   URL nor a document identifier.
4. Of the 40 most-cited documents, 30 already exist as document or legislation nodes and 3 as hearing
   events. **1,692 claims cite a document that is already a node, only through a free-text string.**
5. Person links the app never shows: 227 `instId` (101 also drawn as edges), 207 `locId` (16 drawn), 694
   topic tags (5 drawn). `build_app_data.py:458` overwrites `domains` with provenance, so the topic tags
   do not ship at all.
6. 98.2% of nodes (1,116) carry a topical research-file slug; 863 carry exactly one. Case files are
   tightly knit: the share of a case file's edges joining two of its own nodes is Dulce 1.00, propulsion
   0.96, Lazar/S-4 0.91. (Podcast corpus files are provenance, not topics: within-file share 0.01-0.05.)
7. Place: coordinates on 45 nodes, all locations. 0 of 87 events geocoded; 23 touch a location node.
   30.3% of nodes have any direct place field.
8. Time: 89.5% of nodes dated. 1,442 claims contain a day-precision date; only 417 match a timeline event
   on the same node. 45% of timeline events fall in the 2020s.
9. The case against is half-carried: merge drops entity `conflicts` (31 authored) and `unverified` (49
   authored), including S-4, Dulce base and TR-3B (Appendix E puts it at 63 records, 121 items).
10. **Claims about a case are scattered:** Roswell has 11 claims on its node and 79 on 55 other nodes. 1,400
    claims name another node, and 939 of those node pairs have no edge. *(heuristic)*

## 3. Edge types: coarse buckets, not verbs

- The verb exists only inside a unique free-text label. Types double as tier weights (x3 in
  `regrade.py:131`), so authors file edges strategically; nine edge notes say outright that "the board has
  no authorship edge type".
- Testimony wording appears under 11 of the 12 types, authorship wording under 10. Only 53% of `funding`
  labels read as funding, 32% of `institutional` labels read as a role. *(heuristic lexicon)*
- No direction convention: the repo's own audit found denial direction wrong on 34 of 124 edges (27%).
  Of 219 denials: 142 directed, 42 association, 13 undirected, 22 unadjudicated.
- The old shell derived links from shared `instId`/`locId`/domains/dates (`build_dashboard.py:802-856`);
  the app has nothing equivalent. The app's only derived lines are 132 shared-member pairs between map
  nodes.

Three real examples per type (a -> b: label):

| type | examples |
|---|---|
| institutional | MITRE -> JASON "administered JASON since 2002"; Inman -> NSA "Director ... from 5 July 1977"; Chadwell -> Bedell Smith "memoranda were addressed to him" |
| programmatic | COMETA -> 1999 report "produced the 1999 report"; MOGUL -> Roswell Reports "load-bearing element of the official explanation"; AAWSAP -> AATIP "official name vs Reid's name" |
| investigative | Entropy paper -> Nimitz "analysed quantitatively"; Burchett -> Eglin AFB "accompanied Gaetz"; Graves -> PURSUE "set the four-element test" |
| denial | Gough -> Immaculate Constellation report "no record"; Friedman -> Randle "dispute over MJ-12" (not a denial); Minot 1968 -> Blue Book "declined to field-investigate" |
| legislative | NDAA FY22 1683 -> AARO "statutory basis"; Schiff -> GAO/NSIAD-95-187 "directed GAO"; CAUS -> CAUS v. NSA "plaintiff" (litigation) |
| witness-chain | Michels -> Barber "published account"; Hynek -> McDonald "both testified 1968"; Lazar -> Teller "claimed 1982 meeting" (T3) |
| research | Davis -> wormholes DIRD "author of record"; Disclosure Project Briefing -> Greer "Written and compiled by"; Kotlikoff -> Skidmore "co-authored" |
| custody | DIA -> microwave DIRD "published, numbered and released" (a document); Herrera -> Greer "custodian of the written testimony"; FAB -> Arquivo Nacional "transferred its UAP holding" |
| temporal | Reagan -> Nimitz "same year, same behaviour"; Bedell Smith -> 1952 DC sightings "instruction follows the wave"; Galileo -> ODNI assessment "founded in response" (causation) |
| geographic | FTD -> Wright-Patterson "stationed at"; Aztec claim -> Aztec NM "alleged crash site"; International domain -> Toulouse "GEIPAN's base" |
| behavioral | Keoki Jackson -> Lockheed ADP "arrived at MITRE from Lockheed" (career move); DIRD series -> custody domain "exhaustive on paper flow" (argument); documentary -> Puthoff "among 34 interviewees" |
| funding | Reid -> Appropriations Acts "directed the $22M"; Stony Brook -> DOE "contracting agency"; Kirkpatrick -> ORNL "post-government employment" |

## 4. Sources

- Claim sources resolve to **724 canonical documents**; 249 are cited only once; 180 match a document or
  legislation node, 207 if event nodes count. Hearing transcripts, the three most-cited sources (179
  claims), exist only as event nodes.
- **Edge sources are already structured objects:** 97.7% have a URL, 88% a date; 494 documents are cited
  by both claims and edges.
- 1,779 raw unique URLs (1,669 normalised), not the 3,541 CLAUDE.md section 1 states. Top claim-source
  domains: govinfo 227, archive.org 207, dia.mil 181, blackvault docs2 101, irp.fas.org 80.
- Source classes *(heuristic)*: publication text without URL 2,080; government/military URL 1,011;
  document identifier without URL 795; news/web URL 610; archive or FOIA mirror 582; inference 336;
  speaker/testimony without URL 324. A source string names a person node in 1,286 claims; 442 claims on
  a person node are sourced to that same person.
- 39 "Board bookkeeping" placeholder claims, all T3 and the same sentence (6.7% of T3). 324 claim sources
  are marked Inference or Reasoning; 83 cite internal repo paths.

## 5. Latent groupings the redesign can use

| signal | coverage |
|---|---|
| topic and case research-file slugs | 1,116 nodes, 2,500 edges |
| L0 containment (direct or routed) | 1,109 nodes (97.6%) |
| the 59 `domain` topic nodes (incl. person tags) | 404 nodes, 264 of them people |
| event and programme hubs | 164 people (48.5%) touch at least one |
| any place signal | 452 nodes |
| dated | 1,017 nodes |
| dossier roles | 149 nodes |
| threads plus entry paths | 44 and 100 ids |
| `cluster` used as a provenance tag | 132 records (125 nodes) |
| id families | dird 35, aaro 15, ndaa 14, usc 10, hearing 8 |
| orphaned storyline essays | 14 |
| gaps / open questions | 618 / 805 |

- Largest topic files: w2-taxonomy 75, w2-international 58, primes-custody 56, scientists-technical 55,
  congress-house 55, history-1970s-2000s 53; newer case passes: dulce 29, lazar-s4 28,
  disclosure-project 24, propulsion 23, legacy-1947-86 23, tr3b 11, nsc-eo-spine 11, arv 9.
- Domain topics overlap: d-nuclear/d-nuc, three ffrdc variants, d-legislative/d-legislation,
  d-sap/sap-taxonomy, d-denial/d-coverup; 4 domain nodes are unused.
- Event nodes by label *(heuristic)*: incident 43, hearing 13, release 7, meeting 3, other 21; the union of
  their one-hop neighbourhoods is 252 nodes.
- **Orphaned essays in entityInfo** (never shipped): how-money-reaches-an-invisible-program,
  the-named-mechanism, the-21-trillion-stated-precisely, sffas-56-what-it-actually-permits,
  why-the-failed-audit-is-evidence, the-classified-programs-arithmetic, thesis, throughLine, scope,
  methodNote, cia-haines-1997, ndaa-fy2024-sec1687; plus entityInfo stranded under collapsed ids
  `dird-collection` and `dod-sapco-arch` because aliases are not applied to entityInfo.
- Affiliations *(heuristic)*: 356 of 875 affiliation strings name a node; 167 of those person-node pairs
  have no edge.

## 6. Field details

- Person `date`: day 307, year 9, month 1, "1990s" 1, null 20. `locId` 56 distinct (`l-dc` 78); `instId`
  102 distinct (211 institutions, 15 programs, 1 document). Top topic tags: `d-coverup` 100, `d-oversight`
  91, `d-witness` 50. `unverified` stored as a bare string on 4 people; `photoCredit` never set.
- Entity `dateStart` precision: year 429, day 240, month 27; 289 have a range. Id prefixes inconsistent
  (`l-` on 71 of 73 locations, `d-` on 53 of 59 domains, `ev-` on 8 of 87 events, `doc-` on 5 of 237
  documents); 8 ids authored with two different classes.
- Edge `dateStart` precision: year 1,457, day 557, month 148. 110 node pairs carry 2-3 edges; 489 edges
  came from 2+ files. 78 records authored `tier` instead of `claimTier`, 62 `source` instead of `sources`;
  merge ignores both keys (rescued only because each merged with a twin from another file).
- Claims per node: median 4, p90 9, max 48; two nodes have none (`l-san-diego`, `l-virginia`); 264 carry
  the "DEMOTED from Tier 1" marker; 65 claim texts are duplicated across nodes (240 rows).

| class | T1 | T2 | T3 |
|---|---|---|---|
| person | 925 | 713 | 131 |
| document | 964 | 252 | 115 |
| institution | 665 | 197 | 118 |
| program | 286 | 107 | 59 |
| legislation | 403 | 22 | 48 |
| event | 240 | 209 | 37 |
| domain | 154 | 35 | 22 |
| location | 64 | 83 | 48 |

- Timeline by decade: 1940s 34, 1950s 49, 1960s 44, 1970s 36, 1980s 75, 1990s 86, 2000s 106, 2010s 148,
  2020s 481. The 881 letter tiers come from most research files; the 165 numeric ones from `sap-`, `tx-`,
  `spine-` and some `tl-` ids.

## 7. Weaknesses

- Overloaded fields: `entity.sub` (190 ids authored with conflicting values); `status` (9 values mixing
  vital, role and editorial states; 47 "active" people hold former roles *(heuristic)*); timeline `tier`
  (two vocabularies); `domains` (topic tags on the board, provenance in shipped files); `tierRationale`
  (100% machine-generated).
- Shipped but never rendered: `instId`, `locId`, chronology, sequenceChain, affiliations, node-level
  sources. Not shipped: timeline sources, gaps.
- Missing facets: claim ids, dates, speakers; place on events; a case/topic field; aliases; "how the claim
  reached us".
- An undetected duplicate: `gao-nsiad-95-187` and `gao-roswell-report-1995` are the same report. Detected
  but unresolved: dodm-5205-07 series/v1, gimbal/gofast videos, l-skinwalker/l-utah, earthtech/IASA.
- The `cluster` fallback puts 103 nodes in "other". "Tier" names three grading systems (node A/B/C, claim
  1/2/3, edge claimTier).
- `SCHEMA.md` is stale (3 status values documented, 9 in use; says geographic/research/temporal edges are
  derived by rule, all 380 are hand-written; says axes are never summed, `regrade.py:150` sums them; says
  tier A means "named in sworn testimony", it is a forced percentile).
- CLAUDE.md section 1 figures are stale (1,057 / 2,460 / 5,303 / 913; now 1,136 / 2,685 / 5,897 / 1,059).
