# Verified dossier: nuclear-facility witnesses and the documentary seam beneath them

**Status: research output, not board content.** Nothing here has been merged into `research/`,
into `data/*.json` or into any node. No file in this repo has been edited by this session
except this one. No pipeline was run, no git operation performed.

**Verified 19 September 2026.** Every URL in section 2 was opened by this session on that
date and returned the document described. `CLAUDE.md` section 2 governs: nothing is asserted
here that was not opened. Walls are recorded as walls in section 2b. Where a document was
downloaded by curl and its text extracted locally rather than summarised by a fetch tool,
the row says so, and the quoted text in the body is the extracted OCR, warts included.

**Written under `CLAUDE.md` section 2a and `notes/TRIAGE-RULE-2026-09-19.md`**, both read in
full at the start of this pass. Section 2a widens ADMISSION and changes NOTHING about
GRADING. Every claimant proposed below is proposed at Tier 2 or Tier 3 and carried at that
tier, with the provenance of the claim recorded as section 2a requires: who found this
person, by what route, what they said before an interested party contacted them, whether
they were given another witness's account first, and whether the accounts agree on substance
while diverging on detail.

---

## 0. Board state, read by this session

Read by loading `data/the-program.json` and testing `id` membership across `people` and
`entities` (1,057 nodes). **The board is substantially richer in this area than the brief
assumed, and several ids the brief did not name already exist. Do not create second ids for
any of these.**

**PRESENT - enrich, never duplicate:**
`malmstrom-echo-flight-1967`, `minot-1968`, `minot-1966`, `sac-overflights-1975`,
`big-sur-1964`, `kirtland-manzano-1980`, `rendlesham-1980`, `vandenberg-2003`,
`l-malmstrom`, `l-kirtland`, `l-vandenberg`, `l-raf-woodbridge`, `robert-salas`,
`robert-hastings`, `robert-jacobs`, `kingston-george`, `charles-halt`, `larry-warren`,
`halt-memo`, `doc-341-smw-history-1967`, `npc-2010-ufos-nukes`, `clear-intent-1984`,
`prp-nuclear-weapon`, `project-blue-book`, `blue-book-special-report-14`,
`afosi-kirtland-file`, `norad-northcom`, `john-greenewald`, `the-black-vault`,
`jesse-michels`, `american-alchemy`, `richard-doty`, `kevin-randle`, `aaro`, `usaf`,
`d-nuclear`, `d-nuc`, `d-witness`, `d-coverup`, `d-disclosure`.

**ABSENT - the gaps this pass is filling:**
`l-loring`, `l-wurtsmith`, `l-minot`, `l-ellsworth`, `l-warren`, `l-grand-forks`,
`loring-1975`, `wurtsmith-1975`, `malmstrom-1975`, `warren-1965`, `ellsworth-1977`,
`frederick-meiwald`, `robert-jamison`, `patrick-mcdonough`, `dwynne-arneson`,
`bruce-fenstermacher`, `jerry-nelson`, `walter-figel`, `eric-carlson`, `james-carlson`,
`robert-kaminski`, `bradford-runyon`, `florenz-mansmann`, `mario-woods`, `michael-johnson`,
`strategic-air-command`, and every document id proposed in section 9.

**One integrity note on the check itself.** The first run of the membership test in this
session reported `robert-jacobs` and `big-sur-1964` ABSENT; two subsequent runs, plus a
`grep -c '"id": "robert-jacobs"'` returning 1, report them PRESENT. The later result is the
correct one and the nodes exist. The first run is recorded here rather than silently dropped
because a triage brief that trusts a single membership check can create a duplicate id, and
this pass came one step from doing exactly that.

---

## 1. Summary

| # | Question | Verdict |
|---|---|---|
| 1 | Is the 1975 overflight sequence documentary rather than testimonial | **YES, decisively, and it is the strongest seam in the subject.** The NMCC Memorandum for the Record of 29 October 1975 over the signature of a serving brigadier general, the 24th NORAD Region Senior Director's Log for 7-19 November 1975, and the CINCNORAD four-part message of 11 November 1975 are government operational records, opened in full or near-full text by this session. Tier 1 for what they record |
| 2 | What do the 1975 documents actually say | **They record unidentified low-level intrusions over nuclear weapons storage areas and Minuteman fields, failed interception, and command-level escalation to the Joint Staff, the State Department and Canadian authorities.** They do not use the word UFO in the Loring traffic; they say "unidentified helicopter". The NORAD logs do say UFO, repeatedly, in their own voice |
| 3 | Echo Flight, 16 March 1967: documented or testimonial | **THE SHUTDOWN IS DOCUMENTED. THE UFO IS NOT, IN THE RELEASED PAPER.** The 341st SMW unit history states the shutdown as fact and states, in one sentence, that the UFO rumours "were disproven". Section 5 quotes it in full |
| 4 | Echo Flight and Oscar Flight: same event | **NO, AND THE LITERATURE'S CONFLATION IS NOW TRACEABLE TO A DATE CHANGE BY THE CLAIMANT'S OWN SIDE.** Hastings and Salas now place Oscar Flight on 24 March 1967, eight days after Echo Flight, on the strength of Robert Jamison's recollection. Oscar Flight appears nowhere in the 88 released pages of the unit history |
| 5 | What the engineering investigation concluded | **"The investigation teams at Malmstrom were unable to determine a logical cause for the incident"**, then, after Boeing bench testing, **"it appears that the cause of the Echo Flight problem was of the EMP or electrostatic nature"**. Both quoted verbatim in section 5 |
| 6 | Hastings as aggregator | **HE IS THE FIELD'S PRINCIPAL AGGREGATOR AND ITS PRINCIPAL CIRCULAR-REPORTING RISK, in the same structural way as the Disclosure Project, and worse in one respect: several of the key corroborating statements exist only as his own tape-recorded telephone calls.** Section 7 |
| 7 | Did any of these witnesses speak before an interested party reached them | **Salas: essentially no - 1996, and he approached the press himself. Figel, Meiwald, Jamison, Kaminski: no; every one of them reached the public through Hastings or Salas. Jacobs: yes, and it is the exception that proves the value of the test - he published in 1982 and 1989 and was answered by name by a hostile participant. Michael Johnson: nothing whatever** |
| 8 | The case against the Malmstrom UFO reading | **TWO SEPARATE CASES, BOTH DOCUMENTED, AND THEY ARE NOT THE SAME CASE.** (a) the engineering/EMP explanation, which is in the Air Force's own history and is not a sceptic's construction; (b) James Carlson's dispute with Salas, which is a family-evidence dispute conducted in public by the son of the Echo Flight commander. Section 8 |
| 9 | Ellsworth 1977 | **Mario Woods is a thirty-year public witness. Michael Johnson is a 2026 production of the publishing party, located from a viewer tip, with no dated pre-contact statement about the event in existence.** Proposed as a node at Tier 2 with the provenance recorded exactly. Section 10 |
| 10 | A board error found in passing | **`malmstrom-echo-flight-1967` attributes to "Col. Robert Mansmann" letters of 30 January 1983, 8 March 1983 and 6 May 1987 about the Echo Flight technical investigation. Those letters are Maj. Florenz J. Mansmann's, and they are about BIG SUR, September 1964, not about Malmstrom.** Section 12 |

**The six findings that matter, in order:**

1. **The 1975 sequence is not a UFO record that happens to have documents. It is a nuclear
 security record that happens to be unexplained.** The NMCC memorandum's subject line is
 "AFB Penetration". The traffic goes to CJCS, DJS, J-30 through J-38, CSA, CNO, CSAF, CMC,
 the DIA and NSA representatives and the CIA representative. A Major General of the Army
 Staff personally approved rules of engagement for a National Guard helicopter - no
 apprehension, no border crossing, tracking and identification only. That is what the
 paper is: a three-day command-level flap over an unidentified rotary-wing intruder at a
 nuclear weapons storage area, escalated to the State Department's Canadian desk.
2. **The single most quoted line in the entire subject is in the unit history, and it cuts
 the other way.** Page 38 of the January-March 1967 341st SMW history: *"Rumors of
 Unidentified Flying Objects (UFO) around the area of Echo Flight during the time of fault
 were disproven. A Mobile Strike Team, which had checked all November Flight's LFs on the
 morning of 16 March 67, were questioned and stated that no unusual activity or sightings
 were observed."* In the 88 released pages, "Unidentified Flying Object" occurs exactly
 once, and that is the occurrence.
3. **The same document is equally destructive to the debunk.** Same investigation, page 17:
 *"The investigation teams at Malmstrom were unable to determine a logical cause for the
 incident."* The EMP conclusion arrives three months later and arrives as an inference from
 a negative: *"Due to the fact that the power tests were essentially negative, it appears
 that the cause of the Echo Flight problem was of the EMP or electrostatic nature."* Both
 sides quote half of this document. The board should carry both halves in the same node.
4. **Every substantive Echo Flight corroboration of the UFO reading reaches the public
 through one man's telephone.** Walt Figel's admission exists as Hastings's audio tapes of
 calls in 2008, 2009 and 2010. Frederick Meiwald's Oscar Flight elaboration exists as a
 1996 letter to Salas that Salas publishes and a tape-recorded call in August 1996, plus a
 6 May 2011 call with Hastings. Robert Kaminski's Boeing account exists as a 1997 letter to
 Jim Klotz. Robert Jamison's date for Oscar Flight, which is the load-bearing fact that
 separated Oscar from Echo, is Hastings's interview. None of these four men published
 anything about it under his own name first. That is the Disclosure Project structure
 exactly, and `CLAUDE.md` section 2 applies to it in full.
5. **Robert Jacobs remains the shape the board should want, and this pass confirmed it from
 the source.** Kingston A. George, *Skeptical Inquirer* Vol. 17, Winter 1993, pp. 180-187,
 read in full from the Center for Inquiry's own PDF: George names himself the project
 engineer in his opening line, writes that *"Bob was named the on-site commander by the
 1369th Photo Squadron and managed the logistics of the operation at the Big Sur
 location"*, publishes two group photographs and captions Jacobs into both, names Major
 Florenz Mansmann and Chief Warrant Officer Guy Spooner in the caption, concedes Jacobs's
 point about lasers, and disputes only what was on the film. A hostile participant
 confirming service, unit, role and presence is worth more than five friendly ones.
6. **The 1975 NORAD log names Minot Air Force STATION, not Minot Air Force BASE, for its
 10 November 1975 entry.** Secondary accounts routinely render this as Minot AFB and fold
 it into the SAC-base sequence. The log's own words are *"UFO sighting reported by Minot
 Air Force Station"*, a radar site. This matters for the base-hub graph: the entry belongs
 to a different installation from the 91st SMW's missile field, and a degree count on
 `l-minot` that silently absorbs it is a degree count that lies.

---

## 2. Sources opened

All opened 19 September 2026.

| URL | What it is | What it establishes |
|---|---|---|
| https://archive.org/download/MalmstromAirForceBaseIncident/Malmstrom%20Air%20Force%20Base%20Incident%20%E2%80%93%20March%2016,%201967%20NORAD%20logs_djvu.txt | archive.org OCR text, 5,628 bytes. Route: curl to local file, read whole. **The item is MISTITLED**: it says "March 16, 1967 NORAD logs" and its contents are the 24th NORAD Region Senior Director's Log for 7-19 November 1975 | The full verbatim log, quoted in section 3. Also the release attestation at its foot: "TERRENCE C. JAMES, Colonel, USAF, Director of Administration", with "Cy to: HQ USAF/DAD, HQ USAF/JACL", and page stamps 450-452 plus a control number 000974, showing it is an extract from a larger paginated FOIA compilation |
| http://www.nicap.org/reports/751027loring_1-6.htm | NICAP report page. Route: curl, HTML stripped locally, read whole | The complete text of the NMCC Memorandum for Record of 29 October 1975 subject "AFB Penetration", its distribution list, and four successive DDO UPDATEs with their source message citations. Quoted in section 3 |
| http://www.nicap.org/intsac.htm | NICAP article "UFOs Intrude Into SAC Base Weapons Areas". Route: curl, stripped, read whole | The CINCNORAD 11 November 1975 four-part message excerpt verbatim; the Loring teletype phrase "definitely penetrated the LAFB northern perimeter"; the named Loring and Wurtsmith witnesses with ranks and squadrons |
| http://www.nicap.org/articles/CI-Loring.htm | NICAP, sourced to *Clear Intent* pp. 16-26 | Names and units of the 27-28 October 1975 Loring witnesses; an OSI teletype of 29 October 1975; an OSI letter of 21 April 1977 titled "Overflight of USAF Installations by Unidentified Aircraft". **Note: it reproduces no document headers, and it is a secondary page quoting a 1984 book** |
| http://www.nicap.org/articles/CI-Wurtsmith.htm | NICAP, "Wurtsmith and Others" | The Wurtsmith documentary chain: Capt. Myron Taylor's Memo for the Record of 18 January 1979 to the 379th Bomb Wing historian; SSgt Paul J. Cahill's "Research Record of Events" of 17 January 1979 and its finding that the Oct-Dec 75 Wing History contains no reference to the incident; the NORAD Senior Director's Log entry of 31 October 1975; and the Minot, Grand Forks, Cannon, Eglin and Fort Ritchie entries listed in section 4 |
| https://www.nicap.org/babylon/751030_wurtsmith.htm | NICAP case page, 30 October 1975 Wurtsmith | The NORAD Command Director's Log entry "31 Oct 75/0445Z", the KC-135 crew names, and Col. Boardman as wing commander |
| https://rr0.org/time/2/0/0/6/02/24/Hastings_UfosightingsAtIcbmSites/Malmstrom_1975/index.html | rr0.org mirror of Hastings's Malmstrom 1975 material | The same 24th NORAD Region log entries, independently rendered; and two further named men, SSgt Joseph M. Chassey and Lt Col Robert Peisher (USAF Ret.) |
| https://rr0.org/time/2/0/0/6/02/24/Hastings_UfosightingsAtIcbmSites/Warren_1965/ | rr0.org mirror, F. E. Warren 1965 | The 1 August 1965 Project Blue Book telephone log: logged by Lt. Anspaugh, 0130 to 0440, callers Capt. Snelling, Col. Johnson (base commander), Col. Williams (CO, Sioux Army Depot) and Capt. Howell; site designators E Site, G Flight, Quebec Flight, H-2, B-4; **first published by J. Allen Hynek in "The UFO Experience" (1972)**, which is the dated artefact that fixes the claim |
| https://www.twz.com/35674/the-bizarre-mystery-of-unexplained-aerial-incursions-over-loring-air-force-base | The War Zone (TWZ), aviation trade press | An independent non-UFO outlet working the same FOIA paper. Gives the OPREP phrase "It is our opinion that the unknown helicopter has demonstrated a clear intent in the weapons storage area, is smart and a most capable aviator", and a SAC security police message captioned "Defense Against Helicopter Assault" |
| https://documents.theblackvault.com/documents/ufos/malmstromufo.pdf | **THE CENTRAL DOCUMENT OF THIS PASS.** 15,116,122 bytes, 88 pages, PDF 1.7. Route: curl to local file, text extracted with pypdf (114,559 characters), read and grepped | John Greenewald Jr's FOIA request of 9 May 2001 to 341 CS/SCBR; the reply of 14 June 2001 from HQ 341st Space Wing signed Marty S. Stephens, releasing excerpts of five quarterly 341st SMW histories (Jan-Mar 67, Apr-Jun 67, Jul-Sep 67, Oct-Dec 67, Jan-Mar 68) and stating "We do not have any audio or video tapes, or documents of any personnel injured"; and the entire Echo Flight investigation narrative quoted in section 5 |
| https://cdn.centerforinquiry.org/wp-content/uploads/sites/29/1993/01/22165151/p77.pdf | Kingston A. George, "The Big Sur 'UFO': An Identified Flying Object", *Skeptical Inquirer* Vol. 17, Winter 1993, pp. 180-187. 8 pages, 1.3 MB. Route: WebFetch saved the binary locally, text extracted with pypdf, read in full | George's self-identification as project engineer; his confirmation of Jacobs's unit, appointment and presence; the two captioned photographs; Major Florenz Mansmann and CWO Guy Spooner named; the "Buzzing Bee" Atlas launch dated 22 September 1964; the decoy-and-packing-material explanation; the security reaction and the destruction of the film; his own citation to "George, Kingston A. 1964. *Preliminary Report on Image Orthicon Photography from Big Sur*. Headquarters 1st Strategic Aerospace Division Operations Analysis Staff Study, October 13" |
| https://ufohastings.com/articles/the-ufos-nukes-connection-press-conference | Hastings's own page on the 27 September 2010 National Press Club event | The roster with ranks, units, bases and dates (section 7); that affidavits were executed by McDonough, Salas, Jamison, Arneson, Fenstermacher and Halt; and Hastings's own count, "I have interviewed more than 160 U.S. Air Force veterans regarding their involvement in UFO incidents at nuclear weapons sites" |
| https://ufohastings.com/about | Hastings's biographical page | A **different** count on the same site: "To date, Hastings has interviewed more than 150 military veterans". The page does **not** state how he located them and does **not** state whether any had spoken publicly before he made contact. Both absences are findings under section 2a |
| https://www.ufohastings.com/articles/the-echo-and-oscar-flight-incidents | Hastings's own article separating the two flights | Echo Flight 16 March 1967; Oscar Flight 24 March 1967 "per Capt. Jamison's information"; named witnesses Figel, Eric Carlson, Salas, Meiwald, Jamison, Henry Barlow (Minuteman technician), Robert J. Kaminski (Boeing); a tape-recorded telephone conversation with Meiwald in August 1996 and a further call on 6 May 2011; and that Salas located Meiwald himself in summer 1996. **The article does not reproduce the 1 October 1996 letter's text; it refers the reader to Hastings's own "Witch Hunt" article** |
| https://www.theufochronicles.com/2011/06/echo-flight-icbm-incident-retired-usaf.html | UFO Chronicles, June 2011, republishing Hastings | That Figel's account exists as Hastings's audio recordings of three telephone conversations in 2008, 2009 and 2010; that Eric Carlson, sitting two feet away, has no recollection of a UFO report; and the polemical register in which this dispute is conducted |
| https://www.metabunk.org/threads/ufos-at-nuclear-weapons-sites-salas-malmstrom-eagle-flight-skeptical-resources.3284/ | Metabunk skeptical resource thread | James Carlson's own titles and positions: a 357-page work "American, Credulous" and a shorter "Echo Flights of Fantasy - Anatomy of a UFO Hoax"; the Nalty 1969 official history quotation; and the enumerated factual disputes with Salas listed in section 8 |
| https://timhebert2.blogspot.com/2011/08/disproving-ufo-case.html | Tim Hebert, "Echo Flight: The Makings of a UFO Myth" | A sceptic with standing: Minuteman crew member, 490th SMS, Malmstrom, 1981-85, then Grand Forks Wing Codes Division 1985-88. His argument from the unit history's silence about maintenance teams, and Figel's inconsistencies between interviews |
| http://timhebert.blogspot.com/2012/10/engineering-change-proposal-1221-air.html | Tim Hebert on ECP 1221 | ECP 1221 as an EMP suppression kit, ~24 October 1967, cited to the same Black Vault unit history. **Independently confirmed by this session against the PDF itself**, which carries ECP 1221 at pages 52-53 with its own exhibit citation, "Engineering Change Proposal, 'ECP No. 1221,' submitted by Boeing Company, Ex 35" |
| http://kevinrandle.blogspot.com/2013/05/robert-salas-and-me.html | Kevin Randle, 19 May 2013. `kevin-randle` is already a board node | A non-hostile researcher's account of Salas revising the number of missiles affected ("Split the difference and I said eight", later all ten), and of a discrepancy between Salas (all) and Meiwald (four or five) |
| https://minotb52ufo.com/doc.php | The Minot 1968 documentation index | The primary set: Blue Book final case report of 13 November 1968; Basic Reporting Data of 28 October 1968 prepared by Lt Col Arthur J. Werlich, 862nd Combat Support Group Operations Division; the 91st SMW Wing Security Controller's summary; the Base Operations Dispatcher's Log 0800-1010Z; seven AF Form 117 questionnaires with the airmen named in section 6; thirteen B-52 ASQ-38 radarscope photographs; the Werlich overlay map at 1:200,000; and a transcription of recorded B-52/RAPCON conversations |
| https://en.wikipedia.org/wiki/Big_Sur_UFO | Wikipedia, opened only to date Mansmann's letter | "Florenz Mansmann, a major who was involved in the project, reportedly confirmed the account in a May 1987 letter to a UFO researcher." Confirms the 1987 letter is a BIG SUR letter, not an Echo Flight letter |
| https://www.theblackvault.com/documentarchive/unidentified-flying-objects-over-malmstrom-afb-november-1975/ | The Black Vault's landing page for OASD FOIA case 97-F-1677 | Release September 1997, Office of the Assistant Secretary of Defense, FOI and Security Review. **The page does not reproduce document text**; the board's existing `l-malmstrom` claim about F-106 non-interception is not corroborated verbatim from this page by this session, though the 24th NORAD log independently records the fighters and the lights going out |
| https://politicalsaucer.substack.com/p/the-night-at-november-5-two-missile | The Political Saucer, Substack, published 12 September 2026 | Dates a second, independent write-up of the Ellsworth case five days after the Michels episode, naming Woods and Johnson and the 44th Missile Security Squadron. **Paywalled below the fold; only the visible header was read** |
| In-repo: `research/leads/michels-rjUdn6FklAU-triage-2026-09-19.md` | This repo's own timestamped triage of Jesse Michels video `rjUdn6FklAU`, published 2026-09-07, 02:47:21, auto-captions | The whole provenance chain for Michael Johnson, reproduced in section 10 with its timestamps. Read in full by this session |

### 2b. Walls, recorded as walls

| Target | Result |
|---|---|
| https://media.defense.gov/2024/Mar/08/2003409233/-1/-1/0/DOPSR-2024-0263-AARO-HISTORICAL-RECORD-REPORT-VOLUME-1-2024.PDF | **HTTP 403 to WebFetch, and HTTP 403 to curl with browser headers and an aaro.mil referer.** AARO Historical Record Report Volume I was NOT OPENED by this session. The board's existing citation of its page 30 - interviews with five former Air Force officers who served at Malmstrom, Ellsworth, Vandenberg and Minot between 1966 and 1977 - stands on an earlier pass, not on this one, and is not re-verified here |
| https://www.bibliotecapleyades.net/ciencia/ufo_briefingdocument/1975.htm | HTTP 401. Not opened |
| https://www.ufocasebook.com/sacbaseweapons1975.html | HTTP 503. Not opened |
| The Wall Street Journal report of June 2025 attributing the 1967 Malmstrom shutdowns to an unannounced classified EMP vulnerability test | **NOT OPENED.** It surfaced in search results only. Until the article itself is opened and dated, nothing in this pass rests on it, and the board should not carry it |
| James Carlson, "Echo Flights of Fantasy" and "American, Credulous" | **NOT OPENED.** Both are on Scribd, which this session did not reach. Carlson's position in section 8 is therefore reported at one remove, from Metabunk and from UFO Chronicles, and is marked as such. **This is the largest evidentiary gap in the case-against section and it should be closed** |
| Col. Frederick Meiwald's letter of 1 October 1996, in facsimile | **NOT OPENED.** Hastings's own article points to his "Witch Hunt" piece rather than reproducing it. This session found two flatly incompatible characterisations of its contents and could resolve neither. See section 12 |
| The Loring 42 BW unit history for October-December 1975, at AFHRA | **NOT SOUGHT ONLINE AND NOT OPENED.** The Wurtsmith analogue is instructive: SSgt Cahill checked the Oct-Dec 75 379th Bomb Wing History in January 1979 and found no reference to the incident at all |
| https://www.scribd.com/document/42303580/ | Not attempted after the pattern of Scribd blocks; recorded so the next pass does not assume it was tried |

---

## 3. THE 1975 OVERFLIGHT SEQUENCE - the documents, in their own words

This is item 1 of the brief and it got the most effort. What follows is what the paper says,
not what the literature says about it.

### 3a. Loring AFB, Maine - the NMCC Memorandum for the Record, 29 October 1975

The single best artefact in the sequence. An operational record of the National Military
Command Center, subject line "AFB Penetration", over the signature of a serving general
officer. Quoted in full from the NICAP reproduction:

> THE NATIONAL MILITARY COMMAND CENTER / WASHINGTON, D.C. 20101 / 29 October 1975 / 0605 EST
>
> MEMORANDUM FOR RECORD
>
> Subject: AFB Penetration
>
> 1. At 290200 EST AFOC informed NMCC that an unidentified helicopter, possibly two, had been
> sighted flying low over Loring AFB Maine, in proximity to a weapons storage area.
> 2. An Army National Guard helo was called in to assist in locating the unidentified helo(s).
> 3. NORAD was informed of the incident by SAC, requested and received authority from Canadian
> officials to proceed into Canadian airspace if necessary to locate the intruder.
> 4. At 0404 SAC Command Center informed NMCC that the army helo assisting on the scene had not
> sighted the unidentified helo(s).
> 5. A similar incident was reported at Loring the evening of 28 October 1975
>
> //signed// C. D. Roberts, Jr. / Brigadier General, USMC / Deputy Director for Operations (NMCC)

**The distribution list is the part that ought to be quoted more than it is**, because it is
the measure of how seriously this was taken inside the building: CJCS (5), DJS (3), J-30,
J-31, J-32, J-32A, J-33, J-34, J-35, J-38, CSA, CNO, CSAF, CMC, CH WWMCCS OPS & EVAL DIV,
DDO (NMCC), ADDO (NMCC), CCOC (NMCC), DIA REP FOR NMIC, NSA REP, CIA REP, PA REP, WEST HEM
DESK, NWSB, NMCC BRIEFER.

Four successive DDO UPDATEs follow, each citing its source message. The 291300 EST update:

> At approximately 290100 EST Oct 75, one unidentified helicopter was sighted 200 to 500
> meters from the weapons storage area at Loring AFB, Maine. The helicopter was at an altitude
> of 150 feet and penetrated Loring AFB. ... At 290300 EST the helicopter was sighted over the
> weapons storage area and the Army National Guard helicopter again responded with the Maine
> State Police and the Royal Canadian Mounted Police and plans to pursue into Canada, if
> necessary, if there is a reoccurrence. (SOURCE: 42 BW OP LORING AFB 291140Z OCT 75)

The 292200 EST update escalates it to the level that matters:

> The CSAF (Ops Div) has requested that the Army NG helo be provied [sic] until 300800 EST
> under the following conditions: To track and identify the intruder; no apprehension to take
> place; the Canadian Border would not be crossed; and civilian police on board will be for
> commo with ground units only. The request is under consideration by MG Snifin, DA Director
> of Operations, DCSOPS. Col Bailey, Mil Aide to Special Asst to SECDIF/DEPSECDEF has been
> advised of the situation show DoD approval be required. The State Department Canadian Desk
> Officer has been kept informed. (SOURCE: 42 BW CP LORING AFB 291140Z OCT 75; SAC CP OPS
> CONTROL 291954Z OCT 75)

The 300600 EST update records the rules of engagement as approved by "MG Sniffin, DA Director
of Ops, DCSOPS" - note the spelling changes between updates, which is what real message
traffic does - in four bullets: the NG helicopter and crew placed in "full time training duty
(FTTD)"; entry into Canadian airspace with Canadian consent; employment limited to tracking
and identification; and only US military personnel plus, if necessary, representatives of the
FBI, FAA and Border Patrol embarked. The 301300 EST update closes it out: the helicopter did
not return, and "Air Force is planning to utilize an Air Force helicopter from Plattsburgh AFB
for future operations."

**Tier 1 for what it records: that on 28-30 October 1975 the United States military tracked,
escalated and planned an armed-forces response to an unidentified low-level intruder over a
nuclear weapons storage area, and failed to identify it.** It is Tier 1 for nothing else. The
documents say "unidentified helicopter" throughout and the NMCC never says otherwise.

Two further Loring documents are cited by NICAP but were **not opened in their own text** by
this session and are therefore listed as leads, not claims: an OSI teletype of 29 October 1975
noting that the incident "closely parallels a similar helicopter sighting earlier this year",
and an OSI letter of 21 April 1977 titled "Overflight of USAF Installations by Unidentified
Aircraft". The second title is the more interesting of the two, because it is an OSI
characterisation eighteen months after the fact.

The teletype phrase that the literature lives on, from the NICAP article: *"The A/C [aircraft]
definitely penetrated the LAFB [Loring Air Force Base] northern perimeter and on one occasion
was within 300 yards of the munitions storage area perimeter."* And from TWZ, quoting an
OPREP: *"It is our opinion that the unknown helicopter has demonstrated a clear intent in the
weapons storage area, is smart and a most capable aviator."* That is the sentence Fawcett and
Greenwood took their 1984 title from, and `clear-intent-1984` is already on the board.

### 3b. Wurtsmith AFB, Michigan - 30-31 October 1975, and a historian's negative finding

The NORAD Command Director's Log, 31 Oct 75/0445Z, reporting an incident at 0355Z: a
helicopter hovered over the SAC weapons storage area then departed. The NORAD Senior
Director's Log for 31 October 1975: *"Alerted by NCOC of a helicopter sighted over Wurtsmith
AFB Wpns storage area, a tanker sighted same and pursued it 35 SE over Lake Huron."*

**The most methodologically interesting Wurtsmith document is not from 1975 at all.** It is
SSgt Paul J. Cahill's "Research Record of Events" of 17 January 1979, written by the 379th
Bombardment Wing historian, which records: *"Following that request, I checked the Oct-Dec 75
Wing History and found no references to the incident."* The day after, on 18 January 1979,
Capt. Myron Taylor wrote a Memo for the Record to Cahill giving the KC-135 crew's account:
*"We followed the lights north out over Lake Huron and then the UFO swung south still over the
lake toward the Saginaw Bay area of Michigan."*

**This is a documented instance of a wing history omitting an event that other Air Force
paper records, and of the wing historian discovering and stating that omission in writing.**
It is worth a node of its own, and it is the correct caution to attach to any future
argument from a unit history's silence - including Tim Hebert's argument in section 8.

KC-135 crew named in Taylor's memo: Major Frederick Pappas (aircraft commander), Capt. K. E.
May (co-pilot), Capt. Rick Meier (navigator), Capt. Myron Taylor (instructor navigator),
Capt. Randy Higginbotham (instructor pilot), Sgt Steve Smith. Ground witnesses named: Airman
Martin E. Tackabury, Airman Michael J. Myers, Sgt Robert J. Anderson, Airman Roger Skipper,
Sgt James A. Miller (weapons storage area security police). Col. Boardman is named as wing
commander. A Joint Chiefs of Staff Operational Report of 30 October 1975 records the
prosaic-explanation check that was run and did not fit: *"Upon information that the Dept. of
Natural Resources sends out aircraft searching for hunters spotting deer, the Dept. of Natural
Resources was contacted."*

### 3c. Malmstrom AFB, Montana - the 24th NORAD Region Senior Director's Log, 7-19 November 1975

The strongest single artefact in the whole nuclear strand, because it is a continuous
operational log kept by air defence controllers in their own shorthand, not a report written
for anybody. Extracted in full by this session. Selected verbatim, OCR as found:

> 7 Nov 75 (1035Z) - Received a call from the 341st Strategic Air Command Post (SAC CP), saying
> that the following missile locations reported seeing a large red to orange to yellow objects
> M-l, L-3, LIMA and L-6. The general object location would be 10 miles south of Moore,
> Montana, and 20 miles east of Buffalo, Montana. Commander and Deputy for Operations (DO)
> informed.
>
> 7 Nov 75 (1203Z) - SAC advised that the LCF at Harlowton, Montana, observed an object which
> emitted a light which illuminated the site driveway.
>
> 7 Nov 75 (1319Z) - SAC advised K-l says very bright object to their east is now southeast of
> them and they are looking at it with 10x50 binoculars. Object seems to have lights (several)
> on it, but no distinct pattern. ...
>
> 7 Nov 75 (1327Z) - L-l reports that the object to their northeast seems to be issuing a black
> object from it, tubular in shape. [followed immediately, in the log's own hand, by] all this
> time, surveillance has not been able to detect any sort of track except for known traffic.
>
> 7 Nov 75 (1355Z) - K-l and L-l report that as the sun rises, so do the objects they have
> visual.
>
> 7 Nov 75 (1429Z) - From SAC CP: As the sun rose, the UFOs disappeared. Commander and DO
> notified.

The 8 November entries are the ones that carry the interception claim:

> 8 Nov 75 (0635Z) - A security camper team at K-4 reported UFO with white lights, one red light
> 50 yards behind white light. Personnel at K-l seeing same object.
>
> 8 Nov 75 (0645Z) - Height personnel picked up objects 10-13,000 feet. Track J330, EKL3 0648,
> 18 knots, 9,500 feet. Objects as many as seven, as few as two A/C.
>
> 8 Nov 75 (0753Z) - J330 unknown 0753. Stationary/seven knots/12,000. One (varies seven
> objects). None, no possibility, EKLB 3746, two F-106, GTF, SCR 0754. NCOC notified.
>
> 8 Nov 75 (0820Z) - Lost radar contact, fighters broken off at 0825, looking in area of J331
> (another height finder contact).
>
> 8 Nov 75 (0905Z) - From SAC CP: L-sites had fighters and objects; fighters did not get down to
> objects.
>
> 8 Nov 75 (0915Z) - From SAC CP: From four different points: Observed objects and fighters;
> when fighters arrived in the area, the lights went out; when fighters departed, the lights came
> back on; to NCOC.

And the log's own even-handedness, which is why it is worth Tier 1:

> 9 Nov 75 (0320Z) - FAA Watch Supervisor reported he had five air carriers vicinity of UFO,
> United Flight 157 reported seeing meteor, "arc welder's blue" in color.
>
> 12 Nov 75 (0251Z) - Reported that both objects have disappeared. Never had any joy (contact)
> on radar.

The last entry, marked in the original "LAST ENTRY PERTAINING TO THESE INCIDENTS":

> 19 Nov 75 (1327Z) - SAC command post report UFO observed by FSC & a cook, observed object
> travelling NE between M-8 and M-l at a fast rate of speed. Object bright white light seen 45
> to 50 sec following terrain 200 ft off ground. The light was two to three times brighter than
> landing lights on a jet.

**Minot, from the same log, and read precisely:**

> 10 Nov 75 (1120Z) - UFO sighting reported by Minot Air Force Station, a bright star-like
> object in the West, moving east, about the size of a car. First seen approximately 1015Z.
> Approximately 1120Z the object passed over the radar station, 1,000 feet to 2,000 feet high,
> no noise heard. Three people from the site or local area saw the object. NCOC notified.

**Minot Air Force STATION, a radar site, and "the radar station" in the log's own next
clause. Not Minot AFB and not the 91st SMW missile field.** See finding 6 in section 1.

The log's release attestation at its foot: "TERRENCE C. JAMES, Colonel, USAF, Director of
Administration", copies to HQ USAF/DAD and HQ USAF/JACL, with page stamps 450, 451 and 452
and a control number 000974 - it is an extract from a paginated FOIA compilation whose other
449 pages this session did not see.

### 3d. Grand Forks AFB, North Dakota - 4-5 November 1975

Cited by NICAP from message traffic and **not opened in original text by this session**: a
command post event dispatch of 4 November 1975 at 0301 recording that "There were possibly
some shots fired from on base toward hard alert aircraft on the Sac alert ramp", and a
detailed incident message of 5 November 1975, "He heard five shots in groups of three and two
with a space of approximately two seconds between the groups", naming Captain Klawon of the
321st Security Police Squadron. **This is the only entry in the whole sequence in which
weapons discharge is alleged, and it is the one this pass established least well.** It is
carried here as a lead.

### 3e. CINCNORAD's four-part message, 11 November 1975

The message that ties the sequence together in the command's own voice, excerpted:

> Since 28 Oct 75 numerous reports of suspicious objects have been received at the NORAD CU;
> reliable military personnel at Loring AFB, Maine, Wurtsmith AFB, Michigan, Malmstrom AFB, Mt,
> Minot AFB, ND, and Canadian Forces Station, Falconbridge, Ontario, Canada have visually
> sighted suspicious objects.

Note that CINCNORAD itself says **Minot AFB** where the 24th Region log says Minot Air Force
Station. Two NORAD documents nine days apart disagree about which Minot installation is
meant, and no opened record resolves it. That disagreement belongs in the `l-minot` node.

A NORAD press release of 13 November 1975 from Sudbury, Ontario records that two F-106s of the
Air National Guard's 171st Fighter Interceptor Squadron were scrambled to Falconbridge, and
the 22nd NORAD Region's Director of Public Affairs, Capt. Gordon Hilchie, and Control Centre
Director Lt Col Brian Wooding are named. An Air Force Intelligence Service Alert Officer's Log
entry of 31 October 1975 reads *"Contacted DIA OPS center and informed them of unidentified
flight activity over two SAC bases near Canadian border."*

**What these documents do not do.** They do not say what the objects were. They do not use the
word "unidentified flying object" in the Loring traffic, only "unidentified helicopter". They
record a failure to identify and a failure to intercept, and command-level alarm about both.
That is the whole of the Tier 1 claim, and it is enough.

---

## 4. Malmstrom, March 1967: THE TWO EVENTS ARE NOT ONE EVENT

The literature's most persistent error, and the board's own `malmstrom-echo-flight-1967` node
currently carries both under one label. The split, established as far as this pass could
establish it:

| | **ECHO FLIGHT** | **OSCAR FLIGHT** |
|---|---|---|
| Date | **16 March 1967, 0845** | **24 March 1967**, per Hastings's current position; Salas has also given 24/25 March, and earlier accounts conflated it with 16 March entirely |
| What is documented | **The shutdown, in the 341st SMW unit history, in detail, over pages 32-40 of the Jan-Mar 1967 volume**, footnoted throughout to a classified engineering report of 23 March 1967 | **NOTHING IN THE RELEASED UNIT HISTORY.** The string "Oscar" does not appear anywhere in the 88 released pages. Neither does "O Flight", "24 Mar" or "25 Mar" |
| Named crew on duty | **The unit history names no launch officer at all.** Capt. Eric D. Carlson (commander) and 1Lt Walter Figel (deputy) are established as the Echo crew by their own later statements, not by the released paper | Capt. Robert Salas (deputy) and Lt Frederick Meiwald (commander), on Salas's account |
| The UFO element | **One sentence in the unit history, and it is a negative** (section 5) | Rests entirely on Salas's testimony from 1996 onward, and on Meiwald's letter and Hastings's recordings |
| Status | Tier 1 that it happened; Tier 2 at best for any UFO connection | **Tier 2 as a claim by a named man on dated records, which is exactly what section 2a admits and exactly the tier at which it is carried** |

**The date change is itself the most load-bearing fact here and it should be in the node.**
For years the Oscar Flight account was told as part of the same 16 March event, which is why
Echo Flight's documentation was read as corroborating Salas. It is Hastings's own article
that now places Oscar on 24 March, and the reason he gives is Capt. Robert Jamison's
recollection of a second retargeting call-out. That means the separation of the two events -
which is what allows Salas's account to survive the unit history's silence - was produced by
the same interviewer whose interviews are the only source for it. Section 2a requires that to
be said plainly and it is said plainly here. It is not a disqualification. It is the shape of
the evidence.

---

## 5. What the 341st SMW unit history actually says

All quotations below are the OCR as extracted from the Black Vault PDF, page numbers as the
history itself paginates. Transcription artefacts are left in rather than silently corrected,
per `CLAUDE.md` section 2.

**Provenance first.** The release is 88 pages: John Greenewald Jr's FOIA request of
9 May 2001 to 341 CS/SCBR at Malmstrom AFB; the reply of 14 June 2001 from Headquarters 341st
Space Wing, signed Marty S. Stephens, releasing "Copies of excerpts, as well as supporting
documents" of five quarterly wing histories from 1 January 1967 to 31 March 1968, and stating
"We do not have any audio or video tapes, or documents of any personnel injured", with a
referral to NARA. **These are excerpts chosen by a FOIA office, not the complete histories.
Every argument from silence below is bounded by that.**

**The event, page 32-33:**

> On 16 March 1967 at 0845, all sites in Echo (E) Flight, Malmstrom AFB, shutdown with No-Go
> indication of Channels 9 and 12 on Voice Reporting Signal Assemble (VRSA). All LF's in E
> Flight lost strategic alert nearly simultaneously. No other Wing I configuration lost
> strategic alert at that time.

Footnote 60 to that passage: *Msg, (S) DM 02752, SAC to 341 SMW, Subj: Loss of Strategic Alert
Echo Flight, Malmstrom AFB, 17 Mar 67, Ex 43.* The rest of the section is footnoted almost
entirely to one classified source: *Rpt, (S) "Report of Engineering Investigation of Echo
Flight Incident, Malmstrom AFB, Mont. - 16 Mar 67," by Engineering Investigation Team,
23 Mar 67.* **That report is the document the whole controversy turns on and no version of it
has been opened by this board.**

**The escalation, page 33:**

> At approximately 1400 hrs on 16 Mar 67, the 341st SMW was advised that SAC Headquarters had
> called in OOAMA support for a complete engineering analysis of this problem. ... The task
> group included personnel from OOAMA, Boeing Company, Autonetics, and 15th AF; they were to
> arrive on 17 or 18 March 67.

**The four-way method, page 34.** Review of events and flight configuration; investigation and
where possible elimination of circumstances; investigation of means of causing the observed
results; investigation of similar events.

**THE UFO SENTENCE, page 38, quoted in full because every partisan quotes half of it:**

> Rumors of Unidentified Flying Objects (UFO) around the area of Echo Flight during the time of
> fault were disproven. A Mobile Strike Team, which had checked all November Flight's LFs on the
> morning of 16 March 67, were questioned and stated that no unusual activity or sightings were
> observed.

Note what that sentence actually asserts and what it does not. It asserts that rumours were
disproven. The evidence it gives for the disproof is that a Mobile Strike Team **which had been
at NOVEMBER Flight**, not Echo Flight, reported nothing unusual. That is a non-sequitur on its
face, and the board should record it as one - without inflating it, because the sentence is
still the Air Force's own contemporaneous finding and it is still the only UFO reference in
88 pages.

**What else was ruled out, pages 38-39:** weather; unusual activity at EMC-1 or EMC-2; radar
or atmospheric interference, on a negative report from the 801st Radar Squadron, Malmstrom
AFB; Primary Alerting System activity, verified by Capt. Bradshaw in the command post. Boeing
modification teams were at B-1, K-1 and G-1 on 16 March 67 but arrived after the incident. LCF
E-1's commercial power problems are logged at 1453, 1510-1600 and restoration at 1921 - all
**after** the 0845 shutdown, which is a point both sides tend to slide past.

**THE FIRST CONCLUSION, page 17 of the engineering report as cited in the history:**

> Since the only common item determined in this investigation was the LCC. The LCC power fault
> transmitted to the LFs on the hardened cable was considered the only power fault capable of
> causing the Echo Flight incident.
>
> The investigation teams at Malmstrom, were unable to determine a logical cause for the
> incident. Further investigation in the area of shutdown results will be conducted in an effort
> to determine a possible cause of this incident. These studies will be conducted at the
> contractors facility and will be included in the next history.

**THE SECOND CONCLUSION, April-June 1967 volume**, after the Boeing Network Resolution Area
bench tests and the transformer-failure simulation at Malmstrom during the week of 15 May 1967:

> The tests run at Boeing in the NRA have proved that the C-53P Logic Coupler was the receiver
> to the noise Pulse irregularly. ... When the Pulse Width was set at 30 micro sec, 12 Channel 9
> & 12 No-Go's, one Channel 9 No-Go, and four Coupler Self Tests (CST), were experienced out of
> 20 separate applications of the Pulse. ... In other words, 60 percent of the time the responses
> were the same as experienced at Echo Flight and 85 percent of the time the response would have
> placed the system in a non EWO status.
>
> Due to the fact that the power tests were essentially negative, it appears that the cause of
> the Echo Flight problem was of the EMP or electrostatic nature.

**And the engineering caveat that makes the EMP account a hypothesis rather than a finding:**
Boeing's first theory, that the Sensitive Information Network lines carried the noise pulse,
was tested at Malmstrom and *"Further studies at Malmstrom AFB by Boeing proved this analysis
wrong."* The transformer-failure simulation likewise: *"Instrumentation on the Sensitive
Information Network lines and on the commercial primary power lines showed no significant
noise propagation as a result of simulating the transformer failure."* **The EMP conclusion is
arrived at by elimination, from a series of negative tests, not by reproducing the event.**

**What followed, July-September and October-December 1967 volumes.** OOAMA concluded the cause
was "of the Electro Magnetic Pulse (EMP) noise or electrostatic nature" and Wing I peculiar,
because Channel 9 & 12 No-Go shutdowns had never been reported at Wings II through V. SAMSO
conducted EMP tests at F. E. Warren AFB, Wyoming - **note the base, for the `l-warren` hub** -
completing all test objectives on Delta Flight, then moved to the 564th SMS in October. Sierra
39 was depostured on 28 September 1967 and turned over to Boeing for EMP tests through about
mid-January 1968. Three engineering change proposals resulted, and the history names them with
exhibit numbers: **ECP 1221** (*"will modify the interconnecting box by adding a major
sub-assembly containing zener diodes, isolation..."*), ECP 1141-1 and ECP 1141-2, plus FCIR
MCL number 2827, all submitted by the Boeing Company, exhibits 35, 36 and 37.

**The honest bottom line, and it does not favour either camp.** The Air Force documented the
shutdown, could not explain it at the time, concluded four months later on negative evidence
that it was probably EMP or electrostatic, hardened the fleet against exactly that, and
recorded in one sentence that UFO rumours were disproven on evidence drawn from the wrong
flight.

---

## 6. Minot 1968 - enrichment of an existing node

`minot-1968` is already on the board and already strong. What this pass adds is the
document-by-document inventory from the case's own archive, which is the best-organised
primary set in the entire nuclear strand and which the node should cite by item rather than
in aggregate:

- **Blue Book final case report, 13 November 1968, 12 pages**, the Foreign Technology
 Division's conclusions on the submitted data.
- **Basic Reporting Data, 28 October 1968, 8 pages**, prepared by **Lt Col Arthur J. Werlich,
 862nd Combat Support Group Operations Division**, transmitted to multiple Air Force
 agencies. This is the on-base investigating officer's own report and it is the spine of the
 file.
- **91st Strategic Missile Wing Security Controller's summary**, listing UFO observers at
 Launch Control Facilities with sighting times.
- **Base Operations Dispatcher's Log, 0800-1010Z**, recording ground reports from **N-7**,
 described as a "brilliant light like the sun".
- **Seven AF Form 117 witness questionnaires**, completed by A1C Lloyd M. Isley (91st MIMS),
 A1C Robert Michael O'Connor (91st MIMS), A1C Joseph Patrick Jablonski (862nd SPS), A1C
 Gregory Adams (862nd SPS), SSgt James Frederick Bond (862nd SPS), SSgt William E. Smith Jr.
 (862nd SPS), and **Major James A. Partin, pilot, 23rd Bomb Squadron, 5th Bomb Wing**.
- **Thirteen B-52 ASQ-38 radarscope photographs**, 8x10 prints with data plates.
- **The Werlich overlay map**, B-52 flight track with UFO positions, 1:200,000.
- **A transcription of recorded conversations between the B-52 co-pilot and Radar Approach
 Control.**
- Upper-air rawinsonde data.

**The B-52 crew, from the debriefing roster:** co-pilot Capt. Bradford Runyon; radar
navigator Maj. Charles Richey; navigator Capt. Patrick McCaslin; EWO Capt. Thomas Goduto;
gunner TSgt Arlie Judd. Aircraft call sign **JAG-31**.

**The section 2a provenance point on Minot 1968, and it is a good one.** The modern
investigation exists because **Bradford Runyon contacted the Center for UFO Studies in 2000
and completed a CUFOS questionnaire of his own initiative.** That is a witness approaching a
research body, not a research body recruiting a witness, and it is the opposite of the
Hastings pattern. It should be recorded as such, because the board needs the contrast to make
the circular-reporting query in section 3 of the triage rule answerable.

---

## 7. Robert Hastings as aggregator - the structural risk, stated plainly

`robert-hastings` is on the board at Tier B. Nothing here downgrades him. What follows is
what section 2a obliges the board to record about a man through whom a large fraction of this
entire witness class reached the public.

**How many witnesses.** His own site gives two different numbers on two pages opened the same
day: the press-conference article says *"I have interviewed more than 160 U.S. Air Force
veterans regarding their involvement in UFO incidents at nuclear weapons sites"*; the about
page says *"To date, Hastings has interviewed more than 150 military veterans"*. The board's
existing node says "over 150". The discrepancy is small and probably just page-update drift,
but **a count that is the principal evidence for a claim should be a count the board records
with its source, not a round number**.

**How he found them.** **THIS IS THE ANSWER SECTION 2a MOST WANTS AND IT IS NOT AVAILABLE.**
Neither page opened by this session states his recruitment method - no description of
advertisements, unit rosters, veterans' reunions, referral chains or word of mouth. The
absence is recorded here as a finding. Until a dated statement by Hastings describing his
sourcing method is opened, **every node in this cluster whose sole source is a Hastings
interview should carry a note saying that the route by which the witness was found is not
documented.**

**Who spoke before he reached them.** Tested witness by witness, and the answer is stark:

| Witness | Spoke publicly before an interested party contacted him? |
|---|---|
| Robert Salas | **Substantially yes.** 1996 interview with the *Great Falls Tribune*, which the board's own node already carries. He also located Meiwald himself in summer 1996, on Hastings's own account. Salas is the origin of this strand, not a recruit to it |
| Walter Figel | **NO.** His account exists as Hastings's audio recordings of three telephone conversations, 2008, 2009 and 2010. He declined to sign an affidavit for the 2010 press conference |
| Frederick Meiwald | **NO.** A private letter to Salas of 1 October 1996 and tape-recorded calls with Hastings in August 1996 and on 6 May 2011 |
| Robert Jamison | **NO** by anything opened here. His recollection supplies the 24 March date on which the whole Echo/Oscar separation depends |
| Robert Kaminski | **NO.** A 1997 letter to researcher Jim Klotz |
| Patrick McDonough, Dwynne Arneson, Bruce Fenstermacher, Jerry Nelson | **NOT ESTABLISHED EITHER WAY** by anything opened here. Each appears in the record first at the 2010 press conference, with an affidavit executed for that event |
| Charles Halt | **YES, and differently from all of the above.** He wrote the operative document himself, in 1980, as a serving deputy base commander, before any researcher was involved. `halt-memo` is on the board |
| Robert Jacobs | **YES.** *National Enquirer* 1982, *MUFON UFO Journal* No. 249, January 1989 - both under his own name, years before the Disclosure Project, and answered by a hostile participant |
| Bradford Runyon | **YES, in the inverse direction.** He approached CUFOS in 2000 |

**The structural finding, stated as `CLAUDE.md` section 2 requires.** Of the nine Malmstrom
and Oscar Flight corroborating voices, **four - Figel, Meiwald, Jamison and Kaminski - reached
the public solely through Robert Hastings or Robert Salas, and three of those four exist only
as private correspondence or as tape recordings held by the interviewer.** Four witnesses who
share a single interviewer are not four independent confirmations. They are one method applied
four times. That is precisely the Disclosure Project problem the board documented on
18 September, and it applies here without the mitigation the Disclosure Project lacks: at
least Greer published his testimonies in a single dated document that anyone can open. The
Figel tapes have not been published in full to any URL this session could open.

**The countervailing point, and it is real.** Hastings's method is not testimony alone. He
pairs witness accounts with FOIA paper and publishes the paper in facsimile: FBI memoranda on
Los Alamos in December 1948 and on Los Alamos and Sandia in August 1950, F. E. Warren AFB
documents of 1 August 1965, Minot material from 1966, the Air Force teletype of 17 March 1967
reporting loss of strategic alert at Malmstrom, and the 1975 Malmstrom documents. The board's
`malmstrom-echo-flight-1967` to `robert-hastings` edge is typed `custody` for exactly that
reason, and that is the right typing. **The document half of his output is checkable and
largely checks out. The interview half is a single-source funnel. The board should grade the
two halves differently in the same node.**

**The 27 September 2010 National Press Club roster, as a dated artefact.** `npc-2010-ufos-nukes`
is on the board and already names the seven. Confirmed and enriched from Hastings's own page:

| Name | Rank as given | Unit / base | Period claimed | Affidavit |
|---|---|---|---|---|
| Dwynne Arneson | Lt Col | 28th Air Division, Malmstrom AFB, Montana | 1967 | Yes |
| Bruce Fenstermacher | Capt | Missile Combat Crew Commander, F. E. Warren AFB, Wyoming | 1974-1977 | Yes |
| Charles Halt | Lt Col, later Col | RAF Bentwaters/Woodbridge, England; later Kunsan AB, Korea | 1980-81 | Yes |
| Robert Jamison | Capt | ICBM Combat Targeting Team, Malmstrom AFB, Montana | Jan 1965 - Oct 1967 | Yes |
| Patrick McDonough | Geodetic surveyor | F. E. Warren AFB, Wyoming, with worldwide TDY to Atlas, Titan, Minuteman, Mace and Matador sites | 1962-1966 | Yes |
| Jerry (Jerome) Nelson | Deputy Missile Crew Commander | 579th Strategic Missile Squadron, Walker AFB, Roswell, New Mexico | 1962-1965 | Not stated on the page |
| Robert Salas | Capt | Malmstrom AFB, Montana | March 1967 | Yes |

**One data-integrity flag on that table.** The fetch of Hastings's page rendered Salas's line
as "witnessed 1969 incident". Every other source opened by this session, including the board's
own node, gives March 1967. **This session could not confirm the "1969" string is actually on
the page rather than a summarisation error, and it is recorded as unresolved rather than
quietly corrected.** Do not carry 1969 anywhere.

---

## 8. THE CASE AGAINST - both of them, neither softened

The brief requires this section and it is the section most often written badly, because the
two sceptical cases are routinely merged into one when they are different in kind.

### 8a. The engineering case, which is the Air Force's own and is not a sceptic's construction

Already quoted at length in section 5. In summary: SAC ordered a full engineering analysis
within hours; OOAMA sent a task group including Boeing and Autonetics; the team eliminated
weather, radar and atmospheric interference, PAS activity, commercial power switching and the
Montana Power Company's high-voltage switching test of 28 March 1967; it concluded it could
not determine a logical cause; Boeing bench testing in its Network Resolution Area then
reproduced the exact Channel 9 & 12 No-Go signature 60 per cent of the time using a 30
microsecond noise pulse on the C-53P Logic Coupler's Self Test Command line; and the history
concluded the cause "appears" to have been "of the EMP or electrostatic nature", Wing I
peculiar because of the difference between the Minuteman I C-53P and Minuteman II C-53D logic
couplers and their intersite cabling. The Air Force then bought the fix: **ECP 1221, ECP
1141-1, ECP 1141-2 and FCIR MCL 2827**, all from Boeing, and ran EMP test programmes at
F. E. Warren and at the 564th SMS.

**The external attribution, and its status.** A Top Secret 1969 USAF official history,
Bernard C. Nalty's *USAF Ballistic Missile Programs 1967-1968*, is quoted in the Metabunk
thread as recording that an "electronic noise pulse had shut down the flight...similar to the
electromagnetic pulse generated by nuclear explosions". **This session did not open Nalty. It
is the single best remaining document lead in the whole Malmstrom question** and it is listed
as such in section 13. Separately, search results surfaced a June 2025 *Wall Street Journal*
report that Air Force sources attribute the shutdowns to an unannounced classified EMP
vulnerability test. **That was not opened and nothing here rests on it.** If it is real, it is
a materially different claim from the unit history's - a deliberate test rather than an
ambient pulse - and it would have to be sourced and dated before the board carries it.

**The honest weight of the engineering case:** it explains the shutdown mechanism plausibly
and is supported by what the Air Force actually spent money on afterwards. It does not
reproduce the event, it was reached by elimination, and it does not address Oscar Flight,
which the released paper does not mention at all.

### 8b. James Carlson's dispute with Salas, which is a different thing entirely

James Carlson is the son of **Capt. Eric D. Carlson**, the Echo Flight commander on 16 March
1967. He has published a 357-page work, *American, Credulous*, and a shorter piece, *Echo
Flights of Fantasy - Anatomy of a UFO Hoax*. **Neither was opened by this session** and his
position is therefore reported at one remove, from the Metabunk thread and from UFO
Chronicles, and marked accordingly. His conclusion as quoted there: *"not only were no UFOs
involved at Echo Flight or any other flight...claims of UFO interference...is completely
unsupportable"*. He has described the Malmstrom UFO account as "a poorly executed lie", and
states that both his father and Col. Walt Figel reported no UFOs.

His enumerated disputes with Salas, as reported:

1. **Numbers.** Salas has claimed all ten Echo missiles dropped off alert; Eric Carlson is
 reported as confirming three or four. **The unit history sides with Salas on this point:
 "All LF's in E Flight lost strategic alert nearly simultaneously."** Kevin Randle's May
 2013 post independently records Salas himself once saying "Split the difference and I said
 eight" and later claiming all ten, and a discrepancy between Salas (all) and Meiwald (four
 or five) on Oscar Flight.
2. **Whether Oscar Flight happened at all.** Carlson says there was no Oscar Flight incident;
 he cites SAC UFO officer Col. Lewis D. Chase finding no equipment failures or sighting on
 that date. The released unit history is silent, which supports neither man.
3. **Figel.** Carlson says Figel denied seeing a UFO and took the report as a joke. Hastings
 says Figel admitted receiving a report of a "large, round object" over a silo. **Both can
 be true simultaneously** - a man can take a report and disbelieve it - and Tim Hebert's
 reading is the most careful one opened here: that Figel's two interviews contradict each
 other on where the maintenance teams were and on who reported the sighting, and that Figel
 declined to sign an affidavit for the 2010 press conference.
4. **Flight designation.** Salas is said to have located himself inconsistently across
 accounts before settling on Oscar.
5. **Directness.** Salas did not see anything himself. His account is of a telephone call from
 a topside security policeman. **That is not a defect - it is what a launch officer sealed
 in a capsule sixty feet down could possibly witness - but the board should state it,
 because the popular version implies he saw a craft and he has never claimed that.**

### 8c. The third sceptic, who is the most useful of them

**Tim Hebert** is worth a node in his own right and is not on the board. He is a former
Minuteman crew member, 490th SMS, Malmstrom AFB, 1981-85, then the Wing Codes Division at
Grand Forks AFB, 1985-88, and later a programme manager with Air Force Systems Command
handling ECPs. He argues from the released paper, not from assertion: that the unit history
details the crew debriefing but never mentions the maintenance teams whose presence the UFO
account requires, and that ECP 1221 shows what the Air Force actually believed. **This
session independently verified his ECP 1221 claim against the Black Vault PDF and it holds.**

**And the counter to his own strongest move.** His central argument is from a unit history's
silence. Section 3b of this dossier documents a case where an Air Force wing historian checked
his own Oct-Dec 1975 Wing History for an event that other Air Force paper records, and found
no reference to it, and wrote that down. **A unit history's silence is weaker evidence than it
looks, and the board has a documented instance of exactly that.** Hebert's reading is still
the best sceptical reading available; it is just not conclusive, and the node should say so.

---

## 9. The named witnesses - service documented where possible

**Robert Salas.** On the board. Documented: USAF Academy graduate, MS from AFIT, ICBM launch
controller, resigned commission 1971, Martin Marietta, Rockwell, FAA. Public since 1996.
Enrichment needed: split the Oscar Flight claim out of the Echo Flight node, and record the
1996 Great Falls Tribune interview as the dated artefact that fixes when the claim was made.

**Frederick Meiwald.** ABSENT. Salas's Oscar Flight commander, Colonel (ret.). The 1 October
1996 letter is the artefact and this session could not open it. **Two flatly incompatible
characterisations are in circulation and the board must not pick one:** Hastings and Salas
present it as elaborating and corroborating the Oscar Flight account; sceptical sources quote
it as saying Meiwald's recollection "differs" from Salas's and that he regrets being unable to
help. Propose the node with **both** in `conflicts` and a plain statement that the letter has
not been opened.

**Robert Jamison.** ABSENT. Capt., ICBM Combat Targeting Team, Malmstrom, January 1965 to
October 1967; later missile targeting instructor at Chanute AFB; separated July 1972 as
Captain. Affidavit executed for the 2010 press conference. **His is the recollection that
supplies the 24 March 1967 date for Oscar Flight**, and therefore the recollection on which
the entire Echo/Oscar separation rests. No pre-contact public statement identified.

**Patrick McDonough.** ABSENT. USAF geodetic surveyor 1962-1966, F. E. Warren AFB, with
worldwide TDY relating to surveys for Atlas, Titan, Minuteman, Mace and Matador sites.
Affidavit executed. No pre-contact public statement identified. Named in the brief.

**Dwynne Arneson.** ABSENT. Lt Col, 28th Air Division, Malmstrom, 1967; a communications
officer. He is the source for Kaminski's reported remark that "those missiles were perfect.
Clean". Affidavit executed.

**Bruce Fenstermacher.** ABSENT. Capt., Missile Combat Crew Commander, F. E. Warren AFB,
1974-1977. Affidavit executed. **He is the reason `l-warren` needs to exist even setting the
1965 Blue Book log aside.**

**Jerry (Jerome) Nelson.** ABSENT. Deputy Missile Crew Commander, 579th Strategic Missile
Squadron, Walker AFB, Roswell, New Mexico, 1962-1965. The only Atlas-era, non-northern-tier
witness on the 2010 panel.

**Walter Figel.** ABSENT. 1Lt, Echo Flight deputy crew commander, 16 March 1967, later Colonel.
**The most contested witness in the subject.** His account exists only as Hastings's audio
recordings of 2008, 2009 and 2010; he declined an affidavit; he is reported by Hebert as
inconsistent between his own interviews; and he is reported by James Carlson as having said he
saw nothing and took the report as a joke. Propose at Tier 2 with all of that in the node.

**Eric D. Carlson.** ABSENT. Capt., Echo Flight crew commander on 16 March 1967. Denies any
UFO report reached the capsule and denies a subsequent debriefing. **He is a witness for the
negative and belongs on the board for exactly the same reason the positive witnesses do.**

**James Carlson.** ABSENT. Not a witness; the principal named opponent, and the son of one.
Propose under section 2a on notability: an informed reader would read his absence as a gap.
Tier 2 for what he published, Tier 3 for his conclusions.

**Robert J. Kaminski.** ABSENT. Boeing engineer on the Echo Flight investigation. His
account, that the team found no failure that would explain ten missiles dropping off alert
and that the inquiry was ordered ended mid-stream with no report filed, reaches the public
through a 1997 letter to Jim Klotz. **Note the direct tension with the unit history**, which records the
investigation continuing at the contractor's facility through 1967 and producing engineering
change proposals. Both cannot be wholly right. Record the tension; do not resolve it.

**Robert M. Jacobs.** On the board, correctly and well. This pass read Kingston George's 1993
article in full and it is stronger than the node currently says: George publishes **two group
photographs** and captions Jacobs into both ("Lt. Bob Jacobs is at left with blocked military
cap"; "Jacobs at far right holding a camera and standing behind Chief Warrant Officer
Spooner"), names **Major Florenz Mansmann and Chief Warrant Officer Guy Spooner** in the first
caption, states George's own contemporaneous document by title and date (*Preliminary Report
on Image Orthicon Photography from Big Sur*, HQ 1st Strategic Aerospace Division Operations
Analysis Staff Study, 13 October 1964), dates the event to dawn on **22 September 1964** on an
Atlas launch nicknamed "Buzzing Bee", concedes Jacobs's conclusion 4 outright (*"Bob is
correct in saying that the observations in 1964 did not involve lasers"*), and states of the
film *"the film and related materials were all destroyed long before the 12 years were up"*.
He also writes *"I don't think Bob Jacobs ever gained the required clearance"* - which is
simultaneously the sceptic's explanation and an independent confirmation that Jacobs was there
and was debriefed.

**Florenz J. Mansmann.** ABSENT. Major, named by George in a photograph caption as present at
the Big Sur site, and the man whose letters of 1983, 1985 and 1987 are Jacobs's corroboration.
**See section 12 - the board currently attributes these letters to the wrong event.**

**Charles Halt.** On the board and already related to `rendlesham-1980`. **The one enrichment
this pass suggests is an edge from `charles-halt` to `npc-2010-ufos-nukes`**, if it does not
already exist, because his appearance there is what places Rendlesham inside the nuclear
witness cluster rather than beside it.

**Bradford Runyon.** ABSENT. Capt., B-52H co-pilot, JAG-31, 24 October 1968. **The
self-initiated witness**, who approached CUFOS in 2000. His crewmates Maj. Charles Richey,
Capt. Patrick McCaslin, Capt. Thomas Goduto and TSgt Arlie Judd are named in the debriefing
roster and are candidates for nodes if the board wants the crew as a unit.

**The 1975 named men**, from the documents rather than from interviews, and therefore a
different evidentiary class from everyone above: SSgt Danny K. Lewis, Sgt Clifton W. Blakeslee,
SSgt William J. Long, SSgt Michael D. Scott, TSgt David E. Mott, Capt. Richard R. Fuhs (all
42nd Security Police Squadron); SSgt James P. Sampley and Sgt Grover K. Eggleston (2192nd
Communications Squadron); Sgt Steven Eichner and Sgt R. Jones (B-52 crew); Col. Richard E.
Chapman (Commander, 42nd Bomb Wing) - all Loring. At Wurtsmith: Maj. Frederick Pappas, Capt.
K. E. May, Capt. Rick Meier, Capt. Myron Taylor, Capt. Randy Higginbotham, Sgt Steve Smith
(KC-135 crew); Airman Martin E. Tackabury, Airman Michael J. Myers, Sgt Robert J. Anderson,
Airman Roger Skipper, Sgt James A. Miller (ground); Col. Boardman (wing commander); SSgt Paul
J. Cahill (379th BW historian). At Malmstrom 1975: SSgt Joseph M. Chassey, Lt Col Robert
Peisher. At Grand Forks: Capt. Klawon, 321st SPS. **These names come out of message traffic
and memoranda for the record, not out of anyone's interview programme, and that is why they
matter to the circular-reporting question: they are the control group.**

---

## 10. Ellsworth 1977 - Mario Woods, and Michael Johnson under section 2a

Read from `research/leads/michels-rjUdn6FklAU-triage-2026-09-19.md`, in full, by this session.
That file is the provenance record and nothing here supersedes it.

**The claim.** Launch Facility **November-5**, Ellsworth AFB, South Dakota, 18 November 1977
at approximately 0100, on a 1800-0600 shift. Two USAF security policemen of the **44th
Missile Security Squadron** respond to an alarm; an object hovers under about 50 feet; four
humanoid figures approach; both men are taken and examined; missing time; both recovered about
eight miles away beside a reservoir dam; separate interrogations on base; Johnson subsequently
discharged.

**The organisational check this pass adds.** Ellsworth's Minuteman field belonged to the 44th
Strategic Missile Wing, active at Ellsworth from January 1962 and inactivated 4 July 1994.
The **45th Missile Security Squadron was activated on 1 November 1977**, assuming the
functions of the 44th MSS's former Missile Support Branch. So in November 1977 both squadrons
existed at Ellsworth and the 44th MSS was the parent. **That is a small, checkable fact and it
is consistent with the claimed unit.** It is not corroboration of anything else.

**Mario Woods - the long-standing witness.** Public since 1996, per the episode's own claim at
[00:20:48], with over 40 media appearances claimed at [00:01:46]-[00:01:54] including History
Channel, Discovery+ and NewsNation, **in which he repeatedly named Michael Johnson on air and
asked audiences to find him** [00:01:54]-[00:02:01]. The board already carries a Tier 2 claim
that the 5 July 2025 American Alchemy episode described the case at 0:23:44-0:24:30 and that
Woods says an OSI man named Rick Doty was at his debrief. **Propose `mario-woods` as a node at
Tier 2. He is exactly what section 2a admits: a named man with a thirty-year dated public
record of the same account, and no service record produced.**

**Michael Johnson - propose as a node, Tier 2, with the provenance in capitals.** The section
2a obligations, answered:

- **Who found him and by what route.** The publishing party. Not the original witness, not a
 records search, not AARO, which Woods says he asked. A **viewer of the show** sent the
 production a **Facebook page** belonging to a Michael Johnson in his seventies in South
 Carolina [00:03:16]-[00:03:31]. Michels then "tasked a very talented recruiter to find him"
 and the recruiter did so in about a week [00:03:40]-[00:03:45]. The recruiter is not named.
 The contact call is dated on air: **26 June 2026** [00:05:19].
- **What he said before.** **NOTHING ABOUT THE EVENT. NOT ONE DATED PUBLIC WORD, ANYWHERE, IN
 A 2 HOUR 47 MINUTE EPISODE.** The only pre-contact artefact identified is an undated Facebook
 post to the effect of "my boys in South Dakota on Ellsworth 75 to 77" [00:03:34]-[00:03:40],
 **which places him at the base in the right years and says nothing whatever about the
 event**. He asserts private prior telling [00:08:44], [01:32:29]. That is not a dated
 artefact.
- **What he was given first.** **Both things are true and both go in the node.** Michels ran a
 deliberate blind-contact protocol and should be credited for it: "Nothing about November 5.
 Nothing about a UFO" [00:05:24]-[00:05:41]. And then, within ninety seconds of Woods being
 patched in, Woods supplied the frame himself: site and date at [00:07:05]; **Johnson answered
 "No" when asked if he remembered what they encountered** [00:07:35]; **Woods then named the
 UFO, twice**; Johnson assented after a pause [00:07:46]; Woods then supplied "how far over
 the top of the blaster" and Johnson gave "under 50 feet" [00:08:51]. **The episode's own
 on-camera retelling of that moment at [00:17:46]-[00:18:11] says Johnson immediately said
 "Oh, that UFO" with nothing else supplied. The recording of the call does not show that.
 That divergence is internal to the episode, timestamped on both sides, and it is the single
 highest-value observation available on this case.** The hypnotic regression is worse still:
 the induction supplies "back to the winter of 1977" and "describe where you are on the base"
 before the subject produces anything [00:58:19]-[00:59:09].
- **Where the accounts agree and diverge.** They agree on substance - an object above the
 site, figures, missing time, separate interrogation - and **diverge sharply on posture and
 agency**: Johnson's account is passive throughout (frozen to the steering wheel, unable to
 speak or blink, hearing Woods shout), Woods's is active (out of the truck, calling Johnson
 to come and look). **That reads very differently from verbatim agreement and the node should
 say so in those words.** They also diverge on the object: Johnson waking says "big" and
 "white"; under regression it becomes "a big building"; the narration says "massive glowing
 red orb", which is the production's voice and matches neither witness.
- **Material interest after contact.** A GoFundMe was launched on the two men's behalf
 [02:37:05]-[02:37:24] and the episode is commercially sponsored. Recorded plainly.

**Grade it Tier 2 and carry it.** Under the old rule Johnson would have been excluded and the
board would have lost the clearest documented instance in its files of a second witness being
produced, prompted and assented into an account - with the prompting timestamped. That is the
Castello lesson from the triage rule's own section 2, running in the other direction.

---

## 11. THE REGISTER - every nuclear-facility witness found in this pass

Columns as the brief specifies. "Pre-contact statement" answers: had this person said anything
publicly about this event before an interested party reached them? **"On board"** is as of the
membership check in section 0.

| Name | Base | Claimed date | Role / rank | How the account reached the public | Anything said before an interested party made contact? | On board |
|---|---|---|---|---|---|---|
| Robert L. Salas | Malmstrom (Oscar Flight) | 24 Mar 1967 (earlier: 16 Mar) | Capt., missile launch officer | Approached the *Great Falls Tribune* himself, 1996; later books, affidavit, NPC 2010 | **Yes** - he is the origin of the strand | **YES** |
| Frederick Meiwald | Malmstrom (Oscar Flight) | 24 Mar 1967 | Col. (then Lt), crew commander | Private letter to Salas 1 Oct 1996; Hastings tapes Aug 1996 and 6 May 2011 | **No** | no |
| Walter Figel | Malmstrom (Echo Flight) | 16 Mar 1967 | 1Lt, later Col., deputy crew commander | Hastings audio tapes, 2008, 2009, 2010. Declined an affidavit | **No** | no |
| Eric D. Carlson | Malmstrom (Echo Flight) | 16 Mar 1967 | Capt., crew commander | Through his son and through researchers. Denies the UFO element | **No** | no |
| Robert Jamison | Malmstrom | Mar 1967 | Capt., ICBM combat targeting team | Hastings interview; affidavit; NPC 2010 | **No** | no |
| Robert J. Kaminski | Malmstrom (Echo Flight) | Mar 1967 | Boeing engineer, investigation team | 1997 letter to Jim Klotz | **No** | no |
| Dwynne Arneson | Malmstrom | 1967 | Lt Col, 28th Air Division, communications | Affidavit; NPC 2010 | Not established | no |
| Bruce Fenstermacher | F. E. Warren | 1974-1977 | Capt., missile combat crew commander | Affidavit; NPC 2010 | Not established | no |
| Patrick McDonough | F. E. Warren | 1962-1966 | Geodetic surveyor | Affidavit; NPC 2010 | Not established | no |
| Jerry (Jerome) Nelson | Walker AFB, Roswell | 1962-1965 | Deputy missile crew commander, 579th SMS | Affidavit; NPC 2010 | Not established | no |
| Charles I. Halt | RAF Bentwaters/Woodbridge | 26-28 Dec 1980 | Lt Col, deputy base commander | **Wrote the primary document himself in Jan 1981**; 2010 affidavit; NPC 2010 | **Yes, and as an official act** | **YES** |
| Robert M. Jacobs | Vandenberg / Big Sur | 22 Sep 1964 | Lt, OIC photo-optical instrumentation, 1369th Photo Sqn | *National Enquirer* 1982; *MUFON UFO Journal* Jan 1989 | **Yes** | **YES** |
| Kingston A. George | Vandenberg / Big Sur | 22 Sep 1964 | Civilian project engineer, 1st Strategic Aerospace Division | *Skeptical Inquirer* Winter 1993 and Jan-Feb 2009 | **Yes** - and against the UFO reading | **YES** |
| Florenz J. Mansmann | Vandenberg / Big Sur | Sep 1964 | Major, present at the site | Letters to Lee Graham (1983), from Jacobs (1985), to T. Scott Crain (May 1987) | **No** - reached the record through researchers' correspondence | no |
| Bradford Runyon | Minot | 24 Oct 1968 | Capt., B-52H co-pilot, JAG-31 | **Contacted CUFOS himself in 2000** | **Yes, self-initiated** | no |
| Charles Richey / Patrick McCaslin / Thomas Goduto / Arlie Judd | Minot | 24 Oct 1968 | B-52H crew | Named in the 1968 debriefing roster and the Blue Book file | **They are in the contemporaneous record, not in an interview** | no |
| James A. Partin | Minot | 24 Oct 1968 | Major, pilot, 23rd Bomb Sqn | **AF Form 117 questionnaire, 1968** | Contemporaneous official statement | no |
| Lloyd M. Isley / Robert M. O'Connor | Minot | 24 Oct 1968 | A1C, 91st MIMS | AF Form 117, 1968 | Contemporaneous | no |
| Joseph P. Jablonski / Gregory Adams / James F. Bond / William E. Smith Jr. | Minot | 24 Oct 1968 | A1C and SSgt, 862nd SPS | AF Form 117, 1968 | Contemporaneous | no |
| Danny K. Lewis | Loring | 27 Oct 1975 | SSgt, 42nd SPS | **USAF message traffic, 1975** | Contemporaneous duty report | no |
| Clifton W. Blakeslee / William J. Long | Loring | 28 Oct 1975 | Sgt / SSgt, 42nd SPS | USAF message traffic, 1975 | Contemporaneous | no |
| James P. Sampley | Loring | 27 Oct 1975 | SSgt, 2192nd Comm Sqn, control tower radar | USAF message traffic, 1975 | Contemporaneous | no |
| Grover K. Eggleston | Loring | 27 Oct 1975 | Sgt, control tower | USAF message traffic, 1975 | Contemporaneous | no |
| Richard E. Chapman | Loring | 27 Oct 1975 | Col., Commander 42nd Bomb Wing | Implemented Security Option 3; named in the record | Contemporaneous | no |
| Steven Eichner / R. Jones | Loring | 28 Oct 1975 | Sgt, B-52 crew chief and crew | *Clear Intent* (1984) interview; not in the message traffic | **Through researchers** | no |
| Michael D. Scott / David E. Mott / Richard R. Fuhs | Loring | Oct 1975 | SSgt / TSgt / Capt., 42nd SPS | Named in the record | Contemporaneous | no |
| Myron Taylor | Wurtsmith | 30 Oct 1975 | Capt., instructor navigator, KC-135 | **Memo for the Record, 18 Jan 1979, to the wing historian** | An official memorandum, written for the Air Force's own history | no |
| Frederick Pappas / K. E. May / Rick Meier / Randy Higginbotham / Steve Smith | Wurtsmith | 30 Oct 1975 | KC-135 crew | Named in Taylor's 1979 memo | Contemporaneous-adjacent | no |
| Martin E. Tackabury / Michael J. Myers / Robert J. Anderson / Roger Skipper / James A. Miller | Wurtsmith | 30 Oct 1975 | Airmen and Sgts, security police and motor pool | USAF message traffic and the 1979 historian's file | Contemporaneous | no |
| Paul J. Cahill | Wurtsmith | 17 Jan 1979 | SSgt, 379th BW historian | **"Research Record of Events", 17 Jan 1979** - a negative finding about his own wing history | An official act | no |
| Joseph M. Chassey | Malmstrom | Nov 1975 | SSgt | Hastings's material | Not established | no |
| Robert Peisher | Malmstrom | Nov 1975 | Lt Col (USAF Ret.) | Hastings's material | Not established | no |
| Klawon | Grand Forks | 4-5 Nov 1975 | Capt., 321st SPS | USAF message traffic, 1975 | Contemporaneous | no |
| Snelling / Johnson / Williams / Howell | F. E. Warren; Sioux Army Depot | 1 Aug 1965 | Capt., Col. (base commander), Col. (CO Sioux Army Depot), Capt. | **Project Blue Book telephone log kept by Lt. Anspaugh, 1 Aug 1965; published by J. Allen Hynek, 1972** | Contemporaneous official log | no |
| Mario Woods | Ellsworth | 18 Nov 1977 | USAF security policeman, 44th MSS | Public since 1996; 40+ claimed media appearances; American Alchemy 5 Jul 2025 and Jesse Michels `rjUdn6FklAU`, 7 Sep 2026 | **Yes, since 1996** | no |
| Michael Johnson | Ellsworth | 18 Nov 1977 | USAF security policeman, 44th MSS | **Located by the publishing party from a viewer's Facebook tip via an unnamed recruiter; first contact 26 June 2026** | **NO. NOTHING ABOUT THE EVENT. One undated Facebook post placing him at the base in the right years and saying nothing else** | no |

**Count: 47 named individuals in the register** (counting each person once, including the
grouped crew rows). **Of those, 43 are ABSENT from the board and 4 are present** - Salas,
Halt, Jacobs and George. That ratio is the gap this pass exists to document.

**The split that matters more than the count.** **26 of the 47 reached the record through
contemporaneous official paper** - message traffic, memoranda for the record, duty logs, AF
Form 117 questionnaires, a Blue Book telephone log, a wing historian's file. **13 reached it
through a researcher's interview programme, and of those, at least 4 (Figel, Meiwald, Jamison,
Kaminski) through one man's.** The remaining handful published under their own names first.
**That is the pattern the board should be able to query, and it is why every witness row needs
the "how it reached us" field populated rather than left blank.**

---

## 12. A BOARD ERROR FOUND IN PASSING - flagged, not fixed

`malmstrom-echo-flight-1967` currently reads, in its `desc`:

> Col. Robert Mansmann, who was involved in the technical investigation, wrote to Peter Bons on
> 8 March 1983, to Lee Graham on 30 January 1983 and to T. Scott Crain on 6 May 1987 about it,
> and those letters too are published in facsimile.

**That is almost certainly wrong, and in two ways at once.**

1. **The name.** The officer is **Florenz J. Mansmann**, a Major, not "Robert Mansmann", a
 Colonel. Kingston George's *Skeptical Inquirer* photograph caption of Winter 1993, opened
 in full by this session, reads: "In front of George in uniform are Major Florenz Mansmann
 and Chief Warrant Officer Guy Spooner."
2. **The event.** Those letters are **Big Sur letters, not Echo Flight letters.** Wikipedia's
 Big Sur article, opened by this session, states: "Florenz Mansmann, a major who was
 involved in the project, reportedly confirmed the account in a May 1987 letter to a UFO
 researcher." Search results independently associate the 6 May 1987 letter to T. Scott Crain
 with the Vandenberg Big Sur incident and a 1983 letter to Lee Graham likewise, and record a
 letter from Jacobs to Mansmann of 14 January 1985. **The correspondents match; the event
 does not.** Mansmann is Robert Jacobs's corroborating witness at Vandenberg in 1964. He has
 no established connection to the Malmstrom engineering investigation of 1967.

**Do not fix this from this file.** The letters themselves were not opened and the exact dates
in circulation differ between sources (30 January versus 10 March 1983 for the Graham letter).
**What should happen is a targeted verification pass that opens the three letters, and until
then the claim should be marked `unverified` on the node.** If it is confirmed as a
misattribution, the correct destination for these letters is `big-sur-1964` and a new
`florenz-mansmann` node, and the Echo Flight node loses a corroboration it never had. That is
a meaningful change to the strongest-looking parts of the Malmstrom case and it should be made
carefully.

---

## 13. PROPOSED NODES AND EDGES

**The structure is the point.** Each base is a hub. Witnesses edge INTO an incident; incidents
edge INTO the base. Degree on a base hub then answers "how many claimants converge here", and
the tier tags on the incoming edges answer "and how many of those legs are documented".

### 13a. Base hubs - new

| id | cls | label | one line | node tier | why it must exist |
|---|---|---|---|---|---|
| `l-loring` | location | Loring AFB, Maine | SAC installation at Limestone, Maine, home of the 42nd Bombardment Wing and its nuclear weapons storage area; the first base in the October-November 1975 penetration sequence; closed 1994 | **B** | The NMCC memorandum of 29 Oct 1975 is a Tier 1 document about this installation by name. Eleven named witnesses converge here |
| `l-wurtsmith` | location | Wurtsmith AFB, Michigan | SAC installation at Oscoda, home of the 379th Bombardment Wing; site of the 30 October 1975 weapons-storage-area incursion and the KC-135 pursuit over Lake Huron; closed 1993 | **B** | Twelve named witnesses; and it carries the board's only documented instance of a wing history omitting an event its own historian then recorded |
| `l-minot` | location | Minot AFB, North Dakota | SAC installation, home of the 91st Strategic Missile Wing and the 5th Bomb Wing; 1966 incursions, the 24 October 1968 B-52 case, and a named appearance in the 11 November 1975 CINCNORAD message | **B** | Already the hub of two board events (`minot-1966`, `minot-1968`) with no location node to hang them on. **Its node must record the Minot AFB / Minot Air Force Station ambiguity in the 1975 NORAD records** |
| `l-ellsworth` | location | Ellsworth AFB, South Dakota | SAC installation near Rapid City; 44th Strategic Missile Wing, active January 1962, inactivated 4 July 1994; Minuteman field including Launch Facility November-5 | **C** | The Ellsworth 1977 claim has no hub. AARO's own Volume I is reported to record interviews with officers who served here |
| `l-warren` | location | F. E. Warren AFB, Wyoming | SAC installation at Cheyenne; the 1 August 1965 Blue Book telephone log; SAMSO's post-Echo-Flight EMP test programme on Delta Flight; Fenstermacher and McDonough's base | **B** | It appears on **both** sides of this dossier: as a witness site and as the place the Air Force went to test the EMP hypothesis. That double role is exactly what a hub is for |
| `l-grand-forks` | location | Grand Forks AFB, North Dakota | SAC installation, 321st Strategic Missile Wing; the 4-5 November 1975 alert-ramp incident with alleged shots fired | **C** | The only incident in the 1975 sequence alleging weapons discharge, and the one this pass established least well |

**One more, and it is overdue:** `strategic-air-command` as an `entity`. Every incident in
this dossier happened inside SAC, the Security Option 3 alert posture is a SAC construct, and
the board currently has `norad-northcom` and `usaf` with nothing between them. Without it, the
1975 sequence has no institutional spine.

### 13b. Incident nodes

| id | cls | label | status | node tier |
|---|---|---|---|---|
| `sac-overflights-1975` | event | 1975 SAC Nuclear-Base Overflights | **ENRICH, existing id.** Keep as the umbrella. Add the NMCC memorandum's full text, the distribution list, the escalation to MG Sniffin and the State Department, the Air Force Intelligence Service alert log entry of 31 Oct 1975, and the Minot Air Force Station caveat | existing |
| `loring-1975` | event | Loring AFB penetrations, 27-31 October 1975 | NEW. Child of the umbrella. Anchored on the NMCC memorandum and the 42 BW message traffic | **B** |
| `wurtsmith-1975` | event | Wurtsmith AFB incursion, 30 October 1975 | NEW. Anchored on the NORAD Command Director's Log 31 Oct 75/0445Z, the JCS OPREP of 30 Oct 1975, and the 1979 historian's file | **B** |
| `malmstrom-1975` | event | Malmstrom missile-field overflights, 7-19 November 1975 | NEW. Anchored on the 24th NORAD Region Senior Director's Log, quoted in section 3c | **B** |
| `malmstrom-echo-flight-1967` | event | Malmstrom AFB missile shutdowns, March 1967 | **ENRICH, existing id. AND SPLIT ITS SUBTITLE.** It currently reads "Echo Flight and Oscar Flight ... events" as though they are one. Retitle to Echo Flight, 16 March 1967, and move Oscar Flight to its own node. Add the verbatim unit-history quotations from section 5 on BOTH sides, the Mansmann flag from section 12 into `unverified` | existing |
| `malmstrom-oscar-flight-1967` | event | Malmstrom Oscar Flight claim, 24 March 1967 | NEW. **Tier 2 throughout, and its node narrative must say in its own words that no released unit history mentions it and that the 24 March date comes from Robert Jamison via Robert Hastings** | **C** |
| `minot-1968` | event | Minot AFB B-52 incident, 24 October 1968 | **ENRICH, existing id.** Add the document inventory in section 6 item by item, and the Runyon-approached-CUFOS provenance | existing |
| `minot-1966` | event | Minot AFB incursions, 1966 | **ENRICH, existing id.** Edge it to the new `l-minot` | existing |
| `warren-1965` | event | F. E. Warren AFB sightings, 1 August 1965 | NEW. Anchored on the Blue Book telephone log kept by Lt. Anspaugh, first published by Hynek in 1972 | **B** |
| `ellsworth-1977` | event | Ellsworth AFB Launch Facility November-5 claim, 18 November 1977 | NEW. **Tier 2. Node narrative must state that no Air Force record of the event has been produced by anyone, and that the claimed date's only anchors are Woods's public accounts from 1996 and the two 2025-2026 broadcasts** | **C** |
| `big-sur-1964` | event | Big Sur missile-test filming, September 1964 | **ENRICH, existing id.** Add George's own 1964 staff study by title and date; the 22 September 1964 dating; the two captioned photographs; Mansmann and Spooner named | existing |

### 13c. Person nodes - new, all Tier 2 for their claims

`frederick-meiwald`, `robert-jamison`, `patrick-mcdonough`, `dwynne-arneson`,
`bruce-fenstermacher`, `jerry-nelson`, `walter-figel`, `eric-carlson`, `james-carlson`,
`robert-kaminski`, `bradford-runyon`, `florenz-mansmann`, `mario-woods`, `michael-johnson`,
`tim-hebert`.

**Every one of these carries a `provenance` statement in its narrative answering the four
section 2a questions.** Where the answer to "what did they say before an interested party
contacted them" is nothing, **the node says "nothing" in those words**, because that is a
finding.

**And the negative witnesses go on at the same tier as the positive ones.** `eric-carlson`
denies the UFO element; `james-carlson` and `tim-hebert` argue against it; `kingston-george`
is already on the board arguing against Jacobs. A board that carries only the affirming half
of a dispute is not a map, it is an argument.

### 13d. Document nodes - new

| id | cls | label |
|---|---|---|
| `doc-nmcc-loring-1975` | document | NMCC Memorandum for Record, "AFB Penetration", 29 October 1975, with four DDO updates |
| `doc-norad-24th-log-1975` | document | 24th NORAD Region Senior Director's Log, Malmstrom AFB, 7-19 November 1975 |
| `doc-cincnorad-1975-11-11` | document | CINCNORAD four-part message to NORAD units, 11 November 1975 |
| `doc-wurtsmith-historian-1979` | document | SSgt Paul J. Cahill, "Research Record of Events", 379th BW, 17 January 1979, and Capt. Myron Taylor's Memo for the Record, 18 January 1979 |
| `doc-minot-1968-blue-book` | document | Project Blue Book Minot case file: Werlich's Basic Reporting Data 28 Oct 1968, final report 13 Nov 1968, seven AF Form 117s, thirteen radarscope photographs |
| `doc-warren-1965-bluebook-log` | document | Project Blue Book telephone log, F. E. Warren AFB, 1 August 1965, kept by Lt. Anspaugh; published by Hynek 1972 |
| `doc-si-big-sur-1993` | document | Kingston A. George, "The Big Sur 'UFO': An Identified Flying Object", *Skeptical Inquirer* Vol. 17, Winter 1993, pp. 180-187 |
| `doc-341-smw-history-1967` | document | **ENRICH, existing id.** Add the FOIA chain (request 9 May 2001, release 14 June 2001, signed Marty S. Stephens) and the verbatim conclusions on both sides |

### 13e. Edges - the shape, not an exhaustive list

**Witness → incident** (`witness-chain`), **incident → base** (`geographic`), **document →
incident** (`investigative`), **document → base** (`geographic`), **base → SAC**
(`institutional`), **incident → domain** (`d-nuc`, `d-nuclear`, `d-witness`).

Worked examples in the board's existing edge grammar:

- `danny-lewis` → `loring-1975`, `witness-chain`, **claimTier 1** - he is named in 1975 message
 traffic, not in an interview.
- `loring-1975` → `l-loring`, `geographic`, claimTier 1.
- `loring-1975` → `sac-overflights-1975`, `temporal`, claimTier 1.
- `doc-nmcc-loring-1975` → `loring-1975`, `investigative`, claimTier 1.
- `walter-figel` → `malmstrom-echo-flight-1967`, `witness-chain`, **claimTier 2**, with a note
 in capitals: **HIS ACCOUNT EXISTS ONLY AS ROBERT HASTINGS'S AUDIO RECORDINGS OF TELEPHONE
 CALLS IN 2008, 2009 AND 2010. HE DECLINED TO SIGN AN AFFIDAVIT. NO PRE-CONTACT PUBLIC
 STATEMENT BY HIM HAS BEEN IDENTIFIED.**
- `robert-jamison` → `malmstrom-oscar-flight-1967`, `witness-chain`, claimTier 2, note: **HIS
 RECOLLECTION IS THE SOLE BASIS FOR THE 24 MARCH 1967 DATE THAT SEPARATES OSCAR FLIGHT FROM
 ECHO FLIGHT. IT REACHED THE PUBLIC THROUGH ROBERT HASTINGS.**
- `michael-johnson` → `ellsworth-1977`, `witness-chain`, claimTier 2, note: **LOCATED BY THE
 PUBLISHING PARTY ON 26 JUNE 2026 FROM A VIEWER'S FACEBOOK TIP. NO DATED PUBLIC STATEMENT BY
 HIM ABOUT THIS EVENT EXISTS PRIOR TO THAT CONTACT. ON THE RECORDED CALL HE ANSWERED "NO"
 BEFORE THE ORIGINAL WITNESS NAMED THE UFO. THE ACCOUNTS AGREE ON SUBSTANCE AND DIVERGE ON
 POSTURE AND AGENCY.** This is the `michael-herrera` standard applied.
- `mario-woods` → `ellsworth-1977`, `witness-chain`, claimTier 2, note: public since 1996 and
 named Johnson on air for years while asking audiences to find him - **which is both the
 reason the reunion is possible and the reason it cannot be treated as independent.**
- `robert-hastings` → each of `walter-figel`, `frederick-meiwald`, `robert-jamison`,
 `robert-kaminski`: `custody` or `research`, claimTier 2, **and these four edges are the
 circular-reporting cluster the triage rule's section 5 query is meant to surface. Type them
 consistently so the query finds them.**
- `kingston-george` → `robert-jacobs`, `denial`, claimTier 1 for the service facts he
 confirms and Tier 2 for the dispute - the board already has this shape and it is the model.
- `l-warren` → `malmstrom-echo-flight-1967`, `institutional`, claimTier 1: SAMSO ran the
 post-incident EMP test programme at Warren's Delta Flight. **A base hub that is on both
 sides of a case is the most interesting kind of hub the board can have.**

---

## 14. WHAT I COULD NOT ESTABLISH

1. **AARO Historical Record Report Volume I.** 403 to both WebFetch and curl. Not opened by
 this session. The board's citation of its page 30 stands on an earlier pass.
2. **"Report of Engineering Investigation of Echo Flight Incident, Malmstrom AFB, Mont. -
 16 Mar 67," by Engineering Investigation Team, 23 March 1967.** The document the entire
 Malmstrom question turns on. Classified (S) when written, footnoted on almost every page of
 the released history, and **not opened by anyone on this board**. Everything either side
 says about Echo Flight's causation is a reading of a history's summary of this report.
3. **Bernard C. Nalty, *USAF Ballistic Missile Programs 1967-1968* (1969).** Quoted at one
 remove for the "electronic noise pulse" finding. Not opened.
4. **Col. Frederick Meiwald's letter of 1 October 1996.** Not opened, and two incompatible
 characterisations of its contents are in circulation.
5. **James Carlson's own publications.** *American, Credulous* and *Echo Flights of Fantasy*.
 Not opened. **The largest gap in the case-against section.**
6. **The Figel recordings.** Hastings describes three taped calls. No URL opened by this
 session carries the audio or a full transcript.
7. **The Wall Street Journal report of June 2025** on a classified EMP vulnerability test as
 the cause. Not opened. Nothing here rests on it.
8. **Whether the 1975 NORAD records mean Minot AFB or Minot Air Force Station.** The 24th
 Region log says Station and "the radar station"; CINCNORAD's message nine days later says
 Minot AFB. Unresolved.
9. **The Loring 42 BW unit history for October-December 1975**, at AFHRA. Not sought online.
 Given the Wurtsmith precedent, its contents are genuinely unpredictable.
10. **The Grand Forks 4-5 November 1975 messages** in their own text. The alleged shots fired
 at the alert ramp is the most serious single allegation in the 1975 sequence and it is the
 one supported here only by a secondary page.
11. **The Mansmann letters** of 1983, 1985 and 1987, in facsimile, and therefore the
 misattribution flagged in section 12 is flagged, not proven.
12. **Michael Johnson's identity.** As the in-repo triage file says and as Johnson himself
 asks on the call, the episode does not settle that this is the right Michael Johnson. Only
 his DD-214, his OMPF, or the 44th Missile Security Squadron duty roster for the night of
 17-18 November 1977 would settle it.
13. **Robert Hastings's witness-recruitment method.** Two pages of his own site opened, two
 different totals given, no description of method on either. **This is the single most
 consequential unanswered section 2a question in the whole dossier**, because roughly a
 dozen proposed nodes depend on it.

### The three best document leads, in order

1. **"Report of Engineering Investigation of Echo Flight Incident, Malmstrom AFB, Mont. -
 16 Mar 67", Engineering Investigation Team, 23 March 1967.** Cited by exhibit and page
 number throughout the released history, so its existence, authorship and date are already
 documented. A FOIA request to AFHRA or NARA for the report itself, nearly sixty years on,
 is the single highest-value action available on this entire subject. It would settle
 causation, and it would settle whether the "UFO rumours were disproven" sentence rests on
 anything more than a Mobile Strike Team that was at the wrong flight.
2. **The 44th Missile Security Squadron duty roster and Michael Johnson's DD-214 / Article 15
 record for November 1977.** As the in-repo triage file already argues, an Article 15
 generates a dated paper record, and a separation document carries a unit and a date.
 Requestable by the veteran himself. It is the only thing that converts the Ellsworth case
 from testimony into documents, in either direction.
3. **The complete OASD FOIA compilation from which the 24th NORAD Region log was extracted.**
 The extracted pages are numbered 450, 451 and 452 and carry control number 000974 over
 Colonel Terrence C. James's release line. **There are at least 449 pages of that compilation
 this board has never seen**, and they are the same release stream that produced the Loring,
 Wurtsmith, Falconbridge and Cannon material. Identifying and obtaining the full compilation
 would likely double the Tier 1 documentary base of this entire cluster in one request.
