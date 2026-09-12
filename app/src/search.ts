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
/* claim text, lowercased and with punctuation flattened, computed once when
   claims.json arrives rather than on every keystroke over 5,303 rows */
let claimLc: string[] = [];
let claimFlat: string[] = [];
let claimSquash: string[] = [];
let claimsAsked = false;
let claimsState: 'idle' | 'loading' | 'ready' | 'absent' = 'idle';

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

function askClaims(rerun: () => void): void {
  if (claimsAsked) return;
  claimsAsked = true;
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
}

/* Lower is better. 0 to 4 are the exact and substring ranks this has always had;
   5 is the new one, every word of the query somewhere in the name. */
function score(n: IndexNode, q: string, flat: string, terms: string[]): number {
  const label = n.label.toLowerCase();
  const short = (n.short || '').toLowerCase();
  if (n.id === q) return 0;
  if (label === q || short === q) return 1;
  if (label.startsWith(q) || short.startsWith(q)) return 2;
  if (n.id.includes(q)) return 3;
  if (label.includes(q) || short.includes(q)) return 4;
  if (terms.length > 1) {
    const hay = flatten(n.label + ' ' + (n.short || '') + ' ' + n.id);
    if (hay.includes(flat)) return 4;
    if (terms.every((t) => hay.includes(t))) return 5;
  }
  return -1;
}

/* Claim ranking. Before 12 September 2026 this was `filter(...).slice(0, 12)`,
   which took the first twelve in file order -- alphabetical by node id -- so a
   search for Roswell showed whichever claims happened to sit early in the
   alphabet rather than the strongest ones. Lower is better here too:

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
     still scores better than the best Tier 2 one (tier 2 - 0.25). That is not
     arbitrary tuning: this board's whole point is the grading, and a ranking in
     which an early mention can push a documented claim below an inferred one
     would quietly argue the opposite. */
  s += c.tier;
  s += Math.min(0.5, (at >= 0 ? at : 500) / 1000);
  if (nodeHit.has(c.node)) s -= 0.25;
  return s;
}

/* The excerpt, centred on the first thing the reader actually typed that is in
   this claim. With a multi-word query the whole phrase is often not present, so
   fall back to the earliest single term rather than showing the claim's opening
   words and highlighting nothing. */
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
    (from > 0 ? '\u2026' : '') + text.slice(from, i),
    h('mark', null, text.slice(i, i + len)),
    text.slice(i + len, i + len + 90) + (text.length > i + len + 90 ? '\u2026' : ''),
  );
  return span;
}

function render(panel: HTMLElement, raw: string, rerun: () => void): void {
  clear(panel);
  const q = raw.trim().toLowerCase();
  if (q.length < 2) { panel.hidden = true; return; }
  panel.hidden = false;
  const flat = flatten(q);
  const terms = termsOf(q);

  const scored: { n: IndexNode; s: number }[] = [];
  for (const n of nodes) {
    const s = score(n, q, flat, terms);
    if (s >= 0) scored.push({ n, s });
  }
  scored.sort((a, b) => a.s - b.s || b.n.deg - a.n.deg || a.n.label.localeCompare(b.n.label));
  const top = scored.slice(0, MAX_NODE_HITS);

  panel.append(h('div', { class: 'res-head' },
    top.length ? scored.length + ' node' + (scored.length === 1 ? '' : 's') + ' match \u201c' + raw.trim() + '\u201d'
      : 'no node matches \u201c' + raw.trim() + '\u201d'));

  for (const { n } of top) {
    panel.append(h('a', { class: 'res', href: '#/n/' + n.id },
      mark(clsColour(n.cls)),
      h('span', { class: 'label' }, n.label),
      h('span', { class: 'meta' },
        n.cls + ' \u00b7 tier ' + (n.tier || '?') + ' \u00b7 ' + (n.dateStart || 'no date') +
        ' \u00b7 ' + (n.claims[0] + n.claims[1] + n.claims[2]) + ' claims'),
    ));
  }

  askClaims(rerun);

  if (claimsState === 'loading') {
    panel.append(h('div', { class: 'res-empty' }, 'loading claim text\u2026'));
    return;
  }
  if (claimsState === 'absent') {
    panel.append(h('div', { class: 'res-empty' },
      'claims.json is not served on this deployment, so this search covers node names only'));
    return;
  }
  if (!claims) return;

  const nodeHit = new Set(top.map((t) => t.n.id));
  const sq = squash(q);
  const sqq = sq.length >= 5 ? sq : '';
  const chits: { c: ClaimRow; s: number }[] = [];
  for (let i = 0; i < claims.length; i++) {
    const s = claimScore(i, q, terms, sqq, nodeHit, claims[i]);
    if (s >= 0) chits.push({ c: claims[i], s });
  }
  chits.sort((a, b) => a.s - b.s || a.c.tier - b.c.tier || a.c.node.localeCompare(b.c.node));
  const shown = chits.slice(0, MAX_CLAIM_HITS);

  panel.append(h('div', { class: 'res-head' },
    chits.length
      ? chits.length + ' claim' + (chits.length === 1 ? '' : 's') + ' mention it'
        + (chits.length > shown.length ? ', strongest ' + shown.length : '')
      : 'no claim text matches'));
  for (const { c } of shown) {
    panel.append(h('a', { class: 'res claim', href: '#/n/' + c.node, 'data-tier': String(c.tier) },
      mark(clsColour(c.cls)),
      h('span', { class: 'label' }, c.label),
      h('span', { class: 'meta t' + c.tier }, 'T' + c.tier),
      hitLine(c.text, q, terms),
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
