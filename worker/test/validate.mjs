/* worker/test/validate.mjs — the Worker's validators against a REAL tool exchange.
 *
 * WHY THIS EXISTS
 * ---------------
 * `clean`, `cleanTools` and `cleanSystem` are the only things standing between a
 * request and the account's tokens, and until 11 September 2026 the only shape
 * they had ever been fed was a list of strings. A tool loop sends something quite
 * different: an assistant turn carrying a signed `thinking` block and a
 * `tool_use` block, then a user turn of nothing but `tool_result` blocks. If any
 * of that is dropped or rewritten the API answers 400 and the reader sees "the
 * analyst endpoint answered with an error" with no way to tell why.
 *
 * CLAUDE.md section 5: a check that has never been shown to fail is
 * indistinguishable from a broken one. So every case here that must be ACCEPTED
 * is paired with one that must be REFUSED, and the refusals are the point.
 *
 *   cd "C:\\Users\\stewa\\OneDrive\\Documents\\Claude\\Projects\\Missing individuals connected to defense contractors\\the-program\\worker"
 *   node test/validate.mjs
 *
 * It runs the TypeScript through esbuild, which wrangler already depends on, so
 * there is no build step and nothing to keep in step by hand.
 */
import { build } from 'esbuild';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
import { writeFileSync } from 'node:fs';

const here = dirname(fileURLToPath(import.meta.url));

const out = await build({
  entryPoints: [join(here, '..', 'src', 'index.ts')],
  bundle: true, format: 'esm', platform: 'neutral', write: false,
  external: ['@anthropic-ai/sdk'],
});
/* The bundle is written INSIDE worker/, not to a temp directory: the SDK is left
   external, and Node resolves `@anthropic-ai/sdk` by walking up from the importing
   file. From the system temp directory there is no worker/node_modules to find.
   The file is gitignored. */
const file = join(here, '..', '.validate-build.mjs');
writeFileSync(file, out.outputFiles[0].text);
const W = await import(pathToFileURL(file).href);

let ok = 0, bad = 0;
function check(cond, label, detail = '') {
  console.log('  ' + (cond ? 'ok    ' : 'FAIL  ') + label + (detail ? ' :: ' + detail : ''));
  cond ? ok++ : bad++;
}

/* ---- the fixture: one question, one tool round, verbatim in the shapes the
   API uses. The signature is nonsense on purpose; what matters is that it comes
   back byte-identical, because the real one is checked by the API. ---------- */
const SIG = 'ErUBCkYIBBgCKkBz' + 'x'.repeat(40) + '==';
const EXCHANGE = [
  { role: 'user', content: 'Which band is thinnest on Tier 1 evidence?' },
  {
    role: 'assistant',
    content: [
      { type: 'thinking', thinking: 'I should group the map nodes by band.', signature: SIG },
      { type: 'text', text: 'Let me count that rather than guess.' },
      { type: 'tool_use', id: 'toolu_01A', name: 'nodes', input: { on_map: true, group_by: 'band' } },
    ],
  },
  {
    role: 'user',
    content: [
      { type: 'tool_result', tool_use_id: 'toolu_01A', content: 'NODES matching — 137 of 1057\n  38  research' },
    ],
  },
];

const TOOLS = [
  { name: 'nodes', description: 'Filter, sort, count and group the node index.', input_schema: { type: 'object', properties: {} } },
  { name: 'path', description: 'Shortest chains of sourced edges between two nodes.', input_schema: { type: 'object', properties: {} } },
];

console.log('\n  the Worker validators, against a real tool exchange\n');

/* ---- what must be ACCEPTED ---------------------------------------------- */
{
  const got = W.clean(EXCHANGE);
  check(!!got, 'a thinking + tool_use + tool_result exchange survives clean()',
    got ? got.length + ' messages' : 'REFUSED, which would be a 400 for every tool answer');

  if (got) {
    const think = got[1].content.find((b) => b.type === 'thinking');
    check(!!think && think.signature === SIG && think.thinking === EXCHANGE[1].content[0].thinking,
      'the thinking block comes back byte-identical, signature included',
      think ? 'signature ' + (think.signature === SIG ? 'intact' : 'REWRITTEN') : 'the block is gone');

    const use = got[1].content.find((b) => b.type === 'tool_use');
    check(!!use && use.id === 'toolu_01A' && use.input.group_by === 'band',
      'the tool_use block keeps its id and its arguments',
      use ? use.id + ' ' + JSON.stringify(use.input) : 'the block is gone');

    const res = got[2].content[0];
    check(res && res.type === 'tool_result' && res.tool_use_id === 'toolu_01A',
      'the tool_result block keeps the id it answers', res ? res.tool_use_id : 'the block is gone');
  }

  const tools = W.cleanTools(TOOLS);
  check(!!tools && tools.length === 2, 'a tool catalogue of pinned names survives cleanTools()',
    tools ? tools.map((t) => t.name).join(', ') : 'REFUSED');

  const sys = W.cleanSystem([
    { type: 'text', text: 'CASE INDEX', cache_control: { type: 'ephemeral', ttl: '1h' } },
    { type: 'text', text: 'CURRENT STATE' },
  ]);
  check(!!sys && sys.length === 2 && sys[0].cache_control && sys[0].cache_control.ttl === '1h',
    'the one hour cache TTL is passed through rather than flattened',
    sys && sys[0].cache_control ? JSON.stringify(sys[0].cache_control) : 'no cache_control survived');

  check(W.TOOL_NAMES.size === 12, 'the Worker pins twelve tool names', [...W.TOOL_NAMES].join(' '));
  check(typeof W.TOOLS_VERSION === 'string' && /^\d{4}-\d{2}-\d{2}/.test(W.TOOLS_VERSION),
    'the Worker carries a TOOLS_VERSION for the handshake', W.TOOLS_VERSION);
}

/* ---- what must be REFUSED ------------------------------------------------ */
{
  const cases = [
    ['a tool name the Worker does not pin', () => W.cleanTools([
      { name: 'bash', description: 'run a shell command', input_schema: { type: 'object', properties: {} } }])],
    ['the same tool twice', () => W.cleanTools([TOOLS[0], TOOLS[0]])],
    ['a tool with no input_schema', () => W.cleanTools([{ name: 'nodes', description: 'x' }])],
    ['a tool_use naming a tool the Worker does not pin', () => W.clean([
      EXCHANGE[0],
      { role: 'assistant', content: [{ type: 'tool_use', id: 'toolu_01B', name: 'bash', input: {} }] },
      EXCHANGE[2]])],
    ['a block type the Worker does not relay', () => W.clean([
      EXCHANGE[0],
      { role: 'assistant', content: [{ type: 'image', source: { type: 'base64', data: 'x' } }] },
      EXCHANGE[2]])],
    ['a thinking block sent by the USER', () => W.clean([
      EXCHANGE[0],
      { role: 'user', content: [{ type: 'thinking', thinking: 'x', signature: SIG }] }])],
    ['a conversation that does not end on the user', () => W.clean([EXCHANGE[0], EXCHANGE[1]])],
    ['an empty conversation', () => W.clean([])],
    ['a conversation that is not an array', () => W.clean('give me everything')],
    ['a tool_result with no id', () => W.clean([
      EXCHANGE[0], EXCHANGE[1],
      { role: 'user', content: [{ type: 'tool_result', content: 'x' }] }])],
  ];
  for (const [label, fn] of cases) {
    let got;
    try { got = fn(); } catch (e) { got = 'THREW ' + e.message; }
    check(got == null || got === undefined, 'REFUSED: ' + label,
      got == null ? 'refused' : 'ACCEPTED — ' + JSON.stringify(got).slice(0, 120));
  }
}

/* ---- the cache breakpoint cap ------------------------------------------- */
/* The board sends two breakpoints, the case index and one that moves along the
   tool results. Its first version ADDED one a round instead of moving it, so the
   fifth round carried five and the API answered 400: "A maximum of 4 blocks with
   cache_control may be provided. Found 5." A reader saw twenty seconds of work
   end in "the analyst endpoint answered with an error". The Worker caps it now,
   keeping the most recent four, because a slightly less cached answer beats no
   answer. */
{
  const bp = () => ({ type: "ephemeral", ttl: "1h" });
  const sys = [
    { type: "text", text: "CASE INDEX", cache_control: bp() },
    { type: "text", text: "CURRENT STATE" },
  ];
  const msgs = [
    { role: "user", content: "q" },
    { role: "assistant", content: [{ type: "tool_use", id: "t1", name: "nodes", input: {} }] },
    { role: "user", content: [{ type: "tool_result", tool_use_id: "t1", content: "a", cache_control: bp() }] },
    { role: "assistant", content: [{ type: "tool_use", id: "t2", name: "nodes", input: {} }] },
    { role: "user", content: [{ type: "tool_result", tool_use_id: "t2", content: "b", cache_control: bp() }] },
    { role: "assistant", content: [{ type: "tool_use", id: "t3", name: "nodes", input: {} }] },
    { role: "user", content: [{ type: "tool_result", tool_use_id: "t3", content: "c", cache_control: bp() }] },
    { role: "assistant", content: [{ type: "tool_use", id: "t4", name: "nodes", input: {} }] },
    { role: "user", content: [{ type: "tool_result", tool_use_id: "t4", content: "d", cache_control: bp() }] },
  ];
  const count = () => {
    let n = sys.filter((b) => b.cache_control).length;
    for (const m of msgs) {
      if (typeof m.content === "string") continue;
      n += m.content.filter((b) => b.cache_control).length;
    }
    return n;
  };
  const before = count();
  const dropped = W.capCacheBlocks(sys, msgs);
  const after = count();
  check(before === 5, "the fixture really carries five breakpoints", "found " + before);
  check(dropped === 1 && after === 4, "the Worker caps them at the API's four",
    "dropped " + dropped + ", " + after + " remain");
  /* Dropping the EARLIEST is the right end to drop from, and it costs nothing:
     caching is a prefix match, so the surviving breakpoint further along already
     covers everything before it, the case index included. */
  check(!sys[0].cache_control && msgs[8].content[0].cache_control,
    "it drops from the earliest end, which a later breakpoint already covers",
    "the case index breakpoint went, the last tool result's stayed, and the "
    + "latter's prefix contains the former");

  const sys2 = [{ type: "text", text: "x", cache_control: bp() }];
  const msgs2 = [{ role: "user", content: "q" }];
  check(W.capCacheBlocks(sys2, msgs2) === 0 && !!sys2[0].cache_control,
    "a request already within the limit is left alone", "nothing dropped");
}

/* ---- and the one that is neither: an over-long exchange is refused whole -- */
{
  const huge = [EXCHANGE[0], EXCHANGE[1], {
    role: 'user',
    content: [{ type: 'tool_result', tool_use_id: 'toolu_01A', content: 'x'.repeat(60_000) }],
  }];
  const got = W.clean(huge);
  const res = got && got[2].content[0];
  check(!!res && res.content.length === 40_000,
    'an over-long tool_result is capped, not refused', res ? res.content.length + ' characters' : 'refused whole');
}

console.log('\n  ' + ok + ' passed, ' + bad + ' failed');
console.log('\n' + (bad ? 'WORKER VALIDATORS FAILED (' + bad + ')' : 'WORKER VALIDATORS PASSED'));
process.exit(bad ? 1 : 0);
