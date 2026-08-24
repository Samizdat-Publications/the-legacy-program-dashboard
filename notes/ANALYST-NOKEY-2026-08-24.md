# The no-key analyst, the highlights layer, and Design's second package

**24 August 2026** · commit `3d89ffa`

---

## 1. The bug that mattered most

`scriptedReply()` — the function that answers every question when no API key is
set — was inherited from the sibling board with **one string swapped**. A reader
without a key asking about this board was answered about JPL headcount, Ning Li
and Jason Thomas: confidently, at length, with real figures, from a different
project.

This is the worst failure mode available on this board, because it is
indistinguishable from the thing working. Nothing errors. Nothing looks broken.

Rewritten: eleven topics covering all seven suggestion chips plus entity lookup,
money, foreign counter-examples and a "where do I start". Every figure is
computed from the loaded data at answer time — nothing is typed as a literal,
because a hardcoded count silently goes stale and no check would catch it.

## 2. The test that passed while six of seven chips were broken

The first version of the test asserted that an answer came back, was long
enough, and emitted parseable commands that exist. All fifteen probes passed.

Six were routing to the wrong branch.

| chip | went to | why |
|---|---|---|
| Trace the custody chain from Grusch | Grusch's dossier | a bare name match beat the topic |
| What is the legal mechanism… | a node dossier | a node label contains the word "oversight" |
| Plot the cover-up strand… | a node dossier | same |
| Chart the board by claim tier… | the hostile-audit topic | `/thinnest/` matched first |
| Export every Tier A node… | the tier topic | tier was checked before export |
| tell me about AAWSAP | the mechanism topic | `/sap/` matches **inside** the word `aawsap` |

The test could not name the branch it expected, so it could not reject a wrong
one. This is the fourth time this session the same lesson has come up in a
different costume, and it is worth stating in its sharpest form yet:

> **A check that cannot say what it expected cannot detect that it got something
> else.** Length, type and validity assertions feel like tests and are not. They
> pass on any well-formed wrong answer.

Rewritten to assert a topic tag on every answer. It then caught all six
immediately. Fixes:

- the entity matcher keys on **id** and **parenthetical acronym** as well as
  label, because `david grusch` does not match the label "David Charles Grusch"
  and `AAWSAP` does not match "Advanced Aerospace Weapon System Applications
  Program (AAWSAP)"
- entity answers are gated on **lookup-shaped phrasing** rather than any name
  appearing anywhere
- `\bsaps?\b` so an acronym cannot match inside a longer word
- explicit action verbs (export) are ordered before descriptive topics (tier)

`tools/test_scripted_analyst.mjs`, wired in as verify check 18, self-tested via
`BREAK=1`. Gate: 18 verify + 38 audit checks, idempotent.

## 3. Also inherited, also wrong, NOT yet fixed

- **The analyst input placeholder** advertised a node id from the sibling board,
  so the very first thing a new reader is invited to type warned "no node with
  that id". Fixed. Note it lives *above* `explainEdge` in the markup, so it
  could not go in the code-scoped patch list — which is exactly how it failed
  on the first attempt.
- **The COVER-UP view still carries the sibling board's skeptical record** — the
  JPL matched-denominator argument, the NeuroLogica entry. Same class of bug as
  `scriptedReply`, different surface, not yet touched. **This is the top item
  for the next pass.**

The general lesson: this board was built by porting a shell, and *every*
inherited surface should be assumed to be answering about the wrong project
until it has been read. Two found today by accident while looking for something
else.

## 4. Design's second package

Both open questions answered, and §6.1 closed.

**Rarity ties → pin AND recompute.** `RARITY_PIN` is the rule; the observed
order is derived every run; `figures.rarityDrift` reports disagreement rather
than obeying it. Current data: zero drift. Legacy data reports the
oversight/disclosure inversion, which is the check working rather than failing.
Do not edit the constant to silence a warning.

**`disclosure` at 3 nodes → do not promote by hand.** A tag claimed by more than
half the map can only win when a node carries nothing rarer, so its population
is a *residual*, not a category. Now labelled as one. Merging it with
`oversight` would destroy the strongest thing the layout says — oversight at
13 of 17 in the last decade is the 79-year gap made visible.

**Two fixes re-applied**, because the package shipped from a baseline predating
them:

1. `fileURLToPath` rather than `.pathname`. A file URL percent-encodes spaces
   and this repo lives under a path with three of them.
2. Capability **detection** rather than a hardcoded `false` for the five fields
   backfilled into `design-extract.json`. This one mattered more than it looks:
   the generator was printing "C/A/D absent from this source" while its own
   `fields` flag said present, and silently taking the degraded band order.
   Two parts of the same program disagreeing, with neither of them wrong enough
   to stop.

## 5. New data layers

**`data/l0-highlights.json`** — 14 flags, draft, each with a stated reason.
Under the 15% cap (16 of 110) with two slots spare. Carries `authoredFor`:
a flag naming a node missing from the board it was written for is fatal, and
the same mismatch on any other dataset is reported. Three of the fourteen are
absent from the superseded 96-node legacy snapshot; they must not be trimmed
away to silence that message.

**`data/l0-images.json`** — plumbed, validating, and deliberately empty.
Fallback order confirmed: **photograph → institutional mark → class letter.**
Currently all 110 draw the class letter, which is a supported state, not a hole.

The register is empty on purpose. A record here asserts that a specific image
exists at a specific URL under a specific licence, and that is a sourcing claim
like any other — the one rule that never bends applies to image URLs exactly as
it applies to document numbers. The file names where to look first and the four
clearance states; filling it is a verification pass, not a guess.

Hardest category, flagged in the file: a private person who gave testimony has
not thereby licensed their likeness. Those default to the class letter.
