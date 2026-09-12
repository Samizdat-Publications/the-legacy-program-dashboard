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
  loadIndex, loadHighlights, loadMap, clsLetter,
  type BoardIndex, type Highlight, type EntryPath,
} from '../data';

const n = (x: number) => x.toLocaleString('en-GB');

export async function renderHome(view: HTMLElement): Promise<void> {
  setTitle();
  clear(view);
  /* Two columns for the top of the page, then FULL WIDTH for the cards and the
     start-here register. The rail used to carry the counts panel and the
     analyst below it; the analyst moved to the dock on 11 September and left a
     420px hole beside the entry paths, which is what `wide` is for. */
  const wrap = h('div', { class: 'home' });
  const main = h('div', { class: 'home-main' });
  const side = h('div', { class: 'home-side' });
  const wide = h('div', { class: 'home-wide' });
  wrap.append(main, side);
  view.append(wrap, wide);

  const [idx, hl, map] = await Promise.all([
    loadIndex(),
    loadHighlights().catch(() => ({ flags: [] as Highlight[] })),
    loadMap().catch(() => ({ entryPaths: [] as EntryPath[] })),
  ]);

  const claimTotal = Object.values(idx.counts.claims).reduce((a, b) => a + b, 0);

  /* ---- search, large ---------------------------------------------------- */
  main.append(searchBox({
    big: true,
    placeholder: 'Search ' + n(idx.counts.nodes) + ' nodes, ' + n(claimTotal) +
      ' claims, ' + n(idx.counts.timeline) + ' events · a name, a programme, a statute',
  }));

  /* ---- the paragraph. Stewart's own text. Every figure in it is read from
     index.json above, so it can never drift from the board. --------------- */
  main.append(h('p', { class: 'home-para' },
    'A research board on the alleged United States programme for recovering and ' +
    'reverse-engineering non-human craft, 1944 to now. It is a sourced graph: ' +
    n(idx.counts.nodes) + ' people, institutions, programmes, documents, events, laws and ' +
    'places, joined by ' + n(idx.counts.edges) + ' hand-written edges that each cite a ' +
    'document, and ' + n(claimTotal) + ' claims graded by evidence strength: ',
    h('span', { class: 't1' }, 'Tier 1'), ' documented (' + n(idx.counts.claims['1'] ?? 0) + '), ',
    h('span', { class: 't2' }, 'Tier 2'), ' a named person on the record (' + n(idx.counts.claims['2'] ?? 0) + '), ',
    h('span', { class: 't3' }, 'Tier 3'), ' stated inference (' + n(idx.counts.claims['3'] ?? 0) + '). ' +
    'Where what a witness said and what the record shows disagree, the contradiction is ' +
    'recorded as a finding. Statements by AARO and the Department of Defense are treated ' +
    "as an interested party's and capped at Tier 2 unless the claim is about what they " +
    'said. No source, URL, document number or quotation appears here that was not opened.',
  ));

  /* ---- the six entry paths --------------------------------------------- */
  if (map.entryPaths.length) {
    const paths = h('div', { class: 'paths' });
    /* An entry path is the L0 model's grouping (custody, denial, foreign,
       mechanism, money, witness); a thread is an authored chain in
       research/threads.json. Three of the six have a thread of the same subject
       and link to it; the other three open the map, because a link to a thread
       that does not exist landed four of six cards on the not-found page
       (check C9, 3 September 2026). */
    const THREAD_FOR: Record<string, string> = { custody: 'custody', money: 'money', denial: 'denials' };
    for (const p of map.entryPaths) {
      const t = THREAD_FOR[p.id];
      paths.append(h('a', { class: 'path', href: t ? '#/t/' + t : '#/map' },
        h('div', { class: 'path-head' },
          h('span', { class: 'path-title' }, p.label),
          h('span', { class: 'path-go' }, t ? 'THREAD ›' : 'MAP ›'),
        ),
        h('div', { class: 'path-blurb' }, p.blurb),
        h('div', { class: 'path-counts' }, n(p.total) + ' nodes · ' + n(p.onMap) + ' on the map'),
      ));
    }
    wide.append(paths);
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
    wide.append(sh);
  }

  /* ---- what is on the board -------------------------------------------- */
  side.append(countsPanel(idx, claimTotal));

  /* The analyst used to be the second panel in this rail. It is now mounted on
     every route by main.ts, below the page: analyst/panel.ts. */
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
