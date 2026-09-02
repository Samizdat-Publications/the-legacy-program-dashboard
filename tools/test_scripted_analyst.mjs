/* Branch test for the no-key analyst.

   WHY THIS EXISTS. The scripted analyst is the only thing a reader without an
   API key ever hears from, and every failure mode it has is silent: it answers
   confidently, at length, with real figures, from the wrong branch. Six of the
   seven suggestion chips did exactly that on first write --

     "Trace the custody chain from Grusch"  answered with Grusch's dossier,
                                            because a name match beat the topic
     "What is the legal mechanism..."       matched a node label containing the
                                            word oversight
     "tell me about AAWSAP"                 hit the mechanism topic, because
                                            /sap/ matches inside the word aawsap
     "Export every Tier A node..."          hit the tier topic, because it was
                                            checked first

   -- and the first version of this test passed all six, because it asserted
   only that an answer came back, was long enough, and emitted valid commands.
   A check that cannot name the branch it expected cannot reject a wrong one.

   So every case asserts the TOPIC TAG, not the prose. Run:
     node tools/test_scripted_analyst.mjs
   Exits non-zero on any mismatch. Set BREAK=1 to prove it still fails when the
   function is broken -- a green check that has never been shown to go red is
   indistinguishable from a broken one. */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rd = p => fs.readFileSync(path.join(root, p), 'utf8');

const CASES = [
  // the seven chips, as shipped on 2 September 2026
  ['Where should I start?',                                          'start'],
  ['How did AAWSAP become AATIP, and then KONA BLUE?',               'lineage'],
  ['What did the Nimitz pilots see in 2004, and what has the government confirmed?', 'nimitz'],
  ['Trace the custody chain from Grusch back to a named contractor', 'custody'],
  ['Show me every entity the government has formally denied',        'denial'],
  ['Follow the money: who paid, and where does the trail stop?',     'money'],
  ['Which claims would collapse first under a hostile audit?',       'audit'],
  // the earlier chips, still valid questions
  ['What is the legal mechanism that lets a program escape oversight?', 'mechanism'],
  ['Plot the cover-up strand against the oversight strand on one axis', 'strands'],
  ['Chart the board by claim tier and show me where the evidence is thinnest', 'tiers'],
  ['Export every Tier A node to a spreadsheet with its axes and sources', 'export'],
  ['tic tac',                   'nimitz'],
  ['tell me about AAWSAP',      'entity'],
  ['who is Sean Kirkpatrick',   'entity'],
  ['david grusch',              'entity'],
  ['where do I start',          'start'],
  ['follow the money',          'money'],
  ['what about France',         'foreign'],
  ['download a csv',            'export'],
  ['asdfgh qwerty zxcvb',       'default'],
];

const html = rd('dist/the-program.html');
function slice(marker){
  const a = html.indexOf(marker);
  if (a < 0) throw new Error('not found in the build: ' + marker);
  let d = 0, k = html.indexOf('{', a);
  for (;; k++){
    if (html[k] === '{') d++;
    else if (html[k] === '}' && --d === 0) break;
  }
  return html.slice(a, k + 1);
}
let fn = slice('function scriptedReply');
if (process.env.BREAK === '1'){
  /* Self-test: disable the topic table so every probe falls through to the
     entity matcher or the default. If the test still passes, it is broken. */
  fn = fn.replace(/return say\('(custody|export|tiers|audit|denial|mechanism|strands|money|foreign|start|lineage|nimitz)',/g,
                  "return say('entity',");
}
const cmdBlock = html.slice(html.indexOf('const CMD = {'), html.indexOf('\n};', html.indexOf('const CMD = {')));
const CMDS = new Set([...cmdBlock.matchAll(/^  (\w+)\s*[:(]/gm)].map(m => m[1]));

const board  = JSON.parse(rd('data/the-program.json'));
const L0DATA = JSON.parse(rd('data/l0-model.json'));
const NODES  = (board.people || []).concat(board.entities || []);

let ran = [];
const S = { turns: [] };
const scriptedReply = new Function('NODES','L0DATA','S','renderTranscript','runCommandLine',
  fn + '; return scriptedReply;')(NODES, L0DATA, S, () => {}, l => { ran.push(l); return true; });

let fails = 0;
for (const [q, want] of CASES){
  S.turns.length = 0; ran = [];
  scriptedReply(q);
  await new Promise(r => setTimeout(r, 700));   // actions fire on a stagger
  const turn = S.turns[S.turns.length - 1] || {};
  const got = turn.topic || '(untagged)';
  const txt = turn.text || '';
  const acts = turn.actions || [];
  const bad = [];
  if (got !== want) bad.push('branch: wanted ' + want + ', got ' + got);
  if (txt.length < 400 && want !== 'default') bad.push('answer is only ' + txt.length + ' chars');
  if (/undefined|NaN|\[object Object\]/.test(txt)) bad.push('an interpolation produced undefined/NaN');
  for (const a of acts){
    const m = String(a).match(/^(\w+)\s*\(/);
    if (!m) bad.push('unparseable action: ' + String(a).slice(0, 40));
    else if (!CMDS.has(m[1])) bad.push('action calls a command that does not exist: ' + m[1]);
  }
  if (acts.length && ran.length !== acts.length) bad.push('not every action actually ran');
  if (bad.length) fails++;
  console.log((bad.length ? 'FAIL ' : 'ok   ') + got.padEnd(10) +
    String(txt.length).padStart(5) + 'ch  ' + q.slice(0, 52));
  bad.forEach(b => console.log('       -> ' + b));
}
console.log('\n' + (fails ? fails + ' of ' + CASES.length + ' FAILED'
                          : 'all ' + CASES.length + ' branch assertions pass'));
process.exit(fails ? 1 : 0);
