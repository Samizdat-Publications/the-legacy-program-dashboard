/* Thread page: Design response section 1.6, route #/t/<id>.
 *
 * A rail of the eight threads across the top. Left: the ordered chain, one step
 * per row with class mark, year, the evidence line, and the join graded
 * type · tier · direct|derived (with the via ids on a derived join). Right: the
 * small map on the program grid, and a timeline slice of the steps' years.
 *
 * Every string on this page comes from data/threads.json or data/index.json.
 * The evidence lines are the authored ones; nothing is written here, and a step
 * with no join prints "thread start" rather than an invented one.
 */
import '../styles/thread.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadIndex, clsColour, type IndexNode } from '../data';
import { loadThreads, loadGrid, threadById, edgeLine, type Thread } from '../thread/data';
import { renderSmallMap } from '../thread/smallmap';
import { renderSlice } from '../thread/slice';
import { notFound } from './notfound';

export async function renderThread(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  const [tf, idx, grid] = await Promise.all([loadThreads(), loadIndex(), loadGrid()]);
  const th = threadById(tf, id);
  if (!th) {
    notFound(view, '#/t/' + id,
      'The eight authored threads are ' + tf.threads.map((t) => t.id).join(', ') + '.');
    return;
  }
  setTitle(th.label, 'Thread');

  const byId = new Map<string, IndexNode>();
  for (const n of idx.nodes) byId.set(n.id, n);
  const onGrid = new Set(grid.nodes.map((n) => n.id));
  const nOnMap = th.steps.filter((s) => onGrid.has(s.node)).length;

  /* ---- rail ------------------------------------------------------------ */
  const rail = h('div', { class: 'th-rail' });
  tf.threads.forEach((t, i) => {
    rail.append(h('a', {
      class: 'th-rail-item' + (t.id === th.id ? ' on' : ''),
      href: '#/t/' + t.id,
      'aria-current': t.id === th.id ? 'page' : null,
    }, h('span', { class: 'th-rail-n' }, String(i + 1)), ' ', t.label));
  });

  const head = h('div', { class: 'th-head' },
    h('div', { class: 'th-head-l' },
      h('span', { class: 'eyebrow' }, 'Thread'),
      h('h1', { class: 'th-h1' }, th.title),
      h('span', { class: 'dim th-head-n' },
        th.steps.length + ' steps · ' + nOnMap + ' on the map'),
    ),
    rail,
  );
  view.append(head);

  const wrap = h('div', { class: 'thread' });
  const left = h('div', { class: 'th-chain' });
  const right = h('div', { class: 'th-side' });
  wrap.append(left, right);
  view.append(wrap);

  /* ---- blurb and chain ------------------------------------------------- */
  left.append(h('p', { class: 'th-blurb' }, th.blurb));
  left.append(chain(th, byId, onGrid));

  /* ---- the small map and the slice ------------------------------------- */
  const mapHost = h('div', { class: 'th-map' });
  const sliceHost = h('div', { class: 'th-slice' });
  right.append(mapHost, sliceHost);

  const w = Math.max(280, Math.floor(right.getBoundingClientRect().width) - 4);
  renderSmallMap(mapHost, th, grid, byId, w);
  renderSlice(sliceHost, th, byId, w);
}

function chain(th: Thread, byId: Map<string, IndexNode>, onGrid: Set<string>): HTMLElement {
  const list = h('ol', { class: 'th-steps' });
  th.steps.forEach((s, i) => {
    const n = byId.get(s.node);
    const row = h('li', { class: 'th-step', 'data-node': s.node });
    row.append(h('span', { class: 'th-n' }, String(i + 1)));

    const body = h('div', { class: 'th-body' });
    const title = h('div', { class: 'th-title' },
      mark(n ? clsColour(n.cls) : 'var(--line2)'),
      h('a', { class: 'th-label', href: '#/n/' + s.node }, n ? n.label : s.node),
      h('span', { class: 'th-year dim' }, s.year == null ? 'no year on the board' : String(s.year)),
      n && n.hl ? h('span', { class: 'th-hl amber' }, 'start here ' + n.hl) : null,
      onGrid.has(s.node) ? null : h('span', { class: 'th-floor faint' }, 'below the L0 floor'),
    );
    body.append(title);
    body.append(h('div', { class: 'th-ev' }, s.evidence));
    body.append(h('div', { class: 'th-edge dim' }, edgeLine(s.edge)));
    row.append(body);
    list.append(row);
  });
  return list;
}
