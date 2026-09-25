/* thread/slice.ts: the timeline slice on the Thread page: the steps' own years.
 *
 * One tick per year the chain touches. A year's label is drawn only where the
 * whole label fits clear of the one before it, which is the label rule of
 * Design section 2.2; what will not fit is counted, never shrunk and never
 * truncated. Steps the board dates with nothing are named under the axis rather
 * than given a year.
 */
import { h, clear } from '../dom';
import { clsColour, type IndexNode } from '../data';
import { textWidth } from '../timeline/layout';
import type { Thread } from './data';

const PAD_R = 12;
const LABEL_GAP = 10;

export function renderSlice(
  host: HTMLElement, thread: Thread, byId: Map<string, IndexNode>, width: number,
): void {
  clear(host);
  const dated = thread.steps
    .map((s, i) => ({ step: i + 1, node: s.node, year: s.year }))
    .filter((s) => s.year != null) as { step: number; node: string; year: number }[];
  const undated = thread.steps
    .map((s, i) => ({ step: i + 1, node: s.node, year: s.year }))
    .filter((s) => s.year == null);

  if (!dated.length) {
    host.append(h('div', { class: 'ts-cap dim' }, 'Timeline slice · no step on this thread carries a year'));
    return;
  }

  const years: number[] = [];
  for (const d of dated) if (years.indexOf(d.year) < 0) years.push(d.year);
  years.sort((a, b) => a - b);
  const lo = years[0];
  const hi = years[years.length - 1];
  const span = Math.max(1, hi - lo);
  const inner = Math.max(120, width - PAD_R);

  host.append(h('div', { class: 'ts-cap dim' },
    'Timeline slice · ' + lo + ' – ' + hi + ' · ' + dated.length + ' of ' + thread.steps.length + ' steps dated'));

  const axis = h('div', { class: 'ts-axis', style: 'width:' + Math.round(inner + PAD_R) + 'px' });

  /* ticks */
  for (const y of years) {
    const x = ((y - lo) / span) * inner;
    axis.append(h('i', { class: 'ts-tick', style: 'left:' + x.toFixed(1) + 'px', 'aria-hidden': 'true' }));
  }

  /* Labels are placed left to right into rows: a label goes into the first row
     where its whole text is clear of everything already there. Nothing is
     shrunk or truncated to make room, and a label with no row at all is
     counted rather than drawn on top of another. */
  const rows: { x0: number; x1: number }[][] = [];
  let dropped = 0;
  let usedRows = 0;
  let maxNames = 1;
  for (const y of years) maxNames = Math.max(maxNames, dated.filter((d) => d.year === y).length);
  const rowH = 18 + maxNames * 15;
  for (const y of years) {
    const mine = dated.filter((d) => d.year === y);
    const head = String(y) + '  ' + mine.map((m) => m.step).join(' ');
    const names = mine.map((m) => { const n = byId.get(m.node); return n ? (n.short || n.label) : m.node; });
    let wNeeded = textWidth(head);
    for (const s of names) wNeeded = Math.max(wNeeded, textWidth(s));
    const x = ((y - lo) / span) * inner;
    if (x + wNeeded > inner + PAD_R) { dropped++; continue; }

    let row = -1;
    for (let r = 0; r < 8; r++) {
      if (!rows[r]) rows[r] = [];
      let clash = false;
      for (const b of rows[r]) if (x < b.x1 + LABEL_GAP && x + wNeeded + LABEL_GAP > b.x0) { clash = true; break; }
      if (!clash) { rows[r].push({ x0: x, x1: x + wNeeded }); row = r; break; }
    }
    if (row < 0) { dropped++; continue; }
    usedRows = Math.max(usedRows, row + 1);

    const box = h('div', {
      class: 'ts-lab',
      style: 'left:' + x.toFixed(1) + 'px;width:' + Math.ceil(wNeeded) + 'px;top:' + (8 + row * rowH) + 'px',
    });
    box.append(h('div', { class: 'ts-year' },
      h('b', null, String(y)), ' ',
      h('span', { class: 'dim' }, mine.map((m) => m.step).join(' '))));
    for (const m of mine) {
      const n = byId.get(m.node);
      box.append(h('a', {
        class: 'ts-name', href: '#/n/' + m.node,
        style: 'border-left-color:' + (n ? clsColour(n.cls) : 'var(--line2)'),
      }, n ? (n.short || n.label) : m.node));
    }
    axis.append(box);
  }

  axis.style.minHeight = (12 + Math.max(1, usedRows) * rowH) + 'px';
  host.append(axis);

  const notes: string[] = [];
  if (dropped) notes.push(dropped + (dropped === 1 ? ' year' : ' years') + ' not labelled: no room at 11px');
  if (undated.length) {
    notes.push('no year on the board for ' + undated.map((u) => {
      const n = byId.get(u.node);
      return u.step + ' ' + (n ? n.label : u.node);
    }).join(', '));
  }
  if (notes.length) host.append(h('div', { class: 'ts-note dim' }, notes.join(' · ')));
}
