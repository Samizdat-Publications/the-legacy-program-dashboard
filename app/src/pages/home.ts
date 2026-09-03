/* Home — Design response section 1.2.
 *
 * Search first, the paragraph, the six entry paths as cards, the fourteen
 * start-here chips in the owner's reading order, the counts table, the analyst.
 *
 * Every figure on this page is read from index.json. None is typed in here.
 */
import { h, clear } from '../dom';
import { searchBox } from '../search';
import { setTitle } from '../router';
import {
  loadIndex, loadHighlights, loadMap, loadAnalyst, clsLetter,
  type BoardIndex, type Highlight, type EntryPath,
} from '../data';
import { ask, probeEndpoint, type Turn } from '../analyst';

const n = (x: number) => x.toLocaleString('en-GB');

export async function renderHome(view: HTMLElement): Promise<void> {
  setTitle();
  clear(view);
  const wrap = h('div', { class: 'home' });
  const main = h('div', { class: 'home-main' });
  const side = h('div', { class: 'home-side' });
  wrap.append(main, side);
  view.append(wrap);

  const [idx, hl, map, an] = await Promise.all([
    loadIndex(),
    loadHighlights().catch(() => ({ flags: [] as Highlight[] })),
    loadMap().catch(() => ({ entryPaths: [] as EntryPath[] })),
    loadAnalyst().catch(() => ({ worker: '', suggestions: [] as string[] })),
  ]);

  const claimTotal = Object.values(idx.counts.claims).reduce((a, b) => a + b, 0);

  /* ---- search, large ---------------------------------------------------- */
  main.append(searchBox({
    big: true,
    placeholder: 'Search ' + n(idx.counts.nodes) + ' nodes, ' + n(claimTotal) +
      ' claims, ' + n(idx.counts.timeline) + ' events · a name, a programme, a statute',
  }));

  /* ---- the paragraph. The one placeholder this build is allowed to leave:
     Stewart writes it. Design's draft is inside the brackets so the page still
     says what the board is while it waits. ------------------------------- */
  main.append(h('p', { class: 'home-para', 'data-placeholder': '1' },
    h('span', { class: 'ph' }, '[placeholder: the Home paragraph — Stewart writes this. Design\'s draft, from the brief: '),
    '“A research board on the alleged US programme for recovering and reverse-engineering ' +
    'non-human craft, 1944 to now. It is a sourced graph: every node carries claims graded ' +
    'by evidence strength — ',
    h('span', { class: 't1' }, 'Tier 1'), ' documented, ',
    h('span', { class: 't2' }, 'Tier 2'), ' a named person on the record, ',
    h('span', { class: 't3' }, 'Tier 3'), ' stated inference. Every edge is hand-written and ' +
    'sourced. Where what a witness said and what the record shows disagree, the contradiction ' +
    'is recorded as a finding.”',
    h('span', { class: 'ph' }, ']'),
  ));

  /* ---- the six entry paths --------------------------------------------- */
  if (map.entryPaths.length) {
    const paths = h('div', { class: 'paths' });
    for (const p of map.entryPaths) {
      paths.append(h('a', { class: 'path', href: '#/t/' + p.id },
        h('div', { class: 'path-head' },
          h('span', { class: 'path-title' }, p.label),
          h('span', { class: 'path-go' }, 'THREAD ›'),
        ),
        h('div', { class: 'path-blurb' }, p.blurb),
        h('div', { class: 'path-counts' }, n(p.total) + ' nodes · ' + n(p.onMap) + ' on the map'),
      ));
    }
    main.append(paths);
  }

  /* ---- the start-here register. The flags carry the id, the owner's rank and
     the reason; the name and the class come from the index, so the chip can
     never disagree with the node page. --------------------------------- */
  if (hl.flags.length) {
    const byId = new Map(idx.nodes.map((x) => [x.id, x]));
    const sh = h('div', { class: 'starthere' });
    sh.append(h('div', null,
      h('span', { class: 'amber eyebrow' }, 'Start here'), ' ',
      h('span', { class: 'dim' }, hl.flags.length + ' nodes, flagged by the owner · numbered in reading order'),
    ));
    const chips = h('div', { class: 'chips' });
    for (const f of hl.flags.slice().sort((a, b) => a.rank - b.rank)) {
      const node = byId.get(f.id);
      chips.append(h('a', { class: 'chip', href: '#/n/' + f.id, title: f.why },
        h('span', { class: 'chip-n' }, String(f.rank)),
        h('span', { class: 'chip-body' },
          h('span', { class: 'chip-cls' }, clsLetter(node ? node.cls : '')),
          h('span', { class: 'label' }, node ? node.short || node.label : f.id),
        ),
      ));
    }
    sh.append(chips);
    main.append(sh);
  }

  /* ---- what is on the board -------------------------------------------- */
  side.append(countsPanel(idx, claimTotal));

  /* ---- the analyst ------------------------------------------------------ */
  side.append(analystPanel(an.suggestions));
}

function countsPanel(idx: BoardIndex, claimTotal: number): HTMLElement {
  const c = idx.counts;
  const rows: [string, string][] = [
    [n(c.nodes), 'nodes · ' + n(c.people) + ' people · ' + n(c.entities) + ' entities'],
    [n(c.edges), 'sourced edges'],
    [n(claimTotal), 'claims · T1 ' + n(c.claims['1'] ?? 0) + ' · T2 ' + n(c.claims['2'] ?? 0) + ' · T3 ' + n(c.claims['3'] ?? 0)],
    [n(c.timeline), 'timeline events'],
    [n(c.l0), 'nodes on the program map · ' + idx.bands.length + ' bands · ' + idx.eras.length + ' eras'],
    [n(c.threads ?? 0), 'threads'],
    [n(c.patents ?? 0) + ' · ' + n(c.sheets ?? 0), 'Navy patents · drawing sheets'],
    [n(c.foia.requests) + ' · ' + n(c.foia.questions),
      'FOIA requests · open questions on ' + n(c.foia.nodes) + ' nodes'],
  ];
  const table = h('table');
  for (const [num, key] of rows) {
    table.append(h('tr', null, h('td', { class: 'n' }, num), h('td', { class: 'k' }, key)));
  }
  return h('section', { class: 'panel counts' },
    h('div', { class: 'eyebrow' }, 'What is on the board'),
    table,
    h('div', { class: 'faint', style: 'margin-top:8px' }, 'generated ' + (idx.generated || '').slice(0, 10)),
  );
}

function analystPanel(suggestions: string[]): HTMLElement {
  const panel = h('section', { class: 'panel analyst' });
  const status = h('span', { class: 'faint' }, 'answers cite nodes · the only runtime fetch');
  panel.append(h('div', { class: 'analyst-head' },
    h('span', { class: 'eyebrow' }, 'Ask the analyst'), status));

  const input = h('input', {
    type: 'text',
    placeholder: 'Ask a question about the record…',
    'aria-label': 'Ask the analyst',
  });
  panel.append(input);

  const list = h('div', { class: 'suggest' });
  const transcript = h('div', { class: 'transcript' });
  panel.append(list, transcript);

  const turns: Turn[] = [];
  let busy = false;

  const paint = () => {
    clear(transcript);
    for (const t of turns) {
      transcript.append(h('div', { class: 'turn ' + (t.role === 'you' ? 'you' : '') + (t.err ? ' err' : '') },
        h('div', { class: 'who' }, t.role === 'you' ? 'YOU' : 'ANALYST'),
        h('div', { class: 'say' }, t.thinking ? 'thinking…' : t.text),
      ));
    }
  };

  const send = async (q: string) => {
    if (busy || !q.trim()) return;
    busy = true;
    list.hidden = true;
    turns.push({ role: 'you', text: q });
    const pending: Turn = { role: 'analyst', text: '', thinking: true };
    turns.push(pending);
    paint();
    const nodeId = (location.hash.match(/^#\/(?:n|report\/n)\/([a-z0-9._-]+)/) || [])[1] || null;
    const reply = await ask(q, turns.slice(0, -2), nodeId);
    turns[turns.length - 1] = reply;
    busy = false;
    paint();
  };

  for (const s of suggestions) {
    list.append(h('button', { type: 'button', onclick: () => void send(s) },
      h('span', { class: 'faint' }, '›'), h('span', null, s)));
  }

  input.addEventListener('keydown', (e) => {
    if ((e as KeyboardEvent).key !== 'Enter') return;
    const q = input.value;
    input.value = '';
    void send(q);
  });

  void probeEndpoint().then((ep) => {
    status.textContent = ep
      ? 'live on this deployment · no key needed'
      : 'endpoint not reachable from here · the board works by hand';
  });

  return panel;
}
