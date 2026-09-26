/* data.ts: the runtime data contract of notes/APP-SPEC-2026-09-02.md section 2.
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
/* phase 8: a claim's registry sources (research/_sources.json), each linking to
   #/s/<id>; `unresolved` says why a claim has none. The original source string
   stays in `source` either way. */
export interface SourceRef { id: string; title: string; locator?: string | null; }
export interface Claim {
  id?: string; tier: number; text: string; source?: string | Source | null;
  sources?: SourceRef[]; unresolved?: string | null;
}

export interface Connection {
  id: string; label: string; cls: string; tier: string | null; l0: boolean;
  type: string; claimTier: number | null; note?: string; edgeLabel?: string;
  dateStart: string | null; dateEnd: string | null;
  sources: Source[]; direction: 'out' | 'in';
  /* phase 7: the controlled predicate and its family; `verb` is the words to
     print from THIS node's side (the predicate's label where `predicateShown`,
     the family's neutral phrase otherwise); `predicateSide` says whether this
     node is the predicate's subject, its object, or either (symmetric). */
  predicate?: string | null; family?: string | null; verb?: string | null;
  predicateSide?: 'subject' | 'object' | 'either' | null; predicateShown?: boolean;
}

/* `a` and `b` are the edge's two ends in record order. `by` and `of` are set only
   where data/denial-adjudication.json names the denier; otherwise both are null
   and no direction may be printed (redesign phase 3, decision 5). */
export interface Denial {
  a: { id: string; label: string };
  b: { id: string; label: string };
  by: { id: string; label: string } | null;
  of: { id: string; label: string } | null;
  label: string; claimTier: number | null; note?: string;
  denialKind?: string | null; sources?: Source[];
}

/* `grade` is the event's own A/B/C grade and `claimTier` a claim tier 1/2/3: two
   fields since phase 3, where one `tier` field used to carry both vocabularies. */
export interface TimelineEvent {
  id: string; strand: string; date: string; precision: string;
  label: string; text?: string; grade?: string | null; claimTier?: number | null;
  node?: string; era?: string;
  /* phase 9: the section of the node's primary topic ("other" when none), that
     topic, the event's own sources, and, for a same-day repeat, the id of the
     event the timeline shows in its place */
  section?: string; topic?: string | null;
  sources?: { text: string; url: string | null }[];
  sameAs?: string;
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
  sequenceChain?: { date: string; event: string; isAnomalous?: boolean; source?: string | null }[];
  affiliations?: string[];
  conflicts?: string[] | string;
  unverified?: string[] | string;
  /* an entity's own open questions, carried since phase 3; they print after the
     dossier's, which are the ones FOIA request indices point into */
  openQuestions?: string[];
  /* authored topic tags (ids of domain nodes); `sourceFiles` is the provenance */
  domains?: string[];
  sourceFiles?: string[];
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

/* map.json carries the whole program map, not only the entry paths. The pages
   read entryPaths; the analyst's tools read the rest of it, so the shape is
   stated in full here rather than re-declared next to them. */
export interface MapNode {
  id: string; label: string; short?: string; cls: string; cluster?: string | null;
  tier: string | null; band: string; era: string;
  C?: number; A?: number; D?: number; dateStart?: string | null; hl?: number | null;
}
export interface MapFile {
  entryPaths: EntryPath[];
  bands?: Band[];
  eras?: Era[];
  cells?: Record<string, string[]>;
  nodes?: MapNode[];
  denialPairs?: { by: string; of: string; kind: string; label: string }[];
  summarised?: { a: string; b: string; via: string[] }[];
}

export interface EdgeRow {
  a: string; b: string; t: string; tier: number | null;
  label?: string; dateStart?: string | null;
}

export interface ThreadStep {
  node: string; year: number | null; evidence: string;
  edge: { kind: string; tier: number | null; type: string; via: string[] } | null;
}
export interface Thread { id: string; label: string; title?: string; blurb: string; steps: ThreadStep[]; }
export interface ThreadsFile { threads: Thread[]; }

export interface Patent {
  number: string; title: string; sub?: string; node?: string | null;
  application?: string; docket?: string; examiner?: string; supervisor?: string;
  artUnits?: string[]; assignee?: string | null; inventor?: string | null;
  filed?: string | null; published?: string | null; granted?: string | null;
  expired?: string | null; status?: string; sheets?: unknown;
  fee?: { finding?: string; lapsed?: string; title?: string } | null;
  absent?: string[];
  prosecution?: { date: string; kind: string; label: string; note?: string | null; file?: string | null }[];
  source?: unknown;
}
export interface PatentsFile {
  patents: Patent[];
  title?: string; standfirst?: string; eyebrow?: string;
  findings?: unknown; observables?: unknown; quotes?: unknown;
  comparison?: unknown; openQuestions?: unknown; drawings?: unknown;
}

export interface FoiaNodeLink { node: string; questions: number[]; partial: number[]; }
export interface FoiaRecord {
  id: string; agency?: string; title?: string; status?: string; sendTo?: string;
  nodes?: FoiaNodeLink[]; body?: string;
}
export interface FoiaFile {
  requests: FoiaRecord[];
  byNode: Record<string, FoiaRequest[]>;
  status?: unknown; letters?: unknown;
}

/* Per-route chips. `shape: "per-route"` means `byRoute` is authoritative and
   `suggestions` is the home list repeated for a reader on an older cached copy
   of the page; a flat file with neither is read as home-only (see analyst/chips). */
export interface AnalystFile {
  worker: string;
  suggestions: string[];
  shape?: string;
  byRoute?: Record<string, string[]>;
}

export interface ClaimRow {
  id?: string;
  node: string; label: string; cls: string; cluster: string | null; tier: number;
  text: string; source: { text: string; url: string | null; domain?: string | null };
  sources?: SourceRef[]; unresolved?: string | null;
  denied: boolean; open: boolean;
}

/* ---- the Library (redesign phase 8) ------------------------------------------ */

export interface LibraryRow {
  id: string; type: string; title: string; issuer: string | null; date: string | null;
  era: string; interestedParty: boolean; identifiers: string[]; host?: string | null;
  claims: number; edges: number; listedOn: number; node: string | null;
  urls: number; archived: number;
}
export interface LibraryFile {
  generated: string; count: number; sources: LibraryRow[];
  claims: { total: number; resolved: number };
}
export interface NodeRef { id: string; label: string; cls: string | null; }
export interface SourceRecord {
  id: string; type: string; title: string; issuer: string | null; date: string | null;
  era: string; interestedParty: boolean; identifiers: string[];
  urls: string[]; archived: string[]; node: NodeRef | null; host?: string | null;
  claims: { id: string; node: string; nodeLabel: string; cls: string; tier: number;
    text: string; sourceText: string; locator: string | null }[];
  topics: { id: string; title: string; claims: string[] }[];
  edges: { id: string; a: NodeRef; b: NodeRef; type: string; label: string;
    claimTier: number | null; note: string }[];
  listedOn: NodeRef[];
}

/* ---- topics (redesign phase 5 data, read by the pages from phase 6) --------- */

export interface TopicSection { id: string; order: number; title: string; blurb: string; }
export interface TopicCounts {
  cites: number; members: number; questions: number;
  record: number; claimed: number; contested: number;
}
export interface TopicRow {
  id: string; title: string; kind: string; section: string; focusEra: string;
  span: { from?: string | null; to?: string | null } | null;
  lead: string | null; researchGap: boolean; status: string;
  related: string[]; counts: TopicCounts;
}
/* node id -> [topic id, role, 1 when the node is one of that topic's anchors],
   primary topic first (build_app_data.py appears_in) */
export type AppearsIn = Record<string, [string, string, number][]>;
export interface TopicsFile {
  generated: string; source: string;
  sections: TopicSection[];
  topics: TopicRow[];
  appearsIn: AppearsIn;
  coverage: unknown;
}

/* One cited id, resolved: a claim (with the node it sits on and its source) or
   an edge (with its two ends and its sources). */
export interface TopicCite {
  id: string; kind: 'claim' | 'edge' | null; tier: number; text: string;
  node?: string; nodeLabel?: string;
  source?: { text: string; url: string | null; domain?: string | null };
  sourceRefs?: SourceRef[];
  label?: string; type?: string;
  endpoints?: { id: string; label: string }[];
  sources?: Source[];
  missing?: boolean; unplaced?: boolean;
}
export interface TopicItem { text: string; cite: string[]; }
export interface TopicMember { id: string; role: string; label: string | null; cls: string | null; }
export interface TopicRecord {
  id: string; title: string; kind: string; section: string; focusEra: string;
  span: { from?: string | null; to?: string | null } | null;
  lead: TopicItem | null;
  summary: TopicItem[]; record: TopicItem[]; claimed: TopicItem[]; contested: TopicItem[];
  members: TopicMember[]; anchors: string[]; absorbs: string[];
  questions: string[]; related: string[];
  researchGap?: string | boolean;
  cites: Record<string, TopicCite>;
}

export interface VocabFile {
  topicKinds: { id: string; blurb: string }[];
  topicRoles: { id: string; blurb: string }[];
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
export const loadLibrary = () => get<LibraryFile>('sources.json');
export const loadSource = (id: string) => get<SourceRecord>('sources/' + id + '.json');
/* The five below are read only by the analyst's tools today. They go through the
   same cache as everything else, so a reader who has already opened the timeline
   does not fetch it twice when the analyst asks about it. */
export const loadEdges = () => get<EdgeRow[]>('edges.json');
export const loadTimeline = () => get<TimelineEvent[]>('timeline.json');
export const loadThreads = () => get<ThreadsFile>('threads.json');
export const loadTopics = () => get<TopicsFile>('topics.json');
export const loadTopic = (id: string) => get<TopicRecord>('topics/' + id + '.json');

/* A topic's span as one line, exactly as the record has it. */
export function spanText(s: TopicRow['span']): string {
  const a = s && s.from, b = s && s.to;
  if (a && b && a !== b) return a + ' to ' + b;
  return a || b || 'no span recorded';
}
/* Phase 9: the person facets (research/_person_facets.json as shipped). */
export type FacetKey = 'roles' | 'vitalStatus' | 'roleStatus' | 'underOath';
export interface PersonFacets {
  roles: string[]; vitalStatus: string; roleStatus: string; underOath: string;
  basis?: Partial<Record<FacetKey, string>>;
}
export interface FacetsFile {
  generated: string; source: string;
  vocab: Record<FacetKey, string[]>;
  people: Record<string, PersonFacets>;
}
export const loadFacets = () => get<FacetsFile>('facets.json');
/* Phase 8's Library (sources.json, one row per registry source), for search.
   A failed fetch is not an error: search simply has no sources to offer. */
export type SourceRow = LibraryRow;
export function loadSourcesIfAny(): Promise<SourceRow[]> {
  return loadLibrary().then((f) => (f && Array.isArray(f.sources) ? f.sources : []), () => []);
}

export const loadPatents = () => get<PatentsFile>('patents.json');
export const loadFoia = () => get<FoiaFile>('foia.json');

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
