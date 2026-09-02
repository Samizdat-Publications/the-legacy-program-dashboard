# Brief for a verification agent (Area 52 corpus candidates, 2 September 2026)

You hold five or six candidates chosen by the orchestrating session from section A
of the five triage files `research/leads/area52-triage-1.md` to `-5.md`. For each,
open the record that would justify a node and say what it actually says. You
write one verification file. You do not add anything to the board, and you do
not run git or the build.

## Read first

1. `CLAUDE.md` section 2. The one rule: nothing is asserted that was not opened.
   A search-result snippet is not an opened document. If a record cannot be
   opened from here, the verdict is NOT OPENED and you say what you tried.
2. `research/leads/VERIFY-BRIEF-2026-09-02.md` (the Michels brief): the verdict
   vocabulary, the draft-node shape and its rules all apply here unchanged.
3. `research/leads/verified-michels-1.md`: the format, in use this morning. Copy
   its shape: a status header, a summary table with a verdict per lead, then one
   section per lead with the URL opened, what the document is, what it
   establishes, what the transcript claimed that it does NOT establish, and the
   draft node in a fenced JSON block.
4. Your candidates' rows in the triage file named in your instructions, which
   cite the lead maps (`research/leads/area52-corpus-NN.md`) and timestamps;
   read those rows and the lead-map rows behind them for what the speakers
   actually claimed. The transcripts are in `dist/transcripts/md/` and carry no
   speaker labels: attribute a claim to a guest only where the passage makes it
   clear who is talking.

## What reaches from this machine, as of today

Reaches: `govinfo.gov`, `congress.gov`, `archive.org` (including the
`archive.org/details/DTIC_*` mirror and the CIA reading-room mirror at
`archive.org/download/cia-readingroom-document-<docnum>/`), `theblackvault.com`,
`irp.fas.org`, `vault.fbi.gov`, `nicap.org`, `history.state.gov`, `nasa.gov`,
`boe.es`, `lanl.gov`, `physics.unc.edu`, `oversight.house.gov`, `burlison.house.gov`
(recent press page only), `patents.google.com`, `uspto.gov`.

Refuses or fails: `web.archive.org` (does not reach at all), `cia.gov/readingroom`
(302 loop; use the archive.org mirror), `nro.gov`, `esd.whs.mil`, `spaceforce.mil`,
`nsa.gov`, `dodig.mil`, `hansard.parliament.uk`, `rand.org`, `battelle.org`
(Cloudflare wall), NewsNation. `sec.gov` needs a browser user agent on curl.
`aaro.mil` and `dia.mil` refuse curl but answer WebFetch. `fas.org` (not irp)
served a zero-byte 202 this morning. A wall is a NOT OPENED, not a guess.

## Judgement calls specific to this corpus

- Several Area 52 episodes are the host reading a document aloud. A record that
  exists only inside such a reading is not a record. Open the thing itself.
- Where a triage row says "resolution mine" (a `[PHON?]` caption resolved by the
  triage agent), the identity is part of what you verify; say whether the
  opened record supports it.
- A person candidate needs the office and its dates from a record (a
  confirmation, an official biography, an order), not a biography page.
- An event candidate needs the official file or report on that event, and the
  draft node's `date` is the record's date, not the speaker's.
- Where the record contradicts the speaker, keep the contradiction: it is the
  finding, and the draft node's desc says so.
- The board already carries: the twenty Michels nodes built this morning
  (`atomic-energy-commission`, `nicap`, `church-committee`, `sandia`, and so on),
  `sapoc`, `stargate-program`, `center-lane`, `uk-mod`, `uk-defe24`, `atic`,
  `nasic`, `bdm-international`, `mufon`, `kit-green`, `william-mccasland`,
  `john-podesta`. Grep `data/the-program.json` for an id before drafting an edge
  to it, and never draft an edge to an id you did not find.

## Rules

- Never invent a URL, a document number, a date or a quotation. Copy them from
  the page you opened.
- Quote no more than a short phrase, except a claim's own quoted source text,
  which may be one sentence.
- No em dashes. Straight quotes. Tables where the content is comparative.
- Write only `research/leads/verified-area52-N.md` where N is your agent number.

## When you finish

Reply with your agent number, the verdicts in one line each, and anything that
contradicted the transcript or the triage row. Under twelve lines.
