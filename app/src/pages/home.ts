/* Home: rebuilt around topics in redesign phase 6 (redesign section 5, "Home").
 *
 * Search first; what the board is and how to read a tier, the "said on the
 * record" mark included; Start here, the owner's fourteen flags as a tour of
 * their topics in the signed-off order; the ten sections with their topics;
 * the counts, and the big questions (phase 10).
 *
 * Every figure on this page is read from index.json or topics.json. None is
 * typed in here. app/checks/run.mjs C11, C27 and C38 hold it to the data.
 */
import { h, clear } from '../dom';
import { searchBox } from '../search';
import { setTitle } from '../router';
import {
  loadIndex, loadHighlights, loadTopics, spanText,
  type BoardIndex, type Highlight, type TopicsFile,
} from '../data';
import { SAID_LABEL, SAID_TITLE, READ_T1, SAID_TWICE } from '../attrib';
import { loadQuestions } from '../p10data';

const n = (x: number) => x.toLocaleString('en-GB');

export async function renderHome(view: HTMLElement): Promise<void> {
  setTitle();
  clear(view);
  const wrap = h('div', { class: 'home' });
  const main = h('div', { class: 'home-main' });
  const side = h('div', { class: 'home-side' });
  const wide = h('div', { class: 'home-wide' });
  wrap.append(main, side);
  view.append(wrap, wide);

  const [idx, hl, tf] = await Promise.all([
    loadIndex(),
    loadHighlights().catch(() => ({ flags: [] as Highlight[] })),
    loadTopics().catch(() => null),
  ]);

  const claimTotal = Object.values(idx.counts.claims).reduce((a, b) => a + b, 0);

  /* ---- search, large ---------------------------------------------------- */
  main.append(searchBox({
    big: true,
    /* a placeholder that does not fit its field is a cut label, so a phone
       gets the short one */
    placeholder: window.innerWidth <= 760 ? 'Search the board'
      : 'Search ' + n(idx.counts.nodes) + ' nodes, ' + n(claimTotal) +
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

  /* ---- how to read a tier, and the mark ---------------------------------- */
  main.append(h('div', { class: 'home-tiers' },
    h('div', { class: 'eyebrow' }, 'How to read a claim'),
    h('div', { class: 'ht-row' }, h('span', { class: 'ht-k t1' }, 'T1'),
      h('span', null, 'a primary record says so: a document, a statute, a filing, a transcript.')),
    h('div', { class: 'ht-row' }, h('span', { class: 'ht-k t2' }, 'T2'),
      h('span', null, 'a named person on the record says so: testimony, an allegation, an official statement.')),
    h('div', { class: 'ht-row' }, h('span', { class: 'ht-k t3' }, 'T3'),
      h('span', null, 'a stated inference: what the board reasons from the record, flagged as such.')),
    h('div', { class: 'ht-row said-read' }, h('span', { class: 'ht-k' }), h('span', null, READ_T1)),
    h('div', { class: 'ht-row said-twice' }, h('span', { class: 'ht-k' }), h('span', null, SAID_TWICE)),
    h('div', { class: 'ht-row' }, h('span', { class: 'said-mark' }, SAID_LABEL.said),
      h('span', null, SAID_TITLE.said)),
    h('div', { class: 'ht-row' }, h('span', { class: 'said-mark' }, SAID_LABEL.office),
      h('span', null, SAID_TITLE.office)),
  ));

  /* ---- start here: the flags as a tour of their topics ------------------- */
  if (hl.flags.length) {
    const byId = new Map(idx.nodes.map((x) => [x.id, x]));
    const titleOf = new Map((tf ? tf.topics : []).map((t) => [t.id, t.title]));
    const sh = h('section', { class: 'starthere' });
    sh.append(h('div', { class: 'sh-head' },
      h('span', { class: 'amber eyebrow' }, 'Start here'), ' ',
      h('span', { class: 'dim' }, 'a tour in ' + hl.flags.length +
        ' steps, in the owner\'s reading order: a record the owner flagged, and the topic to read it in')));
    const ol = h('ol', { class: 'tour' });
    for (const f of hl.flags.slice().sort((a, b) => a.rank - b.rank)) {
      const node = byId.get(f.id);
      const first = tf && (tf.appearsIn[f.id] || [])[0];
      /* the flagged record is the step's headline and its topic is where the
         step opens: two flags can share a topic, and a tour that printed the
         same title twice read as a mistake (blind critic, phase 6 round 1) */
      ol.append(h('li', { class: 'tour-step' },
        h('span', { class: 'tour-n' }, String(f.rank)),
        h('div', { class: 'tour-body' },
          h('a', { class: 'tour-node', href: '#/n/' + f.id }, node ? node.label : f.id),
          h('div', { class: 'tour-via' },
            h('span', { class: 'dim' }, 'read it in the topic '),
            first
              ? h('a', { class: 'tour-topic', href: '#/topic/' + first[0] }, titleOf.get(first[0]) || first[0])
              : h('span', { class: 'tour-topic faint' }, 'in no topic yet')),
          h('div', { class: 'tour-why dim' }, f.why),
        ),
      ));
    }
    sh.append(ol);
    wide.append(sh);
  }

  /* ---- the big questions (phase 10), each linking its page ---------------- */
  const qf = await loadQuestions().catch(() => null);
  if (qf && qf.questions.length) {
    const qs = qf.questions.slice().sort((a, b) => a.order - b.order);
    const ol = h('ol', { class: 'home-qlist' });
    for (const q of qs) ol.append(h('li', null, h('a', { class: 'home-q', href: '#/q/' + q.id }, q.title)));
    wide.append(h('section', { class: 'home-questions' },
      h('div', { class: 'sec-head' }, h('span', { class: 'eyebrow' }, 'Big questions'), ' ',
        h('span', { class: 'dim' }, qs.length + ' questions, each answered so far from the record, with the case for and against · '),
        h('a', { href: '#/questions' }, 'all questions ›')),
      ol));
  }

  /* ---- the sections, each with its topics -------------------------------- */
  if (tf) wide.append(sections(tf));

  /* ---- what is on the board -------------------------------------------- */
  side.append(countsPanel(idx, claimTotal, tf));
  side.append(h('a', { class: 'home-atlas', href: '#/atlas' },
    h('span', { class: 'eyebrow cyan' }, 'Open the Atlas ›'),
    h('span', { class: 'dim' }, 'every topic on one page, by section and era')));
}

function sections(tf: TopicsFile): HTMLElement {
  const box = h('section', { class: 'home-sections' },
    h('div', { class: 'sec-head' }, h('span', { class: 'eyebrow' }, 'The sections'), ' ',
      h('span', { class: 'dim' }, tf.sections.length + ' sections, ' + tf.topics.length + ' topics')));
  const grid = h('div', { class: 'hsec-grid' });
  for (const s of tf.sections) {
    const ts = tf.topics.filter((t) => t.section === s.id)
      .sort((a, b) => Number(a.focusEra) - Number(b.focusEra) ||
        String((a.span && a.span.from) || '').localeCompare(String((b.span && b.span.from) || '')));
    const ul = h('ul', { class: 'hsec-topics' });
    for (const t of ts) {
      ul.append(h('li', null,
        h('a', { class: 'hsec-topic', href: '#/topic/' + t.id }, t.title), ' ',
        h('span', { class: 'faint' }, spanText(t.span))));
    }
    grid.append(h('div', { class: 'hsec', 'data-section': s.id },
      h('h3', { class: 'hsec-title' }, s.title),
      h('p', { class: 'hsec-blurb dim' }, s.blurb),
      ul));
  }
  box.append(grid);
  return box;
}

function countsPanel(idx: BoardIndex, claimTotal: number, tf: TopicsFile | null): HTMLElement {
  const c = idx.counts;
  const rows: [string, string][] = [
    [n(c.nodes), 'nodes · ' + n(c.people) + ' people · ' + n(c.entities) + ' entities'],
    [n(tf ? tf.topics.length : 0), 'topics · ' + n(tf ? tf.sections.length : 0) + ' sections'],
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
