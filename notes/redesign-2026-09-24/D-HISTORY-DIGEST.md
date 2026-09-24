# The Program: history digest for the redesign

Scope: all 112 files in `notes/` (12 Aug to 19 Sep 2026), `research/leads/CANON-GAPS-2026-09-18.md`,
the `notes/design-*` folders, and the candidate files where Stewart's approvals are recorded.
Cross-checked read-only on 24 Sep 2026 against git, the CI run list and the shipped data in
`app/public/data/`. Paths are repo-relative to
`C:\Users\stewa\ClaudeProjects\Missing individuals connected to defense contractors\the-program`.

Conventions:
- A quote in quotation marks is verbatim from the named file. "(recorded paraphrase)" means the
  note itself renders Stewart in the session's words or says "paraphrased".
- Em dashes inside quoted source text are rendered as " - " (the no-em-dash rule). Nothing else
  in a quote is altered.
- All dates are 2026.

---

## 0. Where things actually stand (verified 24 Sep, read-only)

| | |
|---|---|
| master | `origin/master` = local `master` = `838c134` ("Handoff: the spine is built and on its own branch, not parked."). Gate run 35482093152 success; deploy 35483115506 success, 2026-09-20 02:06 UTC |
| consequence | The silent-defaults fixes (`f89996d`..`ffc1d76`) and the NSC/EO spine (`f803638`) ARE in production. `notes/HANDOFF-2026-09-19-AFTERNOON.md` section 1 ("IT NEEDS STEWART'S YES TO MERGE") and the auto-memory line "master d545a79" are both stale |
| shipped board | 1,136 nodes: 338 person, 237 document, 196 institution, 87 event, 82 program, 73 location, 64 legislation, 59 domain. 2,685 sourced edges in 12 types (institutional 720, programmatic 324, investigative 302, denial 219, legislative 215, witness-chain 204, research 198, custody 162, temporal 91, geographic 91, behavioral 84, funding 75). Claims T1 3,701 / T2 1,618 / T3 578. Timeline 1,059. L0 135, of which 0 are people. Node tiers A 169 / B 398 / C 569 |
| still unmerged | `nuclear-2026-09-19` at `359958f` (canon "pass 5", the nuclear witnesses); `trial/nuclear-on-defaults` (local only, a measurement) |
| production | The app (`app/`, Vite + TypeScript, hash router) at https://the-program-zxz.pages.dev since the 4 Sep cutover. Review site https://the-program-next.pages.dev |
| old shell | `dist/the-program.html` (about 17 MB) still built and still gated in CI by `state_snapshot.py --gate` (runtime_check.js, test_packed_layout.js etc.), deployed nowhere. Its checks can still block a deploy |
| CLAUDE.md | Its "Starting a fresh session?" paragraph still says `notes/HANDOFF-2026-09-18.md` "is the current one"; five later handoffs exist (09-18-EVENING, 09-18-NIGHT, 09-19, 09-19-LATE, 09-19-AFTERNOON) and none is named there |

### 0a. Ten things a redesign must know

1. The whole-graph map failed twice in Stewart's own words: "way too busy ... no opportunity for
   discovery" (14 Aug) and "a thousand dots that mean nothing" (2 Sep). The fix that worked was
   entity-first pages, question-shaped entry paths and threads, not label tuning.
2. What he liked: the orthogonal look, the animated directional lines, and seeing every connection
   of the node he clicked, named. What he disliked: anonymous geometry, floating white labels,
   filters that do nothing visible, panels covering the map.
3. The meaning model he asked for on 18 Sep is the hub rule: claimants run INTO the thing claimed
   about, with the case against as an edge, so a busy hub reads as "a lot is claimed here".
4. The current top-level map cannot show that: L0 admits no people and no locations, so Lazar,
   S-4 and Dulce are all off it, and the map is capped at 135 by a declared stopgap.
5. The size limit is structural: one label size, no truncation, 1:1 layout for the viewport, a
   growing membership rule, and a check (C11) that needs 14 highlights drawn as chips.
6. Size never encodes importance, labels are chosen by space and never by rank, nothing is drawn
   anonymously, motion only where attested. These survived every redesign and should survive this one.
7. Node tier A/B/C is a forced-percentile artefact of 12 Aug that nobody reads the way it is
   defined; claim tiers 1-3 are the real evidence system and search already ranks on them.
8. The gate still tests a shell no reader sees, and one of its pixel-ink checks blocks the nuclear
   cluster. `state_snapshot.py --gate` does not run the app checks that CI runs.
9. Research is lost between files: unbuilt section-A candidates, seven unwired analyst finds, and
   the canon audit's own pass 5 dropped by a renumbering.
10. Stewart has delegated research and tier decisions fully; only a push to master still needs his
    yes. He wants the result shareable with research friends and defensible in front of
    "respectable individuals".

---

## 1. Stewart's voice

### 1a. Chronological record

| Date | What he said or decided | File |
|---|---|---|
| 12 Aug | Redirected the research brief away from balance: "the initial research brief was written balanced/both-sides. Stewart redirected to the pro-disclosure stance above. Wave 1 was killed and relaunched." (session record) | `notes/RESEARCH_LOG.md` |
| 12 Aug | The session's restatement to him of his ask: "you asked for a board that presumes the program exists and treats the official record as obfuscation." | `notes/DASHBOARD_PLAN.md` s3.5 |
| 12 Aug | Craft catalogue: a visual per catalogued craft; "Preference: build these in Claude Design rather than generating them." (recorded paraphrase; the note says "Stewart's stated reason to prefer design over image generation is right") | `notes/WANTS.md` |
| 13 Aug | Public README and "visually impressive landing page", recorded as "Explicitly gated on reaching 1.0"; and "Stewart wants Claude to own all GitHub work: publishing, version control, branches, releases" | `notes/WANTS.md` |
| 13 Aug | The map framing, recorded as his: "Roll the map up to the level of the program - institutions, programs, events, legislation - and reveal individuals only when a node is opened." Followed by: "Stewart's framing, and it is better than the alternative I proposed. A filter hides 820 nodes and a board built on 'we left nothing out' has no answer for what got cut." Section heading: "the map is of the program, not of people (Stewart, 13 Aug)" | `notes/DESIGN-BRIEF-L0-MAP.md` s2; `notes/PERF-AND-DENSITY-PLAN.md` Part 5 |
| 14 Aug | Seeing the board cold: "way too busy ... no opportunity for discovery, nothing visually identifying what the important connections are. In the current state this is basically useless to the end user." | `notes/L0-IMPLEMENTATION-2026-08-13.md` Stage 12; `notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md` s1 |
| about 24 Aug | Rejected a scan bar moving across the map: "Stewart objected to it on sight and he was right." (Design's words) | `notes/design-2026-08-24/DESIGN-RESPONSE-LAYOUT-2026-08-24.md` s3 |
| 25 Aug | Signing off the packed-cell comp: "The arrangement looks good. Obviously on our live one we have the animated lines etc that design gave us plus all the other stuff for how to show that screen, but layout wise this looks good and want all 3 options turned on." Also: all 14 start-here flags "all kept, none cut" | `notes/PACKED-LAYOUT-BUILD-2026-08-25.md`; `notes/HANDOFF-2026-08-26-packed.md` s2 |
| 26 Aug | (the note says "verbatim in substance") "I choose something from the start menu and menus overlap, the right bar expands to half the screen, you never actually get to see the full map. Even clicking fit leads to the view where it just uses the numbers, which I want to save for only super zoomed out. I need fit to display the full map… nobody ever gets to see the map in its normal form and it's central to it, as it shows how robust our connections are." | `notes/HANDOFF-2026-08-26-UX.md` s1 |
| 26 Aug | "when I click a starting point I want it to select the relevant cells but then fit to screen." | same, s2C |
| 26 Aug | "I wonder if we don't swap it out with analyst, so analyst stays on the right panel and the stuff currently on the right panel could be where the analyst is now, since it takes up the entire bottom of the screen." | same, s3 |
| 26 Aug | Asked what would let a session "click everything, see how it looks, write notes" (produced `tools/walk.js`) | same, s5 |
| 26 Aug | "The map is never able to fit ... it really should auto fit until someone clicks something so they can see the whole thing." / "Clicking show on the map doesn't do much since the map is so obscured by the panels." / "It's also not clear how to collapse the right or left panel." | `notes/SHELL-FIT-2026-08-26.md` |
| 26 Aug | "make sure ALL of claude designs stuff it designed is implemented" | `notes/DESIGN-CONFORMANCE-2026-08-26.md` |
| 26 Aug | Told sessions twice to stop offering adversarial review here: "Adversarial review does NOT apply to this project. Stop offering it here. ... (Told twice: 26 August 2026.)" (reverses the 12 Aug "standing instruction" in `notes/SESSION-HANDOFF-2026-08-12-cloud.md`) | `CLAUDE.md` s4 |
| 27 Aug | "licensing is for me to deal with on my end. You're just collecting the pictures for our project." | `notes/IMAGE-SOURCING-2026-08-27.md` |
| 27 Aug | "I can drag the right sidebar but what I want is the sidebar to have a clickable edge that, when clicked, on a curved motion sends the drawer back to its closed position on the right, same with the left pane, then I should be able to open the closed drawer by clicking it to expand." | `notes/DRAWERS-2026-08-27.md` |
| 27 Aug | "that tab needs to exist on the open version too" | `notes/SHELL-2026-08-27.md` s4 |
| 27 Aug | "it spawns the panel on the right plus the panel that says the specifics about that node that floats ... but then it blocks the map." / "the entire map and yellow part is fading in and out of the background rendering it illegible." / "we STILL have not implemented the color and particle system for the lines showing which way the connection goes that design gave us." | `notes/SELECTION-2026-08-27.md` |
| 28 Aug | "This board absolutely needs to have him, his connections, and his patents on file." (Pais) | `notes/PAIS-PATENTS-2026-08-28.md` |
| 28 Aug | **"I want to not just have this be a conspiracy brain item but something I can put in front of respectable individuals and not have them immediately dismiss it."** And, when told the disconfirming NAWCAD result would go on the node: "No you're doing it right." The note adds that his personal views on Pais are "his commentary rather than the board's content" and should go on as Tier 3 | `notes/PAIS-PATENTS-2026-08-28.md`; `notes/HANDOFF-2026-08-28-pais.md` s8 |
| 28 Aug | The five observables are "key to this whole thing" | `notes/HANDOFF-2026-08-28-pais.md` s2 |
| 28 Aug | Asked "whether it matters that this repo has no CI, whether it is a problem, and whether it is easy to fix" | `notes/GATE-PORTABILITY-2026-08-28.md` |
| 29 Aug | **"I clicked on grusch or someone and instead of our orthogonal map it gave me this which is I think the style from the vanishing. I actually think I like this better ... it shows the connections better than the orthogonal one which I like but when a subject is clicked you can't see all the connections like you can here"** / "Maybe the orthogonal map becomes its own tab that's just the whole map so you can see it while our primary map is in the style in the screenshots below, where the analysis tab sends you" | `notes/HANDOFF-2026-08-29-MAPS.md` s1 |
| 29 Aug | Patents mockup: "for now this is fine" (twice); observables: reuse them elsewhere, "call it observables or something"; drawings: "Thumbnails I think. Do whatever you think would look best." | same, s5 |
| 29 Aug | "The FOIA will have to happen way later but keep them there and ready. In fact integrate them into the board somehow." | `notes/FOIA-LAYER-2026-08-29.md` |
| 29 Aug | "unless there's some reason not to, save our work after any big changes... especially if I ask for a session handoff." | `CLAUDE.md` s4 |
| 30 Aug | Approved the sixteen-node candidate list: "Yes build it" | `notes/HANDOFF-2026-08-30-EVENING.md` s2 |
| 30 Aug | "when I click tom delong, I would expect to see connections to the stars academy, tom delong, mcCasland etc etc but instead it labels nothing. This defeats the purpose" | `notes/LABELS-2026-08-30.md` |
| 30 Aug | **"I'm so torn because I like the look of this, but the nodes are just geometry with occasional white text, they need to be boxes like the names like DeLonge etc are or something. I think we really need design to think this through again."** / "I also don't like the plain white labels we have everywhere, maybe they need a background or something." / "clicking the various filters doesn't really materially change or highlight anything." / **"if you need it to rethink this entire map knowing what we've built and what we now know, let's give it the chance to redo it in a way that allows us to have this much data plotted without making it useless and all noise."** | `notes/DESIGN-BRIEF-2026-08-30-NETWORK.md` s3 |
| 30 Aug | "not a single node is named… the white text scales as you zoom and never lands on anything." | `notes/HANDOFF-2026-08-30-NIGHT.md` s2 |
| 30 Aug | Backlog from his screenshots: patent drawings "not clickable to full screen", wants Design "to eventually recreate the schematics"; Analysis panel "the area in the white is squished to the left and doesn't make use of the blank space"; wants more than the 34 analysis examples | `notes/HANDOFF-2026-08-30-EVENING.md` s5 |
| 30 Aug | Eric Davis "has later/recently come out in interview and said the Wilson-Davis memos were all true etc so we don't have to speculate anymore." He then accepted the board's classification and "notes the UFO community treats it as all but confirmed" | `notes/HANDOFF-2026-08-30-EVENING.md` s6; `-NIGHT.md` s5 |
| 2 Sep | **The network map at 1,027 nodes is "a thousand dots that mean nothing"; the white labels never land on what they name; the patents sheets are not grouped or openable; the Analysis tab "was computed for a board of fifty things"; "rethink this entire dashboard, if you think we should scrap stuff and start over, I'm down. I want the best possible end product so I can share this with my research friends as a tool that's useful."** | `notes/RETHINK-2026-09-02.md` opening |
| 2 Sep | Decisions: public; the name **The Legacy Program Research Terminal**; a hosted site with dependencies and runtime data files rather than a single file; build what Design specified (recorded decisions) | `notes/APP-SPEC-2026-09-02.md`; `notes/NEW-SHELL-2026-09-03.md` |
| 2 Sep | Blanket approval: "I'm good with all decisions" | `research/leads/CANDIDATES-2026-09-02-AREA52.md` |
| 3 Sep | "go get it" | `research/leads/CANDIDATES-2026-09-03-DANNYJONES.md` |
| 3 Sep | Showed the usage panel ($30 session, Fable 71%) and asked how to keep performance and cut cost; produced the token-economy rules | `CLAUDE.md` s4; auto-memory `token-economy-rules.md` |
| 3-4 Sep | The back button was "Stewart's one condition before cutover"; on driving it: "this is just perfect" | `notes/NEW-SHELL-2026-09-03.md`; `notes/HANDOFF-2026-09-04.md` s1 |
| 4 Sep | "Stewart wants Audio Overview podcasts of the board." The export's prompt: "Take the angle that the recovery programme is real and the denials are the cover story, and tell it that way for entertainment," with two hard rules (say the tier aloud; never invent) | `notes/HANDOFF-2026-09-04.md`; `exports/notebooklm/README.md` |
| 4 Sep | "You own the repo end to end" (auto-memory only; no repo note carries it) | auto-memory `the-program-repo-audit-role.md` |
| 11 Sep | **"Right now the analyst is just used by me so for now I'm not worried about anything regarding restricting it too much. If I make it public it will be bring your own key. I want it to be basically able to answer any question I would ask here and be able to sift across the data to reason across the dataset, understand the timeline etc."** Answers: no daily spend ceiling; leave effort `high` and the 60/min global limit; yes to the one-hour cache; custom domain "Not answered" | `notes/ANALYST-TOOLS-2026-09-11.md` opening and s3 |
| 12-18 Sep | Handed over the tier decision: "make whatever decision you think would be best for our project" | `notes/TIER-SCOPE-2026-09-12.md` s4a |
| 18 Sep | **"You have full authority to make decisions, treat this project as your own... However you think is right, do that."** Goal, as the session recorded it: "a database of all the players, entities and patents that documents the programme and those claiming, or thought, to be involved" (recorded paraphrase; no note carries the goal inside quotation marks). Also wants the next sessions on Opus 5 to save credits | `notes/HANDOFF-2026-09-18.md` s1 |
| 18 Sep | Wants 3D models of reported craft (Meshy AI), starting with McCandlish's "Fluxliner", "as relevant eye candy on the board and eventually as something he can 3D print" (recorded paraphrase) | same, s3a |
| 18 Sep | **The hub rule, "His words, paraphrased: if ten people make claims about a place, one diagrams it and one says he worked there, the network map must show that convergence as a set of connections into that place's node, so a reader sees a node with a lot going on and asks what is happening there."** Ruling: "a historically notable claimant goes on the board REGARDLESS of tier, graded honestly, with the case against on the same node." (session's rendering) | same, s3b |
| 18 Sep | Long term, a visual evidence pass: "every node's detail page gets whatever relevant visual material exists, so the board is not just text." (recorded paraphrase) | same, s3c |
| 18 Sep | **"I don't want this to be just about the program because that would be incomplete without all the major whistleblowers and people who have testified to Congress about UAP since that's some of the primary evidence we have about the whole thing."** On Ryan Graves: "He isn't himself in the program." | `notes/HANDOFF-2026-09-18-NIGHT.md` s4a; `notes/CENTRALITY-2026-09-18.md` s5 |
| 18 Sep | Job order, recorded as "His words: do the centrality fix first, then TR-3B, then the rest in the order given. On the red check, option 1. The propulsion strand is worth a pass." | `notes/HANDOFF-2026-09-18-EVENING.md` s2 |
| 18 Sep | Confirmed American Alchemy and Jesse Michels are the same channel. Passed a Reddit patent "with the correct caveat that the thread is unreliable"; rules out Alcubierre on his own reasoning (bending spacetime above a building "would have effects nobody could conceal", recorded paraphrase) | `notes/HANDOFF-2026-09-18-EVENING.md` s6; `notes/PROPULSION-CLAIMS-2026-09-18.md` |
| 19 Sep | "make decisions in my absence you have full control" | `notes/HANDOFF-2026-09-19.md` update |
| 19 Sep | Handed the layout check to Design and **declined excluding the hubs from L0**, "on the grounds that it hides them from the map and defeats the rule"; denial weighting: "do it next session, measured" | `notes/PACKED-LAYOUT-INK-2026-09-19.md` s6; `notes/HANDOFF-2026-09-19.md` s2, s4a |
| 19 Sep | **"this is literally the most secret program since the Manhattan project... we have to find a way to document even loose evidence like testimonies just to make sure we are documenting the programs history, including claims made about it."** The triage note's paraphrase of his position: applying ordinary scientific proof thresholds "guarantees failure"; "The goal is to get all the witness claims on the board, tagged by tier, and then see where the connections lead." | `notes/HANDOFF-2026-09-19-LATE.md` s3; `notes/TRIAGE-RULE-2026-09-19.md` s2 |
| 19 Sep | **On the map: it "is mostly a cool visual at this point but with how dense this will eventually get I feel like we'll have to rethink it at some point anyways. Perhaps there is a better way to display or group it."** | `notes/HANDOFF-2026-09-19-LATE.md` s3; comment in `tools/build_l0.py` |

### 1b. What he wants, by theme (synthesis of 1a)

| Theme | What the record shows |
|---|---|
| Usability | Fit must show the whole map, not numerals; auto-fit until the first interaction; panels must not cover the map; obvious collapse affordances on a curve; one panel on selection, nothing floating over the map; a back button; clicking a node must show AND NAME its connections; labels need a background or a box; filters must visibly change something. Most of these were reported from the live site, not from mockups |
| The maps | He likes the orthogonal program map's look and says it "shows how robust our connections are"; he likes the force graph for seeing a selected node's connections and the animated, coloured, directional lines. The RETHINK records "the two things Stewart asked to keep, the orthogonal look and the animated lines". By 19 Sep the top-level map is "mostly a cool visual" and he expects a rethink: "a better way to display or group it" |
| Discovery | 14 Aug: "no opportunity for discovery, nothing visually identifying what the important connections are". 18 Sep: a hub "with a lot going on" should make a reader ask "what is happening there". 19 Sep: tag every claim and "see where the connections lead" |
| Sharing, audience | "share this with my research friends as a tool that's useful" (2 Sep); public (2 Sep); credibility with "respectable individuals" (28 Aug). The RETHINK's articulation of research friends (session's words): "people who already know the subject, want to check a specific thing, and will not read a manual", with seven jobs: look up by name, see connections and WHY, follow a thread, check a date or era, send a link, ask a question, take a brief away |
| Public vs private | Site public in principle since 2 Sep, but no launch: no custom domain, landing page gated on an undefined "1.0", analyst on his own key with no spend ceiling; "If I make it public it will be bring your own key" (11 Sep). Transcripts never published; licensing of images and drawings is his call |
| The analyst | "answer any question I would ask here ... sift across the data ... understand the timeline" |
| Podcasts | NotebookLM Audio Overviews of the board, pro-programme angle "for entertainment", tiers spoken aloud, nothing invented |
| Scope | Whistleblowers and congressional witnesses (18 Sep); notable claimants regardless of tier, claimants joined into the thing claimed about (18 Sep); "loose evidence like testimonies" (19 Sep); Pais and his patents (28 Aug); the five observables, reusable (28-29 Aug); FOIA integrated (29 Aug); 3D models and visual evidence (18 Sep) |
| Database goal | "a database of all the players, entities and patents that documents the programme and those claiming, or thought, to be involved" (recorded paraphrase, 18 Sep) |
| Authority | Escalated from "I'm good with all decisions" (2 Sep) to "full authority" (18 Sep) and "full control" (19 Sep). The harness still requires his yes in chat for any push to master, because it is a production deploy |
| Working style | "He is technical, direct, and reads carefully" (`notes/HANDOFF-2026-08-25-claude-code.md` s7) but "not a programmer" (auto-memory); cannot read JSON; tables over lists; no em dashes; every command block starts with its own quoted `cd` (corrected three times on 26 Aug) |

---

## 2. Principles in force

Judgement key: **ESSENTIAL** keep in any redesign; **JUSTIFIED** keep unless the redesign changes
its premise; **ACCIDENT** a historical artefact a redesign could revisit.

| Principle | Origin | Judgement |
|---|---|---|
| No invented sources, URLs, document numbers or quotes, including in mockup copy and placeholders | `notes/RESEARCH_LOG.md` 12 Aug ("The one thing that does not bend"); every Design brief | ESSENTIAL. The whole product's credibility rests on it; 604 quoting claims were substring-checked and none was invented (`notes/HANDOFF-2026-08-25-audit.md`) |
| Claim tiers 1-3 as "ammunition grading, not hedging"; an automatic honesty pass demotes Tier 1 claims without a primary record | `notes/RESEARCH_LOG.md` 12 Aug | ESSENTIAL. The implementation's node-scoped primary-URL test is a known flaw (`notes/TIER-SCOPE-2026-09-12.md`); option C (claim-scoped, identifier-aware) is open |
| AARO and DoD sources cap at Tier 2 unless the claim is about what they said; applies to edges since 1 Sep | commit `0ae5e89` about 13 Aug (`notes/DESIGN-BRIEF-L0-MAP.md` s5); edges via `notes/AUDIT-FABLE-2026-09-01.md` finding 2 | ESSENTIAL |
| A denial is data about the denier; denials recorded in full "as artifacts of the concealment effort" | `notes/RESEARCH_LOG.md` 12 Aug | ESSENTIAL as a record; see the stance row below for how it evolved |
| Denial in three states: directed (denier named), undirected, association; adjudicated once in `data/denial-adjudication.json` | Design 24 Aug s3; `notes/DENIAL-ADJUDICATION-2026-08-26.md` (the old `a`-end convention was wrong on 27%; 22 of 47 map arrowheads pointed the wrong way) | ESSENTIAL concept. ACCIDENT in storage: `denialKind`/`denier` cannot be written in research files and are silently inert there (`notes/DENIAL-WEIGHT-2026-09-19.md` s4a) |
| Editorial stance: presume the programme exists; "Do not write balanced both-sides prose. Do not append skeptical disclaimers." | `notes/SESSION-HANDOFF-2026-08-12-cloud.md` | Evolved, and the evolved form is what is in force: tag, do not exclude; "The case against is an edge too ... A hub with only believers on it is a false picture" (`notes/HANDOFF-2026-09-18.md` s3b); Castello was caught only "because this board tags rather than excludes" (`notes/TRIAGE-RULE-2026-09-19.md`). The x4.0 denial weight is "the stance encoded as arithmetic" |
| Node tiers A/B/C = proximity to the programme, not credibility, by forced percentile 15/35/50; PROGRAM_EDGES x3.0, denial x4.0, unsourced nodes forced to B | `notes/DASHBOARD_PLAN.md` s3.3, 12 Aug: wave 1 had "553 of 911 nodes are Tier A - 61%" because fourteen agents graded within their own domains | ACCIDENT, revisit. Zero-sum, shares three colours with claim tiers ("a known weakness", `CLAUDE.md` s6), contested in practice (Graves), invisible in search (which ranks on claim tier), yet it drives L0 selection and the analyst index. Two scoring defects in two days (witness-chain in x3; denial x4 paying for scholarly refutation) |
| Three axes C/A/D, 0-3, "never summed" | `notes/SESSION-HANDOFF-2026-08-12-cloud.md` | JUSTIFIED; lightly used in the UI (three bars on the node page, band ordering by mean C) |
| Size never encodes importance ("Position is available. Size is not.") | `notes/DESIGN-BRIEF-L0-MAP.md` 13 Aug ("Size on this map means implicated, not authoritative"), hardened in `notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md` s4 and Design's channel table 24 Aug | ESSENTIAL in spirit (AARO would be the biggest node). Inconsistently applied: L0 membership is a degree floor and, since 19 Sep, a degree-ranked budget (`tools/build_l0.py`: "Membership competes on degree"), and 18 Sep allows degree to mean "a lot is claimed here, never this is true" |
| One label size; labels chosen by space, never by rank; skip, never shrink or truncate | Design's 30 Aug changes 1-3 (`notes/DESIGN-BUILD-2026-08-30.md`), which found the board already degree-gating names (`PLATE_DEGREE`, `LABEL_DEGREE`); `notes/DESIGN-RESPONSE-SHELL-2026-09-02.md` s2.2; checks C2, C4 | ESSENTIAL as honesty, but it is the binding constraint behind both "a thousand dots that mean nothing" (17 of 1,027 named) and the L0 size limit. Keep the rule, change the unit that is drawn |
| No anonymous marks: what cannot be named is counted, not drawn | Design 24 Aug (`overview_is_never_anonymous`); `notes/DESIGN-BRIEF-SHELL-2026-09-02.md`; check C3 | ESSENTIAL. It is the direct answer to Stewart's complaint |
| Motion only where attested: a particle only on the selected node's edges (running away from the reader) or on a directed denial; static at rest; `e.pair.flip` must never steer a particle | Design 24 Aug ("A moving dot is a far stronger implication than a static line"); `notes/MAP-INVERSION-2026-08-29.md` s4; `notes/SELECTION-2026-08-27.md` | ESSENTIAL, and compatible with Stewart's liking for animated lines |
| Position means something: X = era (four columns plus NO DATE), Y = function band by "rarest tag wins", bands ordered by measured mean C; `concealment` "is the field, not a row" | Design 24 Aug s1 | JUSTIFIED but fragile: near-tie tags swap rank (the rarity pin was re-pinned 19 Sep with a caution); two bands are residuals, not categories |
| The map is of the programme, not of people: L0 admits only institution, program, event, legislation and document above a floor | Stewart 13 Aug; `tools/build_l0.py` `STRUCTURAL` and `PROMOTE_DOCUMENTS` | JUSTIFIED origin, ACCIDENTAL consequence (verified 24 Sep): locations and people can never reach L0, so the place hubs `s-4-papoose-lake` (degree 16) and `dulce-base` (degree 15) and every claimant are off the top-level map; the "Start from a witness" entry path has 7 nodes and 0 on the map (`app/public/data/map.json`) |
| Aggregation, not filtering: a summary "states its own contents and expands on demand"; aggregated edges carry the count and the strongest claim tier | `notes/PERF-AND-DENSITY-PLAN.md` Part 5; `notes/DESIGN-BRIEF-L0-MAP.md` constraint 4 | ESSENTIAL. It is the board's answer to "what got cut" |
| Derived pairs (shared employer, location, domain) visually separate from hand-written sourced edges | Inherited credibility rule (`notes/DESIGN-BRIEF-L0-MAP.md` constraint 3); Design Q5 of 30 Aug never answered | ESSENTIAL. 1,747 of 3,941 drawn links on the old network map were derived |
| L0 floor of 6 distinct neighbours, then a BUDGET of 135 with the 14 highlights admitted by right | `notes/L0-IMPLEMENTATION-2026-08-13.md`; `tools/build_l0.py` 19 Sep | ACCIDENT and self-declared STOPGAP ("The real answer is a different top-level surface, and that is a Design question, not a constant.") |
| Start-here pointer: 14 editorial flags in amber, offset from the chip, never more than 15% of the map, each with a reason | Design 24 Aug; signed off 25 Aug | JUSTIFIED. The accident is C11 binding them to individually drawn chips |
| Entry paths are QUESTIONS computed at build time ("Follow the money", "The custody chain", "Who denied what", "The legal mechanism", "The foreign counter-examples", "Start from a witness") | `notes/L0-IMPLEMENTATION-2026-08-13.md` Stage 12, 14 Aug | ESSENTIAL for discovery |
| Threads: authored ordered chains, every consecutive pair joined by a board edge, evidence line quoted from the edge or a claim | `notes/RETHINK-2026-09-02.md` s4; `notes/APP-SPEC-2026-09-02.md` s5; verify check with seven poisons | ESSENTIAL. Eight exist: lineage, custody, money, denials, wilson-davis, patents, scientists, oversight |
| Entity first, map second; every node a page with an address; deep links on every state | `notes/RETHINK-2026-09-02.md` s4 | ESSENTIAL ("Deep links are the single feature that makes the board shareable") |
| Content lives in gate-checked data files, never typed into a renderer | `notes/PATENTS-TAB-BUILD-2026-08-29.md` s1 | ESSENTIAL |
| Runtime fetch allow-list: same-origin `/data`, `/patents`, `/fonts` and the analyst Worker only (C14); fonts self-hosted | `notes/APP-SPEC-2026-09-02.md` s1; `notes/FIRST-PAINT-2026-08-26.md` (a Google Fonts link blocked first paint for 12.4 s) | JUSTIFIED |
| A check that has never been shown to fail is a broken check; every check ships with a poison; poison the page, not only the predicate; reading the source is not verification | `notes/PERF-AND-DENSITY-PLAN.md` Part 1, 12 Aug; `CLAUDE.md` s5 | ESSENTIAL as discipline. The cost: checks were written against display thresholds (pixel-ink ratios, viewport height) on a shell nobody sees, and those checks now block research |
| An independent audit must restate a rule, never import it | `notes/L0-IMPLEMENTATION-2026-08-13.md` Stage 10; `notes/HANDOFF-2026-09-19-LATE.md` s5b | ESSENTIAL |
| Notability is a second, parallel admission criterion; grading unchanged; the anchor is the dated artefact of the claim; every notability node records how the claim reached us | `notes/TRIAGE-RULE-2026-09-19.md`; `CLAUDE.md` s2a | ESSENTIAL (Stewart's scope) |
| The hub rule: the thing claimed about is a node and the hub; every claimant gets an edge INTO it; the edge says what kind of claimant; the case against is an edge too; degree may mean "a lot is claimed here", never "this is true" | `notes/HANDOFF-2026-09-18.md` s3b | ESSENTIAL. It is the clearest answer on record to "not a sea of nodes without meaning". Under-modelled: no craft or claimed-site class (`arv-fluxliner` built as `cls: program` because "the board has no craft class", `notes/ARV-BUILD-2026-09-18.md` R1); claimant kind lives in note prose "for now" |
| `witness-chain` is not a structural edge (out of the x3 set) | `notes/CENTRALITY-2026-09-18.md` | JUSTIFIED |
| Tier strictly dominates search ranking | `notes/HANDOFF-2026-09-12.md` s4 | JUSTIFIED |
| The analyst's tools run in the reader's browser; the Worker holds no copy of the board; the cited-id guard flags and never edits; no board counts in prompts | `notes/ANALYST-TOOLS-2026-09-11.md` s6 | ESSENTIAL |
| Transcripts are never committed or published | `notes/NEW-SHELL-2026-09-03.md`; `notes/HANDOFF-2026-09-03.md` s4 | ESSENTIAL (copyright) |
| An image URL, a drawing or a 3D model is a sourcing claim; captioned as whose account it depicts; seals never altered, evidence images never cropped | `notes/WANTS.md` 12 Aug; Design 24 Aug; `notes/HANDOFF-2026-09-18.md` s3a, s3c | ESSENTIAL |
| Two agents agreeing is not corroboration when they share a method | `notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md` s7; load-bearing from 19 Sep | ESSENTIAL |
| Podcast claims read "On <show>, <date>, <speaker> said ...", Tier 2, never asserted as fact | `notes/HANDOFF-2026-09-01.md` s8 | ESSENTIAL |
| No layout change without a mockup at 1366, 1920 and 2560 shown to Stewart ("the last three layout changes that were built directly were all wrong on the first cut") | `notes/HANDOFF-2026-08-26-UX.md` s3 | JUSTIFIED |
| "The map is Design's": its interaction model is not changed without Design | `notes/MAP-CELL-PANEL-2026-09-12.md`; `CLAUDE.md` s4 | ACCIDENT in effect: it froze issues everyone could see (cell panel, bridge, network brief Q1-Q5 never sent) |

---

## 3. Do-not-undo list

### Research corrections the records forced (un-correcting them re-introduces a known error)
- `sapoc` established 5 January 1994 (Deutch chair), not 1 July 2010. `notes/HANDOFF-2026-09-03.md` s4
- ATIC redesignated 1959, discontinued 1 July 1961 with FTD constituted the same day; "ATIC became FTD" is wrong. same
- CENTER LANE's office was the Security Support Detachment; Bluegill 25 October, no debris; Inman never headed SAIC; the Church Committee never examined agency files itself; the Oversight letters say "at least ten" and "began in 2023". same
- The nitinol lineage carries the NOL record beside the Battelle allegation (NASA SP-5110, NOLTR 61-75, patent filed 1 December 1961). `notes/HANDOFF-2026-09-03-EVENING.md` s4
- `wilson-davis-memo` is typed, not handwritten, and two pages are Miller's letter; ARPA's first Director was Roy W. Johnson; Cabell was at USAF Intelligence, not CIA, when Blue Book launched; Army SAP office September 1984; GRILL FLAME to INSCOM 11 February 1981; DRAGOON ABSORB. same
- Lockheed unaccounted-for total is 11, not 17 plus 46; Moon Dust 49/17 are deorbit notifications received, not objects recovered; JANAP 146 carries no dollar figure (18 U.S.C. 793 does); neither Brown patent claims anti-gravity; Winterhaven contains no saucer. `notes/HANDOFF-2026-08-30-EVENING.md` s2
- The transcript claims that records contradicted are findings, not errors to fix back toward the podcast (Bluegill, Inman/SAIC, the Church Committee, Silver Bug). `notes/HANDOFF-2026-09-01.md` s3a; `CLAUDE.md` s9
- `lanl` connection to Lazar is "named in a directory", NEVER "employed by"; "Lazar pleaded guilty in 2006" is wrong twice (the company pled, in 2007). `notes/HANDOFF-2026-09-19.md` s3d
- Davis: authorship of the notes confirmed, the meeting not; Wilson still denies. `notes/HANDOFF-2026-09-01.md` s6
- The five observables cap at Tier 2, attributed to Elizondo; "Four out of five, never five" in the Pais mapping. `notes/HANDOFF-2026-08-28-pais.md` s5; `notes/PATENTS-TAB-MOCKUP-2026-08-29.md` s3
- NSC 10/2 is already carried in substance by `cia-office-of-policy-coordination`: never build a node that re-quotes it; NSAM 303 belongs on the board as a correction, not as spine. `notes/HANDOFF-2026-09-19-AFTERNOON.md` s7
- The four tier-scope demotions are deliberate (two are "conservative rather than correct"); `william-l-moore` and `the-roswell-incident-1980` carry byte-identical claim text, so edits there must be scoped by node id. `notes/TIER-SCOPE-2026-09-12.md` s4a; `notes/HANDOFF-2026-09-18.md` s5

### Modelling decisions (each looks like something missing)
- No `robert-sarbacher` to `research-development-board` edge; no Trimble-recruited-Witten edge; no BDM-to-Northrop edge; `sperry-rand` deliberately unattached (MacArthur has no node). `notes/HANDOFF-2026-08-30-EVENING.md` s2
- No Lemnitzer, York, Goldberger, Garwin, Jafari, Snowbird, Norton or Lovekin nodes; the `sperry-rand` edge to the Talbert series does not create a MacArthur edge. `notes/HANDOFF-2026-09-03-EVENING.md` s4
- No edge from Pais to AATIP, AAWSAP, KONA BLUE, any DIRD or any custody chain ("Drawing that edge is the thing that would get this board dismissed"). `notes/HANDOFF-2026-08-28-pais.md` s7
- The King patent (US 3,322,374) does not go into the Pais patents view. `notes/PROPULSION-CLAIMS-2026-09-18.md` s4
- ARV build rulings: a hub node for the claimed craft; James Allen death claims excluded; the National Press Club 9 May 2001 appearance is not a claim; the Brown edges must not imply anti-gravity; Sorensen disowning the drawing is a claim. `notes/ARV-BUILD-2026-09-18.md` s2
- `jason-turner` deliberately not given the Navy FOIA releases (they document the incident, not the confiscation). `notes/THIN-SOURCING-2026-08-27.md`
- `ben-rich` exists: enrich, never build (five duplicate people got on the board that way); check existence by canonical id before any build. `notes/HANDOFF-2026-09-18-NIGHT.md` s5
- American Alchemy is Jesse Michels: identify episodes by video id, no separate node. `notes/HANDOFF-2026-09-18-EVENING.md` s6
- Do not "fix" the nuclear blocker by trimming the nuclear cluster ("shaping research to fit a display measure is backwards"). `notes/HANDOFF-2026-09-19-LATE.md` s1
- Do not exclude hubs from L0 to force a check green (Stewart declined it). `notes/PACKED-LAYOUT-INK-2026-09-19.md` s6
- `dateEnd` absence on extant institutions, statutes and documents is correct; do not backfill. `notes/DATE-EXTENT-2026-08-26.md`
- Do not "fix" `gao-130581`'s truncation by shortening the document's real title. `notes/HANDOFF-2026-08-30-EVENING.md` s7
- "Same source, different tier" is normal (102 sources over 706 claims); never write a check on it. `notes/TIER-SCOPE-2026-09-12.md` s5

### Scoring
- `witness-chain` stays out of `PROGRAM_EDGES`; claim-tier weighting of the degree counters is rejected on measurement: "Do not re-propose it without a new argument". `notes/CENTRALITY-2026-09-18.md`; `notes/HANDOFF-2026-09-18-EVENING.md`
- The `s *= 0.35` unsourced discount and the explicit `new == "A"` demotion are two halves of one rule; `verify.py` asserts a Tier A node has a sourced URL. `notes/HANDOFF-2026-09-18-EVENING.md` s3c
- `GOLDEN.json` moves only through `verify.py --update-golden`, never by hand; `merge.py` and `regrade.py` share `canonical_id`, do not fork it. same
- The denial x4.0 constant is not in question; the directed-only variants fail (eight documented nodes fall) and must not ship. `notes/DENIAL-WEIGHT-2026-09-19.md` s3, s6
- Rarity pin: at a 3% gap, do NOT re-pin again on another 2-count margin. `notes/HANDOFF-2026-09-19.md` U5
- The tier/axes silent-overwrite audit and the `_corrections.json` audit are closed; do not re-open without a new mechanism. `notes/HANDOFF-2026-09-19-AFTERNOON.md` s2, s5

### Visual and interaction rules
- The particle rule governs the default surface; `e.pair.flip` must never steer a particle. `notes/HANDOFF-2026-08-30.md` s4
- Size never encodes importance; a spinning 3D model goes on the node's own page, never Home or the map. `notes/HANDOFF-2026-09-18.md` s3a
- The label threshold 0.62 stays: at k=0.63 the label is 4.69 CSS px on a 1x monitor; screenshots at deviceScaleFactor 2 flatter small text. `notes/SHELL-2026-08-27.md` s8
- Nothing may take height from `.map-root` or `.hood` (about 7 px of clearance at 1920 on CI). `notes/ANALYST-TOOLS-2026-09-11.md` s6
- The back button calls `history.back()` only and never writes `location.hash`. `notes/HANDOFF-2026-09-04.md` s4
- Panels fold via registered `@property` lengths to a labelled 30 px spine, never `display:none`; `applyChrome` is the single owner of the rail's chrome (old shell). `notes/HANDOFF-2026-08-27-shell.md` s4
- `test_packed_layout.js` drives the PROGRAM tab and is never weakened ("If it goes red, fix the map, not the check"). `notes/HANDOFF-2026-08-30.md` s4; wording from `CLAUDE.md` s9
- `walk.js` is a camera and "must never enter the gate"; do not chase the cell-panel overlap count to zero. `notes/SHELL-2026-08-27.md` s7; `notes/MAP-CELL-PANEL-2026-09-12.md`

### The analyst
- Tools run in the browser, not the Worker; thinking blocks relayed untouched; all tool results in ONE user message; one cache breakpoint that moves; `TOOLS_VERSION` in two files, bumped only when a tool's shape changes; no board count in the prompt, state blocks or tool descriptions; a thread report cites only the authored thread file or a board edge source (C21); the cited-id guard flags and never edits. `notes/ANALYST-TOOLS-2026-09-11.md` s6; `notes/HANDOFF-2026-09-12.md` s4
- `data/analyst-suggestions.json` is Stewart's: chips change through a table in chat; when a build moves a quoted count, update the numerals only, never the wording, and tell him. `notes/HANDOFF-2026-09-18-EVENING.md` s8

### Build, deploy, infrastructure
- `build_l0.py` uses its own `_sin`, `_cos` and `sqrt` of a sum, never libm (one ulp between MSVC and glibc produced two maps and kept CI red a day); forward-slash source path. `notes/HANDOFF-2026-09-03-EVENING.md` s4
- `gate.yml` uploads rebuilt artifacts when reproducibility fails. same
- `build_app_data.py`'s fingerprint is content-only (CRLF-normalised bytes, no git id, no mtime); no `-I` flags on the app job's diff. `notes/HANDOFF-2026-09-04.md` s4
- `_headers` gives `/data/*` `no-cache`, not `immutable`; `_redirects` are 302s. same
- Never deploy the repo's `dist/` (it held transcript exports); `test ! -d dist/transcripts` guard. `notes/NEW-SHELL-2026-09-03.md`
- `research/_edge_tiers.json` is the edge adjudication record; a red check after a research pass is answered by a line there, not a weaker check. `notes/HANDOFF-2026-09-01.md` s5
- `corpus_crosscheck.py`'s alias rules are self-tested; do not loosen them to shorten a list ("A false NODE deletes a lead"). `notes/HANDOFF-2026-09-03.md` s4
- Default late: absence stays `None` until `finalise_defaults()` runs, so load order cannot decide a field; the guard in `audit_independent.py` restates the rule. `notes/SILENT-DEFAULTS-2026-09-19.md` s4, s5
- Every denial edge gets a verdict in `data/denial-adjudication.json`. `notes/DENIAL-WEIGHT-2026-09-19.md` s4
- A thin entity enrichment must carry `cls` (and, before the default-late fix, `cluster`). `notes/HANDOFF-2026-09-19.md` U3, s4b
- Playwright pinned at CI's version. `notes/HANDOFF-2026-09-12.md` s1

### Process
- Commit and push often; a handoff request means commit and push first; `git fetch --all` BEFORE reading a handoff. `CLAUDE.md` s4
- Never merge a branch's own reverted history back into it; revert the revert on the target. `notes/HANDOFF-2026-09-19-LATE.md` s5b
- `capture_strip.js` runs immediately before `audit_independent.py`, every time. same
- Design briefs are self-contained, on master, never pointing at files over the 1 MB API read cap. `CLAUDE.md` s4; `notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md` s0

---

## 4. Recurring failure modes and process costs

### 4a. The classes, with instances

| Class | Instances (date, file) | Cost |
|---|---|---|
| **Silent drops and silent defaults**: data never reaches the board and the build stays green | 35 dates nulled on every rebuild (12 Aug, `QA-PASS-2026-08-12`); five people on the board twice (12 Aug); FY2024 sec. 1687 three times (22 Aug, `DUPLICATES`); nothing read `REJECTS.json`, 30 claims lost, `waived-usap-mechanism` at 0 claims (25 Aug, `SILENT-REJECTS`); `norm_source` discarded 732 bare-string sources (25 Aug); Pais's 19-entry patent timeline absent since researched (2 Sep, `AUDIT-FABLE` s2b); a 120-character dedup key collapsed claims; a hardcoded "yankee blue" filter "was removing the corroboration, not the error"; records without `cls` dropped (30 Aug: 7 records, 22 claims; 19 Sep: 11 Lazar enrichments); fill-if-falsy defaults: 267 nodes on the wrong `cluster`, 24 people shipped `active` including Harry Reid and Gerald Ford (19 Sep, `SILENT-DEFAULTS`); dates losing precision to filename order (14); `denialKind` inert in research files; the layout generator's main guard never fired on Windows, so "Every earlier Windows build of the layout model was a stale file" (2 Sep); the 820 px timeline patch never applied for a month (1 Sep) | Correctness, and trust in every count |
| **Checks that pass while broken** | `canvasInk` never fired (12 Aug); "Three of eight checks were born broken", later "Six of six"; the scripted-analyst test passed while six of seven chips misrouted (24 Aug); an overflow test returned zero while the dossier clipped every line; `head-row-clear`'s self-test read a default; C18 to C21 "each ... was wrong before it was right" (12 Sep); `check_rebuild.py` "does not rebuild" and printed success over eleven stale artifacts (30 Aug); the backfill-queue check only asserted one direction; `walk.js` reported 33 false overlaps; `fitChipInk` is a whole-canvas colour histogram at an uncontrolled camera (19 Sep) | The gate grew to roughly 250 assertions, each needing its own poison, and several now measure display artefacts rather than meaning |
| **Inherited surfaces** from The Vanishing | Scripted analyst answering about JPL headcount; `explainEdge` captions from the other project ("Both left the same category of personal item behind"); 3 KB of the sibling's sceptical `COUNTERS`; a "Left behind" section naming two missing persons; the Google Fonts link that blocked first paint for 12.4 s; the page title's subtitle; a particle on every edge flowing along time; degree-gated names (`PLATE_DEGREE`, `LABEL_DEGREE`); filters that were additive reveals (Tier A took the map from 501 visible nodes to 956); 463 of 980 nodes at 1% opacity at rest; a 0.12-per-frame fade with no last frame, mis-called "a flake" for three sessions; two map implementations, one dead, and a patch applied to the dead one; four patch modules of "about 6,000 lines of Python strings containing JavaScript" | Most of Stewart's complaints from 14 Aug to 2 Sep. Production retired the shell on 4 Sep, but its gate still runs in CI and still blocks research |
| **Unmerged work and stale handoffs** | Branch `claude/status-update-bewtdk` held 19 commits off master (21-25 Aug); PR #5 held all of 26 Aug as a draft ("an unmerged PR is invisible to the next session"); PRs #12/#13 stacked; `arv-regrade` 13 commits; `nuclear-2026-09-19` still unmerged; "every handoff this project has written went stale while continuing to read as confident" (25 Aug); 40 minutes re-deriving pushed work because nobody ran `git fetch` (29 Aug); `CLAUDE.md` pointed at the EVENING handoff a day after NIGHT (1 Sep) and today points at 18 Sep while 19 Sep is current (verified); the auto-memory says master `d545a79`, it is `838c134` (verified); command blocks in handoffs still cite the retired OneDrive path; an OOM fix "measured three hours earlier and never reached a commit" (30 Aug); research committed without running the pipeline turned master red (30 Aug) | Hours per session re-deriving state; decisions made on stale facts |
| **Red master from checks not run locally** | `state_snapshot.py --gate` does not run the app's C1-C21; the 19 Sep run went red on C11 in CI and master was reverted (`STATE-2026-09-19`); CI red all day on 3 Sep over one libm ulp; red twice on 4 Sep over a CRLF fingerprint; rapid pushes cancel the ~23 minute gate | A revert of a whole night's research; a day of red CI |
| **Layout at size limits** | 1366 never fits labels; label type at fit was 3.6 px at 1366, 4.7 px at 1600 and 5.9 px at 1920 on the old shell (27 Aug); "a constant standing in for something that varies" (three times on 26-27 Aug); the dossier at half the viewport (182 characters per line at 2560); the analyst dock could take no height (7 px clearance at 1920 on CI, whose fallback font wraps two more rows); L0 137 to 149 pushed the map out of label mode (54 rows need 1008 px of 938); the budget caps count but not label width (C5 headroom 56 px to 20 px with L0 unchanged); `fitChipInk` versus first-of-kind nodes | The top-level map cannot absorb growth, and each new kind of object is a potential red gate |
| **Confident generalisation from two or three points** | "You cannot reach the layout threshold by building more" (wrong); "`runtime_check` is not really a flake" then "is a flake" (both wrong, it was the fade); "L0 held at 137" offered as evidence (it was master's L0). "The pattern in all three is the same: a confident generalisation from two or three data points." (`HANDOFF-2026-09-19-LATE` s5c) | Wrong conclusions written into notes others acted on |
| **Research backlog lost between files** | The record-first filter excluded claimants: "No Bob Lazar, no John Lear, no Dulce"; worse, "the triage passes ALREADY FOUND most of these, ranked them in their section A, and nobody built them" (McCandlish twice, McKinnon twice, Oppenheimer ranked second); the 14 Aug analyst pass found seven novel joins and they were "not yet wired as edges" (verified 24 Sep: `john-schuessler` still has only two edges); the canon audit's own pass 5 (astronauts, ministers, officials) was displaced when the nuclear cluster was called "pass 5" and is unbuilt (verified: no `edgar-mitchell`, `gordon-cooper`, `paul-hellyer`, `haim-eshed`, `hill-norton`, `jimmy-carter`); the Maury Island / Crisman / Dahl / Kelso / LeMay / Eaker scope call has waited since 29 Aug | The board's coverage gaps are process gaps as much as rule gaps |
| **Generated output not cleaned** | `exports/notebooklm/` carries six stale tracked band files from earlier builds (`02-reverse-engineering`, `03-retrieval`, `06-research`, `07-disclosure`, `07-oversight`, `08-research`); `03-retrieval.md` says 149 map nodes while `02-retrieval.md` says 135, and the README tells Stewart to "Multi select every numbered .md file" (verified 24 Sep) | NotebookLM is fed contradictory figures |
| **Data-model drift** | `cluster` used as a provenance tag by the `_rs-*` files (132 entries, nine tokens); person `status` has no vocabulary (eight values; `dead`/`deceased`, `active`/`alive`); `entity.sub` is "two fields wearing one name" (164 conflicts); no craft or claimed-site class; claimant kind lives in note prose; three taxonomies for position (`cluster`, map `band` by rarest role, `roles`) plus eight classes and twelve edge types | Every consumer re-derives meaning; the map band depended on alphabetical file order |
| **Environment and cost** | GitHub API 1 MB read cap made files "read as absent" and misled Design twice; `deg` counted edge instances (107 vs 96 L0 nodes, "cost a session to unpick"); Windows paths with spaces, CRLF; YouTube blocked Stewart's IP after 169 malformed requests; the DIA remap "fabricated 116 citations"; a HEAD-only link probe hid a dead citation; the orchestrator's re-sent context was 71% of a $30 session (3 Sep); Sonnet subagents stalled "after burning 140k to 250k tokens each" (18 Sep); a 16 MB artifact committed per build, `.git` 435 MB (audit finding 14, still open); the harness refuses agent pushes to master | Money, hours, and one near-fabrication |
| **Decision latency by ownership** | "The map is Design's", so the cell panel (12 Sep), the map bridge and the inversion questions (29-30 Aug) were written up and not changed; the 30 Aug network brief (Q1 what a node is visually, Q2 labels, Q3 the 48% at 1% opacity, Q4 what a filter does, Q5 sourced vs derived) was never sent and was overtaken by the rethink; Design's queue is now three items | Known problems persist for weeks |

### 4b. What a better architecture would prevent

| Failure class | Structural prevention |
|---|---|
| Silent drops and defaults | One schema with enums (`cls`, `status`, bands, edge types, claimant kind, denial kind) validated at load; explicit null; rejects surfaced as a failing build, not a file nobody reads; merge semantics independent of file order by construction; no field that can only be set in a side file |
| Checks that measure artefacts | Checks that assert meaning (every node reachable by name, no anonymous mark, every thread step joined, every count re-derived) rather than pixel-ink ratios or "fits in 938 px"; a layout whose legibility does not depend on the board's size |
| Inherited surfaces and dual shells | One shell, one renderer family, one gate that tests only what readers see; retire `dist/the-program.html` and its checks so a legacy threshold cannot block a research deploy |
| Size limits | A top-level surface that aggregates by level (cells, groups, hubs) so growth changes counts, not geometry; the budget stops being a constant |
| Stale state | A generated STATE file (branches unmerged, candidate rows unbuilt, Design questions open, Stewart decisions pending) rather than hand-written handoffs; the backlog as data with statuses |
| Local vs CI divergence | One command that runs exactly what CI runs, including the app checks |
| Generated debris | Export and build directories wiped and regenerated whole on every run |
| Research loss between files | Candidate rows, analyst finds and canon passes as tracked records with a state (proposed, verified, built, refused) and a reason |

---

## 5. UX history

| # | When | Surface | What happened | What it taught |
|---|---|---|---|---|
| 0 | 12 Aug | Port of The Vanishing v2 | Single self-contained HTML, four-row shell (top bar, stats strip, rail / view / dock, analyst across the bottom), force-directed map with Barnes-Hut and plates only for degree 10 or more, eight then ten views. 976 nodes. The parent was "tuned to stay legible at 3×" of 52 nodes; this was 17.5x (`DASHBOARD_PLAN`) | A shell designed for 50 nodes does not scale by tuning |
| 1 | 12-13 Aug | Performance | Load 19.8 s to 1.6 s, 104 fps; precomputed layout; `verify.py` born after four BROKEN bugs shipped past a "did anything throw" check (`PERF-AND-DENSITY-PLAN`) | Performance was never the problem; legibility was |
| 2 | 13 Aug | L0 aggregation | Stewart's "map of the program, not of people": structural nodes above a degree floor, summarised edges carrying count and strongest tier; built as a force layout of 96 then 110 nodes | Aggregation beats filtering for a board promising "we left nothing out"; 346 orphans was the hard part |
| 3 | 14 Aug | Entry surface | Stewart: "way too busy ... no opportunity for discovery". Six question-shaped entry paths computed at build; focus on select. Diagnosis: "Position carries no information" | Readers want questions, not categories |
| 4 | 24-25 Aug | Design's packed cells | X era by Y function band, one chip size 205 by 20, an edge budget (cross two bands and an era, plus one anchor per node, about 100 at rest), a channel table, three denial states, amber start-here, dense occupancy mode below the label threshold. Comp signed off; built with pixel-reading canvas assertions | Zero overlap by construction; the chip holds 37 characters, so labels needed authored shorts; residual bands look broken unless labelled |
| 5 | 26-27 Aug | Shell usability | FIT showed numerals because one constant did two jobs; the dossier took half the window; start-here zoomed in to 1.15x; overlays printed over controls; drawers could not animate; selection spawned two panels; the breath pulsed over a selection; directed-denial particles missing. All fixed; cell mode became an explicit opt-in; the dock capped at 640 px (89 characters) | "A constant standing in for something that varies"; sample the animation, do not read the CSS; under about 1750 px the map shows the lattice without names |
| 6 | 29 Aug | The inversion | Stewart preferred the force graph because clicking a node there showed its connections. Force graph became the primary NETWORK map (964 nodes), packed map the PROGRAM tab. Part of the cause was a bug (`renderSurface` refused to re-mount, so every frame/path command failed on the view it targeted). The Design brief says "the comparison he made was not quite the one he thought he was making" | What he needed was "see all the connections of the thing I clicked", a neighbourhood question, not a whole-map preference |
| 7 | 30 Aug | Network map labels | Design's five changes (name only, chosen by space, pointer proximity, warm arrival, two bridges). Then: DeLonge named 1 of 10 neighbours; labels offset by 1/dpr on Windows scaling; labels floating over an unreadable field; filters that reveal instead of filter; "nodes are just geometry with occasional white text". A network brief with five questions was written and never sent | No label treatment rescues a whole-graph rest state at about 1,000 nodes; 17 of 1,027 named |
| 8 | 2 Sep | The rethink | "a thousand dots that mean nothing". Entity first: every node a page and a URL, Home as a start page, threads first-class, the program map as default, the network reduced to a scoped neighbourhood, an evidence explorer, a report. Design returned nine screens at three widths, an interaction spec and checks C1-C16. Stewart: public, the name, a hosted site | The corpus is the asset; the shell stood between readers and it |
| 9 | 3-4 Sep | The new app | Vite + TypeScript, hash router; map computed at 1:1 for the viewport with label mode and cell mode, no zoom; neighbourhood as a ring with 15 px slots (hop 2 is 136 nodes); timeline lanes; patents with lightbox; evidence explorer; report; back button (his condition, "this is just perfect"); cutover 4 Sep | The shell-as-patch era ended; the same data now drives an app built for it |
| 10 | 11-12 Sep | Analyst and search | Twelve browser-side tools, a dock on every route, ranked search, thread report; nine live questions all answered; the analyst found a real tier contradiction unprompted | The analyst is the strongest discovery tool on the board today |
| 11 | 12 Sep | Cell panel | At 1366 the cell panel "earns its place"; at 1920 it repeats chips and covers a neighbour. Written up, not changed ("the map is Design's") | Label mode and cell mode need different interactions |
| 12 | 18-19 Sep | Canon pass versus the map | The hub rule added new kinds of object; L0 grew 137 to 149; label mode no longer fit at 1920 on CI; C11 failed (9 of 14 highlights drawn); master reverted; L0 became a budget of 135 with highlights by right, a declared stopgap; Stewart: "mostly a cool visual ... rethink ... a better way to display or group it"; the old shell's `fitChipInk` blocks the nuclear cluster; two of five hubs reach L0 | A fixed-viewport, one-label-size map with a growing membership rule cannot keep up with the research |

### Why the L0 map hit its size limit (mechanism, from the notes)
1. The app's map is laid out at 1:1 for the viewport with no zoom (`notes/NEW-SHELL-2026-09-03.md`).
   Label mode holds only if the sum over bands of (max rows in the band x pitch) fits the viewport
   height AND every label fits its column at 11 px; otherwise the whole map drops to cell mode
   (`notes/DESIGN-RESPONSE-SHELL-2026-09-02.md` s2.2).
2. Labels are one size and never truncated or shrunk, so every chip's width is its text.
3. L0 membership was a degree floor (6 distinct neighbours), so "every research pass adds edges,
   more nodes cross six distinct neighbours, and the map gets denser for ever" (`tools/build_l0.py`).
4. The hub rule and the canon pass add edges and first-of-kind nodes; 18-19 Sep took L0 137 to 149.
5. CI's fallback font wraps two more rows than Windows; clearance at 1920 was about 7 px, and
   nothing may take height from the map (the analyst dock lives in the gutter for that reason).
6. C11 requires each of the 14 start-here highlights to draw its own numbered chip, which cell mode
   cannot do. Result on CI: "54 rows need 1008px of the 938px available" (`notes/STATE-2026-09-19.md`).
7. The budget caps membership but not label width: on the nuclear build C5 headroom fell from 56 px
   to 20 px with L0 unchanged at 135 (`notes/HANDOFF-2026-09-19-LATE.md` s5a).

### Options that were on the table
| Option | Status |
|---|---|
| Cap or trim L0 ("Editorial: L0 selection decides what the top-level map IS") | ADOPTED as `BUDGET = 135`, highlights by right, cuts reported every build. Declared a stopgap |
| Accept cell mode at 1920 and teach C11 that a highlight may sit inside a counted cell | Not taken |
| Give the map more height | Forbidden by the "nothing takes height from `.map-root`" rule |
| Raise the floor to 7 | Rejected: "it overshoots ... would cut L0 to about 115, twenty nodes below what actually fits" |
| Exclude the hubs from L0 | Declined by Stewart |
| Build more to dilute the ink ratio | Worked once (chips 29 / cells 12), then the nuclear cluster turned it red again under the budget |
| Pin the camera and measure over the map's extent in `fitChipInk` | Suggested, not built (`notes/PACKED-LAYOUT-INK-2026-09-19.md` s9) |
| Hand to Design: `fitChipInk`, the map at density, L0 and the hub rule | Open. Stewart's own view: rethink the top-level surface ("a better way to display or group it") |

---

## 6. Open items and backlog

### 6a. Canon passes (from `research/leads/CANON-GAPS-2026-09-18.md` s4)
Passes 1 to 4 are built and on master (Lazar/S-4, ARV, Dulce/Bennewitz, Disclosure Project 2001),
plus TR-3B, the congressional witness pass, the propulsion strand and the NSC/EO spine. The
nuclear cluster, called "pass 5" by the handoffs, is built on its own branch and blocked.

| Pass | Contents | State |
|---|---|---|
| audit's own 5 | Astronauts, ministers and officials on the record: Edgar Mitchell; Gordon Cooper; Paul Hellyer; Haim Eshed; Lord Hill-Norton; Jimmy Carter; the 2013 Citizen Hearing with Stephen Bassett (~7) | **Unbuilt and at risk**: displaced by the "pass 5" renumbering; "Passes 6 to 15 remain" (`notes/HANDOFF-2026-09-19-LATE.md` s1) skips it (verified: none of these nodes exists) |
| 6 | 1947 and the MJ-12 named list: Vannevar Bush; J. Robert Oppenheimer; Lloyd Berkner; Gen. Robert Montague; Jerome Hunsaker; Mack Brazel; Col. William Blanchard; Sheridan Cavitt; the alleged 1947 Einstein draft (~9) | Open |
| 7 | Blue Book, the Robertson Panel and the sceptics: Thornton Page; Luis Alvarez; Samuel Goudsmit; Dewey Fournet; Gen. John Samford; Albert Chop; Philip J. Klass; Carl Sagan (~8) | Open |
| 8 | 1947-86 crash-claim literature: Silas Newton; Leo GeBauer; William Steinman; Timothy Good; Larry Fawcett; Barry Greenwood; Karl Pflock (~7) | Open |
| 9 | Trinity / San Antonio NM 1945; Magenta 1933 and Gabinetto RS/33; Roberto Pinotti; Battle of Los Angeles 1942 (~4) | Open |
| 10 | Oversight refused: Barry Goldwater; Gen. Curtis LeMay; the Wright-Patterson "Blue Room" / Hangar 18 (~3) | Open |
| 11 | Contractors, ranges and custody: Hughes Aircraft / HRL; Wackenhut / Group 4 Falck; Dugway; REECo; Norton AFB; the Janet fleet as a line on `eg-and-g` (~6) | Open |
| 12 | The media substrate: Art Bell / Coast to Coast AM; Joe Rogan; Danny Jones; Larry King; Helene Cooper; Whitley Strieber; Annie Jacobsen (~7) | Open |
| 13 | Modern claimants: Michael Herrera (built); Matthew Brown; Gary McKinnon; John E. Mack; Michael Schratt (~5) | Mostly open |
| 14 | Allied and civil-aviation records: Calvine 1990 and JARIC; JAL 1628 (partly built with the Disclosure Project); Lonnie Zamora / Socorro 1964; Ubatuba 1957; Phoenix Lights 1997 with the flare counter-explanation (~5) | Mostly open |
| 15 | Antigravity research, named: Ning Li; Evgeny Podkletnov; Nick Cook; Boyd Bushman (~4) | Open |

The audit counts 241 canon entries, 92 on the board, 149 missing, and warns "the 149 is a floor,
not a ceiling" (Ben Rich was missed). Also queued: the Gerb triage's ~100 absent candidates
(the NSC and the EO spine were the first taken).

### 6b. The nuclear cluster
Branch `nuclear-2026-09-19` at `359958f`: 19 people, 29 entities, 77 edges, 192 claims, four L0
dossiers, a 47-name witness register, seven base hubs, the 1975 documentary seam, the Mansmann
fix. Key finding: "26 of 47 nuclear-facility witnesses reached the record through contemporaneous
official paper". Blocked only by the old shell's `fitChipInk` (chips 29 vs cells 18; needs
36 < 29). Restore: `git merge nuclear-2026-09-19`. Unopened documents that would move it most:
Col. Frederick Meiwald's letter to Salas of 1 October 1996; the Echo Flight engineering report of
23 March 1967; Michael Johnson's DD-214 and Article 15 record; ~449 pages of the OASD FOIA
compilation; the SAF/AA history. (`notes/HANDOFF-2026-09-19-LATE.md` s1, s6)

### 6c. Design's queue (`notes/HANDOFF-2026-09-19-LATE.md` s7)
1. `fitChipInk`, with its correction block and the afternoon's disproof of the "+7 per new cell"
   mechanism (the budget displaces rather than adds; 30 cells with and without the cluster).
2. The map at density: Stewart's view that it needs rethinking; the budget is a stopgap; label
   width is uncontrolled.
3. L0 and the hub rule: `arv-fluxliner` and `tr-3b` are on the map; `s-4-papoose-lake` and
   `dulce-base` are not. Verified mechanism: they are `location` class, and L0 admits only
   institution, program, event, legislation and document.
Older Design items never closed: the cell panel at 1920 (`notes/MAP-CELL-PANEL-2026-09-12.md`);
the inversion questions and the bridge (`notes/MAP-INVERSION-2026-08-29.md` s9); the 30 Aug
network brief Q1-Q5.

### 6d. Data-model questions
| Question | Source |
|---|---|
| Person `status`: eight values with synonyms; probably conflates vital status with role status; wants an enum | `notes/SILENT-DEFAULTS-2026-09-19.md` s8 |
| `entity.sub`: 164 conflicts, a type token against a sentence of prose | same |
| The 132 out-of-vocabulary `cluster` tags from `_rs-*` files should move to a provenance field of their own | same |
| A class for claimed craft, sites and materials (the ARV hub is a `program`; the `WANTS.md` of 12 Aug already asked "Does a craft become a node class (a ninth) ... Probably yes") | `notes/ARV-BUILD-2026-09-18.md` R1 |
| Claimant kind (worked there, witness, relay, illustrator, investigator, debunker) as a field on the edge | `notes/HANDOFF-2026-09-18.md` s3b |
| Provenance fields for notability nodes (how it reached us, what came first, what they were given, where it diverges) | `notes/TRIAGE-RULE-2026-09-19.md` s3 |
| Should `association` denials be a different edge type (e.g. `research`)? "the most promising direction" | `notes/DENIAL-WEIGHT-2026-09-19.md` s6 |
| 13 genuine date conflicts in `tools/DATE-CONFLICTS.json` (e.g. `geipan` 1977 vs 2005); 33 people with conflicting key dates | `notes/SILENT-DEFAULTS-2026-09-19.md` s9 |

### 6e. Scoring
- Denial weighting: classify the ~22-23 remaining denial edges first, then re-run the simulation.
- Tier option C: a document-identifier pattern beside `PRIMARY_URL_PAT`, plus a self-documenting rule for document-class nodes; size both among the 90 node-scoped demotions first; it moves claims UP.
- Ryan Graves held at Tier B; the two honest routes if the letter must change (hand-set, zero-sum; or redefine node tier as importance, re-grading every node). Stewart has not chosen.
- `dod-oig` under-documented (a coverage gap, not a scoring error).

### 6f. Platform and product
| Item | State |
|---|---|
| Retire the old shell | Plan in `notes/HANDOFF-2026-09-12.md` s3 item 1: write two replacement checks against `app/` first (no parent-board editorial content; the analyst system prompt describes this board), re-point `_l0()`, judge five UI-copy checks, then delete with `check_rebuild.py`'s `BUILT` tuple. Retiring it also removes the check that blocks the nuclear cluster |
| Worker redeploy | Caps cache breakpoints at four; Stewart's to run; not urgent |
| Custom domain | Unanswered since 3 Sep; the Worker must be told first or the analyst goes quiet |
| Public / BYOK | Site public in principle; the Worker accepts `x-analyst-key` and skips rate limits for it, but the shipped app never sends one; no spend ceiling set |
| Landing page and README | Gated on an undefined 1.0 (`notes/WANTS.md`); `README.md` stale since 25 Aug |
| FOIA | 17 filing-ready letters closing 121 open questions on 42 nodes; none filed; four decisions at the top of `notes/FOIA-LETTERS-2026-08-29.md` are Stewart's |
| USPTO | Papers after 20 Aug 2018 on 15/141,270; wrappers for 15/431,823, 15/678,672, 15/928,703 |
| Images | Register at 13 institutional marks, "at its ceiling for THAT category"; ISOO seal keying is Stewart's call |
| Visual evidence pass and 3D models | After the canon pass settles; licensing Stewart's; Fluxliner wants hand modelling in Blender, and the cheap route is Stewart emailing the arvp.co.uk owner |
| Carried forward by name | Roderick Castle, Randy Anderson, Steven Digna, Matthew Brown (from the 9 Sep 2025 record); Edgar Mitchell, Michael Schratt, Jim Goodall, James Fox, Jeremy Rys, Jeffrey Richelson, the Office of Global Access; T.D. Barnes deliberately unbuilt; `lawrence-livermore` missing; Ben Rich to enrich; held candidates (Oppenheimer, the JIO memo, NURO, Craven, Pandolfi, FIA); Maury Island / Crisman / Dahl / Kelso B-25, LeMay, Eaker |
| Analyst-pass finds of 14 Aug | Seven finds, never wired as edges (Schuessler, Kirkpatrick at DIA, Clapper, Mellon and the SAP nodes, SRI and JASON, and others) |
| Larger passes proposed | A contracts pass over USAspending ("the strongest Tier 1 material available and mostly unused"); a patents register of assignees and inventors; the Tier 3 claims (578) as a queue |
| Housekeeping | Danny Jones section C pass; audit finding 14 (history bloat); `spot_check.py --links`; the stale NotebookLM files; the stale `CLAUDE.md` handoff pointer; OneDrive paths in handoff command blocks |

---

## 7. Research process

### 7a. The pipeline
| Stage | How | Model |
|---|---|---|
| Transcribe | `tools/fetch_podcast.py` over podcast RSS (YouTube had blocked Stewart's IP); `faster-whisper base.en` on CPU, about 19x realtime in the cloud container and 21-31x on Stewart's machine alone; windowed decoding after an OOM (12.37 GB to 0.53-0.70 GB); transcripts gitignored, never published | none (machine time) |
| Map | Agents read batches (four episodes each for Michels) and list every name, document number, date, programme and company | Sonnet |
| Cross-check | `tools/corpus_crosscheck.py` classifies each name NODE / PROSE / ABSENT, with self-tested alias rules | script |
| Triage | "ABSENT + a document is a candidate; ABSENT + an anecdote is noise"; ranked sections A to E | Opus |
| Verify | Open the record; verdicts CONFIRMED / PARTLY / NOT OPENED / CONTRADICTED; draft node JSON | Opus |
| Decide | A decision list (`CANDIDATES-*.md`) under Stewart's approval | orchestrator |
| Build | One research file per pass, dossiers for new L0 nodes, authored shorts, full gate | Opus |
| Section C | What a corpus says about existing nodes, as Tier 2 "On <show>, <date>, <speaker> said" claims | Opus |

### 7b. Throughput and cost recorded
| Pass | Figures | Source |
|---|---|---|
| Waves 1-2 (12 Aug) | 14 domain agents, concurrency capped at 2, about 6 hours; WebSearch budget 200 exhausted; result 249 people, 662 entities, 1,553 edges, 3,311 claims | `notes/RESEARCH_LOG.md`; `notes/SESSION-HANDOFF-2026-08-12-cloud.md` |
| Gerb (30 Aug) | 35 episodes to 16 nodes | `notes/HANDOFF-2026-08-30-NIGHT.md` |
| Michels (2 Sep) | 140 episodes, 285 hours; 35 Sonnet mappers; 1,609 names (384 NODE, 206 PROSE, 1,019 ABSENT); 6 Opus triage; 20 candidates to 4 verifiers; 980 to 1,000 nodes; section C: 93 claims on 41 nodes | `notes/HANDOFF-2026-09-01.md` s3a, s7, s8 |
| Area 52 (2 Sep) | 107 episodes, 185 hours; 27 mappers; 895 names (275 / 152 / 468); 6 triage; 35 candidates to 7 verifiers; 1,000 to 1,027 nodes "in one afternoon" | same, s9 |
| Danny Jones (3 Sep) | 136 of 426 episodes; 35 mappers; 981 names (259 / 164 / 558); 6 triage; 36 candidates to 6 verifiers; 1,027 to 1,057; "About a third of this corpus was off-subject" | `notes/HANDOFF-2026-09-03-EVENING.md` |
| Canon run (18-19 Sep) | One continuous session: 1,057 to 1,125 nodes, edges 2,460 to 2,738 with the nuclear branch, Tier 3 claims 514 to 613 | `notes/HANDOFF-2026-09-19-LATE.md` s1 |
| Cost | The Danny Jones session: $30, "Fable 71% (108M cached input tokens across hundreds of small turns), Opus 28% (20 research agents), Sonnet 1% (14 mappers)"; the analyst's first turn about 50 cents, later turns about 13 cents (2 Sep); the nine live analyst questions used 145k to 577k cached input tokens each | auto-memory `token-economy-rules.md`; `notes/ANALYST-2026-09-02.md`; `notes/ANALYST-TOOLS-2026-09-11.md` s8 |
| Gate | About 20-24 minutes per CI run; pushes faster than that cancel runs | `notes/HANDOFF-2026-09-12.md` s5; CI run list |

### 7c. What worked
- Opening the record every time. 604 quoting claims checked, no invented quotation (`notes/HANDOFF-2026-08-25-audit.md`); "roughly one note in six turned out to assert more than its document does" when edges were sourced (`notes/SOURCING-2026-08-25.md`).
- Keeping contradictions as findings: the nitinol lineage, Fouche's novel catalogued as "Science fiction", Castello "a confessed fabrication", DIA's antigravity survey never mentioning Brown, JAL 1628's NARA file owing Greer nothing.
- Verifiers that return a substantial "could not establish" list rather than padding; refusals ("Those three refusals are worth more than three invented edges", `notes/L0-IMPLEMENTATION-2026-08-13.md`).
- Measuring before changing a scoring rule, and testing both directions (the centrality fix: right-way ratio 19.5 with zero documented nodes falling).
- An independent audit that re-derives everything without importing the build.
- Reach notes recording which hosts refuse which route.
- The analyst as a traversal tool: the 14 Aug pass (two-hop joins neither node's text mentions; open questions matched to claims on non-adjacent nodes; affiliation co-tenancy; same-day timeline collisions) found seven joins "no single node states", and the live analyst found the tier contradiction unprompted. These are discovery mechanics a redesign could expose to readers.
- One backgrounded shell command beats a subagent for long mechanical sequences (`notes/HANDOFF-2026-09-18-EVENING.md` s7).

### 7d. What did not
- The record-first triage filter, which kept the claimant layer off the board until 18-19 Sep.
- Candidate rows ranked in section A and never built; finds left in notes.
- Transcripts with no speaker labels, which produced most lead-map errors; read-aloud documents mistaken for records.
- Titles as identifiers (a renamed channel); existence checks skipped before builds (duplicates).

---

## Appendix: what was read

- Read in full: every priority note named in the brief (RETHINK, DESIGN-BRIEF-SHELL, DESIGN-RESPONSE-SHELL, APP-SPEC, NEW-SHELL, HANDOFF-2026-08-26-UX, MAP-INVERSION, TIER-SCOPE, MAP-CELL-PANEL, HANDOFF-2026-09-12, -09-18, -09-18-EVENING, -09-18-NIGHT, -09-19, -09-19-LATE, -09-19-AFTERNOON, TRIAGE-RULE, PACKED-LAYOUT-INK, CENTRALITY, ANALYST-TOOLS, AUDIT-FABLE), `research/leads/CANON-GAPS-2026-09-18.md` sections 1, 2, 3 (band 1), 4 and 5, plus WANTS, DASHBOARD_PLAN, RESEARCH_LOG, SESSION-HANDOFF-2026-08-12-cloud, PERF-AND-DENSITY-PLAN, DESIGN-BRIEF-L0-MAP, DESIGN-BRIEF-LAYOUT-2026-08-14, HANDOFF-2026-08-25-claude-code, -08-25-audit, PACKED-LAYOUT-COST, SHELL-2026-08-27, SHELL-DOCK, DRAWERS, SELECTION, HANDOFF-2026-08-27-shell, -08-28-pais, -08-29, -08-29-MAPS, MAINTENANCE, PATENTS-TAB-MOCKUP, HANDOFF-2026-08-30, DESIGN-BRIEF-2026-08-30 (and the NETWORK and STANDALONE versions), HANDOFF-2026-08-30-NIGHT and most of -EVENING, HANDOFF-2026-09-01, -09-03, -09-03-EVENING, -09-04, ANALYST-2026-09-02, ANALYST-PLAN, STATE-2026-09-19, PROPULSION-CLAIMS, SILENT-DEFAULTS, DENIAL-WEIGHT, ARV-BUILD, INHERITED-SURFACES (first half), THIN-SOURCING.
- Skimmed (first screens plus targeted greps): the remaining notes, including L0-IMPLEMENTATION (stages 10-12 read), ANALYST-PASS-2026-08-14 (finds 1-2), ANALYST-NOKEY, AUDIT-STRIP, BACKFILL-QUEUE, DATE-EXTENT, DENIAL-ADJUDICATION, DENIAL-DIRECTION, DUPLICATES, EDGE-TIERS, FIRST-PAINT, SHELL-FIT, LOOKING, IMAGE-*, GATE-PORTABILITY, LINK-HEALTH, NARA-AIRFORCE, PACKED-LAYOUT-BUILD, PAIS-*, PATENTS-TAB-BUILD, SILENT-REJECTS, SOURCING, SPOT-CHECK, FOIA-LETTERS (decisions block), FOIA-LAYER, REQUEST-QUEUE, WAVE2_WORKORDER, WAVE3_QUEUE, DESIGN-CONFORMANCE, DESIGN-BUILD, LABELS, FIT-SCALE, QA-PASS-2026-08-12 and -13.
- Design folders: `notes/design-2026-08-24/` (README and the layout response in full), `notes/design-2026-08-26/` (README and response), `notes/design-2026-09-02/` (README), and two of the 28 mockup captures in `notes/shots/design-2026-09-02/` (Home and Map at 1920).
- Verification (read-only): `git log`, `git rev-parse`, `gh run list`, `app/public/data/index.json`, `edges.json`, `threads.json`, `map.json`, `highlights.json`, `tools/build_l0.py`, `.github/workflows/gate.yml` step names, `exports/notebooklm/`, and the relevant `CLAUDE.md` sections for orientation only.
