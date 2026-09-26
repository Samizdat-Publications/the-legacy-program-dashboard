/* The directories (redesign phase 9, task 2): #/people #/orgs #/programmes
 * #/laws #/places #/events, one per node class.
 *
 * A sortable table of every node of the class, each row linking its node, with a
 * rail of facet chips beside it. Every filter and the sort order are in the URL,
 * so a filtered directory is a link. The count on a chip is the number of rows in
 * the WHOLE directory with that value, not in the current filter (the evidence
 * explorer's convention); the header carries the filtered count.
 *
 * People carry the facets of research/_person_facets.json (shipped as
 * /data/facets.json): roles, vital status, role status and sworn testimony, each
 * derived from the person's own record, with `unknown` where the record is
 * silent. Every other value is read from the board: era and dates from
 * index.json, the topic and its section from topics.json. Nothing is written
 * here: every string is a label, a value, a count, or the fixed words below.
 *
 * At phone width the rail folds behind one control and each row is a card.
 */
import '../styles/directory.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import {
  loadIndex, loadTopics, loadFacets, clsColour,
  type IndexNode, type TopicsFile, type FacetsFile, type PersonFacets,
} from '../data';

interface DirDef { id: string; cls: string; title: string; noun: [string, string]; }
export const DIRS: DirDef[] = [
  { id: 'people', cls: 'person', title: 'People', noun: ['person', 'people'] },
  { id: 'orgs', cls: 'institution', title: 'Organisations', noun: ['organisation', 'organisations'] },
  { id: 'programmes', cls: 'program', title: 'Programmes', noun: ['programme', 'programmes'] },
  { id: 'laws', cls: 'legislation', title: 'Laws', noun: ['law', 'laws'] },
  { id: 'places', cls: 'location', title: 'Places', noun: ['place', 'places'] },
  { id: 'events', cls: 'event', title: 'Events', noun: ['event', 'events'] },
];

/* One row, with every facet value it can be filtered on. */
interface Row {
  n: IndexNode;
  topic: string | null;       /* primary topic id */
  section: string;            /* its section, or NONE */
  topics: Set<string>;        /* every topic the node is a member of */
  f: PersonFacets | null;
}

const NONE = 'none';
const UNK = 'unknown';

/* The facet groups, by URL key. `people` groups apply only to #/people. */
interface Group {
  key: string; head: string; blurb?: string; people?: boolean;
  values: (rows: Row[], ctx: Ctx) => { value: string; label: string }[];
  of: (r: Row) => string[];
}

interface Ctx { topics: TopicsFile; facets: FacetsFile; eraLabel: Map<string, string>; }

const ROLE_WORD: Record<string, string> = {
  official: 'official', military: 'military', intelligence: 'intelligence', scientist: 'scientist',
  contractor: 'contractor', legislator: 'legislator', witness: 'witness (first-hand account)',
  claimant: 'claimant', researcher: 'researcher', journalist: 'journalist', media: 'media',
  counsel: 'counsel',
};

const GROUPS: Group[] = [
  {
    key: 'role', head: 'Role', people: true,
    blurb: 'From the person’s own record. A person may hold several.',
    values: (_r, c) => c.facets.vocab.roles.filter((x) => x !== 'claimant').map((x) => ({ value: x, label: ROLE_WORD[x] || x }))
      .concat([{ value: NONE, label: 'no role the record states' }]),
    of: (r) => {
      const rs = (r.f ? r.f.roles : []).filter((x) => x !== 'claimant');
      return rs.length ? rs : [NONE];
    },
  },
  {
    key: 'claimant', head: 'Claimant', people: true,
    blurb: 'Asserts something about the programme that no primary record on the board confirms. The assertion itself is testimony: Tier 2.',
    values: () => [{ value: 'yes', label: 'claimant' }, { value: 'no', label: 'not a claimant' }],
    of: (r) => [r.f && r.f.roles.indexOf('claimant') >= 0 ? 'yes' : 'no'],
  },
  {
    key: 'vital', head: 'Vital status', people: true,
    blurb: 'Dead only where the record states a death; alive where it records an act in 2020 or later; otherwise unknown.',
    values: (_r, c) => c.facets.vocab.vitalStatus.map((x) => ({ value: x, label: x })),
    of: (r) => [r.f ? r.f.vitalStatus : UNK],
  },
  {
    key: 'rstatus', head: 'Role status', people: true,
    blurb: 'Whether the record says they still hold the post that puts them here.',
    values: (_r, c) => c.facets.vocab.roleStatus.map((x) => ({ value: x, label: x })),
    of: (r) => [r.f ? r.f.roleStatus : UNK],
  },
  {
    key: 'oath', head: 'Testified under oath', people: true,
    blurb: 'Yes only where the record says the testimony was sworn.',
    values: (_r, c) => c.facets.vocab.underOath.map((x) => ({ value: x, label: x === 'yes' ? 'under oath' : x === 'no' ? 'record says not' : x })),
    of: (r) => [r.f ? r.f.underOath : UNK],
  },
  {
    key: 'era', head: 'Era',
    blurb: 'By the start date the record carries.',
    values: (_r, c) => Array.from(c.eraLabel, ([value, label]) => ({ value, label })),
    of: (r) => [r.n.era],
  },
  {
    key: 'section', head: 'Topic section',
    blurb: 'The section of the node’s primary topic.',
    values: (_r, c) => c.topics.sections.map((s) => ({ value: s.id, label: s.title }))
      .concat([{ value: NONE, label: 'in no topic' }]),
    of: (r) => [r.section],
  },
];

const SORTS: { key: string; head: string }[] = [
  { key: 'name', head: 'NAME' }, { key: 'date', head: 'DATES' }, { key: 'topic', head: 'PRIMARY TOPIC' },
  { key: 'claims', head: 'CLAIMS' }, { key: 'links', head: 'LINKS' },
];

export async function renderDirectory(view: HTMLElement, dir: string, q: URLSearchParams): Promise<void> {
  clear(view);
  const def = DIRS.filter((d) => d.id === dir)[0] || DIRS[0];
  setTitle(def.title);
  const wait = h('div', { class: 'dir-wait dim' }, 'Reading the board …');
  view.append(wait);

  let idx, topics: TopicsFile, facets: FacetsFile;
  try {
    [idx, topics, facets] = await Promise.all([loadIndex(), loadTopics(), loadFacets()]);
  } catch (e) {
    clear(view);
    view.append(h('section', { class: 'notice' },
      h('h2', null, 'The directory data is not being served'), h('p', null, (e as Error).message)));
    return;
  }
  clear(view);

  const eraLabel = new Map<string, string>();
  for (const e of idx.eras) eraLabel.set(e.id, e.label);
  const ctx: Ctx = { topics, facets, eraLabel };
  const tsec = new Map(topics.topics.map((t) => [t.id, t.section]));
  const ttitle = new Map(topics.topics.map((t) => [t.id, t.title]));
  const stitle = new Map(topics.sections.map((s) => [s.id, s.title]));

  const all: Row[] = idx.nodes.filter((n) => n.cls === def.cls).map((n) => {
    const ai = topics.appearsIn[n.id] || [];
    const topic = ai.length ? ai[0][0] : null;
    return {
      n, topic, section: (topic && tsec.get(topic)) || NONE,
      topics: new Set(ai.map((x) => x[0])),
      f: def.id === 'people' ? (facets.people[n.id] || null) : null,
    };
  });

  const groups = GROUPS.filter((g) => !g.people || def.id === 'people');
  const active = new Map<string, string>();
  for (const g of groups) { const v = q.get(g.key); if (v) active.set(g.key, v); }
  const topicQ = q.get('topic');
  let shown = all.filter((r) => {
    for (const g of groups) {
      const v = active.get(g.key);
      if (v != null && g.of(r).indexOf(v) < 0) return false;
    }
    return !topicQ || r.topics.has(topicQ);
  });
  const sort = SORTS.some((s) => s.key === q.get('sort')) ? String(q.get('sort')) : 'date';
  const desc = q.get('desc') === '1';
  shown = sortRows(shown, sort, desc, ttitle);

  const root = h('div', { class: 'dir', 'data-dir': def.id, 'data-cls': def.cls });
  view.append(root);

  /* ---- the tabs --------------------------------------------------------- */
  const tabs = h('nav', { class: 'dir-tabs', 'aria-label': 'Directories' });
  for (const d of DIRS) {
    const n = idx.nodes.filter((x) => x.cls === d.cls).length;
    const on = d.id === def.id;
    tabs.append(h('a', {
      class: 'dir-tab' + (on ? ' on' : ''), href: '#/' + d.id, 'data-dir': d.id,
      'aria-current': on ? 'page' : null,
    }, d.title.toUpperCase(), ' ', h('span', { class: 'dir-tab-n' }, String(n))));
  }
  root.append(h('div', { class: 'dir-top' },
    h('div', { class: 'eyebrow' }, 'Directories'),
    h('h1', { class: 'dir-h1' }, def.title), tabs));

  const wrap = h('div', { class: 'dir-body' });
  const rail = h('aside', { class: 'dir-rail', 'data-open': '0' });
  const main = h('div', { class: 'dir-main' });
  wrap.append(rail, main);
  root.append(wrap);

  /* ---- the rail --------------------------------------------------------- */
  const nAct = active.size + (topicQ ? 1 : 0);
  const tog = h('button', {
    type: 'button', class: 'dir-filter-toggle', 'aria-expanded': 'false',
    onclick: () => {
      const on = rail.getAttribute('data-open') !== '1';
      rail.setAttribute('data-open', on ? '1' : '0');
      tog.setAttribute('aria-expanded', on ? 'true' : 'false');
    },
  }, 'FILTERS' + (nAct ? ' · ' + nAct + ' on' : '') + ' ', h('span', { class: 'cyan', 'aria-hidden': 'true' }, '▾'));
  const filters = h('div', { class: 'dir-filters' });
  rail.append(tog, filters);
  filters.append(h('p', { class: 'dir-note faint' },
    'The number on each filter counts the whole directory, not the rows now shown.'));
  if (nAct) filters.append(h('a', { class: 'dir-clear', href: link(def.id, q, null) },
    'clear ' + nAct + ' filter' + (nAct === 1 ? '' : 's')));

  for (const g of groups) {
    const counts = new Map<string, number>();
    for (const r of all) for (const v of g.of(r)) counts.set(v, (counts.get(v) || 0) + 1);
    const vals = g.values(all, ctx).filter((v) => (counts.get(v.value) || 0) > 0 || active.get(g.key) === v.value);
    if (!vals.length) continue;
    filters.append(h('div', { class: 'dir-ghead eyebrow' }, g.head));
    if (g.blurb) filters.append(h('div', { class: 'dir-gblurb faint' }, g.blurb));
    const box = h('div', { class: 'dir-chips', 'data-key': g.key });
    for (const v of vals) {
      const on = active.get(g.key) === v.value;
      box.append(h('a', {
        class: 'dir-chip' + (on ? ' on' : ''), href: link(def.id, q, [g.key, on ? null : v.value]),
        'aria-pressed': on ? 'true' : 'false', 'data-key': g.key, 'data-val': v.value,
      }, h('span', { class: 'dir-chip-l' }, v.label), h('span', { class: 'dir-chip-n' }, String(counts.get(v.value) || 0))));
    }
    filters.append(box);
  }

  /* the topic, as a list grouped by section: 93 topics are too many for chips */
  const tcount = new Map<string, number>();
  for (const r of all) for (const t of r.topics) tcount.set(t, (tcount.get(t) || 0) + 1);
  filters.append(h('div', { class: 'dir-ghead eyebrow' }, 'Topic'));
  filters.append(h('div', { class: 'dir-gblurb faint' }, 'Any topic the node is a member of.'));
  const sel = h('select', { class: 'dir-topic', 'aria-label': 'Filter by topic' });
  sel.append(h('option', { value: '' }, 'every topic'));
  for (const s of topics.sections) {
    const og = h('optgroup', { label: s.title });
    for (const t of topics.topics.filter((x) => x.section === s.id)) {
      const n = tcount.get(t.id) || 0;
      if (!n && t.id !== topicQ) continue;
      og.append(h('option', { value: t.id, selected: t.id === topicQ ? 'selected' : null }, t.title + ' · ' + n));
    }
    if (og.childNodes.length) sel.append(og);
  }
  sel.addEventListener('change', () => { location.hash = link(def.id, q, ['topic', sel.value || null]); });
  filters.append(sel);

  /* ---- the header ------------------------------------------------------- */
  const head = h('div', { class: 'dir-head' },
    h('span', { class: 'dir-count' }, String(shown.length)),
    h('span', { class: 'dim' }, 'of ' + all.length + ' ' + def.noun[all.length === 1 ? 0 : 1]));
  const bits: string[] = [];
  for (const g of groups) {
    const v = active.get(g.key);
    if (v == null) continue;
    const lab = (g.values(all, ctx).filter((x) => x.value === v)[0] || { label: v }).label;
    bits.push(g.head.toLowerCase() + ': ' + lab);
  }
  if (topicQ) bits.push('topic: ' + (ttitle.get(topicQ) || topicQ));
  if (bits.length) head.append(h('span', { class: 'dir-active amber' }, bits.join('  ·  ')));
  main.append(head);

  if (!shown.length) {
    main.append(h('p', { class: 'dir-note dim' }, 'No ' + def.noun[0] + ' on the board matches every one of those filters.'));
    publish();
    return;
  }

  /* ---- the table -------------------------------------------------------- */
  const people = def.id === 'people';
  const th = (key: string | null, label: string, cls: string): HTMLElement => {
    if (!key) return h('th', { class: cls }, label);
    const on = sort === key;
    const nq = new URLSearchParams(q);
    nq.set('sort', key);
    if (on && !desc) nq.set('desc', '1'); else nq.delete('desc');
    return h('th', { class: cls, 'aria-sort': on ? (desc ? 'descending' : 'ascending') : null },
      h('a', { class: 'dir-sort' + (on ? ' on' : ''), href: '#/' + def.id + qs(nq) },
        label + (on ? (desc ? ' ↓' : ' ↑') : '')));
  };
  const heads: HTMLElement[] = [th('name', 'NAME', 'c-name')];
  if (people) heads.push(th(null, 'ROLES', 'c-roles'), th(null, 'STATUS', 'c-status'), th(null, 'UNDER OATH', 'c-oath'));
  heads.push(th('date', people ? 'DATE' : 'DATES', 'c-date'), th('topic', 'PRIMARY TOPIC', 'c-topic'),
    th('claims', 'CLAIMS T1 · T2 · T3', 'c-claims'), th('links', 'LINKS', 'c-links'));
  const table = h('table', { class: 'dir-table' + (people ? ' people' : '') },
    h('thead', null, h('tr', null, ...heads)));
  const tbody = h('tbody');
  table.append(tbody);
  main.append(table);

  for (const r of shown) tbody.append(row(r, people, ttitle, stitle, eraLabel));
  publish();
}

function row(r: Row, people: boolean, ttitle: Map<string, string>, stitle: Map<string, string>,
             eraLabel: Map<string, string>): HTMLElement {
  const n = r.n;
  const tr = h('tr', { class: 'dir-row', 'data-id': n.id });
  tr.append(h('td', { class: 'c-name' }, mark(clsColour(n.cls)), ' ', h('a', { href: '#/n/' + n.id }, n.label)));
  if (people) {
    const f = r.f;
    const b = (f && f.basis) || {};
    tr.append(h('td', { class: 'c-roles', 'data-h': 'roles', title: b.roles || null },
      f && f.roles.length ? f.roles.map((x) => ROLE_WORD[x] || x).join(', ') : h('span', { class: 'faint' }, 'none stated')));
    const st = h('td', { class: 'c-status', 'data-h': 'status' });
    st.append(h('span', { class: 'dir-st' + (f && f.vitalStatus !== UNK ? '' : ' faint'), title: b.vitalStatus || null },
      f ? (f.vitalStatus === UNK ? 'vital status unknown' : f.vitalStatus) : 'no facets'));
    st.append(h('span', { class: 'dir-st' + (f && f.roleStatus !== UNK ? ' dim' : ' faint'), title: b.roleStatus || null },
      f ? (f.roleStatus === UNK ? 'role status unknown' : f.roleStatus + ' role') : ''));
    tr.append(st);
    tr.append(h('td', { class: 'c-oath', 'data-h': 'under oath', title: b.underOath || null },
      !f || f.underOath === UNK ? h('span', { class: 'faint' }, 'not stated')
        : f.underOath === 'yes' ? 'under oath' : 'record says not'));
  }
  /* the era on its own line, named as the era, so "1946 · THROUGH 1969" is
     never read as a span (blind critic, phase 9 round 1) */
  const d = n.dateStart && n.dateEnd && n.dateStart !== n.dateEnd ? n.dateStart + ' to ' + n.dateEnd
    : n.dateStart || n.dateEnd || '';
  tr.append(h('td', { class: 'c-date', 'data-h': people ? 'date' : 'dates' },
    d || h('span', { class: 'faint' }, 'no date recorded'),
    h('span', { class: 'faint dir-era' }, 'era ' + (eraLabel.get(n.era) || n.era))));
  tr.append(h('td', { class: 'c-topic', 'data-h': 'primary topic' },
    r.topic ? h('a', { href: '#/topic/' + r.topic, title: stitle.get(r.section) || r.section }, ttitle.get(r.topic) || r.topic)
      : h('span', { class: 'faint' }, 'in no topic')));
  tr.append(h('td', { class: 'c-claims', 'data-h': 'claims T1 · T2 · T3' },
    h('span', { class: 't1' }, String(n.claims[0])), ' · ',
    h('span', { class: 't2' }, String(n.claims[1])), ' · ',
    h('span', { class: 't3' }, String(n.claims[2]))));
  tr.append(h('td', { class: 'c-links', 'data-h': 'links' }, String(n.deg)));
  return tr;
}

function sortRows(rows: Row[], key: string, desc: boolean, ttitle: Map<string, string>): Row[] {
  const name = (r: Row) => r.n.label.toLowerCase();
  const k = (r: Row): [number, string | number] => {
    if (key === 'date') return r.n.dateStart ? [0, r.n.dateStart] : [1, ''];
    if (key === 'topic') return r.topic ? [0, (ttitle.get(r.topic) || r.topic).toLowerCase()] : [1, ''];
    if (key === 'claims') return [0, -(r.n.claims[0] + r.n.claims[1] + r.n.claims[2])];
    if (key === 'links') return [0, -r.n.deg];
    return [0, name(r)];
  };
  const out = rows.slice().sort((a, b) => {
    const x = k(a), y = k(b);
    /* the undated, the topic-less: always last, whichever way the sort runs */
    if (x[0] !== y[0]) return x[0] - y[0];
    let c = x[1] < y[1] ? -1 : x[1] > y[1] ? 1 : 0;
    if (desc) c = -c;
    return c || (name(a) < name(b) ? -1 : name(a) > name(b) ? 1 : 0);
  });
  return out;
}

function qs(q: URLSearchParams): string {
  const s = q.toString();
  return s ? '?' + s : '';
}

/* The route with one key set or removed; null clears every filter but keeps the sort. */
function link(dir: string, q: URLSearchParams, kv: [string, string | null] | null): string {
  const nq = new URLSearchParams();
  if (kv) {
    q.forEach((v, k) => { if (k !== kv[0]) nq.set(k, v); });
    if (kv[1] != null) nq.set(kv[0], kv[1]);
  } else {
    for (const k of ['sort', 'desc']) { const v = q.get(k); if (v) nq.set(k, v); }
  }
  return '#/' + dir + qs(nq);
}

function publish(): void {
  const w = window as unknown as { __app?: Record<string, unknown> };
  w.__app = w.__app || {};
  (w.__app as Record<string, unknown>).directory = { ready: true };
}
