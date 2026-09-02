# Brief for a triage agent (Area 52 corpus, 2 September 2026)

You are one of five agents. Each holds four or five lead maps and the list of names from
them that the board has never heard of. Your job is to say which of those names
could become a node on this board, and what document would have to be opened to
justify it. You do not open documents and you do not add anything to the board.

## Read first

1. `CLAUDE.md` sections 1, 2 and 6 (what the board is, the one rule, the two
   grading systems). Ten minutes; it governs everything below.
2. `research/leads/README.md` (what a lead map is and is not).
3. `research/leads/CANDIDATES-2026-09-02-MICHELS.md`, this morning's decision list
   from the Michels corpus, and `research/leads/CANDIDATES-2026-08-30.md` sections
   A and E: that is the standard a candidate has to meet, and section E
   shows what a deliberate exclusion looks like.
4. Your lead maps, `research/leads/area52-corpus-NN.md` (group 1 holds batches 01
   to 05, group 2 06 to 10, group 3 11 to 14, group 4 15 to 19, group 5 20 to 23, group 6 24 to 27),
   and your ABSENT list, `research/leads/area52-absent/group-G.tsv` (name, batch, and where the
   cross-check found a near miss in the board's prose).

## What you write

One file, `research/leads/area52-triage-G.md`, with four sections. Tables, not
prose. Every row cites the lead map and timestamp it came from.

**A. Document-backed candidates.** A name the speaker ties to a specific record:
a report, memo, letter, patent, hearing, statute, contract, FOIA case, accession
number, court filing, corporate record, or a dated official publication. For
each: the name, its class on this board (person, institution, program, document,
event, location, legislation), the record that would justify it, where to look
for that record (an archive, a docket, a reading room, a patent number), and one
line on why it belongs on THIS board rather than on a general UFO timeline. Rank
the section: the candidates that would change the board's argument first. Aim
for the strongest ten to twenty, not everything.

**B. Needs a document.** Names that matter to the programme structure but rest
only on what a speaker says. One line each: what is claimed and what record
would settle it. These are research questions for later, not candidates.

**C. Corrections to existing nodes.** Where a lead map records something about
a node the board already carries (the cross-check called it NODE or PROSE) that
the board seems not to have: a date, a role, a document, a denial. Name the node
id if you can find it in `data/the-program.json` (it is 8 MB; grep it, do not
read it).

**D. Noise, and why.** Everything else, grouped: guests' biographies, celebrities,
places named in passing, folklore, names that resolve to nothing. One line per
group with counts, and the names, so the next pass can see what was excluded.

## What the Michels pass taught, and this corpus adds

- The Michels pass built 20 nodes from 1,609 names; the strongest candidates were
  the ones a speaker tied to a record that could be opened (a DTIC report number,
  a statute, a Church Committee volume, a NASA release). Several transcript claims
  were CONTRADICTED by the record once opened, and those contradictions were the
  most valuable rows. Prefer a candidate with a findable record over a famous one.
- The verifiers found that the lead maps had attributed host remarks to guests
  because the transcripts carry no speaker labels. Where a row's importance rests
  on WHO said it, re-read the passage before ranking it.
- Much of this corpus is contactee, abduction and channeling material, and
  several episodes are the host reading a document or a book aloud (the Lacerta
  files, the MJ-12 manual, Lear's 1987 text, a Redfern chapter, a fictional
  serial). A name that exists only inside a read-aloud document is not a
  candidate unless the document itself is a record the board could hold (an
  authenticated release, a filed FOIA, a statute). Say which read-aloud documents
  you excluded and why.
- Names now on the board since this morning include Harald Malmgren, Bobby Ray
  Inman, Richard Bissell, Lawrence Gise, Andrija Puharich, Arthur Trudeau, Walter
  Bedell Smith, Allen Dulles, the AEC, Bluegill Triple Prime, TRW, the Invention
  Secrecy Act, the PRP, MOL, DSP, Silver Bug, AFSWC TR-59-39, the Church
  Committee, the Atomic Energy Act of 1946 and NICAP; and `william-mccasland`,
  `richard-doty`, `james-lacatski` and `jay-stratton` may already exist under
  those ids. Grep before calling any of them new.

## Rules

- A speaker naming a thing is not evidence the thing exists. Section A is for
  names tied to a record, and the record is the thing to be opened later.
- The board caps claims sourced to AARO or DoD at Tier 2 unless the claim is
  about what the document says. Keep that in mind when you write "why it
  belongs".
- Where the same name appears in more than one lead map, say so; recurrence
  across different guests is the signal the board's owner cares most about.
- `[PHON?]` and `[UNRESOLVED]` names were left out of your list on purpose. If a
  lead map shows one that clearly resolves to a real, well-attested figure (the
  guest "Harald Malmgren" is the standing example, corrupted five ways across the
  corpus), you may carry it into B with the resolution stated as yours.
- No em dashes. No quotation longer than a short phrase. Do not edit any other
  file. Do not run the build.

## When you finish

Reply with your group number, the counts per section, and the three candidates
you would put first. Under twelve lines.
