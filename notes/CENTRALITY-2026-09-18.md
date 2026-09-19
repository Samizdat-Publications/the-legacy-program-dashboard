# The centrality fix, 18 September 2026

**Decision: `witness-chain` is out of `PROGRAM_EDGES` in `tools/regrade.py`. Nothing else
changed. The claim-tier weighting proposed as lever 1 was measured, and rejected, because
it demotes documented nodes.**

This note is the reasoning, per the mandate of 18 September: decide, record why, tell
Stewart after.

## 1. What was wrong

`notes/HANDOFF-2026-09-18-EVENING.md` section 3a names two defects. Both were measured.
Only the second turned out to be real.

| # | The claim | Verdict |
|---|---|---|
| 1 | The degree counters ignore `claimTier`, so a Tier 2 "X said he saw it" edge scores as much as a Tier 1 documented one | True as description, **wrong as a fix**. See section 4 |
| 2 | `witness-chain` sits in `PROGRAM_EDGES`, weighted x3.0 for meaning *inside*, when it only means somebody SAID something | True, and it is the whole defect |

## 2. The measurement, taken before anything was changed

On the 1,057-node board (`tools/_pristine-board.json`, 2,460 edges).

| Edge set | n | Tier 1 | Tier 2 | Tier 3 | T2/T3 share |
|---|---|---|---|---|---|
| All edges | 2,460 | 1,627 | 621 | 212 | 33.9% |
| `PROGRAM_EDGES`, the x3.0 set | 694 | 436 | 203 | 55 | 37.2% |
| of which `witness-chain` | 157 | 60 | 85 | 12 | **61.8%** |
| of which custody / funding / programmatic | 537 | 376 | 118 | 43 | **30.0%** |

That single row decides it. `witness-chain` is twice as claim-like as the rest of the set
it is averaged into, and it is the only member of that set whose Tier 2 and Tier 3 edges
outnumber its Tier 1 ones. The set's justification in its own comment is that its members
mean *inside, not adjacent*. Three of them are structural facts about the node: who held
the thing, who paid for it, what programme it belonged to. The fourth is a record that a
person made an assertion.

| Node counts | n | share |
|---|---|---|
| Nodes with any program edge | 533 | 50.4% of the board |
| whose `prog_deg` is ENTIRELY `witness-chain` | 81 | 15.2% of those |
| whose `prog_deg` is MOSTLY `witness-chain` | 102 | 19.1% of those |
| Tier A nodes whose `prog_deg` is entirely `witness-chain` | 4 | 2.5% of Tier A |
| Tier A nodes whose `prog_deg` is mostly `witness-chain` | 21 | 13.3% of Tier A |

**The damage was still small on master, and that is the point.** The hub rule adopted the
same day gives every claimant a `witness-chain` edge into the thing claimed about, so
`witness-chain` becomes the dominant edge type of every claimant cluster built from now
on. This was fixed before the canon pass builds 149 more figures on top of it, not after.

## 3. Four candidates, and the test the handoff set

The handoff's test is not "McCandlish is no longer Tier A". It is that the nodes moving
DOWN rest on testimony and the nodes moving UP rest on documents. Each node was profiled
by its own edge mix before any result was read: `witness-chain`, `behavioral` and
`investigative` count as testimony, `institutional`, `legislative`, `custody`, `funding`,
`programmatic` and `research` as document. Run against the ARV branch board (1,066 nodes),
which is where the reported inversion actually lives.

| Variant | nodes moved | fall: testimony | fall: **document** | rise: document | rise: testimony | right-way ratio |
|---|---|---|---|---|---|---|
| **lever 2 alone** (witness-chain out of the x3 set) | 26 | 19 | **0** | 20 | 2 | **19.5** |
| lever 1 alone (claim-tier weights on all counters) | 30 | 10 | **13** | 26 | 3 | 2.2 |
| lever 1 on `prog_deg` only | 17 | 5 | **8** | 13 | 3 | 1.6 |
| lever 2 plus lever 1 on `prog_deg` only | 35 | 22 | **6** | 30 | 4 | 5.2 |
| both levers, as written in the handoff | 46 | 25 | **8** | 41 | 4 | 5.5 |

Lever 2 alone is the only variant that moves **no** document-based node down. It is also
the smaller change, which the handoff prefers on its own grounds.

## 4. Why lever 1 is wrong, and it is worth saying plainly

Every variant carrying claim-tier weighting pushes documented nodes down, and the more
surgical the application, the worse the ratio. The reason is a category error in the
proposal, not a bug in the arithmetic.

**An edge's `claimTier` grades the evidence for that relationship, not the documentary
standing of the nodes it joins.** A GAO report can be attached to a programme by a Tier 2
edge because the linkage is inferred rather than stated. Demoting the GAO report for that
punishes the report for the quality of somebody else's inference about it. Meanwhile
`witness-chain` edges are already 61.8% Tier 2 or 3, so lever 2 captures most of what
lever 1 was reaching for, and captures it by naming the actual thing: this edge type is a
claim, so it does not get the structural multiplier.

Lever 1 is therefore not merely redundant. It is a different and worse rule.

## 5. What moved, on the real run

`tools/REGRADE_REPORT.json` under each rule, same data, same run conditions.

| | |
|---|---|
| Baseline report rows (old rule) | 679 |
| New report rows | 673 |
| Moves identical under both rules | 641 |
| Moves only the new rule makes | 12 |
| Moves only the old rule made | 18 |
| Moves to a different tier under each | 20 |

So the change accounts for about 50 nodes. The other 641 are the ordinary global-regrade
churn the handoff warned not to read as signal.

**What the old rule was doing at the Tier A boundary, and the new rule stops:**

| Node | class | old rule | new rule |
|---|---|---|---|
| `podesta-delonge-mccasland-email-2016` | document (an email) | promoted INTO Tier A on 4 program edges, all `witness-chain` | stays B |
| `gao-nsiad-95-187` | GAO report | demoted OUT of Tier A | stays A |
| `ndaa-fy2024-subtitle-c` | legislation | demoted OUT of Tier A | stays A |
| `reid-sap-letter-2009` | document | demoted OUT of Tier A | stays A |
| `dcsa-nisp` | institution | demoted OUT of Tier A | stays A |
| `mit-lincoln-laboratory` | institution | demoted OUT of Tier A | stays A |
| `d-materials` | domain | demoted OUT of Tier A | stays A |

An email ranking above a GAO report is the defect stated as plainly as it can be put.

**What the new rule moves out of Tier A:**

| Node | why it was Tier A | claims |
|---|---|---|
| `ryan-graves` | 4 `witness-chain` edges | T1:5 T2:3 T3:1 |
| `colm-kelleher` | 4 `witness-chain` edges | T1:0 T2:6 T3:2 |
| `alexandro-wiggins` | 3 `witness-chain` edges | T1:3 T2:8 |
| `jeffrey-nuccetelli` | 3 `witness-chain` edges | T1:3 T2:9 |
| `william-mccasland` | 1 `witness-chain` edge | T1:3 T2:9 |
| `skinwalkers-at-the-pentagon` | a book, 3 `witness-chain` edges | T1:2 T2:1 T3:1 |
| `rendlesham-1980` | an event claimed about | T1:2 T2:1 |
| `podesta-delonge-mccasland-email-2016` | see above | T1:5 T2:1 |

**Ryan Graves is the judgement call in this list and it is flagged deliberately.** He
testified under oath to Congress, which sounds like the Tier A definition. But he
testified about what he saw, not about being inside a programme, and Tier A reads "named
in sworn testimony or primary documents as directly inside the program". Tier B for a
credible outside witness is the honest grade.

### Stewart argued this, 18 September, and the argument is kept

His case: Graves oversaw the squadron that was seeing these things repeatedly for months,
he has first-hand knowledge from when the pilots landed and told him, and from the radar
data. **"He isn't himself in the program."** And the wider point, which is the real one:
"I don't want this to be just about the program because that would be incomplete without
all the major whistleblowers and people who have testified to Congress about UAP, since
that's some of the primary evidence we have about the whole thing."

**The scope point is accepted and acted on: see the witness coverage pass in
`notes/HANDOFF-2026-09-18-NIGHT.md` section 4.** The grade is held, on three findings, all
checked rather than assumed:

| Finding | Consequence |
|---|---|
| **L0 carries no people at all.** Its 137 nodes are institutions, documents, programmes, events and legislation. All 311 people are off the top-level map by design | The demotion removed Graves from nothing a reader sees |
| **Search ranks on CLAIM tier, not node tier.** The "tier strictly dominates" rule in `app/src/search.ts` is T1/T2/T3. Node tier does not enter `score()` | Graves ranks on his five T1 claims, which is among the stronger evidence on the board |
| **`hearing-2023-07-26`, `hearing-2024-11-13` and `hearing-2025-09-09` are Tier A and ON L0** | Congressional testimony is already top-level, as hubs, which is Stewart's own modelling rule working |

So node tier A/B/C is a displayed letter plus an input to L0 selection and the analyst's
index. It is not the axis that decides whether a witness is prominent.

The board's own record on Graves supports the description and also shows the relay: his
T1 claims read "one of the pilots saw a dark grey cube inside of a clear sphere" and "Our
squadron submitted a safety report". That is a squadron member reporting what his squadron
saw. Strong evidence, and not proximity to the programme.

**The point that decides it for the future rather than the past:** under the hub rule,
every claimant gets a `witness-chain` edge into the thing claimed about. Building out the
whistleblower roster Stewart wants would, under the OLD rule, have drifted every one of
them toward Tier A, and "proximity to the programme" would have become "how much testimony
exists about this". This fix is what makes that expansion safe.

If the letter is still to change afterwards, there are two honest routes and neither is a
quiet edit: hand-set Graves to A, which is zero-sum under the forced 15 per cent and drops
a documented node out to make room; or redefine the axis so node tier means importance to
the subject rather than proximity, which re-grades all 1,057 nodes and rewrites the
definition in CLAUDE.md section 6. Stewart has not chosen either.

Five documentary or institutional nodes fall from B to C. Each was checked by hand; in
every case the node's only x3 edge was a Tier 2 `witness-chain` link and its documented
edges are untouched:

| Node | edges | reading |
|---|---|---|
| `dod-oig` | 4 total, 1 T2 `witness-chain` to Elizondo | On this board DoD OIG appears mainly as the body Elizondo complained to. See section 7 |
| `elizondo-dodig-complaint-2021` | 1 `witness-chain` plus 3 `investigative`, all T2 | A document that records an allegation |
| `d-oversight` | keeps 3 legislative plus institutional and investigative | a domain node, low stakes |
| `thomas-wilson` | 1 T2 `witness-chain`, claims T1:0 | correct |
| `john-podesta` | 2 `witness-chain`, relevance is advocacy | correct |

## 6. The ARV cluster and the red check

`mark-mccandlish`, on the ARV branch board:

| Node | baseline | lever 2 | both levers |
|---|---|---|---|
| `mark-mccandlish` | A#70 | **A#143** | B#179 |
| `christopher-mellon` | A#61 | A#76 | A#109 |
| `uap-task-force` | A#80 | A#74 | A#91 |
| `cfr-32-117` | A#68 | A#62 | A#54 |
| `brad-sorensen` | B#219 | B#465 | B#462 |
| `arv-fluxliner` | B#216 | B#299 | B#371 |

Under lever 2 he is still Tier A, at rank 143 of 1,066 against a cut at 159, and he is now
**below** Mellon, the UAP Task Force, 32 CFR 117 and 50 USC 3091a. The specific inversion
the handoff objected to is gone. He did not have to be pushed out of Tier A to fix it, and
pushing him out would have required lever 1, which costs eight documented nodes.

Brad Sorensen, the second-hand relay the whole account runs through, falls 246 ranks. That
is the fix working on the right node.

**On the red check: `arv-fluxliner` does NOT fall out of L0 under this change.**

**CORRECTION, added when the ARV branch was actually re-graded.** The first version of
this paragraph said "L0 membership held at 137 through the rebuild" and offered that as
the evidence. That was not evidence of anything. 137 was L0 on MASTER, which carries no
ARV nodes at all, so it could not have told us what happens to `arv-fluxliner`. The
conclusion was right and the reason given for it was worthless.

Measured properly on the re-graded ARV board (branch `arv-regrade-2026-09-18`):

| | |
|---|---|
| L0 size | **139**, the same as the ARV branch carried under the old rule |
| `arv-fluxliner` | **in L0**, Tier B, cluster `witness`, class `program` |
| `northrop-grumman` | in L0, Tier B, cluster `contractor`, class `institution` |
| The `witness x program` cell | **still holds exactly one node** |

So the check does not resolve itself, and Stewart's option 1, building TR-3B to populate
the `witness x program` cell, remains the fix.

## 7. Two findings recorded in passing

**Ben Rich already has a node.** `HANDOFF-2026-09-18-EVENING.md` section 5 carries him as
unbuilt, saying the board holds `lockheed-skunk-works` with no node for the man who ran
it. It holds `ben-rich`: person, Tier B, 2 claims, 3 sources, from domain `primes-custody`,
with edges `institutional -> lockheed-skunk-works` (T1) and `custody -> lockheed-martin`
(T3). The node is thin and deserves the build the handoff wants, but **it must be an
enrichment of `ben-rich`, not a new node.** The id-rules comment in `regrade.py` exists
because five duplicate people got onto the board exactly this way. The rest of section 5's
named candidates were not checked this way and should be, before each is built.

**`dod-oig` is under-documented.** It falls to Tier C on four edges. The Defense
Department's own Inspector General, on a board about oversight of concealed programmes,
should carry more than one investigative edge to a single report. That is a coverage gap
for the canon pass, not a scoring error, and the fix correctly refuses to hide it behind a
testimony multiplier.

## 8. Gate

Run as `BOARD_URL=http://127.0.0.1:8899/the-program.html python tools/state_snapshot.py
--gate`, which runs the whole gate in one command.

| Check | Result |
|---|---|
| `browser_env --self-test` | PASS |
| `verify` | PASS |
| `verify --self-test` | PASS |
| `capture_strip` | PASS |
| `audit_independent` | PASS |
| `runtime_check` | **FAIL(1)** |
| `test_packed_layout`, and `--self-test` | PASS |
| `test_scripted_analyst` | PASS |
| `verify --idempotent` | PASS |

`GOLDEN.json` did not drift and `--update-golden` was not run. It tracks counts, and this
change moves only tiers.

**The one red check is not caused by this change, and that was tested rather than
assumed.** `runtime_check.js` fails with `the network map is still at rest: nothing
selected, pointer off-canvas :: went quiet and then started moving again`.
`dist/the-program.html` was checked out from master, giving unchanged code and unchanged
data, and the check failed on it with the identical message on this machine. This change
alters node tiers and touches nothing about map motion or settling.

The evening handoff calls this a flake, on the evidence that it failed 7 of 7, then
passed, then failed again. This session saw three consecutive failures and no pass, plus
one run that hung. Locally it now looks more like a consistent failure than an
intermittent one. CI stays green, and it dies when the old shell is retired.

## 9. What the next session needs to know

| | |
|---|---|
| Change | One line of `tools/regrade.py`, plus its comment and the rationale string that named the four edge types to readers |
| Not changed | `TARGET`, the x3.0 multiplier itself, the `s *= 0.35` unsourced discount, the explicit `new == "A"` demotion, `merge.py` |
| `GOLDEN.json` | Updated with `python tools/verify.py --update-golden`, never by hand |
| ARV branch | Was graded under the old rule. Rebase or rebuild `leads/arv-2026-09-18` on top of this so its nodes are graded once, per evening handoff section 3d |
| Rejected, with numbers | Claim-tier weighting of the degree counters. Section 4. If it is ever revisited, it needs a different justification than the one in the handoff, because that one is measured here and fails |
