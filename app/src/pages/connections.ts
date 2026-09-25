/* connections.ts: a node's sourced connections, grouped by relationship and by
 * counterpart, each link with its own sentence, dates, tier and sources.
 *
 * One row per counterpart per relationship: a neighbour joined by two
 * institutional edges is one row with two sentences, not two rows.
 * Order: relationships in the reading order of vocab.ts; rows by earliest date,
 * then strongest tier, then label.
 */
import { h, mark } from '../dom';
import { clsColour, dateRange, type Connection } from '../data';
import { EDGE_TYPES, LAYER_HEAD, NO_SENTENCE, edgeTypeName, type Layer } from '../vocab';

export interface ConnRow { id: string; label: string; cls: string; links: Connection[]; }
export interface ConnGroup { type: string; rows: ConnRow[]; }

const ORDER = EDGE_TYPES.map((t) => t.id);
const rank = (type: string): number => { const i = ORDER.indexOf(type); return i < 0 ? 99 : i; };
const firstDate = (r: ConnRow): string => r.links.map((l) => l.dateStart || '9999').sort()[0];
const bestTier = (r: ConnRow): number => Math.min(...r.links.map((l) => l.claimTier ?? 3));

export function groupConnections(conns: Connection[]): ConnGroup[] {
  const byType = new Map<string, Map<string, ConnRow>>();
  for (const c of conns) {
    let g = byType.get(c.type);
    if (!g) { g = new Map(); byType.set(c.type, g); }
    let r = g.get(c.id);
    if (!r) { r = { id: c.id, label: c.label, cls: c.cls, links: [] }; g.set(c.id, r); }
    r.links.push(c);
  }
  return [...byType.keys()]
    .sort((a, b) => rank(a) - rank(b) || a.localeCompare(b))
    .map((type) => ({
      type,
      rows: [...byType.get(type)!.values()].sort((a, b) =>
        firstDate(a).localeCompare(firstDate(b)) || bestTier(a) - bestTier(b) || a.label.localeCompare(b.label)),
    }));
}

function rowEl(r: ConnRow, type: string): HTMLElement {
  const row = h('div', { class: 'conn' + (type === 'denial' ? ' denial' : ''), 'data-id': r.id });
  row.append(h('a', { class: 'conn-head', href: '#/n/' + r.id }, mark(clsColour(r.cls)), h('span', { class: 'row-label' }, r.label)));
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
  let layer: Layer | null = null;
  for (const g of groups) {
    const t = edgeTypeName(g.type);
    if (t.layer !== layer) {
      layer = t.layer;
      wrap.append(h('div', { class: 'conn-layer eyebrow dim' }, LAYER_HEAD[layer]));
    }
    const box = h('div', { class: 'conn-group', 'data-type': g.type, 'data-layer': t.layer },
      h('div', { class: 'conn-ghead' },
        h('span', { class: 'eyebrow' + (g.type === 'denial' ? ' red' : '') }, t.label), ' ',
        h('span', { class: 'dim' }, '· ' + g.rows.length),
        t.blurb ? h('div', { class: 'faint' }, t.blurb) : null),
    );
    for (const r of g.rows) box.append(rowEl(r, g.type));
    wrap.append(box);
  }
  return wrap;
}
