# The Program — Data Schema v2
### A companion board to *The Vanishing*, built on the same engine

Source of truth for the format: `the-vanishing-v2.html` (Samizdat-Publications/the-vanishing).
This file records the existing schema exactly, then defines the deltas needed to track
the legacy UAP recovery and reverse-engineering program and the disclosure movement.

---

## PART 1 — The existing schema (unchanged, reproduced for reference)

### Helpers

```js
const P_ = (o) => Object.assign({
  cls: 'person', leftBehind: [], tookWith: [], domains: [], conflicts: [],
  unverified: [], sequenceChain: [], claims: [], chronology: [], sources: [],
  isNonDefense: false, mediaLinkedOnly: false, unexplainedResidual: null
}, o);

const other = (id, cls, label, cluster, sub, desc, srcs) =>
  ({ id, cls, label, cluster, sub, desc: desc || null, sources: srcs || [] });

const E = (a, b, type) => ({ a, b, type });
```

### Person record

```js
P_({
  id, label, status: 'dead'|'missing'|'resolved', date: 'YYYY-MM-DD', age,
  loc, locId, instId, sub, cluster,
  tier: 'A'|'B'|'C', S: 0-3, P: 0-3, I: 0-3,
  domains: ['d-prop', ...],
  narrative: '...',                 // the dossier body
  affiliations: ['Org (years)'],
  tierRationale: '...',
  chronology: [{ date, event, precision: 'day'|'month'|'year'|'ranged' }],
  claims:     [{ tier: 1|2|3, text, source }],
  sources:    [{ name, url, date }],
  leftBehind, tookWith, conflicts, unverified, sequenceChain,
  unexplainedResidual, photoCredit
})
```

### Non-person node classes
`institution` · `program` · `location` · `domain` — all via `other()`, all carrying
`desc` and `sources`. `NODES = [...PEOPLE, ...INSTITUTIONS, ...PROGRAMS, ...LOCATIONS, ...DOMAINS]`.

Long descriptions and sources for non-person nodes live in the side tables
`ENTITY_INFO` and `ENTITY_SOURCES`, keyed by node id.

### Edge types (`EDGE_TYPES`)
`institutional` · `geographic` · `research` · `temporal` · `behavioral` ·
`programmatic` · `investigative` · `witness-chain`

Geographic, research and temporal edges are **derived by rule** from shared
`cluster` / `domains` / dates. `PROGRAM_EDGES` are **hand-written and sourced** —
that distinction is load-bearing and is preserved here.

### Claim tiers (`tabSources`)
`1` Tier 1 · documented — `2` Tier 2 · sourced claim — `3` Tier 3 · inference

### Entity tiers (`TIERS`)
`A` cyan — `B` amber — `C` grey. Meaning is board-specific (see Part 2).

### Other structures
`CLUSTERS` · `AXES` · `STATUS_LABEL` · `TIMELINE` (with `strand`) · `STRANDS` ·
`PRECEDENT` · `SOURCES` · `PHOTOS` · `PRECISION_LABEL`

---

## PART 2 — Deltas for *The Program* board

The engine is unchanged. What changes is the meaning of the scored axes, the tier
definitions, the cluster set, the strand set, and two added node classes.

### Editorial stance

*The Vanishing* holds a case open and lets the prosaic explanation stand where it
holds. **This board does not.** It is built from the premise that a legacy recovery
and reverse-engineering program exists, has existed since the 1940s, and has been
deliberately concealed from Congress and the public. The research question is not
*whether* — it is **who, where, under what authority, and paid for how**.

Official denials are still recorded, in full, with sources — but they are catalogued
as **artifacts of the concealment effort**, not as counterweights. That is what the
new `coverup` strand and the `denial` edge type are for. A denial is data about the
denier.

**The tier system is not hedging — it is ammunition grading.** Tier 1 is what
survives a hostile audit. Tier 3 is where the research goes next. Keeping them
separate is what makes the board usable against a skeptic rather than dismissible by one.

Standing rule that does not bend: **no invented sources, no invented URLs, no
invented document numbers.** If it can't be sourced, it goes in `unverified[]` or
becomes a Tier 3 inference with the reasoning stated. A fabricated citation is the
single fastest way to discredit the whole board.

### New scored axes (replaces S/P/I)

```js
const AXES = [
  { key: 'C', label: 'Custody proximity',
    question: 'How close is this entity to alleged possession of recovered material or craft?' },
  { key: 'A', label: 'Access level',
    question: 'What SAP, USAP or waived-unacknowledged access did this entity hold?' },
  { key: 'D', label: 'Disclosure role',
    question: 'How central is this entity to forcing the record into the open?' },
];
```

Scored 0–3, never summed — same discipline as the parent board. An entity can be
C3/D0 (a contractor deep in custody, invisible in the disclosure fight) or C0/D3
(a legislator with no program access driving the whole effort). Collapsing that
destroys the information.

### Redefined entity tiers

```js
const TIERS = {
  A: { label: 'Tier A', color: '#5ed4e6',
       note: 'Named in sworn testimony or primary documents as directly inside the program' },
  B: { label: 'Tier B', color: '#efb555',
       note: 'Documented channel and capability; program role indicated but not yet nailed to a primary source' },
  C: { label: 'Tier C', color: '#8d97a4',
       note: 'Contextual — real and relevant, no direct program linkage on the record yet' },
};
```

### New node classes
- `legislation` — bills, statutes, NDAA sections, amendments. Same `other()` shape.
- `document` — a specific released or leaked record (Twining memo, Wilson-Davis memo,
  the ICIG complaint, an AARO report). Same `other()` shape.
- `event` — hearings, incidents, retrievals, release tranches.

`NODES = [...PEOPLE, ...INSTITUTIONS, ...PROGRAMS, ...LOCATIONS, ...DOMAINS, ...LEGISLATION, ...DOCUMENTS, ...EVENTS]`

### New edge types (added to `EDGE_TYPES`)

```js
custody:     { color: '#e8705f', dash: [],        label: 'Custody chain' },
funding:     { color: '#66d69f', dash: [8, 3],    label: 'Funding channel' },
denial:      { color: '#8d97a4', dash: [2, 4],    label: 'Official denial' },
legislative: { color: '#a795e8', dash: [5, 2, 1, 2], label: 'Legislative' },
```

`witness-chain`, `programmatic`, `institutional` and `investigative` carry over and
do the heaviest lifting on this board.

### New clusters

```js
const CLUSTERS = {
  'legacy':      { label: 'Legacy era 1940-1969' },
  'contractor':  { label: 'Contractor custody' },
  'ffrdc':       { label: 'FFRDC / advisory layer' },
  'ic':          { label: 'Intelligence community' },
  'oversight':   { label: 'Congress & oversight' },
  'witness':     { label: 'Witness chain' },
  'research':    { label: 'Research & academic' },
  'media':       { label: 'Media & investigators' },
  'other':       { label: 'Unclustered' },
};
```

### New strands (timeline)

```js
const STRANDS = [
  { key: 'program',   label: 'THE PROGRAM',    sub: 'retrieval, custody, reverse engineering', color: '#e8705f' },
  { key: 'witness',   label: 'WITNESS CHAIN',  sub: 'who told whom, and under what oath',      color: '#f0d264' },
  { key: 'oversight', label: 'OVERSIGHT',      sub: 'hearings, legislation, records law',      color: '#66d69f' },
  { key: 'coverup',   label: 'THE COVER-UP',   sub: 'denials, destroyed records, disinformation', color: '#8d97a4' },
];
```

### `PRECEDENT` — carried over and extended
The parent board uses `PRECEDENT` for documented state-secrecy precedent
(MKULTRA, Frank Olson, Church Committee). That structure is even more load-bearing
here: it is the documented proof that programs of exactly this shape have existed,
been concealed, been lied about to Congress, and had their records destroyed on
order. Extend it — Manhattan Project compartmentation, NRO's existence classified
until 1992, the Church and Pike Committees, the 1973 MKULTRA record destruction,
Iran-Contra, the Tuskegee study, the Atomic Energy Commission human radiation
experiments, and the 1997 CIA admission on U-2 and UFO report falsification.

---

## PART 3 — File layout

```
data/program-people.js         PEOPLE[]
data/program-entities.js       INSTITUTIONS[] PROGRAMS[] LOCATIONS[] DOMAINS[] LEGISLATION[] DOCUMENTS[] EVENTS[]
data/program-edges.js          PROGRAM_EDGES[]
data/program-entity-info.js    ENTITY_INFO{} ENTITY_SOURCES{}
data/program-timeline.js       TIMELINE[] STRANDS[] PRECEDENT[]
data/program-meta.js           EDGE_TYPES CLUSTERS TIERS AXES STATUS_LABEL
data/the-program.json          everything, combined, for non-JS consumers
```

## PART 4 — Integrity rules

1. Every `PROGRAM_EDGES` endpoint resolves to a node id that exists.
2. Every non-person node has a `desc` — or `desc: null`, which the dock prints as a
   stated gap. Never an empty string pretending to be content.
3. Every person has `tier`, `tierRationale`, and all three axis scores.
4. Every `claims[]` entry has a `tier` and a `source` string. "No attributed source
   on file" is an acceptable value; a fabricated one is not.
5. Every `sources[]` entry is `{name, url, date}`. For undated institutional pages,
   `date` is the date the URL was verified — same convention as the parent board.
6. Officially denied entities still get nodes, with the denial recorded as a
   `denial` edge and cited.
7. No duplicate ids across any node class.
