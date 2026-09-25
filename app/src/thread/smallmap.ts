/* thread/smallmap.ts: the small map on the Thread page (Design 1.6).
 *
 * The same 7 x 5 grid as the program map: the bands and eras of data/map.json,
 * each step drawn as its numbered chip in its own band x era cell, orthogonal
 * links between consecutive steps.
 *
 * A step whose node is below the L0 floor has no band, so it is placed by era
 * in a "below the floor" row under the seven bands rather than being dropped or
 * given a band it does not have.
 *
 * Chips are all one size. The number is the step's position in the chain and is
 * the only thing that varies; nothing here encodes importance.
 */
import { h, clear } from '../dom';
import { clsColour, type IndexNode } from '../data';
import type { GridFile, Thread } from './data';

export const BAND_COL = 92;
export const ROW_H = 28;
export const HEAD_H = 28;
export const CHIP_W = 21;
export const CHIP_H = 14;
export const CHIP_GAP = 3;
const FLOOR = '_floor';

export interface Slot { step: number; node: string; band: string; era: string; x: number; y: number }

export function renderSmallMap(
  host: HTMLElement, thread: Thread, grid: GridFile, byId: Map<string, IndexNode>, width: number,
): void {
  clear(host);
  const bands = grid.bands.map((b) => b.id);
  const rows = bands.concat([FLOOR]);
  const eras = grid.eras;
  const gridNode = new Map(grid.nodes.map((n) => [n.id, n]));

  const colW = Math.max(46, (width - BAND_COL) / eras.length);
  const boardW = BAND_COL + colW * eras.length;

  /* Which cell each step belongs in, and how the chips stack inside it. */
  const perCell = new Map<string, number>();
  const slots: Slot[] = [];
  let onMap = 0;
  thread.steps.forEach((s, i) => {
    const g = gridNode.get(s.node);
    const meta = byId.get(s.node);
    const band = g ? g.band : FLOOR;
    const era = (g ? g.era : meta ? meta.era : eras[eras.length - 1].id);
    if (g) onMap++;
    const key = band + '.' + era;
    const k = perCell.get(key) || 0;
    perCell.set(key, k + 1);
    const ri = Math.max(0, rows.indexOf(band));
    const ci = Math.max(0, eras.findIndex((e) => e.id === era));
    const perRow = Math.max(1, Math.floor((colW - 8) / (CHIP_W + CHIP_GAP)));
    const sub = Math.floor(k / perRow);
    const col = k % perRow;
    slots.push({
      step: i + 1,
      node: s.node,
      band,
      era,
      x: BAND_COL + ci * colW + 4 + col * (CHIP_W + CHIP_GAP),
      y: HEAD_H + ri * ROW_H + 5 + sub * (CHIP_H + 2),
    });
  });

  const boardH = HEAD_H + rows.length * ROW_H + 8;
  const board = h('div', {
    class: 'tm-board',
    style: 'width:' + Math.round(boardW) + 'px;height:' + boardH + 'px',
  });

  /* era heads and band rows: the frame the chips sit in */
  eras.forEach((e, ci) => {
    board.append(h('div', {
      class: 'tm-erahead',
      style: 'left:' + (BAND_COL + ci * colW) + 'px;width:' + colW + 'px;top:0px;height:' + HEAD_H + 'px',
    }, e.label));
    board.append(h('i', {
      class: 'tm-vline', 'aria-hidden': 'true',
      style: 'left:' + (BAND_COL + ci * colW) + 'px;top:' + HEAD_H + 'px;height:' + (rows.length * ROW_H) + 'px',
    }));
  });
  rows.forEach((b, ri) => {
    const label = b === FLOOR
      ? 'not on the map'
      : (grid.bands.filter((x) => x.id === b)[0] || { label: b }).label;
    board.append(h('div', {
      class: 'tm-bandhead' + (b === FLOOR ? ' floor' : ''),
      style: 'top:' + (HEAD_H + ri * ROW_H) + 'px;height:' + ROW_H + 'px;width:' + (BAND_COL - 6) + 'px',
    }, label));
    board.append(h('i', {
      class: 'tm-hline' + (b === FLOOR ? ' floor' : ''), 'aria-hidden': 'true',
      style: 'top:' + (HEAD_H + ri * ROW_H) + 'px;width:' + Math.round(boardW) + 'px',
    }));
  });

  /* orthogonal links between consecutive steps: out horizontally, one vertical,
     in horizontally. Drawn under the chips. */
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'tm-links');
  svg.setAttribute('width', String(Math.round(boardW)));
  svg.setAttribute('height', String(boardH));
  svg.setAttribute('aria-hidden', 'true');
  for (let i = 1; i < slots.length; i++) {
    const a = slots[i - 1];
    const b = slots[i];
    const ay = a.y + CHIP_H / 2;
    const by = b.y + CHIP_H / 2;
    const ax = a.x < b.x ? a.x + CHIP_W : a.x;
    const bx = a.x < b.x ? b.x : b.x + CHIP_W;
    const mid = (ax + bx) / 2;
    const pts = ay === by
      ? [ax + ',' + ay, bx + ',' + by]
      : [ax + ',' + ay, mid + ',' + ay, mid + ',' + by, bx + ',' + by];
    const pl = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    pl.setAttribute('points', pts.join(' '));
    pl.setAttribute('class', 'tm-link');
    svg.append(pl);
  }
  board.append(svg);

  /* the chips */
  for (const s of slots) {
    const meta = byId.get(s.node);
    const a = h('a', {
      class: 'tm-chip' + (meta && meta.hl ? ' hl' : ''),
      href: '#/t/' + thread.id + '/map',
      style: 'left:' + s.x.toFixed(1) + 'px;top:' + s.y + 'px;width:' + CHIP_W + 'px;height:' + CHIP_H +
        'px;border-left-color:' + (meta ? clsColour(meta.cls) : 'var(--line2)'),
      title: 'step ' + s.step + ' · ' + (meta ? meta.label : s.node) + ' · show the thread on the map',
      'data-step': String(s.step),
      'data-node': s.node,
      'data-cell': s.band + '.' + s.era,
    }, String(s.step));
    board.append(a);
  }

  host.append(h('div', { class: 'tm-cap dim' },
    'Small map · ' + onMap + ' of ' + thread.steps.length + ' steps on the program grid · ' +
    (thread.steps.length - onMap) + ' not on the program map · numbered as at left'));
  host.append(board);
}
