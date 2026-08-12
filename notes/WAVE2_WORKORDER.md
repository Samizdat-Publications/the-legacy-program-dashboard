# THE PROGRAM — WAVE 2 WORK ORDER
**Completeness critic pass over `/root/uap-tracker/research/` (14 domain files)**
Compiled 12 August 2026. Audit artifacts: `/root/uap-tracker/notes/wave2-audit/`
(`dangling.json`, `dupes.json`, `degree.json`, `urls.json`, `sweepall.txt`, and the four
`analyze*.py` scripts that produced them — re-run any of them to refresh these numbers).

---

## 0. STATE OF THE BOARD

| Measure | Value |
|---|---|
| Domain files | 14 |
| Node **records** written | 677 |
| **Unique node ids** | **533** (193 person, 116 document, 83 institution, 47 program, 41 event, 28 legislation, 19 location, 7 domain, 1 mis-classed) |
| Ids defined in more than one file | 84 (merge-collision set) |
| Edges (raw) | **1,205** |
| Edges unique on `(a,b,type)` | 1,139 |
| Edges unique on node pair | 1,075 |
| Timeline entries | 547 (1944–2026; 158 of them 2025–2026) |
| Claims | 2,096 — **Tier 1: 1,248 / Tier 2: 633 / Tier 3: 215** |
| Unique source URLs | 616 |
| Stated gaps across files | 183 |
| **Undefined ids referenced somewhere** | **116** (18 by edges, 83 by `instId`/`locId`, 26 by `domains[]`) |
| Board size if every referenced id is defined | **649 nodes** |

Edge-type distribution: institutional 357 · investigative 163 · denial 126 · witness-chain 124 ·
programmatic 114 · legislative 99 · custody 67 · behavioral 67 · temporal 51 · funding 35 · **oversight 2 (invalid)**.

**Headline judgment.** The board is deep and, on sourcing discipline, unusually clean — 452 of 616
URLs return HTTP 200 unauthenticated, and only two Tier-1 claims anywhere carry a source string too
short to identify a document. The weaknesses are structural, not evidentiary: (a) the connective
tissue of the graph is unfinished — 116 referenced ids have no dossier, including `dod`, `cia`, `doe`,
`nro`, `odni`, `nimitz-2004` and `immaculate-constellation`; (b) the domain taxonomy was never fixed,
so 26 `d-*` ids are referenced ~550 times and defined zero times; (c) the single mechanism the entire
thesis rests on — how a waived unacknowledged SAP legally escapes congressional notification — has no
node, no dossier and no domain file, despite being the most documentable thing on the board; and
(d) the world outside the United States does not exist on this board at all.

---

## 1. DANGLING EDGES — ids used as edge endpoints that no file defines
**18 ids, 88 edge-endpoint references. This is the highest-value work in wave 2:**
every one is an organisation or event already load-bearing in the graph, already carrying sourced
edges written by other researchers, and needing only a dossier to become a first-class node.

Each entry below states: reference count · which files depend on it · what the existing edges already
assert (so the dossier must support those assertions) · what the dossier must establish.

### 1.1 `dod` — Department of Defense / Department of War — **18 refs**
Referenced by: aviators-incidents, congress-house, grusch, media-structure, releases-2023-2026, uaptf-aaro.
Also used as `instId` by 27 person records across 8 files.
Existing edges make it the **denial hub of the entire board**: 15 of its 18 edges are type `denial` —
Gough on Immaculate Constellation; the 17 Dec 2024 four-agency NJ drone statement; the FY2025 report's
no-possession sentence; Reagan deck-log destruction; SCIF access refused to Burchett; the HASC/HAC-D
read-in gate told to Oversight staff; Burlison's blocked 2024 AARO briefing; Luna's missed video
deadline; no reply to Crane's 24 Jul 2025 reprisal letter; no RG 615 compliance accounting;
DODIG-2023-109 withheld.
**Dossier must establish:** the 2025 renaming to Department of War and its effect on citations
(defense.gov 302-redirects to war.gov — already observed by elizondo-ttsa and releases-2023-2026);
the OSD components that actually hold UAP equities (OUSD(I&S), SAPCO, DOPSR, WHS/ESD FOIA, Public
Affairs); the public-affairs statement chain as an institutional artifact; and the fact that DoD is
the counterparty to essentially every unanswered demand on this board. Cluster `ic` or a new
`executive` grouping; C/A/D scoring should be high-A, low-D.
**Do not** fold this into `aaro` — the board needs the parent so denials attributable to the
Department rather than the office stay separable.

### 1.2 `nimitz-2004` — USS Nimitz / 2004 CSG-11 encounter — **13 refs**
Referenced by: aviators-incidents, congress-senate-legislation, scientists-technical.
**Note: `entityInfo['nimitz-2004']` already exists in aviators-incidents with no matching node** —
the dossier body is written, the node record is simply missing. This is a 15-minute fix.
Existing edges: witness-chain to fravor / dietrich / kevin-day; custody to `uss-princeton` and
`flir1-video`; institutional to `vfa-41` and `odni-preliminary-assessment-2021`; investigative to
`navy-range-fouler-reports` and `paper-knuth-powell-reali-2019`; temporal to `kidd-russell-2019`,
`uss-jackson-2023`, `uss-reagan-2004`; and legislative to `ndaa-fy2026` (Congress set 1 Jan 2004 as
the retroactive NORAD intercept floor — i.e. Congress legislated to the Nimitz year).
**Class:** `event`. Read `entityInfo['nimitz-2004']` first and do not re-research from scratch.

### 1.3 `immaculate-constellation` — the alleged parent USAP — **10 refs**
Referenced by: aviators-incidents, congress-house, media-structure, releases-2023-2026, uaptf-aaro.
Distinct from `immaculate-constellation-12-page-report` (which **is** defined, in congress-house and
releases-2023-2026, deg 15). The programme and the document must stay separate nodes; four files
already wrote edges assuming both exist.
Existing edges: programmatic to `gallaudet-2015-email`, `gerb-nro-investigation` (alleges NRO Sentient
fed IMINT/SIGINT into it) and the 12-page report; investigative to `michael-shellenberger` and
`micah-hanks`; denial from `dod` (Gough: no record of any SAP by that name), from `aaro`, and from
`hearing-2024-11-19` (Kosloski's SFR does not mention it).
**Dossier must establish:** entry into the Congressional Record 13 Nov 2024; the ODNI unclassified
press item of 22 Oct 2024; the 2025 provenance dispute attributing the name to a 2018 Schriever
Wargame folder (releases-2023-2026 flags this as unresolved — carry the conflict, do not resolve it);
and the standing fact that no AARO product has ever addressed it.

### 1.4 `cia` — Central Intelligence Agency — **9 refs**, plus 6 as `instId`
Referenced by: congress-house, history-1940s-1960s, history-1970s-2000s, media-structure,
primes-custody, scientists-technical.
Existing edges: funding→`robertson-panel` (convened, sponsored, and concealed the sponsorship);
institutional→`hoyt-vandenberg` (DCI before AF Chief of Staff), →`kit-green` (Life Sciences Division,
OSI), →`michels-gerb-structural-episode` ("The Office of Global Access" chapter at 43:04);
denial→`cia-haines-1997` (the agency's own history conceding deceptive public statements),
→`kona-blue` (alleged termination), →`lockheed-martin` (alleged blocking of the Bigelow divestment —
Elizondo's "it was blocked"); programmatic→`saic`; investigative→`comer-luna-agency-letters-2025`
(addressed to Director Ratcliffe).
**Dossier must establish:** Haines 1997 as a tier-1 self-admission; OSI/DS&T lineage; the Robertson
Panel sponsorship concealment; the named individuals already on the board who came through CIA
(Green, Gaffney, O'Sullivan, Ratcliffe); and the 2025 Comer/Luna agency letters. **`john-ratcliffe`
also needs a person node** (5 mentions in congress-house, no node).

### 1.5 `l-wright-patterson` — **7 refs**, plus 5 as `locId`
Referenced by: aviators-incidents, congress-house, ffrdcs, grusch, history-1940s-1960s, history-1970s-2000s.
The single most cross-domain location on the board and it has no node. Existing edges: custody to
`pentacle-memorandum` (addressed to Miles E. Goll there), to `david-grusch` (the corroborating NASIC
officer sits at the installation), to `operation-blue-fly`; funding to `battelle` (the 1948–49 NiTi
work); institutional to `atic`, to `william-mccasland` (AFRL commander there — now a missing person),
and to `nj-drone-incursions-2024` (airspace closed ~4 hrs, Dec 2024).
**Class:** `location`. Must carry: AMC T-2 → ATIC → FTD → NAIC → NASIC lineage in one place; AFRL;
the 1947–51 T-2 intelligence files that the 1995 GAO search never reached (history-1940s-1960s gap).

### 1.6 `doe` — Department of Energy — **5 refs**
Referenced by: ffrdcs, media-structure, uaptf-aaro.
Existing edges: funding→`jason-advisory-group` (NNSA rescued JASON after DoD declined renewal),
funding→`llnl`; custody→`manhattan-project-2` (alleges custody of recovered material vested in AEC
national laboratories); institutional→`michels-gerb-structural-episode` ("The DOE NEST" at 1:22:01);
investigative→`aaro-fy2025-annual-report` (50 UAS notifications near nuclear infrastructure).
**This node is the gateway to the entire Atomic Energy Act strand** (see §4.1). Must cover: AEC →
ERDA → DOE succession; Restricted Data under 42 U.S.C. §2014(y) as a classification authority
*independent of executive order*; NNSA; the M&O contract model; NEST. `aec` and `nnsa` should be
created at the same time.

### 1.7 `l-kirtland` — **4 refs**, plus 5 as `locId`
Referenced by: ffrdcs, history-1970s-2000s, uaptf-aaro. Edges tie it to `kirtland-manzano-1980`
(Manzano Weapons Storage Area / Coyote Canyon), `afosi-kirtland-file` (AFOSI District 17),
`yankee-blue` (Kirtland linkage — uaptf-aaro grades this tier-2/3, keep it that way), and `aaro`
(nuclear-adjacent unresolved cases). Class `location`.

### 1.8 `nasa` — **3 refs**, plus 4 as `instId`
Edges: institutional→`mark-mcinerney` (Director of UAP Research, name withheld at the 14 Sep 2023
briefing); custody→`pursue-release-01` (Apollo 12/17 records) and →`pursue-release-03` (Gemini crew
debriefings). Must also carry the 2022–23 Independent Study Team (`nasa-uap-ist` / `nasa-uapist` —
see §8.2, these are duplicate ids for one thing).

### 1.9 `afosi` — Air Force Office of Special Investigations — **3 refs**, 1 `instId`
Edges: investigative→`garry-reid-memo-2017` (the AFOSI inquiry into Elizondo's video handling);
denial→`yankee-blue` (AFOSI case 2025-06002-F: no records); institutional→`gerb-hidden-wing` (names
AFOSI/PJ, "the Office of Special Projects," as an operational element). 145 mentions in body text
across 7 files. This node is the hinge between Bennewitz/Doty, Yankee Blue and the Elizondo
disciplinary track — write it once, properly.

### 1.10 `nro` — **2 refs**, 1 `instId`
Edges: institutional→`david-grusch` (Senior Intelligence Officer 2016–2021, Director's briefer) and
→`gerb-nro-investigation`. Precedent value is high: NRO's *existence* was classified until Sept 1992,
which is the board's cleanest documented case of an entire agency being concealed from the public —
that belongs in `PRECEDENT` as well as in the node.

### 1.11 `odni` — **2 refs**, 2 `instId`
Edges: institutional→`uap-science-advisory-council` (established by ODNI with FBI support) and
→`odni-uap-d001` (an ODNI-originated document inside a DoW release). Also the addressee of the
stripped IAA FY2024 §1102 contractor turn-in provision. Must carry the 2021 preliminary assessment
lineage and the 2026 UAP Governance Board relationship.

### 1.12 `oni` — Office of Naval Intelligence — **2 refs**, 3 `instId`
Edges: programmatic→`gerb-mitre-investigation` (two Navy-spearheaded legacy programmes);
institutional→`uap-task-force` (UAPTF sited in the Department of the Navy with ONI involvement).

### 1.13 `stargate-program` — **2 refs**
Edges: programmatic→`sun-streak` and →`harold-puthoff`. history-1970s-2000s defines `grill-flame`,
`center-lane` and `sun-streak` but not the umbrella. Cite the CIA STARGATE corpus via The Black
Vault copies (cia.gov/readingroom is blocked to automated retrieval from this environment).

### 1.14 `l-roswell` — **2 refs**, 2 `locId`
Edges: institutional→`roswell-1947`, investigative→`gao-roswell-report-1995`. Class `location`.

### 1.15 `ndaa-fy2023` — **2 refs**
Edges: legislative→`david-grusch` (helped draft the whistleblower language) and →`aaro` (codified
AARO in statute with a public reporting mandate). congress-senate-legislation defines
`ndaa-fy2023-sec-1673` but not the parent act. P.L. 117-263, §1673 and §1683 lineage.

### 1.16 `l-groom-lake` — **2 refs** (primes-custody)
Edges: institutional→`eg-and-g` and →`groom-lake-presidential-determination`. Class `location`.
The annual presidential determinations are Federal Register-citable — a rare tier-1 anchor for a
site the government spent decades refusing to name.

### 1.17 `nga` — **1 ref** — institutional→`david-grusch` (GS-15 Senior GEOINT Capabilities
Requirements Officer; the agency that detailed him to the UAPTF).

### 1.18 `dhs` — **1 ref** — programmatic→`kona-blue` (prospective SAP, terminated 10 Feb 2024;
Canegallo letter of 5 Feb 2024 already sourced in uaptf-aaro). `kristie-canegallo` also needs a
person node (3 mentions, no node).

---

## 2. DANGLING `instId` / `locId` — 83 ids, ~270 references
Not edge endpoints, so they do not break the graph, but every one is a person dossier pointing at an
affiliation or location the board cannot render. **`l-dc` alone is referenced 115 times by all 14
files** and does not exist.

**Batch A — must exist, high reference count (do these first, ~1 hour total):**
`l-dc` (115) · `dod` (27, §1.1) · `us-senate` (15) · `l-nyc` (10) · `l-la` (8) · `house-oversight`
(7 — **note: `house-oversight-committee` IS defined; this is an id-drift bug in grusch.json, fix by
rewrite not by creating a second node**) · `l-las-vegas` (6) · `cia` (6, §1.4) · `usaf` (6) ·
`l-kirtland` (5) · `l-wright-patterson` (5) · `nasa` (4) · `us-house` (4) · `l-stanford` (4).

**Batch B — id-drift / near-duplicate, fix by normalising the pointer, not by creating a node:**
`l-lasvegas`→`l-las-vegas` · `ous-house`→`us-house` (typo, releases-2023-2026 ×2) ·
`usn`/`us-navy`→one id · `oversight-congress`→`congress` or the committee id ·
`l-cambridge`/`l-cambridge-ma`→one id · `l-langley-afb` vs the defined `l-langley` ·
`l-detroit` vs `l-detroit-arsenal` (these are genuinely different — keep both, define both).

**Batch C — small institutions named as employers, need thin real nodes:**
`afrl` · `nsa` · `dod-sapco` (see §4.1 — this one is not thin, it is central) · `the-intercept` ·
`pogo` · `enigma-labs` · `documatica-research` · `blue-marble-space-institute` ·
`wayne-state-university` · `vanderbilt-university` · `harvard-university` · `eop` · `congress`.

**Batch D — 40+ single-reference city/site locations** (`l-boise-id`, `l-fort-worth-tx`,
`l-boulder-co`, `l-ft-meade`, `l-sri`, `l-huntington-beach`, `l-london`, `l-stockholm`, and the ~25
congressional home-district cities from congress-house). Cheapest possible fix: a generated
locations file with `{id, cls:'location', label, desc:null, sources:[]}` — the schema explicitly
permits `desc: null` as a stated gap. Do this mechanically; do not spend research time on it.

---

## 3. UNDEFINED DOMAIN TAXONOMY — 26 `d-*` ids, ~550 references, 0 definitions
This is the largest single integrity defect on the board and nobody caught it, because `domains[]`
is not validated the way edges are. Seven domain nodes exist (`d-custody`, `d-materials`, `d-media`,
`d-structure`, `d-ffrdc`, plus `ffrdc-mechanism` and `sap-readin-gate` which are mis-classed as
`domain`). Twenty-six more are referenced and undefined:

| id | refs | id | refs | id | refs |
|---|---|---|---|---|---|
| d-oversight | 124 | d-legacy | 22 | d-recovery | 5 |
| d-coverup | 115 | d-exotic | 18 | d-psyop | 5 |
| d-witness | 40 | d-aviators | 18 | d-legislation | 3 |
| d-records | 33 | d-legislative | 17 | d-policy | 3 |
| d-disclosure | 29 | d-ic | 11 | d-program | 2 |
| d-research | 29 | d-prop | 8 | d-secrecy-architecture | 2 |
| d-funding | 26 | d-astro | 7 | d-contracting | 1 |
| | | d-paranormal | 5 | d-contractor | 1 |
| | | d-bio | 5 | d-ffrdc-mechanism | 1 |
| | | | | d-legal | 1 |

**Task:** one session, one owner, no research required. Fix the canonical set (recommend ~16:
`d-legacy`, `d-recovery`, `d-custody`, `d-materials`, `d-exotic`→merge into `d-materials`,
`d-funding`, `d-secrecy-architecture` (absorbing `d-legal`/`d-policy`), `d-ic`, `d-psyop`,
`d-coverup`, `d-witness`, `d-aviators`, `d-oversight` (absorbing `d-legislative`/`d-legislation`),
`d-records` (absorbing `d-disclosure`), `d-research` (absorbing `d-astro`/`d-bio`/`d-prop`/
`d-paranormal`), `d-media`, `d-ffrdc` (absorbing `d-ffrdc-mechanism`), `d-contractor` (absorbing
`d-contracting`)), write the domain nodes, then rewrite every `domains[]` array against the canon.
Also reclass `ffrdc-mechanism` and `sap-readin-gate` from `domain` to `program`/`document` — they are
mechanisms, not taxonomy, and mixing them corrupts any domain filter in the UI.

---

## 4. MISSING DOMAINS — new research assignments
Ranked by how much load the board's thesis puts on them.

### 4.1 ⭐ THE SAP / USAP LEGAL ARCHITECTURE — *the largest hole on the board*
**Nothing on this board explains, from statute and regulation, how a programme can lawfully exist
without congressional notification.** That is the mechanism the entire premise rests on, it is
entirely documentable from open sources, and it has no domain file, no node and no dossier.
Present coverage: `usc-10-119` (1 node, primes-custody), `sap-readin-gate` (congress-house, mis-classed
as `domain`), `dod-sapco` (an `instId` pointer to nothing), 16 body-text mentions of "unacknowledged
special access" and 13 of "Gang of Eight." Zero nodes for USAP, waived SAP, black budget, or the
Gang of Eight convention.
**Primary documents to build from (all retrievable):**
- 10 U.S.C. §119 — SAP congressional oversight; §119(e) waiver: the SecDef may waive notification for
  a programme if he determines it is "essential to the national security" and notifies only the
  chairs and ranking members of the defense committees. **This is the waived-unacknowledged mechanism
  in statute; quote §119(e)(1)–(3) verbatim.** uscode.house.gov (govinfo bulk USLM works from here).
- 50 U.S.C. §3093(c)(2) — the Gang of Eight limitation on covert-action notification.
- E.O. 13526 §4.3 — Special Access Programs; the limitation on who may create one.
- DoDD 5205.07 and the DoDM 5205.07 volumes — SAP policy, categories (acknowledged / unacknowledged /
  waived), and the SAPCO structure. DoD Directives Division (esd.whs.mil — 403s to curl, fetches fine
  via a browser agent).
- DoDI 5205.11 — management of SAPs. DoDI 3204.01 — IR&D (already cited by primes-custody).
- The annual SAP Annual Report to Congress requirement and the SAPOC.
- 32 CFR Part 117 (NISPOM as a rule) and the DD Form 254 — the contractor-side instrument (ffrdcs
  already flags DD-254 as an unexecuted research route).
- 42 U.S.C. §2014(y) / §2162 — Restricted Data, the AEA classification channel that does **not** run
  through E.O. 13526 and is not subject to §119. primes-custody already flags this as a tier-3
  inference re Bechtel Nevada; this domain should upgrade it to tier 1 as a matter of law.
**Nodes to create:** `usap`, `waived-sap-mechanism`, `usc-10-119` (extend the existing node),
`usc-50-3093`, `eo-13526`, `dodd-5205-07`, `dodi-5205-11`, `dod-sapco`, `sapoc`, `gang-of-eight`,
`dd-form-254`, `nispom-32cfr117`, `restricted-data-aea`, `david-abba` (exists but deg 1 — see §6),
plus a domain node `d-secrecy-architecture`.
**Why it matters editorially:** media-structure already carries a tier-3 inference that if the
mechanism works as alleged, congressional ignorance is *lawful non-reporting rather than unlawful
concealment*. That inference is currently unsupported by any legal node. Supporting it converts the
board's weakest rhetorical point into its strongest structural one.

### 4.2 ⭐ BLACK BUDGET MECHANICS AND THE APPROPRIATIONS CHANNEL
Adjacent to but distinct from §4.1. "black budget" appears in exactly one file, 8 times.
**Build:** the National Intelligence Program / Military Intelligence Program split and the only two
figures ever published; the classified annex convention in the defense appropriations conference
report; the "pass-through" line; 10 U.S.C. §424 (DIA/NGA/NRO exemption from disclosing organisation
and function — the statute aawsap-aatip found blocks FPDS/USAspending visibility); 31 U.S.C. §1301
purpose statute; the CIA Act of 1949 §8(b) unvouchered-funds authority (**the cleanest documented
precedent for lawful, auditless federal spending — it belongs in `PRECEDENT`**); GAO's standing
inability to audit; the DCAA IR&D route already legislated against in NDAA FY2024 §1687(b).
Three files independently flagged the IR&D reconciliation (Defense Innovation Marketplace submissions
+ DCAA audits + FPDS) as never attempted — this domain should own that task.

### 4.3 ⭐ INTERNATIONAL PROGRAMS — **zero coverage; every search term returns 0 hits**
Condign, COMETA, GEIPAN, Operação Prato, CEFAA, Project Magnet: **not one appears anywhere in
1,205 edges or 547 timeline entries.** This is a whole continent of primary documents the board has
not touched, and much of it is *better sourced than the American material* because the documents were
officially released rather than leaked.
- **UK:** DI55 / *Unidentified Aerial Phenomena in the UK Air Defence Region* ("Project Condign"),
  commissioned 1996, delivered Dec 2000, released under FOI 2006 — a formally classified (Secret UK
  Eyes Only) government study concluding UAP are real and of defence interest. The full PDF set is in
  The National Archives (Kew) DEFE 24 series and on the TNA UFO release pages. Also: MoD Sec(AS)2,
  the 2009 desk closure, the Rendlesham Halt memo's UK-side records (history-1970s-2000s covers the
  US side only), Nick Pope (1 file, 3 mentions, no node).
- **France:** COMETA report *Les OVNI et la Défense* (July 1999) — produced by IHEDN auditors
  including a former head of the Institut des Hautes Études de Défense Nationale; GEIPAN inside CNES,
  the only permanently funded state UAP office in the world, with a **public case database** (the
  single most auditable government UAP dataset in existence — a direct empirical counterweight to
  AARO's unpublished holdings); its predecessors GEPAN (1977) and SEPRA.
- **Brazil:** Operação Prato (1977, I Comando Aéreo Regional, Colares) — the Air Force's own
  photographic and medical files, released 2004–09 to the Brazilian UFO research community and now in
  the Arquivo Nacional; "A Noite Oficial dos OVNIs" (19–20 May 1986), acknowledged in a live press
  conference by the Minister of Aeronautics Octávio Moreira Lima — **a serving defence minister
  confirming multi-aircraft radar-visual intercepts on the record, which no US official has ever
  done.** Brazil's 2010 ministerial order requiring military UAP reports to be archived at the
  Arquivo Nacional is the world's only functioning analogue to RG 615.
- **Chile:** CEFAA within the DGAC, the 2014 Chilean navy helicopter FLIR case and its published
  analysis.
- **Canada:** Project Magnet (Wilbert Smith, Department of Transport, 1950–54) and the **1950 Smith
  memorandum** stating the subject was classified in the US "two points higher than the H-bomb" and
  that Vannevar Bush headed a small study group — held by Library and Archives Canada, and one of the
  earliest documents anywhere alleging exactly the structure this board asserts. Also Project Second
  Storey.
**Editorial payoff:** these are foreign-government primary documents that do not depend on US
declassification and cannot be suppressed by any US authority. For a board built on the premise of
American concealment, they are the strongest available external corroboration and their total absence
is the most conspicuous gap in the corpus.

### 4.4 CRASH-RETRIEVAL CASE LITERATURE
Zero hits for Stringfield or Ryan Wood. The board asserts a retrieval programme and has no node for
the body of case literature that documents the alleged retrievals.
**Build:** Leonard H. Stringfield's *Status Report* series I–VII (1978–94) and his 1978 MUFON
symposium paper — the first systematic aggregation of retrieval testimony, with a named-source
methodology and a documented practice of protecting informant identities that is itself worth
recording as a chain-of-custody problem; Ryan S. Wood's *Majic Eyes Only* and the Wood
"Majestic Documents" corpus (**must be handled with the same discipline history-1940s-1960s applied
to MJ-12 — NARA's forensic take-down of the Cutler-Twining memo is already on the board and should
anchor the tier grading here**); Kevin Randle and Don Schmitt; the Aztec 1948 and Del Rio claims;
Kecksburg 1965 and the CBS/Leslie Kean NASA records litigation (a *documented* federal records fight,
tier 1, currently 1 mention); Varginha 1996 (2 files, 4 mentions, no node); Trinity/San Antonio 1945.
**Grade these hard.** Most of it is tier 2 at best and some is tier 3. The value is that the board
currently has an assertion with no literature behind it; a critic will ask where the cases are.

### 4.5 IC COUNTERINTELLIGENCE AND THE DISINFORMATION APPARATUS
Partially present (Doty 123 mentions, AFOSI 145, Bennewitz in history-1970s-2000s) but **no node
treats disinformation as a system rather than as one man's misconduct.**
**Build:** the Robertson Panel's 1953 recommendation to strip UFOs of "special status" and to use
mass media (already on the board via history-1940s-1960s) as the founding policy document; the
CIA-acknowledged U-2/OXCART cover-story practice from Haines 1997; AFOSI's counterintelligence
mission as the institutional home of the Bennewitz operation; the alleged use of forged documents
(Aquarius paper, MJ-12) as a CI technique rather than as evidence; Yankee Blue as the modern instance
— and the structural point that a *documented* USAF programme convincing its own personnel of a
fictitious alien-technology mission is the strongest evidence on the board that this apparatus is
operational, not historical. Nodes: `disinformation-apparatus`, `robertson-panel-media-recommendation`,
`afosi` (§1.9), `mirage-men`.
**Precedent extension** (schema Part 2 asks for this explicitly): MKULTRA and the 1973 Helms-ordered
record destruction; Church and Pike; Iran-Contra; the AEC human radiation experiments; NRO's
classified existence to 1992.

### 4.6 THE AEROSPACE INSIDER / DEATHBED-TESTIMONY LAYER
`ben-rich` exists with 1 source and deg 2; `james-ryder` deg 2, 1 claim; `alfred-odonnell` in
primes-custody; Boyd Bushman, Don Phillips, Brad Sorensen: **0 hits.** primes-custody itself names
the Ben Rich 1993 UCLA remark and the John Andrews letters as "the single most valuable recoverable
artifact in this domain" and grades them tier 3 with no archival primary. This layer needs either a
proper domain file that runs the archival searches (UCLA event records, the Andrews correspondence in
the Testors/model-industry papers, Bushman's Lockheed personnel record) or an explicit board-level
decision to keep it thin. **Do not let it stay in its current state — one source, tier-3, high
narrative prominence is exactly the profile that gets a board discredited.**

### 4.7 THE VATICAN AND THE RELIGIOUS ANGLE — 0 hits
Low evidentiary weight, real structural weight: Monsignor Corrado Balducci's Italian television
statements; the Vatican Observatory (Consolmagno, Funes, Coyne) and its published positions;
Sheehan's account of a 1977 Vatican Library review (his own claim — tier 2 at best, and it belongs in
his `unverified[]` alongside the 1988 Rule 11 sanction already recorded there); the 2023 "Age of
Disclosure" religious-preparation framing. One thin, honestly graded node cluster; do not inflate it.

### 4.8 THE 2025–2026 NEWS CYCLE — **not a gap in volume, a gap in ownership**
158 timeline entries already sit in 2025–26 (2026 alone is the single densest year on the board at
100 entries). The problem is that PURSUE, the UAP Science Advisory Council, the UAP Governance Board,
the Burlison FFRDC letters and the FY2027 NDAA amendment are each written **four to six times by
different researchers**, which is where most of the 84 duplicate ids come from. Wave 2 should not
re-research this; it should **assign a single owner to reconcile it** (see §8).
Genuinely unowned 2026 items: the **UAP Governance Board** (named in four files, charter located by
none — the most important undocumented institution created in 2026); whether a signed instrument
establishing PURSUE exists at all (Hegseth called it "that executive order"; only a Truth Social post
is documented); the McCasland disappearance and the Comer/Burlison missing-scientists probe (the
board's direct bridge to *The Vanishing*, currently 1 file / 2 sources).

---

## 5. THIN NODES — fewer than 2 unique source URLs
**85 nodes.** Full machine list: `notes/wave2-audit/rows.json` regenerated by `analyze2.py`.
Ordered by degree, because a thin node with high degree is a load-bearing claim resting on one cite.

**Priority 1 — thin AND well-connected (deg ≥ 4). Fix these or the graph is resting on single cites:**

| node | deg | srcs | file | what it needs |
|---|---|---|---|---|
| `nyt-2017-12-16` | 10 | 1 | elizondo-ttsa | The founding press artifact of the modern era with one URL. Add the NYT piece itself, the Politico same-day piece, the Kean/Blumenthal bylines, and the 2023 NYT refusal recorded in media-structure. |
| `jeremy-corbell` | 6 | 1 | media-structure | Sourced to Wikipedia only (see §7.2). Needs primary: his own releases, the Weaponized feed, the 2021 leaked-video reporting. |
| `michels-gerb-structural-episode` | 6 | 1 | media-structure | The board's central structural-media artifact on one YouTube URL. Add the description capture as a separate archived source and any third-party coverage. |
| `capitol-disclosure-event-2026-06-09` | 5 | 1 | congress-house | Grusch's "slush funds… billions per annum" claim hangs off this. Needs video, transcript and at least one wire report. |
| `navy-range-fouler-reports` | 4 | 1 | aviators-incidents | **Highest-priority thin node on the board.** It carries the single strongest primary-document suppression finding ("Reporting terminated at 3rd Fleet, there was no process to share the reporting") on one FOIA URL. Add the FOIA case number, the release letter, and a mirrored copy. |
| `uap-select-committee-proposal` | 4 | 1 | congress-house | |
| `missing-scientists-probe-2026` | 4 | 1 | congress-house | The bridge to *The Vanishing*. Needs the committee letter itself. |
| `ndaa-fy2024-subtitle-c` | 4 | 1 | congress-senate-legislation | Statutory — trivially fixable from govinfo + uscode. |
| `ndaa-fy2023-sec-1673` | 4 | 1 | congress-senate-legislation | Same. |
| `debrief-2023-06-05` | 4 | 1 | grusch | The Kean/Blumenthal Debrief article — needs the archived copy and the NYT-refusal context. |
| `james-mcdonald` | 4 | 1 | history-1940s-1960s | Arizona archives hold his papers; his 1968 House testimony is in the hearing record. |
| `gerb-nro-investigation`, `gerb-hidden-wing`, `gerb-sandia-investigation` | 4/4/1 | 1 | media-structure | Single-YouTube-URL nodes making programmatic allegations. Either add corroboration or drop their claim tiers. |
| `jiatf-401` | 3 | 1 | aviators-incidents | A standing joint task force with one source. DoD releases + defense trade press. |
| `crane-dod-reprisal-letter` / `crane-secdef-grusch-reprisal-letter-2025` | 3/2 | 1 | grusch / congress-house | **Same document, two ids** (§8.2). Full text still not located — both files flag it. |
| `low-memo` | 3 | 1 | history-1940s-1960s | Colorado archives hold the original. |
| `l-pax-river` | 3 | 1 | primes-custody | Storage allegation on unnamed sources — keep tier low, add sources. |

**Priority 2 — thin, deg 2–3, high narrative weight:** `william-mccasland` (the missing general),
`uss-reagan-2004` (deck-log destruction), `ben-rich`, `james-ryder`, `project-bear`, `jonathan-grey`,
`david-abba`, `mark-milley`, `nasic`, `donald-kerr`, `beacon-hill-study`, `charette-memo-2023`,
`doty-personnel-file`, `off-world-technologies-division`, `trump-uap-declass-directive-2026`
(**a presidential directive with one source — unacceptable for a tier-1 artifact; find the signed
instrument or downgrade the tier**).

**Priority 3 — deg 1, thin, low stakes:** the ~30 remaining, including most congress-house member
nodes with a single claim. Acceptable to leave, but mark them tier C.

---

## 6. UNDER-CONNECTED HUBS
Degree top of board for calibration: `david-grusch` 78 · `aaro` 60 · `luis-elizondo` 43 ·
`pursue-releases` 41 · `aaro-historical-record-vol1` 38 · `hearing-2025-09-09` 28 ·
`eric-burlison` 28 · `anna-paulina-luna` 26 · `mitre-corporation` 25 · `sol-foundation` 23.

**Nodes whose dossier weight is badly out of proportion to their edge count:**

| node | deg | claims | srcs | files | edges it should have |
|---|---|---|---|---|---|
| `kit-green` | 8 | 12 | 11 | 4 | The single most cross-domain person on the board (CIA OSI → AAWSAP DIRD author → Wilson-Davis custodian → Nolan's medical-effects predecessor) with 8 edges. Needs: →`cia`, →`dird-green-clinical-medical`, →`wilson-davis-memo` custody, →`garry-nolan`, →`institute-advanced-studies-austin`, →`aawsap`, →`eric-davis`, →`robert-bigelow`. |
| `kona-blue` | 13 | 18 | 12 | 5 | 18 claims, 5 files, and it is the only programme on the board DoD has *admitted*. Needs edges to `dhs`, `doe`, `james-lacatski`, `colm-kelleher`, `aaro-historical-record-vol1` (which names it), `uapda-2023`. |
| `jon-kosloski` | 13 | 17 | 19 | 4 | Sitting AARO director, 19 sources, 13 edges. Needs edges to every annual report, to `hearing-2024-11-19`, `hearing-2025-09-09`, `uap-science-advisory-council`, `pursue-releases`, `immaculate-constellation`, `aaro-historical-record-vol2`. |
| `matt-gaetz` | 1 | 4 | 2 | 1 | Sworn witness-adjacent member who demanded the Eglin radar under oath. Needs →`l-eglin`, →`hearing-2023-07-26`, →`dod` denial. |
| `alexandria-ocasio-cortez` | 2 | 6 | 3 | 2 | The "dead email box" congressional-notification exchange is a structural finding with 2 edges. |
| `jay-stratton` | 6 | 9 | 9 | 3 | Alleged UAPTF director; needs →`uap-task-force`, →`aawsap`, →`baass`, →`oni`, →`nimitz-2004`. |
| `sandia` | 3 | 7 | 5 | 2 | Three Sandia reviewers appear in the 2009 DIA deliverables review; sandia has 3 edges. |
| `dodig-2023-109` | 5 | 9 | 5 | 2 | The finding that DoD does not require components to report UAP to AARO invalidates every "AARO has not discovered" statement — that should be an edge to each annual report and to `aaro`, not a claim sitting in one node. |
| `aaro-historical-record-vol2` | 5 | 9 | 8 | 2 | The board's central *absent* artifact. Should carry a denial edge to every official who promised it (Ryder, Kosloski, Gough) and to `yankee-blue`. |
| `mit-lincoln-laboratory` | 5 | 8 | 6 | 2 | First FFRDC to commit to producing a UAP record to Congress — 5 edges. |
| `avi-loeb` | 5 | 8 | 15 | 2 | Chairs the 2026 council; 15 sources, 5 edges. |
| `steven-schiff` | 3 | 8 | 4 | 2 | The member who forced GAO/NSIAD-95-187 — the load-bearing tier-1 document of the legacy era. |
| `jeffrey-nuccetelli`, `alexandro-wiggins`, `dylan-borland` | 4/5/7 | | | 3–4 | Three 2025 sworn witnesses written by 3–4 researchers each and connected to almost nothing. |
| `bigelow-aerospace` | 4 | 6 | 6 | 2 | Should be a custody hub: →`baass`, →`aawsap`, →`nids`, →`l-skinwalker`, →`lockheed-martin` (the alleged transfer), →`robert-bigelow`. |

**Systemic cause:** researchers wrote edges within their own domain and reached across only for the
ids on the shared list. The merge pass should run a deliberate **cross-domain edge sweep**: for each
of the 84 duplicated ids, look at the union of its edges and ask what is missing.

---

## 7. SOURCING RISK — flag hard
The corpus is, on the whole, defensible: 616 unique URLs, 452 return HTTP 200 to an unauthenticated
sweep from this environment, and **only two Tier-1 claims anywhere carry a source string too short to
identify a document** (both are `war.gov/UFO`, the PURSUE portal — fix by citing the specific portal
page and capture date). No fabricated document numbers were found. Every researcher who lost
WebSearch said so in their notes. That is the good news; the following are the real exposures.

### 7.1 ⭐ TIER-1 INFLATION — 59.5% of all claims are Tier 1
1,248 of 2,096. On a board whose entire premise is contested, a 6:3:1 tier ratio is the profile of a
grading standard that drifted. Tier 1 is defined in SCHEMA.md as "what survives a hostile audit."
**Assign a reviewer to re-grade, starting with the categories in 7.2–7.5.** A defensible target is
closer to 45–50% Tier 1.

### 7.2 ⭐ WIKIPEDIA CITED AS TIER 1 — 29 URLs, 20 Tier-1 claims, nearly all in `media-structure`
`ross-coulthart`, `leslie-kean`, `ralph-blumenthal`, `george-knapp` (×3), `jeremy-corbell` (×2),
`michael-shellenberger`, `bryce-zabel` (×2), `daniel-sheehan` (×2), `steven-greer` (×2),
`weaponized-podcast`, `klas-tv`, `cseti`, `public-substack`, `new-paradigm-institute`, `d-media`.
**Wikipedia is a tertiary source and cannot support Tier 1 on any board that expects hostile review.**
This is the single most quotable weakness in the corpus: a critic needs one screenshot to make the
point. Two acceptable fixes — (a) downgrade all to Tier 2, or (b) follow Wikipedia's own citations to
the primary and re-cite. The researcher's own note says WebSearch was exhausted and Wikipedia
citation metadata was used as a substitute; that is honest, but it must not be graded Tier 1.

### 7.3 ⭐ YOUTUBE AS TIER 1 FOR PROGRAMMATIC ALLEGATIONS
29 YouTube URLs (all returned 429 in the sweep — rate-limiting, not absence). Two Tier-1 claims in
`ffrdcs` cite the UAP Gerb MITRE video and its publication record. **The distinction must be held
explicitly in the text of each claim:** Tier 1 is defensible for *"this video was published on this
date with this description"* (a verifiable fact about the artifact); it is not defensible for *"MITRE
was founded with a hidden reverse-engineering impetus"* (the artifact's content). ffrdcs and
media-structure both mostly did this correctly — verify claim by claim and fix any that conflate the
two. The Atlantic "tic tac factory" USO allegation is already self-flagged by media-structure as the
weakest link; keep that flag and make sure it is Tier 3, not Tier 2.

### 7.4 DEAD AND UNRESOLVABLE URLS — fix or replace
- `https://dpo.tothestarsacademy.com/blog/crada-faq` — **HTTP 000, DNS/connection failure**
- `https://dpo.tothestarsacademy.com/blog/to-the-stars-academy-of-arts-science-makes-groundbreaking-metamaterials-acquisition` — **HTTP 000**
  Both cited in elizondo-ttsa / primes-custody for the CRADA and the $35,000 metamaterials purchase.
  **These are load-bearing for the only fully documented private-custody chain on the board.**
  Replace with the SEC EDGAR Form 1-A Exhibit 6.28 (already cited elsewhere in primes-custody, and
  sec.gov works) and a web.archive.org capture. Do not leave a dead TTSA marketing URL supporting a
  custody claim.
- `https://www.newsmax.com/newsfront/eric-burlison-gop-uap/2026/05/16/id/1256505/` — **HTTP 000**
- `https://irp.fas.org/dia/aatip-list.pdf` — HTTP 202 empty body through the proxy (scientists-technical
  reported this; the FAS landing page confirms the URL). Cite the landing page as well.
- 3 × HTTP 406 (cbsnews, huffpost) and 2 × 302 (cia.gov readingroom) — verify content, add archive links.

### 7.5 130 URLS RETURN 403 TO AUTOMATED RETRIEVAL — **not errors, but not independently verified either**
Hosts: aaro.mil (18) · congress.gov (15) · thehill.com (12) · mitre.org (11) · war.gov (9) ·
newsnationnow (6) · doi.org (6) · sec.gov (5) · esd.whs.mil (5) · dni.gov (4) · media.defense.gov (4) ·
avi-loeb.medium.com (4) · 8newsnow (4) · gao.gov, dodig.mil, dia.mil, vault.fbi.gov, af.mil,
norad.mil, navy.mil, nytimes.com, science.org, c-span.org, documentcloud, harvard, aerospace.org.
These are bot-blocks and several researchers independently reported fetching the same URLs
successfully via browser agents. **But the board should not ship with 21% of its citations
unverifiable by the tooling that will be used to check it.** Wave 2 task: re-verify all 130 through a
browser agent, record the verification date in each `sources[].date`, and add a
`web.archive.org` mirror for every `.mil` and `war.gov` URL — the PURSUE portal in particular is a
politically volatile artifact that could change or disappear between now and publication.

### 7.6 SPECIFIC CLAIMS TO RE-GRADE (named by their own authors, and one they did not name)
Carried honestly by the researchers and still needing a second look:
- Ben Rich 1993 UCLA remark and the John Andrews letters — no archival primary, currently Tier 3 in
  primes-custody. Correct grading; the exposure is that the *narrative* leans on them harder than
  the tier does.
- Dana White's alleged Dec 2017 confirmation that Elizondo led AATIP — correctly in `unverified[]`.
  Verify no other file promoted it.
- USS Princeton recording-media confiscation — Tier 3, and **in direct documented conflict with
  Fravor's own written testimony** ("tapes were never taken"). aviators-incidents recorded the
  conflict on four records; make sure the merge does not smooth it.
- Rubio's "very high clearances and high positions" — in `unverified[]`, citation unpinned.
- Jay Stratton's UAPTF directorship — Tier 2/3, no government record; Wikipedia names a different
  person. Do not let this drift to Tier 1 in the merge.
- Travis Taylor as UAPTF chief scientist — rests on a single *Science* article.
- The Luna-reported Kosloski apology (May 2026) — no transcript, letter or memorandum.
- **Not previously flagged:** `trump-uap-declass-directive-2026` and `uap-nda-waiver-directive-2026`
  are cited across three files as directives but no file located a signed instrument, and
  releases-2023-2026 records that only a Truth Social post is documented for PURSUE. Three files
  nonetheless treat the directive as an established artifact. **Either produce the Federal Register /
  whitehouse.gov presidential action or restate every one of these as "announced, instrument not
  located."** This is the highest-consequence unflagged sourcing risk in the corpus, because it sits
  at the head of the 2026 disclosure strand.

---

## 8. MERGE AND INTEGRITY TASKS (mechanical, no research)

### 8.1 Eighty-four ids defined in more than one file
Full matrix in `notes/wave2-audit/dupes.json`. Worst collisions:
`aaro-historical-record-vol1` (7 files) · `hearing-2025-09-09` (6) · `luis-elizondo` (5) ·
`kona-blue` (5) · `anna-paulina-luna` (5) · `hearing-2024-11-13` (5) · then 12 ids at 4 files.
**56 of the 84 carry conflicting `label` strings.** Rule for the merge: prefer the record from the
file that *owns* the subject (grusch.json owns `david-grusch`; uaptf-aaro owns `aaro`), then union
the `claims[]`, `sources[]`, `chronology[]`, `conflicts[]` and `unverified[]` arrays, then dedupe
claims on normalised text. Do not average the tiers — take the **lowest** tier where two files grade
the same claim differently.

### 8.2 Near-duplicate ids that are the same object (38 pairs found; these are the real ones)
- `nasa-uap-ist` (aviators-incidents) ≡ `nasa-uapist` (scientists-technical) — **identical object**
- `gerb-mitre-investigation` (media-structure) ≡ `uap-gerb-mitre-investigation` (ffrdcs)
- `aaro-grusch-interview-memo` (grusch) ≡ `aaro-grusch-interview-memo-2024` (uaptf-aaro)
- `kirkpatrick-sciam-oped` (grusch) ≡ `kirkpatrick-sciam-oped-2024` (uaptf-aaro)
- `ttsa-army-crada` (elizondo-ttsa, primes-custody) ≡ `ttsa-army-crada-2019` (scientists-technical)
- `age-of-disclosure` (media-structure) ≡ `age-of-disclosure-2025` (scientists-technical)
- `crane-dod-reprisal-letter` (grusch) ≡ `crane-secdef-grusch-reprisal-letter-2025` (congress-house)
- `trump-uap-declass-directive-2026` (grusch) ≡ `trump-uap-release-directive-2026` (releases-2023-2026)
- `aaro-fy2025-report` (aviators-incidents) ≡ `aaro-fy2025-annual-report` (3 files)
- `iaa-fy2024-sec-1102` (congress-senate-legislation) vs `iaa-fy2024-sec1104` (primes-custody) —
  **these are different sections of the same act; confirm which is which before merging. The Senate
  original was §1102 in Division M; primes-custody cites S.2103 §1104. Resolve against the engrossed
  text; getting this wrong is a citation error in the board's single best legislative finding.**
- `hearing-2024-11-13` (5 files) vs `hearing-2024-11-19` (uaptf-aaro) — **verify these are two
  different hearings and not a date error.** One is the House Oversight Task Force hearing at which
  Shellenberger delivered Immaculate Constellation; check the second against the GPO record.
- `hr-5060-uap-whistleblower-protection-act` vs `hr-10111-uap-whistleblower-protection-act`;
  `hr-1187-uap-transparency-act` vs `hr-8424-uap-transparency-act` — likely different Congresses of
  the same bill; confirm and cross-link rather than merge.
- Not duplicates, do not merge: `garry-reid` / `harry-reid`; the five `pursue-release-0N` nodes;
  `elizondo-resignation-letter-1` / `-2` (elizondo-ttsa established these are genuinely two letters).

### 8.3 Schema violations
- **Invalid edge type `oversight`** — 2 edges in `aawsap-aatip.json`
  (`reid-sap-letter-2009`→`william-lynn`; `dia-aatip-letter-2018`→`defense-appropriations-aawsap`).
  Not in `EDGE_TYPES`. Remap to `legislative` and `funding` respectively.
- **`nara-uap-collection` in grusch.json has `cls: 'entity'`** — not a valid class. Should be
  `institution` or `document`, and it collides in meaning with `nara-uap-records-collection`
  (releases-2023-2026), `uap-records-collection-rg615` (congress-senate-legislation) and
  `rg-615-uap-records` (history-1940s-1960s). **Four ids for one records collection.** Pick one.
- **Cluster set drift:** `custody` (1 use) and `program` (1 use) appear as cluster values but are not
  in the schema's `CLUSTERS`. Reassign to `contractor` and `legacy`.
- `ffrdc-mechanism` and `sap-readin-gate` are classed `domain` but are mechanisms — reclass (§3).
- `entityInfo['nimitz-2004']` has no node (§1.2).

### 8.4 Edge count discipline
1,205 raw → 1,139 unique on `(a,b,type)` → 1,075 unique pairs. Five files exceeded the 30–80 edge
guidance (congress-house 128, media-structure 100, aviators-incidents 98, scientists-technical 93,
uaptf-aaro / elizondo-ttsa 87). Each author defended the overage and each defence is sound — the
excess is hand-written, individually sourced denial chains and custody structures. **Recommendation:
accept the overage; do not trim.** But dedupe the 66 exact repeats and the 64 same-pair-different-type
edges, and prefer the version carrying the better source.

---

## 9. TOP 15 WAVE-2 TASKS, RANKED

1. **Write the 18 dangling-edge dossiers** (§1) — `dod`, `nimitz-2004`, `immaculate-constellation`,
   `cia`, `l-wright-patterson`, `doe`, `l-kirtland`, `nasa`, `afosi`, `nro`, `odni`, `oni`,
   `stargate-program`, `l-roswell`, `ndaa-fy2023`, `l-groom-lake`, `nga`, `dhs`. 88 sourced edges are
   currently pointing at nothing. Start with `nimitz-2004` — its `entityInfo` body already exists.
2. **New domain file: SAP / USAP legal architecture** (§4.1). The mechanism the whole thesis rests on,
   fully documentable from 10 U.S.C. §119(e), 50 U.S.C. §3093(c)(2), E.O. 13526 §4.3, DoDD 5205.07 and
   32 CFR 117. Highest intellectual return on the board.
3. **Fix the domain taxonomy** (§3). 26 undefined `d-*` ids, ~550 references. One session, no research.
4. **Re-grade Tier 1** (§7.1–7.3), starting with the 20 Wikipedia-sourced Tier-1 claims in
   media-structure and the YouTube-sourced programmatic claims in ffrdcs. Target ≤50% Tier 1.
5. **Resolve the 2026 presidential directives** (§7.6). Produce the signed instruments for the Feb 2026
   declassification directive, the July 2026 NDA waiver and PURSUE — or restate all three across four
   files as announced-but-uninstrumented. This sits at the head of the entire 2026 strand.
6. **New domain file: international programs** (§4.3) — Condign/DEFE 24, COMETA, GEIPAN's public
   database, Operação Prato and the 1986 Brazilian ministerial press conference, CEFAA, Project Magnet
   and the 1950 Smith memorandum. Zero current coverage; foreign primary documents immune to US
   classification.
7. **New domain file: black budget and appropriations mechanics** (§4.2), including the IR&D/DCAA/FPDS
   reconciliation that three separate files independently named as never attempted.
8. **Merge the 84 duplicate ids and the 11 real near-duplicate pairs** (§8.1–8.2), settling
   `iaa-fy2024-sec-1102`/`-sec1104` and `hearing-2024-11-13`/`-11-19` against primary text first.
9. **Repair the 16 thin-and-connected nodes** (§5 Priority 1), starting with `navy-range-fouler-reports`
   — the strongest primary suppression document on the board, resting on one URL.
10. **Cross-domain edge sweep for the 14 under-connected hubs** (§6): `kit-green`, `kona-blue`,
    `jon-kosloski`, `jay-stratton`, `bigelow-aerospace`, `dodig-2023-109`,
    `aaro-historical-record-vol2`, `sandia`, `mit-lincoln-laboratory`, `avi-loeb`, `matt-gaetz`,
    `alexandria-ocasio-cortez`, `steven-schiff`, and the three 2025 sworn witnesses.
11. **Re-verify the 130 bot-blocked URLs via browser agent and mirror every `.mil`/`war.gov` citation
    to web.archive.org** (§7.5). Replace the two dead `dpo.tothestarsacademy.com` URLs with the SEC
    EDGAR exhibit (§7.4).
12. **New domain file: IC counterintelligence and the disinformation apparatus** (§4.5), plus the
    `PRECEDENT` extension the schema asks for (MKULTRA and the 1973 record destruction, Church/Pike,
    Iran-Contra, AEC human radiation experiments, NRO's classified existence to 1992, CIA Act §8(b)).
13. **New domain file: crash-retrieval case literature** (§4.4) — Stringfield's Status Reports, Ryan
    Wood, Kecksburg's documented records litigation, Varginha, Aztec — graded hard, with the MJ-12
    forensic discipline already established in history-1940s-1960s applied throughout.
14. **Fix the `instId`/`locId` layer** (§2): Batch A by hand (14 ids, ~270 refs), Batches B–D
    mechanically. `l-dc` alone is referenced 115 times by all 14 files.
15. **Schema-violation cleanup** (§8.3): the 2 `oversight` edges, the `cls:'entity'` node, the two
    stray cluster values, the two mis-classed `domain` nodes, the missing `nimitz-2004` node, and the
    **four competing ids for the NARA UAP records collection**.

**Also queued, below the line:** the aerospace insider / deathbed-testimony layer (§4.6) needs either
real archival work or an explicit decision to keep it thin; the Vatican strand (§4.7) is worth one
honestly graded cluster and nothing more; and the **UAP Governance Board** — named in four files,
charter located by none — should be assigned to a single owner as the most important undocumented
institution created in 2026.

---

## 10. HOW TO PICK UP A SINGLE ITEM COLD
1. Read `/root/uap-tracker/SCHEMA.md` — the editorial stance in Part 2 is not optional. Denials are
   catalogued as artifacts of concealment, with signatory and date, never as counterweights.
2. Re-run `python3 /root/uap-tracker/notes/wave2-audit/analyze.py` (and `analyze2/3/4.py`) to refresh
   dangling-id, degree, thin-node and URL inventories against the current state of `research/`.
3. Read the `notes` block for the file(s) that already touch your item — every researcher recorded
   their method constraints, their corrections to the original brief, and what they deliberately left
   thin. Several corrections are load-bearing (Yankee Blue is **not** in AARO Volume I; the operative
   Gough reversal is 6 Dec 2019 not 2021; JANAP 146(C) cites 18 U.S.C. 793/794 not 798; the priority
   investigator is **UAP Gerb**, not "UAP Herb"; AARO Vol I mentions **none** of the Kirtland/
   Bennewitz/Doty/Rendlesham/MJ-12 material).
4. Check the item against the 183 stated gaps already recorded in the 14 `gaps[]` arrays before
   opening new research — most high-value document requests are already specified there with the
   repository and the route.
5. Standing rule, no exceptions: **no invented sources, no invented URLs, no invented document
   numbers.** If it cannot be sourced it goes in `unverified[]` or becomes a Tier-3 inference with the
   reasoning stated. Fetch every URL before citing it and record the verification date.
