# Handoff, 18 September 2026, evening (the current one)

Opus 5 session. It ran item 1 and item 1a of `notes/HANDOFF-2026-09-18.md` section 3.
That file is still correct on everything it says; its section 3 now carries an UPDATE
block pointing here. `git fetch --all` before reading further.

## 1. What is live, and what is waiting

| | |
|---|---|
| **Item 1, DONE and deployed** | `tier-scope-b` merged to master as `92b5903`. Gate run 35380678058 green, deploy 35382933598 green. Production carries the four demotions. T1 3,363, T2 1,426, T3 514 |
| **Item 1a, BUILT, COMMITTED, NOT PUSHED** | The ARV cluster, commits `056ec48` and `cde1c57` on `leads/arv-2026-09-18`. Board 1,057 to 1,066. **One check is red.** Read `notes/ARV-BUILD-2026-09-18.md` in full before touching it: its section 2 is the twelve build rulings, its section 4 is the whole gate and the red check traced to its cause |
| **`runtime_check.js`** | Failed 7 of 7, then PASSED later in the same session on the same data, then failed again. It is a Windows-local flake, confirmed. CI runs it green. Do not chase it |

## 2. What Stewart decided, 18 September evening

His words: do the centrality fix first, then TR-3B, then the rest in the order given.
On the red check, option 1. The propulsion strand is worth a pass.

So the order is fixed and is section 4 of this file. **He also widened the mandate on
18 September morning and it still stands:** decide, write the reasoning in a note, tell
him after. He is not asking to be consulted on research or tier judgement.

## 3. THE NEXT SESSION: the centrality fix. Do this and nothing else

> **UPDATE, 18 September 2026, night. THIS SECTION IS DONE and this file reached master
> for the first time with the ARV re-grade.** Current handoff is
> `notes/HANDOFF-2026-09-18-NIGHT.md`; the reasoning is `notes/CENTRALITY-2026-09-18.md`.
>
> | | |
> |---|---|
> | Built | **Lever 2 only.** `witness-chain` out of `PROGRAM_EDGES`. Merged and deployed |
> | **Lever 1 REJECTED on measurement** | Claim-tier weighting of the counters demotes documented nodes in every form tested, which is the failure condition section 3b sets. Do not re-propose it without a new argument |
> | Section 3d, the ARV re-grade | **Done.** The branch was rebuilt on master rather than rebased: master's tree plus the ARV branch's source files only, with everything generated regenerated |
> | Section 3d, the red check | **Does not resolve itself.** Confirmed by measurement, not inference: L0 139, `arv-fluxliner` in it, `witness x program` still holding one node. TR-3B remains the fix |
> | Section 5, Ben Rich | **Wrong. He already has a node**, `ben-rich`, Tier B. Enrich, do not build |
> | Section 1, the `runtime_check.js` flake | Three consecutive local failures this session and no pass, including on master's own untouched board. Not caused by any change here, CI green, but "flake" may be the wrong word |
>
> Section 4's job order below is unchanged and still governs, with one addition: a
> **witness coverage pass** as item 3a, on Stewart's scope ruling of 18 September.



One phase. It re-grades every node on the board, so it does not share a session with a
corpus build.

### 3a. The finding

`tools/regrade.py` assigns node tier A/B/C by **forced percentile**, `TARGET = {"A": 0.15,
"B": 0.35, "C": 0.50}` at line 111. Score comes from `centrality()` at line 119.

Two things in it are wrong now, and the second is the sharper one:

1. **The degree counters ignore `claimTier`.** Lines about 236 to 243 build `deg`,
   `prog_deg` and `denial_deg` by walking edges and counting `+= 1`, never reading
   `e["claimTier"]`. A Tier 2 "X said he saw it" edge scores exactly as much as a Tier 1
   documented one.
2. **`witness-chain` is inside `PROGRAM_EDGES`** (line 114), which is weighted **x3.0** and
   whose own comment says these are "edges of the types that mean *inside*, not
   *adjacent*". A witness-chain edge does not mean inside. It means somebody SAID
   something about this node. The other three members, `custody`, `funding` and
   `programmatic`, are documented structural relationships. This one is a claim.

That was tolerable while witness-chain edges mostly joined documented witnesses to
documented programmes. **Handoff section 3b changed it**: under the hub rule, every
claimant gets a witness-chain edge into the thing claimed about, so witness-chain becomes
the dominant edge type of every claimant cluster and its x3 weight systematically promotes
claimants.

**The evidence.** The ARV build put `mark-mccandlish` at **Tier A, rank 70 of 1,066**,
score 72, degree 16, program_edges 8, denials 1. A man with no documented office, no
documented clearance and an account that is wholly a second-hand relay now ranks above a
sitting congressman, among `christopher-mellon` (61), `james-lacatski` (65), `cfr-32-117`
(68), `usc-50-3091a` (72) and `uap-task-force` (80). His 8 program edges alone are 24 of
his 72 points.

Stewart's own rule in section 3b: "Degree is allowed to mean *a lot is claimed here*,
never *this is true*." At tier level it currently means the second.

### 3b. The job

**Size both levers BEFORE changing either.** This is the discipline the tier option C note
already demands, and it matters more here because the distribution is forced: A always
holds 15 per cent, so this is **zero-sum**. Every claimant demoted promotes something else.
The review has to look in both directions, not only at the names that fall.

Suggested order:

1. **Measure first, change nothing.** For all 1,066 nodes dump `deg`, `prog_deg`,
   `denial_deg`, claim weight, C/A/D and score. How many nodes have a `prog_deg` made
   mostly of `witness-chain`? How many edges carry `claimTier` 2 or 3? Write the numbers
   into the note before choosing.
2. **Try lever 2 alone**: drop `witness-chain` out of `PROGRAM_EDGES`, leaving it in plain
   degree at x1.0. Re-grade, diff `tools/REGRADE_REPORT.json`, read what moves.
3. **Try lever 1 alone**: weight each edge by its `claimTier` in the counters, for example
   Tier 1 at 1.0, Tier 2 at 0.5, Tier 3 at 0.25. Re-grade, diff, read.
4. **Choose on the evidence and write why in a note.** Both may be right. Lever 2 alone may
   be enough, and it is the smaller change.
5. Only then the full gate.

**The test of a good outcome is not "McCandlish is no longer Tier A".** It is that the
nodes which move DOWN are ones whose standing rests on testimony, and the nodes which move
UP are ones whose standing rests on documents. Read a sample of BOTH directions by hand.
If documented nodes are falling, the fix is wrong.

### 3c. Cautions

- `verify.py` asserts on the shipped board that a Tier A node has a sourced URL. The
  `s *= 0.35` discount at line 136 and the explicit `new == "A"` demotion at about line 266
  are two halves of one rule. Do not disturb either.
- `REGRADE_REPORT.json` already lists **684 moved nodes on a normal run**, so "lots moved"
  is not by itself a signal. Compare against a baseline run on the same data.
- `tools/GOLDEN.json` will move on the tier distribution lines. Update it **deliberately**
  with `python tools/verify.py --update-golden`, never by hand.
- `merge.py` and `regrade.py` share id rules through `from merge import canonical_id`. Do
  not fork that.
- Regenerate the NotebookLM export afterwards.
- Full gate. `capture_strip.js` runs immediately before `audit_independent.py`, every time.

### 3d. Then rebuild the ARV cluster on top

`leads/arv-2026-09-18` was graded under the OLD rule. After the centrality fix lands on
master, rebase or rebuild it so its nodes are graded once under the new rule rather than
twice. Its research files do not change; only the pipeline output does.

**This may also resolve the red check by itself** and the next session should check whether
it does: if `arv-fluxliner` scores lower under the new rule it may fall out of L0, which
empties the `witness x program` cell the failure traces to. If that happens it is a real
outcome and not a dodge, but **say so explicitly in the note**, because it means the hub is
no longer on the top-level map and that is a visible change to what section 3b asked for.

## 4. Then, in Stewart's order

| # | job | notes |
|---|---|---|
| 1 | **The centrality fix** | Section 3 above |
| 2 | **TR-3B, the next witness-band hub** | `research/leads/CANDIDATES-2026-09-18-ARVP.md` section B is the brief. Same shape as the ARV and a bigger case: one of the most repeated craft claims in the subject, tracing to one named claimant, Edgar Fouche, 1998, and the board carries nothing for it. **This is also Stewart's chosen option 1 for the red check**: TR-3B is `program` class in the `witness` band, so it populates the cell `arv-fluxliner` currently occupies alone. Open Fouche's 1998 presentation and the "military documents" the arvp site links, and find the sceptical literature, BEFORE building |
| 3 | **Gate ARV and TR-3B together and push both** | Ask Stewart first, as always |
| 4 | **The propulsion-mechanism strand. APPROVED by Stewart, 18 September** | `notes/PROPULSION-CLAIMS-2026-09-18.md` is the brief. For each claimed mechanism, record what the cited document actually claims. Brown and Pais are already on the board; **US 3,322,374 (King, 1967) was opened this session** and is the missing piece: a real MHD patent, private inventor, no assignee, no secrecy order, zero occurrences of "scalar", "spin" or "gravity". It is informative precisely because it is ordinary. Do NOT drop it into the Pais patents view, which exists because the Navy filed those |
| 5 | **The rest of the canon pass** | The audit's passes 1, 3, 4, then 5 (nuclear, brief in `HANDOFF-2026-09-18.md` section 3b), then the rest |
| 6 | **Retire the old shell** | Unchanged, `HANDOFF-2026-09-12.md` section 3 item 1. The `runtime_check.js` flake dies with it |
| 7 | **Tier option C** | Unchanged |

## 5. Carried forward, unbuilt, BY NAME

The coverage audit's own process finding is that a candidates file with unbuilt rows must
be carried in the handoff by name until built or refused. These are all unbuilt.

**From `research/leads/CANDIDATES-2026-09-18-ARVP.md`**, found on the site Stewart pointed
at and checked against the board:

- **Ben Rich.** Director of Lockheed's Skunk Works 1975 to 1991, fully documented, and the
  board already carries `lockheed-skunk-works` with **no node for the man who ran it**. He
  is NOT in the coverage audit's 149. **So the 149 is a floor, not a ceiling**, and that is
  the most useful thing this session learned about the audit
- **TR-3B** (see section 4), **Edgar Fouche**, **Michael Herrera** (audit band 1),
  **Edgar Mitchell** (audit band 1), **Michael Schratt** (audit passes 2 and 13),
  **Jim Goodall**, **James Fox**, **Jeremy Rys / AlienScientist**, **Jeffrey Richelson**,
  **Office of Global Access**
- Already on the board, no action: Dolan, Vallee, Greenewald, Puthoff, Jake Barber, Michels

**From `notes/PROPULSION-CLAIMS-2026-09-18.md`:** US 3,322,374 (King, 1967), opened.

## 6. Source-identity fact, so nobody logs it as a contradiction again

**American Alchemy and Jesse Michels are the same person and the same channel.** Stewart
confirmed it on 18 September: treat them interchangeably. The corpora on disk say American
Alchemy and use titles that no longer match; YouTube now serves the channel as Jesse
Michels and at least one episode has been retitled. **Identify those episodes by video id,
never by title or channel name.** The board carries `jesse-michels`; there is no separate
American Alchemy node and there should not be one.

## 7. Three things about this session's mechanics

- **Sonnet subagents stalled twice** waiting on their own background jobs and returned
  "I'll wait" instead of a report, after burning 140k to 250k tokens each. `TaskStop` plus
  running the gate directly from the orchestrator was faster and cheaper. For long
  mechanical sequences, prefer one backgrounded shell command over a subagent.
- **`state_snapshot.py --gate` runs the ENTIRE gate itself**, including the double-build
  `--idempotent` pass. Running it and then the individual checks runs everything twice. Use
  one or the other.
- The repo's `.gh-token` is stale and returns HTTP 401. The keyring login works: do not
  export `GH_TOKEN`, it overrides the good credential.

## 8. A note on the analyst chips, for Stewart

`data/analyst-suggestions.json` is marked "Stewart's decisions only" in CLAUDE.md. This
session edited it and should say so plainly. `build_app_data.py` carries a check,
`check_chip_figures`, added 11 September and **never tripped until now**: three chips quote
board counts in their prose, a `_figures` block declares what they quote, and any research
pass that moves a count leaves a chip quietly wrong.

Four figures were updated, 913 to 931, 137 to 139, 1,057 to 1,066, 514 to 516. **No
question was reworded.** The reasoning: the question is Stewart's editorial decision, the
number is the board's fact, and the check exists to force the number to track. If he would
rather a chip stopped quoting a live count at all, that is a real editorial choice and it
is his.
