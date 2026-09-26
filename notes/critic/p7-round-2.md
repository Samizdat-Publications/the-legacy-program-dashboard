# Blind critic, phase 7 round 2

Judged from the 30 screenshots in `dist/critic/p7-round-2/` only. Note first: `*-node.png` and
`*-person.png` are pixel-identical at all three widths (both are David Charles Grusch), so no non-person
node page (institution, document, programme, event) was shown. Nothing below covers one.

## The five worst problems, worst first

### 1. The node page's case against is a separate pile, and the claims it sits beside are padded

- **Screenshots:** 1920-node.png, 1920-person.png, 1366-node.png, 375-node.png, 1920-report.png
- **What is wrong:** "The case against" is its own column (1920, 1366) or a block placed above the claims
  (375). None of its 4 conflicts or 9 not-verified items points at the claim it answers, so the reader has
  to match them by hand. The claims list headed "32 in all, 16 at Tier 1" also includes two T1 items that
  only quote the UAPDA's definitions of "legacy program" and "controlling authority" (S. 2226, Sec.
  9003). They say nothing about Grusch. And one "not verified" entry is sourcing housekeeping, not a
  counter-argument: "The direct NewsNation URL for the 9 June 2026 report (cited here via the Wikipedia
  footnote)".
- **Why a reader cares:** The rule is that the case against sits beside the claim. Here it sits beside
  the page instead. Statute text counted as Tier 1 claims about a person inflates his documented score.
  An informed reader checking Grusch will spot both at once, and will read the Wikipedia admission as the
  board citing Wikipedia.
- **Severity:** major

### 2. The program map at 1366 draws no links and hides names behind anonymous "+N" boxes

- **Screenshots:** 1366-map.png (also 1920-map.png)
- **What is wrong:** At 1366 the header reads "0 links" while LINES AT REST is lit. Many cells collapse
  into dashed "+4", "+1" and "+8" boxes with no names. Disclosure through 1969 is only "+4", and the NO
  DATE cells for reverse engineering and oversight are only "+1". START HERE is on, yet most of the
  numbered start-here nodes (MITRE 6, Carve-Out 7, Immaculate Constellation 9, KONA BLUE 10, Wilson-Davis
  11, AARO 5, Waived SAP group 2, AARO Historical Record 4) are hidden inside those boxes. At 1920 the
  links are drawn, but they run as bundled parallel verticals in the column gutters. One runs down the
  far right page edge (from "38 Defense Intelligence Ref. Docs" at the top to Research), so a line cannot
  be traced from end to end.
- **Why a reader cares:** 1366 is a main laptop width. There the map is a table of counts: it breaks
  "nothing is drawn without a name", and its own start-here highlighting points at things it does not
  show. At 1920 the lines are there but cannot be read.
- **Severity:** major

### 3. The patent drawing captions do not match the drawings

- **Screenshots:** 1920-patent.png, 1366-patent.png
- **What is wrong:** In the drawing-sheet grid, "US 10,135,366 · FIG 1 · sheet 1 of 3" and "US
  10,322,827 · FIG 1 · sheet 1 of 3" show pages of printed text, not a figure. The next tiles, captioned
  "FIG 2" and "FIG 3", show the drawings marked FIG-1/FIG-2 and FIG-3/FIG-4. The same offset repeats for
  10,322,827 ("FIG 2" shows FIG-1; "FIG 3" shows FIG-2 and FIG-3). The patent selected on the left
  (10,135,366) is not first in the grid either: the grid opens on 10,144,532.
- **Why a reader cares:** The page says the figures are rendered "with full provenance". On a board whose
  promise is that nothing is invented, a caption that names the wrong figure is a sourcing error the
  reader can see.
- **Severity:** major

### 4. The timeline axis runs past its own era, and some events appear twice

- **Screenshots:** 1920-timeline.png, 1366-timeline.png, 375-timeline.png
- **What is wrong:** The open era is headed "2017-2026", but its year axis ends with an orange italic
  "2029". That label sits one year-step after 2026, and event dots run past the 2026 tick to reach it.
  Separately, the same event appears twice under two wordings on the same date: "To The Stars Academy
  formed" and "To The Stars Academy launches" (both 2017-10-11), and "NYT reveals AATIP" and "New York
  Times breaks AATIP" (both 2017-12-16). This is plain in the phone list and also visible at 1920.
- **Why a reader cares:** A mislabelled axis, or events dated after "now", makes every date on the
  surface suspect. Duplicate events inflate the headline "1,076 events" and suggest nobody reconciled the
  sources.
- **Severity:** major

### 5. The neighbourhood ring labels each connection with one family word, and some look wrong

- **Screenshots:** 1920-hood.png, 1366-hood.png
- **What is wrong:** Each spoke carries only a family word and a tier, not a reason. Several look
  mislabelled: "The Intercept testimony T1" (a news outlet, whose article the case against calls a
  smear), "The Boeing Company place or time T3", "Waived SAP Notification Group testimony T3", "IAA FY2024
  Sec. 1102 link T3". At 1920, 73 "two steps" names fill the side margins, each repeating the words "two
  steps". Their faint dotted links cannot be followed to the member they pass through.
- **Why a reader cares:** "Every connection says in words why it exists" is not met on this surface,
  and a wrong family word (a newspaper as "testimony") misleads rather than just under-explains. The
  two-step margins add 146 labels that say nothing a reader can use.
- **Severity:** major

## Also noticed (below the five)

- Home, all widths: the "Start from a witness" card reads "7 nodes · 0 on the map" and still offers a
  "MAP ›" link. (minor)
- Home and map: the grey single letters (P, I, L, D, E) on every chip are never explained where they
  appear. On the map only a colour legend is keyed. (minor)
- Evidence: an AARO statement ("AARO held 1,870 total UAP reports...") is tagged "said on the record",
  while its neighbours from the same office are tagged "the office's own account". (minor)
- 375 home: two search boxes stack at the top of the page (the header field and "Search the board").
  (cosmetic)
- 1366 home stats: "T3" breaks from "580" and "7" from "bands" across line ends. (cosmetic)
- 1920 home: the explainer is a narrow column with a large empty field to its right, and the bottom third
  of the screen is empty. (cosmetic)

## What works best

The two outlined tags on claims, "said on the record" and "the office's own account", each say in one
line that Tier 1 here documents the saying, not the truth. They appear consistently on the node page,
the evidence explorer and the printed report.
