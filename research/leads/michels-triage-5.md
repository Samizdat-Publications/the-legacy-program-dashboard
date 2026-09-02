# Michels corpus triage, group 5 (lead maps 21 to 25)

**Written 2 September 2026** against `research/leads/michels-corpus-21.md` through `-25.md`
and `research/leads/michels-absent/group-5.tsv` (305 names: 100 from batch 21, 33 from 22,
41 from 23, 87 from 24, 44 from 25).

**Nothing here is board content and nothing here is asserted as true.** Every row records
what a named speaker said, with the lead map and timestamp it came from. Section A names the
record that would have to be opened; it does not claim the record says anything. No document
was opened for this pass. Board greps below were run against `data/the-program.json`.

**Counts.** A: 23 names in 20 rows. B: 65 names, plus 2 `[PHON?]` names carried in under the
brief's rule and not part of the 305. C: 34 names, plus 14 corrections keyed to node ids.
D: 183 names in 8 groups. 23 + 65 + 34 + 183 = 305.

## Read this before Section A: the ABSENT list is about 11 percent wrong

I grepped `data/the-program.json` for roughly 60 of the 305. The cross-check reports ABSENT
for a name the board already carries whenever the two differ in **form** rather than in
substance. Confirmed cases are itemised in C1. Three shapes:

| shape | example | what the board actually has |
|---|---|---|
| acronym against spelled-out name | `CIA`, `NRO`, `AEC`, `ONI`, `DIA`, `NGA`, `DOE`, `FAA` | "Central Intelligence Agency" 30 hits, "National Reconnaissance Office" 67, "Atomic Energy Commission" 21, "Office of Naval Intelligence" 8, "Defense Intelligence Agency" 158, "National Geospatial" 17, "Department of Energy" 37, "Federal Aviation" 8 |
| informal or shortened personal name | `Jim Ryder`, `Chuck McCullough`, `Jim Lacatski`, `Bob Salas`, `Bob Hastings`, `Colin Kelleher` | `james-ryder`, `charles-mccullough-iii`, `james-lacatski`, `robert-salas`, `robert-hastings`, `colm-kelleher` |
| caption corruption of a node's own name | `David Grush`, `Lou Elizondo`, `Jim Wire`, `Jay Allen Hynek`, `Beatrice Villarroel` | `david-grusch`, `luis-elizondo`, `james-ryder`, `j-allen-hynek`, `beatriz-villarroel` |

`README.md` says a false ABSENT is the expensive error because it sends a researcher after
something the board already carries. Two of my five maps would have sent one after Jim Ryder,
who has a node and 27 mentions. **`tools/corpus_crosscheck.py` needs an alias pass before the
next corpus, not after it.** `research/_removed.json` already holds an alias map.

---

## A. Document-backed candidates

Ranked: the rows that would change the board's argument come first. "The record" is what a
later pass would open.

| # | Name | Class | The record that would justify it | Where to open it | Why THIS board rather than a general UFO timeline | Map / TS |
|---|---|---|---|---|---|---|
| 1 | **Matthew Sullivan** | person | A DoD Inspector General finding that his original complaint was "warranted and credible"; a congressional letter about his death; an FBI referral sent through House Oversight, reportedly not received and resubmitted | DoD IG published reports and FOIA reading room; House Oversight correspondence | The board carries the reprisal thread already (`crane-secdef-grusch-reprisal-letter-2025`, `grusch-icig-complaint`). A death roughly two weeks before scheduled closed-door testimony, with an IG adjudication already sitting on the underlying complaint, is the only reprisal-adjacent item in my five maps with a government finding attached rather than a speaker's opinion. **Named independently in two maps by two guests.** | 22 file 03 2:19:13-2:21:03; 23 file 04 1:21:14-1:23:05 |
| 2 | **Andrija Puharich** | person | His own US patents on hearing-transmission devices; an AEC grant to Intelectron; his Army service record; an FBI file on his movements in Israel the filmmakers say they obtained by FOIA (21 D11) | USPTO Patent Public Search; DOE OpenNet and NARA RG 326 for AEC grant records; NPRC for the service record; FBI Vault | The board carries `l-sri` and `stargate-program` but nothing before them. Puharich is the agency-funded predecessor of both, and Intelectron is the same private-company-as-custody-layer shape the board already argues at RIAS and Battelle. **Named in three of my five maps by three different guests** (Milazzi, Josek, Brown and Mishlove), which is the recurrence signal the owner asked to be told about. Board grep: zero occurrences of "Puharich". | 21 file 02 throughout, 0:44:10, 1:15:57; 23 file 01 1:57:10; 25 file 04 1:22:37 and file 02 0:38:08 |
| 3 | **Personal Reliability Program** | program | The DoD nuclear weapons Personnel Reliability Program directive and its service instructions, with their decertification criteria | DTIC; the Washington Headquarters Services directives archive | The board carries `malmstrom-echo-flight-1967`, `l-malmstrom`, `robert-salas` and `robert-hastings`. PRP is the named administrative instrument deciding whether a witness at a nuclear site keeps his access after reporting. It turns "they were afraid to report" from testimony into a published rule. Board grep: zero occurrences. | 24 file 01 0:13:03 |
| 4 | **Invention Secrecy Act of 1951** | legislation | The Act itself, and the annual secrecy-order counts the patent office reports | Statutes at Large on govinfo; USPTO; the long-running FAS secrecy-order series | The board has a PATENTS tab whose whole argument is what does and does not appear in the patent record. This is the statute that makes an absence there a legal artefact rather than evidence of nothing. **Promotion, not discovery:** board prose already names it once, in the same sentence as the Atomic Energy Act "born classified" regime and 50 U.S.C. 3510. It belongs beside `janap-146` and `afr-200-2`. | 21 file 04 0:59:15 |
| 5 | **MK-Ultra** | program | The 1977 Senate joint hearing on the CIA's programme of research in behavioral modification, and the financial records located in 1977 after the 1973 destruction order | govinfo for the hearing; CIA CREST for the financial records | The board carries the 2026 declassification task force's MKULTRA hearing (`tl-mkultra-hearing`, `tl-2026-mkultra`) but not the programme. MK-Ultra is the best documented instance of the custody failure this board argues: records ordered destroyed, surviving only by having been misfiled, so a programme's absence from the record proves nothing about its existence. | 21 file 01 1:18:24 and file 02 throughout; 25 file 04 1:22:37 |
| 6 | **Brookings Report, 1960** | document | The Brookings Institution study for NASA's Committee on Long Range Studies, transmitted to the House Committee on Science and Astronautics in 1960 | NASA HQ history office; the transmittal is a House committee document, so govinfo and HathiTrust | The cover-up view's strongest instruments are the ones predating what they are said to conceal. **Carry it with the correction:** the report discusses the societal consequences of discovering artefacts and recommends further study. It does not, on the reading available to me, recommend withholding, which is what the speaker asserts (24 S5). Recording it accurately is worth more here than the transcript's version. Board grep: zero occurrences. | 24 file 03 1:01:38 |
| 7 | **Aldo Rabelo** | person | His tenure as Brazil's Minister of Defense 2015-16; the Operation Prato archive his ministry holds; Portaria 551/GC3 of 2009 | Brazilian government records; the FAB's own Prato release. The board already carries the Portaria and cites its publication in the Diário Oficial, so that half is done | The board has `operacao-prato`, `ev-varginha-1996`, `l-varginha` and `hospital-regional-varginha` but no officeholder node. Rabelo is the most senior official on the public record about them, and his stated position that Brazilian disclosure is conditioned on reciprocal US disclosure is a structural claim by a named minister, not a witness account. Board grep: zero occurrences of "Rabelo". | 22 file 04 1:09:05-1:11:21, 1:16:45-1:17:37, 0:22:26-0:23:18 |
| 8 | **Lord Hill-Norton** | person | His written questions and the ministerial answers to them; the UK Ministry of Defence Rendlesham file released to the National Archives | Hansard; TNA, the DEFE series holding the Rendlesham correspondence | The board carries `rendlesham-1980`, `ev-rendlesham-files` and Halt. Hill-Norton, a former Chief of the Defence Staff and Chairman of the NATO Military Committee, is the most senior officer of any nation to put that incident on a parliamentary record and receive a defence ministry's answer. That is a documented denial the board's denial machinery can grade. Board grep: zero occurrences. | 22 file 01 1:33:04-1:38:25 |
| 9 | **Bobby Ray Inman** | person | His confirmation record as Deputy Director of Central Intelligence; his SAIC directorship in the company's own filings; the recorded public remarks in which he refers to a national underwater reconnaissance capability | govinfo for the confirmation hearings; SEC EDGAR for the directorship. The recording is the thing a researcher cites, so it must be located, not assumed | SAIC is already in the board's prose and the board already carries the Kirkpatrick-to-SAIC line. Inman is the documented officeholder linking a DCI-level post to it. He also **denies** knowledge of Puharich when cold-called (21 file 02), and this board grades denials. Named in two of my maps. Board grep: zero occurrences of "Inman". | 21 file 02 (Milazzi's call); 25 file 03 1:18:07-1:19:55 |
| 10 | **Richard Bissell** | person | The CIA's own declassified U-2 and OXCART histories, plus his testimony and papers | CIA CREST and the CIA FOIA reading room | The officer who ran the Directorate of Plans and stood up the facility the board's Area 51 and S4 material rests on. Two of my maps independently make him the origin of the 1933 Magenta briefing claim; **that claim is a single deathbed account and must not travel with him.** The man is document-backed on his own. | 23 file 03 0:33:19; 24 file 01 1:51:39 |
| 11 | **Project A119** | program | "A Study of Lunar Research Flights", Air Force Special Weapons Center, May 1959, declassified around 2000 | DTIC, and the `archive.org/details/DTIC_*` mirror the board's notes record as reachable | A dated, denied-then-declassified USAF study whose existence was maintained as non-existent for four decades. The denial adjudication gets an instrument rather than an anecdote, and the participant's disclosure of it in an unclassified fellowship application is a documented compartmentation breach. Board grep: zero occurrences. | 24 file 03 1:03:29 |
| 12 | **Manned Orbiting Laboratory** | program | The NRO's own October 2015 MOL declassification release | nro.gov FOIA reading room | A fully documented case where a crewed-laboratory programme carried a reconnaissance mission, closed and then released by the agency itself. The board argues about cover programmes; this one needs no witness at all. Board grep: zero occurrences. | 24 file 03 1:44:06-1:46:44 |
| 13 | **Defense Support Program** | program | USAF and NRO DSP programme records; and the Black Vault FOIA request for "fastwalker" and "slowwalker" documents, answered with a claimed statutory exemption (24 D18) | Air Force fact sheets and DTIC; theblackvault.com, which the board's notes record as reachable | The board carries the Townsend AFIT thesis (`afit-townsend-2008`), Osedacz and the 1972-onward fastwalker database, but not the satellite constellation those observations come off. **A FOIA case is explicitly a record class for this section**, and an exemption claim on a term the board already carries is a gradeable denial. Board grep: zero occurrences of "Defense Support Program". | 24 file 03 1:12:46, 1:17:20-1:18:16 |
| 14 | **N3 (Next Generation Non-Surgical Neurotechnology)** and **Brainstorms** | program | DARPA's own N3 programme announcement and solicitation, and Battelle's 2020 Phase 2 release naming the Air Force Research Laboratory and Carnegie Mellon (21 D7) | darpa.mil; the federal solicitation archive; Battelle's own release | Battelle is load-bearing here and its 1950s role rests entirely on the Project Stork status reports, per `CANDIDATES-2026-08-30.md` section C. A publicly announced modern DARPA prime contract is the cheapest evidence that the same institution is still the government's chosen contractor for the awkward problem. **The AARO and DoD Tier 2 cap does not bite:** DARPA publishing its own programme is a primary record of that programme. | 21 file 04 1:22:03, 1:22:55 |
| 15 | **Charles Chase**, with the patent "Cognitive Enhancement Using Feedback" | person, document | A USPTO patent of that title assigned to Lockheed Martin, inventors given as Charles Chase and a second whose surname the caption corrupts | USPTO Patent Public Search, by assignee and title | The board has a PATENTS tab and already carries the Pais patents individually (`pais-patent-imrd`, `pais-patent-hfgw`, `pais-patent-emfg`). This patent either exists or does not, and settling it closes a whole transcript thread in an afternoon. Michels states his surrounding synthesis is speculative (21 S9) and Chase reportedly denies any connection to Norsen; **the patent is the only checkable piece and must not carry the synthesis with it.** | 21 file 04 1:20:26 |
| 16 | **Intelectron Corporation** | institution | The AEC grant, given on tape as roughly 300,000 dollars in the early 1960s with Annie Jacobsen credited for the archival find; New York State corporate filings | DOE OpenNet and NARA RG 326; NY Department of State corporate records | AEC money into a private biomedical company is the custody shape the board's AEC thread already argues, and unlike the Round Table Foundation both the grantor and the figure are named. Pairs with row 2. Board grep: zero occurrences. | 21 file 02 0:38:27-1:04:01, 0:44:10, 0:47:45 |
| 17 | **Peraton** and **Veritas Capital** | institution | Peraton's 2021 acquisition of Northrop Grumman's IT services business, and Veritas Capital's ownership, in filings and antitrust clearance notices | SEC EDGAR; DOJ and FTC premerger notices | Exactly the shape of last pass's accepted candidate 12 (BDM to TRW to `northrop-grumman`): an unrepresented corporate predecessor or successor of a node the board already carries. **The claim that Peraton holds Lockheed craft material is one reporter's theory and must not travel with the corporate record.** Board grep: zero occurrences of either. | 23 file 03 0:57:29-0:58:03; 23 file 02 1:32:53 |
| 18 | **Amentum** | institution | Amentum's own filings, and the corporate history by which EG&G's government-services business reached it | SEC EDGAR; DOE OpenNet for EG&G's Nevada test-site contracts | EG&G is already on the board with 48 mentions and is the canonical AEC-to-private-contractor bridge. Its present-day successor should be named from a filing rather than left to rumour. **The Pax River hangar claim attached to it is a tweet read aloud on air and stays out.** Board grep: zero occurrences of "Amentum". | 25 file 04 1:54:13, 1:59:20 |
| 19 | **Bettis Atomic Power Laboratory** | institution | The AEC and Naval Reactors contract record for the laboratory, and the nuclear space-power programme record | DOE OpenNet; NARA RG 326 | The board's custody argument runs through AEC-contracted laboratories. Bettis is a named one with a documented naval nuclear mandate and a documented space-power adjacency. The "contract conveniently ended" framing is the speaker's and is not part of the record being requested. Board grep: zero occurrences. | 25 file 01 0:10:59 |
| 20 | **Project Pandora** | program | The ARPA and Army Project PANDORA files on the Moscow embassy signal, in the CIA and Army FOIA releases | CIA CREST; The Black Vault; NARA | A documented US programme studying whether a foreign radio-frequency exposure had neurological effects, contemporaneous with the AEC-funded Intelectron work in row 16. It dates the directed-energy custody thread without depending on any UAP claim, and it is the only anchor under the Havana-syndrome material in map 21. Board grep: zero occurrences. | 21 file 02 1:23:11 |

**Three I would put first:** rows 1, 2 and 3. Sullivan because a government finding already
exists and the board already carries the thread it belongs to. Puharich because he is the
only name in my group that three different guests reach independently, and because the board
has an SRI node with nothing behind it. PRP because it is one directive that converts a
recurring testimonial claim into a published rule.

---

## B. Needs a document

Matters to the programme structure, rests only on what a speaker says. Research questions,
not candidates. Two `[PHON?]` names carried in under the brief's rule are marked **[carried]**
with the resolution stated as mine.

| Name | Map / TS | What is claimed | What record would settle it |
|---|---|---|---|
| **Harald Malmgren** [carried] | 23 file 03 0:32:26-0:34:10; 24 file 01 1:51:39; 25 file 03 1:18:07 | Corrupted five ways across my three maps (`Mamgren`, `Maumgren`, "Harold", "Terrell"). Claimed to have held UFO debris given him by Lawrence Preston Gise, to have been briefed by Bissell on the 1933 Magenta crash, and to have held Bluegill Triple Prime plume material | Resolution is mine: the real figure is **Harald B. Malmgren**, the trade negotiator and White House adviser. Board grep: zero occurrences of "Malmgren" in 6.9MB. The record is his own published writing and his NSC and USTR service file, not the deathbed accounts |
| **NURO, National Underwater Reconnaissance Office** [carried] | 25 file 03 1:18:07-1:19:55 | Rendered `neuro` throughout. A Navy and NRO joint body a Navy chief oceanographer with TS/SCI says he had never heard of | Resolution is mine. The record is the NRO's own declassification of its existence and the Navy directive establishing it. Gallaudet's claim is that a cleared officer did not know it existed, which is checkable only against his clearance record |
| Allen Dulles | 21 file 02 throughout | Met Puharich personally, per Puharich's own journal (21 D9) | The journal is a private archive. The openable record is the CIA's own chartering documents for the 1953 scientific advisory panel. Board grep: zero occurrences of "Allen Dulles" |
| CIA Directorate of Plans | 24 file 02 0:16:28 | Unlocked funding around 1952 for roughly 12 people to study a UFO and occult correlation | The claim traces to one author's book, not to a document. Directorate budget records, CREST |
| Office of Net Assessment | 25 file 04 0:52:35-0:53:21 | Named only as the office whose method the witness was trained in | ONA's establishing directive and its contract record on the federal procurement database |
| DTRA | 25 file 01 0:50:14, 1:44:12 | Witness's employer 2019-2024; tied institutionally back to DOE | Its establishing directive; the DOE link is an assertion about lineage, not a claim about UAP |
| JSOC, Joint Special Operations Command | 21 file 04 0:27:44, 0:45:44 | Coordinates with the CIA Office of Global Access and NEST on crash retrievals | Both entries come from a **novel's plot** relayed as encoding a real claim. Nothing to open until the claim is separated from the fiction |
| Naval Information Warfare Center | 21 file 04 1:17:07 | The N66001 contract prefix under which a Lockheed "biofusion" report was allegedly filed | The contract prefix is the one usable handle in this whole thread. Federal procurement records and DTIC by contract number. The speaker flags it as pieced together from multiple references, not a located document (21 D5) |
| Defense Nuclear Security | 21 file 04 0:45:44 | NNSA protective forces operate outside the normal DoD chain under Atomic Energy Act authority | The NNSA protective-force authorities are published. The crash-retrieval use is unsourced |
| Army Specialized Training Program | 21 file 02 0:02:50 | Recruited Puharich in 1947 | Real WWII programme; his enrolment is a service-record question. Note the date is suspect, the programme was wound down in 1944 |
| US Forest Service | 21 file 04 1:00:52 | Public cover for a guarded facility with an alleged portal | A land-transfer record for the parcel would settle the cover claim in either direction |
| Round Table Foundation | 21 file 02 0:09:06-0:40:21 | Puharich's Maine lab 1948-1957, funded by Army, Navy and CIA money | Maine incorporation and dissolution filings; the funding claim needs the grant records, and one funder's name is unresolved on tape |
| Lab Nine | 21 file 02 2:06:29-2:08:24 | Puharich's Ossining house and lab; a document exists from SRI to Lab Nine dated 1973 | The 1973 SRI document is the single most valuable unopened item in map 21. It is in a private archive; SRI's own contract correspondence is the alternative route. Hal Puthoff disputes the linkage on tape |
| TD-100 | 21 file 02 1:00:20-1:02:10 | Puharich's hearing-transmission device, demonstrated at the Pentagon | If it exists it is patented. Same USPTO search as row 2 in A |
| Operation Midnight Climax | 21 file 02 0:50:26 | Named as a CIA project alongside MK-Ultra | Documented inside the 1977 hearings, so this is subsumed by A row 5 rather than separate |
| CE-5 and Coherent Thought Sequencing | 21 file 04 1:04:05 | A named UAP-summoning protocol | A protocol published by a private individual. Nothing governmental to open |
| Operation Ketsana | 21 file 04 0:40:26 | A named 2009 Marine humanitarian operation in the Philippines during which a witness's unit encountered a craft | The operation is real and its unit records exist. Whether the named witness's unit was deployed is a muster-roll question, and it is the only falsifiable half |
| Project Preserve Destiny | 25 file 04 1:17:06-1:20:45 | A 1960s NSA and Air Force programme using genetically selected personnel as signals conduits | Rests entirely on one memoir. The checkable half is the author's own service record and the base assignments the host supplies |
| Vanguard Enterprise | 25 file 01 3:18:34; 25 file 04 3:16:46 | A whistleblower-support nonprofit founded by two named whistleblowers | State nonprofit registration and IRS filings. Present-day, and a support organisation rather than programme structure |
| Clementine | 24 file 03 0:10:58-0:12:55 | The 1994 mission's real purpose was reconnaissance for undisclosed lunar bases | The mission is documented. The purpose claim is one man's on-camera statement in a 2014 documentary (24 D3), so what is needed is the mission's own programme documentation, not the interview |
| Lunex | 24 file 03 1:44:06 | A 1957-1961 USAF crewed lunar base plan | The report exists at DTIC; nothing in the transcript ties it to the board's argument beyond adjacency |
| Sidney Gottlieb | 21 file 02 throughout | MK-Ultra architect; interviewed by an author for a planned book | Documented in the 1977 hearings, so subsumed by A row 5 |
| Jose Delgado | 21 file 02 (Delgado thread) | Implanted radio receivers to remote-control a bull; a close friend of Puharich per recovered letters | His own published work and his ONR and Army funding record are open. The Puharich link is in a private archive |
| Elizabeth Rauscher | 21 file 02 1:29:20 | Received a large ONI grant while working with Puharich | The grant would be an ONI contract record. Her papers are said to be at Berkeley |
| Beardsley Graham | 21 file 02 (Berkeley archive) | NASA-connected consultant whose Berkeley archive holds Intelectron correspondence | A named archive with named correspondence. Cheap to check, and it would corroborate A row 16 |
| Aharon Yariv | 21 file 02 (channelling tapes) | Named repeatedly on Puharich's channelling tapes | A real head of Israeli military intelligence. The tapes are private and their content is not a record of anything he did |
| Dan Sherman | 21 file 01 (referenced); 25 file 04 1:17:06 | Author of a memoir naming Project Preserve Destiny | Service record. See Project Preserve Destiny above |
| John Norsen | 21 file 03 (late file); 21 file 04 1:12:14-1:18:49 | Lockheed neuro-engineer, present at Allagash in 1976 on a classified tracking exercise, later found dead in a motel room | **Named independently in two files of the same map by unconnected speakers**, which is why it is here and not in D. A death certificate and an employment record would settle the man; the "biofusion" report would settle the work |
| Lyn Buchanan | 22 file 01 throughout | Army remote viewer; saw a UFO control panel in a hangar; interrogated at DIA the following week | His Army service record, and the 2017 CREST release of the remote-viewing files |
| Ed Dames | 22 file 01 | Gave the unit informal UFO practice targets | Same CREST release |
| Christopher Fox | 22 file 03 0:10:06 | Current Inspector General of the Intelligence Community | An appointment record. The board already carries `charles-mccullough-iii`, so the office is represented and this is an officeholder update |
| Gary McKinnon | 24 file 01 1:46:21-1:48:05 | 2003 intrusion into US military and NASA networks; describes an object populating on screen | The UK extradition proceedings and the Home Secretary's 2012 Commons statement are dated official publications. **What they establish is the intrusion, not its contents**, which were never adjudicated in open court |
| Donna Hare | 24 file 01 1:46:21 | A colleague told her they airbrush UFOs from photos before release | The photo-archive accession record for the named building is the only openable thing here, and it would not evidence the claim |
| Jordan Josek | 23 file 01 throughout | Removed from public school 2008-2010 into a facility supporting defense-contractor psychic research | School district and medical records are the witness's own to release. Nothing institutional to open from outside |
| Nick Cook | 25 file 02 (Mishlove thread) | Author on anti-gravity research | Board grep: zero occurrences. Worth noting for a different reason: `README-michels.md` records that his episode and the Townsend Brown documentary are **outside the pull window**, so the electrogravitics thread the owner asked for is not in this corpus at all |
| Thomas Bearden | 25 file 04 (scalar weapons) | Scalar-weapon claims | Self-published. Nothing to open |
| Andrew Marshall | 25 file 04 0:52:35 | Founder of the Office of Net Assessment | Documented, but named only as a biography line. See Office of Net Assessment above |
| Jeffrey Nusatelli | 25 file 04 3:16:46 | A new Vanguard co-founder; separately credited with a black triangle account at Vandenberg | The Vandenberg account, if made under oath anywhere, is the record |
| Pete Worden | 24 file 03 0:17:00-0:18:39 | NASA figure heavily involved in Clementine; connected DeLonge to a general | His NASA service record is public. The connection claim is not |
| Dan Goldin | 24 file 03 0:18:39 | A former NASA administrator who may know more | No claim with a record attached |
| Aberdeen Proving Ground | 21 file 02 1:16:51 | Puharich allegedly admitted in a letter to an Israeli-US mind-control programme based there | The letter is in a private archive |
| Restricted Area 5107 | 21 file 04 0:30:13 | Named restricted airspace over White Sands | Real airspace designation; no claim attached beyond scene-setting for a novel |
| Crane Naval Surface Warfare Center | 21 file 04 0:49:12 | A whistleblower says he was taken underground there and shown a device | The facility is real. The account has no document |
| NASA Eagle Works | 21 file 01 1:51:27 | Powered a microchip via the Casimir effect | The group publishes. A paper or a NASA technical report would settle it |
| NASA Langley | 25 file 01 0:00:52-0:34:41 | Site of the core triangle sighting; scrubbed LinkedIn map annotations | The scrub is checkable via archived captures; the sighting is not |
| Walt Disney Imagineering | 21 file 01 0:50:13, 2:24:08 | Developed a laser-plasma effect later offered as a possible tic-tac explanation | A patent or a published technical description would settle whether the effect exists as described |
| Johnson Space Center | 24 file 01 1:46:21; 24 file 03 0:44:35 | Building 8 named as the airbrushing site and as a 2003 intrusion target | See Donna Hare and Gary McKinnon above |
| Utah Test and Training Range, Space Dynamics Laboratory | 24 file 04 2:37:15 | Named as nearby facilities that might conventionally explain ranch activity | Named to be dismissed by the speaker. No claim |
| Bradshaw Ranch, Secret Mountain, Secret Canyon | 21 file 04 1:26:12-1:28:46; 22 file 01 1:27:53; 24 file 04 2:12:01 | Alleged underground facility; land sold to the Forest Service under a climate-research cover; a tunnel found by geophysical survey | **Named in three of my five maps.** The land-transfer record is a county deed and is the cheapest check in this whole section. The survey (21 D18) has no report number |
| Congonhas Airport, Anápolis Air Base | 22 file 04 0:32:07-0:35:24 | Tower and scramble sites for the 19 May 1986 mass incursion | FAB radar and operations logs. Rabelo says part remains classified, which is itself the finding |
| IPD Laboratory | 22 file 04 1:13:41 | Varginha pathology laboratory that examined samples from a soldier's fatal infection | A Brazilian pathology report. The board already carries `hospital-regional-varginha`, so this is an adjacent custody question |
| Baker Victory Services, OLV Human Services | 23 file 01 0:18:20-0:22:06 | A cover facility for defense-contractor psychic research | The litigation, the settlement and a supervisor's felony arrest are all real court records and all openable. **They would document abuse litigation, not a programme**, and nothing links the two but the witness |
| Odyssey Systems | 23 file 01 1:56:20 | A debated candidate for the platform underlying the alleged programme | The speaker says the stronger pointer is MITRE, which the board already carries with four nodes |
| Grey Fox | 23 file 03 0:20:21 | The Army intelligence unit the film's fictional corporation is mapped onto by geography | The mapping is the host's own inference, stated as such |
| Caladan Oceanic | 25 file 03 1:11:48 | A private deep-ocean expedition company partnered with NOAA | The NOAA partnership is a real agreement. Nothing UAP attaches to it |
| Pergamon Press | 25 file 04 2:39:41 | Framed as a scientific gatekeeping node | The publishing history is documented. The gatekeeping claim is the host's framing |
| Reinhard Gehlen, Reinhard Gehlen organisation | 24 file 02; 25 file 04 2:33:29 | Postwar Nazi intelligence network persistence | Documented at length in the CIA's own Nazi war crimes disclosure releases. **The UAP tie is the speaker's inference and he declines to affirm it** |
| World Commerce Corporation | 24 file 02 1:24:11-1:35:36 | A 1945 private intelligence and trading structure offered as the real custody layer above the aerospace primes | Panama corporate registration and the papers of its named officers. The custody claim rests on a novel's plot being read as encoded fact (24 D12) |
| Renaissance Technologies | 24 file 03 0:04:32-0:08:58 | Possibly a financial front for a programme physics component | Explicitly relayed by the speaker as someone else's theory, not endorsed. Nothing to open |

---

## C. Corrections to existing nodes

### C1. Names the cross-check called ABSENT that the board already carries (34)

Verified by direct grep of `data/the-program.json`. **These are not leads.**

| ABSENT row | Batch | What the board has |
|---|---|---|
| `CIA` | 21 | "Central Intelligence Agency", 30 occurrences |
| `ONI` | 21 | "Office of Naval Intelligence", 8 |
| `AEC` | 21 | "Atomic Energy Commission", 21 |
| `DOE` | 21 | "Department of Energy", 37 |
| `Sky Watcher` | 21 | node `skywatcher` |
| `Miguel Alcubierre` | 21 | prose in `richard-obousy`, 1 occurrence. Promotion question |
| `Joe McMoneagle` | 21 | prose in `l-sri`, 2 occurrences. Promotion question |
| `Jessica Utz` | 21 | prose in `stargate-program` as **Jessica Utts**, 1 occurrence. Promotion question; see C2 |
| `DIA` | 22 | "Defense Intelligence Agency", 158 |
| `NGA` | 22 | "National Geospatial", 17 |
| `CENTCOM`, `US Central Command` | 22 | "Central Command", 2 |
| `Brazilian Ministry of Defense` | 22 | "Ministry of Defence/Defense", 55 |
| `Jim Ryder` | 22 | node `james-ryder`, 27 occurrences |
| `Colin Kelleher` | 22 | node `colm-kelleher`, 75 |
| `Chuck McCullough` | 22 | node `charles-mccullough-iii`, 26 |
| `Jim Penniston`, `Colonel Halt` | 22 | prose in `rendlesham-1980`: "Penniston" 13, "Halt" 68 |
| `David Grush` | 23 | node `david-grusch`, 788 |
| `Lou Elizondo` | 23 | node `luis-elizondo`, 483 |
| `Jay Allen Hynek` | 23 | node `j-allen-hynek`, 44 |
| `James Forrestal` | 23 | prose in `william-l-moore`, 3. Promotion question |
| `Bill Steinman` | 23 | prose in `robert-sarbacher`, 14. Promotion question |
| `Alva Douglas` | 23 | a stated pen name of `jake-barber`, which is a node |
| `Bob Salas` | 24 | node `robert-salas` |
| `Bob Hastings` | 24 | node `robert-hastings` |
| `Jim Lacatski` | 24 | node `james-lacatski` |
| `Jim Wire` | 24 | a caption corruption of `james-ryder`; batch 22 renders the same man, same claim, correctly |
| `Herman Oberth` | 24 | prose in `friedwardt-winterberg`, 1. Promotion question, and the spelling is **Hermann** |
| `Guglielmo Marconi` | 24 | prose in `michels-gerb-structural-episode`, 2. Promotion question |
| `Beatrice Villarroel` | 24 | node `beatriz-villarroel`, 63, plus `paper-villarroel-bruehl-2025`, which is the exact collaboration the map describes. The board's spelling is the correct one |
| `NRO` | 25 | "National Reconnaissance Office", 67 |
| `FAA` | 25 | "Federal Aviation", 8 |
| `Donald Keyhoe` | 25 | prose in `roscoe-hillenkoetter`, 2. Promotion question |

**Low-count and ambiguous, not asserted:** "Nixon" 2, "Epstein" 5, "Maxwell" 3, "Walton" 1
and "Rockefeller" 61 all appear, but I could not confirm from the counts alone that they are
the same people. A re-run of the cross-check with an alias pass should decide these, not me.

### C2. Things the maps record about nodes the board already carries

| Node id | What the map records that the board seems not to have | Map / TS |
|---|---|---|
| `mit-lincoln-laboratory`, `burlison-mit-lincoln-letter-2026` | MIT has **confirmed it holds** a 1952 reel-to-reel recording of a senior DoD official briefing MIT scientists about the saucers, and is processing it for SCIF access, in response to the retention demand. A confirmed holding, not an allegation | 23 file 04 0:21:35-0:22:32 |
| `sean-kirkpatrick`, `kirkpatrick-sciam-oped-2024`, `l-skinwalker` | Brandon Fugal says he holds a **photograph** placing Kirkpatrick in the room at a briefing on a named April 2018 date, produced to rebut a reporter, against Kirkpatrick's public denial of any pre-2022 UAP interest. A dated, first-hand, checkable counter to a denial the board already carries | 24 file 04 2:38:11-2:43:54 |
| `battelle`, `gerb-battelle-investigation` | Battelle led a DARPA N3 Phase 2 team with the Air Force Research Laboratory and Carnegie Mellon, per Battelle's own 2020 release. See A row 14 | 21 file 04 1:22:03-1:22:55 |
| `immaculate-constellation`, `immaculate-constellation-12-page-report` | Brown states the 2017 origin story is itself a counterintelligence poison pill, that the programme is older, that Schriever AFB is at least one hub, that NRO's Sentient was integrated with it, and that its cognizant authority sits in the **NSC**, with DoD merely implementing. All his own inference, and he says so | 25 file 04 0:09:35-0:20:11, 0:19:12, 0:59:29 |
| `dylan-borland`, `jon-kosloski` | Borland alleges AARO sent ODNI a Memorandum for Record he did not sign, and argues that because AARO lacks original classification authority, leaving his triangle account unclassified is itself documentary | 25 file 01 1:56:39-2:04:40, 2:21:37-2:23:27 |
| `william-mccasland`, and the SAPOC entries | **Three independent non-corroborations in my group.** Buchanan does not recognise the name (22 file 01); Corbell says flatly there is no such general and calls the contact an operation (22 file 03); Shermer treats the disappearance as statistically unremarkable (24 file 01). Against that, Burlison places him on SAPOC and at AFRL and details the REI medical kit and absent ring-camera footage, flagging his own uncertainty on the gun | 22 file 01 and file 03, plus 22 section 4; 23 file 04 1:28:33-1:32:14; 24 file 01 0:00:50, 1:15:12 |
| `glenn-gaffney`, `george-knapp`, `bigelow-aerospace` | Gaffney is named independently in **four of my five maps** as the CIA Science and Technology director who blocked the 2008 Lockheed-to-Bigelow transfer, always sourced to Knapp's congressional testimony. Burlison separately names him as his top subpoena target | 22 file 03 1:51:22; 23 file 03 0:26:24 and file 04 1:48:44; 25 file 01 and file 02 |
| `l-skinwalker`, `skinwalkers-at-the-pentagon` | Travis Taylor was concurrently chief scientist of the Pentagon UAP Task Force while on the ranch team, disclosed only once authorised | 24 file 04 2:16:52-2:19:37 |
| `tim-gallaudet` | He sits on a UAP Science Advisory Council that reports to **ODNI**, not to the White House, and he corrects the host on this on air. He also says he personally reviewed Bluegill Triple Prime deck logs | 25 file 03 0:30:53-0:31:51, 1:25:19-1:29:50 |
| `robert-hastings`, `robert-salas` | The 167-witness figure is **unstable across three episodes and two corpora** (167 against "12 to 15" here, 400-800 against "a couple hundred" in the Gerb corpus). One recurring instability, not three observations | 25 section 5; 24 file 01 0:12:15; 25 file 04 2:26:26 |
| `salvatore-pais`, `pais-patent-imrd`, `pais-app-superconductor` | Burlison met Pais in person near Pax River with AARO's current director present, describes him as fearful, and says he refused an on-record topic. Three patent subjects named together | 23 file 04 0:35:56-0:39:35 |
| `eric-burlison`, `burlison-mitre-letter-2026` | The FFRDC letter campaign extends beyond MITRE to Aerospace Corporation, RAND and IDA; the Aerospace SCIF meeting produced two executives who knew nothing, which Burlison reads as sub-compartment structure rather than as exculpatory | 23 file 04 0:18:53-0:21:35, 2:11:52 |
| `thomas-townsend-brown` | Two additions worth chasing: Edward Teller is said to have connected **Floyd Odlum**, a Northrop shareholder, to invest in Brown (24 file 03 2:26:29-2:27:25); and a wartime telegram from William Stevenson to Brown's wife is described (24 file 02 1:30:18). The board already carries `tl-1953-brown-fag`, so the fraud framing is in place | 24 file 03 2:26:29; 24 file 02 1:09:19-1:30:18 |
| `stargate-program` | The Jessica Utts prose mention has a document behind it that the board does not appear to name: the 1995 commissioned evaluation of remote viewing that closed the programme, of which she was one of two named assessors | 21 file 01 (Utts, ASA presidency); 24 file 03 2:11:54 |

---

## D. Noise, and why (183 names)

Grouped, with counts and every name, so the next pass can see what was excluded and why.

**D1. Journalists, podcasters, documentary makers and authors named as sources or hosts (32).**
Excluded because a person relaying a claim is not a node; the claim's own source is.
21: Dick Russell, Martin Cannon, David Hatcher Childress, Doug Pasternack, William Arkin,
Noe Torres, Ruben Uriarte, Ray Fowler. 22: Ned Day, Joe Rogan, Larry King, Ibrahim Sued.
23: Robert Temple, Bud Hopkins, Chris Ramsey, Bruce Maccabee, Timothy Alberino, Beverly
McKittrick. 24: Peter Dale Scott, Carroll Quigley, Aline Griffith, Robert Ruark, Steven
Greenstreet. 25: Richard Botelho, Susan Casey, Whitney Webb, Colin Ross, Jeffrey Mishlove,
Randall Carlson, Graham Hancock, Ivan Sanderson, Brian Fitzpatrick.

**D2. Guests' own biographies, family members and immediate associates (22).**
Excluded under the brief's biography carve-out; none is placed inside the structure by
anything but the guest's own account.
21: Chris Gilbert, Jim Weiner, Jack Weiner, Charlie Foltz, Mike Asherman, Andy Puharich,
Richard Gildreich, John Whitmore, Phyllis Schlemmer, Bob Beck, Jacobo Grinberg.
23: Brent Friedman, John Harrington, Ryan Bledsoe, Chris Bledsoe, Amy Escridge, Richard
Escridge, Larry Smalley. 24: Colliers International, Trent Reznor, Dennis Åsberg.
25: Carl Nell.

**D3. Entertainment industry, celebrities and production companies (14).**
Maps 23 and 24 carry a long Hollywood thread. It is about depiction, not about custody.
21: Michael Eisner, Gene Roddenberry. 23: Toby Hooper, Steven Spielberg, Chase Brandon,
Tommy Lee Jones, Amblin Entertainment, Electronic Arts, Robert Zemeckis, Jackie Gleason,
Jack Black. 24: Sky Elements, Colossal Biosciences. 25: James Cameron.

**D4. Politicians, diplomats, officeholders and civil bodies named only in passing (25).**
None is tied to a record about the programme.
21: Anatoly Dobrynin, Walter Stoessel, Henry A. Wallace. 22: Bill Clinton, Barack Obama,
John Brennan, G. Gordon Liddy, Carol Rosin. 23: Richard Nixon, Sidney Souers, Stephen Miller,
Ron Pandolfi. 24: Jared Isaacman, Jimmy Carter, James Baker, Alonzo McDonald, Nelson
Rockefeller, Congress of Vienna, Klemens von Metternich, Pope Pius XII, Pope Francis,
Francis Spellman, Center for American Progress. 25: Elon Musk, Sam Altman.

**D5. The pre-war and post-war finance and intelligence network (31).**
Map 24 file 02 is the densest file in my group and almost all of it is this. The entities are
historically real and heavily documented; **the UAP tie rests on reading a novel's plot as
encoded fact** (24 D12), which is not a record. Note that `William Stephenson` (21) and
`William Stevenson` (24) are the same man under two spellings, and `Agnew Bahnson` is the one
name here worth revisiting if the Townsend Brown episodes outside the pull window are ever
fetched.
21: William Stephenson, Claude Shannon, William Shockley. 24: William Donovan, Office of the
Coordination of Inter-American Affairs, British Security Coordination, William Stevenson,
Special Operations Executive, Charles Hambro, Knights of Malta, Resorts International,
Intertel, Hawksbill Creek Agreement, Robert Maxwell, Otto Skorzeny, Ricardo Sicre, Michele
Sindona, Jeffrey Epstein, Steve Bannon, Agnew Bahnson, Charles Proteus Steinmetz, Eldridge
Reeves Johnson, Alfred Krupp, Axel Wenner-Gren, Detlev Bronk, I.G. Farben, Standard Oil,
Union Banking Corporation, Prescott Bush, Bank for International Settlements.
25: Ghislaine Maxwell.

**D6. MK-Ultra-adjacent, JFK-adjacent and parapsychology figures (21).**
Subsumed by A row 5 where they are documented at all; the rest is folklore.
21: Marina Oswald, Jolly West, Jack Ruby, Aldous Huxley, Arthur Young, Ruth Forbes Payne
Young, Mary Bancroft, Ruth Payne, Oliver Reiser, Jack Sarfatti, Hugh Angleton, James Jesus
Angleton. 24: Dean Radin, Robert G. Jahn, Brenda Dunne, Charles Honorton. 25: John Dee,
Edward Kelly, Michael Levin, Charles Manson, John Lilly.

**D7. Astronauts, NASA figures and lunar or Martian anomaly researchers (18).**
Map 24 file 03 is an image-archive argument. It belongs to a lunar-anomaly board, not this
one. **`Floyd Odlum` is the exception and is carried into C2** under Townsend Brown.
21: Sonny White, Gordon Cooper, Jean Cernan, Neil deGrasse Tyson. 23: Tim Taylor.
24: Buzz Aldrin, Harrison Schmitt, Eugene Cernan, Richard Hoagland, Gerald Soffen, Mark
Carlotto, Donald Menzel, Dorit Hoffleit, John Brandenburg, Bernard Haisch, Floyd Odlum.
25: Wally Schirra, Scott Carpenter.

**D8. Witnesses, comparanda and places named in passing with no institutional handle (20).**
21: Koyame, Mount Hayes, Mount Perdido, Mount Inyangani, Mount Zyl, Travis Walton, Mario
Woods, Don Phillips, J. Storrs Hall. 22: S4, John Lear, William P. Lear, Betty Hill, Barney
Hill. 23: Greenbrier. 25: El Paso International Airport, Bermuda Triangle, Iron Bottom Sound,
Don Walsh, Victor Vescovo.

---

## What is not in these five maps

Recorded so a later pass does not re-derive it.

- **No electrogravitics thread.** `README-michels.md` names six Townsend Brown episodes and
  says they fall outside the pull window. My five maps confirm it: Brown appears only as a
  cross-reference in maps 23 and 24, never as a subject. The thread the owner asked for is
  not in this corpus.
- **No Battelle at Wright-Patterson, no Moon Dust, no SAPOC Senior Review Group detail, no
  Wilson-Davis memo text, no AATIP contract figures, no Roswell chain of custody** beyond
  passing mention. Maps 21, 22, 23 and 25 each say so in their own closing sections.
- **One dollar figure only**: the AEC grant to Intelectron, roughly 300,000 dollars (21 file
  02 0:44:10). Everything else in my group is either already logged or commercial colour.
- **`Neil McCasland` is the sharpest unresolved name across my group** and the board already
  has a node for him. See C2.
