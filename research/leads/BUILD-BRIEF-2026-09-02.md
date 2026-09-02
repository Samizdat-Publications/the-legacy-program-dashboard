# Brief for the build agent (Michels corpus, 2 September 2026)

Stewart approved every decision in `research/leads/CANDIDATES-2026-09-02-MICHELS.md` this
morning. You turn the approved drafts into research records the merge accepts, apply the
corrections the records force on existing nodes, and prove it with the merge and verify.
You do NOT run the browser gate, commit, or deploy; the orchestrating session does those.

## Read first

1. `CLAUDE.md` sections 2, 3 and 6.
2. `research/leads/CANDIDATES-2026-09-02-MICHELS.md`: sections A (rows 1 to 12), A2 (rows
   21 to 23) and B (rows 13 to 16) are approved. Rows 17 to 20, 24 and 25 are NOT built.
3. The five verification files `research/leads/verified-michels-1.md` to `-5.md`, which
   carry a fenced JSON draft per row. The drafts were written by five different agents and
   their shapes differ; you normalise them.
4. `research/legacy-1947-86.json`, the 30 August research file, as the shape to match
   exactly: top-level keys `domain`, `people`, `entities`, `edges`, `timeline`,
   `entityInfo`, `gaps`. Read one person, one entity, one edge, one timeline event and one
   gap from it before writing anything.
5. `tools/merge.py` lines 60 to 75 for the valid vocabularies: `cls` in {person,
   institution, program, location, domain, legislation, document, event}; `cluster` in
   {legacy, contractor, ffrdc, ic, oversight, witness, research, media, other}; `tier` in
   {A, B, C}; edge `type` in {institutional, geographic, research, temporal, behavioral,
   programmatic, investigative, witness-chain, custody, funding, denial, legislative};
   timeline `strand` in {program, witness, oversight, coverup}; `precision` in {day,
   month, year, ranged}.

## What you write

**One new file, `research/michels-2026-09-02.json`**, with `"domain": "michels-2026-09-02"`.

- People (Malmgren, Bissell, Inman, Gise, Puharich, Trudeau, Bedell Smith, Dulles) go in
  `people` with the person shape: `id, label, cls: "person", status, date, age, loc, locId,
  instId, sub, cluster, tier, C, A, D, domains, narrative, claims, sources, unverified`.
  `narrative` is the prose field for a person; a draft that used `desc` is renamed.
  `status` is "deceased" or "active" as the record shows; `date` is the record's date for
  the person's key act; `age` may be null; `locId` and `instId` must be existing node ids
  or null.
- Everything else goes in `entities` with the entity shape: `id, cls, label, cluster, sub,
  tier, C, A, D, dateStart, dateEnd, desc, claims, sources`. Every entity needs C, A and D
  (0 to 3 each, per CLAUDE.md section 6: custody proximity, access level, disclosure
  role); give the verifier's values where present and reason from the record otherwise,
  saying so in `tierRationale`.
- Every draft's `edges` array comes OUT of the node and INTO the file's top-level `edges`,
  in the edge shape: `a, b, type, claimTier, label, dateStart, dateEnd, sources, note`.
  Both ends must be existing node ids (check `data/the-program.json` with grep) or ids
  defined in this file. An edge the verifier marked draft-only, or whose target does not
  exist, is dropped and the reason goes in `gaps`.
- Every claim has `tier` (1, 2 or 3) and `source` (a string naming the document and its
  URL). Tier 1 only for what the opened record itself states. Claims about what a podcast
  guest said are Tier 2 and name the episode and timestamp. Claims sourced only to
  aaro.mil or defense.gov cap at Tier 2 unless they are about what that document says.
- `sources` is a list of `{name, url, date}` objects, `date` ISO or null.
- `timeline`: one event per dated record worth a place on the axis (the 1946 Act, the
  Bluegill shot on 1962-10-25, the Church Committee report, the MOL release of
  2015-10-22, the 1955 Silver Bug report, the 1959 lunar study, NICAP's 1956
  incorporation), with `id` starting `tl-`, `strand`, `date`, `precision`, `label`, `text`,
  and a `source`.
- `gaps`: one entry per NOT OPENED item the decision list names (the Albuquerque
  directorship, the AEC grant to Puharich, the DC incorporation filing, the OCRD FTD, the
  current PRP manual), and one per dropped edge. Shape as in the 30 August file.
- The four transcript contradictions the decision list calls findings (Bluegill's date and
  contents, Inman and SAIC, the Church Committee's own account, Silver Bug's purpose) go
  into the node's `desc` and a Tier 1 claim each, sourced to the opened record.

**Corrections to existing nodes**, as records in `research/_corrections.json` where the
field is a replacement, or as additions in the file that already owns the node where it
is a new claim or source (find the owner with grep on `"id": "<id>"` across `research/`):

- `missing-scientists-probe-2026`: the Committee's letters of 20 April 2026 say "at least
  ten" and "began in 2023". Add a Tier 1 claim quoting the letter with its
  oversight.house.gov URL from verified-michels-4.md, and correct the node's own figures
  where they say eleven and 2022, keeping the Fox News figure as what Fox reported.
- `yankee-blue`: add the WSJ article as a source with the republication URL and Salas's
  rebuttal URL from verified-michels-4.md.
- `afit-townsend-2008`: an edge to `defense-support-program` (type research, Tier 2) with
  the note that the thesis's "ballistic missile early warning satellites in GEO" is the
  DSP constellation and that no opened government document names it.
- `eric-wang`: leave as is; the Stansel material was not verified by a record and goes in
  `gaps`.
- `george-trimble`: leave as is; the Institute of Field Physics funding claim was not
  verified and goes in `gaps`.

## Prove it

Run, from the repo root, and paste the tails into your reply:

    python tools/merge.py
    python tools/verify.py

`merge.py` must report `rejects 0` and no `dangling` problems in its integrity block for
your ids. `verify.py` will fail only on `counts match the golden manifest` (that is the
expected drift and the orchestrator refreshes it); every other check must pass. If a
check names one of your records, fix the record, not the check.

## Rules

- No em dashes anywhere in the JSON. Straight quotes inside strings are escaped.
- No invented URLs, dates, document numbers or quotations: everything copied from the
  verification files, which copied it from the opened pages.
- Ids are lower-case hyphenated and must not collide with existing ids (grep first).
- Do not edit `tools/`, `data/`, `dist/`, or any note. Do not run `regrade.py` or the
  browser checks.

## When you finish

Reply with: the file's counts (people, entities, edges, timeline, gaps), the merge and
verify tails, every edge you dropped and why, and any place you had to reason a C/A/D or
tier value rather than copy it. Under twenty lines.
