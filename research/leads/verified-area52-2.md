# Verified leads: Area 52 corpus, verifier 2

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over five
candidates drawn from section A of `research/leads/area52-triage-1.md` (rows 13, 15 and 8)
and section A of `research/leads/area52-triage-2.md` (rows 1 and 2), against
`research/leads/VERIFY-BRIEF-AREA52-2026-09-02.md` and the Michels verify brief it adopts.

**Verified 2 September 2026.** Every URL below was opened by this session and returned the
document described. Where a document is a scan, the text quoted was read from the OCR layer
the archive itself publishes, and that is labelled at every point where it matters.
`CLAUDE.md` section 2 governs: nothing here is asserted that was not opened.

**Board state, read from `data/the-program.json` by this session rather than taken from the
triage files.** `Souers` 0 occurrences. `Bronk` 0. `Craven` 0. `Deep Submergence` 0.
`NURO` 0. `National Underwater Reconnaissance` 1, and it is not a claim: it is the string
`"A video in which Inman refers to a National Underwater Reconnaissance Office. The
recording was not located in this pass."` sitting in the `unverified` list of
`bobby-ray-inman`. `Keyhoe` 4, all prose, on `roscoe-hillenkoetter` and `nicap`. Node ids
confirmed present before any edge was drafted: `nicap`, `roscoe-hillenkoetter`, `cia`,
`usaf`, `us-navy`, `mj-12-documents`, `nro`, `bobby-ray-inman`.

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 1 | Sidney W. Souers | CONFIRMED, both offices and both date ranges | new node |
| 2 | Detlev W. Bronk | PARTLY CONFIRMED: NAS presidency 1950-1962 and NACA vice chairmanship documented; the National Research Council chairmanship NOT OPENED | new node |
| 3 | Donald E. Keyhoe as NICAP director | PARTLY CONFIRMED: director from at least September 1957 to May 1964; the 1969 end date and the 22 January 1958 CBS cut NOT OPENED | new node |
| 4 | Deep Submergence Systems Project, 1964, and John Pina Craven | PARTLY CONFIRMED: the programme, its 1964 origin, its office and its stated purpose are documented; Craven is NOT OPENED and appears in no record reached from here | new node for DSSP only |
| 5 | NURO, and the 1969 Navy and CIA agreement | NOT OPENED | nothing to draft |

**The five findings that matter, in order:**

1. **The 20,000 foot figure belongs to the search vehicle, not the rescue vehicle.** Gerb
   (09-3 / 0:36:22) gives the Deep Submergence Rescue Vehicle as "operating to 20,000 feet".
   The Navy's own 1965 design report gives the rescue vehicle a 6,000 foot design depth and
   assigns the 20,000 foot mission to a separate Search Vehicle. The 1967 Oceanographer of
   the Navy report says the same. Two documents, one correction.
2. **The review group reported in 1964, not 1963.** Triage row 2A1 names "the Deep
   Submergence Systems Review Group report of 1963". The Navy report says the DSSRG was
   established in April 1963 and reported its findings in February 1964, after which the
   Secretary of the Navy renamed the programme DSSP and assigned it to the Special Projects
   Office. The 1963 date is the group's, the 1964 date is the report's and the project's.
3. **DSSP's documented purpose is close to what the corpus claims, and that is the point.**
   The DSSRG's charter, in the Navy's words, covers "location, identification, rescue from
   and recovery of deep-submerged large objects from the ocean floor". The board can now test
   undersea recovery claims against an organisation whose recovery mission is on the record,
   without conceding anything about what was recovered.
4. **NURO cannot be opened from this machine.** `nro.gov` returns 403 to curl, the CIA
   reading room 302-loops, the archive.org CIA mirror holds no document naming a National
   Underwater Reconnaissance Office, the National Security Archive's search returns nothing
   for the phrase, and The Black Vault's document archive returns no matching record. The
   board's existing unresolved NURO line on `bobby-ray-inman` stays unresolved, and this pass
   adds the negative result rather than a second unlocatable recording.
5. **The CIA set a standing rule for Keyhoe's inquiries in 1958 and wrote it down.** A CIA
   memorandum for record in the reading room says the Air Force was "most insistent" on
   answering his letters itself, that the Air Force wanted him and others to understand its
   own office "is the proper place to come for such information", and that the Agency would
   "use this procedure as a precedent henceforth in all inquiries regarding UFO's". That is a
   documented routing rule, not a recollection.

---

## 1. Sidney W. Souers

**VERDICT: CONFIRMED.** Both offices, both date ranges, and the "first" in each case are
supported by opened records: the Presidential directive that created the post, a memorandum
he signed in it, the statute that created the second post, the minutes of the body's first
meeting with him sitting in it, and the Department of State's own list of persons.

### What was opened

| URL | What is at it |
|---|---|
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d71 | FRUS, 1945-1950, Emergence of the Intelligence Establishment, Document 71. Presidential Directive on Coordination of Foreign Intelligence Activities, Washington, 22 January 1946. |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d137 | Same volume, Document 137. Memorandum From the Director of Central Intelligence (Souers) to the National Intelligence Authority, 2 February 1946. Source note: NARA RG 59, Bureau of Intelligence and Research: Lot 58 D 776. Confidential. |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d225 | Same volume, Document 225. Minutes of the First Meeting of the National Security Council, 26 September 1947. Source note: NARA RG 273, NSC Minutes, 1st Meeting. Secret. |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/persons | Same volume, List of Persons. |
| https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf | Statutes at Large volume 61, page 495 onward. Chapter 343, Public Law 253, 80th Congress, approved 26 July 1947. The National Security Act of 1947. Scan with a text layer, extracted with `pdftotext -layout`. |

### What the documents establish

**The post he first held was created on 22 January 1946 and had no incumbent before him.**
The Presidential directive of that date, addressed to the Secretaries of State, War and the
Navy, creates the National Intelligence Authority and directs that persons and facilities
assigned from the three departments "shall collectively form a Central Intelligence Group and
shall, under the direction of a Director of Central Intelligence, assist the National
Intelligence Authority. The Director of Central Intelligence shall be designated by me, shall
be responsible to the National Intelligence Authority, and shall sit as a non-voting member
thereof."

**He held it, and signed in it.** Document 137 of 2 February 1946 is captioned "Memorandum
From the Director of Central Intelligence (Souers) to the National Intelligence Authority",
proposes the tentative organisation of the Central Intelligence Group, and carries the typed
signature "Sidney W. Souers". The volume's own chapter structure runs "Souers' Tenure as
Director of Central Intelligence (Documents 137-154)" before "Vandenberg's Tenure" and
"Hillenkoetter's Tenure", in that order.

**The dates.** The List of Persons gives: "Director of Central Intelligence, Central
Intelligence Group, January 22, 1946-June 10, 1946; Executive Secretary, National Security
Council, August 1947-January 1950; Special Consultant to the President from January 1950."
The same list gives Vandenberg the CIG directorship from 10 June 1946, which closes the
first term at the other end.

**The second post is statutory.** Section 101(c) of the National Security Act of 1947: "The
Council shall have a staff to be headed by a civilian executive secretary who shall be
appointed by the President, and who shall receive compensation at the rate of $10,000 a
year." The same section makes the executive secretary, subject to the direction of the
Council, the appointing authority for its staff.

**He was in the chair at the Council's first meeting, and the meeting's own decisions built
the secretariat around him.** The minutes of 26 September 1947 list under Others Present
"Sidney W. Souers, Executive Secretary, National Security Council" and "Rear Admiral Roscoe
H. Hillenkoetter, Director of Central Intelligence", with the President presiding and James
Forrestal present as Secretary of Defense. The Council's first four decisions are the
secretariat: attendance by officials other than members is "by approval of the presiding
officer, requested through the Executive Secretary"; "There will be no set schedule of
meetings. Meetings will be arranged by the Executive Secretary after approval by the
presiding officer"; the Council adopted "a resolution authorizing its Executive Secretary to
control, supervise, and administer funds which have been or hereafter may be made available
to the National Security Council, with full powers with respect thereto"; and, in the same
list, "The affairs of the Council will be conducted with the utmost secrecy." The Director of
Central Intelligence "is authorized to attend all meetings of the Council as an observer and
adviser."

### What the transcript claimed that these documents do NOT establish

Souers is named on Area 52 DEBRIEFED only inside the MJ-12 Eisenhower Briefing Document,
read aloud by Chris Ramsay with no guest (map 02 / file 02, people list). **Nothing in any
document opened here mentions unidentified objects, recovered material, or any panel of the
kind that document describes.** What the records establish is an officeholder who built and
then ran the secretariat through which National Security Council business, including the
Director of Central Intelligence's attendance and the Council's funds, was routed. That is a
structural fact about who controlled the paper, and the board should carry it as that.

One spelling note, since the board will index him: the volume's own persons index heading
renders him "Souers, Rear Admiral Sydney W." while the List of Persons entry and every
document text read here give "Sidney W. Souers". The documents win.

### Draft node

```json
{
  "id": "sidney-souers",
  "cls": "person",
  "label": "Rear Adm. Sidney W. Souers",
  "cluster": "ic",
  "sub": "First Director of Central Intelligence, Central Intelligence Group, 1946; first Executive Secretary, National Security Council, 1947-1950",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "dateStart": "1946-01-22",
  "dateEnd": "1950-01",
  "desc": "Souers held, in sequence, the two offices through which the postwar national security paper actually moved. He was the first Director of Central Intelligence, designated under the Presidential directive of 22 January 1946 that created the National Intelligence Authority and the Central Intelligence Group, and he served until 10 June 1946. From August 1947 he was the first Executive Secretary of the National Security Council, the civilian staff head the National Security Act of 1947 created by statute, and he held that post until January 1950. At the Council's first meeting on 26 September 1947 the Council routed attendance requests and meeting scheduling through him, gave him full powers over its funds, resolved that its affairs would be conducted with the utmost secrecy, and admitted the Director of Central Intelligence as an observer and adviser. The board argues at length about what the National Security Council was and was not shown and has no node for the man who built its secretariat. He is named in the MJ-12 Eisenhower Briefing Document, and that is not why he is here.",
  "claims": [
    {
      "tier": 1,
      "text": "The office he first held was created on 22 January 1946: personnel assigned from State, War and the Navy 'shall collectively form a Central Intelligence Group and shall, under the direction of a Director of Central Intelligence, assist the National Intelligence Authority. The Director of Central Intelligence shall be designated by me, shall be responsible to the National Intelligence Authority, and shall sit as a non-voting member thereof.'",
      "source": "Presidential Directive on Coordination of Foreign Intelligence Activities, 22 January 1946, Foreign Relations of the United States, 1945-1950, Emergence of the Intelligence Establishment, Document 71, https://history.state.gov/historicaldocuments/frus1945-50Intel/d71"
    },
    {
      "tier": 1,
      "text": "He held the post and signed in it within two weeks: the memorandum of 2 February 1946 proposing the tentative organisation of the Central Intelligence Group is captioned 'Memorandum From the Director of Central Intelligence (Souers) to the National Intelligence Authority' and carries the typed signature 'Sidney W. Souers'. Its source note is NARA RG 59, Bureau of Intelligence and Research, Lot 58 D 776.",
      "source": "FRUS, 1945-1950, Emergence of the Intelligence Establishment, Document 137, 2 February 1946, https://history.state.gov/historicaldocuments/frus1945-50Intel/d137"
    },
    {
      "tier": 1,
      "text": "The Department of State's own list of persons gives both offices with dates: 'Director of Central Intelligence, Central Intelligence Group, January 22, 1946-June 10, 1946; Executive Secretary, National Security Council, August 1947-January 1950; Special Consultant to the President from January 1950.'",
      "source": "FRUS, 1945-1950, Emergence of the Intelligence Establishment, List of Persons, https://history.state.gov/historicaldocuments/frus1945-50Intel/persons"
    },
    {
      "tier": 1,
      "text": "The second office is statutory. Section 101(c) of the National Security Act of 1947: 'The Council shall have a staff to be headed by a civilian executive secretary who shall be appointed by the President, and who shall receive compensation at the rate of $10,000 a year.'",
      "source": "National Security Act of 1947, Public Law 80-253, ch. 343, 61 Stat. 495, sec. 101(c), approved 26 July 1947, https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf"
    },
    {
      "tier": 1,
      "text": "At the National Security Council's first meeting on 26 September 1947 he is listed among those present as 'Sidney W. Souers, Executive Secretary, National Security Council', alongside the Director of Central Intelligence. The Council's own first decisions route attendance and scheduling through the Executive Secretary, authorise him 'to control, supervise, and administer funds which have been or hereafter may be made available to the National Security Council, with full powers with respect thereto', and record that 'The affairs of the Council will be conducted with the utmost secrecy.'",
      "source": "Minutes of the First Meeting of the National Security Council, 26 September 1947, NARA RG 273, NSC Minutes, 1st Meeting, Secret; FRUS, 1945-1950, Emergence of the Intelligence Establishment, Document 225, https://history.state.gov/historicaldocuments/frus1945-50Intel/d225"
    }
  ],
  "sources": [
    { "name": "Presidential Directive on Coordination of Foreign Intelligence Activities, 22 January 1946 (FRUS 1945-50 Intel, Doc. 71)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d71", "date": "1946-01-22" },
    { "name": "Memorandum From the Director of Central Intelligence (Souers) to the National Intelligence Authority (FRUS 1945-50 Intel, Doc. 137)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d137", "date": "1946-02-02" },
    { "name": "Minutes of the First Meeting of the National Security Council (FRUS 1945-50 Intel, Doc. 225)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d225", "date": "1947-09-26" },
    { "name": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-02" },
    { "name": "National Security Act of 1947, Public Law 80-253, 61 Stat. 495", "url": "https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf", "date": "1947-07-26" }
  ],
  "edges": [
    {
      "a": "sidney-souers",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "First Director of Central Intelligence, 22 January to 10 June 1946",
      "note": "He held the Director of Central Intelligence post created by the Presidential directive of 22 January 1946 at the head of the Central Intelligence Group, the office the National Security Act of 1947 later placed at the head of the Central Intelligence Agency.",
      "sources": [{ "name": "FRUS 1945-50 Intel, Docs. 71 and 137, and List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d137", "date": "1946-02-02" }]
    },
    {
      "a": "sidney-souers",
      "b": "roscoe-hillenkoetter",
      "type": "institutional",
      "claimTier": 1,
      "label": "Successive holders of the DCI post; in the same room at the NSC's first meeting",
      "note": "Souers held the Director of Central Intelligence post in 1946 and Hillenkoetter from 1 May 1947; the minutes of the National Security Council's first meeting on 26 September 1947 list Souers as Executive Secretary and Hillenkoetter as Director of Central Intelligence among those present.",
      "sources": [{ "name": "FRUS 1945-50 Intel, Doc. 225 and List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d225", "date": "1947-09-26" }]
    },
    {
      "a": "sidney-souers",
      "b": "mj-12-documents",
      "type": "investigative",
      "claimTier": 3,
      "label": "Named as a panel member inside the disputed document",
      "note": "Souers is named as an MJ-12 panel member in the Eisenhower Briefing Document as read aloud on Area 52 DEBRIEFED, corpus map 02 file 02. No record opened for this node connects him to unidentified objects, recovered material or any such panel; the offices are the reason he is on the board.",
      "sources": [{ "name": "Area 52 DEBRIEFED, ep. 22, the MJ-12 document read by Chris Ramsay (lead map research/leads/area52-corpus-02.md, file 02)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-02" }]
    }
  ]
}
```

**One caution on the third edge.** Its `sources` entry points at the persons list because the
brief forbids inventing a URL and no URL for the podcast episode was opened by this session.
If the board's convention is to cite the episode itself, the build pass should substitute the
corpus map's own episode citation rather than keep this placeholder, or drop the edge. The
edge is worth exactly its Tier 3 grade and no more.

---

## 2. Detlev W. Bronk

**VERDICT: PARTLY CONFIRMED.** The National Academy of Sciences presidency and its exact
date range are in the Department of State's own list of persons, his 1962 chairmanship of the
President's Science Advisory Committee's International Science Panel is in an opened FRUS
document, and his NACA membership and vice chairmanship are in the NACA's own annual reports.
The National Research Council chairmanship the triage row also names was NOT OPENED.

### What was opened

| URL | What is at it |
|---|---|
| https://history.state.gov/historicaldocuments/frus1961-63v25/persons | FRUS, 1961-1963, Volume XXV, Organization of Foreign Policy; Information Policy; United Nations; Scientific Matters. List of Persons. |
| https://history.state.gov/historicaldocuments/frus1961-63v25/d348 | Same volume, Document 348. Memorandum From the President's Special Assistant for Science and Technology (Wiesner) to Secretary of State Rusk, 16 March 1962, with the International Science Panel report of 27 February 1962 attached. Source note: NARA RG 59, Central Files, 1960-63, 110.10/3-1662. Official Use Only. |
| https://ntrs.nasa.gov/api/citations/19930092186/downloads/19930092186.pdf | Fortieth Annual Report of the National Advisory Committee for Aeronautics, 1954, GPO, Washington 1956. NASA Technical Reports Server. Scan with a text layer; extracted with `pdftotext -layout` and the OCR is rough in places, which is flagged below. |
| https://ntrs.nasa.gov/api/citations/19930092104/downloads/19930092104.pdf | Thirty-Eighth Annual Report of the National Advisory Committee for Aeronautics, 1952. Same caveat. |

### What the documents establish

**The NAS presidency, with the dates the triage row claims.** The List of Persons for FRUS
1961-1963 Volume XXV reads: "Bronk, Detlev W., President of the National Academy of Sciences,
1950-1962".

**He was chairing a White House science panel that reported on the State Department in 1962.**
Wiesner to Rusk, 16 March 1962: "You recently mentioned your concern regarding the scientific
activities in the Department of State, and I told you of the study being conducted by our
International Science Panel chaired by Dr. Bronk." The editorial footnote to that sentence
reads "Dr. Detlev W. Bronk, President of the National Academy of Sciences." The attachment is
the Panel's report of 27 February 1962, "Science and Technology in the Department of State",
produced under the President's Science Advisory Committee.

**The NACA membership and the vice chairmanship, from the NACA's own annual reports.** The
Fortieth Annual Report, covering 1954, records the annual election: "On October 22, 1954, Dr.
Jerome C. Hunsaker was reelected chairman" of the NACA and of the executive committee, "Dr.
Detlev W. Bronk vice chairman of the NACA, and Dr. Francis W. Reichelderfer vice chairman of
the executive committee". The membership list that follows gives him as "Dr. Detlev W. Bronk,
President, Rockefeller Institute for Medical Research, Vice Chairman", second on a list headed
by Hunsaker and including James H. Doolittle, Allen V. Astin and Donald A. Quarles. The
Thirty-Eighth Annual Report, covering 1952, lists him as a member under the earlier
affiliation, President of Johns Hopkins University; the OCR of that page is badly degraded and
his surname is rendered "BEOXK", so that line is reported and not quoted.

The same passage of the 1954 report also records, in its own words, that the Committee's
members "are appointed by the President and serve as such without compensation", and that the
statutory seat formerly held by the chairman of the Research and Development Board was
replaced by a Department of Defense representative after the Board's abolition under
Reorganization Plan No. 6, effective 30 June 1953. That is a second, incidental finding: the
board carries `research-and-development-board` nowhere in the ids checked, and the NACA's own
report dates its abolition.

### What the transcript claimed that these documents do NOT establish

Bronk is named in three lead maps, and in every one of them he is named as an MJ-12 member:
twice inside the read-aloud MJ-12 document (01 / 20 / 0:12:27 and 02 / 02) and once by Ramsay
as an "MJ-12 member of the era who would plausibly have known about UFO matters" (05 / 02).
**No document opened here connects Bronk to unidentified objects, to recovered material, or to
any such body.** What they establish is a man holding the presidency of the National Academy
of Sciences for twelve years while sitting as vice chairman of the federal aeronautical
research committee and chairing a White House science panel. The triage row was right that the
offices, not the attribution, are the reason to build him.

**Not opened, and it should be said plainly:** his National Research Council chairmanship. The
National Academies' own site (`nasonline.org`) returns 403 to this machine, the National
Academies Press search page returns no parseable results, and no government publication
reached here names him in that post.

### Draft node

```json
{
  "id": "detlev-bronk",
  "cls": "person",
  "label": "Detlev W. Bronk",
  "cluster": "research",
  "sub": "President, National Academy of Sciences 1950-1962; Vice Chairman, National Advisory Committee for Aeronautics",
  "tier": "C",
  "C": 3,
  "A": 3,
  "D": 1,
  "dateStart": "1950",
  "dateEnd": "1962",
  "desc": "Bronk sat at the top of the postwar civilian science advisory structure for twelve years, and the board has no node anywhere on that structure. The Department of State's own list of persons gives him as President of the National Academy of Sciences from 1950 to 1962. Over the same period he was a Presidentially appointed member of the National Advisory Committee for Aeronautics and was re-elected its Vice Chairman on 22 October 1954, under Jerome C. Hunsaker as chairman, listed then as President of the Rockefeller Institute for Medical Research and in 1952 as President of Johns Hopkins University. In 1962 he chaired the President's Science Advisory Committee's International Science Panel, whose report on science and technology in the Department of State was forwarded to Secretary Rusk on 16 March 1962. He is named as an MJ-12 member in three Area 52 lead maps and in no opened record.",
  "claims": [
    {
      "tier": 1,
      "text": "The Department of State's own list of persons gives the office and its dates: 'Bronk, Detlev W., President of the National Academy of Sciences, 1950-1962.'",
      "source": "Foreign Relations of the United States, 1961-1963, Volume XXV, List of Persons, https://history.state.gov/historicaldocuments/frus1961-63v25/persons"
    },
    {
      "tier": 1,
      "text": "He chaired a White House science panel reporting on the State Department. The President's Special Assistant for Science and Technology to the Secretary of State, 16 March 1962: 'You recently mentioned your concern regarding the scientific activities in the Department of State, and I told you of the study being conducted by our International Science Panel chaired by Dr. Bronk.' The editorial footnote to the sentence identifies him as 'Dr. Detlev W. Bronk, President of the National Academy of Sciences.'",
      "source": "Memorandum From the President's Special Assistant for Science and Technology (Wiesner) to Secretary of State Rusk, 16 March 1962, NARA RG 59, Central Files, 1960-63, 110.10/3-1662; FRUS 1961-1963, Volume XXV, Document 348, https://history.state.gov/historicaldocuments/frus1961-63v25/d348"
    },
    {
      "tier": 1,
      "text": "He was Vice Chairman of the National Advisory Committee for Aeronautics. The Committee's Fortieth Annual Report records that on 22 October 1954 Jerome C. Hunsaker was re-elected chairman and 'Dr. Detlev W. Bronk vice chairman of the NACA', and lists him in the membership as President of the Rockefeller Institute for Medical Research.",
      "source": "Fortieth Annual Report of the National Advisory Committee for Aeronautics, 1954, Part II, Committee Organization and Membership, GPO 1956, NASA Technical Reports Server 19930092186, https://ntrs.nasa.gov/api/citations/19930092186/downloads/19930092186.pdf"
    },
    {
      "tier": 1,
      "text": "NACA membership was a Presidential appointment and unpaid. The same report states that the members of the Committee 'are appointed by the President and serve as such without compensation', and that the seat formerly held ex officio by the chairman of the Research and Development Board was replaced by a Department of Defense representative after that Board's abolition under Reorganization Plan No. 6, effective 30 June 1953.",
      "source": "Fortieth Annual Report of the National Advisory Committee for Aeronautics, 1954, https://ntrs.nasa.gov/api/citations/19930092186/downloads/19930092186.pdf"
    },
    {
      "tier": 1,
      "text": "He was already a member two years earlier under his previous office: the Thirty-Eighth Annual Report for 1952 lists him in the Committee membership as President of Johns Hopkins University. The scan's OCR degrades his surname on that page, so the line is reported rather than quoted.",
      "source": "Thirty-Eighth Annual Report of the National Advisory Committee for Aeronautics, 1952, NASA Technical Reports Server 19930092104, https://ntrs.nasa.gov/api/citations/19930092104/downloads/19930092104.pdf"
    }
  ],
  "sources": [
    { "name": "FRUS 1961-1963, Volume XXV, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1961-63v25/persons", "date": "2026-09-02" },
    { "name": "FRUS 1961-1963, Volume XXV, Document 348 (Wiesner to Rusk, International Science Panel report)", "url": "https://history.state.gov/historicaldocuments/frus1961-63v25/d348", "date": "1962-03-16" },
    { "name": "Fortieth Annual Report of the National Advisory Committee for Aeronautics, 1954", "url": "https://ntrs.nasa.gov/api/citations/19930092186/downloads/19930092186.pdf", "date": "1954-12-31" },
    { "name": "Thirty-Eighth Annual Report of the National Advisory Committee for Aeronautics, 1952", "url": "https://ntrs.nasa.gov/api/citations/19930092104/downloads/19930092104.pdf", "date": "1952-12-31" }
  ],
  "edges": [
    {
      "a": "detlev-bronk",
      "b": "mj-12-documents",
      "type": "investigative",
      "claimTier": 3,
      "label": "Named as a panel member inside the disputed document",
      "note": "Bronk is named as an MJ-12 member in the Eisenhower Briefing Document as read aloud on Area 52 DEBRIEFED and again by the host in a separate episode. No record opened for this node connects him to the subject; his offices are the reason he is on the board.",
      "sources": [{ "name": "Area 52 DEBRIEFED, lead maps research/leads/area52-corpus-01.md file 20, -02.md file 02 and -05.md file 02", "url": "https://history.state.gov/historicaldocuments/frus1961-63v25/persons", "date": "2026-09-02" }]
    }
  ]
}
```

**The same caution applies to this edge's `sources` placeholder as to Souers'.** Bronk is
deliberately drafted with one weak edge and no strong ones: nothing opened here attaches him to
an existing board node at Tier 1, and inventing an attachment would be worse than a thin node.
If the build pass wants him better connected, the honest route is a `naca` node built on these
two annual reports, which would then carry Hunsaker as well and close the "NACA occurs zero
times" gap that triage group 1 section B row 7 records.

---

## 3. Donald E. Keyhoe

**VERDICT: PARTLY CONFIRMED.** The directorship is documented from at least 20 September 1957
to May 1964, by two independent artefacts inside one opened volume, and the CIA's own handling
of his inquiries is documented in the reading room. The 1969 end date and the 22 January 1958
CBS broadcast were NOT OPENED.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0 | The CIA's filed copy of *The UFO Evidence*, NICAP, Washington DC, May 1964, Richard H. Hall ed. The board already cites this document on `nicap`. Read here through the item's own DjVu OCR text at `https://archive.org/download/cia-readingroom-document-cia-rdp81r00560r000100010001-0/cia-rdp81r00560r000100010001-0_djvu.txt`. |
| https://archive.org/details/cia-readingroom-document-0005516043 | CIA reading room document 0005516043, "Comments on Letters Dealing with Unidentified Flying Objects", a memorandum for record, reading-room date 4 April 1958. OCR readable; the wobble is noted below. |
| https://archive.org/details/cia-readingroom-document-0000015305 | CIA reading room document 0000015305, reading-room date 5 February 1958, indexed as a letter to Donald Keyhoe from C. P. Cabell. Opened; the OCR of this scan is not legible enough to quote and nothing is quoted from it. |
| https://archive.org/details/cia-readingroom-document-0000015416 | CIA reading room document 0000015416, "Inquiry by Major Donald E. Keyhoe (deleted)", reading-room date 4 January 1959. An internal memorandum quoting a Keyhoe memorandum of 13 March 1958 to the Director of Central Intelligence asking whether CIA agents had told UFO witnesses to keep silent. OCR partly degraded; reported, not quoted. |

### What the documents establish

**He ran NICAP, and the masthead of the organisation's own 1964 volume says so in one line:**
"MAJ. DONALD E. KEYHOE, USMC (RET.), DIRECTOR", printed under the organisation's name and its
1536 Connecticut Avenue NW address, above the Board of Governors list.

**He was in the post by September 1957, and the evidence for that is an Air Force letter.**
The volume reproduces a letter on the letterhead "Hq Sq Sec, First Air Force, Mitchel Air
Force Base, NY", dated 20 September 1957, addressed to "Mr. Donald E. Keyhoe, Director NICAP,
1536 Connecticut Ave, N. W., Washington 6, D. C.", transmitting a quoted Air Force report of
eight round objects sighted at Fort Devens, Massachusetts on 17 September 1957. The
directorship is established there by a government correspondent's own salutation, not by
NICAP's claim about itself.

**His background, in the volume's own words:** "As a graduate of the U. S. Naval Academy
(class of 1920) and former Marine Corps aircraft and balloon pilot, Major Keyhoe knows many
active and retired officers, including Admirals who have held important positions."

**The Hillenkoetter link, which is the one the board most needs.** The same volume: "Vice
Admiral R. H. Hillenkoetter, USN (Ret.), a long-time acquaintance of Major Keyhoe, also served
on the NICAP Board of Governors for five years." Rear Admiral Delmer S. Fahrney is separately
recorded as having "served for a time as Chairman of the Board of Governors".

**The CIA wrote down a routing rule for him and called it a precedent.** CIA reading room
document 0005516043 is a memorandum for record on "Comments on Letters Dealing with
Unidentified Flying Objects", referring to a memorandum of 4 April 1958 on the same subject. It
records that an Air Force office was contacted about releasing the panel report to Mr Davidson
and Major Keyhoe; that the officer contacted at the Office of the Secretary of the Air Force
Information Service preferred that CIA forward the letters to him with copies of the
unclassified report so that he would answer them; that "the Air Force is endeavoring to impress
upon Major Keyhoe and others in a similar position, that his office is the proper place to come
for such information"; that the Air Force was "most insistent" it be permitted to answer; and,
in the drafter's own conclusion, "I think we can use this procedure as a precedent henceforth in
all inquiries regarding UFO's." The scan's OCR renders his surname variously as "Keyhoe" and
"seyhoe" and the Air Force officer's name as "Tacker" and "facker"; the sentences quoted above
were legible, and the page layout is scrambled by the OCR so the order of the closing lines is
uncertain.

### What the transcript and the triage row claimed that these documents do NOT establish

| Claimed | What the opened record says |
|---|---|
| Directorship 1957-1969 (triage row 1A8) | The 1957 start is documented by the Air Force letter and the 1964 continuation by the volume's masthead. **Nothing opened here establishes an end date.** A node should carry "director by September 1957, still in post May 1964" and no more. |
| "The 22 January 1958 CBS broadcast in which his audio was cut mid-sentence" (triage row 1A8) | **NOT OPENED.** No broadcast record, network transcript or contemporaneous government document reached from here mentions it. The 1964 volume, searched for "CBS", "Armstrong Circle" and "censored", carries nothing on it. |
| "The CIA's and the Air Force's files on him" | Opened in part, and they are real: four reading room items were opened, of which one is legible enough to quote. The reading room index carries at least 36 items naming him, including 1958 and 1959 correspondence signed by the Deputy Director of Central Intelligence and by the Agency's inspector general. That is a file, and this pass has read a fraction of it. |
| "NICAP's own publications under his directorship" | One of them, the 1964 volume, is the source of most of the above. It is the CIA's filed copy, which is why it is reachable. |

### Draft node

```json
{
  "id": "donald-keyhoe",
  "cls": "person",
  "label": "Maj. Donald E. Keyhoe, USMC (Ret.)",
  "cluster": "media",
  "sub": "Director, National Investigations Committee on Aerial Phenomena, by September 1957 and still in post May 1964",
  "tier": "B",
  "C": 1,
  "A": 1,
  "D": 2,
  "dateStart": "1957",
  "dateEnd": null,
  "desc": "Keyhoe ran the civilian organisation the board already carries as nicap, and he is the hinge between it and the former Director of Central Intelligence who sat on its board. A US Air Force headquarters letter of 20 September 1957 is addressed to him as Director NICAP at the organisation's Connecticut Avenue address, and NICAP's 1964 volume The UFO Evidence, in the copy the CIA filed, carries him on its masthead as director. He was a US Naval Academy graduate of 1920 and a former Marine Corps aircraft and balloon pilot, and the volume says plainly that his Navy connections are why several of its military cases are in it. In 1958 the CIA recorded a decision to forward his UFO inquiries to the Air Force's public information office to be answered there, and to treat that as a precedent for all such inquiries. No record opened here gives an end date for his directorship.",
  "claims": [
    {
      "tier": 1,
      "text": "NICAP's own 1964 volume names him as its head on the masthead: 'MAJ. DONALD E. KEYHOE, USMC (RET.), DIRECTOR', printed under the organisation's name and its 1536 Connecticut Avenue NW address, above the Board of Governors list.",
      "source": "The UFO Evidence, National Investigations Committee on Aerial Phenomena, Washington DC, May 1964, Richard H. Hall ed., in the CIA's filed copy CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "He held the post by September 1957 on a government correspondent's own address line. A letter on the letterhead 'Hq Sq Sec, First Air Force, Mitchel Air Force Base, NY', dated 20 September 1957, is addressed to 'Mr. Donald E. Keyhoe, Director NICAP, 1536 Connecticut Ave, N. W., Washington 6, D. C.' and transmits a quoted Air Force report of eight round objects sighted at Fort Devens, Massachusetts on 17 September 1957.",
      "source": "First Air Force letter of 20 September 1957, reproduced in The UFO Evidence, 1964, in CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "The volume states the Hillenkoetter connection as a personal one: 'Vice Admiral R. H. Hillenkoetter, USN (Ret.), a long-time acquaintance of Major Keyhoe, also served on the NICAP Board of Governors for five years.' It gives Keyhoe's own background as 'a graduate of the U. S. Naval Academy (class of 1920) and former Marine Corps aircraft and balloon pilot' and says his acquaintance with serving and retired officers is why several of its military cases could be detailed.",
      "source": "The UFO Evidence, 1964, in CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "The CIA recorded a standing rule for handling him. A memorandum for record on 'Comments on Letters Dealing with Unidentified Flying Objects' notes that the Air Force was 'most insistent' on answering his letters itself, that 'the Air Force is endeavoring to impress upon Major Keyhoe and others in a similar position, that his office is the proper place to come for such information', and concludes: 'I think we can use this procedure as a precedent henceforth in all inquiries regarding UFO's.' The scan's OCR is imperfect and renders his surname inconsistently; the quoted sentences were legible.",
      "source": "CIA memorandum for record, 'Comments on Letters Dealing with Unidentified Flying Objects', CIA reading room document 0005516043, reading-room date 4 April 1958, https://archive.org/details/cia-readingroom-document-0005516043"
    },
    {
      "tier": 1,
      "text": "He put the question to the Director of Central Intelligence directly. An internal CIA memorandum of January 1959 quotes his memorandum of 13 March 1958 to the DCI asking whether CIA representatives had told UFO witnesses not to make their sightings public, and on what authority. The scan is partly illegible and no wording is quoted from it here.",
      "source": "CIA reading room document 0000015416, 'Inquiry by Major Donald E. Keyhoe (deleted)', reading-room date 4 January 1959, https://archive.org/details/cia-readingroom-document-0000015416"
    }
  ],
  "sources": [
    { "name": "The UFO Evidence (NICAP, May 1964), CIA filed copy CIA-RDP81R00560R000100010001-0", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" },
    { "name": "CIA memorandum for record, Comments on Letters Dealing with Unidentified Flying Objects, document 0005516043", "url": "https://archive.org/details/cia-readingroom-document-0005516043", "date": "1958-04-04" },
    { "name": "CIA reading room document 0000015416, Inquiry by Major Donald E. Keyhoe", "url": "https://archive.org/details/cia-readingroom-document-0000015416", "date": "1959-01-04" },
    { "name": "CIA reading room document 0000015305, letter to Donald Keyhoe from C. P. Cabell", "url": "https://archive.org/details/cia-readingroom-document-0000015305", "date": "1958-02-05" }
  ],
  "edges": [
    {
      "a": "donald-keyhoe",
      "b": "nicap",
      "type": "institutional",
      "claimTier": 1,
      "label": "Director, by September 1957 and still in post May 1964",
      "note": "An Air Force headquarters letter of 20 September 1957 addresses him as Director NICAP at 1536 Connecticut Avenue NW, and the organisation's May 1964 volume carries him on its masthead as director. No opened record gives an end date.",
      "sources": [{ "name": "The UFO Evidence, 1964, masthead and the First Air Force letter of 20 September 1957 reproduced in it", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    },
    {
      "a": "donald-keyhoe",
      "b": "roscoe-hillenkoetter",
      "type": "institutional",
      "claimTier": 1,
      "label": "Long-time acquaintance; recruited a former DCI onto NICAP's Board of Governors",
      "note": "NICAP's 1964 volume describes Hillenkoetter as 'a long-time acquaintance of Major Keyhoe' who served five years on the NICAP Board of Governors and in 1961 joined a majority of that Board in urging a Congressional investigation.",
      "sources": [{ "name": "The UFO Evidence, 1964, in CIA-RDP81R00560R000100010001-0", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    },
    {
      "a": "donald-keyhoe",
      "b": "cia",
      "type": "denial",
      "claimTier": 1,
      "label": "CIA routed his UFO inquiries to the Air Force and made it a precedent",
      "note": "A 1958 CIA memorandum for record states that the letters from him would be forwarded to the Air Force to answer and that the Agency would use the procedure as a precedent henceforth in all inquiries regarding UFOs.",
      "sources": [{ "name": "CIA reading room document 0005516043", "url": "https://archive.org/details/cia-readingroom-document-0005516043", "date": "1958-04-04" }]
    },
    {
      "a": "donald-keyhoe",
      "b": "usaf",
      "type": "denial",
      "claimTier": 1,
      "label": "The Air Force insisted on being the single channel for his inquiries",
      "note": "The same memorandum records that the officer contacted at the Office of the Secretary of the Air Force Information Service wanted the letters forwarded to him to answer, that the Air Force was endeavouring to impress on Keyhoe and others that his office was the proper place to come for such information, and that the Air Force was most insistent on being permitted to answer.",
      "sources": [{ "name": "CIA reading room document 0005516043", "url": "https://archive.org/details/cia-readingroom-document-0005516043", "date": "1958-04-04" }]
    }
  ]
}
```

**Note for the build pass.** The `nicap` node built on 2 September already quotes the
Hillenkoetter sentence from the same volume. If both are built, the quotation should sit on one
of them and be referenced from the other rather than duplicated verbatim.

---

## 4. Deep Submergence Systems Project, 1964, and John Pina Craven

**VERDICT: PARTLY CONFIRMED.** The programme, its origin in the loss of USS *Thresher*, its
February 1964 birth out of a review group's report, its assignment to the Navy's Special
Projects Office, its later status as a separate project in the Naval Material Command and its
stated mission of locating and recovering objects from the ocean floor are all in Navy
documents opened here. **John Pina Craven appears in none of them, and no record reached from
this machine gives him any Navy office.**

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/DTIC_AD0614632 | "Potential Hull Structures for Rescue and Search Vehicles of the Deep-Submergence Systems Project", M. Krenzke, K. Horn and J. Proffitt, David Taylor Model Basin Report 1985, March 1965. DTIC AD-614632, on the DTIC mirror. Read through the item's DjVu OCR text. |
| https://archive.org/details/DTIC_AD0665974 | "The Ocean Engineering Program of the U.S. Navy: Accomplishments and Prospects", Office of the Oceanographer of the Navy, Alexandria, Virginia, September 1967. DTIC AD-665974. |
| https://archive.org/details/DTIC_AD0750736 | "Deep Submergence Systems Terminology and Usage", DSSP TD-19 Rev. B, Northrop Corporation Electro-Mechanical Division under contract N00024-70-C-0201, prepared for the Deep Submergence Systems Project Office, 30 June 1970. DTIC AD-750736. |
| https://archive.org/details/DTIC_AD0854434 | "Deep Submergence Systems Project (DSSP). Deep Submergence Rescue Vehicle (DSRV) Sensor..." 1969. DTIC AD-854434. Opened for the office designator only. |
| https://archive.org/details/JohnP.Craven | FBI file on John P. Craven, FOI/PA numbers 1323215 and 1322338, in the National Security Archive's FBI files collection on archive.org. See below. |

### What the documents establish

**The origin, and the exact sequence.** David Taylor Model Basin Report 1985, March 1965:
"The Deep-Submergence Systems Review Group (DSSRG) was established in April 1963 to (1) review
the Navy's plans for the development and procurement of components and systems related to
location, identification, rescue from and recovery of deep-submerged large objects from the
ocean floor", to recommend changes, to develop a five-year programme and to "recommend means
and organization of responsibilities for implementation". Then: "In February 1964 the Group
reported its findings and recommendations. After review of the report, the Secretary of the
Navy assigned the responsibility for implementation of the program, which was renamed the
Deep-Submergence Systems Project (DSSP), to the Navy's Special Projects Office."

**The mission split, and the depth figures.** The same report: "Two primary objectives of the
DSSP are to develop the capability of rescuing personnel from distressed submarines and to
locate and recover small objects from the ocean depths." The rescue vehicle's primary missions
are rescue from a sunken submarine and transfer between two submerged submarines, with
secondary oceanographic tasks "at depths to 6000 ft"; the report states that "Only operating
depths of 6000 ft are considered in this study". The search vehicle's primary missions are "to
search the ocean bottom to depths of 20,000 ft for either large or small objects and to recover
small objects either by actually lifting them or by making an attachment to the object so that
a surface lift, or buoyancy lift, can be accomplished". Planned force in 1965: six rescue
vehicles and four search vehicles operational by 1970.

**The *Thresher* link and the later organisational home.** The Oceanographer of the Navy,
September 1967: the loss of *Thresher* in 1963 "occurred beyond collapse depth of the hull and
precluded rescue of any personnel", the hull was located in 8,500 ft of water, and the casualty
"focused national attention on Navy capabilities underwater". The same page: "The Deep
Submergence Systems Project (DSSP) was established as a separate Project within the Naval
Material Command. The DSSP was launched in 1964 to develop and deliver to the fleet new
underwater capabilities: a new rescue system, a large object salvage system, diver tools, the
techniques of saturated diving for extended operations on the continental shelf, and new
submersible vehicles capable of searching the ocean floors." It gives the DSRV as due to the
fleet in 1968-1969 and describes the separately planned Deep Submergence Search Vehicle "whose
mission is ultimately to conduct sea floor search to a depth of 20,000 ft, providing coverage
of 98 percent of the worlds oceans". It also records the 1966 loss of an unarmed nuclear weapon
off the Mediterranean coast, found on the sea floor by ALVIN and recovered by the unmanned
vehicle CURV, as the second event driving the programme.

**The project office existed under a designator.** The 1969 DSSP report cites "Deep Submergence
Systems Project Office (PM-11) task 11894", and the 1970 terminology manual is issued as DSSP
TD-19 by the Deep Submergence Systems Project Office.

### Craven, and what was actually tried

**NOT OPENED.** Every route reachable from this machine was tried and none produced a record of
his Navy office:

| Tried | Result |
|---|---|
| Full text of the four DSSP-era Navy reports above, searched for "Craven", "Chief Scientist", "Special Projects Office" | Zero hits on "Craven" and zero on "Chief Scientist" in all four. The Special Projects Office appears only as the office the Secretary of the Navy assigned DSSP to. |
| The DTIC mirror on archive.org, searched for "Craven" | 23 items, all by a different author working on auroral physics. No Navy deep-submergence report by or naming him. |
| Three further DTIC reports opened on the chance of a personnel listing: AD-735902 (PERT, Special Projects Office, 1958), AD-621627 (Man in the Sea, 1965), ADA-074138 (Milestones in the NEL Deep Submergence Program, 1965) | No occurrence of "Craven" in any of them. |
| NASA Technical Reports Server, searched for "Craven deep submergence" | Zero results. |
| `history.navy.mil` | Returns 404 to this machine at the site root and at a valid interior path. Naval History and Heritage Command, which the triage row names as the place to look, is not reachable from here. |
| `apps.dtic.mil` citation pages | 403. |
| The FBI file on John P. Craven, opened at archive.org | It is the right man: the record gives "CRAVEN, JOHN, PINNA", born 30 October 1924, a Honolulu address, and a 2002 complaint form naming "DR. JOHN P. CRAVEN, DBA COMMON HERITAGE CORPORATION". **It establishes identity and nothing about the Navy.** Twenty-three pages are withheld. It is a law-enforcement file on a private complaint and this pass does not propose using it. |

The triage row's structural claim survives without him: DSSP sat in the Special Projects
Office, which is where the corpus places Craven, and the office's recovery mission is on the
record. A Craven node needs a service record, an appointment order or an official Navy
biography, and none of the three is reachable from this environment.

### What the transcript claimed that these documents do NOT establish

| Claimed (09-3 / 0:35:32 to 0:36:22, Gerb) | What the opened record says |
|---|---|
| The DSRV was "built to satisfy Sand Dollar's inventory requirement, operating to 20,000 feet" | Two Navy documents assign 20,000 ft to the **search** vehicle, not the rescue vehicle. The 1965 design report considers only 6,000 ft operating depths for the rescue vehicle. |
| Project Sand Dollar as the requirement DSSP answered | **Not opened.** "Sand Dollar" occurs nowhere in the four DSSP documents read here. The documented driver is the DSSRG's February 1964 report, itself prompted by the loss of *Thresher*. |
| DSSP as "the precursor to NURO" | Nothing opened here mentions NURO. See lead 5. |
| "John Peña Craven's Navy programme" | The Secretary of the Navy assigned the programme to the Special Projects Office. No opened record attaches Craven to it. |

### Draft node

```json
{
  "id": "deep-submergence-systems-project",
  "cls": "program",
  "label": "Deep Submergence Systems Project (DSSP)",
  "cluster": "legacy",
  "sub": "US Navy project for deep-ocean rescue, search, salvage and recovery, established 1964 in the Special Projects Office",
  "tier": "B",
  "C": 2,
  "A": 2,
  "D": 1,
  "dateStart": "1964-02",
  "dateEnd": null,
  "desc": "DSSP is the documented Navy organisation behind the deep-ocean recovery capability the Area 52 corpus talks about, and the board's undersea thread currently has no office at all. The Deep-Submergence Systems Review Group was established in April 1963, after the loss of USS Thresher, to review Navy plans for the location, identification, rescue from and recovery of deep-submerged large objects from the ocean floor. It reported in February 1964, and the Secretary of the Navy assigned implementation of the resulting programme, renamed the Deep-Submergence Systems Project, to the Navy's Special Projects Office; by 1967 it was a separate project within the Naval Material Command. Its two primary objectives were rescue of personnel from distressed submarines and locating and recovering small objects from the ocean depths, pursued through a rescue vehicle rated for 6,000 feet and a separate search vehicle intended to search the sea floor to 20,000 feet. The project office carried the designator PM-11.",
  "claims": [
    {
      "tier": 1,
      "text": "The programme has a dated origin and a named parent. 'The Deep-Submergence Systems Review Group (DSSRG) was established in April 1963 to (1) review the Navy's plans for the development and procurement of components and systems related to location, identification, rescue from and recovery of deep-submerged large objects from the ocean floor.' Then: 'In February 1964 the Group reported its findings and recommendations. After review of the report, the Secretary of the Navy assigned the responsibility for implementation of the program, which was renamed the Deep-Submergence Systems Project (DSSP), to the Navy's Special Projects Office.'",
      "source": "M. Krenzke, K. Horn and J. Proffitt, Potential Hull Structures for Rescue and Search Vehicles of the Deep-Submergence Systems Project, David Taylor Model Basin Report 1985, March 1965, DTIC AD-614632, https://archive.org/details/DTIC_AD0614632"
    },
    {
      "tier": 1,
      "text": "Its stated objectives are rescue and recovery: 'Two primary objectives of the DSSP are to develop the capability of rescuing personnel from distressed submarines and to locate and recover small objects from the ocean depths.' Planned force in 1965 was six rescue vehicles and four search vehicles operational by 1970.",
      "source": "David Taylor Model Basin Report 1985, March 1965, DTIC AD-614632, https://archive.org/details/DTIC_AD0614632"
    },
    {
      "tier": 1,
      "text": "The 20,000 foot capability belongs to the search vehicle, not the rescue vehicle. The search vehicle's primary missions are 'to search the ocean bottom to depths of 20,000 ft for either large or small objects and to recover small objects either by actually lifting them or by making an attachment to the object so that a surface lift, or buoyancy lift, can be accomplished', while the study states of the rescue vehicle that 'Only operating depths of 6000 ft are considered in this study.'",
      "source": "David Taylor Model Basin Report 1985, March 1965, DTIC AD-614632, https://archive.org/details/DTIC_AD0614632"
    },
    {
      "tier": 1,
      "text": "The Navy's own 1967 account gives the launch year and the organisational home: 'The Deep Submergence Systems Project (DSSP) was established as a separate Project within the Naval Material Command. The DSSP was launched in 1964 to develop and deliver to the fleet new underwater capabilities: a new rescue system, a large object salvage system, diver tools, the techniques of saturated diving for extended operations on the continental shelf, and new submersible vehicles capable of searching the ocean floors.' The same report describes a planned Deep Submergence Search Vehicle 'whose mission is ultimately to conduct sea floor search to a depth of 20,000 ft, providing coverage of 98 percent of the worlds oceans.'",
      "source": "The Ocean Engineering Program of the U.S. Navy: Accomplishments and Prospects, Office of the Oceanographer of the Navy, September 1967, DTIC AD-665974, https://archive.org/details/DTIC_AD0665974"
    },
    {
      "tier": 1,
      "text": "Two real recoveries frame the programme in the Navy's own telling: the loss of USS Thresher in 1963, whose hull was located in 8,500 ft of water after the casualty 'focused national attention on Navy capabilities underwater', and the 1966 loss of an unarmed nuclear weapon off the Mediterranean coast, located on the sea floor by ALVIN and recovered by the unmanned vehicle CURV.",
      "source": "The Ocean Engineering Program of the U.S. Navy, September 1967, DTIC AD-665974, https://archive.org/details/DTIC_AD0665974"
    }
  ],
  "sources": [
    { "name": "Potential Hull Structures for Rescue and Search Vehicles of the Deep-Submergence Systems Project, David Taylor Model Basin Report 1985, DTIC AD-614632", "url": "https://archive.org/details/DTIC_AD0614632", "date": "1965-03-01" },
    { "name": "The Ocean Engineering Program of the U.S. Navy: Accomplishments and Prospects, Office of the Oceanographer of the Navy, DTIC AD-665974", "url": "https://archive.org/details/DTIC_AD0665974", "date": "1967-09-01" },
    { "name": "Deep Submergence Systems Terminology and Usage, DSSP TD-19 Rev. B, prepared for the Deep Submergence Systems Project Office, DTIC AD-750736", "url": "https://archive.org/details/DTIC_AD0750736", "date": "1970-06-30" },
    { "name": "Deep Submergence Systems Project (DSSP), Deep Submergence Rescue Vehicle (DSRV) report citing DSSP Office (PM-11), DTIC AD-854434", "url": "https://archive.org/details/DTIC_AD0854434", "date": "1969-01-01" }
  ],
  "edges": [
    {
      "a": "deep-submergence-systems-project",
      "b": "us-navy",
      "type": "institutional",
      "claimTier": 1,
      "label": "Assigned by the Secretary of the Navy to the Special Projects Office, February 1964",
      "note": "After the Deep-Submergence Systems Review Group reported in February 1964, the Secretary of the Navy assigned implementation of the programme, renamed DSSP, to the Navy's Special Projects Office; by 1967 it was a separate project within the Naval Material Command, and its project office carried the designator PM-11.",
      "sources": [{ "name": "David Taylor Model Basin Report 1985 (DTIC AD-614632) and Office of the Oceanographer of the Navy, September 1967 (DTIC AD-665974)", "url": "https://archive.org/details/DTIC_AD0614632", "date": "1965-03-01" }]
    }
  ]
}
```

---

## 5. NURO, the National Underwater Reconnaissance Office

**VERDICT: NOT OPENED.** No document naming a National Underwater Reconnaissance Office was
opened from this machine, and no 1969 Navy and CIA agreement establishing one was located.
This is reported as a negative result rather than left as a gap, because the board already
carries an unresolved NURO line and a second unlocatable pointer would be worse than none.

### What was tried

| Route | Result |
|---|---|
| `nro.gov`, including the FOIA and Center for the Study of National Reconnaissance PDF paths that a search returned | **403** to curl with a browser user agent. The brief already records nro.gov as refusing, and it does. |
| `cia.gov/readingroom`, the collection page for Directors and Deputy Directors of Central Intelligence | **Redirect loop**, ten hops, exactly as the brief describes. |
| The archive.org mirror of the CIA reading room, searched for "National Underwater Reconnaissance" and for NURO | Two hits for the phrase, both the same 1962 translated Soviet article "Military Thought: The Submarine Operation of the Navy", which is about Soviet submarine reconnaissance and has nothing to do with a US office. The NURO search returns eighteen items, all false positives on unrelated strings. |
| `govinfo.gov` search API, for the exact phrase | **429, over rate limit** on the shared DEMO_KEY, both attempts. The govinfo internal search endpoints answer 400 and 405 to a direct POST. This is the one route that was not exhausted and it is the one a later pass should retry with a real API key. |
| `www.govinfo.gov/content/pkg/GOVPUB-D-PURL-gpo67811`, the Center for the Study of National Reconnaissance almanac, January 2011, downloaded whole from govinfo and searched | Opens; 3.2 MB; **zero occurrences** of "underwater" or "NURO" in the full text. |
| National Security Archive, `nsarchive.gwu.edu`, full-text search for the exact phrase | Site reachable, search returns no documents for the phrase. |
| The Black Vault document archive, searched for the phrase | Site reachable, five results returned and none of them is a NURO record. |
| The DTIC mirror, searched for "underwater reconnaissance" | One hit, a 1979 cultural resource survey. Nothing relevant. |
| `irp.fas.org`, at the agency and collection-program paths | 404 at both. FAS's Intelligence Resource Program has no NURO page at the paths tried. |

### What this means for the board

`bobby-ray-inman` carries, in its `unverified` list, "A video in which Inman refers to a
National Underwater Reconnaissance Office. The recording was not located in this pass." That
line should stay exactly as it is. Two Area 52 guests, John Ramirez (07 / 1:18:03) and UAP Gerb
(09-3 / 0:35:32 to 0:37:13), name the office independently, and the corpus map for batch 07
itself marks the caption as ambiguous between "Underwater" and "Undersea". Recurrence across
two guests is a reason to keep looking; it is not a document, and no node should be drafted.

**Where a later pass should look, in order.** A govinfo full-text search with a real API key,
since govinfo is reachable from here and only the shared demo key was exhausted; the CIA's
Studies in Intelligence account of Project AZORIAN, which is the likeliest declassified CIA
publication to name the office and which was not reachable from any mirror tried here; and
NRO's FOIA reading room, which will need a machine that nro.gov does not refuse.

---

## Appendix: two incidental findings from documents opened for other reasons

1. **The NACA's own 1954 annual report dates the Research and Development Board's abolition.**
   Its membership section records that the statutory seat formerly held by the chairman of the
   Research and Development Board was replaced by a Department of Defense representative under
   Public Law 384 of the 83rd Congress, approved 3 June 1954, the Board "having been abolished
   by Reorganization Plan No. 6, effective June 30, 1953". Triage group 2 section A row 6 wants
   a Research and Development Board connection for Eric A. Walker; this is a dated primary
   statement about the Board's end, free.
2. **Jerome C. Hunsaker's NACA chairmanship is documented in the same sentence as Bronk's vice
   chairmanship.** Triage group 1 section B lists Hunsaker and NACA as needing NACA's annual
   reports. They have now been opened: he was re-elected chairman of the NACA and of its
   executive committee on 22 October 1954, and is listed first in the membership as
   Massachusetts Institute of Technology. "NACA" occurring zero times on a board that carries
   `nasa` is a gap two annual reports would close.
