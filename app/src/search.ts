/* search.ts — client-side search over index.json, with claims.json loaded lazily
 * the first time a query runs, so claim text is searchable without paying for it
 * on first paint.
 *
 * Every result is a node link (`#/n/<id>`), which is a route in section 2.1.
 * The control is the same on every screen; Home repeats it large.
 */
import { h, clear, mark } from './dom';
import { loadIndex, loadClaims, clsColour, type IndexNode, type ClaimRow } from './data';

const MAX_NODE_HITS = 24;
const MAX_CLAIM_HITS = 12;

let nodes: IndexNode[] = [];
let claims: ClaimRow[] | null = null;
let claimsAsked = false;
let claimsState: 'idle' | 'loading' | 'ready' | 'absent' = 'idle';

export async function primeSearch(): Promise<void> {
  const idx = await loadIndex();
  nodes = idx.nodes;
}

function askClaims(rerun: () => void): void {
  if (claimsAsked) return;
  claimsAsked = true;
  claimsState = 'loading';
  loadClaims().then(
    (rows) => { claims = rows; claimsState = 'ready'; rerun(); },
    () => { claimsState = 'absent'; rerun(); },
  );
}

function score(n: IndexNode, q: string): number {
  const label = n.label.toLowerCase();
  const short = (n.short || '').toLowerCase();
  if (n.id === q) return 0;
  if (label === q || short === q) return 1;
  if (label.startsWith(q) || short.startsWith(q)) return 2;
  if (n.id.includes(q)) return 3;
  if (label.includes(q) || short.includes(q)) return 4;
  return -1;
}

function hitLine(text: string, q: string): HTMLElement {
  const i = text.toLowerCase().indexOf(q);
  const span = h('span', { class: 'hit' });
  if (i < 0) { span.append(text.slice(0, 150)); return span; }
  const from = Math.max(0, i - 46);
  span.append(
    (from > 0 ? '…' : '') + text.slice(from, i),
    h('mark', null, text.slice(i, i + q.length)),
    text.slice(i + q.length, i + q.length + 90) + (text.length > i + q.length + 90 ? '…' : ''),
  );
  return span;
}

function render(panel: HTMLElement, raw: string, rerun: () => void): void {
  clear(panel);
  const q = raw.trim().toLowerCase();
  if (q.length < 2) { panel.hidden = true; return; }
  panel.hidden = false;

  const scored: { n: IndexNode; s: number }[] = [];
  for (const n of nodes) {
    const s = score(n, q);
    if (s >= 0) scored.push({ n, s });
  }
  scored.sort((a, b) => a.s - b.s || b.n.deg - a.n.deg || a.n.label.localeCompare(b.n.label));
  const top = scored.slice(0, MAX_NODE_HITS);

  panel.append(h('div', { class: 'res-head' },
    top.length ? scored.length + ' node' + (scored.length === 1 ? '' : 's') + ' match “' + raw.trim() + '”'
      : 'no node matches “' + raw.trim() + '”'));

  for (const { n } of top) {
    panel.append(h('a', { class: 'res', href: '#/n/' + n.id },
      mark(clsColour(n.cls)),
      h('span', { class: 'label' }, n.label),
      h('span', { class: 'meta' },
        n.cls + ' · tier ' + (n.tier || '?') + ' · ' + (n.dateStart || 'no date') +
        ' · ' + (n.claims[0] + n.claims[1] + n.claims[2]) + ' claims'),
    ));
  }

  askClaims(rerun);

  if (claimsState === 'loading') {
    panel.append(h('div', { class: 'res-empty' }, 'loading claim text…'));
    return;
  }
  if (claimsState === 'absent') {
    panel.append(h('div', { class: 'res-empty' },
      'claims.json is not served on this deployment, so this search covers node names only'));
    return;
  }
  if (!claims) return;

  const chits = claims.filter((c) => c.text.toLowerCase().includes(q)).slice(0, MAX_CLAIM_HITS);
  panel.append(h('div', { class: 'res-head' },
    chits.length ? 'claims mentioning it' : 'no claim text matches'));
  for (const c of chits) {
    panel.append(h('a', { class: 'res', href: '#/n/' + c.node },
      mark(clsColour(c.cls)),
      h('span', { class: 'label' }, c.label),
      h('span', { class: 'meta' }, 'T' + c.tier),
      hitLine(c.text, q),
    ));
  }
}

export function searchBox(opts: { big?: boolean; placeholder: string }): HTMLElement {
  const input = h('input', {
    type: 'search',
    autocomplete: 'off',
    spellcheck: 'false',
    'aria-label': 'Search the board',
    placeholder: opts.placeholder,
  });
  const panel = h('div', { class: 'results', hidden: 'hidden', role: 'listbox' });
  const box = h('div', { class: 'searchbox' + (opts.big ? ' big' : '') },
    h('span', { class: 'glass', 'aria-hidden': 'true' }, '⌕'),
    input,
    opts.big ? h('span', { class: 'slash' }, '/') : null,
    panel,
  );
  const rerun = () => render(panel, input.value, rerun);
  input.addEventListener('input', rerun);
  input.addEventListener('focus', rerun);
  input.addEventListener('keydown', (e) => {
    if ((e as KeyboardEvent).key === 'Escape') { input.value = ''; panel.hidden = true; input.blur(); }
  });
  document.addEventListener('click', (e) => {
    if (!box.contains(e.target as Node)) panel.hidden = true;
  });
  return box;
}
