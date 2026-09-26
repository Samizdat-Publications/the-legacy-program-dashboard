# Blind critic, phase 9, round 3

Read: `tools/critic/BRIEF.md` and the 39 PNGs in `dist/critic/p9-round-3/` (13 surfaces at 1920, 1366 and 375). Nothing else was opened.

Ambiguity noted first: `*-node.png` and `*-person.png` are pixel-identical at every width (both are David Charles Grusch), so no non-person node page was seen this round. Every screenshot is one viewport, so lower parts of long pages (the timeline's later lanes, the rest of the directories) are unseen.

## The five worst problems, worst first

### 1. The timeline's open era hides most of its events behind "+N", and its lanes and axis mislead
- **Files:** `1920-timeline.png`, `1366-timeline.png`, `375-timeline.png`
- **What is wrong:** With 2017-2026 open at 1920, the "Official study programmes" lane names about 37 chips and hides the rest behind +9, +3, +6, +14, +19, +7 and +47: 105 of its 142 open-era events, about 74%. "The custody allegations" hides 50 of 73 (+3 +2 +10 +15 +2 +18). The +N counts sit in a row under the lane and do not say which year they belong to. Lanes are named with dates ("The early record, 1944-1969") but hold chips dated 2026 ("State of the record, August 2026"). The axis runs 2017 to 2026 a year apart, then puts "2029" in the space of about one year, with no break mark at 1920. Chip position depends on which side the colour bar is on, which is explained only in a dense header line. The chip colours have no legend. On the phone (375), the header still explains chips, bar sides and +N counts, none of which the phone list shows.
- **Why a reader cares:** Opening the busiest era should show the most. Instead the reader sees a quarter of it and has to click numbered stubs to find the rest. A lane named 1944-1969 that is full of 2026 entries, and an axis that squeezes three years into one, make the reader doubt the dates, and the dates are the point of a timeline.
- **Severity:** major

### 2. At 1366, a main laptop width, the program map draws no links and hides most of its nodes
- **Files:** `1366-map.png` (compare `1920-map.png`)
- **What is wrong:** The header reads "135 nodes · 0 links · too narrow to name every node, so each cell shows its count". Cells show two to four names and a "+N" stub: Custody through 1969 shows 4 of 12, Research 2017-2026 shows 3 of 10, Disclosure through 1969 shows only "+4". At 1920 the same map names every node and draws 118 of 413 links. Even there the lines bunch into long parallel runs down the column edges and are hard to follow from one chip to another.
- **Why a reader cares:** The brief puts laptop readers at 1366 or 1920. At 1366 the map turns into a grid of counts with no connections, which leaves out what the map exists to show. The reader has to expand cell after cell to learn what is there.
- **Severity:** major

### 3. The neighbourhood's connection labels often do not say why the link exists
- **Files:** `1920-hood.png`, `1366-hood.png`
- **What is wrong:** Many ring labels name only a category, not a reason: "IAA FY2024 Sec. 1102 **link** T3", "Booz Allen Hamilton **conduct link** T3", "The Boeing Company **place or time link** T3", "Burlison to MITRE **document link** T3", "Capitol UAP Disclosure Press Conference **media link** T2". At 1920 the roughly 75 names in the two outer columns all say only "two steps". Some of those names read like category placeholders rather than records: "Public", "Enacted Statute", "Funding Channels", "Chain of custody". The page does not say who each second step goes through.
- **Why a reader cares:** The board promises that every connection says in words why it exists. "Link T3" or "two steps" tells a reader checking the Grusch-Boeing connection nothing they can test. Names like "Public" make the reader wonder whether these nodes are real.
- **Severity:** major

### 4. The People directory is sorted by a date whose meaning changes from row to row, and documents have no directory
- **Files:** `1920-people.png`, `1366-people.png`, `375-people.png`, `1920-orgs.png`, `1920-events.png`
- **What is wrong:** The default sort is a DATE column. The page admits the date marks different things ("a post, an appearance, the event that brought them here"), and the table never says which one a row carries. Harry S. Truman and Sidney Souers both read 1946-01-22 with nothing to say what happened then. The Under Oath column prints "not stated" while the filter for the same thing calls it "unknown 325". The directory tabs cover 351 + 191 + 78 + 60 + 76 + 93 = 849 nodes, against the home page's 1,138, and there is no tab for documents.
- **Why a reader cares:** A reader who sorts or scans by date will compare dates that do not measure the same thing, and draw wrong conclusions about order. A reader looking for a report or memo, one of the board's most-cited node types, has no directory to find it in.
- **Severity:** major

### 5. The evidence explorer has cryptic columns and broken filter chips
- **Files:** `1920-evidence.png`, `1366-evidence.png`
- **What is wrong:** The NODE DENIED column shows "on the node" with no further meaning. The FOIA column shows strings like "F8 · OSD · not filed / F11 · OSD / AARO · not filed / closes ▾" with no key on the screen. At 1366 the source-domain chip breaks mid-word ("documents2.theblackvau / lt.com"). At 1920 the source-domain box clips a chip at its bottom edge.
- **Why a reader cares:** This is the page where a sceptical reader checks claims. Columns they cannot decode slow them down and read as internal bookkeeping. Broken chips go against the owner's own rule that nothing is clipped.
- **Severity:** minor

## What works best

The node page puts "The case against" (4 conflicts and 9 not-verified items) right beside the claims and the sourced connections. Each connection carries its own sentence, dates, tier and source count, so the case for and against can be read side by side.
