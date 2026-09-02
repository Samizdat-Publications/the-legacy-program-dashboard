# Michels corpus triage, group 2 (lead maps 06-10)

**Scope.** `research/leads/michels-corpus-06.md` through `-10.md` and the 294 names in
`research/leads/michels-absent/group-2.tsv`. Nothing here is board content and nothing here
is asserted as true. Every row records what a named speaker said, and names the record that
would have to be opened before any of it could become a node. `CLAUDE.md` section 2 governs.

**Citation format.** `NN f0X TS` = lead map `michels-corpus-NN.md`, its file 0X, timestamp as
that map prints it. Where a name recurs in more than one map every occurrence is listed,
because recurrence across different guests is the signal that matters here.

**Counts.** A 21 rows / 35 names. B 100 names. C 19 rows, touching 4 names from the list plus 15
existing nodes. D 155 names in four groups. 35 + 100 + 4 + 155 = 294, checked
programmatically against the TSV.

**Two things found while checking the list against `data/the-program.json`.**

1. **Fourteen ABSENT rows are false.** The cross-check was given bare acronyms and caption
   spellings; the board carries the expanded label. `CIA` is `cia` / Central Intelligence
   Agency, `DIA` is `dia`, `NSA` is `nsa`, `NRO` is `nro`, `SRI` is `sri-international`,
   `Sky Watchers` is `skywatcher`, `David Grush` is `david-grusch`, `Stephen Greer` is
   `steven-greer`, `Danny Sheehan` is `daniel-sheehan`, `Wilbur Smith` is `wilbert-smith`,
   `Bob Salas` is `robert-salas`, `Carl Nell` is `karl-nell`, `MK-Ultra` is carried by
   `hearing-2026-06-30` and `tl-mkultra-hearing`, and `US Army INSCOM` is already in
   `stargate-program.desc`. All fourteen are in section D group 1. **A false ABSENT is the
   expensive error the README names**, and this batch produced fourteen of them from one
   cause: the candidate list holds acronyms, the board holds names. Worth fixing in
   `corpus_crosscheck.py` before the next wave rather than re-finding it per group.
2. **What is genuinely missing is larger than what is falsely missing.** The board has no
   node for the **Atomic Energy Commission**, none for the **National Security Council**,
   none for **TRW**, none for **Eisenhower**, and none for the Army office named on the face
   of a document the board already quotes. Those are section A.

---

## A. Document-backed candidates

Ranked. Rows 1 to 9 would change the board's argument; rows 10 to 21 would extend it.

| # | Name | Class | The record that would justify it | Where to look | Why on THIS board | Lead map |
|---|---|---|---|---|---|---|
| 1 | **Atomic Energy Commission** | institution | Atomic Energy Act of 1946 (P.L. 79-585) and of 1954 (P.L. 83-703); AEC organisational records for the **Division of Military Applications** and the Albuquerque Operations Office | NARA RG 326; DOE OpenNet; the two statutes at govinfo | The board argues that recovered material was safer in a contractor's hands than in an acknowledged government programme, and every version of that argument routes through born-secret classification. The instrument is a **statute**, not testimony, and the board currently has `nnsa` and `oak-ridge-national-laboratory` with nothing above them. Four separate guests across four maps put the AEC at the custody point | 06 f04 1:16:46; 08 f04 1:05:41; 09 f02 0:33:21, f03 1:12:28; 10 f04 0:50:15 |
| 2 | **Bluegill Triple Prime** | event | Defense Nuclear Agency report **DNA 6040F**, Operation DOMINIC I 1962, and DNA 6039F for Operation FISHBOWL; the 1998 declassification review of the "Kettle 1" film; the 2023 mandatory declassification review for "Kettle 2"; the **RC-135S Cobra Ball** aircraft that filmed both, per USAF unit records | DTIC and archive.org DTIC mirror for the DNA reports; DTRA FOIA/MDR office; ISCAP for the MDR appeal | The single strongest recurrence in the whole slice: four guests in four maps, none sharing a source, converge on one dated shot, 26 October 1962, Johnston Atoll. The underlying test documentation is fully public and none of it is AARO or DoD press material, so the tier is not capped. The claim to be tested is narrow and checkable: whether the film exists, what the review removed, and whether the ship's log records what is said of it | 06 f01 1:58:08, f04 1:27:17; 08 f04 1:16:49; 09 f02 0:33:21, f03 0:58:43; 10 f04 0:51:04 |
| 3 | **Lawrence Preston Gise** | person | AEC Albuquerque Operations Office appointment and organisational records; the DOE Albuquerque records series | NARA RG 326 (Albuquerque); DOE OpenNet | The named custodian in every version of the Bluegill debris chain, in four maps, from four guests who are not each other's sources. His office is a matter of record; only the briefing is testimony. Establishing which he held and when separates the two | 06 f04 1:16:46; 08 f04 1:22:20; 09 f02 0:33:21, f03 1:12:28; 10 f04 0:52:53 |
| 4 | **Harald B. Malmgren** | person | Senate confirmation as Deputy Special Representative for Trade Negotiations, 1972, with ambassadorial rank; Executive Office of the President staff records; his February 2025 obituary | Congressional Record and Senate Executive Journal at govinfo; Ford, Nixon and JFK library staff files | The whole Gise-Bissell-Los Alamos chain rests on one man's late-life account, and his public service record is entirely open. It settles whether he was where he says he was in October 1962 without touching the UAP claim at all. **Name resolution is mine:** the corpus corrupts him five ways (`Malmgram`, `Momgren`, `Herald Namgren`, `Malmaren`, `Mongrin`); the working form is Harald B. Malmgren | 06 f01 1:58:08, f04 1:24:42; 08 f04 1:22:20; 09 f03 throughout; 10 f04 0:52:53 |
| 5 | **TRW Inc.** | institution | The 1997 BDM International acquisition and the Northrop Grumman acquisition of TRW completed 11 December 2002, both on the public filing record | SEC EDGAR (Schedule TO, Form S-4, and the TRW 10-K series) | The board added `bdm-international` on 30 August **specifically** to reach `northrop-grumman`, and the middle link of that chain is not on the board. Without TRW the edge is an assertion; with it, it is a corporate record. Cheapest structural win in the slice | 07 f01 0:45:57, 1:54:44 |
| 6 | **Richard M. Bissell Jr.** | person | The CIA's own declassified in-house history of overhead reconnaissance (Pedlow and Welzenbach, released 1998), which documents the site selection that became Groom Lake | CIA reading room / CREST; his papers | The board's Nevada material has no documented origin point. Bissell is where the site's real record begins, which is the T1 anchor that a T3 corridor needs. Three maps put him at the briefing end of the 1962 chain as well | 06 f04 1:30:39; 09 f02 0:34:13, f03 1:14:12; 10 f04 1:59:40 |
| 7 | **John A. McCone** | person | AEC chairman 1958-60 and DCI 1961-65; the McCone memoranda in FRUS 1961-63; his own AEC and CIA personnel record | NARA RG 326 and RG 263; FRUS at history.state.gov | The AEC-to-CIA personnel continuity is a structural claim the board can test from published record with no witness involved, and it is the claim batch 10 is built on. He is already the addressee of the disputed JFK letter the board carries, and is named in `aaro-historical-record-vol1.desc` without a node | 06 f01 1:59:02; 07 f02 0:25:06; 09 f01 1:34:10; 10 f04 0:50:15 |
| 8 | **US Army Foreign Technology Division, Office of the Chief of Research and Development** | institution | Corso's DA Form 66, **already on this board and already quoted in `philip-corso.narrative`**, which names the office on its face; OCRD annual historical summaries | NARA RG 319; US Army Center of Military History | The board quotes a form naming an office it has no node for, so the three months Corso spent as its chief hang on prose. The office is the hinge of the entire distribution-conduit argument and it is documented independently of Corso | 06 f04 1:05:21; 07 f01 0:16:28, 0:18:03 |
| 9 | **Lt. Gen. Arthur G. Trudeau** | person | His papers at the US Army Heritage and Education Center; the OCRD historical summaries for 1958-62; his published memoir | USAHEC, Carlisle Barracks; NARA RG 319 | The only man who could confirm or destroy the Corso conduit from inside the Army's own record, and the one the corpus names as Corso's superior. If the conduit existed, it existed under him | 07 f01 0:16:28, 0:18:50 |
| 10 | **Walter Bedell Smith** | person | Two CIA memoranda described in the corpus: a 1952 memo on the flying-saucer situation as a national-security risk, and a memo to the director of the Psychological Strategy Board citing over 1,500 reports with 20 per cent unexplained | CIA reading room / CREST, DCI files 1950-53 | These are the documents that produced the Robertson Panel, which is already a node (`robertson-panel`). A DCI writing that the phenomenon is to be operationalised is a first-party record of intent, not a claim about what happened. Two maps, two unrelated guests | 06 f04 1:09:25; 09 f02 0:21:37 |
| 11 | **Psychological Strategy Board and its successor, the Operations Coordinating Board** | institution | The Truman directive establishing the PSB, 4 April 1951; NSC 5412; PSB and OCB records | Truman Library and Eisenhower Library; NARA RG 59 lot files | Corso's DA Form 66, which the board already quotes, places him on the **OCB** from 24 February 1954 to 1957. The board carries the fact and not the office. The corpus independently puts Gordon Gray, **Charles Douglas Jackson** and Corso there together | 06 f04 1:09:25; 09 f02 0:19:04, 0:22:32 |
| 12 | **Gordon Gray** | person | The published transcript of the AEC personnel security board he chaired, *In the Matter of J. Robert Oppenheimer* (USGPO 1954, full text released 2014); PSB director records | Truman and Eisenhower libraries; DOE OpenNet for the 2014 release | The clearest fully documented instance on this board of the mechanism it argues about: a clearance adjudication used to remove a scientist from a compartment. Nothing about it requires MJ-12 | 06 f04 1:09:25; 09 f02 0:22:32 |
| 13 | **Avco Corporation and the 19 September 1962 Atlas 8F / Mark IV re-entry vehicle test report** | document | The USAF/NASA post-flight report on the Atlas 8F test at Cape Canaveral / the Atlantic Missile Range, said to record objects of unknown origin and identity pacing the vehicle | DTIC; Air Force Space and Missile Systems Center historical office; NASA Technical Reports Server | If the language is there it is a first-party government test report describing an unidentified object, which is a T1 document rather than a witness. Two maps describe the same dated test, one naming the contractor and one naming the range | 08 f04 1:25:11; 09 f03 1:02:19 |
| 14 | **Defense Special Weapons Agency** | institution | The 1998 declassification review that sanitised the "Kettle 1" film under **Byron L. Ristvet**; the 2023 MDR to which DOE reportedly answered that "Kettle 2" cannot be located | DTRA FOIA and MDR office (DSWA became DTRA in 1998); ISCAP | A named official, a named review, a named missing film. This is the board's records-custody argument in its most checkable form, and it has a docket rather than a witness | 09 f03 1:06:08, 1:07:00 |
| 15 | **Ansel E. Talbert, "Conquest of Gravity" series, New York Herald Tribune, November 1955** | document | The published series itself | Library of Congress newspaper microfilm; ProQuest Historical Newspapers | **This addresses a named section E exclusion.** `CANDIDATES-2026-08-30` left out the 1956 "Electrogravitics Systems" report because a WorldCat search returns nothing, which leaves the electrogravitics thread with a hole exactly where `thomas-townsend-brown` was added. Talbert's series is dated, attributed and locatable and would carry the contemporaneous press record without the unlocatable report | 09 f02 0:30:31 |
| 16 | **Nikola Tesla, and the January 1943 Office of Alien Property custody of his papers** | event | The Office of Alien Property custody record and the technical review by **John G. Trump**; the FBI Tesla file released 2016 | vault.fbi.gov; NARA RG 131 (Office of Alien Property) | A documented federal seizure and technical evaluation of a private inventor's papers is this board's custody argument in its earliest verifiable form, and it is entirely open record. The corpus also supplies its own correction: the speaker disputes the claim that everything was taken, and the file supports him | 08 f04 (Tesla, McConnell); 09 f03 (John Trump) |
| 17 | **Center for Naval Analyses** | institution | The OSD annual FFRDC Master List and CNA's Navy sponsoring agreement | OSD (R&E) FFRDC listings; USAspending | The board carries `mitre-corporation`, `rand-corporation`, `ida` and `aerospace-corporation` and has a whole `d-ffrdc` seam. CNA is the one named in the corpus that is missing from the set. Small, clean, completes an argument the board already makes | 08 f03 1:24:19 |
| 18 | **Lt. Gen. Alfred D. Starbird** | person | DNA 6040F naming him Commander, Joint Task Force 8 for Operation DOMINIC; **William E. Ogle**'s published DOE history *An Account of the Return to Nuclear Weapons Testing by the United States after the Test Moratorium 1958-1961* (DOE/NV-291) | DTIC; DOE OpenNet / Nevada Field Office | The two men who can date and place the Bluegill account against a published DOE narrative rather than against a podcast. Ogle's report is a real openable document with a report number | 09 f03 1:11:32 |
| 19 | **31st Marine Expeditionary Unit, 2009 deployment / Operation Ketsana** | event | The 31st MEU command chronology for 2009; **USS Denver** deck logs | Marine Corps History Division (command chronologies); NARA RG 24 for the deck logs | The most falsifiable item in the whole slice. Herrera's account either matches his unit's own chronology and the ship's logs or it does not, and no interested party controls either record. It also tests nothing about the craft, only about where the unit was, which is why it is worth doing first | 08 f03 0:05:26, 0:05:43 |
| 20 | **Dr. Eric A. Walker** | person | Penn State University Archives, Eric A. Walker Papers; Research and Development Board committee records | Penn State Special Collections; NARA RG 330 | A real and distinct figure who connects to `research-development-board`, added on 30 August. The corpus flags, in two maps, that he is being confused with `eric-wang`, a node the board already carries. The board should own the distinction rather than inherit the conflation. See section C row 2 | 07 f01 0:28:38, 1:32:41; 09 f02 0:04:25 |
| 21 | **STAR GATE session record, the 1979 Soviet submarine report (Joseph McMoneagle, caption form `Joseph McMonagle`)** | document | The declassified STAR GATE collection, including the session the speaker identifies as TK-089, and the NRO tasking said to follow it 114 days later | CIA reading room, STARGATE collection | A documented instance of the board's oversight argument running the other way: an analyst (**Robert Gates**) rejecting a product that senior political will pushed forward anyway. The programme is already a node; the session record is not, and it carries an identifier | 07 f03 1:05:33, 1:08:09, 1:09:59 |

---

## B. Needs a document

Research questions, not candidates. 100 names. What is claimed, and what would settle it.

### B1. Offices and units named as structure

| Name | Claimed | What would settle it | Lead map |
|---|---|---|---|
| **NSC**, **303 Committee**, **40 Committee**, **US Space Council** | Offered as the plausible real institutional lineage in place of MJ-12 | FRUS 1964-68 vol. XXXIII and Church Committee Book IV both describe these bodies by name and charter. **Strongest item in B**; it is A-grade sourcing attached to a claim no document has yet been asked to test | 07 f01 1:56:31; 09 f02 0:50:32, f01 2:16:23 |
| **Army Interplanetary Phenomenon Unit** | Existence confirmed to William Steinman in 1986-87; records said to have gone to the Air Force in 1958 | The Army response letter itself, and an INSCOM FOIA for the 1958 transfer accession | 07 f01 0:16:28 |
| **Intelligence Support Activity**, **JSOC** | Named as performing crash retrieval alongside CIA Office of Global Access | Unit lineage and organisational records at the Center of Military History; JSOC activation records 1980 | 07 f01 0:43:24 |
| **Office of Naval Research** | Publishing a human sixth-sense study 2011-12 | The ONR award record on USAspending and the published paper | 07 f01 0:34:21 |
| **CIC (Army Counter Intelligence Corps)** | Kissinger's unit, placed inside Nazi-technology exploitation | CIC personnel and unit records, NARA RG 319 IRR | 09 f02 0:09:40 |
| **Church Committee**, **Frank Church** | Cited as the precedent for a real congressional accounting | Senate Report 94-755, six books, fully published. Near-A; left here because the board's use for it is comparative rather than evidentiary | 08 f04 1:43:36 |
| **NACA**, **National Advisory Committee for Aeronautics** | Doolittle said to have chaired it after investigating the Swedish ghost rockets | NACA annual reports name their chairmen; this is checkable in an afternoon and the corpus itself doubts it | 08 f04 0:37:54 |
| **Bureau of Indian Affairs** | Held a cover contract for a retrieval team near White Sands | FPDS / USAspending contract search against BIA and the named sovereign nation | 06 f01 0:32:53 |
| **UFO Working Group**, **Golden Age of Army R&D**, **Zodiac**, **MX Missile programme**, **Tactical Mobile Robotics programme** | Programme names attributed to Corso, Stubblebine, TRW and DARPA | Corso's unpublished manuscript for the first two; a DARPA programme-records FOIA for the last two. Zodiac traces only to a 1998 magazine story | 07 f01 0:45:57, 0:00:47, 1:53:48; f03 1:16:35; f04 2:12:54 |
| **Operation Laser Strike** | Real 1997 anti-narcotics operation, setting for the Peru account | SOUTHCOM and JIATF historical records | 07 f01 0:04:50 |
| **Gallagher Amendment** | A 2023 whistleblower provision with a failed 2024 amnesty and eminent-domain clause | The board already carries `uapda-2023` and `uapda-sec-9010-eminent-domain`; reconcile the speakers' account against the enacted text | 08 f03 0:04:32, f04 1:34:27 |
| **Project VASCO**, **ExoProbe**, **European Crash Retrieval Initiative** | Villarroel's own projects | Published papers exist for VASCO; the other two are self-described | 07 f02 0:15:11, 0:27:35, 0:42:02 |
| **Above Black**, **Dan Sherman** | NSA "human antenna" programme, Project Preserve Destiny | His DD-214 and any NSA organisational record; the book is published and self-sourced | 07 f01 0:13:06 |

### B2. Contractors and laboratories

| Name | Claimed | What would settle it | Lead map |
|---|---|---|---|
| **Bell Labs** | Corso's conduit for Roswell material into Kevlar, lasers, the transistor and fibre optics | AT&T Archives laboratory notebooks for each named invention. The speaker himself says he finds no gap in the conventional record | 06 f04 1:06:09; 07 f01 0:24:35 |
| **Southwest Research Institute** | 45 to 50 per cent CIA funded; analysed an implant sliver | SwRI federal award record on USAspending and its IRS Form 990. No report number is given for the analysis | 06 f02 1:28:16 |
| **Mission Research Corporation**, **Draper Labs** | Named as employers only | Corporate record; no claim attaches | 08 f01 0:37:22; 07 f04 1:16:00 |
| **Vought Aerospace**, **LTV** | Built flying saucers for Wright-Patterson in the 1940s-50s | The V-173 airframe survives and is accessioned; the programme was a **Navy Bureau of Aeronautics** contract, not an Air Force one, so the speaker's framing is probably wrong at the sponsor. NASM and BuAer contract records settle it | 10 f04 1:10:12 |
| **Floyd Odlum** | Covert transfer of Townsend Brown IP to Northrop via a RAND visit | Atlas Corporation and Convair corporate records; RAND's own visitor and contract record | 07 f01 1:01:32 |
| **SIAI Marchetti** | Hangars where the alleged 1933 Magenta craft was taken | Italian corporate and Air Ministry records; see B4 | 09 f03 1:39:28 |
| **Burkhard Heim** | A Martin Corporation / RIAS contractor before the Lockheed merger | The board now carries `rias-inc`; its participant and publication lists would show him or not | 06 f03 (Rossi) |
| **Lee Hively** | Godfather of extended electrodynamics; cut off contact and invoked a Navy press office | ORNL publication and employment record. The board carries `oak-ridge-national-laboratory` | 06 f03; 08 f04 |
| **Larry Smalley** | Co-credited on a 2004 NASA patent for an asymmetric barrel capacitor | USPTO assignee search on NASA and Smalley. No number given, which is the whole problem | 06 f03 0:29:39 |
| **Jack Parsons**, **John Mulholland**, **John Pina Craven** | JPL founder, a CIA-contracted magician, and the Navy Special Projects Office chief scientist cited on covert underwater retrieval | Mulholland's manual was declassified and published in 2009 and is a real record; Craven's Deep Submergence Systems Project has a documented Navy record and is the nearest real analogue to the retrieval methodology this board tracks; Parsons carries no programme claim here | 08 f02 |

### B3. People inside the structure, on testimony only

| Name | Claimed | What would settle it | Lead map |
|---|---|---|---|
| **Dwight Eisenhower** | An ET meeting at Muroc; the speaker self-corrects between 1954 and 1956 in one sentence | Presidential daily diary, Eisenhower Library, for both candidate dates. **The board has no Eisenhower node at all**, which is a gap independent of this claim | 09 f01 3:29:00 |
| **Donald Menzel**, **Don Menzel**, and with him **Fred Whipple** and **Halton Arp** as the Harvard and cosmology context | Ordered destruction of Harvard's 1952-flap plates; corroborated in Dorrit Hoffleit's memoir | Hoffleit's memoir is published; the Menzel papers are at the Harvard University Archives. **Near-A**; held back only because the destruction claim comes through two intermediaries | 07 f02 0:18:41; 09 f02 |
| **James Conant** | Harvard president, Manhattan Project administrator, AEC and Joint R&D Board adviser | Documented; and the board now carries `research-development-board`, so his membership is checkable | 07 f02; 09 f02 |
| **Carl Compton** (resolved by me as **Karl Taylor Compton**, MIT president 1930-48) | Briefed on UFO technology at Wright-Patterson in 1950; his FBI file reported destroyed 30 August 2006 in answer to a 2014 FOIA | The FOIA response letter itself, which the requester published. See section C row 4 | 09 f03 |
| **Gordon Dean** | AEC chairman 1950-53 | AEC records; pairs with A row 1 | 09 f02 |
| **Detlev Bronk** | NAS and Johns Hopkins president, alleged autopsy custodian | Nothing but MJ-12 lore attaches; his own papers exist | 07 f04 |
| **James Forrestal** | First Secretary of Defense; death speculatively linked to UFO knowledge | The 1949 Navy board of investigation report, released 2004 | 09 f03 |
| **Allen Dulles** | Two meetings with JFK on 28 June 1961, said to corroborate a 1995 MJ-12 leak | The 2022 JFK-files release of the Dulles diary. The corroboration claim is testable and narrow | 09 f02 0:34:13 |
| **James Jesus Angleton**, **Hugh Angleton** | Vatican and Knights of Malta lineage behind CIA counterintelligence | Nothing here would settle it; the membership rolls are not public. Recorded because the claim recurs | 07 f01; 09 f03 |
| **John Deutch**, **Stephen Hadley**, **Robert McNamara**, **Bobby Ray Inman** | Senior officials named as knowing or as commissioning studies | For Hadley specifically, an Office of Net Assessment study on the cost of disclosure would have a contract record | 08 f04 1:02:06; 07 f04 |
| **Ron Pandolfi** | A CIA science and technology officer described as read in early | No record named. He is real and identifiable | 09 f01 |
| **Rosemary Smith** | Located a downed TU-22 in Zaire by remote viewing; Carter quoted on it | The declassified STAR GATE collection would carry the session | 09 f03 |
| **Sidney Gottlieb**, **Darryl Bem**, **Philip Zimbardo** | MKULTRA and the STAR GATE scientific oversight committee | The 1995 AIR evaluation of remote viewing names the oversight structure; MKULTRA is documented in the 1977 Senate joint hearing | 08 f02 0:24:14; 08 f04 1:43:36 |
| **Lawrence Rockefeller** | Funded Mack, Greer and the abduction-research pipeline | The Rockefeller Initiative correspondence, 1993-96, in the Clinton Library | 06 f02 2:09:35 |
| **David Noble** | Eyewitness aboard USS Finch during Bluegill Triple Prime | The USS Finch deck log, NARA RG 24. Same channel as A row 19 and A row 2 | 09 f03 |
| **Harry Turner** | Reported to Australian Joint Intelligence Organisation that Teller was working on gravity control | National Archives of Australia, JIO series | 09 f02 0:30:31 |
| **Mark McCandlish**, **Brad Sorenson** | The 1988 Norton AFB exhibit, via a 1990 Bill Scott interview in *Aviation Week and Space Technology* | The 1990 volume itself. A dated trade publication with a named author, so this is close to A; the corpus gives no issue date | 07 f01 1:23:43 |
| **John Blitch** | DARPA programme manager; a $70M cephalopod-camouflage SAP cancelled without explanation ~Nov-Dec 2000 | DARPA programme and contract records; a cancellation has a paper trail even when the programme does not | 07 f04 2:25:58 |
| **Mario Woods**, **Ellsworth AFB** | 1977 incident, woke nine miles away, kept a Q clearance for 20 years | Hastings catalogued him; a Q-clearance record and the base blotter would test it | 08 f04 1:10:25 |
| **Collins Elite** | An Air Force-origin evangelical group treating the phenomenon as demonic | Traces only to Redfern's book. An AFOSI organisational record would settle it either way | 06 f02 1:22:33 |
| **William Mallow**, **Paul Shatzkin**, **David W. Webb**, **Chase Brandon**, **Jason Sands**, **Michael Gladych**, **Stanley Deser**, **Richard Arnowitt**, **West Point** | Analysts, biographers and cited physicists around the Strieber and Rossi material | Gladych's 1956 article is dated and locatable and quotes Deser and Arnowitt, so one document covers three names. The rest name no record | 06 f02 1:28:16; 06 f03 0:35:25 |
| **Nick Cook**, **Joseph Farrell**, **Walter Gerlach**, **Hans Kammler** | The Nazi Bell material | Nothing produced in eighty years. Recorded so the next pass does not re-derive it | 08 f04 0:24:17 |
| **Italo Balbo**, **Guglielmo Marconi**, **Mussolini**, **Hitler**, **Pope Pius XII**, **Myron Taylor** | The Magenta 1933 / Gabinetto RS/33 cluster | Archivio Centrale dello Stato for the alleged Air Ministry body. No original has been produced by anyone; two maps carry it and both speakers hedge | 09 f03 1:38:40; 10 f04 2:17:28 |
| **Dan Crenshaw** | New House Intelligence chair, on whom the pending disclosure bill is said to hinge | Committee membership and the bill's own legislative history | 10 f04 2:42:13 |
| **Pippa Malmgren** | Relays her father's off-tape deathbed remark | Nothing; the speaker says it was not recorded | 09 f03 |
| **Project Orion**, **Excalibur**, **Strategic Defense Initiative** | Teller's X-ray laser said to descend from Bluegill data and feed SDI | Livermore's own published Excalibur record and NSDD-119. The lineage claim is checkable; the Bluegill origin is not | 09 f03 1:31:31 |

### B4. Facilities

| Name | Claimed | What would settle it | Lead map |
|---|---|---|---|
| **Dugway Proving Grounds** | Battelle classified contracts; a hangar sighting; a deathbed storage claim | **Already in board prose** (`gerb-mitre-investigation.desc`), so this is a promotion question. Battelle's Dugway contract record on USAspending | 07 f01 1:14:46 |
| **Fort Detrick** | Battelle biological-materials lab | Contract record; the board carries `battelle` | 07 f01 1:10:41 |
| **Norton AFB**, **Holloman AFB** | The 1988 exhibit and the 1971 footage shown to Sandler and Emenegger | Base histories; the Holloman footage claim is fifty years old and has never produced film | 07 f01 1:16:23, 1:23:43 |
| **Camp Hansen**, **Subic Bay** | Where Herrera says he was threatened and his camera was tampered with | Same channel as A row 19: the unit chronology and any base incident report | 08 f03 0:27:24, 0:29:00 |

---

## C. Corrections to existing nodes

Where a lead map records something about a node the board already carries that the board does
not appear to have. Node ids verified against `data/the-program.json` by grep.

| # | Node id | What the lead map has that the board does not | Lead map |
|---|---|---|---|
| 1 | `eric-wang` | The node's own narrative already names **Arthur Stansel** in the UPSHOT-KNOTHOLE reports. The corpus gives him as Arthur Stansell, a blast-effects engineer, places him on site for the **Harry** shot of **19 May 1953** at 32 kilotons, and attaches an alleged Kingman, Arizona 1953 crash-retrieval claim to him. The board has the name and neither the date nor the claim | 09 f02 0:02:38 |
| 2 | `eric-wang` | Two maps flag an **Eric A. Walker / Eric H. Wang conflation** and one adds a widow, **Maria Wang**, claiming Wang reported to Kissinger and that his Department of Special Studies moved from Wright-Patterson to Sandia/Kirtland in **1956**. The node has the 1954 transfer to Wright Air Development Center and a 1960 Structures Division title, and no 1956 Kirtland move. The node says the documentation establishes an office chief and nothing else, which is right; the conflation warning belongs beside it | 07 f01 1:32:41; 09 f02 0:04:25 |
| 3 | `battelle` | The node dates the nickel-titanium work to 1948-49 as **Wright-Patterson sponsored**. The corpus has a speaker naming a **1949 Los Alamos to Battelle Nitinol contract** declassified in the 1960s. Different sponsor for the same year and the same alloy. Do not merge; the contract record settles it | 08 f01 1:34:53 |
| 4 | `robert-sarbacher` | The node's narrative already mentions **Compton**. The corpus supplies the referent and a document: Karl Taylor Compton, briefed at Wright-Patterson in 1950 per Sarbacher via Stanton Friedman, with a **2014 FOIA answer that his FBI file was destroyed 30 August 2006**. The board carries `stanton-friedman` and `john-greenewald` and not this thread | 09 f03 |
| 5 | `robert-sarbacher` | Two further items: a claimed 1986 written account posted to Strieber by UPS and never delivered because Sarbacher died, and a claim via Brown's daughter and biographer that Sarbacher collected **Townsend Brown** after a Paris test. The second is an edge claim between two nodes the board now carries. Both are testimonial | 06 f02 0:14:12, 0:17:29 |
| 6 | `thomas-townsend-brown` | The corpus carries a **named-person denial from inside the advocate circle**: Puthoff and Davis are reported sceptical that Brown achieved what is claimed of him, and his Navy work is said to be still classified. The board's denial adjudication should see this; it is the strongest counter-evidence in the slice and it is not from AARO | 08 f04 |
| 7 | `skywatcher` | The node states plainly that corporate form, funding and personnel were not located. The corpus names **James Fowler** as lead operator, a 23-year military career retiring as Sergeant Major in 2020, and dates the company's origin to a **2021 government-contracted counter-drone war game** at which a seven-craft formation was reportedly seen. That converts an admitted gap into a checkable one: a state corporate registration and a service-verification request | 10 f03 0:04:18, 0:08:35 |
| 8 | `jake-barber` | The node's chronology runs media appearance, NewsNation, Sol Foundation. The corpus adds three structural claims it does not carry: closed testimony to the Senate Intelligence Committee in a SCIF, a **Bureau of Indian Affairs cover contract** near White Sands Missile Range, and a serial **DOPSR** submission used deliberately as a probe of what the review process protects. All testimonial, all with a possible paper trail | 06 f01 0:32:53, 0:55:41, 2:05:43 |
| 9 | `sean-kirkpatrick` | A direct public-versus-private contradiction attributed to him: said to have denied the Herrera account publicly while confirming it privately to Senate Intelligence Committee staff. **Tier note:** this is a claim about what an AARO director said, not a claim sourced to AARO, so the section 2 cap does not apply to it in the way it applies to AARO's own reports | 06 f01 1:28:12 |
| 10 | `sean-kirkpatrick` and `oak-ridge-national-laboratory` | A named former Senate staffer flags a possible conflict of interest: the AARO advisory group's formation contract let through ORNL while he directed AARO, and his employment there as a contractor afterwards. He explicitly declines to call it wrongdoing. The board connects these two nodes only through the 2024 specimen synopsis | 08 f04 1:09:33 |
| 11 | `kirk-mcconnell` | The node covers his SASC service and Sol Foundation role. The corpus is a full interview with him and supplies most of C row 10, the Avco test-report language, the Bluegill footage account and the AARO interview-recording complaint. He is a **node who is also a primary source in this corpus**, which the node does not say | 08 f04 throughout |
| 12 | `nnsa` | A **June 2022 NNSA FOIA response** on Starfish Prime plus UAP acronyms, stating an additional subject-matter-expert review was required. The board's FOIA layer does not carry it and it is a live, requestable case | 09 f03 1:08:45 |
| 13 | `rand-corporation` | The node's UFO record starts at the 1968 Kocher draft. The corpus names a **1961 RAND report on re-entry-vehicle vulnerability to X-rays** as the conceptual basis for the Bluegill interceptor design, which puts RAND upstream of A row 2 by seven years | 09 f03 0:57:51 |
| 14 | `eg-and-g` | Two additions: EG&G as the **DOE / NEST support contractor** for the 1997 Peru response, and a senior EG&G engineer describing an egg-shaped recovered object of roughly SUV size. The board carries EG&G through the Wilson-Davis meeting only | 07 f01 0:08:54; 06 f01 1:30:12 |
| 15 | `paul-bennewitz`, `richard-doty`, `william-moore` | One speaker gives **two different causes of Bennewitz's death in a single passage**, suicide and death in a psychiatric institution. The lead map flags it explicitly. Do not silently pick one; if the board states a cause, it should state which record it rests on | 08 f01 1:40:14 |
| 16 | `sperry-rand` | The node says no UAP claim attaches to it, which was true of the sources then in hand. The corpus has Corso naming **Sperry Rand alongside Bell Labs** as a recipient of Roswell-derived material. That is a testimonial claim and would not change the node's tier, but the node's flat statement that none exists is now inaccurate | 07 f01 0:24:35 |
| 17 | `stargate-program` | Two additions the desc does not carry: a custody claim that the programme moved by the **personal patronage of named general officers** rather than by fixed bureaucratic ownership, and a claim that **Ingo Swann double-reported** his Office of Naval Intelligence work to the Church of Scientology Guardian's Office. The second is extraordinary and rests entirely on one man's recollection of a single viewing decades ago | 07 f03 1:13:18; 10 f04 2:03:47 |
| 18 | `hearing-2025-09-09` | The near miss on **Stephen Digna** resolves: the corpus has Greer naming him as a Fort Irwin witness allegedly seized by Raytheon operatives after seeing more than intended. The board's prose carries the token; it does not carry the claim or the Raytheon attribution, which is a directional accusation against a node the board already holds | 09 f01 2:32:28 |
| 19 | `robert-salas` / `malmstrom-echo-flight-1967` | A Malmstrom base commander is named as `Arnie Arleson`, which may be a corruption of **Duane C. Arneson**, already in the gerb corpus D13 affidavits, or may be a different person. The lead map says do not merge without checking the source, and that instruction should survive into the board | 10 f04 2:31:08 |

Also worth carrying: `philip-corso` gains the **Psychological Strategy Board / Operations
Coordinating Board nexus** (A rows 11 and 12) and the unpublished manuscript *Dawn of a New
Age*, which is said to name a 1986 UFO Working Group that the published book does not
(07 f01 0:25:22). And `mitre-corporation` gains a Robert M. L. Baker high-frequency
gravitational-wave conference paper, abstract-only per the speaker (06 f03 0:30:27).

---

## D. Noise, and why

155 names, four groups. Listed in full so the next pass can see what was excluded and why.

### D1. Already on the board under a fuller label or a different spelling. 14 names.

**These are false ABSENTs and the cross-check produced them, not the corpus.** Every one is a
bare acronym or a caption misspelling that failed to match a node whose label is the expanded
or correct form.

DIA (`dia`), CIA (`cia`), NSA (`nsa`), NRO (`nro`), SRI (`sri-international`),
Sky Watchers (`skywatcher`), David Grush (`david-grusch`), Stephen Greer (`steven-greer`),
Danny Sheehan (`daniel-sheehan`), Wilbur Smith (`wilbert-smith`), Bob Salas (`robert-salas`),
Carl Nell (`karl-nell`), MK-Ultra (`hearing-2026-06-30`, `tl-mkultra-hearing`),
US Army INSCOM (in `stargate-program.desc`).

### D2. Hosts, guests, authors, researchers and commentators. 40 names.

On the board these would be media-structure nodes at best, and the board already carries the
ones that matter (`jesse-michels`, `ross-coulthart`, `richard-dolan`, `robert-hastings`,
`john-greenewald`, `jacques-vallee`, `garry-nolan`, `beatriz-villarroel`). None of the
following is named in connection with a record.

Sean Ryan, Chris Sharp, Peter Levenda, A. J. Hartley, Kai Dickens, Randall Carlson,
Graham Hancock, Dave Rossi, John Lear, Chris Bledsoe, Matthew Pines, Matt Pines,
Whitley Strieber, Bud Hopkins, Paul Davies, John Burrows, Michael Schratt, Bill McDonald,
John DeSouza, Chris Carter, Chris Ramsey, James Goodall, David Jacobs, Gordon Creighton,
Walter Isaacson, Marvin Kalb, Bernard Kalb, William Shawcross, Seymour Hersh, Michael Rich,
William Hamilton, Bill Hamilton, Donna Hare, Roger Hanlon, Jeff Marcy, Stanley McDaniel,
John Brandenburg, Hartley Trent, Peter Thiel, Demi Lovato.

Note: **Matthew Pines / Matt Pines** and **William Hamilton / Bill Hamilton** are each one
person entered twice by the cross-check.

### D3. The JFK-assassination and Cold War political cast. 78 names.

Batch 09 file 04 and batch 10 file 04 carry long assassination narratives, a Knights of Malta
thesis and an "S-Force" account. The speakers themselves say the Anderson Trust material has
nothing to do with UAP and offer it only as a funding precedent. These names are connective
tissue in someone else's argument, not structure in this one, and several are heads of state
named in passing.

E. Howard Hunt, Douglas Caddy, Richard Nixon, Harry Truman, JFK, Jimmy Carter, John Glenn,
William Cohen, Jack Anderson, Bob Monroe, Ho Chi Minh, James Randi, Lyndon B. Johnson,
Lyndon Johnson, Earl Warren, Charles Willoughby, Robert Lovett, Henry Stimson, John J. McCloy,
Edward Lansdale, Howard Hughes, Robert Maheu, Fidel Castro, Che Guevara, Santo Trafficante,
Sam Giancana, Sheffield Edwards, Frank Sturgis, James McCord, George H.W. Bush, George W. Bush,
George H. W. Bush, Donald Trump Jr., Robert F. Kennedy Jr., Eugene Thane Caesar, Bill Holton,
Linda Tripp, Jackie Gleason, Bill Colby, Bill Casey, Wild Bill Donovan, Bill Donovan,
Nelson Rockefeller, McGeorge Bundy, George F. Kennan, John Foster Dulles, Howard Baker,
William Elliott, Harold Greene, Tom Farmer, Bill Seidman, George Ball, Eisaku Sato,
Norman Cousins, Richard Byrd, Reinhard Gehlen, Ted Shackley, Otto Skorzeny, L. Ron Hubbard,
Sidney Sheldon, Stanley McChrystal, Vladimir Putin, Xi Jinping, Vladimir Nabokov, Herman Kahn,
Tom Schelling, Richard Goldschmidt, Alan Mack, Dalton Fury, Osama bin Laden, Terry Lovelace,
Buzz Aldrin, Chris McKay, Pascal Lee, Bob Zubrin, Darlene Lim, Cash Patel, Prince Philip.

Note: **Lyndon B. Johnson / Lyndon Johnson**, **George H.W. Bush / George H. W. Bush** and
**Wild Bill Donovan / Bill Donovan** are each one person entered twice. **Cash Patel** is the
caption form of Kash Patel. The `hughes in sperry-rand.desc` near miss is **Hughes Tool**, a
different referent from Howard Hughes.

### D4. Places, organisations and terms named in passing. 23 names.

Named as scenery, biography or unfalsifiable affiliation. Nothing attaches to a record and in
several cases nothing could: the Knights of Malta membership rolls are not public, so the
recurring Malta thesis in batches 09 and 10 is not merely unsourced but unsourceable from open
material, which is worth stating once rather than re-testing.

Brooke Army Medical Center, Medway Plantation, Crystal City, Bagram Airfield, Tora Bora,
Cape Girardeau, Jet Propulsion Laboratory, Aquarius Reef Base, Fort Jackson, USS Hornet,
Rockefeller JY Ranch, Colorado School of Mines, Marine Biological Laboratory,
Church of Scientology, International Credit Bank, Sullivan & Cromwell, Brown Brothers Harriman,
Momentus, Knights of Malta, CFR, FBI, CE-5, J-SOC.

Note: **FBI** and **J-SOC** are here rather than in D1 because the corpus attaches no
structural claim to either that a record could test; the FBI appears as the recipient of two
unnamed death investigations and J-SOC only inside the Malta thesis.

---

## Cross-batch recurrence

The names that appear in more than one of my five maps, from speakers who are not each other's
sources. This is the ordering signal the board's owner asked for.

| Name | Maps | Section |
|---|---|---|
| Bluegill Triple Prime / Johnston Atoll | 06, 08, 09, 10 | A2 |
| Lawrence Preston Gise | 06, 08, 09, 10 | A3 |
| Harald Malmgren | 06, 08, 09, 10 | A4 |
| John A. McCone | 06, 07, 09, 10 | A7 |
| Atomic Energy Commission | 06, 08, 09, 10 | A1 |
| Richard Bissell | 06, 09, 10 | A6 |
| Thomas Townsend Brown (existing node) | 06, 07, 08, 09 | C6 |
| Philip J. Corso (existing node) | 06, 07, 09 | A8, A11 |
| Battelle (existing node) | 07, 08 | C3 |
| Magenta 1933 | 09, 10 | B3 |
| Karl Nell (existing node) | 06, 07 | D1 |
| Sean Kirkpatrick (existing node) | 06, 08 | C9, C10 |

---

*Written 2 September 2026 by triage agent, group 2. Nothing in this file has been added to the
board and nothing in it is graded. Sections A and B are research targets; section C is a list
of things the board may already be able to say and does not; section D is a record of
exclusions so the next pass does not re-derive them.*
