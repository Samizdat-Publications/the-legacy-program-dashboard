/* thread/data.ts: the two runtime files the Thread page and the Timeline's
 * thread scope read: data/threads.json (authored, phase 1c) and data/map.json
 * (the 7 x 5 grid the small map draws on).
 *
 * Same-origin /data only, like data.ts. Nothing here invents a field: every
 * shape below is the contract in notes/APP-SPEC-2026-09-02.md section 2.
 */

const BASE = import.meta.env.BASE_URL;

export interface ThreadEdge {
  type: string;
  tier: number | null;
  kind: 'direct' | 'derived';
  via: string[];
}

export interface ThreadStep {
  node: string;
  year: number | null;
  evidence: string;
  edge: ThreadEdge | null;
}

export interface Thread {
  id: string;
  label: string;
  title: string;
  blurb: string;
  steps: ThreadStep[];
}

export interface ThreadsFile { generated: string; source: string; threads: Thread[] }

export interface GridNode {
  id: string; label: string; short: string; cls: string; cluster: string | null;
  tier: string | null; C: number | null; A: number | null; D: number | null;
  dateStart: string | null; era: string; band: string; hl: number | null;
}

export interface GridFile {
  generated: string; source: string;
  bands: { id: string; label: string }[];
  eras: { id: string; label: string; sub: string; start: number | null; end: number | null }[];
  nodes: GridNode[];
  cells: Record<string, string[]>;
}

const cache = new Map<string, Promise<unknown>>();

function get<T>(path: string): Promise<T> {
  let p = cache.get(path) as Promise<T> | undefined;
  if (!p) {
    p = fetch(BASE + 'data/' + path).then((r) => {
      if (!r.ok) throw new Error(path + ' -> HTTP ' + r.status);
      return r.json() as Promise<T>;
    });
    cache.set(path, p as Promise<unknown>);
  }
  return p;
}

export const loadThreads = (): Promise<ThreadsFile> => get<ThreadsFile>('threads.json');
export const loadGrid = (): Promise<GridFile> => get<GridFile>('map.json');

export function threadById(f: ThreadsFile, id: string): Thread | undefined {
  for (const t of f.threads) if (t.id === id) return t;
  return undefined;
}

/* The edge line under a step, exactly as the file grades it. A derived join
   names the members it was derived through; a direct one says direct and
   nothing more. Nothing is inferred here. */
export function edgeLine(e: ThreadEdge | null): string {
  if (!e) return 'thread start';
  const bits = [e.type, e.tier == null ? 'tier not graded' : 'Tier ' + e.tier, e.kind];
  if (e.kind === 'derived' && e.via.length) bits.push('via ' + e.via.join(' · '));
  return bits.join(' · ');
}
