# Phase 5, detailed: drafting the topics

Written 25 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 5". Branch
`redesign/p5-drafting-topics`, in the worktree `C:\Users\stewa\ClaudeProjects\tp-p5`. Opus 5.5, high.
Input: the 93 draft stubs in `research/topics/` (phase 4, not yet reviewed by Stewart: if he edits the
table, only the changed topics are redrafted).

## The drafted record (fields added to each stub)

```
status      "draft" (stub only) | "drafted" | "verified"
lead        { text, cite: [ids] }            one or two sentences a reader meets first
summary     [ { text, cite: [ids] } ]        what this topic is about, in order
record      [ { text, cite: [ids] } ]        what the documents show
claimed     [ { text, cite: [ids] } ]        what people say, named as testimony or allegation
contested   [ { text, cite: [ids] } ]        the case against, and disagreements between records
members     [ { id, role } ]                 role from schema/vocab.json topicRoles
questions   [ text ]                         open questions, in the topic's own words, cite-free
related     [ topic ids ]
```

`cite` ids are claim ids (`c-...`) or edge ids (`e-...`) from phase 4. **Roles**
(`topicRoles` in `schema/vocab.json`): subject, official, investigator, witness, claimant, critic,
researcher, journalist, contractor, legislator, document, law, programme, institution, place, event.

## Task 1: the topic checks first (verify.py, each with a poison; restated in audit_independent.py)

For every topic whose status is not "draft":

1. every member exists after alias resolution, and its role is in `topicRoles`;
2. every cited id exists; a claim id belongs to a member (or to the topic's `unplacedClaims`); an edge id
   joins two members;
3. every `lead`, `summary`, `record`, `claimed` and `contested` item cites at least one id;
4. every quoted string (inside straight or curly double quotes, four characters or more) appears verbatim
   in a cited claim's text or edge sentence;
5. no URL in any topic text;
6. **a `record` item cites at least one Tier 1 claim or Tier 1 edge** (the record is what the documents
   show; testimony belongs in `claimed`);
7. fewer than 6 members fails unless the topic is `research-gap`;
8. every `related` id is a topic;
9. coverage (nodes and people in at least one topic's `members`) is reported and must not fall below
   `tools/TOPIC-COVERAGE-FLOOR.json`, which is committed at the drafted level.

## Task 2: the packets and the drafting fan-out

- `tools/topics/topic_packet.py <topic-id>` prints everything a drafter may use, fetched from the built
  board, never paraphrased: the stub; its proposals with signals; each proposed member's label, class,
  dates, desc, claims (id, tier, text, source) and case against; the sourced edges between proposed
  members (id, type, tier, sentence, sources).
- One coordinator agent runs about 8 Opus drafters of about 12 topics each. Rules for drafters: cite
  ids; paraphrase only what the cited claims say; no outside facts; testimony is Tier 2 and is called
  testimony; the case against goes in `contested`; a member is included only if a cited item or a
  sourced edge ties it to the topic; no em dashes.
- Two Opus verifiers work from the packets and the drafted records alone, never the drafters' notes:
  the unsupported sentence, the missing counter-claim, the wrong role. Failures go back to a drafter once,
  then to the orchestrator. A topic that passes is `verified`.

## Task 3: absorb the domain nodes, ship the data

- `build_app_data.py` writes `absorbedBy: <topic id>` on each absorbed `d-*` node's file (the page redirect
  comes with the topic page in phase 6; the analyst's tools skip them in phase 12).
- `app/public/data/topics.json`: id, title, kind, section, span, focusEra, lead, status, counts.
  `app/public/data/topics/<id>.json`: the record with every cited id resolved to its claim or edge (text,
  tier, source, node). `--check` re-derives the counts. `check_rebuild.py` covers both.

## Acceptance

All topic checks and poisons green; coverage 90% of nodes and 95% of people in `members`, or the
shortfall listed by id in `notes/STATE.md` with reasons; every hub of degree 30 or more in 3 or more
topics; gate green; merged and deployed (topics ship as data only; nothing a reader sees changes until
phase 6).
