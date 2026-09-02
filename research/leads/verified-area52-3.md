# Verified leads: Area 52 corpus candidates (verifier 3)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over five
rows of section A of `research/leads/area52-triage-2.md` (rows 3, 11, 12, 13 and 6),
against `research/leads/VERIFY-BRIEF-AREA52-2026-09-02.md`.

**Verified 2 September 2026.** Every URL below was opened by this session and returned the
document described. Where a document is a scan, the text quoted was read from the OCR layer
the archive itself publishes, and that is said where it applies. `CLAUDE.md` section 2
governs: nothing here is asserted that was not opened.

**Board state, read from `data/the-program.json` by this session, not taken from the triage
files.**

| grep | occurrences | node? |
|---|---|---|
| `Haynes` | 0 | the spelling in the triage row does not appear on the board at all |
| `Haines` | 96 | **two** document nodes for the same article: `haines-cia-history` and `cia-haines-1997` |
| `Foreign Technology Division` | 21, all prose | no node |
| `Scientific and Technical Intelligence` | 6, none about the USIB committee | no node |
| `Monroe` | 1, a source line on `l-kirtland` | no node |
| `Gateway` | 0 | no node |
| `Eric Walker` | 1, inside the `robert-sarbacher` adjudication | no node |

The RDB node's id is `research-development-board`, not `research-and-development-board` as
the triage row writes it. Anyone drafting that edge should use the id that exists.

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 1 | Gerald K. Haines, "CIA's Role in the Study of UFOs, 1947-90" | CONFIRMED as a record, but **already on the board twice**; three of Ramirez's four claims about it CONTRADICTED or absent | no new node; **merge two duplicates** |
| 2 | Foreign Technology Division, Wright-Patterson AFB | PARTLY CONFIRMED. The organisation, its parent command, its station and its Blue Book responsibility are Tier 1 from two 1966 records. The **1961 redesignation is NOT OPENED** from an official source, and the one compilation that was opened contradicts the board's wording | new node |
| 3 | Scientific and Technical Intelligence Committee (USIB) | CONFIRMED, and the charter says more than the triage row expected | new node |
| 4 | The Monroe Institute / Gateway Process memorandum, 9 June 1983 | CONFIRMED. The memorandum was opened in full. Triage-5 row A6's claim that the board already cites an item of that description is CONTRADICTED | new node |
| 5 | Dr. Eric A. Walker, Executive Secretary, Research and Development Board | **NOT OPENED** | none |

**The five findings that matter, in order:**

1. **The board carries the Haines article as two separate nodes.** `haines-cia-history`
   ("A Die-hard Issue: CIA's Role in the Study of UFOs, 1947-1990", cluster `ic`, B,
   C0/A3/D2) and `cia-haines-1997` ("'CIA's Role in the Study of UFOs, 1947-90'", cluster
   `other`, B, C0/A2/D3) are the same 1997 Studies in Intelligence article by the same
   author, citing three overlapping quotations. Building a third node for row 3 would make
   it three. This is a merge, not a build.
2. **Ramirez's account of the Haines article does not survive the article.** He attributes
   to Haines a "one in ten" residue of real unresolved UFOs; the article gives 5.9 percent
   in 1955 and 4 percent in 1956. He offers it as the origin of the "men in black" legend
   with CIA officers presenting Air Force credentials; no such passage is in it. He says a
   classified companion version exists and that he holds it; the article makes no reference
   to any such version. What Ramirez did get right is the article's own account of its
   origin: DCI Woolsey ordering a further review in late 1993.
3. **ATIC did not "become" the Foreign Technology Division.** The only lineage record that
   could be opened from here records that ATIC was redesignated **Aerospace** Technical
   Intelligence Center on 21 September 1959 and **discontinued** on 1 July 1961, and that
   FTD was "constituted, activated, and organized 1 July 1961", absorbing the mission and
   resources. The board's prose says ATIC "became the Foreign Technology Division in 1961"
   in at least two places and its `atic` node runs from 1951 with no 1959 name change. That
   record is a private compilation of Department of the Air Force organizational-history
   data, not an official page, so the correction is offered at Tier 2 and the 1961 date is
   NOT OPENED at Tier 1.
4. **The STIC charter puts anomalies in the committee's own objectives.** Priority Group II
   of the 23 October 1974 charter reads: "Assessment and establishment of an Intelligence
   Community position regarding certain unidentified foreign activities and anomalies in the
   S&T area." That is a standing USIB committee tasked, in its charter, with forming a
   community position on unidentified activities. Nobody in the corpus claimed this; the
   triage row asked only for the committee's existence.
5. **Triage-5 row A6 is wrong that the board already cites the Gateway memorandum.** The
   board's single Monroe reference is a source line on `l-kirtland` reading "Wikipedia, Paul
   Bennewitz, citing Moore's 1989 MUFON statement and the Monroe Institute article in the
   CIA reading room", attached to a claim about a **1992** article identifying Moore and
   Doty. It carries no URL and no document number, and it is not the 1983 Army memorandum.

---

## 1. Gerald K. Haines, "CIA's Role in the Study of UFOs, 1947-90"

**VERDICT: CONFIRMED as a record. No new node.** The article exists, was opened, and says
what the board's two existing nodes say it says. The finding is the duplication, plus three
transcript claims the article does not support.

### What was opened

| URL | What is at it |
|---|---|
| https://www.cia.gov/resources/csi/studies-in-intelligence/studies-in-intelligence-1997/cias-role-in-the-study-of-ufos-1947-1990/ | The CIA Center for the Study of Intelligence landing page. Title "A Die-hard Issue: CIA's Role in the Study of UFOs, 1947-1990", author Gerald K. Haines. The page carries only the abstract and a download link; the substantive text is in an 18-page PDF that did not render through this channel. |
| https://www.nicap.org/ciarole.htm | The full text of the article, mirrored. This is the source the board's own `haines-cia-history` node already lists as "Haines article, mirrored full text". All quotations below were read here. |

The Area 52 brief records `cia.gov/readingroom` as a 302 loop from this machine. The
`cia.gov/resources/csi/` path is a different route and it answered, but it answered with the
landing page only.

### What the document establishes

The article states that "CIA officials wanted knowledge of any Agency interest in the
subject of flying saucers carefully restricted, noting not only that the Robertson panel
report was classified but also that any mention of CIA sponsorship of the panel was
forbidden"; that the panel "suggested using the mass media, advertising, business clubs,
schools, and even the Disney corporation to get the message across"; that "By checking with
the Agency's U-2 Project Staff in Washington, BLUE BOOK investigators were able to attribute
many UFO sightings to U-2 flights"; that "According to later estimates from CIA officials
who worked on the U-2 project and the OXCART (SR-71, or Blackbird) project, over half of all
UFO reports from the late 1950s through the 1960s were accounted for by manned
reconnaissance flights"; and that "This led the Air Force to make misleading and deceptive
statements to the public in order to allay public fears and to protect an extraordinarily
sensitive national security project."

Two things the board does not currently carry are on the same page. The article's own
account of why it was written: "In late 1993, after being pressured by UFOlogists for the
release of additional CIA information on UFOs, DCI R. James Woolsey ordered another review
of all Agency files on UFOs." And its figures for the unexplained residue: "The percentage
of what the Air Force considered unexplained UFO sightings fell to 5.9 percent in 1955 and
to 4 percent in 1956."

On ATIC it says only that "With a small staff, the Air Technical Intelligence Center (ATIC)
tried to persuade the public that UFOs were not extraordinary", and that the CIA Study Group
"met with Air Force officials at Wright-Patterson and reviewed their data and findings."

### What the transcript claimed that this document does NOT establish

Batch 07, file 04, John Ramirez, at 0:43:34, 0:44:24 and 0:49:22. Four claims, three of
which fail against the article:

| Ramirez says | The article says |
|---|---|
| Haines gives "one in ten" reported sightings as unresolved real UFOs | 5.9 percent in 1955, 4 percent in 1956 |
| The U-2 daylight silver-airframe explanation is the origin of the "men in black" legend, with CIA officers presenting Air Force credentials | Nothing. Neither "men in black" nor any credential passage is in the text |
| A classified version exists alongside the released one, and he holds it | Nothing. The article makes no reference to a classified companion |
| The article covers CIA's UFO interest from 1947, drawing on U-2 and OXCART overflights | Correct, and the article's own U-2/OXCART section is the passage the board already quotes |

The triage row also asks whether the spelling is Haynes or Haines. **The record decides:
Haines.** Both the CIA page and the mirrored text print Gerald K. Haines. The lead map's
`Gerald K. Haynes` and the triage row that copied it are wrong, and the board is right.

### Recommendation instead of a draft node

No node. Two exist. Merge `cia-haines-1997` into `haines-cia-history`, keeping the longer
title from `haines-cia-history` and the four distinct claims from `cia-haines-1997` (the
Blue Book "ice crystals and temperature inversions" passage and the Philip Strong sanitised-
report passage are on the second node only), then rewire the second node's edges onto the
first. If a session wants the article's own origin and its residue figures on the board,
these two are Tier 1 additions to the merged node:

```json
{
  "target": "haines-cia-history",
  "add_claims": [
    {
      "tier": 1,
      "text": "The article states its own trigger: 'In late 1993, after being pressured by UFOlogists for the release of additional CIA information on UFOs, DCI R. James Woolsey ordered another review of all Agency files on UFOs.'",
      "source": "Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence, mirrored full text, https://www.nicap.org/ciarole.htm"
    },
    {
      "tier": 1,
      "text": "The article gives the Air Force's own unexplained residue as a falling figure: 'The percentage of what the Air Force considered unexplained UFO sightings fell to 5.9 percent in 1955 and to 4 percent in 1956.' On Area 52 (batch 07, file 04, 0:49:22) John Ramirez attributed to this article a figure of one in ten. The article does not carry that figure.",
      "source": "Gerald K. Haines, 'CIA's Role in the Study of UFOs, 1947-90', Studies in Intelligence, mirrored full text, https://www.nicap.org/ciarole.htm"
    }
  ]
}
```

---

## 2. Foreign Technology Division, Wright-Patterson AFB

**VERDICT: PARTLY CONFIRMED.** Two 1966 records establish FTD as a real organisation of Air
Force Systems Command at Wright-Patterson with the Blue Book effort assigned to it, in its
own name, at Tier 1. The **1961 redesignation the triage row asks for was not opened from an
official source**, and the one record that carries it contradicts the board's phrasing.

### What was opened

| URL | What is at it |
|---|---|
| https://nicap.org/afr80-17.htm | Air Force Regulation 80-17, "Research and Development - UNIDENTIFIED FLYING OBJECTS (UFO)", Department of the Air Force, Washington DC, **19 September 1966**. The regulation that replaced AFR 200-2. |
| https://files.ncas.org/condon/text/appndx-a.htm | Condon Report Appendix A: "Special Report of the USAF Scientific Advisory Board Ad Hoc Committee to Review Project 'Blue Book'", **March 1966** (the O'Brien committee). |
| https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf | A PDF headed "AEROSPACE TECHNICAL INTELLIGENCE CENTER", footed "DEPARTMENT OF THE AIR FORCE ORGANIZATIONAL HISTORIES", created 10 December 2025, citing as its source "Air Force Historical Research Agency, U.S. Air Force, Maxwell AFB, Alabama." **This is a private compilation site, not an Air Force site.** Downloaded with curl, 126,018 bytes, text extracted with `pdftotext -layout`. |

**What refused.** The AFHRA lineage fact sheet the search results point to,
`https://www.dafhistory.af.mil/About-Us/Fact-Sheets/Display/Article/432518/national-air-and-space-intelligence-center-acc/`,
returned **HTTP 403** to WebFetch and 403 to curl with a browser user agent.
`https://www.nasic.af.mil/About-Us/Fact-Sheets/Display/Article/1904310/nasic-history/`
returned **403**. `https://www.af.mil/About-Us/Fact-Sheets/Display/Article/104590/...`, the
Blue Book fact sheet the board already cites, also returned **403**. `web.archive.org` does
not reach from here at all, so the board's own Wayback copy of that fact sheet could not be
opened either. Every official Air Force route to the 1961 date is walled from this machine.

### What the documents establish

**AFR 80-17, 19 September 1966.** "The Air Force Systems Command will support the program
with current resources within the Foreign Technology Division (FTD) at Wright-Patterson Air
Force Base, Ohio, to continue Blue Book effort." "FTD will: (1) Analyze and evaluate all
information and evidence reported to bases on those UFOs which are not identified at the
base level." "FTD, Wright-Patterson AFB, Ohio, will prepare a final case report on each
sighting reported to it." Overall responsibility sits elsewhere: "The Deputy Chief of Staff,
Research and Development, is responsible for the overall program, evaluation of
investigative procedures, and the conduct of separate scientific investigations."

**USAF Scientific Advisory Board ad hoc committee, March 1966.** "The Committee next heard
briefings from the AFSC Foreign Technology Division, which is the cognizant Air Force agency
that collates information on UFO sightings and monitors investigations of individual cases."
Its recommendation: "the Foreign Technology Division (FTD) at Wright-Patterson Air Force
Base should continue to exercise its presently assigned responsibilities concerning UFOs."
On resources: "the present Air Force program dealing with UFO sightings has been well
organized, although the resources assigned to it (only one officer, a sergeant, and
secretary) have been quite limited."

**The lineage, from the compilation only.** "Air Technical Intelligence Center established
21 May 1951; redesignated Aerospace Technical Intelligence Center, 21 September 1959;
discontinued 1 July 1961. Foreign Technology Division constituted, activated, and organized
1 July 1961." And: "On 1 July 1961, the organization was inactivated and the mission and
resources absorbed by the Foreign Technology Division (FTD)."

### What the transcript and the triage row claimed that these do NOT establish

Ramirez (batch 07, file 04, 0:08:37) credits FTD with coining the phrase "domes of light
phenomena" for anomalous signatures picked up alongside Soviet missile tests. **Nothing in
either 1966 record touches that**, and no FTD record naming the phrase was found. At 1:28:17
he treats NASIC as FTD's later name, which the lineage compilation supports as far as the
1961 to 1991 half goes and which no opened record carries beyond that.

The triage row asks for "the 1961 redesignation of ATIC as FTD". There was no redesignation
of ATIC as FTD. On the only record opened, ATIC's redesignation in 1959 was to **Aerospace**
Technical Intelligence Center, that organisation was discontinued, and FTD was separately
constituted on the same day. The board's prose in `afrl`, `l-wright-patterson` and elsewhere
says "ATIC became the Foreign Technology Division in 1961"; the record calls it a
discontinuation and an absorption. Keep the distinction.

### Draft node

```json
{
  "id": "foreign-technology-division",
  "cls": "institution",
  "label": "Foreign Technology Division, Wright-Patterson AFB",
  "cluster": "ic",
  "sub": "Air Force Systems Command foreign materiel exploitation centre, 1961-1991; the office that held Project Blue Book",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "dateStart": "1961-07-01",
  "dateEnd": "1991",
  "desc": "The Foreign Technology Division was the Air Force's foreign aerospace materiel exploitation centre at Wright-Patterson AFB, sitting between the Air Technical Intelligence Center and the National Air and Space Intelligence Center in the same lineage and at the same station. Air Force Regulation 80-17 of 19 September 1966 assigned it the Blue Book effort in its own name: FTD analysed and evaluated every report a base could not identify, and wrote the final case report on each. The USAF Scientific Advisory Board's ad hoc review committee of March 1966 called it the cognizant Air Force agency for UFO sightings and recommended it keep the job, while recording that the whole programme ran on one officer, a sergeant and a secretary. The board carries this organisation in prose twenty-one times and has never had a node for it.",
  "claims": [
    {
      "tier": 1,
      "text": "The Blue Book effort was assigned to FTD by regulation: 'The Air Force Systems Command will support the program with current resources within the Foreign Technology Division (FTD) at Wright-Patterson Air Force Base, Ohio, to continue Blue Book effort.'",
      "source": "Air Force Regulation 80-17, 'Research and Development - UNIDENTIFIED FLYING OBJECTS (UFO)', Department of the Air Force, 19 September 1966, https://nicap.org/afr80-17.htm"
    },
    {
      "tier": 1,
      "text": "FTD, not a base, was the terminal analytical office: 'FTD will: (1) Analyze and evaluate all information and evidence reported to bases on those UFOs which are not identified at the base level', and 'FTD, Wright-Patterson AFB, Ohio, will prepare a final case report on each sighting reported to it.'",
      "source": "Air Force Regulation 80-17, 19 September 1966, https://nicap.org/afr80-17.htm"
    },
    {
      "tier": 1,
      "text": "The USAF Scientific Advisory Board's ad hoc committee of March 1966 identified FTD as 'the AFSC Foreign Technology Division, which is the cognizant Air Force agency that collates information on UFO sightings and monitors investigations of individual cases', and recommended that it 'should continue to exercise its presently assigned responsibilities concerning UFOs.'",
      "source": "Special Report of the USAF Scientific Advisory Board Ad Hoc Committee to Review Project 'Blue Book', March 1966, printed as Appendix A of the Condon Report, https://files.ncas.org/condon/text/appndx-a.htm"
    },
    {
      "tier": 1,
      "text": "The same 1966 committee recorded the resources behind the whole Air Force UFO programme as 'only one officer, a sergeant, and secretary'.",
      "source": "Special Report of the USAF Scientific Advisory Board Ad Hoc Committee to Review Project 'Blue Book', March 1966, Condon Report Appendix A, https://files.ncas.org/condon/text/appndx-a.htm"
    },
    {
      "tier": 2,
      "text": "The Air Force organizational-history lineage records a discontinuation and a new constitution rather than a renaming: 'Air Technical Intelligence Center established 21 May 1951; redesignated Aerospace Technical Intelligence Center, 21 September 1959; discontinued 1 July 1961. Foreign Technology Division constituted, activated, and organized 1 July 1961', with the mission and resources absorbed by FTD on that date. Tier 2 because the compilation carrying this text is a private site citing the Air Force Historical Research Agency, and AFHRA's own page returns HTTP 403 from this environment.",
      "source": "'AEROSPACE TECHNICAL INTELLIGENCE CENTER', Department of the Air Force Organizational Histories compilation, created 10 December 2025, sourced to the Air Force Historical Research Agency, https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf"
    }
  ],
  "sources": [
    { "name": "Air Force Regulation 80-17, Unidentified Flying Objects (UFO), 19 September 1966", "url": "https://nicap.org/afr80-17.htm", "date": "1966-09-19" },
    { "name": "Special Report of the USAF Scientific Advisory Board Ad Hoc Committee to Review Project 'Blue Book', March 1966 (Condon Report Appendix A)", "url": "https://files.ncas.org/condon/text/appndx-a.htm", "date": "1966-03-01" },
    { "name": "Aerospace Technical Intelligence Center, Department of the Air Force Organizational Histories compilation (private site, sourced to AFHRA)", "url": "https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf", "date": "2025-12-10" }
  ],
  "edges": [
    {
      "a": "atic",
      "b": "foreign-technology-division",
      "type": "institutional",
      "claimTier": 2,
      "label": "ATIC discontinued 1 July 1961; FTD constituted the same day and absorbed its mission",
      "note": "The lineage record says ATIC was redesignated Aerospace Technical Intelligence Center in 1959 and discontinued on 1 July 1961, with the mission and resources absorbed by the newly constituted Foreign Technology Division, so this is a succession rather than the renaming the board's prose describes.",
      "sources": [{ "name": "Aerospace Technical Intelligence Center, DAF Organizational Histories compilation sourced to AFHRA", "url": "https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf", "date": "2025-12-10" }]
    },
    {
      "a": "foreign-technology-division",
      "b": "project-blue-book",
      "type": "programmatic",
      "claimTier": 1,
      "label": "Held the Blue Book effort by regulation from 19 September 1966",
      "note": "AFR 80-17 assigns the Blue Book effort to FTD at Wright-Patterson, requires FTD to analyse every report not identified at base level, and requires FTD to write the final case report on each sighting.",
      "sources": [{ "name": "AFR 80-17, 19 September 1966", "url": "https://nicap.org/afr80-17.htm", "date": "1966-09-19" }]
    },
    {
      "a": "foreign-technology-division",
      "b": "l-wright-patterson",
      "type": "geographic",
      "claimTier": 1,
      "label": "Stationed at Wright-Patterson AFB, Ohio",
      "note": "AFR 80-17 names the station in the assignment itself: 'the Foreign Technology Division (FTD) at Wright-Patterson Air Force Base, Ohio'.",
      "sources": [{ "name": "AFR 80-17, 19 September 1966", "url": "https://nicap.org/afr80-17.htm", "date": "1966-09-19" }]
    },
    {
      "a": "foreign-technology-division",
      "b": "nasic",
      "type": "institutional",
      "claimTier": 2,
      "label": "Same Wright-Patterson lineage; NASIC is the later name",
      "note": "The organizational-history compilation carries the FTD to NASIC lineage at the same station; no official Air Force page could be opened from here to raise this above Tier 2.",
      "sources": [{ "name": "Aerospace Technical Intelligence Center, DAF Organizational Histories compilation sourced to AFHRA", "url": "https://www.usafunithistory.com/PDF/A-E/AEROSPACE%20TECHNICAL%20INTELLIGENCE%20CENTER.pdf", "date": "2025-12-10" }]
    },
    {
      "a": "foreign-technology-division",
      "b": "usaf",
      "type": "institutional",
      "claimTier": 1,
      "label": "Air Force Systems Command organisation under the DCS/Research and Development for the UFO programme",
      "note": "AFR 80-17 makes the Deputy Chief of Staff, Research and Development responsible for the overall programme and Air Force Systems Command responsible for supporting it through FTD.",
      "sources": [{ "name": "AFR 80-17, 19 September 1966", "url": "https://nicap.org/afr80-17.htm", "date": "1966-09-19" }]
    }
  ]
}
```

---

## 3. Scientific and Technical Intelligence Committee (USIB)

**VERDICT: CONFIRMED.** The committee's charter was opened. It establishes the committee,
its predecessor name, its relationship to the United States Intelligence Board, its
substantive scope and its internal structure, and it carries one objective directly relevant
to this board that no speaker in the corpus mentioned.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-cia-rdp79m00098a000500020010-4/cia-rdp79m00098a000500020010-4_djvu.txt | The CIA reading-room mirror OCR of **CIA-RDP79M00098A000500020010-4**, "CHARTER / SCIENTIFIC AND TECHNICAL INTELLIGENCE COMMITTEE", dated **23 October 1974**, marked Approved For Release 2005/04/28. |
| https://archive.org/download/cia-readingroom-document-cia-rdp80m01133a000100210002-3/cia-rdp80m01133a000100210002-3_djvu.txt | **CIA-RDP80M01133A000100210002-3**, memorandum on Scientific Intelligence Committee letterhead, **3 August 1975**, to the Deputy to the DCI for the Intelligence Community, subject "Letter of Instruction, Scientific and Technical Intelligence Committee", with the FY-1976 Letter of Instruction attached. Signature and names redacted under 25X1. |
| https://irp.fas.org/offdocs/dcid.htm | The FAS list of Director of Central Intelligence Directives. It lists **"DCID 3/5P - Scientific and Technical Intelligence Committee"** as a title with no text behind it. The directive itself is not available there. |

Both CIA documents are scans; the text quoted is the OCR layer archive.org publishes, and it
is imperfect on the page furniture. The substantive paragraphs quoted below are clean.

### What the documents establish

**The name change, and that it was a renaming.** "Because of the increased emphasis the
Committee will place on foreign intelligence related to technology, the name of the
Committee will be changed from Scientific Intelligence Committee to Scientific and Technical
Intelligence Committee (STIC)." A footnote adds that "This name change and various subunit
changes will become official when the appropriate DCID is approved", which is why the FAS
list carries DCID 3/5P under the new name.

**Its relationship to the USIB.** "The STIC will advise USIB on scientific and technical
matters within the Committee's areas of concern. The STIC, in support of USIB, will also
review, stimulate, guide, and coordinate collection activity and information processing in
response to resource management objectives in these areas."

**Its operating precept.** "to provide early warning of foreign scientific or technical
advances, whether indigenous or imported, which could affect significantly the national
security or national welfare of the United States."

**The objective that matters to this board.** Under Priority Group II: "Assessment and
establishment of an Intelligence Community position regarding certain unidentified foreign
activities and anomalies in the S&T area."

**Structure.** "The STIC will have Subcommittees, Advisory Groups, Working Groups and a
Secretariat." The initial substructure named in the charter is three subcommittees
(Priorities and Resources; Collection Program Evaluation; Production Program Evaluation),
nine Advisory Groups (ASW Technology; Behavioral and Human Engineering; Biomedical Science
and Technology; Civil Technology; Computers, joint with EIC; C3 Technology; Electronics;
Lasers and Electro-optics; S&T Policies and Resources) and two working groups (High Energy
Laser Systems; Military Implications of Technology Transfer). "STIC members or their
alternates will normally serve as subcommittee chairmen and may serve as members."

**Continuity into 1975.** The 3 August 1975 Letter of Instruction, still on Scientific
Intelligence Committee letterhead, instructs STIC to "Complete the reorganization of the
STIC and the transfer of subgroups to GMAIC during August 1975" and to "take the lead to
providing a dynamic overview and coordinate all intelligence community activities related to
significant foreign science and technology which might lead to future political, military,
or economic threats to the US."

### What the transcript claimed that these documents do NOT establish

Ramirez (batch 07, file 04, 0:42:39) calls it "a major committee" from the era when the DCI
ran the intelligence community and says its chairman, whom he names only as "Jim L.",
attended the unclassified 2001 symposium. **The charter confirms the committee's standing
and its USIB relationship and nothing else.** No chairman is named in either document: the
1975 memorandum's signature block is redacted under 25X1, and the third CIA reading-room
item that names a chairman by name in its title is a different document that was not opened
for this pass. The committee's survival to 2001 was not established from any record here.

The triage row's rationale, that STIC is "the standing committee structure that outlived the
[Robertson] panel", is **not established**. Neither document mentions the Robertson Panel,
the Office of Scientific Intelligence, or unidentified flying objects. The link between the
1953 panel and this 1974 charter is an inference, and the node must not assert it.

### Draft node

```json
{
  "id": "stic-usib",
  "cls": "institution",
  "label": "Scientific and Technical Intelligence Committee (USIB)",
  "cluster": "ic",
  "sub": "Standing USIB committee, renamed from the Scientific Intelligence Committee in 1974; chartered to form a community position on unidentified foreign activities and anomalies",
  "tier": "B",
  "C": 0,
  "A": 3,
  "D": 1,
  "dateStart": "1974-10-23",
  "dateEnd": null,
  "desc": "STIC was the United States Intelligence Board's standing committee on scientific and technical intelligence, renamed from the Scientific Intelligence Committee by a charter of 23 October 1974 to reflect a shift of emphasis toward technology. Its operating precept was early warning of foreign scientific or technical advances affecting national security, and it advised, and coordinated collection and production for, the USIB in those areas. Its charter lists among its Priority Group II objectives the assessment and establishment of an Intelligence Community position regarding certain unidentified foreign activities and anomalies in the science and technology area, which places a standing community mechanism for exactly that question inside the intelligence structure of the 1970s. A Letter of Instruction of 3 August 1975 shows the committee still operating under the Deputy to the DCI for the Intelligence Community and reorganising its subgroups.",
  "claims": [
    {
      "tier": 1,
      "text": "The committee is a renaming, not a new body: 'Because of the increased emphasis the Committee will place on foreign intelligence related to technology, the name of the Committee will be changed from Scientific Intelligence Committee to Scientific and Technical Intelligence Committee (STIC).'",
      "source": "CHARTER, Scientific and Technical Intelligence Committee, 23 October 1974, CIA-RDP79M00098A000500020010-4, CIA reading-room mirror, https://archive.org/download/cia-readingroom-document-cia-rdp79m00098a000500020010-4/cia-rdp79m00098a000500020010-4_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Its charter tasks it with anomalies by name. Under Priority Group II: 'Assessment and establishment of an Intelligence Community position regarding certain unidentified foreign activities and anomalies in the S&T area.'",
      "source": "CHARTER, Scientific and Technical Intelligence Committee, 23 October 1974, CIA-RDP79M00098A000500020010-4, https://archive.org/download/cia-readingroom-document-cia-rdp79m00098a000500020010-4/cia-rdp79m00098a000500020010-4_djvu.txt"
    },
    {
      "tier": 1,
      "text": "It answered to the United States Intelligence Board: 'The STIC will advise USIB on scientific and technical matters within the Committee's areas of concern. The STIC, in support of USIB, will also review, stimulate, guide, and coordinate collection activity and information processing in response to resource management objectives in these areas.'",
      "source": "CHARTER, Scientific and Technical Intelligence Committee, 23 October 1974, CIA-RDP79M00098A000500020010-4, https://archive.org/download/cia-readingroom-document-cia-rdp79m00098a000500020010-4/cia-rdp79m00098a000500020010-4_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Its stated purpose was early warning: 'to provide early warning of foreign scientific or technical advances, whether indigenous or imported, which could affect significantly the national security or national welfare of the United States.' Its initial substructure was three subcommittees, nine advisory groups and two working groups, including advisory groups on Behavioral and Human Engineering and on Lasers and Electro-optics.",
      "source": "CHARTER, Scientific and Technical Intelligence Committee, 23 October 1974, CIA-RDP79M00098A000500020010-4, https://archive.org/download/cia-readingroom-document-cia-rdp79m00098a000500020010-4/cia-rdp79m00098a000500020010-4_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The committee was still operating in 1975 under a Letter of Instruction from the Deputy to the DCI for the Intelligence Community, which directed it to 'Complete the reorganization of the STIC and the transfer of subgroups to GMAIC during August 1975' and to coordinate all intelligence community activity on foreign science and technology that might lead to future threats to the US.",
      "source": "Memorandum, Letter of Instruction, Scientific and Technical Intelligence Committee, 3 August 1975, CIA-RDP80M01133A000100210002-3, https://archive.org/download/cia-readingroom-document-cia-rdp80m01133a000100210002-3/cia-rdp80m01133a000100210002-3_djvu.txt"
    }
  ],
  "sources": [
    { "name": "CHARTER, Scientific and Technical Intelligence Committee, 23 October 1974 (CIA-RDP79M00098A000500020010-4)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp79m00098a000500020010-4", "date": "1974-10-23" },
    { "name": "Memorandum, Letter of Instruction, Scientific and Technical Intelligence Committee, 3 August 1975 (CIA-RDP80M01133A000100210002-3)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80m01133a000100210002-3", "date": "1975-08-03" },
    { "name": "FAS list of Director of Central Intelligence Directives, listing DCID 3/5P Scientific and Technical Intelligence Committee", "url": "https://irp.fas.org/offdocs/dcid.htm", "date": "2026-09-02" }
  ],
  "edges": [
    {
      "a": "stic-usib",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "Chartered under the DCI structure; instructed by the Deputy to the DCI for the Intelligence Community",
      "note": "The 1974 charter takes effect when the appropriate DCID is approved, and the 1975 Letter of Instruction is addressed to the Deputy to the DCI for the Intelligence Community, placing the committee inside the DCI's community machinery.",
      "sources": [{ "name": "CHARTER, STIC, 23 October 1974, and Letter of Instruction, 3 August 1975", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp80m01133a000100210002-3", "date": "1975-08-03" }]
    }
  ]
}
```

**Deliberately not drafted.** No edge to `robertson-panel` or `howard-p-robertson`. The
triage row's argument for the node rests on the panel-to-committee continuity, and neither
opened document supports it. This is an exclusion, not an omission.

---

## 4. The Monroe Institute, and the Gateway Process memorandum of 9 June 1983

**VERDICT: CONFIRMED.** The memorandum was opened in full, twenty-nine pages, and it is what
the triage row describes: a United States Army assessment in writing of a private institute's
method. Two things the triage rows say about it are wrong.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5 | The CIA reading-room mirror item, titled "ANALYSIS AND ASSESSMENT OF GATEWAY PROCESS", document **CIA-RDP96-00788R001700210016-5**, 29 pages, marked Approved For Release 2003/09/10. |
| https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001700210016-5/cia-rdp96-00788r001700210016-5.pdf | The scan itself, 2,443,752 bytes. `pdftotext` returns nothing: there is no text layer. |
| https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001700210016-5/cia-rdp96-00788r001700210016-5_djvu.txt | The OCR layer archive.org publishes, 94,841 bytes. Everything quoted below is read from it, and the OCR is noisy on the signature block and on the release stamps. |

### What the document establishes

**What it is.** A memorandum on Department of the Army letterhead reading "DEPARTMENT OF THE
ARMY / US ARMY OPERATIONAL GROUP / US ARMY INTELLIGENCE AND SECURITY COMMAND / FORT GEORGE
G. MEADE, MARYLAND 20755", dated **9 June 1983**, "SUBJECT: Analysis and Assessment of
Gateway Process", "TO: Commander, US Army Operational Group, Fort Meade, MD 20755". The
signature block reads Wayne M. McDonnell, LTC, MI, Commander, Det O; the OCR renders the
name "WAYNIY M. MCDONNELL" and the rank line "LC, MI", so a session using this should read
the scan rather than the OCR before printing the name.

**That it was tasked.** "You tasked me to provide an assessment of the Gateway Experience in
terms of its mechanics and ultimate practicality."

**Who it was for.** "a useful guide for other USAINSCOM personnel who are required to take
the Gateway training or work with Gateway materials." That is the sentence that makes this
more than an officer's private essay: it says, on the face of an Army document, that INSCOM
personnel were **required** to take Monroe Institute training.

**The Institute by name.** "In order to describe the Monroe Institute technique for
achieving altered states of consciousness(the 'Gateway Experience') involving brain
hemisphere synchronization or 'Hemi-Sync'". The bibliography identifies the Institute and
its location: "Jager, Melissa. Monograph: 'The Lamp Turn Laser.' Monroe Institute of Applied
Sciences, Faber, Va, undated", and lists "Monroe, Robert A. Journeys Out of the Body. New
York, Doubleday and Company, 1971."

**Remote viewing inside the Gateway technique.** "In addition, the energy bar tool is used
as a portal for initiating a follow-on technique called 'remote viewing.'"

**The Institute's own claimed results, as the Army recorded them.** "To date, according to
one of the trainers at Monroe Institute, numerous experiments have been conducted involving
persons moving from one coast to the other in the out-of-body state to read a series of ten
computer generated numbers in a university laboratory. Although most have aquired enough of
the digits to make clear that their consciousness was present none have ever succeeded in
getting all ten correct."

**The finding.** "There is a sound, rational basis in terms of physical science parameters
for considering Gateway to be plausible in terms of its essential objectives", followed by a
six-step phased programme, lettered A to F, for accelerating INSCOM personnel into the
out-of-body state under conscious control.

### What the transcript and the triage rows claimed that this document does NOT establish

McMoneagle (batch 10, file 1, at 1:31:25 and 2:12:40) says DoD arranged for him to train
out-of-body control with Robert Monroe, and that he later taught remote-viewing classes
there for years, replacing training officer Skip Atwater. **The memorandum names neither
McMoneagle nor Atwater and does not mention any individual trainee.** What it establishes is
the structural fact underneath his account: that INSCOM required personnel to take Gateway
training, in 1983, and commissioned a written assessment of it. Anything about McMoneagle
himself stays at Tier 2 against the episode.

**Triage-5 row A6 is contradicted.** It says "The board **already cites** an item of that
description." The board's only Monroe reference is a source line on `l-kirtland` reading
"Wikipedia, Paul Bennewitz, citing Moore's 1989 MUFON statement and the Monroe Institute
article in the CIA reading room", attached to a Tier 2 claim about a **1992** article
identifying William Moore and Richard Doty. It has no URL, no document number and no date
matching this memorandum. The board does not cite this record; it cites a secondary
description of a different reading-room item.

### Draft node

```json
{
  "id": "monroe-institute",
  "cls": "institution",
  "label": "The Monroe Institute",
  "cluster": "research",
  "sub": "Private institute at Faber, Virginia; source of the Gateway Experience and Hemi-Sync, assessed in writing by INSCOM in 1983",
  "tier": "B",
  "C": 0,
  "A": 2,
  "D": 1,
  "dateStart": "1983-06-09",
  "dateEnd": null,
  "desc": "The Monroe Institute is a private body at Faber, Virginia, founded around Robert A. Monroe's out-of-body work and the brain hemisphere synchronization technique it markets as Hemi-Sync. It matters to this board because a United States Army intelligence command put a written assessment of its method on the record. On 9 June 1983 the commander of Detachment O, US Army Operational Group, US Army Intelligence and Security Command at Fort George G. Meade, wrote a twenty-nine page memorandum analysing the Gateway Experience, on tasking from his own commander, and said explicitly that it was intended as a guide for other USAINSCOM personnel who were required to take the Gateway training. The memorandum concluded that Gateway is plausible in physical science terms and set out a six-step phased programme for bringing personnel to conscious control of the out-of-body state. The date places it inside CENTER LANE, INSCOM's remote-viewing special access programme of 1983 to 1986.",
  "claims": [
    {
      "tier": 1,
      "text": "A US Army intelligence command assessed the Institute's method in writing: a memorandum of 9 June 1983 from the US Army Operational Group, US Army Intelligence and Security Command, Fort George G. Meade, subject 'Analysis and Assessment of Gateway Process', addressed to the Commander, US Army Operational Group, and opening 'You tasked me to provide an assessment of the Gateway Experience in terms of its mechanics and ultimate practicality.'",
      "source": "Analysis and Assessment of Gateway Process, US Army Operational Group, INSCOM, 9 June 1983, CIA-RDP96-00788R001700210016-5, CIA reading-room mirror, https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5"
    },
    {
      "tier": 1,
      "text": "The memorandum states its readership as personnel under a training requirement: it was written to be 'a useful guide for other USAINSCOM personnel who are required to take the Gateway training or work with Gateway materials.'",
      "source": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5, https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5"
    },
    {
      "tier": 1,
      "text": "The subject of the assessment is named as the Institute's own technique: 'In order to describe the Monroe Institute technique for achieving altered states of consciousness(the \"Gateway Experience\") involving brain hemisphere synchronization or \"Hemi-Sync\"'. The bibliography identifies it as the Monroe Institute of Applied Sciences, Faber, Va, and cites Robert A. Monroe, Journeys Out of the Body, Doubleday, 1971.",
      "source": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5, https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5"
    },
    {
      "tier": 1,
      "text": "Remote viewing appears inside the Gateway technique itself: 'In addition, the energy bar tool is used as a portal for initiating a follow-on technique called \"remote viewing.\"'",
      "source": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5, https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5"
    },
    {
      "tier": 1,
      "text": "The Army's finding was favourable: 'There is a sound, rational basis in terms of physical science parameters for considering Gateway to be plausible in terms of its essential objectives', followed by a six-step phased programme for reaching conscious control of the out-of-body state. The same memorandum records the Institute's own trainers reporting that in cross-country out-of-body number-reading tests 'none have ever succeeded in getting all ten correct.'",
      "source": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5, https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5"
    }
  ],
  "sources": [
    { "name": "Analysis and Assessment of Gateway Process, US Army Operational Group, USAINSCOM, 9 June 1983 (CIA-RDP96-00788R001700210016-5, 29 pages)", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5", "date": "1983-06-09" },
    { "name": "OCR text layer of the same document as published by the Internet Archive", "url": "https://archive.org/download/cia-readingroom-document-cia-rdp96-00788r001700210016-5/cia-rdp96-00788r001700210016-5_djvu.txt", "date": "1983-06-09" }
  ],
  "edges": [
    {
      "a": "monroe-institute",
      "b": "center-lane",
      "type": "programmatic",
      "claimTier": 1,
      "label": "INSCOM assessed the Institute's Gateway training in June 1983, inside CENTER LANE's span",
      "note": "The memorandum is an INSCOM product of 9 June 1983 written for USAINSCOM personnel required to take Gateway training, and CENTER LANE is INSCOM's remote-viewing special access programme of 1983 to 1986; the assessment is contemporaneous with the programme and issued by the same command.",
      "sources": [{ "name": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5", "date": "1983-06-09" }]
    },
    {
      "a": "monroe-institute",
      "b": "stargate-program",
      "type": "research",
      "claimTier": 1,
      "label": "A private method brought inside the Army's remote-viewing effort as required training",
      "note": "The memorandum names remote viewing as a follow-on technique inside the Gateway Experience and was written for USAINSCOM personnel required to take that training, which places the Institute's method inside the programme chain the STAR GATE node covers.",
      "sources": [{ "name": "Analysis and Assessment of Gateway Process, 9 June 1983, CIA-RDP96-00788R001700210016-5", "url": "https://archive.org/details/cia-readingroom-document-cia-rdp96-00788r001700210016-5", "date": "1983-06-09" }]
    }
  ]
}
```

**A note for whoever builds this.** The board's shape would also support a separate document
node for the memorandum, the way `stargate-program` sits beside its released files. Row A6
asks for the institution, so that is what is drafted. If both are built, the memorandum's
claims belong on the document and the institution keeps only the descriptive ones.

---

## 5. Dr. Eric A. Walker, Executive Secretary of the Research and Development Board

**VERDICT: NOT OPENED.** No record naming Eric A. Walker as Executive Secretary of the
Research and Development Board could be opened from this machine. The office itself was
documented, and its holder in 1949 was somebody else, which is the useful part of the
attempt.

### What was tried

| URL or route | Result |
|---|---|
| https://nap.nationalacademies.org/read/5427/chapter/52 | 301 to `www.nationalacademies.org`, which returned the National Academy of Engineering *Memorial Tributes: Volume 8* (1996) reader with the Eric A. Walker tribute at pages 280 to 285 and the message "There was a problem loading page 280" through 285. The page images are placeholders. Refetched at `openbook.php?record_id=5427&page=280` with a browser user agent: 358,959 bytes of page furniture and no tribute text. **The volume exists; its text did not open.** |
| archive.org advanced search, `text:("Eric A. Walker")` restricted to the CIA reading-room mirror | Three items, all 1958 and all about the Yale conference "America's Human Resources to Meet the Scientific Challenge": CIA-RDP70-00058R000100110021-5, CIA-RDP70-00058R000100110023-3 and CIA-RDP80B01676R003800020123-5. The last was opened in full and places Walker as a round-table chairman at that conference on 3 February 1958. **Nothing about the RDB.** |
| archive.org advanced search for `"Executive Secretary of the Research and Development Board"` and for `"Eric A. Walker" AND "Executive Secretary"` | 0 results each. The `text:` field indexes item metadata, not the OCR layer, so this is a null result about the index and not about the record. |
| https://api.govinfo.gov/search with DEMO_KEY | HTTP 429, OVER_RATE_LIMIT. `CLAUDE.md` already records that this key rate-limits after about a dozen queries. |
| history.state.gov and trumanlibrary.gov site searches | Both returned their JavaScript search shells with no results in the HTML. |
| archive.org, the two Research and Development Board official booklets (1948 and 1949) | Opened. Neither names Walker; see below. |

### What was established instead

Two records were opened that bear on the office rather than the man.

**The office exists in the founding directive.** CIA-RDP80R01731R001400050004-2 reproduces
the Secretary of Defense press release "HOLD FOR RELEASE NO. 38-47 ... RADIO RELEASE,
DECEMBER 2l, 1947" announcing that "Secretary of Defense Forrestal announced today the
issuance of a directive defining the powers and duties of the Research and Development
Board", together with the directive text signed "James Forrestal". Its administration
section provides that the Board "shall establish a secretariat consisting of civilians and
such military personnel as may be designated for such duty by the Secretaries of the Army,
the Navy and the Air Force. A civilian Executive Secretary shall be designated by the
Chairman with the approval of the Board. The Executive Secretary shall be the chief
executive officer of the secretariat."

**The office was held by Robert F. Rinehart in mid-1949.** The Board's own booklet
*Research and Development Board*, National Military Establishment, Washington DC, 17 June
1949, with a foreword signed "Karl T. Compton, Chairman", lists "Dr. ROBERT F. RINEHART /
Executive Secretary" as a member of the Executive Council, and its biographical page says
Rinehart "came to the Board in July 1948 as Director of the Planning Division, a position
which he held until becoming Executive Secretary in February 1949." The same booklet dates
the Forrestal directive: "The directive outlining the terms of reference under which the RDB
operates was approved by the Secretary of Defense on 18 December 1947", footnoted "RDB 1/5".

That is consistent with Walker taking the post in 1950 and is not evidence that he did.

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-cia-rdp80r01731r001400050004-2/cia-rdp80r01731r001400050004-2_djvu.txt | CIA-RDP80R01731R001400050004-2, "Contact with Research and Development Board", a CIA Deputy Director memorandum signed for the Director of Central Intelligence, with the December 1947 Secretary of Defense press release and the RDB directive attached. |
| https://archive.org/download/researchdevelopm00unit/researchdevelopm00unit_djvu.txt | *Research and development board ..*, United States Department of Defense, Washington, 17 June 1949. OCR layer of a University of Florida documents-department copy. |

### Where the record should be

NARA Record Group 330 holds "Minutes of meetings of the Executive Council, 1946-50" at
section 330.11.3, which is exactly the series in which a change of Executive Secretary in
1950 would appear, and the board's `research-development-board` node already cites the
finding aid that lists it. That series is not online. A 1950 or 1951 edition of the RDB's own
booklet would settle it in one page; archive.org holds only the 1948 and 1949 editions. The
National Academy of Engineering *Memorial Tributes* volume 8 tribute would settle the
biography if its pages can be made to render, and a print or PDF copy is the cheap route.

**No node.** Under the brief, a person candidate needs the office and its dates from a
record. This one has neither yet.

---

## What this pass did not do

Nothing here was merged. No file under `research/*.json`, `data/` or `notes/` was touched.
Node ids in the draft blocks (`foreign-technology-division`, `stic-usib`,
`monroe-institute`) do not exist on the board and were checked as absent before drafting.
Every edge target above was grepped out of `data/the-program.json` first: `atic`,
`project-blue-book`, `l-wright-patterson`, `nasic`, `usaf`, `cia`, `center-lane`,
`stargate-program`. `afsc`, `air-force-systems-command`, `inscom`, `usib` and `l-fort-meade`
were checked and **do not exist**, so no edge was drafted to any of them.
