# Blind critic, phase 7, round 1

Read: `tools/critic/BRIEF.md` and the 30 screenshots in `dist/critic/p7-round-1/` (10 surfaces at 1920, 1366
and 375). Nothing else was opened. `*-node.png` and `*-person.png` are the same page (David Charles Grusch)
at every width.

## The five worst problems, worst first

### 1. Sworn testimony carries a "T1" badge, and one fact is graded two ways on the same page

- **Screenshots:** 1920-node.png, 1920-person.png, 1366-node.png, 1920-report.png, 1366-report.png,
  375-report.png, 1920-evidence.png
- **What is wrong:** The home page defines Tier 2 as "a named person on the record", but on the Grusch page
  his own sworn statements to Garcia, Mace, Moskowitz, Burchett and Luna are each badged **T1**, with only a
  small "said on the record" chip. AARO's statements in the evidence explorer are also T1, with a "the
  office's own account" chip. On the same 1920 page, the claim "served as NRO representative to the UAP Task
  Force 2019-2021" is T1 in the claims column, while the connection "held a post at UAPTF / NRO
  representative to the UAP Task Force, 2019-2021" in the right column is **T2**. The report repeats the T1
  badges on paper, where the chip is easy to miss.
- **Why a reader cares:** The tier is the board's whole promise. A reader who scans the T column (and "16 at
  Tier 1" in the header) takes the sworn claims as documented fact. The two-line legend that redefines T1
  "here" asks the reader to hold two meanings of the same badge at once. A checker who finds one fact at two
  tiers on one screen stops trusting every other grade.
- **Severity:** major (close to blocker for the stated audience)

### 2. At 1366 the program map draws no links and shows anonymous "+N" marks

- **Screenshots:** 1366-map.png (compare 1920-map.png)
- **What is wrong:** The header reads "0 links · too narrow to name every node, so each cell shows its
  count". Many cells end in bare chips such as "+4", "+6", "+8" and "+1". The Disclosure 1969 cell, the
  Reverse-engineering No-date cell and the Disclosure 2000-2016 and 2017-2026 cells show *only* a "+N" chip
  and no name at all. The "LINES AT REST" button is lit even though nothing is drawn.
- **Why a reader cares:** 1366 is one of the two laptop widths the readers use. At that width the board's
  main view breaks two of its own rules at once: nothing drawn without a name, and every connection explains
  itself. The map becomes a table of counts, and the lit toggle suggests the lines failed to load.
- **Severity:** major

### 3. The case against sits in its own column, not beside the claim it answers

- **Screenshots:** 1920-node.png, 1366-node.png, 375-node.png, 1920-report.png
- **What is wrong:** On the Grusch page the four "Conflict on the record" and nine "Not verified" entries are
  a separate middle column (a right column at 1366), with nothing tying each one to its claim. The AARO
  conflict about "over 40 witnesses" is first in that column, but the matching sworn claim ("interviewing
  over 40 witnesses") is the seventh item in the claims list, about 500px lower and in another column. On a
  phone the whole case against comes as one block *before* any claim. The visible part of the report shows
  claims only.
- **Why a reader cares:** The owner's rule is that the case against sits beside the claim. As built, the
  reader has to pair the rebuttals with the claims by hand, and in the printed brief may never see a
  rebuttal at all.
- **Severity:** major

### 4. Most neighbourhood spokes carry a tier but no words saying why

- **Screenshots:** 1920-hood.png, 1366-hood.png
- **What is wrong:** Around Grusch, most named neighbours show only a name and a tier, for example "Garry
  Nolan T1", "Karl E. Nell T2", "Mark A. Milley T2", "Judicial Watch T2", "The Hill T2" and "Susan Gough
  T1". The few that carry a word use board jargon ("other links", "the board's reading", "conduct"). At
  1920 about 70 two-step names down both edges each say only "two steps", with no "via whom". At 1366 the
  header text is cut off mid-word ("off at this width · share(").
- **Why a reader cares:** "Every connection says in words why it exists" fails on the one surface built to
  show connections. A reader cannot tell whether Milley is a witness, a denier or just someone mentioned
  without going to the node page, where the connections list does give the reason.
- **Severity:** major

### 5. On desktop, timeline labels give no dates and the axis runs to a highlighted 2029

- **Screenshots:** 1920-timeline.png, 1366-timeline.png (compare 375-timeline.png)
- **What is wrong:** In the open 2017-2026 era, event labels are stacked in rows with no date on them. The
  only way to date an event is to judge where its small left tick falls against year ticks about 120px
  apart. The phone version prints the full date beside every event. The year axis ends in an orange
  **2029**, past the era's stated end of 2026, and in a colour nothing else on the axis uses. One strand is
  named "COVER-UP", a conclusion label on a board that otherwise grades claims rather than asserting them.
- **Why a reader cares:** A timeline a reader cannot read dates off is a list with extra steps. The 2029
  tick looks like a data error (an event dated in the future) and invites doubt about everything else. The
  strand name tells a sceptical reader the verdict before the evidence.
- **Severity:** major

## The single thing that works best

The node page's "Sourced connections" column (1920-node.png, and 375-hood.png on a phone) states every link
as a plain sentence with its role, dates, tier and a source count, for example "held a post at National
Geospatial-Intelligence Agency · GS-15 Senior GEOINT Capabilities Requirements Officer · 2021-2023 · T1 · 2
sources", which is exactly the promise the rest of the board should keep.
