# REQUEST QUEUE
## Actionable closures against the 674 open questions

Generated 24 August 2026. Source: `data/l0-model.json` (110 L0 nodes, 674 `dossier.openQuestions`),
cross-read against `notes/L0-IMPLEMENTATION-2026-08-13.md` Stages 8 to 10 ("Genuinely blocked, not
deferred", "Still open", "Recurring research obstacles").

**What this is.** 674 open questions were triaged into four buckets. 601 of them are not on this
list, because they are questions about the interior of classified compartments, about intent, or
about what somebody meant. They stay open. What follows is the 73 that are closable, or partly
closable, by a specific filable request or a manual retrieval a person can do at a desk.

**How the ordering works.** Each section is ranked by expected value over difficulty. Expected value
means how much the board's argument moves if the request succeeds. Difficulty means the realistic
probability of a substantive response inside a year. The top of Section 1 is deliberately weighted
toward records the agency has already conceded exist, in writing, in a document it has already
released. Those are the requests that survive a "does not reasonably describe" rejection and that
cannot be Glomared, because the agency has already un-Glomared them.

**Sourcing discipline.** Every case number, contract number, document number and archive reference
in this file is attested in `l0-model.json` or in the implementation notes. Nothing has been
invented. Where a record is inferred rather than attested, the entry says "if it exists" and
describes the record by content.

> **Correction to the tasking.** Two case numbers supplied in the work order do not appear anywhere
> in the board data: **DODOIG-2021-000806** and **APP-00031-2022**. A full-text search of
> `l0-model.json`, `the-program.json`, `l0-extract.json` and all `program-*.js` files returns zero
> occurrences of either. The DoD IG case the board actually records is **DODOIG-2025-000932**
> (released publicly 7 January 2026, closed February 2025, not substantiated, heavily redacted
> complainant, explicitly a different person from Grusch). Do not cite the two unverified numbers in
> any filed request. Citing a case number that does not exist gives the FOIA officer a free
> administrative closure.

---

# SECTION 1 - FOIA REQUESTS

18 requests. Index first, then the full text of each.

| # | Agency / office | What it gets | Nodes closed |
|---|---|---|---|
| 1 | NARA (Office of General Counsel FOIA) | RG 615 compliance register | `nara-uap-collection`, `ndaa-fy2024`, `us-house` |
| 2 | DIA (FOIA Office, DIA-FOIA) | AAWSAP closeout property inventory and obligation history | `aawsap`, `baass`, `dia`, `earthtech-international` |
| 3 | OSD/JS FOIA (FOID) | YANKEE BLUE remand search result | `yankee-blue` |
| 4 | NASA Langley Research Center FOIA | WB-57F N927NA tasking, 18-19 Dec 2023 | `langley-2023-incursions`, `nasa` |
| 5 | Army DEVCOM GVSC via TACOM FOIA | CRADA 19-15 close-out report and test data | `ttsa-army-crada`, `adam-research-project`, `ttsa` |
| 6 | DHS S&T FOIA | KONA BLUE enclosures 1-4 and the Lute provenance paper | `kona-blue`, `aatip` |
| 7 | DIA FOIA (appeal live) | The 38th DIRD, the tasking memorandum, the distribution list | `dird-series`, `aatip`, `baass` |
| 8 | OSD/JS FOIA (DoD SAPCO equity) | Abba March 2023 memorandum; 21 Nov 2020 DepSecDef charter | `dod-sapco`, `carve-out`, `aaro` |
| 9 | DIA FOIA | BAASS Ten Month Report, CITA, monthly status reports | `aawsap`, `hearing-2025-09-09`, `dia` |
| 10 | Air Force (SAF/AAII) + AFHRA Maxwell | 1975 northern-tier overflight message traffic | `sac-overflights-1975` |
| 11 | OSD/JS FOIA (AARO equity) | Volume II working file and congressional notification | `aaro-historical-record-vol2`, `aaro-historical-record-vol1`, `aaro` |
| 12 | ODNI FOIA | Classified annex distribution record; UAPTF Director identity | `odni`, `odni-preliminary-assessment-2021`, `uap-task-force` |
| 13 | GAO (4 C.F.R. Part 81, **not** FOIA) | NSIAD-95-187 working papers; sec. 6803 audit products | `gao-nsiad-95-187`, `ndaa-fy2023-sec-6802`, `oversight-congress` |
| 14 | Naval Safety Command FOIA | W-72 hazard report and Range Fouler reports 2014-2015 | `roosevelt-2014-2015` |
| 15 | Dept of the Air Force (SAF/AAII) + AFOSI | Service-level YANKEE BLUE stop order and AFOSI files | `yankee-blue`, `afosi` |
| 16 | Navy (CNO FOIA / NHHC) | USS Princeton records and disposition certificates, Nov 2004 | `nimitz-2004` |
| 17 | FBI (FOIPA, Norfolk equity) | Langley December 2023 investigative file status | `langley-2023-incursions` |
| 18 | Air Force (SAF/AAII) + CIA (IMS) | Battelle Project STORK contract file; 9 Jan 1953 Cross memo | `battelle`, `blue-book-special-report-14` |

---

## F1. NARA - the RG 615 compliance register

**Agency and office.** National Archives and Records Administration, FOIA Officer, Office of General
Counsel, 8601 Adelphi Road, College Park MD 20740. Cross-file a copy with the National Declassification
Center, which is the operational custodian of the collection.

**Records described.** All records of agency compliance with sections 1841 through 1843 of the
National Defense Authorization Act for Fiscal Year 2024, Public Law 118-31, in respect of the
Unidentified Anomalous Phenomena Records Collection (Record Group 615), for the period 22 December
2023 to date, specifically: (a) the register, log, tracking sheet or database of agency transmittals
and certifications received by the Archivist; (b) each agency certification of completion of the
section 1842(c)(1) review, and each certification of a null return; (c) each notice of postponement
made under section 1843 and the 15-day notices to Congress attaching to them, with counts by agency;
(d) the subject guidebook and index required by section 1841(a)(1)(D), or any draft of it; (e) any
correspondence with agencies that failed to respond by the 30 September 2025 statutory deadline; and
(f) any NARA guidance, memorandum or legal opinion addressing whether records classified as
Restricted Data or Formerly Restricted Data under the Atomic Energy Act fall inside or outside the
transfer obligation.

**Board nodes and questions closed.** `nara-uap-collection` Q0, Q1, Q2, Q3, Q6, Q7, Q10;
`ndaa-fy2024` Q1, Q2; `us-house` Q0; `doe` Q0; `cia` Q0; `dia` Q0; `odni` Q3; `nro` Q0. That is
fourteen open questions across eight nodes off one request.

**Prior request to reference.** None known. State that no prior request is being referenced and that
this is a first-instance request for records-management artefacts, not for the substantive records.

**Why it ranks first.** These are administrative records of a records programme. They carry no
classification equity of their own. A null answer is as valuable as a positive one: if NARA holds no
compliance register, then Congress created a collection with a deadline and no enforcement instrument,
and the board can say so on NARA's own authority rather than by inference.

**Paste-ready records description.**
> All records constituting or documenting agency compliance with sections 1841-1843 of Public Law
> 118-31 in respect of the Unidentified Anomalous Phenomena Records Collection (Record Group 615),
> 22 December 2023 to the present, including any register or log of agency transmittals and
> certifications, all agency certifications of completion of the section 1842(c)(1) review, all
> agency null-return certifications, all section 1843 postponement notices with counts by agency,
> the section 1841(a)(1)(D) subject guidebook and index or any draft thereof, and any NARA guidance
> or legal opinion addressing the treatment of Restricted Data or Formerly Restricted Data under the
> transfer obligation.

---

## F2. DIA - the AAWSAP closeout property inventory and obligation history

**Agency and office.** Defense Intelligence Agency, FOIA Office (DAN-1A), 7400 Defense Pentagon,
Washington DC 20301-7400.

**Records described.** All records relating to contract **HHM402-08-C-0072**, awarded 22 September
2008 by the DIA Virginia Contracting Activity to Bigelow Aerospace Advanced Space Studies LLC (CAGE
54JU7, DUNS 827037768) under solicitation **HHM402-08-R-0211**, specifically: (a) the property
inventory and return record required by the statement of work clause providing that "Any accountable
property acquired by the contractor with government funds during the execution of this contract shall
become government owned property... This property must be inventoried and returned to the government
not more than 60 days after the end of the contract"; (b) the obligation-by-fiscal-year record and
all funding documents, the line-item prices for which were withheld under exemption (b)(4) in prior
releases; (c) all contract modifications including the FY10 option modification; (d) the executed DD
Form 254 and the amendment changing Block 13 from a pre-implementation Top Secret facility clearance
requirement to an as-soon-as-possible requirement, together with any record of the date on which a
Top Secret facility clearance was in fact granted, or of the fact that none was; (e) the deliverable
acceptance record and contract closeout file; and (f) the contracting officer's representative
designation and the internal approval chain for award.

**Board nodes and questions closed.** `aawsap` Q0, Q1, Q3, Q4; `baass` Q0, Q2; `dia` Q1, Q2;
`earthtech-international` Q0; `nids` Q7.

**Prior requests to reference.** Cite **FOIA-00349-2018** (award document HHM402-08-C-0072, released
13 October 2022), **FOIA-00269-2018** (commercial-items order, released 28 June 2023), and
**FOIA-00255-2022** (the DIA info memo to USD(AT&L), released in draft and in a four-page final).
Framing to use: the released statement of work itself mandates the closeout inventory, so its
existence or documented absence is a fact DIA has already put in the public domain.

**Why it ranks second.** This is the single strongest procurement request on the board. If the
inventory exists, it is a list of physical property bought with appropriated money under a UAP
contract and titled to the government. If it does not exist, DIA failed to execute a mandatory
closeout clause on a contract it now characterises as unauthorised, which is itself the finding.

**Paste-ready records description.**
> All records relating to DIA contract HHM402-08-C-0072 (solicitation HHM402-08-R-0211), awarded 22
> September 2008 to Bigelow Aerospace Advanced Space Studies LLC, specifically: the accountable
> property inventory and return record required within 60 days of contract end by the statement of
> work; all obligation and funding documents showing amounts obligated by fiscal year; all contract
> modifications including the FY10 option modification; the executed DD Form 254 and its amendment to
> Block 13; any record of the date a Top Secret facility clearance was granted to the contractor; the
> deliverable acceptance record; and the contract closeout file. Prior releases of the award document
> and commercial-items order were made under FOIA-00349-2018 and FOIA-00269-2018.

---

## F3. OSD - the YANKEE BLUE remand search result

**Agency and office.** Office of the Secretary of Defense / Joint Staff FOIA Requester Service Center
(FOID), 1155 Defense Pentagon, Washington DC 20301-1155.

**Records described.** (a) All records responsive to the search ordered on the remand of case
**25-A-3514**, decided by the Acting Chief of the OSD FOIA Division on 12 December 2025 and released
as appellate decision **25-A-3514-A1**, including any interim response, search declaration, tasking
memorandum to searched components, and negative-search certification; (b) any directive, memorandum,
message or guidance issued in calendar year 2023 by or on behalf of the Secretary or Deputy Secretary
of Defense ordering the cessation of briefings or indoctrinations representing to personnel that they
were being admitted to a programme concerning the reverse engineering of recovered non-human craft,
or the cessation of the presentation of fabricated or inauthentic materials to cleared personnel; and
(c) the search records showing which OSD components were tasked, expressly including the OSD Executive
Secretariat, the Office of the Under Secretary of Defense for Intelligence and Security, the Office of
the Under Secretary of Defense for Policy, and AARO.

**Board nodes and questions closed.** `yankee-blue` Q0, Q4; partially Q3.

**Prior request to reference.** Yes, and this is the whole point of the request. Cite case
**25-A-3514** and appellate decision **25-A-3514-A1**, quoting the operative sentence: the appellate
authority remanded "your request to FOID for a search for responsive records." Also cite the
authorities the appeal was won on, *Oglesby v. U.S. Dep't of Army*, 920 F.2d 57 (D.C. Cir. 1990), and
*Campbell v. DOJ*, 164 F.3d 20 (D.C. Cir. 1998), and note that the original search was confined to
the Correspondence Management Division.

**Why it ranks third.** The Department's own appellate authority has already found the Department's
categorical no-records answer inadequate and ordered the search redone. This request does not ask the
agency to concede anything. It asks it to produce the result of a search it has already committed to
performing. As of the last published status the case remains open, so a status demand is procedurally
proper.

**Paste-ready records description.**
> All records located by, and all records documenting the conduct of, the search ordered on remand in
> OSD FOIA case 25-A-3514 by the appellate decision of 12 December 2025 (released as 25-A-3514-A1),
> including any interim or final response, search tasking memoranda, component search declarations,
> and any 2023 Secretary- or Deputy Secretary-level directive ordering cessation of briefings
> representing admission to a programme concerning reverse engineering of recovered non-human craft
> or the presentation of inauthentic materials to cleared personnel.

---

## F4. NASA - WB-57F N927NA tasking, 18 and 19 December 2023

**Agency and office.** NASA Langley Research Center FOIA Office, Mail Stop 166, Hampton VA 23681,
with a copy to NASA Johnson Space Center (the WB-57F High Altitude Research Program is operated out
of Ellington Field).

**Records described.** For the aircraft with civil registration **N927NA** on 18 and 19 December 2023:
flight logs and flight records; the sensor tasking order or equivalent tasking document; the mission
request, requestor identity and any sponsor correspondence, including any request originating from
the Department of Defense, NORAD, USNORTHCOM, Air Combat Command, Joint Base Langley-Eustis or the
FBI; the imagery or sensor product inventory generated on those dates and the recipient of each
product; and the entry in the NASA airborne science flight calendar recording the tasking as "Imagery
Support" together with any record explaining the relationship between that tasking and the stated
SpaceX CRS-29 capsule return imaging mission.

**Board nodes and questions closed.** `langley-2023-incursions` Q3, and materially advances Q6 and
Q11; `nasa` Q0, Q1.

**Prior request to reference.** None. Reference instead NASA Langley Research Center's own public
statement that the aircraft was on the East Coast to image the CRS-29 return and that "while in the
area, the aircraft provided additional imaging support in Virginia," and NASA's public airborne
science calendar listing for those two dates.

**Why it ranks fourth.** A tail number, two calendar dates and an entry NASA itself published. There
is no plausible "does not reasonably describe" rejection. NASA is a civil agency with a weak
classification posture and a strong scientific-data release culture. If the flight was tasked by a
military requestor against the Langley incursions, the tasking correspondence is the single cleanest
document tying a federal sensor asset to the event.

**Paste-ready records description.**
> All flight records, flight logs, mission requests, sensor tasking orders, sponsor or requestor
> correspondence, and imagery or sensor product inventories for NASA WB-57F aircraft registration
> N927NA for 18 and 19 December 2023, including any request or tasking originating from the
> Department of Defense, NORAD, USNORTHCOM, Air Combat Command, Joint Base Langley-Eustis or the
> Federal Bureau of Investigation, and any record relating the "Imagery Support" entry on the NASA
> airborne science flight calendar for those dates to the SpaceX CRS-29 capsule return imaging
> mission.

---

## F5. Army - CRADA 19-15 close-out report and test data

**Agency and office.** U.S. Army TACOM Life Cycle Management Command FOIA Office, Warren MI 48397,
for DEVCOM Ground Vehicle Systems Center (formerly CCDC GVSC), 6501 E. 11 Mile Road, Warren MI.
Cross-file with the DEVCOM Office of Research and Technology Applications (ORTA).

**Records described.** All records relating to **CRADA No. 19-15, "Novel and Emerging Technology
Exploitation (NETE)"**, between To The Stars Academy of Arts and Science and CCDC Ground Vehicle
Systems Center, specifically: (a) the signature page showing each signatory and the date of the last
authorised signature fixing the Effective Date under Article 4.3; (b) all Government test reports,
test plans, laboratory notebooks and analytical results produced under the Joint Work Plan, including
any characterisation of metamaterial samples supplied by the Collaborator; (c) the CRADA close-out or
final report; (d) any CRADA Invention disclosure and any record of the Collaborator exercising or
declining the exclusive-license option under 15 U.S.C. section 3710a(b)(2); (e) the material
disposition record at expiry of the sixty-month term, showing whether samples were returned,
retained, consumed in testing or transferred; and (f) all correspondence with the Collaborator's
principal investigator, Luis Elizondo, and with Government principal investigators Ben Soave and Dr.
Joseph Cannon, and ORTA representative Andrea Simon.

**Board nodes and questions closed.** `ttsa-army-crada` Q1, Q2, Q4, Q5, Q7; `adam-research-project`
Q0, Q5; `ttsa` Q0, Q1.

**Prior request to reference.** Yes. The executed 26-page CRADA was released to The Black Vault by
Doug Halleaux, public affairs officer for CCDC Ground Vehicle Systems Center, redacted only for
telephone numbers. Cite that voluntary release as establishing that the agreement is unclassified and
that GVSC has already determined its release does not harm national defence. That framing directly
attacks `ttsa-army-crada` Q5, which asks why DoD later applied national-defence and foreign-policy
exemptions to records of an agreement the Army publicly described as routine unclassified materials
research.

**Paste-ready records description.**
> All records relating to CRADA No. 19-15, "Novel and Emerging Technology Exploitation (NETE)",
> between To The Stars Academy of Arts and Science and CCDC (now DEVCOM) Ground Vehicle Systems
> Center, including the executed signature page with dates, all Government test plans, test reports
> and analytical results produced under the Joint Work Plan, the close-out or final report, any CRADA
> invention disclosure and licensing correspondence under 15 U.S.C. 3710a(b)(2), the disposition
> record for all material samples at expiry of the sixty-month term, and correspondence with
> principal investigators Ben Soave and Dr. Joseph Cannon and ORTA representative Andrea Simon. The
> executed agreement was previously released by GVSC public affairs.

---

## F6. DHS - KONA BLUE enclosures and the Lute-tasked provenance paper

**Agency and office.** Department of Homeland Security, Science and Technology Directorate FOIA
Office, 245 Murray Lane SW, Washington DC 20528. Cross-file with the DHS Privacy Office FOIA unit,
which processed the original KONA BLUE package.

**Records described.** Records relating to the prospective special access program KONA BLUE,
established under DHS Instruction 140-04-001 on approval by Under Secretary for Science and Technology
Tara O'Toole and terminated in December 2011, specifically: (a) Enclosures 1 through 4 to the action
memorandum of 28 November 2011 from Under Secretary O'Toole, including Enclosure 1, described in that
memorandum as an "AATI Program History, dated 23 Nov 2011"; (b) the 5 to 10 page paper documenting
"how we got to where we are now with the KONA BLUE program, its provenance (history) while at DIA,
and exactly what science would be researched", tasked by Deputy Secretary Jane Holl Lute to Under
Secretary O'Toole and Chief SAPCO Steven J. Cover at the SAPOC meeting of 21 November 2011, together
with any record that the paper was not produced; (c) an unredacted or less-redacted version of the
General Counsel remarks by Ivan Fong recorded in the 21 November 2011 SAPOC minutes on the rationale
for SAP status; (d) records identifying the "other entities" holding the "body of previous work...
that requires a SAP level classification to access it" referenced in the November 2011 action memo;
and (e) the administrative debriefing records of 5 June 2013 and any explanation of the seventeen-month
interval between termination and debriefing.

**Board nodes and questions closed.** `kona-blue` Q0, Q1, Q2, Q4, Q5; `aatip` Q1, Q3;
`manhattan-project-2` Q3.

**Prior request to reference.** Reference the joint DoD-DHS declassified KONA BLUE package already in
the public domain, which contains the establishment memo, decision briefing, SAPOC minutes, action
memo, termination memo and memorandum for the record. The enclosures being sought are cited by number
and title inside documents DHS has already released. This is the "the agency has admitted it exists"
test in its purest form.

**Paste-ready records description.**
> Enclosures 1 through 4 to the Under Secretary for Science and Technology action memorandum of 28
> November 2011 concerning KONA BLUE, including the document described therein as "AATI Program
> History, dated 23 Nov 2011"; the 5-10 page programme provenance paper tasked by the Deputy
> Secretary to the Under Secretary for Science and Technology and the Chief SAPCO at the SAP Oversight
> Committee meeting of 21 November 2011, or any record that it was not produced; a less-redacted
> version of the General Counsel remarks recorded in the 21 November 2011 SAPOC minutes; and the
> administrative debriefing records of 5 June 2013.

---

## F7. DIA - the 38th DIRD, the tasking memorandum and the distribution list

**Agency and office.** Defense Intelligence Agency, FOIA Office (DAN-1A).

**Records described.** (a) The SECRET-classified version of the Defense Intelligence Reference
Document titled "State of the Art and Evolution of High-Energy Laser Weapons", being the
thirty-eighth of the thirty-eight DIRDs produced under contract HHM402-08-C-0072, which was neither
released nor listed as withheld in the release of 25 March 2022; (b) the internal DIA tasking or
topic-selection memorandum identifying who selected the thirty-eight DIRD topics, when, and against
what intelligence requirement; (c) the distribution list for the DIRD series, showing all offices
inside and outside DIA that received the documents; and (d) any record that a DIRD author held or was
offered a special access read-in in connection with the work.

**Board nodes and questions closed.** `dird-series` Q0, Q1, Q2, Q3; `aatip` Q5; `baass` Q3;
`earthtech-international` Q1.

**Prior requests to reference.** Cite **FOIA-0159-2018** (the bulk DIRD request, completed 25 March
2022 with thirty-seven of thirty-eight released) and **FOIA-0033-2019** (the listing breakdown). State
the procedural posture precisely: the thirty-eighth document was not listed as withheld under any
exemption, which is why the live appeal was filed on adequacy of search rather than applicability of
exemption. Note that an unclassified version of the same paper is in the released set as DIRD 23, at
thirty-one pages, so the subject matter is not itself the classification equity.

**Paste-ready records description.**
> The SECRET version of the Defense Intelligence Reference Document "State of the Art and Evolution of
> High-Energy Laser Weapons", produced under contract HHM402-08-C-0072 and not addressed in the
> release of 25 March 2022 under FOIA-0159-2018; the DIA tasking or topic-selection memorandum
> identifying who selected the thirty-eight DIRD topics and against what requirement; and the
> distribution list for the DIRD series. An unclassified version of the same paper was released in the
> same set as DIRD 23.

---

## F8. OSD - the Abba memorandum and the STAOC charter

**Agency and office.** OSD/JS FOIA Requester Service Center, with routing to DoD SAPCO for equity
review. Expect a referral. File it anyway, because a referral creates a dated record that the
document was located.

**Records described.** (a) The memorandum issued in March 2023 by Maj. Gen. David Abba, Director of
the DoD Special Access Program Central Office, cited in the AARO Memorandum for Record "Invitations
to Interview Mr. David Grusch" as AARO's access authority, including its full text, classification
markings and distribution, and specifically whether it authorised disclosure to AARO of waived-SAP
information or only non-waived material; (b) the Deputy Secretary of Defense memorandum of **21
November 2020** establishing the Special (or Special/Sensitive) Technical Activities Oversight
Committee, for which the Director of DoD SAPCO serves as Executive Secretary under DoD Directive
5205.07; (c) the Deputy Secretary of Defense Memorandum of **11 July 2023**, "Implementation Guidance
for DoD Special Access Program Enterprise Reform", which DoDD 5205.07 (12 September 2024) both
incorporates and cancels without separate publication; and (d) the identity of the current Director,
DoD SAPCO, and of Abba's successor.

**Board nodes and questions closed.** `dod-sapco` Q1, Q3, Q4; `carve-out` Q2; `aaro` Q3;
`aaro-fy2025-annual-report` Q4; `usc-10-119` Q3.

**Prior request to reference.** Cite **24-F-0266**, the case under which the AARO Memorandum for
Record referencing the Abba memorandum was released. The board records that this MFR cites the March
2023 SAPCO memorandum by name as AARO's access authority. An agency that has released a document
citing a second document by name and date cannot easily claim the second is not reasonably described.

**Paste-ready records description.**
> The March 2023 memorandum of the Director, DoD Special Access Program Central Office, cited as
> AARO's access authority in the AARO Memorandum for Record "Invitations to Interview Mr. David
> Grusch" released under FOIA 24-F-0266; the Deputy Secretary of Defense memorandum of 21 November
> 2020 establishing the Special Technical Activities Oversight Committee; and the Deputy Secretary of
> Defense Memorandum of 11 July 2023, "Implementation Guidance for DoD Special Access Program
> Enterprise Reform", cancelled and incorporated by DoDD 5205.07 of 12 September 2024.

---

## F9. DIA - the BAASS Ten Month Report and the Comprehensive Integrated Threat Assessment

**Agency and office.** Defense Intelligence Agency, FOIA Office (DAN-1A).

**Records described.** The deliverables accepted under contract HHM402-08-C-0072 other than the
Defense Intelligence Reference Documents, being the line items recorded on the Standard Form 1449 as
status reports, a project management plan for tasks 3.a.1 through 3.a.12, research reports for the
same tasks, and a **Comprehensive Integrated Threat Assessment**, and specifically: (a) the report of
approximately 494 pages prepared by the contractor and commonly described as the Ten Month Report;
(b) the Comprehensive Integrated Threat Assessment; (c) all monthly status reports; (d) the project
management plan; (e) the contractor's proposal or proposals to establish laboratories to examine
recovered UFO materials, referenced in AARO's Report on the Historical Record of U.S. Government
Involvement with UAP, Volume I; and (f) the contractor personnel roster or key-personnel list
submitted under the contract.

**Board nodes and questions closed.** `aawsap` Q2; `dia` Q1, Q3; `hearing-2025-09-09` Q2, Q3;
`baass` Q2, Q5; `dird-series` Q4.

**Prior requests to reference.** FOIA-00349-2018, FOIA-00269-2018 and FOIA-0159-2018 as the
established release history on this contract. Quote AARO Volume I's own concession that the
contractor made "proposals to set up laboratories to examine any recovered UFO materials" as the
government's admission that item (e) exists.

**Paste-ready records description.**
> All contract deliverables accepted under DIA contract HHM402-08-C-0072 other than the thirty-eight
> Defense Intelligence Reference Documents, specifically the Comprehensive Integrated Threat
> Assessment, the project management plan for tasks 3.a.1 through 3.a.12, all monthly status reports,
> the approximately 494-page report commonly described as the Ten Month Report, and the contractor's
> proposal or proposals to establish laboratories to examine recovered UFO materials as referenced in
> AARO's Historical Record Report Volume I.

---

## F10. Air Force - the 1975 northern-tier overflight message traffic

**Agency and office.** Department of the Air Force FOIA (SAF/AAII), 1000 Air Force Pentagon,
Washington DC 20330. Cross-file a research request with the Air Force Historical Research Agency,
600 Chennault Circle, Maxwell AFB AL 36112, which holds the wing histories.

**Records described.** For the period 27 October to 15 November 1975: (a) **Alaskan Air Command
message 012224**, subject "Unidentified Foreign Object", referenced in the Air Force Intelligence
Service Alert Officer's Log entry of 3 November 1975 and declared unavailable by the Air Force in
February 1978, together with any record of its disposition or destruction; (b) the SAC Security Police
message subject-lined "Defense Against Helicopter Assault" transmitted to northern-tier bases from
Pease to Barksdale directing assumption of Security Option 3 during hours of darkness; (c) the
operational report containing the assessment that "the unknown helicopter has demonstrated a clear
intent in the weapons storage area, is smart and a most capable aviator"; (d) all OPREP-3 and priority
message traffic to the National Military Command Center, the Chief of Staff of the Air Force, Fort
Ritchie, SAC Headquarters and Ninth Air Force reporting penetration of the Loring AFB weapons storage
area; (e) the press posture guidance requested by CINCNORAD on 11 November 1975 and any SAFOI product
responding to it; (f) the histories of the 42nd Bomb Wing (Loring AFB) and the 379th Bomb Wing
(Wurtsmith AFB) for October-December 1975 and the supporting documents to those histories; and (g)
any AFOSI file relating to the questioning of Capt. Higginbotham following the KC-135 pursuit over
Lake Huron on 30 October 1975.

**Board nodes and questions closed.** `sac-overflights-1975` Q0, Q1, Q3, Q4, Q5, Q8; `afosi` Q5.

**Prior request to reference.** None held on the board. Reference instead the Air Force's own
February 1978 statement that message 012224 was unavailable, and the 18 January 1979 "Memo for the
Record" by instructor navigator Capt. Myron Taylor written for 379th Bomb Wing historian SSgt Paul J.
Cahill, which is already in the public record and establishes that a wing-history file on the event
exists.

**Paste-ready records description.**
> Alaskan Air Command message 012224, subject "Unidentified Foreign Object", referenced in the Air
> Force Intelligence Service Alert Officer's Log of 3 November 1975, together with any disposition or
> destruction record; the Strategic Air Command Security Police message "Defense Against Helicopter
> Assault" directing northern-tier bases to assume Security Option 3; all OPREP-3 and priority message
> traffic reporting unidentified object activity over the Loring AFB and Wurtsmith AFB weapons storage
> areas between 27 October and 15 November 1975; the press posture guidance requested by CINCNORAD on
> 11 November 1975; and the histories and supporting documents of the 42nd and 379th Bomb Wings for
> October to December 1975.

---

## F11. OSD / AARO - the Volume II working file

**Agency and office.** OSD/JS FOIA Requester Service Center, with AARO equity.

**Records described.** Relating to the report required by section 6802 of the James M. Inhofe National
Defense Authorization Act for Fiscal Year 2023 (Public Law 117-263), codified at 50 U.S.C. 3373(j):
(a) any deliverable, draft, outline, interim product or working file labelled or referred to as Volume
II of the Report on the Historical Record of U.S. Government Involvement with Unidentified Anomalous
Phenomena, in any classification, and the identity of the office holding it; (b) any notification,
letter or briefing memorandum transmitted to the congressional defense or intelligence committees
concerning the status, delay or non-production of Volume II; (c) any inquiry received from a
congressional committee concerning Volume II and the response; (d) the interview log or schedule for
the approximately thirty interviews conducted for Volume I, showing dates, tier assignments and
whether an interviewee declined, invoked counsel or was denied clearance to speak, with names
withheld as necessary under exemption (b)(6); (e) the record of the decision not to interview David
Grusch, including the AARO Memorandum for Record on invitations to interview him; and (f) the
clearance and coordination record for Volume I, including any recorded dissent.

**Board nodes and questions closed.** `aaro-historical-record-vol2` Q1, Q2, Q4, Q6;
`aaro-historical-record-vol1` Q0, Q2, Q3; `aaro` Q0; `yankee-blue` Q3; `ndaa-fy2023-sec-6802` Q0.

**Prior request to reference.** Cite **24-F-0266** for the AARO Memorandum for Record on invitations
to interview Grusch, which establishes that AARO documents its interview-invitation decisions in
writing and therefore that item (d) and item (e) exist as a record class.

**Paste-ready records description.**
> All records concerning Volume II of the Report on the Historical Record of U.S. Government
> Involvement with Unidentified Anomalous Phenomena required by section 6802 of Public Law 117-263 (50
> U.S.C. 3373(j)), including any draft, outline, interim product or working file in any
> classification; all correspondence with congressional committees concerning its status, delay or
> non-production; the interview log or schedule for the approximately thirty interviews conducted for
> Volume I with names redacted as necessary; and the coordination and clearance record for Volume I
> including any recorded dissent.

---

## F12. ODNI - the classified annex distribution record and the UAPTF Director's name

**Agency and office.** Office of the Director of National Intelligence, Information Management Office,
Washington DC 20511.

**Records described.** Relating to the Preliminary Assessment: Unidentified Aerial Phenomena of 25
June 2021: (a) the transmittal, distribution or receipt record for the classified annex, showing which
congressional committees and which executive branch offices received it and on what dates. This
request is for the distribution record, not for the annex; (b) the identity of the individual serving
as Director, Unidentified Aerial Phenomena Task Force, on 25 June 2021, whose name was withheld under
exemption (b)(6) in the version released under case **DF-2021-00275** and approved for release 24
March 2022, with the argument that a senior official's identity in an official capacity carries a
minimal privacy interest against a substantial public interest in a document responding to a Senate
demand to name the accountable official; (c) records of the deconfliction attempt described in the
assessment by which the UAPTF sought to check the 144 reports against U.S. classified developmental
programs, including the offices queried and the offices that declined; and (d) any record of action
taken by ODNI or the Director of National Intelligence on the Intelligence Community Inspector
General's credible-and-urgent determination on the Grusch complaint.

**Board nodes and questions closed.** `odni` Q0, Q1, Q2, Q5; `odni-preliminary-assessment-2021` Q0,
Q1, Q2; `uap-task-force` Q1, Q2; `house-oversight-committee` Q4.

**Prior request to reference.** **DF-2021-00275**, the case under which the redacted assessment was
released. The redaction pattern is already characterised on the board: (b)(1) and (b)(3) withholdings
sit alongside the (b)(6) name redaction, which is the weakest of the three and the correct target.

**Paste-ready records description.**
> The transmittal and distribution record for the classified annex to the ODNI Preliminary Assessment:
> Unidentified Aerial Phenomena of 25 June 2021, showing recipient committees and offices and dates of
> transmittal; the name of the individual serving as Director, Unidentified Aerial Phenomena Task
> Force on 25 June 2021, withheld under exemption (b)(6) in the release under case DF-2021-00275; and
> records of the UAPTF's attempt to deconflict the 144 reports against United States classified
> developmental programs, including the offices queried and any office that declined to respond.

---

## F13. GAO - working papers and the section 6803 audit products

**Not a FOIA request.** The Government Accountability Office is a legislative branch agency and is not
subject to the Freedom of Information Act. File under GAO's own public access to records policy, 4
C.F.R. Part 81, addressed to the GAO Chief Quality Officer / records access programme.

**Records described.** (a) The audit working papers underlying **GAO/NSIAD-95-187**, "Results of a
Search for Records Concerning the 1947 Crash Near Roswell, New Mexico", including the record of which
classified documents GAO examined and the correspondence with the Air Force, the National Archives and
the FBI generated during that search; (b) any classified supplement, briefing memorandum or additional
letter provided to Rep. Steven Schiff beyond the published letter report; (c) all products of the
Comptroller General's audit and monitoring role under section 6803 of Public Law 117-263, including
any written product arising from the semiannual briefings to the congressional committees on AARO's
compliance; and (d) any GAO written declination of Rep. J. Edward Roush's request to investigate the
University of Colorado UFO Project, if it exists, and the stated grounds.

**Board nodes and questions closed.** `gao-nsiad-95-187` Q5, Q6; `roswell-1947` Q5;
`ndaa-fy2023-sec-6802` Q3; `oversight-congress` Q5; `senate-armed-services` Q4; `condon-committee` Q3.

**Prior request to reference.** None. Cite the reports by number and the statutory audit mandate by
section.

**Paste-ready records description.**
> Under 4 C.F.R. Part 81: the audit working papers underlying GAO/NSIAD-95-187, including the record
> of classified documents examined and correspondence with the Department of the Air Force, the
> National Archives and the Federal Bureau of Investigation; any classified supplement or briefing
> memorandum provided to Rep. Steven Schiff beyond the published letter report; all written products
> of the Comptroller General's audit and monitoring role under section 6803 of Public Law 117-263; and
> any written GAO declination of Rep. J. Edward Roush's request to investigate the University of
> Colorado UFO Project.

---

## F14. Navy - the W-72 hazard report and the Range Fouler reports

**Agency and office.** Naval Safety Command FOIA Office, 375 A Street, Norfolk VA 23511, with a copy
to the Department of the Navy FOIA/PA Office (DNS-36).

**Records described.** (a) The hazard report submitted by Strike Fighter Squadron 11 (VFA-11) arising
from the near mid-air collision in Warning Area W-72 during 2014 or 2015, in which two F/A-18F
aircraft approximately 100 feet apart took evasive action at the airspace entry point, together with
any endorsement, closure action or disposition record; (b) all hazard reports, safety reports and
"Range Fouler" reports filed by squadrons of Carrier Air Wing One during 2014 and 2015 concerning
unidentified objects in Warning Areas off the Virginia coast, with a count if individual records are
withheld; (c) the retention and disposition schedule applicable to those report series and any
destruction certificate applying to them; and (d) any record of transmittal of those reports to the
All-domain Anomaly Resolution Office or to the National Archives under sections 1841-1843 of Public
Law 118-31.

**Board nodes and questions closed.** `roosevelt-2014-2015` Q2, Q3, Q5.

**Prior request to reference.** None. Reference Ryan Graves's sworn testimony to the House Oversight
Committee of 26 July 2023, in which he states "Our squadron submitted a safety report", as the
statement of a percipient witness establishing that the record was created.

**Paste-ready records description.**
> The hazard report submitted by Strike Fighter Squadron 11 arising from the near mid-air collision in
> Warning Area W-72 in 2014 or 2015 involving two F/A-18F aircraft taking evasive action at the
> airspace entry point, together with all endorsements and closure actions; all hazard, safety and
> "Range Fouler" reports filed by Carrier Air Wing One squadrons during 2014 and 2015 concerning
> unidentified objects in Warning Areas off the Virginia coast; the applicable records retention
> schedule and any destruction certificate; and any record of transmittal of these reports to AARO or
> to the National Archives under Public Law 118-31.

---

## F15. Air Force and AFOSI - the service-level YANKEE BLUE stop order

**Agency and office.** Department of the Air Force FOIA (SAF/AAII), and separately the Air Force
Office of Special Investigations FOIA Office, Quantico VA. File two requests, not one, because the
Air Force secretariat and AFOSI maintain separate FOIA queues and a single filing will be split
anyway.

**Records described.** (a) Any memorandum, message, directive or guidance issued in calendar year 2023
by the Secretary of the Air Force, the Chief of Staff of the Air Force, the Chief of Space Operations,
or AFOSI, ordering personnel to cease briefing or indoctrinating cleared individuals into a programme
represented as concerning the reverse engineering of recovered non-human craft, or ordering cessation
of the presentation of fabricated or inauthentic materials to cleared personnel; (b) any AFOSI
investigative file, closure memorandum or Inspector General referral relating to that practice; (c)
any record of a notification made to the Secretary of the Air Force under Air Force Mission Directive
39 paragraph 2.2, being written notice that an official attempted to impede an investigation, on any
matter relating to unidentified anomalous phenomena; and (d) the OSI file series **24-185**
(Unconventional Aircraft - Special Inquiry) records not transferred to the National Archives in 1975,
and the disposition record for that series.

**Board nodes and questions closed.** `yankee-blue` Q2, Q4; `afosi` Q0, Q3, Q5.

**Prior request to reference.** Quote Pentagon spokesperson Susan Gough's response of 1 October 2025:
"I cannot confirm the existence of any department-level memo as described in the article. You may want
to ask the Air Force or other military services whether they put out such a memo to their personnel."
That is an on-the-record agency referral and should be quoted verbatim in the request as the basis for
filing with the service rather than with OSD. Do **not** cite the AFOSI case number carried in this
project's correction record: the board marks it explicitly as not independently verified against a
released response letter.

**Paste-ready records description.**
> Any memorandum, message or directive issued in calendar year 2023 by the Secretary of the Air Force,
> the Chief of Staff of the Air Force, the Chief of Space Operations or the Air Force Office of
> Special Investigations ordering cessation of briefings representing admission to a programme
> concerning reverse engineering of recovered non-human craft, or cessation of the presentation of
> inauthentic materials to cleared personnel; any AFOSI investigative file, closure memorandum or
> Inspector General referral relating to that practice; and the records of OSI file series 24-185
> (Unconventional Aircraft - Special Inquiry) not transferred to the National Archives in 1975,
> together with the disposition record for that series.

---

## F16. Navy - USS Princeton records and disposition certificates, November 2004

**Agency and office.** Department of the Navy FOIA/PA Office (DNS-36), 2000 Navy Pentagon, Washington
DC 20350, with cross-files to Naval History and Heritage Command (deck logs) and Commander, Naval
Surface Forces Pacific.

**Records described.** For USS Princeton (CG-59), USS Nimitz (CVN-68), Carrier Air Wing Eleven and
Strike Fighter Squadron 41, for 10 to 16 November 2004: (a) deck logs and Combat Information Center
logs; (b) the records retention schedule applicable to AN/SPY-1 radar recordings and any destruction
certificate, disposition form or retention decision applying to recordings from that period; (c) any
report of any kind generated contemporaneously, being safety, intelligence, mishap or operational; (d)
any record of a request, tasking or travel authorisation issued in or after 2009 for the collection of
data recordings or witness statements from Princeton or Nimitz personnel, including any request
originating from the Advanced Aerospace Weapon System Applications Program or its contractor; and (e)
any record of invitations issued to Lt. Cdr. Alex Dietrich to attend the Pentagon in connection with
the event, and the issuing office.

**Board nodes and questions closed.** `nimitz-2004` Q0, Q2, Q4, Q5; partially Q1.

**Prior request to reference.** None held on the board. Reference Cdr. David Fravor's sworn statement
filed for the House Oversight Committee hearing of 26 July 2023, which records the Princeton
controller's account of two weeks of Aegis tracks and states that no investigation followed. Frame the
request so that a documented absence is responsive: ask expressly for the retention schedule and any
destruction certificate, so that "no records" is accompanied by an authority.

**Paste-ready records description.**
> Deck logs and Combat Information Center logs for USS Princeton (CG-59) and USS Nimitz (CVN-68) for
> 10 to 16 November 2004; the records retention schedule applicable to AN/SPY-1 radar recordings
> together with any destruction certificate or disposition form applying to recordings from that
> period; any safety, intelligence, mishap or operational report generated contemporaneously; any
> request, tasking or travel authorisation issued in or after 2009 for collection of recordings or
> witness statements from Princeton or Nimitz personnel; and any record of invitations issued to Lt.
> Cdr. Alex Dietrich to attend the Pentagon in connection with the event.

---

## F17. FBI - the Langley December 2023 investigative file

**Agency and office.** FBI Record/Information Dissemination Section, 170 Marcel Drive, Winchester VA
22602, naming the Norfolk Field Office as the likely originating office.

**Records described.** All records relating to the Bureau's investigation of unmanned aerial system or
unidentified object incursions over Joint Base Langley-Eustis and surrounding areas of southeastern
Virginia between 6 December 2023 and 31 January 2024, including: the opening communication, the
closing communication and the finding on which the case was closed if it has been closed; the video
recording provided to the Bureau by civilian witness Jonathan Butner and any analysis of it; and
correspondence with NORAD, USNORTHCOM, Air Combat Command or Joint Base Langley-Eustis.

**Board nodes and questions closed.** `langley-2023-incursions` Q4, Q7.

**Prior request to reference.** None. Reference the NORAD/USNORTHCOM spokesperson's statement to The
War Zone in December 2023 that NORTHCOM "has been coordinating with [the] FBI" and referred further
questions to the Bureau, which is a government attribution of an FBI equity and defeats a
non-existence defence.

**Note on expected outcome.** If the investigation is open, expect exemption 7(A) in full. That is
still worth having: a 7(A) withholding is an official confirmation that an investigation exists and is
open, which by itself closes half of `langley-2023-incursions` Q4, which asks whether the investigation
was closed and on what finding.

**Paste-ready records description.**
> All records relating to the FBI's investigation of unmanned aerial system or unidentified object
> incursions over Joint Base Langley-Eustis and southeastern Virginia between 6 December 2023 and 31
> January 2024, including the opening and closing communications and any finding on which the matter
> was closed, the video recording provided by civilian witness Jonathan Butner and any analysis of it,
> and correspondence with NORAD, USNORTHCOM, Air Combat Command or Joint Base Langley-Eustis.

---

## F18. Air Force and CIA - the Battelle Project STORK contract file

**Agency and office.** Department of the Air Force FOIA (SAF/AAII) for the contracting and ATIC
records; Central Intelligence Agency Information and Privacy Coordinator for the Office of Scientific
Intelligence file.

**Records described.** (a) The contract file for the classified Battelle Memorial Institute support
effort code-named **Project STORK**, including the contract number, contracting activity, dollar
value, period of performance and all deliverables, together with the intermediate Project STORK status
reports; (b) the memorandum dated **9 January 1953** from Howard C. Cross of Battelle Memorial
Institute to Miles Goll at Wright-Patterson Air Force Base concerning what could and could not be
discussed at the Washington meetings of 14 to 16 January 1953, if it exists in Air Force or CIA
holdings; (c) the items listed at Tab B of the F. C. Durant memorandum of 16 February 1953 to the
CIA's Assistant Director for Scientific Intelligence, specifically evidence item 3, the Project STORK
progress reports; and (d) any Air Technical Intelligence Center or Office of Public Information record
documenting the decision to substitute the 1955 131-case three per cent figure for the unknown rate
computed in Special Report No. 14.

**Board nodes and questions closed.** `battelle` Q0, Q1, Q3, Q5; `blue-book-special-report-14` Q2, Q4;
`robertson-panel` Q5.

**Prior request to reference.** None. Cite the Durant memorandum of 16 February 1953 by date and Tab,
which is already public and which lists the STORK progress reports as an evidence item, so the record
class is attested in a released government document.

**Paste-ready records description.**
> The contract file for the classified Battelle Memorial Institute support effort code-named Project
> STORK, including contract number, contracting activity, value, period of performance, deliverables
> and all intermediate status reports; the memorandum of 9 January 1953 from Howard C. Cross of
> Battelle Memorial Institute to Miles Goll at Wright-Patterson Air Force Base, if it exists in agency
> holdings; and the Project STORK progress reports listed as evidence item 3 at Tab B of the F. C.
> Durant memorandum of 16 February 1953 to the Assistant Director for Scientific Intelligence.

---

# SECTION 2 - ARCHIVE AND MANUAL RETRIEVALS

Eleven items. Nothing here requires a lawyer, a fee or a wait. Every one is blocked only by a login, a
CAPTCHA, a page-range limit, a PDF viewer or a physical trip. Ordered by value over effort.

## A1. Congressional Record granule CREC-2023-07-26-pt1-PgS3627-2 - the verbatim SA 1053 text

**Where.** govinfo.gov, Congressional Record for 26 July 2023, granule
`CREC-2023-07-26-pt1-PgS3627-2`. The board's own citation for the printed text is **SA 1053 at 169
Cong. Rec. S3628-S3642**. In the daily-edition bound PDF the material sits at approximately **pages
2368 to 2374**.

**What to do.** Open the PDF in a viewer and read pages 2368-2374 by eye. Transcribe, in full: the
section numbering of the amendment as printed, the definitions of "legacy program", "controlling
authority", "technologies of unknown origin" and "non-human intelligence", the Review Board
provisions, the eminent domain provision, and the section corresponding to the contractor turn-in
mandate that was renumbered to Section 7343 of Division G.

**Why it is here.** Six automated primary-vehicle attempts failed. govinfo HTML and PDF of S.2226es
and S.2103rs, SSCI's engrossed PDF, and both formats of the Congressional Record granule all die at
the same character extraction ceiling of roughly 92,000 to 145,000 characters, always from file start,
with no range access. The nearest miss reached Title IX, about two printed pages short. A human with
a PDF reader closes this in twenty minutes. Nothing else on this list has a worse
value-to-effort ratio in the machine's favour and a better one in a person's.

**Nodes closed.** `samdt-797` Q0; `uapda-2023` Q4, Q5; `iaa-fy2024-sec-1102` Q0. It also upgrades the
board's Sec. 1102 turn-in claims from Tier 2 to Tier 1, which is a confidence restoration the notes
record as a deliberate downgrade at Stage 9.

## A2. SIAN - the Operação Prato item numbers

**Where.** `http://sian.an.gov.br/sianex/consulta/login.asp`. Consultation requires a gov.br account.
The site and its sibling `dibrarq` return anti-bot CAPTCHA pages to automated clients.

**What to search.** Two searches. First, the free-text term `operação prato`. The Arquivo Nacional has
stated, in its own answer to a litigant quoted in the federal judgment in **Recurso Cível
5002417-48.2022.4.04.7200/SC**, that this search returns **six documents, none audiovisual**. Second,
the reference code `BR DFANBSB ARX`, which the Senate record (RQS 193/2022 justificação) states returns
758 documents.

**What to retrieve.** The six item numbers and titles from the first search. Then the item-level
record for **ARX 184**, "Registros de Observações de OVNI", the compilation forwarding 130 OVNI records
catalogued between 2 September 1977 and 28 November 1978, and the name and rank in its signature
block. Then locate and cite by item number the signed final report of Capitão Uyrange Hollanda. Then
locate the September 2009 report on the 1986 events.

**Nodes closed.** `operacao-prato` Q0, Q1, Q2; `ev-noite-ovnis-1986` Q2; `arquivo-nacional-ufo` Q0, Q4.
The board's Stage 9 note records this explicitly: "No SIAN item numbers were obtained and none were
invented."

## A3. Biblioteca Nacional hemeroteca - the May 1986 Brazilian press

**Where.** `memoria.bn.gov.br`, the Hemeroteca Digital Brasileira. Automated fetches returned an empty
body. The site works in a browser.

**What to search.** Editions of **19, 20, 21, 24 and 25 May 1986** of, at minimum, *Folha de S.Paulo*,
*O Estado de S. Paulo*, *Jornal do Brasil* and *O Globo*. Search terms: `OVNI`, `objetos não
identificados`, `Moreira Lima`, `CINDACTA`, `Ozires Silva`, `F-5E`, `Mirage`, `Anápolis`, `Santa Cruz`.

**What to retrieve.** (a) The contemporaneous report of the 23 May 1986 press conference at the
Ministério da Aeronáutica, to establish the minister's most-quoted sentence in a primary source rather
than in retrospective reporting; (b) the object count as reported at the time, against the 21 used by
both the Arquivo Nacional and the Senate; (c) the names of the intercept pilots and the tail numbers
of the five aircraft; (d) any contemporaneous statement of the undertaking to publish a written report
within thirty days.

**Nodes closed.** `ev-noite-ovnis-1986` Q0, Q1, Q3. Listed in the implementation notes as blocked item
4: "The 1986 press coverage at memoria.bn.gov.br. Empty body returned."

## A4. UK National Archives DEFE 24/2090/1 and the Condign Volume 3 originals

**Where.** The National Archives, Kew. File **DEFE 24/2090/1**, the MoD internal-review correspondence
on the Condign redactions, is digitised and a full-text transcription is at
`archive.org/stream/396201-defe-24-2090-1`. Search the DEFE 24/2090 series and the wider DEFE 24
range for the parent file and for the surviving original three-volume copy that the MoD rediscovered,
per David Clarke's 2023 "Lost and Found" post.

**What to retrieve.** (a) The internal-review annex entries for **Volume 3, Chapter 4, page 3,
paragraph 12**, where the reviewer states that "information regarding DIS, the CIA desk officer and
DI51 must remain redacted", and any accompanying reviewer note identifying the desk officer's parent
office or the nature of the DI51 role; (b) the review entries for **Chapter 3 paragraph 8**, the
POTENTIAL APPLICATIONS section withheld in its entirety under Section 26, and for **Executive Summary
paragraph 9**, the country list withheld under Section 27; (c) the remaining pages of Volume 3 beyond
the 48-page released file, being the contents-page sections on Former Soviet Union Aircraft Incidents,
an FSU/Russian Experimental Vehicle, and OTHER NATIONAL ACTIVITY covering CHINA, SPAIN and USA and
CANADA; (d) Annex A, the two Russian scientific papers.

**Nodes closed.** `doc-condign-vol3` Q0, Q1, Q2, Q3, Q4; `doc-condign-report` Q3. The USA and Canada
section is the highest-value target on this item: it is a foreign defence intelligence organisation's
own assessment of US national activity on the subject, and the board has never reached it.

**Escalation if the file is silent.** A UK Freedom of Information Act 2000 request to the Ministry of
Defence Information Rights team, referencing the 2006 release and DEFE 24/2090/1, asking for internal
review of the continuing Section 26 and Section 27 withholdings on the grounds that twenty-six years
have elapsed and the Soviet institutions named are defunct.

## A5. docs.house.gov - the Immaculate Constellation twelve-page report

**Where.** `docs.house.gov`, House Oversight and Government Reform Committee, hearing of 13 November
2024. The printed hearing record's Index of Documents lists it as "Report, Pentagon, 'Immaculate
Constellation'; submitted by Rep. Mace" and states that "The documents listed above are available at:
docs.house.gov."

**What to retrieve.** The document itself, in whatever form it was posted. Record: whether it carries
classification markings, originator identifiers or control numbers; the full text of the second
section on US Government imagery intelligence, which has never been summarised publicly in detail; and
the Questions for the Record submitted to Shellenberger by Rep. Burlison and any published answers.

**Nodes closed.** `immaculate-constellation-12-page-report` Q0, Q1, Q3, Q4; `immaculate-constellation`
Q4; `house-oversight-committee` Q2.

**Note.** Q0 is a yes/no question about whether the document is in fact retrievable where the Index
says it is. A documented "not posted" answer is a finding about the committee, not a failure.

## A6. govinfo CHRG-118hhrg53022 - the final third of the 26 July 2023 hearing

**Where.** govinfo.gov, printed hearing record **CHRG-118hhrg53022**. Both the govinfo copy and the
committee transcript PDF truncate before the closing rounds of questioning when fetched
programmatically.

**What to do.** Open the PDF and read the final third by eye, or order the GPO print copy. Transcribe
the closing rounds of questioning, particularly any exchange concerning contractors named in open
session and any commitment to a classified follow-on session.

**Nodes closed.** `hearing-2023-07-26` Q3, and materially advances Q1 and Q4.

## A7. Senado Federal - DSF nº 99, pages 7 to 67

**Where.** The Diário do Senado Federal, issue **99**, carrying the full stenographic record of the
commemorative special session of **24 June 2022** held under Art. 199 RISF pursuant to RQS 193/2022.
Available through `legis.senado.leg.br`.

**What to retrieve.** The complete statements of the eight co-signatory senators and of A. J. Gevaerd,
beyond the Agência Senado summary; and the text of the **Carta de Brasília**, which the board has only
through that summary. Check specifically for any statement identifying Army or Navy holdings, and for
the 100-metre diameter figure and the 1954 primacy claim, both of which the board records as author's
assertions entered into the record rather than verified findings.

**Nodes closed.** `senado-brasil` Q2, Q4, Q5; partially Q1 and Q3.

## A8. Diário Oficial da União - Portaria nº 551/GC3

**Where.** `in.gov.br`, DOU archive, searching the period around **9 August 2010**.

**What to retrieve.** The published text of **Portaria nº 551/GC3 of 9 August 2010**, in full,
including Article 3 obliging CENDOC to send originals periodically. Confirm the signing authority's
name as printed, which resolves the Juniti Saito / Junichi Saito discrepancy against a DOU page rather
than against the FAB note and the Senate record.

**Nodes closed.** `fab` Q0, Q1. The board has already established that "Juniti Saito" is correct from
his own signed Ordem do Dia; the DOU page makes the attestation independent of the FAB.

## A9. National Archives at College Park - the AFOSI 24-185 series

**Where.** NARA II, College Park MD, Record Group 341 (Records of Headquarters United States Air
Force). The board records approximately three cubic feet of AFOSI UFO case material transferred in
1975.

**What to retrieve.** The finding aid and box list for the transferred material; the accession record
showing the transfer authority and date; and any indication in the accession paperwork of material
retained by AFOSI rather than transferred. Separately, request the disposition record for the
Wright-Patterson to Maxwell to NARA movement of the Project Blue Book files, which NARA's own page does
not state.

**Nodes closed.** `afosi` Q0; `project-blue-book` Q3, Q5.

## A10. NARA - the Bolender package attachments

**Where.** NARA II, College Park, and the Air Force Historical Research Agency at Maxwell. The target
is the staff package of **20 October 1969** signed by Brig. Gen. C. H. Bolender terminating Project
Blue Book, and specifically its sixteen attachments.

**What to retrieve.** **Attachment 8**, cited for the claim that Blue Book served no intelligence
function, and **Attachment 10**, cited for the JANAP 146 routing. Several of the sixteen have never
been released. Also seek the inventory, index or transfer record for the JANAP 146 (CIRVIS) and AFM
55-11 UFO reporting corpus for 1952 to 1969.

**Nodes closed.** `project-blue-book` Q0, Q1.

## A11. rules.house.gov and govinfo - the FY2027 amendment and the enrolled FY2024 text

**Where.** `rules.house.gov` for the H.R. 8800 amendment records, and govinfo for the enrolled text of
Public Law 118-31.

**What to retrieve.** (a) The amendment number and text as made in order by the House Rules Committee
for H.R. 8800. Reporting places it at amendment 1044; this has not been confirmed against the Rules
Committee record. Also determine whether it was adopted by voice vote, by division, or en bloc, given
that Roll Call 278 is the vote on passage of the underlying bill and not on the amendment. (b) A
direct full-text search of the **enrolled** Public Law 118-31 for "Review Board", "eminent domain",
"controlling authority" and "technologies of unknown origin". The board's negative claim that no such
text survives currently rests on NARA's description of the enacted sections rather than on the enrolled
text, because every full-NDAA fetch truncated.

**Nodes closed.** `uapda-fy2027-house-adopted` Q0, Q1, Q2; `uapda-2023` Q5.

---

# SECTION 3 - PAYWALLED OR PURCHASABLE

Six items. The fix is money, not effort. Total cost of the whole section is under 200 US dollars, most
of it a single-month WSJ subscription and two Elsevier article purchases. Ordered by value.

| # | Outlet / publisher | Item | Date | What it confirms | Node |
|---|---|---|---|---|---|
| P1 | The Wall Street Journal | Joel Schectman and Aruna Viswanatha, "The Pentagon Disinformation That Fueled America's UFO Mythology" | 6 June 2025 | Whether the article describes the alleged spring 2023 SecDef directive by date, originator or classification, and how it characterises its sourcing. Greenewald's public criticism is that it published neither the memorandum, nor its date, nor a description of sourcing. Reading the full text either confirms that criticism or supplies the descriptors that would make a targeted FOIA possible | `yankee-blue` Q0, Q1 |
| P2 | Elsevier, *Progress in Aerospace Sciences* vol. 128 | Nolan, Vallée, Jiang and Lemke, materials analysis paper | 2022 | The stated chain of custody for specimen CB_JV-1 between the 1977 Council Bluffs recovery and Vallée's retained fragment, and the identity and affiliation of "J. Roser", cited in both the 1998 and 2022 papers without a reference | `paper-nolan-vallee-2022` Q0, Q1 |
| P3 | The Wall Street Journal | Langley drone incursions reporting | October 2024 | The object dimensions, altitude and speed figures (approximately 20 feet, 3,000-4,000 feet, over 100 mph) currently held on the board only through The War Zone's verification of quotations, and any sourcing on the launch-point question | `langley-2023-incursions` Q0, Q8 |
| P4 | The Wall Street Journal | Reporting on drone overflights of the Department of Energy's Nevada National Security Site | October 2023 | Dates, duration and federal response, which is the only available basis for testing whether the Nevada events are operationally connected to Langley two months later or merely contemporaneous | `langley-2023-incursions` Q9 |
| P5 | Elsevier | The 2025 multi-author UAP review co-authored by Szydagis and Knuth | 2025 | The exact byline count, against the discrepancy between SCU's "thirty-four authors" and the UAlbany release's "more than 30 other researchers". Trivial in itself, but the board carries it as an open question and it costs one article purchase to close | `university-at-albany` Q5 |
| P6 | Revista UFO (back issue) | The August 1997 Cabo Frio interview with Capitão Uyrange Hollanda by A. J. Gevaerd and Marco Petit | 1997 | The full text of the recantation, as against the summary the board currently relies on, and any statement by Hollanda about the fate of photographs, film and the medical documentation of the Colares hospital admissions | `operacao-prato` Q3, Q4 |

**Not purchasable, time-locked.** The Jacques Vallée papers at Rice University's Woodson Research
Center, MS 0672, include a Series III file titled "11. The Robertson Panel and the 'Pentacle
Memorandum' - January 1953". Series I and II open **24 January 2028**; Series III case files open **1
January 2031**. This is the only known location of the 9 January 1953 Cross memorandum. It cannot be
bought and it cannot be requested. It can be diarised. See also F18, which seeks the same document
from the agency side.

---

# SECTION 4 - PERMANENTLY BLOCKED

Eleven questions or question-clusters where no document class exists in which the answer could appear.
This is a finding, not a failure. Where a record that should exist does not, say so and say why: an
absent artefact that ought to be present is evidence about the institution that failed to produce it.

## B1. Any identified instance, date or count of a 10 U.S.C. 119(e)(1) waiver

**Nodes.** `waived-sap-notification-group` Q1; `usc-10-119` Q0; `waived-usap` Q8, Q9;
`waived-usap` Q0, Q2, Q3; `classified-annex` Q1; `dodi-5205-11` Q1; `carve-out` Q3; `isoo` Q3.

**Why no document class exists.** Four independent closures, each sufficient on its own. First,
section 119 creates no public reporting requirement attaching to the fact that a waiver was exercised;
the statute is silent, so no agency is obliged to generate a releasable artefact. Second, the annual
reporting requirements at subsections (a) and (b), which were the only periodic comprehensive SAP
accounting to Congress, terminated on 31 December 2021 under Public Law 114-328 section 1061, so even
the classified stream stopped. Third, the Moynihan Commission recorded that waived-programme
notification was given only orally, meaning that for the relevant historical period the notification
itself was designed not to create a record. Fourth, a FOIA request naming a waived unacknowledged
programme is answerable with a Glomar response under exemptions (b)(1) and (b)(3), because
acknowledging the existence of the responsive record is the disclosure.

**The absent artefact that is evidence.** DoDI 5205.11, reissued 12 September 2024 and public,
requires the SAP Oversight Committee's annual review to assess "All waived DoD SAPs to determine the
need for continued waived status." That is an agenda item nobody drafts for an empty set. The category
is live, the review is annual, and the count has never been disclosed in any form, aggregate or
otherwise. Note also that subsections (a) and (b) terminated at the end of 2021 and DoD nonetheless
continues to designate waived SAPs "pursuant to Section 119."

## B2. The identity of the IC Controlled Access Program expanded in 2021

**Nodes.** `aaro-historical-record-vol1` Q1; `aaro-historical-record-vol2` Q0; `classified-annex` Q4;
`manhattan-project-2` Q5; `aaro` Q1.

**Why.** The nickname or codeword of a Controlled Access Program is itself classified information, and
the sponsoring element's identity is protected under exemption (b)(3) via 50 U.S.C. 3024(i), which
requires the DNI to protect intelligence sources and methods. No unclassified document class exists in
which a CAP nickname appears. AARO chose to describe the fact of the expansion without naming the
programme, the authorising official or the disestablishing official, which is the maximum the
classification system permits and the minimum the statute required. The only route is a congressional
committee in closed session, and no committee has published a finding.

**What is still worth asserting.** AARO put the sentence in writing in an unclassified report. The
board should keep treating the concession as the artefact and stop treating the name as obtainable.

## B3. The contents of any classified annex to an authorisation or appropriations act

**Nodes.** `classified-annex` Q0; `nip` Q1, Q2; `odni-preliminary-assessment-2021` Q1 in part.

**Why.** Two closures. The annex is a congressional document, and Congress is not an agency within
5 U.S.C. 551(1)(A), so FOIA does not reach it. Where an executive agency holds a copy, it holds it as
properly classified national defence information and withholds under (b)(1). For the National
Intelligence Program specifically, 50 U.S.C. 3306 requires disclosure of the aggregate topline only;
below-topline composition by agency, discipline or programme is statutorily protected, and no agency
maintains a releasable version. No annex from 1944 to the present has ever been released.

## B4. Anything held in congressional committee files

**Nodes.** `hearing-2023-07-26` Q0, Q1; `grusch-misappropriation-allegation` Q0, Q3;
`house-oversight-committee` Q1, Q2; `congressional-uap-caucus` Q0, Q5;
`task-force-declassification-federal-secrets` Q2, Q4, Q5.

**Why.** Congress is exempt from FOIA. Committee records are controlled by the committee under its own
rules, and a former member's or a chair's discretion is the entire access mechanism. Material submitted
to the Intelligence Community Inspector General under the Intelligence Community Whistleblower
Protection Act carries a further statutory protection at 50 U.S.C. 3033(g)(3). The names, locations and
documentation Grusch says he provided are therefore in three custodies (his own counsel, the ICIG, and
two intelligence committees), none of which is subject to a compelled-disclosure instrument a member
of the public can file.

**Route that is not blocked.** Constituent correspondence to a member of the Task Force is not a
records request and produces no compelled response, but it is the only channel that exists. Treat it
as advocacy, not retrieval, and do not book it in this queue.

## B5. Independent authentication of the Wilson-Davis notes

**Nodes.** `wilson-davis-memo` Q0, Q1, Q2; `earthtech-international` Q6.

**Why.** The alleged original is private property. It passed, on the account given, from a private
note-taker to the Edgar Mitchell estate to an anonymous online release in 2019. No federal record class
attaches at any point in that chain, no custodian is under any obligation to produce it, and no agency
ever held it. Handwriting authentication requires the physical original, and no person or institution
has claimed to hold one. Admiral Wilson has publicly disputed the document. The board's correct posture
is the one it already takes: the document sits in a congressional hearing file and AARO's Volume I
contains zero occurrences of "Wilson", and that silence is the finding.

## B6. The circumstances of Uyrange Hollanda's death beyond the coroner's ruling

**Node.** `operacao-prato` Q4.

**Why.** The Brazilian coroner recorded death by asphyxiation due to hanging and the death was ruled
suicide. A. J. Gevaerd, who conducted the interview weeks earlier and who has every professional
incentive to allege otherwise, states flatly that nobody "suicided" him and records a prior attempt on
his own life. There is no document class in which a contrary finding could appear absent a reopened
Brazilian inquest, and no party has sought one. The board's method forbids treating recantation
followed by death as evidentiary without a document, and no such document exists. This stays open as a
knot, permanently, and the honest statement of it is itself the entry.

## B7. AFOSI or DIA bigot lists and program-security records for an unacknowledged programme

**Node.** `afosi` Q2; `nro` Q1; `lockheed-martin` Q0.

**Why.** A bigot list for an unacknowledged special access programme is a record whose existence is
the fact at issue. Any agency response other than Glomar would confirm or deny the programme.
Similarly, carve-out approvals under 32 CFR 117.6 are approved by the Secretary or Deputy Secretary of
Defense and are not published, and the CFR imposes no counting or reporting requirement, so there is no
register to request and no aggregate to disclose. A named-company carve-out request is answerable with
a Glomar in every case.

## B8. Alternative Compensatory Control Measures usage for UAP-adjacent activity

**Node.** `waived-usap` Q4.

**Why.** ACCMs exist by design below the SAP establishment threshold and carry lighter reporting than
SAPs precisely so that the reporting that would create a document class does not attach. There is no
ACCM register, no congressional notification requirement, and no annual accounting. The absence is the
mechanism's purpose, and stating that is the finding.

## B9. The identity of the Immaculate Constellation author

**Node.** `immaculate-constellation` Q0; `hearing-2024-11-13` Q0.

**Why.** Michael Shellenberger has confirmed on the record that he knows the identity and has declined
to disclose it, which places the fact in journalistic source protection. No government record class
names a whistleblower who has not self-identified; identifying one in a releasable document would
itself be a reprisal under the Intelligence Community Whistleblower Protection Act. The only document
that could contain the name is an ICIG or committee file, which is closed under B4.

## B10. Whether any UAP record has ever been classified as Restricted Data

**Nodes.** `doe` Q0, Q1; `nara-uap-collection` Q3; `waived-usap` Q6; `gerb-mitre-investigation` Q5.

**Why, with a caveat.** Restricted Data and Formerly Restricted Data are classified under the Atomic
Energy Act of 1954, not under Executive Order 13526, so they sit outside the classification system that
ISOO oversees and outside the executive-order framework that the FY2024 NDAA transfer provisions were
drafted against. A record's RD status is itself derivative classified information. No document class
exists in which "this UAP record is Restricted Data" appears in releasable form.

**The caveat, and it matters.** The *policy* question is not blocked. Whether the Department of Energy
has asserted to NARA that responsive material is Restricted Data and therefore outside the section
1841-1843 transfer obligation is an administrative correspondence question, and it is inside the scope
of **F1**. The board records this as the single highest-value question on the `doe` node, and F1 is the
instrument that reaches it. Only the substantive answer is permanently blocked. The assertion is not.

## B11. The pre-1987 grandfathering question

**Node.** `waived-usap` Q10; `dod` Q2.

**Why.** Whether a programme predating the 1987 enactment of section 119 was ever brought into the SAP
reporting system, or whether legacy arrangements were grandfathered, would be answered only by the
pre-1987 SAP inventory, which was never created as a public record class, or by the terminated section
119(a) and (b) annual reports, which were classified and which stopped in 2021. The Department's
asserted forty-year gap between BLUE BOOK's termination in 1969 and AAWSAP's standup in 2008 rests on
the absence of a record rather than on a record of absence, and there is no instrument that converts
one into the other. State the asymmetry and stop.

---

# EXECUTION NOTES

**Filing order.** F1, F3, F4, F5 and F6 first, in one sitting. All five name records the agency has
already conceded exist in a document it has already released, all five have a short records
description, and none requires a fee waiver argument to be won before processing starts. F2, F7, F8 and
F9 next: same posture, larger record sets, longer queues at DIA.

**Fee waivers.** Request a fee waiver in every filing under the public-interest standard, citing the
statutory public interest established by section 6802 of Public Law 117-263 and sections 1841-1843 of
Public Law 118-31. If a waiver is denied, request news-media requester status as a secondary position
before agreeing to fees.

**Track the negatives.** Every "no records" response is a board artefact and should be entered as a
claim with the response letter as its source, not discarded. The `yankee-blue` node is built almost
entirely out of negative findings, and it is one of the better-documented nodes on the map. A search
that fails, documented, dated and signed, is evidence about the institution.

**Do not file.** Anything in Section 4. Filing a request that must be Glomared spends a requester's
credibility with a FOIA office for zero return and produces a response letter that says nothing the
board does not already know.

**Adversarial review.** This deliverable has not been through the three-layer audit. Say the word and
it goes through his managers.
