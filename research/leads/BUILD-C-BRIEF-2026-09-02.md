# Brief for the section C build agent (Michels corpus, 2 September 2026)

Six verification agents adjudicated the section C rows of the Michels triage files,
the material the transcripts carry about nodes the board already holds. Their files
are `research/leads/verified-michels-C-1.md` to `-C-6.md`. Stewart has approved
every decision in this pass in advance ("I'm good with all decisions"). You apply
the ATTRIBUTE and RECORD drafts to the board as additive corrections, prove it with
the merge and verify, and stop. You do not run the browser gate, commit, or deploy.

## Read first

1. `CLAUDE.md` sections 2, 3 and 6.
2. `research/leads/VERIFY-C-BRIEF-2026-09-02.md`: the verdict vocabulary and the
   additive record shape the verifiers drafted to.
3. All six verification files. Each has a summary table and, per ATTRIBUTE or
   RECORD row, a fenced JSON block.
4. `research/_corrections.json` in full: how existing additive corrections are
   written, and `tools/merge.py` around `_corrections` for what the merge does with
   a record there (claims and sources are ADDED to the node; a field like `desc`
   REPLACES; an id that does not exist on the board is rejected). Also read
   `removeClaims` in the missing-scientists-probe-2026 record for the shape used
   when a claim must come out.

## What you write

Additive records in `research/_corrections.json`, one per node id. Several nodes
were drafted by more than one agent (`thomas-townsend-brown`, `edward-condon`,
`robert-salas`, `robert-sarbacher`, `eric-wang`, `sean-kirkpatrick`,
`kirk-mcconnell`, `robert-hastings` at least): merge those into ONE record per id,
keeping every distinct claim, dropping a duplicate that says the same thing from the
same timestamp, and merging the `sources` lists without duplicate URLs. If a node id
already has a record in `_corrections.json`, extend that record rather than adding a
second one.

Rules for each claim you carry over:

- Tier 2 for anything a speaker said; Tier 1 only where the verifier opened the
  document and the claim is about what the document says; Tier 3 only where the
  verifier marked the speaker's own inference (agent 2's EG&G row).
- The claim text must not assert the podcast claim as fact. The verifiers wrote
  them in the "On <show>, <date>, <speaker> said ..." form; keep that form.
- `source` strings and `sources` entries are copied verbatim. No URL that is not in
  a verification file. No em dashes.
- `cls` is copied from the node, and the node id must exist in
  `data/the-program.json` (grep before writing).
- A `desc` replacement only where the verifier gave both the sentence to replace
  and the replacement (agent 2's `sperry-rand`; check the others). Apply it by
  replacing that sentence inside the node's current desc, not by rewriting the
  desc. Two nodes agent 3 and agent 1 both flagged as contradicted by a record
  (`thomas-townsend-brown` FBI file, `edward-condon` LA-1, `george-trimble` UNC
  history) get the Tier 1 finding as a claim; do not rewrite their desc unless
  the verifier supplied the sentences.
- Skip every NO ACTION and NOT REACHED row. On `william-mccasland`, carry agent 4's
  drafts as written (they attribute the SAPOC placement to Michels, hedged) and add
  nothing that places McCasland on a SAPOC as fact. Do not create any node.
- A URL a verifier marked NOT OPENED (battelle.org behind a bot wall, for one) may
  appear only inside a `gaps` entry as the address that was tried, never in a
  claim's `source` or a node's `sources`.
- Agent 4's `stargate-program` RECORD supplies a URL for a sentence the node
  already quotes: add the source and the Tier 1 claim; leave the two narrative
  phrases it could not find where they are but add them to `gaps` in a new file
  `research/michels-2026-09-02-c.json` with `"domain": "michels-2026-09-02-c"`,
  shape as in `research/michels-2026-09-02.json` (empty people/entities/edges/
  timeline arrays are fine) holding a `gaps` entry for each NOT OPENED document
  the verifiers named (the Hippler memo, the Gunston Air International 2000
  article, the 1961 RAND report, the Compton FBI FOIA reply, the NNSA FOIA reply,
  the Battelle row, the Stargate phrases, and any other the files call NOT
  OPENED or NOT REACHED with a named document).

## Prove it

From the repo root:

    python tools/merge.py
    python tools/verify.py

`merge.py` must report `rejects 0`. `verify.py` will fail only on
`counts match the golden manifest`; every other check must pass. If a check names
one of your records, fix the record, not the check.

## Rules

- No em dashes, straight quotes, indent 1, newline at end of file, ASCII apart
  from what the drafts contain.
- Do not edit `tools/`, `data/`, `dist/` or any note. Do not run `regrade.py`, git,
  or the browser checks.

## When you finish

Reply with: number of node records written or extended, total claims and sources
added, the merged-duplicate ids, the gaps count, the merge and verify tails, and
anything you had to decide rather than copy. Under twenty lines.
