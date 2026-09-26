# Phase 7, detailed: the relationship vocabulary (plus P5c)

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 7" and the blind critic's
round-0 finding that some connections sit under the wrong relationship (a reporting-duty link under
Money). Branch `redesign/p7-predicates`, worktree `C:\Users\stewa\ClaudeProjects\tp-p7`. Opus 5.5, high.

## Task 0 (P5c): bookkeeping rows are not claims

39 Tier 3 "claims" from `research/_stubs.json` carry the text "Referenced by the board but no dossier
written yet..." and the source "Board bookkeeping". They are notes about the board, not claims about the
world. `merge.py` routes a claim whose source is exactly "Board bookkeeping" to a node field
`boardNote` (text kept verbatim); it no longer counts as a claim. The node page shows it as a plain notice
("No dossier yet: ..."). A verify check with a poison: no claim's source is "Board bookkeeping". GOLDEN
moves by exactly 39 Tier 3 claims; the Tier 3 chip numeral in `data/analyst-suggestions.json` follows.

## Task 1: the predicates

About 40 predicates in about 11 families in `schema/vocab.json`, each with `id`, `family`, a forward label
and an inverse label (so an edge reads as a sentence from either end: "funded" / "was funded by"), and the
classes allowed as subject and object. Draft from the redesign's section 4b, grounded in the 35 authored
verbs phase 3 kept (`authoredVerb`) and a sample of 200 edges read in full. Every predicate maps to exactly
one of the twelve existing types (types stay; predicates refine them); a fallback `connected_to` exists
for the genuinely unclassifiable. Families replace the phase 1 layers as the grouping on the page.

## Task 2: the side-car

`research/_predicates.json`, keyed by edge id (phase 4's stable ids): `{ predicate, subject: "a" | "b",
by, confidence, reviewed }`. `subject` records direction: which end the forward label reads from.
`build_app_data.py` joins it onto connections (predicate, family, the label as read from this node, and
direction). A verify check: every key is a live edge id (an orphaned key is an error, which forces a
re-classification when an edge's label changes).

## Task 3: classification

One coordinator agent runs about 18 Sonnet 5 classifiers of about 155 edges each (2,788 edges). Input per
edge: both endpoints' labels and classes, the type, the sentence, the note, the authored verb, the tier.
Output per edge: predicate, subject, confidence. Two Opus 5.5 reviewers take every low-confidence edge
and a 10% random sample; the disagreement rate goes in the phase note, and above 10% the vocabulary is
revised and the pass re-run for the affected families. Denial edges keep their adjudicated direction
(`denialKind`, `denier`): a predicate may never contradict an adjudication.

## Task 4: checks, with poisons

Every edge has a predicate; `connected_to` at most 3%; the predicate's allowed classes hold for its
subject and object; a predicate never changes a tier (claim and edge tiers equal before and after the
join); the side-car has no orphaned keys; a denial predicate's subject equals its adjudicated denier.

## Task 5: the app

Connections group by family, then by predicate, reading as sentences from this node ("funded
AAWSAP", "was funded by the DIA"), with a direction arrow now that direction is recorded and the inverse
label on the far end; C22 updated to restate the families and read direction; the neighbourhood (list view
on phones, ring on laptops) filters by family. The blind critic loop until the worst in-scope issue is
minor (`notes/critic/p7-round-N.md`).

## Acceptance

Gate green; predicate coverage 100% with `connected_to` at most 3%; disagreement rate recorded; the
critic's connection-group finding closed.
