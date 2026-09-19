# The denial weighting, measured

19 September 2026. Stewart's decision when the defect was found: do it next session,
measured, the same way the witness-chain question was handled. **This note is the
measurement. No weighting was changed.** One data-quality fix was applied and is in
section 5.

## 1. The defect as found

`tr-3b` came out Tier A on its build, and 16 of its 54 points, 30%, came from four
`denial` edges weighted x4.0.

| node | score | from `denial` |
|---|---|---|
| `tr-3b` | 54 | 16 pts, 4 edges |
| `arv-fluxliner` | 37 | 4 pts, 1 edge |

`centrality()` in `tools/regrade.py` weights denial at x4.0 and its comment gives the
reason: "an entity a government body bothered to deny is, on this board, more interesting
rather than less. This is the stance encoded as arithmetic."

The apparent problem: none of TR-3B's four deniers was a government body. So the weight
meant for official denial was paying out for scholarly refutation, and **the better
refuted a claim is, the higher it ranks.** That reads as the same class of defect as
`witness-chain` sitting in the x3.0 program set.

## 2. The census

205 denial edges on the board after the four clusters of 18-19 September.

| field | coverage |
|---|---|
| `denialKind` present | 172 of 205 |
| `denier` present | 124 of 205 |
| `denialKind: directed` | 124, exactly the set carrying a `denier` |
| `denialKind: association` | 35 |
| `denialKind: undirected` | 13 |
| no `denialKind` at all | 33 |
| claim tiers | T1 122, T2 58, T3 25 |

Top deniers, and they are exactly what the x4.0 was written for:
`aaro-historical-record-vol1` 15, `dod` 12, `susan-gough` 8,
`aaro-fy2025-annual-report` 6, `dia` 5, `sean-kirkpatrick` 5, `cia` 4, `aaro` 4,
`mitre-corporation` 3, `roswell-report-case-closed` 3.

**So the board already carries the machinery to separate official denial from analysis.**
It is not weighted on today.

## 3. The obvious fix was simulated and IT FAILS

Same method as `notes/CENTRALITY-2026-09-18.md` section 3: every node profiled by its own
edge mix before any result was read, then the test the board uses, which is that nodes
moving DOWN should rest on testimony and nodes moving UP on documents.

| variant | moved | fall: testimony | fall: **document** | rise: document | rise: testimony | ratio |
|---|---|---|---|---|---|---|
| only `directed` at x4.0, rest x1.0 | 14 | 3 | **8** | 11 | 1 | 1.6 |
| only a named `denier` at x4.0, rest x1.0 | 14 | 3 | **8** | 11 | 1 | 1.6 |
| `directed` x4.0, others x2.0 | 10 | 3 | **5** | 8 | 1 | 1.8 |

**Eight documented nodes fall.** For comparison, the witness-chain fix that shipped scored
19.5 with zero document-based fallers, and the claim-tier lever that was rejected scored
2.2. These score 1.6 to 1.8, which is worse than the rejected lever.

**Do not ship any of these.** The reason they fail is the 33 edges with no `denialKind`
and the 48 with `association` or `undirected`: down-weighting them demotes nodes whose
standing rests on real official denials that were simply recorded without the field. The
weighting is not the thing that is wrong.

## 4. What is actually wrong, which is narrower and better

**The defect was in the build, not in the rule.** All four of TR-3B's denial edges were
written with no `denialKind` and no `denier`, against a board convention that 172 of 205
edges follow. The Lazar cluster had the same gap on six edges. Those ten edges were the
entire reason `tr-3b` looked inflated.

An edge that says "a named aerospace historian published a specific refutation" and an
edge that says "a real aircraft of the same period is shaped nothing like the claim" are
different kinds of object, and the board has always had a field that says so. Two
clusters built in one night did not fill it in.

So the fix is a discipline, not a constant:

> **Every `denial` edge gets a verdict in `data/denial-adjudication.json`.** `directed`
> when a named person or body made a specific act of denial, with that name in `denier`.
> `association` when the edge records that something tells against a claim without anyone
> having denied it, such as a control case or a prior-art inference. `undirected` when a
> denial was made but the record names no denier.

That is worth a line in `CLAUDE.md` section 2 next time it is touched, and worth a check.

### 4a. WHERE THESE FIELDS LIVE, which cost this session two rebuilds

**`denialKind` and `denier` cannot be set from a research file.** Writing them onto an
edge in `research/*.json` is INERT: `merge.py` drops them silently. They are populated at
`tools/merge.py` line 1145 from a single adjudicated record, `data/denial-adjudication.json`,
keyed `a|b` on the edge's own two ends in record order.

That file explains itself and the reason is good: deriving denial direction from
`[a,b].sort()` had put **22 of the 47 arrowheads on the map the wrong way round**, so
direction became one adjudicated record that every consumer reads instead of re-deriving.
It also treats a verdict matching no edge as an error rather than a no-op, and warns,
because a silently ignored verdict would leave an edge reading as undirected for ever.

**A build session adding denial edges must add their verdicts to that file.** Nothing in
the research schema hints at this, which is why two clusters shipped without it, and it is
the single most useful thing in this note for whoever builds the next cluster.

## 5. Applied this session: eleven verdicts added to the adjudication file

Scoring-neutral today, because `regrade.py` reads only `e["type"]`. It makes the data
correct for whoever does weight this. They went into `data/denial-adjudication.json`,
which took it from 175 verdicts to 186, after a first attempt wrote them into the research
files where they did nothing. See 4a.

| edge | kind | denier |
|---|---|---|
| `peter-merlin` to `tr-3b` | directed | peter-merlin |
| `peter-merlin` to `fouche-military-documents` | directed | peter-merlin |
| `testors-sr-75-kit` to `tr-3b` | association | none |
| `northrop-tacit-blue` to `tr-3b` | association | none |
| `tr-3b` to `darpa` | association | none |
| `tom-mahood` to `s-4-papoose-lake` | directed | tom-mahood |
| `stanton-friedman` to `s-4-papoose-lake` | directed | stanton-friedman |
| `stanton-friedman` to `bob-lazar` | directed | stanton-friedman |
| `tom-mahood` to `bob-lazar` | directed | tom-mahood |
| `tom-mahood` to `element-115-claim` | directed | tom-mahood |
| `lazar-clark-county-1990` to `bob-lazar` | association | none |

The judgement in that table: a named person publishing a specific refutation IS a directed
denial, even though they are not a government body. Merlin and Mahood and Friedman each
did the work and put their name on it. What is not a denial by anybody is a control case
or a court record whose mere existence tells against a self-account.

**Note what this does NOT do.** Merlin's two edges stay `directed`, so under a
directed-only weighting `tr-3b` would keep 8 of its 16 denial points, not 4. Classifying
honestly does not make the number go where a tidy story would want it, and that is the
correct outcome.

## 6. What a future session should do

1. Start from the 23 remaining edges with no `denialKind` and classify them by hand
   against the rule in section 4. That is the real backlog and it is small.
2. Only then re-run the simulation in section 3. With the field complete, the variants may
   behave differently; with it incomplete they cannot be trusted, which is what this note
   demonstrates.
3. Consider whether `association` denials should be a different edge type entirely rather
   than a kind of denial. `northrop-tacit-blue` to `tr-3b` is arguably `research`, and if
   it were, the question in section 1 would largely dissolve without touching any weight.
   **That is the most promising direction and it was not pursued here** because it moves
   edge types on shipped data and deserves its own measured pass.
4. The x4.0 constant itself has not been questioned by any of this and probably should not
   be. What an official denial is worth is a stance, and the board is entitled to it.
