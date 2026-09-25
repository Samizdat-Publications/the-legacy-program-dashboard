/* thread/slice.ts: the timeline slice on the Thread page: the steps' own years.
 *
 * One tick per year the chain touches, and one row per year under the axis,
 * in year order. Every year is named at the one label size; nothing is shrunk,
 * truncated or dropped. Steps the board dates with nothing are named under the axis rather
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

  /* One row per year, top to bottom in year order, so the slice reads in the
     order the years run (the old packing put each label in the first free row,
     which read 2007, 2009, 2008). Each label starts at its year's own place on
     the axis, pulled left only as far as it must be to fit inside the slice.
     Nothing is shrunk, truncated or dropped: every year is named. */
  let top = 8;
  for (const y of years) {
    const mine = dated.filter((d) => d.year === y);
    const head = String(y) + '  ' + mine.map((m) => m.step).join(' ');
    const names = mine.map((m) => { const n = byId.get(m.node); return n ? (n.short || n.label) : m.node; });
    let wNeeded = textWidth(head);
    for (const s of names) wNeeded = Math.max(wNeeded, textWidth(s));
    wNeeded = Math.min(wNeeded + 12, inner + PAD_R);
    const at = ((y - lo) / span) * inner;
    const x = Math.max(0, Math.min(at, inner + PAD_R - wNeeded));

    const box = h('div', {
      class: 'ts-lab',
      'data-year': String(y),
      style: 'left:' + x.toFixed(1) + 'px;width:' + Math.ceil(wNeeded) + 'px;top:' + top + 'px',
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
    top += 18 + mine.length * 15 + LABEL_GAP;
  }

  axis.style.minHeight = (top + 4) + 'px';
  host.append(axis);

  const notes: string[] = [];
  if (undated.length) {
    notes.push('no year on the board for ' + undated.map((u) => {
      const n = byId.get(u.node);
      return u.step + ' ' + (n ? n.label : u.node);
    }).join(', '));
  }
  if (notes.length) host.append(h('div', { class: 'ts-note dim' }, notes.join(' · ')));
}
