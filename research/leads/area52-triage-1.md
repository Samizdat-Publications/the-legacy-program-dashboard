# Area 52 corpus triage, group 1 (lead maps 01 to 05)

**Written:** 2 September 2026, against `research/leads/TRIAGE-BRIEF-AREA52-2026-09-02.md`.
**Scope:** `research/leads/area52-corpus-01.md` through `-05.md` and
`research/leads/area52-absent/group-1.tsv` (133 ABSENT names, batches 01 to 05).

**Nothing here is asserted as true and nothing here has been added to the board.** Every row
records what a named speaker says on a podcast, plus the record that would have to be opened
before any of it could become a claim. `CLAUDE.md` section 2 governs: where a document,
statute or series appears below it is an identifier to verify at the named archive, not a
citation this pass has opened.

**Method.** Board state was read from `data/the-program.json` by loading the 1,000 node ids
and by counting raw string occurrences; every node id named in section C was confirmed
against that file. Where a count of board occurrences is given below, it is that count.

**Pointer format.** `map / file / TS`, where *map* is the corpus batch file
(`area52-corpus-NN.md`) and *file* is that map's own episode or file number. Batch 01
numbers its files 17 to 20; batches 02 to 05 number theirs 01 to 04.

**Counts.** A: 17 rows covering 23 ABSENT names. B: 24 rows covering 26 ABSENT names plus 8
carried in under the brief's `[PHON?]` rule. C: 17 rows. D: 84 names in six groups, plus the
read-aloud exclusions.

**What this corpus is.** Six of the twenty episodes across these five batches are Chris
Ramsay reading a document aloud with no guest, and four of those six are the "Lacerta Files",
a 1999 internet fiction. Two further episodes carry no structural content at all. The real
yield is four interviews, with James Fox, Lue Elizondo, Danny Sheehan and Nick Pope, plus a
thinner one with Avi Loeb.

---

## A. Document-backed candidates

Ranked: rows that would change the board's argument first. Class uses the board's vocabulary.

| # | Name (as in the ABSENT list) | Class | The record that would justify it | Where to look | Why THIS board | Map / file / TS |
|---|---|---|---|---|---|---|
| 1 | **Gordon Gray** | person | His own offices, all of which produce paper: Secretary of the Army 1949-50, Director of the Psychological Strategy Board 1951-53, National Security Adviser 1958-61, President of the University of North Carolina 1950-55 | Truman Library, Psychological Strategy Board files; NARA RG 59 lot files; Official Register of the United States; UNC's own presidential records | Zero occurrences on a 1,000-node board that carries `d-psyop` as a whole domain. The PSB is the executive's own perception-management office in exactly the period this board argues about, and `CANDIDATES-2026-09-02-MICHELS.md` section E held the PSB over for a next pass. Batch 05 then puts Gray at UNC while the Institute of Field Physics, which this board already cites nine times, was running. He is the one name in group 1 that joins the psyop domain to the electrogravitics thread, and he does it through offices rather than through the MJ-12 attribution that made three speakers say his name | 01 / 20 / 0:12:27; 02 / 02 / 0:16:58; 05 / 01 / people list |
| 2 | **University of North Carolina at Chapel Hill** (propose the node as the **Institute of Field Physics**) | institution | The 1957 Chapel Hill conference report the board already quotes in `rias-inc` and `louis-witten`; the Institute's founding endowment and Bryce DeWitt's directorship | DTIC for the conference report, which the board has in hand; the DeWitt papers and UNC's institutional records; Bahnson Company records for the endowment | The board cites the Institute of Field Physics nine times across `louis-witten`, `george-trimble` and `rias-inc` and has no node for it. Section D of the Michels candidates file flagged this exact gap. Batch 05 adds what makes it worth building now: a 1957 Townsend Brown demonstration at Bahnson Laboratories, Winston-Salem, tied to the Institute, which would put `thomas-townsend-brown` on the same institutional node as the RIAS to Martin to `lockheed-martin` chain the 30 August pass built. Cheapest high-value row here | 05 / 01 / people list; near miss `louis-witten.claim` |
| 3 | **Donald Menzel** (batch 02) and **Howard Menzel** (batch 05), one man, Donald H. Menzel | person | His own papers, and the specific finding a named researcher reports from them: a thirty-year NSA association and a CIA Top Secret Ultra clearance | Harvard University Archives, Donald H. Menzel papers; NSA's declassification reading room for any consultancy record; his own three debunking books (1953, 1963, 1977) | The string "Menzel" occurs **zero** times in `data/the-program.json`. The board carries `robertson-panel`, `howard-p-robertson`, `edward-condon` and `condon-committee` and has no node for the era's principal scientific debunker. The clearance claim is Friedman's, from April 1986 access to the papers, and it is the testable part: either the papers say it or they do not. A contradiction here would be worth more than a confirmation | 02 / 02 / people list; 05 / 02 / people list |
| 4 | **JARIC** (Joint Air Reconnaissance Intelligence Centre) | institution | Its own written assessment of the six Calvine photographs and negatives, held in the MoD file | The National Archives, Kew, DEFE 24 and DEFE 31; `uk-defe24` is already a board node. David Clarke's FOI releases are the other route | An imagery-intelligence unit that produced a technical assessment concluding a real, solid, roughly 75-foot structured object is a government analytic product, not a witness. The board's entire Calvine content is one clause on `sheffield-hallam` about Andrew Robinson's 2025 analysis; JARIC occurs zero times. This is the board's own strongest evidence class, from an allied government, and the board's oversight view is currently all American | 05 / 03 / 1:25:17 |
| 5 | **James V. Forrestal** (batch 01) and **James Forrestal** (batch 02), one man | person | The Willcutts Report, the US Navy board of investigation into his death of 22 May 1949, withheld for decades and released under FOIA | The released Willcutts Report; NARA Navy Judge Advocate General records | Three maps repeat that his medical records are sealed. There is an official investigation record, and opening it is how the board adjudicates the claim instead of repeating it. Forrestal is the first Secretary of Defense and the addressee of the memo the whole MJ-12 corpus is built on; the board's only Forrestal content is three occurrences inside `william-l-moore`. A long-withheld official record about the death of the man at the top of the structure is this board's subject exactly | 01 / 20 / 0:12:27; 02 / 02 / 0:18:48; 05 / 01 / people list |
| 6 | **RAF Lakenheath**, and the radar and visual incident of 13-14 August 1956 | event | The Condon Report's own Case 2, the Lakenheath-Bentwaters case, which the study's investigator could not dispose of; and the Blue Book record cards for those dates | The Condon Report full text; NARA RG 341 for Blue Book | The board cites the Condon Report **122** times and carries `condon-committee`, `edward-condon` and `robert-low`. "Lakenheath" occurs **zero** times. The board's argument about Condon is an argument about a study that reached a predetermined conclusion; the sharpest test of that argument is the case the study itself left standing, and the board does not name it | 01 / 20 / 0:08:54 |
| 7 | **House Science and Technology Committee**, and the 1977 Congressional Research Service UFO tasking | document | The CRS report on UFOs prepared in the Science Policy Research Division. The transcript gives the analyst as "Marshall Smith"; **resolution mine: Marcia S. Smith** | The CRS report archive; the Carter Library for the 1977 tasking correspondence | A president asking the legislature's own research arm to compile what the executive holds on UFOs, and getting a public report, is the earliest instance in group 1 of the access question being posed from the congressional side with a published answer. "Congressional Research Service" occurs once on the board, on `waived-usap-mechanism`. This is the historical precedent for `task-force-declassification` and the board has no version of it | 04 / 02 / 0:31:37 |
| 8 | **Donald Keyhoe** | person | NICAP's own publications under his directorship, 1957-69; the CIA's and the Air Force's files on him; the 22 January 1958 CBS broadcast in which his audio was cut mid-sentence | CIA CREST; NICAP's published record; the network's own broadcast record | The board built `nicap` on 2 September, on the CIA's filed copy of *The UFO Evidence*, and carries `roscoe-hillenkoetter`. The hinge between the two, the man who ran NICAP and who put a former Director of Central Intelligence on the record, is prose only: four occurrences, on `roscoe-hillenkoetter` and `nicap`. A promotion rather than a discovery, and the cheapest one in this file | 05 / 02 / people list; near miss `roscoe-hillenkoetter.narrative` |
| 9 | **Albert Einstein** and **Eleanor Roosevelt**, via the alleged 1947 memo "Relationships with Inhabitants of Celestial Bodies" | document | Three items, two ordinary and one not. Ordinary: Einstein to Rev. Louis A. Gardner, 23 July 1952, on Institute for Advanced Study letterhead; Oppenheimer to Eleanor Roosevelt, 19 May 1950. Not ordinary: the 1947 memo itself, which the episode says surfaced online with unknown provenance and independently of the Shandera and Friedman leak | Albert Einstein Archives, Hebrew University of Jerusalem; J. Robert Oppenheimer Papers, Manuscript Division, Library of Congress; Eleanor Roosevelt papers, FDR Library | The two letters either exist in the finding aids or they do not, which settles the frame the 1947 memo hangs on without adjudicating the memo. The memo uses "extraterrestrial biological entities" and is claimed to predate the MJ-12 corpus, so its provenance is a dating question with a testable answer. "Einstein" occurs once on the board, inside `louis-witten`; "Oppenheimer" thirteen times with no node. Michels triage group 1 already proposed Oppenheimer the man, so this row is the paper | 05 / 02 / 0:02:48 to 0:37:44 |
| 10 | **Lord Hill-Norton** | person | His own parliamentary questions and the written answers to them, and his correspondence inside the MoD UFO files | Hansard, House of Lords; The National Archives, DEFE 24 | A former Chief of the Defence Staff and Chairman of the NATO Military Committee using the parliamentary record to press his own ministry is an oversight instrument operated from inside the structure, and it leaves a verbatim public record. The board's oversight view is entirely congressional and entirely American. Pope's "maverick priest" story about him is testimony; Hansard is not | 05 / 03 / 2:10:35 |
| 11 | **Robert Emenegger**, with **Paul Shartle**, **Norton AFB** and **Holloman AFB** (four ABSENT names, one story) | document | The 1974 documentary *UFOs: Past, Present and Future*, which either does or does not contain the eight seconds of Holloman footage the account says survived the cut | The film itself; AFHRA base histories for Norton and Holloman | The checkable core is not a landing. It is that the Air Force granted a film crew unusual base access, offered footage through a named base security manager, and withdrew it, leaving a distributable artefact behind. That is a perception-management event in the board's `d-psyop` domain with a physical object at the end of it. Two independent maps carry it from two speakers, Ramsay reading Lear and Fox relaying Sandler, and the second is explicitly secondhand of secondhand, which the node would have to say | 01 / 20 / 0:21:22; 02 / 01 / 0:32:47 |
| 12 | **Lonnie Zamora**, and the Socorro landing of 24 April 1964 | event | The Project Blue Book case file, which leaves it unidentified, and Hynek's on-site report | NARA RG 341, Blue Book, 24 April 1964 | `project-blue-book` is a board node and this is its most consequential surviving unknown. What makes it a group 1 candidate rather than a general UFO timeline entry is that a former Pentagon programme official ties his engraved-glyph claim back to this specific 1964 case, which turns a 2025 assertion into a test against a 1964 official file. "Zamora" occurs zero times on the board; "Socorro" occurs five times and every one is about the Plains of San Agustin, a different place and a different case | 02 / 04 / 1:02:24; 02 / 01 / 0:37:51 |
| 13 | **Sidney Souers** | person | His two offices: first Director of Central Intelligence, January to June 1946, and first Executive Secretary of the National Security Council, 1947-50 | Truman Library, NSC files; the National Security Act of 1947 | Zero occurrences. The board argues at length about what the NSC was and was not shown, and has no node for the man who built its secretariat. He is named here inside a disputed document, which is a reason to open the real record, not a reason to trust the document | 02 / 02 / people list |
| 14 | **Robert Montague** | person | His command of Sandia Base and the Armed Forces Special Weapons Project field command, 1947-51 | NARA RG 374, Defense Nuclear Agency and AFSWP records; Official Register | `sandia` is already a node and the board's `d-nuc` domain is about custody of the stockpile. Montague sits at the exact military-to-AEC junction that `atomic-energy-act-1946` and `atomic-energy-commission` describe, and the board has no person standing on that junction. Zero occurrences | 02 / 02 / 0:16:58 |
| 15 | **Detlev Bronk** | person | National Academy of Sciences Biographical Memoirs; his NAS presidency 1950-62, his National Research Council chairmanship, and his NACA membership | NAS archives; NARA RG 255 for NACA | Three maps, three speakers, zero board occurrences. The board has no node anywhere at the top of the postwar civilian science-advisory structure, which is where the AEC's and the Air Force's outside scientific advice came from. The MJ-12 attribution is not the reason to build him; the offices are | 01 / 20 / 0:12:27; 02 / 02 / people list; 05 / 02 / people list |
| 16 | **Ron Rewald** | event | *United States v. Rewald*, Ninth Circuit 1989, and the district docket; the CIA's own litigated position on what it would confirm about the proprietary | CourtListener and the federal reporter | A documented CIA commercial front whose public collapse forced the Agency into court over what it would acknowledge. That is the corporate-cover mechanism the board argues about, resting on a published appellate opinion rather than a witness. Note that Sheehan places the matter in the Eastern District of Virginia and the Rewald prosecution was in Hawaii; see section B | 04 / 02 / 1:02:15 |
| 17 | **Strategic Defense Initiative** | program | NSDD-119 of 6 January 1984 establishing the SDI Organization; SDIO annual reports to Congress; the 1986 US-Israel SDI participation agreement | Reagan Library for the NSDD; DTIC for the SDIO reports | Two independent maps, and the board has no node for the largest compartmented research organisation of the period. "SDI" appears 26 times in the board's data and 25 of them are the substring inside "OUSDI". The Lear document's claim that SDI was cover for an anti-EBE weapon is a claim only the appropriations record can adjudicate; Loeb's separate account of an Israeli mass-accelerator project as SDI's first funded project is checkable against the participation agreement. Ranked last in A because both routes lead to budget documents rather than to a UAP record | 01 / 20 / 0:42:30; 05 / 04 / 0:01:42, 0:51:00 |

---

## B. Needs a document

Research questions, not candidates. Rows marked **resolution mine** carry a `[PHON?]` or
`[UNRESOLVED]` name reconstructed under the brief's Malmgren rule; the reconstruction is mine
and is not a fact. Rows marked **not on the list** were carried in under that same rule and
are not among the 133.

| Name | What is claimed | What record would settle it | Map / file / TS |
|---|---|---|---|
| **Chris Bledsoe** | That CIA, DIA, DoD, NASA, the UK Ministry of Defence and Australia's DoD all contacted him directly, including a two-star DIA general, and that metal samples given to DeLonge and Elizondo were declared classified and taken back about a year later | Any contact or custody record from any of the six bodies. He offers no document, date or route for any of it. Three maps name him and none adds paper | 02 / 04 / 1:39:31; 03 / 01 / 1:14:21 to 1:19:48; 05 / 04 / 1:40:47 |
| **John Lear** | That his 29 December 1987 Paranet statement describes a real 1969-71 agreement, a real Groom Lake rebuild and a real captive-EBE custody arrangement | An original Paranet-era copy would establish the document's date and wording, which is all it can establish. The statement is a circulated ufology artefact with a known author and no authenticating body, so under the brief's read-aloud rule nothing inside it is a candidate | 01 / 20 / 0:05:11; 04 / 04 / 0:20:29 |
| **John Glenn** | That the NSA's Director of Policy wrote to him confirming both an Air Force "Aquarius" project and a separate NSA project of that name dealing with communications | The correspondence itself. `project-aquarius` records that NARA searched the NSC's paper and minute indexes and found nothing; a senator's own files are a different search. The letter's named signer is UNRESOLVED in the map | 01 / 20 / 0:47:26 |
| **Project Snowbird** | A project nested inside Aquarius, flight-testing a recovered craft at Groom Lake, said to have continued as of 1987 | A code-word index search at AFHRA or NARA. Nothing else is offered anywhere in the batch | 01 / 20 / 0:48:14 |
| **Lew Allen**, **Richard Helms**, **Vernon Walters**, **Theodore von Karman**, **John Poindexter** | Named as past or then-current MJ-12 members inside a videotape the Lear document describes but does not produce | Nothing can settle the attribution, because the videotape is described at second hand. Kept here rather than in D because four of the five held offices the board may want on other grounds, in particular von Karman for the Air Force Scientific Advisory Board and Allen for the NSA-to-JPL sequence | 01 / 20 / 0:43:20 |
| **Al Hibbs** and the **Jet Propulsion Laboratory** | A 1985 Hibbs quote declining to explain UFO footage, cited inside the Lear document | The broadcast the quote came from. JPL is a Caltech-operated federal laboratory and would be a defensible node on FFRDC grounds, which this corpus does not supply | 01 / 20 / 0:17:55 |
| **Jerome Hunsaker** and **NACA** | Hunsaker as NACA chairman, named as an MJ-12 member | NACA's annual reports. "NACA" occurs zero times on a board that carries `nasa` with no predecessor. The offices are real; the attribution is the document's | 02 / 02 / 0:14:14 |
| **Paul Trent** and **Evelyn Trent** | An unnamed government agency searched Evelyn Trent's home while her husband was away, after the 1950 McMinnville photographs | The Condon Report's Case 46 photographic analysis is the record for the photographs. For the visit there is none. A sighting case, and the map's only tie is the intimidation anecdote | 02 / 01 / 0:12:59 |
| **Paul Smith**, **Angela Ford** | Named as Stargate-lineage remote viewers and instructors | The DIA's Stargate release at CIA CREST names unit personnel. `stargate-program` already names May, Swann, Price, McMoneagle and Geller and names neither of these two, nor Lyn Buchanan | 03 / 04 / 1:10:12; 05 / 01 / people list |
| **Carlos Allende** | Named as adjacent disinformation in the Townsend Brown thread | The annotated Jessup copy held by the Office of Naval Research, and the Varo edition. Provenance material of the class the board already carries on `richard-doty` and `william-l-moore` | 05 / 01 / people list |
| **Nick Cook** | Wrote roughly fifty pages on Townsend Brown and could not resolve his credibility | *The Hunt for Zero Point* itself. It matters because it is the provenance chain behind the 1956 "Electrogravitics Systems" report that `CANDIDATES-2026-08-30.md` section E excluded for want of provenance; naming the book would let the board state that exclusion where a reader sees it | 05 / 01 and 05 / 02 / people lists; near miss `robert-low.claim` |
| **Steven Hadley** (resolution mine: Stephen J. Hadley) | That Hadley oversaw a net assessment around 2003-04 on whether UAP disclosure would be worth it, concluding it would be too disruptive. Relayed by Michels as Puthoff's account | An Office of Net Assessment study register, or NSC records for the period. The claim names an official, a date range and a product type, which is more than most rows here have | 05 / 01 / 1:29:56 |
| **Jimmy Carter** | Filed a UFO report with NICAP as governor of Georgia, and as president-elect demanded a CIA briefing which George H.W. Bush declined to give without a tenure guarantee | The NICAP report form, widely reproduced, and the Carter Library's files on the briefing request. The second half is the structural claim and the one with no document attached | 04 / 02 / 0:30:41 |
| **Oscar Wolf** | An Army clerk assigned to a section of Project Blue Book the government never admitted having, holding over 700 inexplicable incidents; later driven from Area 51 to S4 | A service record. The source is deceased and the account is deathbed testimony relayed by one lawyer and then re-relayed by a second speaker in another batch, which is two removes | 04 / 02 / 0:16:19; 05 / 01 / people list |
| **Clifford Stone** | Told Kirkpatrick's AARO to pull his records, and Sheehan says he told Kirkpatrick directly about both Stone and the classified Blue Book photographs | A FOIA to AARO for its holdings on Stone. The board caps AARO-sourced claims at Tier 2, and this one is about what AARO was told rather than what AARO said | 04 / 02 / people list; near misses `ttsa.desc`, `anna-paulina-luna.claim` |
| **Church of Scientology** and the Guardian's Office | That the July 1977 FBI search warrant was struck down as a general warrant after Sheehan obtained a restraining order, and that Sheehan personally read Ingo Swann's remote-viewing reports filed with the Guardian's Office | The suppression litigation docket from the 1977 raids, and the 1979 stipulation of evidence. Note the caption gives Hubbard's wife as "Susan"; the documented name is Mary Sue Hubbard | 04 / 02 / 1:11:13 to 1:24:04 |
| **Eastern District of Virginia** | Described as "the CIA court", and as the venue where a federal judge issued Sheehan a Q clearance on the spot in the Rewald matter | The Rewald docket, which is District of Hawaii. A Q clearance is a Department of Energy access authorisation, not a court's to grant. Both halves of the claim need the docket before either is repeated | 04 / 02 / 1:02:15 |
| **1992 United States Defense Department Policy Planning Guidance document** | Drafted by Cheney's staff from the first Monday after 31 December 1991, leaked to the *Washington Post*, and relevant to UAP secrecy because its authors "all know about the UFO stuff" | The declassified draft is public and findable. Recorded here so a later pass does not mistake a genuinely released document for a relevant one: it contains no UAP material, and the only link to this board is a speaker's assertion about what its authors knew | 04 / 02 / 1:55:49 |
| **Smith-Mundt Act** (not on the list; caption `Smith and Bertz`, **resolution mine**) | That PSYOP doctrine's domestic-audience ban is real on paper and routinely circumvented by personnel who leave the service for marketing and political strategy | The statute: 62 Stat. 6 of 27 January 1948, 22 U.S.C. 1461-1a, and section 1078 of the FY2013 NDAA. The statute is easy; the evasion claim cannot be documented from it and would need something else entirely. The board has zero occurrences of Smith-Mundt and a whole `d-psyop` domain | 03 / 04 / 0:38:36 |
| **"Operation Interloper"** (not on the list) | A deliberate lure operation using a carrier strike group's nuclear signature to draw UAP into observable range, with Joint Staff and intelligence-community approval, killed at the last minute | Joint Staff tasking records, or the AATIP file set. No date is given beyond Elizondo's own tenure. Sheehan describes a similar lure-and-capture programme in a different batch without connecting the two | 02 / 04 / 0:48:55; 04 / 02 / 2:26:02 |
| **"Fast Walker" / "DSO office"** (not on the list; **resolution mine**: the Defense Support Program) | An Air Force effort tracking very fast objects from space, which also picked up objects trailing submarines | The Michels pass already opened the 2013 USNORTHCOM FOIA denial letter on fastwalkers and slowwalkers and recorded that no opened government document equates fastwalker with DSP. This row adds a second speaker using the term and a garbled office name, and does not change that finding | 02 / 04 / 0:37:03 |
| **US Space Command letter on the 8 January 2014 Pacific fireball** (not on the list) | That US Space Command wrote to the White House putting the object at 99.999% likely interstellar, released after Loeb complained as chair of the National Academies Board on Physics and Astronomy | The letter. It is a real government document by Loeb's own account and the strongest single item in batch 05; the board carries `im1-pacific-expedition-2023` without it | 05 / 04 / 0:26:22 |
| **Five Eyes UAP working group, first meeting "May 23"** (not on the list) | AARO testified under oath that it convened a Five Eyes working group at the Pentagon with all five nations represented | The testimony transcript. Pope gives no year, and that is a genuine gap rather than a transcription artefact. The board carries Five Eyes four times, on `navy-range-fouler-reports` and `dodig-2021-000806-foia` | 05 / 03 / 1:49:40 |
| **Marcia S. Smith** (not on the list; caption gives "Marcia" once and "Marshall" thereafter, **resolution mine**) | Tasked by Carter through the House Science and Technology Committee to compile the government's UFO holdings, documents and witnesses | Separable from row A7: the report is the record, the person is a research question. The transcript's own two spellings for one individual are flagged in the map | 04 / 02 / 0:31:37 |

---

## C. Corrections to existing nodes

What these lead maps record about nodes the board already carries. Node ids confirmed against
`data/the-program.json`. Every podcast claim below would enter at Tier 2 in the form "on Area
52 DEBRIEFED, <date>, <speaker> said", per the Michels section C convention.

| Node id | What the corpus adds that the board seems not to have | Map / file / TS |
|---|---|---|
| `nick-pope` | Three things the node does not carry: JARIC's assessment of the Calvine photographs; the MoD's one-page scripting system, "key messages" above and "defensive lines to take (if pressed)" below, with "of no defence significance" as the standard line used even on cases Pope considers plainly significant; and that the same vetting reached his fiction, with one real-world event ordered removed from a novel manuscript | 05 / 03 / 1:25:17, 1:53:18, 1:58:25 |
| `dopsr` | The fiction-vetting point above. DOPSR reviewed Pope's Rendlesham nonfiction alongside UK MoD clearance, and the same process was applied to two science-fiction novels and a counter-terrorism thriller | 05 / 03 / 1:59:18, 2:04:51 |
| `sheffield-hallam`, `david-clarke-uk` | The board's Calvine content is Robinson's 2025 photographic analysis. The corpus adds the provenance chain in front of it: Clarke located a redacted FOI release naming **Craig Lindsay**, the RAF press officer who kept one of five or six original prints and has since surfaced an image the MoD will neither confirm nor deny. The lead maps spell him Lindsey; the public record gives Lindsay | 02 / 01 / 0:18:36; 05 / 03 / 1:23:31 |
| `jay-stratton`, `david-grusch` | The node already carries the 2019 tasking. Pope adds that the forty-source investigation was Stratton's assignment across the whole intelligence community rather than a personal pursuit, and attributes to Grusch the characterisation of some recovered material as not crashed but deliberately left, "gifts from the gods" | 05 / 03 / 1:20:00 |
| `jon-kosloski` | Fox's account of an AARO skiff visit: Kosloski present ten to fifteen minutes, an AFOSI officer for the whole of it, the line "I can't part my own hair without approval from the DoD" offered on the record, and the claim that Fox's own documentary is mandatory viewing for anyone joining the task force or AARO. The board's Tier 2 cap on AARO-sourced claims does not bind here, because the claim is about what an AARO director said | 02 / 01 / 1:47:48 to 1:55:55 |
| `luis-elizondo` | Three items: engraved rather than painted glyph-like markings on more than one craft type, which he traces back to Socorro 1964; "Operation Interloper"; and the allegation that two CIA officers leaked Grusch's medical and PTSD records within 24 hours of the July 2023 testimony, which he calls a HIPAA violation. No named source and no document for the third | 02 / 04 / 1:02:24, 0:48:55, 1:55:42 |
| `daniel-sheehan` | The node's Rule 11 liability paragraph is right and should stay; this corpus is a further instance of the same evidentiary pattern. What the node lacks: the Oscar Wolf deathbed account, the New Madison Building Blue Book microfiche visit and the symbol tracings lost in a 1980s flood, the "documents first" subpoena doctrine naming Lockheed, Northrop Grumman, MITRE and Battelle, and the disclosure-bill counts (17-0 in committee, 94 of 100 on the floor, 23 of 64 pages surviving the House) | 04 / 02 / 0:16:19, 0:35:09, 2:05:10, 2:18:37 |
| `uapda-2023`, `s2226-118` | Sheehan's vote counts above are checkable against the Senate roll call on S.Amdt. 797 and against what survived into P.L. 118-31. He never names the bill, calling it throughout "the control disclosure act"; the map flags that. If the counts are right they belong on the legislation node, and if they are wrong that is the more useful finding | 04 / 02 / 2:05:10 |
| `mike-turner` | Named as the member who kept the remaining pages off the House floor by lobbying Speaker Johnson, with his district's Wright-Patterson geography given as the reason. The board carries `mike-turner` and has Mike Johnson in prose on three nodes | 04 / 02 / 2:07:01 |
| `avi-loeb`, `galileo-project`, `im1-pacific-expedition-2023` | The US Space Command letter (see B); a second expedition costed at about $6.5 million and unfunded as of the interview; and Loeb's stated funding asymmetry, roughly $10 billion for the Habitable Worlds Observatory against a few million total and zero federal dollars for technosignature work. Separately, Michels claims Lazar used the name "Project Galileo" for a 1980s propulsion project and Loeb says on camera he had never heard it, which is a naming coincidence asserted by a third party and corroborated by neither | 05 / 04 / 0:26:22, 0:29:01, 0:37:44, 1:36:18 |
| `thomas-townsend-brown` | The node correctly separates the patents from the literature. The corpus adds two Tier 3 items: a 1957 demonstration at Bahnson Laboratories, Winston-Salem, tied to the Institute of Field Physics while Gordon Gray was UNC's president; and a 1950 Pearl Harbor security incident after which Brown is said to have run deliberate disinformation about his own results, publishing an ion-wind experiment as a decoy. The caption reads "Bonsen Labs"; the Bahnson resolution is mine, and the board already carries Bahnson three times on `louis-witten` | 05 / 01 / people list |
| `harald-b-malmgren`, `richard-m-bissell-jr`, `l-groom-lake` | Michels states that Bissell briefed Malmgren on other-world technologies in the early 1960s and infers from it that such technology was part of Area 51's **founding** rationale rather than an addition eight years later. The board's Bissell node rests on the CIA's own U-2 and OXCART history, which gives the site as found on 12 April 1955 for the U-2. Record the inference as the transcript's; the opened document does not support it | 05 / 01 / 2:06:28 |
| `jim-penniston`, `rendlesham-1980` | The node names the binary download and says it made him easier to dismiss. The corpus adds the specifics a later pass would need to adjudicate it: sixteen notebook pages of handwritten binary written two to three days after under a described compulsion, the decoded English string, and a coordinate list. Separately Pope reports a line in an untitled British intelligence UAP assessment about longer-than-normal exposure to UAP radiation at Rendlesham, and says a similar line recurs in an AAWSAP human-effects paper. Neither report is titled, which is the gap | 05 / 03 / 1:04:52, 0:55:37, 0:56:33 |
| `stargate-program` | The board's node is already more precise than any speaker in this corpus, which is itself worth recording. Three additions it could take: Angela Dellafiora Ford, Paul H. Smith and Lyn Buchanan as unit personnel; Dale Graff's move from the Air Force side to the Army programme; and the three figures two guests state as established fact, 17 of 19 agencies, 505 missions over 20 years, and 141 drug-interdiction taskings, which are checkable against the 1995 American Institutes for Research evaluation the node already cites. Establishing whether those figures are the AIR report's or nobody's is the useful work | 03 / 02 / 1:53:15; 03 / 04 / 1:10:12 |
| `nicap` | Sheehan says Carter filed a UFO report with NICAP as governor of Georgia. The node is one day old and was built on the CIA's filed copy of *The UFO Evidence*; the Carter report form is a separate and widely reproduced NICAP artefact | 04 / 02 / 0:30:41 |
| `jake-barber`, `northrop-grumman` | Sheehan draws a distinction the board may want to carry: Barber's retrievals are of craft already in the possession of the Northrop Grumman test range, as against a separate lure-and-capture programme with, he says, confirmed successes | 04 / 02 / 2:26:02 |
| `ben-rich` | Sheehan says the Wilson-Davis memo's private-sector contact was "almost certainly Ben Rich", reasoned from Rich's own reported remarks to former classmates. The caption gives "Ben Rice". That is an inference from hearsay and should be carried as one if at all | 04 / 02 / 2:19:32 |

---

## D. Noise, and why

84 of the 133 names, in six groups. Names are listed in full so the next pass can see what
was excluded and disagree with it.

### D0. Cross-check defects, not leads (5 names)

Reported first because they are a tooling finding rather than a research one.

| Name in the list | What the board actually has |
|---|---|
| Stargate (Project) | `stargate-program`, a full node. The parenthetical defeated the matcher |
| Jamie Shandera | `jaime-shandera`, a node. The near miss printed points at `house-oversight-committee`, which is a different Jamie |
| Dr. Edwin May | `stargate-program` names Edwin C. May. The near miss was printed and the verdict still came back ABSENT |
| Yuri Geller | `stargate-program` names Uri Geller |
| FBI | "FBI" occurs **347** times in `data/the-program.json`, and the row carries no near miss at all |

Four further rows are one person or place entered twice under two spellings: James V.
Forrestal and James Forrestal; Donald Menzel and Howard Menzel; George Bush Sr. and George
H.W. Bush; and Holloman AFB, which does carry a near miss to `l-white-sands.desc`.

### D1. Celebrities and public figures named in passing (13 names)

No structural claim attaches to any of them: Arthur C. Clarke, Isaac Asimov, Dan Aykroyd,
Larry King, Steven Spielberg, Deontay Wilder, Elon Musk, Jason Fung, Joe Rogan, Michael
Bisping, Kurt Russell, Margot Robbie, Stephen Hawking.

### D2. Guests' biographies, their circles, and authors cited for their books (31 names)

John White, Michael P. Masters, Andrew Greenwood, Kim Arnold, Randall Nickerson, Shane Ryan,
Dr. Diane Powell, Edward Bernays, Hakim Isler, Joseph Goebbels, Rupert Sheldrake, Stephen K.
Hayes, Tom Campbell, Bill Davis, Bill Toddman Jr., Bo Gritz, Dan Burish, F. Lee Bailey,
Stephen Bassett, Bud Hopkins, David Jacobs, Donald Burleson, Frank Edwards, Garrett McNamara,
Nicole McNamara, Otto Struve, Phil Schneider, President's Council of Advisors on Science and
Technology, Richard Hoagland, Ronald Mallett, Sean Ryan.

Two notes. PCAST is here rather than in B because Loeb's membership is his own biography and
bears on nothing structural. John Mack is not on the ABSENT list and is already in board prose
on `daniel-sheehan` and `ralph-blumenthal`; the abduction-research trio is excluded as a group.

### D3. Places and institutions named in passing (13 names)

Datil NM, Sunspot NM, Ariel School, Brigham Young University, El Indio TX, STS-64, Fort Bragg,
HeartMath Institute, Vatican, S4, Borderland Sciences Research Associates, Cornell University,
Vera Rubin Observatory.

Brigham Young is worth one line because it is the only one a speaker builds a claim on: Fox
raises, as his own speculation prompted by an unnamed source, that agencies recruit
disproportionately from BYU, and ties it to an unnamed FBI discrimination lawsuit with no case
name, date or citation. That is the shape section 2 of `CLAUDE.md` forbids.

### D4. General-history figures named only inside a disputed document (3 names)

Harry Truman, Dwight Eisenhower, James H. Doolittle. The board already carries Truman 25 times
and Eisenhower 34 times in prose, and the Doolittle Spitsbergen errand appears only in the Lear
statement. The other officeholders named the same way went to section B instead, because their
real offices may be wanted for other reasons.

### D5. Present-day political, legal and finance names used for positioning (19 names)

George Bush Sr., George H.W. Bush, Brown Brothers Harriman, Union Banking Corporation, George
Herbert Walker, Dan Crenshaw, Doug Feith, Paul Wolfowitz, Richard Perle, Scooter Libby, John
Thune, Pam Bondi, Justice Department, Fritjof Capra, Gorbachev Foundation, State of the World
Forum, Jim Garrison, Mikhail Gorbachev, L. Ron Hubbard.

Sheehan's "deep background" chain from pre-war US finance to German reconstruction is offered
by him as an aside and is developed nowhere in the batch. The four 1992 DPPG drafters are here
rather than in B because the document, not its authors, is the checkable object, and it has its
own B row.

### Read-aloud documents excluded, and why

Required by the brief. Six of the twenty episodes across these five batches are a document read
aloud rather than testimony.

| Document | Where | Why nothing inside it is a candidate |
|---|---|---|
| The Lacerta Files, parts 1 to 4 | 03 / 03, and 04 / 01, 03 and 04 | A 1999 anonymous internet document whose own translator states the alleged non-human subject edited it. Fiction, across four whole episodes. The maps record only Ramsay's real-world asides, and even those are thin |
| John Lear's Paranet statement, 29 December 1987 | the whole of 01 / 20 | A circulated ufology artefact with a known author and no authenticating body. Names existing only inside it are excluded outright: the Los Alamos "YY2" designator, "Pine Town NM", Sgt. Jonathan P. Luet, EBE1 to EBE3, the Dulce 66-soldier incident, the alleged 1969-71 agreement. Real officeholders named inside it were carried to A or B on the strength of their offices and never on the document's say-so |
| The MJ-12 Eisenhower Briefing Document of 18 November 1952, with the Truman-Forrestal memo of 24 September 1947 | the whole of 02 / 02 | The board already carries `mj-12-documents` and `majestic-documents-archive`. Attachments A to G are named in the text and none is produced. Nothing inside is a candidate on its own; the twelve named members were assessed on their real offices |
| The alleged 1947 Einstein and Oppenheimer memo | the whole of 05 / 02 | Carried to A9 as a **document to be searched for** in two named archives, not as content. Ramsay says on air it is unauthenticated. Its supporting correspondence is ordinary archival material and is the part worth opening first |

---

## E. Two things a later pass should not re-derive

1. **Batch 01 episodes 17, 18 and 19 contain no structural content**, and the mappers grepped
   them against the full keyword list to establish it. With the four Lacerta files that is
   seven of twenty episodes with nothing in them.
2. **This corpus produces no FOIA case numbers, no accession numbers, no contract values and no
   dated memoranda of its own.** The only figures anywhere in group 1 are Senate vote counts, a
   $22 million panel-staffing proposal, a $6.5 million unfunded expedition and Loeb's funding
   comparison. Every candidate in section A points at a record held somewhere else, which is
   why the "where to look" column matters more here than it did for the Michels corpus.
