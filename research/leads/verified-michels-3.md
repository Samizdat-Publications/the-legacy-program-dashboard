# Verified leads: Michels corpus candidates 11 to 15 (verifier 3)

**Status: research output, not board content.** Nothing here has been merged into
`research/` or into any node. It is a verification pass over rows 11 to 15 of
`research/leads/CANDIDATES-2026-09-02-MICHELS-DRAFT.md`, drawn from
`michels-triage-1.md` (row A13), `-2.md` (A3), `-3.md` (A2) and `-5.md` (A2, A11).
Those rows record what podcast guests said. They are unverified by construction.

**Verified 2 September 2026.** Every URL in the tables below was opened by this session
and returned the document described. Where a document is an image scan with no text
layer it was rendered page by page and read off the page, and the pages read are named.
`CLAUDE.md` section 2 applies: nothing is asserted here that was not opened.

**Method note, because it changes what a later session can do.** Three of these five
records are image-only PDFs and this environment has `pdftotext` but no page renderer,
so `Read` on a PDF fails with "pdftoppm is not installed". The fix was
`python -m pip install --target ./pylibs pymupdf` inside the session scratchpad, then
rendering selected pages to PNG and reading those. Nothing was installed into the
user's Python. A session that gives up on a scan because `pdftotext` returns 31 bytes
is giving up too early.

**Access facts worth carrying forward.** `patents.google.com` answers 503 to WebFetch
and serves Google's automated-query block page to curl, so the board's usual patent
route is closed; `image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<number>`
works and returns the scan. `cia.gov/readingroom` and `worldwide.espacenet.com` return
403 to both WebFetch and curl. `vault.fbi.gov` returns 403 to WebFetch but answers curl
with a browser user agent, including its search endpoint. `api.govinfo.gov` accepts a
POST full-text search with `DEMO_KEY` and rate-limits after roughly a dozen calls;
`www.govinfo.gov/content/pkg/<packageId>/pdf/<packageId>.pdf` has no such limit and is
the better download route. `www.cufon.org/cufon/Silverbug.pdf`, cited by every secondary
account of Project SILVER BUG, is a 404.

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 11 | Lawrence Preston Gise | PARTLY CONFIRMED, the Albuquerque directorship NOT OPENED | new node |
| 12 | Project SILVER BUG / Avro Project Y / John Frost | CONFIRMED as a document; the transcript's framing CONTRADICTED | new node |
| 13 | Andrija Puharich | PARTLY CONFIRMED; the AEC grant NOT OPENED | new node |
| 14 | Project A119 | CONFIRMED, with a date correction and a name correction | new node |
| 15 | Church Committee | CONFIRMED; the transcript's use of it CONTRADICTED by the committee itself | new node |

**The four findings that matter most, in order:**

1. **The Church Committee said in its own final report that it never once got to look at
   an agency file.** Book I, on the obstacles it met: "Despite its legal Senate mandate,
   and the issuance of subpoenas, in no instance has the Committee been able to examine
   the agencies' files on its own." Both speakers who raised the committee, from opposite
   ends of the argument, used it as the template for a successful congressional
   penetration of a compartmented programme. The record says the penetration was
   mediated throughout. The same report's own note records that three chapters,
   "Cover," "Espionage," and "Budgetary Oversight," were deleted from the published
   version at the request of the agencies.
2. **The Project SILVER BUG report's stated purpose is the opposite of the transcript's
   framing.** The transcript has the Avro disc as a funnel and cover for deeper physics
   at Wright Field. TR-AC-47 says it exists "to correct the distorted picture presented
   in previous releases, both classified and unclassified", and says of the project
   itself that it "should in no way be associated with any science fiction or 'Flying
   Saucer' stories because of its external appearance."
3. **Gise's offices are documented and they are not the office the transcript needs.**
   The Official Register of the United States puts him in the AEC's Division of Military
   Application as Assistant Director on 1 May 1957 and in ARPA as Assistant Director,
   Administration on 1 May 1959. In 1957 the Manager of the Albuquerque Operations
   Office was Hertford, not Gise. Nothing opened here reaches 1962, Bluegill, or a
   briefing.
4. **"A Study of Lunar Research Flights" is dated 19 June 1959, not May 1959**, and the
   string "A119" appears nowhere in it. Carl Sagan is on its contributor list as
   "C. E. Sagan". Its distribution list sends copies to ARPA, to the AEC "for DMA", to
   Sandia Corporation, to Los Alamos, to Lawrence Radiation Laboratory and to WADD at
   Wright-Patterson.

**One cross-link nobody asked for and it is Tier 1 on both sides.** Colonel Carey L.
O'Bryan, Jr., USAF, is listed in the Official Register 1957 as Deputy Director of the
AEC's Division of Military Application, directly above Gise's line. The same officer
signs the publication review of AFSWC TR-59-39, the lunar detonation study, as Deputy
Commander of the Air Force Special Weapons Center. Two of these five leads share an
officer, on the face of two federal publications.

---

## 11. Lawrence Preston Gise

**VERDICT: PARTLY CONFIRMED.** Two offices are documented in a statutory federal
publication and a third record corroborates one of them from outside. The office the
transcript actually needs, Manager of the AEC's Albuquerque Operations Office, is NOT
OPENED, and one record read here names a different man in it.

**What the transcripts claim.** Five lead maps across four guests route the same chain:
Gise, described as head of the AEC's Albuquerque Operations Office and as Jeff Bezos's
maternal grandfather, took custody of material recovered from the 1962 Bluegill Triple
Prime test and showed it to Harald Malmgren at Sandia or Los Alamos, and Richard Bissell
briefed Malmgren afterwards. `michels-corpus-06.md` 04 / 1:16:46 has Matthew Pines
naming "the main belly button on all things nuclear in the military";
`michels-corpus-09.md` 03 / 1:12:28 to 1:15:54 and `michels-corpus-10.md` 4 / 0:52:53
carry the debris briefing; `michels-corpus-15.md` 02 / 0:31:03 repeats it. The corpus
spells the surname `Geis`, `Geiss`, `Hughes`, `Keys` and `Guy` across single transcripts,
which is itself the corruption tell the triage flagged.

**What the records say.**

The *Official Register of the United States 1957*, compiled by the United States Civil
Service Commission under Public No. 387, 74th Congress, lists persons in administrative
and supervisory positions "as of May 1, 1957". Page 629, under UNITED STATES ATOMIC
ENERGY COMMISSION, DIVISION OF MILITARY APPLICATION:

| Name | Official title and station | Legal residence | Salary |
|---|---|---|---|
| Brig. Gen. Alfred D. Starbird, USA | Director | Vt | (footnoted) |
| Col. Carey L. O'Bryan, Jr., USAF | Deputy Director | Okla 4th | (footnoted) |
| Lawrence P. Gise | Assistant Director | Va 10th | 14,190 |
| Glen W. Wiltrout | Chief, Administrative Management Branch | W. Va. 3d | 11,610 |

The *Official Register of the United States 1959*, same compiler, same statutory basis,
"as of May 1, 1959". Page 134, under DEPARTMENT OF DEFENSE, OTHER ACTIVITIES, ADVANCED
RESEARCH PROJECTS AGENCY:

| Name | Official title and station | Legal residence | Salary |
|---|---|---|---|
| Roy W. Johnson | Director | Conn 4th | $19,000 |
| George P. Sutton | Chief Scientist | Calif 22d | (footnoted) |
| Rear Adm. John E. Clark, USN | Deputy Director | Fla 3d | (footnoted) |
| Lawrence P. Gise | Assistant Director, Administration | Va 10th | 17,500 |
| John E. Lynch | Administrative Officer | N.Y. 34th | 6,135 |
| William H. Godel | Director, Policy and Planning Division | | 16,095 |
| Nicholas E. Golovin | Technical Operations Division | Md 6th | 17,000 |

The page footnote reads "Station is Washington, D.C. unless otherwise indicated." Gise
appears once in each volume. He is not in the 1959 volume's AEC section, and he is not
in the 1957 volume's Defense section.

The third record is *DNA 6005F, PLUMBBOB SERIES 1957*, "United States Atmospheric
Nuclear Weapons Tests, Nuclear Test Personnel Review, Prepared by the Defense Nuclear
Agency as Executive Agency for the Department of Defense", published 1981 and served by
govinfo. Its reference list carries two Gise items:

> 152. Gise, L. [Memorandum for Test Manager, Subject: AEC Unofficial Observers, with
> Attachment.] Washington, DC: AEC, Division of Military Application. 08/27/57. 4 pages.

> 153. Gise, L.P., Ass't Director, DMA. [Memo to: R.F. Hertford, Manager, ALOO, Subject:
> USAF-AEC Agreement on Use of Lookout Mountain Lab at (29-2)-383, w/encl.] Washington,
> DC: Atomic Energy Commission, DMA. 04/30/57. 29 pages. AT292383.

That is an independent confirmation of the Register's title, from a DoD report, and it
is the reason the identification is safe rather than a name match. It also settles the
Albuquerque question against the transcript for 1957: reference 202 of the same list is
"Hertford, K., Manager, Albuquerque Operations. [Memorandum to Test Manager...]", so the
ALOO Manager in 1957 was Hertford and Gise was writing to him from headquarters. The
report gives the initial two ways, "R.F." at 153 and "K." at 202; both are reproduced
here as printed and neither is resolved.

The Lookout Mountain subject line is worth the board's attention independently. DNA
6005F, at its section on photographic coverage, records that "The Lookout Mountain
Laboratory Group from Hollywood, California, staffed by the 1352nd Motion Picture
Squadron, Air Photographic and Charting Service, provided motion picture and still
photography coverage", that roughly 75,000 feet of colour motion picture film was shot,
and that "Laboratory facilities established at the test site made it possible to
process, classify, and release coverage to the press within two hours after each
detonation." Gise's 30 April 1957 memorandum is about the agreement under which the Air
Force's classified film unit was used by the AEC.

**What the transcripts claim that these records do NOT establish.**

| Transcript claim | State after this pass |
|---|---|
| Gise headed the AEC Albuquerque Operations Office | NOT OPENED. Nothing opened here places him at ALOO in any role. In 1957 the post was Hertford's. The Official Register series ends with the 1959 volume, so it cannot reach the 1960s at all |
| He took custody of Bluegill Triple Prime material in 1962 | NOT OPENED, and nothing opened here is later than 1959 |
| He briefed Harald Malmgren at Sandia or Los Alamos | NOT OPENED |
| He refused to brief Malmgren because Naval Intelligence controlled the detail | NOT OPENED |
| He is Jeff Bezos's maternal grandfather | NOT OPENED. This is in no record read here, and it is the one element every guest states with confidence |
| He was at ARPA 1958 to 1961 | PARTLY. The 1 May 1959 snapshot is documented. The start and end dates are not |

**A trap for the next session.** `govinfo` full text returns "Lawrence P. Gise, Jr." in
the Congressional Record for 31 March 1958, in a Senate list of service academy
appointments. That is a different person, almost certainly a son, and it is the first
result the search returns. Do not build a claim on it.

**Tier: T1** for both Official Register lines and for the DNA 6005F reference entries,
each being a federal publication stating its own content. **NOT GRADEABLE** for
everything in the transcripts.

**BOARD RECOMMENDATION: yes, a new node, built only on the two offices.** The value to
this board is not the debris story. It is that a single named administrator sat in the
AEC office that owned nuclear weapons work and then in the Defense Department's own
advanced research agency two years later, and that his surviving paper is about the use
of a classified Air Force film laboratory. Build that. Leave 1962 off entirely.

Sources opened:

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952/pdf/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952.pdf | *Official Register of the United States 1957*, US Civil Service Commission, 946 pages. Gise at printed page 629, PDF page 649. Text layer present |
| https://www.govinfo.gov/content/pkg/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff/pdf/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff.pdf | *Official Register of the United States 1959*, 920 pages. Gise at printed page 134, PDF page 156. Page rendered and read to confirm the salary column |
| https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222713/pdf/GOVPUB-D15-PURL-gpo222713.pdf | *DNA 6005F, PLUMBBOB SERIES 1957*, Defense Nuclear Agency, 316 pages. Cover rendered; reference list read from the text layer |

### Draft node

```json
{
  "id": "lawrence-p-gise",
  "cls": "person",
  "label": "Lawrence P. Gise",
  "sub": "AEC Division of Military Application Assistant Director 1957; ARPA Assistant Director, Administration 1959",
  "cluster": "nuclear",
  "tier": "B",
  "C": 3, "A": 2, "D": 2,
  "date": null,
  "loc": "Washington, DC",
  "domains": ["d-nuclear", "d-structure", "d-custody"],
  "desc": "A career federal administrator who sat, two years apart, in the Atomic Energy Commission office that owned military nuclear applications and in the Defense Department's own advanced research agency. The Official Register of the United States, a statutory annual list of federal administrative officers, places him in both. He is named across the Michels podcast corpus as the custodian of material said to have been recovered from a 1962 nuclear test; nothing in any record opened for this node reaches 1962, and the Albuquerque post the corpus assigns him was held by another man in the year his own paper is dated.",
  "claims": [
    {
      "tier": 1,
      "text": "The Official Register of the United States 1957 lists 'Lawrence P. Gise' as 'Assistant Director' of the UNITED STATES ATOMIC ENERGY COMMISSION, DIVISION OF MILITARY APPLICATION, legal residence Va 10th, salary 14,190, at printed page 629. The volume states it lists persons in administrative and supervisory positions 'as of May 1, 1957'.",
      "source": "Official Register of the United States 1957, US Civil Service Commission, p.629, https://www.govinfo.gov/content/pkg/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952/pdf/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952.pdf"
    },
    {
      "tier": 1,
      "text": "The Official Register of the United States 1959 lists 'Lawrence P. Gise' as 'Assistant Director, Administration' of the ADVANCED RESEARCH PROJECTS AGENCY under DEPARTMENT OF DEFENSE, legal residence Va 10th, salary 17,500, at printed page 134, under a footnote reading 'Station is Washington, D.C. unless otherwise indicated.' The volume lists positions 'as of May 1, 1959'. The same page lists Roy W. Johnson as Director and William H. Godel as Director, Policy and Planning Division.",
      "source": "Official Register of the United States 1959, US Civil Service Commission, p.134, https://www.govinfo.gov/content/pkg/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff/pdf/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff.pdf"
    },
    {
      "tier": 1,
      "text": "DNA 6005F, the Defense Nuclear Agency's Nuclear Test Personnel Review volume on Operation PLUMBBOB, cites at reference 153 'Gise, L.P., Ass't Director, DMA. [Memo to: R.F. Hertford, Manager, ALOO, Subject: USAF-AEC Agreement on Use of Lookout Mountain Lab at (29-2)-383, w/encl.] Washington, DC: Atomic Energy Commission, DMA. 04/30/57. 29 pages. AT292383.' Reference 152 cites a further Gise memorandum for the Test Manager, subject 'AEC Unofficial Observers', dated 08/27/57.",
      "source": "DNA 6005F, PLUMBBOB SERIES 1957, Defense Nuclear Agency, references 152 and 153, https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222713/pdf/GOVPUB-D15-PURL-gpo222713.pdf"
    },
    {
      "tier": 1,
      "text": "The same reference list names the Manager of the Albuquerque Operations Office in 1957 as Hertford, at reference 202, 'Hertford, K., Manager, Albuquerque Operations'. Gise's own 1957 memorandum is addressed to that office from AEC headquarters, not written from it.",
      "source": "DNA 6005F, PLUMBBOB SERIES 1957, references 153 and 202, https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222713/pdf/GOVPUB-D15-PURL-gpo222713.pdf"
    },
    {
      "tier": 2,
      "text": "Four guests across five Michels lead maps describe Gise as head of the AEC's Albuquerque Operations Office and as the man who handed anomalous material from the 1962 Bluegill Triple Prime test to Harald Malmgren. No document number is cited by any speaker for any part of the chain, and no record opened for this node is dated later than 1959.",
      "source": "michels-corpus-06.md file 04 at 1:16:46; michels-corpus-09.md file 03 at 1:12:28 to 1:15:54; michels-corpus-10.md file 4 at 0:52:53; michels-corpus-15.md file 02 at 0:31:03"
    }
  ],
  "sources": [
    { "name": "Official Register of the United States 1957, US Civil Service Commission", "url": "https://www.govinfo.gov/content/pkg/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952/pdf/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952.pdf", "date": "1957-05-01" },
    { "name": "Official Register of the United States 1959, US Civil Service Commission", "url": "https://www.govinfo.gov/content/pkg/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff/pdf/GOVPUB-CS1-301ae7b075ad3435b3a7dca00e78e8ff.pdf", "date": "1959-05-01" },
    { "name": "DNA 6005F, PLUMBBOB SERIES 1957, Defense Nuclear Agency", "url": "https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222713/pdf/GOVPUB-D15-PURL-gpo222713.pdf", "date": "1981-01-01" }
  ],
  "edges": [
    {
      "a": "lawrence-p-gise", "b": "darpa", "type": "institutional", "claimTier": 1,
      "label": "held the ARPA post of Assistant Director, Administration",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "The Official Register of the United States 1959 places him in that post as of 1 May 1959, on the same page as Director Roy W. Johnson."
    },
    {
      "a": "lawrence-p-gise", "b": "doe", "type": "institutional", "claimTier": 2,
      "label": "held an AEC headquarters post in the line the DOE node records itself as succeeding",
      "dateStart": "1957", "dateEnd": "1957",
      "note": "The Register documents the AEC Division of Military Application post at Tier 1; the succession from AEC to DOE is the board's own doe node, so the edge itself is an inference and is graded accordingly."
    }
  ]
}
```

---

## 12. Project SILVER BUG, Avro Project Y, John Frost

**VERDICT: CONFIRMED as a document, at primary level, on every element of the record.
The transcript's framing of it is CONTRADICTED by the report's own summary. John Frost
is NOT OPENED.**

**What the transcript claims.** `michels-corpus-13.md` 3 / 2:05:33 to 2:09:51 frames
"Project Y / Silverbug (Avro Car programme)" as "publicly a 'joke' project (the Avrocar,
ground-effect saucer) that failed aerodynamically, but allegedly used as a funnel/cover
to recruit German scientists and fund deeper theoretical-physics work" at Wright Field.
The same file names John Frost as running the project "for British Aircraft interests",
Henri Coanda as a consultant, Richard Miethe as a worker on it, and Victor Schauberger
as a target of the recruiters.

**What the document says.** The joint report was downloaded from The Black Vault as
`AFD-070114-006.pdf`, 31 pages, an image scan with no text layer. Pages 1 to 9, 24, 25,
30 and 31 were rendered and read.

The title page reads, top to bottom: "TECHNICAL REPORT", then a plate carrying
"TR-AC-47", "(Unclassified)", "JOINT ATIC-WADC REPORT ON", "PROJECT SILVER BUG",
"PROJECT NO. 9961", "15 FEBRUARY 1955", and below the Department of the Air Force seal,
"AIR TECHNICAL INTELLIGENCE CENTER / WRIGHT-PATTERSON AIR FORCE BASE / OHIO". Handwritten
across the plate is a declassification stamp: "Declassified 29 MAR 95", "Auth: DoD
5200.1.R", "SAF/AAZD", a signature, and a rank line. Interior pages carry an
"UNCLASSIFIED" stamp with an obliterated marking beside it. The printing code "T55-2049"
appears in the page footers.

Page iii, SUMMARY. Under **Purpose**: "This report presents factual technical data on
A. V. Roe, Canada, Limited, proposed development, Project Y2 (Secret). This proposal is
the second of two designs which can be classified as radical aircraft designs. The
ultimate purpose of presenting this is two-fold; to correct the distorted picture
presented in previous releases, both classified and unclassified, and to acquaint the
intelligence community with the current state-of-the-art facts thereby alerting them to
any air intelligence information which may become available indicating Soviet interest
in this specialized field."

Under **Factual Data**: "Several news mediums have published articles concerning A. V.
Roe, Canada, Limited, Project Y2 (Secret) which, when supplemented by the December Air
Intelligence Digest article, 'The Flying Disc', present an inaccurate picture of the
proposed project."

Under **Discussion**: the contractor is "AVRO Aircraft, Limited, a member of the
Hawker-Siddley Group", and "This project should in no way be associated with any science
fiction or 'Flying Saucer' stories because of its external appearance. The configuration
was a result of an engineering investigation into the solution of a particular problem."

Under **Conclusions**: "This proposal offers a possible solution to the USAF requirement
for achieving dispersed base operations", followed by a two-part intelligence programme,
part b of which is "A collection effort should be initiated to determine whether the
Soviet Bloc is or has been conducting research efforts on a similar project, when this
work began, and the present state of the Soviet development."

Page 1, Section I A Background, gives the requirement as dispersed base operation
against "the growing and possibly catastrophic vulnerability of conventional air bases".
Section I B 1 separates the two designs: "Two versions of small research VTO aircraft
have been designed by the contractor, which, by company designation, are Project Y
(Secret), a 'tail-sitter', and Project Y2 (Secret), a 'flat-riser'. Early in the
investigation, Project Y (Secret) was rejected by the contractor in favor of the
flat-riser."

Page 17, Section I C Performance: "The performance estimated by the contractor was based
on rather broad assumptions and has not as yet been investigated by a wind tunnel test
program." Page 22, TABLE III, CONTRACTOR ESTIMATED PERFORMANCE, Radial-Flow Engine
Aircraft:

| Particular | Without reheat | With 1500 degrees K reheat |
|---|---|---|
| Maximum level speed, mph | 1,720 | 2,300 |
| Maximum level speed, knots | 1,490 | 2,000 |
| Mach No. | 2.6 | 3.48 |
| Ceiling, ft (max power at mean wt) | 71,600 | 80,600 |
| Still air range, miles | 620 | NA |
| Take-off and landing distances | Nil | Nil |
| Max hovering alt at mean wt, 26,000 lbs | 18,000 ft | NA |

Page 23, Section II, USAF RESEARCH AND DEVELOPMENT STATUS, dates the Air Force side
exactly: "Headquarters USAF directed that Headquarters ARDC would issue a technical
requirement to pursue investigation of this project. This resulted in Technical
Requirement No. 3 dated 13 August 1954, which in turn resulted in a development plan
dated 15 September 1954, written by WADC, Directorate of Weapons Systems Operations,
Bombardment Aircraft Division, New Development Office. Work on this project was delayed
pending a decision by higher headquarters. On 29 December 1954 the order to proceed with
this project was issued. The proposed statement of work dated 8 November 1954 will be
incorporated in a study contract in the near future." Five problem areas are listed
before development could proceed, the fifth being "The radial-flow engine feasibility."

**What the transcript claims that the document does NOT establish.**

| Transcript claim | State after this pass |
|---|---|
| The programme was a funnel and cover for deeper theoretical physics | CONTRADICTED in tone and in purpose by the report's own summary, which exists to correct exaggerated accounts and to prime collection against Soviet interest. A document cannot prove the absence of a cover, but this is the cited record and it says the opposite of what it is cited for |
| John Frost ran it for British Aircraft interests | NOT OPENED. Frost is named in no page read here. The report names no individual designer at all |
| Henri Coanda was a consultant on it | NOT ESTABLISHED. The report names the **effect**, not the man: Figure 15 is "Coanda Effect: High Aspect Ratio Jet Bending", and page 17 describes "the so-called 'Coanda effect' whereby a jet stream is deflected through large angles by having a curved surface in contact with its edge at one side" |
| British Aircraft Corporation was involved | CONTRADICTED. The report names "A. V. Roe, Canada, Limited" and "AVRO Aircraft, Limited, a member of the Hawker-Siddley Group". BAC did not exist in 1955 |
| It is the Avrocar | CONFLATION. TR-AC-47 describes a supersonic circular-planform VTO research aircraft with a radial-flow engine. The Avrocar belongs to the later USAF Project 1794 record, which is a separate set of documents |

**The Project 1794 half of the lead was also opened, at listing level only.** The
National Declassification Center's own post records the release: "RG 342: Records of
U.S. Air Force Commands, Activities, and Organizations, Entry UD-UP 138, Research and
Development Project Files, compiled 01/01/1952 to 12/31/1969", naming "Project 1794
Final Development Summary Report, June 1956 (ARC ID 6920770)" and "Program Planning
Report, Project 1794 Extension Program, April 1957 (ARC ID 6981836)", declassified by
the Air Force in June 2001 and processed by the NDC in 2012. The Black Vault's mirror
page lists four PDFs, the largest being "Project Planning Report Project 1794 Final
Development Report", 2 April to 30 May 1956, 116 pages. **Those PDFs were not opened.**
`catalog.archives.gov` returned empty content to WebFetch for both the record page and
the API, so the NARA catalogue records themselves are NOT OPENED.

**Tier: T1** for everything read off TR-AC-47. **T2** for the Project 1794 titles, dates
and record group, which come from an archives.gov blog post and a Black Vault index
page rather than from the documents. **NOT GRADEABLE** for Frost.

**BOARD RECOMMENDATION: yes, a new node, as a document.** The candidates file classes
this as a program. What was opened is a report, and the report is the thing worth
carrying: a joint ATIC and WADC study of a foreign contractor's disc-shaped supersonic
aircraft, written at the board's central custody location, whose stated purpose is to
tell the intelligence community what the real state of the art was because previous
releases had distorted it. That is the control case any Wright-Patterson recovery claim
has to clear, and it also gives the board a dated Air Force document using the phrase
"Flying Saucer" to dismiss a resemblance. Build the document node. If a programme node
is wanted later, build it from the Project 1794 files after somebody opens them.

Sources opened:

| URL | What is at it |
|---|---|
| https://documents.theblackvault.com/documents/SilverBug/AFD-070114-006.pdf | TR-AC-47, JOINT ATIC-WADC REPORT ON PROJECT SILVER BUG, Project No. 9961, 15 February 1955, 31 pages, image scan. Pages 1 to 9, 24, 25, 30 and 31 rendered and read |
| https://www.theblackvault.com/documentarchive/project-silver-bug/ | The Black Vault index page hosting it; gives the file designation AFD-070114-006 |
| https://declassification.blogs.archives.gov/2013/01/30/project-1794-documents-in-arc/ | National Declassification Center post naming the Project 1794 records, their record group and series, and their ARC identifiers |
| https://www.theblackvault.com/documentarchive/project-1794-saucer-type-aircraft/ | The Black Vault index of four Project 1794 PDFs with titles, dates and page counts. The PDFs themselves were not opened |

### Draft node

```json
{
  "id": "tr-ac-47-silver-bug",
  "cls": "document",
  "label": "TR-AC-47, Joint ATIC-WADC Report on Project Silver Bug, 15 February 1955",
  "sub": "Air Technical Intelligence Center, Wright-Patterson AFB; Project No. 9961; declassified 29 March 1995",
  "cluster": "aerospace",
  "tier": "B",
  "C": 2, "A": 1, "D": 2,
  "dateStart": "1955-02-15",
  "dateEnd": "1955-02-15",
  "domains": ["d-aerospace", "d-prop", "d-intel", "d-secrecy"],
  "desc": "A joint report of the Air Technical Intelligence Center and the Wright Air Development Center on a Canadian contractor's proposal for a supersonic circular-planform aircraft with vertical take-off. It is the cleanest documented instance on this board of the Air Force funding a disc-shaped aircraft at Wright-Patterson, and its own stated purpose is to stop the intelligence community from believing the exaggerated accounts already circulating about it. It is the control case any Wright-Patterson recovery claim has to clear, and it is cited in the Michels corpus for the opposite of what it says.",
  "claims": [
    {
      "tier": 1,
      "text": "The title page reads 'TR-AC-47 / (Unclassified) / JOINT ATIC-WADC REPORT ON / PROJECT SILVER BUG / PROJECT NO. 9961 / 15 FEBRUARY 1955', issued by the 'AIR TECHNICAL INTELLIGENCE CENTER, WRIGHT-PATTERSON AIR FORCE BASE, OHIO', and carries a handwritten declassification stamp reading 'Declassified 29 MAR 95', 'Auth: DoD 5200.1.R', 'SAF/AAZD'.",
      "source": "TR-AC-47 title page, rendered from the scan at https://documents.theblackvault.com/documents/SilverBug/AFD-070114-006.pdf"
    },
    {
      "tier": 1,
      "text": "The report's Summary states its purpose: 'This report presents factual technical data on A. V. Roe, Canada, Limited, proposed development, Project Y2 (Secret)... The ultimate purpose of presenting this is two-fold; to correct the distorted picture presented in previous releases, both classified and unclassified, and to acquaint the intelligence community with the current state-of-the-art facts thereby alerting them to any air intelligence information which may become available indicating Soviet interest in this specialized field.'",
      "source": "TR-AC-47, page iii, Summary, Purpose"
    },
    {
      "tier": 1,
      "text": "The Summary's Discussion section states: 'This project should in no way be associated with any science fiction or \"Flying Saucer\" stories because of its external appearance. The configuration was a result of an engineering investigation into the solution of a particular problem.' It names the contractor as 'AVRO Aircraft, Limited, a member of the Hawker-Siddley Group'.",
      "source": "TR-AC-47, page iii, Summary, Discussion"
    },
    {
      "tier": 1,
      "text": "Section I distinguishes the two company designations: 'Two versions of small research VTO aircraft have been designed by the contractor, which, by company designation, are Project Y (Secret), a \"tail-sitter\", and Project Y2 (Secret), a \"flat-riser\". Early in the investigation, Project Y (Secret) was rejected by the contractor in favor of the flat-riser.'",
      "source": "TR-AC-47, page 1, Section I B 1, General Description"
    },
    {
      "tier": 1,
      "text": "Table III, 'CONTRACTOR ESTIMATED PERFORMANCE, Radial-Flow Engine Aircraft', gives Mach 2.6 and a 71,600 ft ceiling without reheat and Mach 3.48 and an 80,600 ft ceiling with 1500 degrees K reheat. The report qualifies these on page 17: 'The performance estimated by the contractor was based on rather broad assumptions and has not as yet been investigated by a wind tunnel test program.'",
      "source": "TR-AC-47, pages 17 and 22"
    },
    {
      "tier": 1,
      "text": "Section II dates the USAF development track: Technical Requirement No. 3 dated 13 August 1954, a development plan dated 15 September 1954 written by 'WADC, Directorate of Weapons Systems Operations, Bombardment Aircraft Division, New Development Office', an order to proceed issued 29 December 1954, and a proposed statement of work dated 8 November 1954 to be incorporated in a study contract.",
      "source": "TR-AC-47, page 23, Section II B, Present Development Status"
    }
  ],
  "sources": [
    { "name": "TR-AC-47, Joint ATIC-WADC Report on Project Silver Bug, Project No. 9961, 15 February 1955 (Air Force file AFD-070114-006)", "url": "https://documents.theblackvault.com/documents/SilverBug/AFD-070114-006.pdf", "date": "1955-02-15" },
    { "name": "The Black Vault document archive index, Project Silver Bug", "url": "https://www.theblackvault.com/documentarchive/project-silver-bug/", "date": "2026-09-02" },
    { "name": "National Declassification Center, 'Project 1794 Documents in ARC'", "url": "https://declassification.blogs.archives.gov/2013/01/30/project-1794-documents-in-arc/", "date": "2013-01-30" }
  ],
  "edges": [
    {
      "a": "tr-ac-47-silver-bug", "b": "atic", "type": "institutional", "claimTier": 1,
      "label": "one of the two issuing organisations, and the one on the title page imprint",
      "dateStart": "1955", "dateEnd": "1955",
      "note": "The title page carries the Air Technical Intelligence Center imprint and the report's own conclusion asks for 'direct liaison between WADC and ATIC personnel'."
    },
    {
      "a": "tr-ac-47-silver-bug", "b": "l-wright-patterson", "type": "geographic", "claimTier": 1,
      "label": "written and issued at Wright-Patterson Air Force Base, Ohio",
      "dateStart": "1955", "dateEnd": "1955",
      "note": "Both issuing bodies, ATIC and the Wright Air Development Center, are named on the report with that station."
    },
    {
      "a": "tr-ac-47-silver-bug", "b": "usaf", "type": "programmatic", "claimTier": 1,
      "label": "records the Air Force research and development status of the disc-aircraft proposal",
      "dateStart": "1954", "dateEnd": "1955",
      "note": "Section II names Technical Requirement No. 3 of 13 August 1954 and the order to proceed of 29 December 1954, so the Air Force interest is dated by the document rather than inferred."
    },
    {
      "a": "tr-ac-47-silver-bug", "b": "d-denial", "type": "denial", "claimTier": 1,
      "label": "a dated Air Force document dismissing the flying-saucer resemblance of an aircraft it was itself funding",
      "dateStart": "1955", "dateEnd": "1955",
      "note": "The Summary's 'should in no way be associated with any science fiction or \"Flying Saucer\" stories' is a denial with an author, a date and a subject, which is what this board's denial domain exists to hold."
    }
  ]
}
```

---

## 13. Andrija Puharich

**VERDICT: PARTLY CONFIRMED.** Two patents and one federal investigative record were
opened and all three name him. The AEC grant, the CIA and Navy funding, and the Israel
movements file are NOT OPENED.

**What the transcript claims.** `michels-corpus-21.md` file 21-2 throughout, with Greg
Milazzi: Puharich's Round Table Foundation in Maine was funded by Army, Navy and CIA
money from about 1948 to 1957; his company Intelectron received "a $300,000 grant" from
the Atomic Energy Commission in the early 1960s, with AEC personnel visiting to test his
hearing-transmission device (0:44:10, 0:47:45); Intelectron developed the "TD-100"
device, demonstrated at the Pentagon (1:00:20 to 1:02:10); the filmmakers obtained an
FBI file on his movements in Israel by FOIA (1:15:57); and a 1973 document exists in his
archive addressed from SRI to "Lab Nine" at Ossining (2:06:29). The triage row names as
the record to open "His own US patents on hearing-transmission devices; an AEC grant to
Intelectron; his Army service record; an FBI file".

**What the records say.**

**US Patent 2,995,633**, front page and specification read from the USPTO scan. Header:
"Aug. 8, 1961 / H. K. PUHARICH ET AL / MEANS FOR AIDING HEARING / 2,995,633 / Filed
Sept. 25, 1958 / 2 Sheets-Sheet 1", with the drawing sheet signed "INVENTORS HENRY K.
PUHARICH, JOSEPH L. LAWRENCE". The specification head reads: "United States Patent
Office 2,995,633, Patented Aug. 8, 1961 / MEANS FOR AIDING HEARING / Henry K. Puharich,
[street address omitted], and Joseph L. Lawrence, [street address omitted], both of New York,
N.Y. / Filed Sept. 25, 1958, Ser. No. 763,406 / 5 Claims. (Cl. 179-107)". **No assignee
is named on the face of the patent.** The invention is described as effecting "the
transmission of sound signals through the dental structure and facial nervous system of
the user", and "in its most advantageous and practical form, the device of the invention
comprises means, in the form of a dental prosthetic device, for imparting or
transmitting to viable nerves of a tooth electrical signals which, when transmitted to
the brain, will give rise to sound sensations."

**US Patent 3,170,993**, specification head read from the USPTO scan: "United States
Patent Office 3,170,993, Patented Feb. 23, 1965 / MEANS FOR AIDING HEARING BY ELECTRICAL
STIMULATION OF THE FACIAL NERVE SYSTEM / Henry K. Puharich, [street address omitted], Ossining,
N.Y., and Joseph L. Lawrence, [street address omitted], New York, N.Y. / Filed Jan. 8,
1962, Ser. No. 164,882 / 24 Claims. (Cl. 179-107)". Again **no assignee**. It opens by
citing the earlier patent: "In our prior United States Patent No. 2,995,633, granted
August 8, 1961, there is disclosed a fundamentally novel arrangement for assisting the
hearing process of the human body through electrical stimulation of the facial nerve
system of a user, employing modulated electrical signals corresponding to audible
sounds." The improvement is a radio frequency receiver whose audio-modulated output is
capacitively coupled to the nerve circuit "which involves the use of one or more
cup-shaped dental caps".

**FBI Office Memorandum, 6 September 1957.** Located by searching the FBI Vault, which
returns five items for "puharich"; the one that contains him is the release titled
"Extra-Sensory Perception Part 01 (Final)", described by the Vault as "cross references
to ESP found in FBI files from 1957 to 1960". The memorandum is at PDF pages 13 and 14
of a 40-page release. Its header: "Office Memorandum, UNITED STATES GOVERNMENT / TO:
MR. A. H. BELMONT / FROM: MR. R. R. ROACH / DATE: September 6, 1957 / SUBJECT: EXTRA
SENSORY PERCEPTION DEMONSTRATION BY MR. WILLIAM FOOS, AUGUST 8, 1957". It was
classified CONFIDENTIAL, the marking is struck through, and a handwritten annotation
records "DECLASSIFIED BY SP-11 ON 2-16-88 per Dept of Army letter dated 2-9-88". The
file number stamped at the foot is 62-4036.

Page 1 of the memorandum names "Lieutenant Colonel John Downie, Special Operations
Branch, ACSI", the office of the Assistant Chief of Staff, Intelligence, Department of
the Army. Page 2 carries the passage that names Puharich:

> Attached hereto also is a copy of a memorandum furnished by Colonel Downie relative to
> Dr. Henry K. Puharich, Round Table Foundation, Glen Cove, Maine. While Dr. Puharich's
> work is not exactly in the field of extra sensory perception, Colonel Downie stated
> that the Army is interested in determining the possibilities of his techniques.

The enclosure itself is not in the release; the memorandum's foot records "Enclosures"
with the count redacted.

**What the transcript claims that these records do NOT establish.**

| Transcript claim | State after this pass |
|---|---|
| An AEC grant of $300,000 to Intelectron | NOT OPENED, and no route to it was found. `cia.gov/readingroom` is 403 from here and the OSTI OpenNet search interface returns 404 at every URL tried. Note that at least one secondary account attributes the same $300,000 to three private New York businessmen rather than to the AEC; neither version is verified here, and the discrepancy is a reason to open the record before carrying either |
| Intelectron built the patented device | NOT ESTABLISHED. Neither patent carries an assignee. On their faces these are personal inventions of Puharich and Lawrence |
| CIA and Navy funded the Round Table Foundation | NOT OPENED. The FBI memorandum documents Army interest and nothing more. The CIA appears in the same memorandum only in connection with William Foos |
| The Round Table Foundation was at Rockland, Maine | The FBI record says "Glen Cove, Maine". Use the record's spelling |
| The TD-100 was demonstrated at the Pentagon | NOT OPENED. Neither patent read here uses that designation |
| An FBI file on his movements in Israel | NOT OPENED. The Vault search returns no such release; the claim is that the filmmakers hold a FOIA copy, which is not a public record this session can reach |
| Puharich is the agency-funded predecessor of SRI and STAR GATE | NOT ESTABLISHED by anything opened. No edge to `l-sri` or `stargate-program` is drafted below for that reason |

**Tier: T1** for both patents and for the FBI memorandum, each read on its own face.
**NOT GRADEABLE** for the funding claims.

**BOARD RECOMMENDATION: yes, a new node, on the three documents only.** The board grep
for "Puharich" returns zero. What the opened records give is narrower and harder than the
transcript: a physician who patented a way to put audio into a person's head through the
teeth, and whose private foundation the Army's intelligence staff was interested in by
1957, on paper, in a memorandum written to the FBI's Assistant Director. That is enough
for a node in the research cluster. Everything about the Nine, the space kids and the
Israeli threads stays off it.

Sources opened:

| URL | What is at it |
|---|---|
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/2995633 | US Patent 2,995,633, "Means for aiding hearing", 5 pages, image scan. Drawing sheet 1 and specification column 1 rendered and read |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3170993 | US Patent 3,170,993, "Means for aiding hearing by electrical stimulation of the facial nerve system", 10 pages, image scan. Specification head rendered and read |
| https://vault.fbi.gov/Extra-Sensory%20Perception/Extra-Sensory%20Perception%20Part%2001%20%28Final%29/view | FBI Vault release "Extra-Sensory Perception Part 01 (Final)", 40 pages. The Roach to Belmont memorandum of 6 September 1957 is at PDF pages 13 and 14 and was rendered and read |

### Draft node

```json
{
  "id": "andrija-puharich",
  "cls": "person",
  "label": "Andrija (Henry K.) Puharich",
  "sub": "Physician and inventor; patented dental and facial-nerve hearing transmission; Round Table Foundation, Glen Cove, Maine",
  "cluster": "research",
  "tier": "C",
  "C": 4, "A": 2, "D": 2,
  "date": null,
  "loc": "Ossining, New York",
  "domains": ["d-research", "d-consciousness", "d-medical"],
  "desc": "A physician who patented, with Joseph L. Lawrence, a means of producing the sensation of hearing by delivering modulated electrical signals to the nerve endings of a tooth, bypassing the ear entirely. The second patent adds a radio frequency receiver capacitively coupled to that nerve circuit through dental caps. Separately, an FBI memorandum of September 1957 records the Army's Assistant Chief of Staff, Intelligence, taking an interest in his techniques at his private foundation in Maine. He is named across three Michels lead maps as the agency-funded predecessor of the later remote-viewing work; none of that funding is documented by anything opened for this node.",
  "claims": [
    {
      "tier": 1,
      "text": "US Patent 2,995,633, 'MEANS FOR AIDING HEARING', names 'Henry K. Puharich, [street address omitted], and Joseph L. Lawrence, [street address omitted], both of New York, N.Y.', filed 25 September 1958 as Ser. No. 763,406, patented 8 August 1961, 5 claims, Cl. 179-107. No assignee appears on the face of the patent.",
      "source": "US Patent 2,995,633, specification head, read off the USPTO image server at https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/2995633"
    },
    {
      "tier": 1,
      "text": "The 1961 patent describes the invention as effecting 'the transmission of sound signals through the dental structure and facial nervous system of the user', and states that 'in its most advantageous and practical form, the device of the invention comprises means, in the form of a dental prosthetic device, for imparting or transmitting to viable nerves of a tooth electrical signals which, when transmitted to the brain, will give rise to sound sensations.'",
      "source": "US Patent 2,995,633, columns 1 and 2"
    },
    {
      "tier": 1,
      "text": "US Patent 3,170,993, 'MEANS FOR AIDING HEARING BY ELECTRICAL STIMULATION OF THE FACIAL NERVE SYSTEM', names 'Henry K. Puharich, [street address omitted], Ossining, N.Y., and Joseph L. Lawrence', filed 8 January 1962 as Ser. No. 164,882, patented 23 February 1965, 24 claims. It cites the 1961 patent as prior work by the same inventors and adds a radio frequency receiver whose audio-modulated output is capacitively coupled to the nerve circuit through 'one or more cup-shaped dental caps'. No assignee appears on the face of the patent.",
      "source": "US Patent 3,170,993, specification head and columns 1 and 2, read off the USPTO image server at https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3170993"
    },
    {
      "tier": 1,
      "text": "An FBI Office Memorandum from R. R. Roach to A. H. Belmont, dated 6 September 1957, file 62-4036, subject 'EXTRA SENSORY PERCEPTION DEMONSTRATION BY MR. WILLIAM FOOS, AUGUST 8, 1957', records: 'Attached hereto also is a copy of a memorandum furnished by Colonel Downie relative to Dr. Henry K. Puharich, Round Table Foundation, Glen Cove, Maine. While Dr. Puharich's work is not exactly in the field of extra sensory perception, Colonel Downie stated that the Army is interested in determining the possibilities of his techniques.' Colonel Downie is identified in the same memorandum as 'Lieutenant Colonel John Downie, Special Operations Branch, ACSI'. The memorandum was classified CONFIDENTIAL and carries a handwritten declassification annotation dated 16 February 1988.",
      "source": "FBI Vault release 'Extra-Sensory Perception Part 01 (Final)', PDF pages 13 and 14, https://vault.fbi.gov/Extra-Sensory%20Perception/Extra-Sensory%20Perception%20Part%2001%20%28Final%29/view"
    },
    {
      "tier": 2,
      "text": "Three Michels lead maps, from three different guests, describe Puharich as funded across decades by Army, Navy, CIA and Atomic Energy Commission money, including a $300,000 AEC grant to his company Intelectron in the early 1960s. Neither patent read here names Intelectron as assignee, and no AEC grant record was reachable from this environment. The claim is carried here as a claim about what was said, not about what happened.",
      "source": "michels-corpus-21.md file 21-2 at 0:44:10 and 0:47:45 (Greg Milazzi); further mentions at michels-corpus-23.md file 01 1:57:10 and michels-corpus-25.md file 04 1:22:37"
    }
  ],
  "sources": [
    { "name": "US Patent 2,995,633, Means for aiding hearing", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/2995633", "date": "1961-08-08" },
    { "name": "US Patent 3,170,993, Means for aiding hearing by electrical stimulation of the facial nerve system", "url": "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3170993", "date": "1965-02-23" },
    { "name": "FBI Vault, Extra-Sensory Perception Part 01 (Final)", "url": "https://vault.fbi.gov/Extra-Sensory%20Perception/Extra-Sensory%20Perception%20Part%2001%20%28Final%29/view", "date": "1957-09-06" }
  ],
  "edges": [
    {
      "a": "andrija-puharich", "b": "dod", "type": "research", "claimTier": 1,
      "label": "the Army's intelligence staff recorded an interest in his techniques in 1957",
      "dateStart": "1957", "dateEnd": "1957",
      "note": "The FBI memorandum of 6 September 1957 attributes the interest to Lieutenant Colonel John Downie of the Special Operations Branch, Assistant Chief of Staff, Intelligence, Department of the Army; the enclosure Downie furnished is not in the release."
    },
    {
      "a": "andrija-puharich", "b": "d-consciousness", "type": "research", "claimTier": 1,
      "label": "the subject on which a federal agency file names him",
      "dateStart": "1957", "dateEnd": "1965",
      "note": "The FBI file that carries him is a release of cross references to extra-sensory perception, and his own patents are about routing sound into the nervous system without the ear."
    }
  ]
}
```

**Deliberate exclusion.** No edge to `l-sri`, `sri-international` or `stargate-program`
is drafted. The corpus asserts the lineage; nothing opened here documents it, and the
board already carries those nodes, so a speculative edge would render as sourced
structure. If a later pass opens the 1973 SRI to Lab Nine document, the edge follows
from that.

---

## 14. Project A119

**VERDICT: CONFIRMED.** The report exists, was opened in full, and says what the lead
says it says. Two corrections: the date and the name.

**What the transcript claims.** `michels-corpus-24.md` 03 / 1:03:29 gives "Project A119,
1958: Plan to detonate a nuclear device on the Moon as a Cold War show of force; Carl
Sagan said to have held clearance and participated." The triage row adds a framing: "A
dated, denied-then-declassified USAF study whose existence was maintained as
non-existent for four decades... the participant's disclosure of it in an unclassified
fellowship application is a documented compartmentation breach."

**What the document says.** The Defense Documentation Center copy, AD 425380, was read
in full from the OCR text of the DTIC mirror on archive.org.

The title page: "AFSWC-TR-59-39 / TR 59-39 Vol I / HEADQUARTERS / AIR FORCE SPECIAL
WEAPONS CENTER / AIR RESEARCH AND DEVELOPMENT COMMAND / KIRTLAND AIR FORCE BASE, NEW
MEXICO / A STUDY OF LUNAR RESEARCH FLIGHTS / Vol I / L. Reiffel / ARMOUR RESEARCH
FOUNDATION / Illinois Institute of Technology". The command page names "Major General
Charles M. McCorkle, Commander", "Colonel Carey L. O'Bryan, Jr., Deputy Commander" and
"Colonel Leonard A. Eddy, Director, Research Directorate".

The report page: "(Unclassified Title) / A STUDY OF LUNAR RESEARCH FLIGHTS / by L.
Reiffel / With contributions by R. W. Benson, J. J. Brophy, I. Filosofo, N. S. Kapany,
D. Langford, W. E. Loewe, D. Mergerian, O. H. Olson, V. J. Raelson, **C. E. Sagan**, P.
N. Slater", dated **19 June 1959**, under "Project Number 5776-57853, Contract AF
29(601)-1164". The publication review is signed by O'Bryan as Deputy Commander.

The Abstract: "Nuclear detonations in the vicinity of the moon are considered in this
report along with scientific information which might be obtained from such explosions.
The military aspect is aided by investigation of space environment, detection of nuclear
device testing, and capability of weapons in space."

Chapter I, Introduction, is where the show-of-force reading is earned, in the report's
own words: "Among various possibilities, the detonation of a nuclear weapon on or near
the moon's surface has often been suggested. The motivation for such a detonation is
clearly threefold: scientific, military and political." And: "Obviously, however,
specific positive effects would accrue to the nation first performing such a feat as a
demonstration of advanced technological capability. It is also certain that, unless the
climate of world opinion were well-prepared in advance, a considerable negative reaction
could be stimulated."

The distribution list is the part with the most value to this board. Under HEADQUARTERS
USAF it lists AFOAT, AFTAC, AFCIN and others; under ARDC CENTERS it lists "WADD,
Wright-Patterson AFB, Ohio"; and under "ACC ACTIVITIES" it lists "US Atomic Energy
Commission, ATTN: Technical Reports Library (Mrs. J. O'Leary, **for DMA**), Wash 25, DC",
"President, Sandia Corporation, ATTN: Document Control Division, Sandia Base, NMex",
"Director, Los Alamos Scientific Laboratory", and "Director, Lawrence Radiation
Laboratory". Under the DoD entries it lists "Director, Advanced Research Projects
Agency, Department of Defense, ATTN: Ward Low, The Pentagon, Wash 25, DC".

**What the transcript and triage claim that the document does NOT establish.**

| Claim | State after this pass |
|---|---|
| "Project A119" | The string "A119" appears nowhere in the report. The document identifies itself only by report number and contract |
| Dated 1958, or May 1959 | CONTRADICTED. The report page is dated **19 June 1959**. The candidates file's "May 1959" is wrong |
| Carl Sagan held clearance and participated | PARTLY. "C. E. Sagan" is on the contributor list, and he appears three more times in the reference list and in the appendix rosters of the National Academy of Sciences WESTEX group and the AFNRC Panel on Extraterrestrial Life. His clearance status is not in the document |
| Denied then declassified, existence maintained as non-existent for four decades | NOT ESTABLISHED. The DDC copy read here carries UNCLASSIFIED markings on its cover pages and the title is expressly marked "(Unclassified Title)". No declassification stamp, downgrading instruction or distribution limitation appears in the OCR. Whatever the classification history was, this copy does not carry it |
| The fellowship-application disclosure is a documented compartmentation breach | NOT OPENED. That claim is about a separate document, a 1959 fellowship application, and nothing about it is in this report |

**Tier: T1** for everything above read off the report. **NOT GRADEABLE** for the
programme name, the classification history and the fellowship application.

**BOARD RECOMMENDATION: yes, a new node, as a document, not a programme.** The
candidates file classes it as a program. The record is a report, the report does not name
a programme, and this board's own rule is that a claim caps at what the opened record
states. What the report earns is real without the programme framing: an Air Force
laboratory at Kirtland paid a university research foundation to work out what could be
learned from detonating a nuclear weapon on the Moon, said in its own introduction that
one of the three motivations was political demonstration, and posted the result to the
AEC's Division of Military Application, to Sandia, to Los Alamos, to Livermore, to ARPA
and to Wright-Patterson.

Sources opened:

| URL | What is at it |
|---|---|
| https://archive.org/details/DTIC_AD0425380 | The DTIC mirror item for AD 425380, giving title, author, date and abstract |
| https://archive.org/download/DTIC_AD0425380/DTIC_AD0425380_djvu.txt | The full OCR text of the scanned report, 268,820 bytes, read for the title page, command page, abstract, Chapter I and the distribution list |

### Draft node

```json
{
  "id": "afswc-tr-59-39",
  "cls": "document",
  "label": "AFSWC TR-59-39 Vol I, A Study of Lunar Research Flights, 19 June 1959",
  "sub": "Air Force Special Weapons Center, Kirtland AFB; L. Reiffel, Armour Research Foundation; contributor C. E. Sagan; DDC AD 425380",
  "cluster": "nuclear",
  "tier": "B",
  "C": 3, "A": 1, "D": 2,
  "dateStart": "1959-06-19",
  "dateEnd": "1959-06-19",
  "domains": ["d-nuclear", "d-research", "d-astro"],
  "desc": "A contractor study for the Air Force Special Weapons Center on what could be learned from detonating a nuclear weapon on or near the Moon, and on what it would cost politically. Its own introduction names three motivations, scientific, military and political, and says plainly that a nation performing the feat first would accrue positive effects as a demonstration of advanced technological capability. It is carried on this board as an instrument rather than an anecdote: a dated federal record of a plan whose public existence was, for decades, a matter of assertion. Its distribution list also documents who in the nuclear weapons complex received it.",
  "claims": [
    {
      "tier": 1,
      "text": "The report is 'AFSWC-TR-59-39, TR 59-39 Vol I, A STUDY OF LUNAR RESEARCH FLIGHTS', issued by 'HEADQUARTERS AIR FORCE SPECIAL WEAPONS CENTER, AIR RESEARCH AND DEVELOPMENT COMMAND, KIRTLAND AIR FORCE BASE, NEW MEXICO', authored by L. Reiffel of the Armour Research Foundation, Illinois Institute of Technology, dated 19 June 1959, under Project Number 5776-57853 and Contract AF 29(601)-1164. Its title page marks the title '(Unclassified Title)'.",
      "source": "AFSWC TR-59-39 Vol I, title page and report page, DDC AD 425380, https://archive.org/details/DTIC_AD0425380"
    },
    {
      "tier": 1,
      "text": "The abstract opens: 'Nuclear detonations in the vicinity of the moon are considered in this report along with scientific information which might be obtained from such explosions. The military aspect is aided by investigation of space environment, detection of nuclear device testing, and capability of weapons in space.'",
      "source": "AFSWC TR-59-39 Vol I, Abstract"
    },
    {
      "tier": 1,
      "text": "The introduction states the political motive in the report's own words: 'The motivation for such a detonation is clearly threefold: scientific, military and political... Obviously, however, specific positive effects would accrue to the nation first performing such a feat as a demonstration of advanced technological capability. It is also certain that, unless the climate of world opinion were well-prepared in advance, a considerable negative reaction could be stimulated.'",
      "source": "AFSWC TR-59-39 Vol I, Chapter I, Introduction"
    },
    {
      "tier": 1,
      "text": "The contributor list on the report page includes 'C. E. Sagan' alongside ten others. The report's appendix separately lists 'C. Sagan, U. of Chicago, Astronomy' as a member of the National Academy of Sciences WESTEX group and 'C. Sagan, ARF - Yerkes, Astronomy' on the Armed Forces National Research Council Panel on Extraterrestrial Life. The document says nothing about his security clearance.",
      "source": "AFSWC TR-59-39 Vol I, report page and appendix on extraterrestrial-life panels"
    },
    {
      "tier": 1,
      "text": "The distribution list sends copies to 'Director, Advanced Research Projects Agency, Department of Defense, ATTN: Ward Low, The Pentagon'; to 'US Atomic Energy Commission, ATTN: Technical Reports Library (Mrs. J. O'Leary, for DMA)'; to 'President, Sandia Corporation, ATTN: Document Control Division, Sandia Base, NMex'; to 'Director, Los Alamos Scientific Laboratory'; to 'Director, Lawrence Radiation Laboratory'; and to 'WADD, Wright-Patterson AFB, Ohio'.",
      "source": "AFSWC TR-59-39 Vol I, DISTRIBUTION list"
    },
    {
      "tier": 1,
      "text": "The command page names 'Colonel Carey L. O'Bryan, Jr., Deputy Commander' of the Air Force Special Weapons Center, and the publication review page carries his name over 'USAF' and 'Deputy Commander'. The same officer is listed in the Official Register of the United States 1957, page 629, as Deputy Director of the Atomic Energy Commission's Division of Military Application, on the line directly above Gise's.",
      "source": "AFSWC TR-59-39 Vol I, command page and publication review page, and Official Register of the United States 1957, p.629, https://www.govinfo.gov/content/pkg/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952/pdf/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952.pdf"
    }
  ],
  "sources": [
    { "name": "AFSWC TR-59-39 Vol I, A Study of Lunar Research Flights, DDC AD 425380 (DTIC mirror)", "url": "https://archive.org/details/DTIC_AD0425380", "date": "1959-06-19" },
    { "name": "OCR full text of AFSWC TR-59-39 Vol I", "url": "https://archive.org/download/DTIC_AD0425380/DTIC_AD0425380_djvu.txt", "date": "1959-06-19" },
    { "name": "Official Register of the United States 1957, US Civil Service Commission", "url": "https://www.govinfo.gov/content/pkg/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952/pdf/GOVPUB-CS1-a5ad60ca6d6113c71c09c45dce6b9952.pdf", "date": "1957-05-01" }
  ],
  "edges": [
    {
      "a": "afswc-tr-59-39", "b": "usaf", "type": "programmatic", "claimTier": 1,
      "label": "commissioned and published by the Air Force Special Weapons Center under Air Research and Development Command",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "The title page names the command and the station, and the publication review is signed by the Center's Deputy Commander."
    },
    {
      "a": "afswc-tr-59-39", "b": "l-kirtland", "type": "geographic", "claimTier": 1,
      "label": "issued from Kirtland Air Force Base, New Mexico",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "Headquarters Air Force Special Weapons Center is named on the title page with Kirtland as its station."
    },
    {
      "a": "afswc-tr-59-39", "b": "sandia", "type": "custody", "claimTier": 1,
      "label": "a numbered copy went to Sandia's document control division",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "The distribution list reads 'President, Sandia Corporation, ATTN: Document Control Division, Sandia Base, NMex'; the board's sandia node is the same site under its later name."
    },
    {
      "a": "afswc-tr-59-39", "b": "l-los-alamos", "type": "custody", "claimTier": 1,
      "label": "a copy went to the Los Alamos Scientific Laboratory report library",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "The distribution list names the Director, Los Alamos Scientific Laboratory, with two attention lines including 'Helen Redman, Report Library'."
    },
    {
      "a": "afswc-tr-59-39", "b": "darpa", "type": "custody", "claimTier": 1,
      "label": "a copy went to the Director of ARPA at the Pentagon",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "The distribution list reads 'Director, Advanced Research Projects Agency, Department of Defense, ATTN: Ward Low, The Pentagon, Wash 25, DC'."
    },
    {
      "a": "afswc-tr-59-39", "b": "l-wright-patterson", "type": "custody", "claimTier": 1,
      "label": "a copy went to WADD at Wright-Patterson",
      "dateStart": "1959", "dateEnd": "1959",
      "note": "Listed under ARDC CENTERS as 'WADD, Wright-Patterson AFB, Ohio'."
    }
  ]
}
```

---

## 15. Church Committee

**VERDICT: CONFIRMED** as to the committee, its mandate, its scale and its report.
**The transcript's use of it is CONTRADICTED by the report itself**, which records that
the committee never once examined an agency's files on its own and that three chapters
were struck from its published findings at the agencies' request.

**What the transcripts claim.** `michels-corpus-02.md` 02 / 13;52 and 14;51: Michael
Shellenberger names the "1975 CIA/FBI reform hearings" as "his explicit template for
what UAP oversight needs now, 'bipartisan'". `michels-corpus-05.md` 04 / 18;41: Mick
West raises it as "the precedent for how a real secret programme gets surfaced
('something like that where we can actually get these things in')". The triage row's
argument for the node is that recurrence across two speakers who agree on almost nothing
else is the signal, and that "the board's oversight view has no historical benchmark for
a successful congressional penetration."

**What the document says.** Book I of the final report was downloaded from the Senate
Select Committee on Intelligence's own site, a 42.7 MB PDF with a text layer, and read.

The title page: "94TH CONGRESS, 2d Session, SENATE REPORT No. 94-755 / FOREIGN AND
MILITARY INTELLIGENCE / BOOK I / FINAL REPORT OF THE SELECT COMMITTEE TO STUDY
GOVERNMENTAL OPERATIONS WITH RESPECT TO INTELLIGENCE ACTIVITIES UNITED STATES SENATE /
TOGETHER WITH ADDITIONAL, SUPPLEMENTAL, AND SEPARATE VIEWS / APRIL 26 (legislative day,
APRIL 14), 1976 / U.S. GOVERNMENT PRINTING OFFICE WASHINGTON: 1976".

Membership: "FRANK CHURCH, Idaho, Chairman; JOHN G. TOWER, Texas, Vice Chairman", then
Philip A. Hart, Walter F. Mondale, Walter D. Huddleston, Robert Morgan and Gary Hart for
the majority, and Howard H. Baker, Jr., Barry Goldwater, Charles McC. Mathias, Jr. and
Richard S. Schweiker for the minority. Staff Director William G. Miller, Chief Counsel
Frederick A. O. Schwarz, Jr.

Mandate: "On January 27, 1975, Senate Resolution 21 established a select committee 'to
conduct an investigation and study of governmental operations with respect to
intelligence activities and of the extent, if any, to which illegal, improper, or
unethical activities were engaged in by any agency of the Federal Government.'" Fifteen
enumerated areas follow; item 8 is "The need for specific legislative authority to
govern the operations of any intelligence agencies of the Federal Government now
existing without that explicit statutory authority, including but not limited to
agencies such as the Defense Intelligence Agency and the National Security Agency."

Scale: "The Committee staff of 100, including 60 professionals, has assisted the 11
members of the Committee in this indepth inquiry which involved more than 800 interviews,
over 250 executive hearings, and documentation in excess of 110,000 pages."

**The two passages that answer the transcript.** First, the report's own NOTE, on the
page after the letter of transmittal:

> The Committee's Final Report has been reviewed and declassified by the appropriate
> executive agencies... At the request of the agencies, the Committee deleted three
> chapters from this report: "Cover," "Espionage," and "Budgetary Oversight." In
> addition, two sections of the chapter "Covert Action of the CIA" and one section of
> the chapter "Department of State" have been deleted at the request of the agencies.

Second, section C, "The Focus and Scope of the Committee's Inquiry and Obstacles
Encountered":

> Despite its legal Senate mandate, and the issuance of subpoenas, in no instance has the
> Committee been able to examine the agencies' files on its own. In all the agencies,
> whether CIA, FBI, NSA, INR, DIA, or the NSC, documents and evidence have been presented
> through the filter of the agency itself.

And immediately after it: "Although the Senate inquiry was congressionally ordered and
although properly constituted committees under the Constitution have the right of full
inquiry, the Central Intelligence Agency and other agencies of the executive branch have
limited the Committee's access to the full record."

The committee's findings on oversight are consistent with that: "The Committee finds that
Congress has failed to provide the necessary statutory guidelines to ensure that
intelligence agencies carry out their missions in accord with constitutional processes.
Mechanisms for, and the practice of, congressional oversight have not been adequate."
And on money: "Congress' failure as a whole to monitor the intelligence agencies'
expenditures has been a major element in the ineffective legislative oversight of the
intelligence community." And the recommendation that connects directly to the board's
existing budget node: "The Committee finds that publication of the aggregate figure for
national intelligence would begin to satisfy the constitutional requirement and would
not damage the national security."

**What the transcripts claim that the record does NOT establish.**

| Transcript claim | State after this pass |
|---|---|
| The Church Committee is the template for how a real secret programme gets surfaced | CONTRADICTED in the committee's own words. It never inspected a file itself, its access was limited by the CIA and other executive agencies, and its published report lost three chapters, one of them on budgetary oversight, at those agencies' request |
| It was bipartisan | CONFIRMED on the face of the report: six majority members with Church as chairman, five minority members with Tower as vice chairman, and the report carries additional, supplemental and separate views |
| "1975 CIA/FBI reform hearings" | PARTLY. The committee was established 27 January 1975 and this volume was filed 26 April 1976. Its scope was far wider than CIA and FBI: NSA, DIA, INR, the NSC and the intelligence components of Defense are all named in the report's own list of what it examined |

**Tier: T1** throughout, the report being a published Senate document read on its own
face. Note that only Book I was opened; Books II to VI were not.

**BOARD RECOMMENDATION: yes, a new node, and it is the most useful of my five.** The
board's oversight view has needed a historical benchmark. What it gets is better than
the benchmark the transcripts wanted: the one thorough congressional investigation of
the secret state, saying in its own final report that it never got to look at a file by
itself, and losing its budgetary-oversight chapter to the agencies it was investigating.
That is the board's structural argument stated by a Senate committee in 1976, and it is
the strongest single answer available to any claim that Congress can simply look.

The candidates file classes this as an event. It is drafted below as an institution,
because it existed from a dated resolution to a dated final report and did things; if
the owner prefers the event class, the record supports either. The report itself could
carry a separate document node; that is not drafted here to avoid two nodes for one
opened record.

Sources opened:

| URL | What is at it |
|---|---|
| https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-94755-i.pdf | S. Rept. 94-755, Book I, "Foreign and Military Intelligence", Final Report of the Select Committee to Study Governmental Operations with Respect to Intelligence Activities, 26 April 1976, GPO 1976. Text layer present and read |

### Draft node

```json
{
  "id": "church-committee",
  "cls": "institution",
  "label": "Senate Select Committee to Study Governmental Operations with Respect to Intelligence Activities (Church Committee)",
  "sub": "Established by S. Res. 21, 27 January 1975; final report S. Rept. 94-755, six books, 1976",
  "cluster": "oversight",
  "tier": "A",
  "C": 2, "A": 1, "D": 1,
  "dateStart": "1975-01-27",
  "dateEnd": "1976-04-26",
  "domains": ["d-oversight", "d-legislative", "d-secrecy", "d-records"],
  "desc": "The only thorough congressional investigation ever made of the United States intelligence system, and the benchmark this board's oversight view has lacked. Eleven senators, a hundred staff, more than eight hundred interviews and over a hundred and ten thousand pages of documents. It is carried here for what its own final report concedes rather than for what it achieved: that it never once examined an agency's files on its own, that the CIA and other executive agencies limited its access to the record, and that three chapters of its published findings, including the chapter on budgetary oversight, were deleted at the request of the agencies it was investigating.",
  "claims": [
    {
      "tier": 1,
      "text": "'On January 27, 1975, Senate Resolution 21 established a select committee \"to conduct an investigation and study of governmental operations with respect to intelligence activities and of the extent, if any, to which illegal, improper, or unethical activities were engaged in by any agency of the Federal Government.\"' Book I of the final report, Senate Report 94-755, was filed on 'APRIL 26 (legislative day, APRIL 14), 1976'.",
      "source": "S. Rept. 94-755, Book I, title page and Part I section A, https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-94755-i.pdf"
    },
    {
      "tier": 1,
      "text": "The committee's own account of the obstacles it met: 'Despite its legal Senate mandate, and the issuance of subpoenas, in no instance has the Committee been able to examine the agencies' files on its own. In all the agencies, whether CIA, FBI, NSA, INR, DIA, or the NSC, documents and evidence have been presented through the filter of the agency itself.' It adds that 'the Central Intelligence Agency and other agencies of the executive branch have limited the Committee's access to the full record.'",
      "source": "S. Rept. 94-755, Book I, Part I section C, 'The Focus and Scope of the Committee's Inquiry and Obstacles Encountered'"
    },
    {
      "tier": 1,
      "text": "The report's own publication note records that it 'has been reviewed and declassified by the appropriate executive agencies' and that 'At the request of the agencies, the Committee deleted three chapters from this report: \"Cover,\" \"Espionage,\" and \"Budgetary Oversight.\"' Two sections of the covert-action chapter and one section of the State Department chapter were also deleted at agency request.",
      "source": "S. Rept. 94-755, Book I, NOTE following the Letter of Transmittal"
    },
    {
      "tier": 1,
      "text": "The committee was chaired by Frank Church of Idaho with John G. Tower of Texas as Vice Chairman, and had eleven members, six from the majority and five from the minority. 'The Committee staff of 100, including 60 professionals, has assisted the 11 members of the Committee in this indepth inquiry which involved more than 800 interviews, over 250 executive hearings, and documentation in excess of 110,000 pages.'",
      "source": "S. Rept. 94-755, Book I, committee page and Part I section C"
    },
    {
      "tier": 1,
      "text": "Among its findings: 'The Committee finds that Congress has failed to provide the necessary statutory guidelines to ensure that intelligence agencies carry out their missions in accord with constitutional processes. Mechanisms for, and the practice of, congressional oversight have not been adequate.' And on money: 'Congress' failure as a whole to monitor the intelligence agencies' expenditures has been a major element in the ineffective legislative oversight of the intelligence community.'",
      "source": "S. Rept. 94-755, Book I, Findings and Recommendations"
    },
    {
      "tier": 2,
      "text": "Two Michels-corpus speakers who agree on very little else, Michael Shellenberger and Mick West, each name the Church Committee as the model for what oversight of a compartmented programme should look like. The committee's own report describes an inquiry whose every document arrived through the filter of the agency that held it.",
      "source": "michels-corpus-02.md file 02 at 13;52 and 14;51 (Shellenberger); michels-corpus-05.md file 04 at 18;41 (West)"
    }
  ],
  "sources": [
    { "name": "S. Rept. 94-755, Book I, Foreign and Military Intelligence, Final Report of the Select Committee to Study Governmental Operations with Respect to Intelligence Activities", "url": "https://www.intelligence.senate.gov/wp-content/uploads/2024/08/sites-default-files-94755-i.pdf", "date": "1976-04-26" }
  ],
  "edges": [
    {
      "a": "church-committee", "b": "us-senate", "type": "legislative", "claimTier": 1,
      "label": "created as a select committee of the Senate by S. Res. 21 of 27 January 1975",
      "dateStart": "1975", "dateEnd": "1976",
      "note": "The report states the resolution, the date and the mandate in its own opening section."
    },
    {
      "a": "church-committee", "b": "oversight-congress", "type": "investigative", "claimTier": 1,
      "label": "the historical benchmark, and the source of the board's sharpest statement of the limit",
      "dateStart": "1975", "dateEnd": "1976",
      "note": "The committee found that 'Mechanisms for, and the practice of, congressional oversight have not been adequate', and recorded that in no instance had it examined an agency's files on its own."
    },
    {
      "a": "church-committee", "b": "cia", "type": "denial", "claimTier": 1,
      "label": "named by the committee as having limited its access to the full record",
      "dateStart": "1975", "dateEnd": "1976",
      "note": "The report says 'the Central Intelligence Agency and other agencies of the executive branch have limited the Committee's access to the full record', in some instances by assertion of executive privilege."
    },
    {
      "a": "church-committee", "b": "intel-budget-disclosure-record", "type": "legislative", "claimTier": 1,
      "label": "recommended annual publication of the aggregate national intelligence figure, and lost its own budget chapter",
      "dateStart": "1976", "dateEnd": "1976",
      "note": "The committee recommended publication of the aggregate figure while the chapter titled 'Budgetary Oversight' was deleted from the published report at the agencies' request."
    },
    {
      "a": "church-committee", "b": "senate-intelligence", "type": "legislative", "claimTier": 2,
      "label": "recommended the permanent oversight committee that followed it",
      "dateStart": "1976", "dateEnd": "1976",
      "note": "Book I says 'a strong and effective oversight committee is an essential first step' and refers throughout to 'any successor oversight committee'; the establishing resolution for the Senate Select Committee on Intelligence was not opened for this pass, so the succession itself is graded Tier 2."
    }
  ]
}
```

---

## What a next session should open, in priority order

1. **The AEC Albuquerque Operations Office manager series, 1960 to 1968.** The Official
   Register ends with the 1959 volume, `cia.gov/readingroom` and the OSTI OpenNet search
   interface are both unreachable from here, and `catalog.archives.gov` returned empty
   content to every form tried. Without it the Gise node cannot carry the office the
   whole corpus assigns him. NARA RG 326 Albuquerque is the place.
2. **The Project 1794 PDFs on The Black Vault**, listed and named but not opened.
   `1794.pdf`, 116 pages, is the Final Development Report and is the record that would
   let the board carry the Avrocar separately from Silver Bug.
3. **An AEC record for the Intelectron grant.** Both the amount and the funder are in
   dispute between the corpus and the secondary literature, which is exactly the
   condition under which the board should not carry either.
4. **Books II to VI of S. Rept. 94-755.** Only Book I was opened. Book II is the domestic
   half and is where the NSA and mail-opening findings sit.
