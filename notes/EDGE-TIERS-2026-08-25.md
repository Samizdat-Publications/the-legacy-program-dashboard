# The grade that was never audited

**25 August 2026**

## What happened

Restoring the 732 bare-string sources `norm_source` had been dropping (see
`notes/SILENT-REJECTS-2026-08-25.md` for the sibling finding) put citations back
on 23 edges that a previous pass had recorded as UNSOURCED. Two of them landed
oddly:

| edge | tier | only source |
|---|---|---|
| `setka-program -> izmiran` | 1 | debunker.com |
| `vincent-teofilo -> lockheed-martin` | 1 | a legacy.com obituary |

Tier 1 renders in the dock as **"Tier 1 · documented"**, and the board's own copy
tells the reader that Tier 1 is "what survives a hostile audit". Neither of those
sources is a primary record. So the question was whether edge tiers are subject to
the source-quality rules the board already applies to claims.

They were not.

`merge.py::remediate_tiers()` — the honesty pass, which demotes a Tier 1 claim
whose only support is an encyclopedia entry or a video — walks `people` and
`entities`. Edges are not in it. An edge's `claimTier` was whatever the research
authored, merged across duplicates by `min()`, and audited by nothing at any
point in the pipeline. `tools/GOLDEN.json` tracked `claim_tiers` and not edge
tiers, so no count moved when the grade drifted.

## The scale of it

Of 1,476 Tier 1 edges, **93 held the board's highest evidentiary grade with no
primary record anywhere on the edge and an encyclopedic source as their only
support**:

| what the edge was cited to | edges |
|---|---|
| Wikipedia | 60 |
| YouTube | 24 |
| blogspot | 3 |
| other wiki | 3 |
| medium.com | 1 |
| substack | 1 |
| podcast | 1 |

Among them: George Knapp to Harry Reid, George Knapp to Robert Bigelow, Leslie
Kean to David Grusch, Daniel Sheehan to Luis Elizondo, and every UAP Gerb
investigation edge on the board.

## What was done

Two of the 93 were a sourcing error rather than a grading one. Three edges cited
the AARO Historical Record Report Volume I through a Wikisource page-by-page
transcription; the DOPSR-cleared PDF of the same document was already cited on a
sibling edge in the same file. Those two edges gained the record itself, keeping
the Wikisource cite for its page number. Nothing was invented — the URL was
already on the board.

The remaining **91 were demoted to Tier 2** by a new `remediate_edge_tiers()`
pass in `merge.py`, applying to edges the rule `remediate_tiers()` already applies
to claims. Edge tiers now read 1,385 / 575 / 199.

A demoted edge is not a removed edge. Nothing was collapsed, no note was rewritten
and no relationship left the board. Only the grade changed, and it changed toward
what the sources actually support.

## What was deliberately not carried over

The **interested-party rule** — which caps a claim at Tier 2 when it rests on
AARO or DoD asserting an external fact — does **not** transfer to edges, and this
is a decision rather than an omission.

It works on claims because a claim's text is a single assertion, so
`ATTRIBUTION_PAT` can ask whether the claim is *about what the interested party
said*. An edge's `note` is a summary of a relationship, and the same test misreads
it. Applied to edges it would demote 49, and most of them wrongly:

- `aaro -> aaro-fy2023-annual-report` is an office publishing its own report. It
  is a primary record by definition.
- Notes phrased "AARO disclosed", "AARO confirms", "AARO refers to Bigelow only
  as...", "AARO's own words" are attribution that the verb list happens not to
  name.

Capping these needs a per-edge reading, not a regex. It stays a research question.
**134 Tier 1 edges rest on an aaro.mil, defense.gov or war.gov URL**, and that
number is worth someone's attention; it is recorded here rather than acted on.

## Where the queue lives

Demoted edges are written to `tools/EDGE-DEMOTIONS.json`, beside
`DEMOTIONS.json`, with the note and source list of each.

They are deliberately **not** flagged in the edge note. The claims pass writes its
flag into `claim.source`, which is not the assertion. The edge analogue would be
the note — and `verify.py::"no edge note leaks build bookkeeping"` already holds
that an edge note carries only what the edge asserts, after twelve notes shipped
carrying collapse provenance. A demotion is editing history, the same category.

## What now stops this recurring

Two things, because the file that was missing was never the problem — nothing was
*looking*:

1. **`verify.py::"no Tier 1 edge rests only on a secondary source"`**, self-tested
   against a poisoned board carrying exactly such an edge. It asserts the rule
   independently of `merge.py`, so removing the remediation pass fails the gate.
2. **`edge_tiers` added to `tools/GOLDEN.json`**. Any future drift in the
   distribution now has to be deliberately accepted and explained in a commit
   message.

## Still open

- 336 Tier 1 edges carry no primary-record URL at all. The 93 above are the subset
  whose sources are affirmatively encyclopedic; the rest are mostly journalism,
  which the claims pass also leaves at Tier 1. Consistent, but the number is
  larger than it looks.
- The 134 interested-party Tier 1 edges described above.
