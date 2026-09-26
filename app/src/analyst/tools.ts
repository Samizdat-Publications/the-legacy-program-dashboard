/* analyst/tools.ts — the board, as twelve tools the model can call.
 *
 * WHY THIS EXISTS
 * ---------------
 * Until 11 September 2026 the analyst was sent one snapshot and nothing else: a
 * one-line index of all 1,057 nodes, plus whichever node the reader had open, in
 * full. It could recall what was on that page and it could not do anything else.
 * It could not count, could not cross-reference, could not read the timeline,
 * could not trace a chain, and could not see a claim on a node that was not open.
 * Every question shaped like "which of these" or "how many" or "what changed
 * between" was answered from 1,057 one-line summaries or not at all.
 *
 * So the model gets tools, and the tools run HERE, in the reader's browser,
 * against the same /data files the pages read. Nothing about the board is
 * uploaded anywhere: the Worker relays a question and a set of tool results and
 * holds no copy of the board. The loop is in analyst/client.ts.
 *
 * THE CONTRACT WITH THE WORKER
 * ----------------------------
 * The names below are pinned in worker/src/index.ts as an allowlist. A name in
 * one and not the other is a build that must not ship, which is what
 * TOOLS_VERSION and the Worker's /api/analyst/health response are for.
 *
 * RULES THESE TOOLS KEEP
 * ----------------------
 * 1. Every tool returns TEXT, in the board's own `a | b | c` idiom, never JSON.
 *    It is cheaper per token and it is the shape the rest of the prompt is in.
 * 2. Every tool caps its own output (RESULT_CAP) and says so when it truncates,
 *    so a clipped answer can never read as a complete one.
 * 3. No tool invents anything. A field the record does not carry prints as
 *    absent, never as a plausible value. CLAUDE.md section 2.
 * 4. Counting is done here, not by the model. `count_only` and `group_by` exist
 *    so "how many" is answered by arithmetic over the file rather than by
 *    eyeballing a list that was truncated at 60 rows.
 */
import {
  loadIndex, loadNode, loadClaims, loadEdges, loadTimeline, loadThreads,
  loadPatents, loadFoia,
  type IndexNode, type ClaimRow, type EdgeRow, type TimelineEvent, type Claim,
} from '../data';

/* Bump when a tool is ADDED, REMOVED, or its ARGUMENTS change shape, and not for
   anything else. The Worker carries the same string and the page refuses to ask a
   question while the two disagree, so a bump the Worker has not been given yet
   takes the analyst off the air until somebody redeploys it. Rewording a
   description is not a bump: the Worker validates names and argument schemas and
   never reads the prose. */
export const TOOLS_VERSION = '2026-09-11.1';

const RESULT_CAP = 26000;      /* characters, per tool result                 */
const MAX_NODE_IDS = 6;        /* full records per `node` call                */
const DEFAULT_LIMIT = 40;
const HARD_LIMIT = 400;

/* ---- small shared helpers ----------------------------------------------- */

function clip(s: unknown, n: number): string {
  const str = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  return str.length > n ? str.slice(0, n - 3) + '...' : str;
}

function cap(body: string, what: string): string {
  if (body.length <= RESULT_CAP) return body;
  return body.slice(0, RESULT_CAP) +
    '\n[' + what + ' truncated at ' + RESULT_CAP + ' characters. Narrow the filter, ' +
    'lower `limit`, or ask for counts with `count_only`.]';
}

function num(v: unknown, fallback: number, lo: number, hi: number): number {
  const n = typeof v === 'number' ? v : parseInt(String(v ?? ''), 10);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(lo, Math.min(hi, Math.trunc(n)));
}

function str(v: unknown): string { return typeof v === 'string' ? v.trim() : ''; }
function lower(v: unknown): string { return str(v).toLowerCase(); }

function strList(v: unknown): string[] {
  if (Array.isArray(v)) return v.map((x) => String(x).trim()).filter(Boolean);
  const s = str(v);
  return s ? s.split(/[,\s]+/).filter(Boolean) : [];
}

function bool(v: unknown): boolean | null {
  if (v === true || v === 'true' || v === 1 || v === '1') return true;
  if (v === false || v === 'false' || v === 0 || v === '0') return false;
  return null;
}

/* A date on this board is `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. Comparing the
   strings is comparing the dates, as long as a bare year is padded at the ends
   rather than in the middle: `1984` as a floor is 1984-01-01, as a ceiling it is
   1984-12-31, and a naive string compare would drop every dated event in 1984. */
function floorDate(s: string): string {
  const d = str(s);
  if (/^\d{4}$/.test(d)) return d + '-01-01';
  if (/^\d{4}-\d{2}$/.test(d)) return d + '-01';
  return d;
}
function ceilDate(s: string): string {
  const d = str(s);
  if (/^\d{4}$/.test(d)) return d + '-12-31';
  if (/^\d{4}-\d{2}$/.test(d)) return d + '-31';
  return d;
}

function tally(rows: string[]): string {
  const m = new Map<string, number>();
  for (const r of rows) m.set(r, (m.get(r) || 0) + 1);
  return [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([k, v]) => '  ' + v + '  ' + k).join('\n');
}

function claimSourceText(src: Claim['source']): string {
  if (!src) return '';
  if (typeof src === 'object') return src.name || src.url || '';
  return String(src);
}

/* ---- the node index line, the same one the case index is built from ------ */

function dates(a?: string | null, b?: string | null): string {
  const x = a || '', y = b || '';
  return x || y ? x + (y && y !== x ? '..' + y : '') : 'undated';
}

function nodeLine(n: IndexNode): string {
  return [
    n.id,
    clip(n.short || n.label, 70),
    n.cls,
    'tier ' + (n.tier || '?'),
    'C' + (n.C ?? '?') + 'A' + (n.A ?? '?') + 'D' + (n.D ?? '?'),
    dates(n.dateStart, n.dateEnd),
    'deg ' + n.deg,
    'T1/T2/T3 ' + n.claims.join('/'),
  ].join(' | ');
}

/* ==========================================================================
   The catalogue
   ========================================================================== */

export interface ToolDef {
  name: string;
  description: string;
  input_schema: { type: 'object'; properties: Record<string, unknown>; required?: string[] };
}

const S = {
  limit: { type: 'integer', description: 'rows to return, 1 to ' + HARD_LIMIT + ' (default ' + DEFAULT_LIMIT + ')' },
  count_only: { type: 'boolean', description: 'return the count and nothing else' },
  contains: { type: 'string', description: 'case-insensitive substring the text must contain' },
};

export const TOOLS: ToolDef[] = [
  {
    name: 'overview',
    description:
      'What is on the board: every count, the eras, the node classes, ' +
      'the clusters, the threads, the patents and the editorial ' +
      'start-here flags, all read live from the data. Call this FIRST when a question ' +
      'turns on what the board holds rather than on one record, and whenever you need ' +
      'a number: no count is written into any tool description, because a written-down ' +
      'count goes stale.',
    input_schema: { type: 'object', properties: {} },
  },
  {
    name: 'find',
    description:
      'Full-text search over everything at once: node labels and ids, every claim text ' +
      'and its source, every timeline event, every edge label, the threads, the ' +
      'patents and the FOIA requests. Ranked. This is the tool for "where does the board ' +
      'mention X" when you do not already know the node.',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'words to look for' },
        kinds: {
          type: 'array', items: { type: 'string' },
          description: 'restrict to any of: node, claim, timeline, edge, thread, patent, foia',
        },
        limit: S.limit,
      },
      required: ['query'],
    },
  },
  {
    name: 'nodes',
    description:
      'Filter, sort, count and group the node index. Every argument is optional and ' +
      'they combine. Use group_by with count_only to answer "how many" and "which of these ' +
      'is thinnest" without reading rows.',
    input_schema: {
      type: 'object',
      properties: {
        cls: { type: 'string', description: 'document, domain, event, institution, legislation, location, person or program' },
        cluster: { type: 'string', description: 'contractor, ffrdc, ic, legacy, media, other, oversight, research or witness' },
        tier: { type: 'string', description: 'node tier A, B or C: proximity to the programme, NOT credibility' },
        band: { type: 'string', description: 'retired with the program map on 26 September 2026: no node carries a band now, and passing one says so' },
        era: { type: 'string', description: 'era id: 0, 1, 2, 3 or nd' },
        on_map: { type: 'boolean', description: 'retired with the program map on 26 September 2026: passing it says so' },
        label_contains: S.contains,
        date_from: { type: 'string', description: 'YYYY, YYYY-MM or YYYY-MM-DD; keeps nodes whose start date is on or after it' },
        date_to: { type: 'string', description: 'keeps nodes whose start date is on or before it' },
        min_degree: { type: 'integer', description: 'fewest sourced edges' },
        min_t1: { type: 'integer', description: 'fewest Tier 1 claims' },
        max_t1: { type: 'integer', description: 'most Tier 1 claims, so 0 finds nodes with none' },
        sort: { type: 'string', description: 'degree (default), claims, t1, date, label' },
        group_by: { type: 'string', description: 'cls, cluster, tier, era or decade' },
        count_only: S.count_only,
        limit: S.limit,
      },
    },
  },
  {
    name: 'node',
    description:
      'The full record for up to ' + MAX_NODE_IDS + ' nodes: what it is, why implicated, its ' +
      'denial posture, its tier rationale, every claim with its tier and source, every sourced ' +
      'edge with its label, its denials, its own timeline, its open questions and its FOIA ' +
      'requests. This is the deepest read on the board.',
    input_schema: {
      type: 'object',
      properties: {
        ids: { type: 'array', items: { type: 'string' }, description: 'node ids, at most ' + MAX_NODE_IDS },
        sections: {
          type: 'array', items: { type: 'string' },
          description: 'restrict the record to any of: dossier, claims, edges, denials, timeline, questions, foia. Omit for all (members went with the program map)',
        },
        max_claims: { type: 'integer', description: 'claims per node, default 40, up to 200' },
        max_edges: { type: 'integer', description: 'edges per node, default 60, up to 300' },
      },
      required: ['ids'],
    },
  },
  {
    name: 'claims',
    description:
      'Filter, count and group every tiered claim with its source. Claim tiers are ' +
      'evidence strength, 1 strongest: T1 documented, T2 a named person on the record, T3 a ' +
      'stated inference. This is the tool for "what would collapse under audit" and for any ' +
      'question about sourcing.',
    input_schema: {
      type: 'object',
      properties: {
        tier: { type: 'integer', description: '1, 2 or 3' },
        node: { type: 'string', description: 'a node id' },
        cls: { type: 'string' },
        cluster: { type: 'string' },
        denied: { type: 'boolean', description: 'the claim sits on a node the record carries a denial against' },
        open: { type: 'boolean', description: 'the claim sits on a node with an open question' },
        contains: S.contains,
        source_contains: { type: 'string', description: 'substring of the source text or its URL, e.g. a domain' },
        has_url: { type: 'boolean', description: 'false finds claims whose source is named but not linked' },
        group_by: { type: 'string', description: 'tier, node, cls, cluster or domain' },
        count_only: S.count_only,
        limit: S.limit,
      },
    },
  },
  {
    name: 'timeline',
    description:
      'Every dated event, filtered, counted or grouped. Dates are YYYY, YYYY-MM or ' +
      'YYYY-MM-DD and `precision` says which. This is the tool for anything about sequence, ' +
      'density, what came before what, or what the board carries in a given year.',
    input_schema: {
      type: 'object',
      properties: {
        from: { type: 'string', description: 'YYYY, YYYY-MM or YYYY-MM-DD, inclusive' },
        to: { type: 'string', description: 'inclusive; a bare year means the whole year' },
        strand: { type: 'string', description: 'the lane an event is drawn in' },
        era: { type: 'string', description: '0, 1, 2, 3 or nd' },
        node: { type: 'string', description: 'events attached to this node id' },
        contains: S.contains,
        group_by: { type: 'string', description: 'year, decade, strand, era or tier' },
        count_only: S.count_only,
        limit: S.limit,
      },
    },
  },
  {
    name: 'edges',
    description:
      'Every hand-written sourced edge. Each carries a type, a claim tier and a written ' +
      'label saying what the join is. Filter by node, by the pair, by type or by tier.',
    input_schema: {
      type: 'object',
      properties: {
        node: { type: 'string', description: 'every edge touching this node id' },
        other: { type: 'string', description: 'with `node`, only edges between the two' },
        type: { type: 'string', description: 'the edge type, e.g. custody, programmatic, funding' },
        max_tier: { type: 'integer', description: '1 keeps only documented edges' },
        contains: S.contains,
        group_by: { type: 'string', description: 'type, tier or node' },
        count_only: S.count_only,
        limit: S.limit,
      },
    },
  },
  {
    name: 'path',
    description:
      'Shortest chains of sourced edges between two nodes, with every edge label and tier on ' +
      'the way. This is how a custody or money chain is traced. It walks only edges the board ' +
      'actually carries, so "no path" means the board does not join them, not that nothing does.',
    input_schema: {
      type: 'object',
      properties: {
        from: { type: 'string' },
        to: { type: 'string' },
        max_hops: { type: 'integer', description: 'default 5, up to 7' },
        max_paths: { type: 'integer', description: 'default 3, up to 8' },
        max_tier: { type: 'integer', description: 'only walk edges at this claim tier or stronger' },
      },
      required: ['from', 'to'],
    },
  },
  {
    name: 'thread',
    description:
      'The authored chains: lineage, custody, money, denials, wilson-davis, patents, ' +
      'scientists, oversight. Each step names a node, a year, the evidence in prose, and the ' +
      'edge that joins it to the step before.',
    input_schema: {
      type: 'object',
      properties: { id: { type: 'string', description: 'omit for all of them in brief' } },
    },
  },
  {
    name: 'patent',
    description:
      'The Navy patents with their prosecution history, examiner, art unit, docket, ' +
      'maintenance-fee record and what the board records as absent from the file.',
    input_schema: {
      type: 'object',
      properties: { number: { type: 'string', description: 'digits only, e.g. 10144532. Omit for all of them' } },
    },
  },
  {
    name: 'foia',
    description:
      'The drafted FOIA requests, the agency each goes to, its filing status and the open ' +
      'questions on which nodes it would close. None has been filed.',
    input_schema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'a request id, e.g. F1' },
        node: { type: 'string', description: 'requests touching this node id' },
      },
    },
  },
  {
    name: 'map',
    description:
      'RETIRED. The program map was replaced by the Atlas of topics on 26 September 2026 ' +
      '(redesign phase 11); calling this says so and names the tools that answer instead. ' +
      'Use `nodes` with `era` for when, `edges` and `node` for what surrounds a node.',
    input_schema: {
      type: 'object',
      properties: {
        cell: { type: 'string', description: 'a cell id, band.era, e.g. custody.2' },
        band: { type: 'string' },
        era: { type: 'string' },
        denials: { type: 'boolean', description: 'true returns the denial pairs instead of the grid' },
      },
    },
  },
];

export const TOOL_NAMES = TOOLS.map((t) => t.name);

/* ==========================================================================
   The executors
   ========================================================================== */

type Args = Record<string, unknown>;

export async function runTool(name: string, args: Args): Promise<string> {
  switch (name) {
    case 'overview': return await tOverview();
    case 'find': return await tFind(args);
    case 'nodes': return await tNodes(args);
    case 'node': return await tNode(args);
    case 'claims': return await tClaims(args);
    case 'timeline': return await tTimeline(args);
    case 'edges': return await tEdges(args);
    case 'path': return await tPath(args);
    case 'thread': return await tThread(args);
    case 'patent': return await tPatent(args);
    case 'foia': return await tFoia(args);
    case 'map': return await tMap(args);
    default:
      return 'No tool called `' + name + '` exists on this board. The tools are: ' +
        TOOL_NAMES.join(', ') + '.';
  }
}

/* ---- overview ------------------------------------------------------------ */

async function tOverview(): Promise<string> {
  const [idx, threads, pat] = await Promise.all([
    loadIndex(), loadThreads().catch(() => ({ threads: [] })),
    loadPatents().catch(() => ({ patents: [] })),
  ]);
  const c = idx.counts;
  const out: string[] = [];
  out.push('BOARD, generated ' + (idx.generated || '').slice(0, 10) + ', source fingerprint ' + (idx.source || '?'));
  out.push('nodes ' + c.nodes + ' (people ' + c.people + ', entities ' + c.entities + ')');
  out.push('sourced edges ' + c.edges);
  out.push('claims ' + (c.claims['1'] + c.claims['2'] + c.claims['3']) +
    ' (T1 ' + c.claims['1'] + ', T2 ' + c.claims['2'] + ', T3 ' + c.claims['3'] + ')');
  out.push('timeline events ' + c.timeline);
  out.push('program map: retired on 26 September 2026; the Atlas of topics replaced it');
  out.push('threads ' + c.threads + ' · patents ' + c.patents + ' · drawing sheets ' + c.sheets);
  out.push('FOIA ' + c.foia.requests + ' drafted requests on ' + c.foia.questions +
    ' open questions across ' + c.foia.nodes + ' nodes. None filed.');
  out.push('');
  out.push('ERAS: ' + idx.eras.map((e) => e.id + '=' + e.label + ' (' + e.sub + ')').join(' · '));
  out.push('CLASSES: ' + idx.classes.map((x) => x.id).join(' · '));
  out.push('CLUSTERS: ' + idx.clusters.map((x) => x.id).join(' · '));
  out.push('');
  const ths = (threads as { threads?: { id: string; label: string; steps: unknown[] }[] }).threads || [];
  if (ths.length) {
    out.push('THREADS: ' + ths.map((t) => t.id + ' (' + t.label + ', ' + t.steps.length + ' steps)').join(' · '));
  }
  const ps = (pat as { patents?: { number: string; title: string; status?: string }[] }).patents || [];
  if (ps.length) {
    out.push('PATENTS:');
    for (const p of ps) out.push('  ' + p.number + ' | ' + clip(p.title, 90) + ' | ' + (p.status || 'status not recorded'));
  }
  const flags = idx.nodes.filter((n) => n.hl != null).sort((a, b) => (a.hl || 0) - (b.hl || 0));
  if (flags.length) {
    out.push('');
    out.push('START HERE, the owner\'s reading order:');
    for (const f of flags) out.push('  ' + f.hl + '. ' + f.id + ' | ' + clip(f.short || f.label, 70));
  }
  return cap(out.join('\n'), 'overview');
}

/* ---- find ---------------------------------------------------------------- */

const STOP = new Set(['the', 'a', 'an', 'of', 'and', 'or', 'to', 'in', 'on', 'is', 'was',
  'for', 'with', 'at', 'by', 'from', 'that', 'this', 'it', 'as', 'be', 'are', 'what', 'which',
  'who', 'how', 'does', 'did', 'do', 'any', 'all', 'me', 'show', 'tell']);

function terms(q: string): string[] {
  return [...new Set(lower(q).split(/[^a-z0-9]+/).filter((w) => w.length > 1 && !STOP.has(w)))];
}

/* Score a haystack against the query. The head (a label, an id, a title) is
   worth three times the body, and the whole query appearing verbatim anywhere is
   worth another three, so an exact name beats a page that mentions every word. */
function score(ts: string[], phrase: string, head: string, body: string): number {
  const H = ' ' + head.toLowerCase() + ' ', B = ' ' + body.toLowerCase() + ' ';
  let s = 0;
  for (const t of ts) {
    if (H.includes(t)) s += 3;
    else if (B.includes(t)) s += 1;
  }
  if (!s) return 0;
  if (phrase.length > 3) {
    if (H.includes(phrase)) s += 6;
    else if (B.includes(phrase)) s += 3;
  }
  return s;
}

async function tFind(a: Args): Promise<string> {
  const q = str(a.query);
  if (!q) return 'find needs a `query`.';
  const ts = terms(q);
  if (!ts.length) return 'The query `' + q + '` is only common words; give find something specific to look for.';
  const phrase = lower(q);
  const limit = num(a.limit, 20, 1, HARD_LIMIT);
  const want = new Set(strList(a.kinds).map((k) => k.toLowerCase()));
  const on = (k: string) => want.size === 0 || want.has(k);

  const hits: { s: number; kind: string; line: string }[] = [];
  const push = (s: number, kind: string, line: string) => { if (s > 0) hits.push({ s, kind, line }); };

  const jobs: Promise<void>[] = [];

  if (on('node')) jobs.push(loadIndex().then((idx) => {
    for (const n of idx.nodes) {
      push(score(ts, phrase, n.id + ' ' + n.label + ' ' + (n.short || ''), n.cls + ' ' + n.cluster),
        'node', nodeLine(n));
    }
  }));

  if (on('claim')) jobs.push(loadClaims().then((rows) => {
    for (const r of rows) {
      push(score(ts, phrase, r.label, r.text + ' ' + (r.source ? r.source.text : '')),
        'claim', r.node + ' T' + r.tier + ': ' + clip(r.text, 240) +
        (r.source && r.source.text ? '  [' + clip(r.source.text, 110) + ']' : ''));
    }
  }).catch(() => undefined));

  if (on('timeline')) jobs.push(loadTimeline().then((evs) => {
    for (const e of evs) {
      push(score(ts, phrase, e.label, e.text || ''),
        'timeline', e.date + ' | ' + clip(e.label, 90) + (e.node ? ' | node ' + e.node : '') +
        (e.text ? ' | ' + clip(e.text, 180) : ''));
    }
  }).catch(() => undefined));

  if (on('edge')) jobs.push(loadEdges().then((es) => {
    for (const e of es) {
      push(score(ts, phrase, e.a + ' ' + e.b, e.label || ''),
        'edge', e.a + ' -> ' + e.b + ' [' + e.t + ', T' + (e.tier ?? '?') + '] ' + clip(e.label, 150));
    }
  }).catch(() => undefined));

  if (on('thread')) jobs.push(loadThreads().then((tf) => {
    for (const t of tf.threads || []) {
      const body = t.blurb + ' ' + (t.steps || []).map((s) => s.evidence).join(' ');
      push(score(ts, phrase, t.label + ' ' + t.id, body),
        'thread', t.id + ' | ' + t.label + ' | ' + (t.steps || []).length + ' steps | ' + clip(t.blurb, 200));
    }
  }).catch(() => undefined));

  if (on('patent')) jobs.push(loadPatents().then((pf) => {
    for (const p of pf.patents || []) {
      const body = (p.sub || '') + ' ' + (p.prosecution || []).map((x) => x.label + ' ' + (x.note || '')).join(' ');
      push(score(ts, phrase, p.number + ' ' + p.title, body),
        'patent', p.number + ' | ' + clip(p.title, 110) + (p.node ? ' | node ' + p.node : ''));
    }
  }).catch(() => undefined));

  if (on('foia')) jobs.push(loadFoia().then((ff) => {
    for (const r of ff.requests || []) {
      push(score(ts, phrase, (r.id || '') + ' ' + (r.title || ''), (r.agency || '') + ' ' + (r.sendTo || '')),
        'foia', r.id + ' | ' + (r.agency || 'agency not recorded') + ' | ' + clip(r.title, 120) +
        ' | ' + (r.status || 'status not recorded'));
    }
  }).catch(() => undefined));

  await Promise.all(jobs);
  hits.sort((x, y) => y.s - x.s);
  const top = hits.slice(0, limit);
  if (!top.length) return 'Nothing on the board matches `' + q + '`.';

  const by = new Map<string, string[]>();
  for (const hp of top) {
    let arr = by.get(hp.kind);
    if (!arr) { arr = []; by.set(hp.kind, arr); }
    arr.push('  ' + hp.line);
  }
  const out = ['FIND `' + q + '` — ' + hits.length + ' hits, strongest ' + top.length + ' shown.'];
  for (const [k, lines] of by) { out.push(''); out.push(k.toUpperCase() + ':'); out.push(...lines); }
  return cap(out.join('\n'), 'find');
}

/* ---- nodes --------------------------------------------------------------- */

async function tNodes(a: Args): Promise<string> {
  const idx = await loadIndex();
  const cls = lower(a.cls), cluster = lower(a.cluster), tier = lower(a.tier);
  const era = lower(a.era), lab = lower(a.label_contains);
  /* the map's bands and its on-map flag went with the map: say so rather than
     filter on a field no node carries any more */
  if (lower(a.band) || bool(a.on_map) !== null || lower(a.group_by) === 'band') {
    return RETIRED + '. No node carries a band or an on-map flag now; ask again without `band`, `on_map` or `group_by: band`.';
  }
  const from = floorDate(str(a.date_from)), to = ceilDate(str(a.date_to));
  const minDeg = a.min_degree == null ? null : num(a.min_degree, 0, 0, 100000);
  const minT1 = a.min_t1 == null ? null : num(a.min_t1, 0, 0, 100000);
  const maxT1 = a.max_t1 == null ? null : num(a.max_t1, 0, 0, 100000);

  let rows = idx.nodes.filter((n) => {
    if (cls && n.cls.toLowerCase() !== cls) return false;
    if (cluster && (n.cluster || '').toLowerCase() !== cluster) return false;
    if (tier && (n.tier || '').toLowerCase() !== tier) return false;
    if (era && String(n.era).toLowerCase() !== era) return false;
    if (lab && !(n.label + ' ' + (n.short || '') + ' ' + n.id).toLowerCase().includes(lab)) return false;
    if (from && !(n.dateStart && n.dateStart >= from)) return false;
    if (to && !(n.dateStart && n.dateStart <= to)) return false;
    if (minDeg !== null && n.deg < minDeg) return false;
    if (minT1 !== null && n.claims[0] < minT1) return false;
    if (maxT1 !== null && n.claims[0] > maxT1) return false;
    return true;
  });

  const head = 'NODES matching — ' + rows.length + ' of ' + idx.nodes.length;
  const gb = lower(a.group_by);
  if (gb) {
    const key = (n: IndexNode): string =>
      gb === 'cls' ? n.cls
        : gb === 'cluster' ? (n.cluster || 'none')
          : gb === 'tier' ? (n.tier || 'none')
              : gb === 'era' ? n.era + ' ' + (idx.eras.find((e) => e.id === n.era)?.label || '')
                : gb === 'decade' ? (n.dateStart ? n.dateStart.slice(0, 3) + '0s' : 'undated')
                  : '(group_by ' + gb + ' is not one of cls, cluster, tier, era, decade)';
    return cap(head + ', grouped by ' + gb + ':\n' + tally(rows.map(key)), 'grouping');
  }
  if (bool(a.count_only)) return head + '.';

  const sort = lower(a.sort) || 'degree';
  const cmp: Record<string, (x: IndexNode, y: IndexNode) => number> = {
    degree: (x, y) => y.deg - x.deg,
    claims: (x, y) => (y.claims[0] + y.claims[1] + y.claims[2]) - (x.claims[0] + x.claims[1] + x.claims[2]),
    t1: (x, y) => y.claims[0] - x.claims[0],
    date: (x, y) => (x.dateStart || '9999').localeCompare(y.dateStart || '9999'),
    label: (x, y) => x.label.localeCompare(y.label),
  };
  rows = rows.slice().sort(cmp[sort] || cmp.degree);
  const limit = num(a.limit, DEFAULT_LIMIT, 1, HARD_LIMIT);
  const shown = rows.slice(0, limit);
  return cap(head + ', sorted by ' + sort + ', ' + shown.length + ' shown:\n' +
    shown.map((n) => '  ' + nodeLine(n)).join('\n'), 'node list');
}

/* ---- node ---------------------------------------------------------------- */

async function tNode(a: Args): Promise<string> {
  const ids = strList(a.ids).slice(0, MAX_NODE_IDS);
  if (!ids.length) return 'node needs `ids`, a list of node ids.';
  const sections = new Set(strList(a.sections).map((s) => s.toLowerCase()));
  const want = (s: string) => sections.size === 0 || sections.has(s);
  const maxClaims = num(a.max_claims, 40, 1, 200);
  const maxEdges = num(a.max_edges, 60, 1, 300);

  const out: string[] = [];
  for (const id of ids) {
    let rec;
    try { rec = await loadNode(id); } catch {
      out.push('NODE ' + id + ': no such node on this board. Use `find` or `nodes` to get the id right.');
      continue;
    }
    const L: string[] = [];
    L.push('NODE ' + rec.id + ' | ' + rec.label + ' | ' + rec.cls +
      (rec.cluster ? '/' + rec.cluster : '') + ' | node tier ' + (rec.tier || '?') +
      ' | C' + (rec.C ?? '?') + 'A' + (rec.A ?? '?') + 'D' + (rec.D ?? '?') +
      ' | ' + dates(rec.dateStart, rec.dateEnd));
    const d = rec.dossier || {};
    if (want('dossier')) {
      if (d.whatItIs) L.push('what it is: ' + clip(d.whatItIs, 1400));
      if (d.whyImplicated) L.push('why implicated: ' + clip(d.whyImplicated, 1400));
      if (d.narrative) L.push('narrative: ' + clip(d.narrative, 1400));
      if (d.denialPosture) L.push('denial posture: ' + clip(d.denialPosture, 600));
      if (rec.tierRationale) L.push('tier rationale: ' + clip(rec.tierRationale, 400));
      if (d.roles && d.roles.length) L.push('roles: ' + d.roles.join(', '));
      if (!d.whatItIs && !d.whyImplicated && !rec.desc) L.push('(this node carries no dossier)');
      else if (!d.whatItIs && rec.desc) L.push('description: ' + clip(rec.desc, 800));
    }
    if (want('claims')) {
      const cl = (rec.claims || []).slice().sort((x, y) => (x.tier || 3) - (y.tier || 3));
      if (cl.length) {
        L.push('claims, ' + cl.length + ' in all, strongest first' +
          (cl.length > maxClaims ? ', ' + maxClaims + ' shown' : '') + ':');
        for (const c of cl.slice(0, maxClaims)) {
          const src = claimSourceText(c.source);
          L.push('  T' + c.tier + ': ' + clip(c.text, 520) + (src ? '  [' + clip(src, 180) + ']' : '  [no source recorded]'));
        }
      } else L.push('claims: none on this node');
    }
    if (want('edges')) {
      const cn = rec.connections || [];
      if (cn.length) {
        L.push('sourced edges, ' + cn.length + ' distinct neighbours' +
          (cn.length > maxEdges ? ', ' + maxEdges + ' shown' : '') + ':');
        for (const c of cn.slice(0, maxEdges)) {
          L.push('  ' + (c.direction === 'in' ? c.id + ' -> ' + rec.id : rec.id + ' -> ' + c.id) +
            ' [' + c.type + ', T' + (c.claimTier ?? '?') + '] ' + clip(c.edgeLabel || c.label, 140) +
            (c.note ? ' -- ' + clip(c.note, 260) : ''));
        }
      } else L.push('sourced edges: none');
    }
    if (want('denials') && rec.denials && rec.denials.length) {
      L.push('denials on the record:');
      for (const x of rec.denials) {
        /* by/of are null where the adjudication names no denier (phase 3); the
           wording of this tool is phase 12's, this only keeps it from crashing */
        L.push(x.by && x.of
          ? '  ' + x.by.label + ' (' + x.by.id + ') denies ' + x.of.label + ' (' + x.of.id + '): ' + clip(x.label, 260)
          : '  ' + x.a.label + ' (' + x.a.id + ') / ' + x.b.label + ' (' + x.b.id + '), ' +
            (x.denialKind || 'direction not adjudicated') + ': ' + clip(x.label, 260));
      }
    }
    if (want('timeline') && rec.timeline && rec.timeline.length) {
      L.push('its timeline, ' + rec.timeline.length + ' events:');
      for (const e of rec.timeline.slice(0, 40)) L.push('  ' + e.date + ' ' + clip(e.label, 120));
    }
    if (want('questions') && d.openQuestions && d.openQuestions.length) {
      L.push('open questions, ' + d.openQuestions.length + ':');
      d.openQuestions.forEach((q, i) => L.push('  [' + i + '] ' + clip(q, 300)));
    }
    if (want('foia') && rec.foia && rec.foia.requests && rec.foia.requests.length) {
      L.push('FOIA requests that would close questions here:');
      for (const r of rec.foia.requests) {
        L.push('  ' + r.request + ' | ' + (r.agency || '?') + ' | ' + clip(r.title || '', 120) +
          ' | ' + (r.status || 'status not recorded') +
          (r.questions && r.questions.length ? ' | closes questions ' + r.questions.join(', ') : ''));
      }
    }
    /* `members` (the people and documents a map node rolled up) went with the
       program map in redesign phase 11; a node's neighbours are its edges. */
    if (rec.unverified) {
      const u = Array.isArray(rec.unverified) ? rec.unverified : [String(rec.unverified)];
      if (u.length) L.push('recorded as unverified: ' + u.map((x) => clip(x, 200)).join(' · '));
    }
    out.push(L.join('\n'));
  }
  return cap(out.join('\n\n'), 'node records');
}

/* ---- claims -------------------------------------------------------------- */

async function tClaims(a: Args): Promise<string> {
  const rows = await loadClaims();
  const tier = a.tier == null ? null : num(a.tier, 0, 1, 3);
  const node = lower(a.node), cls = lower(a.cls), cluster = lower(a.cluster);
  const contains = lower(a.contains), srcHas = lower(a.source_contains);
  const denied = bool(a.denied), open = bool(a.open), hasUrl = bool(a.has_url);

  const keep = rows.filter((r: ClaimRow) => {
    if (tier !== null && r.tier !== tier) return false;
    if (node && r.node.toLowerCase() !== node) return false;
    if (cls && r.cls.toLowerCase() !== cls) return false;
    if (cluster && (r.cluster || '').toLowerCase() !== cluster) return false;
    if (denied !== null && r.denied !== denied) return false;
    if (open !== null && r.open !== open) return false;
    if (contains && !r.text.toLowerCase().includes(contains)) return false;
    if (srcHas && !((r.source.text || '') + ' ' + (r.source.url || '')).toLowerCase().includes(srcHas)) return false;
    if (hasUrl !== null && Boolean(r.source.url) !== hasUrl) return false;
    return true;
  });

  const head = 'CLAIMS matching — ' + keep.length + ' of ' + rows.length;
  const gb = lower(a.group_by);
  if (gb) {
    const key = (r: ClaimRow): string =>
      gb === 'tier' ? 'T' + r.tier
        : gb === 'node' ? r.node + ' (' + clip(r.label, 50) + ')'
          : gb === 'cls' ? r.cls
            : gb === 'cluster' ? (r.cluster || 'none')
              : gb === 'domain' ? (r.source.domain || (r.source.url ? 'url, domain not recorded' : 'no url'))
                : '(group_by ' + gb + ' is not one of tier, node, cls, cluster, domain)';
    return cap(head + ', grouped by ' + gb + ':\n' + tally(keep.map(key)), 'grouping');
  }
  if (bool(a.count_only)) {
    const byTier = tally(keep.map((r) => 'T' + r.tier));
    return head + '.\nby tier:\n' + byTier;
  }
  const limit = num(a.limit, DEFAULT_LIMIT, 1, HARD_LIMIT);
  const shown = keep.slice().sort((x, y) => x.tier - y.tier).slice(0, limit);
  return cap(head + ', ' + shown.length + ' shown, strongest first:\n' + shown.map((r) =>
    '  ' + r.node + ' T' + r.tier + (r.denied ? ' [denied]' : '') + (r.open ? ' [open question]' : '') +
    ': ' + clip(r.text, 400) +
    '  [' + (r.source.text ? clip(r.source.text, 150) : 'no source recorded') + ']').join('\n'), 'claim list');
}

/* ---- timeline ------------------------------------------------------------ */

async function tTimeline(a: Args): Promise<string> {
  const evs = await loadTimeline();
  const from = floorDate(str(a.from)), to = ceilDate(str(a.to));
  const strand = lower(a.strand), era = lower(a.era), node = lower(a.node), contains = lower(a.contains);

  const keep = evs.filter((e: TimelineEvent) => {
    if (from && ceilDate(e.date) < from) return false;
    if (to && floorDate(e.date) > to) return false;
    if (strand && (e.strand || '').toLowerCase() !== strand) return false;
    if (era && String(e.era || '').toLowerCase() !== era) return false;
    if (node && (e.node || '').toLowerCase() !== node) return false;
    if (contains && !((e.label || '') + ' ' + (e.text || '')).toLowerCase().includes(contains)) return false;
    return true;
  });

  const head = 'TIMELINE matching — ' + keep.length + ' of ' + evs.length + ' events';
  const gb = lower(a.group_by);
  if (gb) {
    const key = (e: TimelineEvent): string =>
      gb === 'year' ? e.date.slice(0, 4)
        : gb === 'decade' ? e.date.slice(0, 3) + '0s'
          : gb === 'strand' ? (e.strand || 'none')
            : gb === 'era' ? String(e.era || 'none')
              : gb === 'tier' ? (e.grade || (e.claimTier != null ? 'T' + e.claimTier : 'none'))
                : '(group_by ' + gb + ' is not one of year, decade, strand, era, tier)';
    const rows = keep.map(key);
    const body = gb === 'year' || gb === 'decade'
      ? [...new Set(rows)].sort().map((k) => '  ' + rows.filter((r) => r === k).length + '  ' + k).join('\n')
      : tally(rows);
    return cap(head + ', grouped by ' + gb + ':\n' + body, 'grouping');
  }
  if (bool(a.count_only)) return head + '.';

  const limit = num(a.limit, DEFAULT_LIMIT, 1, HARD_LIMIT);
  const shown = keep.slice().sort((x, y) => x.date.localeCompare(y.date)).slice(0, limit);
  return cap(head + ', ' + shown.length + ' shown, earliest first:\n' + shown.map((e) =>
    '  ' + e.date + ' (' + (e.precision || '?') + ') | ' + (e.strand || '?') + ' | ' + clip(e.label, 110) +
    (e.node ? ' | node ' + e.node : '') + (e.text ? '\n      ' + clip(e.text, 300) : '')).join('\n'), 'timeline');
}

/* ---- edges --------------------------------------------------------------- */

async function tEdges(a: Args): Promise<string> {
  const es = await loadEdges();
  const node = lower(a.node), other = lower(a.other), type = lower(a.type), contains = lower(a.contains);
  const maxTier = a.max_tier == null ? null : num(a.max_tier, 3, 1, 3);

  const keep = es.filter((e: EdgeRow) => {
    if (node && e.a.toLowerCase() !== node && e.b.toLowerCase() !== node) return false;
    if (other && e.a.toLowerCase() !== other && e.b.toLowerCase() !== other) return false;
    if (type && (e.t || '').toLowerCase() !== type) return false;
    if (maxTier !== null && (e.tier == null || e.tier > maxTier)) return false;
    if (contains && !((e.label || '') + ' ' + e.a + ' ' + e.b).toLowerCase().includes(contains)) return false;
    return true;
  });

  const head = 'EDGES matching — ' + keep.length + ' of ' + es.length;
  const gb = lower(a.group_by);
  if (gb) {
    const key = (e: EdgeRow): string =>
      gb === 'type' ? e.t
        : gb === 'tier' ? 'T' + (e.tier ?? '?')
          : gb === 'node' ? e.a + ' / ' + e.b
            : '(group_by ' + gb + ' is not one of type, tier, node)';
    return cap(head + ', grouped by ' + gb + ':\n' + tally(keep.map(key)), 'grouping');
  }
  if (bool(a.count_only)) return head + '.';

  const limit = num(a.limit, DEFAULT_LIMIT, 1, HARD_LIMIT);
  const shown = keep.slice().sort((x, y) => (x.tier ?? 9) - (y.tier ?? 9)).slice(0, limit);
  return cap(head + ', ' + shown.length + ' shown, strongest first:\n' + shown.map((e) =>
    '  ' + e.a + ' -> ' + e.b + ' [' + e.t + ', T' + (e.tier ?? '?') + ']' +
    (e.dateStart ? ' ' + e.dateStart : '') + ' ' + clip(e.label, 220)).join('\n'), 'edge list');
}

/* ---- path ---------------------------------------------------------------- */
/* Breadth first over the sourced edge list, so the first paths found are the
   shortest. It walks the edges the board carries and nothing else: a pair with
   no path here is a pair the record does not join, which is itself an answer. */

async function tPath(a: Args): Promise<string> {
  const from = lower(a.from), to = lower(a.to);
  if (!from || !to) return 'path needs `from` and `to`, both node ids.';
  const [idx, es] = await Promise.all([loadIndex(), loadEdges()]);
  const ids = new Set(idx.nodes.map((n) => n.id));
  const missing = [from, to].filter((x) => !ids.has(x));
  if (missing.length) return 'Not a node on this board: ' + missing.join(', ') + '. Use `find` to get the id right.';
  if (from === to) return from + ' and ' + to + ' are the same node.';

  const maxTier = a.max_tier == null ? null : num(a.max_tier, 3, 1, 3);
  const maxHops = num(a.max_hops, 5, 1, 7);
  const maxPaths = num(a.max_paths, 3, 1, 8);

  const adj = new Map<string, { to: string; e: EdgeRow }[]>();
  for (const e of es) {
    if (maxTier !== null && (e.tier == null || e.tier > maxTier)) continue;
    let x = adj.get(e.a); if (!x) { x = []; adj.set(e.a, x); } x.push({ to: e.b, e });
    let y = adj.get(e.b); if (!y) { y = []; adj.set(e.b, y); } y.push({ to: e.a, e });
  }

  const found: { to: string; e: EdgeRow }[][] = [];
  let frontier: { node: string; trail: { to: string; e: EdgeRow }[]; seen: Set<string> }[] =
    [{ node: from, trail: [], seen: new Set([from]) }];
  for (let hop = 0; hop < maxHops && found.length < maxPaths && frontier.length; hop++) {
    const next: typeof frontier = [];
    for (const f of frontier) {
      for (const step of adj.get(f.node) || []) {
        if (f.seen.has(step.to)) continue;
        const trail = f.trail.concat([step]);
        if (step.to === to) { found.push(trail); if (found.length >= maxPaths) break; continue; }
        if (next.length < 40000) {
          const seen = new Set(f.seen); seen.add(step.to);
          next.push({ node: step.to, trail, seen });
        }
      }
      if (found.length >= maxPaths) break;
    }
    if (found.length) break;     /* shortest only: stop at the first hop that lands */
    frontier = next;
  }

  const label = new Map(idx.nodes.map((n) => [n.id, n.short || n.label]));
  if (!found.length) {
    return 'No chain of ' + (maxTier ? 'Tier ' + maxTier + ' or stronger ' : '') + 'sourced edges joins ' +
      from + ' to ' + to + ' within ' + maxHops + ' hops. The board does not join them. ' +
      'That is a fact about the record, not about the world.';
  }
  const out = ['PATH ' + from + ' -> ' + to + ': ' + found.length + ' chain(s) of ' +
    found[0].length + ' hop(s), the shortest the board carries.'];
  found.forEach((trail, i) => {
    out.push('');
    out.push('chain ' + (i + 1) + ': ' + from + ' (' + clip(label.get(from), 60) + ')');
    let at = from;
    for (const step of trail) {
      out.push('  --[' + step.e.t + ', T' + (step.e.tier ?? '?') + '] ' + clip(step.e.label, 200));
      out.push('  -> ' + step.to + ' (' + clip(label.get(step.to), 60) + ')');
      at = step.to;
    }
    void at;
  });
  return cap(out.join('\n'), 'paths');
}

/* ---- thread -------------------------------------------------------------- */

async function tThread(a: Args): Promise<string> {
  const tf = await loadThreads();
  const all = tf.threads || [];
  const id = lower(a.id);
  if (!id) {
    return cap('THREADS, all ' + all.length + ':\n' + all.map((t) =>
      '  ' + t.id + ' | ' + t.label + ' | ' + t.steps.length + ' steps | ' +
      t.steps.map((s) => s.node).join(' -> ') + '\n      ' + clip(t.blurb, 300)).join('\n'), 'threads');
  }
  const t = all.find((x) => x.id.toLowerCase() === id);
  if (!t) return 'No thread called `' + id + '`. The eight are: ' + all.map((x) => x.id).join(', ') + '.';
  const out = ['THREAD ' + t.id + ' | ' + t.label + (t.title ? ' | ' + t.title : ''), t.blurb, ''];
  t.steps.forEach((s, i) => {
    if (s.edge) {
      out.push('  --[' + s.edge.type + ', ' + s.edge.kind + ', T' + (s.edge.tier ?? '?') + ']' +
        (s.edge.via && s.edge.via.length ? ' via ' + s.edge.via.join(', ') : ''));
    }
    out.push('step ' + (i + 1) + ': ' + s.node + (s.year ? ' (' + s.year + ')' : ''));
    out.push('  ' + clip(s.evidence, 900));
  });
  return cap(out.join('\n'), 'thread');
}

/* ---- patent -------------------------------------------------------------- */

async function tPatent(a: Args): Promise<string> {
  const pf = await loadPatents();
  const all = pf.patents || [];
  const want = str(a.number).replace(/[^0-9]/g, '');
  const list = want ? all.filter((p) => String(p.number).replace(/[^0-9]/g, '') === want) : all;
  if (!list.length) {
    return 'No patent numbered ' + want + '. The five are: ' + all.map((p) => p.number).join(', ') + '.';
  }
  const out: string[] = [];
  for (const p of list) {
    const L = ['PATENT ' + p.number + ' | ' + p.title];
    if (p.sub) L.push(clip(p.sub, 500));
    L.push('application ' + (p.application || 'not recorded') +
      ' | docket ' + (p.docket || 'not recorded') +
      ' | examiner ' + (p.examiner || 'not recorded') +
      (p.supervisor ? ' | supervisor ' + p.supervisor : '') +
      ' | art unit ' + ((p.artUnits || []).join(', ') || 'not recorded'));
    L.push('filed ' + (p.filed || '-') + ' | published ' + (p.published || '-') +
      ' | granted ' + (p.granted || 'not granted, this is an application') +
      ' | expired ' + (p.expired || '-') + ' | status ' + (p.status || 'not recorded'));
    if (p.node) L.push('board node: ' + p.node);
    if (p.fee) L.push('fee record: ' + (p.fee.title || '') + ' — ' + (p.fee.finding || '') +
      (p.fee.lapsed ? ', lapsed ' + p.fee.lapsed : ''));
    if (p.prosecution && p.prosecution.length) {
      L.push('prosecution history, ' + p.prosecution.length + ' entries:');
      for (const e of p.prosecution) {
        L.push('  ' + e.date + ' [' + e.kind + '] ' + e.label + (e.note ? ' — ' + clip(e.note, 260) : ''));
      }
    }
    if (p.absent && p.absent.length) {
      L.push('recorded as ABSENT from the file: ' + p.absent.map((x) => clip(x, 200)).join(' · '));
    }
    out.push(L.join('\n'));
  }
  return cap(out.join('\n\n'), 'patents');
}

/* ---- foia ---------------------------------------------------------------- */

async function tFoia(a: Args): Promise<string> {
  const ff = await loadFoia();
  const reqs = ff.requests || [];
  const id = lower(a.id), node = lower(a.node);
  let list = reqs;
  if (id) list = list.filter((r) => (r.id || '').toLowerCase() === id);
  if (node) list = list.filter((r) => (r.nodes || []).some((n) => n.node.toLowerCase() === node));
  if (!list.length) {
    return 'No FOIA request matches' + (id ? ' id ' + id : '') + (node ? ' node ' + node : '') +
      '. There are ' + reqs.length + ' drafted requests: ' + reqs.map((r) => r.id).join(', ') + '.';
  }
  const out = ['FOIA — ' + list.length + ' of ' + reqs.length + ' drafted requests. None has been filed.'];
  for (const r of list) {
    out.push('');
    out.push(r.id + ' | ' + (r.agency || 'agency not recorded') + ' | ' + (r.status || 'status not recorded'));
    if (r.title) out.push('  ' + clip(r.title, 400));
    if (r.sendTo) out.push('  send to: ' + clip(r.sendTo, 400));
    const ns = r.nodes || [];
    if (ns.length) {
      out.push('  closes questions on ' + ns.length + ' node(s):');
      for (const n of ns.slice(0, 40)) {
        out.push('    ' + n.node + ' questions ' + (n.questions || []).join(', ') +
          (n.partial && n.partial.length ? ' (partial: ' + n.partial.join(', ') + ')' : ''));
      }
    }
  }
  return cap(out.join('\n'), 'foia');
}

/* ---- map ----------------------------------------------------------------- */
/* Retired in redesign phase 11 with the program map. The tool keeps its name and
   its argument schema, so TOOLS_VERSION and the Worker's allowlist are
   unchanged; it answers that the map is gone and names what answers instead. */
const RETIRED = 'The program map was retired on 26 September 2026 (redesign phase 11) and the Atlas of topics replaced it';


async function tMap(_a: Args): Promise<string> {
  return RETIRED + '. There is no map left to describe. For when a node sits, use `nodes` with ' +
    '`era` or `group_by: era`; for what surrounds a node, `node` and `edges`; for how two ' +
    'nodes connect, `path`; for the denials on the board, `edges` with its type filter.';
}
