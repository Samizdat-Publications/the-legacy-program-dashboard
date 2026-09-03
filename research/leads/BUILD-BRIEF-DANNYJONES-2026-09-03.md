# Brief for the build agent (Danny Jones corpus, 3 September 2026)

The decision list is `research/leads/CANDIDATES-2026-09-03-DANNYJONES.md`. Every row in
its section A (and A2 if present) is to be built; section C's corrections are to be
applied; section B is NOT built. You turn the verifiers' drafts into research records
the merge accepts and prove it with the merge and verify. You do NOT run the browser
gate, regrade, git, or deploy.

## Read first

1. `CLAUDE.md` sections 2, 3 and 6.
2. `research/leads/BUILD-BRIEF-2026-09-02.md`, the Michels build brief. Every rule in
   it applies here unchanged: the file shape (`domain`, `people`, `entities`, `edges`,
   `timeline`, `entityInfo`, `gaps`), the person and entity shapes, the vocabularies in
   `tools/merge.py` lines 60 to 75, edges lifted out of drafts into the top-level
   `edges` with both ends existing, claims with `tier` and `source`, AARO and DoD
   sources capped at Tier 2, `sources` as objects, timeline events, gaps for every NOT
   OPENED item, no em dashes, indent 1.
3. `research/area52-2026-09-02.json` as the shape to match exactly (it is the most
   recent sibling and carries every field the merge wants).
4. The verification files `research/leads/verified-dannyjones-1.md` onward, each
   carrying a draft JSON per row. Shapes differ between agents; you normalise them.
   Where a draft carries no `tier` or C/A/D, reason them from the record and say so in
   `tierRationale`.

## What you write

**One new file: `research/dannyjones-2026-09-03.json`**, with
`"domain": "dannyjones-2026-09-03"`. People in `people`, everything else in
`entities`, per the Michels brief.

Ids are those in the decision list's section A. Grep `data/the-program.json` before
writing each to be sure it does not collide; grep `research/*.json` too.

**Corrections to existing nodes** go in `research/_corrections.json` as additive
records (id, the node's own `cls`, claims, sources), the way the section C pass and
the Area 52 build wrote them; a field replacement is a replacement field in the same
record, with the exact current sentence replaced by the exact new one, not a rewrite
of the desc. Podcast claims about existing nodes are Tier 2 in the form "On the Danny
Jones Podcast, <date>, <speaker> said" and cite the episode by number and timestamp.

**Do not undo** the corrections the records forced this week: `sapoc` established
5 January 1994; ATIC redesignated 1959 and discontinued 1 July 1961 with FTD
constituted the same day; CENTER LANE's office was the Security Support Detachment;
Bluegill 25 October and no debris; Inman never headed SAIC; the Church Committee never
examined agency files itself. Denial direction is the adjudicated `denier` field.

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
