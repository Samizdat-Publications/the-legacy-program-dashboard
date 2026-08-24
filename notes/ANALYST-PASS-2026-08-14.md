# ANALYST PASS — cross-node traversal of the L0 model and the full board

**Method.** Loaded `data/l0-model.json` (110 L0 dossiers, 4,320 keyed connection rows, 21 authority entries, 968-node table) and `data/the-program.json` (968 nodes, 2,160 edges, 5,994 tiered claims across the entity and dossier layers, 858 timeline events) into Python and traversed rather than read. Four passes were run: (1) two-hop joins over the L0 set and over the full 968-node adjacency, filtered to pairs where neither node's text mentions the other; (2) a TF-IDF match of all 674 `openQuestions` against the full claim corpus, restricted to answering nodes that are **not** adjacent to the asking node; (3) an affiliation-overlap pass that normalised every `affiliations` string on all 279 person nodes into institution + year-span keys and flagged co-tenancies with no connecting edge; (4) a day-precision temporal-collision pass over the timeline. Seven finds survived. Each is traceable to node ids and quoted text, and each was checked against the `connections` layer first — none of them restates an existing edge.

---

## FIND 1 — John Schuessler appears twice inside the AAWSAP contract, and his node knows about neither

**Grade: STRONG**

**Nodes:** `john-schuessler`, `baass`, `operacao-prato`, `aawsap`, `kit-green`, `dird-green-clinical-medical`, `dird-anomalous-acute-and-subacute-field-effects`, `betty-cash`, `wayne-state-university`

**Evidence.**

The `baass` → `operacao-prato` connection row (type `research`) names a specific contractor deliverable and its author:

> "The AAWSAP product list in 'Skinwalkers at the Pentagon' includes the BAASS March 2009 monthly report **'The UFO Assault on Brazil with its Epicenter at Colares (1977-2003) by John Schuessler'**, the August 2009 monthly report 'Relations with South American organizations', and a July 2009 report 'Project Colares/Brazil, Outreach to South America'."

Separately, on `kit-green` (Tier 1 claim):

> "The document draws on 42 relevant cases from the peer-reviewed medical literature plus roughly 300 unpublished cases, and includes appendices titled **'Schuessler Catalog'**, 'Green Morris Cases' and 'Green-Morris ICD Diagnostics'."

And on `wayne-state-university` (Tier 1):

> "The human-effects DIRD's evidentiary base includes UFO-report catalogues and the author's own private patient files: **Appendix A is the 'Schuessler Catalog of UFO-Related Human Physiological Effects'**…"

The DIRD in question, `dird-green-clinical-medical` / `dird-anomalous-acute-and-subacute-field-effects` (DIA, Acquisition Threat Support series, 11 March 2010, produced under the AAWSAP contract with BAASS), states its purpose as:

> "Hypothesis One is that 'sufficient evidence exists from human injury / effects to reverse engineer certain aspects of the Energy / Propulsion Systems'."

The `john-schuessler` node has exactly two neighbours: `betty-cash` and `mufon`. Its dossier describes him solely as the 1981 Cash-Landrum field investigator and "the type specimen of the credentialled contractor-engineer investigator." It does not mention AAWSAP, BAASS, DIA, Kit Green, the DIRD series, or Colares. `operacao-prato` is likewise not connected to `kit-green` or to any DIRD.

**Why it matters.** The same private individual supplied material to both halves of the same $22M DIA contract in the same twelve months: the collection arm (a BAASS monthly report on the Colares wave, March 2009, while BAASS field teams were in Brazil in May and October 2009) and the analytic arm (Appendix A of the government's human-effects reverse-engineering paper, March 2010). Colares is the board's single largest documented set of UAP-attributed human tissue injury; "human effects" is one of the eleven technical areas named in the AAWSAP statement of work. This is the mechanism by which a 1981 civilian MUFON injury catalogue became the evidentiary base of a Defense Intelligence Agency hypothesis that human injury can be reverse-engineered into propulsion physics. It also sharpens the argument against `aaro-historical-record-vol1`: AARO's disposal of the record is "circular reporting from a group of individuals who believe this to be the case, despite the lack of any evidence." Here is a documented circuit — but it runs from civilian case files *into* the government product, on contract, with a named author and dated deliverables. Either reading is damaging, and neither is stated anywhere on the board.

**Would confirm:** the released text of the Green DIRD showing which cases Appendix A carries (does it include Colares / Chupa-Chupa cases?); the BAASS March 2009 monthly report itself; any BAASS subcontract or consulting instrument naming Schuessler. **Would kill it:** if "Schuessler Catalog" in the DIRD refers to a pre-1998 published compilation with no 2009-10 involvement by Schuessler, the double role collapses to a single citation and the find weakens to a bibliographic coincidence.

**Action for the board:** add edges `john-schuessler` ↔ `baass` (research/authorship), `john-schuessler` ↔ `operacao-prato`, `john-schuessler` ↔ `dird-green-clinical-medical`, `operacao-prato` ↔ `dird-anomalous-acute-and-subacute-field-effects`.

---

## FIND 2 — Sean Kirkpatrick was inside DIA for the entire life of the programme he later called the seed of the delusion

**Grade: STRONG**

**Nodes:** `sean-kirkpatrick`, `dia`, `aawsap`, `aatip`, `james-lacatski`, `dird-series`, `kirkpatrick-sciam-oped-2024`, `aaro-historical-record-vol1`

**Evidence.**

`sean-kirkpatrick`, `affiliations`:

> "Defense Intelligence Agency (2007-2016)", "Defense Intelligence Agency, chief scientist for the Defense Intelligence Directorate", "CIA / NRO (2003-2007)"

`sean-kirkpatrick`, narrative:

> "then the Defense Intelligence Agency 2007-2016 as **Chief Technology Officer, Division Chief and Defense Intelligence Officer for Scientific and Technical Intelligence**"

`sean-kirkpatrick`, Tier 2 claim:

> "He characterised the entire crash-retrieval narrative as 'a textbook example of circular reporting' sourced to 'a small group of interconnected believers' influenced by Robert Bigelow and AATIP."

`aawsap`: conceived inside DIA's Defense Warning Office by James Lacatski, solicited 18 August 2008, awarded 22 September 2008 as HHM402-08-C-0072; the 38 DIRDs are DIA "Acquisition Threat Support" series products dated 2010; AATIP ran to 2012.

`sean-kirkpatrick` adjacency: `aaro`, `aaro-historical-record-vol1`, `aaro-ornl-materials-analyses`, `anna-paulina-luna`, `avi-loeb`, `david-grusch`, `dod-sapco`, `gerb-battelle-investigation`, `hearing-2023-04-19`, `immaculate-constellation`, `immaculate-constellation-12-page-report`, `jon-kosloski`, `kirkpatrick-sciam-oped`, `kirkpatrick-sciam-oped-2024`, `marik-von-rennenkampff`, `oak-ridge-national-laboratory`, `sap-annual-report`, `shootdowns-feb-2023`. **There is no edge to `dia`, `aawsap`, `aatip`, `james-lacatski`, `baass`, or `dird-series`.** The reciprocal is also true: `dia`'s neighbour list does not contain `sean-kirkpatrick`.

**Why it matters.** The board treats Kirkpatrick's DIA years as biography and his AARO findings as institutional output, and never joins them. The join is this: the officer who wrote the government's finding that the crash-retrieval record is circular reporting traceable to AATIP held the DIA Scientific and Technical Intelligence portfolio — the same agency, in the same S&T lane, for the entire 2008-2012 lifespan of AAWSAP/AATIP and the whole production run of the 38 DIRDs. That is either (a) a disqualifying conflict, because he was investigating an office he sat inside, or (b) far more interesting, because it means AARO's founding director had contemporaneous first-hand institutional knowledge of the programme AARO characterises as misunderstood by everyone who touched it. `aaro-historical-record-vol1`'s open question — "The report does not publish the list of roughly thirty interviewees" — becomes sharper: the report's author was himself a potential Tier-1 interviewee.

Note also a data gap that probably explains why nobody drew this: **no tiered claim on the board sources Kirkpatrick's DIA tenure.** It exists only in the `affiliations` array and the free-text narrative. The claim layer never carries it, so it never entered the connection graph.

**Would confirm:** a DIA organisation chart or official biography placing the Defense Warning Office (AAWSAP's home) and the Defense Intelligence Officer for S&T in the same reporting chain, 2008-2012; any AARO recusal or ethics record. **Would kill it:** documentation that DWO and the S&T directorate were wholly separate stovepipes with no overlap in Kirkpatrick's remit.

---

## FIND 3 — `sue-gough` and `susan-gough` are the same person, and the board's denial record is split in half because of it

**Grade: STRONG** (structural / data-integrity, with substantive consequence)

**Nodes:** `sue-gough`, `susan-gough`, `immaculate-constellation`, `immaculate-constellation-12-page-report`, `yankee-blue`, `aatip`, `christopher-sherwood`, `luis-elizondo`, `aaro-historical-record-vol1`

**Evidence.** Both nodes exist, both are `person`, both are DoD/OSD Public Affairs UAP spokesperson, and both carry the affiliation string "Office of the Secretary of Defense, Public Affairs." They are non-adjacent and neither dossier mentions the other. The claim corpus mixes the two spellings for **the same statements**:

- `yankee-blue`, Tier 1: "On 1 October 2025 Pentagon spokesperson **Susan Gough** stated: 'Regarding the alleged memo: I cannot confirm the existence of any department-level memo as described in the article.'"
- `yankee-blue`, Tier 2: "A Department of Defense statement attributed to spokesperson **Sue Gough** said: 'The department is committed to releasing a second volume of its Historical Record Report…'"
- `immaculate-constellation`, Tier 2: "Department of Defense spokesperson **Sue Gough** is quoted in the written testimony: 'The DOD has no record, present or historical, of any type of SAP called "IMMACULATE CONSTELLATION."'"
- `susan-gough`, Tier 1: "The Department's June 2023 statement responding to Grusch was issued in **Gough's** name…"

The split runs through the graph. `sue-gough` has 2 neighbours (`aaro`, `immaculate-constellation-12-page-report`). `susan-gough` has 12 (`aatip`, `christopher-sherwood`, `luis-elizondo`, `reid-sap-letter-2009`, `foia-21-f-0938`, `yankee-blue`, `david-grusch`, `hearing-2023-07-26`, `elizondo-dodig-complaint-2021`, `john-greenewald`, `immaculate-constellation`, `aaro`).

**Why it matters.** Merged, this is one person issuing a documented, repeating pattern over seven years: categorical negative, then later partial reversal.

1. 13 Jun 2019 — authenticates the Reid SAP letter and says it "makes no change to previous statements."
2. 6 Dec 2019 — "Neither AATIP nor AAWSAP were UAP related," repudiating her own colleague Christopher Sherwood.
3. 21 May 2021 — partial reversal: the AATIP contract "allowed for research drawn from a wide variety of sources, including reports of UAPs."
4. Nov 2024 — "The DOD has no record, present or historical, of any type of SAP called 'IMMACULATE CONSTELLATION.'"
5. 1 Oct 2025 — "I cannot confirm the existence of any department-level memo as described" (Yankee Blue) — after which, per the board's own cited source title, the Department reopened the search.
6. 25 Feb 2026 — Volume II: "We have nothing to announce at this time," plus the 2,000-case / roughly 1,000-unanalysed disclosure.

Split across two nodes, that is two thin biographies. Merged, it is the board's single best evidentiary series on the reliability of Departmental categorical negatives, and it directly supports the `aaro-historical-record-vol1` argument that a "no evidence found" from OSD Public Affairs is not a statement about the world. It also affects the `authority` table's `publicRecord.denialsIssued` arithmetic wherever Gough is counted.

**Would confirm:** a single DoD press-office roster entry. This is effectively already confirmed by the board's own quotations; the only open question is which spelling is canonical (contemporaneous DoD statements use "Sue Gough"; FOIA 21-F-0938 correspondence uses "Susan Gough").

**Action:** merge to one node, re-point all edges, re-run the denial counts.

---

## FIND 4 — James Clapper is the only person on the board who held authority over both of DIA's anomalous-phenomena programmes, and terminated or refused protection to both

**Grade: STRONG**

**Nodes:** `james-clapper`, `stargate-program`, `sun-streak`, `dia`, `aawsap`, `depsecdef-sap-packet-2009`, `waived-usap`, `harry-reid`

**Evidence.**

`james-clapper`, `affiliations`: "**Director, DIA (1992-1995)**", "Under Secretary of Defense for Intelligence (2007-2010)", "Director of National Intelligence (2010-2017)".

`stargate-program`, narrative:

> "moved to **DIA's Scientific and Technical Intelligence Directorate** as SUN STREAK in late 1985, and was consolidated as STAR GATE in 1991… **James Clapper, later Director of National Intelligence, led the project in the 1990s**… In 1995 CIA commissioned the American Institutes for Research to evaluate the programme… the official finding was that remote viewing information 'is vague and ambiguous'."

`james-clapper` → `waived-usap` (type `denial`):

> "Clapper as Under Secretary of Defense for Intelligence recommended against establishing a special access program in response to Senator Reid's June 2009 request."

`sun-streak` → `dia` (funding edge note):

> "**DIA's prior experience running an unacknowledged programme in a ridiculed domain is the institutional precedent for its 2008 AAWSAP contract.**"

`james-clapper` has exactly three neighbours: `depsecdef-sap-packet-2009`, `stargate-program`, `waived-usap`. **There is no edge `james-clapper` ↔ `dia`**, and the Clapper narrative never mentions his DIA directorship or STAR GATE. The `stargate` edge note says only "Clapper is recorded as a project leader in the 1990s."

**Why it matters.** The board already asserts, in the `sun-streak` → `dia` note, that STAR GATE is the institutional precedent for AAWSAP. It does not notice that the *same official* sits at the terminal decision point of both. As DIA Director 1992-1995 he held the agency through STAR GATE's final years and its 1995 termination and transfer; as USD(I) in November 2009 he recommended against compartmenting DIA's successor effort. Two DIA anomalous programmes, seventeen years apart, one officer, the same outcome both times: no protection, no continuation, official finding of insufficient merit. The `waived-usap` dossier's open question — "Whether any of the eight members has ever been briefed on a UAP-related waived SAP" — has a corollary the board never asks: Clapper is the one living official who held both DIA's institutional memory of an unacknowledged anomalous programme *and*, later, USD(I) waived-SAP determination authority, and by the board's own narrative "has never been asked on the record about the memorandum bearing his recommendation."

**Would confirm:** the AIR / 1995 STAR GATE termination file showing Clapper's signature or approval chain; a DIA organisational history placing STAR GATE under the Director's cognizance 1992-1995. **Would kill it:** if "led the project in the 1990s" refers to a narrower role that predates or postdates his directorship, the two-programme symmetry weakens (the SAP refusal stands regardless).

---

## FIND 5 — The board's own authority table names Christopher Mellon as holder of the waived-SAP and carve-out determination, then disconnects him from every SAP node on the map

**Grade: STRONG** (on the contradiction) / **PLAUSIBLE** (on the Wilson overlap)

**Nodes:** `christopher-mellon`, `thomas-wilson`, `wilson-davis-memo`, `carve-out`, `waived-usap`, `waived-sap-notification-group`, `dod-sapco`, `usc-10-119`

**Evidence.**

`authority["christopher-mellon"]`:

> `"authority": "Co-equal approval authority for SAP designation and carve-out provisions; the officer to whom the waived-SAP reporting determination belongs."`
> `"instruments": ["DoDD 5205.07 (12 September 2024)", "10 U.S.C. 119"]`, `"tense": "held"`, `"weight": 2`

`christopher-mellon`, `affiliations`: "**Deputy Assistant Secretary of Defense for Intelligence (1999-2002)**", "Minority Staff Director, Senate Select Committee on Intelligence", "To The Stars Academy (2017-2021)", "The Sol Foundation (advisory)", "Disclosure Foundation".

`thomas-wilson`, `affiliations`: "Joint Staff J-2 (1994-1997)", "**Defense Intelligence Agency (Director, 1999-2002)**". His narrative records the alleged 1997 approach and refusal, and the Davis notes of 16 October 2002.

`christopher-mellon` adjacency: `aaro-historical-record-vol1`, `anna-paulina-luna`, `david-grusch`, `fy2026-ndaa-uap-provisions`, `gerb-hidden-wing`, `hearing-2024-11-13`, `navy-flir-gimbal-gofast-videos`, `nyt-2017-12-16`, `pursue-programme-2026`, `pursue-releases`, `ttsa`, `uap-task-force`. **No edge to `carve-out`, `waived-usap`, `waived-sap-notification-group`, `dod-sapco`, `usc-10-119`, `thomas-wilson`, or `wilson-davis-memo`.**

`carve-out` open questions include: "Is there any record of a carve-out provision ever being denied or revoked by a Secretary or Deputy Secretary of Defense?" and "Who are the Cognizant Security Offices designated to inspect carved-out programs in lieu of DCSA, and are any of them staffed by the contractor's own personnel?"

`wilson-davis-memo` open question: "Whether Kostelnik, Ward, Daly, Gansler or Kaminski have ever been asked about the memo's assertions on the record or under oath."

**Why it matters.** Two things, one hard and one soft.

*Hard:* the `authority` layer and the `connections` layer contradict each other. The board asserts that Mellon held the exact determination authority that `carve-out` and `waived-usap` record as unanswerable, and then wires him only to the advocacy and disclosure clusters. He is the board's most prominent living critic of the Department's UAP posture and, on the board's own account, one of the very few people who sat in the chair that could answer the structural questions the board has flagged as open. Nobody has recorded whether he has ever been asked.

*Soft:* his DASD(I) tenure (1999-2002) is exactly coterminous with Thomas Wilson's DIA directorship (1999-2002), the window bracketing the board's most specific custody allegation — Wilson's alleged 1997 approach and refusal, and the Davis notes of 16 October 2002. The board has never joined the OSD intelligence-policy chair to the DIA chair for those years. Mellon's own dossier does not mention Wilson; Wilson's node has only two neighbours (`disclosure-project`, `wilson-davis-memo`).

**Would confirm:** any on-record question put to Mellon about waived-SAP or carve-out determinations from his DASD(I) period; any statement from Mellon about the Wilson episode. **Would kill it:** if DASD(I) in 1999-2002 held no SAP determination role — in which case the *authority table entry itself* is the error and should be corrected, which is equally a finding.

---

## FIND 6 — SRI International administered JASON while running the CIA psychoenergetics programme, and the board has no edge between them

**Grade: PLAUSIBLE**

**Nodes:** `jason-advisory-group`, `sri-international`, `stargate-program`, `harold-puthoff`, `russell-targ`, `mitre-corporation`, `ida`

**Evidence.**

`jason-advisory-group`, narrative:

> "Established in 1960, it was administered by the Institute for Defense Analyses from 1960 to 1973, **then by SRI International**, and since 2002 by MITRE… If a government body ever commissioned a genuinely independent technical assessment of recovered material, JASON is the body it would go to."

`sri-international`, narrative:

> "**from 1972 its Radio Physics Laboratory hosted Harold Puthoff and Russell Targ's psychoenergetics programme**, funded initially by CIA's Office of Technical Service and later by Army INSCOM and DIA under successive codenames… SRI is where the template of government-funded, privately-housed, unacknowledged anomalous research was proven to work."

`jason-advisory-group` adjacency: `dird-high-frequency-gravitational-wave-communications`, `doe`, `ida`, `mitre-corporation`. `sri-international` adjacency: `grill-flame`, `harold-puthoff`, `kit-green`, `russell-targ`, `stargate-program`. **No edge between them, and neither narrative mentions the other.**

**Why it matters.** For roughly 1973-1990 one nonprofit institute simultaneously (a) administered the United States government's most elite standing independent scientific advisory panel and (b) housed a compartmented, unacknowledged CIA/DIA anomalous-phenomena programme. The board's argument about the FFRDC and nonprofit layer is that independent scientific judgement in this domain is always contractor-administered and therefore never independent. This is the strongest single instance of that thesis available on the board and it is not stated: the institution that would have convened any independent assessment of the phenomenon was, at the same time, the phenomenon's classified contractor. It also reframes the JASON node's own point — the board notes JASON is the body a government would go to for an independent assessment; from 1973 the "independent" administrator had a standing financial interest in the subject.

**Would confirm:** the SRI-JASON administration contract dates; any record of JASON being tasked on UAP or psychoenergetics during the SRI period, or of a firewall between SRI's JASON administration and its Radio Physics Laboratory. **Would kill it:** if the SRI administration period was short (say 1973-1976), the overlap narrows and the point weakens to a coincidence of corporate host.

---

## FIND 7 — The connections layer already answers the AAWSAP dossier's own open question about the monthly status reports

**Grade: STRONG** (small, clean, immediately actionable)

**Nodes:** `aawsap`, `baass`, `operacao-prato`

**Evidence.**

`aawsap` open question:

> "The full deliverable inventory. Thirty-seven of thirty-eight DIRDs are public; the Ten Month Report, the Comprehensive Integrated Threat Assessment, **and the monthly status reports are not.**"

`baass` → `operacao-prato` connection note:

> "The AAWSAP product list in 'Skinwalkers at the Pentagon' includes the **BAASS March 2009 monthly report** 'The UFO Assault on Brazil with its Epicenter at Colares (1977-2003) by John Schuessler', the **August 2009 monthly report** 'Relations with South American organizations', and a **July 2009 report** 'Project Colares/Brazil, Outreach to South America'."

**Why it matters.** The dossier layer records the monthly status reports as wholly unrecovered. The connections layer, elsewhere on the board, carries three of their titles, one author attribution, and three dated months — enough to serve a FOIA request or a congressional production demand with specificity rather than a category. This is a direct, targetable partial answer to a live open question, produced by nothing more than reading two layers of the same board against each other. It also indicates the failure mode to watch for across the rest of the model: high-value facts are being deposited in edge `note` fields and never promoted into the dossier claim arrays where the open-question logic can see them.

**Action:** promote the three report titles into `aawsap` dossier claims with the Lacatski / Kelleher / Knapp citation, and narrow the open question to the reports still unaccounted for.

---

## Also flagged, below the bar for a numbered find

- **`jon-kosloski` ↔ `nsa` is missing.** Kosloski's affiliations include "National Security Agency, senior research scientist (until 2024)"; his node has no edge to `nsa`. `nsa` is the board's most absolute FOIA-withholding node — the Yeates affidavit in *CAUS v. NSA* conceded the Agency held classified UFO documents whose number and nature could not be described even to a federal judge in open session — and `nsa` **is** connected to `nara-uap-collection`, meaning it now carries a sections 1841-1843 transfer obligation into RG 615. The current AARO Director is a 2024 alumnus of that agency. PLAUSIBLE; worth an edge and a question, not a claim.
- **`kirk-mcconnell`** spent 37 years on SASC, HPSCI and SSCI staff to March 2024 and now writes Sol Foundation policy briefings arguing Congress should pay witnesses. He was on committee staff through the December 2023 FY2024 NDAA conference. `uapda-2023`'s open question — "Which members or agencies asked for the Review Board and eminent domain sections to be struck… and in what written form was the request made?" — is a question a professional staffer of that period could answer or narrow. His node has two neighbours and connects to none of the legislative nodes. PLAUSIBLE.
- **`mike-turner` and Wright-Patterson.** Turner is the member named as demanding the eminent domain clause and the Review Board's subpoena power be struck, and `l-wright-patterson` is the board's principal custody location. The board records Turner only as "R-OH" and records WPAFB as sitting "immediately east and northeast of Dayton, Ohio." **The board does not contain Turner's district number or any Dayton link, so nothing is asserted here.** SPECULATIVE. The single fact that would settle it: Turner's congressional district and its relationship to Greene and Montgomery Counties, from the Congressional Directory. If it lands, the shape is "a denial issued by someone with a stake in what they are denying" and it belongs in the record; if it does not, it should be written off explicitly so nobody chases it again.
- **Internal contradiction to resolve.** `immaculate-constellation`'s open questions state: "Claims elsewhere that former AARO director Sean Kirkpatrick denied the programme could not be verified against a primary source for this dossier and are not asserted here." But the `dod` → `immaculate-constellation-12-page-report` denial edge note asserts flatly: "Pentagon spokesperson Sue Gough stated DoD has 'no record' of such a program; **Kirkpatrick also denied it.**" Two layers of the board disagree about whether a named official issued a denial. Pick one.

---

## What I looked for and did NOT find

Recorded because a negative on an obvious hypothesis is worth as much as a positive.

1. **Temporal collisions across unrelated strands.** Ran every day-precision timeline event (640 of 858) against every other within a 21-day window, filtered to non-adjacent nodes. Essentially all 2,884 hits are the *same* event recorded from different strands (Roswell, 8 July 1947, five ways; Blue Book termination, 17 Dec 1969, three ways; the NYT story, 16 Dec 2017, six ways). No genuine cross-strand coincidence survived. The one near-miss worth naming and dismissing: FASAB issued the **SFFAS 56 exposure draft on 14 December 2017, two days before the New York Times broke AATIP** (`sffas-56`, `nyt-2017-12-16`). Tempting, but the board's own `sffas-56` narrative records that DoD identified the need for the standard in **August 2016**, sixteen months earlier, which supplies an innocent explanation and no mechanism links the two. Not a find. Recorded so it is not re-discovered.
2. **Two-hop joins across the L0 set.** Only 14 non-adjacent L0 pairs share three or more neighbours, and 12 of the 14 are legislative or AARO-reporting nodes that are near-duplicates of each other (`uapda-2023` / `ndaa-fy2022-sec-1683`, `aaro-fy2024-annual-report` / `pursue-releases`, and so on). The L0 layer is too densely and correctly wired for this technique to yield much, which is a compliment to the board. The one productive pair, `nids` / `operacao-prato` sharing `aawsap`, `baass` and `jacques-vallee`, is what led to Find 1.
3. **Open questions answered by distant nodes.** 163 of 674 open questions had a high-scoring answer from a non-adjacent node, but on inspection nearly all are the *same claim* restated on a neighbouring node (the "IC Controlled Access Program expanded in 2021" text appears verbatim on five nodes; the GAO / RAAF records-destruction finding on six). The board's redundancy is high and its open questions are, with the exceptions above, honestly open. **The most-repeated open question on the entire board — the identity of the 2021 IC Controlled Access Program — is genuinely unanswered by any node.** Nothing on the map names it, names the official who expanded it, or names the official who disestablished it.
4. **A funding path through an unconnected entity.** Traced all 64 funding edges. Every dollar path on the board is already wired: Reid / Inouye / Stevens to appropriation to DIA to BAASS; Rockefeller to the Initiative; NNSA sole-source to MITRE to JASON; Battelle to ORNL to the specimen; IR&D to the primes. The one genuinely dangling money node is **`radiance-technologies`** (roughly $2.6bn in prime obligations since FY2008, one edge, to `dia`), and its own dossier is explicit and honest that no personnel record has been located. It should stay flagged as a research gap, not promoted.
5. **A denial issuer with an undisclosed holding.** Crossed all 175 denial edges against the affiliation table. The board has already drawn the two best instances itself (Kirkpatrick to ORNL / UT-Battelle post-employment; Clapper to DNI nine months after the SAP refusal). The residual case is Mellon (Find 5), which is the inverse shape — an authority holder on the *disclosure* side whose own prior authority nobody has interrogated.
6. **Two people in the same room at the same time, unremarked.** The affiliation-overlap pass produced more than 40 co-tenancy groups, but almost all are committees and boards whose members are correctly treated as a set (Task Force on the Declassification of Federal Secrets, UAP Science Advisory Council, Sol Foundation, NIDS, COMETA). The only co-tenancies where the board plausibly missed something are the DIA group — `sean-kirkpatrick` (2007-2016), `jay-stratton` (2000s-2021), `thomas-wilson` (Director 1999-2002), all mutually non-adjacent — which produced Finds 2 and 5. `jay-stratton` and `sean-kirkpatrick` overlapped inside DIA for nine years and later ran, respectively, the UAP Task Force and the office that absorbed it; neither dossier mentions the other. That one is recorded here as an observation rather than a find, because the board gives no role detail that would make the overlap operationally meaningful — but it is the first thing to test if a personnel record surfaces.
