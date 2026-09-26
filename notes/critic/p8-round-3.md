# Blind critic, phase 8 round 3

Screenshots judged: 39 (13 surfaces at 1920, 1366 and 375: home, node, person, map, hood, timeline, evidence, thread, patent, report, library, source, topic).

## The five worst problems

### 1. The same source is linked on one claim and "not matched to a Library entry" on the claim below it

- **Screenshots:** 1920-topic.png, 1366-topic.png, 1920-evidence.png, 1920-library.png, 1920-source.png
- **What is wrong:** On the Roswell topic, claim 1 links to the Library entry "RAAF Press Release, 8 July 1947". Claim 7 cites the same press release and says "source, as cited (not matched to a Library entry)". Claims 2 and 6 link to "The Roswell Report: Fact Versus Fiction in the New Mexico Desert (1995)", but claim 4 cites "The Roswell Report: Fact vs. Fiction" and is left unmatched. In the Evidence explorer, an AARO claim cites the "AARO FY2025 Consolidated Annual Report" and is also unmatched, though "AARO FY2025 Annual Report" is a node on the program map.
- **Why a reader would care:** The Library's opening line says every source has "its own page listing every claim and link that rests on it". A reader who opens the RAAF press release's page will not find Walter Haut's claim, so the page undercounts what rests on that source. The source page does admit that unmatched citations "are not counted here". But when the missed source sits on the same screen, already linked one row up, the admission reads as a known gap left in place, not a hard case.
- **Severity:** major

### 2. The source page grades two quotations of the same AARO promise differently, and repeats one claim almost word for word

- **Screenshots:** 1920-source.png, 1366-source.png
- **What is wrong:** Under "AARO Historical Record Report, Volume II (unpublished)", a quotation from page 45 saying Volume II "will be published in accordance with the date established in Section 6802" is T1, tagged "the office's own account". Five rows below, a quotation from page 6 saying AARO "will publish Volume II in accordance with the date established in Section 6802" is T2, "held at Tier 2: ... asserting an external fact". The same group also holds two nearly identical T1 claims, "Volume I states that Volume II will cover interviews and research conducted between 1 November 2023 and 15 April 2024 plus additional unresolved allegations", one ending "from Volume I." and one not.
- **Why a reader would care:** The source page lays out a source's claims side by side so a checker can compare them. That comparison shows the same statement from the same document given two different tiers, and near-duplicate rows inflating "cited by 122 claims". This hits the tier system itself, which is what the board asks readers to trust.
- **Severity:** major

### 3. The "interested party" flag does not follow the rule the site states

- **Screenshots:** 1920-library.png, 1366-library.png, 375-library.png, 1920-home.png, 1920-topic.png
- **What is wrong:** The home page says "Statements by AARO and the Department of Defense are treated as an interested party's". The Library defines an interested party as the office "or its parent department". Yet the Library flags only 46 sources. The issuer facet shows 47 from the Department of Defense alone, plus 76 from the Defense Intelligence Agency. Visible DoD items carry no flag: "DoDI 5205.11" (issuer Department of Defense), "Special Access Program (SAP) Policy (DoDD 5205.07)", and the DIA letter to Steven Aftergood. On the Roswell topic, the Air Force's own Roswell Reports support T1 claims with no "office's own account" tag.
- **Why a reader would care:** A reader who sees the flag missing from a DoD regulation cannot tell whether the flag and the Tier 2 cap were applied, or whether the rule only reaches AARO. That leaves every DoD-sourced T1 claim open to doubt.
- **Severity:** major

### 4. At 1366 the program map draws no links and hides most nodes behind unnamed "+N" chips

- **Screenshots:** 1366-map.png (compare 1920-map.png), 1366-hood.png
- **What is wrong:** The 1366 header says "0 links · too narrow to name every node, so each cell shows its count". Cells show two or three names and then "+4", "+8", "+7". Several cells are nothing but a bare "+1" or "+2". At 1920 the same map draws 118 links and names all 135 nodes. At 1366 the neighbourhood also says "two steps away: off at this width".
- **Why a reader would care:** 1366 is one of the two stated laptop widths. There the site's main picture shows no connections at all and hides most of its nodes behind anonymous counters. That breaks "nothing is drawn without a name" and "every connection says why it exists", and a laptop reader has to click cell by cell to see what a wider screen shows at once.
- **Severity:** major

### 5. Labels are cut off or broken badly

- **Screenshots:** 1366-evidence.png, 1920-evidence.png, 1920-node.png, 1920-person.png
- **What is wrong:** In the Evidence explorer at 1366, a source-domain chip reads "documents2.theblackvau 101": the name is cut off. At 1920 the last visible source-domain chip ("cdn.centerforinquiry.org 67") is sliced in half by its scroll box. On the node page at 1920, the claims header wraps as "3 at Tier" with a lone "3" on the next line.
- **Why a reader would care:** The owner's rule is that labels are never truncated. A cut-off domain name cannot be recognised or trusted as a filter, and the orphaned "3" makes the tier count read wrong at a glance. Noticeable, but not misleading.
- **Severity:** minor

## What works best

The source page's opening block: a boxed interested-party notice saying exactly what the document proves and what it does not, a "where to read it" list with the original URL, extra copies and archived captures, and each claim printed with its "as cited" text, so a checker can open the record in one step.
