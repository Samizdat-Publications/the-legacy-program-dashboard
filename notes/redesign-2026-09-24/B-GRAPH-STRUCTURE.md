# Structure of the Legacy Program board: a measurement for the redesign

Data: `app/public/data/` as generated 2026-09-19 (source 8785b01c31ba), plus `data/l0-model.json`, `data/the-program.json` for edge notes. All numbers below are MEASURED by the scripts in this folder unless a line is marked INFERRED. Read-only on the repo; stdlib Python only.

Graph model used throughout: nodes = the 1,136 board nodes; edges = the 2,685 hand-written sourced edges in `edges.json`, treated as undirected. "Degree" means distinct neighbours (matches the `deg` field shipped in `index.json` for all 1,136 nodes). Multi-edges (110 node pairs carry 2 or more edges) are summed as weights where weights are used.

## 1. Basics

| Measure | Value |
|---|---|
| Nodes / sourced edges / distinct linked pairs | 1,136 / 2,685 / 2,568 |
| Density | 0.0040 (mean degree 4.52, median 3, max 67) |
| Connected components | 2: one of 1,135 nodes plus 1 isolated node (`jason-sands`) |
| Degree-1 leaves | 216 (19%); degree <= 2: 40% |
| Degree Gini | 0.47; top 1% of nodes hold 10% of edge endpoints, top 10% hold 38% |
| k-core | max core 5 (49 nodes); 237 nodes are only in the 1-core |
| Giant component path length | mean 4.67, diameter 15, radius 8; 3.7% of pairs within 2 hops, 18% within 3, 48% within 4 |

Degree histogram:

| degree | 0-0 | 1-1 | 2-2 | 3-4 | 5-9 | 10-19 | 20-49 | 50-99 | 100+ |
|---|---|---|---|---|---|---|---|---|---|
| nodes | 1 | 216 | 235 | 365 | 217 | 79 | 20 | 3 | 0 |

Degree by node class:

| class | n | mean | median | p90 | max | leaves | share of all edge endpoints |
|---|---|---|---|---|---|---|---|
| person | 338 | 3.8 | 2 | 7 | 67 | 91 (27%) | 25% |
| document | 237 | 4.0 | 4 | 6 | 41 | 27 (11%) | 19% |
| institution | 196 | 6.1 | 4 | 13 | 61 | 32 (16%) | 23% |
| event | 87 | 4.6 | 3 | 8 | 23 | 13 (15%) | 8% |
| program | 82 | 6.4 | 4 | 12 | 59 | 9 (11%) | 10% |
| location | 73 | 3.0 | 2 | 5 | 19 | 33 (45%) | 4% |
| legislation | 64 | 4.3 | 3 | 8 | 26 | 6 (9%) | 5% |
| domain | 59 | 4.7 | 4 | 9 | 13 | 5 (8%) | 5% |

Mean degree by node tier: A 12.7 (median 10, n=169), B 4.3 (median 4, n=398), C 2.3 (median 2, n=569). Tier is partly computed from degree (`tools/regrade.py`), so this is expected, not a finding.

**Reading.** This is not a star-shaped graph: the biggest hub has 67 neighbours (6% of the board), the top 1% of nodes hold under 10% of edge ends, and the median node has 3 links. The whole board is one component. People are the thinnest class (median 2 links, 27% leaves); locations are the most leaf-like (45%).

## 2. Hubs and the hairball effect

### Top 20 hubs by degree

| # | node | class | cluster | tier | on L0 | degree | betweenness (norm.) | dominant edge types |
|---|---|---|---|---|---|---|---|---|
| 1 | `david-grusch` | person | witness | A | no | 67 | 0.168 | witness-chain 28, investigative 11, denial 10 |
| 2 | `aaro` | institution | oversight | A | yes | 61 | 0.116 | institutional 26, denial 11, investigative 9 |
| 3 | `aawsap` | program | legacy | A | yes | 59 | 0.081 | programmatic 43, funding 9, investigative 2 |
| 4 | `dod` | institution | legacy | A | yes | 45 | 0.115 | institutional 21, denial 17, research 2 |
| 5 | `cia` | institution | ic | A | yes | 43 | 0.073 | institutional 24, denial 7, programmatic 7 |
| 6 | `dird-series` | document | other | A | yes | 41 | 0.015 | programmatic 37, investigative 2, funding 1 |
| 7 | `pursue-releases` | program | oversight | A | yes | 40 | 0.057 | programmatic 9, temporal 8, denial 6 |
| 8 | `luis-elizondo` | person | witness | A | no | 38 | 0.055 | witness-chain 13, denial 7, investigative 6 |
| 9 | `dia` | institution | ic | A | yes | 35 | 0.048 | custody 13, institutional 10, denial 5 |
| 10 | `aaro-historical-record-vol1` | document | ic | A | yes | 32 | 0.119 | denial 18, programmatic 5, temporal 5 |
| 11 | `lockheed-martin` | institution | contractor | A | yes | 31 | 0.064 | institutional 10, custody 5, investigative 4 |
| 12 | `waived-sap-notification-group` | institution | oversight | A | yes | 31 | 0.032 | institutional 27, investigative 1, funding 1 |
| 13 | `eric-burlison` | person | oversight | A | no | 28 | 0.038 | investigative 12, legislative 8, witness-chain 4 |
| 14 | `project-blue-book` | program | legacy | A | yes | 27 | 0.032 | programmatic 9, institutional 6, denial 5 |
| 15 | `anna-paulina-luna` | person | oversight | A | no | 26 | 0.021 | legislative 9, investigative 8, institutional 5 |
| 16 | `mitre-corporation` | institution | ffrdc | A | yes | 26 | 0.026 | institutional 19, denial 3, investigative 2 |
| 17 | `uapda-2023` | legislation | oversight | A | yes | 26 | 0.030 | legislative 11, programmatic 8, denial 3 |
| 18 | `usaf` | institution | legacy | A | yes | 25 | 0.031 | institutional 16, programmatic 4, denial 3 |
| 19 | `hearing-2025-09-09` | event | oversight | A | yes | 23 | 0.019 | witness-chain 9, programmatic 6, institutional 5 |
| 20 | `eric-davis` | person | research | A | no | 22 | 0.017 | research 6, institutional 5, witness-chain 4 |

### Reach of the top 10

| hub | within 1 hop | within 2 hops | cumulative top-k, 1 hop | cumulative top-k, 2 hops |
|---|---|---|---|---|
| `david-grusch` | 6.0% | 37.6% | 6.0% | 37.6% |
| `aaro` | 5.5% | 25.5% | 10.5% | 44.2% |
| `aawsap` | 5.3% | 17.9% | 15.4% | 50.9% |
| `dod` | 4.0% | 25.6% | 18.1% | 54.7% |
| `cia` | 3.9% | 15.2% | 21.6% | 60.8% |
| `dird-series` | 3.7% | 11.4% | 22.1% | 61.6% |
| `pursue-releases` | 3.6% | 21.0% | 24.0% | 62.8% |
| `luis-elizondo` | 3.4% | 20.9% | 26.0% | 64.5% |
| `dia` | 3.2% | 17.3% | 26.8% | 65.4% |
| `aaro-historical-record-vol1` | 2.9% | 30.4% | 28.0% | 68.9% |

### Removing hubs

| removed | giant component (share of remaining) | components | isolated after | mean path in giant |
|---|---|---|---|---|
| none | 1,135 (99.9%) | 2 | 1 | 4.67 |
| top 10 by degree | 1,088 (96.6%) | 33 | 26 | 5.49 |
| top 20 by degree | 1,051 (94.2%) | 57 | 48 | 5.95 |
| top 50 by degree | 942 (86.7%) | 116 | 95 | 7.37 |
| top 10 by betweenness | 1,097 (97.4%) | 29 | 27 | 5.48 |
| top 20 by betweenness | 1,062 (95.2%) | 54 | 52 | 5.88 |
| 10 random nodes (mean of 20) | (99.6%) | 4.0 | 2.6 | |
| 20 random nodes (mean of 20) | (99.5%) | 5.6 | 4.2 | |
| 50 random nodes (mean of 20) | (98.8%) | 12.1 | 10.1 | |

Removing the top 10 cuts off 38 nodes (person 16, document 15, institution 5, location 2); the top 20 cut off 65. 47 nodes have ONLY top-20 hubs as neighbours. The top 10 hubs carry 23% of all shortest-path betweenness, the top 20 carry 32%. Pairs touching a top-10 hub: 17%; top-20: 27%.

Shortest paths: in a sample of 400 random node pairs, 67% have EVERY shortest path passing through a top-20 hub.

### Hub roles (participation across the hub-damped communities of section 3)

Participation P = 1 - sum over communities of (share of the hub's neighbours in that community)^2; "home" = share of neighbours in the hub's own community. Connector = P >= 0.6; provincial = the hub's neighbourhood mostly sits inside one topic.

| hub | degree | P | communities among neighbours | home share | role |
|---|---|---|---|---|---|
| `david-grusch` | 67 | 0.80 | 9 | 34% | connector hub |
| `aaro` | 61 | 0.76 | 10 | 43% | connector hub |
| `aawsap` | 59 | 0.31 | 8 | 83% | provincial hub |
| `dod` | 45 | 0.88 | 15 | 24% | connector hub |
| `cia` | 43 | 0.70 | 8 | 51% | connector hub |
| `dird-series` | 41 | 0.14 | 4 | 93% | provincial hub |
| `pursue-releases` | 40 | 0.69 | 8 | 50% | connector hub |
| `luis-elizondo` | 38 | 0.61 | 7 | 61% | connector hub |
| `dia` | 35 | 0.30 | 4 | 83% | provincial hub |
| `aaro-historical-record-vol1` | 32 | 0.82 | 10 | 34% | connector hub |
| `lockheed-martin` | 31 | 0.84 | 11 | 32% | connector hub |
| `waived-sap-notification-group` | 31 | 0.59 | 7 | 61% | provincial hub |
| `eric-burlison` | 28 | 0.63 | 7 | 57% | connector hub |
| `project-blue-book` | 27 | 0.43 | 5 | 74% | provincial hub |
| `anna-paulina-luna` | 26 | 0.71 | 6 | 38% | connector hub |
| `mitre-corporation` | 26 | 0.50 | 6 | 69% | provincial hub |
| `uapda-2023` | 26 | 0.45 | 6 | 73% | provincial hub |
| `usaf` | 25 | 0.66 | 9 | 56% | connector hub |
| `hearing-2025-09-09` | 23 | 0.62 | 5 | 57% | connector hub |
| `eric-davis` | 22 | 0.44 | 4 | 73% | provincial hub |
| `doe` | 21 | 0.79 | 8 | 38% | connector hub |
| `hearing-2023-07-26` | 20 | 0.49 | 6 | 70% | provincial hub |
| `nimitz-2004` | 20 | 0.27 | 4 | 85% | provincial hub |
| `baass` | 19 | 0.28 | 4 | 84% | provincial hub |

**Hub verdict (MEASURED, then INFERRED).** The graph does not fall apart without its hubs: removing the top 10 detaches 38 nodes (3.4%) and the rest stays one component with the mean path rising from 4.67 to 5.49. So hubs are shortcuts, not the skeleton. But they own the shortcuts: two thirds of random pairs can only be joined through a top-20 hub. The hubs split into two kinds. Provincial hubs (AAWSAP 83% home, DIRD series 93%, DIA 83%, Blue Book 74%, UAPDA 73%, Nimitz 85%, BAASS 84%) have neighbourhoods that ARE a topic, so opening them shows meaning. Connector hubs (DoD: neighbours in 15 communities, only 24% home; AARO Vol I 34%; Grusch 34%; Lockheed Martin 32%; AARO 43%; DOE 38%; House Oversight 39%) have neighbourhoods that are lists of unrelated stories joined by generic institutional or denial edges. INFERRED: the "sea of nodes" feeling comes from connector hubs rendered as undifferentiated fans, and from the modern era (section 5), not from a few mega-hubs.

## 3. Communities

Method: weighted Louvain (own implementation, resolution 1), 30 random seeds per weighting, then consensus clustering (co-association matrix of the 30 runs, pairs co-clustered in >= 50% of runs kept, Louvain re-run until all 30 re-runs agree; converged in 2 rounds for every weighting). Three weightings:

- **all**: every sourced edge weight 1.
- **hub-damped**: each edge weight 1/sqrt(max(1, k_a/10) x max(1, k_b/10)), k = degree; edges between ordinary nodes keep weight 1, an edge into a degree-60 hub gets about 0.4, hub-to-hub about 0.15. This is the "generic hub edges down-weighted" run.
- **type-damped** (sensitivity check): witness-chain, behavioral and temporal edges at 0.3.

| weighting | best raw Q | mean Q (sd) | communities per run | NMI between runs mean (min) | consensus Q | consensus communities |
|---|---|---|---|---|---|---|
| all | 0.669 | 0.666 (0.002) | 17.2 [15-19] | 0.761 (0.681) | 0.664 | 16 |
| hubdamp | 0.712 | 0.706 (0.002) | 18.8 [16-21] | 0.786 (0.690) | 0.705 | 18 |
| typedamp | 0.686 | 0.682 (0.002) | 18.6 [17-21] | 0.799 (0.718) | 0.684 | 17 |

Null model: degree-preserving rewiring of the same graph (8 rewirings, best of 5 Louvain runs each) gives Q = 0.476 (max 0.480) against 0.668 on the real simple graph. The community structure is real, not an artefact of sparsity.

Agreement between weightings (consensus partitions): all vs hub-damped NMI 0.761; all vs type-damped 0.805; hub-damped vs type-damped 0.688. 

Robustness of each hub-damped community under the other two weightings (best-match Jaccard, and containment = share of the community found inside its best match):

| community | size | Jaccard vs all-edges | containment in all-edges | Jaccard vs type-damped | containment in type-damped |
|---|---|---|---|---|---|
| H0 Navy encounters, the 2017 story and the whistleblower hearings | 146 | 0.34 | 0.38 | 0.32 | 0.36 |
| H1 AAWSAP / AATIP / BAASS lineage and the DIRDs | 133 | 0.93 | 0.93 | 0.86 | 0.88 |
| H2 Other nations' programmes | 88 | 0.94 | 0.94 | 0.88 | 0.89 |
| H3 2025-2026 House push and the FFRDC / contractor probes | 86 | 0.39 | 0.57 | 0.50 | 0.81 |
| H4 Air Force and CIA handling, 1947-1969 | 83 | 0.62 | 0.99 | 0.63 | 0.99 |
| H5 UAP legislation and the records trail | 74 | 0.66 | 0.66 | 0.64 | 0.64 |
| H6 SAP law and the congressional reporting architecture | 70 | 0.57 | 0.94 | 0.55 | 0.94 |
| H7 Nevada, Groom Lake and the nuclear-weapons complex | 69 | 0.51 | 0.88 | 0.45 | 0.75 |
| H8 Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles | 69 | 0.83 | 0.93 | 0.41 | 0.48 |
| H9 AARO and the PURSUE releases, 2022-2026 | 62 | 0.34 | 0.92 | 0.44 | 0.74 |
| H10 Anti-gravity, the ARV and the Disclosure Project | 56 | 0.49 | 0.66 | 0.45 | 0.68 |
| H11 Academic UAP science | 52 | 0.88 | 0.88 | 0.85 | 0.88 |
| H12 The money: classified budgets and the unauditable ledger | 44 | 0.39 | 1.00 | 0.37 | 0.98 |
| H13 Cold War secrecy architecture (with editorial domain nodes) | 36 | 0.23 | 0.86 | 0.18 | 0.69 |
| H14 Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12 | 35 | 0.27 | 0.89 | 0.23 | 0.71 |
| H15 TTSA and the Army CRADA | 18 | 0.24 | 1.00 | 0.24 | 1.00 |
| H16 Military airspace incursions and drones, 2023-2026 | 14 | 0.07 | 0.86 | 0.13 | 0.86 |
| H17 Isolated node | 1 | 1.00 | 1.00 | 1.00 | 1.00 |

Three communities are the same under every weighting (Jaccard >= 0.85 both ways): AAWSAP lineage (H1), other nations (H2), academic science (H11). Five more survive intact but nested inside a larger community when hubs are not damped (containment >= 0.85 both ways): Air Force / CIA 1947-1969 (H4), SAP law (H6), the money (H12), TTSA (H15), incursions (H16). The Roswell tradition (H8) is stable against the all-edges run (0.93) but half dissolves when witness-chain edges are damped (0.48), which says it is held together by testimony. What never recurs is the modern whistleblower material (H0: Jaccard <= 0.34 everywhere): Grusch, Elizondo, the Navy encounters, AARO and the House are one dense tangle that Louvain cuts differently each time.

Node-level home stability (hub-damped): 601 of 1,135 linked nodes share their community with >= 80% of its members in the average run; 174 (15%) are floating (< 50%). The floating set is led by exactly the nodes readers open first: `david-grusch`, `hearing-2023-07-26`, `nimitz-2004`, `house-oversight-committee`, `nasa`, `tim-burchett`, `uap-task-force`, `nyt-2017-12-16`, `odni-preliminary-assessment-2021`, `us-navy`.

### 3a. Hub-damped consensus (primary): 18 communities

Stability = mean share of member pairs that land in the same community across the 30 raw runs (1.0 = always together).

| id | proposed label | size | stability | top 8 by internal degree | classes | internal edge types | years (node p10-p90) | years (edge p10-p90) | clusters | L0 home band | threads touching |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H0 | Navy encounters, the 2017 story and the whistleblower hearings | 146 | 0.37 | david-grusch, luis-elizondo, nimitz-2004, hearing-2023-07-26, immaculate-constellation, nasa, hearing-2024-11-13, nyt-2017-12-16 | person 35%, document 23%, institution 15% | investigative 21%, institutional 21%, witness-chain 13% | 1984-2024 (median 2019) | 2004-2024 (median 2021) | witness 26%, oversight 23% | oversight, custody | 5 |
| H1 | AAWSAP / AATIP / BAASS lineage and the DIRDs | 133 | 0.91 | aawsap, dird-series, dia, eric-davis, baass, harry-reid, earthtech-international, george-knapp | document 38%, person 31%, institution 12% | programmatic 32%, institutional 19%, research 18% | 1974-2021 (median 2009) | 1978-2023 (median 2008) | research 29%, other 29% | reverse-engineering, funding | 4 |
| H2 | Other nations' programmes | 88 | 0.94 | rendlesham-1980, setka-program, geipan, cometa, fab, cefaa, doc-condign-report, operacao-prato | person 27%, institution 25%, location 14% | institutional 25%, geographic 13%, custody 12% | 1950-2014 (median 1992) | 1976-2022 (median 1990) | research 26%, oversight 20% | research, custody | 0 |
| H3 | 2025-2026 House push and the FFRDC / contractor probes | 86 | 0.47 | mitre-corporation, eric-burlison, hearing-2025-09-09, tim-burchett, uap-gerb, rand-corporation, house-oversight-committee, d-ffrdc | person 34%, institution 14%, document 14% | institutional 31%, investigative 22%, legislative 12% | 1947-2026 (median 2024) | 1960-2026 (median 2025) | oversight 43%, ffrdc 17% | custody, oversight | 3 |
| H4 | Air Force and CIA handling, 1947-1969 | 83 | 0.89 | cia, project-blue-book, usaf, l-wright-patterson, robertson-panel, condon-committee, battelle, mkultra | person 34%, document 18%, institution 18% | institutional 39%, programmatic 16%, denial 13% | 1947-1992 (median 1955) | 1948-1980 (median 1955) | ic 33%, legacy 31% | custody, retrieval | 1 |
| H5 | UAP legislation and the records trail | 74 | 0.79 | uapda-2023, ndaa-fy2024, odni, samdt-797, ndaa-fy2026, ndaa-fy2022-sec-1683, d-legislation, iaa-fy2024-sec-1102 | legislation 28%, institution 26%, person 24% | legislative 43%, institutional 24%, denial 12% | 1961-2026 (median 2023) | 2000-2026 (median 2023) | oversight 58%, ic 24% | custody, funding | 1 |
| H6 | SAP law and the congressional reporting architecture | 70 | 0.79 | waived-sap-notification-group, dod, dod-sapco, usc-10-119, carve-out, oversight-congress, waived-usap-mechanism, us-house | institution 29%, legislation 21%, person 20% | institutional 41%, programmatic 22%, legislative 21% | 1987-2023 (median 2009) | 1987-2024 (median 2013) | oversight 56%, legacy 26% | funding, oversight | 3 |
| H7 | Nevada, Groom Lake and the nuclear-weapons complex | 69 | 0.71 | l-groom-lake, s-4-papoose-lake, bob-lazar, doe, atomic-energy-commission, tr-3b, edgar-fouche, lockheed-skunk-works | person 29%, institution 22%, location 17% | institutional 30%, geographic 13%, research 10% | 1945-2014 (median 1958) | 1949-2014 (median 1982) | legacy 22%, witness 16% | custody, reverse-engineering | 2 |
| H8 | Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles | 69 | 0.78 | roswell-1947, jesse-marcel, malmstrom-echo-flight-1967, roswell-report-case-closed, stringfield-status-reports, william-l-moore, aztec-1948, kevin-randle | person 41%, document 22%, event 17% | research 22%, witness-chain 16%, institutional 13% | 1947-2022 (median 1990) | 1947-2002 (median 1987) | research 30%, witness 26% | custody, retrieval | 0 |
| H9 | AARO and the PURSUE releases, 2022-2026 | 62 | 0.87 | aaro, pursue-releases, aaro-historical-record-vol1, anna-paulina-luna, aaro-fy2025-annual-report, jon-kosloski, sean-kirkpatrick, john-greenewald | document 42%, person 24%, institution 11% | institutional 30%, programmatic 16%, investigative 14% | 2021-2026 (median 2024) | 2023-2026 (median 2025) | oversight 45%, ic 27% | custody, oversight | 5 |
| H10 | Anti-gravity, the ARV and the Disclosure Project | 56 | 0.57 | mark-mccandlish, disclosure-project-briefing-2001, institute-of-field-physics, steven-greer, disclosure-project, national-press-club-2001, talbert-gravity-series-1955, arv-fluxliner | person 30%, domain 21%, institution 20% | institutional 26%, research 19%, witness-chain 18% | 1947-2017 (median 1970) | 1955-2023 (median 2000) | witness 23%, research 21% | custody, funding | 1 |
| H11 | Academic UAP science | 52 | 0.88 | uap-science-advisory-council, sol-foundation, galileo-project, garry-nolan, paper-nolan-vallee-2022, university-at-albany, d-custody, avi-loeb | person 35%, institution 17%, document 15% | institutional 40%, investigative 24%, research 14% | 1947-2026 (median 2022) | 2005-2026 (median 2023) | research 75%, legacy 8% | oversight, research | 0 |
| H12 | The money: classified budgets and the unauditable ledger | 44 | 0.76 | dod-agencywide-audit, classified-annex, d-funding, nip, d-contracting, fas, sffas-56, classified-schedule-authorizations | document 25%, person 20%, institution 18% | institutional 27%, funding 20%, legislative 12% | 1947-2026 (median 2000) | 1989-2026 (median 2017) | oversight 43%, research 18% | funding, reverse-engineering | 1 |
| H13 | Cold War secrecy architecture (with editorial domain nodes) | 36 | 0.69 | d-oversight, d-sap, national-security-council, d-secrecy, gao-nsiad-88-152, nsc-5412, gao-130581, d-witness | domain 36%, legislation 17%, institution 14% | institutional 31%, legislative 20%, programmatic 18% | 1947-1986 (median 1962) | 1953-2008 (median 1972) | oversight 36%, ic 31% | oversight, retrieval | 1 |
| H14 | Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12 | 35 | 0.85 | dulce-base, paul-bennewitz, richard-doty, l-kirtland, kirtland-manzano-1980, sandia, afosi, afosi-kirtland-file | person 40%, document 31%, institution 11% | institutional 19%, witness-chain 19%, investigative 17% | 1953-2021 (median 1983) | 1961-2021 (median 1980) | media 23%, witness 20% | oversight, custody | 0 |
| H15 | TTSA and the Army CRADA | 18 | 1.00 | ttsa, ttsa-army-crada, adam-research-project, l-detroit-arsenal, joseph-cannon, aaro-metallic-specimen-analysis, elizondo-resignation-letter-1, ccdc-gvsc | person 33%, document 22%, institution 17% | institutional 46%, programmatic 12%, custody 12% | 1985-2019 (median 2017) | 2017-2019 (median 2019) | contractor 44%, ic 22% | reverse-engineering, oversight | 0 |
| H16 | Military airspace incursions and drones, 2023-2026 | 14 | 0.89 | langley-2023-incursions, norad-northcom, barksdale-2026-incursions, gregory-guillot, jiatf-401, defense-support-program, nj-drone-incursions-2024, shootdowns-feb-2023 | event 29%, location 21%, document 14% | institutional 53%, investigative 20%, research 7% | 1967-2026 (median 2023) | 2013-2026 (median 2023) | oversight 36%, witness 29% | oversight, custody | 0 |
| H17 | Isolated node | 1 | 1.00 | jason-sands | person 100% |  | n/a | n/a | witness 100% |  | 0 |

Longer descriptions of the hub-damped communities:

- **H0 Navy encounters, the 2017 story and the whistleblower hearings**: Nimitz and Roosevelt, NYT 2017, Elizondo, Grusch, UAPTF, ODNI 2021, Immaculate Constellation, the 2023 and 2024 hearings.
- **H1 AAWSAP / AATIP / BAASS lineage and the DIRDs**: DIA contract, Reid, Bigelow, NIDS, EarthTech, Skinwalker, Stargate, Kona Blue, Wilson-Davis notes.
- **H2 Other nations' programmes**: UK MoD, Condign and Rendlesham; France GEIPAN and COMETA; Brazil FAB and Prato; USSR SETKA; Chile CEFAA; Canada.
- **H3 2025-2026 House push and the FFRDC / contractor probes**: Burlison, Burchett, the September 2025 hearing, MITRE, RAND, Northrop/TRW, UAP Gerb, Manhattan Project 2.
- **H4 Air Force and CIA handling, 1947-1969**: Sign, Blue Book, ATIC, Robertson Panel, Condon, Battelle, MKULTRA, the Twining and Schulgen memos.
- **H5 UAP legislation and the records trail**: UAPDA 2023, NDAAs, IAAs, Senate sponsors; ODNI, NARA RG 615, NSA and NRO, CAUS v. NSA.
- **H6 SAP law and the congressional reporting architecture**: waived / unacknowledged SAPs, SAPCO, 10 USC 119, DoDD 5205.07 series, carve-outs, the Gang of Eight.
- **H7 Nevada, Groom Lake and the nuclear-weapons complex**: S-4 and Lazar, TR-3B and Fouche, AEC / DOE labs, EG&G, Skunk Works at Groom.
- **H8 Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles**: Marcel, Stringfield, Friedman, Randle, GAO 1995, Mogul, Malmstrom and Minot, Varginha.
- **H9 AARO and the PURSUE releases, 2022-2026**: AARO directors and reports, the Historical Record, the 2026 release directives.
- **H10 Anti-gravity, the ARV and the Disclosure Project**: McCandlish, Greer, NPC 2001, 1950s gravity research, Norton 1988, Podesta; many editorial domain nodes.
- **H11 Academic UAP science**: Sol Foundation, Galileo Project, Nolan, Knuth, UAPx, Villarroel, SCU.
- **H12 The money: classified budgets and the unauditable ledger**: DoD audit, classified annex, NIP / MIP, SFFAS 56, Skidmore-Fitts, IR&D.
- **H13 Cold War secrecy architecture (with editorial domain nodes)**: NSC, NSC 5412, National Security Act 1947, classification EOs, GAO 88-152; 13 domain nodes.
- **H14 Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12**: the AFOSI disinformation affair and its afterlife.
- **H15 TTSA and the Army CRADA**: the 2017-2019 materials agreement, ADAM project, Detroit Arsenal.
- **H16 Military airspace incursions and drones, 2023-2026**: Langley, the February 2023 shootdowns, New Jersey 2024, Barksdale 2026.
- **H17 Isolated node**: jason-sands, no edges.

### 3b. All-edges consensus: 16 communities

| id | proposed label | size | stability | top 8 by internal degree | classes | internal edge types | years (node p10-p90) | years (edge p10-p90) | clusters | L0 home band | threads touching |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | AARO, PURSUE and the 2023-2026 Congress | 164 | 0.40 | aaro, pursue-releases, anna-paulina-luna, hearing-2025-09-09, eric-burlison, aaro-historical-record-vol1, nasa, aaro-fy2025-annual-report | document 27%, person 27%, event 15% | institutional 25%, investigative 14%, programmatic 13% | 1980-2026 (median 2024) | 2017-2026 (median 2025) | oversight 46%, research 15% | custody, oversight | 6 |
| A1 | Air Force and CIA handling, 1947-1969 (with NSC and 25 domain nodes) | 132 | 0.67 | cia, project-blue-book, usaf, l-wright-patterson, robertson-panel, condon-committee, battelle, mkultra | person 27%, domain 19%, institution 17% | institutional 37%, programmatic 18%, denial 9% | 1947-1992 (median 1957) | 1948-1997 (median 1956) | ic 32%, legacy 23% | retrieval, custody | 1 |
| A2 | AAWSAP / AATIP / BAASS lineage and the DIRDs | 125 | 0.98 | aawsap, dird-series, dia, eric-davis, baass, harry-reid, earthtech-international, nids | document 39%, person 30%, institution 12% | programmatic 33%, institutional 18%, research 18% | 1974-2018 (median 2008) | 1980-2021 (median 2008) | other 30%, research 28% | reverse-engineering, funding | 4 |
| A3 | SAP law and the money | 112 | 0.56 | waived-sap-notification-group, dod, dod-sapco, usc-10-119, d-funding, oversight-congress, waived-usap-mechanism, carve-out | institution 23%, person 21%, document 20% | institutional 37%, legislative 19%, programmatic 17% | 1952-2023 (median 2007) | 1987-2025 (median 2015) | oversight 51%, legacy 18% | funding, oversight | 3 |
| A4 | Nevada, New Mexico and the nuclear-weapons complex | 111 | 0.51 | doe, s-4-papoose-lake, dulce-base, bob-lazar, l-groom-lake, paul-bennewitz, richard-doty, atomic-energy-commission | person 29%, institution 18%, document 18% | institutional 24%, witness-chain 12%, geographic 11% | 1946-2017 (median 1967) | 1949-2016 (median 1982) | legacy 23%, witness 18% | reverse-engineering, custody | 1 |
| A5 | Other nations' programmes | 83 | 0.92 | rendlesham-1980, setka-program, geipan, cometa, fab, doc-condign-report, cefaa, operacao-prato | person 29%, institution 23%, event 13% | institutional 26%, geographic 13%, custody 12% | 1952-2013 (median 1992) | 1976-2022 (median 1990) | research 27%, oversight 22% | research, custody | 0 |
| A6 | Elizondo, TTSA and the 2017 story to Immaculate Constellation | 76 | 0.73 | luis-elizondo, immaculate-constellation, ttsa, hearing-2024-11-13, nyt-2017-12-16, ttsa-army-crada, aatip, immaculate-constellation-12-page-report | person 38%, document 25%, institution 17% | investigative 26%, institutional 24%, witness-chain 11% | 1994-2024 (median 2019) | 2017-2024 (median 2019) | media 25%, oversight 18% | oversight, reverse-engineering | 2 |
| A7 | Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles | 72 | 0.76 | roswell-1947, jesse-marcel, malmstrom-echo-flight-1967, stringfield-status-reports, william-l-moore, aztec-1948, kevin-randle, roswell-report-case-closed | person 39%, document 21%, event 19% | research 20%, investigative 14%, witness-chain 12% | 1947-2013 (median 1984) | 1947-1999 (median 1984) | research 31%, witness 29% | retrieval, custody | 0 |
| A8 | Lockheed, Skunk Works, the ARV and the Disclosure Project | 56 | 0.72 | lockheed-martin, mark-mccandlish, disclosure-project-briefing-2001, institute-of-field-physics, lockheed-skunk-works, steven-greer, arv-fluxliner, disclosure-project | person 36%, institution 21%, document 14% | institutional 29%, witness-chain 19%, research 18% | 1954-2023 (median 1990) | 1957-2023 (median 2000) | witness 23%, research 20% | reverse-engineering, custody | 3 |
| A9 | Navy encounters to the 2023 Grusch hearing | 55 | 0.74 | david-grusch, nimitz-2004, hearing-2023-07-26, uap-task-force, odni-preliminary-assessment-2021, roosevelt-2014-2015, ryan-graves, us-navy | person 38%, institution 20%, document 16% | institutional 32%, witness-chain 20%, programmatic 10% | 2003-2023 (median 2021) | 2004-2023 (median 2021) | witness 40%, oversight 24% | custody, oversight | 3 |
| A10 | UAP legislation 2021-2026 | 49 | 0.88 | uapda-2023, ndaa-fy2024, samdt-797, ndaa-fy2026, ndaa-fy2022-sec-1683, d-legislation, iaa-fy2024-sec-1102, d-legislative | legislation 43%, person 24%, institution 14% | legislative 51%, institutional 16%, programmatic 12% | 1975-2026 (median 2023) | 2021-2025 (median 2023) | oversight 71%, ic 16% | custody, funding | 1 |
| A11 | Academic UAP science | 46 | 0.99 | uap-science-advisory-council, sol-foundation, galileo-project, garry-nolan, paper-nolan-vallee-2022, university-at-albany, avi-loeb, kevin-knuth | person 39%, institution 20%, document 15% | institutional 44%, investigative 26%, research 14% | 2008-2026 (median 2023) | 2019-2026 (median 2024) | research 83%, ic 7% | oversight, research | 0 |
| A12 | FFRDCs and the contractor-custody probes | 35 | 0.89 | mitre-corporation, uap-gerb, d-ffrdc, rand-corporation, gerb-mitre-investigation, manhattan-project-2, northrop-grumman, gerb-northrop-trw-investigation | person 26%, institution 20%, document 17% | institutional 49%, investigative 22%, geographic 7% | 1947-2026 (median 1994) | 1958-2026 (median 2017) | ffrdc 40%, media 17% | custody, funding | 2 |
| A13 | Signals-intelligence agencies and records litigation | 16 | 0.79 | odni, nsa, nro, nara-uap-collection, caus-v-nsa, nga, yeates-affidavit, betty-sapp | institution 44%, document 25%, person 19% | institutional 60%, denial 25%, legislative 5% | 1952-2024 (median 1980) | 1980-2025 (median 2012) | ic 50%, oversight 31% | disclosure, funding | 0 |
| A14 | Age of Disclosure documentary | 3 | 1.00 | age-of-disclosure, gerb-hidden-wing, dan-farah | document 67%, person 33% | institutional 50%, investigative 50% | 2025-2026 (median 2025) | 2025-2026 (median 2025) | media 67%, research 33% | reverse-engineering, retrieval | 0 |
| A15 | Isolated node | 1 | 1.00 | jason-sands | person 100% |  | n/a | n/a | witness 100% |  | 0 |

### 3c. Two levels exist (resolution sweep)

| weighting and resolution | communities per run | of which >= 10 nodes | NMI between runs | best Q | largest sizes |
|---|---|---|---|---|---|
| all@0.25 | 6.8 | 5.8 | 0.740 | 0.802 | 505, 262, 256, 90, 12, 10, 1 |
| all@0.5 | 10.8 | 9.8 | 0.710 | 0.731 | 280, 206, 151, 151, 140, 88, 48, 41 |
| all@1.0 | 17.2 | 16.0 | 0.766 | 0.669 | 123, 122, 111, 110, 92, 90, 74, 69 |
| all@2.0 | 29.1 | 27.9 | 0.838 | 0.607 | 81, 64, 59, 53, 53, 48, 48, 47 |
| all@3.0 | 41.4 | 39.0 | 0.846 | 0.566 | 63, 58, 45, 40, 40, 39, 38, 36 |
| hubdamp@0.25 | 6.5 | 5.5 | 0.681 | 0.813 | 466, 295, 278, 86, 10, 1 |
| hubdamp@0.5 | 11.4 | 10.2 | 0.716 | 0.762 | 249, 180, 172, 154, 97, 94, 77, 44 |
| hubdamp@1.0 | 19.2 | 18.1 | 0.784 | 0.712 | 163, 125, 94, 88, 85, 83, 73, 72 |
| hubdamp@2.0 | 33.6 | 31.6 | 0.855 | 0.658 | 78, 65, 53, 47, 47, 47, 47, 45 |
| hubdamp@3.0 | 43.6 | 40.4 | 0.880 | 0.625 | 57, 50, 48, 46, 45, 40, 40, 40 |

At resolution 0.25 (hub-damped) the board resolves into four regions plus fragments; they are assemblies of the section 3a topics:

| region | size | made of | node eras (0 / 1 / 2 / 3 / nd) |
|---|---|---|---|
| Washington, 2017-2026 | 466 | hub-damped H0, H3, H5, H6, H9, H12, H16 | 50 / 54 / 58 / 275 / 29 |
| The Cold War record, 1947-1990 | 295 | H4, H8, H13, H14 and parts of H7 and H10 | 156 / 79 / 20 / 19 / 21 |
| AAWSAP and the science / contractor strand | 278 | H1, H11, H15 and parts of H10 and H7 | 41 / 41 / 65 / 81 / 50 |
| Other nations | 86 | H2 | 14 / 33 / 15 / 5 / 19 |
| Skidmore-Fitts audit fragment | 10 | part of H12 | 2 / 1 / 2 / 5 / 0 |
| Isolated node | 1 |  | 0 / 0 / 0 / 0 / 1 |

The coarse level is less stable than the topic level (NMI between runs 0.68 versus 0.78), so treat the four regions as a navigation convenience, not a finding of the same strength.

### 3d. Communities against the existing organising schemes

NMI (0 = unrelated, 1 = identical). "Null" = mean NMI after shuffling the scheme's labels 30 times, which is the chance level for that many categories.

| scheme compared with the community partition | NMI all-edges (null) | NMI hub-damped (null) | ARI hub-damped |
|---|---|---|---|
| node `cluster` (9 values) | 0.167 (0.023) | 0.165 (0.026) | 0.059 |
| node class (8) | 0.073 (0.021) | 0.080 (0.024) | 0.021 |
| node era (5) | 0.179 (0.013) | 0.163 (0.014) | 0.078 |
| node tier A/B/C | 0.019 (0.008) | 0.025 (0.009) | 0.005 |
| L0 band, the 135 L0 nodes only | 0.275 (0.153) | 0.274 (0.173) | 0.061 |
| L0 band of each node's L0 home (1,109 nodes that have one) | 0.245 (0.018) | 0.236 (0.020) | 0.122 |
| L0 home node itself (nodes with one home) | 0.550 (0.245) | 0.571 (0.271) | 0.133 |
| reference: cluster vs L0 band (L0 nodes) | 0.202 | | |

How scattered each existing `cluster` is across the hub-damped communities (share of the cluster that sits in its single largest community; number of communities it touches):

| cluster | n | largest share | communities touched |
|---|---|---|---|
| oversight | 278 | 15% | 16 |
| research | 206 | 19% | 16 |
| ic | 152 | 18% | 16 |
| legacy | 121 | 21% | 16 |
| witness | 118 | 32% | 14 |
| other | 103 | 37% | 16 |
| media | 69 | 30% | 14 |
| contractor | 58 | 24% | 13 |
| ffrdc | 31 | 48% | 6 |

| L0 home band | n | largest share | communities touched |
|---|---|---|---|
| custody | 280 | 14% | 16 |
| reverse-engineering | 201 | 51% | 12 |
| oversight | 197 | 24% | 15 |
| research | 140 | 42% | 10 |
| funding | 134 | 23% | 11 |
| retrieval | 119 | 23% | 16 |
| disclosure | 38 | 26% | 8 |

Crosstab, hub-damped community x cluster (counts):

| community | contractor | ffrdc | ic | legacy | media | other | oversight | research | witness |
|---|---|---|---|---|---|---|---|---|---|
| H0 | 2 | 0 | 13 | 4 | 21 | 8 | 34 | 26 | 38 |
| H1 | 14 | 1 | 16 | 9 | 6 | 38 | 7 | 39 | 3 |
| H2 | 0 | 0 | 12 | 11 | 2 | 13 | 18 | 23 | 9 |
| H3 | 4 | 15 | 3 | 5 | 7 | 1 | 37 | 6 | 8 |
| H4 | 1 | 4 | 27 | 26 | 5 | 3 | 6 | 11 | 0 |
| H5 | 2 | 0 | 18 | 1 | 1 | 8 | 43 | 1 | 0 |
| H6 | 4 | 0 | 6 | 18 | 0 | 1 | 39 | 2 | 0 |
| H7 | 9 | 9 | 6 | 15 | 4 | 4 | 5 | 6 | 11 |
| H8 | 0 | 0 | 0 | 13 | 2 | 2 | 13 | 21 | 18 |
| H9 | 0 | 1 | 17 | 1 | 3 | 9 | 28 | 2 | 1 |
| H10 | 6 | 0 | 5 | 3 | 7 | 3 | 7 | 12 | 13 |
| H11 | 1 | 0 | 3 | 4 | 1 | 0 | 3 | 39 | 1 |
| H12 | 5 | 0 | 7 | 3 | 1 | 1 | 19 | 8 | 0 |
| H13 | 1 | 0 | 11 | 1 | 0 | 3 | 13 | 4 | 3 |
| H14 | 1 | 1 | 2 | 6 | 8 | 4 | 1 | 5 | 7 |
| H15 | 8 | 0 | 4 | 0 | 1 | 3 | 0 | 1 | 1 |
| H16 | 0 | 0 | 2 | 1 | 0 | 2 | 5 | 0 | 4 |
| H17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

Crosstab, hub-damped community x L0 home band (counts; `none` = not a member of any L0 node's ledger):

| community | retrieval | reverse-engineering | custody | funding | oversight | disclosure | research | none |
|---|---|---|---|---|---|---|---|---|
| H0 | 3 | 16 | 40 | 16 | 47 | 9 | 13 | 2 |
| H1 | 1 | 103 | 4 | 14 | 1 | 0 | 9 | 1 |
| H2 | 8 | 0 | 17 | 1 | 0 | 3 | 59 | 0 |
| H3 | 9 | 10 | 26 | 13 | 23 | 0 | 5 | 0 |
| H4 | 22 | 0 | 26 | 0 | 11 | 2 | 22 | 0 |
| H5 | 8 | 1 | 25 | 16 | 11 | 7 | 6 | 0 |
| H6 | 6 | 2 | 7 | 31 | 23 | 0 | 1 | 0 |
| H7 | 5 | 26 | 32 | 4 | 2 | 0 | 0 | 0 |
| H8 | 27 | 0 | 28 | 0 | 4 | 0 | 0 | 10 |
| H9 | 2 | 0 | 36 | 1 | 14 | 2 | 7 | 0 |
| H10 | 5 | 8 | 15 | 10 | 0 | 10 | 5 | 3 |
| H11 | 1 | 9 | 4 | 0 | 24 | 0 | 13 | 1 |
| H12 | 2 | 5 | 4 | 24 | 3 | 0 | 0 | 6 |
| H13 | 12 | 1 | 2 | 4 | 13 | 2 | 0 | 2 |
| H14 | 4 | 5 | 10 | 0 | 12 | 3 | 0 | 1 |
| H15 | 0 | 15 | 0 | 0 | 3 | 0 | 0 | 0 |
| H16 | 4 | 0 | 4 | 0 | 6 | 0 | 0 | 0 |
| H17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

**Reading (MEASURED).** The graph's own communities are topical and historical (a programme and its people, a country, a decade, a law), and they are nearly independent of the two schemes the app organises by. Community vs `cluster` NMI is 0.16-0.17 (chance 0.02-0.03); under the hub-damped partition every cluster is spread over 6-16 communities with 15-48% in its largest one (the oversight cluster, 278 nodes, touches 16 communities and has only 15% in any one). Community vs L0 band is 0.24 (chance 0.02); each band touches 8-16 communities. `cluster` is a ROLE (witness, media, oversight, contractor) and the L0 band is a FUNCTION (custody, funding, oversight), and both cut across every story. The communities align best with the L0 home node itself (NMI 0.55-0.57 against chance 0.24-0.27), i.e. the L0 ledger already groups nodes somewhat topically, but the L0 grid then scatters those groups by band.

## 4. Edge types

Intra = share of that type's edges that fall inside one community (all-edges consensus / hub-damped consensus). The configuration-model expectation for a random edge is about 0.09; overall observed is 0.76. Hub lift = the type's share among edges touching a top-20 hub divided by its share overall.

| type | edges | share | T2+T3 | T3 | dated | touches top-20 hub | hub lift | intra (all) | intra (hub-damped) |
|---|---|---|---|---|---|---|---|---|---|
| institutional | 720 | 26.8% | 26% | 3% | 82% | 27% | 0.97 | 78% | 76% |
| programmatic | 324 | 12.1% | 26% | 8% | 61% | 45% | 1.62 | 88% | 86% |
| investigative | 302 | 11.2% | 39% | 8% | 87% | 25% | 0.90 | 69% | 71% |
| denial | 219 | 8.2% | 41% | 12% | 95% | 42% | 1.51 | 61% | 63% |
| legislative | 215 | 8.0% | 17% | 6% | 92% | 23% | 0.83 | 73% | 70% |
| witness-chain | 204 | 7.6% | 63% | 9% | 91% | 30% | 1.09 | 70% | 68% |
| research | 198 | 7.4% | 34% | 14% | 62% | 10% | 0.34 | 81% | 81% |
| custody | 162 | 6.0% | 35% | 9% | 80% | 19% | 0.69 | 74% | 70% |
| temporal | 91 | 3.4% | 43% | 27% | 87% | 23% | 0.83 | 71% | 71% |
| geographic | 91 | 3.4% | 38% | 5% | 58% | 8% | 0.28 | 91% | 88% |
| behavioral | 84 | 3.1% | 77% | 31% | 92% | 32% | 1.15 | 73% | 68% |
| funding | 75 | 2.8% | 36% | 9% | 80% | 31% | 1.10 | 83% | 73% |

Edge-type groups used below: structural = custody, funding, programmatic, institutional, legislative, research (1,694 edges, 63%; 73% Tier 1); assertion = witness-chain, behavioral, investigative, denial (809, 30%; 50% Tier 1); context = temporal, geographic (182, 7%; 59% Tier 1).

Which types join the hub-damped communities to each other (top community pairs by number of edges between them):

| community pair | edges between | dominant types |
|---|---|---|
| H0 Navy encounters, the 2017 story and the whistleblower hearings / H9 AARO and the PURSUE releases, 2022-2026 | 56 | denial 18, investigative 7, institutional 6 |
| H0 Navy encounters, the 2017 story and the whistleblower hearings / H3 2025-2026 House push and the FFRDC / contractor probes | 32 | witness-chain 8, institutional 8, investigative 6 |
| H0 Navy encounters, the 2017 story and the whistleblower hearings / H1 AAWSAP / AATIP / BAASS lineage and the DIRDs | 29 | witness-chain 6, programmatic 5, investigative 4 |
| H3 2025-2026 House push and the FFRDC / contractor probes / H9 AARO and the PURSUE releases, 2022-2026 | 28 | legislative 9, institutional 4, temporal 4 |
| H0 Navy encounters, the 2017 story and the whistleblower hearings / H6 SAP law and the congressional reporting architecture | 23 | witness-chain 7, denial 5, institutional 4 |
| H5 UAP legislation and the records trail / H6 SAP law and the congressional reporting architecture | 20 | institutional 10, legislative 6, investigative 1 |
| H5 UAP legislation and the records trail / H9 AARO and the PURSUE releases, 2022-2026 | 18 | legislative 8, institutional 6, programmatic 2 |
| H3 2025-2026 House push and the FFRDC / contractor probes / H5 UAP legislation and the records trail | 16 | legislative 6, investigative 4, institutional 4 |
| H0 Navy encounters, the 2017 story and the whistleblower hearings / H5 UAP legislation and the records trail | 15 | institutional 5, witness-chain 3, legislative 2 |
| H3 2025-2026 House push and the FFRDC / contractor probes / H6 SAP law and the congressional reporting architecture | 15 | institutional 7, denial 5, legislative 2 |

Graph bridges (edges whose removal disconnects something): 237, of which 216 merely attach a leaf; the 21 non-leaf bridges are research 8, institutional 4, investigative 3, programmatic 2, legislative 2, temporal 1, witness-chain 1.

### Candidate backbones

| edge set | edges | nodes covered | Tier A covered | L0 covered | components | giant (share of covered) | mean path | Louvain Q | communities | NMI vs full hub-damped | top hubs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PROGRAM_EDGES (custody, funding, programmatic) | 561 | 477 (42%) | 86% | 76% | 44 | 347 (73%) | 7.39 | 0.849 | 57 | 0.60 | aawsap 52, dird-series 38, dia 19 |
| + institutional | 1281 | 848 (75%) | 96% | 93% | 36 | 744 (88%) | 5.72 | 0.793 | 52 | 0.58 | aawsap 53, dird-series 38, aaro 32 |
| + institutional + legislative | 1496 | 896 (79%) | 97% | 98% | 32 | 799 (89%) | 5.46 | 0.764 | 48 | 0.62 | aawsap 53, aaro 39, dird-series 38 |
| structural 6 (+ research) | 1694 | 975 (86%) | 99% | 100% | 22 | 912 (94%) | 5.73 | 0.758 | 39 | 0.62 | aawsap 54, aaro 42, dird-series 39 |
| structural 6 + denial | 1913 | 1006 (89%) | 99% | 100% | 15 | 967 (96%) | 5.13 | 0.724 | 35 | 0.63 | aawsap 55, aaro 51, dod 42 |
| all minus witness-chain, behavioral, temporal | 2306 | 1099 (97%) | 100% | 100% | 3 | 1095 (100%) | 4.98 | 0.700 | 22 | 0.68 | aaro 59, aawsap 58, dod 44 |
| assertion layer only (witness-chain, behavioral, investigative, denial) | 809 | 599 (53%) | 76% | 80% | 39 | 486 (81%) | 5.30 | 0.749 | 54 | 0.52 | david-grusch 50, luis-elizondo 28, aaro-historical-record-vol1 22 |
| all types | 2685 | 1135 (100%) | 100% | 100% | 1 | 1135 (100%) | 4.71 | 0.669 | 16 | 0.78 | david-grusch 67, aaro 61, aawsap 59 |

### Leave-one-type-out

| type removed | nodes left without any edge | giant | components | mean path | Louvain Q | change in Q |
|---|---|---|---|---|---|---|
| institutional | 131 | 983 | 7 | 5.00 | 0.690 | +0.021 |
| programmatic | 14 | 1106 | 6 | 4.89 | 0.666 | -0.003 |
| investigative | 42 | 1075 | 7 | 4.96 | 0.689 | +0.020 |
| denial | 10 | 1118 | 3 | 5.04 | 0.687 | +0.018 |
| legislative | 30 | 1099 | 3 | 4.74 | 0.679 | +0.010 |
| witness-chain | 16 | 1117 | 2 | 4.88 | 0.683 | +0.014 |
| research | 46 | 1070 | 9 | 4.80 | 0.670 | +0.001 |
| custody | 15 | 1120 | 1 | 4.83 | 0.675 | +0.006 |
| temporal | 7 | 1125 | 2 | 4.76 | 0.677 | +0.008 |
| geographic | 33 | 1102 | 1 | 4.67 | 0.669 | +0.000 |
| behavioral | 5 | 1130 | 1 | 4.77 | 0.673 | +0.004 |
| funding | 5 | 1130 | 1 | 4.78 | 0.672 | +0.003 |

**Backbone verdict.** MEASURED: there is no junk edge type. Every type is strongly within-topic (61-91% intra against about 9% expected), and no single type's removal raises modularity by more than 0.021. What differs is role. The six structural types form a navigable backbone on their own: 63% of edges, 86% of nodes, 99% of Tier A, all 135 L0 nodes, one giant component holding 94% of what they touch (including 133 of the 135 L0 nodes and 166 of the 169 Tier A nodes), mean path 5.7. `PROGRAM_EDGES` alone (custody / funding / programmatic) is too thin to navigate (42% of nodes, 44 components, mean path 7.4); adding `institutional` is the step that makes it a network (+371 nodes). The assertion types are the cross-topic layer: `denial` is clearly the most bridging type under both partitions (61% / 63% intra) while most other types sit at 68-83% and `geographic` (88-91%) and `programmatic` (86-88%) are the most local; `denial` plus `programmatic` are the types over-represented on hubs (lift 1.5-1.6). When a random shortest path steps INTO a top-20 hub it does so on a `denial` edge 27% of the time and on `institutional` 22%. `denial` is what joins AARO to the whistleblower story (18 of the 56 edges between H0 and H9). `witness-chain` is the most claim-like large type (63% Tier 2/3) and is the core of the Grusch and Elizondo fans. `behavioral` (77% T2/T3, 31% T3) and `temporal` (27% T3) are small and the weakest evidentially. INFERRED: a clean default view is the structural backbone; `denial` and the testimony types are better drawn as a deliberate second layer ("who contests what") than mixed into the same hairball, because they are exactly the edges that make every topic touch every other.

## 5. Time

| Measure | Value |
|---|---|
| Edges with their own `dateStart` | 2,164 of 2,685 (81%); precision: day 557, month 148, year 1457 |
| Edges whose two endpoint nodes are both dated | 2,289 (85%) |
| Edges dated either way | 2,416 (90%) |
| Edges whose label or note contains a year | 1,484 |
| Edges with no date signal at all | 80 (3.0%) |
| Dated nodes | 1,016 of 1,136; by class: document 198/237, domain 59/59, event 86/87, institution 171/196, legislation 55/64, location 47/73, person 318/338, program 82/82 |
| Edge date vs its endpoints (both dated) | after both start dates 260, between them 1703, before both 74; median gap from the older endpoint 3 years |
| Edges joining nodes of different eras | 941 (35%); same era 1348; touching an undated node 396 |
| Retrospective edges (edge date in a later era than its older endpoint) | 763 of 2159 dated |
| Nodes with at least one timeline event | 576 |

Caveats found on the way: person nodes carry ONE date (the `date` sort key, e.g. Grusch = 2023-07-26, the hearing), not a life span; the 59 domain nodes carry nominal dates (8 of them exactly 1947-01-01), which puts 39 editorial concept nodes in the pre-1970 era.

Per-era counts:

| era | nodes (node era) | edges (edge date) | timeline events |
|---|---|---|---|
| through 1969 | 263 | 352 | 127 |
| 1970-1999 | 208 | 409 | 197 |
| 2000-2016 | 160 | 331 | 175 |
| 2017-2026 | 385 | 1072 | 560 |
| no date | 120 | 521 | - |

Nodes per era by class:

| era | document | domain | event | institution | legislation | location | person | program |
|---|---|---|---|---|---|---|---|---|
| through 1969 | 23 | 39 | 17 | 70 | 6 | 32 | 54 | 22 |
| 1970-1999 | 43 | 10 | 18 | 47 | 16 | 8 | 38 | 28 |
| 2000-2016 | 45 | 5 | 10 | 23 | 4 | 2 | 60 | 11 |
| 2017-2026 | 87 | 5 | 41 | 31 | 29 | 5 | 166 | 21 |
| no date | 39 | 0 | 1 | 25 | 9 | 26 | 20 | 0 |

### Era slices

Slice A, by EDGE date (an edge belongs to the era of its own date; nodes come in with their edges):

| slice | edges | nodes | components | giant share | mean path | max degree | Louvain Q | communities >= 5 | top hubs | dominant hub-damped topics |
|---|---|---|---|---|---|---|---|---|---|---|
| through 1969 | 352 | 247 | 17 | 83% | 5.39 | 21 | 0.750 | 12 | project-blue-book 21, cia 20, usaf 13, condon-committee 12, robertson-panel 12 | H4 (63), H7 (39), H13 (21), H8 (20) |
| 1970-1999 | 409 | 345 | 27 | 81% | 7.56 | 13 | 0.857 | 15 | s-4-papoose-lake 13, bob-lazar 12, setka-program 10, tr-3b 10, nids 9 | H2 (49), H8 (47), H1 (41), H7 (41) |
| 2000-2016 | 331 | 287 | 24 | 60% | 6.99 | 12 | 0.861 | 16 | baass 12, kona-blue 11, mark-mccandlish 11, nimitz-2004 11, disclosure-project-briefing-2001 10 | H0 (53), H1 (50), H6 (35), H2 (31) |
| 2017-2026 | 1072 | 562 | 12 | 94% | 4.31 | 60 | 0.637 | 17 | david-grusch 60, aaro 47, pursue-releases 39, luis-elizondo 31, aaro-historical-record-vol1 27 | H0 (106), H3 (69), H5 (60), H9 (58) |
| undated edges | 521 | 385 | 18 | 87% | 5.97 | 47 | 0.771 | 13 | aawsap 47, dird-series 34, waived-sap-notification-group 26, dia 22, aaro 14 | H1 (82), H6 (51), H0 (35), H2 (35) |

Slice B, by NODE era (the subgraph induced on nodes of that era):

| slice | era nodes | nodes with an in-era edge | edges | components | giant share | top hubs |
|---|---|---|---|---|---|---|
| through 1969 | 263 | 232 | 359 | 9 | 91% | cia 26, project-blue-book 21, usaf 16, l-wright-patterson 13 |
| 1970-1999 | 208 | 160 | 175 | 17 | 30% | richard-doty 8, dod-sapco 7, paul-bennewitz 7, setka-program 6 |
| 2000-2016 | 160 | 104 | 131 | 11 | 47% | aawsap 13, nimitz-2004 9, baass 8, harry-reid 8 |
| 2017-2026 | 385 | 334 | 683 | 4 | 98% | david-grusch 47, aaro 43, pursue-releases 35, luis-elizondo 27 |
| no date | 120 | 53 | 48 | 9 | 64% | dird-series 33, wayne-state-university 5, dird-anomalous-acute-and-subacute-field-effects 2, dird-cognitive-limits-on-simultaneous-control-of 2 |

Topic x era (hub-damped communities; edges touching the topic, by edge-date era: through 1969 / 1970-1999 / 2000-2016 / 2017-2026 / undated):

| topic | edges by era | nodes by era |
|---|---|---|
| H0 Navy encounters, the 2017 story and the whistleblower hearings | 11 / 14 / 77 / 338 / 54 | 12 / 8 / 33 / 86 / 7 |
| H1 AAWSAP / AATIP / BAASS lineage and the DIRDs | 10 / 62 / 96 / 84 / 190 | 8 / 25 / 49 / 14 / 37 |
| H2 Other nations' programmes | 14 / 63 / 32 / 21 / 41 | 14 / 34 / 15 / 6 / 19 |
| H3 2025-2026 House push and the FFRDC / contractor probes | 32 / 11 / 13 / 209 / 18 | 21 / 5 / 2 / 54 / 4 |
| H4 Air Force and CIA handling, 1947-1969 | 161 / 33 / 6 / 21 / 44 | 65 / 13 / 0 / 3 / 2 |
| H5 UAP legislation and the records trail | 3 / 26 / 11 / 168 / 33 | 8 / 10 / 4 / 44 / 8 |
| H6 SAP law and the congressional reporting architecture | 8 / 34 / 49 / 81 / 87 | 4 / 22 / 19 / 20 / 5 |
| H7 Nevada, Groom Lake and the nuclear-weapons complex | 69 / 71 / 17 / 20 / 17 | 35 / 18 / 3 / 6 / 7 |
| H8 Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles | 27 / 68 / 7 / 9 / 19 | 21 / 27 / 9 / 8 / 4 |
| H9 AARO and the PURSUE releases, 2022-2026 | 2 / 7 / 7 / 247 / 39 | 2 / 1 / 0 / 55 / 4 |
| H10 Anti-gravity, the ARV and the Disclosure Project | 25 / 24 / 37 / 24 / 44 | 24 / 9 / 9 / 6 / 8 |
| H11 Academic UAP science | 8 / 4 / 6 / 87 / 10 | 6 / 1 / 3 / 38 / 4 |
| H12 The money: classified budgets and the unauditable ledger | 7 / 7 / 18 / 38 / 14 | 9 / 11 / 8 / 15 / 1 |
| H13 Cold War secrecy architecture (with editorial domain nodes) | 34 / 23 / 6 / 5 / 10 | 21 / 10 / 2 / 0 / 3 |
| H14 Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12 | 18 / 36 / 10 / 15 / 9 | 9 / 13 / 3 / 5 / 5 |
| H15 TTSA and the Army CRADA | 1 / 1 / 0 / 40 / 1 | 2 / 1 / 0 / 15 / 0 |
| H16 Military airspace incursions and drones, 2023-2026 | 1 / 0 / 5 / 19 / 2 | 2 / 0 / 1 / 10 / 1 |

**Time verdict.** MEASURED: time is almost fully recoverable (97% of edges carry a date signal; 81% carry their own date), and edge dates behave like event dates: of edges with both ends dated, 59% carry the year of the newer endpoint and 33% the year of the older one (median gap from the older endpoint 3 years), and 35% of dated edges are retrospective, e.g. a 2024 AARO report denying a 1947 event. Slicing by EDGE date gives coherent, readable sub-graphs with era-appropriate hubs (Blue Book / CIA / Condon through 1969; S-4, Lazar, SETKA, NIDS 1970-1999; BAASS, Kona Blue, McCandlish, Nimitz 2000-2016): the first two slices are over 80% one component and 2000-2016 is 60%, with a maximum degree of 12-21 and modularity 0.75-0.86. Slicing by NODE era works much worse: the 1970-1999 and 2000-2016 slices shatter (giant component 30% and 47%) because those eras are held together by later documents about them. The hairball is the modern slice: 2017-2026 holds half of all dated edges (1,072 of 2,164), max degree 60, the lowest modularity (0.64) and the shortest paths (4.3). Topics carry strong era signatures: 61% of the edges touching H4 (Air Force / CIA) are dated through 1969, 52% of H8's (Roswell tradition) fall in 1970-1999, while 82% of H9's (AARO), 74% of H3's (House 2025-2026) and 70% of H5's (legislation) are 2017-2026. A topic-by-era grid is well supported. The 521 undated edges are concentrated: 190 touch the AAWSAP topic (mostly AAWSAP-to-DIRD programmatic links) and 87 the SAP-law topic.

## 6. Coverage by existing curation

| structure | nodes | share of 1,136 |
|---|---|---|
| in any of the 8 threads (step nodes plus `via` nodes) | 44 | 3.9% |
| highlights (start-here flags) | 14 | 1.2% |
| map entry paths (6) | 100 | 8.8% |
| on the L0 map | 135 | 11.9% |
| with a dossier | 149 | 13.1% |
| named by a timeline event | 576 | 50.7% |
| with a FOIA request | 42 | 3.7% |
| patents view | 5 | 0.4% |
| direct member of an L0 node's ledger (one click from the map) | 670 | 59.0% |
| routed member (depth 2-4) | 304 | 26.8% |
| union of threads, highlights, entry paths, L0, dossiers (authored) | 170 | 15.0% |
| ... plus timeline, FOIA, patents | 618 | 54.4% |
| ... plus L0 direct membership | 964 | 84.9% |
| in no authored structure (only search, graph browsing or an L0 ledger) | 518 | 45.6% |
| ... and not even a direct L0 ledger member (search or deep browsing only) | 172 | 15.1% |

Threads are small: lineage 6, custody 8, money 7, denials 8, wilson-davis 6, patents 7, scientists 6, oversight 7 nodes; 10 nodes sit in more than one thread. The L0 map holds no person at all (institution 54, document 31, program 26, event 13, legislation 11). Nodes with no authored structure: person 220, institution 95, document 61, location 56, domain 36, legislation 21, program 20, event 9; tiers C 339, B 163, A 16; median degree 2. Strictly search-only by class: person 83, institution 25, domain 24, location 17, document 8, legislation 7, event 5, program 3.

Tier A nodes in a narrative structure (thread, highlight, entry path): 51%; in any authored structure: 62%. Tier A nodes in no authored structure: `kit-green`, `d-funding`, `d-custody`, `sap-taxonomy`, `uap-records-review-board`, `richard-genik`, `sap-annual-report`, `sapoc`, `dodm-5205-07-series`, `jay-stratton`, `classified-programs-line`, `uapda-sec-9010-eminent-domain`, `pl118-31-sec-1687`, `project-azorian`, `odni-capco`, `sap-cover-mechanisms`.

Top-50-degree nodes missing from the narrative structures: `dird-series`, `george-knapp`, `sol-foundation`, `john-greenewald`, `mark-mccandlish`, `sean-kirkpatrick`, `uap-gerb`, `harold-puthoff`, `hearing-2024-11-13`, `s-4-papoose-lake`, `tim-burchett`, `dulce-base`. Missing from L0: `david-grusch`, `luis-elizondo`, `eric-burlison`, `anna-paulina-luna`, `eric-davis`, `george-knapp`, `l-wright-patterson`, `harry-reid`, `john-greenewald`, `mark-mccandlish`, `sean-kirkpatrick`, `uap-gerb`, `harold-puthoff`, `s-4-papoose-lake`, `tim-burchett`, `dulce-base`.

Curation per hub-damped community:

| community | size | thread nodes | threads touching | L0 | highlights | entry paths | dossiers | timeline | no authored structure |
|---|---|---|---|---|---|---|---|---|---|
| H0 Navy encounters, the 2017 story and the whistleblower hearings | 146 | 10 | custody, denials, lineage, oversight, patents | 16 | 1 | 15 | 17 | 82 | 57 (39%) |
| H1 AAWSAP / AATIP / BAASS lineage and the DIRDs | 133 | 7 | custody, denials, lineage, wilson-davis | 15 | 3 | 9 | 17 | 52 | 77 (58%) |
| H2 Other nations' programmes | 88 | 0 | - | 13 | 2 | 13 | 14 | 35 | 48 (55%) |
| H3 2025-2026 House push and the FFRDC / contractor probes | 86 | 7 | denials, oversight, scientists | 10 | 1 | 5 | 12 | 54 | 30 (35%) |
| H4 Air Force and CIA handling, 1947-1969 | 83 | 1 | scientists | 11 | 0 | 9 | 11 | 46 | 34 (41%) |
| H5 UAP legislation and the records trail | 74 | 1 | oversight | 17 | 1 | 8 | 17 | 38 | 32 (43%) |
| H6 SAP law and the congressional reporting architecture | 70 | 5 | custody, denials, money | 13 | 3 | 11 | 13 | 24 | 40 (57%) |
| H7 Nevada, Groom Lake and the nuclear-weapons complex | 69 | 3 | custody, wilson-davis | 7 | 0 | 7 | 7 | 39 | 27 (39%) |
| H8 Roswell and the crash-retrieval research tradition; UFOs and nuclear missiles | 69 | 0 | - | 3 | 0 | 3 | 7 | 36 | 33 (48%) |
| H9 AARO and the PURSUE releases, 2022-2026 | 62 | 4 | denials, lineage, oversight, patents, wilson-davis | 8 | 2 | 7 | 8 | 42 | 19 (31%) |
| H10 Anti-gravity, the ARV and the Disclosure Project | 56 | 2 | scientists | 8 | 0 | 4 | 8 | 29 | 26 (46%) |
| H11 Academic UAP science | 52 | 0 | - | 4 | 0 | 1 | 5 | 21 | 30 (58%) |
| H12 The money: classified budgets and the unauditable ledger | 44 | 3 | money | 2 | 1 | 2 | 3 | 18 | 24 (55%) |
| H13 Cold War secrecy architecture (with editorial domain nodes) | 36 | 1 | custody | 1 | 0 | 0 | 1 | 18 | 17 (47%) |
| H14 Kirtland 1980: Bennewitz, Doty, Dulce and MJ-12 | 35 | 0 | - | 3 | 0 | 3 | 4 | 25 | 9 (26%) |
| H15 TTSA and the Army CRADA | 18 | 0 | - | 3 | 0 | 3 | 3 | 9 | 9 (50%) |
| H16 Military airspace incursions and drones, 2023-2026 | 14 | 0 | - | 1 | 0 | 0 | 2 | 8 | 5 (36%) |
| H17 Isolated node | 1 | 0 | - | 0 | 0 | 0 | 0 | 0 | 1 (100%) |

**Coverage verdict (MEASURED).** Authored narrative reaches few nodes: threads 3.9%, highlights 1.2%, entry paths 8.8%, L0 11.9%; together with dossiers 15.0%. The timeline is the broadest authored structure (51%). Almost half the board (518 nodes, 45.6%) is in no authored structure, and 172 (15.1%) are not even one click from the map. Six topics have no thread at all: other nations (88 nodes), the Roswell / nuclear-missile tradition (69), academic science (52), Kirtland / Bennewitz / Dulce (35), TTSA and the CRADA (18), incursions (14); the Air Force / CIA 1947-1969 topic (83) has one thread node. Thread nodes concentrate in H0 (10), H1 (7), H3 (7), H6 (5) and H9 (4): the modern Washington material, AAWSAP and SAP law, which are also the topics best served by L0, dossiers and entry paths.

## 7. Paths a reader would ask for

For each pair: all shortest paths in the full graph, then the same query with the top-20 hubs removed, with structural edge types only, and a hub-penalised path (entering a node costs 1 + log2(degree)). Full edge labels are in `s9_paths.txt`.

| pair | distance | shortest paths | share through a top-20 hub | shortest-path intermediates | without top-20 hubs | structural types only | hub-penalised |
|---|---|---|---|---|---|---|---|
| Whistleblower to contractor: `david-grusch` to `lockheed-skunk-works` | 3 | 4 | 25% | kona-blue (2), aaro-historical-record-vol1 (1), usc-10-119 (1), boeing (1) | 3 (3) boeing > mark-mccandlish | 3 (1) l-wright-patterson > podesta-delonge-mccasland-email-2016 | boeing > mark-mccandlish |
| Programme to law: `aawsap` to `uapda-2023` | 2 | 1 | 100% | aaro-historical-record-vol1 (1) | 3 (3) harry-reid > chuck-schumer | 3 (8) dird-ultracapacitors-as-energy-and-power-storage > lockheed-martin | aaro-historical-record-vol1 |
| 1947 event to 2023 hearing: `roswell-1947` to `hearing-2023-07-26` | 3 | 2 | 100% | aaro-historical-record-vol1 (2), david-grusch (1), hearing-2024-11-13 (1) | 5 (7) battelle > naval-ordnance-laboratory > us-navy > nimitz-2004 | 4 (1) battelle > l-wright-patterson > david-grusch | aaro-historical-record-vol1 > hearing-2024-11-13 |
| Claimant to the official office: `bob-lazar` to `aaro` | 4 | 22 | 18% | oni (8), the-black-vault (5), john-greenewald (5), s-4-papoose-lake (4) | 4 (18) s-4-papoose-lake > d-custody > nasa-uapist | 4 (8) lanl > doe > nasa | oni > uap-task-force > aaro-establishment-memo-2022 |
| Legacy programme to modern office: `project-blue-book` to `aaro` | 3 | 6 | 67% | aaro-historical-record-vol1 (2), gerb-battelle-investigation (1), sean-kirkpatrick (1), project-moon-dust (1) | 3 (2) gerb-battelle-investigation > sean-kirkpatrick | 4 (6) usaf > manned-orbiting-laboratory > nasa | haines-cia-history > yankee-blue |
| Patents to contractor (extra): `salvatore-pais` to `lockheed-skunk-works` | 4 | 6 | 83% | l-pax-river (4), lockheed-martin (4), harold-puthoff (2), ben-rich (1) | 4 (1) harold-puthoff > stargate-program > l-groom-lake | 4 (3) l-pax-river > lockheed-martin > ben-rich | l-pax-river > lockheed-martin > ben-rich |
| Nuclear witness to the official office (extra): `robert-salas` to `aaro` | 4 | 9 | 100% | prp-nuclear-weapon (8), dod (8), aaro-fy2025-annual-report (1), pursue-releases (1) | 5 (8) malmstrom-echo-flight-1967 > doc-341-smw-history-1967 > john-greenewald > enigma-labs | none (0)  | prp-nuclear-weapon > dod > dodig-2023-109 |
| Wilson-Davis author to the contractor (extra): `eric-davis` to `lockheed-martin` | 3 | 14 | 29% | thomas-townsend-brown (3), mark-mccandlish (3), dird-series (3), harry-reid (2) | 3 (10) arv-fluxliner > thomas-townsend-brown | 3 (5) earthtech-international > d-contracting | d-custody > project-azorian |

Worked readings (INFERRED judgements; the edge labels are the board's own):

1. **Grusch to Lockheed Skunk Works** (3 hops, 4 paths). One path is a real story: AARO's Volume I rebuts Grusch (denial, T1, 2024), Volume I offers KONA BLUE as the explanation for the reverse-engineering allegations, and the KONA BLUE proposal alleged Lockheed-held material was to be transferred (custody, T2, 2011). The hub-penalised alternative (Grusch > Boeing > McCandlish > Skunk Works) reads as a chain of associations resting on a T3 funding edge and a relayed unnamed informant.
2. **AAWSAP to the UAP Disclosure Act** (2 hops, 1 path). The only shortest path hops through AARO Volume I on a T3 legislative edge. Removing the hubs gives the better story at 3 hops: Reid co-sponsored the AAWSAP money (T1), Schumer names Reid as the legacy he is continuing (T2), Schumer sponsored S.Amdt. 797 (T1).
3. **Roswell 1947 to the July 2023 hearing** (3 hops, 2 paths, both through AARO Volume I). The path is two denials in a row (AARO reaffirms Mogul; AARO rebuts Grusch) and then Grusch's testimony: a hop through the official rebuttal hub, not a connection between Roswell and the hearing. Without hubs it becomes a 5-hop associative chain (memory metal > nitinol > Navy lab > Navy > Nimitz > Fravor's testimony).
4. **Bob Lazar to AARO** (4 hops, 22 paths). Many near-equal routes (ONI, UAPTF, S-4 > Knapp > hearing, Los Alamos > DOE > NASA). The hub-penalised route is a plausible lineage story (Lazar's claimed Naval Intelligence pay, T3 > ONI > UAPTF > the memo that transferred UAPTF data to AARO), but it rests on a T3 claim.
5. **Project Blue Book to AARO** (3 hops, 6 paths, 67% through hubs). Six equal-length routes of very different quality: one is a genuine document lineage (Special Report 14, republished by the Department of War in PURSUE Release 03, staged by AARO; all T1); two are "AARO's 2024 review does not mention X" (Moon Dust, the 1975 overflights), an argument about omission; three rest on a T3 link (UAP Gerb's Battelle investigation to Kirkpatrick; the Haines history to Yankee Blue "precedent"; Wright-Patterson to Grusch). Nothing in the graph ranks the first above the others.

Extra pairs: Pais to Skunk Works (4 hops, 6 paths, 4 of them via Lockheed Martin); Robert Salas to AARO (4 hops, 9 paths, 8 of them through the nuclear PRP regime and then `dod`, a pure containment hop, the ninth through Grusch; no path exists on structural edges at all); Eric Davis to Lockheed Martin (3 hops, 14 paths spread over T. Townsend Brown's 1947 patent assignment, McCandlish, the DIRD series, Reid and Knapp: associations, none of them the Wilson-Davis custody story).

**Path verdict.** MEASURED: paths are short (mean 4.7) and 67% of random pairs can only be joined through a top-20 hub. Over 1,000 random pairs the most frequent intermediates are `david-grusch` 0.17, `aaro-historical-record-vol1` 0.12, `aaro` 0.12, `dod` 0.10, `aawsap` 0.10, `cia` 0.08 (expected appearances as an intermediate per random pair); top-20 hubs are 31% of all intermediate appearances, and the step into them is a `denial` or `institutional` edge 49% of the time. AARO's Historical Record Volume I lies on at least one shortest path for 7 of the 8 reader pairs, and is the whole middle of the AAWSAP-to-UAPDA and Roswell-to-hearing answers. INFERRED from the readings: in two of the five main pairs a genuine story is among the shortest paths but sits beside weaker routes of the same length that nothing distinguishes (Grusch to Skunk Works: 1 or 2 of 4; Blue Book to AARO: 1 of 6); in two every shortest path is a hop through AARO Volume I, which tells the reader that the same office addressed both ends, not how the ends are related (AAWSAP to UAPDA, Roswell to the hearing); and Lazar to AARO has 22 equal routes, the best a plausible lineage resting on a T3 claim. Removing the top-20 hubs recovers a better story in one case (AAWSAP to UAPDA via Reid and Schumer) and a meandering association chain in another (Roswell to the hearing); hub-penalised routing is no more reliable. "Show me the path between X and Y" should therefore not be a headline feature without curation; where it is offered, equal-length paths need ranking by claim tier and edge type, and paths through connector hubs and `denial` edges should be labelled as such.

## 8. Implications for the information architecture (INFERRED from the measurements above)

1. **Organise by topic, and offer topic x era as the map.** The board has about 16-18 topical communities (modularity 0.66-0.70 against 0.48 for a rewired null); three are identical under every weighting and five more survive intact inside larger ones, and they have clear era signatures. They are nearly independent of `cluster` and of the L0 function bands (NMI 0.16-0.24). A reader discovering meaning needs the topics as the primary unit ("AAWSAP lineage", "Roswell and the retrieval tradition", "SAP law", "Other nations"), with role and function as filters inside a topic rather than as the rows of the map. Four macro-regions (Washington 2017-2026, the Cold War record, AAWSAP and the science / contractor strand, other nations) are a usable top level.
2. **Treat connector hubs as indexes, not as nodes to draw.** DoD, AARO, AARO Volume I, Grusch, Lockheed Martin, CIA, DOE and the House Oversight Committee have neighbours in 6-15 topics. Their pages should group neighbours by topic and by edge type ("denied by", "employed", "testified about") instead of fanning them out; provincial hubs (AAWSAP, DIRD series, DIA, Blue Book, UAPDA, Nimitz, BAASS) can be shown as the anchor of their topic. Let connector nodes belong to several topics: 15% of nodes, including the most-opened ones, have no single stable home.
3. **Default to the structural backbone and make the assertion layer a deliberate overlay.** Custody, funding, programmatic, institutional, legislative and research edges alone reach 86% of nodes, and their giant component holds 133 of the 135 L0 nodes and 166 of the 169 Tier A nodes. Denial, witness-chain, investigative and behavioral edges are the cross-topic layer (and the most claim-like); drawing them only when the reader asks "who claims / who denies" keeps the argument while removing most of the "everything connects to everything" effect.
4. **Use time as a slicer on EDGE dates, and give the modern era its own treatment.** 97% of edges can be placed in time; edge-date slices before 2017 are small, sparse and readable, while 2017-2026 is half of all edges and is the hairball. The modern era needs sub-topics (whistleblowers, AARO and releases, legislation, House 2025-2026, incursions) more than any other period. Do not slice by node era.
5. **Close the curation gaps the topics expose, and put people back on the top level.** 45.6% of nodes are in no authored structure and 172 are search-only. Six topics have no thread (other nations, the Roswell tradition, academic science, Kirtland / Dulce, TTSA, incursions), the Cold War Air Force / CIA topic has one thread node, and L0 carries no person although persons are 30% of the board and include the biggest hub on it (Grusch) and three more of the top 15 (Elizondo, Burlison, Luna). One authored thread or topic page per community, plus a person layer, would cover the board with about 18 entry points instead of 1,136 nodes.

## Files

Scripts (run in order): `g.py` (loader and algorithms), `s1_basics.py`, `s2_communities.py`, `s3_consensus.py`, `s4_profiles.py all|hubdamp`, `s5_levels.py`, `s6_edgetypes.py`, `s7_time.py`, `s8_coverage.py`, `s9_paths.py`, `s10_hubroles.py`, `s11_extra.py`, `s12_checks.py`, `make_report.py`. Outputs: `s*.json`, `s9_paths.txt` (full path listings with edge labels), `communities.json`, this report.
