# Verified leads: Danny Jones corpus, the 1946 to 1961 institutional cluster (verifier 3)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over six
candidates drawn from section A of `research/leads/dannyjones-triage-2.md`, `-3.md`,
`-5.md` and `-6.md`, run against `research/leads/VERIFY-BRIEF-DANNYJONES-2026-09-03.md`
and, through it, `research/leads/VERIFY-BRIEF-2026-09-02.md` and the format of
`research/leads/verified-area52-1.md`.

**Verified 3 September 2026.** Every URL below was opened by this session and returned the
document described. Where the route was an archive's own download or metadata API rather
than its web page, the row says so. `CLAUDE.md` section 2 governs: nothing here is
asserted that was not opened. A wall is recorded as a wall, and an illegible scan is
recorded as illegible.

**Board state, read from `data/the-program.json` by this session (1,027 ids) rather than
taken from a triage file.** No id contains `groves`, `truman`, `cabell`, `mcelroy`,
`seaborg`, `opc`, `policy-coordination`, `arpa` (only `darpa`),
`research-and-development-board`, `vannevar-bush` or `psychological-strategy-board`.
The ids the draft edges below point at, all confirmed present: `afswp`, `cia`, `dod`,
`usaf`, `us-navy`, `darpa`, `atomic-energy-commission`, `doe`, `sidney-souers`,
`roscoe-hillenkoetter`, `walter-bedell-smith`, `allen-w-dulles`, `richard-m-bissell-jr`,
`donald-keyhoe`, `nicap`, `project-blue-book`, `project-grudge`, `edward-ruppelt`,
`robertson-panel`, `sandia`, `nro`.

**One trap for whoever builds these.** `manhattan-project-2` is NOT the Manhattan Project.
Its label is "'Manhattan Project 2.0' (alleged secrecy architecture)" and its sub is
"Alleged 1947-present secrecy construct". **The board carries no node for the actual
Manhattan Project or Manhattan Engineer District**, which is why the Groves edge below
runs to `afswp` and not to a wartime parent. Do not wire Groves to `manhattan-project-2`.

## Summary

| # | Lead | Verdict | Note |
|---|---|---|---|
| 1 | Leslie R. Groves | CONFIRMED for the AFSWP office and its exact dates; the transcript claim CONTRADICTED | The DoD agency history dates his chieftaincy 28 Feb 1947 to his retirement 29 Feb 1948. It says nothing about OSS, CIA or a militia, and the dates break the claim's premise |
| 2 | Harry S. Truman | CONFIRMED | Both instruments opened in full. The 22 January 1946 directive carries his signature; the 1947 Act's own text establishes the NSC, the CIA, the National Military Establishment and the office Souers held |
| 3 | Charles P. Cabell | CONFIRMED for the offices and their dates; the transcript CONTRADICTED; the Keyhoe letter PARTLY CONFIRMED | FRUS puts him at USAF Intelligence until 1953 and at CIA only from 1953. Blue Book launched March 1952. The scan of document 0000015305 is almost entirely illegible |
| 4 | CIA Office of Policy Coordination | CONFIRMED, with a naming correction the triage row does not carry | NSC 10/2 creates an "Office of Special Projects". The name Office of Policy Coordination appears only from September 1948, in the same volume's persons list |
| 5 | Neil McElroy and the founding of ARPA | CONFIRMED for the founding instrument; the transcript CONTRADICTED twice | The directive's text is reproduced in an ARPA-commissioned history at DTIC. ARPA's first Director was Roy W. Johnson, not Herb York, and the date is 1958, not 1956 to 1957 |
| 6 | Glenn T. Seaborg | PARTLY CONFIRMED | The start of the chairmanship and two dated instances of him in it were opened. **No record opened gives an end date**, so the triage row's "1961 to 1971" is not attested from here |

**The five findings that matter, in order:**

1. **Groves did not "leave in 1947". He took a new command in 1947 and retired in 1948.**
   The Defense Threat Reduction Agency's own history gives, in its chronology, "Feb. 28,
   1947. Maj Gen Groves becomes first Chief AFSWP, serving for one year, until his
   retirement on February 29, 1948; he is promoted to Lt. General on January 24, 1948."
   Kruse's whole construction rests on Groves exiting government in 1947
   and turning the OSS into the CIA as a "parting gift". The record has him inside
   government, in a new joint command, through February 1948.
2. **The OSS was already gone before the period Kruse assigns to Groves.** The FRUS
   persons list, opened for a different candidate, records John Magruder as "Deputy
   Director for Intelligence, Office of Strategic Services, until September 1945; Director
   of Strategic Services Unit, War Department, October 1, 1945-April 4, 1946". The
   operational residue of OSS moved to the War Department on 1 October 1945. Nothing
   opened here connects Groves to any of it.
3. **Cabell was not at CIA when Blue Book launched.** FRUS, 1950-1955, The Intelligence
   Community, List of Persons: "Cabell, General Charles P., USAF, Director of Intelligence,
   Office of the Deputy Chief of Staff from 1951 to 1953; Intelligence Advisory Committee,
   Deputy Director of Central Intelligence from 1953 to 1962". The board's own
   `project-blue-book` node dates the project from March 1952. Ehret's claim that Blue Book
   was "launched under CIA Deputy Director Charles Cabell" is contradicted by the office
   dates: at that date he was the Air Force's Director of Intelligence.
4. **NSC 10/2 does not contain the words "Office of Policy Coordination".** It creates "a
   new Office of Special Projects" inside CIA, under a Chief nominated by the Secretary of
   State, reporting directly to the DCI and operating "independently of other components of
   Central Intelligence Agency". The operating name appears in the same volume's persons
   list, which gives Frank G. Wisner as "Assistant Director for Policy Coordination,
   Central Intelligence Agency, from September 1, 1948". A node built on NSC 10/2 must say
   the office was chartered under one name and stood up under another.
5. **ARPA's first Director was Roy W. Johnson, and Herbert York was its first Chief
   Scientist.** The ARPA-commissioned history at DTIC says so three times, and the CIA
   Historical Staff Chronology's 7 February 1958 entry independently names Johnson.
   Jacobsen's on-tape account ("first director was Herb York", ARPA "created ~1956-57") is
   wrong on both the person and the year. York's actual elevation was from ARPA Chief
   Scientist to first Director of Defense Research and Engineering.

---

## 1. Leslie R. Groves

**VERDICT: CONFIRMED for the AFSWP office and its dates. The transcript claim is
CONTRADICTED.** The record named in the triage row was reopened and its chronology read
directly rather than through the sentence the board already carries in `afswp.desc`.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt | The full OCR text (1.42 MB) of *Defense's Nuclear Agency 1947-1997*, Defense Threat Reduction Agency, 2002, DTIC ADA412977. Downloaded and read locally; the AFSWP narrative, the Appendix C chronology and the index were all read |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/persons | FRUS, 1945-1950, Emergence of the Intelligence Establishment, List of Persons. Read for Magruder and for whether Groves appears at all. **He does not appear in it** |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d71 | The 22 January 1946 presidential directive, opened for candidate 2 below and read here for whether Groves figures in the founding of the postwar intelligence structure. He does not |

### What the document establishes

**The appointment, from the agency's own chronology.** Appendix C, "CHRONOLOGY", carries
three consecutive entries: "Jan. 31, 1947. Maj Gen Leslie R. Groves becomes member of
MLC."; "Feb. 1, 1947. Brig Gen James McCormack, Jr., is appointed Director of the Division
of Military Application, a division within the AEC."; and then "Feb. 28, 1947. Maj Gen
Groves becomes first Chief AFSWP, serving for one year, until his retirement on February
29, 1948; he is promoted to Lt. General on January 24, 1948." The scan renders AFSWP as
"AFS WP" with a broken space throughout the appendix; the rest of the entry is clean.

**Why the post was empty for two months.** The narrative text: "Therefore, between the
beginning of January and the end of February 1947, there was no officially appointed chief
of AFSWP. During this period, Groves' aide, Colonel Hasbrouck, assumed Headquarters command
in Washington as the senior officer of the organization." The same passage records that
AFSWP's offices were first in the new War Department Building "where the Washington offices
of the Manhattan District had been located", and moved to the Pentagon on 15 April 1947.

**The deputy, and the joint character of the command.** "Mar. 31, 1947. Rear Admiral W.S.
Parsons, U.S. Navy, receives appointment as Deputy Chief AFSWP", having become a Navy
member of the Military Liaison Committee to the AEC on 6 November 1946. Brigadier General
Kenneth D. Nichols is captioned in the illustrations as "first AFSWP Deputy Director".

**What the history contains about intelligence work.** Nothing bearing on this claim.
"Office of Strategic Services" and "OSS" do not occur in the text. "Central Intelligence
Agency" occurs five times: once in a footnote saying an officer named Scoville "went to the
Central Intelligence Agency", twice in bibliography entries, once in an index line. "Alsos"
occurs once, as a book title in the bibliography (Goudsmit). "Paperclip" does not occur.
"Militia" does not occur.

### What the transcript claimed that the document does NOT establish

The passage is Jack Kruse on the Danny Jones Podcast #263, "Exiled Brain Surgeon", 30
September 2024, at 1:48:12 to 1:49:51. It was read in the transcript, not only in the lead
map. His words: "this has been planned all the way from when General Groves left in 1947.
You know what his parting gift was? Turning the OSS into the CIA." Then at 1:49:00: "He
formed a militia outside the military and they got powerful", funded by "companies in
Texas, Illinois, and California", and, of the war years, "1942 to 1945, he takes Operation
Paperclip. Allen Dulles, sound familiar?"

| Claim | What the opened record does to it |
|---|---|
| Groves "left" government in 1947 | **Contradicted.** He took AFSWP on 28 February 1947 and served in it until his retirement on 29 February 1948, being promoted to Lieutenant General on 24 January 1948 while in the post |
| His "parting gift was turning the OSS into the CIA" | **No support, and the sequence is wrong.** The DTIC history contains no OSS or CIA transition material at all. The FRUS persons list records the OSS intelligence branch passing to the War Department's Strategic Services Unit on 1 October 1945, and the 22 January 1946 directive creating the Central Intelligence Group names the three service secretaries and no one else |
| He "formed a militia outside the military" funded by companies in three named states | **Nothing opened bears on this.** No company, no state and no post-retirement activity of any kind appears in the record |
| Operation Paperclip, 1942 to 1945, with Allen Dulles | **Outside the record and outside its dates.** Paperclip does not appear in the DTIC history, and the dates Kruse gives precede the operation's own name |

### Draft node

```json
{
  "id": "leslie-r-groves",
  "cls": "person",
  "label": "Lt. Gen. Leslie R. Groves",
  "status": "dead",
  "sub": "First Chief, Armed Forces Special Weapons Project, 28 February 1947 to 29 February 1948",
  "cluster": "legacy",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "date": "1947-02-28",
  "domains": ["d-nuclear", "d-secrecy", "d-custody"],
  "narrative": "Groves is the hinge the board has been carrying in prose. The Armed Forces Special Weapons Project node already reproduces the sentence that makes him its first Chief, and the man himself has had no node on a 1,027-node board. The Defense Threat Reduction Agency's own history dates the appointment to 28 February 1947, one year exactly before his retirement on 29 February 1948, with promotion to Lieutenant General on 24 January 1948 while in post. The same history explains why the post stood empty for two months: neither Eisenhower nor Nimitz had made a selection, and Groves's own aide held the Washington headquarters in the interval. He is here for the office and its dates, and because the transcript that surfaced him is contradicted by the record on the point that carries the claim.",
  "claims": [
    {
      "tier": 1,
      "text": "The Defense Threat Reduction Agency's chronology of its own lineage: 'Feb. 28, 1947. Maj Gen Groves becomes first Chief AFSWP, serving for one year, until his retirement on February 29, 1948; he is promoted to Lt. General on January 24, 1948.'",
      "source": "Defense's Nuclear Agency 1947-1997, Defense Threat Reduction Agency, 2002, Appendix C: Chronology, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt"
    },
    {
      "tier": 1,
      "text": "He had joined the Military Liaison Committee to the Atomic Energy Commission four weeks earlier: 'Jan. 31, 1947. Maj Gen Leslie R. Groves becomes member of MLC.'",
      "source": "Defense's Nuclear Agency 1947-1997, Appendix C: Chronology, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The command was vacant when it was created, and his own aide held it. 'Therefore, between the beginning of January and the end of February 1947, there was no officially appointed chief of AFSWP. During this period, Groves' aide, Colonel Hasbrouck, assumed Headquarters command in Washington as the senior officer of the organization.'",
      "source": "Defense's Nuclear Agency 1947-1997, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast #263, 30 September 2024, at 1:48:12, Jack Kruse said the covert apparatus he describes 'has been planned all the way from when General Groves left in 1947' and that Groves's 'parting gift was turning the OSS into the CIA', adding at 1:49:00 that Groves 'formed a militia outside the military'. The agency history opened for this node contradicts the premise: Groves did not leave government in 1947, he took a new joint command on 28 February 1947 and retired on 29 February 1948. The same history contains no reference to the Office of Strategic Services, to Operation Paperclip or to any militia.",
      "source": "Danny Jones Podcast #263, 'Exiled Brain Surgeon', 30 September 2024, transcript at 1:48:12 to 1:49:51; contradicted against Defense's Nuclear Agency 1947-1997, DTIC ADA412977, https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt"
    }
  ],
  "sources": [
    {"name": "Defense's Nuclear Agency 1947-1997, Defense Threat Reduction Agency, 2002, DTIC ADA412977", "url": "https://archive.org/download/DTIC_ADA412977/DTIC_ADA412977_djvu.txt", "date": "2002-01-01"},
    {"name": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-03"}
  ],
  "edges": [
    {"a": "leslie-r-groves", "b": "afswp", "type": "institutional", "claimTier": 1, "dateStart": "1947-02-28", "dateEnd": "1948-02-29", "label": "First Chief, AFSWP", "note": "The agency's own chronology dates the appointment and the retirement to the day, and gives the promotion to Lieutenant General on 24 January 1948 while in post."},
    {"a": "leslie-r-groves", "b": "atomic-energy-commission", "type": "institutional", "claimTier": 1, "dateStart": "1947-01-31", "label": "Member, Military Liaison Committee to the AEC", "note": "He joined the Military Liaison Committee on 31 January 1947, four weeks before taking AFSWP, so the same officer sat on both sides of the military-civil split of the atomic programme."},
    {"a": "leslie-r-groves", "b": "us-navy", "type": "institutional", "claimTier": 1, "dateStart": "1947-03-31", "label": "Joint command with a Navy deputy", "note": "Rear Admiral W.S. Parsons was appointed Deputy Chief AFSWP on 31 March 1947, the deputy coming from the opposite service by the terms of the activating directive."}
  ]
}
```

---

## 2. Harry S. Truman

**VERDICT: CONFIRMED.** Both instruments named in the triage row were opened in full. This
is a promotion from prose and the records support it without qualification.

### What was opened

| URL | What is at it |
|---|---|
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d71 | FRUS, 1945-1950, Emergence of the Intelligence Establishment, Document 71: "Presidential Directive on Coordination of Foreign Intelligence Activities", Washington, 22 January 1946, ten numbered paragraphs, signed "Sincerely yours, Harry S. Truman". Source note: *Public Papers of the Presidents of the United States: Harry S. Truman, 1946*, pp. 88-89, also published at 11 Fed. Reg. 1337, 1339 on 5 February 1946 |
| https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf | The National Security Act of 1947, Public Law 80-253, ch. 343, 61 Stat. 495. The PDF was fetched and converted to text locally with `pdftotext -layout`; sections 2, 101, 102, 201 and 202 were read in full |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/persons | The same volume's List of Persons: "Truman, Harry S., President of the United States from April 12, 1945" |

### What the documents establish

**The 1946 directive, and that he signed it.** It is addressed "To the Secretary of State,
the Secretary of War, and the Secretary of the Navy". Paragraph 1 opens "It is my desire,
and I hereby direct, that all Federal foreign intelligence activities be planned, developed
and coordinated so as to assure the most effective accomplishment of the intelligence
mission related to the national security", and designates the three of them, with a fourth
personal representative, as the National Intelligence Authority. Paragraph 2 is the one the
board already quotes on `sidney-souers`: the assigned personnel "shall collectively form a
Central Intelligence Group and shall, under the direction of a Director of Central
Intelligence, assist the National Intelligence Authority. The Director of Central
Intelligence shall be designated by me". Paragraph 4 reads in full: "No police, law
enforcement or internal security functions shall be exercised under this directive."
Paragraph 10 makes the Authority and the DCI "responsible for fully protecting intelligence
sources and methods".

**The 1947 Act, in its own words.** The statute page carries "Approved July 26, 1947."
Section 2, the Declaration of Policy, states the intent "to provide a comprehensive program
for the future security of the United States" and "to provide for their authoritative
coordination and unified direction under civilian control but not to merge them". Section
101(a): "There is hereby established a council to be known as the National Security
Council", over whose meetings "The President of the United States shall preside". Section
102(a): "There is hereby established under the National Security Council a Central
Intelligence Agency with a Director of Central Intelligence, who shall be the head
thereof." Section 102(d)(5), the residual clause NSC 10/2 would later invoke, authorises
the Agency "to perform such other functions and duties related to intelligence affecting
the national security as the National Security Council may from time to time direct."
Section 201(a): "There is hereby established the National Military Establishment, and the
Secretary of Defense shall be the head thereof." Section 202(a) requires that Secretary to
"be appointed from civilian life" and bars anyone who "has within ten years been on active
duty as a commissioned officer in a Regular component of the armed services".

**A detail the board should carry.** Section 101(a) lists as possible additional NSC members
"the Chairman of the Munitions Board appointed under section 213, and the Chairman of the
Research and Development Board appointed under section 214". The Research and Development
Board that the board discusses in prose is a creature of this statute, section 214.

### What the transcript claimed that the documents do NOT establish

Nothing. This candidate is a promotion from the board's own prose, not a transcript claim,
and the triage row says so. The row also names "his July 1952 incoming correspondence" at
the Truman Library; **that was not opened and is not drafted here.** The Farnsworth letter
of July 1952 is a separate candidate (triage-5 row 13) and belongs to whoever takes it.

### Draft node

```json
{
  "id": "harry-s-truman",
  "cls": "person",
  "label": "Harry S. Truman",
  "status": "dead",
  "sub": "President of the United States from 12 April 1945; signatory of the 22 January 1946 intelligence directive and of the National Security Act of 1947",
  "cluster": "ic",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "date": "1946-01-22",
  "domains": ["d-ic", "d-structure", "d-policy"],
  "narrative": "The president who signed the founding instruments of the structure this board maps has had no node on it, because the board's prose says 'Truman' and never 'Harry'. Two records settle the office and the instruments. The directive of 22 January 1946 creates the National Intelligence Authority and the Central Intelligence Group and the post of Director of Central Intelligence, and carries his signature. The National Security Act of 1947, approved 26 July 1947, creates the National Security Council, the Central Intelligence Agency, the National Military Establishment and a Research and Development Board, and requires the Secretary of Defense to come from civilian life. He is here for the instruments, not for anything said about him on a podcast.",
  "claims": [
    {
      "tier": 1,
      "text": "The 22 January 1946 directive is signed by him and creates the office by fiat: 'It is my desire, and I hereby direct, that all Federal foreign intelligence activities be planned, developed and coordinated so as to assure the most effective accomplishment of the intelligence mission related to the national security.' The Director of Central Intelligence 'shall be designated by me'.",
      "source": "Presidential Directive on Coordination of Foreign Intelligence Activities, 22 January 1946, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 71, https://history.state.gov/historicaldocuments/frus1945-50Intel/d71"
    },
    {
      "tier": 1,
      "text": "The same directive draws the domestic line the board's later argument keeps testing: 'No police, law enforcement or internal security functions shall be exercised under this directive', and it makes the Authority and the Director 'responsible for fully protecting intelligence sources and methods'.",
      "source": "Presidential Directive on Coordination of Foreign Intelligence Activities, 22 January 1946, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 71, https://history.state.gov/historicaldocuments/frus1945-50Intel/d71"
    },
    {
      "tier": 1,
      "text": "The statute approved on 26 July 1947 creates, in one instrument, the Council, the Agency and the military establishment: 'There is hereby established a council to be known as the National Security Council'; 'There is hereby established under the National Security Council a Central Intelligence Agency with a Director of Central Intelligence, who shall be the head thereof'; 'There is hereby established the National Military Establishment, and the Secretary of Defense shall be the head thereof.'",
      "source": "National Security Act of 1947, Public Law 80-253, ch. 343, 61 Stat. 495, secs. 101(a), 102(a), 201(a), approved 26 July 1947, https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf"
    },
    {
      "tier": 1,
      "text": "Section 102(d)(5) of the same Act is the residual authority every later covert-action directive is written under: the Agency is 'to perform such other functions and duties related to intelligence affecting the national security as the National Security Council may from time to time direct.'",
      "source": "National Security Act of 1947, Public Law 80-253, 61 Stat. 495, sec. 102(d)(5), https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf"
    },
    {
      "tier": 1,
      "text": "The Department of State's own list of persons gives the office and its start: 'Truman, Harry S., President of the United States from April 12, 1945'.",
      "source": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons, https://history.state.gov/historicaldocuments/frus1945-50Intel/persons"
    }
  ],
  "sources": [
    {"name": "Presidential Directive on Coordination of Foreign Intelligence Activities, 22 January 1946 (FRUS 1945-50 Intel, Doc. 71)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d71", "date": "1946-01-22"},
    {"name": "National Security Act of 1947, Public Law 80-253, 61 Stat. 495", "url": "https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf", "date": "1947-07-26"},
    {"name": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-03"}
  ],
  "edges": [
    {"a": "harry-s-truman", "b": "cia", "type": "institutional", "claimTier": 1, "dateStart": "1947-07-26", "label": "Signed the statute that created the Agency", "note": "Section 102(a) of the National Security Act of 1947, approved 26 July 1947, establishes the Central Intelligence Agency under the National Security Council."},
    {"a": "harry-s-truman", "b": "sidney-souers", "type": "institutional", "claimTier": 1, "dateStart": "1946-01-22", "label": "Designated the first Director of Central Intelligence", "note": "The directive reserves the designation to the President: 'The Director of Central Intelligence shall be designated by me'. The board's Souers node already carries the office and its dates."},
    {"a": "harry-s-truman", "b": "dod", "type": "institutional", "claimTier": 1, "dateStart": "1947-07-26", "label": "Signed the statute that created the National Military Establishment", "note": "Section 201(a) establishes the National Military Establishment under a Secretary of Defense who, by section 202(a), must be appointed from civilian life."},
    {"a": "harry-s-truman", "b": "usaf", "type": "institutional", "claimTier": 1, "dateStart": "1947-07-26", "label": "Signed the statute that created the Department of the Air Force", "note": "Section 2's declaration of policy provides three military departments including the Air Force, and section 101(a) names a Secretary of the Air Force appointed under section 207."},
    {"a": "harry-s-truman", "b": "roscoe-hillenkoetter", "type": "institutional", "claimTier": 2, "dateStart": "1947", "label": "Appointed the first Director of Central Intelligence of the CIA", "note": "The board's Hillenkoetter node dates his DCI service from May 1947. The appointment power is in the 1946 directive and in section 102(a) of the 1947 Act; the specific appointment paper was not opened here, so this edge is capped at Tier 2."}
  ]
}
```

---

## 3. Charles P. Cabell

**VERDICT: CONFIRMED for the offices and their dates. The transcript claim placing him at
CIA when Blue Book launched is CONTRADICTED. The letter to Keyhoe is PARTLY CONFIRMED:
the document exists and is his, and the scan is almost entirely illegible.**

### What was opened

| URL | What is at it |
|---|---|
| https://history.state.gov/historicaldocuments/frus1950-55Intel/persons | FRUS, 1950-1955, The Intelligence Community, List of Persons. The Cabell entry reads: "Cabell, General Charles P., USAF, Director of Intelligence, Office of the Deputy Chief of Staff from 1951 to 1953; Intelligence Advisory Committee, Deputy Director of Central Intelligence from 1953 to 1962" |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/persons | The earlier volume's List of Persons: "Cabell, General Charles P., Director of Intelligence, Office of the Deputy Chief of Staff, U.S. Air Force; member, Intelligence Advisory Committee". No dates are given in that volume, which covers 1945 to 1950 |
| https://archive.org/download/cia-readingroom-document-cia-rdp85b00803r000200050003-5/cia-rdp85b00803r000200050003-5_djvu.txt | The CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, Secret, "Declassified in Part - Sanitized Copy Approved for Release 2013/07/08", CIA-RDP85B00803R000200050003-5. Full OCR text downloaded and read |
| https://archive.org/details/cia-readingroom-document-0000015305 and its download at https://archive.org/download/cia-readingroom-document-0000015305/0000015305_djvu.txt | CIA reading room document 0000015305, the letter the board already cites on `donald-keyhoe`. Its item metadata and its full OCR text were both retrieved |

### What the documents establish

**The offices, with dates.** The two FRUS persons lists between them put Cabell at Air Force
Intelligence across the whole 1948 to 1953 span, with the later volume giving "from 1951 to
1953" within its own period of coverage, and then at CIA as Deputy Director of Central
Intelligence "from 1953 to 1962".

**The end of the CIA post, to the day.** The CIA Historical Staff Chronology, under
"Dec 61": "27 DEC. Lt. Gen. C.P. Cabell resigns as DDCI (effective 31 Jan 62)." Under
"Mar-Apr 62": "9 MAR. Maj. Gen. Marshall S. Carter appointed DDCI, succeeding Cabell; 2
Apr. confirmed by Senate, promoted to Lt. Gen.; 3 Apr. sworn in". The same chronology, under
"Dec 61", records that USIB membership was expanded that month and "DDCI Cabell named CIA
member".

**The Keyhoe letter, as far as it can be read.** The archive.org item's own catalogue title
is "CIA Reading Room 0000015305: UNTITLED (TO DONALD KEYHOE FROM C P CABELL ACKNOWLEDGING
HIS LETTER OF MARCH 1", truncated in the metadata field itself, with a reading-room date of
5 February 1958 and no description. The OCR of the scan is close to unusable: the
addressee line resolves to "Mejor Docabld 3. Reyha-", the signature block to "C. P. Cezehh"
over "Bopaty Directs", and a distribution list of five lines follows. Read against the
title, the signature is C. P. Cabell and the title beneath it is Deputy Director. **No
sentence of the letter's body is legible and none is quoted here.** The board's existing
citation of this document on `donald-keyhoe` is a source entry, not a quotation, and that
is the right treatment.

### What the transcript claimed that these documents do NOT establish

The passage is Matthew Ehret on the Danny Jones Podcast #406, "They Want to Replace God",
19 June 2026, at 1:24:32 to 1:25:21 as recorded in `dannyjones-corpus-08.md`.

| Claim | What the opened record does to it |
|---|---|
| Blue Book was "launched under CIA Deputy Director Charles Cabell" | **Contradicted.** FRUS puts him at CIA only from 1953. The board's own `project-blue-book` node dates the project from March 1952, when FRUS has him as the Air Force's Director of Intelligence. The office is real, the agency is wrong |
| He was "fired by JFK, 1961" | **Contradicted in form, close in date.** The CIA's own chronology says he "resigns as DDCI" on 27 December 1961, effective 31 January 1962, and was succeeded on 9 March 1962. Nothing opened says he was dismissed |
| Blue Book was launched "at the urging of Sir Henry Tizard's UK flying saucer working party (1950)" | **Not opened.** No record on the UK Flying Saucer Working Party was reached in this pass. This is a NOT OPENED, not a denial |

### Draft node

```json
{
  "id": "charles-p-cabell",
  "cls": "person",
  "label": "Gen. Charles P. Cabell",
  "status": "dead",
  "sub": "Director of Intelligence, USAF, to 1953; Deputy Director of Central Intelligence, 1953 to 1962",
  "cluster": "ic",
  "tier": "B",
  "C": 2,
  "A": 2,
  "D": 2,
  "date": "1953-01-01",
  "domains": ["d-ic", "d-intel", "d-denial"],
  "narrative": "The board already holds a document over Cabell's signature, cited as a source on the Keyhoe node, and has never had a node for the man who signed it. The two FRUS persons lists give the offices: Director of Intelligence in the Office of the Deputy Chief of Staff, U.S. Air Force, through 1953, then Deputy Director of Central Intelligence from 1953 to 1962. Those dates are the finding. He was the Air Force's intelligence chief through the reorganisation of the UFO project and only afterwards a CIA officer, which is the reverse of how the podcast corpus places him. The CIA's own historical chronology closes the second office: he resigned as DDCI on 27 December 1961, effective 31 January 1962, and was succeeded by Marshall S. Carter in March 1962.",
  "claims": [
    {
      "tier": 1,
      "text": "The Department of State's list of persons for the intelligence volume gives both offices: 'Cabell, General Charles P., USAF, Director of Intelligence, Office of the Deputy Chief of Staff from 1951 to 1953; Intelligence Advisory Committee, Deputy Director of Central Intelligence from 1953 to 1962.'",
      "source": "FRUS, 1950-1955, The Intelligence Community, List of Persons, https://history.state.gov/historicaldocuments/frus1950-55Intel/persons"
    },
    {
      "tier": 1,
      "text": "He held the Air Force post in the earlier period too. The 1945-1950 volume's list of persons carries him without dates as 'Director of Intelligence, Office of the Deputy Chief of Staff, U.S. Air Force; member, Intelligence Advisory Committee'.",
      "source": "FRUS, 1945-1950, Emergence of the Intelligence Establishment, List of Persons, https://history.state.gov/historicaldocuments/frus1945-50Intel/persons"
    },
    {
      "tier": 1,
      "text": "The CIA's own declassified chronology closes the CIA post: '27 DEC. Lt. Gen. C.P. Cabell resigns as DDCI (effective 31 Jan 62)', and '9 MAR. Maj. Gen. Marshall S. Carter appointed DDCI, succeeding Cabell'. The same volume records that in December 1961 'DDCI Cabell named CIA member' when USIB membership was expanded that month.",
      "source": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, CIA-RDP85B00803R000200050003-5, declassified in part 8 July 2013, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5"
    },
    {
      "tier": 1,
      "text": "The board already cites a letter he sent to Donald Keyhoe. The reading room's own catalogue entry for it reads 'UNTITLED (TO DONALD KEYHOE FROM C P CABELL ACKNOWLEDGING HIS LETTER OF MARCH 1', reading-room date 5 February 1958. The scan's OCR is close to unusable: the signature block resolves only far enough to read C. P. Cabell over the title Deputy Director, and no sentence of the body is legible. Nothing is quoted from it here.",
      "source": "CIA reading room document 0000015305, https://archive.org/details/cia-readingroom-document-0000015305"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast #406, 19 June 2026, at 1:24:32, Matthew Ehret said Project Blue Book was launched under 'CIA Deputy Director Charles Cabell' at the urging of Sir Henry Tizard's UK flying saucer working party, and that Cabell was fired by John F. Kennedy in 1961. The opened records contradict the office: at Blue Book's launch in March 1952 he was the Air Force's Director of Intelligence, and he joined CIA as Deputy Director only in 1953. The CIA's own chronology records a resignation, not a dismissal, on 27 December 1961 effective 31 January 1962.",
      "source": "Danny Jones Podcast #406, 'They Want to Replace God', 19 June 2026, at 1:24:32 to 1:25:21; contradicted against FRUS, 1950-1955, The Intelligence Community, List of Persons, https://history.state.gov/historicaldocuments/frus1950-55Intel/persons"
    }
  ],
  "sources": [
    {"name": "FRUS 1950-1955, The Intelligence Community, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1950-55Intel/persons", "date": "2026-09-03"},
    {"name": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-03"},
    {"name": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, CIA-RDP85B00803R000200050003-5", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5", "date": "1970-06-01"},
    {"name": "CIA reading room document 0000015305, letter to Donald Keyhoe from C. P. Cabell", "url": "https://archive.org/details/cia-readingroom-document-0000015305", "date": "1958-02-05"}
  ],
  "edges": [
    {"a": "charles-p-cabell", "b": "usaf", "type": "institutional", "claimTier": 1, "dateEnd": "1953", "label": "Director of Intelligence, Office of the Deputy Chief of Staff, USAF", "note": "Both FRUS persons lists give the office; the later volume dates it to 1953 within its own coverage. This is the office he held while Project Blue Book was created."},
    {"a": "charles-p-cabell", "b": "cia", "type": "institutional", "claimTier": 1, "dateStart": "1953", "dateEnd": "1962-01-31", "label": "Deputy Director of Central Intelligence", "note": "FRUS gives 1953 to 1962; the CIA's own chronology gives the resignation as 27 December 1961, effective 31 January 1962."},
    {"a": "charles-p-cabell", "b": "donald-keyhoe", "type": "denial", "claimTier": 1, "dateStart": "1958-02-05", "label": "Signed the CIA reply to Keyhoe", "note": "The reading room's catalogue entry names him as the sender and Keyhoe as the addressee. The scan's body text is illegible, so the edge records the correspondence and not its content."},
    {"a": "charles-p-cabell", "b": "project-blue-book", "type": "temporal", "claimTier": 1, "dateStart": "1952-03", "label": "Air Force intelligence chief at Blue Book's creation", "note": "The edge exists to carry the correction: the office he held in March 1952 was USAF Director of Intelligence, not a CIA post, and the transcript that surfaced him has it the other way round."},
    {"a": "charles-p-cabell", "b": "allen-w-dulles", "type": "institutional", "claimTier": 1, "dateStart": "1953", "label": "Served as deputy to the Director of Central Intelligence", "note": "Cabell's DDCI service from 1953 runs alongside the board's Dulles node; the deputy relationship is the office, and no shared action is asserted here."}
  ]
}
```

---

## 4. CIA Office of Policy Coordination

**VERDICT: CONFIRMED, with a naming correction the triage row does not carry.** NSC 10/2
was opened in full. It creates the office, and it does not use the name the office
operated under.

### What was opened

| URL | What is at it |
|---|---|
| https://history.state.gov/historicaldocuments/frus1945-50Intel/d292 | FRUS, 1945-1950, Emergence of the Intelligence Establishment, Document 292: "National Security Council Directive on Office of Special Projects", Washington, 18 June 1948, NSC 10/2, Top Secret, six numbered paragraphs plus two editorial footnotes. Source note: NARA RG 273, Records of the National Security Council, NSC 10/2. The page was fetched and its text extracted locally, not read through a search snippet |
| https://history.state.gov/historicaldocuments/frus1945-50Intel/persons | The same volume's List of Persons, read for the operating name and the officers |

### What the document establishes

**Why it exists, and under what authority.** Paragraph 1: the Council, "taking cognizance of
the vicious covert activities of the USSR, its satellite countries and Communist groups",
determined "that, in the interests of world peace and US national security, the overt
foreign activities of the US Government must be supplemented by covert operations."
Paragraph 3 acts "under the authority of Section 102(d)(5) of the National Security Act of
1947", the residual clause quoted in candidate 2 above.

**What is created, and under what name.** Paragraph 3.a: "A new Office of Special Projects
shall be created within the Central Intelligence Agency to plan and conduct covert
operations; and in coordination with the Joint Chiefs of Staff to plan and prepare for the
conduct of such operations in wartime." Paragraph 3.b puts the nomination of its Chief with
the Secretary of State, subject to the DCI's acceptance and the Council's approval.
Paragraph 3.c: "The Chief of the Office of Special Projects shall report directly to the
Director of Central Intelligence. For purposes of security and of flexibility of operations,
and to the maximum degree consistent with efficiency, the Office of Special Projects shall
operate independently of other components of Central Intelligence Agency."

**The definition of covert operations, which is the paragraph a node should carry.**
Paragraph 5: covert operations are "all activities (except as noted herein) which are
conducted or sponsored by this Government against hostile foreign states or groups or in
support of friendly foreign states or groups but which are so planned and executed that any
US Government responsibility for them is not evident to unauthorized persons and that if
uncovered the US Government can plausibly disclaim any responsibility for them."
Specifically included: "propaganda, economic warfare; preventive direct action, including
sabotage, anti-sabotage, demolition and evacuation measures; subversion against hostile
states, including assistance to underground resistance movements, guerrillas and refugee
liberation groups, and support of indigenous anti-communist elements in threatened countries
of the free world." Specifically excluded: "armed conflict by recognized military forces,
espionage, counter-espionage, and cover and deception for military operations."

**Wartime.** Paragraph 4: "In time of war, or when the President directs, all plans for
covert operations shall be coordinated with the Joint Chiefs of Staff." Paragraph 6
supersedes and cancels NSC 4-A.

**The operating name, and the officers, from the same volume's persons list.** "Wisner,
Frank G., Deputy Assistant Secretary of State for the Occupied Areas, 1947-1948; Assistant
Director for Policy Coordination, Central Intelligence Agency, from September 1, 1948."
Two senior consultants are recorded "from September 1948": George F. Kennan representing the
Secretary of State (an editorial footnote to the directive itself says Kennan "was
subsequently appointed as the representative of the Secretary of State", per an August 13
memorandum from Davies to Kennan), and John Magruder representing the Secretary of Defense.

### What the transcript claimed that the document does NOT establish

The passages are Matthew Ehret, Danny Jones Podcast #406, 19 June 2026, at 1:25:21 to
1:26:10 and 1:29:15 to 1:31:56.

| Claim | What the opened record does to it |
|---|---|
| OPC was "The CIA's Psychological Warfare Department, 1951" | **Partly.** The charter is 18 June 1948 and the name in it is Office of Special Projects. Propaganda is the first named category of covert operation, so "psychological warfare" is a fair reading of part of the mandate and a wrong reading of the whole |
| NICAP was "founded/staffed by CIA officials out of the Office of Policy Coordination" | **Nothing opened bears on it.** The charter says what the office may do, not who later worked where. The board's own `nicap` node dates the body from 1956, eight years after the charter and four years after the office was absorbed |
| The *National Enquirer*'s founder "worked here for 14 months immediately before founding it" | **Nothing opened bears on it.** No personnel record was reached |
| Richard Bissell "headed this CIA psychological-warfare bureau" | **Not established.** The only OPC officer named in the records opened is Frank G. Wisner, Assistant Director for Policy Coordination from 1 September 1948. The board's own Bissell node gives his CIA post as Special Assistant for Planning and Coordination from 1954 |
| The 1952 merger into the Directorate of Plans | **NOT OPENED.** The triage row names it and no record for it was reached in this pass |

### Draft node

```json
{
  "id": "cia-office-of-policy-coordination",
  "cls": "institution",
  "label": "CIA Office of Policy Coordination",
  "sub": "Covert action office chartered by NSC 10/2 as the Office of Special Projects, 18 June 1948; operating from 1 September 1948",
  "cluster": "ic",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "dateStart": "1948-06-18",
  "domains": ["d-ic", "d-psyop", "d-secrecy"],
  "desc": "The office the Danny Jones corpus keeps invoking has a charter, and the charter is openable. NSC 10/2 of 18 June 1948 created it inside the Central Intelligence Agency under the residual authority of section 102(d)(5) of the National Security Act of 1947, to plan and conduct covert operations, with its Chief nominated by the Secretary of State, reporting directly to the Director of Central Intelligence, and operating 'independently of other components of Central Intelligence Agency'. Two things a node must say and the transcript does not. The directive names the office the Office of Special Projects; the name Office of Policy Coordination appears only from September 1948, when Frank G. Wisner became Assistant Director for Policy Coordination. And the directive's own definition of covert operations is a definition of deniability rather than of psychological warfare: operations 'so planned and executed that any US Government responsibility for them is not evident to unauthorized persons and that if uncovered the US Government can plausibly disclaim any responsibility for them'.",
  "claims": [
    {
      "tier": 1,
      "text": "The charter creates the office by that name: 'A new Office of Special Projects shall be created within the Central Intelligence Agency to plan and conduct covert operations; and in coordination with the Joint Chiefs of Staff to plan and prepare for the conduct of such operations in wartime.'",
      "source": "NSC 10/2, National Security Council Directive on Office of Special Projects, 18 June 1948, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 292, https://history.state.gov/historicaldocuments/frus1945-50Intel/d292"
    },
    {
      "tier": 1,
      "text": "It is written under the residual clause of the 1947 Act: the Council directs the creation 'under the authority of Section 102(d)(5) of the National Security Act of 1947'.",
      "source": "NSC 10/2, 18 June 1948, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 292, https://history.state.gov/historicaldocuments/frus1945-50Intel/d292"
    },
    {
      "tier": 1,
      "text": "The definition is a definition of deniability. Covert operations are those 'so planned and executed that any US Government responsibility for them is not evident to unauthorized persons and that if uncovered the US Government can plausibly disclaim any responsibility for them', and the named categories are 'propaganda, economic warfare; preventive direct action, including sabotage, anti-sabotage, demolition and evacuation measures; subversion against hostile states'. Espionage, counter-espionage and 'cover and deception for military operations' are expressly excluded.",
      "source": "NSC 10/2, 18 June 1948, paragraph 5, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 292, https://history.state.gov/historicaldocuments/frus1945-50Intel/d292"
    },
    {
      "tier": 1,
      "text": "The office was built to sit apart inside its own agency: 'The Chief of the Office of Special Projects shall report directly to the Director of Central Intelligence. For purposes of security and of flexibility of operations, and to the maximum degree consistent with efficiency, the Office of Special Projects shall operate independently of other components of Central Intelligence Agency.'",
      "source": "NSC 10/2, 18 June 1948, paragraph 3.c, FRUS 1945-1950, Emergence of the Intelligence Establishment, Document 292, https://history.state.gov/historicaldocuments/frus1945-50Intel/d292"
    },
    {
      "tier": 1,
      "text": "The operating name and the first officer come from the same volume's list of persons: 'Wisner, Frank G., Deputy Assistant Secretary of State for the Occupied Areas, 1947-1948; Assistant Director for Policy Coordination, Central Intelligence Agency, from September 1, 1948.' George F. Kennan and John Magruder are recorded as senior consultants to the Office of Policy Coordination representing the Secretary of State and the Secretary of Defense respectively, both from September 1948.",
      "source": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons, https://history.state.gov/historicaldocuments/frus1945-50Intel/persons"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast #406, 19 June 2026, at 1:29:15 to 1:31:56, Matthew Ehret said the office staffed NICAP's leadership and that the founder of the National Enquirer worked in it for fourteen months before founding the paper, and at 1:25:21 that Richard Bissell headed it. No record opened here bears on any of the three. The only officer named in the opened records is Frank G. Wisner, from 1 September 1948.",
      "source": "Danny Jones Podcast #406, 'They Want to Replace God', 19 June 2026, at 1:25:21 to 1:31:56; tested against NSC 10/2, https://history.state.gov/historicaldocuments/frus1945-50Intel/d292"
    }
  ],
  "sources": [
    {"name": "NSC 10/2, National Security Council Directive on Office of Special Projects (FRUS 1945-50 Intel, Doc. 292)", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/d292", "date": "1948-06-18"},
    {"name": "FRUS 1945-1950, Emergence of the Intelligence Establishment, List of Persons", "url": "https://history.state.gov/historicaldocuments/frus1945-50Intel/persons", "date": "2026-09-03"},
    {"name": "National Security Act of 1947, Public Law 80-253, 61 Stat. 495, sec. 102(d)(5)", "url": "https://www.govinfo.gov/content/pkg/STATUTE-61/pdf/STATUTE-61-Pg495.pdf", "date": "1947-07-26"}
  ],
  "edges": [
    {"a": "cia-office-of-policy-coordination", "b": "cia", "type": "institutional", "claimTier": 1, "dateStart": "1948-06-18", "label": "Created inside the Agency by NSC 10/2", "note": "The directive places the office within CIA but requires it to operate independently of the Agency's other components and to report through its Chief directly to the Director of Central Intelligence."},
    {"a": "cia-office-of-policy-coordination", "b": "harry-s-truman", "type": "legislative", "claimTier": 1, "dateStart": "1948-06-18", "label": "Chartered under section 102(d)(5) of the Act he signed", "note": "The directive names its own authority as the residual clause of the National Security Act of 1947, approved 26 July 1947."},
    {"a": "cia-office-of-policy-coordination", "b": "d-psyop", "type": "programmatic", "claimTier": 1, "dateStart": "1948-06-18", "label": "Propaganda is the first named category in the charter", "note": "Paragraph 5 lists propaganda first among covert operations, which is the documented basis for treating the office as a psychological-operations instrument, before any claim about UFO matters is made."}
  ]
}
```

---

## 5. Neil McElroy and the founding of ARPA

**VERDICT: CONFIRMED for the founding instrument, its number and its date. The
transcript is CONTRADICTED on two points, and the ARPA claim it makes about Herbert York
is wrong.**

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt | *The Advanced Research Projects Agency, 1958-1974*, a study prepared for ARPA by Richard J. Barber Associates, Inc., DTIC AD-A154 363. Full OCR text (1.85 MB) downloaded and read. Its Figure II-2 is captioned "TEXT OF DOD DIRECTIVE NUMBER 5105.15, FEBRUARY 7, 1958 (Establishing ARPA)" and reproduces the directive |
| https://archive.org/download/cia-readingroom-document-cia-rdp85b00803r000200050003-5/cia-rdp85b00803r000200050003-5_djvu.txt | The CIA Historical Staff Chronology 1946-65, Volume II 1956-65, read for its own 1958 entries |
| https://archive.org/metadata/cia-readingroom-document-cia-rdp85b00803r000100040092-9 and its OCR text | CIA reading room document CIA-RDP85B00803R000100040092-9, "ESTABLISHMENT OF ADVANCED RESEARCH PROJECTS AGENCY, THOR (USAF PROJECT)", an index card dated 15 January 1958 quoting the *U.S. Government Organization Manual, 1958-59*, revised as of 1 June 1958, p. 193 |
| https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/510515p.pdf | **NOT OPENED.** The Washington Headquarters Services issuance repository returned HTTP 403 to curl with and without a browser user agent, and to WebFetch. The `cancelled/` path returned 403 as well. The directive's own PDF at its issuing office is a wall from this machine |

### What the documents establish

**The directive, reproduced.** Figure II-2 of the ARPA-commissioned history gives the text.
Section I, PURPOSE: "The purpose of this directive is to provide within the Department of
Defense an agency for the direction and performance of certain advanced research and
development projects." Section II.A, Establishment: "In accordance with the provisions of
the National Security Act of 1947, as amended, and Reorganization Plan No. 6 of 1953, there
is established in the Office of the Secretary of Defense the Department of Defense Advanced
Research Projects Agency." Section II.B, Responsibility: the Agency is responsible for "the
direction or performance of such advanced projects in the field of research and development
as the Secretary of Defense shall, from time to time, designate by individual project or by
category." Section III.A: "The Director of Advanced Research Projects shall report to the
Secretary of Defense." Section IV: "This directive is effective immediately." The
authorities in II.C run to directing DoD projects the Secretary designates, arranging work
through other agencies "including the military departments", contracting with private and
academic bodies, and acquiring facilities, "However, existing facilities of the Department
of Defense shall be utilized to the maximum extent practicable."

**An OCR warning that matters.** The scan is a poor one. It renders ARPA as "AREA" and
"AEPA", "National" as "Uaticral", "Reorganization" as "Reorganisation", and in one narrative
sentence gives the issue date as "February 1, 1953" where the same page's figure caption and
the same chapter's appointment sentence both give February 7, 1958. Where a word above is
given in clean modern spelling, it has been normalised from an obvious OCR corruption and
the reading is stated here rather than hidden.

**Who issued it, and who ran the agency.** The history's narrative: "ARPA started life by
means of a DOD Directive issued by the Secretary on February [7, 1958]; a supplemental Air
Force appropriations bill enacted on February 11; and Congressional authorization in a
section of a military construction bill enacted on February 12." And: "Secretary McElroy,
sworn in just five days after Sputnik, took a highly personal hand in establishing ARPA and
ultimately selected Mr. Roy W. Johnson as its first Director." The chapter's own heading and
a later sentence date the appointment: "Roy Johnson's appointment as Director of ARPA, on
February 7, 1958." Herbert York is identified in the same study as "first ARPA Chief
Scientist", and his later move is described as an "elevation from Chief Scientist of ARPA to
become the first Director of Defense Research and Engineering (DDR&E)".

**Independent corroboration from a second agency's record.** The CIA Historical Staff
Chronology, under the period heading "Jan-Apr 58": "7 FEB. Advanced Research Projects Agency
(ARPA) established in DOD, Roy W. Johnson of General Electric named director, responsible for
US space program, including missiles and anti-missiles." The same chronology's 1961 entries
give "17 JAN. Dr. Jack P. Ruina succeeds Brig. Gen. Austin W. Betts as director of Advanced
Research Projects Agency (in DOD)" and "9 Mar. Dr. Harold Brown succeeds Dr. Herbert C. York
as Deputy Director, Research and Engineering (DOD)", which puts York outside the ARPA
directorship from a second source.

**A third, at one remove.** The CIA index card of 15 January 1958 quotes the *U.S. Government
Organization Manual, 1958-59*: the Advanced Research Projects Agency was "established by DOD
Directive 5105.15, dated February 7, 1958" to "direct and perform advanced research and
development projects in the fields of space science and technology, ballistic missile
defense, and other advanced research and development as assigned by the Secretary of
Defense", with "Roy W. Johnson, Director". The card's OCR renders the year once as 1956 and
the archive's own metadata transcription of the same card gives 1958; the two agree on the
day and month. The date 1958 is taken from the ARPA history, which gives it three times.

**McElroy's own words, before the name existed.** Testifying on 20 November 1957 to the House
Appropriations Subcommittee on Defense Appropriations, "The Ballistic Missile Program",
Hearings, November 20-21, 1957, quoted at length in the ARPA history: "We plan to establish
in the Department of Defense a special agency to handle our satellite and space research and
development projects. Tentatively we are thinking of calling this ... the Special Projects
Agency of the Department of Defense." The history records that Representative Scrivner
objected to that name because it was confusable with the OSD Office of Special Operations
and with the Armed Forces Special Weapons Project, and that McElroy promised a better one.

### What the transcript claimed that these documents do NOT establish

The passage is Annie Jacobsen on the Danny Jones Podcast #228, 11 March 2024, at 2:00:47 to
2:06:12, as recorded in `dannyjones-corpus-34.md`.

| Claim | What the opened record does to it |
|---|---|
| ARPA was "created ~1956-57" | **Contradicted.** DoD Directive 5105.15 is dated 7 February 1958, given by the ARPA-commissioned history three times, by the CIA chronology's own 7 February 1958 entry, and by the Government Organization Manual as quoted on a CIA index card |
| "First director was Herb York" | **Contradicted.** The first Director was Roy W. Johnson, appointed 7 February 1958. York was ARPA's first Chief Scientist and became the first Director of Defense Research and Engineering |
| "after Von Braun's Nazi-colleague condition was refused" | **Nothing opened bears on it.** No record reached here discusses Wernher von Braun in connection with the ARPA directorship |
| Neil McElroy was "an advertising executive by background" | **Loosely supported.** The ARPA history calls him "An experienced corporate executive with a strong sales and public relations background" and "a novice in government" |
| McElroy's "January 1958 testimony on the reorganisation", as the triage row puts it | **The record found is earlier.** The testimony quoted in the ARPA history is of 20 November 1957 to the House Appropriations Subcommittee on Defense Appropriations. A January 1958 hearing was not opened |

**Note for the builder.** The `darpa` node currently carries a self-description, a 2026
budget line and the board's counterfactual argument, and no founding date, instrument or
officer. The three claims above are what closes that gap, and they belong on `darpa` as much
as on the person.

### Draft node

```json
{
  "id": "neil-h-mcelroy",
  "cls": "person",
  "label": "Neil H. McElroy",
  "status": "dead",
  "sub": "Secretary of Defense from 9 October 1957; issued DoD Directive 5105.15 establishing ARPA, 7 February 1958",
  "cluster": "legacy",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "date": "1958-02-07",
  "domains": ["d-research", "d-structure", "d-program"],
  "narrative": "The board's DARPA node argues a counterfactual about the agency and carries no founding record at all. This is that record and the officer behind it. McElroy was sworn in as Secretary of Defense on 9 October 1957, five days after Sputnik, and on 7 February 1958 issued DoD Directive 5105.15, which established the Advanced Research Projects Agency in the Office of the Secretary of Defense under the authority of the National Security Act of 1947 as amended and Reorganization Plan No. 6 of 1953. The agency's own commissioned history reproduces the directive in full and records that he took a personal hand in the founding and selected Roy W. Johnson as first Director. His public description of the plan predates the name: testifying on 20 November 1957 he called it the Special Projects Agency and was told the name was confusable with the Armed Forces Special Weapons Project.",
  "claims": [
    {
      "tier": 1,
      "text": "The founding instrument, reproduced in the agency's own commissioned history: 'In accordance with the provisions of the National Security Act of 1947, as amended, and Reorganization Plan No. 6 of 1953, there is established in the Office of the Secretary of Defense the Department of Defense Advanced Research Projects Agency.' The figure is captioned 'TEXT OF DOD DIRECTIVE NUMBER 5105.15, FEBRUARY 7, 1958 (Establishing ARPA)'. The scan is a poor one and renders ARPA as 'AREA' throughout; the readings given here are normalised from obvious OCR corruption.",
      "source": "The Advanced Research Projects Agency, 1958-1974, Richard J. Barber Associates, Inc., prepared for ARPA, Figure II-2, DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The mandate is open-ended by design. The Agency is responsible for 'the direction or performance of such advanced projects in the field of research and development as the Secretary of Defense shall, from time to time, designate by individual project or by category', and 'The Director of Advanced Research Projects shall report to the Secretary of Defense.' The directive is 'effective immediately'.",
      "source": "The Advanced Research Projects Agency, 1958-1974, Figure II-2, DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt"
    },
    {
      "tier": 1,
      "text": "A second agency's record dates the founding and names the first Director independently. The CIA Historical Staff Chronology, under Jan-Apr 58: '7 FEB. Advanced Research Projects Agency (ARPA) established in DOD, Roy W. Johnson of General Electric named director, responsible for US space program, including missiles and anti-missiles.'",
      "source": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, CIA-RDP85B00803R000200050003-5, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5"
    },
    {
      "tier": 1,
      "text": "He proposed the agency in public before it had its name. Testifying on 20 November 1957 to the House Appropriations Subcommittee on Defense Appropriations he said: 'We plan to establish in the Department of Defense a special agency to handle our satellite and space research and development projects. Tentatively we are thinking of calling this ... the Special Projects Agency of the Department of Defense.' The history records that a member objected to that name as confusable with the OSD Office of Special Operations and the Armed Forces Special Weapons Project.",
      "source": "House Appropriations Subcommittee on Defense Appropriations, 'The Ballistic Missile Program', Hearings, November 20-21, 1957, p. 25, quoted in The Advanced Research Projects Agency, 1958-1974, DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast #228, 11 March 2024, at 2:00:47, Annie Jacobsen said ARPA was created around 1956 to 1957 and that its first director was Herb York. The opened records contradict both: the directive is dated 7 February 1958 and Roy W. Johnson was appointed Director the same day, while Herbert York was ARPA's first Chief Scientist and was later elevated to first Director of Defense Research and Engineering.",
      "source": "Danny Jones Podcast #228, 11 March 2024, at 2:00:47 to 2:06:12; contradicted against The Advanced Research Projects Agency, 1958-1974, DTIC AD-A154 363, https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt"
    }
  ],
  "sources": [
    {"name": "The Advanced Research Projects Agency, 1958-1974, Richard J. Barber Associates, Inc., DTIC AD-A154 363", "url": "https://archive.org/download/DTIC_ADA154363/DTIC_ADA154363_djvu.txt", "date": "1975-12-01"},
    {"name": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, CIA-RDP85B00803R000200050003-5", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5", "date": "1970-06-01"},
    {"name": "CIA reading room document CIA-RDP85B00803R000100040092-9, Establishment of Advanced Research Projects Agency", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000100040092-9", "date": "1958-01-15"}
  ],
  "edges": [
    {"a": "neil-h-mcelroy", "b": "darpa", "type": "institutional", "claimTier": 1, "dateStart": "1958-02-07", "label": "Issued the directive that established ARPA", "note": "DoD Directive 5105.15 of 7 February 1958 established the Agency in the Office of the Secretary of Defense with its Director reporting to the Secretary. The board's DARPA node has carried no founding instrument until now."},
    {"a": "neil-h-mcelroy", "b": "dod", "type": "institutional", "claimTier": 1, "dateStart": "1957-10-09", "label": "Secretary of Defense", "note": "The ARPA history records him sworn in on 9 October 1957, five days after Sputnik, and describes him taking a personal hand in the agency's creation."},
    {"a": "neil-h-mcelroy", "b": "afswp", "type": "temporal", "claimTier": 1, "dateStart": "1957-11-20", "label": "Named AFSWP as the reason the new agency was renamed", "note": "The ARPA history's footnote records that Rep. Scrivner objected to 'Special Projects Agency' as confusable with the OSD Office of Special Operations and the Armed Forces Special Weapons Project, and that McElroy promised a better name. This is the documented reason ARPA is called ARPA."},
    {"a": "darpa", "b": "harry-s-truman", "type": "legislative", "claimTier": 1, "dateStart": "1958-02-07", "label": "Founded under the authority of the 1947 Act", "note": "The directive's establishment clause cites the National Security Act of 1947 as amended, together with Reorganization Plan No. 6 of 1953."}
  ]
}
```

---

## 6. Glenn T. Seaborg as AEC chairman

**VERDICT: PARTLY CONFIRMED.** The appointment and two dated instances of him in office
were opened. **No record opened here gives an end date for the chairmanship**, so the
triage row's "1961 to 1971" is attested at its start and not at its end.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-cia-rdp85b00803r000200050003-5/cia-rdp85b00803r000200050003-5_djvu.txt | The CIA Historical Staff Chronology 1946-65, Volume II 1956-65. Under the period heading "Jan 61": "16 JAN. Dr. Glenn T. Seaborg named AEC chairman, succeeding John A. McCone (confirmed by Senate 24 Feb)." |
| https://archive.org/metadata/cia-readingroom-document-cia-rdp80b01676r002800020014-7 | CIA reading room document CIA-RDP80B01676R002800020014-7, dated 20 March 1963, on "UNITED STATES ATOMIC ENERGY COMMISSION, WASHINGTON 25, D.C." letterhead, signed "Glenn T. Seaborg, Chairman", addressed to "Honorable John A. McCone, Director, Central Intelligence Agency". Retrieved through archive.org's metadata API, whose description field carries the item's full transcribed text |
| https://archive.org/metadata/cia-readingroom-document-cia-rdp80b01676r000700150004-7 | CIA reading room document CIA-RDP80B01676R000700150004-7, dated 25 October 1961, a letter from "Allen W. Dulles, Director" addressed to "The Honorable Glenn T. Seaborg, Chairman, Atomic Energy Commission, Washington 25, D.C." |
| An AEC annual report to Congress itself | **NOT OPENED.** An archive.org title search for the series returned one bookseller listing with no text; a full-text search on Seaborg plus the annual report returned only the CIA correspondence above. The 1963 letter names and describes the 1962 report, which is not the same as opening it |
| A record of the end of the chairmanship | **NOT OPENED.** Full-text searches on "succeeding Seaborg" and on Seaborg with Schlesinger and the Commission returned nothing bearing on it |

### What the documents establish

**The appointment, dated twice.** The CIA's own declassified chronology gives 16 January
1961 for the naming and 24 February 1961 for Senate confirmation, and records the
predecessor: John A. McCone. That is a structural fact this board should carry on its own
account, because McCone went on to be Director of Central Intelligence, and the 1963 letter
below is Seaborg writing to him in that second office.

**Him in the office, in his own hand, on the Commission's letterhead.** The letter of 20
March 1963: "It is with pleasure that I forward to you a copy of the Commission's Annual
Report to Congress for 1962." It then walks the report's five parts, and the passage worth
a claim is the one that points a Director of Central Intelligence at the fallout appendix:
"In connection with the Military Applications section, you may find Appendix
15--Environmental Contamination from Nuclear Explosives--of interest, since it concerns
fallout data obtained from recent nuclear detonations." Part Three is described as covering
"the three major areas of activity related to the Commission's national defense mission",
with radioactive-waste management included "because of their close relationship to our
nuclear materials production program".

**A second dated instance, from the other direction.** On 25 October 1961 the Director of
Central Intelligence, Allen W. Dulles, wrote to "The Honorable Glenn T. Seaborg, Chairman,
Atomic Energy Commission", thanking him for a letter of 19 October giving his impression of
a conference in Vienna and saying "I am showing your good report to a few of our interested
people."

### What the transcript claimed that these documents do NOT establish

The passage is Jeremy Rys on the Danny Jones Podcast #181, "Explosive New Bob Lazar
Evidence & Area 51 Secrets Revealed", 16 April 2023, at 3:24 to 4:16.

| Claim | What the opened record does to it |
|---|---|
| Seaborg predicted the "island of stability" for superheavy elements, published in *Scientific American* May 1969, cited against Lazar's element 115 | **NOT OPENED.** The magazine issue was not reached. The lead map's own internal inconsistency (May 1989 in one row, 1969 in another) is therefore unresolved, and a node must not pick one |
| The triage row's "AEC chairmanship, 1961 to 1971" | **Half attested.** 16 January 1961 named, 24 February 1961 confirmed, in office on 25 October 1961 and on 20 March 1963. The end of the chairmanship is not attested by anything opened here |

### Draft node

```json
{
  "id": "glenn-t-seaborg",
  "cls": "person",
  "label": "Glenn T. Seaborg",
  "status": "dead",
  "sub": "Chairman, United States Atomic Energy Commission, named 16 January 1961, confirmed 24 February 1961",
  "cluster": "legacy",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "date": "1961-01-16",
  "domains": ["d-nuclear", "d-secrecy", "d-structure"],
  "narrative": "The board's own framing calls the programme's security apparatus one taken from the Manhattan Project and the Atomic Energy Commission, and it has never named a single AEC chairman. Seaborg is the one the corpus reaches, and the records that name him in the office also carry the structural fact the board should want: the CIA's declassified chronology records him named AEC chairman on 16 January 1961 succeeding John A. McCone, and McCone became Director of Central Intelligence, so two years later Seaborg is writing on Commission letterhead to the same man at CIA. That 20 March 1963 letter transmits the Commission's Annual Report to Congress for 1962 and points the DCI at its fallout appendix. The end of the chairmanship is not established by any record opened for this pass and is left off this node deliberately.",
  "claims": [
    {
      "tier": 1,
      "text": "The CIA's own declassified chronology dates the appointment and its confirmation: '16 JAN. Dr. Glenn T. Seaborg named AEC chairman, succeeding John A. McCone (confirmed by Senate 24 Feb).' The entry sits under the volume's period heading for January 1961.",
      "source": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, June 1970, CIA-RDP85B00803R000200050003-5, declassified in part 8 July 2013, https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5"
    },
    {
      "tier": 1,
      "text": "He is in the office on Commission letterhead in 1963, writing to the man he succeeded at the AEC, now at CIA: 'It is with pleasure that I forward to you a copy of the Commission's Annual Report to Congress for 1962', signed 'Glenn T. Seaborg, Chairman', addressed to 'Honorable John A. McCone, Director, Central Intelligence Agency'.",
      "source": "CIA reading room document CIA-RDP80B01676R002800020014-7, 20 March 1963, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r002800020014-7"
    },
    {
      "tier": 1,
      "text": "The same letter points the Director of Central Intelligence at the report's fallout material: 'In connection with the Military Applications section, you may find Appendix 15--Environmental Contamination from Nuclear Explosives--of interest, since it concerns fallout data obtained from recent nuclear detonations.'",
      "source": "CIA reading room document CIA-RDP80B01676R002800020014-7, 20 March 1963, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r002800020014-7"
    },
    {
      "tier": 1,
      "text": "A second, earlier instance of the office runs the other way. On 25 October 1961 the Director of Central Intelligence wrote to 'The Honorable Glenn T. Seaborg, Chairman, Atomic Energy Commission', thanking him for his impressions of a conference in Vienna and saying 'I am showing your good report to a few of our interested people.' It is signed 'Allen W. Dulles, Director'.",
      "source": "CIA reading room document CIA-RDP80B01676R000700150004-7, 25 October 1961, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r000700150004-7"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast #181, 16 April 2023, at 3:24, Jeremy Rys cited Seaborg's island-of-stability prediction for superheavy elements against the claim that Bob Lazar predicted element 115. The publication he names was not opened for this node, and the lead map for that episode gives its date inconsistently as May 1969 in one row and May 1989 in another. Nothing here resolves it.",
      "source": "Danny Jones Podcast #181, 'Explosive New Bob Lazar Evidence & Area 51 Secrets Revealed', 16 April 2023, at 3:24 to 4:16"
    }
  ],
  "unverified": [
    "The end of the chairmanship. The triage row gives 1961 to 1971 and no record opened for this pass gives an end date. An AEC annual report to Congress was not opened either; the 1963 letter names and describes the 1962 report but is not that report."
  ],
  "sources": [
    {"name": "CIA Historical Staff Chronology 1946-65, Volume II 1956-65, CIA-RDP85B00803R000200050003-5", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp85b00803r000200050003-5", "date": "1970-06-01"},
    {"name": "Letter to John A. McCone from Glenn T. Seaborg, CIA-RDP80B01676R002800020014-7", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r002800020014-7", "date": "1963-03-20"},
    {"name": "Letter to Glenn T. Seaborg from Allen W. Dulles, CIA-RDP80B01676R000700150004-7", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r000700150004-7", "date": "1961-10-25"}
  ],
  "edges": [
    {"a": "glenn-t-seaborg", "b": "atomic-energy-commission", "type": "institutional", "claimTier": 1, "dateStart": "1961-01-16", "label": "Chairman of the Commission", "note": "Named 16 January 1961 and confirmed by the Senate on 24 February 1961 per the CIA's own chronology; in office on Commission letterhead in October 1961 and March 1963. No end date is attested by any record opened here."},
    {"a": "glenn-t-seaborg", "b": "cia", "type": "institutional", "claimTier": 1, "dateStart": "1963-03-20", "label": "Transmitted the Commission's annual report to the Director of Central Intelligence", "note": "The 20 March 1963 letter forwards the Annual Report to Congress for 1962 to DCI John A. McCone and directs his attention to the appendix on environmental contamination from nuclear explosives."},
    {"a": "glenn-t-seaborg", "b": "allen-w-dulles", "type": "institutional", "claimTier": 1, "dateStart": "1961-10-25", "label": "Corresponded with the Director of Central Intelligence", "note": "Dulles thanks him for a report on a Vienna conference and says he is circulating it inside the Agency. The edge records a documented channel between the AEC chair and the DCI, which is the board's own structural claim in miniature."}
  ]
}
```

---

## What was tried and did not reach

| Target | Route tried | Result |
|---|---|---|
| DoD Directive 5105.15, the issuing office's own PDF | `esd.whs.mil/Portals/54/Documents/DD/issuances/dodd/510515p.pdf` and the `cancelled/` path, by curl with and without a browser user agent, and by WebFetch | HTTP 403 in every case. **NOT OPENED.** The directive's text was reached instead through the ARPA-commissioned history at DTIC, which reproduces it |
| An AEC annual report to Congress | archive.org title search and full-text search on the series | One bookseller listing with no text. **NOT OPENED** |
| The end of Seaborg's AEC chairmanship | archive.org full-text searches on "succeeding Seaborg" and on Seaborg with Schlesinger and the Commission | Nothing bearing on it. **NOT OPENED** |
| The body of the Cabell letter to Keyhoe | archive.org download of `0000015305_djvu.txt`, plus the item metadata | The scan's OCR is close to unusable. Signature and title readable against the catalogue entry; no sentence of the body legible. **PARTLY OPENED** |
| The UK Flying Saucer Working Party and Sir Henry Tizard | Not attempted in this pass | **NOT OPENED**, and named here so the next pass knows it is still open |
| Scientific American, the Seaborg island-of-stability article | Not attempted; the lead map gives two different years for it | **NOT OPENED** |
