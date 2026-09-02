# Brief for a section C verification agent (Michels corpus, 2 September 2026)

Section C of each `research/leads/michels-triage-G.md` lists things the Michels
transcripts say about nodes the board ALREADY carries. Your job is to turn your
assigned rows into one of three verdicts, and to draft the additive record for the
ones that earn it. You write one file. You do not touch `research/*.json`,
`tools/`, `data/` or `dist/`, and you do not run git.

## Read first

1. `CLAUDE.md` section 2 (nothing asserted that was not opened; no invented URL,
   number, date or quotation; AARO and DoD sources cap at Tier 2 unless the claim
   is about what the document says) and section 6 (claim tiers 1 to 3 are evidence
   strength; node tiers A/B/C are proximity and are not yours to change).
2. `research/leads/VERIFY-BRIEF-2026-09-02.md` for the verdict vocabulary, what
   reaches from this machine, and the record format. Add these reach facts from
   the 2 September pass: `nro.gov`, `esd.whs.mil`, `spaceforce.mil`, `nsa.gov`,
   `dodig.mil` and `hansard.parliament.uk` answer 403 here; `sec.gov` needs a
   browser user agent; `web.archive.org` does not reach; NewsNation is behind a
   bot wall.
3. Your assigned section C rows, and for each row the node's current record:
   grep `"id": "<id>"` across `research/*.json` for the owning file and read the
   node's desc or narrative, claims and sources. The triage row was written from
   a grep of the board; the node may already say more than the row believes.
4. The transcript pointer in the row (`batch / timestamp`): batch NN is
   `research/leads/michels-corpus-NN.md`, whose header names its four episode
   files in `dist/transcripts/md/`. Re-read the passage at the timestamp before
   relying on the lead map's paraphrase. The transcript file's header carries the
   show, the published date and the audio URL; that URL is the only URL you may
   cite for a podcast claim, and only after confirming it is in the header.

## The three verdicts

| Verdict | Meaning | What you draft |
|---|---|---|
| NO ACTION | the board already carries it, the row is a false ABSENT, or the material is a caption corruption worth at most a note | nothing, one line saying why |
| ATTRIBUTE | the transcript claim is checkable only as "a named person said this on this show": worth carrying because it names a source the node otherwise refuses without naming, or records a figure the node gets differently | one Tier 2 claim, text in the form "On <show>, <date>, <speaker> said ..." with the timestamp, source = episode title, date, timestamp and the audio URL from the transcript header |
| RECORD | a document would settle it and you opened one | a Tier 1 claim quoting no more than one sentence of the document, with its URL, and if the document contradicts the transcript, say so in the claim text: the contradiction is the finding |

An ATTRIBUTE claim never states the thing as fact. "Gunston wrote in Air
International in 2000 that ..." is stated by the speaker; unless you open the
Gunston article it stays "Michels said that Gunston wrote ...".

## The output file

Write `research/leads/verified-michels-C-N.md` where N is your agent number.
Format: a status header, a summary table (node id, verdict, one-line reason),
then one section per ATTRIBUTE or RECORD row holding the draft as a fenced JSON
block in the additive `_corrections.json` shape:

```json
{
 "id": "<existing node id>",
 "cls": "<the node's own cls, copied>",
 "claims": [
  {"tier": 2, "text": "...", "source": "..."}
 ],
 "sources": [
  {"name": "...", "url": "...", "date": "YYYY-MM-DD"}
 ]
}
```

`cls` must be copied from the node (a record without it is dropped in silence).
No `desc` replacement unless the record contradicts the node's own words, and
then quote the sentence you would replace and the sentence you would put there.

## Rules

- No em dashes. Straight quotes. Every URL copied from a page you opened or from
  a transcript header you read.
- Quote no more than a short phrase from a transcript; a claim's own quoted
  source text may be one sentence.
- Where two rows in different triage files concern the same node, handle them
  together and say so.
- Under fifty minutes of work: prefer fewer rows done to the standard over all
  rows done loosely, and list the rows you did not reach under NOT REACHED.

## When you finish

Reply with your agent number, a count per verdict, every RECORD that contradicted
the transcript, and the rows not reached. Under twelve lines.
