# Verified leads: Area 52 corpus, section A candidates A1, A2, A3, A5, A7, A9 (verifier 6)

**Status: research output, not board content.** Nothing here has been merged into
`research/`, into `data/*.json` or into any node. This is a verification pass over six
section A rows of `research/leads/area52-triage-5.md`, against
`research/leads/VERIFY-BRIEF-AREA52-2026-09-02.md`.

**Verified 2 September 2026.** Every URL below was opened by this session and returned the
document described. Where a document is a scan, the text quoted was read from the OCR layer
the archive itself publishes, and that is labelled where it applies. `CLAUDE.md` section 2
governs: nothing here is asserted that was not opened.

**Board state, read from `data/the-program.json` by this session, not taken from the triage
file.**

| string searched | occurrences | reading |
|---|---|---|
| `Stony Brook` | 0 | absent |
| `E-Systems` | 1 | the one hit is the substring inside "space-systems"; the company is absent |
| `LTV`, `Vought` | 0, 0 | absent |
| `Armed Forces Institute of Pathology`, `Joint Pathology` | 0, 0 | absent |
| `Naval Investigative`, `\bNIS\b`, `\bNCIS\b` | 0, 0, 0 | absent. The triage file's "NCIS 11" was a substring artefact, inside "Francisco" and "inciso" |
| `Pandolfi` | 0 | absent |
| `Federal Aviation Administration`, `\bFAA\b` | 8, 77 | prose only, no node. Triage C1 is right that the ABSENT verdict was wrong |

## Summary

| # | Lead | Verdict | Board |
|---|---|---|---|
| A1 | LTV Aerospace to E-Systems to Raytheon | PARTLY CONFIRMED; the first link of the succession is CONTRADICTED | new node, but for **E-Systems, Inc.**, not LTV Aerospace |
| A2 | Stony Brook University via the Brookhaven M&O contract | CONFIRMED | new node |
| A3 | Armed Forces Institute of Pathology | CONFIRMED | new node |
| A5 | Naval Investigative Service to NCIS | PARTLY CONFIRMED; the row's **1992** date is not established by anything opened | new node |
| A7 | Ronald Pandolfi | NOT OPENED | no node |
| A9 | Federal Aviation Administration | CONFIRMED as a promotion from prose | new node |

**The four findings that matter, in order:**

1. **E-Systems' predecessor was LTV Electrosystems, not LTV Aerospace.** SEC EDGAR carries
   the former conformed names for CIK 0000030875 in its own submission header: "LTV
   ELECTROSYSTEMS INC", name change 16 May 1972, and "LTV ELECTROSYSTEMS INC GREENVILLE
   EMPLOY", name change 21 June 1973. The speaker's chain has the wrong LTV subsidiary at its
   head. LTV Aerospace has no EDGAR filer record and was not opened from here.
2. **Edward C. Aldridge is not on E-Systems' board.** The Schedule 14D-9 information
   statement of 3 April 1995 lists the company's ten directors by name, age and year of
   election. None is Aldridge or Aldrich. His claimed seat is on LTV Aerospace's board, which
   is a different body, but the E-Systems record does not place him anywhere in this chain
   either.
3. **The 1992 NIS to NCIS date is not in any record opened from here.** The earliest opened
   federal record carrying the new name is 9 June 1994, when the Navy amended 32 CFR 701.5 by
   striking "Commander, Naval Investigative Service Command" and inserting "Director, Naval
   Criminal Investigative Service". Eight days earlier, on 1 June 1994, another Navy rule
   still printed the old title. Do not carry 1992 into a node on the triage row's word.
4. **10 U.S.C. 176 is still on the books.** The Office of Law Revision Counsel serves the
   section with the line "Text contains those laws in effect on September 1, 2026". AFIP was
   disestablished by a BRAC recommendation and its functions dispersed, and the statute that
   created it was never repealed. The gap between the administrative and the statutory record
   is the finding, and it is this board's structural argument in miniature.

---

## A1. LTV Aerospace to E-Systems to Raytheon

**Opened**

| document | URL |
|---|---|
| Schedule 14D-1, Raytheon Company and RTN Acquisition Corporation for E Systems Inc, filed 3 April 1995, accession 0000950109-95-001096 | https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001096.txt |
| Schedule 14D-9, E-Systems Inc, filed 3 April 1995, accession 0000950109-95-001097 | https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001097.txt |
| Form 10-K for fiscal 1994, E Systems Inc, filed 27 March 1995, accession 0000912057-95-001713 | https://www.sec.gov/Archives/edgar/data/30875/0000912057-95-001713.txt |
| Schedule 14D-1/A Amendment No. 4 (Final Amendment), filed 1 May 1995, accession 0000950130-95-000863 | https://www.sec.gov/Archives/edgar/data/30875/0000950130-95-000863.txt |

`sec.gov` answered curl once a browser user agent and a contact address were sent, as the
brief said it would.

**What the documents are.** A completed cash tender offer and its final amendment, plus the
target's last annual report and its board's recommendation statement. The EDGAR submission
header on every one of them carries the filer's own name history.

**What they establish.**

- E Systems Inc, central index key 0000030875, Delaware, SIC 3812 (search, detection,
  navigation, guidance, aeronautical systems), principal offices at 6250 LBJ Freeway, Dallas,
  Texas. Former conformed names in the EDGAR header: "LTV ELECTROSYSTEMS INC", date of name
  change 16 May 1972, and "LTV ELECTROSYSTEMS INC GREENVILLE EMPLOY", date of name change 21
  June 1973.
- The 10-K states "The Company was incorporated in Delaware in 1964", and in its
  environmental disclosures refers to "the Company and its predecessor corporation, LTV". The
  composite certificate of incorporation filed as Exhibit 3(i) is signed by its incorporators
  on 28 December 1964.
- The 14D-9 information statement's biography of director E. F. Buehring names "Texas
  Engineering and Manufacturing Company (TEMCO), an E-Systems predecessor company", and says
  he was president and chief executive of the company "from its beginning in 1965 until
  1969".
- The business description carried into the 14D-1 from the 10-K: reconnaissance and
  surveillance systems and command, control and communications systems were "approximately
  75% of the Company's sales in 1994"; the company also designed and made "intelligence
  collection and processing systems".
- Raytheon Company, through RTN Acquisition Corporation, offered $64.00 per share in cash for
  all shares under an Agreement and Plan of Merger dated as of 2 April 1995. The offer expired
  at midnight on 28 April 1995. The final amendment records approximately 96.46 per cent of
  shares tendered, and Raytheon's press release of 1 May 1995 announces completion of a
  transaction "valued at $2.3 billion", with E-Systems' 1994 sales at about $2 billion and
  approximately 16,000 employees.

**What the transcript claimed that these do NOT establish.** The passage, DEBRIEFED with
Chris Ramsay, 17 July 2026, at 0:55:31: "He was a senior, I think, board member at LTV
Aerospace, which was eventually transitioned to E systems, which was a CIA show company and
then bought up by Raytheon." Three parts fail against the record. The predecessor named in
the filings is LTV **Electrosystems**, not LTV Aerospace. Aldridge appears nowhere in the
14D-9's list of directors (Bitonti, Kling, Tacke, Buehring, Gabriel, Lawson, Haden, Hoffmann,
Keiffer, Neff). And nothing in any filing supports "CIA shell company"; the filings describe
a listed NYSE defence electronics contractor. The acquisition by Raytheon is the one part of
the chain the record supports, and it supports it exactly.

**Not opened.** LTV Aerospace's own corporate record. EDGAR's company search returns no LTV
Aerospace filer; the LTV entities that do appear are Ohio steel companies and unrelated
blank-check shells. The triage row's other suggestions, Delaware and Texas corporate records
and the LTV Chapter 11 docket, were not reached from here.

```json
{
  "id": "e-systems-inc",
  "cls": "institution",
  "label": "E-Systems, Inc.",
  "dateStart": "1964-12-28",
  "dateEnd": "1995-05-01",
  "desc": "A Dallas defence electronics contractor, incorporated in Delaware in 1964 and acquired by Raytheon in a $2.3 billion cash tender offer completed on 1 May 1995. Its SEC filer record carries its own name history: it filed as LTV Electrosystems, Inc. until 1972. Three quarters of its 1994 sales were reconnaissance and surveillance systems and command, control and communications systems, and it also built intelligence collection and processing systems. It is drafted here because a podcast panel used it as the middle term of a custody chain running LTV Aerospace to E-Systems to Raytheon; the filings contradict the first link, naming LTV Electrosystems rather than LTV Aerospace as the predecessor, and place Edward C. Aldridge nowhere in the company's governance.",
  "claims": [
    {
      "tier": 1,
      "text": "SEC EDGAR records E Systems Inc at central index key 0000030875, incorporated in Delaware, SIC 3812, with two former conformed names: LTV ELECTROSYSTEMS INC, date of name change 16 May 1972, and LTV ELECTROSYSTEMS INC GREENVILLE EMPLOY, date of name change 21 June 1973.",
      "source": "Schedule 14D-1 submission header, Raytheon Company and RTN Acquisition Corporation for E Systems Inc, accession 0000950109-95-001096, filed 3 April 1995, https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001096.txt"
    },
    {
      "tier": 1,
      "text": "E-Systems' Form 10-K for fiscal 1994 states that 'The Company was incorporated in Delaware in 1964' and, in its environmental disclosures, refers to 'the Company and its predecessor corporation, LTV'.",
      "source": "E Systems Inc Form 10-K, accession 0000912057-95-001713, filed 27 March 1995, https://www.sec.gov/Archives/edgar/data/30875/0000912057-95-001713.txt"
    },
    {
      "tier": 1,
      "text": "The Form 10-K business description states that reconnaissance and surveillance systems and command, control and communications systems 'represented approximately 75% of the Company's sales in 1994', and that the company also designed and manufactured intelligence collection and processing systems.",
      "source": "E Systems Inc Form 10-K, accession 0000912057-95-001713, filed 27 March 1995, https://www.sec.gov/Archives/edgar/data/30875/0000912057-95-001713.txt"
    },
    {
      "tier": 1,
      "text": "Raytheon Company, through RTN Acquisition Corporation, offered $64.00 per share in cash for all E-Systems shares under an Agreement and Plan of Merger dated as of 2 April 1995; the offer expired on 28 April 1995 with approximately 96.46 per cent of shares tendered, and Raytheon's press release of 1 May 1995 announced completion of a transaction 'valued at $2.3 billion'.",
      "source": "Schedule 14D-1/A Amendment No. 4 (Final Amendment) and Exhibit (a)(9), accession 0000950130-95-000863, filed 1 May 1995, https://www.sec.gov/Archives/edgar/data/30875/0000950130-95-000863.txt"
    },
    {
      "tier": 1,
      "text": "The ten directors of E-Systems listed in the Schedule 14D-9 information statement of 3 April 1995 are James A. Bitonti, S. Lee Kling, David R. Tacke, E. F. Buehring, Charles A. Gabriel, A. Lowell Lawson, C. Roland Haden, Martin R. Hoffmann, E. Gene Keiffer and Francine I. Neff. Edward C. Aldridge is not among them.",
      "source": "Schedule 14D-9, E-Systems Inc, accession 0000950109-95-001097, filed 3 April 1995, https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001097.txt"
    },
    {
      "tier": 2,
      "text": "On DEBRIEFED with Chris Ramsay, 17 July 2026, at 0:55:31, a panel speaker who self-identifies at 0:58:00 as the maker of 'my Air Force video' said of Edward C. 'Pete' Aldridge that 'He was a senior, I think, board member at LTV Aerospace, which was eventually transitioned to E systems, which was a CIA show company and then bought up by Raytheon.' The opened SEC filings name LTV Electrosystems, not LTV Aerospace, as the predecessor, list ten directors none of whom is Aldridge, and describe a listed NYSE contractor rather than a proprietary.",
      "source": "DEBRIEFED with Chris Ramsay, 'Jesse Michels, UAPGerb & Chris Ramsay - Flying Saucer Diner', 17 July 2026, 0:55:31, transcript in dist/transcripts/md/"
    }
  ],
  "sources": [
    "https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001096.txt",
    "https://www.sec.gov/Archives/edgar/data/30875/0000950109-95-001097.txt",
    "https://www.sec.gov/Archives/edgar/data/30875/0000912057-95-001713.txt",
    "https://www.sec.gov/Archives/edgar/data/30875/0000950130-95-000863.txt"
  ],
  "edges": [
    {
      "to": "raytheon",
      "type": "custody",
      "note": "Raytheon acquired E-Systems outright on 1 May 1995, taking its reconnaissance, surveillance and intelligence-collection business lines into the Raytheon node the board already carries."
    }
  ]
}
```

---

## A2. Stony Brook University, via the Brookhaven management-and-operating contract

**Opened**

| document | URL |
|---|---|
| Brookhaven National Laboratory, "About Brookhaven", management and leadership statement | https://www.bnl.gov/about/ |
| USAspending award search, recipient "Brookhaven Science Associates" | https://api.usaspending.gov/api/v2/search/spending_by_award/ |

**What the documents are.** The laboratory's own statement of who manages it under the DOE
Office of Science contract, and the federal spending record of the two
management-and-operating contracts themselves.

**What they establish.**

- "Brookhaven Lab is managed for the Office of Science by Brookhaven Science Associates, a
  partnership between Stony Brook University and Battelle, and six core universities:
  Columbia, Cornell, Harvard, Massachusetts Institute of Technology, Princeton, and Yale."
- The same site states the arrangement more precisely in its standing footer text: "BSA is a
  partnership between Battelle and The Research Foundation for the State University of New
  York on behalf of Stony Brook University."
- USAspending records two Department of Energy contracts to BROOKHAVEN SCIENCE ASSOCIATES
  LLC:

| award ID | description | period | obligations |
|---|---|---|---|
| DESC0012704 | "M&O CONTRACT FOR BNL" | 5 January 2015 to 4 January 2030 | $8,629,200,535.17 |
| DEAC0298CH10886 | "OPERATION OF BROOKHAVEN NATIONAL LABORATORY" | 15 October 1999 to 4 January 2015 | $7,896,665,930.11 |

This is the same evidence shape the board already accepts on the `battelle` node for Pacific
Northwest (DEAC0576RL01830) and Oak Ridge (DEAC0500OR22725), so the node lands in an existing
pattern rather than opening a new one.

**What the transcript claimed that these do NOT establish.** The passage, 17 July 2026 at
1:01:18: "And then Stony Brook, he oversees. He was Stony Brook and he also over set- it's
Brookhaven National Labs. So is this kind of iron triangle." Nothing in the opened record
names James Simons, the Simons Foundation or any individual as overseeing either body. The
opened record shows a corporate partnership holding a DOE contract. The speaker says in the
same passage "This is a lot of crazy connections", and the triage row already flags that he
offers no mechanism.

**A correction to the triage row itself.** The row describes Brookhaven Science Associates as
"a Stony Brook and **Battelle** partnership". That is what the About page's summary sentence
says, but the fuller statement on the same site adds six core universities and routes Stony
Brook's participation through The Research Foundation for the State University of New York. A
node should carry the fuller form, not the shorthand.

```json
{
  "id": "stony-brook-university",
  "cls": "institution",
  "label": "Stony Brook University",
  "dateStart": "1999-10-15",
  "desc": "A State University of New York campus that is one of the two named partners in Brookhaven Science Associates LLC, the entity holding the Department of Energy management-and-operating contract for Brookhaven National Laboratory. The other named partner is Battelle, which this board already carries as its most persistent institution. Brookhaven's own statement routes Stony Brook's participation through The Research Foundation for the State University of New York and adds six core universities. It is drafted here because the board states that Battelle is a partner in Brookhaven without naming the other partner, and because a podcast panel used the Stony Brook and Brookhaven pairing as an innuendo where the record offers a contract.",
  "claims": [
    {
      "tier": 1,
      "text": "Brookhaven National Laboratory states that 'Brookhaven Lab is managed for the Office of Science by Brookhaven Science Associates, a partnership between Stony Brook University and Battelle, and six core universities: Columbia, Cornell, Harvard, Massachusetts Institute of Technology, Princeton, and Yale.'",
      "source": "Brookhaven National Laboratory, 'About Brookhaven', https://www.bnl.gov/about/"
    },
    {
      "tier": 1,
      "text": "The same site states that 'BSA is a partnership between Battelle and The Research Foundation for the State University of New York on behalf of Stony Brook University.'",
      "source": "Brookhaven National Laboratory, 'About Brookhaven', https://www.bnl.gov/about/"
    },
    {
      "tier": 1,
      "text": "Brookhaven Science Associates LLC holds Department of Energy contract DESC0012704, described on USAspending as the management-and-operating contract for BNL, running 5 January 2015 to 4 January 2030 with recorded obligations of $8,629,200,535.17.",
      "source": "USAspending.gov award search, recipient Brookhaven Science Associates, https://api.usaspending.gov/api/v2/search/spending_by_award/"
    },
    {
      "tier": 1,
      "text": "The predecessor contract DEAC0298CH10886, described as 'OPERATION OF BROOKHAVEN NATIONAL LABORATORY', ran 15 October 1999 to 4 January 2015 with recorded obligations of $7,896,665,930.11 to the same recipient.",
      "source": "USAspending.gov award search, recipient Brookhaven Science Associates, https://api.usaspending.gov/api/v2/search/spending_by_award/"
    },
    {
      "tier": 2,
      "text": "On DEBRIEFED with Chris Ramsay, 17 July 2026, at 1:01:18, a panel speaker said that James Simons 'oversees' Stony Brook and Brookhaven National Laboratory and called the pairing with the Medallion Fund and the Simons Foundation an 'iron triangle', adding in the same passage 'This is a lot of crazy connections.' No document opened here names Simons in connection with either body.",
      "source": "DEBRIEFED with Chris Ramsay, 'Jesse Michels, UAPGerb & Chris Ramsay - Flying Saucer Diner', 17 July 2026, 1:01:18, transcript in dist/transcripts/md/"
    }
  ],
  "sources": [
    "https://www.bnl.gov/about/",
    "https://api.usaspending.gov/api/v2/search/spending_by_award/"
  ],
  "edges": [
    {
      "to": "battelle",
      "type": "institutional",
      "note": "Stony Brook and Battelle are the two named partners in Brookhaven Science Associates LLC, which holds the DOE management-and-operating contract for Brookhaven National Laboratory."
    },
    {
      "to": "doe",
      "type": "funding",
      "note": "The Department of Energy is the contracting agency for both Brookhaven management-and-operating contracts, DEAC0298CH10886 and DESC0012704."
    }
  ]
}
```

---

## A3. Armed Forces Institute of Pathology

**Opened**

| document | URL |
|---|---|
| 10 U.S.C. 176, "Armed Forces Institute of Pathology", with source credit and statutory notes | https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section176&num=0&edition=prelim |
| 2005 Defense Base Closure and Realignment Commission Report, Volume 1, 8 September 2005, DTIC AD-A466177, OCR text layer | https://archive.org/download/DTIC_ADA466177/DTIC_ADA466177_djvu.txt |

The BRAC report was read through the OCR text layer archive.org publishes for the DTIC mirror
item `DTIC_ADA466177`. Volume 2 of the same report was downloaded and contains no mention of
the Institute.

**What the documents are.** The codified statute that created AFIP, carrying in its notes the
verbatim text of the 2008 provision that established the Joint Pathology Center; and the
Commission's own final report to the President, which prints both the Secretary of Defense's
proposed recommendation and the Commission's amended one.

**What they establish.**

- 10 U.S.C. 176(a)(1): "There is in the Department of Defense an Institute to be known as the
  Armed Forces Institute of Pathology". Added by Pub. L. 94-361, title VIII, section 811(b),
  14 July 1976, 90 Stat. 933, and amended six times through Pub. L. 107-107 in 2001.
- The Office of Law Revision Counsel serves the section with the line "Text contains those
  laws in effect on September 1, 2026", so the section has not been repealed.
- The Institute is "a joint entity of the three military departments, subject to the
  authority, direction, and control of the Secretary of Defense", governed by a Board of
  Governors chaired by the Assistant Secretary of Defense for Health Affairs and including
  the Surgeons General of the Army, Navy and Air Force and the Under Secretary for Health of
  the Department of Veterans Affairs.
- The BRAC report's Walter Reed recommendation, numbered 169 (Med 4), carries in both the
  Secretary's and the Commission's versions the clause "disestablish all elements of the
  Armed Forces Institute of Pathology except the National Medical Museum and the Tissue
  Repository". The Commission's version adds that "AFIP capabilities not specified in this
  recommendation will be absorbed into other DoD, Federal, or civilian facilities, as
  necessary".
- The Commission "found that DoD failed to sufficiently address several AFIP functions, such
  as the Radiologic Pathology program, with the associated tissue repository, veterinary
  pathology and continuing medical education", and found that the Secretary of Defense
  "deviated substantially from final selection criteria 1, as well as from the Force
  Structure Plan".
- The report gives the lineage: AFIP "was originally established as the Army Medical Museum in
  1862 as a public and professional repository for injuries and disease specimens of Civil War
  soldiers", opened its educational facilities to civilian medicine in 1888, and was made a
  joint entity by Congress in 1976.
- The Joint Pathology Center: Pub. L. 110-181, division A, title VII, section 722, 28 January
  2008, 122 Stat. 199, provides that "The President shall establish and maintain a Joint
  Pathology Center that shall function as the reference center in pathology for the Federal
  Government", to be established in the Department of Defense "consistent with the final
  recommendations of the 2005 Defense Base Closure and Realignment Commission, as approved by
  the President", and to provide, at a minimum, diagnostic pathology consultation, pathology
  education, diagnostic pathology research and "Maintenance and continued modernization of the
  Tissue Repository".

**What the transcript claimed that these do NOT establish.** Doty's account, 21 August 2026 at
3:21:29, places Kit Green at AFIP performing or reviewing autopsies on recovered non-human
bodies. Nothing in the statute or the BRAC report names any individual, and neither document
characterises any specimen. It is also worth recording what the transcript actually does: the
lead map has Green "reviewed/performed autopsies", but the speaker corrects himself inside one
passage, from "green did autopsies" to "he saw the aftermaths read reports". A node's Tier 2
claim should carry the corrected form.

```json
{
  "id": "armed-forces-institute-of-pathology",
  "cls": "institution",
  "label": "Armed Forces Institute of Pathology",
  "dateStart": "1976-07-14",
  "desc": "A Department of Defense pathology institute created by statute in 1976 as a joint entity of the three military departments, with a lineage the 2005 BRAC Commission traces to the Army Medical Museum of 1862. The 2005 BRAC recommendation on Walter Reed disestablished all of its elements except the National Medical Museum and the Tissue Repository, and directed that its unspecified capabilities be absorbed into other DoD, Federal or civilian facilities; Congress then required a Joint Pathology Center in the FY2008 National Defense Authorization Act. Its authorising statute, 10 U.S.C. 176, was never repealed and remains in force. It is drafted here for that documented custody chain over a national tissue repository, not for the claim that put it into the corpus.",
  "claims": [
    {
      "tier": 1,
      "text": "10 U.S.C. 176 provides that 'There is in the Department of Defense an Institute to be known as the Armed Forces Institute of Pathology', a joint entity of the three military departments subject to the authority, direction and control of the Secretary of Defense, added by Pub. L. 94-361, title VIII, section 811(b), 14 July 1976, 90 Stat. 933.",
      "source": "10 U.S.C. 176, Office of Law Revision Counsel, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section176&num=0&edition=prelim"
    },
    {
      "tier": 1,
      "text": "The Office of Law Revision Counsel serves 10 U.S.C. 176 with the statement 'Text contains those laws in effect on September 1, 2026', so the section creating the Institute remains in force after the Institute itself was disestablished.",
      "source": "10 U.S.C. 176, Office of Law Revision Counsel, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section176&num=0&edition=prelim"
    },
    {
      "tier": 1,
      "text": "The 2005 Defense Base Closure and Realignment Commission's final report of 8 September 2005, recommendation 169 (Med 4) on Walter Reed Army Medical Center, directs the Department to 'disestablish all elements of the Armed Forces Institute of Pathology except the National Medical Museum and the Tissue Repository', with the Commission's amended version adding that AFIP capabilities not specified 'will be absorbed into other DoD, Federal, or civilian facilities, as necessary'.",
      "source": "2005 Defense Base Closure and Realignment Commission Report, Volume 1, DTIC AD-A466177, OCR text layer, https://archive.org/download/DTIC_ADA466177/DTIC_ADA466177_djvu.txt"
    },
    {
      "tier": 1,
      "text": "The same report records that the Commission found the Department 'failed to sufficiently address several AFIP functions, such as the Radiologic Pathology program, with the associated tissue repository, veterinary pathology and continuing medical education', and that the Secretary of Defense 'deviated substantially from final selection criteria 1, as well as from the Force Structure Plan'.",
      "source": "2005 Defense Base Closure and Realignment Commission Report, Volume 1, DTIC AD-A466177, OCR text layer, https://archive.org/download/DTIC_ADA466177/DTIC_ADA466177_djvu.txt"
    },
    {
      "tier": 1,
      "text": "Pub. L. 110-181, division A, title VII, section 722, 28 January 2008, 122 Stat. 199, provides that 'The President shall establish and maintain a Joint Pathology Center that shall function as the reference center in pathology for the Federal Government', established in the Department of Defense consistent with the 2005 BRAC recommendations, and providing for maintenance and continued modernization of the Tissue Repository.",
      "source": "Statutory note 'Establishment of Joint Pathology Center' to 10 U.S.C. 176, https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section176&num=0&edition=prelim"
    },
    {
      "tier": 2,
      "text": "On DEBRIEFED with Chris Ramsay, 21 August 2026, at 3:21:29, Richard Doty said he knew of autopsies on recovered bodies 'from people like Kate Green and others that work for the Institute for Armed Force Institute for Pathology', then corrected himself within the same passage from 'green did autopsies' to 'he saw the aftermaths read reports'. No document opened here names any individual at the Institute.",
      "source": "DEBRIEFED with Chris Ramsay, 'Former Counterintelligence Agent Shares Wild Alien Encounters - Richard Doty', 21 August 2026, 3:21:29, transcript in dist/transcripts/md/"
    }
  ],
  "sources": [
    "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title10-section176&num=0&edition=prelim",
    "https://archive.org/download/DTIC_ADA466177/DTIC_ADA466177_djvu.txt"
  ],
  "edges": [
    {
      "to": "dod",
      "type": "institutional",
      "note": "10 U.S.C. 176 places the Institute in the Department of Defense as a joint entity of the three military departments under the Secretary's authority, direction and control."
    },
    {
      "to": "kit-green",
      "type": "witness-chain",
      "note": "Richard Doty places Green at the Institute on 21 August 2026 at 3:21:29, a Tier 2 claim that no opened Institute record corroborates or refutes."
    }
  ]
}
```

---

## A5. Naval Investigative Service and the redesignation as NCIS

**Opened**

| document | URL |
|---|---|
| Federal Register Doc 94-13966, Department of the Navy final rule amending 32 CFR part 701, effective 9 June 1994 | https://www.federalregister.gov/documents/full_text/text/1994/06/09/94-13966.txt |
| Federal Register Doc 94-13279, Department of Defense, Department of the Navy, 1 June 1994 | https://www.federalregister.gov/documents/1994/06/01/94-13279/ |
| FAS Navy Intelligence and Security Doctrine, SECNAVINST index | https://irp.fas.org/doddir/navy/secnavinst/index.html |

**What the documents are.** Two Navy rulemakings published eight days apart in 1994, one of
which changes the codified name of the organisation and the title of its head, and the FAS
index of Secretary of the Navy instructions.

**What they establish.**

- FR Doc 94-13966, effective 9 June 1994, amends 32 CFR part 701, the Navy's Freedom of
  Information Act program, which its preamble says is "derived from the Secretary of the Navy
  Instruction 5720.42 series". Item 6 of the amendment removes "Commander, Naval Investigative
  Service Command" from section 701.5(e)(2)(iii)(B) and adds in its place "Director, Naval
  Criminal Investigative Service". The same rule replaces "Naval Intelligence Command" with
  "Office of Naval Intelligence" in the adjacent paragraph.
- FR Doc 94-13279, published 1 June 1994, still lists "Commander, Naval Investigative Service
  Command" among the officers it designates. The former title was therefore in current Federal
  Register use eight days before the substitution.
- The FAS SECNAVINST index, opened as HTML, lists "SECNAV 5430.107 12/28/05 MISSION AND
  FUNCTIONS OF THE NAVAL CRIMINAL INVESTIGATIVE SERVICE 20" pages.

**What the triage row claimed that these do NOT establish.** The row calls for "the SECNAV
instruction establishing NIS and the 1992 redesignation as NCIS". Neither the establishing
instruction nor a 1992 date was opened. The earliest federal record reached from here that
carries the new name is 9 June 1994, and the 1 June 1994 rule still carries the old one. The
1992 date should not be carried into a node.

**Not opened, and what was tried.**

| target | what happened |
|---|---|
| SECNAVINST 5430.107 PDF at `irp.fas.org/doddir/navy/secnavinst/5430_107.pdf` | HTTP 202 with a zero-byte body, three times, on curl and on WebFetch. HTML pages on the same host answer normally; the PDFs do not. Same failure the brief records for `fas.org` |
| `ncis.navy.mil` history page and the NCIS Manual 1 PDF | HTTP 403 on both curl and WebFetch |
| `secnav.navy.mil/doni` directive PDFs | an Imperva interstitial in place of the file |
| govinfo search API, for congressional and GAO material on the redesignation | OVER_RATE_LIMIT on every attempt, including the collections listing, with `DEMO_KEY`. The `wssearch` endpoint rejected the payload |
| `gao.gov` | HTTP 403 |
| Federal Register full-text search before 1994 | the API's full-text index begins 1 January 1994, so a 1992 or 1993 notice cannot be found this way |

What the speaker himself says, at 1:17:09 on 21 August 2026, carries no date either: "the
Naval Investigative Service, which is now Naval Criminal Investigative Service. Back then, it
was just NIS."

```json
{
  "id": "naval-criminal-investigative-service",
  "cls": "institution",
  "label": "Naval Criminal Investigative Service",
  "dateStart": "1994-06-09",
  "desc": "The Department of the Navy's criminal investigative and counterintelligence organisation, known as the Naval Investigative Service and then the Naval Investigative Service Command before it was renamed. The earliest federal record opened for this node is the Navy's final rule of 9 June 1994, which struck 'Commander, Naval Investigative Service Command' from 32 CFR 701.5 and inserted 'Director, Naval Criminal Investigative Service'; a Navy rule published eight days earlier still printed the old title. It is drafted here because Richard Doty places NIS inside the MJ-12 chain of custody the board already holds through Jaime Shandera, describing Shandera as an NIS asset on an unrelated operation when the dead drop arrived. The commonly cited 1992 redesignation date was not established by any record opened from this machine and is deliberately absent from this node.",
  "claims": [
    {
      "tier": 1,
      "text": "The Department of the Navy final rule published on 9 June 1994, FR Doc 94-13966, amended 32 CFR 701.5(e)(2)(iii)(B) by removing 'Commander, Naval Investigative Service Command' and adding in its place 'Director, Naval Criminal Investigative Service'.",
      "source": "Federal Register Doc 94-13966, 'Availability of Department of the Navy Records and Publication of Department of the Navy Documents Affecting the Public', effective 9 June 1994, https://www.federalregister.gov/documents/1994/06/09/94-13966/availability-of-department-of-the-navy-records-and-publication-of-department-of-the-navy-documents"
    },
    {
      "tier": 1,
      "text": "A Department of the Navy document published on 1 June 1994, FR Doc 94-13279, still lists 'Commander, Naval Investigative Service Command' among the officers it designates, so the former title was in current Federal Register use eight days before the substitution.",
      "source": "Federal Register Doc 94-13279, 1 June 1994, https://www.federalregister.gov/documents/1994/06/01/94-13279/"
    },
    {
      "tier": 2,
      "text": "On DEBRIEFED with Chris Ramsay, 21 August 2026, at 1:17:09, Richard Doty said that Jaime Shandera 'was an asset that was being used by the Naval Investigative Service, which is now Naval Criminal Investigative Service. Back then, it was just NIS', placing that relationship on a separate operation roughly two weeks before the MJ-12 document reached Shandera's mailbox.",
      "source": "DEBRIEFED with Chris Ramsay, 'Former Counterintelligence Agent Shares Wild Alien Encounters - Richard Doty', 21 August 2026, 1:17:09, transcript in dist/transcripts/md/"
    },
    {
      "tier": 3,
      "text": "The date of the redesignation from Naval Investigative Service Command to Naval Criminal Investigative Service is an open question on this board. The Secretary of the Navy instruction that would fix it was not reachable: the FAS Navy directives index lists SECNAVINST 5430.107, 'Mission and Functions of the Naval Criminal Investigative Service', dated 28 December 2005 and running 20 pages, but the PDF returns a zero-byte HTTP 202 and ncis.navy.mil returns 403.",
      "source": "FAS Navy Intelligence and Security Doctrine, SECNAVINST index, https://irp.fas.org/doddir/navy/secnavinst/index.html"
    }
  ],
  "sources": [
    "https://www.federalregister.gov/documents/1994/06/09/94-13966/availability-of-department-of-the-navy-records-and-publication-of-department-of-the-navy-documents",
    "https://www.federalregister.gov/documents/full_text/text/1994/06/09/94-13966.txt",
    "https://www.federalregister.gov/documents/1994/06/01/94-13279/",
    "https://irp.fas.org/doddir/navy/secnavinst/index.html"
  ],
  "edges": [
    {
      "to": "us-navy",
      "type": "institutional",
      "note": "NCIS is a Department of the Navy organisation whose head's title is fixed in the Navy's own codified regulations at 32 CFR part 701."
    },
    {
      "to": "jaime-shandera",
      "type": "witness-chain",
      "note": "Richard Doty states that Shandera was an NIS asset on an unrelated operation shortly before the MJ-12 film was dead-dropped, a Tier 2 claim no opened NIS record corroborates."
    },
    {
      "to": "richard-doty",
      "type": "investigative",
      "note": "Doty, a former AFOSI special agent, is the sole source for both NIS episodes recorded here, the Shandera handling and an NCIS role in the Kirtland contractor confrontation."
    }
  ]
}
```

---

## A7. Ronald Pandolfi

**Verdict: NOT OPENED.** No record was reached that states a position of record for Ronald
Pandolfi at CIA, at its Directorate of Science and Technology, or at ODNI. No node is drafted.

**What was tried**

| route | result |
|---|---|
| archive.org full-text search, all collections, "Pandolfi" | 670 items, none federal or intelligence-related; the hits are musicians, an Italian mathematics text and concert recordings |
| archive.org search restricted to `collection:(cia-readingroom)` | 0 results |
| `cia.gov/readingroom/docs/...`, for the FY2020 FOIA case logs PDF that a search engine surfaced against the surname | HTTP 302 to `https://www.cia.gov/readingroom`, the loop the brief records. A FOIA case log entry would in any case record a request, not an office |
| theblackvault.com site search and document-archive search | returned the site shell with no result list |
| web search restricted to govinfo.gov, congress.gov, dni.gov, cia.gov, gao.gov, courtlistener.com, archive.org, theblackvault.com, uspto.gov and patents.google.com | nothing naming him in a federal position |

**Where the record should be.** A CIA or ODNI FOIA response giving position of record, or a
CREST document bearing the surname. The triage row says as much. The CIA reading room is
behind the 302 loop from this machine and its archive.org mirror returns nothing for the name.

**What the transcript actually says, for the next pass.** At 0:29:13 on 17 July 2026 the claim
is hedged twice, by the speaker, in one breath: "it's like the weird desk at the CIA... that
they say, you know, they say, kick green was on it. Then they say, Ron Pandolfi took over." A
second speaker then says of the same desk "that one almost seemed performative to me." The
succession the triage row wants to test is offered as hearsay in the source that carries it,
so even a confirmed position of record would not by itself confirm the succession.

---

## A9. Federal Aviation Administration

**Opened**

| document | URL |
|---|---|
| NARA, "Record Group 615: Unidentified Anomalous Phenomena Records Collection", last reviewed 28 August 2026 | https://www.archives.gov/research/topics/uaps/rg-615 |
| NARA Catalog metadata export for the FAA series, National Archives Identifier 493468575 | https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json |
| NARA, "Bulk Downloads for Records Related to Unidentified Anomalous Phenomena (UAPs)" | https://www.archives.gov/research/catalog/catalog-bulk-downloads/uap-bulk-download |

`catalog.archives.gov/id/493468575` is a single-page application and returns only a
5,454-byte shell to curl; its `api/v1` and `api/v2` endpoints return the same shell without a
key. The catalog's own machine-readable export, linked from the NARA bulk-downloads page,
carries the full series description and was opened instead.

**What the documents are.** NARA's authoritative list of RG 615 contributors, and the
catalog's own description of the FAA series within it.

**What they establish.**

- The RG 615 page, last reviewed 28 August 2026, lists eight contributing agencies, the FAA
  first, at National Archives Identifier 493468575. This confirms the board's existing
  `nara-rg615` claim from that claim's own source.
- The series is titled "Records from the Federal Aviation Administration Relating to
  Unidentified Anomalous Phenomena", level of description "series", under record group 615,
  "Unidentified Anomalous Phenomena Records Collection", NAID 445887258, whose own inclusive
  start date is 23 December 2023.
- Accession numbers TR-0615-2025-0006 and TR-0615-2025-0008. Extent "575 portable document
  files (pdf)". Inclusive start date 1 October 2023; coverage end date 26 October 2024. Held
  by "National Archives at College Park - Electronic Records". Language English.
- Scope note: "This series consists of copies of Government, Government-provided, or
  Government-funded records relating to unidentified anomalous phenomena, technologies of
  unknown origin, and non-human intelligence (or equivalent subjects by any other name with
  the specific and sole exclusion of temporarily non-attributed objects)."
- Access restriction status "Restricted - Partly", specific restriction "UAP Records
  Collection Postponement Code 1843(a)(3)". Use restriction "Unrestricted".
- Creator authority heading: "Department of Transportation. Federal Aviation Administration.
  (04/01/1967 - )", NAID 10480916, establish date 1 April 1967.
- Finding aid note: "The agency provided a metadata list of all files in this series", source
  given as the Federal Aviation Administration.

**One thing the board does not yet carry.** The FAA series is withheld in part under a named
statutory postponement code, 1843(a)(3). The `nara-rg615` node records the FAA as a
contributor and records its bulk-download volume, but not that any of its series is
restricted. That belongs on whichever node is built.

**What the transcript claimed that these do NOT establish.** The map 20 claim, 22 May 2026 at
0:09:40, is Ramsay relaying Jorge Martin: "they actually confirmed deploying multiple F-14s
for testing during that time. So the FAA confirmed this, but then when they went to the
Americans, they denied it." Nothing opened here touches Puerto Rico, F-14s or a denial. The
triage row is right that this claim is not the reason to build the node, and it should sit at
Tier 2 as a claim about what was said, if it is carried at all.

```json
{
  "id": "faa",
  "cls": "institution",
  "label": "Federal Aviation Administration",
  "dateStart": "1967-04-01",
  "desc": "The civil aviation regulator inside the Department of Transportation, and one of the eight agencies that have transferred records into the National Archives' Unidentified Anomalous Phenomena Records Collection under sections 1841 to 1843 of the FY2024 National Defense Authorization Act. Its series, National Archives Identifier 493468575, holds 575 PDF files under two accessions and is listed first on NARA's own RG 615 page. The series is withheld in part under UAP Records Collection Postponement Code 1843(a)(3). This node is a promotion from board prose, where the agency is already named as an RG 615 contributor, rather than a discovery from the podcast corpus.",
  "claims": [
    {
      "tier": 1,
      "text": "NARA's Record Group 615 page, last reviewed 28 August 2026, lists the Federal Aviation Administration first among eight contributing agencies, at National Archives Identifier 493468575.",
      "source": "National Archives, 'Record Group 615: Unidentified Anomalous Phenomena Records Collection', https://www.archives.gov/research/topics/uaps/rg-615"
    },
    {
      "tier": 1,
      "text": "The FAA series is titled 'Records from the Federal Aviation Administration Relating to Unidentified Anomalous Phenomena', carries accession numbers TR-0615-2025-0006 and TR-0615-2025-0008, has an extent of '575 portable document files (pdf)', an inclusive start date of 1 October 2023 and a coverage end date of 26 October 2024, and is held by the National Archives at College Park, Electronic Records.",
      "source": "National Archives Catalog metadata export for NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json"
    },
    {
      "tier": 1,
      "text": "The series carries access restriction status 'Restricted - Partly' with the specific restriction 'UAP Records Collection Postponement Code 1843(a)(3)', and a use restriction of 'Unrestricted'.",
      "source": "National Archives Catalog metadata export for NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json"
    },
    {
      "tier": 1,
      "text": "The catalog's creator authority for the series is 'Department of Transportation. Federal Aviation Administration. (04/01/1967 - )', National Archives Identifier 10480916, with an establish date of 1 April 1967.",
      "source": "National Archives Catalog metadata export for NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json"
    },
    {
      "tier": 1,
      "text": "The series' finding aid note records that 'The agency provided a metadata list of all files in this series', with the source given as the Federal Aviation Administration.",
      "source": "National Archives Catalog metadata export for NAID 493468575, https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json"
    },
    {
      "tier": 2,
      "text": "On DEBRIEFED with Chris Ramsay, 22 May 2026, at 0:09:40, host Chris Ramsay, attributing the account to the Puerto Rican researcher Jorge Martin, said that the FAA confirmed the deployment of multiple F-14s 'for testing' near Cabo Rojo at the time of a December 1988 mass sighting, and that the Americans later denied it. No record opened here bears on that claim.",
      "source": "DEBRIEFED with Chris Ramsay, 'Hidden Alien Photos - Amaury Rivera pt 3', 22 May 2026, 0:09:40, transcript in dist/transcripts/md/"
    }
  ],
  "sources": [
    "https://www.archives.gov/research/topics/uaps/rg-615",
    "https://catalog.archives.gov/medialz/bulk-downloads/uaps/JSON/catalog-export-493468575.json",
    "https://www.archives.gov/research/catalog/catalog-bulk-downloads/uap-bulk-download"
  ],
  "edges": [
    {
      "to": "nara-rg615",
      "type": "custody",
      "note": "The FAA's transferred UAP records sit in Record Group 615 as series NAID 493468575, one of eight agency series NARA lists in the collection."
    },
    {
      "to": "national-archives",
      "type": "institutional",
      "note": "NARA holds and describes the FAA series at the National Archives at College Park, Electronic Records, and publishes its metadata export."
    }
  ]
}
```

---

## Access notes, for the next verifier

| host | behaviour observed 2 September 2026 |
|---|---|
| `sec.gov` EDGAR | answers curl with a user agent and a contact address; `browse-edgar` with `output=atom` is the fastest route to a CIK and a filing list |
| `bnl.gov` | answers curl normally. Not on the brief's reach list, but it opened |
| `api.usaspending.gov` | answers POST to `/api/v2/search/spending_by_award/` without a key |
| `uscode.house.gov` | answers, and serves source credits and statutory notes in the same page. The equivalent `govinfo.gov/content/pkg/USCODE-...` path returned Page Not Found for the same section |
| `api.govinfo.gov` | OVER_RATE_LIMIT on every call this session, including the collections listing, with `DEMO_KEY`. The `wssearch` web endpoint rejected the payload |
| `federalregister.gov` API | answers. Full-text search reaches back to 1 January 1994 only, which is why the 1992 question could not be closed there |
| `catalog.archives.gov` | single-page application. `/id/NNN`, `/api/v1/` and `/api/v2/` all return the same 5,454-byte shell. Use the bulk metadata exports linked from `archives.gov` |
| `archives.gov` | answers, but `/research/uap` is a 404; the live path is `/research/topics/uaps/` |
| `irp.fas.org` | HTML answers, PDFs return HTTP 202 with a zero-byte body |
| `gao.gov`, `ncis.navy.mil`, `secnav.navy.mil/doni` PDFs, `cia.gov/readingroom` | 403, 403, Imperva interstitial, 302 loop |
