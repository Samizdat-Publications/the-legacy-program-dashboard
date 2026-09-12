# The demotion rule is scoped to the node, not to the claim, 12 September 2026

Found by the analyst, on its third live question, unprompted. Written up here
because it is a research decision and research decisions are Stewart's.

## 1. What it said

Asked "what are this node's Tier 1 claims, and which one is weakest?" on
`battelle`, it named claim 3, the H. C. Cross memorandum of 9 January 1953, and
gave this reason:

> The identical assertions sit on `pentacle-memorandum`, and there they have been
> demoted to Tier 2 with the explicit note "DEMOTED from Tier 1 (node carries no
> primary-record URL); needs primary replacement". On `battelle` the same fact is
> still graded T1.

## 2. It is right, and this is why

| | |
|---|---|
| `battelle` | T1. Source: "CUFON transcription; Jacques Vallee, Forbidden Science" |
| `pentacle-memorandum` | T2. Source: the same, plus "DEMOTED from Tier 1 (node carries no primary-record URL); needs primary replacement" |

Both come from one record, `research/ffrdcs.json`, where all three instances of
this assertion are authored at tier 1 (`.people[7].claims[0]`,
`.entities[10].claims[1]`, `.entities[13].claims[0]`).

The split happens in `remediate_tiers` in `tools/merge.py`. Read the first two
lines of its body:

```python
urls = " ".join(s.get("url", "") for s in n.get("sources", []))
has_primary = bool(PRIMARY_URL_PAT.search(urls))
```

`has_primary` is a property of the **node**, not of the claim. `battelle` carries
primary URLs for other things entirely: its PNNL contract on USAspending, NASA
SP-5110 on NTRS. `pentacle-memorandum` carries none. So the same claim, with the
same sources, is demoted on the node that has no primary record anywhere and
survives at Tier 1 on the node that has one for something else.

## 3. How big the class is

Every figure below was derived from `app/public/data/claims.json` on 12 September
2026, by normalising each claim's source string with the demotion note stripped
and looking for strings that appear both demoted and still at Tier 1.

| | |
|---|---|
| Source strings demoted on one node and still Tier 1 on another | 26 |
| Tier 1 claims riding on one of those 26 | 72 |
| Tier 1 claims in total | 3,367 |

**And a large part of that 72 is the rule working correctly, not the artefact.**
`remediate_tiers` has four separate demotion grounds and only one of them is
node-scoped. The AARO one is claim-scoped and is doing exactly what CLAUDE.md
section 2 asks of it: an AARO-sourced claim that says what AARO *said* keeps Tier
1, and one that asserts an external fact on AARO's word is demoted. That is why
`aaro-historical-record-vol1` carries both T1 and demoted claims from the same
PDF, and nothing is wrong with that.

So the 72 is an upper bound on the class, not a count of defects. Separating them
is per-claim judgement, which is why this note stops here.

## 4. The decision, for Stewart

Three ways to go, and they are not equal.

| | What it means |
|---|---|
| **A. Leave it** | The board keeps one claim at T1 whose own twin says it cannot be T1. The contradiction is visible to any reader who opens both nodes, and the analyst now finds it on request |
| **B. Fix the instance** | Demote the `battelle` and `h-c-cross` copies of the 1953 memorandum claim to T2 by hand, in `research/ffrdcs.json`, with the same reason. Small, safe, and leaves the rule as it is. T1 3,367 to 3,365 |
| **C. Fix the rule** | Make the no-primary-record ground claim-scoped rather than node-scoped in `remediate_tiers`. Correct, and it moves an unknown number of the other 71 claims. Needs the gate, the golden manifest and a re-read of what moved |

**B is the recommendation** and C is a session of its own. B is applying an
adjudication this repo has already made and written down, to the two copies it
was not applied to. C changes the rule that made it, and a rule change that moves
claims off Tier 1 across the board is the kind of thing that should be read
before it is merged, not merged and then read.

Neither was done on 12 September, because both change claim tiers and
`CLAUDE.md` section 6 is explicit that tiers are the ammunition grading. The
counts that would move with either: `index.json`, the golden manifest,
`_figures` in `data/analyst-suggestions.json` (which declares 514 Tier 3 claims,
unaffected by B), and the NotebookLM export.

## 5. What is NOT a defect, so nobody chases it

A source string carrying claims at more than one tier is normal and there are 102
of them over 706 claims. A primary document backs Tier 1 quotations of what it
says and Tier 3 inferences drawn from it, and both cite the same URL. Any check
written on "same source, different tier" would fire on all 706 and teach the next
session to ignore it. The narrow pattern in section 3, demoted on one node and
Tier 1 on another, is the one that carries signal, and even that is an upper
bound.
