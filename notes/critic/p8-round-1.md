# Blind critic, phase 8 round 1

Screenshots judged: 39 (13 surfaces at 1920, 1366 and 375). The *-node and *-person captures are identical at every width (both show David Charles Grusch), so no non-person node page was seen.

## The five worst problems

### 1. The Library names the host as the issuer, and the source page contradicts itself about it

- **Screenshots:** 1920-library.png, 1366-library.png, 375-library.png, 1920-source.png, 1366-source.png, 375-source.png
- **What is wrong:** The first and most-cited Library row, "AARO Report on the Historical Record ... Volume I", reads "report · The Black Vault · 2024". Its source page says "issued by The Black Vault" in the meta line, and directly below that the interested-party box says it was "Published by the office this board investigates". The ISSUER facet has the same fault throughout: The Black Vault 115, Wikipedia 112, Internet Archive 65, mgln.ai 37 and YouTube 33 are all listed as issuers, and "issuer not recorded" (137) is the largest group.
- **Why a reader would care:** Who issued a document is the first thing a checker asks about it. On the showcase entry the page gives two answers in two lines, and a facet labelled Issuer that mostly lists mirrors and hosting sites cannot be used to filter by author. The board promises that its sourcing is careful, and an informed reader will stop trusting that the moment they see an AARO report credited to The Black Vault.
- **Severity:** blocker (the Issuer facet and the source meta line cannot be trusted)

### 2. Source dates are missing, contradictory or falsely precise

- **Screenshots:** 1920-library.png, 1366-library.png, 1920-topic.png
- **What is wrong:** The ERA facet puts 1,382 of 1,899 sources under "no date". Three congressional hearing records (CHRG-118hhrg53022, CHRG-118hhrg57440, CHRG-119hhrg61718) are shown as "undated", yet the Grusch page dates the first of them to 26 July 2023. The DoDI 5205.11 row has "(12 Sep 2024)" in its title and "2013-02-06" as its date. On the Roswell topic page, sources known only by year carry an invented day: "(1980-01-01)" on the Berlitz and Moore book and "(1995-01-01)" on the USAF report.
- **Why a reader would care:** A reader who filters by era silently loses nearly three quarters of the Library. Two dates on one row means one of them is wrong. A "-01-01" date looks like a sourced fact when it is actually a placeholder, which is exactly the kind of invention the board says it does not make.
- **Severity:** major

### 3. At 1366 the program map shows neither links nor most of its names

- **Screenshots:** 1366-map.png (compare with 1920-map.png)
- **What is wrong:** The header reads "135 nodes · 0 links · too narrow to name every node". Most cells show two or three named chips and then an anonymous "+3", "+4" or "+8". Some cells contain no name at all: DISCLOSURE through 1969 shows only "+4", and REVERSE ENGINEERING / NO DATE shows only "+1".
- **Why a reader would care:** 1366 is one of the two laptop widths the readers use. At that width the main map loses every connection line and hides most nodes behind numbered chips, which breaks the "nothing drawn without a name" rule and leaves the reader to click cell by cell to find out what the map is saying.
- **Severity:** major

### 4. The timeline draws hundreds of unnamed dots

- **Screenshots:** 1920-timeline.png, 1366-timeline.png
- **What is wrong:** Beneath each strand's named chips in 2017-2026 sit dense grids of coloured squares with no labels, several hundred per screen. The three earlier eras show only a count box ("79 events", "66 events") until clicked. The year axis also runs to an orange italic "2029" that sits outside the era label "2017-2026".
- **Why a reader would care:** Most of what is drawn cannot be read or identified without clicking, and the owner's rule is that nothing is drawn without a name. The dots also look like data, so a reader will read their density as meaning something. The 2029 tick next to a 2017-2026 heading is confusing until the reader works out what it is for.
- **Severity:** major

### 5. On the source page, the claims sit below a wall of raw URLs

- **Screenshots:** 1920-source.png, 1366-source.png, 375-source.png
- **What is wrong:** "WHERE TO READ IT" lists 14 bare URLs for one report. Most are mirrors of the same PDF (Black Vault, four Wikisource pages, three media.defense.gov files, aaro.mil), followed by five Wayback copies that wrap mid-URL. Nothing says which copy is the official one. At 1366 the "CLAIMS CITING IT · 122" section starts at the very bottom of the first screen, and at 375 it is several screens down.
- **Why a reader would care:** The reason to open a source page is to see what rests on the source, and here that is pushed below the fold by links the reader cannot tell apart. The reader has to guess which link is the primary record.
- **Severity:** minor

## What works best

The node page puts "The case against" (4 conflicts, 9 not verified) in its own column right beside the claims at 1920 and 1366, so a reader cannot read Grusch's claims without seeing AARO's rebuttal next to them.

## Notes on the screenshots

- Also seen, not ranked: at 1366 the Evidence explorer's SOURCE DOMAIN facet truncates "documents2.theblackvau" (1366-evidence.png). At 1920 the same facet box cuts off its last row, "cdn.centerforinquiry.org" (1920-evidence.png).
- The node and person captures are the same page at every width, so this round judged no institution, document or programme page.
