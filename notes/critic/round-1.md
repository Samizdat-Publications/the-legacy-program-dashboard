# Blind critic, round 1 (25 September 2026)

Redesign phase 5b, after the first pass of reader fixes (commit 51b47898). 30 screenshots from
`node tools/look.js --critic --out dist/critic/round-1`; the critic (a separate Opus agent) was told to
read `tools/critic/BRIEF.md`, open the PNGs and nothing else. Its report, verbatim:

---

Blind critic, round 1. I read BRIEF.md and the 30 PNGs in dist/critic/round-1 and opened nothing else. One note first: the "node" and "person" captures are pixel-identical at every width (both show David Charles Grusch), so there are really 27 distinct views. The node page of any other type was not seen.

**The five worst problems, worst first**

**1. Claims cannot be checked: the sources are not links**
- **Files:** 1920-node.png, 1920-person.png, 1366-node.png, 1920-evidence.png, 1366-evidence.png, 375-evidence.png
- **What is wrong:** The claims header on the node page promises "each claim → its source, as a link". But every visible claim row (about 11 at 1920) shows grey "source, not a link" at the right edge. In the evidence explorer, the largest source-domain bucket is "no url in the source 3,669", which is more than half of the 6,099 claims. The same table also counts board housekeeping as a claim: a 509th Bomb Group row, graded T3, reads "Referenced by the board but no dossier written yet ... see the wave-3 queue" and gives its source as "Board bookkeeping".
- **Why a reader cares:** These readers come to check claims. The page promises a link, then withholds it on every claim of the flagship person. The headline claim count is also inflated by internal notes.
- **Severity:** blocker.

**2. Sworn testimony is graded Tier 1**
- **Files:** 1920-node.png, 1366-node.png, 1920-report.png, 1366-report.png
- **What is wrong:** The home page defines Tier 2 as "a named person on the record". Yet Grusch's sworn hearing statements are marked T1 next to an orange "said on the record" chip, for example "Sworn: 'I was informed...'", "'biologics came with some of these recoveries'" and the Moskowitz and Burchett answers. The printed report repeats this. The claims header "32 Tier 1 · 16 Tier 2 · 13 Tier 3 · 3" also reads as 32 Tier 1 claims, when 32 is the total.
- **Why a reader cares:** The tier grading is the board's central promise. Here the most contested testimony wears the "documented" grade. An informed reader will take that as either an error or advocacy, and trust the other 6,000 grades less.
- **Severity:** major.

**3. The case against sits apart from the claim it answers**
- **Files:** 1920-node.png, 1366-node.png, 375-node.png
- **What is wrong:** At 1920 and 1366 "THE CASE AGAINST" is a separate column. Its 4 conflicts and 9 not-verified items are not attached to any claim row. For example, AARO's rebuttal of "over 40 witnesses" sits in column 2 near the top. The claim it answers ("Absolutely, based on interviewing over 40 witnesses") is about 700px lower in column 1, and nothing connects the two. On the phone the whole case-against block comes before the claims, as its own section.
- **Why a reader cares:** The owner's rule is that the case against sits beside the claim. As laid out, the reader has to match rebuttals to claims by hand.
- **Severity:** major.

**4. Marks with no name, especially on a laptop**
- **Files:** 1366-map.png, 1920-timeline.png, 1366-timeline.png, 1920-hood.png, 1366-hood.png
- **What is wrong:**
  - **Map at 1366:** it drops to "0 links" and cells show bare "+4", "+1", "+8" chips. Some cells hold nothing but an anonymous count, for example Disclosure/Through 1969 "+4", No date/Reverse engineering "+1", and 2000-2016/Disclosure "+2".
  - **Timeline:** every strand ends in rows of unnamed coloured dots. The header admits "an event whose name will not fit is a dot". The 2017-2026 axis also runs to 2029, past today.
  - **Neighbourhood:** "6 more linked directly, 288 more two steps away: no room on the ring for their full names" at 1920, and "8 more" at 1366.
- **Why a reader cares:** The rule "nothing is drawn without a name" is broken on three surfaces. At 1366, the most common laptop width, the program map loses both its links and many of its names.
- **Severity:** major.

**5. Neighbourhood links do not say why they exist**
- **Files:** 1920-hood.png, 1366-hood.png
- **What is wrong:** Each label on the ring carries only a tier, and sometimes a one-word type in faint grey ("witness-chain", "institutional", "temporal", "programmatic"). Most people get nothing but a tier, for example "Garry Nolan T1", "Karl E. Nell T2", "Ryan Graves T1". The two-hop names along the screen edges say only "hop 2", with near-invisible dotted lines, and never name the member they connect through. The phone version (375-hood.png) does give a sentence per link, so the words exist and are simply missing from the ring.
- **Why a reader cares:** "Every connection says in words why it exists" is the board's promise. The ring shows 66 lines and explains almost none of them, and "witness-chain" means nothing to an outside reader.
- **Severity:** major.

**Works best:** the thread page (1920-thread.png, 1366-thread.png). Each numbered step says in a plain sentence why it follows the last, with its relationship and tier, and the small map and the timeline slice reuse the same step numbers, so the chain can be followed across all three at once.

---

## Triage (phase 5b)

| # | Problem | In 5b scope? | What was done |
|---|---|---|---|
| 1 | "as a link" promise; "source, not a link" hides the source | partly: the wording and the display | the header no longer promises a link; a claim with no URL prints its source's own words; no-URL sources themselves: phase 8; bookkeeping rows: P5c |
| 2 | sworn testimony at Tier 1; header reads "32 Tier 1" | the header and the mark's explanation: yes; the grading: no (no tier moves in 5b) | header rewritten as "32 claims: 16 at Tier 1, ..."; a key under the header says what the mark means; claimant attribution: phase 10 |
| 3 | case against not attached to the claim it answers | no: needs claim-level links in the data | recorded for phase 10 |
| 4 | unnamed marks (map +N at 1366, timeline dots, hood +N); axis to 2029 | no, except the axis | map/hood: phase 11, timeline: phase 9; 2029 carries a scheduled event, so the axis keeps it and years after the board's date are now marked as such |
| 5 | ring links without sentences; "witness-chain", "hop 2" shown raw | the raw words: yes; the sentences: no | relationship words on the ring are the vocabulary's reader names; sentences on the ring: phase 11 |
