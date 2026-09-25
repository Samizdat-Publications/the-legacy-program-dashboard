/* hood/layout.ts: where the marks go, and which labels are drawn at all.
 *
 * The rule, from Design response 2.2, is the whole of this file: ONE font size,
 * 11px. A label is drawn only if the whole label fits in the room its side has
 * at that size. Nothing is truncated, abbreviated or shrunk. A mark whose label
 * does not fit is not drawn: it is counted, and the count is drawn instead.
 *
 * Ring positions are assigned by y, not by angle. The unit is Design's 15px
 * label slot, used as a MINIMUM: the ring's names are spread evenly over the
 * ring's height at whatever pitch that gives, never closer than one slot, and
 * the outer columns take 15px slots that the ring has not already claimed. Two
 * names on the same side are therefore always at least 15px apart in y, so a
 * collision is impossible by construction rather than by inspection.
 *
 * Order is start date, then label. Never degree, tier or connections.
 */
import type { Entry } from './model';

export const SLOT_H = 15;          /* Design 1.5: label slots of 15px per side */
const MARK_W = 7;                  /* dom.ts .mark, one size for every mark    */
const MARK_GAP = 6;
const RESERVE = MARK_W + MARK_GAP;
/* the ring's names occupy the middle 92% of its diameter, so that no name lands
   where the circle has run out of horizontal room for a label */
const RING_USE = 0.92;

export interface Geom {
  w: number; h: number;
  cx: number; cy: number;
  R: number;
  outerInset: number;
  room1: number;
  room2: number;
  /* the slot lattice, measured in whole slots from the centre: slot 0 is the
     centre line, slot k is cy + k*15. It is the same arithmetic the checks do
     on ring(), so "no two names on a side share a slot" means the same thing
     inside this file and outside it. */
  slotMin: number;
  slotMax: number;
  ringTop: number;
  ringBottom: number;
}

export interface Placed {
  e: Entry;
  x: number;                       /* the mark's centre, stage coordinates */
  y: number;
  side: -1 | 1;                    /* -1 left, +1 right                    */
}

export interface Layout {
  geom: Geom;
  placed: Placed[];
  unnamed: Entry[];                /* everything counted into the +N chip  */
  named: { one: number; two: number; three: number };
  total: { one: number; two: number; three: number };
}

/* Measured, never assumed: the same 11px face the labels render in. */
let mctx: CanvasRenderingContext2D | null = null;
export function measure(text: string): number {
  if (!mctx) {
    const c = document.createElement('canvas');
    mctx = c.getContext('2d');
    if (mctx) {
      const cs = getComputedStyle(document.body);
      mctx.font = '400 ' + (cs.getPropertyValue('--fs-label').trim() || '11px') +
        ' ' + (cs.fontFamily || 'monospace');
    }
  }
  return mctx ? mctx.measureText(text).width : text.length * 6.6;
}

export function printed(e: Entry): string {
  return e.suffix ? e.label + ' ' + e.suffix : e.label;
}
function need(e: Entry): number {
  return measure(printed(e)) + RESERVE;
}

export function geometry(w: number, h: number, hops: 1 | 2 | 3): Geom {
  /* Design 1.5: ring radius 230 at 1366, 300 at 1920, 420 at 2560. */
  const R = w < 1600 ? 230 : w < 2200 ? 300 : 420;
  const outerInset = Math.round(w * 0.11);
  const cx = Math.round(w / 2);
  const cy = Math.round(h / 2);
  /* Design 2.2: hop-1 labels have (distance from centre to the outer column)
     − radius − 26 when hop 2 is on, and (half-width − radius − 24) when off. */
  const room1 = hops >= 2 ? (cx - outerInset) - R - 26 : cx - R - 24;
  const room2 = outerInset - 16;   /* hop-2 labels: the room to the viewport edge */

  const use = R * RING_USE;
  return {
    w, h, cx, cy, R, outerInset, room1, room2,
    slotMin: Math.ceil((10 - cy) / SLOT_H),
    slotMax: Math.floor((h - 10 - cy) / SLOT_H),
    ringTop: Math.max(SLOT_H, cy - use),
    ringBottom: Math.min(h - SLOT_H, cy + use),
  };
}

/* The slot a y falls in, and the y of a slot. */
export function slotOf(y: number, cy: number): number {
  return Math.round((y - cy) / SLOT_H);
}
export function ySlot(k: number, cy: number): number {
  return cy + k * SLOT_H;
}

/* n names spread evenly down [top..bottom], never closer than one slot. */
function ringYs(n: number, top: number, bottom: number, cy: number): number[] {
  if (n <= 0) return [];
  if (n === 1) return [cy];
  const pitch = Math.max(SLOT_H, (bottom - top) / (n - 1));
  const start = cy - (pitch * (n - 1)) / 2;
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(start + i * pitch);
  return out;
}

/* Pick `n` of the free slots, spread evenly across them. */
function pickFree(n: number, free: number[]): number[] {
  if (n <= 0 || free.length === 0) return [];
  if (n === 1) return [free[Math.floor(free.length / 2)]];
  const step = (free.length - 1) / (n - 1);
  const out: number[] = [];
  for (let i = 0; i < n; i++) out.push(free[Math.round(i * step)]);
  return out;
}

export function layout(
  hop1: Entry[], outer: Entry[], w: number, h: number, hops: 1 | 2 | 3,
): Layout {
  const g = geometry(w, h, hops);
  const placed: Placed[] = [];
  const unnamed: Entry[] = [];
  const taken: Record<string, Set<number>> = { '-1': new Set(), '1': new Set() };

  const ringCap = Math.floor((g.ringBottom - g.ringTop) / SLOT_H) + 1;

  /* ---- hop 1 on the ring ------------------------------------------------ */
  const fits1: Entry[] = [];
  for (const e of hop1) (need(e) <= g.room1 ? fits1 : unnamed).push(e);
  const keep1 = fits1.slice(0, ringCap * 2);
  for (const e of fits1.slice(ringCap * 2)) unnamed.push(e);

  const leftN = Math.min(ringCap, Math.ceil(keep1.length / 2));
  const sides1: [Entry[], -1 | 1][] = [[keep1.slice(0, leftN), -1], [keep1.slice(leftN), 1]];
  for (const [list, side] of sides1) {
    const ys = ringYs(list.length, g.ringTop, g.ringBottom, g.cy);
    list.forEach((e, i) => {
      const y = ys[i];
      const dy = y - g.cy;
      const dx = Math.sqrt(Math.max(0, g.R * g.R - dy * dy));
      taken[String(side)].add(slotOf(y, g.cy));
      placed.push({ e, x: g.cx + side * dx, y, side });
    });
  }

  /* ---- hops 2 and 3 in the two outer columns ---------------------------- */
  const fits2: Entry[] = [];
  for (const e of outer) (need(e) <= g.room2 ? fits2 : unnamed).push(e);

  const freeOf = (side: -1 | 1): number[] => {
    const out: number[] = [];
    for (let k = g.slotMin; k <= g.slotMax; k++) if (!taken[String(side)].has(k)) out.push(k);
    return out;
  };
  const freeL = freeOf(-1);
  const freeR = freeOf(1);
  const cap2 = freeL.length + freeR.length;
  const keep2 = fits2.slice(0, cap2);
  for (const e of fits2.slice(cap2)) unnamed.push(e);

  const leftN2 = Math.min(freeL.length, Math.ceil(keep2.length / 2));
  const sides2: [Entry[], -1 | 1, number[]][] = [
    [keep2.slice(0, leftN2), -1, freeL],
    [keep2.slice(leftN2), 1, freeR],
  ];
  for (const [list, side, free] of sides2) {
    const ks = pickFree(list.length, free);
    list.forEach((e, i) => {
      if (ks[i] === undefined) { unnamed.push(e); return; }
      placed.push({
        e, side,
        x: side < 0 ? g.outerInset : g.w - g.outerInset,
        y: ySlot(ks[i], g.cy),
      });
    });
  }

  const count = (list: Entry[], hop: number) => list.filter((e) => e.hop === hop).length;
  const drawn = placed.map((p) => p.e);
  return {
    geom: g, placed, unnamed,
    named: { one: count(drawn, 1), two: count(drawn, 2), three: count(drawn, 3) },
    total: { one: count(hop1, 1), two: count(outer, 2), three: count(outer, 3) },
  };
}
