/* connections.ts: a node's sourced connections, grouped by relationship family,
 * then by predicate, each reading as a sentence from this node.
 *
 * Redesign phase 7. Families (schema/vocab.json predicateFamilies) replace the
 * phase 1 layers. Inside a family, rows run in the vocabulary's predicate order;
 * each row is one counterpart under one reading ("was funded by  DIA"), with the
 * direction arrow only where the predicate itself is shown, which the generator
 * decides (a high-confidence classification; otherwise the row reads the
 * family's neutral phrase and draws no arrow). Every link keeps its authored
 * sentence, dates, tier and sources, so no link loses its explanation.
 *
 * Order: families in the vocabulary's order; inside a family, shown predicates
 * in the vocabulary's order, the family phrase last; rows by earliest date, then
 * strongest tier, then label.
 */
import { h, mark } from '../dom';
import { clsColour, dateRange, type Connection } from '../data';
import { FAMILIES, NO_SENTENCE, PREDICATE_ORDER, familyName } from '../vocab';

export interface ConnRow {
  id: string; label: string; cls: string; links: Connection[];
  verb: string; side: 'subject' | 'object' | 'either' | null; shown: boolean; predicate: string | null;
}
export interface ConnGroup { family: string; rows: ConnRow[]; }

const FORDER = FAMILIES.map((f) => f.id);
const frank = (f: string): number => { const i = FORDER.indexOf(f); return i < 0 ? 99 : i; };
const prank = (r: ConnRow): number => {
  if (!r.shown || !r.predicate) return 999;
  const i = PREDICATE_ORDER.indexOf(r.predicate);
  return i < 0 ? 998 : i;
};
const sideRank = (r: ConnRow): number => (r.side === 'subject' ? 0 : r.side === 'object' ? 1 : 2);
const firstDate = (r: ConnRow): string => r.links.map((l) => l.dateStart || '9999').sort()[0];
const bestTier = (r: ConnRow): number => Math.min(...r.links.map((l) => l.claimTier ?? 3));

/* The family a connection sits under: its predicate's family. A connection the
   generator could not classify (none should reach the page; verify.py holds
   that every edge carries one) falls under `other` rather than disappearing. */
export const familyOf = (c: Connection): string => c.family || 'other';

export function groupConnections(conns: Connection[]): ConnGroup[] {
  const byFam = new Map<string, Map<string, ConnRow>>();
  for (const c of conns) {
    const fam = familyOf(c);
    let g = byFam.get(fam);
    if (!g) { g = new Map(); byFam.set(fam, g); }
    const shown = !!c.predicateShown;
    const verb = c.verb || familyName(fam).phrase;
    const side = shown ? (c.predicateSide || null) : null;
    const key = c.id + '|' + verb + '|' + (side || '');
    let r = g.get(key);
    if (!r) {
      r = { id: c.id, label: c.label, cls: c.cls, links: [], verb, side, shown, predicate: c.predicate || null };
      g.set(key, r);
    }
    r.links.push(c);
  }
  return [...byFam.keys()]
    .sort((a, b) => frank(a) - frank(b) || a.localeCompare(b))
    .map((family) => ({
      family,
      rows: [...byFam.get(family)!.values()].sort((a, b) =>
        prank(a) - prank(b) || sideRank(a) - sideRank(b) || firstDate(a).localeCompare(firstDate(b)) ||
        bestTier(a) - bestTier(b) || a.label.localeCompare(b.label)),
    }));
}

/* The direction mark, drawn only where the predicate itself is shown. The row
   reads from this node: "→" when this node does it to the counterpart, "←" when
   the counterpart does it to this node. A symmetric predicate has no direction. */
export function dirMark(r: { side: ConnRow['side']; shown: boolean }): HTMLElement | null {
  if (!r.shown || (r.side !== 'subject' && r.side !== 'object')) return null;
  const out = r.side === 'subject';
  return h('span', {
    class: 'conn-dir', 'data-dir': out ? 'out' : 'in',
    title: out ? 'this node is the one acting' : 'the named node is the one acting',
  }, out ? '→' : '←');
}

function rowEl(r: ConnRow, family: string): HTMLElement {
  const row = h('div', {
    class: 'conn' + (family === 'denial' ? ' denial' : '') + (r.shown ? ' shown' : ' family-only'),
    'data-id': r.id, 'data-predicate': r.shown ? (r.predicate || '') : '', 'data-side': r.side || '',
  });
  row.append(h('a', { class: 'conn-head', href: '#/n/' + r.id },
    mark(clsColour(r.cls)),
    h('span', { class: 'conn-say' },
      h('span', { class: 'conn-verb' + (r.shown ? '' : ' dim') }, r.verb), ' ',
      dirMark(r), dirMark(r) ? ' ' : '',
      h('span', { class: 'row-label' }, r.label))));
  for (const l of r.links) {
    row.append(h('div', { class: 'conn-line' },
      h('span', { class: 'conn-text' }, l.edgeLabel || l.note || NO_SENTENCE),
      h('span', { class: 'cmeta' }, dateRange(l.dateStart, l.dateEnd) + ' · T' + (l.claimTier ?? '?')),
    ));
    const src = l.sources || [];
    if (src.length) {
      const d = h('details', { class: 'conn-src' }, h('summary', null, src.length + ' source' + (src.length === 1 ? '' : 's')));
      for (const s of src) {
        const text = (s.name || s.url || '') + (s.date ? ' (' + s.date + ')' : '');
        d.append(s.url ? h('a', { href: s.url, target: '_blank', rel: 'noreferrer noopener' }, text) : h('span', null, text));
      }
      row.append(d);
    }
  }
  return row;
}

export function renderConnGroups(groups: ConnGroup[]): HTMLElement {
  const wrap = h('div', { class: 'conn-groups' });
  for (const g of groups) {
    const f = familyName(g.family);
    const links = g.rows.reduce((n, r) => n + r.links.length, 0);
    const box = h('div', { class: 'conn-group', 'data-family': g.family },
      h('div', { class: 'conn-ghead' },
        h('span', { class: 'eyebrow' + (g.family === 'denial' ? ' red' : '') }, f.label), ' ',
        h('span', { class: 'dim' }, '· ' + links),
        f.blurb ? h('div', { class: 'faint' }, f.blurb) : null),
    );
    for (const r of g.rows) box.append(rowEl(r, g.family));
    wrap.append(box);
  }
  return wrap;
}
