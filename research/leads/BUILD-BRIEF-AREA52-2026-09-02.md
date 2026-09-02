# Brief for the build agent (Area 52 corpus, 2 September 2026)

The decision list is `research/leads/CANDIDATES-2026-09-02-AREA52.md`. Every row in its
section A and A2 is to be built; section C's corrections are to be applied; section B is
NOT built. You turn the verifiers' drafts into research records the merge accepts and
prove it with the merge and verify. You do NOT run the browser gate, regrade, git, or
deploy.

## Read first

1. `CLAUDE.md` sections 2, 3 and 6.
2. `research/leads/BUILD-BRIEF-2026-09-02.md`, this morning's Michels build brief. Every
   rule in it applies here unchanged: the file shape (`domain`, `people`, `entities`,
   `edges`, `timeline`, `entityInfo`, `gaps`), the person and entity shapes, the
   vocabularies in `tools/merge.py` lines 60 to 75, edges lifted out of drafts into the
   top-level `edges` with both ends existing, claims with `tier` and `source`, AARO and
   DoD sources capped at Tier 2, `sources` as objects, timeline events, gaps for every
   NOT OPENED item, no em dashes, indent 1.
3. `research/michels-2026-09-02.json` as the shape to match exactly.
4. The seven verification files `research/leads/verified-area52-1.md` to `-7.md`, each
   carrying a draft JSON per row. Shapes differ between agents; you normalise them.
   Agent 6's drafts carry no `tier` or C/A/D: reason them from the record and say so in
   `tierRationale`.

## What you write

**One new file, `research/michels-2026-09-02.json`'s sibling:
`research/area52-2026-09-02.json`**, with `"domain": "area52-2026-09-02"`. People in
`people`, everything else in `entities`, per the Michels brief.

Ids are those in the decision list's section A (and A2). Grep `data/the-program.json`
before writing each to be sure it does not collide; grep `research/*.json` too.

**Corrections to existing nodes** go in `research/_corrections.json` as additive
records (id, the node's own `cls`, claims, sources), the way this afternoon's section C
pass wrote them; a field replacement (`sapoc`'s `dateStart` and its establishment
sentence; `atic`'s lineage sentence) is a replacement field in the same record, with
the exact current sentence replaced by the exact new one, not a rewrite of the desc.
The `sapoc` correction is the important one: the board says 2010 and the 1994 bulletin
says 5 January 1994. Quote the bulletin. Keep the 2010 directive as a later instrument.

**The three duplicate collapses** are already in `research/_removed.json` and
`_corrections.json`; do not touch them, but expect `merge.py` to report the three
removed ids and the re-pointed edges.

## Prove it

    python tools/merge.py
    python tools/verify.py

`merge.py` must report `rejects 0` and no dangling references. `verify.py` will fail
only on `counts match the golden manifest`; every other check must pass. If a check
names one of your records, fix the record, not the check.

## When you finish

Reply with: the file's counts (people, entities, edges, timeline, gaps), the corrections
written, the merge and verify tails, every edge you dropped and why, and every C/A/D or
tier you reasoned rather than copied. Under twenty lines.
