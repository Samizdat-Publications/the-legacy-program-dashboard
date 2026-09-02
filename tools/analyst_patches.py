"""The analyst's case file and request path, rebuilt for this board.

WHY THIS EXISTS
---------------
On 1 September 2026 the live analyst was tested end to end for the first time and
it had never worked. Two things, in series:

1. The Pages domain never routed /api/* to the Worker, so the same-origin health
   probe got the board's own HTML back and the endpoint was never "live".
   (Fixed in l0_patches.py: the client now tries the Worker's hostname second.)

2. With the endpoint live, SYSTEM_PROMPT() THREW. The inherited caseContext()
   walked PEOPLE only and read the parent board's fields: leftBehind, tookWith,
   unexplainedResidual, and `(p.unverified||[]).join(...)` -- `unverified` is a
   string on some of this board's nodes. The exception escaped askAnalyst()
   before its try, the turn sat on "thinking" for ever, and nothing reported it.
   Every one of the gate's analyst assertions exercised the scripted path.

So the inherited case file was wrong twice over: it could throw, and when it did
not it described 286 people and none of the 694 entities -- no AAWSAP, no AARO,
no KONA BLUE -- to a model asked to reason about the programme.

WHAT THIS BUILDS
----------------
Two halves, because the API caches by prefix and the case file is the prefix:

  CASE INDEX   one line per node, all 980, byte-stable between turns. Sent as the
               first system block with cache_control, so every turn after the
               first reads it from cache at a tenth of the price.
  FOCUS        the selected node in full -- claims with tiers and sources, its
               hand-written edges, its dossier and open questions, the FOIA
               requests drafted to close them -- plus a one-line brief on each
               neighbour. With nothing selected: the start-here flags and the
               most connected nodes. Sent second, uncached, because it changes.

Plus the request path made honest: a timeout, a message for every failure mode
that used to be a spinner, the length limit reported when it is hit, and the
question no longer sent twice (pushTurn() had already appended it).

Every patch goes through must_replace() and fails the build by name.
"""
import sys

CASE_JS = r"""/* ---- the analyst's case file, rebuilt for this board (1 September 2026) ----
   The inherited caseContext() walked PEOPLE only and read the parent board's
   fields. On this board `unverified` is a string on some nodes, so `.join`
   threw inside SYSTEM_PROMPT() and the model path never sent a request. See
   tools/analyst_patches.py for the whole story. */
const AN_INDEX_CAP = 220000, AN_FOCUS_CAP = 60000;
function anList(v){ return Array.isArray(v) ? v.filter(Boolean).map(String) : (v ? [String(v)] : []); }
function anClip(str, n){ str = String(str == null ? '' : str).replace(/\s+/g, ' ').trim(); return str.length > n ? str.slice(0, n - 3) + '...' : str; }
function anDates(n){ const a = n.dateStart || n.date || '', b = n.dateEnd || ''; return (a || b) ? (a + (b ? '..' + b : '')) : 'undated'; }
function anLine(n){
  /* POISON=analyst in tools/runtime_check.js: dereference a field no node has,
     on the real page, so the check is shown catching the failure it exists for. */
  if (window.__ANALYST_POISON) return n.__missing.join('');
  return [n.id, anClip(n.label, 70), n.cls || '?', 'tier ' + (n.tier || '?'),
          'C' + (n.C == null ? '?' : n.C) + 'A' + (n.A == null ? '?' : n.A) + 'D' + (n.D == null ? '?' : n.D),
          anDates(n), (n.claims || []).length + ' claims', anClip(n.sub || n.loc || '', 60)].join(' | ');
}
function caseIndex(){
  const head = 'CASE INDEX. One line per node, all of them: id | label | class | node tier (A/B/C is proximity to the programme, not credibility) | C/A/D axes | dates | claim count | role. The FOCUS section in the next message carries the selected node in full. When a question is about a node that is only in this index, answer from its line and say what a fuller answer needs: select that node on the board and ask again, and its claims, sources and open questions will be in front of you.';
  let out = NODES.map(anLine).join('\n');
  if (out.length > AN_INDEX_CAP) out = out.slice(0, AN_INDEX_CAP) + '\n[index truncated at ' + AN_INDEX_CAP + ' characters]';
  return head + '\n' + out;
}
function anClaims(n, cap){
  const cs = (n.claims || []).slice().sort((a, b) => (a.tier || 3) - (b.tier || 3)).slice(0, cap);
  return cs.map(c => '  T' + (c.tier || '?') + ': ' + anClip(c.text, 420) + (c.source ? '  [' + anClip(c.source, 160) + ']' : '')).join('\n');
}
function anRecord(n, full){
  const L0 = (typeof L0DATA === 'object' && L0DATA && L0DATA.l0) ? L0DATA.l0.find(x => x.id === n.id) : null;
  const d = (L0 && L0.dossier) || {};
  const lines = [anLine(n)];
  const info = (typeof ENTITY_INFO === 'object' && ENTITY_INFO && ENTITY_INFO[n.id]) || {};
  const desc = n.desc || n.narrative || info.desc || '';
  if (desc) lines.push('about: ' + anClip(desc, full ? 1400 : 400));
  if (n.tierRationale) lines.push('tier rationale: ' + anClip(n.tierRationale, 300));
  if (full){
    if (d.whatItIs) lines.push('what it is: ' + anClip(d.whatItIs, 600));
    if (d.whyImplicated) lines.push('why implicated: ' + anClip(d.whyImplicated, 600));
    if (d.denialPosture) lines.push('denial posture: ' + anClip(d.denialPosture, 400));
    const conf = anList(n.conflicts); if (conf.length) lines.push('conflicts: ' + anClip(conf.join(' | '), 600));
    const unv = anList(n.unverified); if (unv.length) lines.push('unverified: ' + anClip(unv.join(' | '), 600));
    const oq = anList(d.openQuestions); if (oq.length) lines.push('open questions: ' + oq.map((q, i) => 'Q' + i + ' ' + anClip(q, 200)).join(' ; '));
    const foia = (typeof FOIADATA === 'object' && FOIADATA && FOIADATA.byNode && FOIADATA.byNode[n.id]) || [];
    if (foia.length) lines.push('FOIA requests drafted for it: ' + foia.map(f => f.request + ' ' + anClip(f.title, 80)).join(' ; '));
    const cl = anClaims(n, 40); if (cl) lines.push('claims (strongest first):\n' + cl);
    const srcs = (n.sources || []).slice(0, 12).map(s => '  ' + anClip(s.name || '', 100) + (s.url ? ' ' + s.url : '')).join('\n');
    if (srcs) lines.push('sources:\n' + srcs);
  } else {
    const cl = anClaims(n, 3); if (cl) lines.push('top claims:\n' + cl);
  }
  return lines.join('\n');
}
function caseFocus(){
  const byId = new Map(NODES.map(n => [n.id, n]));
  const sel = S.sel && byId.get(S.sel);
  const hand = (typeof PROGRAM_EDGES === 'object' && PROGRAM_EDGES) ? PROGRAM_EDGES : [];
  const parts = [];
  if (sel){
    parts.push('SELECTED NODE, in full.\n' + anRecord(sel, true));
    const edges = hand.filter(e => e.a === sel.id || e.b === sel.id);
    if (edges.length){
      parts.push('ITS HAND-WRITTEN EDGES (' + edges.length + '; every one is sourced; T is evidence strength, 1 strongest).\n'
        + edges.slice(0, 60).map(e => '  ' + e.a + ' -> ' + e.b + ' [' + e.type + ', T' + (e.claimTier || '?') + '] ' + anClip(e.label || '', 90)
            + (e.note ? ' -- ' + anClip(e.note, 260) : '')
            + ((e.sources || [])[0] && (e.sources[0].url || e.sources[0].name) ? ' [' + anClip(e.sources[0].url || e.sources[0].name, 120) + ']' : '')).join('\n'));
      const nb = new Map();
      for (const e of edges){ const o = e.a === sel.id ? e.b : e.a; if (byId.has(o) && !nb.has(o)) nb.set(o, byId.get(o)); }
      const nbs = [...nb.values()].slice(0, 16);
      if (nbs.length) parts.push('ITS NEIGHBOURS, briefly.\n' + nbs.map(n => anRecord(n, false)).join('\n--\n'));
    }
  } else {
    const flags = (typeof L0DATA === 'object' && L0DATA && L0DATA.highlights && L0DATA.highlights.flags) || [];
    if (flags.length) parts.push('NOTHING IS SELECTED. The board flags these as places to start, each with a stated reason:\n'
      + flags.map(f => '  ' + f.id + ': ' + anClip(f.why || '', 220)).join('\n'));
    const deg = new Map();
    for (const e of hand){ deg.set(e.a, (deg.get(e.a) || 0) + 1); deg.set(e.b, (deg.get(e.b) || 0) + 1); }
    const top = [...deg.entries()].sort((a, b) => b[1] - a[1]).slice(0, 10).map(([id]) => byId.get(id)).filter(Boolean);
    if (top.length) parts.push('MOST CONNECTED NODES, briefly.\n' + top.map(n => anRecord(n, false)).join('\n--\n'));
  }
  let out = parts.join('\n\n');
  if (out.length > AN_FOCUS_CAP) out = out.slice(0, AN_FOCUS_CAP) + '\n[focus truncated at ' + AN_FOCUS_CAP + ' characters]';
  return out;
}
/* kept so anything that still calls caseContext() gets this board, not a throw */
function caseContext(){ return caseIndex() + '\n\n' + caseFocus(); }"""

PROMPT_TAIL_OLD = """CURRENT STATE. view=${S.view} selection=${S.sel||'none'} hops=${S.hops} filters=${[...S.filters].join(',')||'none'}

CASE FILE.
${caseContext()}

STRONGEST COMPUTED CONNECTIONS (weight = number of independent connection types).
${graphContext()}`;"""

PROMPT_TAIL_NEW = """HOW TO READ THE DATA. The CASE INDEX below lists every node on the board, one line each, and is the authority on what exists. A second message, CURRENT STATE, follows it with the selected node in full, its sourced edges and its neighbours. Cite ids. When the user asks about a node that is only in the index, answer from its line and say plainly that selecting it and asking again puts its claims, sources and open questions in front of you.

${caseIndex()}`;

/* The volatile half: selection, the focus record, live weights. Sent after the
   cached index so the index stays byte-identical between turns. */
const SYSTEM_STATE = () => `CURRENT STATE. view=${S.view} selection=${S.sel||'none'} hops=${S.hops} filters=${[...S.filters].join(',')||'none'}

${caseFocus()}

STRONGEST COMPUTED CONNECTIONS (weight = number of independent connection types).
${graphContext()}`;"""

BODY_OLD = """  const body = {
    model: S.model,
    max_tokens: 4000,
    system: SYSTEM_PROMPT(),
    messages: S.turns.filter(t=>t.text && !t.err).slice(-10).map(t=>({
      role: t.role==='YOU' ? 'user' : 'assistant', content: t.text })).concat([{ role:'user', content:text }]),
  };"""

BODY_NEW = """  let body;
  try {
    const history = S.turns.filter(t=>t.text && !t.err).slice(-10).map(t=>({
      role: t.role==='YOU' ? 'user' : 'assistant', content: t.text }));
    /* pushTurn() above already appended this question, so the history ends with
       it. The inherited version appended it a second time. */
    if (!history.length || history[history.length-1].role !== 'user' || history[history.length-1].content !== text)
      history.push({ role:'user', content:text });
    body = {
      model: S.model,
      max_tokens: 8000,
      system: [
        { type:'text', text: SYSTEM_PROMPT(), cache_control: { type:'ephemeral' } },
        { type:'text', text: SYSTEM_STATE() },
      ],
      messages: history,
    };
  } catch(e){
    /* Building the prompt reads every node. If a record has a shape this code
       does not expect, it shows here as a message rather than as a spinner. */
    turn.thinking = false; turn.err = true;
    turn.text = 'Could not assemble the case file for the analyst: ' + e.message + '. The dashboard still works by hand.';
    S.anBusy = false; renderAnalystChrome(); return;
  }
  const AC = new AbortController();
  setTimeout(() => AC.abort(), 180000);"""

WORKER_OPTS_OLD = """          headers:{ 'content-type':'application/json' },
          body: JSON.stringify({ system: body.system, messages: body.messages }),"""
WORKER_OPTS_NEW = """          headers:{ 'content-type':'application/json' },
          body: JSON.stringify({ system: body.system, messages: body.messages }),
          signal: AC.signal,"""

DIRECT_OPTS_OLD = """'anthropic-dangerous-direct-browser-access':'true' },
          body: JSON.stringify(body),"""
DIRECT_OPTS_NEW = """'anthropic-dangerous-direct-browser-access':'true' },
          body: JSON.stringify(body),
          signal: AC.signal,"""

TAIL_OLD = """    const j = await r.json();
    const out = (j.content||[]).filter(b=>b.type==='text').map(b=>b.text).join('\\n');
    applyAnalystReply(turn, out);
  } catch(e){
    turn.thinking = false; turn.err = true;
    turn.text = 'Could not reach api.anthropic.com. ' + e.message
      + ' If this is a CORS or network error, the dashboard still works by hand: every control the analyst uses is clickable.';
  }
  S.anBusy = false; renderAnalystChrome();
}"""

TAIL_NEW = """    const j = await r.json();
    if (j && j.error && !j.content){
      turn.thinking = false; turn.err = true;
      turn.text = 'The analyst endpoint answered with an error: '
        + anClip(typeof j.error === 'string' ? j.error : JSON.stringify(j.error), 300);
      S.anBusy = false; renderAnalystChrome(); return;
    }
    let out = (j.content||[]).filter(b=>b.type==='text').map(b=>b.text).join('\\n');
    if (!out.trim()){
      turn.thinking = false; turn.err = true;
      turn.text = 'The model returned no text this turn (stop reason: ' + (j.stop_reason||'unknown')
        + '). Ask again, or narrow the question.';
      S.anBusy = false; renderAnalystChrome(); return;
    }
    if (j.stop_reason === 'max_tokens') out += '\\n\\n[The answer hit the length limit and was cut off here. Ask me to continue.]';
    if (j.stop_reason === 'refusal') out += '\\n\\n[The model declined to continue on this question.]';
    applyAnalystReply(turn, out);
  } catch(e){
    turn.thinking = false; turn.err = true;
    const where = (S.analystEndpoint && !key) ? 'the analyst endpoint' : 'api.anthropic.com';
    turn.text = (e && e.name === 'AbortError')
      ? 'The analyst took more than three minutes and the request was cancelled. Ask a narrower question, or ask again.'
      : 'Could not reach ' + where + '. ' + (e && e.message ? e.message : '')
        + ' If this is a CORS or network error, the dashboard still works by hand: every control the analyst uses is clickable.';
  }
  S.anBusy = false; renderAnalystChrome();
}"""

BOARD_OLD = "window.__board = { CMD, S, L0DATA, FOIADATA, mountL0, l0Fit,"
BOARD_NEW = ("window.__board = { CMD, S, L0DATA, FOIADATA, mountL0, l0Fit,\n"
             "                   analystPrompt: () => ({ stable: SYSTEM_PROMPT(), state: SYSTEM_STATE() }),")


def _replace_block(s, start, end, new, label, lo, hi):
    """Replace from `start` through the first `end` after it, checking the slice
    is a plausible size so a moved anchor cannot silently eat half the file."""
    a = s.find(start)
    if a < 0:
        print(f"  !! PATCH FAILED [{label}]: start anchor not found", file=sys.stderr)
        return s, False
    b = s.find(end, a)
    if b < 0:
        print(f"  !! PATCH FAILED [{label}]: end anchor not found", file=sys.stderr)
        return s, False
    b += len(end)
    if not (lo <= b - a <= hi):
        print(f"  !! PATCH FAILED [{label}]: slice is {b - a} bytes, expected {lo}..{hi}",
              file=sys.stderr)
        return s, False
    return s[:a] + new + s[b:], True


def apply(s, must_replace):
    ok = True
    s, o = _replace_block(s, "function caseContext(){", "].join('\\n')).join('\\n---\\n');\n}",
                          CASE_JS, "analyst case file (caseContext replaced)", 500, 1400); ok &= o
    s, o = must_replace(s, PROMPT_TAIL_OLD, PROMPT_TAIL_NEW, "analyst prompt split into cached index and state", 1); ok &= o
    s, o = must_replace(s, BODY_OLD, BODY_NEW, "analyst request body: cached system blocks, no doubled question", 1); ok &= o
    s, o = must_replace(s, WORKER_OPTS_OLD, WORKER_OPTS_NEW, "analyst worker fetch carries the timeout signal", 1); ok &= o
    s, o = must_replace(s, DIRECT_OPTS_OLD, DIRECT_OPTS_NEW, "analyst direct fetch carries the timeout signal", 1); ok &= o
    s, o = must_replace(s, TAIL_OLD, TAIL_NEW, "analyst reply handling: errors, empty text, length limit", 1); ok &= o
    s, o = must_replace(s, BOARD_OLD, BOARD_NEW, "analyst prompt exposed for the runtime check", 1); ok &= o
    return s, ok
