/* analyst/panel.ts — the analyst on every route.
 *
 * It used to live inside pages/home.ts and render on Home only. Decision 1 of
 * notes/ANALYST-PLAN-2026-09-03.md moves it out: one host element after #view in
 * index.html, painted once at boot, re-chipped on every route change. main.ts
 * clears #view on every route and would otherwise take the transcript with it,
 * which is why the panel is not inside it.
 *
 * The transcript survives navigation on purpose. A reader asks on the map, walks
 * to the node the answer named, and asks the follow-up there; the analyst is
 * told where they now are through the CURRENT STATE block.
 */
import { h, clear } from '../dom';
import { currentRoute, type Route } from '../router';
import { ask, probeEndpoint, resetConversation, checkCitedIds, type Turn } from './client';
import { chipsFor, chipKey } from './chips';
import { stateSummary } from './state';
import { TOOLS, TOOLS_VERSION, runTool } from './tools';

let host: HTMLElement | null = null;
let listEl: HTMLElement | null = null;
let transcriptEl: HTMLElement | null = null;
let statusEl: HTMLElement | null = null;
let whereEl: HTMLElement | null = null;
let inputEl: HTMLInputElement | null = null;
let barEl: HTMLButtonElement | null = null;
let chevEl: HTMLElement | null = null;

const turns: Turn[] = [];
let busy = false;
let live: boolean | null = null;

/* ---- rendering an answer ------------------------------------------------- */
/* The answer is text, drawn with white-space: pre-wrap, with one exception:
   anything in backticks that is a real node id becomes a link to that node, and
   anything in backticks shaped like an id that is NOT on the board is marked.
   The guard flags and never edits, so a wrong id stays visible and labelled. */

function renderSay(text: string, known: Set<string>, unknown: Set<string>): HTMLElement {
  const say = h('div', { class: 'say' });
  let i = 0;
  const re = /`([^`\n]{1,80})`/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    if (m.index > i) say.append(document.createTextNode(text.slice(i, m.index)));
    const tok = m[1].trim();
    if (known.has(tok)) {
      say.append(h('a', { href: '#/n/' + tok, class: 'cited' }, tok));
    } else if (unknown.has(tok)) {
      say.append(h('span', { class: 'cited bad', title: 'not a node on this board' }, tok),
        h('span', { class: 'faint' }, ' [not a node on this board]'));
    } else {
      say.append(h('code', null, tok));
    }
    i = m.index + m[0].length;
  }
  if (i < text.length) say.append(document.createTextNode(text.slice(i)));
  return say;
}

function usageLine(t: Turn): HTMLElement | null {
  if (!t.usage) return null;
  return h('div', { class: 'usage faint' },
    t.usage.rounds + (t.usage.rounds === 1 ? ' round' : ' rounds') + ' · ' +
    t.usage.in.toLocaleString('en-GB') + ' in · ' +
    t.usage.cached.toLocaleString('en-GB') + ' cached · ' +
    t.usage.out.toLocaleString('en-GB') + ' out');
}

/* One turn. `ids` is the guard's verdict on this turn's text, and is null for a
   turn that has none: the reader's own questions, an error, a pending answer. */
function turnEl(t: Turn, ids: { ok: string[]; bad: string[] } | null): HTMLElement {
  const el = h('div', { class: 'turn ' + (t.role === 'you' ? 'you' : '') + (t.err ? ' err' : '') },
    h('div', { class: 'who' }, t.role === 'you' ? 'YOU' : 'ANALYST'));

  if (t.steps && t.steps.length) {
    const s = h('div', { class: 'steps' });
    for (const step of t.steps) s.append(h('div', null, h('span', { class: 'faint' }, 'read '), step));
    el.append(s);
  }

  if (ids) el.append(renderSay(t.text, new Set(ids.ok), new Set(ids.bad)));
  else el.append(h('div', { class: 'say' + (t.thinking ? ' faint' : '') }, t.text));

  if (ids && ids.bad.length) {
    el.append(h('div', { class: 'usage red' },
      ids.bad.length + (ids.bad.length === 1 ? ' id was' : ' ids were') +
      ' cited that this board does not carry: ' + ids.bad.join(', ')));
  }
  const u = usageLine(t);
  if (u) el.append(u);
  return el;
}

async function paint(): Promise<void> {
  if (!transcriptEl) return;
  const drawn: HTMLElement[] = [];
  for (const t of turns) {
    const guardable = t.role === 'analyst' && !t.err && !t.thinking && !!t.text;
    drawn.push(turnEl(t, guardable ? await checkCitedIds(t.text) : null));
  }
  if (!transcriptEl) return;
  clear(transcriptEl);
  for (const el of drawn) transcriptEl.append(el);
}

/* ---- asking -------------------------------------------------------------- */

async function send(q: string): Promise<void> {
  if (busy || !q.trim()) return;
  setOpen(true);
  busy = true;
  if (inputEl) inputEl.disabled = true;
  turns.push({ role: 'you', text: q });
  const pending: Turn = { role: 'analyst', text: 'thinking…', thinking: true, steps: [] };
  turns.push(pending);
  await paint();

  const route = currentRoute();
  const reply = await ask(q, route, {
    onStep: (note) => {
      pending.steps = (pending.steps || []).concat([note]);
      pending.text = 'reading the board…';
      void paint();
    },
  });
  turns[turns.length - 1] = reply;
  busy = false;
  if (inputEl) { inputEl.disabled = false; }
  await paint();
}

/* ---- the panel ----------------------------------------------------------- */

export function setOpen(on: boolean): void {
  if (!host) return;
  host.setAttribute('data-open', on ? '1' : '0');
  if (chevEl) chevEl.textContent = on ? '▾' : '▴';
  if (barEl) {
    barEl.setAttribute('aria-expanded', on ? 'true' : 'false');
    barEl.setAttribute('title', on ? 'Close the analyst' : 'Open the analyst');
  }
  if (on && inputEl) inputEl.focus();
}

export function mountAnalyst(el: HTMLElement): void {
  host = el;
  clear(host);
  host.setAttribute('data-open', '0');

  statusEl = h('span', { class: 'faint an-status' }, 'checking the analyst…');
  whereEl = h('span', { class: 'an-where' }, '');
  chevEl = h('span', { class: 'an-chev' }, '▴');

  barEl = h('button', {
    type: 'button', class: 'an-bar', 'aria-controls': 'analyst-body', 'aria-expanded': 'false',
    title: 'Open the analyst',
    onclick: () => setOpen(host!.getAttribute('data-open') !== '1'),
  },
    chevEl,
    h('span', { class: 'eyebrow' }, 'Ask the analyst'),
    whereEl,
    statusEl,
  );

  inputEl = h('input', {
    type: 'text',
    placeholder: 'Ask a question about the record…',
    'aria-label': 'Ask the analyst',
  });

  listEl = h('div', { class: 'suggest' });
  transcriptEl = h('div', { class: 'transcript' });

  const body = h('div', { class: 'an-body', id: 'analyst-body' },
    h('div', { class: 'an-row' },
      inputEl,
      h('button', {
        type: 'button', class: 'an-clear', title: 'Forget this conversation and start again',
        onclick: () => { turns.length = 0; resetConversation(); void paint(); },
      }, 'CLEAR'),
    ),
    listEl,
    transcriptEl,
  );

  host.append(barEl, body);

  inputEl.addEventListener('keydown', (e) => {
    if ((e as KeyboardEvent).key !== 'Enter' || !inputEl) return;
    const q = inputEl.value;
    inputEl.value = '';
    void send(q);
  });

  void probeEndpoint().then((ep) => {
    live = !!ep;
    if (!statusEl) return;
    statusEl.textContent = ep
      ? 'live · no key needed'
      : 'endpoint not reachable from here · the board works by hand';
    statusEl.setAttribute('data-live', ep ? 'yes' : 'no');
  });
}

/* Called after every route render. The chips are the only thing that changes;
   the transcript is the reader's and is left alone. */
export async function refreshAnalyst(r: Route): Promise<void> {
  if (!listEl || !host) return;
  host.setAttribute('data-chipkey', chipKey(r));
  const chips = await chipsFor(r);
  clear(listEl);
  for (const s of chips) {
    listEl.append(h('button', { type: 'button', class: 'an-chip', onclick: () => void send(s) },
      h('span', { class: 'faint' }, '›'), h('span', { class: 'an-chip-text' }, s)));
  }
  if (whereEl) whereEl.textContent = await stateSummary(r);
}

export function analystIsLive(): boolean | null { return live; }

/* A probe, on the pattern of window.__app.map and window.__app.timeline. The
   twelve tools are the analyst's whole reach over the board and they draw
   nothing, so nothing in the DOM can be read to tell whether one of them is
   answering correctly. This is the channel the gate uses instead: C19 drives
   each tool and compares its answer with one it derives from the same data
   file itself. It exposes no state the page keeps; runTool is a pure function
   of the /data files. */
{
  const w = window as unknown as { __app?: Record<string, unknown> };
  w.__app = w.__app || {};
  (w.__app as Record<string, unknown>).analyst = {
    version: TOOLS_VERSION,
    names: TOOLS.map((t) => t.name),
    run: (name: string, args: Record<string, unknown>) => runTool(name, args),
  };
}
