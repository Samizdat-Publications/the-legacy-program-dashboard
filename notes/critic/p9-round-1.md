# Blind critic, phase 9, round 1

Read: tools/critic/BRIEF.md and the 39 PNGs in dist/critic/p9-round-1/ (13 surfaces at 1920, 1366 and 375). Nothing else.

## The five worst problems, worst first

### 1. Timeline: counts stand in for names where there is room, and the year axis runs past the data

- **Files:** 1920-timeline.png, 1366-timeline.png, 375-timeline.png
- **What is wrong:** In the open 2017-2026 era, the lane "The early record, 1944-1969" is empty except for a bare "+4" at 2026. The phone view shows those four events by name ("Special Report No. 14 republished...", "1949 Los Alamos green fireballs records publicised", and two more), and the desktop lane has a whole empty row where they would fit. Every other lane ends in a row of "+N" chips: "+48" and "+21" (Official study programmes), "+28" and "+25" (Congress), "+18" and "+16" (custody). So a large share of the era is a count, not a name. The year axis ends in an orange "2029" after 2026, with nothing under it.
- **Why a reader cares:** The owner's rule is that nothing is drawn without a name. Here the reader sees a count in an empty lane and has to click to learn what it is. "2029" on a board that runs "1944 to now" looks like a future-dated event or a broken axis.
- **Severity:** major

### 2. Directories: the era tag reads as an end date, and long date ranges go unexplained

- **Files:** 1920-people.png, 1920-events.png, 1920-orgs.png, 1366-people.png, 1366-events.png, 1366-orgs.png, 375-people.png, 375-events.png, 375-orgs.png
- **What is wrong:** The DATES column prints the era straight after the date in the same line: "1946-01-22 · THROUGH 1969" (Truman), "1789-03-04 · THROUGH 1969" (House of Representatives), "1947-06-14 - 1947-07-09 · THROUGH 1969" (Roswell). It reads as a span ending in 1969. Some real ranges are also implausibly long and nothing says what the end date marks: "1977-11-18 - 2026-09-07" (Ellsworth AFB claim), "1953-11-19 - 2013-07-17" (Olson death), "1953 - 1980-09-02" (Kingman), "1947-07 - 1992" (San Agustin).
- **Why a reader cares:** Checking dates is the main reason to open a sortable directory. A reader will take "through 1969" as a fact about the person, or take a 49-year span as the length of the event.
- **Severity:** major

### 3. Program map at 1366: no links at all, and cells made of bare counts

- **Files:** 1366-map.png (compare 1920-map.png)
- **What is wrong:** At 1366 the header says "0 links · too narrow to name every node". The map draws no connections, and several cells are only a count: Disclosure/through 1969 is just "+4", Oversight/no date "+1", Reverse engineering/no date "+1", Retrieval/2017-2026 "IAA FY2024 Sec. 1102 +1". The gold-bordered chips carry a number too ("Operação Prato 14", "GEIPAN 13", "UAP Disclosure Act of 2023 12"). Those are start-here tour steps, but they sit beside "+4"-style count chips and look like counts.
- **Why a reader cares:** 1366 is the most common laptop width. At that width the board's central view shows no relationships, and it breaks the "no anonymous marks" rule. A reader cannot tell which number is a tour step and which is a count.
- **Severity:** major

### 4. Neighbourhood, two-steps ring: about 75 names that say only "two steps"

- **Files:** 1920-hood.png
- **What is wrong:** The outer columns list 75 names (Harry S. Truman, Marco Rubio, Chain of custody, Washington, D.C., Enigma Labs...). Each one carries the same words "two steps", joined by a dotted line so faint it is close to invisible. No name says through whom, or why. The footer adds "283 more two steps away". The inner ring, by contrast, gives every name a reason ("refused T2", "had a post T1").
- **Why a reader cares:** "Every connection says in words why it exists" fails for the largest group of names on the screen. A reader who sees Truman two steps from Grusch cannot check the path without clicking.
- **Severity:** major

### 5. Phone directories: broken character in every person card, and unlabelled claim counts

- **Files:** 375-people.png (compare 375-events.png, 375-orgs.png)
- **What is wrong:** Every person card's status line prints a literal "�b7" where a separator should be: "dead �b7 former role", "vital status unknown �b7 former role". The same cards print "claims: 5 · 0 · 0" with no T1/T2/T3 key on the phone layout.
- **Why a reader cares:** Raw encoding garbage on every card is the fastest way to make a board that promises care look unfinished. The unlabelled triple is a puzzle on first sight.
- **Severity:** minor (noticeable on every card; does not mislead)

## What works best

The node page puts the case against beside the claims: the conflicts and not-verified items for Grusch sit in their own column next to his claims at 1920 and 1366, and directly under the analysis on the phone (1920-node.png, 1366-node.png, 375-node.png).
