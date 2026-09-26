/* Connect: redesign section 5, "Connect", and phase 10 task 4.
 *
 *   #/connect                 two ends to choose, and the eight worked pairs
 *   #/connect/<a>/<b>         up to three routes between a and b
 *
 * The routes are found in the reader's browser from the board's sourced links
 * (data/edges.json) by a weighted shortest-path search:
 *
 *   a link costs  1
 *                 + its tier      (Tier 1 nothing, Tier 2 0.75, Tier 3 2)
 *                 + its family    (the backbone families, roles, organisation,
 *                                  money, custody, law and documents, nothing;
 *                                  a denial, the board's own analysis or a shared
 *                                  place or time 1; every other family 0.5)
 *   passing through a node costs  2 x max(0, log2(1 + its distinct neighbours) - 3)
 *                 so a specific node (seven neighbours or fewer) costs nothing and a
 *                 connector hub a great deal; the board's domain nodes, which the
 *                 topics replaced, are never passed through.
 *
 * The first route is the cheapest. Each next route may not pass through any node
 * an earlier route passed through, so the three are distinct stories, not one
 * story three ways. A route through one of the board's twenty most-connected
 * nodes says so on the route; when every route does, the page says so plainly.
 * Each hop is printed from the record of the node it leaves: the words of the
 * relationship read from that side, the link's own sentence, its tier, its
 * dates and its sources. Nothing on this page is written here except the method.
 *
 * app/checks/run.mjs C62 holds it: on the eight test pairs of
 * notes/redesign-2026-09-24/B-GRAPH-STRUCTURE.md section 7, AARO's Historical
 * Record Volume I is not the first route unless it is on every route, and then
 * the page says so; and every hop is a real link between its two ends.
 */
import '../styles/connect.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import {
  loadIndex, loadEdges, loadNode, clsColour, dateRange,
  type EdgeRow, type IndexNode, type Connection,
} from '../data';
import { familyName, PREDICATES, NO_SENTENCE } from '../vocab';
import { notFound } from './notfound';

const BACKBONE = new Set(['role', 'organisation', 'money', 'custody', 'law', 'documents']);
const HEAVY = new Set(['denial', 'analysis', 'place-time']);
const TIER_COST: Record<number, number> = { 1: 0, 2: 0.75, 3: 2 };
const HUB_WEIGHT = 2;
const HUB_FREE = 3;           /* log2(1 + 7): seven neighbours or fewer cost nothing */
const HUBS_N = 20;
const K = 3;

/* The eight pairs a reader asks for, from the graph study (Appendix B section 7). */
export const TEST_PAIRS: [string, string][] = [
  ['david-grusch', 'lockheed-skunk-works'],
  ['aawsap', 'uapda-2023'],
  ['roswell-1947', 'hearing-2023-07-26'],
  ['bob-lazar', 'aaro'],
  ['project-blue-book', 'aaro'],
  ['salvatore-pais', 'lockheed-skunk-works'],
  ['robert-salas', 'aaro'],
  ['eric-davis', 'lockheed-martin'],
];

interface EdgeX extends EdgeRow { id: string; predicate?: string; }
interface Hop { from: string; to: string; edge: EdgeX; }
interface Route { hops: Hop[]; cost: number; mids: string[]; }

function familyOfEdge(e: EdgeX): string {
  const p = e.predicate ? PREDICATES.get(e.predicate) : undefined;
  return p ? p.family : 'other';
}

function linkCost(e: EdgeX): number {
  const f = familyOfEdge(e);
  return 1 + (TIER_COST[Number(e.tier)] ?? 2) + (BACKBONE.has(f) ? 0 : HEAVY.has(f) ? 1 : 0.5);
}

/* the cheapest route from s to t that avoids `banned` nodes and edges */
function cheapest(s: string, t: string, adj: Map<string, [string, number, EdgeX][]>,
  nodeCost: (id: string) => number, bannedN: Set<string>, bannedE: Set<string>,
  skip: (id: string) => boolean): Route | null {
  const dist = new Map<string, number>([[s, 0]]);
  const prev = new Map<string, [string, EdgeX]>();
  const done = new Set<string>();
  /* a binary heap of [cost, id] */
  const heap: [number, string][] = [[0, s]];
  const push = (x: [number, string]) => {
    heap.push(x);
    let i = heap.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (heap[p][0] <= heap[i][0]) break;
      [heap[p], heap[i]] = [heap[i], heap[p]]; i = p;
    }
  };
  const pop = (): [number, string] => {
    const top = heap[0];
    const last = heap.pop()!;
    if (heap.length) {
      heap[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < heap.length && heap[l][0] < heap[m][0]) m = l;
        if (r < heap.length && heap[r][0] < heap[m][0]) m = r;
        if (m === i) break;
        [heap[m], heap[i]] = [heap[i], heap[m]]; i = m;
      }
    }
    return top;
  };
  while (heap.length) {
    const [d, u] = pop();
    if (done.has(u)) continue;
    done.add(u);
    if (u === t) break;
    for (const [w, c, e] of adj.get(u) || []) {
      if (bannedE.has(e.id) || (w !== t && (bannedN.has(w) || skip(w)))) continue;
      const nd = d + c + (w === t ? 0 : nodeCost(w));
      /* strictly cheaper only: the edge list's own order breaks ties, so the
         page draws the same routes every time */
      if (nd < (dist.get(w) ?? Infinity) - 1e-9) {
        dist.set(w, nd); prev.set(w, [u, e]); push([nd, w]);
      }
    }
  }
  if (!prev.has(t)) return null;
  const hops: Hop[] = [];
  for (let x = t; x !== s;) {
    const [u, e] = prev.get(x)!;
    hops.push({ from: u, to: x, edge: e });
    x = u;
  }
  hops.reverse();
  return { hops, cost: dist.get(t)!, mids: hops.slice(0, -1).map((p) => p.to) };
}

export function findRoutes(a: string, b: string, edges: EdgeX[], nodes: IndexNode[]): Route[] {
  const deg = new Map(nodes.map((n) => [n.id, n.deg || 0]));
  const cls = new Map(nodes.map((n) => [n.id, n.cls]));
  const adj = new Map<string, [string, number, EdgeX][]>();
  const add = (x: string, y: string, c: number, e: EdgeX) => {
    let l = adj.get(x);
    if (!l) { l = []; adj.set(x, l); }
    l.push([y, c, e]);
  };
  for (const e of edges) {
    if (e.a === e.b) continue;
    const c = linkCost(e);
    add(e.a, e.b, c, e); add(e.b, e.a, c, e);
  }
  const nodeCost = (id: string) => HUB_WEIGHT * Math.max(0, Math.log2(1 + (deg.get(id) || 0)) - HUB_FREE);
  const skip = (id: string) => cls.get(id) === 'domain';
  const routes: Route[] = [];
  const bannedN = new Set<string>(), bannedE = new Set<string>();
  for (let k = 0; k < K; k++) {
    const r = cheapest(a, b, adj, nodeCost, bannedN, bannedE, skip);
    if (!r) break;
    routes.push(r);
    if (!r.mids.length) bannedE.add(r.hops[0].edge.id);
    for (const m of r.mids) bannedN.add(m);
  }
  return routes;
}

export async function renderConnect(view: HTMLElement, a: string | null, b: string | null): Promise<void> {
  clear(view);
  const idx = await loadIndex();
  const byId = new Map(idx.nodes.map((n) => [n.id, n]));
  const raw = '#/connect' + (a ? '/' + a : '') + (b ? '/' + b : '');
  if (a && !byId.has(a)) { notFound(view, raw, 'No node with the id ' + a + ' is on the board.'); return; }
  if (b && !byId.has(b)) { notFound(view, raw, 'No node with the id ' + b + ' is on the board.'); return; }

  const page = h('article', { class: 'connect', 'data-a': a || '', 'data-b': b || '' });
  view.append(page);
  page.append(h('div', { class: 'crumb' }, h('div', { class: 'crumb-l' }, h('span', { class: 'eyebrow' }, 'Connect'))));
  const A = a ? byId.get(a)! : null, B = b ? byId.get(b)! : null;
  setTitle(A && B ? 'Connect ' + A.label + ' and ' + B.label : 'Connect');
  page.append(A && B
    ? h('h1', { class: 'connect-h1' }, h('a', { href: '#/n/' + A.id }, A.label), h('span', { class: 'dim' }, ' and '),
      h('a', { href: '#/n/' + B.id }, B.label))
    : h('h1', { class: 'connect-h1' }, 'How two things on the board are joined'));
  page.append(h('p', { class: 'connect-method dim' },
    'Up to three routes through the board\'s sourced links, no two passing through the same node. ' +
    'A route prefers Tier 1 links, the backbone relationships (roles, organisation, money, custody, law and ' +
    'documents) and specific nodes over the board\'s most-connected ones. Every step prints the link\'s own ' +
    'sentence, its tier and its sources. A route is a chain of recorded links, not a finding that the ends ' +
    'are related in any further way.'));
  page.append(picker(idx.nodes, a, b));

  if (!A || !B) {
    page.append(examples(byId));
    return;
  }
  if (a === b) {
    page.append(h('p', { class: 'connect-none' }, 'Both ends are the same node.'));
    return;
  }

  const edges = (await loadEdges()) as EdgeX[];
  const routes = findRoutes(a!, b!, edges, idx.nodes);
  const hubs = new Set(idx.nodes.slice().sort((x, y) => (y.deg || 0) - (x.deg || 0) || (x.id < y.id ? -1 : 1))
    .slice(0, HUBS_N).map((n) => n.id));
  if (!routes.length) {
    page.append(h('p', { class: 'connect-none' }, 'The board holds no chain of sourced links between these two.'));
    return;
  }
  const hubbed = routes.map((r) => r.mids.filter((m) => hubs.has(m)));
  if (hubbed.every((x) => x.length)) {
    const names = [...new Set(hubbed.flat())].map((m) => byId.get(m)!.label);
    page.append(h('div', { class: 'connect-onlyhub', 'data-hubs': [...new Set(hubbed.flat())].join(' ') },
      h('span', { class: 'amber eyebrow' }, 'Only through a connector hub'),
      h('span', null, 'Every route the board holds between these two runs through ' + list(names) +
        ', among the board\'s twenty most-connected nodes. Read each as two things the same ' +
        (names.length === 1 ? 'node' : 'nodes') + ' touched, not as a story that joins them.')));
  }

  /* each hop is printed from the record of the node it leaves */
  const need = [...new Set(routes.flatMap((r) => r.hops.map((p) => p.from)))];
  const recs = new Map(await Promise.all(need.map(async (id) => [id, await loadNode(id).catch(() => null)] as const)));
  routes.forEach((r, i) => page.append(route(r, i, byId, recs, hubbed[i])));
}

function list(xs: string[]): string {
  return xs.length <= 1 ? (xs[0] || '') : xs.slice(0, -1).join(', ') + ' and ' + xs[xs.length - 1];
}

function route(r: Route, i: number, byId: Map<string, IndexNode>,
  recs: Map<string, { connections: Connection[] } | null>, hubs: string[]): HTMLElement {
  const tiers = r.hops.map((p) => 'T' + (p.edge.tier ?? '?'));
  const box = h('section', { class: 'croute', 'data-route': String(i + 1), 'data-mids': r.mids.join(' ') },
    h('div', { class: 'croute-head' },
      h('span', { class: 'eyebrow' }, 'Route ' + (i + 1)), ' ',
      h('span', { class: 'dim' }, '· ' + r.hops.length + (r.hops.length === 1 ? ' link' : ' links') + ' · ' + tiers.join(' '))));
  if (hubs.length) {
    const names = hubs.map((m) => byId.get(m)!.label);
    box.append(h('div', { class: 'croute-hub', 'data-hubs': hubs.join(' ') },
      'Runs through ' + list(names) + ', among the board\'s twenty most-connected nodes: this route shows that ' +
      (hubs.length === 1 ? 'it touches' : 'they touch') + ' both ends, not how the ends are related.'));
  }
  const ol = h('ol', { class: 'chops' });
  r.hops.forEach((p, k) => {
    const from = byId.get(p.from)!, to = byId.get(p.to)!;
    const rec = recs.get(p.from);
    const conn = rec ? rec.connections.find((c) => (c as Connection & { edgeId?: string }).edgeId === p.edge.id && c.id === p.to) : undefined;
    const fam = familyName(conn?.family || familyOfEdge(p.edge));
    const verb = (conn && conn.verb) || fam.phrase;
    const li = h('li', { class: 'chop' + (fam.id === 'denial' ? ' denial' : ''), 'data-edge': p.edge.id, 'data-from': p.from, 'data-to': p.to },
      k === 0 ? h('a', { class: 'chop-node', href: '#/n/' + from.id }, mark(clsColour(from.cls)), h('span', { class: 'label' }, from.label)) : null,
      h('div', { class: 'chop-link' },
        h('span', { class: 'chop-verb' + (conn && conn.predicateShown ? '' : ' dim') }, verb),
        h('span', { class: 'chop-fam faint' }, ' · ' + fam.label.toLowerCase())),
      h('div', { class: 'chop-say' },
        h('span', { class: 'chop-text' }, (conn && (conn.edgeLabel || conn.note)) || p.edge.label || NO_SENTENCE),
        h('span', { class: 'cmeta' }, dateRange(conn ? conn.dateStart : p.edge.dateStart || null, conn ? conn.dateEnd : null) +
          ' · ', h('span', { class: 'chop-tier t' + (p.edge.tier ?? '') }, 'T' + (p.edge.tier ?? '?')))),
    );
    const src = conn ? conn.sources || [] : [];
    const d = h('details', { class: 'conn-src chop-src' },
      h('summary', null, src.length ? src.length + ' source' + (src.length === 1 ? '' : 's') : 'no source recorded on this link'));
    for (const s of src) {
      const text = (s.name || s.url || '') + (s.date ? ' (' + s.date + ')' : '');
      d.append(s.url ? h('a', { href: s.url, target: '_blank', rel: 'noreferrer noopener' }, text) : h('span', null, text));
    }
    li.append(d);
    li.append(h('a', { class: 'chop-node', href: '#/n/' + to.id }, mark(clsColour(to.cls)), h('span', { class: 'label' }, to.label)));
    ol.append(li);
  });
  box.append(ol);
  return box;
}

function picker(nodes: IndexNode[], a: string | null, b: string | null): HTMLElement {
  const byLabel = new Map<string, string>();
  const dl = h('datalist', { id: 'connect-nodes' });
  for (const n of nodes.slice().sort((x, y) => x.label.localeCompare(y.label))) {
    const key = byLabel.has(n.label) ? n.label + ' (' + n.id + ')' : n.label;
    byLabel.set(key, n.id);
    dl.append(h('option', { value: key }));
  }
  const labelOf = (id: string | null) => {
    if (!id) return '';
    for (const [k, v] of byLabel) if (v === id) return k;
    return id;
  };
  const ia = h('input', { type: 'text', list: 'connect-nodes', class: 'connect-in', 'aria-label': 'from', placeholder: 'one end: a name', value: labelOf(a) }) as HTMLInputElement;
  const ib = h('input', { type: 'text', list: 'connect-nodes', class: 'connect-in', 'aria-label': 'to', placeholder: 'the other end', value: labelOf(b) }) as HTMLInputElement;
  const msg = h('span', { class: 'connect-msg faint' });
  const form = h('form', { class: 'connect-form' }, ia, h('span', { class: 'dim' }, 'and'), ib,
    h('button', { type: 'submit', class: 'act key' }, 'FIND ROUTES'), msg, dl);
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const x = byLabel.get(ia.value.trim()) || (nodes.some((n) => n.id === ia.value.trim()) ? ia.value.trim() : null);
    const y = byLabel.get(ib.value.trim()) || (nodes.some((n) => n.id === ib.value.trim()) ? ib.value.trim() : null);
    if (!x || !y) { msg.textContent = 'choose both ends from the list'; return; }
    location.hash = '#/connect/' + x + '/' + y;
  });
  return form;
}

function examples(byId: Map<string, IndexNode>): HTMLElement {
  const box = h('section', { class: 'connect-examples' },
    h('div', { class: 'sec eyebrow' }, 'Pairs a reader asks about'));
  const ul = h('ul', null);
  for (const [x, y] of TEST_PAIRS) {
    const A = byId.get(x), B = byId.get(y);
    if (!A || !B) continue;
    ul.append(h('li', null, h('a', { href: '#/connect/' + x + '/' + y }, A.label + ' and ' + B.label)));
  }
  box.append(ul);
  return box;
}
