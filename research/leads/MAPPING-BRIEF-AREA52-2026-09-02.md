# Brief for a transcript-mapping agent (Area 52 corpus, 2 September 2026)

You are extracting LEADS from machine transcripts of the Area 52 podcast (AREA52 -
DEBRIEFED with Chris Ramsay; Ramsay is the host, and a few episodes are panel
recordings with more than one guest). Your batch number NN names a block in
`research/leads/area52-batches.txt`, which lists your four files. You are one of about 27 agents, each holding four episodes. Read
this whole file before opening a transcript.

## What you are producing

Two files, named for your batch number `NN`, written into `research/leads/`:

1. `area52-corpus-NN.md`: the lead map, in the format of
   `research/leads/gerb-corpus-01-12.md`. Open that file first and copy its shape
   exactly: the header block, the corruption key, the file key table, then numbered
   sections of tables. One row per named thing, with the role the SPEAKER assigns
   it, the file number and a timestamp.
2. `area52-candidates-NN.txt`: one name per line, ONLY the names you tagged
   `[CONF]`, for `tools/corpus_crosscheck.py`. Lines starting with `#` are
   comments; put your batch number and the four episode titles at the top.

Write nothing else anywhere. Do not edit any other file. Do not run the build.

## The one rule

`CLAUDE.md` section 2 of this repo: no invented sources, URLs, document numbers or
quotes. **These files are NOT board content and nothing in them is asserted as
true.** They record what a named speaker claims, so that a later pass can check it.
Every proper noun is a lead to verify, not a fact.

The transcripts are machine-generated (faster-whisper) and corrupt proper nouns
silently and plausibly. Tag every name:

- `[CONF]` spelled consistently and matches a well-attested public figure,
  organisation, document or programme you already know exists.
- `[PHON?]` phonetically corrupted; give your best reconstruction with the raw
  transcript form in backticks. A search string, not a fact.
- `[UNRESOLVED]` you could not reconstruct it. Record the raw form.

Never "fix" a name into something you merely think it might be and tag it
`[CONF]`. When in doubt, `[PHON?]`.

## Where the transcripts are

`dist/transcripts/md/`, one Markdown file per episode, with a `**[H:MM:SS]**`
marker every paragraph. Your four files are named in your instructions. Use the
marker nearest the statement as the timestamp, in the form `H:MM:SS`.

## What counts as structural, and what does not

This board maps the alleged US programme for recovering and reverse-engineering
non-human craft, and the custody, access, funding, oversight and disclosure
structures around it, 1944 to now. Record:

- government offices, agencies, panels, committees, units, and named officials
- contractors, laboratories, FFRDCs, companies, universities, and named staff
- programmes, projects, special access programmes, code words, contracts
- documents: reports, memos, letters, patents, hearings, statutes, FOIA case
  numbers, accession numbers, with the date the speaker gives
- named witnesses and what they are said to have seen, held or signed
- money: appropriations, contract values, who paid whom
- foreign counterparts: other governments' programmes and offices
- places tied to the above: bases, ranches, plants, hangars, test ranges

Do NOT record: folklore, ancient history, religion, psychedelics, health, the
guest's biography except where it places them inside the structure above, and
anything that names a private living person only as a rumour target.

An episode can be plainly off-subject (pyramids, telepathy, a music producer). For
those, read the first ten percent and search the file for these words:
`program`, `SAP`, `contract`, `Pentagon`, `DoD`, `CIA`, `DIA`, `NRO`, `AARO`,
`Lockheed`, `Battelle`, `Bigelow`, `Wilson`, `Grusch`, `Elizondo`, `crash`,
`retrieval`, `reverse`, `Roswell`, `patent`, `FOIA`, `hearing`, `Senate`,
`Congress`, `whistleblower`. If nothing structural appears, write one line in the
file key saying so and move on. Do not pad.

## Attribution, learned from the Michels pass

The transcripts carry NO speaker labels. In the Michels pass, most of the errors
the verifiers later found were a host's remark attributed to the guest, or one
anecdote retold by the host counted as three witnesses. So: identify the host and
the guest from the episode's own opening (the header gives the show and the
title; the first minutes give the names), attribute a claim to a speaker only
when the passage makes it clear who is talking, and otherwise write "speaker
unclear" in the speaker column. A host's paraphrase of a guest's story is the
host's, and a story the host tells about a third party is not that third party's
testimony.

## Quotation

No quotation longer than a short phrase. Where the wording matters, give the
timestamp instead so the claim can be re-read at source.

## Style

No em dashes anywhere; use double hyphens or restructure. Tables, not prose.
British spelling is the house style but consistency matters more than which.

## When you finish

Reply with: your batch number, the four titles, how many rows in each section,
how many `[CONF]` names in the candidates file, and any name you think is
important and could not resolve. Under fifteen lines.
