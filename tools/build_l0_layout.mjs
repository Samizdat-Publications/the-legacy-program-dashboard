/**
 * build_l0_layout.mjs — bake the L0 *positional* layout model.
 *
 *   node tools/build_l0_layout.mjs        # -> data/l0-layout-model.json
 *
 * WHAT THIS IS
 * ------------
 * The answer to notes/DESIGN-BRIEF-LAYOUT-2026-08-14.md §3A and §3B: a layout in
 * which position carries era and function, and an edge budget for the rest state.
 * It emits the model the comp draws AND the figures the comp prints, so a figure
 * cannot drift from the file it describes — there is one number, in one place.
 *
 * TWO DATASETS, ON PURPOSE
 * ------------------------
 *   current  data/design-extract.json   968-node board, 110 L0, 24 Aug 2026
 *   legacy   data/l0-extract.json       970-node board, 96 L0, commit 9ccc25d
 *
 * `current` is authoritative for every figure. `legacy` is kept and switchable
 * because it carries four fields `current` does not, and the design depends on
 * all four. Keeping both is the only way to show what each missing field costs
 * instead of arguing about it:
 *
 *   via[]       which members two nodes share, so a summarised line can name
 *               "Puthoff · Bigelow" instead of printing "2"
 *   members[]   the off-map neighbours of each node — the individuals and
 *               documents the rollup withholds. `current` gives a count and a
 *               class mix, which is enough to state the arithmetic and not enough
 *               to answer "which people?"
 *   C / A / D   the three scored axes. Band display order is the measured mean C
 *               of each band, which is what makes the vertical axis mean distance
 *               from the material rather than a sort somebody chose.
 *   denial a/b  which end of a denial edge issued it. Motion on this map carries
 *               attested direction and nothing else, so without this the particle
 *               layer has nothing it is allowed to say at rest.
 *
 * The two are never mixed. A figure comes from one dataset or the other and the
 * model says which.
 *
 * THE READ CAP — the correction to §0 of the comp
 * ----------------------------------------------
 * The brief cited data/l0-model.json and data/the-program.json and this generator
 * originally reported them absent. They are not absent: both are tracked and
 * pushed, at 5.7MB and 6.9MB, and the GitHub read API caps around 1MB, so they
 * read as missing over the API. The brief's figures were correct and reproducible
 * all along. data/design-extract.json exists to be readable, and every figure in
 * the brief does reproduce from it.
 *
 * One trap survives: data/l0-extract.json carries a `deg` field that is an
 * edge-instance count, not a degree. It moves the L0 set from 96 to 107. Degree
 * here is always distinct neighbours, recomputed, for both datasets.
 *
 * DETERMINISM
 * -----------
 * No physics and no random(). Position is a pure function of (era, band, degree,
 * id). The same inputs give byte-identical output, which is what makes a
 * screenshot citable and `verify.py --idempotent` meaningful.
 */

/* ============================ pure core ============================ */
/* No imports and no I/O above the node main block, so this section can be
   evaluated as-is by a browser or a test harness. */

const FLOOR = 6;
const L0_CLASSES = new Set(['institution', 'program', 'event', 'legislation', 'document']);
const HIGHLIGHT_CAP = 0.15;

/* Era boundaries carried over from the brief §2 unchanged, with one correction:
   the first band is open-ended downwards. Nodes exist with a dateStart before
   1940 and a band labelled "1940-1969" silently drops them off the axis. */
const ERAS = [
  { id: 0, from: null, to: 1969, label: 'THROUGH 1969', note: 'Estimate through Blue Book' },
  { id: 1, from: 1970, to: 1999, label: '1970-1999', note: 'Post-Blue Book' },
  { id: 2, from: 2000, to: 2016, label: '2000-2016', note: 'AAWSAP / AATIP' },
  { id: 3, from: 2017, to: 2100, label: '2017-2026', note: 'Post-disclosure' },
];

const BAND_VOCAB = ['retrieval', 'reverse-engineering', 'funding', 'research',
  'custody', 'disclosure', 'oversight', 'concealment'];

/* RARITY PIN — the answer to "pin the rank or let it re-derive?"

   Neither, quite. The order is PINNED here and RECOMPUTED every run, and a
   disagreement is reported rather than obeyed. Pure re-derivation is unsafe now
   that position carries information: oversight (68) and disclosure (74) are 8%
   apart, so six tags landing in a research pass can invert them and silently move
   every node carrying both into a different row. A reader who saw the map last
   month would find fourteen nodes relocated with no editorial change behind it,
   and no way to see that it happened. Pure pinning is also unsafe — it goes stale
   and stops describing the board.

   So: the pin is the rule, drift is a finding, and moving a node between bands
   becomes a decision someone makes with a diff in front of them. This is the same
   discipline that caught 107-vs-96: state the invariant, make the violation loud.

   Pinned 24 August 2026 against data/design-extract.json, counts at pin time:
     concealment 79 · disclosure 74 · oversight 68 · custody 48 · research 46
     funding 27 · reverse-engineering 17 · retrieval 10
   Three adjacent pairs were within 10% at pin time (research/custody,
   oversight/disclosure, disclosure/concealment) and are the ones to watch.
   Re-pin deliberately; do not edit this to silence a warning.

   RE-PINNED 19 September 2026, and this is the decision the mechanism asked for.
   research and custody swapped, exactly the pair flagged above. Counts now:
     concealment 100 · disclosure 94 · oversight 75 · research 66 · custody 64
     funding 34 · reverse-engineering 19 · retrieval 11
   The cause is editorial and not jitter: four research passes landed on 18-19
   September (ARV/TR-3B, the congressional witnesses, Lazar/S-4, the Disclosure
   Project) plus the propulsion strand, which brought NASA and DIA reference
   documents and two patents onto the board. The board genuinely holds more
   research-tagged material than custody-tagged material now, and it did not
   before. That is a real change in what the board is, so the map should show it.
   The diff was reviewed before re-pinning: 28 nodes carry BOTH custody and
   research and are the ones that can move band on this swap.

   CAUTION FOR THE NEXT SESSION. research 66 against custody 64 is a 3% gap, well
   inside the zone this pin exists to stabilise. A single further pass could swap
   them back. If that happens, do NOT re-pin again on another 2-count margin:
   two tags this close carry no real ordering, and the honest answer at that point
   is to ask Design whether they should share a band rather than to keep flipping
   28 nodes between rows. */
const RARITY_PIN = ['retrieval', 'reverse-engineering', 'funding', 'custody',
  'research', 'oversight', 'disclosure', 'concealment'];
const RARITY_PIN_DATE = '2026-09-19';

const GEO = {
  /* headRow was 46 and that was too short by exactly the height of the map's own
     DOM control row. .l0crumb and .l0ctl are absolutely positioned at top:10px
     INSIDE .l0wrap, over the canvas, and occupy y 10..33; the frozen head strip
     drew its era label at baseline 20 and its note at 33. So the first column
     head and the last one -- the two the controls sit above -- were painted
     underneath PROGRAM MAP / START and LINES AT REST at every viewport size, and
     rendered as an unreadable smear. Nothing in the source said so; the pixels
     did, on the first day anybody looked. See notes/LOOKING-2026-08-26.md.
     76 clears the control row with the label and note below it. It costs 30px of
     reserved top strip and changes no opening fit: at every size the sweep in
     tools/look.js covers, the fit is bound by WIDTH, not height. */
  gutter: 148, headRow: 76, colGap: 10, bandGap: 8,
  /* One chip size for the whole map. Not a layout convenience: §4 says size must
     not encode importance, and letting a sparse cell stretch its chips would make
     width a channel by accident. Columns per cell fall out of the fixed width. */
  chipW: 205, chipH: 20, chipGapY: 5, chipGapX: 7, cellPadY: 12, cellPadX: 10,
  /* Same world width as the existing bake in tools/build_l0.py (WORLD_W 2200),
     so this is the same canvas reorganised, not a bigger one asked for. */
  mapW: 2200,
};

/* Authored chip labels win over the derived ones. data/l0-shorts.json carries 46,
   one for every node whose derived short overflowed the 205px chip -- see that
   file for the rules. The derivation stays as the fallback for the other 64 and
   for any node added later, so an unauthored node still gets a usable label
   rather than nothing. */
let AUTHORED_SHORTS = {};
export function setAuthoredShorts(m){ AUTHORED_SHORTS = (m && m.shorts) || m || {}; }
function shortLabel(s) {
  return s.replace(/\s*\([^)]*\)\s*$/, '').replace(/\s*[-\u2014\u2013:]\s.*$/, '').trim();
}
function shortOf(n) {
  const a = AUTHORED_SHORTS[n.id];
  /* a spaced em dash in a display label becomes " - " (phase 3 decision 7) */
  return (typeof a === 'string' && a.trim()) ? a.trim().replace(/\s+\u2014\s+/g, ' - ') : shortLabel(n.label);
}
const yearOf = s => (s ? parseInt(String(s).slice(0, 4), 10) : null);
const eraIndex = y => y == null ? null
  : ERAS.findIndex(e => (e.from === null || y >= e.from) && y <= e.to);

/** dateStart / dateEnd for every node document in research/*.json. First value
 *  wins in file order. Conflicts are reported, never silently resolved. */
export function buildDates(docs) {
  const out = {}, conflicts = {};
  const walk = (o) => {
    if (Array.isArray(o)) { o.forEach(walk); return; }
    if (!o || typeof o !== 'object') return;
    if (typeof o.id === 'string' && (o.dateStart || o.dateEnd)) {
      const cur = out[o.id];
      if (!cur) out[o.id] = { s: o.dateStart || null, e: o.dateEnd || null };
      else {
        if (!cur.s && o.dateStart) cur.s = o.dateStart;
        if (!cur.e && o.dateEnd) cur.e = o.dateEnd;
        if (cur.s && o.dateStart && cur.s !== o.dateStart) {
          (conflicts[o.id] ||= [cur.s]).push(o.dateStart);
        }
      }
    }
    for (const k of Object.keys(o)) if (o[k] && typeof o[k] === 'object') walk(o[k]);
  };
  docs.forEach(walk);
  return { dates: out, conflicts };
}

/* ------------------------------------------------------ normalisation
   Both inputs are reduced to the same shape before any layout runs, so the
   layout code cannot know or care which board it is drawing. `fields` records
   what the source could not supply; the comp reads it to say so out loud. */

export function normaliseCurrent(dx) {
  const nodes = dx.l0.map(n => {
    const ys = yearOf(n.dateStart), ye = yearOf(n.dateEnd);
    return ({
    id: n.id, label: n.label, short: shortOf(n), cls: n.cls,
    cluster: n.cluster, tier: n.tier, deg: n.deg, claims: n.claims, t1: n.t1,
    roles: n.roles || [],
    y0: ys,
    /* span was the literal 0. Not "no node has an extent" -- the LITERAL ZERO,
       while normaliseLegacy two hundred lines down computed the same field
       properly from the same pair of years. dateEnd reaches this projection fine
       (46 of 110 arrive, as y1); it was the subtraction that never happened.

       So the backfill queue's row 6 -- "dateEnd ... unlocks: how many nodes could
       carry an extent at all" -- had an answer the whole time and the pipeline
       was reporting 0 to it. It is 24: yankee-blue runs 1980-2023, AAWSAP
       2007-2012, KONA BLUE 2011-2012. A hardcoded zero is indistinguishable from
       a measured one, which is this repo's own rule about checks applied to
       data. */
    era: eraIndex(ys),
    di: n.di || 0, dr: n.dr || 0,
    /* Backfilled into design-extract.json on 24 Aug. Design's baseline nulled
       these because the extract did not carry them at pin time; it does now, so
       nulling them here made the generator announce "C/A/D absent from this
       source" while fields.cad reported true -- the two disagreeing is exactly
       the class of silent degradation this package is built to prevent. */
    C: n.C != null ? n.C : null, A: n.A != null ? n.A : null,
    D: n.D != null ? n.D : null,
    y1: ye,
    span: (ys != null && ye != null && ye > ys) ? ye - ys : 0,
    memberCount: n.members || 0, mix: n.mix || {},
    /* The P1 split. build_l0.py computes members.direct and members.routed
       separately and design-extract.json carries both counts; this projection
       flattened them into memberCount and dropped the split, so "5 on the map,
       14 held back" could not be made to sum to the degree. */
    membersDirect: n.membersDirect != null ? n.membersDirect : null,
    membersRouted: n.membersRouted != null ? n.membersRouted : null,
    members: Array.isArray(n.direct) ? n.direct : null,
    why: n.whyImplicated || '',
  });});
  /* denialPairs carries the raw, UNSORTED ends of every denial link on the map,
     plus `denier` where the record names who issued it. The generator used to
     record only that the array was non-empty (see figures.denialDir) and never
     joined it, so `dn` came out empty on every edge and the renderer fell back to
     the aggregated a/b -- which is [a,b].sort(), i.e. alphabetical. That is how
     22 of 47 denial arrowheads came to point the wrong way.
     Join it here, and carry `denier` only when every underlying denial for the
     pair agrees on one. Disagreement means unattested, not majority rule. */
  const dnByPair = new Map();
  for (const d of (dx.denialPairs || [])) {
    const k = [d.a, d.b].sort().join('|');
    if (!dnByPair.has(k)) dnByPair.set(k, []);
    dnByPair.get(k).push(d);
  }
  const direct = dx.directEdges.map(e => {
    const ds = dnByPair.get([e.a, e.b].sort().join('|')) || [];
    /* Association links carry no denier by definition, so they are excluded from
       the direction vote -- counting them would veto a direction every actual
       denial act in the bundle agrees on. */
    const acts = ds.filter(d => d.denialKind !== 'association');
    const named = [...new Set(acts.map(d => d.denier).filter(Boolean))];
    const directed = acts.length > 0 && named.length === 1 && acts.every(d => d.denier);
    return {
      a: e.a, b: e.b, n: e.n, kind: 'direct', tier: e.tier,
      types: e.types || [], denial: (e.types || []).indexOf('denial') >= 0,
      dn: ds.map(d => [d.a, d.b]),
      denier: directed ? named[0] : null,
      /* ALL THREE STATES, not just one of them. This returned 'association' or
         null, so an edge with a known issuer came through with denialKind null
         and `denier` set beside it -- the pair contradicting itself, and the
         renderer reading the null as "no adjudication yet".
           association  only when EVERY underlying record is one. A pair carrying
                        one real denial and one association is still a denial.
           directed     when the denial acts all name the SAME issuer. Two ends
                        denying each other is not a direction.
           undirected   otherwise. Claims the least, which is the right default. */
      denialKind: !ds.length ? null
        : ds.every(d => d.denialKind === 'association') ? 'association'
        : directed ? 'directed' : 'undirected',
    };
  });
  const summarised = dx.summarised.map(e => ({
    a: e.a, b: e.b, n: e.n, kind: 'shared', tier: e.tier,
    via: e.via && e.via.length ? e.via : null,   /* backfilled 24 Aug */
  }));
  return {
    key: 'current',
    label: 'design-extract.json · 24 Aug 2026',
    source: 'data/design-extract.json',
    boardNodes: (dx.counts || {}).total, boardEdges: null,
    nodes, direct, summarised, viaMembers: {},
    dates: {}, conflicts: {},
    /* Detected, not asserted. Five of these were backfilled into
       design-extract.json on 24 Aug; a hardcoded false makes the generator
       announce it lacks fields the file now carries, and silently take the
       degraded path. Re-applied after the package shipped without it. */
    fields: {
      via: (dx.summarised || []).some(e => e.via && e.via.length),
      members: (dx.l0 || []).some(n => Array.isArray(n.direct)),
      cad: (dx.l0 || []).every(n => n.C != null && n.A != null && n.D != null),
      denialDir: Array.isArray(dx.denialPairs) && dx.denialPairs.length > 0,
      dateEnd: (dx.l0 || []).some(n => n.dateEnd),
    },
    /* What `members` counts here, and it is NOT the node's off-map neighbours.
       design-extract.json carries the P1 roll-up from tools/build_l0.py: direct
       members plus members routed through up to routeCap 3 intermediates. So it
       is not the remainder of deg and must never be printed as one. */
    memberBasis: 'rollup',
    note: 'Authoritative. Every figure in the brief reproduces from this file.',
  };
}

export function normaliseLegacy(extract, dossierEntries, dateDocs) {
  const { dates, conflicts } = buildDates(dateDocs);
  const byId = new Map(extract.nodes.map(n => [n.id, n]));
  const adj = new Map(extract.nodes.map(n => [n.id, new Set()]));
  const pair = new Map();
  let dangling = 0;
  for (const e of extract.edges) {
    if (!adj.has(e.a) || !adj.has(e.b)) { dangling++; continue; }
    adj.get(e.a).add(e.b); adj.get(e.b).add(e.a);
    const k = [e.a, e.b].sort().join('|');
    (pair.get(k) || pair.set(k, []).get(k)).push(e);
  }
  const deg = id => adj.get(id).size;
  const l0 = extract.nodes.filter(n => L0_CLASSES.has(n.cls) && deg(n.id) >= FLOOR);
  const L0 = new Set(l0.map(n => n.id));

  const roles = new Map();
  for (const e of dossierEntries) {
    const r = (e.entityDossier || {}).roles;
    if (!r) continue;
    const prev = roles.get(e.id);
    if (!prev || r.length > prev.length) roles.set(e.id, r);
  }
  const issued = {}, received = {};
  for (const e of extract.edges) {
    if (e.t !== 'denial') continue;
    issued[e.a] = (issued[e.a] || 0) + 1;
    received[e.b] = (received[e.b] || 0) + 1;
  }

  const nodes = l0.map(n => {
    const d = dates[n.id] || {};
    const ys = yearOf(d.s), ye = yearOf(d.e);
    const rows = [];
    const mix = {};
    for (const other of adj.get(n.id)) {
      if (L0.has(other)) continue;
      const o = byId.get(other); if (!o) continue;
      mix[o.cls] = (mix[o.cls] || 0) + 1;
      for (const e of (pair.get([n.id, other].sort().join('|')) || [])) {
        rows.push([other, shortLabel(o.label), o.cls, e.t, e.ct, e.a === n.id ? 1 : 0]);
      }
    }
    rows.sort((x, y) => x[4] - y[4] || (x[3] < y[3] ? -1 : x[3] > y[3] ? 1 : 0) || (x[1] < y[1] ? -1 : 1));
    return {
      id: n.id, label: n.label, short: shortOf(n), cls: n.cls,
      cluster: n.cluster, tier: n.tier, deg: deg(n.id), claims: n.claims, t1: n.t1,
      roles: roles.get(n.id) || [], y0: ys, y1: ye,
      span: (ys != null && ye != null && ye > ys) ? ye - ys : 0,
      era: eraIndex(ys), di: issued[n.id] || 0, dr: received[n.id] || 0,
      C: n.C, A: n.A, D: n.D,
      memberCount: new Set(rows.map(r => r[0])).size, mix, members: rows, why: '',
    };
  });

  const direct = [];
  for (const [k, es] of pair) {
    const [a, b] = k.split('|');
    if (!L0.has(a) || !L0.has(b)) continue;
    direct.push({
      a, b, n: es.length, kind: 'direct',
      tier: Math.min(...es.map(e => e.ct)),
      types: [...new Set(es.map(e => e.t))],
      denial: es.some(e => e.t === 'denial'),
      /* Direction is preserved for denials only. D3 draws them directional, and
         the pair key is sorted, so the issuer would otherwise be lost: `a`
         issued it, `b` is the subject. */
      dn: es.filter(e => e.t === 'denial').map(e => [e.a, e.b]),
      /* Same rule as the current path: a/b is not a denier, so direction is
         attested only where the record names one. */
      denier: (() => {
        /* Association links carry no denier by definition, so counting them in
           `every(e => e.denier)` would veto a direction that every actual denial
           act in the bundle agrees on. */
        const acts = es.filter(e => e.t === 'denial' && e.denialKind !== 'association');
        const named = [...new Set(acts.map(e => e.denier).filter(Boolean))];
        return (acts.length && named.length === 1 && acts.every(e => e.denier)) ? named[0] : null;
      })(),
      /* All three states, not just the one. This used to return 'association' or
         null, so a map edge with a known issuer came through with denialKind
         null while `denier` was set beside it -- the pair contradicting itself.
         An aggregated edge stands for several underlying links, so:
           association  only if EVERY link is an association. One real denial in
                        the bundle means the pair carries a denial.
           directed     if the links that are denial acts all name the SAME
                        issuer. Two ends denying each other is not a direction.
           undirected   otherwise: an act, no single attributable issuer. It
                        claims the least, which is the right default. */
      denialKind: (() => {
        const dn = es.filter(e => e.t === 'denial');
        if (!dn.length) return null;
        if (dn.every(e => e.denialKind === 'association')) return 'association';
        const acts = dn.filter(e => e.denialKind !== 'association');
        const named = [...new Set(acts.map(e => e.denier).filter(Boolean))];
        return (acts.length && named.length === 1 && acts.every(e => e.denier))
          ? 'directed' : 'undirected';
      })(),
    });
  }

  const depth = new Map(); const q = [...L0];
  q.forEach(i => depth.set(i, 0));
  for (let i = 0; i < q.length; i++)
    for (const v of adj.get(q[i])) if (!depth.has(v)) { depth.set(v, depth.get(q[i]) + 1); q.push(v); }
  const directKeys = new Set(direct.map(e => [e.a, e.b].sort().join('|')));
  const shared = new Map();
  for (const n of extract.nodes) {
    if (L0.has(n.id) || depth.get(n.id) !== 1) continue;
    const ps = [...adj.get(n.id)].filter(v => L0.has(v));
    for (let i = 0; i < ps.length; i++) for (let j = i + 1; j < ps.length; j++) {
      const k = [ps[i], ps[j]].sort().join('|');
      if (directKeys.has(k)) continue;
      (shared.get(k) || shared.set(k, []).get(k)).push(n.id);
    }
  }
  const summarised = [];
  for (const [k, vias] of shared) {
    if (vias.length < 2) continue;
    const [a, b] = k.split('|');
    let tier = 9;
    for (const m of vias) for (const p of [a, b])
      for (const e of (pair.get([p, m].sort().join('|')) || [])) tier = Math.min(tier, e.ct);
    summarised.push({ a, b, n: vias.length, kind: 'shared', tier, via: vias });
  }

  /* Who the shared members ARE. A summarised line reading "5" is a count with no
     content: the reader cannot tell whether NIDS and AATIP are joined by five
     documents or by Robert Bigelow. `disp` is a display truncation of the board's
     own label and never a rewrite: surname for a person, short_label otherwise. */
  const viaMembers = {};
  for (const id of new Set(summarised.flatMap(e => e.via))) {
    const n = byId.get(id); if (!n) continue;
    const short = shortLabel(n.label);
    viaMembers[id] = [
      n.cls === 'person'
        ? (short.split(/\s+/).filter(w => !/^[A-Z]\.$/.test(w)).slice(-1)[0] || short)
        : short,
      n.cls, n.label,
    ];
  }

  return {
    key: 'legacy',
    label: 'l0-extract.json · commit 9ccc25d',
    source: 'data/l0-extract.json',
    boardNodes: extract.nodes.length, boardEdges: extract.edges.length,
    nodes, direct, summarised, viaMembers, dates, conflicts, dangling,
    staleDegL0: extract.nodes.filter(n => L0_CLASSES.has(n.cls) && n.deg >= FLOOR).length,
    multiEdgePairs: [...pair.values()].filter(v => v.length > 1).length,
    pairs: pair.size,
    fields: { via: true, members: true, cad: true, denialDir: true, dateEnd: true },
    /* Off-map neighbours, derived here from the adjacency, so on-map direct edges
       plus members is exactly deg. */
    memberBasis: 'neighbours',
    note: 'Superseded. Kept because it carries four fields design-extract.json does not.',
  };
}

/* ------------------------------------------------------ highlights */
function buildHighlights(supplied, nodes, edges, L0) {
  if (supplied && Array.isArray(supplied.flags) && supplied.flags.length) {
    return {
      source: 'data/l0-highlights.json', placeholder: false,
      rule: supplied.rule || 'no rule stated in the highlights file',
      unknownIds: supplied.flags.filter(f => f && !L0.has(f.id)).map(f => f.id),
      flags: supplied.flags.filter(f => f && L0.has(f.id))
        .map((f, i) => ({ id: f.id, rank: i + 1, why: f.why || '' })),
    };
  }
  const reach = new Map([...L0].map(i => [i, { n: 0, bands: new Set() }]));
  const bandOf = new Map(nodes.map(n => [n.id, n.band]));
  for (const e of edges) {
    if (e.role !== 'structural') continue;
    for (const [p, q] of [[e.a, e.b], [e.b, e.a]]) {
      const r = reach.get(p); if (!r) continue;
      r.n++; r.bands.add(bandOf.get(q));
    }
  }
  const byId = new Map(nodes.map(n => [n.id, n]));
  return {
    source: 'derived', placeholder: true, unknownIds: [],
    rule: 'PLACEHOLDER, derived from the shipped model and not an editorial pass: ' +
      'the nine nodes carrying the most edges that cross two or more bands and at ' +
      'least one era. Replace with data/l0-highlights.json.',
    flags: [...reach.entries()]
      .map(([id, r]) => ({ id, n: r.n, b: r.bands.size }))
      .sort((x, y) => y.n - x.n || y.b - x.b || (x.id < y.id ? -1 : 1))
      .slice(0, 9)
      .map((r, i) => {
        const n = byId.get(r.id);
        return {
          id: r.id, rank: i + 1,
          why: r.n + ' structural edges, reaching ' + r.b + ' bands · degree ' +
            n.deg + ' · ' + n.claims + ' claims, ' + n.t1 + ' tier 1',
        };
      }),
  };
}

/* ------------------------------------------------------ the layout */
export function layout(src, supplied, images) {
  const N = src.nodes.map(n => ({ ...n }));
  const byId = new Map(N.map(n => [n.id, n]));
  const L0 = new Set(N.map(n => n.id));

  /* PRIMARY FUNCTION: rarest tag wins ---------------------------------------
     Brief question 1. The tags are not a partition — they overlap heavily and
     most nodes carry `concealment`. A node's band is its RAREST claimed role,
     where rarity is counted on the map itself. Rarity is a proxy for
     specificity: the rarest tag is the most particular thing the board says
     this node did. One line, no manual pass, re-derives itself when the
     research moves. Where C is available the result is checked against it. */
  const tally = {};
  for (const n of N) for (const r of n.roles) tally[r] = (tally[r] || 0) + 1;
  const observed = Object.entries(tally)
    .sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1)).map(([r]) => r);
  const rarity = Object.fromEntries(RARITY_PIN.map((r, i) => [r, i]));
  // any tag the pin does not know about sorts last, loudly
  for (const r of observed) if (rarity[r] == null) rarity[r] = RARITY_PIN.length;
  const unpinnedTags = observed.filter(r => RARITY_PIN.indexOf(r) < 0);
  /* Where the pinned order and this board's own counts disagree. Reported, never
     obeyed — obeying it is the silent-relocation failure the pin exists to stop. */
  const pinDrift = observed
    .map((r, i) => [r, i, RARITY_PIN.indexOf(r), tally[r]])
    .filter(row => row[1] !== row[2])
    .map(row => ({ tag: row[0], observedRank: row[1] + 1, pinnedRank: row[2] + 1, count: row[3] }));
  for (const n of N) {
    n.band = n.roles.slice().sort((a, b) => rarity[a] - rarity[b] || (a < b ? -1 : 1))[0] || null;
  }
  const missingRoles = N.filter(n => !n.band).map(n => n.id);
  for (const n of N) if (!n.band) n.band = 'concealment';

  const present = BAND_VOCAB.filter(b => N.some(n => n.band === b));
  const meanC = b => {
    const ns = N.filter(n => n.band === b && n.C != null);
    return ns.length ? ns.reduce((s, n) => s + n.C, 0) / ns.length : null;
  };
  /* Band display order. Measured mean C descending where the axis exists, so the
     vertical dimension means distance from the alleged material rather than a
     sort somebody chose. Without C the fallback is rarity — specific at the top,
     universal at the bottom — which lands in nearly the same place but is a
     property of the tags rather than of the board's scoring. */
  const haveC = src.fields.cad && present.every(b => meanC(b) != null);
  const bands = haveC
    ? present.slice().sort((a, b) => meanC(b) - meanC(a))
    : present.slice().sort((a, b) => rarity[a] - rarity[b]);
  const bandOrderBasis = haveC ? 'measured mean C, descending' : 'role rarity — C/A/D absent from this source';

  /* ---- edges: enrich with band and era distance ---- */
  const all = [];
  for (const e of [...src.direct, ...src.summarised]) {
    const A = byId.get(e.a), B = byId.get(e.b);
    if (!A || !B) continue;
    all.push({
      ...e,
      db: Math.abs(bands.indexOf(A.band) - bands.indexOf(B.band)),
      de: (A.era == null || B.era == null) ? null : Math.abs(A.era - B.era),
    });
  }
  const direct = all.filter(e => e.kind === 'direct');
  const summarised = all.filter(e => e.kind === 'shared');

  /* THE EDGE BUDGET ----------------------------------------------------------
     Brief question B. Tier does not thin the map and degree should not. The
     budget comes out of the layout instead: position already states era and
     band, so a short edge largely restates where its endpoints sit while a long
     one asserts something position cannot.

       clause 1 STRUCTURAL — crosses >= 2 bands AND >= 1 era.
       clause 2 ANCHOR — every node keeps its single strongest edge regardless
                (lowest tier, then longest span, then id). Nothing sits on this
                map unexplained. Direct preferred; a node with no direct L0-L0
                edge takes its strongest summarised one.

     Everything else is LOCAL, drawn only on selection. Summarised edges are off
     at rest: they are the closest thing to what the bands already say. */
  const strength = e => ((4 - e.tier) * 100) + (e.db * 6) + ((e.de || 0) * 4) + (e.kind === 'direct' ? 2 : 0);
  const key = e => [e.a, e.b].sort().join('|');
  const structural = direct.filter(e => e.db >= 2 && (e.de || 0) >= 1);
  const restKeys = new Set(structural.map(key));
  const touched = new Set(); structural.forEach(e => { touched.add(e.a); touched.add(e.b); });
  const anchors = [];
  for (const n of N) {
    if (touched.has(n.id)) continue;
    const cands = all.filter(e => (e.a === n.id || e.b === n.id) && !restKeys.has(key(e)))
      .sort((x, y) => strength(y) - strength(x) || (key(x) < key(y) ? -1 : 1));
    if (!cands.length) continue;
    restKeys.add(key(cands[0])); anchors.push(cands[0]);
    touched.add(cands[0].a); touched.add(cands[0].b);
  }
  for (const e of all) {
    e.rest = restKeys.has(key(e));
    e.role = structural.indexOf(e) >= 0 ? 'structural' : (anchors.indexOf(e) >= 0 ? 'anchor' : 'local');
  }
  /* `isolated` = no L0-L0 relationship of any kind exists, so no budget could
     have drawn one; it gets an explicit no-link marker rather than looking like a
     rendering failure. `orphans` = the budget dropped every edge a node had,
     which is a bug in the budget and fails the build. */
  const hasCandidate = new Set(all.flatMap(e => [e.a, e.b]));
  const isolated = N.filter(n => !hasCandidate.has(n.id)).map(n => n.id);
  const orphans = N.filter(n => hasCandidate.has(n.id) && !touched.has(n.id)).map(n => n.id);
  for (const n of N) {
    n.restEdges = all.filter(e => e.rest && (e.a === n.id || e.b === n.id)).length;
    n.allEdges = all.filter(e => e.a === n.id || e.b === n.id).length;
    n.onMapEdges = all.filter(e => e.kind === 'direct' && (e.a === n.id || e.b === n.id)).length;
    n.isolated = isolated.indexOf(n.id) >= 0;
  }

  /* POSITION: cell packing, no physics --------------------------------------
     A node's cell is (band, era). Inside a cell it is packed highest degree
     first, so the most connected node reads top-left and packing is stable under
     a data change that does not move degrees. Undated nodes get their own
     labelled column: absent prints as absent. */
  const undated = N.filter(n => n.era == null);
  const cols = [
    ...ERAS.map(e => ({ ...e, kind: 'era' })),
    /* The note is reader-facing copy sitting beside 'Post-Blue Book' and
       'Post-disclosure'. It read 'dateStart absent', which is the name of a JSON
       field, not a thing to tell a reader. */
    ...(undated.length ? [{ id: 'nd', label: 'NO DATE', note: 'no start date recorded', kind: 'nodate' }] : []),
  ];
  const colOf = n => n.era == null ? 'nd' : n.era;
  const cellOf = (b, c) => N.filter(n => n.band === b && colOf(n) === c)
    .sort((x, y) => y.deg - x.deg || (x.id < y.id ? -1 : 1));
  const colsFor = w =>
    Math.max(1, Math.floor((w - GEO.cellPadX * 2 + GEO.chipGapX) / (GEO.chipW + GEO.chipGapX)));

  /* Equal-width era columns, and NO DATE at 60% of one. Brief question 5: the
     last decade holds nearly half the map. Equal columns are what make that
     visible — widening the crowded column to fit its contents is the finding,
     erased. */
  const nodateW = 0.6;
  const units = cols.reduce((s, c) => s + (c.kind === 'era' ? 1 : nodateW), 0);
  const avail = GEO.mapW - GEO.gutter - GEO.colGap * (cols.length - 1);
  let x = GEO.gutter;
  for (const c of cols) {
    c.w = Math.round(avail * ((c.kind === 'era' ? 1 : nodateW) / units));
    c.x = x; x += c.w + GEO.colGap;
  }

  let y = GEO.headRow;
  const bandRecs = [];
  for (const b of bands) {
    let rows = 1;
    for (const c of cols) {
      const m = cellOf(b, c.id).length;
      if (m) rows = Math.max(rows, Math.ceil(m / colsFor(c.w)));
    }
    const h = GEO.cellPadY * 2 + rows * GEO.chipH + (rows - 1) * GEO.chipGapY;
    const mc = meanC(b);
    bandRecs.push({
      id: b, y, h, rows, n: N.filter(n => n.band === b).length,
      meanC: mc == null ? null : +mc.toFixed(2), tagged: tally[b] || 0,
      residual: (tally[b] || 0) > N.length * 0.5,
    });
    y += h + GEO.bandGap;
  }
  const worldH = y - GEO.bandGap + 10;
  const bandRec = new Map(bandRecs.map(b => [b.id, b]));

  for (const b of bands) for (const c of cols) {
    const cell = cellOf(b, c.id);
    if (!cell.length) continue;
    const nc = colsFor(c.w), br = bandRec.get(b);
    cell.forEach((n, i) => {
      const r = Math.floor(i / nc), k = i % nc;
      n.x = Math.round(c.x + GEO.cellPadX + k * (GEO.chipW + GEO.chipGapX));
      n.y = Math.round(br.y + GEO.cellPadY + r * (GEO.chipH + GEO.chipGapY));
      n.w = GEO.chipW; n.h = GEO.chipH;
      n.col = c.id; n.cell = b + '/' + c.id; n.slot = i;
    });
  }

  const matrix = bands.map(b => ({
    band: b, cells: cols.map(c => cellOf(b, c.id).length),
    total: N.filter(n => n.band === b).length,
  }));

  const restEdges = all.filter(e => e.rest);
  const dated = N.filter(n => n.era != null);
  const figures = {
    dataset: src.key, datasetLabel: src.label, datasetSource: src.source,
    boardNodes: src.boardNodes, boardEdges: src.boardEdges,
    l0: N.length, l0StaleDeg: src.staleDegL0 ?? null,
    multiEdgePairs: src.multiEdgePairs ?? null, pairs: src.pairs ?? null,
    directEdges: direct.length, summarisedEdges: summarised.length,
    maxShared: summarised.reduce((m, e) => Math.max(m, e.n), 0),
    drawnBeforeBudget: all.length,
    restDrawn: restEdges.length,
    restStructural: structural.length, restAnchor: anchors.length,
    clause1Covers: new Set(structural.flatMap(e => [e.a, e.b])).size,
    bareAfterClause1: N.length - new Set(structural.flatMap(e => [e.a, e.b])).size,
    restShared: restEdges.filter(e => e.kind === 'shared').length,
    restPct: Math.round(restEdges.length / all.length * 100),
    localHidden: all.length - restEdges.length,
    orphans: orphans.length, orphanIds: orphans,
    isolated: isolated.length, isolatedIds: isolated,
    tier1Direct: direct.filter(e => e.tier === 1).length,
    bothHighDegree: direct.filter(e => byId.get(e.a).deg >= 15 && byId.get(e.b).deg >= 15).length,
    sameCell: direct.filter(e => e.db === 0 && e.de === 0).length,
    roleTags: Object.values(tally).reduce((a, b) => a + b, 0),
    roleTagsPerNode: +(Object.values(tally).reduce((a, b) => a + b, 0) / N.length).toFixed(2),
    withDate: dated.length, withoutDate: undated.length,
    withoutDateIds: undated.map(n => n.id),
    preFirstEra: N.filter(n => n.y0 != null && n.y0 < 1940).map(n => [n.id, n.y0]),
    withEnd: N.filter(n => n.y1 != null).length,
    withRealSpan: N.filter(n => n.span > 0).length,
    longSpans: N.filter(n => n.span > 10).map(n => [n.id, n.y0, n.y1]),
    lastEraShare: Math.round(N.filter(n => n.era === 3).length / (dated.length || 1) * 100),
    dateConflicts: Object.keys(src.conflicts || {}).length,
    dateConflictsOnMap: Object.keys(src.conflicts || {}).filter(i => L0.has(i)),
    dateConflictsChangingEra: Object.entries(src.conflicts || {})
      .filter(([i]) => L0.has(i))
      .map(([i, vs]) => [i, [...new Set(vs.map(v => eraIndex(yearOf(v))))]])
      .filter(([, es]) => es.length > 1),
    missingRoles,
    bandOrderBasis, haveC,
    /* The pin, its drift, and the near-ties that make drift possible. */
    rarityPin: RARITY_PIN, rarityPinDate: RARITY_PIN_DATE,
    rarityObserved: observed, rarityDrift: pinDrift, unpinnedTags,
    /* A band whose tag is claimed by more than half the map can only win when a
       node carries nothing rarer, so its population is a RESIDUAL rather than a
       category. Naming that is the difference between a thin row that is honest
       and a thin row that looks broken. */
    residualBands: bands.filter(b => (tally[b] || 0) > N.length * 0.5),
    /* Adjacent tags whose counts sit within 10% of each other. These are the pairs
       whose rarity ranks can swap between research passes, and a swap moves every
       node carrying both from one band to the other. It happened between these two
       datasets: oversight (68) and disclosure (74) are 8% apart on the current
       board and inverted from the legacy one, moving fourteen nodes. The rule is
       still right — it is the near-ties that need watching, and they are named
       here rather than discovered later. */
    rarityTies: Object.entries(tally).sort((a, b) => a[1] - b[1])
      .flatMap(([r, c], i, arr) => {
        const nxt = arr[i + 1];
        return nxt && (nxt[1] - c) / nxt[1] < 0.1 ? [[r, c, nxt[0], nxt[1]]] : [];
      }),
    degMin: Math.min(...N.map(n => n.deg)), degMax: Math.max(...N.map(n => n.deg)),
    degAtFloor: N.filter(n => n.deg === FLOOR).length,
    memberRows: N.reduce((s, n) => s + (n.members ? n.members.length : 0), 0),
    membersMin: Math.min(...N.map(n => n.memberCount)),
    membersMax: Math.max(...N.map(n => n.memberCount)),
    membersMedian: N.map(n => n.memberCount).sort((a, b) => a - b)[Math.floor(N.length / 2)],
  };

  /* IMAGES. Absent by default and that is a supported state, not a hole: the chip
     falls back to its class letter, which says what the node IS rather than
     implying an unknown face. Only CLEARS and ASK are drawn — an image that does
     not clear, or was never found, is not drawn at all, exactly as an unsourced
     claim is not printed. Field names inherited from the sibling board:
     `photo` + `photoCredit`, plus `photoKind` because a logo must not be cropped. */
  /* Records live under `images` so the file can carry its own documentation --
     the clearance vocabulary and the record shape -- without those doc keys
     sitting in the same namespace as node ids. Bare top-level keying is still
     accepted, which is the shape Design specified. */
  const IMG = (images && images.images) ? images.images : (images || {});
  let imgClears = 0, imgAsk = 0;
  for (const n of N) {
    const r = IMG[n.id];
    const ok = !!(r && r.photo && (r.clearance === 'clears' || r.clearance === 'ask'));
    n.photo = ok ? r.photo : null;
    n.photoCredit = ok ? (r.photoCredit || '') : null;
    n.photoKind = ok ? (r.photoKind || (n.cls === 'person' ? 'portrait' : 'mark')) : null;
    n.photoClearance = ok ? r.clearance : null;
    n.photoNote = ok && r.clearance === 'ask' ? (r.note || 'clearance ambiguous') : '';
    if (ok) { if (r.clearance === 'clears') imgClears++; else imgAsk++; }
  }
  figures.withPhoto = imgClears + imgAsk;
  figures.photoClears = imgClears;
  figures.photoAsk = imgAsk;
  figures.photoMissing = N.length - imgClears - imgAsk;

  const highlights = buildHighlights(supplied, N, all, L0);
  figures.flagged = highlights.flags.length;
  figures.flaggedPct = Math.round(highlights.flags.length / N.length * 100);
  figures.flaggedOverCap = highlights.flags.length > Math.round(N.length * HIGHLIGHT_CAP);
  figures.flaggedUnknownIds = highlights.unknownIds;

  const ladder = [
    { rule: 'every hand-written L0-L0 edge (today\'s rest state)', n: direct.length, of: 'direct' },
    { rule: '+ summarised shared-member edges', n: all.length, of: 'drawn' },
    { rule: 'claim tier 1 only', n: figures.tier1Direct, of: 'direct' },
    { rule: 'both endpoints degree >= 15', n: figures.bothHighDegree, of: 'direct' },
    { rule: 'crosses >= 1 function band', n: direct.filter(e => e.db >= 1).length, of: 'direct' },
    { rule: 'crosses >= 1 era', n: direct.filter(e => (e.de || 0) >= 1).length, of: 'direct' },
    { rule: 'crosses >= 2 bands', n: direct.filter(e => e.db >= 2).length, of: 'direct' },
    { rule: 'crosses >= 2 bands AND >= 1 era  [clause 1]', n: structural.length, of: 'direct' },
    { rule: '+ one anchor per node  [clause 2] = THE RULE', n: restEdges.length, of: 'drawn' },
  ].map(r => ({ ...r, pct: Math.round(r.n / (r.of === 'direct' ? direct.length : all.length) * 100) }));

  return {
    key: src.key, label: src.label, source: src.source, note: src.note,
    fields: src.fields, memberBasis: src.memberBasis,
    config: {
      floor: FLOOR, degreeIs: 'distinct neighbours',
      primaryRule: 'rarest role tag on the map wins',
      bandOrder: bandOrderBasis,
      edgeRule: 'db>=2 && de>=1, plus one anchor per node',
      sharedAtRest: false, geo: GEO,
    },
    figures, rarity: tally, matrix, ladder, highlights,
    viaMembers: src.viaMembers || {},
    eras: cols, bands: bandRecs, worldH, worldW: GEO.mapW,
    nodes: N, edges: all,
  };
}

export function buildAll(inputs) {
  setAuthoredShorts(inputs.shorts);
  const current = layout(normaliseCurrent(inputs.design), inputs.highlights, inputs.images);
  const legacy = inputs.extract
    ? layout(normaliseLegacy(inputs.extract, inputs.dossiers, inputs.docs), inputs.highlights, inputs.images)
    : null;
  return {
    generated: new Date().toISOString().slice(0, 10),
    default: 'current',
    /* The correction to the comp's §0. Kept in the model rather than typed into
       the page so it cannot drift from the run that produced it. */
    readCap: {
      cap: '~1MB on the GitHub read API',
      overCap: [
        ['data/the-program.json', '6.9MB', 'the whole board'],
        ['data/l0-model.json', '5.7MB', 'the L0 model the brief cited'],
      ],
      correction: 'Both are tracked and pushed. They read as absent over the API ' +
        'because of the cap, not because they are missing, and the brief\'s figures ' +
        'were reproducible all along. data/design-extract.json exists to be readable.',
      trap: 'data/l0-extract.json is readable and accurate for the 968-node graph, ' +
        'but its `deg` field is an edge-instance count. Degree here is always ' +
        'recomputed from distinct neighbours.',
    },
    /* THE BACKFILL QUEUE — every field the design reads that the authoritative
       extract does not yet carry, with where to pull it from. Written as
       instructions rather than complaints: each row is a task, and the design
       degrades honestly until it lands rather than guessing. */
    gaps: [
      /* RETIRED 26 August 2026, after auditing every row against the data rather
         than against the row. Three were describing gaps that had already been
         filled -- via[] (109 of 109 shared edges carry the id array), members[]
         (110 of 110 carry full member records) and C/A/D (110 of 110) -- and the
         queue went on listing them because nothing ever asked whether a queued
         field was still missing. A stale backfill row is not harmless: it is a
         standing instruction to redo finished work, and it made this file and the
         data disagree, which is the exact drift the row-count check was written
         for. verify.py now asserts the queue in BOTH directions. */
      /* RETIRED 26 August 2026. membersDirect and membersRouted are now projected
         onto every one of the 110 nodes. Nothing CONSUMES them yet, but an unused
         field is not a backfill gap -- the queue lists data the design reads and
         the data withholds, and leaving a supplied field in it is the staleness
         verify.py now checks for in both directions. */
      /* RETIRED 26 August 2026, as a CATEGORY ERROR rather than as work done.
         The row asked for an end year for the 64 nodes without one. Audited, they
         overwhelmingly SHOULD NOT HAVE ONE: 37 are institutions that still exist
         (CIA, DIA, NASA, DoD, the House), 8 are statutes that have not been
         repealed, 9 are documents and 1 an event -- point-in-time by nature -- and
         all 9 programmes are ongoing or alleged with no attested end. Absence is
         the correct value, not a hole.

         Searching their own records for end-language returned 10 hits and NOT ONE
         was an end for that node: AARO disestablished AOIMSG; CIA, DIA and the FAB
         each terminated something else; TTSA RENAMED itself in 2022; 10 U.S.C.
         119's subsection (a)/(b) reporting terminated in 2021 while the statute
         remains law. Pattern-matching would have written ten false end dates, each
         one asserting that a live body had ceased to exist.

         And the field is not rendered: y0/y1/span reach the layout model and
         Design's brief figures, never the page. notes/DATE-EXTENT-2026-08-26.md */
      ['photo / photoCredit / photoKind', 'a mark for the 101 nodes that have none',
        'REWRITTEN 26 August 2026 after the sourcing pass; 9 of 110 now carry one. What is left is NOT one task. 30 institutions have no free-licensed mark of their OWN that survives an 11px square -- a parent body\u2019s seal asserts a false identity, a wide wordmark becomes a 2px sliver, CC BY-SA carries share-alike, and several are foreign-state or trademarked. The other 71 nodes are documents, programmes, legislation and events, which mostly have no mark to find at all. notes/IMAGE-SOURCING-2026-08-26.md has the per-node reasons',
        'the chip glyph slot and the dossier tile are built, tested and now populated for 9; the class letter is a supported state for the rest and is not a failure'],
      /* Added 26 August 2026, both from the implementation session. The standing
         rule is that any new field the design reads gets a row here saying what to
         pull and where from, so nobody has to re-derive the ask. */
      /* RETIRED 26 August 2026. All 174 denial edges adjudicated one at a time
         against a rule fixed before reading any of them: 124 directed, 36
         association, 14 undirected. data/denial-adjudication.json is the record
         and merge.py stamps it onto the edges. The shipped convention -- `a`
         always issues -- was wrong on 34 of the 124.
         notes/DENIAL-ADJUDICATION-2026-08-26.md */
      /* RETIRED 26 August 2026. All 46 overlong labels authored in
         data/l0-shorts.json; 0 of 110 now exceed the 37 characters the chip
         holds, and `every chip label fits the chip it is drawn in` keeps it
         that way. Middle truncation stays as the safety net it was meant to be. */
    ],
    current, legacy,
  };
}

/* ============================ node main ============================ */

async function main() {
  const fs = await import('node:fs');
  const path = await import('node:path');
  /* fileURLToPath, not .pathname. A file URL percent-encodes spaces, so
     .pathname yields "Missing%20individuals..." and every read fails with
     ENOENT on a path that plainly exists. This repo lives under a directory
     with three spaces in it. Reported to Design; re-applied 24 Aug after the
     layout package shipped from a baseline that did not carry it. */
  const { fileURLToPath } = await import('node:url');
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const rd = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
  const has = p => fs.existsSync(path.join(root, p));
  const glob = d => fs.readdirSync(path.join(root, d))
    .filter(f => f.endsWith('.json')).sort().map(f => rd(path.join(d, f)));

  const highlightsFile = has('data/l0-highlights.json') ? rd('data/l0-highlights.json') : null;
  const inputs = {
    design: rd('data/design-extract.json'),
    extract: has('data/l0-extract.json') ? rd('data/l0-extract.json') : null,
    dossiers: has('research/dossiers') ? glob('research/dossiers').flat() : [],
    docs: has('research') ? glob('research') : [],
    highlights: highlightsFile,
    images: has('data/l0-images.json') ? rd('data/l0-images.json') : null,
    shorts: has('data/l0-shorts.json') ? rd('data/l0-shorts.json') : null,
  };

  /* The marks are NOT inlined here. `photo` stays a repo path in this model.
     Inlining them here put ~695KB of base64 into the file TWICE -- `current` and
     `legacy` both carry nodes -- and took it from 490KB to 1836KB, straight
     through the ~1MB GitHub API read cap this file exists to stay under. The
     build's own guard caught it.
     The bytes belong in the page, not in the description of the page. (The old
     shell inlined them at its own build time; it was retired on 25 September
     2026.) */

  const out = buildAll(inputs);

  const json = JSON.stringify(out);
  fs.writeFileSync(path.join(root, 'data/l0-layout-model.json'), json);
  /* It also wrote data/l0-layout-model.js, a window global for the old
     single-file shell, until that shell was retired on 25 September 2026. */

  for (const m of [out.current, out.legacy]) {
    if (!m) continue;
    const f = m.figures;
    console.log(`${m.key.padEnd(8)} L0 ${f.l0} · direct ${f.directEdges} · summarised ${f.summarisedEdges} ` +
      `· at rest ${f.restDrawn} of ${f.drawnBeforeBudget} (${f.restPct}%) · dated ${f.withDate}/${f.l0} ` +
      `· last era ${f.lastEraShare}% · bands by ${f.bandOrderBasis}`);
    if (f.orphans) { console.error('FATAL: the budget dropped every edge on: ' + f.orphanIds.join(', ')); process.exit(1); }
    /* The highlights file is an editorial pass authored against ONE board, and
       it names the board it was written for. Fatal on that board -- a flag
       pointing at a node that is not there is a broken pointer. On any other
       dataset the same mismatch is a finding, not a fault: `legacy` is a
       superseded 96-node snapshot kept as a cross-check, and three of the
       fourteen flags name nodes the old floor excluded. Killing the build over
       that would be obeying a stale dataset, which is the same error the rarity
       pin exists to prevent -- so report it and carry on, and never silence it
       by trimming the editorial file to the intersection. */
    const authoredFor = (highlightsFile || {}).authoredFor || 'current';
    if (f.flaggedUnknownIds.length) {
      if (m.key === authoredFor) {
        console.error('FATAL: highlights name ids not on the ' + m.key +
          ' map, which they are authored for: ' + f.flaggedUnknownIds.join(', '));
        process.exit(1);
      }
      console.log('  note  ' + f.flaggedUnknownIds.length + ' of ' +
        (f.flagged + f.flaggedUnknownIds.length) + ' highlights are absent from `' +
        m.key + '` (authored for `' + authoredFor + '`): ' +
        f.flaggedUnknownIds.join(', '));
    }
    if (f.flaggedOverCap) { console.error('FATAL: highlight flags over the ' + Math.round(HIGHLIGHT_CAP * 100) + '% cap'); process.exit(1); }
  }
  /* The whole point of a purpose-built extract is that it can be read. */
  const kb = Math.round(json.length / 1024);
  console.log(`  model ${kb}KB -> data/l0-layout-model.json`);
  if (json.length > 1024 * 1024) {
    console.error(`FATAL: model is ${kb}KB, over the ~1MB read cap this file exists to stay under`);
    process.exit(1);
  }
}

/* Main guard. The previous form compared import.meta.url against the last
   '/'-separated segment of argv[1]; on Windows argv[1] is backslash-separated,
   the split found no '/', the comparison ran against the whole path and the
   script exited 0 having written nothing (found 2 Sept 2026). Resolve both
   sides to a real path instead. */
if (typeof process !== 'undefined' && process.argv && process.argv[1]) {
  const { fileURLToPath } = await import('node:url');
  const path = await import('node:path');
  if (path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url))) main();
}
