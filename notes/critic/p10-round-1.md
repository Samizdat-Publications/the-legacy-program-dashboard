# Blind critic, phase 10, round 1

Read: tools/critic/BRIEF.md and the 30 screenshots in dist/critic/p10-round-1-sel/ (home, homeq, person, made, office, questions, q, qblocks, connect, connect2 at 1920, 1366 and 375). Nothing else.

Ambiguity first: none of the shots looks mid-load. Some of the repeated statements in problem 1 cite different source strings (a CHRG number in one, an HHRG transcript id in another), so they may be separate records on purpose. The screen gives no reason why they carry different tiers, and the reader sees none either. The empty middle band at 1920 in made and office may just be the case-against column running out. Either way, the reader sees a blank strip about 480px wide.

## The five worst problems, worst first

### 1. The same words carry different tiers, side by side

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 375-qblocks.png, 1920-q.png, 1920-made.png, 1366-made.png, 1920-office.png, 1366-office.png
- **What is wrong:** Under "The evidence for", items [16] T2, [17] T1 and [18] T2 are the same Grusch quote ("I was informed in the course of my official duties..."), stacked one under another. The same quote also appears as T2 and as T1 ("said on the record") under "Witnesses who have gone to Congress" on the made view. The Nancy Mace biologics answer is T1 in one card and T2 in the next. On the office view, the 291-reports figure is T2 as "Caseload" and T1 as "Reporting period", and a bibliographic description of a title page is T2 while AARO's contested denial is T1. The "7 for" count on the question is padded by three copies of one quote. On the questions list, every visible question reads "5 open" with 6 or 7 for and 6 or 7 against, so the counts look like a quota.
- **Why a reader cares:** The tier is the board's central promise. A checker who finds one statement graded two ways, three cards apart, has no reason to trust any grade on the site, or any for/against count built from them.
- **Severity:** blocker

### 2. Interested-party statements show as T1, and the flag that qualifies them is in Tier 2's colour

- **Files:** 1920-q.png, 1366-q.png, 1920-qblocks.png, 1366-qblocks.png, 1920-office.png, 1920-made.png
- **What is wrong:** In the answer to "Has the US recovered non-human craft?", AARO's denials are T1 four times ([2], [8], [9], [10]) and Grusch's sworn account is T2 ([1]). The qualifier "the office's own account" is a small amber box, the same amber as T2, "NOT VERIFIED", "START HERE" and "THE BOARD'S ANALYSIS". The rule is also applied unevenly. [39] "Formal DoD rebuttal" is T1 with no qualifier, while [41], from the same report, is T2 and marked demoted. In the made view's connections, "Standing DoD denial" by Susan Gough is T1 with no qualifier, and Milley's denial is T2.
- **Why a reader cares:** The home page says AARO and DoD are capped at Tier 2 unless the claim is about what they said. Someone scanning the tier column sees government denials outranking sworn testimony, and the colour that should warn them means four other things.
- **Severity:** major

### 3. Internal workflow notes are printed as the source of evidence

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 1920-made.png, 1366-made.png
- **What is wrong:** Item [41] under "The evidence against" prints a raw defense.gov PDF URL, then "DEMOTED from Tier 1 (sourced to an interested party (AARO/DoD) asserting an external fact; primary record of the statement, not of the fact); needs primary replacement". The source line of [39] is a run-on machine list ("denials link between ... and ... ↗ · Roll Call ... ↗ · ..."). The made view opens with "Reasoning: the advisory role is recorded in wave-1 sourcing on this board".
- **Why a reader cares:** "Needs primary replacement" tells the reader that the board knows this citation is inadequate but still counts it as evidence against. The editor's to-do list, shown where a citation should be, reads as an unfinished draft.
- **Severity:** major

### 4. On a node page, the case against is detached from the claims and has no sources

- **Files:** 1920-person.png, 1366-person.png, 375-person.png, 1920-made.png
- **What is wrong:** "The case against" (4 conflicts, 9 not verified) is a separate column at 1920 and 1366. At 375 it sits above all the claims. None of its cards names the claim it contests, and none carries a tier, a source line or a link, although every claim card next to it has all three. At 1920 the column ends and leaves a blank strip about 480px wide between the claims and the connections.
- **Why a reader cares:** The owner's rule is that the case against sits beside the claim. Here the reader has to match each conflict to a claim by hand and cannot check the conflicts at all. Only the side the page is weighing up gets citations.
- **Severity:** major

### 5. The connect page's all-T1 route runs through a hub and states the Roswell custody story as documented

- **Files:** 1920-connect2.png, 1366-connect2.png, 375-connect2.png, 1920-connect.png, 375-connect.png
- **What is wrong:** Route 1 from Roswell to the 2023 hearing is headed "T1 T1 T1 T1 T1". Its first step reads "Roswell Incident / is held by / 509th intelligence office took possession of the Roswell debris · T1": the verb makes no sense for an incident, and a retracted 1947 claim is shown as documented with no "said on the record" flag. The route then passes through "United States House of Representatives", although the page says a route prefers specific nodes over the most-connected ones. Separately, both input boxes cut names off mid-word ("...Division G of the Ser", "Applications P"). At 375 the H1 alone fills the first screen.
- **Why a reader cares:** A string of five T1s makes a bureaucratic chain look like a strong, documented link between Roswell and Grusch's hearing. That is exactly the reading the page's own disclaimer warns against.
- **Severity:** major

**What works best:** on the question page, each paragraph of the answer sits beside its numbered claims, and each claim shows its tier, its node and its source, so every sentence can be checked where it is read.

## Disposition (the session, after the round)

| # | in phase 10's scope? | what was done |
|---|---|---|
| 1 | no: the data | The same testimony carried as a Tier 1 record of speech and as a Tier 2 claim is the research queue's first item ("the claims that sit at two tiers", `notes/plans/P5-research-queue.md`); the tier decision is phase R's, and the plan fixes this contradiction in words, not by moving a tier. The key's Tier 1 sentence now stands wherever the key renders. Five open questions per page was the drafter's choice, left. |
| 2 | partly | The "said on the record" and "office's own account" marks no longer share Tier 2's amber: neutral text on a dashed border, every surface. The office's own account staying Tier 1 is the board's rule (a Tier 1 claim about what the office said). |
| 3 | no: the data | "DEMOTED from Tier 1 ... needs primary replacement" and "wave-1 sourcing" are in the claims' source strings, written by the regrade pass; a reader-facing rewording of those strings is for phase 12's copy pass. Recorded in `notes/plans/P10-findings.md`. |
| 4 | no | The node page's case-against layout is phase 5b and 6's; not touched here. |
| 5 | yes | The route header now reads "each link graded T1 T1 ... · N things in between", and the method line says a tier grades one link, not the route. The end inputs take a full row each, so a long name is not cut at a laptop width; at 375 the heading drops to body size. "is held by" is the phase 7 vocabulary's inverse wording, left. |
