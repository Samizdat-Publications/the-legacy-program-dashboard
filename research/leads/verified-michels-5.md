# Verified leads: Michels corpus candidates, section A rows 1 to 5 (verifier 5)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over rows 1
to 5 of section A of `research/leads/michels-triage-6.md`, against
`research/leads/VERIFY-BRIEF-2026-09-02.md`.

**Verified 2 September 2026.** Every URL below was opened by this session and returned the
document described. Where a document is a scan, what is quoted was read from the page
image rendered at high zoom, not from the OCR layer, wherever the OCR was poor enough to
matter; that is stated per document. `CLAUDE.md` section 2 governs: nothing here is
asserted that was not opened.

**Board state, read from `data/the-program.json` by this session rather than taken from
the triage file.** `McMahon` 0 occurrences. `Allen Dulles` 0, `Dulles` 0. `Bedell Smith` 1.
`NICAP` **73**, not the 156 the triage row states; `National Investigations Committee` 0.
`Office of Strategic Services` 1; `OSS` as a whole word 0 (the 40 raw hits are substrings).
`Chadwell` 23 and there is already an `h-marshall-chadwell` node, which the triage row for
candidate 3 does not mention. `Robertson Panel` 112. `Townsend Brown` 11. No node exists
for any of the five.

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 1 | Atomic Energy Act of 1946 (McMahon Act) | CONFIRMED; the popular name is NOT OPENED and the Condon-drafting claim is not established | new node |
| 2 | Harry Turner and the 1971 Australian JIO memorandum | **NOT OPENED** | no node |
| 3 | Walter Bedell Smith and Allen Dulles | CONFIRMED as people and offices; **the transcript's "1953 Bedell Smith letter" is CONTRADICTED in date, in authorship and in content** | two new nodes |
| 4 | NICAP | CONFIRMED, including Townsend Brown by name; the DC incorporation instrument itself NOT OPENED | new node |
| 5 | Office of Strategic Services | CONFIRMED as an institution; **the Brown personnel-file test was run and came back negative**, with a limit that matters | new node |

**The five findings that matter, in order:**

1. **The Brown OSS test is runnable and it fails.** NARA publishes the name database it
   compiled from the original folders of the OSS personnel-file series, 23,978 names. It
   contains `Brown Thomas G` and `Brown Thomas K` and no other Thomas Brown, no
   `Brown Thomas T`, and no `Townsend` as a Brown forename. It contains
   `Donovan William J`. Two maps say OSS sent Townsend Brown into Germany; the index of
   the series does not carry him.
2. **But that negative has a demonstrable hole, and the hole is Allen Dulles.** NARA's own
   2008 press release names Allen Dulles as one of the notable OSS personnel files being
   opened. The same name database lists `Dulles Clover T` and no Allen Dulles. A name's
   absence from this list is therefore evidence, not proof, and any node must say so.
3. **The "1953 Bedell Smith letter proposing psychological warfare" is three things at
   once and none of them is what the transcript says.** The psychological-warfare framing
   is Chadwell's, in a memorandum **to** the DCI dated **2 October 1952**, on which the
   released copy's approval line over Smith's name is **blank and undated**. Smith's own
   text, in the 2 December 1952 package, recommends a research programme and says nothing
   about exploiting the phenomenon. The date, the author and the content are all wrong in
   the transcript.
4. **Allen Dulles's UFO letters exist, are signed, and are the opposite of a psy-war
   proposal.** Three letters of 13 March 1953, classified SECRET, forward the Robertson
   Panel report to the Secretary of Defense, the Federal Civil Defense Administration and
   the National Security Resources Board, each saying "this Agency does not consider
   problems arising from sightings of 'flying saucers' primarily its concern". Each also
   states that the panel "was convened at the direction of General Smith", which is the
   Agency's own attribution of the Robertson Panel to Bedell Smith and the single most
   useful sentence found in this pass.
5. **NICAP names Townsend Brown in full, in an FBI-filed newspaper record, and states its
   own incorporation.** The FBI's NICAP file opens with a 23 October 1956 Washington Daily
   News clipping: "T. Townsend Brown of Leesburg, Va., who runs it, identified himself as
   executive vice chairman pro tempore." The CIA's own copy of *The UFO Evidence* states
   "NICAP is a non-profit organization incorporated in the District of Columbia (1956)."

**Reach notes for the next session.** `recordsearch.naa.gov.au` cannot be driven by curl at
all: every request lands on `SessionTimeout.aspx`, and a cookie jar does not help. It **can**
be driven from the browser pane by posting the guest-session `__doPostBack` and then
replaying the ASP.NET form, which is how the searches in section 2 were run; the results
page is reached through a self-submitting interstitial, so a single POST returns only
"Your search is running". `www.naa.gov.au` itself times out. `hansard.parliament.uk` is
behind Cloudflare and returned 403 to both curl and WebFetch on 2 September 2026, contrary
to the brief's list. `uscode.house.gov` hangs without responding. `api.govinfo.gov/search`
was already over its `DEMO_KEY` rate limit when this pass began, so no full-text search of
govinfo was possible; direct `content/pkg/<packageId>/pdf/` downloads have no such limit.
`corponline.dcra.dc.gov`, the District of Columbia corporate register, returns 522.
`catalog.archives.gov` serves an SPA shell to curl but its `/proxy/records/search` endpoint
answers JSON from inside the page context. The archive.org mirror of the CIA reading room
is the whole reason candidate 3 could be done: the collection is `ciareadingroom`, 973,512
items, and `archive.org/advancedsearch.php` matches against the OCR text, so a query like
`collection:ciareadingroom AND "unidentified flying" AND "Allen W. Dulles"` finds documents
by their content. Item files are named by the bare document id, not by the identifier
prefix: `archive.org/download/cia-readingroom-document-0005515935/0005515935.pdf`.

---

## 1. Atomic Energy Act of 1946 (McMahon Act)

**VERDICT: CONFIRMED.** The statute was opened in the Statutes at Large and read section by
section. Its short title, its born-secret information regime, its capital penalties, its
Military Liaison Committee, its FBI gate and its Joint Committee were all read in the text.
**Two things the triage row implies were not established:** the popular name "McMahon Act"
appears in no federal record opened here, and nothing opened supports map 30's claim
(D6, 02 / 0:06:46) that Condon helped draft it.

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf | Statutes at Large volume 60 from page 755. **Chapter 724**, **S. 1717**, **Public Law 585**, 79th Congress, "AN ACT For the development and control of atomic energy", approved **August 1, 1946**. Running head "79th CONG., 2d SESS.--CH. 724--AUG. 1, 1946". Scan with a text layer, extracted with `pdftotext -layout`; the section quoted below was located against the running heads and marginal captions. |
| https://www.govinfo.gov/content/pkg/CPRT-87JPRT80013/pdf/CPRT-87JPRT80013.pdf | Joint Committee Print, GPO 80013, February 1962, "Membership, Publications, and Other Pertinent Information of the Joint Committee on Atomic Energy, Congress of the United States, Through the 87th Congress, 1st Session". Section II is the membership of the committee 1945-61. |
| https://www.govinfo.gov/content/pkg/CREC-1994-05-23/html/CREC-1994-05-23-pt1-PgH37.htm | Congressional Record, House, 23 May 1994, debate on H.R. 3724, designating the Bridgeport courthouse the Brien McMahon Federal Building. |
| https://www.govinfo.gov/content/pkg/FR-2010-01-05/pdf/E9-31418.pdf | Federal Register, 5 January 2010, Executive Order 13526, Classified National Security Information. Section 6.2(a) is on the page reached. |

### What the documents establish

**The short title, and only that title.** Section 21: "This Act may be cited as the
'Atomic Energy Act of 1946'." The phrase "McMahon Act" does not appear in the statute and
was not found in any federal document opened in this pass.

**Born secret, defined by category.** Section 10(a): "It shall be the policy of the
Commission to control the dissemination of restricted data in such a manner as to assure
the common defense and security." Section 10(b)(1) then defines restricted data as "all
data concerning the manufacture or utilization of atomic weapons, the production of
fissionable material, or the use of fissionable material in the production of power, but
shall not include any data which the Commission from time to time determines may be
published without adversely affecting the common defense and security." Classification is
the default state of a category of fact; declassification is an affirmative act. That is
the mechanism the board already argues from the 1954 Act, in the instrument that created
it eight years earlier and a year before the programme's own 1947 start.

**The penalty is death.** Section 10(b)(2)(A), and again at (3) and at (4), each provide
that the offender "shall be punished by death or imprisonment for life (but the penalty of
death or imprisonment for life may be imposed only upon recommendation of the jury and only
in cases where the offense was committed with intent to injure the United States); or by a
fine of not more than $20,000 or imprisonment for not more than twenty years, or both."
Subsection (4) reaches the person who "removes, conceals, tampers with, alters, mutilates,
or destroys" such a document. Section 10(b)(5)(A) makes prosecution impossible without the
Attorney General, who must first advise the Commission, and section 10(b)(5)(C) provides:
"All violations of this Act shall be investigated by the Federal Bureau of Investigation of
the Department of Justice."

**The FBI gate on contractor access.** Section 10(b)(5)(B)(i): no arrangement, contract or
licence may be made unless the contractor "agrees in writing not to permit any individual
to have access to restricted data until the Federal Bureau of Investigation shall have made
an investigation and report to the Commission on the character, associations, and loyalty
of such individual and the Commission shall have determined that permitting such person to
have access to restricted data will not endanger the common defense or security."

**A military committee with a channel to the President.** Section 2(c) establishes the
Military Liaison Committee of War and Navy representatives, and directs that "The Commission
shall advise and consult with the Committee on all atomic energy matters which the
Committee deems to relate to military applications, including the development, manufacture,
use, and storage of bombs, the allocation of fissionable material for military research, and
the control of information relating to the manufacture or utilization of atomic weapons."
If the Committee concludes the Commission has acted adversely to the War or Navy
Departments, it may refer the matter to those Secretaries, and if either concurs he may
refer it to the President, "whose decision shall be final."

**Weapons production runs on an annual presidential permission.** Section 6(a) authorises
the Commission to "engage in the production of atomic bombs, atomic bomb parts, or other
military weapons utilizing fissionable materials", "except that such activities shall be
carried on only to the extent that the express consent and direction of the President of the
United States has been obtained, which consent and direction shall be obtained at least once
each year."

**A single congressional committee owns the subject.** Section 15(a) establishes the Joint
Committee on Atomic Energy, nine Senators and nine Representatives, "In each instance not
more than five members shall be members of the same political party", and section 15(b)
directs that "All bills, resolutions, and other matters in the Senate or the House of
Representatives relating primarily to the Commission or to the development, use, or control
of atomic energy shall be referred to the joint committee."

**Where McMahon actually is in the record.** The 1962 Joint Committee print lists, under
"MEMBERSHIP OF THE JOINT COMMITTEE, 1945-61", the "SENATE SPECIAL COMMITTEE ON ATOMIC
ENERGY, Seventy-ninth Congress (1945-46), BRIEN McMAHON, Connecticut, Chairman", and then
the "JOINT COMMITTEE ON ATOMIC ENERGY, Seventy-ninth Congress (1946), BRIEN McMAHON,
Connecticut, Chairman". Its note records the vacancy "created by the death of Brien McMahon,
on July 28, 1952". The 1994 House debate records that McMahon "served as the first chairman
of the Joint Committee on Atomic Energy" and "played a key role in authoring legislation
supporting our Nation's atomic weapons program". None of these documents calls the Act the
McMahon Act.

**The line to the present.** EO 13526 section 6.2(a): "Nothing in this order shall supersede
any requirement made by or under the Atomic Energy Act of 1954, as amended, or the National
Security Act of 1947, as amended. 'Restricted Data' and 'Formerly Restricted Data' shall be
handled, protected, classified, downgraded, and declassified in conformity with the
provisions of the Atomic Energy Act of 1954, as amended, and regulations issued under that
Act." Note the section number: the board should cite **6.2(a)**, not 6.2(b), and note that
the order names the **1954** successor, not the 1946 original.

### What the transcript claimed that this document does NOT establish

| Claim | Where | Adjudication |
|---|---|---|
| "McMahon Atomic Secrecy Act of 1946" | map 30, D6, 02 / 0:06:46 | The statutory short title is "Atomic Energy Act of 1946". There is no "Atomic Secrecy Act". The popular name attaching it to McMahon is not in any record opened here; his chairmanship of both the Senate Special Committee and the Joint Committee in the 79th Congress is documented, which is the fact behind the name |
| Condon helped draft it | map 30, D6 | Nothing opened here names Condon anywhere in the statute or the committee print. Not established; do not carry |
| The 1946 Act is the predecessor of the 1954 Act | map 30, D5 and D6 | True on the face of both statutes, and the board already carries the 1954 regime at 45 occurrences. What is new is the origin instrument and its date |
| Presidential declassification authority does not reach Restricted Data | board prose, per the triage row | Supported, but by EO 13526 section 6.2(a) and by reference to the **1954** Act. The 1946 Act is where the category was invented, not where the modern carve-out is written |

### Draft node

```json
{
  "id": "atomic-energy-act-1946",
  "cls": "legislation",
  "label": "Atomic Energy Act of 1946 (McMahon Act)",
  "cluster": "oversight",
  "sub": "Public Law 79-585, 60 Stat. 755, 1 August 1946; the origin of born-secret classification",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "date": "1946-08-01",
  "desc": "The Atomic Energy Act of 1946 is where classification by category enters United States law. It defines restricted data as an entire class of fact rather than as a set of documents somebody decided to mark, makes publication conditional on an affirmative determination by the Atomic Energy Commission, and backs the rule with a capital penalty that reaches concealment and destruction as well as disclosure. It gates every contractor employee's access behind an FBI investigation and a Commission finding, gives the FBI exclusive jurisdiction over violations, and gives the War and Navy Departments a standing consultative claim over the control of weapons information through the Military Liaison Committee, with an appeal that ends at the President. The board argues the 1954 Act's Restricted Data regime is the statutory shield; this is the instrument that built it, a year before the programme's own 1947 start.",
  "claims": [
    {
      "tier": 1,
      "text": "The Act's own short title is narrow: 'This Act may be cited as the \"Atomic Energy Act of 1946\".' The chapter head gives it as Chapter 724, S. 1717, Public Law 585, 79th Congress, 'AN ACT For the development and control of atomic energy', approved August 1, 1946. The popular name 'McMahon Act' appears nowhere in the statute.",
      "source": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755, sec. 21 and chapter head, https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "Classification runs by category, and publication is the exception. Section 10(b)(1): restricted data 'means all data concerning the manufacture or utilization of atomic weapons, the production of fissionable material, or the use of fissionable material in the production of power, but shall not include any data which the Commission from time to time determines may be published without adversely affecting the common defense and security.' Section 10(a) makes it 'the policy of the Commission to control the dissemination of restricted data in such a manner as to assure the common defense and security.'",
      "source": "Atomic Energy Act of 1946, sec. 10(a) and 10(b)(1), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "The penalty reaches concealment and destruction, not only disclosure, and it is capital. Section 10(b)(4) provides that whoever 'removes, conceals, tampers with, alters, mutilates, or destroys' a document incorporating restricted data with intent to injure the United States 'shall be punished by death or imprisonment for life (but the penalty of death or imprisonment for life may be imposed only upon recommendation of the jury and only in cases where the offense was committed with intent to injure the United States); or by a fine of not more than $20,000 or imprisonment for not more than twenty years, or both.'",
      "source": "Atomic Energy Act of 1946, sec. 10(b)(4), and identically at 10(b)(2)(A) and 10(b)(3), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "The FBI is both the gate and the investigator. Section 10(b)(5)(B)(i) bars any arrangement, contract or licence unless the contractor 'agrees in writing not to permit any individual to have access to restricted data until the Federal Bureau of Investigation shall have made an investigation and report to the Commission on the character, associations, and loyalty of such individual.' Section 10(b)(5)(C): 'All violations of this Act shall be investigated by the Federal Bureau of Investigation of the Department of Justice.'",
      "source": "Atomic Energy Act of 1946, sec. 10(b)(5)(B)(i) and 10(b)(5)(C), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "The military keeps a standing claim over the control of weapons information, with an appeal that ends at the President. Section 2(c) directs that the Commission 'shall advise and consult with the Committee on all atomic energy matters which the Committee deems to relate to military applications, including the development, manufacture, use, and storage of bombs, the allocation of fissionable material for military research, and the control of information relating to the manufacture or utilization of atomic weapons', and provides that where either Secretary concurs in a Military Liaison Committee objection he 'may refer the matter to the President, whose decision shall be final.'",
      "source": "Atomic Energy Act of 1946, sec. 2(c), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    }
  ],
  "sources": [
    { "name": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755 (Ch. 724, S. 1717)", "url": "https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf", "date": "1946-08-01" },
    { "name": "Membership, Publications, and Other Pertinent Information of the Joint Committee on Atomic Energy, Joint Committee Print, February 1962 (GPO 80013)", "url": "https://www.govinfo.gov/content/pkg/CPRT-87JPRT80013/pdf/CPRT-87JPRT80013.pdf", "date": "1962-02-01" },
    { "name": "Congressional Record, House, 23 May 1994, H.R. 3724 (Brien McMahon Federal Building)", "url": "https://www.govinfo.gov/content/pkg/CREC-1994-05-23/html/CREC-1994-05-23-pt1-PgH37.htm", "date": "1994-05-23" },
    { "name": "Executive Order 13526, Classified National Security Information, 75 FR 707", "url": "https://www.govinfo.gov/content/pkg/FR-2010-01-05/pdf/E9-31418.pdf", "date": "2009-12-29" }
  ],
  "edges": [
    {
      "a": "atomic-energy-act-1946",
      "b": "atomic-energy-commission",
      "type": "legislative",
      "claimTier": 1,
      "label": "The instrument that created the Commission",
      "note": "Section 2(a) of this Act establishes the Atomic Energy Commission and section 10 gives it the born-secret regime the Commission then ran for twenty-eight years.",
      "sources": [{ "name": "Atomic Energy Act of 1946, secs. 2(a) and 10", "url": "https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf", "date": "1946-08-01" }]
    },
    {
      "a": "atomic-energy-act-1946",
      "b": "manhattan-project-2",
      "type": "custody",
      "claimTier": 1,
      "label": "Statutory transfer of the Manhattan Engineer District's holdings and its cleared people",
      "note": "Section 9(a) directs the transfer of all fissionable material, all atomic weapons and parts and all processes and technical information, and section 10(b)(5)(B)(iii) lets anyone the Manhattan Engineer District had already cleared keep access pending the new investigation.",
      "sources": [{ "name": "Atomic Energy Act of 1946, secs. 9(a) and 10(b)(5)(B)(iii)", "url": "https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf", "date": "1946-08-01" }]
    },
    {
      "a": "atomic-energy-act-1946",
      "b": "eo-13526",
      "type": "legislative",
      "claimTier": 1,
      "label": "The category this Act invented is the one the executive order cannot reach",
      "note": "EO 13526 sec. 6.2(a) provides that nothing in the order supersedes any requirement made by or under the Atomic Energy Act of 1954 and that Restricted Data is handled and declassified only under that Act; the 1954 statute carried the category forward from this one.",
      "sources": [{ "name": "Executive Order 13526, sec. 6.2(a)", "url": "https://www.govinfo.gov/content/pkg/FR-2010-01-05/pdf/E9-31418.pdf", "date": "2009-12-29" }]
    }
  ]
}
```

**Note on the first edge.** `atomic-energy-commission` does not exist on the board as of
this pass. It is the draft node in `research/leads/verified-michels-1.md` section 1. If that
node is not merged, this edge must be dropped rather than repointed.

---

## 2. Harry Turner and the 1971 Australian Joint Intelligence Organisation memorandum

**VERDICT: NOT OPENED.** The memorandum was not found. Below is exactly what was searched
and where the record would be if it exists.

### What was tried

RecordSearch, the National Archives of Australia's public catalogue, was reached at
`https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/SearchScreens/BasicSearch.aspx`
and at `.../AdvSearchItems.aspx`, in a guest session opened from the browser pane. Seven
item-level searches were run. `www.naa.gov.au` itself timed out on every attempt and its
research guides could not be read.

| Search | Scope | Result |
|---|---|---|
| keyword "unidentified flying object" | all series, all dates | 23 items. The UFO series is **A9755**, plus `A10907`, `A1945` |
| series **A9755**, all items | all dates | **23 items, 1967 to 1994**, every one a RAAF Unusual Aerial Sightings file (Support Command, 82 Bomber Wing Amberley, 86 Wing Richmond, 92 Wing Edinburgh, Pearce, Williamtown, AF Intelligence and Security Canberra). No Joint Intelligence Organisation item, no 1971 item |
| keyword "flying saucer" | all series | 51 items, all copyright registrations, ABC broadcast material, a 1952 Eastern Area Headquarters sighting report and a 1971 photograph of an inventor's concept sketch |
| keyword "unusual aerial sightings", title and notes, 1965 to 1980 | all series | 6 items: `BP990/1` 5/113/AIR parts 1 and 2, `J63` 5/40/AIR part 3, `A9755` items 2 and 4, and `M1148` "Unidentified Flying Objects (UFOs)", 1970 to 1972, Melbourne, which contains "Department of Air : unusual aerial sightings : summary 3, January 1970-December 1971". That is the closest item found to the claimed date and it is a Department of Air summary, not a JIO memorandum |
| keyword "UFO", title and notes, 1968 to 1975 | all series | 18 items, none from Defence intelligence |
| keyword "Joint Intelligence Organisation", title and notes, 1968 to 1976 | all series | **168 items**, in `AWM282`, `A1851`, `A12381`, `A8913`, `A1838`, `AWM122`, `A452`, `A750`, `A4531`. Vietnam country briefs, Office of Current Intelligence weekly reports, the 1976 Royal Commission on Intelligence and Security hearings, records-disposal policy. **Nothing on aerial phenomena** |
| keyword "Harry Turner", title and notes | all series | 270 items, all of them false positives on the two names separately (enlistment records, passenger manifests, a Cape Turner map mosaic). RecordSearch does not index memorandum authorship |

### What this means, stated precisely

RecordSearch describes **items**, which are usually whole files. A memorandum inside a file
is not indexed, so a negative result here is not a finding that the memorandum does not
exist. What it is: the 1971 JIO memorandum is **not an item in its own right** in any NAA
series reachable by these searches, and it is not in `A9755`, which is the series a
researcher would go to first. No digitised copy was found and no item in the result sets
was flagged as digitised.

**Where a next pass should look.** The Department of Defence and JIO series listed above,
by physical inspection or a NAA reference enquiry rather than by catalogue search;
`M1148`, whose item detail page could not be rendered from here because RecordSearch item
detail requires search-result session state; and the Royal Commission into British Nuclear
Tests in Australia (1985), which was not searched at all in this pass and which the triage
row names for the Montebello, Maralinga and Emu Field half of the claim.

**No node.** Nothing about Harry Turner, the memorandum, the Joint Intelligence
Organisation's nuclear division, the six US academic gravity centres, or the Twining
quotation is carried forward. All of it remains where the triage put it.

---

## 3. Walter Bedell Smith, and Allen Dulles

**VERDICT: CONFIRMED** for both men, their offices and their documented action on this
subject. **The transcript's specific claim is CONTRADICTED.** Map 30 D11 gives "CIA
Director Walter Bedell Smith's 1953 letter" proposing "using the UFO phenomenon for
psychological warfare against the USSR", and D12 gives "Allen Dulles letters" described as
"similar". S12 makes both of them Michels' best evidence against a total-fabrication
theory. What the released CIA file actually contains is set out below, and the date, the
author and the content of D11 are each wrong.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/cia-readingroom-document-0005515933 | CIA document **C00015339**, date stamp **OCT 2 1952**. "MEMORANDUM TO: Director of Central Intelligence / THROUGH: Deputy Director (Intelligence) / FROM: Assistant Director, Office of Scientific Intelligence / SUBJECT: Flying Saucers". Signed H. Marshall Chadwell. Seven pages including TAB A. Page images rendered from `0005515933.pdf` at 5x and 6x and read directly; the OCR layer is poor and was not relied on for any quotation |
| https://archive.org/details/cia-readingroom-document-0005515935 | CIA document **C00015340**, date stamp **DEC 2 1952**, "Approved for Release 2/2010". "MEMORANDUM FOR: Director of Central Intelligence / THRU: Deputy Director for Intelligence / SUBJECT: Unidentified Flying Objects", signed H. MARSHALL CHADWELL, Assistant Director, Scientific Intelligence. Four pages: the memorandum, a verso, a draft memorandum for the Executive Secretary of the NSC over Smith's name, and a draft NSC directive. Read from rendered page images at 2.6x and 7x |
| https://archive.org/details/cia-readingroom-document-0000015454 | **IAC-D-67, 18 February 1953**, "INTELLIGENCE ADVISORY COMMITTEE / UNIDENTIFIED FLYING OBJECTS", signed JAMES Q. REBER, Secretary, transmitting the Robertson Panel report at Tab A with a summary of evidence at Tab B and the participant list at Tab C. Released 6 October 1978. OCR text |
| https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9 | **CIA-RDP80B01676R001000160043-9**, SECRET / Security Information, CIA Office of the Director letterhead, "REWRITTEN 13 March 1953". Letter to "The Honorable The Secretary of Defense", signed **Allen W. Dulles, Director**. One page, rendered at 2.4x and read directly |
| https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160044-8 | The same letter to "The Honorable Jack Gorrie, Vice Chairman, National Security Resources Board", same date, same signature block, with a note to the Executive Registry that an earlier draft "was not sent out, but was rewritten as of 13 March 1953" |
| https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160045-7 | The same letter to "The Honorable J. J. Wadsworth, Acting Administrator, Federal Civil Defense Administration", same date, same signature block, same Executive Registry note |
| https://archive.org/details/cia-readingroom-document-0005516214 | FBI memorandum, **December 5, 1952**, TO: Mr. A. H. Belmont, FROM: V. P. Keay, SUBJECT: "PROPOSED STUDY ON THE 'FLYING SAUCERS' PHENOMENA; INTELLIGENCE ADVISORY COMMITTEE", reporting that a Liaison Section supervisor attended the IAC meeting of December 4, 1952 |

### What the documents establish

**Smith is named as the approving authority on the psychological-warfare memorandum, and
the released copy is unsigned.** The 2 October 1952 memorandum's conclusion reads:
"'Flying saucers' pose two elements of danger which have national security implications.
The first involves mass psychological considerations and the second concerns the
vulnerability of the United States to air attack." Its recommended action (b) is "That the
DCI discuss this subject with the Psychological Strategy Board. A memorandum to the
Director, Psychological Strategy Board, is attached for signature as TAB C." TAB A, the
supporting study, asks whether the sightings "could be used from a psychological warfare
point of view, either offensively or defensively", and says that public concern "indicates
that a fair proportion of our population is mentally conditioned to the acceptance of the
incredible. In this fact lies the potential for the touching-off of mass hysteria and
panic." The routing page carries "CONCURRENCES: ... LOFTUS E. BECKER, Deputy
Director/Intelligence" and then "ACTION BY APPROVING AUTHORITY: Date: ______ Approved
(disapproved): ______ WALTER B. SMITH, Director". **Both the date line and the approval
line are blank on the released copy.**

**Smith personally started the whole thing, on 20 August 1952.** The 2 December 1952
memorandum opens: "On 20 August, the DCI, after a briefing by OSI on the above subject,
directed the preparation of an NSCID for submission to the Council stating the need for
investigation and directing agencies concerned to cooperate in such investigations."

**What Chadwell told the DCI in December.** Paragraph 4: "At this time, the reports of
incidents convince us that there is something going on that must have immediate attention.
The details of some of these incidents have been discussed by AD/SI with DDCI. Sightings of
unexplained objects at great altitudes and travelling at high speeds in the vicinity of
major U.S. defense installations are of such nature that they are not attributable to
natural phenomena or known types of aerial vehicles." Paragraph 5 announces that OSI "is
proceeding to the establishment of a consulting group of sufficient competence and stature
to review this matter", which is the Robertson Panel.

**Smith's own words, and they are not a psy-war proposal.** The draft memorandum attached
at paragraph 6, addressed "MEMORANDUM TO: The Executive Secretary, National Security
Council", subject "Unidentified Flying Objects (Flying Saucers)", over the typed signature
block "Walter B. Smith / Director", says at paragraph 2: "It is my view that this situation
has possible implications for our national security which transcend the interests of a
single service. A broader, coordinated effort should be initiated to develop a firm
scientific understanding of the several phenomena which apparently are involved in these
reports, and to assure ourselves that the incidents will not hamper our present efforts in
the Cold War or confuse our early warning system in case of an attack." Paragraph 3
recommends that CIA and the Department of Defense "be directed to formulate and carry out a
program of intelligence and research activities required to solve the problem of instant
positive identification of unidentified flying objects." The proposal is research, and the
concern is friendly-force confusion rather than offensive use. Paragraph 1 gives a count of
official reports received since 1947 and a percentage still unexplained; **the numeral is
degraded in the scan and is not quoted here**, and no node should carry it from this pass.

**The draft directive was abandoned, and the panel is why.** IAC-D-67, paragraph 3: "The
results of the panel's studies have moved CIA to conclude that no National Security Council
Directive on this subject is warranted." Paragraph 2 proposes transmitting the report "to
the Secretary of Defense; the Director, Federal Civil Defense Administration; and the
Chairman, National Security Resources Board". Paragraph 1 records that the panel was
convened "as a result of the action taken by the Intelligence Advisory Committee on 4
December". The FBI's own memorandum of 5 December 1952 independently records a Bureau
observer at that 4 December IAC meeting and the suggestion there "which would call for a
group of scientists to make a study of the new 'saucers' data in an effort to identify the
phenomena".

**Dulles executed exactly that transmission, and attributed the panel to Smith.** All three
13 March 1953 letters, to the three addressees IAC-D-67 named, read: "I am forwarding you
herewith a copy of a report prepared by a panel of scientists on the subject of
'Unidentified Flying Objects.' This panel was convened at the direction of General Smith,
following the recommendation of the Intelligence Advisory Committee." Each continues: "It
seems to me that the conclusions and recommendations may be of interest to you, in that
they point out certain potential dangers to national security which are related to the
subject and suggest ways of their elimination." Each then says: "Although this Agency does
not consider problems arising from sightings of 'flying saucers' primarily its concern, we
shall be pleased to assist in any appropriate action that you deem advisable."

### What the transcript claimed that these documents do NOT establish

| Claim | Where | Adjudication |
|---|---|---|
| A **1953** letter | map 30, D11 | **CONTRADICTED.** The psychological-warfare document is dated 2 October 1952 and the Smith-signed draft is dated 2 December 1952. Smith left the DCI post in early 1953 and Dulles's letters of 13 March 1953 are signed by Dulles, not Smith |
| **Written by** Bedell Smith | map 30, D11 | **CONTRADICTED.** Both 1952 memoranda are written by H. Marshall Chadwell, Assistant Director for Scientific Intelligence, and addressed to the DCI. Smith appears as the addressee, as the named approving authority on an approval line that the released copy leaves blank, and as the typed signature block on a draft prepared for him |
| Proposing to **use the UFO phenomenon for psychological warfare against the Soviets** | map 30, D11 and S12 | **PARTLY, and the attribution is wrong.** The offensive-or-defensive psychological-warfare question is asked in Chadwell's TAB A of 2 October 1952 and the recommended action is that the DCI take the subject to the Psychological Strategy Board. Smith's own attached text proposes a research programme and says nothing about exploiting the phenomenon against the USSR |
| Allen Dulles wrote "similar letters" | map 30, D12 | **PARTLY CONFIRMED, and the content cuts the other way.** Three Dulles letters of 13 March 1953 exist and were opened. They transmit the Robertson Panel report and state that the Agency does not consider flying saucer sightings primarily its concern. That is a distancing letter, not a proposal to exploit anything |
| The "exploit, don't fabricate" argument | map 30, S12 | The underlying point survives, but on different paper. The Agency's own 1952 documents treat the reports as describing something real enough to need immediate attention and a scientific panel. They do not treat it as invented. That is a Tier 1 fact about the documents, and it is worth more to the board than the misattributed letter |
| Paul Mellon saw a German disc in a Czechoslovak hangar with Dulles present | maps 31 and 32, and triage B13 | Nothing bearing on this was found in the CIA reading room mirror. Not opened, not carried |
| Dulles's published diary shows "meeting with the president" on the date of an Eisenhower MJ-12 briefing | map 33, D8, 02 / 2:23:44 | Not opened. The Dulles papers at Princeton's Seeley G. Mudd Manuscript Library were not reachable from this environment and no date or page is given by the speaker in any case |

### Draft node A

```json
{
  "id": "walter-bedell-smith",
  "cls": "person",
  "label": "Walter Bedell Smith",
  "status": "dead",
  "date": "1952-12-02",
  "age": null,
  "loc": "Washington, DC",
  "locId": "l-dc",
  "instId": "cia",
  "sub": "Director of Central Intelligence; the DCI who ordered the UFO problem into the intelligence community",
  "cluster": "ic",
  "tier": "B",
  "C": 1,
  "A": 3,
  "D": 0,
  "narrative": "Walter Bedell Smith is the Director of Central Intelligence whose own instruction, on 20 August 1952, turned unidentified flying objects from an Air Force nuisance into an intelligence-community problem with a draft National Security Council directive behind it. Chadwell's memoranda run to him, name him as the approving authority on the recommendation that the DCI take the subject to the Psychological Strategy Board, and attach a memorandum to the NSC Executive Secretary over his signature block proposing a coordinated research programme. The Agency's own later correspondence states plainly that the Robertson Panel 'was convened at the direction of General Smith'. The board carries the Robertson Panel at 112 occurrences and has one occurrence of his name; he is the office from which it issued.",
  "affiliations": [
    "Central Intelligence Agency, Director of Central Intelligence"
  ],
  "claims": [
    {
      "tier": 1,
      "text": "Smith personally started the intelligence-community effort. Chadwell's 2 December 1952 memorandum to the DCI opens: 'On 20 August, the DCI, after a briefing by OSI on the above subject, directed the preparation of an NSCID for submission to the Council stating the need for investigation and directing agencies concerned to cooperate in such investigations.'",
      "source": "H. Marshall Chadwell, Memorandum for Director of Central Intelligence, subject: Unidentified Flying Objects, 2 December 1952, CIA document C00015340, para. 1, https://archive.org/details/cia-readingroom-document-0005515935"
    },
    {
      "tier": 1,
      "text": "A memorandum to the National Security Council was drafted over his name proposing research, not exploitation: 'It is my view that this situation has possible implications for our national security which transcend the interests of a single service. A broader, coordinated effort should be initiated to develop a firm scientific understanding of the several phenomena which apparently are involved in these reports, and to assure ourselves that the incidents will not hamper our present efforts in the Cold War or confuse our early warning system in case of an attack.' The typed signature block reads 'Walter B. Smith / Director'.",
      "source": "Draft Memorandum to the Executive Secretary, National Security Council, subject: Unidentified Flying Objects (Flying Saucers), attached to CIA document C00015340, 2 December 1952, para. 2, https://archive.org/details/cia-readingroom-document-0005515935"
    },
    {
      "tier": 1,
      "text": "He is named as the approving authority on the recommendation that the DCI take the subject to the Psychological Strategy Board, and on the released copy the approval was never recorded. The 2 October 1952 routing page reads 'ACTION BY APPROVING AUTHORITY: Date: ____ Approved (disapproved): ____ WALTER B. SMITH, Director'; both lines are blank. The recommendation itself is action (b): 'That the DCI discuss this subject with the Psychological Strategy Board. A memorandum to the Director, Psychological Strategy Board, is attached for signature as TAB C.'",
      "source": "H. Marshall Chadwell, Memorandum to Director of Central Intelligence, subject: Flying Saucers, 2 October 1952, CIA document C00015339, para. 4 and routing page, https://archive.org/details/cia-readingroom-document-0005515933"
    },
    {
      "tier": 1,
      "text": "The CIA attributed the Robertson Panel to him in writing. Allen W. Dulles, transmitting the panel report on 13 March 1953: 'This panel was convened at the direction of General Smith, following the recommendation of the Intelligence Advisory Committee.'",
      "source": "Allen W. Dulles to the Secretary of Defense, 13 March 1953, SECRET, CIA-RDP80B01676R001000160043-9, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9"
    }
  ],
  "sources": [
    { "name": "Chadwell memorandum to the DCI, subject: Flying Saucers, 2 October 1952 (CIA C00015339)", "url": "https://archive.org/details/cia-readingroom-document-0005515933", "date": "1952-10-02" },
    { "name": "Chadwell memorandum for the DCI, subject: Unidentified Flying Objects, 2 December 1952, with draft NSC memorandum and draft NSC directive (CIA C00015340)", "url": "https://archive.org/details/cia-readingroom-document-0005515935", "date": "1952-12-02" },
    { "name": "IAC-D-67, Intelligence Advisory Committee: Unidentified Flying Objects, 18 February 1953", "url": "https://archive.org/details/cia-readingroom-document-0000015454", "date": "1953-02-18" },
    { "name": "Allen W. Dulles to the Secretary of Defense, 13 March 1953 (CIA-RDP80B01676R001000160043-9)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9", "date": "1953-03-13" }
  ],
  "edges": [
    {
      "a": "walter-bedell-smith",
      "b": "robertson-panel",
      "type": "programmatic",
      "claimTier": 1,
      "label": "Convened at his direction",
      "note": "All three of Dulles's 13 March 1953 transmittal letters state that the panel 'was convened at the direction of General Smith, following the recommendation of the Intelligence Advisory Committee'.",
      "sources": [{ "name": "Allen W. Dulles to the Secretary of Defense, 13 March 1953", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9", "date": "1953-03-13" }]
    },
    {
      "a": "h-marshall-chadwell",
      "b": "walter-bedell-smith",
      "type": "institutional",
      "claimTier": 1,
      "label": "Chadwell's UFO memoranda were addressed to him and named him as approving authority",
      "note": "Both the 2 October and 2 December 1952 memoranda are addressed to the Director of Central Intelligence through the Deputy Director for Intelligence, and the October routing page names Walter B. Smith as the approving authority on the Psychological Strategy Board recommendation.",
      "sources": [{ "name": "CIA documents C00015339 and C00015340", "url": "https://archive.org/details/cia-readingroom-document-0005515933", "date": "1952-10-02" }]
    },
    {
      "a": "walter-bedell-smith",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "Director of Central Intelligence",
      "note": "He signs as 'Director' on CIA Office of the Director paper and is addressed as Director of Central Intelligence in the Office of Scientific Intelligence memoranda of October and December 1952.",
      "sources": [{ "name": "CIA document C00015340, draft memorandum to the NSC Executive Secretary", "url": "https://archive.org/details/cia-readingroom-document-0005515935", "date": "1952-12-02" }]
    },
    {
      "a": "walter-bedell-smith",
      "b": "washington-flap-1952",
      "type": "temporal",
      "claimTier": 1,
      "label": "His 20 August 1952 instruction follows the summer 1952 reporting wave",
      "note": "The DCI's direction to prepare an NSC intelligence directive is dated 20 August 1952 in Chadwell's own account, weeks after the Washington sightings, and Chadwell's October study rests on the reporting volume of that summer.",
      "sources": [{ "name": "CIA document C00015340, para. 1", "url": "https://archive.org/details/cia-readingroom-document-0005515935", "date": "1952-12-02" }]
    }
  ]
}
```

### Draft node B

```json
{
  "id": "allen-w-dulles",
  "cls": "person",
  "label": "Allen W. Dulles",
  "status": "dead",
  "date": "1953-03-13",
  "age": null,
  "loc": "Washington, DC",
  "locId": "l-dc",
  "instId": "cia",
  "sub": "Director of Central Intelligence; signed the CIA's distancing letters on the Robertson Panel report",
  "cluster": "ic",
  "tier": "B",
  "C": 1,
  "A": 3,
  "D": 1,
  "narrative": "Allen W. Dulles signed the three letters that closed the Agency's 1952 flying-saucer file. On 13 March 1953, over his name and on Office of the Director paper classified SECRET, the CIA sent the Robertson Panel report to the Secretary of Defense, to the Federal Civil Defense Administration and to the National Security Resources Board, told each that the conclusions pointed to 'certain potential dangers to national security', and then said in the same letter that the Agency did not consider the subject primarily its concern. Those three letters do two things the board needs: they attribute the panel to Bedell Smith in the Agency's own words, and they are a dated, signed instance of the Agency stepping back from a subject it had itself convened a panel on ten weeks earlier. Dulles also has an OSS personnel file, named by the National Archives among the notable files opened in 2008.",
  "affiliations": [
    "Central Intelligence Agency, Director of Central Intelligence",
    "Office of Strategic Services (personnel file, RG 226)"
  ],
  "claims": [
    {
      "tier": 1,
      "text": "On 13 March 1953 Dulles forwarded the Robertson Panel report to three agencies over his own signature, describing it as pointing out 'certain potential dangers to national security which are related to the subject and suggest ways of their elimination.' The three addressees are the Secretary of Defense, the Acting Administrator of the Federal Civil Defense Administration and the Vice Chairman of the National Security Resources Board, which are exactly the three IAC-D-67 had proposed on 18 February 1953.",
      "source": "Allen W. Dulles, three letters of 13 March 1953, CIA-RDP80B01676R001000160043-9, -044-8 and -045-7, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9"
    },
    {
      "tier": 1,
      "text": "The same letters distance the Agency from the subject in the same breath: 'Although this Agency does not consider problems arising from sightings of \"flying saucers\" primarily its concern, we shall be pleased to assist in any appropriate action that you deem advisable.'",
      "source": "Allen W. Dulles to the Secretary of Defense, 13 March 1953, SECRET / Security Information, CIA-RDP80B01676R001000160043-9, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9"
    },
    {
      "tier": 1,
      "text": "The letters attribute the Robertson Panel to his predecessor by name: 'This panel was convened at the direction of General Smith, following the recommendation of the Intelligence Advisory Committee.'",
      "source": "Allen W. Dulles to Jack Gorrie, National Security Resources Board, 13 March 1953, CIA-RDP80B01676R001000160044-8, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160044-8"
    },
    {
      "tier": 1,
      "text": "Each of the three letters is a rewrite of an earlier version that was withdrawn. A note to the Executive Registry filed with two of them reads: 'Please note that the attached letter ... was not sent out, but was rewritten as of 13 March 1953 (copy attached).' The letters themselves carry the stamp 'REWRITTEN 13 March 1953'.",
      "source": "Executive Registry notes filed with CIA-RDP80B01676R001000160044-8 and -045-7, https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160045-7"
    },
    {
      "tier": 1,
      "text": "The National Archives names Dulles among the OSS personnel files opened on 14 August 2008: the press office distributed CDs including 'selected files of some of the notable people who served in the OSS, including former CIA directors Allen Dulles and William Casey'.",
      "source": "National Archives media alert 08-130, 'NARA to Open Official Personnel Files of the OSS', 7 August 2008, https://www.archives.gov/press/press-releases/2008/nr08-130"
    }
  ],
  "sources": [
    { "name": "Allen W. Dulles to the Secretary of Defense, 13 March 1953 (CIA-RDP80B01676R001000160043-9)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9", "date": "1953-03-13" },
    { "name": "Allen W. Dulles to Jack Gorrie, National Security Resources Board, 13 March 1953 (CIA-RDP80B01676R001000160044-8)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160044-8", "date": "1953-03-13" },
    { "name": "Allen W. Dulles to J. J. Wadsworth, Federal Civil Defense Administration, 13 March 1953 (CIA-RDP80B01676R001000160045-7)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160045-7", "date": "1953-03-13" },
    { "name": "IAC-D-67, Intelligence Advisory Committee: Unidentified Flying Objects, 18 February 1953", "url": "https://archive.org/details/cia-readingroom-document-0000015454", "date": "1953-02-18" },
    { "name": "National Archives media alert 08-130", "url": "https://www.archives.gov/press/press-releases/2008/nr08-130", "date": "2008-08-07" }
  ],
  "edges": [
    {
      "a": "allen-w-dulles",
      "b": "robertson-panel",
      "type": "denial",
      "claimTier": 1,
      "label": "Forwarded the panel report while saying the subject was not primarily CIA's concern",
      "note": "The same signed letter that calls the panel's conclusions a matter of potential danger to national security states that the Agency does not consider flying saucer sightings primarily its concern, ten weeks after CIA convened the panel.",
      "sources": [{ "name": "Allen W. Dulles to the Secretary of Defense, 13 March 1953", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9", "date": "1953-03-13" }]
    },
    {
      "a": "allen-w-dulles",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "Director of Central Intelligence, signing as Director on Office of the Director paper",
      "note": "All three 13 March 1953 letters are on Central Intelligence Agency, Office of the Director letterhead and are signed 'Allen W. Dulles, Director'.",
      "sources": [{ "name": "CIA-RDP80B01676R001000160043-9", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160043-9", "date": "1953-03-13" }]
    },
    {
      "a": "allen-w-dulles",
      "b": "walter-bedell-smith",
      "type": "institutional",
      "claimTier": 1,
      "label": "Succeeded him as DCI and attributed the panel to him in writing",
      "note": "Dulles's own letters name General Smith as the officer at whose direction the panel was convened, which is the Agency's contemporaneous account of the handover of the file.",
      "sources": [{ "name": "CIA-RDP80B01676R001000160044-8", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80b01676r001000160044-8", "date": "1953-03-13" }]
    },
    {
      "a": "allen-w-dulles",
      "b": "office-of-strategic-services",
      "type": "institutional",
      "claimTier": 1,
      "label": "Has an OSS personnel file in RG 226",
      "note": "The National Archives names Dulles among the notable OSS personnel files distributed to the press at the 14 August 2008 opening of the series.",
      "sources": [{ "name": "National Archives media alert 08-130", "url": "https://www.archives.gov/press/press-releases/2008/nr08-130", "date": "2008-08-07" }]
    }
  ]
}
```

**Note on the last edge.** `office-of-strategic-services` is the draft node in section 5
below and does not exist on the board. Drop the edge if that node is not merged.
`walter-bedell-smith` is the draft node in section 3A above and is subject to the same
condition in reverse.

---

## 4. National Investigations Committee on Aerial Phenomena (NICAP)

**VERDICT: CONFIRMED.** Both halves the triage row asked for were opened, one of them in a
better form than the row anticipated. The 1964 volume was read in the CIA's own filed copy.
The incorporation is stated by NICAP itself in that volume, and the organisation's formation
under Townsend Brown is documented in the FBI's own NICAP file, with Brown named in full.
**The DC corporate instrument itself was NOT OPENED**; the District's register returns 522.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0 | **CIA-RDP81R00560R000100010001-0**, "Approved For Release 2001/04/02". The CIA's filed copy of ***The UFO Evidence***, published by the National Investigations Committee on Aerial Phenomena, Washington, D.C., **1964**. Title page: "1536 Connecticut Ave., N. W., Washington 36, D. C. / Richard H. Hall Editor / Washington D. C. / May 1964". Copyright notice: "Copyright 1964, National Investigations Committee on Aerial Phenomena." 1.1 MB of OCR text, read in full-text |
| https://archive.org/details/NICAP | The FBI's file on the National Investigations Committee on Aerial Phenomena, three parts, mirrored by the National Security Archive. Bureau file **100-35992**. Part 01 page 2 was rendered at 2.2x from `...(NICAP) 01.pdf` and read directly rather than through OCR |
| https://corponline.dcra.dc.gov/ | The District of Columbia corporate register. Returns **522** on every path tried, including `/Account.aspx/LogOn`. Redirects to `boss.dc.gov`, which does not carry corporate filings. **NOT OPENED** |

### What the documents establish

**The incorporation, in NICAP's own words.** Under the heading "NICAP and its Policies":
"NICAP is a non-profit organization incorporated in the District of Columbia (1956). Our
main goals and purposes are scientific investigation and research of reported unidentified
flying objects, and encouragement of full reporting to the public by responsible authorities
of all information which the government has accumulated on this subject."

**The charge against the Air Force is in the same paragraph.** "The U.S. Air Force is
charged with the official investigation of UFOs, but has practiced an intolerable degree of
secrecy keeping the public in the dark about the amount and possible significance of UFO
evidence. Therefore, we have urged Congressional hearings to help clarify the evidence and
encourage a full scientific review, with the public being kept fully informed."

**Townsend Brown, by name, running it at formation.** The FBI's file opens with a clipping
from **The Washington Daily News, Tuesday, October 23** [1956], headed "'Project Skylight' /
New Group Setting Sights on Saucers", by Jim G. Lucas, Scripps-Howard Staff Writer. The FBI
routing slip is dated 10-23-56 and the file stamps read "NOT RECORDED 191 OCT 29 956" and
"50 NOV 1 1956". The clipping reads: "The brass plate at 1536 Connecticut-av nw reads
'National Investigations Committee on Aerial Phenomena.' Inside they refer to it as Project
Skylight. **T. Townsend Brown of Leesburg, Va., who runs it, identified himself as executive
vice chairman pro tempore. He formerly was a consulting physicist for the Clevite-Brush
Electronics Co. of Cleveland, O.**" It continues: "National Investigations Committee ... is
just now forming. On Nov. 1 it meets to elect a nine-man board of governors", that Brown
"is representing a group of approximately 75 'scientists, educators and church leaders'",
that he "expects to be around until Nov. 15, when he goes back to London as research
director for Whitehall-Rand", and that the committee "will be a 'privately supported
fact-finding body serving the national public interest.' It has applied to the Treasury for
tax-exempt status."

**Hillenkoetter's tenure, stated by NICAP.** "Vice Admiral R. H. Hillenkoetter, USN (Ret.),
a long-time acquaintance of Major Keyhoe, also served on the NICAP Board of Governors for
five years. His service as a former Director of the Central Intelligence Agency (CIA),
coupled with a distinguished Naval record in war and peace, cause his statements about UFOs
to be of unusual interest." The volume adds that "In 1961, Adm. Hillenkoetter joined with a
majority of the NICAP Board in urging a Congressional investigation of the UFO problem."

**The submission to Congress is stated twice.** "Copies of this report have been sent to all
Members of Congress. If you agree that the UFO subject ought to be probed by Congress,
letters to your own Congressman or Senators would help to bring about action." And of the
1962 preview issue: "Copies were sent to all Members of Congress", followed by reproduced
replies from Representatives including a photostat of a 4 November 1960 letter from
"Congress of the United States, House of Representatives, Office of the Majority Leader",
John W. McCormack.

**Who was on the board in 1964.** Maj. Donald E. Keyhoe, USMC (Ret.), Director; Richard H.
Hall, Acting Director. The Board of Governors includes J. B. Hartranft Jr. (President,
Aircraft Owners and Pilots Association), Col. J. Bryan III, USAFR (Ret.), "Former special
assistant to Secretary of Air Force (1952-53)", Rear Adm. H. B. Knowles, USN (Ret.), and
"Mr. Dewey Fournet, Jr., former Major USAFR ... Former Air Force Headquarters Monitor of AF
Project Blue Book UFO investigation, prepared analyses of UFO data for AF, liaison officer
between Dayton project and Pentagon."

**The FBI's own characterisation.** A Bureau memorandum in part 3 records: "We do have a
record of the National Investigations Committee on Aerial Phenomena (100-35992-41). It has
been described as a 'non-profit, privately supported, fact finding body serving the National
Public interest which offers memberships and publications giving authentic sighting reports
and up-to-date developments about "Unidentified Flying Objects".' This information was
furnished to a Special Agent of our Washington Field Office in May, 1961, by Mr. Richard H.
Hall, Secretary of the organization."

### What the transcript claimed that these documents do NOT establish

| Claim | Where | Adjudication |
|---|---|---|
| Townsend Brown founded NICAP | maps 30 and 32, and triage C2 | **CONFIRMED in the strongest available form.** The contemporaneous newspaper record in the FBI's own file names him in full, gives his title as executive vice chairman pro tempore, and says he ran it. The word "founder" is not used; "who runs it" and the fact that the board of governors had not yet been elected are what the record says |
| "NICAP appears 156 times in board prose" | triage A4 | **CONTRADICTED.** The count in `data/the-program.json` read by this session is **73**. The promotion is still right; the arithmetic is not |
| Hillenkoetter on the NICAP board with Brown as founder | map 32, 1:10:49 | Both halves are documented separately and the overlap is not. Brown ran it in October 1956; Hillenkoetter served five years on the board and the volume does not date the start. Do not draw an edge asserting they served together |
| Carter reported a 1969 sighting to NICAP | map 33, f01 §1e, and triage B17 | Not opened. Nothing in the 1964 volume can bear on 1969, and the report form itself was not sought in this pass |

### Draft node

```json
{
  "id": "nicap",
  "cls": "institution",
  "label": "National Investigations Committee on Aerial Phenomena (NICAP)",
  "cluster": "media",
  "sub": "Civilian UFO body incorporated in the District of Columbia, 1956; 1536 Connecticut Avenue NW",
  "tier": "B",
  "C": 1,
  "A": 3,
  "D": 1,
  "dateStart": "1956",
  "desc": "NICAP is the civilian organisation the board narrates constantly and has never named as an entity. It was forming at 1536 Connecticut Avenue NW in October 1956 under Thomas Townsend Brown, who told a Scripps-Howard reporter he was executive vice chairman pro tempore and that the group would elect its nine-man board of governors on 1 November; the clipping is in the FBI's own file on the organisation. By 1964 it was directed by Maj. Donald E. Keyhoe with Richard H. Hall as acting director and editor, carried a former Director of Central Intelligence and a former Blue Book headquarters monitor on its board, and published The UFO Evidence, which it sent to every Member of Congress and which the CIA filed. It is the exact official-and-civilian boundary the board argues about: a private body, staffed at the top by people who had held the government's own positions, campaigning for the hearings the government did not hold.",
  "claims": [
    {
      "tier": 1,
      "text": "NICAP states its own legal form and year: 'NICAP is a non-profit organization incorporated in the District of Columbia (1956).' The same paragraph gives its purpose as 'scientific investigation and research of reported unidentified flying objects, and encouragement of full reporting to the public by responsible authorities of all information which the government has accumulated on this subject.'",
      "source": "The UFO Evidence, National Investigations Committee on Aerial Phenomena, Washington DC, May 1964, Richard H. Hall ed., section 'NICAP and its Policies', in the CIA's filed copy CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "Thomas Townsend Brown ran the organisation at its formation. A Washington Daily News report of Tuesday 23 October 1956, filed in the FBI's NICAP file: 'The brass plate at 1536 Connecticut-av nw reads \"National Investigations Committee on Aerial Phenomena.\" Inside they refer to it as Project Skylight. T. Townsend Brown of Leesburg, Va., who runs it, identified himself as executive vice chairman pro tempore. He formerly was a consulting physicist for the Clevite-Brush Electronics Co. of Cleveland, O.' The same report says the committee 'is just now forming. On Nov. 1 it meets to elect a nine-man board of governors.'",
      "source": "Jim G. Lucas, 'Project Skylight: New Group Setting Sights on Saucers', The Washington Daily News, 23 October 1956, in FBI file 100-35992 on the National Investigations Committee on Aerial Phenomena, part 1, https://archive.org/details/NICAP"
    },
    {
      "tier": 1,
      "text": "A former Director of Central Intelligence sat on its board and joined its campaign for hearings. The 1964 volume: 'Vice Admiral R. H. Hillenkoetter, USN (Ret.), a long-time acquaintance of Major Keyhoe, also served on the NICAP Board of Governors for five years,' and 'In 1961, Adm. Hillenkoetter joined with a majority of the NICAP Board in urging a Congressional investigation of the UFO problem.'",
      "source": "The UFO Evidence, 1964, in CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "The volume was addressed to Congress and says so: 'Copies of this report have been sent to all Members of Congress.' Its board in 1964 also included 'Mr. Dewey Fournet, Jr., former Major USAFR ... Former Air Force Headquarters Monitor of AF Project Blue Book UFO investigation, prepared analyses of UFO data for AF, liaison officer between Dayton project and Pentagon.'",
      "source": "The UFO Evidence, 1964, in CIA-RDP81R00560R000100010001-0, https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0"
    },
    {
      "tier": 1,
      "text": "The FBI kept a file on it, numbered 100-35992, and recorded the organisation's self-description as given by its secretary: 'This information was furnished to a Special Agent of our Washington Field Office in May, 1961, by Mr. Richard H. Hall, Secretary of the organization.'",
      "source": "FBI file 100-35992 on the National Investigations Committee on Aerial Phenomena, part 3, https://archive.org/details/NICAP"
    }
  ],
  "sources": [
    { "name": "The UFO Evidence (NICAP, Washington DC, May 1964), Richard H. Hall ed., CIA filed copy CIA-RDP81R00560R000100010001-0", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" },
    { "name": "FBI file 100-35992, National Investigations Committee on Aerial Phenomena (3 parts)", "url": "https://archive.org/details/NICAP", "date": "1956-10-23" }
  ],
  "edges": [
    {
      "a": "thomas-townsend-brown",
      "b": "nicap",
      "type": "institutional",
      "claimTier": 1,
      "label": "Ran NICAP at its formation, October 1956, as executive vice chairman pro tempore",
      "note": "A Washington Daily News report of 23 October 1956, in the FBI's own NICAP file, names T. Townsend Brown of Leesburg, Virginia as the man who runs it and gives his title, with the board of governors still to be elected on 1 November.",
      "sources": [{ "name": "FBI file 100-35992, part 1, Washington Daily News clipping, 23 October 1956", "url": "https://archive.org/details/NICAP", "date": "1956-10-23" }]
    },
    {
      "a": "roscoe-hillenkoetter",
      "b": "nicap",
      "type": "institutional",
      "claimTier": 1,
      "label": "Served five years on the Board of Governors",
      "note": "NICAP's own 1964 volume states that Hillenkoetter served on its Board of Governors for five years and that in 1961 he joined a majority of the board in urging a Congressional investigation.",
      "sources": [{ "name": "The UFO Evidence, 1964", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    },
    {
      "a": "nicap",
      "b": "usaf",
      "type": "denial",
      "claimTier": 1,
      "label": "Charged the Air Force with an intolerable degree of secrecy, in print, to Congress",
      "note": "The 1964 volume states that the Air Force 'has practiced an intolerable degree of secrecy keeping the public in the dark about the amount and possible significance of UFO evidence', and that copies of the report were sent to all Members of Congress.",
      "sources": [{ "name": "The UFO Evidence, 1964", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    },
    {
      "a": "nicap",
      "b": "project-blue-book",
      "type": "institutional",
      "claimTier": 1,
      "label": "Blue Book's former headquarters monitor sat on the NICAP board",
      "note": "The 1964 board list describes Dewey Fournet Jr. as the former Air Force Headquarters monitor of Project Blue Book and liaison officer between the Dayton project and the Pentagon.",
      "sources": [{ "name": "The UFO Evidence, 1964", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    },
    {
      "a": "cia",
      "b": "nicap",
      "type": "investigative",
      "claimTier": 1,
      "label": "CIA held and filed NICAP's 1964 volume in its own records",
      "note": "The copy of The UFO Evidence read for this record is the Agency's, released as CIA-RDP81R00560R000100010001-0 and marked 'Approved For Release 2001/04/02'.",
      "sources": [{ "name": "CIA-RDP81R00560R000100010001-0", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp81r00560r000100010001-0", "date": "1964-05-01" }]
    }
  ]
}
```

---

## 5. Office of Strategic Services

**VERDICT: CONFIRMED** as an institution, from NARA's own guide and catalogue.
**The falsifiable test the triage row asked for was run.** The National Archives publishes
the name database it compiled from the original folders of the OSS personnel-file series.
It does not contain Thomas Townsend Brown. It does contain William J. Donovan. It also does
not contain Allen Dulles, whom NARA's own press release names as having a file, and that
omission is the reason the negative must be reported as evidence rather than as proof.

### What was opened

| URL | What is at it |
|---|---|
| https://www.archives.gov/research/guide-fed-records/groups/226.html | "Records of the Office of Strategic Services [OSS]", Record Group 226, 1919-49 (bulk 1941-46), Guide to Federal Records in the National Archives. Section 226.1 Administrative History; section 226.3.8 Records of the Civilian Personnel (CP) Branch |
| https://catalog.archives.gov/id/1593270 | National Archives Catalog, NAID **1593270**, series "Personnel Files of the Office of Strategic Services, 1942-ca. 1962", within RG 226. **23,735 File Units**, of which **7 File Units and 87 Items** are in the Catalog |
| https://www.archives.gov/iwg/declassified-records/rg-226-oss/personnel.html | NARA's Interagency Working Group page for RG 226 personnel records. Names the series as **Entry A1-224**, location 230/86/26/3, and links the name database and the folder lists for four further personnel entries |
| https://www.archives.gov/files/iwg/declassified-records/rg-226-oss/personnel-database.pdf | "OSS PERSONNEL FILES - RG 226 ENTRY 224", dated 12/23/2010, 522 pages, columns LAST NAME / FIRST NAME / M I / RANK or SERIAL / BOX / NOTES / LOCATION. **23,978 name rows**, counted programmatically |
| https://www.archives.gov/press/press-releases/2008/nr08-130 | NARA media alert 08-130, 7 August 2008, "NARA to Open Official Personnel Files of the OSS", for the opening on 14 August 2008 |

### What the documents establish

**Establishment and abolition.** From the Guide, section 226.1: "Established: Under the
Joint Chiefs of Staff (JCS) by Presidential military order, June 13, 1942." Predecessor
agency, the Office of the Coordinator of Information, 1941-42. "Abolished: Effective October
1, 1945, by EO 9621, September 20, 1945." Successors for the general intelligence functions:
Strategic Services Unit, Office of the Assistant Secretary of War (1945-46); Central
Intelligence Group, National Intelligence Authority (1946-47); Central Intelligence Agency,
National Security Council (1947-49).

**Custody of the personnel files ran OSS to SSU to CIG to CIA to NARA.** The catalogue
description of NAID 1593270: the records "were transferred to the Strategic Services Unit,
tasked with closing down the OSS, in October 1945 and maintained until October 1946 ... They
were transferred to the Central Intelligence Group in 1946 and maintained until September
1947. They were transferred to the Central Intelligence Agency who maintained them from
September 1947, until the records were transferred to the National Archives and Records
Administration."

**CIA destroyed pages before the transfer, and NARA says so.** From the IWG page: "The
personnel files were retained by the CIA after World War II as the successor agency to the
OSS. Prior to the transfer of the files to NARA, select pages were destroyed by the CIA that
they considered disposable or non-record."

**The name database, and what it is.** From the same page: "This series includes
approximately 23,978 OSS personnel names. NARA compiled the names in the accompanying
database list from the original record folders. NARA retained the separation of any medical
files and has not opened them for research." The catalogue records the series as arranged
"alphabetically by last name" and as **Partially Available in the Catalog**, with only 7
file units and 87 items described online, so a name search inside the catalogue itself is
not possible; the database PDF is the only online index.

**The scale of the 2008 opening.** From media alert 08-130: "The National Archives will open
more than 35,000 official personnel files of men and women who served in the Office of
Strategic Services (OSS) ... The 750,000 pages include initial applications to join the OSS;
preliminary training and subsequent work assignments; pay, leave and travel documents;
evaluations, basic medical information; and awards, decorations and discharge papers." The
opening date was Thursday 14 August 2008 at College Park.

### The Brown test, run and reported in full

The database was downloaded and searched. Results, exact:

| Search | Result |
|---|---|
| `^Brown ` | 106 rows |
| `^Brown +T` | **2 rows: `Brown Thomas G ... 86 230/86/28/01` and `Brown Thomas K ... 86 230/86/28/01`.** No row with middle initial T, none with the forename Townsend |
| `Townsend` anywhere in the file | 6 rows, all with Townsend as the **surname**: Campbell, James B, Jeannette R, Leo H, Milton E, Orlan W |
| `^Donovan +William` | 1 row: `Donovan William J ... 194 230/86/30/02` |
| `^Stephenson` | 5 rows, including `Stephenson William S ... 744 230/86/41/04` |
| `^Dulles` | 1 row: `Dulles Clover T ... 203 230/86/30/03` |

**The finding, stated with its limit.** The only online index to the OSS personnel-file
series does not list Thomas Townsend Brown. It does list the Director, William J. Donovan.
That is real evidence against the claim in maps 32 and 34 that OSS sent Brown into Germany
in 1944 or 1945. It is not proof, for one demonstrable reason: **NARA's own press release
names Allen Dulles among the notable OSS personnel files opened, and the database lists only
Clover T. Dulles.** A name can be in RG 226 and absent from this list. The IWG page names
four further personnel entries with their own folder lists (UD-WX 1569, UD-WX 1567, UD-WX
1583, UD-WX 1584) which were not searched in this pass, and the medical records at UD-WX
1578 are closed to research entirely.

**`Stephenson William S` is a name match and nothing more.** Both maps flag the British
figure in the Brown story as probably William Stephenson. A folder with that name and that
middle initial exists at box 744. Nothing opened here identifies the person in it. Record
the row; do not identify the man.

### What the transcript claimed that these documents do NOT establish

| Claim | Where | Adjudication |
|---|---|---|
| OSS and MI6 sent Townsend Brown into Germany in 1944 or 1945 to investigate Foo Fighters and German disc work | map 32, f2 0:53:54; map 34, f02 0:49:42 | **Not established, and the index runs against it.** No Thomas T. or Thomas Townsend Brown in the 23,978-name OSS personnel-file database. See the limit above before treating this as settled |
| William Stevenson or Stephenson, MI6, organised the mission | map 32, f2 §1e | Not established. A `Stephenson William S` folder exists in the OSS series; nothing opened connects it to the British Security Coordination figure or to Brown |
| "Wild Bill Donovan, OSS chief, co-organiser" | map 32, f2 §1e | Donovan's OSS personnel file exists, at box 194. Nothing opened connects him to Brown or to any such mission |

### Draft node

```json
{
  "id": "office-of-strategic-services",
  "cls": "institution",
  "label": "Office of Strategic Services (OSS)",
  "cluster": "ic",
  "sub": "US wartime intelligence agency, 13 June 1942 to 1 October 1945; direct ancestor of the CIA",
  "tier": "B",
  "C": 1,
  "A": 2,
  "D": 1,
  "dateStart": "1942-06-13",
  "dateEnd": "1945-10-01",
  "desc": "The Office of Strategic Services was established under the Joint Chiefs of Staff by presidential military order on 13 June 1942 and abolished by Executive Order 9621 effective 1 October 1945, its intelligence functions passing through the Strategic Services Unit and the Central Intelligence Group to the Central Intelligence Agency. Its personnel files followed the same chain and stayed with CIA until they reached the National Archives, and NARA records that the Agency destroyed selected pages before the transfer. The series was opened on 14 August 2008: more than 35,000 files and 750,000 pages. It matters to this board because it is the one place a load-bearing biographical claim about Thomas Townsend Brown can be tested against an index rather than against a recollection.",
  "claims": [
    {
      "tier": 1,
      "text": "Established 'Under the Joint Chiefs of Staff (JCS) by Presidential military order, June 13, 1942', with the Office of the Coordinator of Information (1941-42) as predecessor, and 'Abolished: Effective October 1, 1945, by EO 9621, September 20, 1945.' Its general intelligence functions passed to the Strategic Services Unit (1945-46), the Central Intelligence Group (1946-47) and then the Central Intelligence Agency.",
      "source": "Guide to Federal Records in the National Archives, Record Group 226, section 226.1, https://www.archives.gov/research/guide-fed-records/groups/226.html"
    },
    {
      "tier": 1,
      "text": "The personnel files stayed in intelligence custody for sixty years. NARA: the records 'were transferred to the Strategic Services Unit ... in October 1945', 'transferred to the Central Intelligence Group in 1946', and 'transferred to the Central Intelligence Agency who maintained them from September 1947, until the records were transferred to the National Archives and Records Administration.'",
      "source": "National Archives Catalog, NAID 1593270, 'Personnel Files of the Office of Strategic Services, 1942-ca. 1962', https://catalog.archives.gov/id/1593270"
    },
    {
      "tier": 1,
      "text": "The custodian culled the file before releasing it, and the archive says so: 'Prior to the transfer of the files to NARA, select pages were destroyed by the CIA that they considered disposable or non-record.'",
      "source": "National Archives, Records of the Office of Strategic Services (RG 226): Personnel, https://www.archives.gov/iwg/declassified-records/rg-226-oss/personnel.html"
    },
    {
      "tier": 1,
      "text": "The series was opened on 14 August 2008: 'more than 35,000 official personnel files of men and women who served in the Office of Strategic Services', comprising 750,000 pages. NARA compiled a name list from the original folders containing 'approximately 23,978 OSS personnel names', published as Entry 224 of RG 226.",
      "source": "National Archives media alert 08-130, 7 August 2008, https://www.archives.gov/press/press-releases/2008/nr08-130 ; National Archives, RG 226 personnel page, https://www.archives.gov/iwg/declassified-records/rg-226-oss/personnel.html"
    },
    {
      "tier": 1,
      "text": "The published name index does not list Thomas Townsend Brown. Searched in full, the 23,978-row database contains two Thomas Browns, 'Brown Thomas G' and 'Brown Thomas K', neither with the middle initial T, and no row giving Townsend as a forename. It does contain 'Donovan William J' at box 194. The index is not complete for the record group: NARA's own press release names Allen Dulles among the notable OSS personnel files opened, and the database lists only 'Dulles Clover T'.",
      "source": "OSS Personnel Files, RG 226 Entry 224, name database dated 23 December 2010, https://www.archives.gov/files/iwg/declassified-records/rg-226-oss/personnel-database.pdf ; National Archives media alert 08-130, https://www.archives.gov/press/press-releases/2008/nr08-130"
    }
  ],
  "sources": [
    { "name": "Guide to Federal Records in the National Archives, Record Group 226 (Office of Strategic Services)", "url": "https://www.archives.gov/research/guide-fed-records/groups/226.html", "date": "2026-09-02" },
    { "name": "National Archives Catalog, NAID 1593270, Personnel Files of the Office of Strategic Services, 1942-ca. 1962", "url": "https://catalog.archives.gov/id/1593270", "date": "2026-09-02" },
    { "name": "National Archives, Records of the Office of Strategic Services (RG 226): Personnel", "url": "https://www.archives.gov/iwg/declassified-records/rg-226-oss/personnel.html", "date": "2017-06-26" },
    { "name": "OSS Personnel Files, RG 226 Entry 224, name database (522 pp., 23 December 2010)", "url": "https://www.archives.gov/files/iwg/declassified-records/rg-226-oss/personnel-database.pdf", "date": "2010-12-23" },
    { "name": "National Archives media alert 08-130, NARA to Open Official Personnel Files of the OSS", "url": "https://www.archives.gov/press/press-releases/2008/nr08-130", "date": "2008-08-07" }
  ],
  "edges": [
    {
      "a": "office-of-strategic-services",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "Direct institutional ancestor, through SSU and CIG",
      "note": "NARA's guide names the successors of the OSS general intelligence functions as the Strategic Services Unit (1945-46), the Central Intelligence Group (1946-47) and then the Central Intelligence Agency, and the personnel files themselves followed that chain into CIA custody.",
      "sources": [{ "name": "Guide to Federal Records, RG 226, sec. 226.1; NAID 1593270", "url": "https://www.archives.gov/research/guide-fed-records/groups/226.html", "date": "2026-09-02" }]
    },
    {
      "a": "cia",
      "b": "office-of-strategic-services",
      "type": "custody",
      "claimTier": 1,
      "label": "Held the OSS personnel files until transfer and destroyed selected pages first",
      "note": "The National Archives states that the files were retained by CIA as successor agency and that 'select pages were destroyed by the CIA that they considered disposable or non-record' before the transfer.",
      "sources": [{ "name": "National Archives, RG 226 personnel page", "url": "https://www.archives.gov/iwg/declassified-records/rg-226-oss/personnel.html", "date": "2017-06-26" }]
    }
  ]
}
```

**An edge deliberately not drawn.** There is no `office-of-strategic-services` to
`thomas-townsend-brown` edge. The claim that OSS sent Brown into Germany is the thing this
node exists to test, the test came back negative, and a negative belongs in the node's
claims where its limits can travel with it, not in an edge whose existence would imply the
relationship it denies. If a later pass searches entries UD-WX 1569, 1567, 1583 and 1584 and
finds him, that is the moment to draw one.

---

## What is left, and for whom

| Open | Where it is |
|---|---|
| The 1971 Australian JIO memorandum | Not an item in any NAA series reachable by catalogue search. Needs a NAA reference enquiry or physical inspection of the Defence and JIO series, plus `M1148` (item 31415782) whose detail page could not be rendered from here |
| The Royal Commission into British Nuclear Tests in Australia (1985) | Not searched at all in this pass. It is the other half of the Turner row |
| The Dulles papers and published diary | Princeton's Seeley G. Mudd Manuscript Library was not reachable. Map 33's D8 claim about a diary entry has no date and no page and cannot be tested without them |
| The District of Columbia incorporation instrument for NICAP | `corponline.dcra.dc.gov` returns 522. NICAP's own statement of its 1956 DC incorporation is on the record; the filing is not |
| OSS personnel entries UD-WX 1569, 1567, 1583, 1584 | Folder lists are published at `archives.gov/iwg/declassified-records/rg-226-oss/personnel.html` and were not searched. They are where a Brown file would be if the Entry 224 negative is wrong |
| The numeral in Smith's draft NSC memorandum | The count of official reports received since 1947 is degraded in the scan of CIA C00015340 page 3 and was deliberately not quoted. A better scan, or the same document in another CREST copy, would settle it |
