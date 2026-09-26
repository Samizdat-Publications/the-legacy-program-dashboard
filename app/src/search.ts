/* search.ts: one search over the whole board (redesign phase 9, task 3).
 *
 * Topics, the big questions (phase 10), the six directories (and the people
 * directory filtered by a role), sources (phase 8's library, once it is served), nodes, threads, timeline events
 * and claim text, in ONE ranked list, every row carrying a badge that says what
 * it is. index.json is loaded at boot; everything else is fetched the first time
 * a query runs, so none of it is paid for on first paint.
 *
 * THE RANK. Every row gets one number, lower first:
 *   0 to 5   a NAME match (a topic's title, a question's, a directory, a
 *            node's label, a thread's title, a source's title, an event's label): 0 the id,
 *            1 the whole name, 2 its start, 3 inside the id, 4 inside the
 *            name, 5 every word somewhere in it. Ties go to the kind (a
 *            directory, then a topic, a question, then a node, a thread, a source, an
 *            event), then to the node's degree.
 *   6        an event whose text, not its label, matches.
 *   7 and up claims, 7 + their claim rank / 100, so the claim ranking below,
 *            in which TIER STRICTLY DOMINATES, orders them among themselves
 *            and nothing it does can lift a claim above a name match.
 * Each kind is capped (24 nodes, 24 sources, 12 events, 12 claims, every
 * topic, directory and thread) before the list is merged.
 *
 * Keys: ArrowDown and ArrowUp move through the rows, Enter opens the one
 * marked (the first when none is), Escape clears the field and closes the list.
 *
 * Every result is a route: #/topic/<id>, #/q/<id>, #/<directory>, #/n/<id>, #/t/<id>,
 * #/s/<id> (phase 8's source page), and for an event that names
 * no node, its era on the timeline.
 */
import { saidKind, saidMark } from './attrib';
import { h, clear, mark } from './dom';
import {
  loadIndex, loadClaims, loadTimeline, loadThreads, loadTopics, loadFacets, loadSourcesIfAny, clsColour,
  type IndexNode, type ClaimRow, type TimelineEvent, type Thread, type TopicRow, type SourceRow,
} from './data';
import { loadQuestions, type QuestionRow } from './p10data';

const MAX_NODE_HITS = 24;
const MAX_CLAIM_HITS = 12;
const MAX_EVENT_HITS = 12;

let nodes: IndexNode[] = [];
let claims: ClaimRow[] | null = null;
/* claim text, lowercased and with punctuation flattened, computed once when
   claims.json arrives rather than on every keystroke over 6,000 rows */
let claimLc: string[] = [];
let claimFlat: string[] = [];
let claimSquash: string[] = [];
let asked = false;
let claimsState: 'idle' | 'loading' | 'ready' | 'absent' = 'idle';
/* the rest: null until they arrive, [] if they never do */
let events: TimelineEvent[] | null = null;
let eventFlat: string[] = [];
let threads: Thread[] | null = null;
let topics: TopicRow[] | null = null;
let questions: QuestionRow[] | null = null;
let sources: SourceRow[] | null = null;
let roleCounts: Record<string, number> = {};

/* The directories, with the words a reader might type for each. */
const DIRS: { id: string; title: string; words: string; cls: string }[] = [
  { id: 'people', title: 'People', words: 'people persons person directory', cls: 'person' },
  { id: 'orgs', title: 'Organisations', words: 'organisations organizations orgs institutions agencies companies directory', cls: 'institution' },
  { id: 'programmes', title: 'Programmes', words: 'programmes programs projects directory', cls: 'program' },
  { id: 'laws', title: 'Laws', words: 'laws legislation statutes acts directory', cls: 'legislation' },
  { id: 'places', title: 'Places', words: 'places locations sites bases directory', cls: 'location' },
  { id: 'events', title: 'Events', words: 'events incidents directory', cls: 'event' },
];
/* The people directory by role: the facet word and its plural. */
const ROLE_PLURAL: Record<string, string> = {
  official: 'officials', military: 'military', intelligence: 'intelligence officers', scientist: 'scientists',
  contractor: 'contractors', legislator: 'legislators', witness: 'witnesses', claimant: 'claimants',
  researcher: 'researchers', journalist: 'journalists', media: 'media', counsel: 'counsel lawyers',
};

export async function primeSearch(): Promise<void> {
  const idx = await loadIndex();
  nodes = idx.nodes;
}

/* Punctuation to spaces, so "wilson davis" reaches "The Wilson-Davis Notes" and
   "10 usc 119" reaches "10 U.S.C. 119". A reader types words, not hyphens. */
const flatten = (s: string): string =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').replace(/^ | $/g, '');

/* Punctuation REMOVED rather than spaced, so "usc" reaches "U.S.C.". Flattening
   alone turns that abbreviation into "u s c" and the two never meet. Only used
   for queries of five characters or more once squashed, so a short query cannot
   start matching across word boundaries -- "a b" must not find "lab". */
const squash = (s: string): string => s.toLowerCase().replace(/[^a-z0-9]+/g, '');

const termsOf = (q: string): string[] => flatten(q).split(' ').filter((t) => t.length > 1);

function askAll(rerun: () => void): void {
  if (asked) return;
  asked = true;
  claimsState = 'loading';
  loadClaims().then(
    (rows) => {
      claims = rows;
      claimLc = rows.map((r) => r.text.toLowerCase());
      claimFlat = rows.map((r) => flatten(r.text + ' ' + r.label));
      claimSquash = rows.map((r) => squash(r.text + ' ' + r.label));
      claimsState = 'ready';
      rerun();
    },
    () => { claimsState = 'absent'; rerun(); },
  );
  loadTimeline().then(
    (rows) => {
      /* a same-day repeat is shown once, under the event it repeats */
      events = rows.filter((e) => !e.sameAs);
      eventFlat = events.map((e) => flatten(e.label + ' ' + (e.text || '')));
      rerun();
    },
    () => { events = []; },
  );
  loadThreads().then((f) => { threads = f.threads; rerun(); }, () => { threads = []; });
  loadTopics().then((f) => { topics = f.topics; rerun(); }, () => { topics = []; });
  /* phase 10's questions, /data/questions.json */
  loadQuestions().then((f) => { questions = f.questions; rerun(); }, () => { questions = []; });
  loadFacets().then((f) => {
    roleCounts = {};
    for (const p of Object.values(f.people)) for (const r of p.roles) roleCounts[r] = (roleCounts[r] || 0) + 1;
    rerun();
  }, () => { roleCounts = {}; });
  /* phase 8's Library, /data/sources.json */
  loadSourcesIfAny().then((rows) => { sources = rows; if (rows.length) rerun(); });
}

/* The name rank, 0 to 5, or -1. `id` may be empty for things without one. */
function nameScore(label: string, alt: string, id: string, q: string, flat: string, terms: string[]): number {
  const l = label.toLowerCase(), a = alt.toLowerCase();
  if (id && id === q) return 0;
  if (l === q || (a && a === q)) return 1;
  if (l.startsWith(q) || (a && a.startsWith(q))) return 2;
  if (id && id.includes(q)) return 3;
  if (l.includes(q) || (a && a.includes(q))) return 4;
  if (terms.length) {
    const hay = flatten(label + ' ' + alt + ' ' + id);
    if (flat && hay.includes(flat)) return 4;
    if (terms.length > 1 && terms.every((t) => hay.includes(t))) return 5;
  }
  return -1;
}

/* Claim ranking, unchanged in substance since 12 September 2026. Before then
   this was `filter(...).slice(0, 12)`, which took the first twelve in file
   order -- alphabetical by node id. Lower is better:

     the whole phrase present beats the words merely all being present
     Tier 1 beats Tier 2 beats Tier 3, because that is what the board is for
     an early match beats a late one, so the hit line has something to show
     a claim whose node is also a name match beats one whose node is not
*/
function claimScore(i: number, phrase: string, terms: string[], sq: string,
                    nodeHit: Set<string>, c: ClaimRow): number {
  const lc = claimLc[i], flat = claimFlat[i];
  let s: number;
  const at = lc.indexOf(phrase);
  if (at >= 0) s = 0;
  else if (flat.includes(phrase)) s = 4;
  else if (sq && claimSquash[i].includes(sq)) s = 5;
  else if (terms.every((t) => flat.includes(t))) s = 8;
  else return -1;
  /* TIER STRICTLY DOMINATES, and the two adjustments below are bounded so that
     it cannot be outweighed. Position is capped at 0.5 and the node bonus is
     0.25, so within one match route the worst Tier 1 claim (tier 1 + 0.5)
     still scores better than the best Tier 2 one (tier 2 - 0.25). */
  s += c.tier;
  s += Math.min(0.5, (at >= 0 ? at : 500) / 1000);
  if (nodeHit.has(c.node)) s -= 0.25;
  return s;
}

/* The excerpt, centred on the first thing the reader actually typed that is in
   this text. With a multi-word query the whole phrase is often not present, so
   fall back to the earliest single term. */
function hitLine(text: string, q: string, terms: string[]): HTMLElement {
  const lc = text.toLowerCase();
  let i = lc.indexOf(q), len = q.length;
  if (i < 0) {
    i = -1;
    for (const t of terms) {
      const at = lc.indexOf(t);
      if (at >= 0 && (i < 0 || at < i)) { i = at; len = t.length; }
    }
  }
  const span = h('span', { class: 'hit' });
  if (i < 0) { span.append(text.slice(0, 150)); return span; }
  const from = Math.max(0, i - 46);
  span.append(
    (from > 0 ? '…' : '') + text.slice(from, i),
    h('mark', null, text.slice(i, i + len)),
    text.slice(i + len, i + len + 90) + (text.length > i + len + 90 ? '…' : ''),
  );
  return span;
}

/* One row of the merged list. `kind` orders ties and names the badge. */
interface Hit { s: number; kind: number; tie: number; el: HTMLElement; }
const KIND = { directory: 0, topic: 1, question: 2, node: 3, thread: 4, source: 5, event: 6, claim: 7 };

function badge(text: string, colour: string | null): HTMLElement {
  return h('span', { class: 'badge' }, colour ? mark(colour) : null, colour ? ' ' : null, text);
}

function render(panel: HTMLElement, raw: string, rerun: () => void): void {
  clear(panel);
  const q = raw.trim().toLowerCase();
  if (q.length < 2) { panel.hidden = true; return; }
  panel.hidden = false;
  const flat = flatten(q);
  const terms = termsOf(q);
  askAll(rerun);

  const hits: Hit[] = [];
  const tally: Record<string, number> = {};
  const count = (t: string, n: number) => { if (n) tally[t] = (tally[t] || 0) + n; };

  /* directories, and the people directory by role */
  let nd = 0;
  for (const d of DIRS) {
    const a = nameScore(d.title, '', d.id, q, flat, terms);
    const b = nameScore(d.words, '', '', q, flat, terms);
    const s = a < 0 ? (b < 0 ? -1 : Math.max(b, 2)) : a;
    if (s < 0) continue;
    nd++;
    const n = nodes.filter((x) => x.cls === d.cls).length;
    hits.push({ s, kind: KIND.directory, tie: 0, el: h('a', { class: 'res dir', href: '#/' + d.id, 'data-type': 'directory' },
      badge('DIRECTORY', null), h('span', { class: 'label' }, d.title), h('span', { class: 'meta' }, n + ' on the board')) });
  }
  for (const r of Object.keys(roleCounts).sort()) {
    const s = nameScore(r, ROLE_PLURAL[r] || '', '', q, flat, terms);
    if (s < 0) continue;
    nd++;
    hits.push({ s, kind: KIND.directory, tie: 1, el: h('a', {
      class: 'res dir', href: '#/people?' + (r === 'claimant' ? 'claimant=yes' : 'role=' + r), 'data-type': 'directory',
    }, badge('DIRECTORY', null), h('span', { class: 'label' }, 'People: ' + r), h('span', { class: 'meta' }, roleCounts[r] + ' people')) });
  }
  count('directory', nd);

  /* topics */
  if (topics) {
    let n = 0;
    for (const t of topics) {
      const s = nameScore(t.title, '', t.id, q, flat, terms);
      if (s < 0) continue;
      n++;
      hits.push({ s, kind: KIND.topic, tie: -t.counts.members, el: h('a', { class: 'res topic', href: '#/topic/' + t.id, 'data-type': 'topic' },
        badge('TOPIC', null), h('span', { class: 'label' }, t.title), h('span', { class: 'meta' }, t.researchGap ? 'a research gap' : t.counts.members + ' members')) });
    }
    count('topic', n);
  }

  /* the big questions (phase 10): matched on the title; a match in the lead
     ranks as a word match, as a thread's blurb does */
  if (questions) {
    let n = 0;
    for (const x of questions) {
      let s = nameScore(x.title, '', x.id, q, flat, terms);
      if (s < 0) {
        const hay = flatten(x.lead || '');
        if ((flat && hay.includes(flat)) || (terms.length && terms.every((w) => hay.includes(w)))) s = 5;
      }
      if (s < 0) continue;
      n++;
      hits.push({ s, kind: KIND.question, tie: x.order, el: h('a', { class: 'res question', href: '#/q/' + x.id, 'data-type': 'question' },
        badge('QUESTION', null), h('span', { class: 'label' }, x.title), h('span', { class: 'meta' }, 'a big question')) });
    }
    count('question', n);
  }

  /* nodes */
  const scored: { n: IndexNode; s: number }[] = [];
  for (const n of nodes) {
    const s = nameScore(n.label, n.short || '', n.id, q, flat, terms);
    if (s >= 0) scored.push({ n, s });
  }
  scored.sort((a, b) => a.s - b.s || b.n.deg - a.n.deg || a.n.label.localeCompare(b.n.label));
  const top = scored.slice(0, MAX_NODE_HITS);
  count('node', scored.length);
  for (const { n, s } of top) {
    hits.push({ s, kind: KIND.node, tie: -n.deg, el: h('a', { class: 'res node', href: '#/n/' + n.id, 'data-type': 'node' },
      badge(n.cls.toUpperCase(), clsColour(n.cls)),
      h('span', { class: 'label' }, n.label),
      h('span', { class: 'meta' }, (n.dateStart || 'no date') + ' · ' + (n.claims[0] + n.claims[1] + n.claims[2]) + ' claims')) });
  }

  /* threads: the eight authored chains; a match in the blurb ranks as a word match */
  if (threads) {
    let n = 0;
    for (const t of threads) {
      let s = nameScore(t.title || t.label, t.label, t.id, q, flat, terms);
      if (s < 0) {
        const hay = flatten(t.blurb || '');
        if ((flat && hay.includes(flat)) || (terms.length && terms.every((w) => hay.includes(w)))) s = 5;
      }
      if (s < 0) continue;
      n++;
      hits.push({ s, kind: KIND.thread, tie: 0, el: h('a', { class: 'res thread', href: '#/t/' + t.id, 'data-type': 'thread' },
        badge('THREAD', null), h('span', { class: 'label' }, t.title || t.label), h('span', { class: 'meta' }, t.steps.length + ' steps')) });
    }
    count('thread', n);
  }

  /* sources, from phase 8's Library: matched on the title, the identifiers
     (a report or bill number) and the id; each row opens its source page */
  if (sources && sources.length) {
    let n = 0;
    for (const r of sources) {
      const title = r.title || r.id;
      const s = nameScore(title, (r.identifiers || []).join(' '), r.id, q, flat, terms);
      if (s < 0) continue;
      if (++n > MAX_NODE_HITS) continue;
      hits.push({ s, kind: KIND.source, tie: 0, el: h('a', { class: 'res source', href: '#/s/' + r.id, 'data-type': 'source' },
        badge('SOURCE', null), h('span', { class: 'label' }, title), h('span', { class: 'meta' }, r.type || '')) });
    }
    count('source', n);
  }

  /* timeline events: a label match ranks as a name, a text match after every name */
  if (events && terms.length) {
    const ev: { e: TimelineEvent; s: number }[] = [];
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      let s = nameScore(e.label || '', '', '', q, flat, terms);
      if (s < 0 && terms.every((w) => eventFlat[i].includes(w))) s = 6;
      if (s >= 0) ev.push({ e, s });
    }
    ev.sort((a, b) => a.s - b.s || String(a.e.date).localeCompare(String(b.e.date)));
    count('event', ev.length);
    for (const { e, s } of ev.slice(0, MAX_EVENT_HITS)) {
      hits.push({ s, kind: KIND.event, tie: 0, el: h('a', {
        class: 'res event', 'data-type': 'event',
        href: e.node ? '#/n/' + e.node : '#/timeline?era=' + (e.era || ''),
      }, badge('EVENT', null), h('span', { class: 'label' }, e.label), h('span', { class: 'meta' }, String(e.date).slice(0, 10))) });
    }
  }

  /* claims */
  if (claims) {
    const sq = squash(q);
    const sqq = sq.length >= 5 ? sq : '';
    const nodeHit = new Set(top.map((t) => t.n.id));
    const chits: { c: ClaimRow; s: number }[] = [];
    for (let i = 0; i < claims.length; i++) {
      const s = claimScore(i, q, terms, sqq, nodeHit, claims[i]);
      if (s >= 0) chits.push({ c: claims[i], s });
    }
    chits.sort((a, b) => a.s - b.s || a.c.tier - b.c.tier || a.c.node.localeCompare(b.c.node));
    count('claim', chits.length);
    for (const { c, s } of chits.slice(0, MAX_CLAIM_HITS)) {
      hits.push({ s: 7 + s / 100, kind: KIND.claim, tie: 0, el: h('a', {
        class: 'res claim', href: '#/n/' + c.node, 'data-tier': String(c.tier), 'data-cid': c.id || null, 'data-type': 'claim',
      },
        badge('CLAIM', clsColour(c.cls)),
        h('span', { class: 'label' }, c.label),
        h('span', { class: 'meta t' + c.tier }, 'T' + c.tier,
          saidMark(saidKind(c.tier, c.text, c.source ? c.source.text : '', c.source ? c.source.url : null))),
        hitLine(c.text, q, terms)) });
    }
  }

  hits.sort((a, b) => a.s - b.s || a.kind - b.kind || a.tie - b.tie);

  /* the one line over the list: what matched, by kind */
  const WORD: [string, string, string][] = [
    ['directory', 'directory', 'directories'], ['topic', 'topic', 'topics'], ['question', 'question', 'questions'],
    ['node', 'node', 'nodes'],
    ['thread', 'thread', 'threads'], ['source', 'source', 'sources'], ['event', 'event', 'events'], ['claim', 'claim', 'claims'],
  ];
  const parts = WORD.filter(([k]) => tally[k]).map(([k, one, many]) => tally[k] + ' ' + (tally[k] === 1 ? one : many));
  panel.append(h('div', { class: 'res-head' },
    parts.length ? parts.join(' · ') + ' match “' + raw.trim() + '”'
      : 'nothing on the board matches “' + raw.trim() + '”'));
  const capped: string[] = [];
  if ((tally.node || 0) > MAX_NODE_HITS) capped.push('the first ' + MAX_NODE_HITS + ' nodes');
  if ((tally.event || 0) > MAX_EVENT_HITS) capped.push('the earliest ' + MAX_EVENT_HITS + ' events');
  if ((tally.claim || 0) > MAX_CLAIM_HITS) capped.push('the strongest ' + MAX_CLAIM_HITS + ' claims, Tier 1 first');
  if (capped.length) panel.append(h('div', { class: 'res-sub' }, 'listed: ' + capped.join(', ')));
  hits.forEach((x, i) => {
    x.el.setAttribute('role', 'option');
    x.el.setAttribute('id', panel.id + '-o' + i);
    x.el.setAttribute('aria-selected', 'false');
    panel.append(x.el);
  });
  if (claimsState === 'loading') {
    panel.append(h('div', { class: 'res-empty' }, 'loading claim text, events and topics…'));
  } else if (claimsState === 'absent') {
    panel.append(h('div', { class: 'res-empty' },
      'claims.json is not served on this deployment, so this search does not cover claim text'));
  }
}

let boxes = 0;

export function searchBox(opts: { big?: boolean; placeholder: string }): HTMLElement {
  const pid = 'res-' + (++boxes);
  const input = h('input', {
    type: 'search',
    autocomplete: 'off',
    spellcheck: 'false',
    role: 'combobox',
    'aria-label': 'Search the board',
    'aria-controls': pid,
    'aria-expanded': 'false',
    'aria-autocomplete': 'list',
    placeholder: opts.placeholder,
  });
  const panel = h('div', { class: 'results', hidden: 'hidden', role: 'listbox', id: pid });
  const box = h('div', { class: 'searchbox' + (opts.big ? ' big' : '') },
    h('span', { class: 'glass', 'aria-hidden': 'true' }, '⌕'),
    input,
    opts.big ? h('span', { class: 'slash' }, '/') : null,
    panel,
  );
  let at = -1;
  const rows = (): HTMLElement[] => Array.prototype.slice.call(panel.querySelectorAll('a.res'));
  const markAt = (i: number): void => {
    const rs = rows();
    if (!rs.length) { at = -1; input.removeAttribute('aria-activedescendant'); return; }
    at = Math.max(0, Math.min(rs.length - 1, i));
    rs.forEach((r, k) => { r.setAttribute('aria-selected', k === at ? 'true' : 'false'); r.classList.toggle('active', k === at); });
    input.setAttribute('aria-activedescendant', rs[at].id);
    rs[at].scrollIntoView({ block: 'nearest' });
  };
  const rerun = () => {
    /* keep the marked row across a re-render (data arriving) while it is still there */
    const was = at >= 0 ? (rows()[at] || null) : null;
    const href = was ? was.getAttribute('href') : null;
    render(panel, input.value, rerun);
    input.setAttribute('aria-expanded', panel.hidden ? 'false' : 'true');
    at = -1;
    input.removeAttribute('aria-activedescendant');
    if (href) {
      const k = rows().findIndex((r) => r.getAttribute('href') === href);
      if (k >= 0) markAt(k);
    }
  };
  input.addEventListener('input', () => { at = -1; rerun(); });
  input.addEventListener('focus', rerun);
  input.addEventListener('keydown', (e) => {
    const k = (e as KeyboardEvent).key;
    if (k === 'Escape') {
      input.value = ''; panel.hidden = true; at = -1;
      input.setAttribute('aria-expanded', 'false'); input.blur();
    } else if (k === 'ArrowDown') {
      e.preventDefault();
      if (panel.hidden) rerun();
      markAt(at + 1);
    } else if (k === 'ArrowUp') {
      e.preventDefault();
      markAt(at <= 0 ? 0 : at - 1);
    } else if (k === 'Enter') {
      const rs = rows();
      const r = at >= 0 ? rs[at] : rs[0];
      if (r) {
        e.preventDefault();
        panel.hidden = true;
        input.setAttribute('aria-expanded', 'false');
        location.hash = (r.getAttribute('href') || '#/').replace(/^#/, '');
      }
    }
  });
  document.addEventListener('click', (e) => {
    if (!box.contains(e.target as Node)) { panel.hidden = true; input.setAttribute('aria-expanded', 'false'); }
  });
  return box;
}
