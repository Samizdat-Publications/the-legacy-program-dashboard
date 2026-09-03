# Verified leads: Danny Jones corpus, the Wright-Patterson, materials and test cluster (verifier 4)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over six
candidates named in this agent's instructions and drawn from section A of
`research/leads/dannyjones-triage-1.md`, `-2.md`, `-3.md`, `-4.md` and `-5.md`, run against
`research/leads/VERIFY-BRIEF-DANNYJONES-2026-09-03.md` and, through it, against
`research/leads/VERIFY-BRIEF-2026-09-02.md` and the format of
`research/leads/verified-area52-1.md`.

**Verified 3 September 2026.** Every URL below was opened by this session and returned the
document described. `CLAUDE.md` section 2 governs: nothing here is asserted that was not
opened. Walls are recorded as walls.

**The wall that shaped this pass: DTIC does not reach this machine.** `apps.dtic.mil`
returns HTTP 403 to both curl and WebFetch on every PDF path tried
(`/sti/tr/pdf/`, `/sti/pdfs/`), and `apps.dtic.mil/sti/citations/` returns a page reading
"Under Maintenance". Every `*.af.mil` host tried is also 403 from here (`www.af.mil`,
`www.wpafb.af.mil`, `www.afhra.af.mil`), as is `media.defense.gov`. Two candidates were
saved by finding the same or better records off DTIC: **govinfo carries an official Air
Force base history that adjudicates Exon**, and **NASA's technical reports server carries
two federal reports that adjudicate nitinol**. One candidate was not saved and is NOT
OPENED.

**Board state, read from `data/the-program.json` by this session rather than taken from a
triage file.** No id containing `exon`, `ristvet`, `nitinol`, `buehler`, `naval-ordnance`,
`bell-aircraft`, `talbert`, `bergmann`, `weber`, `chapel`, `norton`, `oxcart`, `u-2`,
`area-51`, `flight-dynamics` or `wadc` exists. The ids used in the draft edges below were
each grepped and found: `l-wright-patterson`, `usaf`, `foreign-technology-division`,
`nathan-twining`, `battelle`, `nasa`, `us-navy`, `george-trimble`, `rias-inc`,
`general-dynamics`, `sperry-rand`, `gordon-gray`, `institute-of-field-physics`,
`louis-witten`, `thomas-townsend-brown`, `bluegill-triple-prime`, `dtra`, `cia`, `l-area51`,
`haines-cia-history`.

## Summary

| # | Lead | Verdict | Note |
|---|---|---|---|
| 1 | Arthur E. Exon, Wright-Patterson commander | CONFIRMED, and the rank CORRECTED | An official Air Force base history lists him as installation commander from August 1964, as a **Colonel** |
| 2 | Byron L. Ristvet, and the Wright-Patterson Flight Dynamics Laboratory report on the Bluegill pods | NOT OPENED | DTIC is walled from this machine and the report is not on the archive.org DTIC mirror, OSTI or archive.org |
| 3 | Naval Ordnance Laboratory and the first Nitinol | CONFIRMED for the laboratory; the transcript's 1954 CONTRADICTED; the board's Battelle 1948-49 lineage UNSUPPORTED by the federal literature Battelle itself wrote | Earliest NOL nitinol report cited anywhere in the federal record is August 1961; the patent was filed 1 December 1961 |
| 4 | Bell Aircraft and Talbert's Herald Tribune series | CONFIRMED, and the transcript CONTRADICTED on date, person and substance | November 1955, not 1953; Trimble was a vice-president, not chief executive; and Thomas Townsend Brown appears nowhere in the three articles |
| 5 | Peter Bergmann, Joseph Weber and the Chapel Hill conference | CONFIRMED, and the board's own sponsorship claim REFINED | Both attended; WADC was one of four financial supporters, and IUPAP was the sponsor |
| 6 | Norton AFB and the loss of the CIA's Area 51 records | CONTRADICTED on the identification, unsupported on the rest | The only "Norton" in the CIA's history is Garrison Norton, a man; the study's span ends in 1974 |

**The five findings that matter, in order:**

1. **Nitinol did not come from Battelle in 1948-49, and the report that says where it did
   come from was written by Battelle.** NASA SP-5110, `55-Nitinol: The Alloy With a Memory`,
   was prepared for NASA by Battelle Memorial Institute and published in 1972. Its first
   sentence reads: "Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance
   Laboratory developed a series of engineering alloys that possess a unique mechanical
   (shape) 'memory'." Its acknowledgments say "All the information in the report covers the
   period from 1955 to March 31, 1970." Its reference list contains no Battelle work before
   1968 and no NOL nitinol report before NOLTR 61-75 of 3 August 1961. The board's `battelle`
   node carries the Bragalia allegation that missing 1948-49 Wright-Patterson-sponsored
   Battelle reports are "the research lineage of nitinol shape-memory metal". The
   authoritative federal literature review, commissioned from Battelle, does not contain that
   lineage.
2. **Exon commanded Wright-Patterson as a colonel, not as a general.** The Air Force's own
   base history lists installation commanders in Appendix B: "Colonel Glen McClernon August
   1962 / Colonel Arthur E. Exon August 1964 / Colonel Jowell C. Wise December 1965". The
   corpus reaches him as "General Exon". On the day he held the office the Air Force's own
   list gives him as a colonel, and his successor takes the post in December 1965, not
   January 1966.
3. **Talbert's series contains no Thomas Townsend Brown, and it is dated November 1955.**
   The three New York Herald Tribune articles of 20, 21 and 22 November 1955 name Trimble,
   Lawrence D. Bell, William P. Lear, Igor Sikorsky, Grover Loening, Clarence Birdseye,
   Vaclav Hlavaty, Burkhard Heim and Pascual Jordan, and list Glenn L. Martin, Convair, Bell
   Aircraft, Sikorsky, Lear, Clarke Electronics and the Sperry Gyroscope Division of
   Sperry-Rand as the firms involved. Brown is absent from all three. The board's
   electrogravitics cluster is built around him; the contemporaneous press record that the
   whole "aerospace executives said this on the record" claim rests on does not mention him.
4. **The same articles attach Sperry-Rand to the electrogravitics story with a document.**
   Section E of the 30 August candidates file left `sperry-rand` deliberately unattached
   because MacArthur has no node. Talbert's first article names "the Sperry Gyroscope
   Division of Sperry-Rand Corp., of Great Neck, L. I." among the firms with "scientists
   investigating the gravity problem". That is a different and better reason to attach it.
5. **The CIA history's "Norton" is a person, and the study cannot reach 1979.** The 2013
   release of Pedlow and Welzenbach indexes "Norton, Garrison" at pages 14-15, 31, 70, 260
   and 331, and has no entry for Norton Air Force Base. Its Preface states the programme
   "began with President Eisenhower's authorization of the U-2 project in late 1954 and ended
   with the transfer of the remaining Agency U-2s to the Air Force in 1974". A 1979 records
   handover is outside the document entirely. What the document does carry is a records-loss
   statement of a different kind, in its own Foreword: the authors "have found records that
   were nearly irretrievably lost", and the Preface says "Agency documentation on the
   prehistory of the U-2 project is very sketchy".

---

## 1. Arthur E. Exon

**VERDICT: CONFIRMED for the office and its start date. The rank is CORRECTED by the record,
and the end date the secondary literature gives is CONTRADICTED by it.**

### What was opened

| URL | What is at it |
|---|---|
| https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo111353/pdf/GOVPUB-D301-PURL-gpo111353.pdf | `Wright-Patterson Air Force Base: The First Century`, History Office, Air Force Life Cycle Management Center, Air Force Materiel Command, Wright-Patterson Air Force Base, Ohio, 2015. 76 pages. GPO package GOVPUB-D301-PURL-gpo111353. Text extracted and searched in full; read at Appendix B, page 44 of the publication |
| http://www.nicap.org/roswell/roswell_exon.htm | Kevin Randle's narrative of Exon's Roswell remarks. Opened, and it is **not** a record: it gives dates but attributes them to the author's own research and ends with a citation to a paperback |

**Walls.** `https://www.af.mil/About-Us/Biographies/Display/Article/104819/brigadier-general-arthur-ernest-exon/`
returns HTTP 403 to WebFetch and to curl with a browser user agent; an Akamai access-denied
page is what comes back. `www.af.mil`, `www.wpafb.af.mil` and `www.afhra.af.mil` all return
403 at their roots as well. The official USAF biography and the AFHRA command histories were
therefore NOT OPENED, and the finding below rests on the base's own published history
instead, which is the better record for the specific question of who commanded the
installation and when.

### What the document establishes

Appendix B, "WRIGHT-PATTERSON AIR FORCE BASE INSTALLATION COMMANDERS", is a continuous list
from April 1944. In sequence it reads: "Colonel Glen McClernon August 1962 / Colonel Arthur
E. Exon August 1964 / Colonel Jowell C. Wise December 1965". Every entry gives the month and
year the officer took the post, so Exon's tenure as installation commander runs from August
1964 to December 1965. The list gives his rank in the post as **Colonel**. The officers from
1958 onward are listed as colonels and those from 1945 to 1958 as brigadier generals, so the
rank column carries real information rather than a convention.

Exon is named nowhere else in the 76 pages. The publication is an installation history, not
a personnel record, and it says nothing about him beyond the appendix line.

### What the transcripts and the triage row claimed that this does NOT establish

| Claim | What the record says |
|---|---|
| Strieber, 13 / 259 / 0:37:23 to 0:47:13, reaches Exon as "General Exon" and as Wright-Patterson's commander | The base's own history gives him as **Colonel** Arthur E. Exon in the post. The promotion to brigadier general is not in this document, and the af.mil biography that would date it is walled |
| The triage row and the secondary literature give January 1966 as his departure | Appendix B puts his successor, Colonel Jowell C. Wise, in the post from **December 1965** |
| Strieber's uncle, the claimed telephone conversations, and everything Exon is said to have said about 1947 | The document touches none of it. It establishes the office and its dates and nothing more. That is what the brief asked of it |
| The row's framing of Wright-Patterson custody | The base history contains no reference to any recovery or exploitation of unidentified material, and no reference to Roswell |

### Draft node

```json
{
  "id": "arthur-e-exon",
  "cls": "person",
  "label": "Arthur E. Exon",
  "dateStart": "1964-08",
  "dateEnd": "1965-12",
  "desc": "Arthur E. Exon was installation commander of Wright-Patterson Air Force Base from August 1964 to December 1965. The Air Force's own centennial history of the base lists him in its table of installation commanders as a colonel, between Colonel Glen McClernon and Colonel Jowell C. Wise. He reaches this board only through the Danny Jones corpus, where Whitley Strieber calls him General Exon and attributes to him an account of 1947 material at this installation. Nothing in the opened record touches that account, and the record corrects the rank the corpus gives him for the period he actually held the command.",
  "claims": [
    {
      "tier": 1,
      "text": "The Air Force's own base history lists the installation commanders in sequence: 'Colonel Glen McClernon August 1962 / Colonel Arthur E. Exon August 1964 / Colonel Jowell C. Wise December 1965'. Exon held the post as a colonel, from August 1964, and was succeeded in December 1965.",
      "source": "Wright-Patterson Air Force Base: The First Century, History Office, Air Force Life Cycle Management Center, Air Force Materiel Command, 2015, Appendix B, p. 44. https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo111353/pdf/GOVPUB-D301-PURL-gpo111353.pdf"
    },
    {
      "tier": 1,
      "text": "The same 76-page installation history names Exon in no other place and records nothing about him beyond the appendix entry.",
      "source": "Wright-Patterson Air Force Base: The First Century, 2015, searched in full. https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo111353/pdf/GOVPUB-D301-PURL-gpo111353.pdf"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, episode 259, at 0:37:23 to 0:47:13 and 1:12:05, Whitley Strieber refers to Exon as a general and as the commander of Wright-Patterson, and attributes to him and to Strieber's uncle an account of 1947 material at the installation. The opened Air Force record gives his rank in the post as colonel and carries none of the account.",
      "source": "research/leads/dannyjones-corpus-13.md, batch 13, episode 259."
    }
  ],
  "sources": [
    "https://www.govinfo.gov/content/pkg/GOVPUB-D301-PURL-gpo111353/pdf/GOVPUB-D301-PURL-gpo111353.pdf"
  ],
  "edges": [
    { "to": "l-wright-patterson", "type": "institutional", "note": "Exon was the installation commander of Wright-Patterson Air Force Base from August 1964 to December 1965 per the base's own published history." },
    { "to": "usaf", "type": "institutional", "note": "He held the command as a United States Air Force officer, listed as a colonel in the Air Force's own installation-commander table." }
  ]
}
```

**Do not draft an edge from Exon to `foreign-technology-division` or to `nathan-twining`.**
The base history does not connect him to either, and the only thing that does is the
transcript.

---

## 2. Byron L. Ristvet, and the Wright-Patterson Flight Dynamics Laboratory report on the Bluegill instrumentation pods

**VERDICT: NOT OPENED, both halves.**

### What was tried

| Route | Result |
|---|---|
| `https://apps.dtic.mil/sti/pdfs/ADA995482.pdf`, the identifier a search result attaches to the pod report | HTTP 403 to WebFetch and to curl with a browser user agent |
| `https://apps.dtic.mil/sti/tr/pdf/ADA055688.pdf`, a second DTIC path, tested to see whether the wall was path-specific | HTTP 403 |
| `https://apps.dtic.mil/sti/citations/ADA995482` | HTTP 200, but the body is a page reading "Under Maintenance / Our Site is Getting an Upgrade" |
| `https://archive.org/details/DTIC_ADA995482` and `https://archive.org/download/DTIC_ADA995482/DTIC_ADA995482.pdf` | 404 and 503. The archive.org DTIC mirror does not hold this item |
| archive.org advanced search, `identifier:DTIC_ADA9954*` | 0 results |
| archive.org advanced search, `"POR-2037" OR "WT-2037"` | 0 results |
| archive.org advanced search, `"Blue Gill" AND "King Fish"` | 3 results, all unrelated FISHBOWL diagnostics reports (AD0353599, AD0355326, AD0354288) |
| OSTI API, `"POR-2037"` and `"Close-In Thermal and X-ray Vulnerability"` | 0 records each |
| OSTI and archive.org, `Ristvet` | Nothing by this author. archive.org returns a Washington district-court docket for a different Ristvet and two unrelated books |

### What this means for the row

The row is a good row and it stays open. What a search result carries is a title, a project
number and an abstract; the row's whole value is the sentence the speaker gives near
verbatim, denying that even the closest pod was immersed in the fireball, and that sentence
lives in the report's text. **A search-result snippet is not an opened document**, so nothing
about the pods, their slant ranges or their recovery is asserted here, and no report number
is asserted either.

The board's `bluegill-triple-prime` node already records, at Tier 1, that DNA 6040F "carries
no reference to any unidentified object, unknown craft, anomalous observation, recovery or
debris associated with the detonation". Whatever the Flight Dynamics Laboratory report says,
it is a second document and it has not been read.

Note for the next pass: the transcript's own attribution should be checked before this is
opened again. The row's claim is that Ristvet applied a sanitization to imagery in 1998. The
Bluegill node's existing Tier 1 finding, that KETTLE is a DOMINIC aircraft call sign and not
a film, already cuts against the "Kettle footage" framing the row inherits.

**No draft node.**

---

## 3. Naval Ordnance Laboratory and the first Nitinol

**VERDICT: CONFIRMED that the discovery belongs to the Naval Ordnance Laboratory.
CONTRADICTED on the transcript's date of 1954. And the result the brief expected is present:
the board's Battelle 1948-49 nitinol lineage does not appear in the federal literature,
including in the federal literature Battelle itself wrote.**

### What was opened

| URL | What is at it |
|---|---|
| https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf | NASA SP-5110, `55-Nitinol: The Alloy With a Memory: Its Physical Metallurgy, Properties, and Applications`, by C. M. Jackson, H. J. Wagner and R. J. Wasilewski, "Prepared under contract for NASA by Battelle Memorial Institute", Technology Utilization Office, 1972. 94 pages, Library of Congress catalog card number 74-177266. Text extracted and read: front matter, acknowledgments, Chapter 1 and the reference list |
| https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf | NASA CR-1433, `Nitinol Characterization Study`, by William B. Cross, Anthony H. Kariotis and Frederick J. Stimler, Goodyear Aerospace Corporation report GER 14188, under contract NAS 1-7522 for Langley Research Center, September 1969. 72 pages. Foreword and the "Review of Nitinol Properties and Unique Behavior" section read |
| https://patents.google.com/patent/US3174851A/en | US Patent 3,174,851, "Nickel-base alloys", William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy. **Filed 1 December 1961**, granted 23 March 1965 |

`https://apps.dtic.mil/sti/tr/pdf/ADA055688.pdf`, the NOL and NSWC source manual for nitinol,
was NOT OPENED: 403, as above.

### What the documents establish

**The laboratory, and the name.** SP-5110 opens: "Some 10 years ago, Buehler and Wiley of the
U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique
mechanical (shape) 'memory'. The generic name of the series of alloys is 55-Nitinol, where
Nitinol stands for Nickel Titanium Naval Ordnance Laboratory." CR-1433 opens its review
section: "Since the recent discovery, at the U.S. Naval Ordnance Laboratory, of the
extraordinary shape recovery or mechanical 'memory' property of the equiatomic NiTi
intermetallic compound designated 55-Nitinol". The transcript's institution is right, and the
mapper's name for it, "Naval Ordnance Research Labs", is wrong.

**The date.** Four independent handles, all landing between 1959 and 1962, none reaching 1954:

| Handle | What it gives |
|---|---|
| SP-5110's own framing, published 1972 | "Some 10 years ago", so about 1962 |
| SP-5110's acknowledgments | "All the information in the report covers the period from 1955 to March 31, 1970" |
| The earliest NOL nitinol report anywhere in SP-5110's reference list | NOLTR 61-75 (AD 266607), Buehler and Wiley, "The Properties of TiNi and Associated Phases", U.S. Naval Ordnance Laboratory, **3 August 1961** |
| The patent | Filed **1 December 1961**, granted 23 March 1965 |
| CR-1433, September 1969 | Calls it "the recent discovery" |

**Where Battelle actually sits in the record, and where it does not.** Battelle is present in
both documents, and its role is late and contractual, not originating. SP-5110 was prepared
for NASA "by Battelle Memorial Institute". CR-1433's Foreword: "As subcontractor to GAC,
Battelle Memorial Institute (BMI), Columbus, Ohio, processed the basic Nitinol rod into
diameters of 100, 20, 15, and 10 mils", with the raw material "supplied by Mr. William J.
Buehler of the Magnetism and Metallurgy Division of the U.S. Naval Ordnance Laboratory (NOL),
Silver Spring, Maryland". The earliest Battelle item in SP-5110's reference list is a summary
report of 14 June 1968. Nothing in either document refers to Battelle nickel-titanium work of
1948-49, to Wright-Patterson sponsorship of any nitinol work, or to a Los Alamos contract.

### What the transcript and the board claimed that these documents do NOT establish

| Claim | What the record says |
|---|---|
| Rys, 28 / 181 / 1:15:27: the first Nitinol discovery belongs to the Naval Ordnance Laboratory and is dated **1954** | The laboratory is right. The date is not supported by any of the handles above. The earliest NOL nitinol report is August 1961 and the patent was filed December 1961 |
| The board's `battelle` node, Tier 2: researchers including Bragalia allege that 1948-49 Wright-Patterson-sponsored Battelle reports are "the research lineage of nitinol shape-memory metal", missing from both archives | Neither opened document contains that lineage. This is an absence, and an absence is not a disproof: it does not show the alleged reports do not exist. What it does show is that the standard federal literature review of the alloy, commissioned from Battelle in 1972, traces the alloy to Buehler and Wiley at NOL around 1962 and cites no Battelle nickel-titanium work earlier than 1968 |
| The board's `battelle` node, Tier 2: Brandenburg's claim of a 1949 Los Alamos to Battelle contract "around nitinol", declassified in the 1960s | Neither document contains any Los Alamos nitinol contract, and neither refers to any declassification |

### Draft node

```json
{
  "id": "naval-ordnance-laboratory",
  "cls": "institution",
  "label": "U.S. Naval Ordnance Laboratory (White Oak, Silver Spring)",
  "date": "1961-08-03",
  "desc": "The U.S. Naval Ordnance Laboratory at Silver Spring, Maryland is where William J. Buehler and Raymond C. Wiley developed the nickel-titanium shape-memory alloys named 55-Nitinol, the acronym standing for Nickel Titanium Naval Ordnance Laboratory. It reaches this board because the board's strongest materials claim runs the other way: an allegation, carried at Tier 2 on the Battelle node, that the alloy's research lineage is a set of missing 1948-49 Wright-Patterson-sponsored Battelle reports. Two federal reports opened for this pass, one of them written by Battelle for NASA, place the discovery at NOL around 1959 to 1962, cite no NOL nitinol report before August 1961, and cite no Battelle nickel-titanium work before 1968. The Danny Jones corpus dates the NOL discovery to 1954; the record does not support that either.",
  "claims": [
    {
      "tier": 1,
      "text": "NASA SP-5110, prepared for NASA by Battelle Memorial Institute in 1972, opens: 'Some 10 years ago, Buehler and Wiley of the U.S. Naval Ordnance Laboratory developed a series of engineering alloys that possess a unique mechanical (shape) memory. The generic name of the series of alloys is 55-Nitinol, where Nitinol stands for Nickel Titanium Naval Ordnance Laboratory.'",
      "source": "NASA SP-5110, 55-Nitinol: The Alloy With a Memory, C. M. Jackson, H. J. Wagner and R. J. Wasilewski, Battelle Memorial Institute for the NASA Technology Utilization Office, 1972, Chapter 1, p. 1. https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf"
    },
    {
      "tier": 1,
      "text": "The earliest Naval Ordnance Laboratory nitinol report cited anywhere in SP-5110's reference list is NOLTR 61-75 (AD 266607), Buehler and Wiley, 'The Properties of TiNi and Associated Phases', U.S. Naval Ordnance Laboratory, 3 August 1961. The report's own acknowledgments state that 'All the information in the report covers the period from 1955 to March 31, 1970.'",
      "source": "NASA SP-5110, references 12 and 74, and Acknowledgments, p. iv. https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf"
    },
    {
      "tier": 1,
      "text": "US Patent 3,174,851, 'Nickel-base alloys', by William J. Buehler and Raymond C. Wiley, assigned to the United States as represented by the Secretary of the Navy, was filed on 1 December 1961 and granted on 23 March 1965.",
      "source": "US Patent 3,174,851. https://patents.google.com/patent/US3174851A/en"
    },
    {
      "tier": 1,
      "text": "Battelle's documented role in the alloy is late and contractual. NASA CR-1433 of September 1969 records that the nitinol was 'supplied by Mr. William J. Buehler of the Magnetism and Metallurgy Division of the U.S. Naval Ordnance Laboratory (NOL), Silver Spring, Maryland', and that 'As subcontractor to GAC, Battelle Memorial Institute (BMI), Columbus, Ohio, processed the basic Nitinol rod'. The same report calls the NOL work 'the recent discovery'.",
      "source": "NASA CR-1433, Nitinol Characterization Study, Goodyear Aerospace Corporation report GER 14188 under contract NAS 1-7522 for NASA Langley Research Center, September 1969, Foreword p. iii and p. 2. https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, episode 181, at 1:15:27, the guest credited the first Nitinol discovery to the Naval Ordnance Laboratory and dated it 1954. The laboratory is corroborated by the federal record; the date is not. No opened document places any NOL nitinol work before 1961.",
      "source": "research/leads/dannyjones-corpus-28.md, batch 28, episode 181."
    }
  ],
  "sources": [
    "https://ntrs.nasa.gov/api/citations/19720022818/downloads/19720022818.pdf",
    "https://ntrs.nasa.gov/api/citations/19690026989/downloads/19690026989.pdf",
    "https://patents.google.com/patent/US3174851A/en"
  ],
  "edges": [
    { "to": "us-navy", "type": "institutional", "note": "The Naval Ordnance Laboratory was a Navy laboratory; the 55-Nitinol patent is assigned to the United States as represented by the Secretary of the Navy." },
    { "to": "battelle", "type": "research", "note": "Battelle Memorial Institute wrote the 1972 NASA literature review of 55-Nitinol and was a 1967-69 processing subcontractor for it; the review traces the alloy to the Naval Ordnance Laboratory around 1962 and cites no Battelle nickel-titanium work before 1968." },
    { "to": "nasa", "type": "research", "note": "NASA's Technology Utilization Office commissioned SP-5110 and NASA Langley commissioned CR-1433, the two federal reports that date and attribute the alloy." }
  ]
}
```

**A note the next pass should not undo.** If this node is built, the `battelle` node's
existing Tier 2 Bragalia claim stays. The finding is not that Bragalia is wrong; it is that
the federal literature carries a different, dated and documented origin, and the board should
carry both with the record's date on the record's side.

---

## 4. Bell Aircraft Corporation and Ansel Talbert's Herald Tribune series

**VERDICT: CONFIRMED that the series exists, is dated November 1955, and quotes named
aerospace executives on gravity control. The transcript is CONTRADICTED on the date, on who
said it, and on what was said.**

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/talbert1ny/talbert1ny_djvu.txt | Page-image scan and OCR of "Conquest of Gravity Aim Of Top Scientists in U. S.", by Ansel E. Talbert. The page carries a ProQuest Historical Newspapers citation header reading "New York Herald Tribune (1926-1962); Nov 20, 1955 ... pg. 1" |
| https://archive.org/download/talbert2ny/talbert2ny_djvu.txt | "Space-Ship Marvel Seen If Gravity Is Outwitted", same header, "Nov 21, 1955" |
| https://archive.org/download/talbert3ny/talbert3ny_djvu.txt | "New Air Dream, Planes Flying Outside Gravity", same header, "Nov 22, 1955" |

**Provenance, stated plainly.** What was opened is a ProQuest Historical Newspapers page
image of each article, uploaded to the Internet Archive on 9 February 2024 by an anonymous
account, under the descriptions "Ansel Talbert Herald Tribune antigravity series 1 of 3",
"2 of 3" and "3 of 3". It is not a library microfilm consulted directly. Each page carries
the newspaper's own layout, the byline, the series standfirst and the copyright line for
1955, New York Herald Tribune Inc. The OCR is imperfect and single words are visibly garbled,
so nothing is quoted here from a passage where the OCR is unclear.

### What the documents establish

**The series and its dates.** Three articles, 20, 21 and 22 November 1955, by "Ansel E.
Talbert, Military and Aviation Editor". Each carries the standfirst identifying it as one of
a series of three "on new pure and applied research into the mysteries of gravity and efforts
to devise ways to counteract it".

**The firms.** Part one lists them: "Aircraft industry firms now participating or actively
interested in gravity include the Glenn L. Martin Co. of Baltimore ... Convair of San Diego
... Bell Aircraft of Buffalo, builders of the first piloted airplane to fly faster than sound
and a current jet 'vertical take-off and landing' airplane, and Sikorsky Division of United
Aircraft". It continues: "Lear, Inc., of Santa Monica ... Clarke Electronics, of Palm
Springs, Calif. ... and the Sperry Gyroscope Division of Sperry-Rand Corp., of Great Neck, L.
I. ... also have scientists investigating the gravity problem."

**Bell.** Part three, 22 November 1955, quotes the company's founder directly, under the
subhead "Bell is Optimistic": "Lawrence D. Bell, whose company in Buffalo built the first
piloted aircraft in history to fly faster than sound, is certain that practical results will
come out of current gravity research. He told this correspondent: 'Aviation as we know it is
on the threshold of amazing new concepts.'" His statement closes: "Our next step will be to
prove that we can operate outside the earth's atmosphere and the third will be to operate
outside the gravity of the earth."

**Trimble, and the atom-bomb comparison.** Part one captions him "George S. Trimble jr.,
vice-president in charge of advanced design planning of Martin Aircraft Corp." and says he is
"organizing a new Research Institute for Advanced Study to push a program of theoretical
research on gravitational effects", with Martin "building between Washington and Baltimore a
new laboratory for the Research Institute for Advanced Study". Part three quotes him: "I
think we could do the job in about the time that it actually required to build the first atom
bomb if enough trained scientific brain-power simultaneously began thinking about and working
towards a solution", and "I know that if Washington decides it will be vital to our national
survival to go where we want and to do what we want without having to worry about gravity,
we'd find the answer rapidly."

**The Institute of Field Physics, under its earlier name, and Gordon Gray.** Part one: "A
proposal to establish at the University of North Carolina at Chapel Hill, N. C., an
'Institute of Pure Physics' primarily to carry on theoretical research on gravity was
approved earlier this month by the university's board of trustees. This had the approval of
Dr. Gordon Gray, who has since retired as president of the university." It adds: "Funds to
make the institute possible were collected by Agnew H. Bahnson jr., an industrialist of
Winston Salem, N. C.", and "The directorship has been offered to Dr. Bryce S. DeWitt of the
Radiation Laboratory at the University of California at Berkeley".

### What the transcript claimed that these documents do NOT establish

| Jorjani, 12 / 248 / 2:34:20 to 2:35:18 | What the articles say |
|---|---|
| The reporting is dated **1953** | 20, 21 and 22 November **1955** |
| Martin's **chief executive** was quoted | George S. Trimble jr., **vice-president in charge of advanced design planning**. The articles quote no chief executive of Martin |
| With Manhattan-Project-scale **funding** the company could put such **engines into production** "in a few years" | Trimble's comparison is to the **time** the first atom bomb took, not to its funding, and the thing he says could be done is finding "the answer", not producing engines. The word engines does not appear in his quoted remarks |
| Bell Aircraft made "the same public electro-gravitics claims" (12 / 248 / 2:35:18) | Bell Aircraft is named as a participating firm, and Lawrence D. Bell is quoted on gravity research generally. The electro-gravitational language in the series belongs to William P. Lear, who speaks of "artificial electro-gravitational fields", not to Bell |
| The board's electrogravitics cluster centres on `thomas-townsend-brown` | **Brown appears in none of the three articles.** Neither does Winterhaven, nor any Navy or Air Force electrogravitics contract |

### Draft nodes

```json
{
  "id": "talbert-gravity-series-1955",
  "cls": "document",
  "label": "Ansel E. Talbert, three-part gravity series, New York Herald Tribune, 20-22 November 1955",
  "date": "1955-11-20",
  "desc": "Three consecutive front-page articles by Ansel E. Talbert, Military and Aviation Editor of the New York Herald Tribune, published 20, 21 and 22 November 1955 under the titles 'Conquest of Gravity Aim Of Top Scientists in U. S.', 'Space-Ship Marvel Seen If Gravity Is Outwitted' and 'New Air Dream, Planes Flying Outside Gravity'. They are the contemporaneous press record behind every later claim that American aerospace executives said on the record in the 1950s that gravity could be controlled. They name the firms, quote Lawrence D. Bell, William P. Lear and George S. Trimble jr. directly, and report the founding of the Chapel Hill gravity institute under an earlier name. They do not mention Thomas Townsend Brown.",
  "claims": [
    {
      "tier": 1,
      "text": "The series lists the firms: 'Aircraft industry firms now participating or actively interested in gravity include the Glenn L. Martin Co. of Baltimore ... Convair of San Diego ... Bell Aircraft of Buffalo ... and Sikorsky Division of United Aircraft', and adds 'Lear, Inc., of Santa Monica ... Clarke Electronics, of Palm Springs, Calif., and the Sperry Gyroscope Division of Sperry-Rand Corp., of Great Neck, L. I.'",
      "source": "Ansel E. Talbert, 'Conquest of Gravity Aim Of Top Scientists in U. S.', New York Herald Tribune, 20 November 1955, p. 1 and continuation p. 36. Page image at https://archive.org/download/talbert1ny/talbert1ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Lawrence D. Bell, founder and president of Bell Aircraft Corp. of Buffalo, is quoted directly: 'Aviation as we know it is on the threshold of amazing new concepts', and 'Our next step will be to prove that we can operate outside the earth's atmosphere and the third will be to operate outside the gravity of the earth.'",
      "source": "Ansel E. Talbert, 'New Air Dream, Planes Flying Outside Gravity', New York Herald Tribune, 22 November 1955, p. 1. Page image at https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "George S. Trimble jr. is identified as 'vice-president in charge of advanced design planning of Martin Aircraft Corp.' and as 'organizing a new Research Institute for Advanced Study', and is quoted: 'I think we could do the job in about the time that it actually required to build the first atom bomb if enough trained scientific brain-power simultaneously began thinking about and working towards a solution.'",
      "source": "Talbert, New York Herald Tribune, 20 November 1955 (caption and continuation p. 36) and 22 November 1955 (continuation p. 10). https://archive.org/download/talbert1ny/talbert1ny_djvu.txt and https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The series reports the Chapel Hill institute at its founding, under an earlier name: 'A proposal to establish at the University of North Carolina at Chapel Hill, N. C., an Institute of Pure Physics primarily to carry on theoretical research on gravity was approved earlier this month by the university's board of trustees. This had the approval of Dr. Gordon Gray, who has since retired as president of the university.' It names Agnew H. Bahnson jr. as the fundraiser and says the directorship had been offered to Bryce S. DeWitt.",
      "source": "Talbert, New York Herald Tribune, 20 November 1955, continuation p. 36. https://archive.org/download/talbert1ny/talbert1ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Thomas Townsend Brown is named in none of the three articles, and neither Winterhaven nor any Navy or Air Force electrogravitics contract appears in them.",
      "source": "All three articles read in full: https://archive.org/download/talbert1ny/talbert1ny_djvu.txt, https://archive.org/download/talbert2ny/talbert2ny_djvu.txt, https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, episode 248, at 2:34:20 to 2:35:18, Jason Reza Jorjani dated the Herald Tribune reporting to 1953, attributed it to Martin's chief executive, and said the executive claimed Manhattan-Project-scale funding could put such engines into production in a few years. The articles are dated November 1955, the speaker is a vice-president for advanced design, and the comparison he draws is to the time the first atom bomb took rather than to its funding.",
      "source": "research/leads/dannyjones-corpus-12.md, batch 12, episode 248."
    }
  ],
  "sources": [
    "https://archive.org/download/talbert1ny/talbert1ny_djvu.txt",
    "https://archive.org/download/talbert2ny/talbert2ny_djvu.txt",
    "https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
  ],
  "edges": [
    { "to": "george-trimble", "type": "research", "note": "The series quotes Trimble by name as Martin's vice-president for advanced design planning and reports him organizing the Research Institute for Advanced Study." },
    { "to": "rias-inc", "type": "institutional", "note": "The series reports Martin building a new laboratory for the Research Institute for Advanced Study between Washington and Baltimore in November 1955." },
    { "to": "sperry-rand", "type": "research", "note": "The series names the Sperry Gyroscope Division of Sperry-Rand Corp. among the firms with scientists investigating the gravity problem, which is a documented attachment for a node the 30 August pass left deliberately unattached." },
    { "to": "general-dynamics", "type": "research", "note": "The series names Convair of San Diego and photographs a Convair division senior research engineer conducting a gravity-control experiment." },
    { "to": "institute-of-field-physics", "type": "institutional", "note": "The series reports the UNC trustees approving the institute in November 1955 under the name Institute of Pure Physics, names Bahnson as fundraiser and records the directorship offered to Bryce S. DeWitt." },
    { "to": "gordon-gray", "type": "institutional", "note": "The series records that the UNC gravity institute was approved with Gray's approval and that he had by then retired as president of the university." },
    { "to": "thomas-townsend-brown", "type": "denial", "note": "The contemporaneous press series that the electrogravitics claim rests on names Brown nowhere in its three parts." }
  ]
}
```

```json
{
  "id": "bell-aircraft-corporation",
  "cls": "institution",
  "label": "Bell Aircraft Corporation",
  "date": "1955-11-22",
  "desc": "Bell Aircraft Corporation of Buffalo, New York is one of the aircraft firms named in Ansel Talbert's November 1955 New York Herald Tribune series as participating or actively interested in gravity research, and its founder and president Lawrence D. Bell is quoted in the series directly. It reaches this board through the Danny Jones corpus, where a guest names it alongside Martin as a company making public electrogravitics claims in 1953. The opened press record puts the claims two years later and puts them in more careful language than the transcript does: Bell speaks of operating outside the earth's gravity as a third step after atmospheric flight, not of a working engine.",
  "claims": [
    {
      "tier": 1,
      "text": "The Herald Tribune series of November 1955 lists 'Bell Aircraft of Buffalo, builders of the first piloted airplane to fly faster than sound and a current jet vertical take-off and landing airplane' among the aircraft industry firms 'now participating or actively interested in gravity'.",
      "source": "Ansel E. Talbert, New York Herald Tribune, 20 November 1955, continuation p. 36. https://archive.org/download/talbert1ny/talbert1ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Lawrence D. Bell told Talbert: 'Aviation as we know it is on the threshold of amazing new concepts', and 'The Wright Brothers proved that man does not have to be earth-bound. Our next step will be to prove that we can operate outside the earth's atmosphere and the third will be to operate outside the gravity of the earth.'",
      "source": "Ansel E. Talbert, 'New Air Dream, Planes Flying Outside Gravity', New York Herald Tribune, 22 November 1955, p. 1. https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The same article reports that Bell's company had in the preceding days made the first powered flights with its new Bell X-2 rocket plane, and that it was testing a jet vertical-rising-and-landing aircraft. Its photograph caption names three Air Force test pilots with Bell: Lt. Col. Frank J. Everest, Maj. Charles Yeager and Maj. Arthur Murray.",
      "source": "Talbert, New York Herald Tribune, 22 November 1955, p. 1 and caption. https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, episode 248, at 2:35:18, Jason Reza Jorjani named Bell alongside Martin as a second company making the same public electrogravitics claims, and dated the claims to 1953. The opened articles are dated November 1955, and the words attributed to Bell in them do not use the term electrogravitics.",
      "source": "research/leads/dannyjones-corpus-12.md, batch 12, episode 248."
    }
  ],
  "sources": [
    "https://archive.org/download/talbert1ny/talbert1ny_djvu.txt",
    "https://archive.org/download/talbert3ny/talbert3ny_djvu.txt"
  ],
  "edges": [
    { "to": "usaf", "type": "institutional", "note": "The 22 November 1955 article photographs Lawrence D. Bell with three named Air Force test pilots during the Bell X-2 programme." },
    { "to": "thomas-townsend-brown", "type": "denial", "note": "Bell Aircraft reaches this board as an electrogravitics claim; the press series that carries the claim names Brown nowhere." }
  ]
}
```

**Two limits to keep.** Bell Aircraft's later corporate history and its 1960 sale to Textron
were NOT OPENED, and nothing above asserts them. And if the document node above is not built,
the Bell node's `sources` must still carry the two archive.org URLs, because they are what
its Tier 1 claims rest on.

---

## 5. Peter Bergmann, Joseph Weber and the January 1957 Chapel Hill conference

**VERDICT: CONFIRMED. Both men attended, with affiliations. And the record REFINES a Tier 1
claim the board already carries: WADC was one of four financial supporters, not the sponsor.**

### What was opened

| URL | What is at it |
|---|---|
| https://edition-open-sources.org/sources/5/5/index.html | The Foreword of the original Chapel Hill report by Cecile M. DeWitt, dated "Chapel Hill, North Carolina, March 15, 1957", reproduced with the report's own title page including the sponsorship block, the steering committee, the reporters and the Air Force imprint |
| https://edition-open-sources.org/sources/5/6/index.html | "Participants in the Conference", the report's own attendee list with institutional affiliations |
| https://edition-open-sources.org/sources/5/ | The volume's table of contents |

**What this edition is.** `The Role of Gravitation in Physics: Report from the 1957 Chapel
Hill Conference`, Max Planck Institute for the History of Science, Edition Open Sources,
Berlin, 2011, ISBN 978-3-945561-29-4, an open-access reissue of the original report. Its
"Original Chapel Hill Report" section reproduces the 1957 front matter verbatim, including
the title page. **The DTIC copy of WADC Technical Report 57-216 itself was NOT OPENED**, for
the DTIC wall recorded in section 2. What is opened here is a scholarly reissue that reprints
the original's front matter, and that is said plainly rather than presented as the DTIC file.

### What the document establishes

**Both men attended.** The participants list prints "Bergmann, P. G. | Syracuse University"
and "Weber, J. | University of Maryland". It also prints "Witten, L. | RIAS, Inc.,
Baltimore", which is the entry the board already carries on `louis-witten`.

**Bergmann's role was larger than attendance.** He sits on the six-member steering committee
alongside Belinfante, Bryce DeWitt, Cecile DeWitt, Freeman Dyson and John Wheeler, and he
wrote the closing "Summary of Conference". The Foreword's abstract says so: "A conference
summary statement is presented by Professor P. G. Bergmann."

**The sponsorship, in the report's own words.** The title page reads: "UNDER THE SPONSORSHIP
OF THE International Union of Pure and Applied Physics, with financial support from UNESCO /
National Science Foundation / Wright Air Development Center, U.S. Air Force / Office of
Ordnance Research, U.S. Army". Below the steering committee it prints: "MARCH 1957 / Wright
Air Development Center / Air Research and Development Command / United States Air Force /
Wright-Patterson Air Force Base, Ohio".

**Why the report exists at all.** The Foreword's second paragraph: "The present report was
undertaken as a necessary requirement to obtain conference funds."

**Four service affiliations in the room.** The participants list gives "Estabrook, F. B. |
Office of Ordnance Research" and "Mace, R. | Office of Ordnance Research", "Goldberg, J. N. |
Wright Air Development Center", and "Lilley, A. E. | Naval Research Laboratory, Washington".
Four of the forty-six participants were serving in US military research offices. The Goldberg
entry corroborates, from the conference's own paper, the board's existing Tier 1 claim on
`institute-of-field-physics` about the Air Force officer in charge of general-relativity
funding.

**Institutional context.** The title page states: "This conference was an activity of the
North Carolina Project of the Institute of Field Physics, established in 1956 in the
Department of Physics of the University of North Carolina, Chapel Hill."

### What the transcripts and the board claimed that this does NOT establish

| Claim | What the record says |
|---|---|
| The triage row's question, whether "Wright Field sponsored it", framed as Michels's specific claim | The record splits the two words. **IUPAP sponsored it.** WADC was one of four financial supporters, alongside UNESCO, the NSF and the Army's Office of Ordnance Research. WADC's imprint is on the report because the report was the funding requirement, not because the Air Force convened the meeting |
| The board's existing Tier 1 claim on `louis-witten`: the report "exists because of a conference funding agreement with the Wright Air Development Center" | Supported in substance and slightly too narrow. The Foreword says the report was "a necessary requirement to obtain conference funds", and the funders are four |
| The board's `institute-of-field-physics` node dates the institute's incorporation to 7 September 1955 | The conference title page says the Institute was "established in 1956 in the Department of Physics". These are two different acts, the North Carolina incorporation and the establishment inside the department, and a node should not collapse them |
| Anything about anti-gravity, electrogravitics or Townsend Brown | The front matter carries none of it. The board's existing Tier 1 finding, that the Institute attached an anti-gravity disclaimer to its publicity, is the relevant record and it is already on the board |

### Draft nodes

```json
{
  "id": "peter-bergmann",
  "cls": "person",
  "label": "Peter G. Bergmann",
  "date": "1957-01-18",
  "desc": "Peter G. Bergmann of Syracuse University sat on the six-member steering committee of the January 1957 Conference on the Role of Gravitation in Physics at Chapel Hill and delivered its closing summary. The conference report, issued as Wright Air Development Center Technical Report 57-216, prints him among its forty-six participants. He reaches this board because the board already carries the Chapel Hill conference through Louis Witten and the Institute of Field Physics, and because a guest in the Danny Jones corpus names him. Everything asserted here comes from the conference report's own front matter; nothing about his other work or affiliations has been opened.",
  "claims": [
    {
      "tier": 1,
      "text": "The conference report's participants list prints 'Bergmann, P. G. | Syracuse University'.",
      "source": "Participants in the Conference, The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, the Edition Open Sources reissue of WADC Technical Report 57-216, Max Planck Institute for the History of Science, 2011. https://edition-open-sources.org/sources/5/6/index.html"
    },
    {
      "tier": 1,
      "text": "Bergmann sat on the conference steering committee with F. J. Belinfante, Bryce S. DeWitt, Cecile M. DeWitt, Freeman J. Dyson and John A. Wheeler, and the Foreword's abstract records that 'A conference summary statement is presented by Professor P. G. Bergmann.'",
      "source": "Foreword by Cecile M. DeWitt, Chapel Hill, 15 March 1957, printed with the report's title page. https://edition-open-sources.org/sources/5/5/index.html"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, batch 16 file 04 at 2:38:20, Bergmann is named in connection with the Chapel Hill conference. The conference report confirms his attendance and his steering-committee role and carries nothing else the transcript attributes to him.",
      "source": "research/leads/dannyjones-corpus-16.md, batch 16, file 04."
    }
  ],
  "sources": [
    "https://edition-open-sources.org/sources/5/5/index.html",
    "https://edition-open-sources.org/sources/5/6/index.html"
  ],
  "edges": [
    { "to": "institute-of-field-physics", "type": "research", "note": "The conference was, in the report's own words, an activity of the North Carolina Project of the Institute of Field Physics, and Bergmann sat on its steering committee." },
    { "to": "louis-witten", "type": "research", "note": "Both are printed on the same forty-six-name participants list of the January 1957 Chapel Hill conference." }
  ]
}
```

```json
{
  "id": "joseph-weber",
  "cls": "person",
  "label": "Joseph Weber",
  "date": "1957-01-18",
  "desc": "Joseph Weber of the University of Maryland is printed among the forty-six participants of the January 1957 Conference on the Role of Gravitation in Physics at Chapel Hill, whose report was issued as Wright Air Development Center Technical Report 57-216. He reaches this board as the second name on that document, named independently by a different guest in a different batch of the Danny Jones corpus. Nothing beyond his attendance and his affiliation as of January 1957 has been opened, and his later gravitational-radiation detector work is not asserted here.",
  "claims": [
    {
      "tier": 1,
      "text": "The conference report's participants list prints 'Weber, J. | University of Maryland'.",
      "source": "Participants in the Conference, The Role of Gravitation in Physics: Report from the 1957 Chapel Hill Conference, the Edition Open Sources reissue of WADC Technical Report 57-216, 2011. https://edition-open-sources.org/sources/5/6/index.html"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, batch 19 file 04 at 1:02:34, Weber is named by a guest in connection with gravitational research. The conference report confirms his presence at Chapel Hill in January 1957 and carries nothing else the transcript attributes to him.",
      "source": "research/leads/dannyjones-corpus-19.md, batch 19, file 04."
    }
  ],
  "sources": [
    "https://edition-open-sources.org/sources/5/6/index.html"
  ],
  "edges": [
    { "to": "institute-of-field-physics", "type": "research", "note": "He attended the Institute of Field Physics' inaugural conference at Chapel Hill in January 1957." },
    { "to": "louis-witten", "type": "research", "note": "Both are printed on the same forty-six-name participants list." }
  ]
}
```

**Optional third node, and the one that would earn its place.** The board cites WADC
Technical Report 57-216 inside `louis-witten`'s claims and has no node for the document. If
one is built, its `desc` must carry the sponsorship split above, because that is the fact the
whole Chapel Hill row turns on: IUPAP sponsored, four bodies paid, and the Air Force's name
is on the cover because the report was the condition of the money.

---

## 6. Norton AFB and the claimed loss of the CIA's Area 51 records

**VERDICT: CONTRADICTED on the identification of "Norton", and unsupported on everything
else. The record was opened in quantity and does not carry the claim, and cannot: its span
ends in 1974.**

### What was opened

| URL | What is at it |
|---|---|
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/ | The National Security Archive's posting of the 25 June 2013 CIA release, with the study broken into chapter PDFs |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Cover-Contents-Foreword-Preface.pdf | Cover, contents, Foreword by J. Kenneth McDonald (1992) and Preface. 13 pages, read in full |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf | Chapter 2, "Developing the U-2", 54 pages, the Groom Lake and Area 51 chapter. Searched in full |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%206.pdf | Chapter 6, 57 pages. Searched in full |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%207.pdf | "Conclusion", 10 pages, read in full |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Index.pdf | The study's index, 39 pages, searched in full |
| https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Appendices-Bibliography.pdf | Appendices, biographic appendix and bibliography, 30 pages, searched in full |

**What the document is.** `The Central Intelligence Agency and Overhead Reconnaissance: The
U-2 and OXCART Programs, 1954-1974`, Gregory W. Pedlow and Donald E. Welzenbach, History
Staff, Central Intelligence Agency, Washington DC, 1992. Every page is stamped "Approved for
Release: 2013/06/25". The National Security Archive's copy carries the release banner
"FREEDOM OF INFORMATION RELEASE TO THE NATIONAL SECURITY ARCHIVE".

### What the document establishes, and what it forecloses

**"Norton" in this document is a man.** The index entry reads "Norton, Garrison | 14-15, 31,
70, 260, 331". There is no index entry for Norton Air Force Base. The biographic appendix
identifies him as an aide to Trevor Gardner who "became an supporter of the Lockheed CL-282
and started the CIA's interest in overhead re-", the sentence broken by the release's own
redaction. Chapter 6 places him as the Navy's Assistant Secretary for Research and Development
opposite the Air Force's Joseph V. Charyk. Chapter 2 puts him among the outsiders present at
the U-2's official first flight on 8 August 1955. The bibliography lists "Interview with
Garrison Norton by Donald E. Welzenbach, Washington, DC, 23 May 1983 (Secret)". Every
occurrence of the string "Norton" across the six PDFs searched is this man.

**The study cannot reach 1979.** The Preface: "The Agency's manned overhead reconnaissance
program lasted 20 years. It began with President Eisenhower's authorization of the U-2 project
in late 1954 and ended with the transfer of the remaining Agency U-2s to the Air Force in
1974." The Conclusion ends there. Nothing in the opened chapters mentions 1979, a handover of
the site, or the disposition of records after the programme.

**What it does say about records, which is not what the transcript says.** The Foreword states
that the study "is the only history of this program based upon both full access to CIA records
and extensive classified interviews of its participants" and that "The authors have found
records that were nearly irretrievably lost and have interviewed participants whose personal
recollections gave information available nowhere else." The Preface says "Agency documentation
on the prehistory of the U-2 project is very sketchy and there are no accurate published
accounts", names the record sets used ("the records of the Director of Central Intelligence,
the Office of Special Activities in the Directorate of Science and Technology, and the
Intelligence Community Staff", plus the Eisenhower Presidential Library), and thanks "Agency
records management officers in the search for documents".

### What the transcript claimed that this document does NOT establish

| TD Barnes, 09 / 415 / 0:07:39 to 0:08:29 | What the record says |
|---|---|
| The CIA's Area 51 records went to Norton Air Force Base after the 1979 handover | The CIA's published history of the site's programmes contains no Norton Air Force Base, and its span stops in 1974. The claim is neither supported nor addressed |
| The records were lost there | The document's only records-loss statements are its Foreword's, about records the authors themselves recovered, and its Preface's, that pre-1954 documentation is "very sketchy" |
| The Agency had to rebuild its own history from a crowdsourced website Barnes helped create | The study was completed in 1992, before the public web, from CIA record sets and classified interviews the Preface names. It could not have been built that way, and it says how it was built |

**Recommendation: build no Norton Air Force Base node from this row.** The record the triage
row nominated as the thing that would settle it has been opened and it settles it in the
negative. What the pass does produce is a candidate document node the board does not carry,
and it is worth naming because the board already leans on the CIA's other self-history:

```json
{
  "id": "cia-overhead-reconnaissance-history-1992",
  "cls": "document",
  "label": "The Central Intelligence Agency and Overhead Reconnaissance: The U-2 and OXCART Programs, 1954-1974",
  "date": "1992",
  "desc": "The CIA History Staff's own study of the Agency's manned overhead reconnaissance programmes, written by Gregory W. Pedlow and Donald E. Welzenbach and published internally in 1992 at the Secret level, released on 25 June 2013 in response to a Freedom of Information request from the National Security Archive. The 2013 release is the version that left the Area 51 references intact. It reaches this board as the record against which a claim in the Danny Jones corpus was tested and failed: it contains no Norton Air Force Base, and its own stated span ends with the 1974 transfer of the remaining Agency U-2s to the Air Force, five years before the events the transcript describes.",
  "claims": [
    {
      "tier": 1,
      "text": "The study states its own span: 'The Agency's manned overhead reconnaissance program lasted 20 years. It began with President Eisenhower's authorization of the U-2 project in late 1954 and ended with the transfer of the remaining Agency U-2s to the Air Force in 1974.'",
      "source": "Pedlow and Welzenbach, The Central Intelligence Agency and Overhead Reconnaissance, CIA History Staff, 1992, Preface. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Cover-Contents-Foreword-Preface.pdf"
    },
    {
      "tier": 1,
      "text": "Its Foreword records a records-recovery claim of the Agency's own: the study 'is the only history of this program based upon both full access to CIA records and extensive classified interviews of its participants', and 'The authors have found records that were nearly irretrievably lost'.",
      "source": "Foreword by J. Kenneth McDonald, CIA History Staff, 1992. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Cover-Contents-Foreword-Preface.pdf"
    },
    {
      "tier": 1,
      "text": "The study's index carries the entry 'Norton, Garrison | 14-15, 31, 70, 260, 331' and no entry for Norton Air Force Base. Every occurrence of the string Norton across the front matter, chapters 2, 6 and 7, the index and the appendices is Garrison Norton, the Navy Assistant Secretary for Research and Development, whom the bibliography records being interviewed by Welzenbach on 23 May 1983.",
      "source": "Index p. 20, Appendices and Bibliography pp. 7 and 29, Chapter 6 p. 2, Chapter 2 p. 32. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Index.pdf"
    },
    {
      "tier": 1,
      "text": "The Preface names the record sets the authors used: 'the records of the Director of Central Intelligence, the Office of Special Activities in the Directorate of Science and Technology, and the Intelligence Community Staff, along with documents from the Eisenhower Presidential Library in Abilene, Kansas, and additional interviews.'",
      "source": "Preface. https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Cover-Contents-Foreword-Preface.pdf"
    },
    {
      "tier": 2,
      "text": "On the Danny Jones Podcast, episode 415, at 0:07:39 to 0:08:29, TD Barnes said the CIA's Area 51 records went to Norton Air Force Base after the 1979 handover, were lost there, and that the Agency had to rebuild its own history from a crowdsourced website he helped create. The Agency's published history of those programmes contains no Norton Air Force Base, was completed in 1992, and states that it was built from CIA record sets and classified interviews.",
      "source": "research/leads/dannyjones-corpus-09.md, batch 09, episode 415."
    }
  ],
  "sources": [
    "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/",
    "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Cover-Contents-Foreword-Preface.pdf",
    "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Index.pdf",
    "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%202.pdf",
    "https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/docs/U2%20-%20Chapter%207.pdf"
  ],
  "edges": [
    { "to": "cia", "type": "institutional", "note": "Written by the CIA History Staff in 1992 and released by the Agency on 25 June 2013." },
    { "to": "l-area51", "type": "custody", "note": "It is the Agency's own account of the establishment and use of the Groom Lake site, and the 2013 release is the version in which the Area 51 references were left intact." },
    { "to": "haines-cia-history", "type": "investigative", "note": "The board's Haines UFO history of 1997 cites CIA officials who worked on the U-2 and OXCART projects; this is the Agency's own history of those projects, by the same History Staff." }
  ]
}
```

---

## What a next pass should carry forward

1. **DTIC is a wall from Stewart's Windows machine, and so is every af.mil host.** Two
   independent egress paths were tried, curl with a browser user agent and WebFetch, against
   three DTIC PDF paths and four af.mil hosts. All 403. The DTIC citation endpoint answers
   200 with a maintenance page. Any brief that assigns a DTIC candidate to a verifier on this
   machine should expect NOT OPENED unless the report is also on the archive.org DTIC mirror,
   on NTRS, on govinfo or on OSTI. **govinfo and NTRS both answer, and both carried a better
   record than DTIC would have** for candidates 1 and 3.
2. **Two of the six rows turned on a date the speaker got wrong**, and in both cases the
   record moved the date later: 1953 to November 1955 for the Herald Tribune series, and 1954
   to 1961 or later for nitinol. That is a pattern worth watching in this corpus.
3. **Three exclusions are decisions, not gaps.** No Exon edge to `foreign-technology-division`
   or `nathan-twining`, because the base history connects him to neither. No Bell Aircraft
   edge to `george-trimble` or `rias-inc`, because the articles put those two on the Martin
   side and nothing links them to Bell. And no Norton Air Force Base node at all.
