/* evidence/model.ts — the filter state of #/evidence and the counts behind the
 * chips. The rows are claims.json, one per claim, 5,120 of them; the FOIA linkage
 * is foia.json's byNode and the question text is in nodes/<id>.json, which is why
 * the FOIA column reads a node record lazily rather than shipping the questions
 * a second time.
 *
 * Every count here is derived from the rows. Nothing is typed in.
 */
import type { ClaimRow } from '../data';

const BASE = import.meta.env.BASE_URL;

export interface FoiaEntry {
  request: string;
  agency?: string;
  title?: string;
  status?: string;
  sendTo?: string;
  questions?: number[];
  partial?: number[];
}

export interface FoiaFile {
  byNode: Record<string, FoiaEntry[]>;
  status?: string;
  letters?: string;
}

let foiaPending: Promise<FoiaFile> | null = null;
export function loadFoia(): Promise<FoiaFile> {
  if (!foiaPending) {
    foiaPending = fetch(BASE + 'data/foia.json').then((r) => {
      if (!r.ok) throw new Error('foia.json -> HTTP ' + r.status);
      return r.json() as Promise<FoiaFile>;
    });
  }
  return foiaPending;
}

/* The six parameters of Design 2.1, and nothing else. */
export const KEYS = ['tier', 'cls', 'cluster', 'domain', 'denied', 'open'] as const;
export type Key = typeof KEYS[number];
export type Filters = Record<Key, string | null>;

export function readFilters(q: URLSearchParams): Filters {
  const f = {} as Filters;
  for (const k of KEYS) f[k] = q.get(k);
  return f;
}

export function activeCount(f: Filters): number {
  return KEYS.reduce((n, k) => n + (f[k] ? 1 : 0), 0);
}

/* A claim whose source string carries no URL has no domain. It is a real state,
   not a missing one, so it gets its own chip value rather than being hidden. */
export const NO_DOMAIN = 'none';
export function rowDomain(r: ClaimRow): string {
  return (r.source && r.source.domain) || NO_DOMAIN;
}

function boolMatch(v: string | null, on: boolean): boolean {
  if (v == null) return true;
  return v === '1' ? on : v === '0' ? !on : true;
}

export function matches(r: ClaimRow, f: Filters): boolean {
  if (f.tier != null && String(r.tier) !== f.tier) return false;
  if (f.cls != null && r.cls !== f.cls) return false;
  if (f.cluster != null && (r.cluster || '') !== f.cluster) return false;
  if (f.domain != null && rowDomain(r) !== f.domain) return false;
  if (!boolMatch(f.denied, !!r.denied)) return false;
  if (!boolMatch(f.open, !!r.open)) return false;
  return true;
}

export function filterRows(rows: ClaimRow[], f: Filters): ClaimRow[] {
  return rows.filter((r) => matches(r, f));
}

export interface Facet { value: string; label: string; n: number }

function tally(rows: ClaimRow[], of: (r: ClaimRow) => string): Map<string, number> {
  const m = new Map<string, number>();
  for (const r of rows) {
    const k = of(r);
    m.set(k, (m.get(k) || 0) + 1);
  }
  return m;
}

function sorted(m: Map<string, number>): Facet[] {
  return [...m.entries()]
    .map(([value, n]) => ({ value, label: value, n }))
    .sort((a, b) => b.n - a.n || a.value.localeCompare(b.value));
}

export interface Facets {
  tier: Facet[];
  cls: Facet[];
  cluster: Facet[];
  domain: Facet[];
  denied: Facet[];
  open: Facet[];
}

export function facets(rows: ClaimRow[]): Facets {
  const denied = rows.filter((r) => r.denied).length;
  const open = rows.filter((r) => r.open).length;
  return {
    tier: [1, 2, 3].map((t) => ({
      value: String(t),
      label: 'T' + t,
      n: rows.filter((r) => r.tier === t).length,
    })),
    cls: sorted(tally(rows, (r) => r.cls)),
    cluster: sorted(tally(rows, (r) => r.cluster || '')),
    domain: sorted(tally(rows, rowDomain)),
    denied: [
      { value: '1', label: 'on a node with a denial on record', n: denied },
      { value: '0', label: 'no denial on record', n: rows.length - denied },
    ],
    open: [
      { value: '1', label: 'open question', n: open },
      { value: '0', label: 'no open question', n: rows.length - open },
    ],
  };
}

/* Toggling a chip sets its parameter, or clears it when it is already the one
   selected. The result is always a route in Design 2.1. */
export function chipHref(q: URLSearchParams, key: Key, value: string, on: boolean): string {
  const next = new URLSearchParams(q.toString());
  if (on) next.delete(key);
  else next.set(key, value);
  const s = next.toString();
  return '#/evidence' + (s ? '?' + s : '');
}

export function clearHref(): string { return '#/evidence'; }

export function fmt(n: number): string {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
