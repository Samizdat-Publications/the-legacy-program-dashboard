# Blind critic, phase 10, round 3

Read: tools/critic/BRIEF.md and the 30 screenshots in dist/critic/p10-round-3-sel/ (home, homeq, person, made, office, questions, q, qblocks, connect, connect2 at 1920, 1366 and 375). Nothing else.

Ambiguity first: each shot is one viewport of a longer page, so I cannot say whether the 1366 person page shows its connections further down, or whether the empty middle band on 1920-made and 1920-office is simply the end of the case-against column. I have not counted either as a problem.

## The five worst problems, worst first

### 1. The same words carry two different tiers, side by side

- **Files:** 1920-made.png, 1366-made.png, 1920-person.png, 1920-office.png, 1366-office.png, 1920-qblocks.png, 1366-qblocks.png
- **What is wrong:** One statement often appears twice, next to itself, at two different tiers. On "made", Grusch's "Nonhuman ..." biologics answer is T1 ("said on the record") and then T2 a few rows lower, and "I was informed in the course of my official duties ..." is T2 and then T1. In the person page's Roles list, "NRO representative to the UAP Task Force, 2019-2021" appears twice, as T2 and as T1. On the office page, "291 reports" is T2 ("Caseload") and T1 ("Reporting period"). A plain description of a PDF's title page is T2, while AARO's substantive "no evidence that U.S. companies ever possessed off-world technology" is T1. On qblocks, AARO's "no empirical evidence" finding is T1 at claim 8 and T2 at claim 39.
- **Why a reader cares:** The tier is the board's main promise. When the same sentence sits at two grades, a reader stops trusting any grade. The legend's line "the same words can also stand at Tier 2" admits the problem without resolving it on the page.
- **Severity:** blocker

### 2. Second-hand and interested-party material graded Tier 1, against the page's own prose

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 375-qblocks.png
- **What is wrong:** The prose says the ICIG's "credible and urgent" finding "is known on the board only through those accounts" [17-20]. Yet claims 18 and 19 carry that finding at T1 "said on the record", sourced to Grusch's testimony and The Debrief, and claim 19 is filed on the Inspector General's own node. Claim 17 is T1 on the strength of Liberation Times reporting. Claim 37, "Formal DoD rebuttal ...", is T1 with no "office's own account" badge, and its claim text includes the board's own argument ("a claim that does not engage Grusch's sworn statement ...").
- **Why a reader cares:** A journalist checking this will see a finding the board admits it has only second-hand, filed as a documented statement by the office that supposedly made it. The interested-party rule also looks applied case by case, not as a rule.
- **Severity:** major

### 3. A block of tier boilerplate opens every surface

- **Files:** 1920-home.png, 375-home.png, 1920-person.png, 1920-made.png, 375-made.png, 1920-office.png, 375-office.png, 1920-q.png, 375-q.png
- **What is wrong:** The same four-part explanation repeats word for word on home, above the claims, above "Claims this person has made", above "Statements by this office" and between a question's title and its answer: "Tier 1 means the record is documented ... The same words can also stand at Tier 2 ... said on the record ... the office's own account". At 375 it fills most of a screen before any content appears.
- **Why a reader cares:** It pushes the answer below the fold. Its content ("Tier 1 ... is not a finding that what was said is true", and then the same words at Tier 2) is the most confusing text on the site, and the reader has to wade through it again on every page.
- **Severity:** major

### 4. Link verbs and dates contradict the sentence they label

- **Files:** 1920-connect.png, 1366-connect.png, 1920-connect2.png, 375-connect2.png, 1920-made.png
- **What is wrong:** On connect, "linked through testimony to" labels a Schumer remark about Reid and also Stratton's career move from AAWSAP to the task force. Neither is testimony. On connect2, "509th Bomb Group received a request from United States House of Representatives" sits over a sentence saying Congress requested a GAO search, and "Roswell Incident is held by" the 509th. On made, "was refused by Defense Intelligence Agency" sits over "Accuses DIA of obstructing ...", and "linked through a denial to" DoD SAPCO sits over a job description. "No date recorded" appears beside events whose dates are in the sentence (FY2008, the 1947 debris, the 1990s GAO search). Route 1 on connect2 is five T1 steps of committee structure, and it is ranked first.
- **Why a reader cares:** The rule is that every connection says in words why it exists. Here the verb says one thing and the sentence another, so a reader cannot trust the relationship families. An all-T1 route through an org chart also looks like the strongest link between Roswell and the 2023 hearing.
- **Severity:** major

### 5. Editorial working notes shown to readers as content

- **Files:** 1920-qblocks.png, 1366-qblocks.png, 1920-person.png, 1920-made.png, 1366-made.png
- **What is wrong:** Claim 39's source line prints a raw URL and then "DEMOTED from Tier 1 (sourced to an interested party ...); needs primary replacement". Under the person's "The case against", one "NOT VERIFIED" entry is about the board's own citation: "The direct NewsNation URL ... (cited here via the Wikipedia footnote)". A claim on "made" ends "Reasoning: the advisory role is recorded in wave-1 sourcing on this board".
- **Why a reader cares:** To-do notes, internal batch names and a Wikipedia footnote inside the case against make the board look unfinished. They also blur the line between the case against a person and the board's own open sourcing tasks.
- **Severity:** major

Works best: on the question page (1920-q, 1366-q), each prose paragraph sits beside the numbered claim cards it cites, each card with its tier and source, so every sentence can be checked without leaving the page.

## Disposition (the session, after the round; the last round the plan allows)

| # | in phase 10's scope? | what was done |
|---|---|---|
| 1 | no: the data | The same words at two tiers is phase R's first queue item; phase 10 was told to fix it in words and does (the key). Unchanged since round 1, and it stays the worst problem on the board until phase R decides the pairs. |
| 2 | no: the data | In `notes/plans/P10-findings.md` (the ICIG finding's tier; the DoD rebuttal claim carrying the board's own argument is added there). |
| 3 | yes, fixed | The key to the marks is folded to its one final sentence on every screen, with "how to read the marks" opening the rest; one key per node page (the claims-made list no longer repeats it); Home keeps the whole key; the printed report keeps it open. |
| 4 | no | The verbs are the phase 7 vocabulary's; "no date recorded" is an edge with no date field. For phase 7's owners and phase R. The all-Tier-1 route through the committee structure is what the weights prefer by design (documented structural links over a hub); its header says the route is not graded. |
| 5 | no: the data | As round 2. |

The worst problem left in phase 10's own scope after this round is the question list's even-looking counts (round 2, item 5), a minor one.
