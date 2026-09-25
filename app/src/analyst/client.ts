/* analyst/client.ts: the analyst's conversation, including the tool loop.
 *
 * Three things are sent and nothing else:
 *
 *   tools    the twelve in ./tools, pinned by name in the Worker. They execute
 *            HERE, in this browser, against the same /data the pages read.
 *   system   two blocks. The first is the case index and the standing
 *            instructions, byte-stable between turns and marked
 *            cache_control ephemeral with a one hour TTL, so every turn after
 *            the first reads it from the API's cache instead of paying for it.
 *            The second is CURRENT STATE, which changes with the route and is
 *            therefore left uncached and sent last.
 *   messages the conversation, including the assistant's own tool_use blocks
 *            and this page's tool_result blocks, verbatim.
 *
 * WHY THE WIRE HISTORY IS KEPT SEPARATELY FROM THE TRANSCRIPT
 * ----------------------------------------------------------
 * Extended thinking plus tool use means the assistant turn that asks for a tool
 * carries a signed `thinking` block, and the API requires it back unchanged
 * alongside the tool results. So `wire` holds the API's own message objects,
 * echoed exactly, and `Turn[]` holds only what a reader sees. Trimming `wire`
 * is done at a plain user message, never inside a tool exchange, because half a
 * tool exchange is a 400.
 *
 * The Worker is the only runtime request this app makes that is not same-origin.
 */
import { loadAnalyst, loadIndex, loadMap, loadThreads, type MapFile, type ThreadsFile } from '../data';
import { TOOLS, TOOLS_VERSION, runTool } from './tools';
import { caseState } from './state';
import type { Route } from '../router';

const AN_INDEX_CAP = 220000;
const TIMEOUT_MS = 240000;     /* one round trip, not the whole loop          */
const MAX_ROUNDS = 14;         /* tool rounds per question                    */
const MAX_WIRE = 40;           /* messages kept on the wire                   */

export interface Turn {
  role: 'you' | 'analyst';
  text: string;
  err?: boolean;
  thinking?: boolean;
  /* what the analyst went and read, in the order it read it */
  steps?: string[];
  usage?: { in: number; cached: number; out: number; rounds: number };
}

/* The API's own shapes, only as far as this file needs them. */
type Block = { type: string; [k: string]: unknown };
type WireMsg = { role: 'user' | 'assistant'; content: string | Block[] };

let endpoint: string | null = null;
let health: { live: boolean; tools?: string; model?: string } | null = null;
/* The PROMISE, not a boolean. A `probed = true` flag set on entry meant a
   question asked while the probe was still in flight saw probed === true and
   endpoint === null, and was answered "the analyst endpoint is not reachable
   from this deployment" by a deployment where it was perfectly reachable. Found
   by driving a real question at the live Worker, not by reading this. */
let probing: Promise<string | null> | null = null;

/* The wire history survives route changes, which is the point: a reader can ask
   on the map, walk to a node and ask a follow-up. */
const wire: WireMsg[] = [];

export function resetConversation(): void { wire.length = 0; }

function clip(s: unknown, n: number): string {
  const str = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  return str.length > n ? str.slice(0, n - 3) + '...' : str;
}

/* ---- the stable half ----------------------------------------------------- */
/* Byte-identical between turns, which is what makes the cache worth marking.
   Nothing here may carry a date, a route, a node or a random id. */

const HEAD =
  'You are the analyst on a sourced research board about the alleged US legacy UAP ' +
  'recovery and reverse-engineering programme, 1944 to now.\n\n' +
  'TWO GRADING SYSTEMS, AND THEY ARE NOT THE SAME ONE.\n' +
  'Claim tiers 1-3 are evidence strength, 1 strongest: T1 documented, T2 a named person ' +
  'on the record, T3 a stated inference. Node tiers A/B/C are proximity to the programme, ' +
  'NOT credibility: a Tier A node carrying only T3 claims is not a contradiction, it is ' +
  'the definition of where to look next. C/A/D are custody proximity, access and ' +
  'disclosure role, scored 0 to 3.\n\n' +
  'THE RULE THAT NEVER BENDS. Never invent a source, a URL, a document number, a date or ' +
  'a quotation. If the board does not carry something, say so plainly and say what would ' +
  'settle it. An answer that says "the board does not record this" is a good answer.\n\n' +
  'YOU HAVE TOOLS AND YOU SHOULD USE THEM. The case index below is one line per node and ' +
  'nothing more. Everything else on the board -- every claim with its source, the ' +
  'timeline, the sourced edges, the threads, the patents, the FOIA requests, the ' +
  'program map -- is reachable only through the tools, and they run against the live ' +
  'data files rather than against anything in this prompt. Call `overview` when you need a count of anything: no number is written into this prompt or into a tool description, because a written-down count goes stale the next time the board grows. So:\n' +
  '  - Count with `count_only` and `group_by` rather than by eye. A list you were shown ' +
  'was probably truncated; a count never is.\n' +
  '  - Reach for `find` when you do not already know which node holds something.\n' +
  '  - Reach for `node` before saying anything specific about a node. The index line does ' +
  'not carry its claims, its sources or its denials.\n' +
  '  - Reach for `path` rather than asserting that two things are connected.\n' +
  '  - Several calls at once is normal and preferred when they do not depend on each other.\n' +
  '  - A tool that returns nothing is an answer. Report it as one.\n\n' +
  'HOW TO WRITE. Put every node id you cite in backticks, like `aawsap`, because the page ' +
  'turns those into links and checks them against the index. Lead with the answer. Give ' +
  'the tier of anything you assert and name the source the board holds for it. Say which ' +
  'of your claims rest on a single source. Prefer a short table to a long list. Do not use ' +
  'em dashes.\n\n' +
  'CASE INDEX. One line per node, all of them:\n' +
  'id | label | class | node tier | C/A/D | dates | degree | T1/T2/T3 claim counts | map band\n';

let indexBlock: Promise<string> | null = null;
function caseIndex(): Promise<string> {
  if (!indexBlock) {
    indexBlock = loadIndex().then((idx) => {
      const line = (n: typeof idx.nodes[number]) => [
        n.id, clip(n.short || n.label, 70), n.cls, 'tier ' + (n.tier || '?'),
        'C' + (n.C ?? '?') + 'A' + (n.A ?? '?') + 'D' + (n.D ?? '?'),
        (n.dateStart || '') + (n.dateEnd && n.dateEnd !== n.dateStart ? '..' + n.dateEnd : '') || 'undated',
        'deg ' + n.deg, n.claims.join('/'), n.l0 ? (n.band || 'on map') : 'off map',
      ].join(' | ');
      let out = idx.nodes.map(line).join('\n');
      if (out.length > AN_INDEX_CAP) out = out.slice(0, AN_INDEX_CAP) + '\n[index truncated]';
      return HEAD + out;
    });
  }
  return indexBlock;
}

/* ---- the endpoint -------------------------------------------------------- */

export function probeEndpoint(): Promise<string | null> {
  if (!probing) probing = probeOnce();
  return probing;
}

async function probeOnce(): Promise<string | null> {
  if (location.protocol !== 'http:' && location.protocol !== 'https:') return null;
  let worker = '';
  try { worker = (await loadAnalyst()).worker; } catch { worker = ''; }
  for (const o of ['', worker].filter((x, i) => i === 0 || x)) {
    /* A health check that never answers must not leave the dock saying
       "checking" forever: after 8 seconds this candidate counts as unreachable. */
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), 8000);
    try {
      const r = await fetch(o + '/api/analyst/health', { signal: ac.signal });
      if (!r.ok) continue;
      if (!(r.headers.get('content-type') || '').includes('json')) continue;
      const j = await r.json();
      if (j && j.live) { health = j; endpoint = o + '/api/analyst'; return endpoint; }
    } catch { /* the next candidate, or none */ } finally { clearTimeout(timer); }
  }
  return null;
}

export function endpointNow(): string | null { return endpoint; }

/* The Worker pins the tool allowlist. If its list is from another build, the
   model can ask for a tool this page cannot run, so say so rather than let the
   reader find out one dead answer at a time. */
export function toolSkew(): string | null {
  if (!health) return null;
  if (!health.tools) return 'none (a service deployed before the tools existed)';
  return health.tools === TOOLS_VERSION ? null : health.tools;
}

/* ---- the cited id guard -------------------------------------------------- */
/* The instruction above asks for backticks, so the guard reads backticked
   tokens only. It flags, it never edits: a wrong id stays visible and is
   labelled, because silently deleting it would hide the mistake. */

const ID_SHAPE = /^[a-z0-9][a-z0-9._-]*$/;

/* Everything that may legitimately appear in backticks. Node ids are the ones
   worth linking; the rest are here so the guard does not cry wolf.

   Two false verdicts on the first two live questions, and both mattered:

   1. `disclosure.3` was flagged "not a node on this board". True and useless: it
      is a map cell, `<band>.<era>`. Cells, bands, classes, clusters, threads and
      entry paths are all id-shaped and all real.
   2. Worse, and silent: the guard skipped any token without a hyphen, dot or
      digit, on the theory that a single plain word is prose. That excluded
      `aawsap`, `nicap`, `cia` and every other single-word node id on the board
      from being linked OR checked. The check caught that one; nothing on screen
      would have.

   So the rule is the other way round now: everything id-shaped in backticks is
   checked, and the legitimate non-node vocabulary is enumerated here. The tool
   names and their argument names are in it because the model writes those in
   backticks too, having been shown them in backticks. */
let known: Promise<{ nodes: Set<string>; other: Set<string> }> | null = null;
function knownIds(): Promise<{ nodes: Set<string>; other: Set<string> }> {
  if (!known) {
    known = Promise.all([
      loadIndex(),
      loadMap().catch((): MapFile => ({ entryPaths: [] })),
      loadThreads().catch((): ThreadsFile => ({ threads: [] })),
    ]).then(([idx, mp, tf]) => {
      const other = new Set<string>();
      for (const k of Object.keys(mp.cells || {})) other.add(k);
      for (const b of idx.bands) other.add(b.id);
      for (const c of idx.classes) other.add(c.id);
      for (const c of idx.clusters) other.add(c.id);
      for (const e of idx.eras) other.add(e.id);
      for (const t of tf.threads || []) other.add(t.id);
      for (const e of mp.entryPaths || []) other.add(e.id);
      for (const t of TOOLS) {
        other.add(t.name);
        for (const arg of Object.keys(t.input_schema.properties || {})) other.add(arg);
      }
      return { nodes: new Set(idx.nodes.map((n) => n.id)), other };
    });
  }
  return known;
}

export async function checkCitedIds(text: string): Promise<{ ok: string[]; bad: string[] }> {
  const k = await knownIds().catch(() => null);
  if (!k) return { ok: [], bad: [] };
  const ok = new Set<string>(), bad = new Set<string>();
  for (const m of text.matchAll(/`([^`\n]{2,80})`/g)) {
    const tok = m[1].trim();
    if (!ID_SHAPE.test(tok)) continue;         /* prose, a field path, a number */
    if (k.other.has(tok)) continue;            /* a cell, band, era, class, cluster, thread or tool */
    /* No node id on this board carries a dot, and map cells are the only dotted
       ids, which the line above has already taken. So a dotted token that is in
       neither set is a hostname or a filename: `www.govinfo.gov` and
       `archive.org` were both reported to a reader as "not a node on this
       board", which is true and is not what the sentence means. */
    if (tok.includes('.')) continue;
    (k.nodes.has(tok) ? ok : bad).add(tok);
  }
  return { ok: [...ok], bad: [...bad] };
}

/* ---- the loop ------------------------------------------------------------ */

function trimWire(): void {
  while (wire.length > MAX_WIRE) {
    /* drop from the front, but only whole exchanges: the first message that
       remains must be a plain user question, never a tool_result */
    wire.shift();
    while (wire.length && !(wire[0].role === 'user' && typeof wire[0].content === 'string')) wire.shift();
  }
}

/* One breakpoint in the messages, never more. The system block holds the other. */
function moveBreakpoint(): void {
  for (const m of wire) {
    if (typeof m.content === 'string') continue;
    for (const blk of m.content) delete blk.cache_control;
  }
}

function textOf(content: Block[]): string {
  return content.filter((b) => b.type === 'text').map((b) => String(b.text ?? '')).join('\n');
}

function describeCall(name: string, input: Record<string, unknown>): string {
  const kv = Object.entries(input)
    .filter(([, v]) => v != null && v !== '' && !(Array.isArray(v) && !v.length))
    .map(([k, v]) => k + '=' + clip(Array.isArray(v) ? v.join(',') : v, 60))
    .join(' ');
  return name + (kv ? ' ' + kv : '');
}

export interface AskOpts {
  onStep?: (note: string) => void;
}

export async function ask(question: string, route: Route, opts: AskOpts = {}): Promise<Turn> {
  const ep = await probeEndpoint();
  if (!ep) {
    return {
      role: 'analyst', err: true,
      text: 'The analyst endpoint is not reachable from this deployment, so this question was not sent. ' +
        'Everything the analyst would cite is on the board by hand: the node pages, the claims and their sources.',
    };
  }
  const skew = toolSkew();
  if (skew) {
    return {
      role: 'analyst', err: true,
      text: 'The analyst service is running tool set ' + skew + ' and this page is built for ' +
        TOOLS_VERSION + '. They have to match before a question can be answered, because the ' +
        'tools run in this page. Redeploy whichever of the two is behind.',
    };
  }

  let system: unknown[];
  try {
    system = [
      { type: 'text', text: await caseIndex(), cache_control: { type: 'ephemeral', ttl: '1h' } },
      { type: 'text', text: await caseState(route) },
    ];
  } catch (e) {
    return {
      role: 'analyst', err: true,
      text: 'Could not assemble the case file for the analyst: ' + (e as Error).message +
        '. The board still works by hand.',
    };
  }

  wire.push({ role: 'user', content: question });
  trimWire();

  const steps: string[] = [];
  const usage = { in: 0, cached: 0, out: 0, rounds: 0 };

  for (let round = 0; round < MAX_ROUNDS; round++) {
    usage.rounds = round + 1;
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), TIMEOUT_MS);
    let j: {
      content?: Block[]; stop_reason?: string; error?: unknown;
      usage?: { input_tokens?: number; output_tokens?: number; cache_read_input_tokens?: number; cache_creation_input_tokens?: number };
    };
    try {
      const r = await fetch(ep, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ system, messages: wire, tools: TOOLS }),
        signal: ac.signal,
      });
      j = await r.json();
    } catch (e) {
      const err = e as Error;
      return {
        role: 'analyst', err: true, steps,
        text: err.name === 'AbortError'
          ? 'The analyst took more than four minutes on one step and the request was cancelled. ' +
            'Ask a narrower question, or ask again.'
          : 'Could not reach the analyst endpoint. ' + (err.message || '') +
            ' If this is a CORS or network error, the board still works by hand: every node, claim and source is on the page.',
      };
    } finally {
      clearTimeout(timer);
    }

    if (j && j.error && !j.content) {
      return {
        role: 'analyst', err: true, steps,
        text: 'The analyst endpoint answered with an error: ' +
          clip(typeof j.error === 'string' ? j.error : JSON.stringify(j.error), 300),
      };
    }
    const content = j.content || [];
    const u = j.usage || {};
    usage.in += (u.input_tokens || 0) + (u.cache_creation_input_tokens || 0);
    usage.cached += u.cache_read_input_tokens || 0;
    usage.out += u.output_tokens || 0;

    /* Echoed back verbatim, thinking blocks and their signatures included. */
    wire.push({ role: 'assistant', content });

    const calls = content.filter((b) => b.type === 'tool_use');
    if (j.stop_reason === 'tool_use' && calls.length) {
      const results: Block[] = [];
      for (const c of calls) {
        const name = String(c.name ?? '');
        const input = (c.input || {}) as Record<string, unknown>;
        const note = describeCall(name, input);
        steps.push(note);
        if (opts.onStep) opts.onStep(note);
        let out: string;
        try { out = await runTool(name, input); } catch (e) { out = 'That tool failed: ' + (e as Error).message; }
        results.push({ type: 'tool_result', tool_use_id: c.id, content: out });
      }
      /* Every result in ONE user message, or parallel tool use stops happening.
         The last block carries a cache breakpoint that MOVES: the previous one
         is cleared first, because the API allows four blocks with cache_control
         in a request and this file already spends one on the case index. Adding
         one a round without clearing the last put five in the request on the
         fifth round and the API answered 400, which a reader saw as "the analyst
         endpoint answered with an error" after twenty seconds of real work.
         Clearing is free: everything before the new breakpoint is still read
         from cache, which is the whole point of moving it forward. */
      moveBreakpoint();
      const last = results[results.length - 1];
      if (last) last.cache_control = { type: 'ephemeral', ttl: '1h' };
      wire.push({ role: 'user', content: results });
      trimWire();
      continue;
    }

    let out = textOf(content);
    if (!out.trim()) {
      return {
        role: 'analyst', err: true, steps, usage,
        text: 'The model returned no text this turn (stop reason: ' + (j.stop_reason || 'unknown') +
          '). Ask again, or narrow the question.',
      };
    }
    if (j.stop_reason === 'max_tokens') out += '\n\n[The answer hit the length limit and was cut off here. Ask me to continue.]';
    if (j.stop_reason === 'refusal') out += '\n\n[The model declined to continue on this question.]';
    return { role: 'analyst', text: out, steps, usage };
  }

  return {
    role: 'analyst', err: true, steps, usage,
    text: 'The analyst read the board ' + MAX_ROUNDS + ' times without reaching an answer and was stopped there. ' +
      'It got as far as: ' + steps.slice(-4).join('; ') + '. Ask a narrower question.',
  };
}
