/* hood/model.ts: the neighbourhood's data, and nothing else's.
 *
 * Redesign phase 11 replaced the ring with a grouped view. Hop 1 is the node's
 * own `connections`, which the generator defines as every SOURCED edge touching
 * the node. Each neighbour is named ONCE, under one family: a denial if any of
 * its links is a denial (the link that must show), otherwise the first family
 * in the vocabulary's order among its links. Two steps out are walked over
 * `edges.json`, the same sourced set, one family at a time, and every node
 * reached is listed under the neighbour it was reached through.
 *
 * The shared-member ("derived") pairs of the retired program map are gone with
 * it: every line on this page is a hand-written, sourced edge.
 *
 * Nothing here invents a relationship. A pair is on this page only because the
 * board already carries it.
 */
import { type Connection } from '../data';
import { FAMILIES, PREDICATES, familyName } from '../vocab';

const BASE = import.meta.env.BASE_URL;

export interface Edge { a: string; b: string; t: string; tier: number | null; label?: string; dateStart?: string | null; }

let edgesP: Promise<Edge[]> | null = null;
/* Same-origin /data, the only network this module touches. */
export function loadEdges(): Promise<Edge[]> {
  if (!edgesP) {
    edgesP = fetch(BASE + 'data/edges.json').then((r) => {
      if (!r.ok) throw new Error('edges.json -> HTTP ' + r.status);
      return r.json() as Promise<Edge[]>;
    });
  }
  return edgesP;
}

let adjP: Promise<Map<string, Set<string>>> | null = null;
export function adjacency(): Promise<Map<string, Set<string>>> {
  if (!adjP) {
    adjP = loadEdges().then((edges) => {
      const adj = new Map<string, Set<string>>();
      const put = (x: string, y: string) => {
        let s = adj.get(x);
        if (!s) { s = new Set(); adj.set(x, s); }
        s.add(y);
      };
      for (const e of edges) { put(e.a, e.b); put(e.b, e.a); }
      return adj;
    });
  }
  return adjP;
}

/* A short word for each family, for a link whose predicate is not shown: the
   row then says which kind of link it is and claims no more than the family. */
const WORD: Record<string, string> = {
  role: 'role', organisation: 'organisation', money: 'money', custody: 'custody', law: 'law',
  oversight: 'oversight', testimony: 'testimony', denial: 'denial', documents: 'document',
  media: 'media', 'place-time': 'place or time', conduct: 'conduct', analysis: 'board inference',
  other: 'link',
};
export const familyWord = (family: string | null): string => (family && WORD[family]) || 'link';

/* What a row prints after a neighbour's name: the link read FROM THE NEIGHBOUR,
   whose name it follows ("Eric Burlison appointed", "Susan Gough denied"; the
   centre is the implied other end). Only a predicate the generator shows gets
   its own words; any other link prints its family's word and "link". */
export function readFromNeighbour(c: Connection): { text: string; shown: boolean } {
  const p = c.predicate ? PREDICATES.get(c.predicate) : undefined;
  if (!c.predicateShown || !p) {
    const w = familyWord(c.family || null);
    return { text: w === 'link' ? w : w + ' link', shown: false };
  }
  if (p.symmetric || c.predicateSide === 'either') return { text: p.forward, shown: true };
  return { text: c.predicateSide === 'subject' ? p.inverse : p.forward, shown: true };
}

export const FAMILY_ORDER = FAMILIES.map((f) => f.id);
const frank = (f: string): number => { const i = FAMILY_ORDER.indexOf(f); return i < 0 ? 99 : i; };

/* One neighbour, named once. `links` are its links in the family it sits
   under; `also` names the other families it is linked through. */
export interface Neighbour {
  id: string;
  label: string;
  cls: string;
  family: string;
  links: Connection[];
  readings: { text: string; shown: boolean }[];
  also: string[];
  first: string;
}
export interface FamilyGroup { family: string; rows: Neighbour[]; }

/* The family a neighbour sits under. Stated in words at the top of this file,
   and restated independently in app/checks/run.mjs (C70). */
export function familyOfNeighbour(links: Connection[]): string {
  const fams = links.map((c) => c.family || 'other');
  if (fams.includes('denial')) return 'denial';
  return fams.slice().sort((a, b) => frank(a) - frank(b) || a.localeCompare(b))[0];
}

export function groupNeighbours(conns: Connection[]): FamilyGroup[] {
  const byId = new Map<string, Connection[]>();
  for (const c of conns) {
    let l = byId.get(c.id);
    if (!l) { l = []; byId.set(c.id, l); }
    l.push(c);
  }
  const groups = new Map<string, Neighbour[]>();
  for (const [id, links] of byId) {
    const family = familyOfNeighbour(links);
    const mine = links.filter((c) => (c.family || 'other') === family);
    const seen = new Set<string>();
    const readings: { text: string; shown: boolean }[] = [];
    for (const c of mine) {
      const r = readFromNeighbour(c);
      if (seen.has(r.text)) continue;
      seen.add(r.text);
      readings.push(r);
    }
    readings.sort((a, b) => Number(b.shown) - Number(a.shown));
    const also = [...new Set(links.map((c) => c.family || 'other').filter((f) => f !== family))]
      .sort((a, b) => frank(a) - frank(b));
    const first = mine.map((c) => c.dateStart || '9999').sort()[0];
    const n: Neighbour = { id, label: links[0].label, cls: links[0].cls, family, links: mine, readings, also, first };
    let g = groups.get(family);
    if (!g) { g = []; groups.set(family, g); }
    g.push(n);
  }
  /* inside a family: earliest dated link first, then the name. Never degree,
     tier or connection count. */
  return [...groups.keys()]
    .sort((a, b) => frank(a) - frank(b) || a.localeCompare(b))
    .map((family) => ({
      family,
      rows: groups.get(family)!.sort((a, b) => a.first.localeCompare(b.first) || a.label.localeCompare(b.label)),
    }));
}

/* Two steps out through one family: every node linked to one of that family's
   neighbours that is neither the centre nor a neighbour itself, listed ONCE,
   under the first of the family's neighbours (in row order) it is reached
   through. */
export interface ViaGroup { via: Neighbour; ids: string[]; }
export function twoSteps(
  centre: string, fam: FamilyGroup, hop1: Set<string>, adj: Map<string, Set<string>>,
  labelOf: (id: string) => string,
): ViaGroup[] {
  const taken = new Set<string>();
  const out: ViaGroup[] = [];
  for (const n of fam.rows) {
    const ids: string[] = [];
    for (const m of adj.get(n.id) || []) {
      if (m === centre || hop1.has(m) || taken.has(m)) continue;
      taken.add(m);
      ids.push(m);
    }
    if (!ids.length) continue;
    ids.sort((a, b) => labelOf(a).localeCompare(labelOf(b)));
    out.push({ via: n, ids });
  }
  return out;
}

/* The line colour of a family: denial red, custody and money amber, the rest
   cyan. The family comes from the edge's predicate, never from a guess. */
export function familyColour(family: string | null): string {
  if (family === 'denial') return 'var(--red)';
  if (family === 'custody' || family === 'money') return 'var(--amber)';
  return 'var(--cyan)';
}

export const familyLabel = (f: string): string => familyName(f).label;
