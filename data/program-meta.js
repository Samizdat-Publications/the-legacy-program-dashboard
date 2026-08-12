/* THE PROGRAM — vocabulary, scoring and rendering constants
   Companion board to The Vanishing. Drop-in replacements for that board's
   EDGE_TYPES / CLUSTERS / TIERS / AXES / STRANDS / STATUS_LABEL / PRECEDENT.

   Editorial premise, stated once here so it does not have to be restated in
   every dossier: a legacy recovery and reverse-engineering program exists,
   has existed since the 1940s, and has been deliberately concealed from
   Congress and the public. The research question is who, where, under what
   authority, and paid for how. Official denials are catalogued as artifacts
   of the concealment effort, not as counterweights to it.
*/

/* Edge types. The first eight carry over from The Vanishing unchanged so the
   renderer needs no new cases; the last four are this board's additions.
   Geographic, research and temporal edges are DERIVED BY RULE from shared
   cluster / domains / dates. Everything else is hand-written and sourced.
   That distinction is load-bearing and is preserved from the parent board. */
export const EDGE_TYPES = {
  institutional:   { color: '#a795e8', dash: [],              label: 'Institutional' },
  geographic:      { color: '#7fb4e8', dash: [6, 4],          label: 'Geographic' },
  research:        { color: '#e08ad0', dash: [2, 3],          label: 'Research domain' },
  temporal:        { color: '#efb555', dash: [1, 4],          label: 'Temporal' },
  behavioral:      { color: '#e8705f', dash: [9, 3, 2, 3],    label: 'Behavioral' },
  programmatic:    { color: '#66d69f', dash: [10, 5],         label: 'Programmatic' },
  investigative:   { color: '#5ed4e6', dash: [4, 3, 1, 3],    label: 'Investigative' },
  'witness-chain': { color: '#f0d264', dash: [],              label: 'Witness chain' },

  custody:         { color: '#e8705f', dash: [],              label: 'Custody chain' },
  funding:         { color: '#66d69f', dash: [8, 3],          label: 'Funding channel' },
  denial:          { color: '#8d97a4', dash: [2, 4],          label: 'Official denial' },
  legislative:     { color: '#a795e8', dash: [5, 2, 1, 2],    label: 'Legislative' },
};

/* Scored axes. Deliberately NOT summed. An entity can be extraordinary on one
   axis and unremarkable on another, and collapsing that destroys the
   information — a contractor can sit at the centre of the custody chain and be
   entirely absent from the disclosure fight, and a legislator can drive the
   whole disclosure effort while holding no program access at all. */
export const AXES = [
  { key: 'C', label: 'Custody proximity',
    question: 'How close is this entity to alleged possession of recovered material or craft?' },
  { key: 'A', label: 'Access level',
    question: 'What special access — SAP, USAP, or waived unacknowledged — did this entity hold?' },
  { key: 'D', label: 'Disclosure role',
    question: 'How central is this entity to forcing the record into the open?' },
];

/* Entity tiers. Same three-band structure and colours as the parent board,
   different question. There the question was how well a death resists a
   prosaic explanation. Here it is how firmly an entity is nailed to the program. */
export const TIERS = {
  A: { label: 'Tier A', color: '#5ed4e6',
       note: 'Named in sworn testimony or primary documents as directly inside the program' },
  B: { label: 'Tier B', color: '#efb555',
       note: 'Documented channel and capability; program role indicated but not yet nailed to a primary source' },
  C: { label: 'Tier C', color: '#8d97a4',
       note: 'Contextual — real and relevant, no direct program linkage on the record yet' },
};

/* Claim tiers. Carried over from the parent board's tabSources() unchanged.
   This is ammunition grading, not hedging: Tier 1 is what survives a hostile
   audit, Tier 3 is where the research goes next. Keeping them separate is what
   makes the board usable against a skeptic rather than dismissible by one. */
export const CLAIM_TIERS = {
  1: { label: 'Tier 1 · documented',   cls: 'b-conf',
       note: 'A primary record exists: FOIA release, contract or award data, court filing, statute, official report, org chart, agency letter, patent, or hearing transcript.' },
  2: { label: 'Tier 2 · sourced claim', cls: 'b-claim',
       note: 'Attributed to a named person on the record — including sworn testimony and signed IG complaints — or to credible named-source journalism.' },
  3: { label: 'Tier 3 · inference',     cls: 'b-open',
       note: 'A reasoned connection not yet nailed to a primary source. The reasoning is stated so it can be attacked or confirmed.' },
};

export const CLUSTERS = {
  legacy:     { label: 'Legacy era 1940-1969' },
  contractor: { label: 'Contractor custody' },
  ffrdc:      { label: 'FFRDC & advisory layer' },
  ic:         { label: 'Intelligence community' },
  oversight:  { label: 'Congress & oversight' },
  witness:    { label: 'Witness chain' },
  research:   { label: 'Research & academic' },
  media:      { label: 'Media & investigators' },
  other:      { label: 'Unclustered' },
};

export const STRANDS = [
  { key: 'program',   label: 'THE PROGRAM',   sub: 'retrieval, custody, reverse engineering',    color: '#e8705f' },
  { key: 'witness',   label: 'WITNESS CHAIN', sub: 'who told whom, and under what oath',         color: '#f0d264' },
  { key: 'oversight', label: 'OVERSIGHT',     sub: 'hearings, legislation, records law',         color: '#66d69f' },
  { key: 'coverup',   label: 'THE COVER-UP',  sub: 'denials, destroyed records, disinformation', color: '#8d97a4' },
];

export const STATUS_LABEL = {
  active: 'ACTIVE', former: 'FORMER', dead: 'DEAD', missing: 'MISSING',
  resolved: 'RESOLVED', disbanded: 'DISBANDED', classified: 'CLASSIFIED',
  denied: 'DENIED', disputed: 'DISPUTED',
};

export const PRECISION_LABEL = {
  day: 'day-precise', month: 'month-precise', year: 'year-precise', ranged: 'ranged',
};

/* Documented precedent. The parent board uses this structure to show that
   programs of a given shape have existed before. On this board it does more
   work: it is the record that the United States government has repeatedly run
   concealed programs, lied to Congress about them, destroyed their records on
   order, and only admitted them decades later under subpoena. Every entry here
   is Tier 1 — none of it is contested, all of it is government-admitted.

   Populated by the research waves; seeded here with the anchors. */
export const PRECEDENT = [
  { date: '1942', precision: 'ranged', label: 'Manhattan Project compartmentation',
    text: 'A programme of roughly 125,000 workers run so that almost none of them knew what they were building. The working demonstration that scale and secrecy are not in tension.' },
  { date: '1953', precision: 'ranged', label: 'MKULTRA authorised',
    text: 'CIA mind-control programme runs to 1973. Most records destroyed in 1973 on the director’s order, which is why the Church Committee could only partially reconstruct it.' },
  { date: '1953', precision: 'year', label: 'Frank Olson',
    text: 'Army biochemist dies in a fall from a New York hotel window days after being dosed with LSD without his knowledge. Ruled suicide; the government later settled with the family.' },
  { date: '1961', precision: 'year', label: 'NRO founded in secret',
    text: 'The National Reconnaissance Office is established in 1961. Its very existence stays classified until 1992 — thirty-one years of an entire agency the public was not told about.' },
  { date: '1975', precision: 'year', label: 'Church Committee',
    text: 'Senate select committee documents assassination plots, domestic surveillance and programmes concealed from Congress for decades.' },
  { date: '1994', precision: 'year', label: 'Human radiation experiments',
    text: 'The Advisory Committee on Human Radiation Experiments confirms decades of federally sponsored experiments on citizens without consent, concealed until the record was forced open.' },
  { date: '1997', precision: 'year', label: 'CIA admits falsifying UFO explanations',
    text: 'A CIA Studies in Intelligence article states the Air Force issued false cover stories attributing sightings to natural phenomena while knowing they were U-2 flights. A government admission, in a government journal, of deliberate public deception on this exact subject.' },
];

export const DISCLAIMER =
  'Every connection on this board carries a claim tier. Tier 1 is documented in a primary ' +
  'record. Tier 2 is attributed to a named person on the record, including under oath. ' +
  'Tier 3 is a stated inference. Official denials are recorded in full and sourced — as ' +
  'evidence about the denier, and about the shape of the concealment, rather than as ' +
  'refutations. Nothing on this board is sourced to a citation that was not found and checked.';
