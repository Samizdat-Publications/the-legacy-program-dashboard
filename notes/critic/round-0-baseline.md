# Blind critic, round 0: the baseline (25 September 2026)

30 screenshots of master after phase 4 (`node tools/look.js --critic`, 10 surfaces at 1920, 1366, 375). The
critic saw only the screenshots and `tools/critic/BRIEF.md`. Its report, condensed, and where each problem
is fixed.

| # | Problem | Severity | Where it is fixed |
|---|---|---|---|
| 1 | Phone layout broken almost everywhere: navigation cut after "HO"; Home's stats panel over the search box and the intro one word wide; map cells overprint; neighbourhood empty with its legend cut; evidence table shows no claim; timeline and patents cut at the right edge | blocker | **P5b** (a phone pass now, not phase 11) |
| 2 | Sworn testimony shown as "T1" with nothing saying that T1 means "documented that it was said"; AARO statements T1 with no mark; housekeeping notes ("Board bookkeeping") counted as Tier 3 claims | major | display of attributed claims: **P5b** (a visible "on the record that it was said" mark, derived from the claim, no tier moved); bookkeeping notes out of the claims: **P5c** (after phase 5 merges, since it moves claim counts); full claimant attribution: phase 10 |
| 3 | Connections do not say why they exist on the neighbourhood (a one-word type) and the map (unlabelled lines); some node-page groups are wrong (a reporting-duty link under Money) | major | wrong groups: phase 7 (predicates); neighbourhood sentences and map lines: phase 11 |
| 4 | Things drawn without names: timeline marks, map "+N" chips, neighbourhood "+288"; what is named changes with window width | major | timeline: phase 9; map and neighbourhood: phase 11; P5b removes nothing here but records it |
| 5 | Node page leads with a 45-line paragraph in the board's own voice; about 780px of dead space at 1920; claims and the case against not visible on the first screen | major | **P5b**: the first screen shows the lead, the case against and the claims; the dossier prose is labelled as the board's analysis and folded after its first lines; no dead gap |
| - | The "Ask the analyst" tab covers content on every page | major | **P5b** |
| - | Internal jargon shown to readers ("row pitch 18", "below the L0 floor", "derived pairs on", raw ids) | minor | **P5b** |
| - | Debug chrome in the header (viewport badge, raw hash) | cosmetic | **P5b** |
| - | Thread timeline slice out of year order | major | **P5b** |
| - | Timeline axis runs to 2029; an empty NO DATE column in every strand | minor | **P5b** |
| - | Patent pages never name the inventor; some "drawing sheets" are text pages | minor | phase 8 (sources) or R |
| - | "no url in the source" is 60% of claims, unexplained; archive URLs wrap mid-string | minor | phase 8 |

**What works best** (the critic): the evidence explorer at desktop widths, with tier, node, the verbatim
claim, the named source and FOIA status on one row.
