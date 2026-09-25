/* timeline/layout.ts: the packing rule of Design response section 1.7 and 2.2.
 *
 * Four strand lanes by five era columns. The open era gets year gridlines and
 * its events as 11px chips packed into rows so that no two overlap. An event
 * whose chip cannot be placed at 11px is a 5px mark until its year is opened.
 *
 * One label size. Nothing is truncated, nothing is shrunk, nothing is sized by
 * importance: a chip's width is its own text and no more.
 *
 * This module computes positions only. The page renders them, and
 * window.__app.timeline.placed() reads the positions back out of the DOM, so a
 * check never has to trust what this file intended.
 */

export interface TEvent {
  id: string;
  strand: string;
  date: string;
  precision: string;
  label: string | null;
  text: string | null;
  tier: string | null;
  node: string | null;
  era: string;
}

export interface EraDef {
  id: string;
  label: string;
  sub: string;
  start: number | null;
  end: number | null;
}

/* The lane order of the Design captures. Strands the board carries and this
   list does not are appended rather than dropped, because a strand that stops
   being drawn is a strand that stops being counted. */
const LANE_ORDER = ['program', 'witness', 'oversight', 'coverup'];
const LANE_LABEL: Record<string, string> = {
  program: 'PROGRAM',
  witness: 'WITNESS',
  oversight: 'OVERSIGHT',
  coverup: 'COVER-UP',
};

export interface Lane { id: string; label: string }

export function lanes(events: TEvent[]): Lane[] {
  const seen = new Set<string>();
  for (const e of events) seen.add(e.strand);
  const out: Lane[] = [];
  for (const id of LANE_ORDER) if (seen.has(id)) out.push({ id, label: LANE_LABEL[id] || id.toUpperCase() });
  for (const id of Array.from(seen).sort()) {
    if (LANE_ORDER.indexOf(id) < 0) out.push({ id, label: id.toUpperCase() });
  }
  return out;
}

/* ---- measurement ------------------------------------------------------- */

export const LABEL_FONT =
  '400 11px "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace';

let mctx: CanvasRenderingContext2D | null = null;
export function textWidth(s: string): number {
  if (!mctx) {
    const c = document.createElement('canvas');
    mctx = c.getContext('2d');
  }
  if (!mctx) return s.length * 6.7;
  mctx.font = LABEL_FONT;
  return mctx.measureText(s).width;
}

/* ---- geometry ---------------------------------------------------------- */

export const CHIP_H = 15;
/* 3px class rule + 5px left + 6px right. The chip is its text and this much;
   it is never wider or narrower for any other reason. */
export const CHIP_PAD = 14;
export const ROW_PITCH = 18;
export const CHIP_GAP = 6;
export const MARK_W = 5;
export const MARK_H = 5;
export const MARK_PITCH = 7;
export const MARK_GAP = 3;

export interface YearSlot { year: number; x: number; w: number; open: boolean }

export function eraYears(era: EraDef, events: TEvent[]): number[] {
  const ys: number[] = [];
  for (const e of events) {
    const n = Number(e.date.slice(0, 4));
    if (Number.isFinite(n)) ys.push(n);
  }
  if (!ys.length) return [];
  let lo = ys[0];
  let hi = ys[0];
  for (const y of ys) { if (y < lo) lo = y; if (y > hi) hi = y; }
  if (era.start != null && era.start < lo) lo = era.start;
  if (era.end != null && era.end < hi) hi = era.end;
  const out: number[] = [];
  for (let y = lo; y <= Math.max(lo, hi); y++) out.push(y);
  return out;
}

/* An opened year is given openWeight times the room of a closed one, which is
   what makes its events placeable at 11px. Nothing else about them changes. */
export function yearSlots(years: number[], open: Set<number>, width: number, openWeight: number): YearSlot[] {
  if (!years.length) return [];
  const w = years.map((y) => (open.has(y) ? openWeight : 1));
  const total = w.reduce((a, b) => a + b, 0);
  const slots: YearSlot[] = [];
  let x = 0;
  for (let i = 0; i < years.length; i++) {
    const ww = (w[i] / total) * width;
    slots.push({ year: years[i], x, w: ww, open: open.has(years[i]) });
    x += ww;
  }
  return slots;
}

/* Where in its year a date falls. Precision is respected: a year-precision date
   sits at the head of its year rather than pretending to a month. */
export function dateFraction(ev: TEvent): number {
  const m = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?/.exec(ev.date);
  if (!m) return 0.02;
  if (ev.precision === 'year' || !m[2]) return 0.02;
  const mo = Number(m[2]) - 1;
  const da = m[3] ? Number(m[3]) - 1 : 0;
  return Math.max(0, Math.min(0.98, (mo + da / 31) / 12));
}

export function eventX(ev: TEvent, slots: YearSlot[]): number {
  const y = Number(ev.date.slice(0, 4));
  let s: YearSlot | undefined;
  for (const z of slots) if (z.year === y) { s = z; break; }
  if (!s) s = slots[slots.length - 1];
  if (!s) return 0;
  return s.x + dateFraction(ev) * s.w;
}

/* ---- packing ------------------------------------------------------------ */

export interface Item {
  ev: TEvent;
  kind: 'chip' | 'mark';
  x: number;
  y: number;
  w: number;
  h: number;
  row: number;
}

export interface LaneLayout {
  strand: string;
  label: string;
  items: Item[];
  chips: number;
  marks: number;
  chipRows: number;
  markRows: number;
  height: number;
}

export interface PackOpts {
  width: number;
  slots: YearSlot[];
  chipRowBudget: number;
}

/* Greedy first-fit by date. A chip is placed only where its whole label fits at
   11px inside the column and clear of every chip already in that row; anything
   else falls to a 5px mark, which is Design's own answer and not a truncation.
   Marks are packed too, in their own rows below the chips, so that no two
   rendered things overlap. */
export function packLane(lane: Lane, events: TEvent[], o: PackOpts): LaneLayout {
  /* Events in an opened year claim the rows first. Without that the row budget
     is spent on the earlier years before the opened one is reached, and opening
     a year would widen it without placing anything in it, and the control would
     look like it worked and would not have. Order is otherwise by date. */
  const openYear = new Set<number>();
  for (const s of o.slots) if (s.open) openYear.add(s.year);
  const rank = (e: TEvent): number => (openYear.has(Number(e.date.slice(0, 4))) ? 0 : 1);
  const evs = events.slice().sort((a, b) => {
    const r = rank(a) - rank(b);
    if (r) return r;
    return a.date < b.date ? -1 : a.date > b.date ? 1 : a.id < b.id ? -1 : 1;
  });
  const rows: { x0: number; x1: number }[][] = [];
  const markRows: number[][] = [];
  const items: Item[] = [];
  let chips = 0;
  let marks = 0;

  /* A mark keeps its year. Within its own year it takes the first free
     position, wrapping to the head of the year and then to the next mark row,
     so a day that carries thirty events does not build a thirty-row tower and
     no mark ever leaves the year it happened in. */
  const step = MARK_W + MARK_GAP;
  const asMark = (ev: TEvent, x: number): void => {
    const yr = Number(ev.date.slice(0, 4));
    let lo = 0;
    let hi = Math.max(0, o.width - MARK_W);
    for (const s of o.slots) {
      if (s.year !== yr) continue;
      lo = s.x;
      hi = Math.max(s.x, Math.min(hi, s.x + s.w - MARK_W));
      break;
    }
    const start = Math.max(lo, Math.min(hi, x));
    const tries: number[] = [];
    for (let p = start; p <= hi; p += step) tries.push(p);
    for (let p = lo; p < start; p += step) tries.push(p);
    if (!tries.length) tries.push(start);

    let r = 0;
    let mx = start;
    for (; r < 2000; r++) {
      if (!markRows[r]) markRows[r] = [];
      let found = false;
      for (const p of tries) {
        let clash = false;
        for (const px of markRows[r]) if (Math.abs(px - p) < step) { clash = true; break; }
        if (!clash) { mx = p; found = true; break; }
      }
      if (found) { markRows[r].push(mx); break; }
    }
    items.push({ ev, kind: 'mark', x: mx, y: 0, w: MARK_W, h: MARK_H, row: r });
    marks++;
  };

  for (const ev of evs) {
    const text = ev.label || '';
    const x = eventX(ev, o.slots);
    if (!text) { asMark(ev, x); continue; }
    const w = Math.ceil(textWidth(text)) + CHIP_PAD;
    if (x + w > o.width) { asMark(ev, x); continue; }

    let placed = false;
    for (let r = 0; r < o.chipRowBudget; r++) {
      if (!rows[r]) rows[r] = [];
      let clash = false;
      for (const b of rows[r]) if (x < b.x1 + CHIP_GAP && x + w + CHIP_GAP > b.x0) { clash = true; break; }
      if (clash) continue;
      rows[r].push({ x0: x, x1: x + w });
      items.push({ ev, kind: 'chip', x, y: r * ROW_PITCH, w, h: CHIP_H, row: r });
      chips++;
      placed = true;
      break;
    }
    if (!placed) asMark(ev, x);
  }

  let chipRows = 0;
  for (const r of rows) if (r && r.length) chipRows++;
  let usedMarkRows = 0;
  for (const r of markRows) if (r && r.length) usedMarkRows++;
  const chipBlock = chipRows * ROW_PITCH;
  for (const it of items) if (it.kind === 'mark') it.y = chipBlock + 4 + it.row * MARK_PITCH;

  return {
    strand: lane.id,
    label: lane.label,
    items,
    chips,
    marks,
    chipRows,
    markRows: usedMarkRows,
    height: chipBlock + (usedMarkRows ? 4 + usedMarkRows * MARK_PITCH : 0),
  };
}
