# Appendix T: the topic taxonomy, draft v1 (24 September 2026)

**What this is.** The first cut of the layer the board is missing: about 75 topics in 10 sections,
drafted from four kinds of evidence, not from a blank page:

1. the 17 measured communities (Appendix B, `communities-2026-09-24.json`, ids H0 to H16);
2. the 59 `domain` nodes, which are editorial topics already written into the graph as if they were
   entities (`d-funding`, `d-custody`, `four-regime-map`, `sap-taxonomy` ...);
3. the eight authored threads and the 14 start-here flags;
4. the canon audit's clusters (`research/leads/CANON-GAPS-2026-09-18.md` section 4), so the gaps have a
   home before they are built.

**Status: DRAFT.** Phase 3 of `notes/PLAN-2026-09-24.md` validates it against the data: every topic must
reach at least 6 member nodes that exist on the board, or be merged into a neighbour, or be marked
`research-gap` (a topic the canon says should exist and the board cannot yet fill). Anchors below are
real node ids checked against `app/public/data/index.json` on 24 September 2026 (degree in brackets
where it helps). Anything marked **(gap)** has no node yet.

**Kinds** (a facet on every topic): `incident` (a dated event or encounter), `programme` (an official
effort), `allegation` (a claim about custody or a hidden effort), `mechanism` (how secrecy, law or money
works), `hearing` (congressional or legal proceedings), `saga` (a person-centred story), `document`
(a document trail), `institution` (an organisation's history), `nation` (a country's record), `movement`
(media and civilian research).

**Roles** (each member node carries one per topic): `subject`, `witness`, `claimant`, `official`,
`investigator`, `institution`, `document`, `law`, `place`, `critic`, `media`.

---

## Section 1. The early record, 1944-1969 (communities H4, H8; canon 6 to 9)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `wave-1947` | Kenneth Arnold and the 1947 wave | incident | `kenneth-arnold` | thin today; may merge into `sign-estimate` |
| `roswell-1947` | Roswell, July 1947 | incident | `roswell-1947`, `jesse-marcel`, `gao-nsiad-95-187`, `project-mogul`, `steven-schiff` | the anchor topic of the section; carries the 1978-80 revival and the 1994-97 USAF reports as its tail |
| `crash-claims-1940s-60s` | Other crash-retrieval claims: Aztec, San Agustin, Kingman, Kecksburg | allegation | `aztec-1948`, `plains-san-agustin-1947`, `kingman-1953`, `kecksburg-1965`, `stringfield-status-reports`, `frank-scully` | canon 8 and 9 (Trinity, Magenta) extend it |
| `sign-estimate` | The Twining memo, Project Sign and the Estimate of the Situation, 1947-49 | programme | `twining-memo`, `project-sign`, `estimate-of-the-situation`, `project-grudge`, `nathan-twining` | |
| `blue-book` | Project Blue Book, 1952-1969 | programme | `project-blue-book` (27), `blue-book-special-report-14`, `j-allen-hynek` | provincial hub: 74% of its neighbours are inside its own community |
| `robertson-cia-1953` | The CIA and the Robertson Panel, 1952-53 | programme | `robertson-panel`, `cia`, `howard-p-robertson` | |
| `condon-1966-69` | The Condon Committee and the end of Blue Book | programme | `condon-committee`, `edward-condon`, `low-memo` | carries the Hippler letter of 16 January 1967 |
| `mj12-documents` | The Majestic-12 documents | document | `mj-12-documents`, `majestic-documents-archive` | canon 6 (Vannevar Bush and the named list) extends it |
| `cold-war-intelligence-context` | CIA secrecy precedents of the 1950s (MKULTRA, the Olson death) | institution | `mkultra`, `frank-olson-death-1953` | context only; merge or drop in phase 3 if it does not reach 6 members |

## Section 2. The secrecy machinery: law, classification and money (H6, H12, H13; domain nodes)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `nsc-spine` | The National Security Act and the NSC spine, 1947-1985 | mechanism | `national-security-act-1947`, `national-security-council`, `nsc-5412`, `nsdd-159`, `nsam-303` | `nsam-303` belongs as the correction (a two-sentence renaming memo) |
| `classification-orders` | Classification orders from EO 10501 to EO 13526 | mechanism | `eo-10501`, `eo-11652`, `eo-12065`, `eo-12356`, `eo-13526` | |
| `atomic-secrecy` | Atomic energy secrecy and "born classified" | mechanism | `atomic-energy-act-1946`, `atomic-energy-act-1954`, `atomic-energy-commission`, `d-nuclear` | the phrase does not appear in the 1954 Act; the topic says so |
| `sap-states` | Special access programmes: acknowledged, unacknowledged, waived | mechanism | `sap-taxonomy`, `waived-usap`, `waived-usap-mechanism`, `sap-cover-mechanisms`, `d-sap` | the two `waived-usap*` nodes are a duplicate candidate |
| `sap-reporting` | Who gets told: 10 U.S.C. 119, the Gang of Eight, the waived-SAP notification group | mechanism | `usc-10-119`, `usc-10-119e`, `waived-sap-notification-group` (31), `gang-of-eight`, `four-regime-map`, `sap-readin-gate` | start-here flag 2 and 3 live here |
| `sap-governance` | The SAP oversight machinery: SAPCO, SAPOC, the Senior Review Group | mechanism | `dod-sapco` (18), `sapoc`, `ic-sapco` | `sapoc` was established 5 January 1994 (do-not-undo) |
| `carve-outs` | Carve-outs and contractor security oversight | mechanism | `carve-out`, `d-contractor` | start-here flag 7 |
| `black-budget` | The classified budget: annexes, NIP and MIP, unvouchered funds | mechanism | `classified-annex`, `nip`, `mip`, `nip-fy2013-summary-disclosure` | |
| `unauditable-ledger` | The unauditable ledger: DoD audits and SFFAS 56 | mechanism | `dod-agencywide-audit`, `sffas-56` | start-here flag 8 |
| `funding-channels` | How a programme gets paid: transfers, reprogramming, IR&D, contracts | mechanism | `d-funding` (13), `d-contracting` (10), `reprogramming-dd1415`, `sec-8084-nip-reprogramming` | thread `money` runs through here |

## Section 3. The custody allegations (H7, H10, parts of H0; the `custody` thread)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `grusch-allegations` | Grusch's allegations: crash retrieval, biologics, misappropriation, reprisal | saga | `david-grusch` (67), `grusch-icig-complaint`, `grusch-misappropriation-allegation`, `grusch-dopsr-clearance`, `crane-secdef-grusch-reprisal-letter-2025` | the highest-degree node on the board; its page becomes an index grouped by topic |
| `wilson-davis-notes` | The Wilson-Davis notes (2002) | document | `wilson-davis-memo`, `thomas-wilson` | thread `wilson-davis`; start-here flag 11 |
| `kona-blue` | KONA BLUE (2011) | allegation | `kona-blue`, `aaro-kona-blue-release` | start-here flag 10 |
| `immaculate-constellation` | Immaculate Constellation (2024) | allegation | `immaculate-constellation`, `immaculate-constellation-12-page-report` | start-here flag 9 |
| `lazar-s4` | Bob Lazar, S-4 and Element 115 | saga | `bob-lazar`, `s-4-papoose-lake`, `lazar-tape-1991`, `klas-lazar-broadcasts-1989`, `corbell-lazar-2018` | canon pass 1, built |
| `area-51-ranges` | Area 51 and the Nevada ranges | institution | `l-groom-lake`, `l-nevada-test-site`, `bechtel-nevada`, `groom-lake-presidential-determination` | |
| `arv-tr3b` | The ARV / Flux Liner and TR-3B claims | allegation | `mark-mccandlish`, `arv-fluxliner`, `tr-3b`, `edgar-fouche` | canon pass 2, built |
| `skunk-works` | Lockheed and the Skunk Works in the custody record | institution | `lockheed-martin` (31), `lockheed-skunk-works` | GAO accession 130581 (the Burbank document-control review) sits here |
| `battelle-nitinol` | Battelle, Wright-Patterson and the nitinol lineage | allegation | `battelle`, `gerb-battelle-investigation` | carries the NOL record beside the Battelle allegation (do-not-undo) |
| `named-contractors` | Other contractors named in custody claims | allegation | `northrop-grumman`, `saic`, `raytheon`, `bdm-international`, `general-dynamics`, `eg-and-g` if present | canon 11 extends it; the board's exclusions (no BDM-to-Northrop edge) stay |
| `ffrdc-probes` | FFRDCs and the 2026 contractor probes | allegation | `mitre-corporation` (26), `burlison-mitre-letter-2026`, `d-ffrdc`, `ffrdc-mechanism`, `rand-corporation`, `aerospace-corporation`, `mit-lincoln-laboratory` | |
| `corso-day-after` | Philip Corso's account | saga | `philip-corso` | thin; canon 13 |

## Section 4. Official study programmes (H1, H9, H15, H16)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `aawsap-baass` | AAWSAP and BAASS, 2007-2012 | programme | `aawsap` (59), `baass`, `aawsap-contract-hhm402-08-c-0072`, `james-lacatski`, `robert-bigelow` | start-here flag 1; the `lineage` thread starts here |
| `dirds` | The 38 Defense Intelligence Reference Documents | document | `dird-series` (41) plus the 38 `dird-*` | provincial hub: 93% of its neighbours are inside |
| `skinwalker-nids` | Skinwalker Ranch and NIDS | institution | `l-skinwalker`, `nids`, `skinwalkers-at-the-pentagon` | |
| `aatip-elizondo` | AATIP and Luis Elizondo | saga | `aatip`, `luis-elizondo` (38), `elizondo-resignation-letter-1`, `elizondo-dodig-complaint-2021` | |
| `stargate` | STAR GATE and remote viewing | programme | `stargate-program`, `sri-international`, `center-lane`, `inscom` | |
| `uaptf-odni-2021` | The UAP Task Force and the 2021 ODNI assessment | programme | `uap-task-force`, `odni-preliminary-assessment-2021`, `navy-flir-gimbal-gofast-videos` | |
| `aaro` | AARO, 2022 to now | programme | `aaro`, `sean-kirkpatrick`, `jon-kosloski`, AARO annual reports | connector hub: its page groups neighbours by topic |
| `aaro-historical-record` | AARO's historical record reports and their critics | document | `aaro-historical-record-vol1`, AARO Vol II | start-here flag 4; sits on 7 of 8 shortest test paths, so it must be a topic, not a shortcut |
| `pursue-2026` | PURSUE and the 2026 releases | programme | `pursue-releases` (40), `pursue-release-01` to `05`, `trump-uap-release-directive-2026` | |
| `ttsa` | To The Stars Academy and the Army CRADA | institution | `ttsa`, `ttsa-army-crada`, `adam-research-project` | community H15, stability 1.00 |
| `incursions-2023-26` | Drone incursions over bases, 2023-2026 | incident | `langley-2023-incursions`, `nj-drone-incursions-2024`, `norad-northcom` | |
| `nasa-uap-study` | NASA's UAP independent study, 2022-23 | programme | `nasa-uap-ist`, `nasa` | three `nasa-uapist*` nodes are a duplicate candidate |

## Section 5. Encounters and witnesses (H0, H8, H10; canon 4, 5; the nuclear register)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `nimitz-2004` | USS Nimitz, November 2004 | incident | `nimitz-2004` (20), `david-fravor`, `alex-dietrich`, `flir1-video` | |
| `roosevelt-2014-15` | USS Theodore Roosevelt, 2014-15 | incident | `roosevelt-2014-2015`, `ryan-graves`, `gimbal-video`, `gofast-video` | |
| `nuclear-sites` | UFOs over nuclear weapons sites | incident | `malmstrom-echo-flight-1967`, `sac-overflights-1975`, `robert-salas`, `robert-hastings` | the 47-witness register on branch `nuclear-2026-09-19` lands here |
| `disclosure-project-2001` | The Disclosure Project, 2001 | movement | `disclosure-project`, `disclosure-project-briefing-2001`, `steven-greer`, `clifford-stone` | canon pass 4, built; the single-interviewer provenance is part of the topic |
| `officials-on-record` | Astronauts, officials and ministers on the record | saga | **(gap)**: Mitchell, Cooper, Hellyer | canon cluster 5; dropped when the nuclear pass took the number 5 |
| `aviation-cases` | Civil aviation encounters (JAL 1628 and others) | incident | `jal-1628-1986`, `john-callahan` | canon 14 extends it |
| `congressional-witnesses` | Who has testified to Congress, and what the record corroborates | saga | `michael-herrera`, `jason-sands` (isolated, degree 0), the 2023 to 2025 hearing witnesses | Stewart's 18 September scope ruling; `jason-sands` must stop being an island |

## Section 6. Congress and the disclosure fight (H0, H3, H5)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `oversight-before-2017` | Congress before 2017: 1966, the Church Committee, the 1994 GAO request | hearing | `hearing-1966-04-05`, `church-committee`, `steven-schiff` | canon 10 (Goldwater, LeMay) extends it |
| `nyt-2017` | The December 2017 story | movement | `nyt-2017-12-16`, `leslie-kean`, `ralph-blumenthal` | |
| `hearing-2023` | The July 2023 House hearing | hearing | `hearing-2023-07-26` (20), `nancy-mace`, `tim-burchett` if present | |
| `uapda` | The UAP Disclosure Act and what survived it | hearing | `uapda-2023` (26), `uapda-fy2027-house-adopted`, `uapda-2024-samdt-2610`, `uapda-sec-9010-eminent-domain` | start-here flag 12 |
| `uap-statutes` | UAP law in the NDAAs and IAAs, 2021-2026 | mechanism | `ndaa-fy2022-sec-1683`, `ndaa-fy2023-sec-6802`, `ndaa-fy2024-1687`, `iaa-fy2024-sec-1102`, `ndaa26-uap-provisions` | several twin nodes here are duplicate candidates |
| `records-collection` | The National Archives UAP records collection (RG 615) | institution | `nara-uap-collection`, `nara-rg615`, `odni-memo-es-2026-00818` | five nodes may be one thing: first entity-resolution case |
| `hearing-2024` | The November 2024 House hearing | hearing | `hearing-2024-11-13` (16) | |
| `task-force-2025` | The House Task Force on declassification and the September 2025 hearing | hearing | `hearing-2025-09-09` (23), `anna-paulina-luna` (26), `task-force-declassification-federal-secrets` | three task-force nodes are a duplicate candidate |
| `house-push-2026` | The 2026 House push | hearing | `eric-burlison` (28), Capitol events of June 2026, `hr-5060` | |
| `whistleblower-channels` | Whistleblower channels, protections and reprisal | mechanism | `grusch-icig-complaint`, `icig`, `icig-briefing-2024-01-12`, `hr-5060` | |

## Section 7. Science, technology and patents (H11, H10, patents)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `academic-science` | Academic UAP science: Sol, Galileo, SCU, UAPx | movement | `sol-foundation`, `galileo-project`, `garry-nolan` | community H11, stability 0.88 |
| `navy-patents` | The Navy patents and their prosecution | document | `salvatore-pais`, `pais-patent-imrd`, `pais-patent-hfgw`, `pais-patent-emfg` | the Patents pages already carry the file wrapper; no Pais edges to AATIP or any DIRD (do-not-undo) |
| `gravity-research-1950s` | 1950s gravity research: the Talbert series, the Institute of Field Physics, Townsend Brown | programme | `talbert-gravity-series-1955`, `institute-of-field-physics`, `thomas-townsend-brown` | canon 15 extends it |
| `propulsion-claims` | Propulsion and exotic-physics claims, and what the documents actually say | allegation | `propulsion-2026-09-19` build, `d-prop`, `d-exotic` | the pass found each document "says less than is claimed for it" |
| `specimens` | Physical material and specimen analyses | allegation | `oak-ridge-national-laboratory`, `ornl-metallic-specimen-report`, `aaro-metallic-specimen-analysis`, `d-materials` | twin specimen nodes are a duplicate candidate |
| `five-observables` | The five observables | mechanism | `five-observables` | an explainer; content already in `research/observables-view.json` |
| `biology-medical` | Biologics and medical effects | allegation | `d-bio`, `d-medical` | thin; merge if under 6 |

## Section 8. Disinformation, fabrication and the case against (H14, parts of H9; the `denials` thread)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `kirtland-1980` | Kirtland 1980: Bennewitz, Doty and Project Beta | saga | `paul-bennewitz`, `richard-doty`, `bennewitz-project-beta-1981` | community H14, stability 0.85 |
| `dulce` | Dulce Base: an allegation and its origins | allegation | `dulce-base`, `thomas-castello` (fabricated), `tal-levesque` | canon pass 3, built |
| `perception-management` | Perception management: YANKEE BLUE and disinformation practice | mechanism | `yankee-blue`, `d-psyop`, `d-disinformation` | |
| `denial-ledger` | What the government denies, and how | mechanism | `d-denial`, `d-coverup` | the `denials` thread; the 219 denial edges |
| `official-explanations` | Official explanations: Mogul, balloons, misidentification | document | `project-mogul`, the USAF Roswell reports, AARO resolutions | the case against, in one place |
| `sceptics` | Sceptics and debunkers | movement | `donald-h-menzel`, `philip-j-klass` | canon 7 (Sagan) extends it |

## Section 9. Other nations (H2, stability 0.94)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `france` | France: GEPAN, SEPRA, GEIPAN and COMETA | nation | `geipan`, `gepan`, `sepra`, `cometa`, `doc-cometa-report` | start-here flag 13 |
| `brazil` | Brazil: Operacao Prato, the 1986 night, Varginha | nation | `operacao-prato`, `ev-varginha-1996`, `hospital-regional-varginha` | start-here flag 14 |
| `uk` | Britain: the MoD desk, Rendlesham, Condign | nation | `uk-mod`, `uk-mod-ufo-desk`, `rendlesham-1980`, `doc-condign-report` | |
| `latin-america` | Chile, Peru and the other Latin American offices | nation | `cefaa`, `peru-uap-office` | |
| `canada` | Canada: Project Magnet and Sky Canada | nation | `project-magnet`, `sky-canada-project` | |
| `ussr` | The USSR: SETKA and the Soviet programmes | nation | `setka-program` | |
| `europe-other` | Belgium and the rest of Europe | nation | `belgian-af-f16-intercept-1990` | merge into `uk` or `france` if thin |
| `office-models` | How governments organise UAP offices | mechanism | `intl-uap-office-model`, `d-international` | an explainer |

## Section 10. Media, civilian research and the movement (media-structure; canon 12)

| id | title | kind | anchors | notes |
|---|---|---|---|---|
| `media-substrate` | Podcasts, broadcasters and independent media | movement | `d-media` (12), `jesse-michels`, `george-knapp` (19), `jeremy-corbell`, `newsnation`, `the-debrief` | the three mined podcast corpora are sources here, not subjects |
| `civilian-groups` | Civilian research groups: NICAP, APRO, MUFON, CUFOS, CAUS | movement | `nicap`, `mufon`, `cufos`, `caus`, `donald-keyhoe` | |
| `missing-scientists` | Deaths and disappearances: the scientists probe | saga | `missing-scientists-probe-2026` | the `scientists` thread; overlaps The Vanishing at Amy Eskridge only |
| `documentaries` | The Age of Disclosure and other documentaries | movement | `age-of-disclosure`, `age-of-disclosure-2025` | twin nodes; merge if thin |

---

## What the draft deliberately does not do

- It does not assign all 1,136 nodes. Phase 3 does that with a script (community plus anchor
  neighbourhood plus the `domain` node memberships) and an Opus review of the uncertain cases.
- It does not rank topics. Order within a section is by date; size never encodes importance.
- It does not write summaries. Phase 3 does, citing claim ids only (the checks are in the plan).

## Coverage targets for phase 3

| measure | target |
|---|---|
| nodes in at least one topic | 90% or more (today 15% are in any curated structure) |
| people in at least one topic | 95% or more (today 10 of 338 are on a thread) |
| topics with fewer than 6 members | 0 (merge them, or mark `research-gap`) |
| connector hubs (degree 30+) in 3 or more topics | all of them |
| `domain` nodes migrated to topic records or explainers | all 59 |
