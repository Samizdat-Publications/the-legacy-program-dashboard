# Brief for a verification agent (Michels corpus candidates, 2 September 2026)

You hold five candidates from `research/leads/CANDIDATES-2026-09-02-MICHELS-DRAFT.md`.
For each, open the record that would justify a node and say what it actually says.
You write a verification file. You do not add anything to the board.

## Read first

1. `CLAUDE.md` section 2. The one rule: nothing is asserted that was not opened.
   A search-result snippet is not an opened document. If a record cannot be
   opened from here, the verdict is NOT OPENED and you say what you tried.
2. `research/leads/verified-institutional.md`: the format. Copy its shape: a
   status header, a summary table with a verdict per lead, then one section per
   lead with the URL opened, what the document is, what it establishes, what
   the transcript claimed that it does NOT establish, and the draft node.
3. The candidate's rows in the triage files (`research/leads/michels-triage-G.md`)
   and the lead-map rows they cite, for what the speakers actually claimed.

## Verdicts

CONFIRMED (the record exists, was opened, and supports the node), PARTLY
CONFIRMED (the record exists but supports less than the transcript claimed; say
exactly what), CONTRADICTED (the record says otherwise; this is a finding, keep
it), NOT OPENED (say what was tried and where the record should be).

## What reaches from this environment

`govinfo.gov`, `congress.gov`, `archive.org` (including `archive.org/details/DTIC_*`,
the DTIC mirror), `theblackvault.com`, `irp.fas.org`, `fas.org`, `nro.gov`,
`cia.gov` reading room, `sec.gov` EDGAR, `uspto.gov` and `patents.google.com`,
`history.state.gov`, `hansard.parliament.uk`, `nasa.gov` all answer to WebFetch.
`web.archive.org` does not reach at all. `aaro.mil` and `dia.mil` refuse curl but
answer WebFetch. NewsNation and some news sites sit behind bot walls; a wall is a
NOT OPENED, not a guess.

## The draft node

For a CONFIRMED or PARTLY CONFIRMED lead, draft the node the way the research
files are written (look at one record in `research/legacy-1947-86.json` for the
shape): `id` (lower-case, hyphenated), `cls` (person, institution, program,
document, event, location, legislation), `label`, `dateStart`/`dateEnd` or `date`,
a `desc` of two to four sentences, two to five claims each with `tier` and a
`source` naming the document and its URL, `sources`, and the edges to EXISTING
node ids with a type from: institutional, geographic, research, temporal,
behavioral, programmatic, investigative, witness-chain, custody, funding, denial,
legislative, and a one-sentence note per edge. Tier 1 only for what the opened
record itself states. A claim about what a podcast guest said is Tier 2 at most
and names the episode and timestamp. Claims sourced only to aaro.mil or
defense.gov cap at Tier 2 unless they are about what that document says.

Draft the JSON in a fenced block inside the markdown. Do not write into
`research/*.json`.

## Rules

- Never invent a URL, a document number, a date or a quotation. Copy them from
  the page you opened.
- Quote no more than a short phrase, except a claim's own quoted source text,
  which may be one sentence.
- No em dashes. Tables where the content is comparative.
- Write only `research/leads/verified-michels-N.md` where N is your agent number.

## When you finish

Reply with your agent number, the five verdicts in one line each, and anything
that contradicted the transcript. Under twelve lines.
