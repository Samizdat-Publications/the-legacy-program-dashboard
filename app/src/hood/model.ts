/* hood/model.ts: the neighbourhood's data, and nothing else's.
 *
 * Design response 1.5 and 2.2. Hop 1 is the node's own `connections`, which the
 * generator defines as every SOURCED edge touching the node. Hops 2 and 3 are
 * walked over `edges.json`, which is the same sourced set. Derived pairs are the
 * L0 model's `summarised` entries (two map nodes that share members below the
 * floor), and they are hop 2 by construction, which is what the legend says.
 *
 * Nothing here invents a relationship. A pair is in this file only because the
 * board already carries it.
 */
/* A short word for each family, for the ring, where a name and its reason must
   fit one label slot. The node page and the phone list carry the full sentence;
   the ring's hover title carries the reading from the centre. */
const RING_WORD: Record<string, string> = {
  role: 'role', organisation: 'organisation', money: 'money', custody: 'custody', law: 'law',
  oversight: 'oversight', testimony: 'testimony', denial: 'denial', documents: 'document',
  media: 'media', 'place-time': 'place or time', conduct: 'conduct', analysis: 'board inference',
  other: 'link',
};
export const ringWord = (family: string | null): string => (family && RING_WORD[family]) || 'link';
import { loadIndex, loadMap, loadNode, type IndexNode } from '../data';

const BASE = import.meta.env.BASE_URL;

export interface Edge { a: string; b: string; t: string; tier: number | null; label?: string; dateStart?: string | null; }
export interface Summarised { a: string; b: string; via: string[] }
interface MapWithSummarised { summarised?: Summarised[] }

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

/* One entry on the ring or in an outer column. `suffix` is the second half of
   the printed label: the edge's type and tier at hop 1, the hop number beyond. */
export interface Entry {
  id: string;
  /* `label` is the board's own authored short label, which is what the program
     map draws and what Design's capture shows on the ring. It is a field, not a
     truncation: every L0 node carries one and it is never over 37 characters.
     `full` is the record's full label, used in the expand list and on hover. */
  label: string;
  full: string;
  cls: string;
  dateStart: string | null;
  l0: boolean;
  hop: 1 | 2 | 3;
  kind: 'member' | 'map' | 'outer';
  edgeType: string | null;
  /* the relationship family of the hop-1 link (phase 7), which colours the line
     and names the link; null beyond hop 1 */
  family: string | null;
  claimTier: number | null;
  derived: boolean;
  suffix: string;
  /* the link read from the centre ("held a post at"), for the hover title */
  say: string | null;
}

export interface Hood {
  centre: IndexNode | null;
  centreLabel: string;
  hop1: Entry[];
  hop2: Entry[];
  hop3: Entry[];
  derivedIds: Set<string>;
  /* the families the centre's own links fall under, unfiltered, with the number
     of neighbours in each: what the family filter offers */
  families: { id: string; n: number }[];
  /* every id in the hop-1 ∪ hop-2 ∪ hop-3 sets, for C10 */
  parentOf: Map<string, string>;
}

function cmp(a: Entry, b: Entry): number {
  /* start date, then label. Never degree, tier or connections (Design 2.2).
     A node with no start date sorts before the dated ones and stays in label
     order, which is the only order the record supports for it. */
  const da = a.dateStart || '';
  const db = b.dateStart || '';
  if (da !== db) return da < db ? -1 : 1;
  return a.label.localeCompare(b.label);
}

function entry(
  meta: IndexNode, hop: 1 | 2 | 3, kind: Entry['kind'],
  edgeType: string | null, claimTier: number | null, derived: boolean, family: string | null = null,
): Entry {
  let suffix: string;
  if (hop === 1) {
    /* every hop-1 name says why it is there, in its family's ring word (phase 7:
       it used to be map nodes only, and the rest showed a bare tier) */
    suffix = (family ? ringWord(family) + ' ' : '') + 'T' + (claimTier ?? '?');
  } else {
    const steps = hop === 2 ? 'two steps' : 'three steps';
    suffix = derived ? steps + ', shared member' : steps;
  }
  return {
    id: meta.id, label: meta.short || meta.label, full: meta.label,
    cls: meta.cls, dateStart: meta.dateStart,
    l0: meta.l0, hop, kind, edgeType, family, claimTier, derived, suffix, say: null,
  };
}

/* The 14 start-here nodes, in the owner's order, as a ring with no centre. */
export async function startHereHood(flags: { id: string; rank: number }[]): Promise<Hood> {
  const idx = await loadIndex();
  const by = new Map(idx.nodes.map((n) => [n.id, n]));
  const hop1: Entry[] = [];
  for (const f of flags.slice().sort((a, b) => a.rank - b.rank)) {
    const m = by.get(f.id);
    if (!m) continue;               /* an id the board does not carry is not drawn */
    const e = entry(m, 1, 'map', null, null, false);
    e.suffix = 'start here ' + f.rank;
    hop1.push(e);
  }
  return {
    centre: null, centreLabel: 'pick a node',
    hop1, hop2: [], hop3: [], derivedIds: new Set(), parentOf: new Map(), families: [],
  };
}

/* `family`, when set, keeps hop 1 to the neighbours linked through that family
   (the page's family filter), and hops 2 and 3 walk out from those alone. */
export async function buildHood(id: string, hops: 1 | 2 | 3, derived: boolean, family: string | null = null): Promise<Hood> {
  const idx = await loadIndex();
  const by = new Map(idx.nodes.map((n) => [n.id, n]));
  const centre = by.get(id) || null;
  const rec = await loadNode(id);

  /* ---- the families on offer, before any filter -------------------------- */
  const famN = new Map<string, Set<string>>();
  for (const c of rec.connections) {
    const f = c.family || 'other';
    if (!famN.has(f)) famN.set(f, new Set());
    famN.get(f)!.add(c.id);
  }
  const families = [...famN.entries()].map(([fid, ids]) => ({ id: fid, n: ids.size }));

  /* ---- hop 1: the node's own sourced edges, deduplicated by neighbour ---- */
  const seen = new Map<string, Entry>();
  for (const c of rec.connections) {
    const m = by.get(c.id);
    if (!m) continue;
    const fam = c.family || 'other';
    if (family && fam !== family) continue;
    const prev = seen.get(c.id);
    if (prev) {
      /* two sourced edges to the same neighbour: the denial is the one that
         must show, and otherwise the first stands. */
      if (fam === 'denial' && prev.family !== 'denial') {
        const e = entry(m, 1, m.l0 ? 'map' : 'member', c.type, c.claimTier, false, fam);
        e.say = c.verb || null;
        seen.set(c.id, e);
      }
      continue;
    }
    const e1 = entry(m, 1, m.l0 ? 'map' : 'member', c.type, c.claimTier, false, fam);
    e1.say = c.verb || null;
    seen.set(c.id, e1);
  }
  const hop1 = [...seen.values()].sort(cmp);
  const s1 = new Set(hop1.map((e) => e.id));

  const parentOf = new Map<string, string>();
  const derivedIds = new Set<string>();
  let hop2: Entry[] = [];
  let hop3: Entry[] = [];

  if (hops >= 2) {
    const adj = await adjacency();
    const s2 = new Map<string, string>();       /* id -> the hop-1 node it came through */
    for (const a of s1) {
      for (const b of adj.get(a) || []) {
        if (b === id || s1.has(b) || s2.has(b)) continue;
        s2.set(b, a);
      }
    }
    /* derived pairs: two map nodes sharing members below the floor. They are a
       two-hop relationship and are drawn as one; DERIVED switches them off. */
    const mp = (await loadMap()) as unknown as MapWithSummarised;
    /* a family filter keeps to sourced links of that family, so the derived
       pairs, which belong to no family, stay out while it is on */
    for (const p of family ? [] : mp.summarised || []) {
      const other = p.a === id ? p.b : p.b === id ? p.a : null;
      if (!other || other === id || s1.has(other)) continue;
      derivedIds.add(other);
      if (!s2.has(other)) s2.set(other, p.via[0] || id);
    }
    for (const [nid, via] of s2) {
      if (!derived && derivedIds.has(nid)) continue;
      const m = by.get(nid);
      if (!m) continue;
      parentOf.set(nid, via);
      hop2.push(entry(m, 2, 'outer', null, null, derivedIds.has(nid)));
    }
    hop2.sort(cmp);

    if (hops >= 3) {
      const s2ids = new Set(hop2.map((e) => e.id));
      const s3 = new Map<string, string>();
      for (const a of s2ids) {
        for (const b of adj.get(a) || []) {
          if (b === id || s1.has(b) || s2ids.has(b) || s3.has(b)) continue;
          s3.set(b, a);
        }
      }
      for (const [nid, via] of s3) {
        const m = by.get(nid);
        if (!m) continue;
        parentOf.set(nid, via);
        hop3.push(entry(m, 3, 'outer', null, null, false));
      }
      hop3.sort(cmp);
    }
  }

  for (const e of hop1) parentOf.set(e.id, id);

  return {
    centre,
    centreLabel: centre ? (centre.short || centre.label) : id,
    hop1, hop2, hop3, derivedIds, parentOf, families,
  };
}

/* Edge colour by type. Denial red, custody and funding amber, everything else
   the member/map cyan. The type comes from the edge, never from a guess. */
/* the line colour of a hop-1 link, by its relationship family (phase 7) */
export function edgeColour(family: string | null): string {
  if (family === 'denial') return 'var(--red)';
  if (family === 'custody' || family === 'money') return 'var(--amber)';
  return 'var(--cyan)';
}
