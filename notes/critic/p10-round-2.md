# Blind critic, phase 10, round 2

Read: tools/critic/BRIEF.md and the 30 screenshots in dist/critic/p10-round-2-sel/ (home, homeq, person, made, office, questions, q, qblocks, connect, connect2 at 1920, 1366 and 375). Nothing else was opened.

Ambiguity first: every shot is one viewport of a long page, so I cannot judge what lies below the fold or whether any figure matches its source. No shot looks mid-load. The Grusch connections column ends at the bottom of 1920-person, which is the viewport edge, not a clip.

## The five worst problems, worst first

### 1. The same sworn statement is graded Tier 1 in one row and Tier 2 in the next

- **Files:** 1920-q.png, 1366-q.png, 1920-made.png, 1366-made.png, 1920-office.png, 1920-qblocks.png
- **What is wrong:** On the question page, claim 1 (Grusch testified under oath on 26 July 2023, T2) and claim 7 (Grusch sworn to Rep. Garcia at the same hearing, marked "said on the record", T1) are the same kind of statement from the same transcript, graded differently in one list. On "Claims this person has made" the same quote appears twice: "I was informed in the course of my official duties..." is T2 in one row and T1 in another, and the "Nonhuman, and that was the assessment..." answer to Rep. Mace is T1 once and T2 once. The AARO page does it too: "291 reports, 274 in period" is T2 as "Caseload" and T1 as "the office's own account", and a literal description of the report's title page is T2. In qblocks, claims 8 and 38 (AARO's words, T1 with the badge), 37 (a DoD rebuttal, T1 with no badge) and 39 (an AARO quotation, T2) sit together.
- **Why a reader cares:** The tier is the board's whole promise. A reader checking a claim finds the identical quote carrying two grades on one screen and can no longer tell what any T1 or T2 means.
- **Severity:** blocker

### 2. Internal working notes are printed to the reader as if they were sources

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 1920-person.png, 1920-made.png, 1366-made.png
- **What is wrong:** Claim 39's source line is a raw media.defense.gov URL followed by "DEMOTED from Tier 1 (sourced to an interested party ...); needs primary replacement", with a long dash in it. A "Not verified" item on the Grusch page reads as an editor's to-do about a NewsNation URL "cited here via the Wikipedia footnote". The top of the "made" view carries "Reasoning: the advisory role is recorded in wave-1 sourcing on this board".
- **Why a reader cares:** A journalist reading these sees the workbench, not the finding. "Needs primary replacement" tells them the claim on screen is known to be weakly sourced, while it is still shown and counted. It makes the board look unfinished at exactly the place it asks to be trusted.
- **Severity:** major

### 3. Secondhand accounts are graded Tier 1, and "said on the record" is pinned to the wrong speaker

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 375-qblocks.png, 1920-home.png, 1366-home.png
- **What is wrong:** The qblocks paragraph says the ICIG finding "is known on the board only through those accounts", yet claims 17, 18 and 19 are all Tier 1. Claim 17 (no badge, so read as documented) is sourced to Liberation Times and The Debrief. Claim 19, "Determined Grusch's PPD-19 urgent-concern complaint credible and urgent", sits on the ICIG with a "said on the record" badge but is sourced to Grusch's own testimony, so it is not the ICIG on the record at all. Meanwhile the front door says AARO and DoD statements are "capped at Tier 2", and every page then shows their statements at Tier 1 under "the office's own account".
- **Why a reader cares:** The prose and the grade contradict each other in adjacent lines. A reader who trusts the grade is told a press report is a primary record. A reader who trusts the front door finds its rule apparently broken on every AARO row.
- **Severity:** major

### 4. On the routes page, many link verbs do not say why the link exists, and a chain of five Tier 1 links joins two things only through "the House includes a committee"

- **Files:** 1920-connect2.png, 1366-connect2.png, 375-connect2.png, 1920-connect.png, 1366-connect.png
- **What is wrong:** "Roswell Incident is held by 509th Bomb Group" (an incident cannot be held). "509th Bomb Group received a request from United States House of Representatives" describes a GAO records search. "United States Navy had in a post", "linked through custody to", "linked through a document to" and "Harry M. Reid linked through testimony to Charles E. Schumer" (for a remark by Schumer) are placeholders, not reasons. Route 1 in connect2 runs Roswell to the 2023 hearing through the House, its committee and a subcommittee, and its header advertises "each link graded T1 T1 T1 T1 T1".
- **Why a reader cares:** The owner's rule is that every connection says in words why it exists. These verbs make readers decode each step themselves. The five-T1 header makes a trivial organisational chain look like strong evidence, whatever the caveat paragraph above says.
- **Severity:** major

### 5. Every big question shows almost the same evidence balance, which reads as a quota

- **Files:** 1920-questions.png, 1366-questions.png, 375-questions.png
- **What is wrong:** Under each question the tallies are 7 for, 7 against, 5 open, 1 thread; then 7/7/5/1, 6/7/5/1, 6/6/5/2, 6/6/5/1, 6/7/5/1. Every visible question has exactly 5 open items and near-equal for and against.
- **Why a reader cares:** A sceptical reader will assume the for and against lists were filled to a fixed length, not drawn from the record. That undermines the claim that each question is "answered so far from the record", and hides which questions are actually lopsided.
- **Severity:** major

The single thing that works best: the question page's two columns, with each paragraph of the answer set beside the numbered claims it rests on, each with its tier and source, and the evidence for and against placed side by side at 1366 and 1920.

## Disposition (the session, after the round)

| # | in phase 10's scope? | what was done |
|---|---|---|
| 1 | in words only | The pairs themselves are phase R's first item. Every key to the marks, and Home's "How to read a claim", now adds under the final Tier 1 sentence: "The same words can also stand at Tier 2: there they are the claim itself, resting on the speaker's word, not the record that it was said." |
| 2 | no: the data | Source-string bookkeeping and editorial "Not verified" notes; recorded in `notes/plans/P10-findings.md` for the phase 12 copy pass. |
| 3 | no: the data | The ICIG finding at Tier 1 on secondhand sources is already in `notes/plans/P10-findings.md` (`c-5ba9eae189`, `c-b19d0fe80f`); the claim-meta row now names Grusch as the claimant, which is what the person page shows. The office's own account at Tier 1 is the board's stated exception ("unless the claim is about what they said"). |
| 4 | partly | The route header now reads "N things in between, M links · the links, one by one: T1 ... · the route itself is not graded". The verbs are the phase 7 vocabulary's (a family phrase where the predicate is not confident); left for that vocabulary. |
| 5 | no | Five open questions each is what the drafter found worth asking; the for and against counts are the record's. Left. |
