# Verified leads: Michels corpus candidates 1 to 5 (verifier 1)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over rows 1
to 5 of `research/leads/CANDIDATES-2026-09-02-MICHELS-DRAFT.md`, against
`research/leads/VERIFY-BRIEF-2026-09-02.md`.

**Verified 2 September 2026.** Every URL below was opened by this session and returned the
document described. Where a document is a scan, the text quoted was read from the OCR
layer the archive itself publishes, and that is labelled where it applies. `CLAUDE.md`
section 2 governs: nothing here is asserted that was not opened.

**Board state, read from `data/the-program.json` by this session, not taken from the
triage files.** `Bissell` 0 occurrences. `Malmgren` 0. `BLUEGILL`, `Bluegill`, `FISHBOWL`,
`Johnston Island`, `Johnston Atoll` 0 each. `Atomic Energy Commission` 21 prose
occurrences and `Atomic Energy Act` 45, with no node for the Commission. `TRW` 31
occurrences, all of them inside `gerb-northrop-trw-investigation`, with no node for the
company. All five candidates are genuinely absent.

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| 1 | Atomic Energy Commission | CONFIRMED | new node |
| 2 | Bluegill Triple Prime, DOMINIC I / FISHBOWL | CONFIRMED as an event; the row's document number and its date both CONTRADICTED | new node |
| 3 | Harald B. Malmgren | CONFIRMED for the public office; the UAP-adjacent account is Tier 3 and single-source | new node |
| 4 | TRW Inc. | CONFIRMED | new node |
| 5 | Richard M. Bissell Jr. | CONFIRMED | new node |

**The four findings that matter, in order:**

1. **DNA 6039F is not the FISHBOWL report.** The candidates row names "DNA 6039F for
   Operation FISHBOWL". DNA 6039F was opened: it is **Operation ARGUS 1958**. FISHBOWL has
   no separate DNA report of its own in this series; it is the high-altitude phase covered
   inside DNA 6040F, whose own keyword list carries FISHBOWL. Anyone citing DNA 6039F for a
   1962 Johnston Island shot is citing a 1958 South Atlantic test series.
2. **The date is 25 October 1962 in the source, not 26 October.** DNA 6040F gives the shot
   as "BLUEGILL Triple Prime (25 October 1962, 2359)" and its Table 1 dates it 25 Oct.
   Every ship and aircraft entry in the report repeats "25 October, 2359". 26 October is the
   GMT rendering of the same instant; the DoD operational record says 25 October local, and
   a node dated 26 October will not match the document it cites.
3. **No RC-135 and no Cobra Ball appear anywhere in DNA 6040F.** Zero occurrences of
   "RC-135" and zero of "Cobra". What the report does carry is a **call sign KETTLE**,
   assigned to three KC-135 **photographic** aircraft in the DOMINIC air participation
   table. That is a real, documented origin for the "Kettle" film names the corpus uses,
   and it is not the aircraft type the triage row assumed.
4. **Bissell's own agency history documents the Groom Lake decision and the Blue Book
   arrangement in the same monograph.** The site was found on 12 April 1955, the AEC was
   asked to absorb it, and the CIA project staff later checked Blue Book's UFO reports
   against U-2 flight logs while, in the monograph's own words, not revealing the cause.
   That is one document tying `l-groom-lake`, the AEC and `project-blue-book` together at
   Tier 1, and the board currently has none.

---

## 1. Atomic Energy Commission

**VERDICT: CONFIRMED.** The Commission's creation, its internal structure, its statutory
custody of fissionable material and atomic weapons, its born-secret information regime and
its abolition were all read in the Statutes at Large text itself.

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf | Statutes at Large volume 60, page 755 onward. Chapter 724, S. 1717, **Public Law 585**, 79th Congress, approved **1 August 1946**. The Atomic Energy Act of 1946. |
| https://www.govinfo.gov/content/pkg/STATUTE-68/pdf/STATUTE-68-Pg919.pdf | Statutes at Large volume 68, page 919 onward. **Public Law 703**, Chapter 1073, H.R. 9757, approved **30 August 1954**. The Atomic Energy Act of 1954. |
| https://www.govinfo.gov/content/pkg/STATUTE-88/pdf/STATUTE-88-Pg1233.pdf | Statutes at Large volume 88, page 1233 onward. **Public Law 93-438**, approved **11 October 1974**. The Energy Reorganization Act of 1974. |
| https://www.archives.gov/research/guide-fed-records/groups/326.html | "Records of the Atomic Energy Commission", Guide to Federal Records in the National Archives, Record Group 326. |

Both statute PDFs are scans with a text layer, extracted with `pdftotext -layout`; the
quotations below were read from that layer against the page furniture (running heads,
marginal captions) so the page could be located.

### What the documents establish

**Creation and composition.** Section 2(a)(1) of the 1946 Act: "There is hereby established
an Atomic Energy Commission (herein called the Commission), which shall be composed of five
members." Members are appointed by the President by and with the advice and consent of the
Senate; the President designates the Chairman; the principal office is in the District of
Columbia.

**The Division of Military Application exists in the founding statute, not later.** Section
2(a)(4)(B) of the 1946 Act establishes within the Commission "a Division of Research, a
Division of Production, a Division of Engineering, and a Division of Military Application",
and provides that "The Director of the Division of Military Application shall be a member of
the armed forces." The 1954 Act keeps it at section 25 and hardens the language: the
Director "shall be an active member of the Armed Forces."

**Statutory custody, and the Manhattan Engineer District hand-over.** Section 9(a) directs
the President to transfer to the Commission all United States interests in "All fissionable
material; all atomic weapons and parts thereof; all facilities, equipment, and materials for
the processing, production, or utilization of fissionable material or atomic energy; all
processes and technical information of any kind, and the source thereof", and, at (3), "Such
other property owned by or in the custody or control of the Manhattan Engineer District or
other Government agencies as the President may determine." Section 10(b)(2)(B)(iii)
separately provides that pending FBI investigation "any individual who was permitted access
to restricted data by the Manhattan Engineer District may be permitted access to restricted
data" and that the Commission may employ any individual who worked for the District. That is
the Manhattan-to-AEC custody link the board's prose asserts, in the statute, on its face.

**Born-secret classification.** Section 10(b)(1) of the 1946 Act: the term "restricted data"
"means all data concerning the manufacture or utilization of atomic weapons, the production
of fissionable material, or the use of fissionable material in the production of power, but
shall not include any data which the Commission from time to time determines may be
published without adversely affecting the common defense and security." The 1954 Act
recasts it at section 11r as "all data concerning (1) design, manufacture, or utilization of
atomic weapons; (2) the production of special nuclear material; or (3) the use of special
nuclear material in the production of energy", excluding only what is declassified under
section 142. The default is classification by category, and the exception is an affirmative
act of the Commission. Section 10(b)(2)(B)(i) makes FBI investigation and a Commission
determination the precondition for any contractor employee's access.

**Abolition.** Section 104(a) of the Energy Reorganization Act of 1974: "The Atomic Energy
Commission is hereby abolished." Sections 21 and 22 of the 1954 Act are repealed and the
Commission's functions vest in the Administrator of the Energy Research and Development
Administration. Section 312(a) makes the Act effective 120 days after enactment "or on such
earlier date as the President may prescribe and publish in the Federal Register". The NARA
guide records the abolition as by "the Energy Reorganization Act of 1974 (88 Stat. 1237),
October 11, 1974", with ERDA and then the Department of Energy taking the research,
development and production functions and the Nuclear Regulatory Commission taking licensing
and regulation.

### What the transcript claimed that these documents do NOT establish

Four guests across four lead maps place the AEC at a custody point for recovered material.
**Nothing in either statute or in the NARA guide says anything about recovered material,
non-human craft, or any programme of that kind.** What the statutes establish is a body with
statutory title to all fissionable material and all atomic weapons, running a
classify-by-category information regime with an FBI gate on contractor access. That is a
structural fact about how such a custody could have been held, not evidence that it was.
The node must carry the statute and leave the testimony where the triage files put it.

### Draft node

```json
{
  "id": "atomic-energy-commission",
  "cls": "institution",
  "label": "Atomic Energy Commission",
  "cluster": "oversight",
  "sub": "Civilian atomic authority, 1946-1974; statutory custodian of fissionable material and atomic weapons",
  "tier": "B",
  "C": 2,
  "A": 3,
  "D": 1,
  "dateStart": "1946-08-01",
  "dateEnd": "1974-10-11",
  "desc": "The Atomic Energy Commission was created by the Atomic Energy Act of 1946 and took statutory title to everything the Manhattan Engineer District had held: all fissionable material, all atomic weapons and parts, and all processes and technical information behind them. It ran the born-secret information regime, under which data in defined categories is classified by operation of statute and declassified only by an affirmative act of the Commission, and it gated every contractor employee's access behind an FBI investigation and a Commission determination. Its Division of Military Application was established in the founding statute and directed by a serving officer of the armed forces. The Energy Reorganization Act of 1974 abolished it and vested its functions in ERDA, from which they passed to the Department of Energy.",
  "claims": [
    {
      "tier": 1,
      "text": "The Commission was created by statute: 'There is hereby established an Atomic Energy Commission (herein called the Commission), which shall be composed of five members.' Members are appointed by the President by and with the advice and consent of the Senate.",
      "source": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755, sec. 2(a), approved 1 August 1946, https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "The Commission took statutory custody of the Manhattan Engineer District's holdings. Section 9(a) directs the transfer to the Commission of 'All fissionable material; all atomic weapons and parts thereof' and of 'Such other property owned by or in the custody or control of the Manhattan Engineer District or other Government agencies as the President may determine.'",
      "source": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755, sec. 9(a), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "Classification runs by category rather than by decision. The 1946 Act defines restricted data as 'all data concerning the manufacture or utilization of atomic weapons, the production of fissionable material, or the use of fissionable material in the production of power, but shall not include any data which the Commission from time to time determines may be published without adversely affecting the common defense and security.'",
      "source": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755, sec. 10(b)(1), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf"
    },
    {
      "tier": 1,
      "text": "A Division of Military Application under a serving officer was in the Commission from the start: the 1946 Act establishes it alongside Research, Production and Engineering and provides that 'The Director of the Division of Military Application shall be a member of the armed forces.' The 1954 Act carries it forward at section 25 with the Director required to be 'an active member of the Armed Forces.'",
      "source": "Atomic Energy Act of 1946, sec. 2(a)(4)(B), https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf ; Atomic Energy Act of 1954, Public Law 83-703, 68 Stat. 919, sec. 25, https://www.govinfo.gov/content/pkg/STATUTE-68/pdf/STATUTE-68-Pg919.pdf"
    },
    {
      "tier": 1,
      "text": "The Commission was abolished by statute: 'The Atomic Energy Commission is hereby abolished.' Its functions vested in the Administrator of the Energy Research and Development Administration, and the Act took effect 120 days after enactment or on an earlier date the President might prescribe.",
      "source": "Energy Reorganization Act of 1974, Public Law 93-438, 88 Stat. 1233, secs. 104(a) and 312(a), approved 11 October 1974, https://www.govinfo.gov/content/pkg/STATUTE-88/pdf/STATUTE-88-Pg1233.pdf"
    }
  ],
  "sources": [
    { "name": "Atomic Energy Act of 1946, Public Law 79-585, 60 Stat. 755", "url": "https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf", "date": "1946-08-01" },
    { "name": "Atomic Energy Act of 1954, Public Law 83-703, 68 Stat. 919", "url": "https://www.govinfo.gov/content/pkg/STATUTE-68/pdf/STATUTE-68-Pg919.pdf", "date": "1954-08-30" },
    { "name": "Energy Reorganization Act of 1974, Public Law 93-438, 88 Stat. 1233", "url": "https://www.govinfo.gov/content/pkg/STATUTE-88/pdf/STATUTE-88-Pg1233.pdf", "date": "1974-10-11" },
    { "name": "Records of the Atomic Energy Commission, Record Group 326, Guide to Federal Records in the National Archives", "url": "https://www.archives.gov/research/guide-fed-records/groups/326.html", "date": "2026-09-02" }
  ],
  "edges": [
    {
      "a": "atomic-energy-commission",
      "b": "manhattan-project-2",
      "type": "custody",
      "claimTier": 1,
      "label": "Statutory transfer of the Manhattan Engineer District's holdings",
      "note": "Section 9(a) of the 1946 Act directs the President to transfer to the Commission all fissionable material, all atomic weapons and parts, all processes and technical information, and such other property in the custody or control of the Manhattan Engineer District as he may determine.",
      "sources": [{ "name": "Atomic Energy Act of 1946, sec. 9(a)", "url": "https://www.govinfo.gov/content/pkg/STATUTE-60/pdf/STATUTE-60-Pg755.pdf", "date": "1946-08-01" }]
    },
    {
      "a": "atomic-energy-commission",
      "b": "doe",
      "type": "institutional",
      "claimTier": 1,
      "label": "Abolished 1974; functions passed through ERDA to the Department of Energy",
      "note": "The Energy Reorganization Act of 1974 abolished the Commission and vested its functions in the ERDA Administrator, and the NARA record group description names the Department of Energy as the eventual holder of the research, development and production functions.",
      "sources": [{ "name": "Energy Reorganization Act of 1974, sec. 104(a); NARA RG 326 guide", "url": "https://www.govinfo.gov/content/pkg/STATUTE-88/pdf/STATUTE-88-Pg1233.pdf", "date": "1974-10-11" }]
    },
    {
      "a": "atomic-energy-commission",
      "b": "l-groom-lake",
      "type": "geographic",
      "claimTier": 1,
      "label": "Absorbed Groom Lake into its Nevada real estate at CIA request, 1955",
      "note": "The CIA's own overhead reconnaissance history records that after the April 1955 overflight Bissell found Groom Lake was not part of the AEC proving ground, and that he and Miller asked the Commission to add it, which Chairman Lewis Strauss agreed to do.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    },
    {
      "a": "atomic-energy-commission",
      "b": "l-nevada-test-site",
      "type": "geographic",
      "claimTier": 1,
      "label": "Area 51 was added to the Nevada Test Site by the Commission",
      "note": "The same CIA history states that Eisenhower approved the addition of the strip known by its map designation as Area 51 to the Nevada Test Site, and DNA 6040F separately locates Groom Lake at the northeast corner of the AEC's Nevada Proving Ground.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    }
  ]
}
```

---

## 2. Bluegill Triple Prime, Operation DOMINIC I / FISHBOWL

**VERDICT: CONFIRMED as an event.** The shot is real, dated and fully documented in a public
DoD technical report that was opened and read. **Two elements of the candidates row are
CONTRADICTED:** the second report number, and the date.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/details/DTIC_ADA136820 | Item page, "DTIC ADA136820: Operation DOMINIC I-1962", the DTIC mirror named in `notes/SOURCING-2026-08-25.md`. |
| https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt | Full OCR text, 961 KB, of **DNA 6040F**, "OPERATION DOMINIC I--1962", United States Atmospheric Nuclear Weapons Tests, Nuclear Test Personnel Review, prepared by the Defense Nuclear Agency as Executive Agency for the Department of Defense. Report Documentation Page: authors L. Berkhouse, S.E. Davis, F.R. Gladeck, J.H. Hallowell, C.B. Jones, E.J. Martin, R.A. Miller, F.W. McMullan, M.J. Osborne; performing organisation Kaman Tempo, Santa Barbara; performing organisation report number KT-82-018(R); contract DNA 001-79-C-0472; report date **1 February 1983**; 436 pages; UNCLASSIFIED; "Approved for public release; distribution unlimited." Keyword list includes FISHBOWL and Johnston Island. |
| https://archive.org/download/DTIC_ADA122341/DTIC_ADA122341_djvu.txt | Full OCR text of **DNA 6039F**. Cover and Report Documentation Page both read "OPERATION ARGUS 1958". |

### What the document establishes

**The shot.** DNA 6040F, in its narrative of the FISHBOWL high-altitude series: "BLUEGILL
Triple Prime (25 October 1962, 2359). The fourth attempt to launch the BLUEGILL device
using a Thor missile was successful." The report describes what observers at Johnston Island
saw, "a brilliant white flash", a thermal pulse felt on bare skin, a distorted bright sphere
turning through yellow, green, pink and violet, blue-purple streamers, and a glow bright
enough at ten minutes to read a watch by, persisting at least thirty minutes.

**The date, in the report's own two places.** Table 1, "DOMINIC detonations, 1962", carries
the row "25 Oct / BLUE GILL / FISHBOWL shot, submegaton, tens of kilometers over Johnston
Island", sourced by the report to "Announced United States Nuclear Tests, NVO-29 (Rev. 1),
Office of Public Affairs, U.S. Department of Energy, Nevada Operations Office, January 1980".
Every one of the report's per-ship and per-unit entries repeats "(Johnston Island, 25
October, 2359)".

**The three failed attempts before it.** The report gives BLUEGILL (2 June 1962), destroyed
in flight by order of CJTF 8 after the tracking system lost it; BLUEGILL Prime, which burned
on the pad; and BLUEGILL Double Prime (15 October 1962, 2130). Triple Prime is the fourth
attempt.

**Who was there.** "The Air Force arrayed 22 aircraft for the detonation", plus WB-50s and
U-2s for weather, Navy P2Vs for surveillance and pod recovery, and Marine helicopters for pod
recovery. Nine Navy ships were positioned to gather scientific data; the report names them,
including USS Princeton (LPH-5), USS John S. McCain (DL-3), USS Jenkins (DD-447), USNS Point
Barrow and USAS American Mariner.

**KETTLE is a call sign, not a film title.** The DOMINIC aircraft participation table lists,
by number, type, call sign and mission: "3 / KC-135 / Kettle / Photographic aircraft",
alongside Cognac and Kibosh (KC-135), Cordova (KC-135, propagation test), Caboodle (C-118,
retinal burn study), Abusive and Lambkin (RC-121), Baxter/Byron (B-47), Hewstone (C-130) and
White Spot (U-2, sampler). The Triple Prime and CHECKMATE array figures repeat the same call
signs.

### What the transcript and the candidates row claim that this document does NOT establish

| Claim | What the document says |
|---|---|
| "DNA 6039F for Operation FISHBOWL" | **CONTRADICTED.** DNA 6039F is Operation ARGUS 1958. FISHBOWL is covered inside DNA 6040F. |
| "26 October 1962" | **CONTRADICTED as written.** The operational record says 25 October 1962, 2359, Johnston Island, in the narrative and in Table 1. 26 October is the same instant expressed in GMT; a node that cites DNA 6040F must carry the report's date. |
| "the RC-135S Cobra Ball aircraft that filmed both" (triage 2.A2) | **NOT SUPPORTED.** "RC-135" appears zero times in DNA 6040F and "Cobra" zero times. The photographic aircraft were three KC-135s under call sign KETTLE. |
| a shoot-down, a recovery, or debris | **ABSENT.** The report contains no reference to any unidentified object, unknown craft, anomalous observation, recovery or debris associated with the shot. Its only uses of "unidentified" are an unidentified number of dosimetry analyses and one unidentified event in a fallout discussion. |
| the "Kettle 1" / "Kettle 2" films and their 1998 and 2023 reviews | **NOT OPENED.** No film, review, MDR or FOIA response was opened for this pass. What the report supplies is the provenance of the name. |
| Lawrence Preston Gise as the custodian | **NOT IN THIS DOCUMENT.** "Gise" appears zero times in DNA 6040F. That candidate is verifier 3's. |

### Draft node

```json
{
  "id": "bluegill-triple-prime",
  "cls": "event",
  "label": "Bluegill Triple Prime",
  "cluster": "legacy",
  "sub": "FISHBOWL high-altitude shot, Operation DOMINIC I, Johnston Island, 25 October 1962",
  "tier": "C",
  "C": 1,
  "A": 1,
  "D": 1,
  "dateStart": "1962-10-25",
  "dateEnd": "1962-10-25",
  "desc": "Bluegill Triple Prime was the fourth attempt to detonate the BLUEGILL device above Johnston Island, and the first that worked. Three earlier attempts failed: the 2 June 1962 launch was destroyed in flight after tracking was lost, BLUEGILL Prime burned on the pad, and BLUEGILL Double Prime failed on 15 October. The successful shot is recorded by the Defense Nuclear Agency at 25 October 1962, 2359 local, submegaton, tens of kilometres over Johnston Island, with 22 Air Force aircraft arrayed and nine Navy ships positioned to gather data. Four guests across four Michels lead maps attach a recovery story to it; the DoD operational record for the shot contains nothing of the kind, and the node exists to hold the documented event so that the testimony has something dated to hang from.",
  "claims": [
    {
      "tier": 1,
      "text": "The shot and its date: 'BLUEGILL Triple Prime (25 October 1962, 2359). The fourth attempt to launch the BLUEGILL device using a Thor missile was successful.'",
      "source": "DNA 6040F, Operation DOMINIC I--1962, Defense Nuclear Agency, 1 February 1983, https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Its place in the test series, from the report's own summary table: '25 Oct / BLUE GILL / FISHBOWL shot, submegaton, tens of kilometers over Johnston Island', sourced there to Announced United States Nuclear Tests, NVO-29 (Rev. 1), Department of Energy, Nevada Operations Office, January 1980.",
      "source": "DNA 6040F, Table 1, DOMINIC detonations, 1962, https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The force present: 'The Air Force arrayed 22 aircraft for the detonation', with WB-50 and U-2 weather aircraft, Navy P2Vs for surveillance and pod recovery and Marine helicopters, and nine Navy ships positioned to gather scientific data.",
      "source": "DNA 6040F, narrative for BLUEGILL Triple Prime, https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt"
    },
    {
      "tier": 1,
      "text": "KETTLE is a DOMINIC aircraft call sign, not a film. The aircraft participation table lists '3 / KC-135 / Kettle / Photographic aircraft' alongside Cognac, Kibosh, Cordova, Caboodle, Abusive, Lambkin, Baxter/Byron, Hewstone and White Spot. The strings 'RC-135' and 'Cobra' do not appear anywhere in the report.",
      "source": "DNA 6040F, Air Force aircraft participation in DOMINIC, https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt"
    },
    {
      "tier": 1,
      "text": "DNA 6039F is not the FISHBOWL report. Its cover and Report Documentation Page both read 'OPERATION ARGUS 1958'. FISHBOWL appears instead in DNA 6040F's own keyword list.",
      "source": "DNA 6039F, Operation ARGUS 1958, Defense Nuclear Agency, https://archive.org/download/DTIC_ADA122341/DTIC_ADA122341_djvu.txt"
    }
  ],
  "sources": [
    { "name": "DNA 6040F, Operation DOMINIC I--1962, Defense Nuclear Agency / Kaman Tempo, report date 1 February 1983, DTIC ADA136820", "url": "https://archive.org/details/DTIC_ADA136820", "date": "1983-02-01" },
    { "name": "DNA 6039F, Operation ARGUS 1958, Defense Nuclear Agency, DTIC ADA122341", "url": "https://archive.org/details/DTIC_ADA122341", "date": "1982-04-30" }
  ],
  "edges": [
    {
      "a": "bluegill-triple-prime",
      "b": "usaf",
      "type": "institutional",
      "claimTier": 1,
      "label": "Air Force flew the shot and its 22-aircraft array",
      "note": "DNA 6040F records that the Air Force arrayed 22 aircraft for the detonation and names the call signs and missions of the KC-135, RC-121, B-47, C-118, C-130 and U-2 aircraft that flew DOMINIC.",
      "sources": [{ "name": "DNA 6040F, Operation DOMINIC I--1962", "url": "https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt", "date": "1983-02-01" }]
    },
    {
      "a": "bluegill-triple-prime",
      "b": "doe",
      "type": "custody",
      "claimTier": 1,
      "label": "The detonation list is a Department of Energy publication",
      "note": "DNA 6040F sources its own table of DOMINIC detonations to Announced United States Nuclear Tests, NVO-29 (Rev. 1), Office of Public Affairs, Department of Energy, Nevada Operations Office, January 1980, so the authoritative date and yield description for this shot are held by DOE rather than by DoD.",
      "sources": [{ "name": "DNA 6040F, Table 1 source note", "url": "https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt", "date": "1983-02-01" }]
    },
    {
      "a": "bluegill-triple-prime",
      "b": "d-nuclear",
      "type": "programmatic",
      "claimTier": 1,
      "label": "A dated, documented high-altitude nuclear test",
      "note": "The board's nuclear-correlation thread runs largely on witness memory; this is an official operational record fixing a date, a location and a force disposition independently of any witness.",
      "sources": [{ "name": "DNA 6040F, Operation DOMINIC I--1962", "url": "https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt", "date": "1983-02-01" }]
    }
  ]
}
```

---

## 3. Harald B. Malmgren

**VERDICT: CONFIRMED for the public office. The UAP-adjacent account is a family narrative
and must be carried, if at all, at Tier 3.**

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/GPO-CRECB-1972-pt13/pdf/GPO-CRECB-1972-pt13-3.pdf | Bound Congressional Record, 1972, part 13. Senate proceedings of **8 May 1972**, pages 16126 to 16127, and the "Executive nomination confirmed by the Senate May 8, 1972" list at the end of the day's Senate proceedings. |
| https://www.joynesfuneralhome.com/obituary/Harald-Malmgren | Joynes Funeral Home, Warrenton VA, obituary page. Its embedded NewsArticle metadata reads "Harald B. Malmgren death notice and obituary, Thursday February 13, 2025. Joynes Funeral Home, Inc. Warrenton, VA 20188", published 27 February 2025. |
| https://sldinfo.com/2025/02/dr-harald-malmgren-passed/ | "Dr. Harald Malmgren Passed", Second Line of Defense, posted 24 February 2025 by Robbin Laird, reproducing a biography written by **Pippa Malmgren**, his daughter. |
| https://www.presidency.ucsb.edu/documents/remarks-the-high-school-football-stadium-los-alamos-new-mexico | "Remarks at the High School Football Stadium, Los Alamos, New Mexico", 7 December 1962, Public Papers of the Presidents, American Presidency Project. |

### What the documents establish

**The office, at Tier 1.** The Congressional Record for 8 May 1972 records, under "OFFICE OF
THE SPECIAL REPRESENTATIVE FOR TRADE NEGOTIATIONS", that the clerk "read the nomination of
Harald Bernard Malmgren, of the District of Columbia, to be a Deputy Special Representative
for Trade Negotiations, with the rank of Ambassador", and then: "Without objection, the
nomination is considered and confirmed." The same nomination is repeated in the day's
confirmed list. His middle name is **Bernard**, and the exact title is Deputy Special
Representative for Trade Negotiations. Note that the popular form of the title, "Principal
Deputy U.S. Trade Representative", is the family biography's wording, not the Senate's.

**The death.** 13 February 2025, per the funeral home's own published record.

**Los Alamos, December 1962.** Kennedy did speak at Los Alamos on 7 December 1962, and
Vice President Johnson was present: the remarks open "Dr. Bradbury, Mr. Vice President,
Senator Anderson, Congressman Montoya, Congressman Morris". The visit is real.

### What the transcript claimed that these documents do NOT establish

The whole Michels chain around this man rests on the biography his daughter published, which
is where the operative sentence lives: that he "oversaw many missile tests in these roles,
including the controversial Blue Gill Triple Prime test which prompted both President
Kennedy and Vice President Lyndon Johnson to urgently visit Los Alamos and the Sandia Labs
in December 1962". Three separate things are packed into that and they grade differently.

| Element | Grade |
|---|---|
| Malmgren held the trade post at ambassadorial rank from May 1972 | **Tier 1**, Congressional Record |
| He died 13 February 2025 | **Tier 1**, funeral home record |
| Kennedy and Johnson were at Los Alamos on 7 December 1962 | **Tier 1**, Public Papers |
| He was assigned to the Institute for Defense Analyses and acted as liaison between the NSC and the Joint Chiefs during the Cuban Missile Crisis | **Tier 2**, family biography only. No IDA or DoD personnel record was opened. |
| He oversaw missile tests including Bluegill Triple Prime | **Tier 3.** Single-source, and the source is his daughter writing after his death. His name appears zero times in DNA 6040F. |
| Bluegill Triple Prime caused the Los Alamos and Sandia visit | **Tier 3 and not carried.** The visit is documented; the causation is asserted by one interested party. Nothing was opened that connects them, and no record of a Sandia visit was opened at all. |

The 1935 birth year and the age at death circulated in search results were **not** opened
and are not asserted here.

### Draft node

```json
{
  "id": "harald-b-malmgren",
  "cls": "person",
  "label": "Harald B. Malmgren",
  "status": "dead",
  "date": "2025-02-13",
  "loc": "Warrenton, Virginia",
  "sub": "Deputy Special Representative for Trade Negotiations with the rank of Ambassador, confirmed 8 May 1972",
  "cluster": "other",
  "tier": "C",
  "C": 1,
  "A": 1,
  "D": 1,
  "narrative": "Harald Bernard Malmgren's public service record is entirely open and settles the part of his story that can be settled. The Senate confirmed him on 8 May 1972 as a Deputy Special Representative for Trade Negotiations with the rank of Ambassador, and he died on 13 February 2025. He reaches this board only through a biography written by his daughter Pippa Malmgren and published after his death, which places him at the Institute for Defense Analyses during the Cuban Missile Crisis and says he oversaw missile tests including Bluegill Triple Prime. The Michels corpus corrupts his name five ways and routes a deathbed account through it. The node carries the documented post and the documented death, and grades the rest where it belongs.",
  "claims": [
    {
      "tier": 1,
      "text": "The Senate confirmed him on 8 May 1972: the clerk 'read the nomination of Harald Bernard Malmgren, of the District of Columbia, to be a Deputy Special Representative for Trade Negotiations, with the rank of Ambassador', and the presiding officer stated 'Without objection, the nomination is considered and confirmed.'",
      "source": "Congressional Record, Senate, 8 May 1972, pp. 16126-16127, bound edition, https://www.govinfo.gov/content/pkg/GPO-CRECB-1972-pt13/pdf/GPO-CRECB-1972-pt13-3.pdf"
    },
    {
      "tier": 1,
      "text": "He died on 13 February 2025. The funeral home's published record reads: 'Harald B. Malmgren death notice and obituary, Thursday February 13, 2025. Joynes Funeral Home, Inc. Warrenton, VA 20188.'",
      "source": "Joynes Funeral Home, Inc., obituary record published 27 February 2025, https://www.joynesfuneralhome.com/obituary/Harald-Malmgren"
    },
    {
      "tier": 2,
      "text": "His daughter's published biography states that Robert McNamara brought him from Cornell, that 'He was assigned to The Institute for Defense Analysis and appointed as the joint liaison between The White House National Security Council and the Joint Chiefs just as the Cuban Missile Crisis began', and that he later headed the Economics Group of the Weapons Systems Evaluation Group. No IDA or Defense Department personnel record was opened for any of it.",
      "source": "Pippa Malmgren, biography of Harald Malmgren, reproduced in 'Dr. Harald Malmgren Passed', Second Line of Defense, 24 February 2025, https://sldinfo.com/2025/02/dr-harald-malmgren-passed/"
    },
    {
      "tier": 3,
      "text": "The Bluegill claim is single-source and posthumous. The same biography says he 'oversaw many missile tests in these roles, including the controversial Blue Gill Triple Prime test which prompted both President Kennedy and Vice President Lyndon Johnson to urgently visit Los Alamos and the Sandia Labs in December 1962'. His name appears zero times in DNA 6040F, the Defense Nuclear Agency's own report on that test series.",
      "source": "Pippa Malmgren, biography of Harald Malmgren, Second Line of Defense, 24 February 2025, https://sldinfo.com/2025/02/dr-harald-malmgren-passed/ ; checked against DNA 6040F, https://archive.org/download/DTIC_ADA136820/DTIC_ADA136820_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The December 1962 visit is real, whatever caused it. Kennedy spoke at Los Alamos on 7 December 1962 with the Vice President present, opening 'Dr. Bradbury, Mr. Vice President, Senator Anderson, Congressman Montoya, Congressman Morris'.",
      "source": "'Remarks at the High School Football Stadium, Los Alamos, New Mexico', 7 December 1962, Public Papers of the Presidents, https://www.presidency.ucsb.edu/documents/remarks-the-high-school-football-stadium-los-alamos-new-mexico"
    }
  ],
  "sources": [
    { "name": "Congressional Record, Senate, 8 May 1972, pp. 16126-16127 (bound edition, 1972 part 13)", "url": "https://www.govinfo.gov/content/pkg/GPO-CRECB-1972-pt13/pdf/GPO-CRECB-1972-pt13-3.pdf", "date": "1972-05-08" },
    { "name": "Joynes Funeral Home, Inc., obituary record for Harald B. Malmgren", "url": "https://www.joynesfuneralhome.com/obituary/Harald-Malmgren", "date": "2025-02-27" },
    { "name": "'Dr. Harald Malmgren Passed', Second Line of Defense, biography by Pippa Malmgren", "url": "https://sldinfo.com/2025/02/dr-harald-malmgren-passed/", "date": "2025-02-24" },
    { "name": "Remarks at the High School Football Stadium, Los Alamos, New Mexico, 7 December 1962", "url": "https://www.presidency.ucsb.edu/documents/remarks-the-high-school-football-stadium-los-alamos-new-mexico", "date": "1962-12-07" }
  ],
  "edges": [
    {
      "a": "harald-b-malmgren",
      "b": "ida",
      "type": "institutional",
      "claimTier": 2,
      "label": "Assigned to IDA during the Cuban Missile Crisis, on a family account",
      "note": "The only source is the biography his daughter published after his death; no IDA or Defense Department personnel record was opened, so this edge must not render as documented.",
      "sources": [{ "name": "Pippa Malmgren, biography of Harald Malmgren, Second Line of Defense", "url": "https://sldinfo.com/2025/02/dr-harald-malmgren-passed/", "date": "2025-02-24" }]
    },
    {
      "a": "harald-b-malmgren",
      "b": "l-los-alamos",
      "type": "temporal",
      "claimTier": 3,
      "label": "Named as the cause of the December 1962 presidential visit",
      "note": "The visit itself is Tier 1 from the Public Papers, dated 7 December 1962 with the Vice President present; the claim that Bluegill Triple Prime prompted it comes only from the family biography and is carried here as a stated inference, not as a documented link.",
      "sources": [{ "name": "Pippa Malmgren biography; Public Papers of the Presidents, 7 December 1962", "url": "https://www.presidency.ucsb.edu/documents/remarks-the-high-school-football-stadium-los-alamos-new-mexico", "date": "1962-12-07" }]
    }
  ]
}
```

---

## 4. TRW Inc.

**VERDICT: CONFIRMED**, at primary-filing level, on both ends of the chain the board added
`bdm-international` to reach.

### What was opened

| URL | What is at it |
|---|---|
| https://www.sec.gov/Archives/edgar/data/870763/0000950152-97-008353.txt | BDM International, Inc., **Schedule 14D-9**, filed 26 November 1997, CIK 0000870763, SEC file number 005-45795. Includes the stockholder letter signed by Philip A. Odeen, President and CEO. |
| https://www.sec.gov/Archives/edgar/data/100030/000089843002004462/d425.htm | Form 425 filed 12 December 2002, filer Northrop Grumman Corporation, subject company TRW, Inc. (No. 1-2384), carrying the press release "NORTHROP GRUMMAN SHAREHOLDERS APPROVE MERGER WITH TRW, INC.", dated 11 December 2002. |
| https://www.sec.gov/Archives/edgar/data/1133421/000089843002004580/d8k.htm | Northrop Grumman Corporation **Form 8-K**, earliest event 11 December 2002, Item 2, Acquisition or Disposition of Assets. |
| https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=TRW+INC | EDGAR company search. CIK **0000100030** is now "NORTHROP GRUMMAN SPACE & MISSION SYSTEMS CORP", "formerly: TRW INC (filings through 2002-12-23)". |

### What the documents establish

**The BDM acquisition, 1997.** The 14D-9 stockholder letter of 26 November 1997: "on
November 20, 1997, BDM International, Inc. entered into a Merger Agreement with TRW Inc. and
Systems Acquisition Inc., a wholly owned subsidiary of TRW, pursuant to which that
subsidiary has commenced a tender offer (the 'Offer') to purchase all of the outstanding
shares of BDM's common stock for a cash price of $29.50 per share." The board recommended
acceptance unanimously; Wasserstein Perella gave the fairness opinion. BDM's filing history
then stops: SC 14D1 amendments through 29 December 1997 and a Form 15-12G the same day.

**The Northrop merger, 2002.** The Form 8-K states that Northrop Grumman "entered into an
Agreement and Plan of Merger dated as of June 30, 2002, by and among TRW Inc., an Ohio
corporation, Northrop Grumman and Richmond Acquisition Corp., an Ohio corporation and
wholly-owned subsidiary of Northrop Grumman", and that "Pursuant to the merger agreement, on
December 11, 2002, Richmond Acquisition Corp. was merged with and into TRW, with TRW
surviving the merger as a wholly-owned subsidiary of Northrop Grumman." The exchange ratio
was 0.5357 Northrop shares per TRW share, the maximum under the collar, and roughly 75.22
million Northrop shares were expected to be issued.

**What became of the businesses.** The 11 December 2002 press release: "TRW Systems will be
renamed Northrop Grumman Mission Systems, with about 15,000 employees and headquartered in
Reston, Va. TRW Space & Electronics will be renamed Northrop Grumman Space Technology, which
has more than 8,600 employees, based in Redondo Beach, Calif." EDGAR's own company record
carries the same event as a name change on CIK 0000100030.

**The antitrust condition.** The 8-K also records that on 11 December 2002 the United States
filed a complaint, a proposed final judgment and a stipulation and order against Northrop
Grumman and TRW, entered by the court that day, effective on the closing of the merger.

### What the transcript claimed that these documents do NOT establish

Triage 1.A10 relays Eric Davis naming TRW as the parent of an unnamed FFRDC he says was
principal investigator on the programme for about 29 years. **Nothing in any filing opened
here supports that.** TRW was a publicly traded corporation, not an FFRDC sponsor in these
records, and no FFRDC is named in them. That claim stays in the triage file. The corporate
record supports the chain and nothing more.

### Draft node

```json
{
  "id": "trw-inc",
  "cls": "institution",
  "label": "TRW Inc.",
  "cluster": "contractor",
  "sub": "Cleveland-based aerospace, defence and automotive prime; acquired BDM 1997, acquired by Northrop Grumman 11 December 2002",
  "tier": "B",
  "C": 1,
  "A": 2,
  "D": 1,
  "dateStart": "1994",
  "dateEnd": "2002-12-11",
  "desc": "TRW Inc. is the middle link of a chain the board already carries at both ends. In November 1997 it agreed to acquire BDM International through a cash tender offer at $29.50 a share, and BDM deregistered a month later. On 11 December 2002 TRW was itself merged into a Northrop Grumman subsidiary, with TRW surviving as a wholly owned subsidiary; TRW Systems became Northrop Grumman Mission Systems at Reston and TRW Space and Electronics became Northrop Grumman Space Technology at Redondo Beach. EDGAR carries the same transition on the company's own CIK. Until now the board reached from BDM to Northrop Grumman with no node in between, and the edge was an assertion where the filings make it a record.",
  "claims": [
    {
      "tier": 1,
      "text": "TRW agreed to acquire BDM in November 1997: 'on November 20, 1997, BDM International, Inc. entered into a Merger Agreement with TRW Inc. and Systems Acquisition Inc., a wholly owned subsidiary of TRW, pursuant to which that subsidiary has commenced a tender offer (the \"Offer\") to purchase all of the outstanding shares of BDM's common stock for a cash price of $29.50 per share.'",
      "source": "BDM International, Inc., Schedule 14D-9, filed 26 November 1997, CIK 0000870763, https://www.sec.gov/Archives/edgar/data/870763/0000950152-97-008353.txt"
    },
    {
      "tier": 1,
      "text": "The Northrop Grumman merger closed on a stated date: 'Pursuant to the merger agreement, on December 11, 2002, Richmond Acquisition Corp. was merged with and into TRW, with TRW surviving the merger as a wholly-owned subsidiary of Northrop Grumman.' The exchange ratio was 0.5357 Northrop shares per TRW share.",
      "source": "Northrop Grumman Corporation, Form 8-K, earliest event 11 December 2002, Item 2, https://www.sec.gov/Archives/edgar/data/1133421/000089843002004580/d8k.htm"
    },
    {
      "tier": 1,
      "text": "The defence businesses were renamed at once: 'TRW Systems will be renamed Northrop Grumman Mission Systems, with about 15,000 employees and headquartered in Reston, Va. TRW Space & Electronics will be renamed Northrop Grumman Space Technology, which has more than 8,600 employees, based in Redondo Beach, Calif.'",
      "source": "Northrop Grumman press release, 11 December 2002, filed as Form 425 on 12 December 2002, https://www.sec.gov/Archives/edgar/data/100030/000089843002004462/d425.htm"
    },
    {
      "tier": 1,
      "text": "The merger required an antitrust consent: on 11 December 2002 the United States filed a complaint, a proposed final judgment and a stipulation and order against Northrop Grumman and TRW, which the court entered the same day and which became effective on the closing of the merger.",
      "source": "Northrop Grumman Corporation, Form 8-K filed 13 December 2002, Item 5(b), https://www.sec.gov/Archives/edgar/data/1133421/000089843002004481/d8k.htm"
    },
    {
      "tier": 1,
      "text": "EDGAR carries the transition on the company's own registration: CIK 0000100030 is listed as NORTHROP GRUMMAN SPACE & MISSION SYSTEMS CORP, 'formerly: TRW INC (filings through 2002-12-23)'.",
      "source": "SEC EDGAR company record, CIK 0000100030, https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=TRW+INC"
    }
  ],
  "sources": [
    { "name": "BDM International, Inc., Schedule 14D-9, filed 26 November 1997", "url": "https://www.sec.gov/Archives/edgar/data/870763/0000950152-97-008353.txt", "date": "1997-11-26" },
    { "name": "Northrop Grumman Corporation, Form 8-K, event 11 December 2002 (Item 2, acquisition of TRW)", "url": "https://www.sec.gov/Archives/edgar/data/1133421/000089843002004580/d8k.htm", "date": "2002-12-20" },
    { "name": "Northrop Grumman Corporation, Form 8-K filed 13 December 2002 (consent decree)", "url": "https://www.sec.gov/Archives/edgar/data/1133421/000089843002004481/d8k.htm", "date": "2002-12-13" },
    { "name": "Northrop Grumman press release of 11 December 2002, filed as Form 425", "url": "https://www.sec.gov/Archives/edgar/data/100030/000089843002004462/d425.htm", "date": "2002-12-12" },
    { "name": "SEC EDGAR company record, CIK 0000100030, formerly TRW INC", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=TRW+INC", "date": "2026-09-02" }
  ],
  "edges": [
    {
      "a": "trw-inc",
      "b": "bdm-international",
      "type": "institutional",
      "claimTier": 1,
      "label": "TRW acquired BDM by cash tender offer, 1997",
      "note": "BDM's own Schedule 14D-9 of 26 November 1997 recites the 20 November merger agreement with TRW Inc. and its subsidiary Systems Acquisition Inc. at $29.50 a share, and BDM filed a Form 15-12G on 29 December 1997.",
      "sources": [{ "name": "BDM International, Inc., Schedule 14D-9, 26 November 1997", "url": "https://www.sec.gov/Archives/edgar/data/870763/0000950152-97-008353.txt", "date": "1997-11-26" }]
    },
    {
      "a": "trw-inc",
      "b": "northrop-grumman",
      "type": "institutional",
      "claimTier": 1,
      "label": "Merged into a Northrop Grumman subsidiary, 11 December 2002",
      "note": "Northrop Grumman's Form 8-K states that Richmond Acquisition Corp. merged with and into TRW on 11 December 2002, leaving TRW a wholly owned subsidiary, with TRW Systems and TRW Space and Electronics renamed as Northrop Grumman Mission Systems and Northrop Grumman Space Technology.",
      "sources": [{ "name": "Northrop Grumman Corporation, Form 8-K, event 11 December 2002", "url": "https://www.sec.gov/Archives/edgar/data/1133421/000089843002004580/d8k.htm", "date": "2002-12-20" }]
    },
    {
      "a": "trw-inc",
      "b": "gerb-northrop-trw-investigation",
      "type": "investigative",
      "claimTier": 2,
      "label": "The subject of the 20 March 2026 corporate-breakaway argument",
      "note": "The video's whole case turns on the 2002 acquisition, which the filings document; its funding-mechanism proposition is an extrapolation and is not in any filing opened here.",
      "sources": [{ "name": "Northrop Grumman Corporation, Form 8-K, event 11 December 2002", "url": "https://www.sec.gov/Archives/edgar/data/1133421/000089843002004580/d8k.htm", "date": "2002-12-20" }]
    }
  ]
}
```

---

## 5. Richard M. Bissell Jr.

**VERDICT: CONFIRMED**, from the CIA's own in-house history, in the fuller 2013 release.

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt | OCR text, 792 KB, of "THE CENTRAL INTELLIGENCE AGENCY AND OVERHEAD RECONNAISSANCE; THE U-2 AND OXCART PROGRAMS, 1954-1974" by **Gregory W. Pedlow and Donald E. Welzenbach**, CIA History Staff monograph. Every page carries "Approved for Release: 2013/06/25" over the struck-through "Secret". This is the archive.org mirror of CIA reading room document 0000190094, in the `ciareadingroom` collection, OCR by the archive. |
| https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf | The CIA Center for the Study of Intelligence copy, 10 MB. **Opened but it has no text layer**, so it was not the copy read. Named here so a later pass does not repeat the attempt blind. |
| https://www.cia.gov/readingroom/document/0000190094 and https://www.cia.gov/readingroom/docs/DOC_0000192682.pdf | Both **NOT OPENED**. Each returned a redirect loop exceeding ten hops to WebFetch, and curl was refused. The reading room is reachable for other paths but not for these two. |

### What the document establishes

**Who he was.** "the Director of Central Intelligence's newly hired Special Assistant for
Planning and Coordination, Richard M. Bissell, Jr." Groton and Yale, a year at the London
School of Economics, a Yale doctorate in 1939, taught economics at Yale and from 1942 at
MIT where he became a full professor in 1948, executive officer of the Combined Shipping
Adjustment Board in the war, deputy director of the Marshall Plan 1948 to 1951, then the
Ford Foundation. "Bissell joined the Agency in late January 1954."

**How he got the programme.** "On 26 November 1954, the day after Thanksgiving, Allen Dulles
called his special assistant, Richard Bissell, into his office to tell him that President
Eisenhower had just approved a very secret program and that Dulles wanted Bissell to take
charge of it." On 3 December 1954 Bissell and Herbert I. Miller represented the Agency at the
Pentagon organisational meeting for the project. The monograph records Dulles's answer when
Bissell asked who would pay: "That wasn't even mentioned. You'll have to work that out."

**Groom Lake, and the date.** "On 12 April 1955 Richard Bissell and Col. Osmund Ritland (the
senior Air Force officer on the project staff) flew over Nevada with Kelly Johnson in a small
Beechcraft plane piloted by Lockheed's chief test pilot, Tony LeVier. They spotted what
appeared to be an airstrip by a salt flat known as Groom Lake, near the northeast corner of
the Atomic Energy Commission's (AEC) Nevada Proving Ground." Then: "Upon returning to
Washington, Bissell discovered that Groom Lake was not part of the AEC proving ground. After
consulting with Dulles, Bissell and Miller asked the Atomic Energy Commission to add the
Groom Lake area to its real estate holdings in Nevada. AEC Chairman Adm. Lewis Strauss
readily agreed, and President Eisenhower also approved the addition of this strip of
wasteland, known by its map designation as Area 51, to the Nevada Test Site." Kelly Johnson
named it Paradise Ranch; when runoff filled the lake it was called Watertown Strip; the base
was ready by July 1955.

**Blue Book.** Under the heading "U-2s, UFOs, AND OPERATION BLUE BOOK", the monograph states
that "BLUE BOOK investigators regularly called on the Agency's Project Staff in Washington to
check reported UFO sightings against U-2 flight logs. This enabled the investigators to
eliminate the majority of the UFO reports, although they could not reveal to the letter
writers the true cause of the UFO sightings. U-2 and later OXCART flights accounted for more
than one-half of all UFO reports during the late 1950s and most of the 1960s."

### What the transcript claimed that this document does NOT establish

Verifier 5's triage row is explicit and this pass agrees with it: two of the Michels maps
make Bissell the origin of a **1933 Magenta briefing** claim, on a single deathbed account.
**Nothing of the kind is in this monograph.** Bissell's name appears 193 times in it and not
once in any such context. The row's instruction, that the claim must not travel with him, is
the right one. Likewise, the monograph's Blue Book passage is the Agency explaining its own
aircraft as the cause of UFO reports; it is a Tier 1 statement about **what the CIA history
says**, and it is an argument against anomaly, not for it. It belongs on the board because
`cia-haines-1997` and `blue-book-special-report-14` already sit near it, and this is the
underlying claim in the Agency's own words.

### Draft node

```json
{
  "id": "richard-m-bissell-jr",
  "cls": "person",
  "label": "Richard M. Bissell Jr.",
  "status": "dead",
  "date": null,
  "loc": "Washington, DC",
  "locId": "l-dc",
  "sub": "CIA Special Assistant for Planning and Coordination from 1954; ran the U-2 project and selected Groom Lake",
  "cluster": "ic",
  "tier": "B",
  "C": 1,
  "A": 3,
  "D": 1,
  "narrative": "Richard Bissell is where the documented record of Area 51 begins, and the board's Nevada material has until now had no origin point. The CIA's own History Staff monograph, in its fuller 2013 release, records that Allen Dulles put him in charge of the U-2 project on 26 November 1954; that on 12 April 1955 he flew over Nevada with Osmund Ritland, Kelly Johnson and Tony LeVier and spotted the airstrip at Groom Lake; that on finding it lay outside the AEC's proving ground he asked the Commission to absorb it, which Chairman Lewis Strauss agreed to and Eisenhower approved; and that the strip's map designation was Area 51. The same monograph records that Blue Book investigators checked their UFO reports against the project's flight logs and were not permitted to tell correspondents the cause. Nothing in it touches the deathbed briefing claim the Michels corpus routes through him, and that claim must not travel with this node.",
  "claims": [
    {
      "tier": 1,
      "text": "Dulles gave him the U-2 project by hand: 'On 26 November 1954, the day after Thanksgiving, Allen Dulles called his special assistant, Richard Bissell, into his office to tell him that President Eisenhower had just approved a very secret program and that Dulles wanted Bissell to take charge of it.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance: The U-2 and OXCART Programs, 1954-1974, CIA History Staff, 2013 release, https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt"
    },
    {
      "tier": 1,
      "text": "He found the site personally and on a dated flight: 'On 12 April 1955 Richard Bissell and Col. Osmund Ritland (the senior Air Force officer on the project staff) flew over Nevada with Kelly Johnson in a small Beechcraft plane piloted by Lockheed's chief test pilot, Tony LeVier. They spotted what appeared to be an airstrip by a salt flat known as Groom Lake, near the northeast corner of the Atomic Energy Commission's (AEC) Nevada Proving Ground.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2, https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Area 51 exists because he asked for it: 'Bissell and Miller asked the Atomic Energy Commission to add the Groom Lake area to its real estate holdings in Nevada. AEC Chairman Adm. Lewis Strauss readily agreed, and President Eisenhower also approved the addition of this strip of wasteland, known by its map designation as Area 51, to the Nevada Test Site.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2, https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt"
    },
    {
      "tier": 1,
      "text": "His project staff serviced Blue Book and withheld the answer: 'BLUE BOOK investigators regularly called on the Agency's Project Staff in Washington to check reported UFO sightings against U-2 flight logs. This enabled the investigators to eliminate the majority of the UFO reports, although they could not reveal to the letter writers the true cause of the UFO sightings.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2, section 'U-2s, UFOs, and Operation BLUE BOOK', https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt"
    },
    {
      "tier": 1,
      "text": "He came to the Agency as an economist and a Marshall Plan administrator, not an operator: a Yale doctorate in 1939, a full professorship at MIT in 1948, executive officer of the Combined Shipping Adjustment Board in the war and deputy director of the Marshall Plan from 1948 to the end of 1951. 'Bissell joined the Agency in late January 1954.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 1, https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt"
    }
  ],
  "sources": [
    { "name": "Gregory W. Pedlow and Donald E. Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance: The U-2 and OXCART Programs, 1954-1974, CIA History Staff, approved for release 25 June 2013 (CIA reading room document 0000190094)", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" },
    { "name": "Same monograph, CIA Center for the Study of Intelligence copy (no text layer)", "url": "https://www.cia.gov/resources/csi/static/CIA-and-U2-Program.pdf", "date": "2026-09-02" }
  ],
  "edges": [
    {
      "a": "richard-m-bissell-jr",
      "b": "cia",
      "type": "institutional",
      "claimTier": 1,
      "label": "Special Assistant to the DCI for Planning and Coordination from January 1954",
      "note": "The Agency's own history names him in that post and records Dulles handing him the U-2 project in November 1954.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    },
    {
      "a": "richard-m-bissell-jr",
      "b": "l-groom-lake",
      "type": "geographic",
      "claimTier": 1,
      "label": "Selected the site on 12 April 1955",
      "note": "He and Ritland flew over Nevada with Kelly Johnson and Tony LeVier, landed on the lakebed and walked the strip, and the monograph notes that a landing on the airstrip itself would probably have killed the key figures in the project.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    },
    {
      "a": "richard-m-bissell-jr",
      "b": "l-area51",
      "type": "institutional",
      "claimTier": 1,
      "label": "Asked the AEC to absorb the land that became Area 51",
      "note": "On finding the site lay outside the proving ground he and Miller asked the Commission to add it to its Nevada holdings; Strauss agreed and Eisenhower approved the addition of the strip known by its map designation as Area 51.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    },
    {
      "a": "richard-m-bissell-jr",
      "b": "project-blue-book",
      "type": "denial",
      "claimTier": 1,
      "label": "His project staff resolved Blue Book's reports and withheld the reason",
      "note": "The CIA history states that Blue Book investigators checked reported sightings against U-2 flight logs held by the Agency's project staff and could not reveal the true cause to the people who had written in.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    },
    {
      "a": "richard-m-bissell-jr",
      "b": "lockheed-skunk-works",
      "type": "programmatic",
      "claimTier": 1,
      "label": "Ran the project Kelly Johnson built the aircraft for",
      "note": "Kelly Johnson was on the 12 April 1955 site flight with Lockheed's chief test pilot, and named the resulting base the Paradise Ranch to make it sound better to his workers.",
      "sources": [{ "name": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, 2013 release, chapter 2", "url": "https://archive.org/download/cia-readingroom-document-0000190094/0000190094_djvu.txt", "date": "2013-06-25" }]
    }
  ]
}
```

---

## Notes on method, and what a later pass should not repeat

- **Every edge above points at a node id confirmed present in `data/the-program.json` by
  this session.** The brief says edges go to existing ids, so the obvious cross-links inside
  this pass are deliberately not drawn: no `atomic-energy-commission` to
  `bluegill-triple-prime` edge, no `richard-m-bissell-jr` to `atomic-energy-commission` edge,
  no `harald-b-malmgren` to `bluegill-triple-prime` edge. All three are supported by
  documents opened here and should be added when the nodes are merged together, not before.
- **`tier`, `C`, `A` and `D` above are first cuts.** `regrade.py` re-derives node tiers on a
  global pass, so the letters will move.
- **`www.dtra.mil` refuses WebFetch with HTTP 403 and returns an HTML error body to curl.**
  DNA 6039F is served there and could not be read from that host. The DTIC mirror on
  archive.org has it as `DTIC_ADA122341`.
- **`www.cia.gov/readingroom/document/...` and `/readingroom/docs/*.pdf` returned redirect
  loops** to WebFetch on this attempt and were refused to curl. The archive.org
  `ciareadingroom` mirror carries the same documents by the same id with an OCR text layer,
  and that is the route that worked.
- **`www.tributearchive.com` and `www.fauquiernow.com` returned HTTP 403.** Both carry the
  Malmgren obituary. The funeral home's own page answered curl.
- **Statutes at Large PDFs on govinfo defeat WebFetch** because the summariser receives raw
  PDF bytes. Downloading them and running `pdftotext -layout` gives clean text with the
  marginal captions intact, which is how the section numbers above were located.
