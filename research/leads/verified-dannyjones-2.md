# Verified leads: Danny Jones corpus, the undersea and custody cluster (verifier 2)

**Status: research output, not board content.** Nothing here has been merged into `research/`,
into `data/*.json` or into any node. This is a verification pass over rows 1, 2, 3, 4, 9 and 10
of section A of `research/leads/dannyjones-triage-4.md` and rows 2 and 18 of section A of
`research/leads/dannyjones-triage-5.md`, run against
`research/leads/VERIFY-BRIEF-DANNYJONES-2026-09-03.md` and, through it, against
`research/leads/VERIFY-BRIEF-2026-09-02.md` and the format of
`research/leads/verified-area52-1.md`.

**Verified 3 September 2026.** Every URL below was opened by this session and returned the
document described. Where the route was an archive's mirror rather than the issuing agency's
own page, the row says so. `CLAUDE.md` section 2 governs: nothing here is asserted that was not
opened. A wall is recorded as a wall.

**Board ids, read out of `data/the-program.json` by this session. Two of the four ids the
instructions named do not exist.** There is no `adm-bobby-ray-inman`; the node is
**`bobby-ray-inman`**. There is no `office-of-naval-intelligence`; the node is **`oni`**.
`deep-submergence-systems-project` and `d-foia` do exist. Also confirmed present and used
below: `cia`, `nsa`, `us-navy`, `dod`, `doe`, `nro`, `lockheed-martin`, `saic`,
`office-of-naval-research`, `d-custody`, `d-denial`, `wilson-davis-memo`, `sean-kirkpatrick`.
Confirmed absent, so each is a new id rather than an edge target: `glomar-explorer`,
`project-azorian`, `uss-halibut`, `ronald-pelton`, `wackenhut`, `shapiro`, `prepublication`.

## Summary

| # | Lead | Verdict | Note |
|---|---|---|---|
| 1 | National Underwater Reconnaissance Office | **NOT OPENED** | No federal record naming it reached. nro.gov and nsa.gov both refuse this caller with 403; govinfo returns nothing; every hit is an encyclopedia or a 1998 trade book |
| 2 | Ivy Bells, through the Pelton prosecution | **PARTLY CONFIRMED**, and the codename NOT OPENED | The Solicitor General's brief gives the counts, the district and the sentence, and says only "several classified NSA operations". No opened record names Ivy Bells, a cable or a submarine |
| 3 | Glomar Explorer, Project AZORIAN | **CONFIRMED**, and two parts of the transcript's coda CONTRADICTED | The full 50-page Studies in Intelligence history opened. It names Lockheed, not Lockheed Martin, and in a four-company consortium, not a lease |
| 4 | USS Halibut | **PARTLY CONFIRMED**, and the triage row's award citations NOT OPENED | The DANFS entry stops in 1967, carries no awards list at all, and contains no special operation, no cable and no Soviet submarine |
| 9 | Sumner Shapiro as Director of Naval Intelligence | **NOT OPENED** | No Navy register, NHHC page or FRUS entry reached. history.state.gov returns "No results were found" for his name |
| 10 | The Wackenhut Corporation and Inman | **CONTRADICTED** for the filings that exist; NOT OPENED before 1997 | Inman appears in none of the three Wackenhut proxies opened. EDGAR's earliest Wackenhut proxy is 1997 |
| T5-2/18 | Bustamante, Zaid, the prepublication mechanism | **PARTLY CONFIRMED** for the mechanism; the book's own PRB history and the Malmstrom claim NOT OPENED | The CIA's own released PRB procedures and a filed court declaration by Zaid both opened. Nothing reaches the shutdown claim |

**The five findings that matter, in order:**

1. **The DANFS entry for Halibut ends in 1967 and contains no awards, no special operations and
   no Soviet submarine.** The triage row proposed the node on "the ship's Dictionary of American
   Naval Fighting Ships entry and its unit award citations for 1968 and 1972". The entry, opened
   in full, was published to the web on 14 July 2015 but is a pre-1968 text: its last narrative
   sentence covers 1966 and "to date in 1967". It has no awards section. The 1968 and 1972
   Presidential Unit Citations exist only in secondary sources. **A named platform with a hull
   number is exactly what the triage row wanted and the official entry does not supply it.**
2. **The CIA's own AZORIAN history never uses the name K-129, and never uses the word NURO.**
   It calls the target "a Soviet submarine of the G-II class" and, once located, "the G-722
   target object". The whole undersea thread's organising acronym is absent from the one
   deep-ocean recovery document the United States has released about itself.
3. **The Lockheed coda is right in outline and wrong in every particular.** The article's closing
   page says a private consortium including Lockheed, Global Marine, Standard Oil of Indiana and
   Royal Dutch Shell were readying the ship for deep-ocean mining from late 1978. Not Lockheed
   Martin, which did not exist until 1995; not a lease; not twenty years; and a consortium, not
   one company.
4. **Inman is in none of the Wackenhut proxy statements that exist.** Three were opened: the 1998
   proxy for the 24 April 1998 meeting, the 1999 proxy for the 7 May 1999 meeting, and the 2002
   merger proxy. All twelve 1999 nominees are named below and none is Inman. The instrument the
   triage row nominated therefore answers no for 1997 to 2002 and cannot answer at all for the
   years before, because Wackenhut's earliest EDGAR filing is 24 March 1994 and its earliest
   proxy is a preliminary 14A of 24 March 1997.
5. **The prepublication mechanism is documented by the CIA in its own released procedures, and it
   is not the mechanism the transcript describes.** The released "Prepublication Review
   Information" sets 30 working days, requires written approval before publication, and routes
   an appeal to the Associate Deputy Director within 30 days of a reconsideration decision.
   Nothing in it provides for a manuscript being "declared classified" and then approved after
   litigation is threatened. That sequence is the author's account, and the record that would
   test it is PRB correspondence obtainable only on FOIA.

---

## 1. National Underwater Reconnaissance Office (NURO)

**VERDICT: NOT OPENED.** This is the second corpus pass to return this verdict, and the routes
tried this time were different from the Area 52 pass's.

### What was tried

| Route | Result |
|---|---|
| `https://www.nro.gov/history-and-studies/Center-for-the-Study-of-National-Reconnaissance/` | HTTP 403 to curl with a browser user agent. The Area 52 pass recorded nro.gov refusing as well |
| `https://www.nsa.gov/Helpful-Links/NSA-FOIA/Declassification-Transparency-Initiatives/` | HTTP 403 |
| `https://irp.fas.org/program/collect/nuro.htm` | HTTP 404. FAS has no NURO page at the path its sibling collection pages use |
| govinfo search API, `"National Underwater Reconnaissance Office"` as a phrase | `{"count":0,"offsetMark":null,"results":[]}`. Two phrase variants returned the API's own error, and an unquoted keyword search returned 34 results whose top hit is FRUS 1951 volume I, that is, noise |
| `https://www.archives.gov/declassification/iscap/appeals-decisions.html` | HTTP 404 |
| The CIA reading-room mirror at `archive.org/download/cia-readingroom-document-0005301269/`, the AZORIAN history, searched for the string | Opened in full. **Neither "NURO" nor "National Underwater Reconnaissance" occurs anywhere in the 50 pages.** The only instance of the words in sequence is the phrase "the extremely dangerous task of underwater reconnaissance", which is not the office |
| The Pelton prosecution record, as the triage row directed | Opened, see row 2. It does not name the office either |

Every reachable description of NURO is an encyclopedia entry, a wiki or a trade press piece
tracing to Sontag and Drew's 1998 book. **A book is not a record on this board and a search
snippet is not an opened document.** The founding instrument the triage row wants, a 1969 Navy
and CIA agreement, was not reached and no session should assert its year, its signatories or
Warner's or Inman's directorships from anything opened here.

**What would settle it, for the FOIA queue:** the NRO's Center for the Study of National
Reconnaissance holds the declassified NRO histories; a mandatory declassification review request
to the NRO and a FOIA to the Chief of Naval Operations for the establishing agreement are the two
instruments. The board's existing gap discipline applies: record it as a gap, not as a claim.

---

## 2. Ivy Bells, through the Pelton prosecution

**VERDICT: PARTLY CONFIRMED for the prosecution. The codename Ivy Bells is NOT OPENED, and so is
every operational detail the transcript attaches to it.**

### What was opened

| URL | What is at it |
|---|---|
| https://www.justice.gov/osg/media/218076/dl | "Ronald W. Pelton, Petitioner v. United States of America, No. 87-6433", the brief for the United States in opposition, filed in the Supreme Court by the Office of the Solicitor General |

Two other routes to the underlying appellate opinion were refused and are recorded as walls:
`law.justia.com` returned HTTP 403 and `openjurist.org` returned HTTP 403 for
`United States v. Pelton`, 835 F.2d 1067 (4th Cir. 1987). The Fourth Circuit's own PDF server
answered for a different case in this file but its text did not extract.

### What the document establishes

Pelton was convicted in the United States District Court for the District of Maryland on
conspiracy to commit espionage, espionage and attempted espionage, and unauthorized disclosure of
classified information. He received, in the brief's words, "concurrent life terms on the espionage
and conspiracy counts, and a concurrent ten-year term on the unauthorized-disclosure count". On
what he gave the Soviets the brief says only that he "furnished the Soviets information about
several classified NSA operations" and refers elsewhere to "details of a classified project that
he had revealed to the Soviets".

### What the transcript claimed that this document does NOT establish

| Claim | Cite | Status against the opened record |
|---|---|---|
| Ivy Bells is the named NURO undersea cable tapping programme | 20 e320 0:28:33 (Gerb) | The name appears nowhere in the brief. Nor does NURO |
| The tap was placed on a cable in the Sea of Okhotsk by USS Halibut around 1970 to 1971 | 18 f04 2:37:23 (Dolan) | Nothing in the brief names a cable, a sea, a submarine or a date of operation |
| The prosecution record is what makes NURO "documentable rather than testimonial" (triage row 2's own argument) | triage-4 A2 | **The argument does not survive the record.** The one federal filing reached in this matter is written to avoid saying what the operations were, which is the ordinary posture of an espionage prosecution and is why it cannot carry the operational claim |

### Draft node

```json
{
  "id": "us-v-pelton-1986",
  "cls": "event",
  "label": "United States v. Ronald W. Pelton (D. Md. 1986)",
  "date": "1986",
  "desc": "The federal espionage prosecution of a former National Security Agency employee in the United States District Court for the District of Maryland. The Solicitor General's brief in opposition to certiorari states the counts of conviction and the sentence and describes the compromise only as information about several classified NSA operations. It names no programme, no codename, no platform and no collection site. It is recorded here because two Danny Jones guests cite this prosecution as the public record of an undersea cable tapping operation, and the federal filing that was opened does not carry that content.",
  "claims": [
    {
      "text": "Pelton was convicted of conspiracy to commit espionage, espionage and attempted espionage, and unauthorized disclosure of classified information, in the United States District Court for the District of Maryland.",
      "tier": 1,
      "source": {"title": "Brief for the United States in opposition, Ronald W. Pelton v. United States, No. 87-6433, Office of the Solicitor General", "url": "https://www.justice.gov/osg/media/218076/dl"}
    },
    {
      "text": "The government's brief describes the sentence as concurrent life terms on the espionage and conspiracy counts and a concurrent ten-year term on the unauthorized-disclosure count.",
      "tier": 1,
      "source": {"title": "Brief for the United States in opposition, No. 87-6433", "url": "https://www.justice.gov/osg/media/218076/dl"}
    },
    {
      "text": "On what was compromised the brief says only that Pelton furnished the Soviets information about several classified NSA operations; it does not name any operation, codename, cable, sea area or submarine.",
      "tier": 1,
      "source": {"title": "Brief for the United States in opposition, No. 87-6433", "url": "https://www.justice.gov/osg/media/218076/dl"}
    },
    {
      "text": "On the Danny Jones show, 4 August 2025, at 0:28:33, the guest identified in the lead map as UAP Gerb named Ivy Bells as an undersea cable tapping programme run under a National Underwater Reconnaissance Office; no record opened by this pass names either.",
      "tier": 2,
      "source": {"title": "Danny Jones corpus lead map, dannyjones-corpus-20.md, episode 320", "url": "research/leads/dannyjones-corpus-20.md"}
    }
  ],
  "edges": [
    {"to": "nsa", "type": "institutional", "note": "Pelton was a former NSA employee and the government's brief describes the compromise as concerning NSA operations."},
    {"to": "d-denial", "type": "denial", "note": "The filing states the fact of a compromise while declining to describe any operation, which is the posture the board tracks."}
  ]
}
```

---

## 3. Glomar Explorer and Project AZORIAN

**VERDICT: CONFIRMED. The CIA's own history opened in full. Two parts of the transcript's coda are
CONTRADICTED and one date in the secondary description of the release is unreconciled.**

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt | The full text of CIA reading-room document 0005301269, "PROJECT AZORIAN: THE STORY OF THE HUGHES GLOMAR EXPLORER", 50 pages, carrying the stamp "APPROVED FOR RELEASE DATE: 01-04-2010" and the classification "SECRET" with a NOFORN control marking. This is the archive.org mirror the brief names; `cia.gov/readingroom` looped to its own front page for this session, as the brief warned |
| https://nsarchive2.gwu.edu/nukevault/ebb305/index.htm | National Security Archive Electronic Briefing Book 305, posted 12 February 2010, which records the FOIA request date of 12 December 2007 and describes the document as from Studies in Intelligence, Fall 1985 |
| https://www.cia.gov/resources/csi/static/The-Glomar-Explorer.pdf | A second, separate Studies in Intelligence article, "The Glomar Explorer in Film and Print" by David Robarge, opened as text |

### What the documents establish

**The preamble, which is the part that matters to this board.** The released article opens with a
publication note stating that several facts had been acknowledged in court "in the course of
continuing litigation related to the project", and it names the categories: "California State tax
liability, Freedom of Information Act matters, and a patent infringement claim". The acknowledged
facts it lists are CIA sponsorship of the project for intelligence collection purposes, the
participation of Hughes Tool Company, the Summa Corporation and Global Marine, Inc., and the
actions of senior CIA officials in 1975 to attempt to persuade members of the media not to
publish. It then states that the prohibition on saying more "applies particularly to the specific
purpose of the AZORIAN mission; the degree of success; operational details; participation of other
contractors, government organizations, and individuals; classified technology; and project funding
matters." **The board carries the Glomar response in `d-foia` prose; here is the FOIA litigation
named inside the operation's own history.**

**The target and the recovery.** "In March 1968 a Soviet submarine of the G-II class was lost with
all hands, 16,500 feet below the surface of the Pacific Ocean." The article gives the boat as the
G-II class ballistic missile submarine pendant 722, sailing from Petropavlovsk on about 1 March
1968. Its second sentence: "On 8 August 1974, that submarine was brought to the surface in a
recovery system designed and developed specifically for that mission."

**The cover.** "As mentioned previously, a deep-sea mining venture was to be used as the cover
story for this operation." A mining machine was to be built for cover purposes, a press release
announced that Global Marine would build a 600-foot mining ship, and when challenged at sea the
ship's answer was that it was conducting deep-ocean mining tests.

**The closing page, which is the checkable coda.** As the article is published, it says, "a
private consortium of companies, including Lockheed, Global Marine, Standard Oil of Indiana, and
Royal Dutch Shell, are readying the Hughes Glomar Explorer for use in deep-ocean mining operations
to begin late in the fall of 1978."

### What the transcript claimed that this document does NOT establish

| Claim | Cite | Status |
|---|---|---|
| The ship "was later leased to Lockheed Martin for deep-sea mining" for twenty years | 20 e320 0:29:24 (Gerb) | **CONTRADICTED in three particulars.** The article names Lockheed, one member of a four-company private consortium, readying the ship; it says nothing about a lease or a term. Lockheed Martin did not exist under that name until 1995 |
| Only a third, possibly more, of the submarine was recovered | 20 e320 0:29:24 (Gerb) | **Not established either way, and the article says why.** Its own second sentence says the submarine was brought to the surface; its preamble lists "the degree of success" among the matters still protected. A node must not resolve this from the released text |
| Glomar and NURO belong to one undersea programme | 20 e320 0:26:45 to 0:29:24 | **Not established.** NURO appears nowhere in 50 pages |

**A date discrepancy a next session must not silently average.** The National Security Archive
describes the article as Studies in Intelligence, Fall 1985. The reading-room record carries a
publication date of 1 March 1978. The article's own closing page places its publication before
late autumn 1978. Record all three, as the board's rule on the Roth grant figures requires.

### Draft node

```json
{
  "id": "project-azorian",
  "cls": "program",
  "label": "Project AZORIAN and the Hughes Glomar Explorer",
  "dateStart": "1968",
  "dateEnd": "1978",
  "desc": "The CIA programme that built a purpose-designed heavy-lift ship under a deep-ocean mining cover and used it in August 1974 to raise part of a Soviet ballistic missile submarine lost in the Pacific in March 1968. Its own 50-page internal history was released under FOIA and stamped for release on 4 January 2010. The history is on this board for the mechanism rather than the salvage: covert recovery of foreign hardware from the deep ocean under commercial cover, with a named corporate front, and with Freedom of Information Act litigation named inside the operation's own account of what it had been forced to concede.",
  "claims": [
    {
      "text": "The released history opens: In March 1968 a Soviet submarine of the G-II class was lost with all hands, 16,500 feet below the surface of the Pacific Ocean.",
      "tier": 1,
      "source": {"title": "PROJECT AZORIAN: THE STORY OF THE HUGHES GLOMAR EXPLORER, CIA reading-room document 0005301269, approved for release 01-04-2010", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    },
    {
      "text": "The same page states: On 8 August 1974, that submarine was brought to the surface in a recovery system designed and developed specifically for that mission.",
      "tier": 1,
      "source": {"title": "CIA reading-room document 0005301269", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    },
    {
      "text": "The article's publication note records that facts about the project had been acknowledged in court in continuing litigation concerning California State tax liability, Freedom of Information Act matters, and a patent infringement claim, and that the acknowledged facts include CIA sponsorship for intelligence collection purposes and the participation of Hughes Tool Company, the Summa Corporation and Global Marine, Inc.",
      "tier": 1,
      "source": {"title": "CIA reading-room document 0005301269", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    },
    {
      "text": "The same note states that the continuing prohibition applies particularly to the specific purpose of the AZORIAN mission, the degree of success, operational details, participation of other contractors, government organizations, and individuals, classified technology, and project funding matters.",
      "tier": 1,
      "source": {"title": "CIA reading-room document 0005301269", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    },
    {
      "text": "The article's closing page states that a private consortium of companies, including Lockheed, Global Marine, Standard Oil of Indiana, and Royal Dutch Shell, are readying the Hughes Glomar Explorer for use in deep-ocean mining operations to begin late in the fall of 1978.",
      "tier": 1,
      "source": {"title": "CIA reading-room document 0005301269", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    },
    {
      "text": "The strings NURO and National Underwater Reconnaissance do not occur anywhere in the 50-page released history.",
      "tier": 1,
      "source": {"title": "CIA reading-room document 0005301269, full text searched by this session", "url": "https://archive.org/download/cia-readingroom-document-0005301269/0005301269_djvu.txt"}
    }
  ],
  "edges": [
    {"to": "cia", "type": "programmatic", "note": "The released history is the Agency's own account and states CIA sponsorship of the project for intelligence collection purposes."},
    {"to": "d-foia", "type": "investigative", "note": "The history names Freedom of Information Act matters among the litigation that forced the first official acknowledgements, which is the doctrine the board already carries in d-foia prose."},
    {"to": "d-custody", "type": "custody", "note": "Covert recovery of foreign hardware from the deep ocean under a commercial cover, with a named corporate front, is the custody mechanism this board tracks."},
    {"to": "lockheed-martin", "type": "funding", "note": "The article's closing page names Lockheed, a predecessor of the board's Lockheed Martin node, as one of four companies in a private consortium readying the ship for deep-ocean mining from late 1978. The transcript's lease to Lockheed Martin is not what the record says and the node desc must carry that correction."},
    {"to": "deep-submergence-systems-project", "type": "temporal", "note": "Contemporary with the board's DSSP node and named alongside it by the same speaker; the connection is chronological and thematic, and no opened document links the two programmes."}
  ]
}
```

---

## 4. USS Halibut

**VERDICT: PARTLY CONFIRMED. The vessel and its dates are established from the official entry. The
unit award citations the triage row was built on are NOT OPENED, and the entry contains nothing
about special operations.**

### What was opened

| URL | What is at it |
|---|---|
| https://www.history.navy.mil/research/histories/ship-histories/danfs/h/halibut-ii.html | Naval History and Heritage Command, Dictionary of American Naval Fighting Ships, "Halibut II (SSG(N)-587)", published to the web Tue Jul 14 11:40:03 EDT 2015. **WebFetch returned HTTP 404 for this URL twice; curl with a browser user agent returned HTTP 200 and 105,373 bytes.** The wall was the fetcher, not the site |

### What the document establishes

Halibut (SSG(N)-587) was launched at Mare Island Naval Shipyard, Vallejo, California on 9 January
1959, sponsored by Mrs. Chet Holifield, and commissioned 4 January 1960 with Lt. Comdr. Walter
Dedrick in command. The entry states she "had the distinction to be the first submarine in the
world designed and built from the keel up to launch guided missiles", intended for the Regulus I,
and that on 25 March 1960 en route to Australia "she became the first nuclear powered submarine to
successfully launch a guided missile." On 4 May 1964 she departed Pearl Harbor for the last Regulus
missile patrol made by a submarine in the Pacific. In February 1965 she entered Pearl Harbor Naval
Shipyard for a major overhaul and on 15 August 1965 "she was redesignated SS(N)-587". The
characteristics line gives speed and complement as "classified".

### What the transcript and the triage row claimed that this document does NOT establish

| Claim | Cite | Status |
|---|---|---|
| Halibut placed a tap on a Soviet undersea communications cable off Kamchatka around 1970 to 1971 | 18 f04 2:37:23 (Dolan) | **Absent.** The narrative ends "to date in 1967". There is no cable, no Sea of Okhotsk, no special operation and no Soviet submarine anywhere in the entry |
| Halibut was NURO's operational platform | 18 f04 2:37:23; triage-4 A4 | **Absent.** NURO does not appear |
| The entry carries "unit award citations for 1968 and 1972" | triage-4 A4, the row's own stated record | **CONTRADICTED as to the record named.** The entry has no awards section of any kind. The two Presidential Unit Citations are asserted only by encyclopedia and enthusiast sites, which are not records on this board |
| The hull is SSN-587 | 18 f04, 20 e320 | **Partly.** DANFS gives the designation as SSG(N)-587 and the 1965 redesignation as SS(N)-587. Copy the entry's own forms, not the podcast's |

**Why this matters more than it looks.** The triage row's argument was that "a named platform is
what turns the NURO claim from an org chart into something with a hull number". The hull number is
real and the official entry is real, and the official entry is silent on everything the claim needs.
Building the node is still worth doing, because the silence is the finding.

### Draft node

```json
{
  "id": "uss-halibut",
  "cls": "institution",
  "label": "USS Halibut (SSG(N)-587, later SS(N)-587)",
  "dateStart": "1959",
  "dateEnd": "1976",
  "desc": "A nuclear powered submarine launched at Mare Island in January 1959 and commissioned in January 1960, the first submarine designed and built from the keel up to launch guided missiles and the first nuclear powered submarine to launch one at sea. Redesignated SS(N)-587 in August 1965 after a major overhaul. Two Danny Jones guests name her as the platform of a Soviet cable tapping operation run under a National Underwater Reconnaissance Office. The Navy's own Dictionary of American Naval Fighting Ships entry, opened in full, records no such operation, no unit awards and no activity after 1967, and that silence is why the node exists.",
  "claims": [
    {
      "text": "The Navy's own entry records that Halibut was launched by Mare Island Naval Shipyard on 9 January 1959 and commissioned 4 January 1960, Lt. Comdr. Walter Dedrick in command.",
      "tier": 1,
      "source": {"title": "Naval History and Heritage Command, DANFS, Halibut II (SSG(N)-587)", "url": "https://www.history.navy.mil/research/histories/ship-histories/danfs/h/halibut-ii.html"}
    },
    {
      "text": "The entry states that in February 1965 Halibut entered Pearl Harbor Naval Shipyard for a major overhaul, and on 15 August she was redesignated SS(N)-587.",
      "tier": 1,
      "source": {"title": "Naval History and Heritage Command, DANFS, Halibut II (SSG(N)-587)", "url": "https://www.history.navy.mil/research/histories/ship-histories/danfs/h/halibut-ii.html"}
    },
    {
      "text": "The published entry carries no awards or unit citation list, no reference to special operations, and no narrative after 1967; its characteristics line gives the ship's speed and complement as classified.",
      "tier": 1,
      "source": {"title": "Naval History and Heritage Command, DANFS, Halibut II (SSG(N)-587), read in full by this session", "url": "https://www.history.navy.mil/research/histories/ship-histories/danfs/h/halibut-ii.html"}
    },
    {
      "text": "On the Danny Jones show, in the episode mapped as file 04 of batch 18, at 2:37:23, Richard Dolan described an underwater version of the NRO started in 1969 that used this ship to place a tap on a Soviet undersea communications cable off Kamchatka around 1970 to 1971; no record opened by this pass supports any part of that.",
      "tier": 2,
      "source": {"title": "Danny Jones corpus lead map, dannyjones-corpus-18.md, file 04", "url": "research/leads/dannyjones-corpus-18.md"}
    }
  ],
  "edges": [
    {"to": "us-navy", "type": "institutional", "note": "A commissioned United States Navy submarine, documented in the Navy's own ship history series."},
    {"to": "d-denial", "type": "denial", "note": "The official ship history stops in 1967 and lists no awards, while the ship's later career is described in trade and encyclopedia sources only; the gap between the two is the finding, not a claim about what happened."}
  ]
}
```

---

## 9. Sumner Shapiro as Director of Naval Intelligence

**VERDICT: NOT OPENED.** No official record establishing the office or its dates was reached, so no
node is drafted and no claim about his tenure should be written from this pass.

### What was tried

| Route | Result |
|---|---|
| `history.navy.mil` leadership and Directors of Naval Intelligence paths | HTTP 404 on both paths tried, by curl with a browser user agent, on a host that answered 200 for the DANFS entry in row 4. The list is not at the URLs guessed and no site search reached it |
| `https://history.state.gov/search?q="Sumner Shapiro"` | The page returned "No results were found." FRUS does not carry him under that name |
| govinfo search API, his name and his name plus the office | 3,630 and 2,362 results respectively, all of them relevance noise (Supreme Court reports, Clerk of the House quarterly reports). The DEMO_KEY search does not honour phrases and returned nothing usable |
| A site-restricted web search over history.state.gov, archives.gov, history.navy.mil and dodig.mil | Returned no page from any of those hosts |

Every reachable statement of the 1978 to 1982 tenure is a newspaper obituary or an encyclopedia
entry. The triage row's own stated records, "the Navy register of commissioned officers" and a
Naval Institute oral history, were not reached: the register is not online at any path found and
the Institute's holdings sit behind a paywall. **A paywall and a 404 are both NOT OPENED.**

**Consequence for the board.** The triage row's argument was that `oni` is "a node with no named
director on it" and that Shapiro would be its first, on the Betty Sapp precedent. The precedent
holds only because Sapp's appointment record was actually opened. It is not available here, and
`oni` should stay without a named director until it is.

---

## 10. The Wackenhut Corporation, and whether Inman sat on its board

**VERDICT: CONTRADICTED for every proxy statement that exists on EDGAR. NOT OPENED for the years
before 1997, because Wackenhut filed no proxy with the Commission before then.**

### What was opened

| URL | What is at it |
|---|---|
| https://www.sec.gov/cgi-bin/browse-edgar?company=wackenhut&CIK=&type=DEF+14A&... | The EDGAR company index. One match: WACKENHUT CORP, CIK 0000104030, Florida, SIC 7381, "SERVICES-DETECTIVE, GUARD & ARMORED CAR SERVICES" |
| https://data.sec.gov/submissions/CIK0000104030.json | The company's full filing index. Earliest filing of any kind 24 March 1994. Proxy filings: PRE 14A 1997-03-24, DEF 14A 1997-05-06, DEFR14A 1998-04-03, DEF 14A 1998-04-28, PRE 14A 1999-01-29, DEF 14A 1999-03-05, DEFR14A 1999-03-23, DEF 14A 2000-05-17, DEF 14A 2001-05-04, PREM14A 2002-04-09, DEFM14A 2002-04-10 |
| https://www.sec.gov/Archives/edgar/data/0000104030/000095014498003074/0000950144-98-003074.txt | The proxy for the annual meeting of 24 April 1998, fiscal year ended 28 December 1997 |
| https://www.sec.gov/Archives/edgar/data/0000104030/000095014499003822/0000950144-99-003822.txt | The proxy for the annual meeting of 7 May 1999, fiscal year ended 3 January 1999, filed 31 March 1999 |
| https://www.sec.gov/Archives/edgar/data/104030/000095014402003675/g74655ddefm14a.htm | The 2002 merger proxy |

### What the documents establish

The 1999 proxy lists twelve nominees with ages and the year each became a director: Julius W.
Becton, Jr. (72, 1994); Alan B. Bernstein (51, 1998); Carroll A. Campbell, Jr. (58, 1997);
Benjamin R. Civiletti (63, 1998); Anne Newman Foreman (51, 1993); Edward L. Hennessy, Jr. (71,
1993); Paul X. Kelley (70, 1988); Nancy Clark Reynolds (71, 1986); John F. Ruffle (61, 1998);
Thomas P. Stafford (68, 1991); George R. Wackenhut (79, 1958); Richard R. Wackenhut (51, 1986). The
1998 proxy lists substantially the same board a year younger. **The name Inman does not appear in
the 1998 proxy, the 1999 proxy or the 2002 merger proxy.**

The 1999 list also settles a related point the triage row did not raise: this board is heavily
populated by former senior federal officials, an Army lieutenant general, a Marine Corps general, a
former Attorney General, a former Air Force general counsel and an astronaut, which is the
revolving-door structure the board tracks. It simply does not include Inman in these years.

### What the transcript claimed that these documents do NOT establish

| Claim | Cite | Status |
|---|---|---|
| "Bobby Ray Inman was a board member" of Wackenhut | 20 e320 2:06:30 (Gerb) | **CONTRADICTED for 1997 to 2002 by the instrument the triage row itself nominated.** No date is given on tape, so the claim is not disproved for earlier years, and EDGAR cannot reach them |
| Wackenhut trained DOE Special Response Teams and guarded Area 51 and S4 | 20 e320 2:06:30 to 2:08:58 | **Not addressed.** The proxies were read for the directorship question; no DOE protective-force contract record was opened this pass |

**What would settle the remainder, for the FOIA and records queue:** Wackenhut proxies before 1997
exist only in paper at the Commission and in the company's own annual reports; a request to the
SEC's public reference facility, or the corporation's 10-K exhibit lists on EDGAR back to 1994, are
the two routes. Do not enter an Inman directorship on the board in any form from this pass. The
board's Inman node is already sourced to SEC filings for SAIC; the same instrument returns a
different answer here and the node should say so.

### Draft node

```json
{
  "id": "wackenhut-corporation",
  "cls": "institution",
  "label": "The Wackenhut Corporation",
  "dateStart": "1954",
  "dateEnd": "2002",
  "desc": "A Florida private security and protective-force contractor, SIC 7381, publicly reporting to the Securities and Exchange Commission under CIK 0000104030 from 1994 until its 2002 merger. Its proxy statements name a board drawn heavily from retired flag officers and former federal appointees. It is on this board because a Danny Jones guest named it as the private guard force at federal special-access sites and placed Adm. Bobby Ray Inman on its board; the proxies covering 1997 to 2002 name every director and none of them is Inman.",
  "claims": [
    {
      "text": "The Wackenhut Corporation reported to the Securities and Exchange Commission under CIK 0000104030, classified under SIC 7381, services-detective, guard and armored car services; its earliest filing of any kind is dated 24 March 1994 and its earliest proxy statement is a preliminary 14A of 24 March 1997.",
      "tier": 1,
      "source": {"title": "SEC EDGAR company filing index, CIK 0000104030", "url": "https://data.sec.gov/submissions/CIK0000104030.json"}
    },
    {
      "text": "The proxy statement for the annual meeting of 7 May 1999 lists twelve directors by name, age and year of first election, among them Julius W. Becton, Jr., Benjamin R. Civiletti, Paul X. Kelley, Thomas P. Stafford and George R. Wackenhut, and the name Inman appears nowhere in it.",
      "tier": 1,
      "source": {"title": "The Wackenhut Corporation, DEF 14A filed 31 March 1999", "url": "https://www.sec.gov/Archives/edgar/data/0000104030/000095014499003822/0000950144-99-003822.txt"}
    },
    {
      "text": "The name Inman also appears nowhere in the proxy for the annual meeting of 24 April 1998 or in the 2002 merger proxy.",
      "tier": 1,
      "source": {"title": "The Wackenhut Corporation, DEF 14A for the 1998 annual meeting and DEFM14A filed 10 April 2002", "url": "https://www.sec.gov/Archives/edgar/data/0000104030/000095014498003074/0000950144-98-003074.txt"}
    },
    {
      "text": "On the Danny Jones show, 4 August 2025, at 2:06:30, the guest identified in the lead map as UAP Gerb said Bobby Ray Inman was a Wackenhut board member; the corporation's own proxy statements for 1997 to 2002 do not name him, and no proxy exists on EDGAR for any earlier year.",
      "tier": 2,
      "source": {"title": "Danny Jones corpus lead map, dannyjones-corpus-20.md, episode 320", "url": "research/leads/dannyjones-corpus-20.md"}
    }
  ],
  "edges": [
    {"to": "bobby-ray-inman", "type": "denial", "note": "Named on the podcast as a Wackenhut director; the corporation's own proxy statements for 1997 to 2002 name every director and he is not among them. The edge exists to carry the contradiction, not the association."},
    {"to": "d-custody", "type": "custody", "note": "A private protective-force contractor is the custody-force claim this board tracks; the DOE contract records that would document it were not opened this pass."}
  ]
}
```

---

## Triage-5 rows 2 and 18. Andrew Bustamante, Mark Zaid, and the prepublication mechanism

**VERDICT: PARTLY CONFIRMED for the mechanism, which is documented in the CIA's own released
procedures and in a filed court declaration. The book's own PRB clearance history is NOT OPENED and
was never a record. The post-2000 Malmstrom multi-missile shutdown is NOT OPENED and is recorded as
a gap needing a FOIA.**

### What was opened

| URL | What is at it |
|---|---|
| https://archive.org/download/cia-readingroom-document-06712956/06712956_djvu.txt | CIA reading-room document C06712956, "Prepublication Review Information", approved for release 2018/11/28. The item bundles the Board's public-facing guidance with an internal document dated 17 April 2013 headed "(U) PREPUBLICATION REVIEW PROCEDURES" and marked SECRET//CIA INTERNAL USE ONLY//NOFORN |
| https://www.cia.gov/about/organization/prepublication-classification-review-board/ | The Agency's current public page for the Prepublication Classification Review Board |
| https://sgp.fas.org/news/2001/08/zaid.html | "Declaration of Mark S. Zaid, Esq.", filed in Danny B. Stillman v. Department of Energy et al., United States District Court for the District of Columbia, Civil Action No. 01-01342 (EGS), signed 16 August 2001 |

`cia.gov/readingroom` looped to its own front page for the direct document URL and for the AR 6-2
regulation PDF; both were reached through the archive.org mirror instead, as the brief directs. The
Fourth Circuit's prepublication-review decision in Edgar v. Haines, No. 20-1568, decided 23 June
2021, was **not** opened: the court's own PDF and the cert petition appendix on supremecourt.gov
both returned compressed content that did not extract, and the Solicitor General's brief in
opposition in No. 21-791 did the same. That case is the right record and it is a gap.

### What the documents establish

**Who is bound and what must be submitted.** Anyone obligated by a CIA secrecy agreement who is
writing or speaking about intelligence-related materials, foreign relations, or CIA employment or
contract matters must submit the work before publishing it or sharing it with anyone. Both official
and personal works are covered. The current public page extends the list to book reviews, opinion
pieces, scholarly papers, resumes, scripts, screenplays, blogs and speeches, and to fiction as well
as non-fiction.

**The clock.** The released guidance says: "Please allow at least 30 working days for completion of
the review process." Written approval must be obtained before publication.

**The appeal, which is the part no secondary account carries.** An author may ask the Board to
reconsider; if the Board upholds its decision the author may formally appeal, in writing to the
Board's Chairman, within 30 days of the reconsideration decision, and the appeal goes to the
Agency's Associate Deputy Director for a final Agency decision.

**The custody provision, which is why this belongs on this board.** If the Board determines that a
manuscript contains classified information, the guidance requires the author to return "any and all
versions of this work, in whatever form" for destruction and to remove the items from their hard
drive, with CIA security personnel available to assist. **That is a documented, self-described
mechanism by which the Agency takes back an author's own text.**

**The required disclaimer.** Every approved writing must carry the Agency's own wording, which
states that nothing in the contents should be construed as asserting or implying US Government
authentication of information, and that the material has been reviewed by the CIA to prevent the
disclosure of classified information.

**Zaid.** The declaration establishes him as attorney of record in a prepublication matter in the
District of Columbia in 2001, states that he specialises in litigating national security cases
including those involving the First Amendment, and recites his 1996 representation of the CIA
whistleblower Patrick G. Eddington over a manuscript.

### What the transcript claimed that these documents do NOT establish

| Claim | Cite | Status |
|---|---|---|
| The manuscript for *Shadow Cell* was submitted in 2021, declared classified by CIA in 2022 in an email the author still holds, and approved about three weeks after suit was threatened | 21 e329 0:05:01 to 0:08:16 (Bustamante) | **NOT OPENED, and unopenable from a book.** The record is PRB correspondence in that specific case, which reaches the public only on FOIA or in a filed complaint. No complaint was found, and the author's account is that none was filed |
| Zaid is the reachable end of that mechanism | triage-5 A18 | **Partly.** He is documented as counsel in prepublication litigation, in 2001, in a different matter. Nothing opened connects him to the *Shadow Cell* review |
| A post-2000 systematic multi-missile shutdown at Malmstrom with multiple witnesses and a filed report, and no light in the sky | 21 e329 0:24:10 to 0:24:43 (Bustamante) | **NOT OPENED. This is a gap needing a FOIA**, to Air Force Global Strike Command and the 341st Missile Wing, for any incident or command-post report of a multi-facility outage in the stated period. The board's Malmstrom thread ends in the 1970s and must not be extended on testimony |

### Draft node

```json
{
  "id": "cia-prepublication-classification-review-board",
  "cls": "institution",
  "label": "CIA Prepublication Classification Review Board",
  "desc": "The CIA board that reviews, before publication, anything an employee or contractor bound by a secrecy agreement intends to say or write about intelligence. Its own released guidance sets a 30 working day clock, requires written approval before publication, routes appeals to the Agency's Associate Deputy Director, and, where a manuscript is found to contain classified information, requires the author to surrender every version of the work for destruction and to delete it from their hard drive. It is on this board as a documented custody mechanism operating on text rather than on hardware, and as the mechanism through which several of the corpus's own witnesses say their accounts were shaped.No founding instrument for the Board was opened by this pass, so the draft node carries no date; one must be added from a record before it is built.",
  "claims": [
    {
      "text": "The Board's released guidance states: Please allow at least 30 working days for completion of the review process.",
      "tier": 1,
      "source": {"title": "Prepublication Review Information, CIA reading-room document C06712956, approved for release 2018/11/28", "url": "https://archive.org/download/cia-readingroom-document-06712956/06712956_djvu.txt"}
    },
    {
      "text": "The same guidance provides that if the Board upholds its decision on reconsideration the author may formally appeal in writing to the Board's Chairman within 30 days, and that such appeals go to the Agency's Associate Deputy Director for a final Agency decision.",
      "tier": 1,
      "source": {"title": "Prepublication Review Information, CIA reading-room document C06712956", "url": "https://archive.org/download/cia-readingroom-document-06712956/06712956_djvu.txt"}
    },
    {
      "text": "Where the Board determines that a manuscript contains classified information, the guidance requires the author to return any and all versions of this work, in whatever form, for destruction and to remove those items from their hard drive, with CIA security personnel available to assist.",
      "tier": 1,
      "source": {"title": "Prepublication Review Information, CIA reading-room document C06712956", "url": "https://archive.org/download/cia-readingroom-document-06712956/06712956_djvu.txt"}
    },
    {
      "text": "The released item includes an internal document dated 17 April 2013 headed Prepublication Review Procedures and marked SECRET//CIA INTERNAL USE ONLY//NOFORN, describing manuscript flow through a case assigner, a Team Lead, equity-holding Information Review Officers and a second reviewer.",
      "tier": 1,
      "source": {"title": "Prepublication Review Information, CIA reading-room document C06712956", "url": "https://archive.org/download/cia-readingroom-document-06712956/06712956_djvu.txt"}
    },
    {
      "text": "Mark S. Zaid was attorney of record for the plaintiff in Danny B. Stillman v. Department of Energy, United States District Court for the District of Columbia, Civil Action No. 01-01342 (EGS), and stated in his declaration of 16 August 2001 that he specialises in litigating national security cases including those involving the First Amendment.",
      "tier": 1,
      "source": {"title": "Declaration of Mark S. Zaid, Esq., Stillman v. Department of Energy, D.D.C. No. 01-01342 (EGS), 16 August 2001", "url": "https://sgp.fas.org/news/2001/08/zaid.html"}
    },
    {
      "text": "On the Danny Jones show, in the episode mapped as 329, at 0:05:01 to 0:08:16, Andrew Bustamante said his manuscript was submitted in 2021, declared classified by CIA in 2022, and approved roughly three weeks after suit was threatened; no CIA record of that review was opened by this pass and the book's own clearance page is not a record.",
      "tier": 2,
      "source": {"title": "Danny Jones corpus lead map, dannyjones-corpus-21.md, episode 329", "url": "research/leads/dannyjones-corpus-21.md"}
    }
  ],
  "edges": [
    {"to": "cia", "type": "institutional", "note": "A board of the Agency, described in the Agency's own released guidance."},
    {"to": "d-custody", "type": "custody", "note": "The guidance's own destruction and hard-drive removal provision is a documented custody mechanism operating on an author's text."},
    {"to": "d-denial", "type": "denial", "note": "The mandatory disclaimer required on every approved writing states that nothing in it implies US Government authentication of the information, which is a formal, self-documented denial attached in advance to every cleared account."}
  ]
}
```

---

## Gaps this pass created, for the FOIA and records queue

| # | What | The instrument |
|---|---|---|
| 1 | The 1969 instrument establishing a National Underwater Reconnaissance Office, and the identity of its directors | Mandatory declassification review to the NRO's Center for the Study of National Reconnaissance; FOIA to the Chief of Naval Operations |
| 2 | The Ivy Bells codename in any federal record | FOIA to NSA for the damage assessment referenced in the Pelton prosecution; the trial record in D. Md. |
| 3 | USS Halibut's unit awards for 1968 and 1972 | The Chief of Naval Operations awards record, or the ship's Command Operations Reports at NHHC |
| 4 | Sumner Shapiro's appointment and tenure as Director of Naval Intelligence | The Navy register of commissioned officers for 1978 to 1982; his official Navy biography |
| 5 | Wackenhut board composition before 1997 | The SEC public reference facility for paper proxies; the corporation's 10-K exhibits from 1994 |
| 6 | The *Shadow Cell* prepublication file | FOIA to the CIA Prepublication Classification Review Board for correspondence in the named matter |
| 7 | A post-2000 multi-missile shutdown at Malmstrom | FOIA to Air Force Global Strike Command and the 341st Missile Wing for incident and command-post reports |
| 8 | Edgar v. Haines, No. 20-1568 (4th Cir., decided 23 June 2021) | The opinion, from a source whose PDF extracts; it is the appellate holding on the whole prepublication regime and it did not open here |
