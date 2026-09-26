/* Questions: redesign section 5, "Questions", and phase 10 task 3.
 *
 *   #/questions        the big questions, in reading order
 *   #/q/<id>           one question: the answer so far, the evidence for and
 *                      against side by side, the open questions, and the threads
 *                      folded in as chains of evidence
 *
 * Authored in research/questions/<id>.json and checked like a topic (verify.py):
 * every sentence cites a claim or a link on the board, a quotation is verbatim in
 * what it cites, the case against is present. Every sentence here carries its
 * numbered references and each cite prints in full under it, exactly as on a
 * topic page (topic.ts item and cite). Nothing on this page is written here.
 * app/checks/run.mjs C61 holds it to its record.
 */
import '../styles/topic.css';
import '../styles/questions.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadTopics, loadThreads, loadIndex, clsColour, type ThreadsFile } from '../data';
import { loadQuestions, loadQuestion, type QuestionRecord } from '../p10data';
import { notFound } from './notfound';
import { item } from './topic';
import { saidKey, READ_T1, type Said } from '../attrib';

export async function renderQuestions(view: HTMLElement): Promise<void> {
  clear(view);
  setTitle('Questions');
  const qf = await loadQuestions().catch(() => null);
  const page = h('article', { class: 'questions' });
  view.append(page);
  page.append(h('div', { class: 'crumb' }, h('div', { class: 'crumb-l' }, h('span', { class: 'eyebrow' }, 'Questions'))));
  page.append(h('h1', { class: 'topic-h1' }, 'The big questions'));
  page.append(h('p', { class: 'dim q-intro' },
    'Each question gathers what the board holds on it: the answer so far, the evidence for and the evidence ' +
    'against side by side, what is still open, and the authored threads that bear on it as chains of evidence. ' +
    'Every sentence cites the claims and links it rests on.'));
  const qs = qf ? qf.questions.slice().sort((a, b) => a.order - b.order) : [];
  if (!qs.length) {
    page.append(h('p', { class: 'faint' }, 'No question is on the board yet.'));
    return;
  }
  const ol = h('ol', { class: 'qlist' });
  for (const q of qs) {
    ol.append(h('li', { class: 'qrow', 'data-id': q.id },
      h('a', { class: 'qrow-title', href: '#/q/' + q.id }, q.title),
      q.lead ? h('p', { class: 'qrow-lead' }, q.lead) : null,
      h('div', { class: 'qrow-counts faint' },
        q.counts.for + ' for · ' + q.counts.against + ' against · ' + q.counts.open + ' open · ' +
        q.counts.threads + (q.counts.threads === 1 ? ' thread' : ' threads'))));
  }
  page.append(ol);
}

export async function renderQuestion(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  let q: QuestionRecord;
  try {
    q = await loadQuestion(id);
  } catch {
    notFound(view, '#/q/' + id, 'No question with this id is on the board.');
    return;
  }
  setTitle(q.title);
  const [tf, th, idx, qf] = await Promise.all([
    loadTopics().catch(() => null), loadThreads().catch(() => null as ThreadsFile | null),
    loadIndex(), loadQuestions().catch(() => null),
  ]);
  const titleOf = new Map((tf ? tf.topics : []).map((t) => [t.id, t.title]));
  const nodeOf = new Map(idx.nodes.map((n) => [n.id, n]));
  const threads = new Map((th ? th.threads : []).map((t) => [t.id, t]));

  const num = new Map<string, number>();
  const numberOf = (cid: string): number => {
    let n = num.get(cid);
    if (n == null) { n = num.size + 1; num.set(cid, n); }
    return n;
  };
  const kinds = new Set<Said>();

  const page = h('article', { class: 'topic question', 'data-id': q.id });
  view.append(page);
  const all = qf ? qf.questions.slice().sort((a, b) => a.order - b.order) : [];
  const at = all.findIndex((x) => x.id === q.id);
  page.append(h('div', { class: 'crumb topic-crumb' },
    h('div', { class: 'crumb-l' },
      h('a', { class: 'eyebrow', href: '#/questions' }, 'Questions'),
      h('span', { class: 'sep' }, '›'),
      h('span', { class: 'eyebrow' }, at >= 0 ? (at + 1) + ' of ' + all.length : 'a question')),
    at >= 0 && at + 1 < all.length
      ? h('a', { class: 'dim q-next', href: '#/q/' + all[at + 1].id }, 'next: ' + all[at + 1].title + ' ›') : null,
  ));
  page.append(h('h1', { class: 'topic-h1' }, q.title));

  /* the answer so far: the lead, then its sentences */
  const prose = h('section', { class: 'topic-prose q-answer', 'data-block': 'answer' },
    h('div', { class: 'eyebrow' }, 'The answer so far'));
  if (q.lead) prose.append(item(q.lead, 'lead', q, numberOf, kinds));
  for (const s of q.answer || []) prose.append(item(s, 'answer', q, numberOf, kinds));
  page.append(prose);

  /* for and against, side by side */
  const grid = h('div', { class: 'tblocks q-blocks' });
  const blocks: ['for' | 'against', string, string, string][] = [
    ['for', 'The evidence for', 'what the record and the witnesses offer, graded', 'b-claimed'],
    ['against', 'The evidence against', 'denials, conflicts and the case against', 'b-contested'],
  ];
  for (const [k, head, blurb, cls] of blocks) {
    const xs = q[k] || [];
    const col = h('section', { class: 'tblock ' + cls, 'data-block': k },
      h('div', { class: 'tblock-head' }, h('span', { class: 'eyebrow' }, head), ' ',
        h('span', { class: 'dim' }, '· ' + xs.length + ' · ' + blurb)));
    for (const it of xs) col.append(item(it, k, q, numberOf, kinds));
    grid.append(col);
  }
  page.append(grid);

  /* the key to the marks, where the reader first meets the cites */
  const key = saidKey(kinds);
  if (key) { key.classList.add('topic-key'); page.insertBefore(key, prose); }
  else page.insertBefore(h('div', { class: 'said-key dim topic-key' }, h('div', { class: 'said-read' }, READ_T1)), prose);

  /* the threads as chains of evidence */
  if ((q.threads || []).length) {
    const sec = h('section', { class: 'q-threads', 'data-block': 'threads' },
      h('div', { class: 'sec eyebrow' }, 'Chains of evidence · ' + q.threads.length));
    for (const t of q.threads) {
      const thr = threads.get(t.id);
      const box = h('div', { class: 'q-thread', 'data-thread': t.id },
        h('a', { class: 'q-thread-title', href: '#/t/' + t.id }, thr ? thr.title : t.id));
      box.append(item(t, 'threads', q, numberOf, kinds));
      if (thr) {
        const ol = h('ol', { class: 'q-steps' });
        for (const st of thr.steps) {
          const n = nodeOf.get(st.node);
          ol.append(h('li', { class: 'q-step' },
            h('span', { class: 'yr faint' }, st.year != null ? String(st.year) : ''),
            h('a', { href: '#/n/' + st.node }, mark(clsColour(n ? n.cls : '')), ' ', n ? n.label : st.node),
            h('span', { class: 'dim q-step-ev' }, st.evidence)));
        }
        box.append(ol);
      }
      sec.append(box);
    }
    page.append(sec);
  }

  /* open questions, and the topics this draws on */
  const tail = h('div', { class: 'topic-tail' });
  if ((q.open || []).length) {
    const ol = h('ol', { class: 'tq' });
    for (const x of q.open) ol.append(h('li', null, x));
    tail.append(h('section', { class: 'topic-questions', 'data-block': 'open' },
      h('div', { class: 'sec eyebrow' }, 'Still open · ' + q.open.length), ol));
  }
  const rel = (q.topics || []).filter((t) => titleOf.has(t));
  if (rel.length) {
    const ul = h('div', { class: 'related-list' });
    for (const t of rel) ul.append(h('a', { class: 'related', href: '#/topic/' + t }, titleOf.get(t)!));
    tail.append(h('section', { class: 'topic-related' },
      h('div', { class: 'sec eyebrow' }, 'Topics to read · ' + rel.length), ul));
  }
  if (tail.childNodes.length) page.append(tail);
}
