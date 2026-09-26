# Blind critic, phase 8 round 2

Judged 39 screenshots: 13 surfaces (home, node, person, map, hood, timeline, evidence, thread, patent, report, library, source, topic) at 1920, 1366 and 375. Note: `*-node.png` and `*-person.png` show the same page (David Charles Grusch) at every width, so no non-person node page was seen this round.

## 1. The same source is a Library link in one claim and plain text in the next, so a source page's "every claim" list is incomplete

- **Screenshots:** 1366-topic.png, 1920-topic.png, 1920-evidence.png, 1920-source.png
- **What is wrong:** On the Roswell topic, claim 1 links "RAAF Press Release, 8 July 1947" to its Library page, but claim 7 cites "source: RAAF press release, 8 July 1947" as unlinked grey text. Claim 4 cites "The Roswell Report: Case Closed (1997)" as plain text while claim 3 links "The Roswell Reports (USAF, 1994-1997)". The evidence table does the same ("source: AARO FY2025 Consolidated Annual Report; Kosloski media roundtable" unlinked, while other AARO reports are linked). Linked labels also repeat the year: "(1980) (1980)", "(1995) (1995)".
- **Why a reader cares:** The Library and source page promise "its own page listing every claim and link that rests on it". A reader who opens the RAAF press release page, or reads "cited by 122 claims" on the AARO report, is getting an undercount and has no way to tell. The new feature says it is complete when the page next to it shows that it is not.
- **Severity:** major

## 2. The source page shows the board's internal editing notes and raw URLs as if they were citations

- **Screenshots:** 1920-source.png, 1366-source.png
- **What is wrong:** Under the one T2 claim on the AARO Volume I page, the "as cited" line reads "...HRRV1-08-MAR-2024-FINAL.PDF", then a long dash, then "DEMOTED from Tier 1 (sourced to an interested party (AARO/DoD) asserting an external fact; primary record of the statement, not of the fact); needs primary replacement". Several other "as cited" lines are bare, unlinked media.defense.gov PDF paths, while the one link that should open the report sits separately under "where to read it".
- **Why a reader cares:** A to-do note ("needs primary replacement") on a public page reads as unfinished work, and it contradicts the grading shown beside it: the tier badge says T2 while the note argues about a T1. A journalist quoting the page cannot tell which parts are the board's finding and which are its workbench.
- **Severity:** major

## 3. Duplicate records inflate the counts

- **Screenshots:** 375-timeline.png, 1920-timeline.png, 1920-source.png, 1366-source.png
- **What is wrong:** The timeline carries "To The Stars Academy formed" and "To The Stars Academy launches", both 2017-10-11, and "NYT reveals AATIP" and "New York Times breaks AATIP", both 2017-12-16, as separate events (visible side by side on the phone list and in the 1920 Program lane). On the AARO source page, "Volume I states that Volume II will cover interviews and research conducted between 1 November 2023 and 15 April 2024 plus additional unresolved allegations" appears twice in a row, once with "from Volume I" added, and a third claim on the same card says the same thing again in different words.
- **Why a reader cares:** The headline numbers ("1,076 events", "6,060 claims", "cited by 122 claims") are the board's credentials. A checker who finds two copies of one event in the first screenful will stop trusting every count on the home page.
- **Severity:** major

## 4. Library metadata is missing where the answer is on the same line

- **Screenshots:** 1920-library.png, 1366-library.png, 375-library.png
- **What is wrong:** "DIA letter to Steven Aftergood listing 38 AATIP reference products (16 January 2019)" is tagged "issuer not recorded", though its own title names the issuer. "Special Access Program (SAP) Policy (DoDD 5205.07)" is "undated". The Era facet puts 1,379 of 1,899 sources (73%) under "no date" and the Issuer facet puts 401 under "issuer not recorded", so the two facets a researcher would use first mostly return the unsorted bucket.
- **Why a reader cares:** The Library is meant to let an informed reader browse by who said it and when. When a DIA letter is not filed under DIA, filtering by issuer silently leaves out records the reader is looking for, and the facet counts next to each issuer are wrong in a way nobody can see.
- **Severity:** major

## 5. At 1366 the program map and timeline turn into unnamed marks

- **Screenshots:** 1366-map.png, 1366-timeline.png, 1920-timeline.png
- **What is wrong:** At 1366 the map header says "0 links · too narrow to name every node". Most cells show one to four names plus "+4", "+8" or "+1" chips, and some cells hold nothing but a chip: Disclosure through 1969 is just "+4", and several 2000-2016 and no-date cells are a bare "+1" or "+2". On the timeline at both laptop widths, the 2017-2026 era shows about a dozen names per lane above several hundred coloured squares with no label.
- **Why a reader cares:** 1366 is one of the two laptop widths this board is read at. There the map, the board's signature view, draws no connections and hides most of its nodes behind counters, which breaks both "nothing is drawn without a name" and "every connection says why it exists". The timeline's dots cannot be read without clicking year by year.
- **Severity:** major

Smaller items seen: the evidence explorer's Source Domain list clips its last row mid-line ("cdn.centerforinquiry.org 67") at 1920; the 1920 node page wraps "3 at Tier / 3" across two lines; start-here card 5 on home says "Size here means implicated", which is out of date against the no-size rule; on the phone source page, "CLAIMS CITING IT · 122" and "group by" each break across two lines; thread step 1 dates Harry Reid to 2009 while its text describes the July 2008 appropriation.

**What works best:** the node page puts "The case against" in its own column right beside the claims, with each conflict and each unverified point stated in full, so the counter-case cannot be missed.
