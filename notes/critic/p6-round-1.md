# Blind critic, phase 6 round 1 (26 September 2026)

Redesign phase 6 (the Atlas, topic pages, the new front door), first build. 42 screenshots from
`node tools/look.js --critic --routes atlas=#/atlas,topic=#/topic/roswell-1947,topic2=#/topic/grusch-allegations,gap=#/topic/pre-roswell-claims --out dist/critic/p6-round-1`;
a separate Opus agent read `tools/critic/BRIEF.md` and the PNGs and nothing else. Its report, verbatim, is
below the triage.

## Triage

| # | Finding | Scope | What was done |
|---|---|---|---|
| 1 | The Atlas shots show "No such route" | capture fault | Git Bash rewrote the `--routes` argument `#/atlas` into a Windows path (the reader's app was never asked for that route; the checks drive `#/atlas` directly and pass). Round 2 is shot with `MSYS_NO_PATHCONV=1`. |
| 2 | Grusch's sworn quote is T1 on his page and T2 on the topic page | R | The board holds the same quote twice at two tiers (`c-e9eeaa6e1d` T1 and `c-66d33c8d87` T2; also `c-8ad250645b` T1 and `c-4e0e09a4b2` T2). The topic cites the T2 copy faithfully. Duplicate claims graded differently are a research-queue item, not a page defect. |
| 3 | Statute text among Grusch's claims; AOC under MONEY; case against off the phone's first screen | 7 (connection groups), R (claims); phone: in scope | Connection groups are phase 7. On a phone the new Appears in row now shows three topics before its control, so it pushes the case against down less. |
| 4 | A bookkeeping placeholder counted as a T3 claim in the evidence explorer | 8 (claim facts `bookkeeping`) | Deferred: the redesign's `_claim_meta.json` `bookkeeping` flag excludes these from counts. |
| 5 | The map at 1366: "+N" chips, no links, orange numbers | 11 | Deferred to the map's phase. |
| below | Home tour steps 2 and 3 have identical titles | in scope | Each step now leads with the flagged record and names the topic it is read in, so two flags sharing a topic no longer print one title twice. |
| below | Tour texts speak of node size | Stewart's wording | `data/l0-highlights.json` is signed off; recorded for Stewart, not edited. |
| below | Topic pages use about 40% of the width at 1920 | in scope | At 1280 and wider each lead and summary sentence sits beside its sources (sentence at a reading measure on the left, cites on the right). |
| below | Timeline axis to 2029; patents FIG captions; analysis ellipsis | 9, other | Deferred (timeline phase 9; patents and the node analysis outside phase 6). |

---

I read only BRIEF.md and the 42 PNGs in dist/critic/p6-round-1. I opened nothing else. The "node" and "person" captures are the same Grusch page at every width, so the node page was only seen once per width.

**1. The atlas never rendered. All three captures show a route error.**
- Files: 1920-atlas.png, 1366-atlas.png, 375-atlas.png
- What is wrong: every atlas capture shows the red heading "No such route: #C:/Program%20Files/Git/atlas" above a developer-style list of hash routes. That address is a local disk path, so this may be a fault in how the screenshots were taken rather than what a reader would get. I cannot tell which from the screen, so the atlas needs to be re-shot before anyone judges it.
- Why a reader would care: the home page's main call to action, "OPEN THE ATLAS", points here. If a reader can reach this page, the front door leads to an error. If they can't, this round has not seen the phase's main new page.
- Severity: blocker, or no finding if it is a capture artefact.

**2. The same sworn words get different grades on different pages.**
- Files: 1920-node.png, 1920-report.png, 1920-topic2.png, 1366-topic2.png
- What is wrong: Grusch's sworn quote "I was informed in the course of my official duties..." is T1 with the "said on the record" badge on the node page and report. On the topic page, item 2, the same quote is T2. His answer on how the programme is funded ("misappropriation... IR&D") is also T1 on the node page and T2 on the topic page, item 4. The home page defines T2 as "a named person on the record", which is exactly what the T1 "said on the record" badge describes.
- Why a reader would care: grading is the board's central promise. A reader who checks one statement on two pages finds two grades and stops trusting the tiers.
- Severity: major.

**3. The node page's claims and connection groups don't describe the node.**
- Files: 1920-node.png, 1366-node.png, 375-hood.png, 1920-report.png
- Claims: items 3 and 4 in Grusch's claim list (and in his report) are the UAP Disclosure Act's definitions of "legacy program" and "controlling authority". They are statute text, not claims about Grusch.
- Connections: under "MONEY: who paid, contracted or was paid" sit Alexandria Ocasio-Cortez and Jared Moskowitz, who asked hearing questions. Jay Stratton, a person, sits under "PROGRAMME LINKS: what ran, produced, succeeded or absorbed what".
- Case against: on the phone it is not on the first screen at all.
- Why a reader would care: the rule is that every connection says why it exists, and here the headings say something false. An informed reader will notice that AOC paid no one, and will wonder what else is misfiled.
- Severity: major.

**4. Internal bookkeeping is shown and counted as a graded claim.**
- Files: 1920-evidence.png, 1366-evidence.png
- What is wrong: row 4 of the evidence explorer is a T3 claim on "509th Bomb Group" that reads "Referenced by the board but no dossier written yet. This node exists so the graph resolves... see the wave-3 queue". Its source column says "Board bookkeeping", and the text contains an em dash.
- Why a reader would care: a placeholder is being presented as evidence and is inflated into the "6,099 claims" and "T3 619" totals on the home page. "Wave-3 queue" is meaningless to a reader. If one row like this shows up, readers will ask how many of the 619 T3 claims are the same.
- Severity: major.

**5. At 1366 the program map loses its links and shows nameless chips.**
- Files: 1366-map.png (compare 1920-map.png)
- What is wrong: the header reads "0 links · too narrow to name every node". Cells collapse to a few names plus dashed "+4", "+1", "+8" chips. Several cells have nothing but a bare chip: Disclosure through 1969 shows only "+4", and Retrieval 2017-2026 and some No-date cells show a lone "+1". Names also carry unexplained orange numbers ("Operação Prato 14", "GEIPAN 13", "DoD Agency-Wide Audit 8") that read like counts.
- Why a reader would care: 1366 is a primary laptop width, and there the map shows no connections and breaks the "nothing drawn without a name" rule. The orange numbers suggest a size or importance ranking the board says it never uses.
- Severity: major.

**Also noticed, below the cut:**
- **Timeline:** the axis ends in an orange "2029" past the 2017-2026 era (1920 and 1366). Desktop event labels float with no visible tie to their year.
- **Home page tour:** steps 2 and 3 have identical titles. Steps 1 and 5 talk about node size ("the largest node on the map", "Size here means implicated"), which contradicts the size rule.
- **Patents:** thumbnails captioned "FIG 1" (10,135,366 and 10,322,827) are text pages, not drawings. The sheets are said to be "IN ORDER", but the first card is 10,144,532 while 10,135,366 is the one selected.
- **Topic pages at 1920:** they use roughly 40% of the width.
- **Node page:** the board's analysis is cut off mid-phrase with an ellipsis.

**What works best:** the research-gap topic page (1920-gap.png, 375-gap.png). It says plainly what the board does not yet hold and lists five precise open questions, including how each claim reached the public.
