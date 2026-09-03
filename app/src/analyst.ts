/* analyst.ts — the analyst client, ported from tools/analyst_patches.py.
 *
 * Same request shape as the board's: two system blocks, the first (the case index,
 * byte-stable between turns) marked `cache_control: ephemeral` so every turn after
 * the first reads it from the API's cache, the second (the volatile state) uncached.
 * The Worker pins the model, the token ceiling and the effort server-side and reads
 * only `system` and `messages` from the body, so those are all this sends.
 *
 * The Worker is the only runtime request this app makes that is not same-origin.
 */
import { loadAnalyst, loadIndex, loadNode, type IndexNode } from './data';

const AN_INDEX_CAP = 220000;
const AN_FOCUS_CAP = 60000;
const TIMEOUT_MS = 180000;

export interface Turn { role: 'you' | 'analyst'; text: string; err?: boolean; thinking?: boolean; }

let endpoint: string | null = null;
let probed = false;

function clip(s: unknown, n: number): string {
  const str = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
  return str.length > n ? str.slice(0, n - 3) + '...' : str;
}

function dates(n: IndexNode): string {
  const a = n.dateStart || '', b = n.dateEnd || '';
  return a || b ? a + (b && b !== a ? '..' + b : '') : 'undated';
}

function line(n: IndexNode): string {
  return [
    n.id, clip(n.label, 70), n.cls || '?', 'tier ' + (n.tier || '?'),
    'C' + (n.C ?? '?') + 'A' + (n.A ?? '?') + 'D' + (n.D ?? '?'),
    dates(n), (n.claims[0] + n.claims[1] + n.claims[2]) + ' claims',
  ].join(' | ');
}

/* The stable half. Byte-identical between turns, which is what makes the cache
   worth marking. */
async function caseIndex(): Promise<string> {
  const idx = await loadIndex();
  const head =
    'You are the analyst on a sourced research board about the alleged US legacy UAP ' +
    'recovery and reverse-engineering programme, 1944 to now. Claim tiers 1-3 are evidence ' +
    'strength, 1 strongest: T1 documented, T2 a named person on the record, T3 a stated ' +
    'inference. Node tiers A/B/C are proximity to the programme, NOT credibility. C/A/D are ' +
    'custody proximity, access and disclosure role. Never invent a source, a URL, a document ' +
    'number or a quotation; cite node ids and say plainly when the board does not carry ' +
    'something.\n\n' +
    'CASE INDEX. One line per node, all of them: id | label | class | node tier | C/A/D axes | ' +
    'dates | claim count. The CURRENT STATE message that follows carries the node in view in ' +
    'full. When a question is about a node that is only in this index, answer from its line and ' +
    'say what a fuller answer needs: open that node and ask again, and its claims, sources and ' +
    'open questions will be in front of you.';
  let out = idx.nodes.map(line).join('\n');
  if (out.length > AN_INDEX_CAP) out = out.slice(0, AN_INDEX_CAP) + '\n[index truncated at ' + AN_INDEX_CAP + ' characters]';
  return head + '\n' + out;
}

/* The volatile half. Sent second, uncached, because it changes every turn. */
async function caseState(nodeId: string | null): Promise<string> {
  const parts: string[] = ['CURRENT STATE. route=' + (location.hash || '#/') + ' node=' + (nodeId || 'none')];
  if (nodeId) {
    try {
      const n = await loadNode(nodeId);
      const lines: string[] = [n.id + ' | ' + n.label + ' | ' + n.cls + ' | tier ' + (n.tier || '?')];
      const d = n.dossier || {};
      if (d.whatItIs) lines.push('what it is: ' + clip(d.whatItIs, 900));
      if (d.whyImplicated) lines.push('why implicated: ' + clip(d.whyImplicated, 900));
      if (d.denialPosture) lines.push('denial posture: ' + clip(d.denialPosture, 400));
      if (n.tierRationale) lines.push('tier rationale: ' + clip(n.tierRationale, 300));
      const cl = (n.claims || []).slice().sort((a, b) => (a.tier || 3) - (b.tier || 3)).slice(0, 40)
        .map((c) => '  T' + c.tier + ': ' + clip(c.text, 420) +
          (c.source ? '  [' + clip(typeof c.source === 'string' ? c.source : c.source.url || c.source.name, 160) + ']' : ''));
      if (cl.length) lines.push('claims (strongest first):\n' + cl.join('\n'));
      const cn = n.connections.slice(0, 60).map((c) =>
        '  ' + n.id + ' -> ' + c.id + ' [' + c.type + ', T' + (c.claimTier ?? '?') + '] ' +
        clip(c.edgeLabel || '', 90) + (c.note ? ' -- ' + clip(c.note, 220) : ''));
      if (cn.length) lines.push('its sourced edges (' + n.connections.length + ' distinct neighbours):\n' + cn.join('\n'));
      if (n.denials.length) lines.push('denials on the record:\n' +
        n.denials.map((x) => '  ' + x.by.label + ' denies ' + x.of.label + ': ' + clip(x.label, 160)).join('\n'));
      parts.push('NODE IN VIEW, in full.\n' + lines.join('\n'));
    } catch {
      parts.push('NODE IN VIEW: ' + nodeId + ' (its record is not loaded on this deployment).');
    }
  } else {
    const idx = await loadIndex();
    const top = idx.nodes.slice().sort((a, b) => b.deg - a.deg).slice(0, 10);
    parts.push('NOTHING IS OPEN. Most connected nodes, briefly.\n' + top.map(line).join('\n'));
  }
  let out = parts.join('\n\n');
  if (out.length > AN_FOCUS_CAP) out = out.slice(0, AN_FOCUS_CAP) + '\n[state truncated at ' + AN_FOCUS_CAP + ' characters]';
  return out;
}

/* Ask once whether this deployment has a live analyst. Same-origin first, then the
   Worker's own hostname: Pages cannot route /api/* to a Worker on a pages.dev
   hostname and answers unknown paths with the app itself. */
export async function probeEndpoint(): Promise<string | null> {
  if (probed) return endpoint;
  probed = true;
  if (location.protocol !== 'http:' && location.protocol !== 'https:') return null;
  let worker = '';
  try { worker = (await loadAnalyst()).worker; } catch { worker = ''; }
  for (const o of ['', worker].filter((x, i) => i === 0 || x)) {
    try {
      const r = await fetch(o + '/api/analyst/health');
      if (!r.ok) continue;
      if (!(r.headers.get('content-type') || '').includes('json')) continue;
      const j = await r.json();
      if (j && j.live) { endpoint = o + '/api/analyst'; return endpoint; }
    } catch { /* the next candidate, or none */ }
  }
  return null;
}

export function endpointNow(): string | null { return endpoint; }

export async function ask(question: string, history: Turn[], nodeId: string | null): Promise<Turn> {
  const ep = await probeEndpoint();
  if (!ep) {
    return {
      role: 'analyst', err: true,
      text: 'The analyst endpoint is not reachable from this deployment, so this question was not sent. ' +
        'Everything the analyst would cite is on the board by hand: the node pages, the claims and their sources.',
    };
  }

  const msgs = history
    .filter((t) => t.text && !t.err)
    .slice(-10)
    .map((t) => ({ role: t.role === 'you' ? 'user' : 'assistant', content: t.text }));
  if (!msgs.length || msgs[msgs.length - 1].role !== 'user' || msgs[msgs.length - 1].content !== question) {
    msgs.push({ role: 'user', content: question });
  }

  let system: unknown[];
  try {
    system = [
      { type: 'text', text: await caseIndex(), cache_control: { type: 'ephemeral' } },
      { type: 'text', text: await caseState(nodeId) },
    ];
  } catch (e) {
    return {
      role: 'analyst', err: true,
      text: 'Could not assemble the case file for the analyst: ' + (e as Error).message +
        '. The board still works by hand.',
    };
  }

  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(ep, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ system, messages: msgs }),
      signal: ac.signal,
    });
    const j = await r.json();
    if (j && j.error && !j.content) {
      return { role: 'analyst', err: true, text: 'The analyst endpoint answered with an error: ' + clip(typeof j.error === 'string' ? j.error : JSON.stringify(j.error), 300) };
    }
    let out = (j.content || []).filter((b: { type: string }) => b.type === 'text').map((b: { text: string }) => b.text).join('\n');
    if (!out.trim()) {
      return { role: 'analyst', err: true, text: 'The model returned no text this turn (stop reason: ' + (j.stop_reason || 'unknown') + '). Ask again, or narrow the question.' };
    }
    if (j.stop_reason === 'max_tokens') out += '\n\n[The answer hit the length limit and was cut off here. Ask me to continue.]';
    if (j.stop_reason === 'refusal') out += '\n\n[The model declined to continue on this question.]';
    return { role: 'analyst', text: out };
  } catch (e) {
    const err = e as Error;
    return {
      role: 'analyst', err: true,
      text: err.name === 'AbortError'
        ? 'The analyst took more than three minutes and the request was cancelled. Ask a narrower question, or ask again.'
        : 'Could not reach the analyst endpoint. ' + (err.message || '') +
          ' If this is a CORS or network error, the board still works by hand: every node, claim and source is on the page.',
    };
  } finally {
    clearTimeout(timer);
  }
}
