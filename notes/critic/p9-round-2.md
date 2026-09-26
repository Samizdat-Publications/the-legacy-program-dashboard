# Blind critic, phase 9, round 2

Read: `tools/critic/BRIEF.md` and the 39 screenshots in `dist/critic/p9-round-2/` (13 surfaces at 375, 1366 and 1920: home, node, person, hood, map, timeline, evidence, thread, patent, report, people, orgs, events). Nothing else was opened.

## The five worst problems, worst first

### 1. Timeline: a chip's left edge is not its date, nothing says so, and the busiest years are mostly unnamed

- **Files:** `1366-timeline.png`, `1920-timeline.png`
- **What is wrong:** Some chips carry their coloured rule on the right and end at their date, others carry it on the left and start there, and the two are mixed in one lane with no legend. The header explains counts and amber but not the rule side. In the early-record lane at 1366, "Special Report No. 14 republished in PURSUE Release 03" starts over 2021 but belongs to 2026. At 1366 the densest recent years become counts: in the custody lane, 13 events are named and 58 sit behind "+1 +4 +4 +11 +16 +4 +18", and 2024 to 2026 are almost entirely counts. The axis also jumps from 2026 to an amber "2029" in the space of one year, with no 2027 or 2028 and no break mark, and the amber event the header promises is not visible in either capture.
- **Why a reader cares:** Most readers put a chip's date at its left edge, so they will date events years wrong. The years readers come to check (2023 to 2026) are the ones hidden behind numbers, and the squeezed axis makes the scale look wrong.
- **Severity:** major

### 2. The Events directory says 93 events while the rest of the board says 1,076

- **Files:** `1366-events.png`, `1920-events.png`, `375-events.png`, `1366-home.png`, `1366-timeline.png`
- **What is wrong:** The directory tab reads "EVENTS 93" and "93 of 93 events". The home panel says "1,076 timeline events" and the timeline header says "1076 events". Nothing on the directory page explains the gap, for example that it lists event nodes and not dated happenings on other nodes.
- **Why a reader cares:** A reader checking coverage sees one count ten times the other and has to guess which one is the board. Anyone looking for an event they saw on the timeline (for example "Grusch joins UAPTF") will not find it in a directory called "every event".
- **Severity:** major

### 3. Directory columns a reader cannot interpret: DATE, era and vital status

- **Files:** `1366-people.png`, `1920-people.png`, `1366-orgs.png`, `1920-orgs.png`, `1366-person.png`
- **What is wrong:** People are sorted by a "DATE" that means a different thing on each row. Truman's is 1946-01-22, Kevin Randle's (1949-06-04) looks like a birth date, and Grusch's page header shows "PERSON · 2023-07-26", a hearing date. Every row repeats a grey "era THROUGH 1969", including the House of Representatives (1789) and Randle, a researcher active long after 1969. Sidney Souers and Gordon Gray read "vital status unknown", and 123 people are "unknown", although informed readers know these men died decades ago. Some "primary topic" cells are hard to account for, for example the Office of Naval Intelligence under "FFRDCs and the 2026 contractor probes".
- **Why a reader cares:** The default sort runs on a column whose meaning the reader cannot work out. "Unknown" on well-known deceased officials reads as ignorance, not caution. Informed readers will stop trusting the directory's other cells.
- **Severity:** major

### 4. The neighbourhood ring names many links only by their kind, not by why they exist

- **Files:** `1366-hood.png`, `1920-hood.png`
- **What is wrong:** About a third of the ring's labels are generic: "IAA FY2024 Sec. 1102 link T3", "Booz Allen Hamilton conduct link T3", "The Boeing Company place or time link T3", "Waived SAP Notification Group testimony link T3", "Luis D. Elizondo board inference link T1", "David C. Grusch v. Michael Chapman et al. document link T1", "Capitol UAP Disclosure Press Conference media link T2". Only "questioned", "denied", "had in a post" and "appointed" actually say what happened. At 1920 with two hops, about 75 outer names each carry the same suffix "two steps", which says nothing.
- **Why a reader cares:** The board promises that every connection says in words why it exists, and this view breaks that promise. "link" and "board inference link" tell the reader nothing about why Boeing or a statute sits next to Grusch.
- **Severity:** major

### 5. The program map at 1366 is mostly counts, with no links drawn

- **Files:** `1366-map.png` (compare `1920-map.png`)
- **What is wrong:** At 1366 the header reads "0 links · too narrow to name every node, so each cell shows its count". Most cells show one or two names and then "+3", "+4", "+8". The Disclosure row, for example, is "+4", "YANKEE BLUE", "+2", "+1". At 1920 the same map names all 135 nodes and draws 118 links.
- **Why a reader cares:** 1366 is one of the two laptop widths readers use, and at that width the board's main picture turns into a grid of numbers with no connections. The reader has to click cell after cell to see what the map is meant to show at a glance.
- **Severity:** major

## What works best

The node page (`1920-node.png`, `1366-node.png`) puts the case against in its own column right beside the claims: four labelled conflicts and nine "not verified" items, and a "said on the record" box on every sworn claim, so the reader never mistakes testimony for a finding.
