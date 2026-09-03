# Brief for a verification agent (Danny Jones corpus candidates, 3 September 2026)

You hold five or six candidates chosen by the orchestrating session from section A
of the six triage files `research/leads/dannyjones-triage-1.md` to `-6.md`. For
each, open the record that would justify a node and say what it actually says. You
write one verification file. You do not add anything to the board, and you do not
run git or the build.

## Read first

1. `CLAUDE.md` section 2. The one rule: nothing is asserted that was not opened.
   A search-result snippet is not an opened document. If a record cannot be
   opened from here, the verdict is NOT OPENED and you say what you tried.
2. `research/leads/VERIFY-BRIEF-2026-09-02.md` (the Michels brief): the verdict
   vocabulary, the draft-node shape and its rules all apply here unchanged.
3. `research/leads/verified-area52-1.md`: the format, in use yesterday. Copy
   its shape: a status header, a summary table with a verdict per lead, then one
   section per lead with the URL opened, what the document is, what it
   establishes, what the transcript claimed that it does NOT establish, and the
   draft node in a fenced JSON block.
4. Your candidates' rows in the triage file named in your instructions, which
   cite the lead maps (`research/leads/dannyjones-corpus-NN.md`) and timestamps;
   read those rows and the lead-map rows behind them for what the speakers
   actually claimed. The transcripts are in `dist/transcripts/md/` (file names
   carry a date prefix and a space) and carry no speaker labels: attribute a
   claim to a guest only where the passage makes it clear who is talking.

## What reaches from this machine

This is Stewart's Windows machine, not the cloud container the earlier briefs
described. WebFetch and WebSearch are available. Yesterday's verifiers reached:
`govinfo.gov`, `congress.gov`, `archive.org` (including the `archive.org/details/DTIC_*`
mirror and the CIA reading-room mirror at
`archive.org/download/cia-readingroom-document-<docnum>/`), `theblackvault.com`,
`irp.fas.org`, `vault.fbi.gov`, `nicap.org`, `history.state.gov`, `nasa.gov`,
`oversight.house.gov`, `patents.google.com`, `uspto.gov`, `sec.gov` EDGAR,
`maryferrell.org` and `archives.gov` for JFK records. `cia.gov/readingroom` may
loop; use the archive.org mirror. `web.archive.org` has not reached from any
session. A wall is a NOT OPENED, not a guess.

## Judgement calls specific to this corpus

- Several Danny Jones guests are ex-intelligence officers speaking from memory.
  An officer's own service dates and offices need a record (a court filing, a
  published official biography, a congressional record, a book's own front
  matter is NOT a record), not their say-so on a podcast.
- Where a triage row says "resolution mine" (a `[PHON?]` caption resolved by the
  triage agent), the identity is part of what you verify; say whether the
  opened record supports it.
- A person candidate needs the office and its dates from a record (a
  confirmation, an official biography, an order), not a biography page.
- An event candidate needs the official file or report on that event, and the
  draft node's `date` is the record's date, not the speaker's.
- A document candidate (a JFK-records release, a CIA reading-room document, a
  patent) needs the document itself opened and its own identifiers copied.
- Where the record contradicts the speaker, keep the contradiction: it is the
  finding, and the draft node's desc says so.
- The board carries 1,027 nodes including the fifty built on 2 September (see
  the triage brief's list). Grep `data/the-program.json` for an id before
  drafting an edge to it, and never draft an edge to an id you did not find.

## Rules

- Never invent a URL, a document number, a date or a quotation. Copy them from
  the page you opened.
- Quote no more than a short phrase, except a claim's own quoted source text,
  which may be one sentence.
- No em dashes. Straight quotes. Tables where the content is comparative.
- Write only `research/leads/verified-dannyjones-N.md` where N is your agent
  number.

## When you finish

Reply with your agent number, the verdicts in one line each, and anything that
contradicted the transcript or the triage row. Under twelve lines.
