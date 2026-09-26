# Phase 7: how the 2,788 edges got their predicates

Written 26 September 2026 by the phase 7 coordinator (Opus 5.5), for tasks 0 to 4 of
`notes/plans/P7-relationship-vocabulary.md`. Task 5 (the app) is not done here.

## Task 0 (P5c)

The 39 rows sourced exactly "Board bookkeeping" (written by `tools/make_stubs.py` on structural
stubs) now leave the claims in `merge.py` (`route_board_notes`) and ship as the node's `boardNote`,
text verbatim. GOLDEN moved by exactly 39 Tier 3 claims (619 to 580). No node tier moved; the
`tierRationale` scores of those 39 nodes fell by the lost Tier 3 weight. The Tier 3 chip numeral and
`_figures` in `data/analyst-suggestions.json` follow (619 to 580, wording untouched). Check: "no
claim is board bookkeeping" (three poisons: the note back among the claims, an emptied note, a stale
app `claims.json` row). "Every authored claim reaches the board or is listed" counts a bookkeeping
row as placed when it is the node's `boardNote`.

## The vocabulary

`schema/vocab.json`: `predicateRules`, `predicateFamilies` (14) and `predicates` (65), each with a
forward and an inverse label, the classes allowed as subject and object (a domain node is allowed
anywhere), the type it refines, and a "use when" line. Grounded in the 35 authored verbs and a
seeded sample of 200 edges read in full (`tools/predicates/edge_packets.py --sample 200`), then a
200-edge Sonnet pilot. Final counts, from `research/_predicates.json`:

| Family | Predicates | Edges | Per predicate |
|---|---|---|---|
| Roles (`role`) | 6 | 334 | held_post 128, led 68, appointed 6, member_of 57, founded 31, worked_with 44 |
| Organisation (`organisation`) | 6 | 377 | part_of 148, outside_of 43, succeeded 34, ran 68, produced 78, same_as 6 |
| Money (`money`) | 2 | 44 | funded 27, contracted 17 |
| Custody (`custody`) | 4 | 85 | holds 54, alleged_to_hold 10, transferred 19, analysed_material 2 |
| Law (`law`) | 6 | 196 | created 43, governs 68, amended 11, implements 16, mandated 27, sponsored_law 31 |
| Oversight (`oversight`) | 5 | 158 | oversaw 30, investigated 59, questioned 17, reports_to 29, requested 23 |
| Testimony (`testimony`) | 9 | 354 | testified_at 43, witnessed 71, made_claims_about 82, corroborated 12, contradicts 17, brought_to_record 70, told 20, acknowledged 21, alleged_tie 18 |
| Denials (`denial`) | 5 | 190 | denied 46, refused 53, disputed 44, explained_away 14, omitted 33 |
| Documents (`documents`) | 6 | 404 | wrote 165, published 50, released 23, concerns 101, cites 56, studied 9 |
| Media (`media`) | 3 | 55 | reported_on 24, appeared_on 16, interviewed 15 |
| Place and time (`place-time`) | 6 | 251 | located_at 74, occurred_at 44, preceded 39, concurrent_with 19, led_to 60, responded_to 15 |
| Conduct (`conduct`) | 3 | 37 | supported 16, acted_against 6, in_contact_with 15 |
| The board's reading (`analysis`) | 3 | 291 | exemplifies 160, parallels 84, affects 47 |
| Other links (`other`) | 1 | 12 | connected_to 12 |

**`connected_to`: 12 of 2,788 (0.4%)**, against a cap of 3%. Confidence: 1,929 high, 786 medium,
73 low. 370 rows are `reviewed: true`; 111 carry the reviewer's answer.

Fourteen families rather than the draft's eleven: `conduct` (reprisal, contact, endorsement),
`analysis` (the board's own analytic links, 291 edges, which would otherwise have been forced into
`connected_to`) and `other` (the fallback alone). 65 predicates rather than about 40, because the
pilot and the reviewers kept finding real relations with nowhere to go.

## The process, and the disagreement rate

1. **Round 1.** 18 Sonnet batches of about 155 (seven re-run as halves after stalls), each validated
   by `tools/predicates/validate_batch.py`. The vocabulary grew during the run (`acknowledged`,
   `alleged_tie`, `outside_of`, `appointed`; events allowed as deniers), so later batches had words
   earlier ones did not. Two Opus reviewers re-derived every low edge (97) plus a seeded 10% sample
   (269): **disagreement 35.2% overall, 25.7% on the random sample, 27.9% at family level.**
2. **Where it clustered:** the exclusion predicate most classifiers never had (`outside_of`, about
   20 of 129); seats vs posts (`held_post`/`member_of`); the routes into the public record
   (`published`, `brought_to_record`, `reported_on`, `holds`); about vs asserting vs citing
   (`concerns`, `made_claims_about`, `cites`); and the analytic links (`affects`, `parallels`,
   `exemplifies`, `connected_to`). By family: analysis 20 of 48, other 11 of 17, denial 11 of 24.
3. **Revised:** added `concurrent_with` and `supported`; widened the classes of `reports_to`,
   `oversaw`, `holds`, `governs` and `implements`; and wrote a tie-breaker section into the brief,
   one rule per confusable pair (`notes/plans/P7-classifier-brief-r2.md`, the brief as sent).
4. **Round 2.** All 2,788 edges re-classified under the one final vocabulary (18 Sonnet batches,
   15 re-run after a server rate-limit, resuming from their own part files). Two fresh Opus reviewers
   took every low edge (101) plus a new seeded 10% sample (269). **Disagreement: 30.0% overall,
   21.2% on the random sample (53.5% on the low edges), 14.9% at family level on the random
   sample.** The reviewer's answer stands on every reviewed edge.

**The 10% target was not met, and one more vocabulary round would not meet it.** The evidence: 68
edges were re-derived by both rounds' Opus reviewers, and those two disagreed on 22 of them (32%;
mostly low-confidence edges). Sonnet round 1 against Sonnet round 2 changed 22% of predicates. The
ceiling is the grain of 65 predicates on sentences written for twelve types, not the classifiers.
Round 2's residue is diffuse: testimony 20 of 54, analysis 21 of 55, the rest small. The page groups
by family, where the random-sample rate is 14.9%. Options for the orchestrator, not taken here:
coarsen the analysis family to one predicate; have Opus re-derive the analysis and testimony
families wholesale (about 645 edges); or accept family as the reliable unit and show the predicate
as the label only.

### The resolution (the orchestrator's decision, 26 September 2026)

**The family is the reliable unit, and the page is built on it.** Family-level disagreement on the
random sample is 14.9%, against 21.2% at predicate level (30.0% on all reviewed edges, 53.5% on the
low ones), and two Opus reviewers disagreed with each other on 32% of the hard edges both saw. So:

- connections group by family;
- a predicate's own label, and the direction arrow, are shown only where its confidence is `high`
  (1,931 of 2,788 edges, 69%). A reviewed row's confidence is the reviewer's, whether the reviewer
  agreed or its answer stands;
- every other row reads its family's neutral `phrase` (`schema/vocab.json`, for example "linked
  through money"), with no direction;
- the authored sentence stays on every row, so no link loses its explanation.

`build_app_data.py` ships `predicateShown` and the displayed `verb` on each connection and `shown`
on each `edges.json` row. `verify.py` and the audit restate the rule (the audit from the side-car's
confidence, not the shipped flag), and a poison prints a medium-confidence predicate's own label.

**The chair rule** (the orchestrator's): a chair or head of a body is `led`; `member_of` is plain
membership. Applied as a targeted pass (`tools/predicates/apply_chair_rule.py`) over every edge
whose sentence says chair, preside, head or seat: 5 rows changed (a subcommittee chairwoman to
`led`; a vice chairman to `member_of`; two chaired hearings to `oversaw`, which the vocabulary gives
for presiding over a hearing; a team chair whose far end is the parent agency to `held_post`).
Seats on the Waived SAP Notification Group held by virtue of chairing another committee stay
`member_of`.

The round-2 brief's inconsistency, now settled by that rule: the chair of a committee that is itself the
object falls under both the "seats" rule (`member_of`) and the "heading the body" rule (`led`).
Reviewers chose `member_of`; the classifiers split. Settle it in the brief before any re-run.

## Types that look wrong under their predicate

1,439 edges carry a predicate that refines a type other than their own. The edge's type is never
changed by a predicate; these are for phase R. The notable ones:

| Type | Edges | In its own family | Where the rest went |
|---|---|---|---|
| `funding` ("Money") | 78 | 32 in money | analysis 10, organisation 8, place-time 6, law 6: most "Money" links are not about money, which is the critic's round-0 finding |
| `custody` | 161 | 57 in custody | documents 43 (publishing and writing), testimony 17, analysis 15 |
| `denial` | 226 | 161 in Denials | testimony 21, analysis 15, organisation 9: 65 denial-typed edges are not denials (reprisal, a claim, a pattern) |
| `behavioral` ("Conduct") | 84 | 10 in conduct | analysis 23, Denials 13, testimony 10 |
| `research` | 216 | 100 in documents | analysis 45 |

29 edges of other types carry a Denials predicate.

## Checks (task 4), each with poisons

In `verify.py`, all shown rejecting their poisons in `--self-test` (poisons on the real side-car and
the real shipped files):

| Check | Poisons |
|---|---|
| every edge carries a predicate from the vocabulary, and the app ships it | row missing; unknown predicate; no provenance; a connection reading the forward label from the object's side; a connection with no family; a stale `edges.json` predicate |
| connected_to is at most 3% of edges | 4% of rows set to `connected_to` |
| every predicate's classes hold at both ends | a document that "wrote" its author; a symmetric predicate recorded on b |
| the predicate join changes no tier | a connection's claim tier; a node file's claim tier; an `edges.json` tier |
| no predicate names an edge that is not on the board | an orphaned key |
| a denial predicate's subject is the adjudicated denier | a denial predicate turned round |

`audit_independent.py` restates the six by another route: the families and the symmetric set
restated, ids and tiers from the shipped `edges.json`, classes from the node files, the denier read
from `data/denial-adjudication.json` through the aliases. One verdict names a denier who is neither
end (`e-1b634c1982`, Kingston George, author of the document at one end); both routes exempt it.

## Files

`research/_predicates.json` (the side-car, key `predicates`, named out of the node-document globs
in `merge.py` and the audit); `tools/predicates/` (packets, table, validator, sampler, merge);
`build_app_data.py` joins it onto `edges.json` (`predicate`, `subject`) and every connection
(`predicate`, `family`, `verb`, `predicateSide`). An orphaned key or an unknown predicate stops the
build. The working files (batches, answers, briefs, statistics) stayed in `.scratch/`, uncommitted.

## Task 5 and the blind critic (26 September 2026)

The node page, the phone neighbourhood and the report group connections by family, then by predicate;
each row reads from this node, with a direction arrow only where the predicate is shown. The ring and
the phone list filter by family (one select, so the ring's strip keeps its height). C22 restates the
fourteen families and their order and reads every drawn arrow against `edges.json`'s own `subject`;
its poison turns one arrow round and two assertions fail. App checks on 4179: 146 pass, C29 fails off
4173 by design.

Three critic rounds (`notes/critic/p7-round-1.md` to `-3.md`). The critic named the connections column
the best thing on the site in rounds 1 and 3.

| Round | In-scope finding | Done |
|---|---|---|
| 1 | most ring spokes carried a bare tier; the 1366 strip clipped mid-word after the family select arrived (a defect this phase introduced) | every hop-1 name carries a reason; the strip drops the bit its own button shows |
| 2 | a bare family word misleads on the ring (a newspaper as "testimony") | the ring reads each link from the neighbour ("Susan Gough denied", "Eric Burlison appointed") where the predicate is shown; family phrases now read into the name ("linked by a role to Garry Nolan") |
| 3 | where the predicate is not shown, the ring still names a category ("place or time link T3", "board inference link T1") | not fixed: this is the display rule working as decided (31% of edges show only their family). The authored sentence is on the node page and the phone list for every link; putting it in the ring's hover title is a small follow-up |

Recorded for other phases, not in phase 7's scope:

- testimony and office statements carry T1 with a "said on the record" chip, against the home page's
  tier definitions (all three rounds; a tier-presentation decision for Stewart);
- the case against sits in its own column, not beside the claim it answers; one "not verified" card is
  a sourcing to-do that mentions Wikipedia (node page);
- the 1366 map draws no links and shows unnamed "+N" chips (phase 11);
- the timeline axis ends on an amber 2029, labels carry no dates on desktop, and same-day duplicate
  events (TTSA formed/launches, NYT AATIP) (timeline phase and phase R);
- duplicate edges with one sentence at two tiers (Grusch to UAPTF, `held_post` T2 and `member_of` T1):
  a phase R dedupe;
- patent drawing captions off by one; two UAPDA definition claims padding Grusch's Tier 1 count; the
  hop-2 margin names with no "via whom".
