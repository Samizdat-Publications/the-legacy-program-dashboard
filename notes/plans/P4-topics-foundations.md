# Phase 4, detailed: stable ids, entity resolution, the taxonomy (drafted)

Written 25 September 2026. Branch `redesign/p4-topics-foundations`, cut from master after phase 3 lands.

**Effort, stated plainly.** The plan marks this phase MAX because task 3 decides what the board's topics
are. This session runs at high and cannot raise its own effort (the harness refuses that for a session's
own turns). So: tasks 1, 2, 4 and 5 are mechanical given the decisions below and run here; task 3's
output is a DRAFT table for Stewart, marked as drafted at high effort. Nothing a reader sees depends on it
until phase 6, which merges only after Stewart's look. If Stewart wants the taxonomy re-decided at max, a
max session re-runs task 3 from `research/topics/` and phase 5 redrafts only the topics that change.

## Task 1: stable ids

- claim `id` = `c-` + first 10 hex of sha1(node id + `|` + NFC-normalised, whitespace-collapsed text);
  edge `id` = `e-` + first 10 hex of sha1(sorted endpoints + `|` + type + `|` + normalised label); a
  collision is a hard error in `merge.py`.
- Shipped in `claims.json`, `edges.json` and node files (claims, connections, denials).
- verify: ids unique; `--idempotent` already proves stability across two builds (ids are content).
  Poison: two claims forced to one id.

## Task 2: entity resolution

Input: the reviewed decisions in `notes/plans/P4-dedupe-decisions.md` (25 MERGE clusters, 32 aliases,
reviewed by an Opus agent from the records; 77 look-alikes kept apart on purpose, listed there).

- Each merge becomes an alias in `research/_removed.json`. Phase 3 made a collapsed node's claims,
  sources, conflicts, unverified notes and open questions follow it to the survivor.
- Where the loser and the survivor disagree (the Grusch interview-memo count; the Hegseth remark's date;
  the TTSA CRADA end date; Division F against Division G for IAA FY2024 section 7343; two person dates),
  both statements are carried and the disagreement goes into the survivor's `conflicts`. Nothing is
  deleted without the source being opened.
- The task-force survivor is an institution, as both losers were.
- Side-cars re-pointed: `data/denial-adjudication.json` (seven merges), `data/l0-shorts.json`
  (nara-rg615, waived-usap-mechanism), dossier files (dodig, nara-rg615, waived-usap-mechanism: their
  dossier text merges into the survivor's; the map loses two nodes).
- UNSURE, decided: the four act-versus-UAP-section pairs stay separate (a whole act and its section are
  different documents; topics group them). `iaa-fy2024-sec-1102` and `iaa-fy2024-sec1104` stay separate
  (the same provision in two bills).
- verify: no alias target is itself aliased; no side-car (threads, highlights, shorts, denial
  adjudication, dossiers, topics) references an aliased id. Poison each.

## Task 3: the sections and topics (DRAFT)

Re-run `tools/analysis/structure/` on the merged board. Validate Appendix T against it: every topic 6 or
more members, or merged, or marked `research-gap`. Write `research/topics/_sections.json` and one stub
per topic (`id`, `title`, `kind`, `section`, `span`, `anchors`, `absorbs`, `essays`, `status: draft`).
The table goes to Stewart in chat.

## Task 4: membership proposals

`tools/topics/propose_members.py` writes `research/topics/_proposals.json` (generated), each proposal with
its signals: community co-membership, anchor neighbourhoods at 1 and 2 hops on backbone edges, domain
node memberships and person topic tags, research-file slugs, thread and highlight membership. Coverage is
reported against the targets (90% of nodes, 95% of people).

## Task 5: the domain nodes and essays

For each `d-*` node, the topic that absorbs it or the explainer topic it becomes (`absorbs`); the
unplaced entityInfo essays attach to topics (`essays`).

## Acceptance

Ids shipped and checked; aliases applied with the candidate list re-run showing zero open duplicates;
sections, stubs and proposals committed; the table sent to Stewart; gate green.
