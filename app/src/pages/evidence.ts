/* The evidence explorer: Design response section 1.9, route
 * #/evidence?tier=&cls=&cluster=&domain=&denied=1&open=1.
 *
 * Left: a rail of filter chips with the real count behind each one, every chip
 * toggling one of the six parameters. Right: the table (tier, class, node, claim,
 * source, denied, FOIA), with the request beside the question it would close.
 *
 * All 5,120 rows are held in memory and filtered there; the table renders in
 * blocks so a filter that matches thousands of rows still paints at once. The
 * header prints the filtered count.
 *
 * Nothing is truncated: claim text, source citations and FOIA questions wrap.
 *
 * The FOIA column prints one line per request (id, office, status) and the
 * question that request would close opens as a full-width expansion under the
 * row, one row open at a time. Every fact stays; it moves out of the row and
 * under it, so the table reads one claim per two or three lines.
 */
import '../styles/evidence.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadClaims, loadNode, clsColour, type ClaimRow, type NodeRecord } from '../data';
import {
  loadFoia, readFilters, filterRows, facets, chipHref, clearHref, activeCount, fmt,
  NO_DOMAIN, KEYS, type Filters, type Facet, type Key, type FoiaFile, type FoiaEntry,
} from '../evidence/model';

const BLOCK = 60;

const GROUPS: { key: Key; head: string }[] = [
  { key: 'tier', head: 'Tier' },
  { key: 'cls', head: 'Class' },
  { key: 'cluster', head: 'Cluster' },
  { key: 'domain', head: 'Source domain' },
  { key: 'denied', head: 'Node denied' },
  { key: 'open', head: 'Open question' },
];

export async function renderEvidence(view: HTMLElement, q: URLSearchParams): Promise<void> {
  clear(view);
  setTitle('Evidence');
  open = null;   /* the previous table is gone; nothing is expanded in this one */

  const wait = h('div', { class: 'ev-wait dim' }, 'Reading data/claims.json …');
  view.append(wait);

  let rows: ClaimRow[];
  let foia: FoiaFile;
  try {
    [rows, foia] = await Promise.all([loadClaims(), loadFoia()]);
  } catch (e) {
    clear(view);
    view.append(h('section', { class: 'notice' },
      h('h2', null, 'The evidence rows are not being served'),
      h('p', null, (e as Error).message)));
    return;
  }
  clear(view);

  const f = readFilters(q);
  const shown = filterRows(rows, f);
  const fac = facets(rows);

  const wrap = h('div', { class: 'ev' });
  const rail = h('aside', { class: 'ev-rail' });
  const main = h('div', { class: 'ev-main' });
  wrap.append(rail, main);
  view.append(wrap);

  /* ---- the rail --------------------------------------------------------- */
  rail.append(h('div', { class: 'eyebrow' }, 'Evidence explorer'));
  rail.append(h('div', { class: 'ev-railcount' },
    h('b', null, fmt(rows.length)), ' claims on the board'));
  rail.append(h('p', { class: 'ev-note faint' },
    'Every count below is the number of claims in the whole file, not in the current ' +
    'filter. The header above the table carries the filtered count.'));
  if (activeCount(f)) {
    rail.append(h('a', { class: 'ev-clear', href: clearHref() },
      'clear ' + activeCount(f) + ' filter' + (activeCount(f) === 1 ? '' : 's')));
  }

  for (const g of GROUPS) {
    rail.append(h('div', { class: 'ev-ghead eyebrow' }, g.head));
    const box = h('div', { class: 'ev-chips' + (g.key === 'domain' ? ' scroll' : '') });
    for (const item of fac[g.key]) box.append(chip(q, g.key, item, f));
    rail.append(box);
  }

  /* ---- the header ------------------------------------------------------- */
  const head = h('div', { class: 'ev-head' },
    h('span', { class: 'eyebrow' }, 'Claims shown'),
    h('span', { class: 'ev-count' }, fmt(shown.length)),
    h('span', { class: 'dim' }, 'of ' + fmt(rows.length)),
  );
  const active: string[] = [];
  for (const k of KEYS) if (f[k] != null) active.push(k + ' = ' + f[k]);
  if (active.length) head.append(h('span', { class: 'ev-active amber' }, active.join('  ·  ')));
  main.append(head);

  if (!shown.length) {
    main.append(h('p', { class: 'ev-note dim' },
      'No claim on the board matches every one of those filters.'));
    return;
  }

  /* ---- the table -------------------------------------------------------- */
  const table = h('table', { class: 'ev-table' });
  const thead = h('thead', null, h('tr', null,
    h('th', { class: 'c-tier' }, 'TIER'),
    h('th', { class: 'c-cls' }, 'CLASS'),
    h('th', { class: 'c-node' }, 'NODE'),
    h('th', { class: 'c-claim' }, 'CLAIM'),
    h('th', { class: 'c-src' }, 'SOURCE'),
    h('th', { class: 'c-den' }, 'NODE DENIED'),
    h('th', { class: 'c-foia' }, 'FOIA')));
  const tbody = h('tbody');
  table.append(thead, tbody);
  main.append(table);

  const foot = h('div', { class: 'ev-foot' });
  const footN = h('span', { class: 'dim' });
  const more = h('button', { class: 'ev-more', type: 'button' }, 'SHOW MORE');
  foot.append(footN, more);
  main.append(foot);

  let at = 0;
  const draw = (): void => {
    const end = Math.min(at + BLOCK, shown.length);
    for (; at < end; at++) tbody.append(row(shown[at], foia));
    footN.textContent = 'showing ' + fmt(at) + ' of ' + fmt(shown.length) + ' rows';
    if (at >= shown.length) {
      more.remove();
      if (io) io.disconnect();
    }
  };
  more.addEventListener('click', draw);

  /* The rows keep coming as the reader reaches the foot, so no filter ever
     paints five thousand rows at once. */
  let io: IntersectionObserver | null = null;
  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) draw();
    }, { rootMargin: '600px' });
    io.observe(foot);
  }
  draw();
}

function chip(q: URLSearchParams, key: Key, item: Facet, f: Filters): HTMLElement {
  const on = f[key] === item.value;
  const label = key === 'domain' && item.value === NO_DOMAIN
    ? 'no url in the source'
    : (item.label || 'no cluster');
  return h('a', {
    class: 'ev-chip' + (on ? ' on' : ''),
    href: chipHref(q, key, item.value, on),
    'aria-pressed': on ? 'true' : 'false',
  },
    h('span', { class: 'ev-chip-l' }, label),
    h('span', { class: 'ev-chip-n' }, fmt(item.n)));
}

function row(r: ClaimRow, foia: FoiaFile): HTMLElement {
  const tr = h('tr') as HTMLTableRowElement;
  tr.append(h('td', { class: 'c-tier t' + r.tier }, 'T' + r.tier));
  tr.append(h('td', { class: 'c-cls' }, mark(clsColour(r.cls)), ' ', h('span', { class: 'dim' }, r.cls)));
  tr.append(h('td', { class: 'c-node' }, h('a', { href: '#/n/' + r.node }, r.label)));
  tr.append(h('td', { class: 'c-claim' }, r.text));

  const src = r.source || { text: '', url: null };
  tr.append(h('td', { class: 'c-src' },
    src.url
      ? h('a', { href: src.url, rel: 'noreferrer', target: '_blank' }, src.text || src.url)
      : (src.text
          ? h('span', { class: 'dim' }, src.text)
          : h('span', { class: 'faint' }, 'no citation on the row'))));

  tr.append(h('td', { class: 'c-den' }, r.denied
    /* the flag is the node's (it is the object of some denial), never this claim's */
    ? h('span', { class: 'dim', title: 'a denial is on record for this node; it is not a denial of this claim' }, 'on the node')
    : ''));
  tr.append(foiaCell(r, foia, tr));
  return tr;
}

/* One row is expanded at a time. The state is module-level because the rows are
   drawn in blocks and any of them may be the open one; renderEvidence drops it
   on every paint, so a stale reference can never outlive the table it came from. */
let open: { tr: HTMLTableRowElement; x: HTMLTableRowElement; btn: HTMLElement } | null = null;

function closeOpen(): void {
  if (!open) return;
  open.x.remove();
  open.btn.setAttribute('aria-expanded', 'false');
  open.tr.classList.remove('ev-open');
  open = null;
}

/* The cell carries the request and the office on one line each. The question the
   request would close is a fact about the request, not about the claim, so it
   opens under the row rather than printing three hundred pixels of prose into it. */
function foiaCell(r: ClaimRow, foia: FoiaFile, tr: HTMLTableRowElement): HTMLElement {
  const td = h('td', { class: 'c-foia' });
  const entries: FoiaEntry[] = (foia.byNode && foia.byNode[r.node]) || [];
  if (!entries.length) {
    td.append(h('span', { class: 'faint' }, r.open ? 'request not on the board' : ''));
    return td;
  }

  const btn = h('button', {
    class: 'ev-foia-btn',
    type: 'button',
    'aria-expanded': 'false',
    title: 'Show the question this would close',
  });
  for (const e of entries) {
    btn.append(h('span', { class: 'ev-foia-line' },
      h('span', { class: 'amber' }, e.request),
      h('span', { class: 'sep' }, ' · '),
      h('span', { class: 'dim' }, e.agency || 'agency not on the board'),
      h('span', { class: 'sep' }, ' · '),
      h('span', { class: 'faint' }, e.status || 'status not on the board')));
  }
  btn.append(h('span', { class: 'ev-caret faint' }, 'closes ▾'));

  btn.addEventListener('click', () => {
    const wasOpen = open != null && open.tr === tr;
    closeOpen();
    if (wasOpen) return;
    const x = expansion(r, entries);
    tr.after(x);
    tr.classList.add('ev-open');
    btn.setAttribute('aria-expanded', 'true');
    open = { tr, x, btn };
  });

  td.append(btn);
  return td;
}

/* The expansion carries everything the cell used to print inline: the request
   line again, the request's own title, and the open question it would close. */
function expansion(r: ClaimRow, entries: FoiaEntry[]): HTMLTableRowElement {
  const x = h('tr', { class: 'ev-x' }) as HTMLTableRowElement;
  const td = h('td', { class: 'ev-xcell', colspan: '7' });
  x.append(td);

  for (const e of entries) {
    const block = h('div', { class: 'ev-foia' });
    block.append(h('div', { class: 'ev-foia-head' },
      h('span', { class: 'amber' }, e.request),
      h('span', { class: 'sep' }, ' · '),
      h('span', { class: 'dim' }, e.agency || 'agency not on the board'),
      h('span', { class: 'sep' }, ' · '),
      h('span', { class: 'faint' }, e.status || 'status not on the board')));
    if (e.title) block.append(h('div', { class: 'dim' }, e.title));
    const qs = h('div', { class: 'ev-foia-q faint' }, 'reading the open question …');
    block.append(qs);
    questions(r.node, e.questions || []).then((lines) => {
      clear(qs);
      qs.className = 'ev-foia-q';
      if (!lines.length) {
        qs.append(h('span', { class: 'faint' }, 'the question this would close is not on the board'));
        return;
      }
      for (const l of lines) qs.append(h('div', { class: 'ev-q' }, 'closes: ' + l));
    });
    td.append(block);
  }
  return x;
}

/* The question text lives on the node record; the FOIA file carries only the
   indices into it. One fetch per node, cached by data.ts. */
const qcache = new Map<string, Promise<string[]>>();
function questions(node: string, idxs: number[]): Promise<string[]> {
  if (!idxs.length) return Promise.resolve([]);
  let p = qcache.get(node);
  if (!p) {
    p = loadNode(node)
      .then((rec: NodeRecord) => (rec.dossier && rec.dossier.openQuestions) || [])
      .catch(() => [] as string[]);
    qcache.set(node, p);
  }
  return p.then((all) => idxs.map((i) => all[i]).filter(Boolean));
}
