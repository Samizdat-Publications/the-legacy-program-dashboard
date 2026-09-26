# Blind critic, phase 6 round 2 (26 September 2026)

After the round-1 fixes. 42 screenshots from `MSYS_NO_PATHCONV=1 node tools/look.js --critic --routes
atlas=#/atlas,topic=#/topic/roswell-1947,topic2=#/topic/grusch-allegations,gap=#/topic/pre-roswell-claims
--out dist/critic/p6-round-2` (the Atlas rendered this time); a separate Opus agent read
`tools/critic/BRIEF.md` and the PNGs and nothing else. Its report, verbatim, is below the triage.

**This is the last round of phase 6.** None of the five worst is a defect of a phase 6 surface: the Atlas,
Home, Appears in, the bar and the domain-node pointer draw no finding at all, and the topic-page finding is
the board's data shown faithfully. The stopping rule (the worst in-scope issue minor or cosmetic) holds.

## Triage

| # | Finding | Scope | Disposition |
|---|---|---|---|
| 1 | One sworn quote T1 on Grusch's page, T2 on the topic page; a Department statement marked "said on the record" and filed under Grusch; an IG finding at T1 resting on Grusch's testimony and The Debrief | **R, first in the queue** | The data holds duplicate claims at two tiers on one node (`c-e9eeaa6e1d` T1 and `c-66d33c8d87` T2; `c-8ad250645b` T1 and `c-4e0e09a4b2` T2); the topic, verified in phase 5, cites the T2 copies and the page prints the record as it is. The fix is to merge each pair to one claim with one tier, and re-cite. The Department statement and the IG finding are the "Tier 1 on a secondary relay" class already in `notes/plans/P5-research-queue.md`; the mark follows the P5b rule (said is tested before office), unchanged here |
| 2 | A bookkeeping placeholder shown and counted as a T3 claim | 8 | the `bookkeeping` claim fact of redesign section 4 excludes these from counts and tables |
| 3 | Timeline dots with no name; the axis to 2029 | 9 | the timeline's phase |
| 4 | Patent figure captions off by one sheet | R (patents data) | the drawing register's sheet-to-figure mapping needs re-reading against the filed sheets |
| 5 | Neighbourhood labels with a tier and no relationship word | 7 / 11 | connection groups and the graph views |
| below | Map at 1366; the analysis fold's ellipsis; tour copy on node size; node and person captures identical | 11; node page; Stewart's signed-off wording; the camera | not phase 6 |

---

I read BRIEF.md and opened all 42 PNGs in p6-round-2. I opened nothing else.

**1. The same sworn statement gets a different tier on different pages.** Severity: **blocker**
- Files: 1920-topic2.png, 1366-topic2.png, against 1920-report.png, 1366-report.png and 1920-person.png.
- What is wrong: On the Grusch topic page, claim 2 is marked **T2**. It is Grusch's sworn quote "I was informed in the course of my official duties…". Claim 4, "misappropriation of funds and self-fund… IR&D", is also **T2**. On the Grusch node page and the printable report, the same two quotes are **T1** with the "said on the record" tag (report items 6 and 9). The tags are also misapplied on the same topic page:
  - Claim 6 is the Department's June 2023 statement. It carries "said on the record" rather than "the office's own account", and it is filed under Grusch, not the Department.
  - Claim 5 is the Inspector General's finding. It is tagged "said on the record" at T1, but its only sources are Grusch's own testimony and The Debrief.
- Why a reader cares: The tier is the board's central promise. A reader who finds one quote graded two ways on two pages will stop trusting every grade.

**2. An internal housekeeping note is shown and counted as a graded claim.** Severity: **major**
- Files: 1920-evidence.png, 1366-evidence.png.
- What is wrong: The fourth row of the default evidence list is a T3 "claim" on 509th Bomb Group: "Referenced by the board but no dossier written yet. This node exists so the graph resolves… see the wave-3 queue." Its source is given as "Board bookkeeping". The text also contains an em dash.
- Why a reader cares: It sits in the claim table as if it were evidence, and it appears to be counted in the 6,099 claims and 619 T3 on the home page. It also exposes internal jargon ("wave-3 queue", "so the graph resolves") on the surface a checker opens first.

**3. The timeline draws hundreds of events as unnamed dots, and its axis ends at a stray "2029".** Severity: **major**
- Files: 1920-timeline.png, 1366-timeline.png.
- What is wrong: Under each strand's labelled rows, most events are small coloured squares with no name, stacked eight or more deep near 2024 to 2026. The header admits it: "an event whose name will not fit is a dot." The 2017-2026 era's year axis also ends with **2029** in orange, highlighted, which the era title does not explain.
- Why a reader cares: This breaks the rule that nothing is drawn without a name, and it hides most of the 562 recent events behind a click. A lone highlighted future year reads as either future-dated events or an error.

**4. The patent drawing captions do not match the drawings.** Severity: **major**
- Files: 1920-patent.png, 1366-patent.png.
- What is wrong: For US 10,135,366, the tile captioned "FIG 1 · sheet 1 of 3" shows a page of text, not a drawing. The tile captioned "FIG 2" shows figures 1 and 2, and "FIG 3" shows figures 3 and 4. US 10,322,827 has the same off-by-one pattern. This is under a heading that promises "federal public-domain figures… with full provenance".
- Why a reader cares: A reader checking the Navy drawings will cite the wrong figure number. On a board whose selling point is exact sourcing, a mislabelled primary document is worse than none.

**5. Many neighbourhood links do not say why they exist.** Severity: **major**
- Files: 1920-hood.png, 1366-hood.png.
- What is wrong: About half the ring labels carry only a tier and no relationship word. Examples: "Garry Nolan T1", "Karl E. Nell T2", "Robert Garcia T1", "Mark A. Milley T2", "The Hill T2". Others do say why, for example "denial T2" or "testimony T3".
  - At 1920, the two-step columns hold over 100 labels. Each says only "two steps" and hangs on a dotted line too faint to follow to anything.
  - 6 direct links (8 at 1366) are hidden behind "expand".
- Why a reader cares: This breaks the rule that every connection says in words why it exists. In practice, "Robert Garcia T1" does not tell the reader whether Garcia questioned Grusch, corroborated him or disputed him.

**Also seen, below the cut:**
- **Map at 1366:** it collapses to "0 links · too narrow to name every node", with anonymous "+4" and "+8" chips (1366-map.png). 1366 is one of the two stated laptop widths.
- **Truncated analysis:** the Board's analysis text ends in an ellipsis on every node page ("Senior Intelligence Officer…", and "crash-…" at 375), which breaks the never-truncate rule.
- **Home start-here copy:** it talks about node size ("the largest node on the map at 82 members", "Size here means implicated").
- **Ambiguous captures:** 1920-node.png and 1920-person.png are the same Grusch page, and so are the 1366 and 375 pairs. No non-person node page was captured, so that surface is unreviewed.

**What works best:** on the node page, "The case against" (4 conflicts, 9 not verified) sits as its own column right beside the claims, and each item says what is on the record and what has never been produced.
