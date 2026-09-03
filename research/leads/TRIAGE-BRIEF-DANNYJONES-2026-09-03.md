# Brief for a triage agent (Danny Jones corpus, 3 September 2026)

You are one of six agents. Each holds five or ten lead maps and the list of names from
them that the board has never heard of. Your job is to say which of those names
could become a node on this board, and what document would have to be opened to
justify it. You do not open documents and you do not add anything to the board.

## Read first

1. `CLAUDE.md` sections 1, 2 and 6 (what the board is, the one rule, the two
   grading systems). Ten minutes; it governs everything below.
2. `research/leads/README.md` (what a lead map is and is not).
3. `research/leads/CANDIDATES-2026-09-02-AREA52.md`, yesterday's decision list
   from the Area 52 corpus, and `research/leads/CANDIDATES-2026-08-30.md` sections
   A and E: that is the standard a candidate has to meet, and section E shows
   what a deliberate exclusion looks like.
4. Your lead maps, `research/leads/dannyjones-corpus-NN.md` (group 1 holds batches
   01 to 05, group 2 06 to 10, group 3 11 to 15, group 4 16 to 20, group 5 21 to 30 (ten maps,
   most of them thin), group 6 31 to 35), and your ABSENT list,
   `research/leads/dannyjones-absent/group-G.tsv` (name, batch, and where the
   cross-check found a near miss in the board's prose).

## What you write

One file, `research/leads/dannyjones-triage-G.md`, with four sections. Tables, not
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
id if you can find it in `data/the-program.json` (it is 7 MB; grep it, do not
read it).

**D. Noise, and why.** Everything else, grouped: guests' biographies, celebrities,
places named in passing, folklore, names that resolve to nothing. One line per
group with counts, and the names, so the next pass can see what was excluded.

## What the Michels and Area 52 passes taught, and this corpus adds

- The strongest candidates were the ones a speaker tied to a record that could
  be opened (a DTIC report number, a statute, a Church Committee volume, a CIA
  reading-room document number, a NASA release). Several transcript claims were
  CONTRADICTED by the record once opened, and those contradictions were the most
  valuable rows. Prefer a candidate with a findable record over a famous one.
- The verifiers found that the lead maps had attributed host remarks to guests
  because the transcripts carry no speaker labels. Where a row's importance rests
  on WHO said it, re-read the passage before ranking it.
- The Danny Jones corpus is long-form and wide: about a third of the 136 episodes
  are off-subject (pyramids, psychedelics, religion, narcotics, geopolitics) and
  the mappers said so in their file keys. The on-subject yield sits in the
  intelligence-officer interviews (Bustamante, Kiriakou, Madison and others), the
  Ryan Graves and Jeremy Rys episodes, the MK-ULTRA and STARGATE episodes, the
  JFK-records episodes (Newman, DiEugenio) and the Annie Jacobsen episodes. A
  name that only exists inside the narcotics or geopolitics material is noise
  for this board however real it is.
- Names that recur across corpora and deserve a dedicated resolution: "SandCorp"
  (an alleged AARO contractor, three corpora), Alfred O'Donnell (two
  irreconcilable accounts), "Tim Taylor" / Pasulka's "Tyler", and the McCasland
  thread. If your maps carry any of these, put the row in B with what THIS corpus
  adds, and say which other corpora carry it if the lead map notes that.
- The board gained 50 nodes on 2 September (the Michels and Area 52 builds) and
  now stands at 1,027. Among them: Harald Malmgren, Bobby Ray Inman, Richard
  Bissell, Allen Dulles, the AEC, the Church Committee, NICAP, Gordon Gray,
  Sidney Souers, Detlev Bronk, Donald Keyhoe, Donald Menzel, James Forrestal,
  James Angleton, INSCOM, the 902d MI Group, the Monroe Institute, AFSWP, DTRA,
  ONR, the Armed Forces Institute of Pathology, NCIS, the FAA, Betty Sapp, the
  NUFOHRC. Grep before calling any of them new; the cross-check ran against the
  1,027-node board, so a name in your ABSENT list is absent from all of them.

## Rules

- A speaker naming a thing is not evidence the thing exists. Section A is for
  names tied to a record, and the record is the thing to be opened later.
- The board caps claims sourced to AARO or DoD at Tier 2 unless the claim is
  about what the document says. Keep that in mind when you write "why it
  belongs".
- Where the same name appears in more than one lead map, say so; recurrence
  across different guests is the signal the board's owner cares most about.
- `[PHON?]` and `[UNRESOLVED]` names were left out of your list on purpose. If a
  lead map shows one that clearly resolves to a real, well-attested figure, you
  may carry it into B with the resolution stated as yours.
- No em dashes. No quotation longer than a short phrase. Do not edit any other
  file. Do not run the build or git.

## When you finish

Reply with your group number, the counts per section, and the three candidates
you would put first. Under twelve lines.
