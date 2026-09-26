# Blind critic, phase 11, round 2

26 September 2026. Read only the brief and the 36 screenshots in `dist/critic/p11-round-2/`. The captures are single viewports, so anything below the fold was not judged. `*-node.png` and `*-person.png` are identical captures of the same person page.

## The five worst problems

### 1. Places grid: you cannot tell which dot a label belongs to (major, close to a blocker for the grid)

**Files:** `1920-places.png`, `1366-places.png`

**What is wrong:** Every leader line runs flat across the plot from its dot to the plot edge, then bends to its label. At the edges about 16 lines on each side squeeze into a band roughly 60px tall and become one grey bundle. The flat stretches overlap one another and pass straight through other dots. Around 35 N, several western leaders sit on top of each other. Boulder, Los Alamos and Colorado Springs are labelled on the east side, so their leaders cross most of the map. On the outside-US grid, the leader for "London, United Kingdom" (left) and the one for "Ministry of Defence Main Building, Whitehall, London" (right) join into one continuous line through the same cluster. That cluster also holds the "United Kingdom" dot. At 1920 the western labels run about 220px below the bottom of the plot, which makes those leaders long diagonals.

**Why a reader cares:** The only point of the grid is to show where each place is, and a reader cannot trace a single line from label to dot with confidence. It breaks the "nothing overlaps" rule. The list on the right is the only usable part of the page, and at 375 the list is all there is.

### 2. Patent drawing captions do not match the drawings (major)

**Files:** `1920-patent.png`, `1366-patent.png`

**What is wrong:** The sheet captioned "US 10,135,366 · FIG 1 · sheet 1 of 3" is a page of text (it looks like a references page), not a figure. The sheet captioned "FIG 2" actually shows FIG-1 and FIG-2, and the one captioned "FIG 3" shows FIG-3 and FIG-4. "US 10,322,827 · FIG 1 · sheet 1 of 3" is also a text page. The header says "3 of them are this filing's", but nothing marks which three.

**Why a reader cares:** The board's promise is that nothing on it is invented. A caption that the picture above it visibly contradicts is the quickest way to lose that trust, and patent readers compare figure numbers.

### 3. "T1" sits in front of sworn allegations, against the home page's own key (major)

**Files:** `1920-report.png`, `1366-report.png`, `1920-node.png`, `1920-home.png`, `1920-evidence.png`

**What is wrong:** The home key says T2 is "testimony, an allegation". The report and the node page, however, print "T1" in front of sworn statements such as "biologics came with some of these recoveries" and "Nonhuman". A small amber "said on the record" box sits after the T1. It is the same amber as Tier 2 and as the "not verified" cards. The badges are also applied inconsistently. In the evidence explorer, "AARO held 1,870 total UAP reports", sourced to the AARO director's roundtable, carries "said on the record". The AARO claims on either side of it carry "the office's own account".

**Why a reader cares:** A reader who skims, or quotes a single line, will take the most extraordinary claims on the board as Tier 1 documented facts. That is the exact misreading the grading exists to prevent, and a critic of the board would seize on it.

### 4. Neighbourhood link wording is sometimes wrong or empty (major)

**Files:** `1920-hood.png`, `1366-hood.png`, `1920-hood2.png`, `1366-hood2.png`

**What is wrong:**

- **Verbs that cannot be true:**
  - Grusch "was refused by" the New York Times article "Glowing Auras and Black Money". An article cannot refuse a person.
  - AARO "succeeded" the "ODNI Preliminary Assessment" of 25 June 2021. An office cannot succeed a report.
  - Grusch "received a request from, linked through oversight to" Jay Stratton. Two phrases are run together and say nothing clear.
- **Generic lines whose sub-line explains the target, not the link:**
  - "linked through a denial to DoD SAPCO" is followed by a description of what SAPCO does. It never says who denied what.
  - "linked organisationally to GREMLIN" has the same problem.
- **Cryptic tags nobody explains:** "also conduct", "also the board's reading", "also organisation".

**Why a reader cares:** "Every link says why it exists" is the page's whole promise, and these rows break it on the two showcase nodes. A reader checking the Grusch page will stop trusting the relationship words as soon as one of them is plainly wrong.

### 5. Node page and neighbourhood give different counts for the same person (minor)

**Files:** `1920-node.png` against `1920-hood.png`, also `1366-hood.png`

**What is wrong:** For David Charles Grusch, the node page's connections column shows "Roles · 9", "Oversight · 12" and "78 links · 66 counterparts". One click away, the neighbourhood shows "Roles · 8" and "Oversight · 9". The neighbourhood's intro says "each named once", but neither family header says whether it counts links or people.

**Why a reader cares:** These readers come to check, and two numbers for one family make them wonder which is right, or whether something was dropped.

## What works best

The case against on the node page (`1920-node.png`, `1366-node.png`). Red "conflict on the record" and amber "not verified" cards sit in their own column right beside the claims, each stating the counter-record in plain words. On a phone (`375-node.png`) they come straight after the analysis, not at the end.

## Disposition (the phase 11 session)

| # | Finding | In scope? | What was done |
|---|---|---|---|
| 1 | Places grid: leaders bundle at the edges, run through dots, cannot be traced | yes | The side columns are gone. Each name sits beside its own marker, or a short way off with a leader, at the free spot that is nearest and whose leader crosses no other name; names never overlap a name, a marker or a grid label. Below 2200 wide the grid takes the page's width and the list follows it |
| 2 | Patent drawing captions do not match the sheets | no | Patents are an earlier phase's surface; recorded for phase R / 12 |
| 3 | T1 before sworn allegations, against Home's key | no | Phase 10's wording fix; no tier moves on presentation |
| 4 | Neighbourhood wording: impossible predicates, two phrases run together, "also conduct" unexplained, sentences that describe the target | partly | Presentation fixed: where a predicate is shown the family's phrase is no longer run after it; "also" now reads "also linked through conduct" with an explanation on hover. Not fixed here: the predicates themselves ("was refused by" an article, AARO "succeeded" a report) and the authored sentences are data, recorded for phase R |
| 5 | Node page and neighbourhood counts differ for one family | yes | Each column now says "8 neighbours": the neighbourhood counts people and things, the node page counts links |
