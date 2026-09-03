/* data.ts — the runtime data contract of notes/APP-SPEC-2026-09-02.md section 2.
 *
 * Everything is fetched from same-origin /data. Nothing else is fetched by this
 * module: /fonts is a stylesheet concern and the analyst Worker is analyst.ts.
 */

const BASE = import.meta.env.BASE_URL;

export interface IndexNode {
  id: string;
  label: string;
  short: string;
  cls: string;
  cluster: string | null;
  tier: string | null;
  C: number | null;
  A: number | null;
  D: number | null;
  status: string | null;
  dateStart: string | null;
  dateEnd: string | null;
  era: string;
  band: string | null;
  l0: boolean;
  deg: number;
  claims: [number, number, number];
  hl: number | null;
}

export interface Era { id: string; label: string; sub: string; start: number | null; end: number | null; }
export interface Band { id: string; label: string; }
export interface ClassDef { id: string; label: string; colour: string; }
export interface ClusterDef { id: string; label: string; }

export interface Counts {
  nodes: number; people: number; entities: number; edges: number;
  claims: Record<string, number>;
  timeline: number; l0: number; threads: number; patents: number; sheets: number;
  foia: { requests: number; questions: number; nodes: number };
}

export interface BoardIndex {
  generated: string;
  source: string;
  counts: Counts;
  eras: Era[];
  bands: Band[];
  classes: ClassDef[];
  clusters: ClusterDef[];
  nodes: IndexNode[];
}

export interface Source { name?: string; url?: string | null; date?: string | null; }
export interface Claim { tier: number; text: string; source?: string | Source | null; }

export interface Connection {
  id: string; label: string; cls: string; tier: string | null; l0: boolean;
  type: string; claimTier: number | null; note?: string; edgeLabel?: string;
  dateStart: string | null; dateEnd: string | null;
  sources: Source[]; direction: 'out' | 'in';
}

export interface Denial {
  by: { id: string; label: string };
  of: { id: string; label: string };
  label: string; claimTier: number | null; note?: string;
  denialKind?: string; sources?: Source[];
}

export interface TimelineEvent {
  id: string; strand: string; date: string; precision: string;
  label: string; text?: string; tier?: string; node?: string; era?: string;
}

export interface FoiaRequest {
  request: string; agency?: string; title?: string; status?: string;
  sendTo?: string; questions?: number[]; partial?: number[];
}

export interface Dossier {
  whatItIs?: string; whyImplicated?: string; narrative?: string;
  denialPosture?: string; roles?: string[]; openQuestions?: string[];
  claims?: Claim[];
}

export interface NodeRecord {
  id: string; label: string; short?: string; cls: string; cluster?: string | null;
  sub?: string; desc?: string; narrative?: string; tier?: string;
  C?: number; A?: number; D?: number;
  dateStart?: string | null; dateEnd?: string | null;
  locLabel?: string; coords?: unknown;
  tierRationale?: string;
  claims?: Claim[];
  sources?: Source[];
  chronology?: { date: string; event: string; precision?: string }[];
  affiliations?: string[];
  conflicts?: string[] | string;
  unverified?: string[] | string;
  dossier: Dossier | null;
  connections: Connection[];
  denials: Denial[];
  timeline: TimelineEvent[];
  /* `questions` are indices into dossier.openQuestions, which is where the text is */
  foia: { requests: FoiaRequest[]; questions: number[] };
  members: { id: string; label: string; cls: string; tier: string | null }[] | null;
}

export interface Highlight { id: string; rank: number; why: string; }
export interface HighlightsFile { flags: Highlight[] }

export interface EntryPath { id: string; label: string; blurb: string; total: number; onMap: number; ids: string[]; }
export interface MapFile { entryPaths: EntryPath[]; }

export interface AnalystFile { worker: string; suggestions: string[]; }

export interface ClaimRow {
  node: string; label: string; cls: string; cluster: string | null; tier: number;
  text: string; source: { text: string; url: string | null; domain?: string | null };
  denied: boolean; open: boolean;
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

export const loadIndex = () => get<BoardIndex>('index.json');
export const loadHighlights = () => get<HighlightsFile>('highlights.json');
export const loadMap = () => get<MapFile>('map.json');
export const loadAnalyst = () => get<AnalystFile>('analyst.json');
export const loadNode = (id: string) => get<NodeRecord>('nodes/' + id + '.json');
export const loadClaims = () => get<ClaimRow[]>('claims.json');

/* Class colour: the data is the authority (index.json carries the class table);
   the token is the fallback so a missing row cannot draw an uncoloured mark. */
let classColours: Record<string, string> = {};
export function registerClasses(classes: ClassDef[]): void {
  classColours = {};
  for (const c of classes) classColours[c.id] = c.colour;
}
export function clsColour(cls: string): string {
  return classColours[cls] || 'var(--cls-' + cls + ', var(--dim))';
}
export function clsLetter(cls: string): string {
  return (cls || '?').charAt(0).toUpperCase();
}

/* One-line date range, exactly as the record has it. Never guessed. */
export function dateRange(a?: string | null, b?: string | null): string {
  if (a && b && a !== b) return a + ' – ' + b;
  return a || b || 'no date recorded';
}

export function asList(v: string[] | string | undefined | null): string[] {
  if (Array.isArray(v)) return v.filter(Boolean);
  return v ? [String(v)] : [];
}

/* A claim's source is a bare string on this board. The first URL in it is the
   link; where there is none the string still prints, unlinked, so a claim is
   never shown as sourced when it is not. */
export function claimSource(src: Claim['source']): { text: string; url: string | null } {
  if (!src) return { text: '', url: null };
  if (typeof src === 'object') return { text: src.name || src.url || '', url: src.url || null };
  const m = String(src).match(/https?:\/\/[^\s)\]]+/);
  return { text: String(src), url: m ? m[0] : null };
}
