/* map/model.ts: the map's own reading of app/public/data/map.json.
 *
 * data.ts types map.json only as far as Home needs it (entryPaths), and data.ts
 * is not mine to edit, so the fuller shape is declared here and the file is read
 * through data.ts's cache. Nothing is derived that the data already states: the
 * band is the data's `band` field (Design response 4.1), the cell membership is
 * the data's `cells` map, the start-here number is `hl`.
 */
import { loadMap as loadMapFile } from '../data';

export interface MapNode {
  id: string;
  label: string;
  short: string;
  cls: string;
  cluster: string | null;
  tier: string | null;
  C: number | null;
  A: number | null;
  D: number | null;
  dateStart: string | null;
  era: string;
  band: string;
  hl: number | null;
}

export interface DirectEdge { a: string; b: string; tier: number; types: string[]; }
export interface SummarisedEdge { a: string; b: string; via: string[]; }
export interface DenialPair { by: string; of: string; label: string; kind?: string; }
export interface EraDef { id: string; label: string; sub: string; start: number | null; end: number | null; }
export interface BandDef { id: string; label: string; }

export interface MapData {
  generated: string;
  source: string;
  nodes: MapNode[];
  direct: DirectEdge[];
  summarised: SummarisedEdge[];
  denialPairs: DenialPair[];
  cells: Record<string, string[]>;
  eras: EraDef[];
  bands: BandDef[];
}

/* The map is drawn from map.json; the class colours come from index.json, which
   main.ts has already registered before any page renders. */
export function loadMapData(): Promise<MapData> {
  return loadMapFile() as unknown as Promise<MapData>;
}

/* ---------------------------------------------------------------------------
   Ordering. Design response 2.2: "Order within a cell or a ring is start date,
   then label; never degree, tier or connections."
   Dates are "1947", "1947-06" or "1947-06-24"; a shorter one sorts before a
   longer one with the same prefix, which is the right reading of "start date".
   A node with no recorded start date sorts last, and is not given one.
--------------------------------------------------------------------------- */
export function byStartDate(a: MapNode, b: MapNode): number {
  const da = a.dateStart || '';
  const db = b.dateStart || '';
  if (da && db && da !== db) return da < db ? -1 : 1;
  if (da !== db) return da ? -1 : 1;
  return a.short.localeCompare(b.short);
}

export function startYear(n: MapNode): string {
  return n.dateStart ? String(n.dateStart).slice(0, 4) : '';
}

/* ---------------------------------------------------------------------------
   Cell keys. The data's own key is `<band>.<era-id>` ("oversight.3"). The URL
   in Design 2.1 spells the era out ("oversight.2017-2026"), so both forms are
   accepted and the spelt-out one is what the map writes into the URL.
--------------------------------------------------------------------------- */
export function eraSlug(e: EraDef): string {
  return e.label.toLowerCase().replace(/\s+/g, '-');
}

export function cellKey(band: string, era: string): string {
  return band + '.' + era;
}

/** `oversight.2017-2026` or `oversight.3` -> the data key `oversight.3`. */
export function resolveCellKey(raw: string | null, data: MapData): string | null {
  if (!raw) return null;
  const dot = raw.lastIndexOf('.');
  if (dot < 0) return null;
  const band = raw.slice(0, dot);
  const era = raw.slice(dot + 1);
  if (!data.bands.some((b) => b.id === band)) return null;
  const hit = data.eras.find((e) => e.id === era || eraSlug(e) === era.toLowerCase());
  if (!hit) return null;
  const key = cellKey(band, hit.id);
  return Object.prototype.hasOwnProperty.call(data.cells, key) ? key : null;
}

/** The shareable form of a data key. */
export function urlCellKey(key: string, data: MapData): string {
  const dot = key.lastIndexOf('.');
  const era = data.eras.find((e) => e.id === key.slice(dot + 1));
  return key.slice(0, dot) + '.' + (era ? eraSlug(era) : key.slice(dot + 1));
}

/* ---------------------------------------------------------------------------
   The rest budget. Design response 1.4 and 4.5: the tier-1 direct edges with
   the most types, 118 of them, denial edges red. Chosen by tier and type count,
   never by endpoint degree.
--------------------------------------------------------------------------- */
export const REST_BUDGET = 118;

export function edgeKey(a: string, b: string): string {
  return a < b ? a + '|' + b : b + '|' + a;
}

export function restEdges(data: MapData): DirectEdge[] {
  const ranked = data.direct.slice().sort((x, y) => {
    if (x.tier !== y.tier) return x.tier - y.tier;
    if (y.types.length !== x.types.length) return y.types.length - x.types.length;
    return edgeKey(x.a, x.b) < edgeKey(y.a, y.b) ? -1 : 1;
  });
  return ranked.slice(0, REST_BUDGET);
}

export function denialKeys(data: MapData): Set<string> {
  return new Set(data.denialPairs.map((p) => edgeKey(p.by, p.of)));
}
