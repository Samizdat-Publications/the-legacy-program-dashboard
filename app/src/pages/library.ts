/* The Library: every source the board cites (redesign phase 8, task 4).
 *
 *   #/library   ?type=&issuer=&era=&ip=1|0&q=&sort=claims|title|date
 *
 * One row per source in research/_sources.json, as app/public/data/sources.json
 * ships it: its title (a link to #/s/<id>), its type, who issued it, its date,
 * how many claims and links cite it, and whether it is an interested party's.
 * Four facets (type, issuer, era, interested party) and a search over title,
 * issuer and identifiers. Every filter is in the URL, so a filtered Library is
 * shareable. A facet's counts are the rows the OTHER filters leave, so a count
 * always says what choosing that value would show.
 *
 * Nothing is truncated: titles wrap. app/checks/run.mjs C42 re-derives the rows
 * and the counts from sources.json.
 */
import '../styles/library.css';
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadLibrary, type LibraryRow, type Era } from '../data';
import { TYPE_LABEL } from '../sources';

type Key = 'type' | 'issuer' | 'era' | 'ip';
const KEYS: Key[] = ['type', 'issuer', 'era', 'ip'];
const PAGE = 100;
const ISSUERS_SHOWN = 12;

const fmt = (n: number): string => n.toLocaleString('en-GB');

function value(r: LibraryRow, k: Key): string {
  if (k === 'type') return r.type;
  if (k === 'issuer') return r.issuer || '-';
  if (k === 'era') return r.era;
  return r.interestedParty ? '1' : '0';
}

function matches(r: LibraryRow, f: Record<Key, string>, q: string, skip: Key | null): boolean {
  for (const k of KEYS) {
    if (k === skip || !f[k]) continue;
    if (value(r, k) !== f[k]) return false;
  }
  if (q) {
    const hay = (r.title + ' ' + (r.issuer || '') + ' ' + r.identifiers.join(' ') + ' ' + r.id).toLowerCase();
    for (const w of q.toLowerCase().split(/\s+/).filter(Boolean)) if (!hay.includes(w)) return false;
  }
  return true;
}

function href(q: URLSearchParams, set: Record<string, string | null>): string {
  const n = new URLSearchParams(q);
  for (const [k, v] of Object.entries(set)) {
    if (v == null || v === '') n.delete(k); else n.set(k, v);
  }
  const s = n.toString();
  return '#/library' + (s ? '?' + s : '');
}

export async function renderLibrary(view: HTMLElement, q: URLSearchParams): Promise<void> {
  setTitle('Library');
  clear(view);
  const [lib, idx] = await Promise.all([loadLibrary(), loadIndex()]);
  const eras: Record<string, Era> = Object.fromEntries(idx.eras.map((e) => [e.id, e]));
  const f: Record<Key, string> = { type: q.get('type') || '', issuer: q.get('issuer') || '', era: q.get('era') || '', ip: q.get('ip') || '' };
  const search = (q.get('q') || '').trim();
  const sort = q.get('sort') || 'claims';

  const root = h('div', { class: 'lib' });
  view.append(root);
  const share = lib.claims.total ? Math.round((1000 * lib.claims.resolved) / lib.claims.total) / 10 : 0;
  root.append(h('div', { class: 'lib-top' },
    h('h1', { class: 'lib-h1' }, 'Library'),
    h('p', { class: 'lib-intro' },
      'Every source the board cites: ' + fmt(lib.count) + ' documents, hearing records, statutes, reports, ' +
      'articles and pages, each with its own page listing every claim and link that rests on it. ' +
      fmt(lib.claims.resolved) + ' of the board\'s ' + fmt(lib.claims.total) + ' claims (' + share + '%) link ' +
      'to their source here; the rest keep their citation exactly as written, and say so.'),
    h('p', { class: 'lib-intro dim' },
      'A source marked "interested party" was issued by AARO, the office the board investigates, or is on file ' +
      'only from the Defense Department\'s own public sites (aaro.mil, defense.gov, war.gov): it is a record of ' +
      'what the office said, not proof of what it says. Other defence and intelligence records (a directive, a ' +
      'DIA letter) are not marked: the board reads them as primary records.'),
  ));

  /* ---- search and sort --------------------------------------------------- */
  const input = h('input', {
    type: 'search', class: 'lib-q', value: search, placeholder: 'search titles, issuers, identifiers',
    'aria-label': 'Search the Library',
  }) as HTMLInputElement;
  const go = () => { location.hash = href(q, { q: input.value.trim() || null }); };
  input.addEventListener('keydown', (e) => { if ((e as KeyboardEvent).key === 'Enter') go(); });
  const sorts = h('span', { class: 'lib-sorts' }, h('span', { class: 'dim' }, 'order: '),
    ...(['claims', 'title', 'date'] as const).map((s) => h('a', {
      class: 'lib-sort' + (sort === s ? ' on' : ''), href: href(q, { sort: s === 'claims' ? null : s }),
      'aria-pressed': sort === s ? 'true' : 'false',
    }, s === 'claims' ? 'most cited' : s)));
  root.append(h('div', { class: 'lib-bar' },
    h('span', { class: 'lib-qwrap' }, input, h('button', { type: 'button', class: 'lib-go', onclick: go }, 'search')),
    sorts));

  /* ---- facets ------------------------------------------------------------ */
  const facets = h('div', { class: 'lib-facets' });
  const label: Record<Key, string> = { type: 'Type', issuer: 'Issuer', era: 'Era', ip: 'Interested party' };
  const name = (k: Key, v: string): string => {
    if (k === 'type') return TYPE_LABEL[v] || v;
    if (k === 'era') return eras[v] ? eras[v].label.toLowerCase() : v;
    if (k === 'ip') return v === '1' ? 'interested party' : 'not an interested party';
    return v === '-' ? 'issuer not recorded' : v;
  };
  for (const k of KEYS) {
    const counts = new Map<string, number>();
    for (const r of lib.sources) {
      if (!matches(r, f, search, k)) continue;
      const v = value(r, k);
      counts.set(v, (counts.get(v) || 0) + 1);
    }
    let vals = Array.from(counts.entries());
    if (k === 'era') vals.sort((a, b) => (a[0] === 'nd' ? 1 : 0) - (b[0] === 'nd' ? 1 : 0) || a[0].localeCompare(b[0]));
    else if (k === 'ip') vals.sort((a, b) => b[0].localeCompare(a[0]));
    else vals.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    /* the chosen value always shows, even when the other filters leave it none */
    if (f[k] && !counts.has(f[k])) vals.unshift([f[k], 0]);
    const chip = ([v, n]: [string, number]) => {
      const on = f[k] === v;
      return h('a', {
        class: 'lib-chip' + (on ? ' on' : ''), href: href(q, { [k]: on ? null : v }),
        'data-value': v, 'data-n': String(n), 'aria-pressed': on ? 'true' : 'false',
      }, h('span', { class: 'lib-chip-l' }, name(k, v)), h('span', { class: 'lib-chip-n' }, fmt(n)));
    };
    const box = h('div', { class: 'lib-facet', 'data-facet': k },
      h('span', { class: 'eyebrow lib-facet-h' }, label[k]));
    const chips = h('div', { class: 'lib-chips' });
    if (k === 'issuer' && vals.length > ISSUERS_SHOWN) {
      const head = vals.slice(0, ISSUERS_SHOWN);
      if (f.issuer && !head.some(([v]) => v === f.issuer)) head.push(vals.find(([v]) => v === f.issuer)!);
      chips.append(...head.map(chip));
      const rest = vals.filter((x) => !head.includes(x));
      const more = h('details', { class: 'lib-more' },
        h('summary', { class: 'lib-more-s' }, 'all ' + fmt(vals.length) + ' issuers'),
        h('div', { class: 'lib-chips' }, ...rest.map(chip)));
      box.append(chips, more);
    } else {
      chips.append(...vals.map(chip));
      box.append(chips);
    }
    facets.append(box);
  }
  root.append(facets);

  /* ---- rows -------------------------------------------------------------- */
  const rows = lib.sources.filter((r) => matches(r, f, search, null));
  const byTitle = (a: LibraryRow, b: LibraryRow) => a.title.localeCompare(b.title, 'en', { sensitivity: 'base' });
  if (sort === 'title') rows.sort(byTitle);
  else if (sort === 'date') rows.sort((a, b) => (b.date || '').localeCompare(a.date || '') || byTitle(a, b));
  else rows.sort((a, b) => (b.claims + b.edges) - (a.claims + a.edges) || byTitle(a, b));

  const active = KEYS.filter((k) => f[k]).map((k) => name(k, f[k]));
  if (search) active.push('"' + search + '"');
  const count = h('div', { class: 'lib-count', 'data-n': String(rows.length) },
    h('b', null, fmt(rows.length)), ' of ' + fmt(lib.count) + ' sources',
    active.length ? h('span', { class: 'dim' }, ' · ' + active.join(' · ') + ' · ') : null,
    active.length ? h('a', { href: '#/library' + (sort !== 'claims' ? '?sort=' + sort : '') }, 'clear filters') : null);
  root.append(count);

  const list = h('ol', { class: 'lib-list' });
  root.append(list);
  const foot = h('div', { class: 'lib-foot' });
  root.append(foot);
  let shown = 0;
  const draw = () => {
    const end = Math.min(rows.length, shown + PAGE);
    for (let i = shown; i < end; i++) list.append(row(rows[i], eras));
    shown = end;
    clear(foot);
    if (shown < rows.length) {
      foot.append(h('button', {
        type: 'button', class: 'lib-next', onclick: draw,
      }, 'show ' + fmt(Math.min(PAGE, rows.length - shown)) + ' more (' + fmt(shown) + ' of ' + fmt(rows.length) + ' shown)'));
    } else if (!rows.length) {
      foot.append(h('p', { class: 'dim' }, 'No source matches these filters.'));
    }
  };
  draw();
}

function row(r: LibraryRow, eras: Record<string, Era>): HTMLElement {
  const bits: (string | HTMLElement)[] = [];
  const sep = () => h('span', { class: 'sep' }, ' · ');
  bits.push(h('span', { class: 'lib-type' }, TYPE_LABEL[r.type] || r.type));
  if (r.issuer) bits.push(sep(), h('span', null, r.issuer));
  else if (r.host) bits.push(sep(), h('span', { class: 'dim' }, 'issuer not recorded; copy hosted by ' + r.host));
  bits.push(sep(), h('span', null, r.date || 'undated'));
  if (!r.date && eras[r.era] && r.era !== 'nd') bits.push(h('span', { class: 'dim' }, ' (' + eras[r.era].label.toLowerCase() + ')'));
  bits.push(sep(), h('span', { class: 'lib-n' }, fmt(r.claims) + (r.claims === 1 ? ' claim' : ' claims')));
  if (r.edges) bits.push(sep(), h('span', { class: 'lib-n' }, fmt(r.edges) + (r.edges === 1 ? ' link' : ' links')));
  if (!r.urls && !r.archived) bits.push(sep(), h('span', { class: 'dim' }, 'no web address on file'));
  return h('li', { class: 'lib-row', 'data-sid': r.id },
    h('a', { class: 'lib-title', href: '#/s/' + r.id }, r.title),
    r.interestedParty ? h('span', { class: 'ip-mark', title: 'Issued by AARO, or on file only from aaro.mil, defense.gov or war.gov: a record of what the office said, not proof of what it says.' }, 'interested party') : null,
    h('div', { class: 'lib-meta' }, ...bits,
      r.identifiers.length ? h('span', { class: 'dim' }, ' · ' + r.identifiers.join(', ')) : null));
}
