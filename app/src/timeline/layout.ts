/* timeline/layout.ts: the packing rule of Design response section 1.7 and 2.2.
 *
 * Section lanes by era columns (redesign phase 9: the lanes were the four
 * strands). The open era gets year gridlines and its events as 11px chips
 * packed into rows so that no two overlap. An event whose chip cannot be placed
 * at 11px is counted in its year ("+N", which opens the named list); there are
 * no unnamed marks.
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
  grade: string | null;
  claimTier: number | null;
  node: string | null;
  era: string;
  /* phase 9, from build_app_data.py */
  section: string;
  topic: string | null;
  sources?: { text: string; url: string | null }[];
  sameAs?: string;
}

export interface EraDef {
  id: string;
  label: string;
  sub: string;
  start: number | null;
  end: number | null;
}

/* Redesign phase 9: the lanes are the ten topic sections, in the order
   topics.json gives them, and one lane for the events whose node is in no topic
   (or that name no node). The four strands are a filter now, not lanes. */
export const OTHER_LANE = 'other';
export interface Lane { id: string; label: string }

export function lanes(sections: { id: string; title: string }[]): Lane[] {
  const out: Lane[] = sections.map((s) => ({ id: s.id, label: s.title }));
  out.push({ id: OTHER_LANE, label: 'In no topic' });
  return out;
}

export const STRANDS: Lane[] = [
  { id: 'program', label: 'PROGRAM' },
  { id: 'witness', label: 'WITNESS' },
  { id: 'oversight', label: 'OVERSIGHT' },
  { id: 'coverup', label: 'COVER-UP' },
];

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
/* how far past its date a right-anchored chip may end: its own rule's width */
export const MARK_ROOM = 3;

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
  kind: 'chip' | 'more';
  ev: TEvent | null;          /* the event, for a chip                          */
  evs: TEvent[];              /* the events a count stands for, for a `more`    */
  year: number;
  x: number;
  y: number;
  w: number;
  h: number;
  row: number;
  right?: boolean;            /* a chip that ends at its date rather than starting there */
}

export interface LaneLayout {
  lane: string;
  items: Item[];
  chips: number;
  counted: number;            /* events behind the counts                       */
  height: number;
}

export interface PackOpts {
  width: number;
  slots: YearSlot[];
  chipRowBudget: number;
}

/* The width of a count: its digits and a sign, and no more. */
export function moreWidth(n: number, year?: number, room?: number): number {
  const short = Math.ceil(textWidth('+' + n)) + 8;
  if (year == null || room == null) return short;
  /* "2024 +16" where the year has room for it, else "+16" */
  const long = Math.ceil(textWidth(year + ' +' + n)) + 8;
  return long <= room ? long : short;
}

/* Greedy first-fit by date. A chip is placed only where its whole label fits at
   11px inside the column and clear of every chip already in that row. Every
   event that cannot be is COUNTED, never drawn as an unnamed mark (blind critic,
   phase 6): one count per year of the lane, "+N", packed first-fit in its own
   rows below the chips, which opens the named list of those N events. So every
   event of the open era is either named on the page or counted and named on
   click, and no two rendered things overlap. */
export function packLane(lane: Lane, events: TEvent[], o: PackOpts): LaneLayout {
  /* Events in an opened year claim the rows first; without that the row budget
     is spent on the earlier years before the opened one is reached, and opening
     a year would widen it without placing anything in it. */
  const openYear = new Set<number>();
  for (const s of o.slots) if (s.open) openYear.add(s.year);
  const yearOf = (e: TEvent): number => Number(e.date.slice(0, 4));
  const rank = (e: TEvent): number => (openYear.has(yearOf(e)) ? 0 : 1);
  const evs = events.slice().sort((a, b) => {
    const r = rank(a) - rank(b);
    if (r) return r;
    return a.date < b.date ? -1 : a.date > b.date ? 1 : a.id < b.id ? -1 : 1;
  });
  const rows: { x0: number; x1: number }[][] = [];
  const items: Item[] = [];
  const left = new Map<number, TEvent[]>();
  let chips = 0;

  for (const ev of evs) {
    const text = ev.label || '';
    const at = eventX(ev, o.slots);
    const w = Math.ceil(textWidth(text)) + CHIP_PAD;
    /* A chip starts at its date. Where the column ends before its label does,
       it ENDS at its date instead (right-anchored, its class rule on the right),
       so the last years of an era are named rather than counted (blind critic,
       phase 9 round 1: four 2026 events of a lane were a bare "+4"). */
    const tries: { x: number; right: boolean }[] = [];
    if (at + w <= o.width) tries.push({ x: at, right: false });
    else {
      const end = Math.min(o.width, at + MARK_ROOM);
      if (end - w >= 0) tries.push({ x: end - w, right: true });
    }
    let placed = false;
    for (const t of text ? tries : []) {
      const x = t.x;
      for (let r = 0; r < o.chipRowBudget && !placed; r++) {
        if (!rows[r]) rows[r] = [];
        let clash = false;
        for (const b of rows[r]) if (x < b.x1 + CHIP_GAP && x + w + CHIP_GAP > b.x0) { clash = true; break; }
        if (clash) continue;
        rows[r].push({ x0: x, x1: x + w });
        items.push({ kind: 'chip', ev, evs: [ev], year: yearOf(ev), x, y: r * ROW_PITCH, w, h: CHIP_H, row: r, right: t.right });
        chips++;
        placed = true;
      }
      if (placed) break;
    }
    if (!placed) {
      const y = yearOf(ev);
      const l = left.get(y);
      if (l) l.push(ev); else left.set(y, [ev]);
    }
  }

  /* the counts: one per year, at the head of its year, first-fit in rows */
  let counted = 0;
  const mrows: { x0: number; x1: number }[][] = [];
  const years = Array.from(left.keys()).sort((a, b) => a - b);
  for (const y of years) {
    const list = (left.get(y) || []).slice().sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.id < b.id ? -1 : 1));
    counted += list.length;
    let x = 0, room = 0;
    for (const s of o.slots) if (s.year === y) { x = s.x; room = s.w - 2; break; }
    const w = moreWidth(list.length, y, room);
    x = Math.max(0, Math.min(x, o.width - w));
    let r = 0;
    for (; r < 200; r++) {
      if (!mrows[r]) mrows[r] = [];
      let clash = false;
      for (const b of mrows[r]) if (x < b.x1 + 2 && x + w + 2 > b.x0) { clash = true; break; }
      if (!clash) { mrows[r].push({ x0: x, x1: x + w }); break; }
    }
    items.push({ kind: 'more', ev: null, evs: list, year: y, x, y: 0, w, h: CHIP_H, row: r });
  }

  let chipRows = 0;
  for (const r of rows) if (r && r.length) chipRows++;
  let moreRows = 0;
  for (const r of mrows) if (r && r.length) moreRows++;
  const chipBlock = chipRows * ROW_PITCH;
  for (const it of items) if (it.kind === 'more') it.y = chipBlock + it.row * ROW_PITCH;

  return {
    lane: lane.id,
    items,
    chips,
    counted,
    height: chipBlock + moreRows * ROW_PITCH,
  };
}
