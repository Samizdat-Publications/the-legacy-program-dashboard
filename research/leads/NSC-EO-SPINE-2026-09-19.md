# Candidates: the NSC and the classification / covert-action spine, 1947 to 1985

19 September 2026. Item 3 of `notes/HANDOFF-2026-09-19-LATE.md` section 6c, "the cheapest
documented gap available". **This is a triage note, not a build.** Nothing here is on the
board yet.

Nine documents were opened during this session at the URLs given below. Where a URL failed
or served something other than the document, that is recorded too, because the next session
should not spend the time again.

**Read section 5 before building anything.** Six widely repeated claims about these
documents turned out to be wrong on the primary text, and three of them are claims this
board would plausibly have written.

---

## 1. What the board already has, which changes the shape of the gap

Checked against `data/the-program.json` before any research was done. Two of the three
findings cut the work down rather than adding to it.

| | |
|---|---|
| **No National Security Council node.** Nothing under any spelling | a genuine gap, and the handoff is right that it is glaring |
| **No National Security Act of 1947 node either**, which the handoff did not name | arguably the bigger one. It is the instrument the NSC, the CIA and the Office of Special Projects all derive from, and existing nodes already cite it in claim text without being able to point at it |
| **NSC 10/2 is ALREADY on the board in substance** | `cia-office-of-policy-coordination` (Tier B, `ic`, dateStart 1948-06-18) carries five Tier 1 claims quoting the charter verbatim, including the plausible-deniability sentence and the section 102(d)(5) authority, with edges to `cia`, `harry-s-truman` and `d-psyop` |
| Between `atomic-energy-act-1946` and `eo-12829` (1993) the board carries **nothing** | the entire 1947 to 1985 spine is absent, which is the period in which the classification system this board is about was actually built |

**So do not build a separate `nsc-10-2` document node that re-quotes the charter.** What is
missing is the BODY that issued it and the STATUTE that authorised it.

---

## 2. The covert-action lineage

### 2a. National Security Council — VERIFIED

- **Opened:** `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title50-section3021&num=0&edition=prelim`, the codified text of 50 U.S.C. 3021 with its source credit.
- Source credit: "July 26, 1947, ch. 343, title I, §101, 61 Stat. 496", amended from "Aug. 10, 1949, ch. 412, §3, 63 Stat. 579".
- Purpose, verbatim and unchanged since 1947: "to advise the President with respect to the integration of domestic, foreign, and military policies relating to the national security".
- Original 1947 membership: President; Secretaries of State and Defense; Secretaries of the Army, Navy and Air Force; Chairman of the National Security Resources Board. **No Vice President and no DCI.**
- Today: subsection (c)(2) makes the DNI and the Chairman of the Joint Chiefs attendees the President MAY designate, not statutory members. Subsection (e)(3) caps professional staff at 200.

Proposed `national-security-council`, `cls: institution`, `cluster: ic`, dateStart 1947.

### 2b. National Security Act of 1947 — VERIFIED

- **Opened:** `https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf`, the Statutes at Large page images, ch. 343 read through Title III.
- Pub. L. 80-253, ch. 343, 61 Stat. 495. Sidenote "July 26,1947 [S. 758] [Public Law 253]". Closing line "Approved July 26, 1947."
- Sec. 101 creates the NSC. Sec. 102(a): "There is hereby established under the National Security Council a Central Intelligence Agency with a Director of Central Intelligence". Sec. 103 the National Security Resources Board. Sec. 201(a) the National Military Establishment. Secs. 205 to 208 the Departments of the Army, Navy and Air Force and the US Air Force. Sec. 211 the Joint Chiefs, Sec. 213 the Munitions Board.
- **Section 102(d)(5)**, the residual "such other functions and duties related to intelligence" clause, is the authority both NSC 10/2 and NSC 5412 invoke. That is the edge that makes this node earn its place.

Proposed `national-security-act-1947`, `cls: legislation`, `cluster: oversight`, dateStart 1947-07-26.

### 2c. NSC 5412 — VERIFIED

- **Opened:** `https://history.state.gov/historicaldocuments/frus1950-55Intel/d171`, full text plus enclosure and source footnotes. Found via the footnote on `.../d212` (NSC 5412/1).
- FRUS heading "171. Note From the Executive Secretary of the National Security Council (Lay) to the National Security Council"; document line "NSC 5412", subject "COVERT OPERATIONS"; enclosure headed "NATIONAL SECURITY COUNCIL DIRECTIVE ON COVERT OPERATIONS". Washington, 15 March 1954. Top Secret. Eisenhower Library.
- Transmittal signed "James S. Lay, Jr."; the text states "The President has this date approved the enclosed National Security Council directive."
- Para. 4 invokes section 102(d)(5) and makes the DCI responsible for keeping covert operations consistent with US foreign and military policy through designated representatives of the Secretaries of State and Defense.
- Para. 7 supersedes and rescinds **NSC 10/2 and NSC 10/5**; para. 7(c) makes the Operations Coordinating Board the normal channel for coordination among State, Defense and CIA.
- Para. 6 carries the same deniability formula as NSC 10/2: "any U.S. Government responsibility for them is not evident to unauthorized persons and that if uncovered the U.S. Government can plausibly disclaim any responsibility."

Proposed `nsc-5412`, `cls: document`, `cluster: ic`, dateStart 1954-03-15. **Its edge to
`cia-office-of-policy-coordination` is a supersession edge**, which the board can show and
currently cannot.

### 2d. NSAM 303 — VERIFIED, and it is a CORRECTION rather than an addition

**The handoff lists NSAM 303 in the EO/statute spine. On the primary document that is
wrong, and the finding is worth more than the node would have been.**

- **Opened:** `https://history.state.gov/historicaldocuments/frus1964-68v33/d204`, FRUS 1964-1968 Vol. XXXIII Doc. 204, read in full. The memo is two numbered sentences.
- Subject "Change in Name of Special Group 5412". Washington, **2 June 1964**. Signed **McGeorge Bundy**, not the President. To the Secretaries of State and Defense and the DCI. Top Secret. NARA, RG 59, S/S-NSC Files: Lot 70 D 265.
- Verbatim: "Henceforth, the Special Group 5412 will be known as the 303 Committee." and "This change in no way alters the composition, function or responsibility of the Special Group 5412 as authorized by NSC 5412/2".
- **It contains no classification rules, no declassification rules and no secrecy policy of any kind.** It is an administrative renaming.
- Catalogue entries seen but NOT counted as document text: `https://irp.fas.org/offdocs/nsam-lbj/index.html`, and `https://www.discoverlbj.org/item/nsf-nsam303`, which served only a page shell.
- No connection of any kind between NSAM 303 and UAP records was found, and none is in the text.

Proposed: build at Tier C, precisely as a documented case of a citation that does not say
what it is cited for. Same shape as the Library of Congress cataloguing Fouche as science
fiction, and this board is better for carrying it.

### 2e. NSDD 159 — VERIFIED, and it is the most valuable document in this pass

- **Opened:** `https://www.reaganlibrary.gov/public/archives/reference/scanned-nsdds/nsdd159.pdf` (4.5 MB, 7 pages), read as both OCR text and page images. Also `https://irp.fas.org/offdocs/nsdd/nsdd-159.htm`, which is **only a table of seven GIF page scans with no text**, plus the scans themselves.
- "National Security Decision Directive Number 159 / COVERT ACTION POLICY APPROVAL AND COORDINATION PROCEDURES", The White House, **18 January 1985**, marked SENSITIVE, SYSTEM II: 90030, NSC/ICS-400030, Copy 1 of 8. **Signed in ink by Reagan on page 7.**
- Originally TOP SECRET, and the struck-through control line reads **TOP SECRET/VEIL**. Original instruction "Declassify on: Presidential Approval Only". The Reagan Library copy is stamped "Authority Leary to Weinstein ltr 4/20/05 / BY RW NARA DATE 1/30/12".
- **The two releases are not the same document and the difference matters.** The FAS copy is stamped "EXTRACT FROM NSDD 159", partially declassified 5 June 1987 under EO 12356. The Reagan Library copy is the fuller 2012 release. **Cite the Reagan Library version.**
- Directs written Presidential Findings for all covert action, Memoranda of Notification for modifications, the NSPG as the recommending committee, and a new Planning and Coordination Group that "replaces all ad hoc interagency groups". The NSC Senior Director for Intelligence Programs holds the only record copies: "No other copies of approved Findings or MONs are authorized."
- **THE COMPARTMENTED CHANNEL, explicit.** Security Procedures ¶1 directs the APNSA to "establish a separate, specially compartmented control and access system at the Top Secret classification level for all policy matters concerning covert action." ¶2: "Each NSPG member shall designate one senior member of his component as the sole focal point for all matters related to covert action." Page 2 states the design goal that knowledge of policy, of operations, and of supporting activity "will be strictly compartmented from each other." ¶3 orders the minimum possible number of documents created.
- **Gap:** the compartment's own implementing rules are "to be promulgated under separate cover" and that document is not in this release and was not located. Also, VEIL appears only as a struck-through marking and never in the body, so it cannot be said from this text that VEIL is the compartment NSDD 159 creates rather than a pre-existing caveat on the paper.

Proposed `nsdd-159`, `cls: document`, `cluster: ic`, dateStart 1985-01-18, and it should
carry edges to `d-sap`, `sapoc` and `cia`. This is a 1985 presidential directive ordering a
separate compartmented access system for an entire policy subject, with one designated
person per agency. That is the architecture this board spends most of its time describing,
forty years earlier than the board currently shows it.

---

## 3. The classification lineage

### 3a. EO 10501 — VERIFIED via a mirror, not the Federal Register

- **Opened:** `https://irp.fas.org/offdocs/eo10501.htm`, full transcribed text, sections 1 to 20 plus the attached agency memorandum. It is a transcription with obvious typos, not an FR scan.
- **`https://www.federalregister.gov/executive-order/10501` FAILED**: it redirects to `https://unblock.federalregister.gov/`, a bot-block page. The "18 FR 7049" citation is therefore UNCONFIRMED and must not be written as if it were read.
- "SAFEGUARDING OFFICIAL INFORMATION IN THE INTERESTS OF THE DEFENSE OF THE UNITED STATES." Eisenhower, 5 November 1953, effective 15 December 1953 (Sec. 20).
- Sec. 19: "Executive Order No. 10290 of September 24, 1951 is revoked as of the effective date of this order."
- Sec. 1 fixes three categories and bars any other designation "except as expressly provided by statute."
- Sec. 2, "Limitation of Authority to Classify", strips original classification authority from agencies with no direct national-defense responsibility, and limits others to the agency head without delegation: "there shall be no authority for original classification of information or material under this order." The attached memorandum names **28 agencies stripped** (FTC, SEC, Veterans Administration among them) and **17 limited to the agency head**.
- **Sec. 13 expressly leaves Atomic Energy Act Restricted Data outside the order's reach.** That is the join between the two lineages and is the reason to build both together.

### 3b. EO 11652 — VERIFIED

- **Opened:** `https://irp.fas.org/offdocs/eo/eo-11652.htm`, all 15 sections through the signature block. A transcription with visible OCR errors. Corroborated at `https://www.archives.gov/federal-register/executive-orders/1972.html`: "Signed: March 8, 1972 / 37 FR 5209; March 10, 1972 / Revokes: EO 10501".
- "Classification and Declassification of National Security Information and Material". Nixon, 8 March 1972, effective 1 June 1972.
- Sec. 14 **supersedes** EO 10501 as amended by EOs 10816, 10901, 10964, 10985, 11097 and sec. 1(a) of 11382. The operative word is supersedes, not revokes.
- Sec. 5(A) creates the **General Declassification Schedule**: Top Secret to Secret at 2 full calendar years, to Confidential at 4, declassified at 10; Secret to Confidential at 2, declassified at 8; Confidential at 6.
- Sec. 5(E)(1) is a **thirty-year rule**: automatic declassification at 30 years unless the head of the originating Department personally determines in writing that continued protection is essential.
- Sec. 7(A) creates the **Interagency Classification Review Committee** under the NSC, with State, Defense, Justice, the AEC, CIA and the NSC Staff, which under 7(A)(2) takes complaints "from persons within or without the government".
- Sec. 1(A) on Top Secret: "This classification shall be used with the utmost restraint."

### 3c. EO 12036 — VERIFIED, and it is NOT what this board would want it for

- **Opened:** `https://irp.fas.org/offdocs/eo/eo-12036.htm` (69,125 bytes), full operative text. FAS transcription; the Federal Register original at 43 FR 3674 was not opened.
- Caption "UNITED STATES INTELLIGENCE ACTIVITIES" (the FAS page heading says "Foreign"; both appear). "JIMMY CARTER / The White House, / January 24, 1978", filed 11:19 a.m., 25 January 1978.
- Sec. 4-101 **supersedes** EO 11905 of 18 February 1976, plus EOs 11985 and 11994.
- Section 3 oversight: 3-1 Intelligence Oversight Board (three members, outside government, inside the White House); 3-2 Inspectors General and General Counsel; 3-3 the Attorney General; 3-4 the congressional intelligence committees, kept "fully and currently informed", expressly "not... a condition precedent".
- Sec. 1-302: "The SCC shall consider and submit to the President a policy recommendation, including all dissents, on each special activity." Special activities defined at 4-212 as activities abroad where the US role "is not apparent or acknowledged publicly."
- **The words "compartment", "special access" and "need-to-know" appear zero times.** Do not cite EO 12036 for compartmentation. Its value to this board is the special-activity approval chain, nothing more.

### 3d. EO 12356 — VERIFIED via the OFR codification

- **`https://irp.fas.org/offdocs/eo/eo-12356.htm` returned HTTP 404. It does not exist. Do not cite it.**
- **Opened:** `https://www.archives.gov/federal-register/codification/executive-order/12356.html`, the OFR codified operative text.
- "Executive Order 12356--National security information". Source line: "of Apr. 2, 1982, appear at 47 FR 14874 and 15557, 3 CFR, 1982 Comp., p. 166." Effective 1 August 1982. The codification carries **no signature block**, so Reagan's signature was not read.
- Sec. 6.2(d): "Executive Order No. 12065 of June 28, 1978, as amended, is revoked as of the effective date of this Order."
- Sec. 1.6(c) authorises officials to "reclassify information previously declassified and disclosed if it is determined in writing" that it needs protection and "may reasonably be recovered". Sec. 1.6(d) allows classification or reclassification AFTER a FOIA, Privacy Act or mandatory-review request, document by document.
- **The public-interest balancing test is gone, and this was checked from both sides.** "public interest" occurs 0 times in EO 12356 and "balanc" 0 times; `https://irp.fas.org/offdocs/eo/eo-12065.htm` was opened and its sec. 3-303 required an official to "determine whether the public interest in disclosure outweighs the damage to national security". Sec. 1.1(c) of 12356 also flips doubt toward secrecy: doubt about level means safeguard at the higher level.

### 3e. Atomic Energy Act of 1954 — VERIFIED

- **Opened:** `https://www.govinfo.gov/content/pkg/STATUTE-68/pdf/STATUTE-68-Pg919.pdf` (8.6 MB, secs. 11, 141-145, 221-227 read) and `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section2014&num=0&edition=prelim`. For the comparison, `https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf`. **nrc.gov returned HTTP 403** on its NUREG-0980 compilation.
- Header: "Public Law 703 / CHAPTER 1073 / August 30, 1954 / [H. R. 9757]", 68 Stat. 919. Long title "To amend the Atomic Energy Act of 1946, as amended, and for other purposes", so it is a complete restatement rather than a repeal. The page image carries no signature line.
- Definition at **42 U.S.C. 2014(y)**, source credit "(Aug. 1, 1946, ch. 724, title I, §11, as added Aug. 30, 1954, ch. 1073, §1, 68 Stat. 922...)". In the 1954 enrolled text it was **section 11 r.**
- Verbatim, 42 U.S.C. 2014(y): "The term 'Restricted Data' means all data concerning (1) design, manufacture, or utilization of atomic weapons; (2) the production of special nuclear material; or (3) the use of special nuclear material in the production of energy, but shall not include data declassified or removed from the Restricted Data category pursuant to section 2162 of this title."
- Verbatim, 1946 Act sec. 10(b)(1): "all data concerning the manufacture or utilization of atomic weapons, the production of fissionable material, or the use of fissionable material in the production of power".
- What changed, from the two texts side by side: 1946 defined the term only "as used in this section"; 1954 makes it a capitalised, Act-wide definition. 1954 **adds "design"**. "Fissionable material" and "production of power" become "special nuclear material" and "production of energy". The 1946 carve-out was open-ended Commission discretion; 1954 ties removal to a formal declassification procedure at sec. 142, including sec. 142 d. transclassification of weapons-utilisation data into "defense information".

---

## 4. The shape of the build

Three lineages, and almost every edge lands on a node that already exists. That is what
makes this the cheapest documented gap available.

| lineage | chain |
|---|---|
| **Classification** | EO 10501 (1953) to EO 11652 (1972) to EO 12356 (1982) to `eo-12829` (1993) to `eo-13526` (2009), domain `d-secrecy` |
| **Covert action** | `national-security-act-1947` sec. 102(d)(5) to NSC 10/2, already represented by `cia-office-of-policy-coordination`, to NSC 5412 (which supersedes it) to NSC 5412/2 to NSAM 303's renaming, to NSDD 159, with `national-security-council` as the issuing body throughout |
| **Nuclear** | `atomic-energy-act-1946` to the Atomic Energy Act of 1954, joined to `atomic-energy-commission`, `doe`, `d-nuclear` and `usc-50-2426`. **EO 10501 sec. 13 is the join to the classification lineage**, because it puts Restricted Data outside the executive classification system entirely |

Presidents are deliberately NOT proposed as nodes. Only `harry-s-truman` exists today, the
spine holds together without signatories, and adding six presidents would be scope creep
dressed as completeness.

---

## 5. SIX THINGS THAT ARE WIDELY REPEATED AND ARE WRONG ON THE PRIMARY TEXT

This is the part to read before writing any claim. Three of these are claims this board
would plausibly have written from secondary sources.

| claim | what the document says |
|---|---|
| **NSAM 303 is part of the secrecy spine** | It is a two-sentence renaming memo signed by Bundy. No classification content of any kind. Cite **NSC 5412/2** for the authority and NSAM 303 only for the name |
| **NSC 5412 created the 5412 Committee / Special Group** | Not in the text. FRUS's own editorial note at `https://history.state.gov/historicaldocuments/frus1964-68v12/actionsstatement` attributes the Special Group to **NSC 5412/2 of 28 December 1955** |
| **The Atomic Energy Act of 1954 makes nuclear information "born classified"** | The phrase appears **nowhere in the Act**. It is a term of art. The doctrine is an inference from the breadth of the sec. 11 r. definition plus the sec. 224 to 227 criminal provisions. Write it as the inference it is, not as statute |
| **EO 12356 revoked EO 11652** | It did not. EO 12065 sec. 6-203 had already revoked 11652 in 1978. EO 12356 revokes **12065** |
| **EO 12036 bears on compartmentation** | Zero occurrences of "compartment", "special access" or "need-to-know" |
| **The National Security Act of 1947 created the Department of Defense** | It created the **National Military Establishment**. The renaming came with the 1949 amendments, Aug. 10, 1949, ch. 412, 63 Stat. 579 |

And two things that could not be verified and must not be asserted:

- **Nobody has read a signature on the National Security Act of 1947.** The Statutes at Large prints only "Approved July 26, 1947" and names no President. Truman's signature is universally reported; it is Tier 2 until a primary signing document is opened. The same applies to the Atomic Energy Act of 1954 and to EO 12356, whose OFR codification carries no signature block.
- **The 18 FR 7049 citation for EO 10501** was not read, because federalregister.gov bot-blocks this environment.

## 6. Access notes for the next session

| host | result |
|---|---|
| `history.state.gov` (FRUS) | works, and is the best source for the NSC directives |
| `govinfo.gov` | works, including large Statutes at Large PDFs |
| `uscode.house.gov` | works |
| `archives.gov` | works, including the OFR codification and the EO disposition tables |
| `reaganlibrary.gov` | works, and its NSDD scans are fuller than the FAS extracts |
| `irp.fas.org` | works, but the pages are transcriptions with OCR errors, some are GIF-only, and `eo/eo-12356.htm` is a 404 |
| `federalregister.gov` | **BLOCKED**, redirects to an unblock page |
| `nrc.gov` | **403** |
| `discoverlbj.org` | served a page shell only |
