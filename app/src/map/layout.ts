/* map/layout.ts — the label rule of Design response 2.2, laid out at 1:1 for the
 * viewport (Design 4.3), never scaled.
 *
 * Label mode: chip width = measured text width + 30 (+16 for a start-here
 * number). Chips pack left to right by start date within their band x era cell,
 * wrapping inside the cell's column. Row pitch starts at 20 (26 at 2560) and
 * steps down to 18, then the band gap steps down to 6, before the map gives up
 * on label mode. A chip whose label does not fit its column at 11px is not
 * drawn -- and because label mode may not draw an anonymous mark, a width that
 * does not fit is a reason to give up on label mode, not to shrink the label.
 *
 * Cell mode: band heights proportional to the band's largest cell; each cell
 * prints its count, then the names that fit in start-date order, reserving room
 * on the last row for a `+N` chip. Nothing is truncated in either mode.
 */
import type { MapData, MapNode } from './model';
import { byStartDate, cellKey } from './model';

export const BAR_H = 40;      /* the common frame, fixed at the top          */
export const STRIP_H = 30;    /* the map's own control strip                 */
export const HEAD_H = 42;     /* the five era column heads                   */
export const LEGEND_H = 26;   /* the legend, at the bottom edge              */
export const GUTTER = 152;    /* the band-label column on the left           */
export const PAD_R = 12;
export const CHIP_H = 16;
export const CHIP_GAP = 6;
export const CELL_PAD = 6;
export const CHIP_EXTRA = 30; /* border, class mark and padding              */
export const HL_EXTRA = 16;   /* the start-here number at the chip's right   */
export const CELL_ROW = 22;   /* row pitch inside a cell in cell mode        */
export const CELL_HEAD = 17;  /* the "N nodes / click to expand" line        */
export const PLUS_W = 40;     /* room reserved for the `+N` chip             */
export const CELL_GAP = 8;    /* between bands in cell mode                  */

export interface Box { x: number; y: number; w: number; h: number; }

export interface ChipPlace extends Box { id: string; }

export interface CellPlace extends Box {
  key: string;
  band: string;
  era: string;
  count: number;
  shown: number;
  plus: number;
  names: ChipPlace[];
  plusBox: Box | null;
}

export interface BandPlace { id: string; label: string; top: number; height: number; rows: number; }

export interface MapLayout {
  mode: 'label' | 'cell';
  reason: string;
  pitch: number;
  gap: number;
  colW: number;
  gridTop: number;
  gridLeft: number;
  width: number;
  height: number;
  bands: BandPlace[];
  cells: CellPlace[];
  chips: ChipPlace[];              /* drawn chips only, in draw order        */
  chipById: Map<string, ChipPlace>;
  undrawn: string[];               /* counted, never truncated               */
  colX: number[];                  /* 6 boundaries: 5 columns                */
}

export type Measure = (text: string) => number;

export function chipWidth(n: MapNode, measure: Measure): number {
  return Math.ceil(measure(n.short)) + CHIP_EXTRA + (n.hl ? HL_EXTRA : 0);
}

function ordered(data: MapData, key: string): MapNode[] {
  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  const ids = data.cells[key] || [];
  const out: MapNode[] = [];
  for (const id of ids) { const n = byId.get(id); if (n) out.push(n); }
  return out.sort(byStartDate);
}

/* Pack one cell's chips left to right, wrapping. Returns the rows, each a list
   of [node, width]; a chip wider than the cell is reported separately. */
function pack(nodes: MapNode[], inner: number, measure: Measure) {
  const rows: { n: MapNode; w: number }[][] = [];
  const tooWide: MapNode[] = [];
  let row: { n: MapNode; w: number }[] = [];
  let used = 0;
  for (const n of nodes) {
    const w = chipWidth(n, measure);
    if (w > inner) { tooWide.push(n); continue; }
    if (row.length && used + CHIP_GAP + w > inner) { rows.push(row); row = []; used = 0; }
    used += (row.length ? CHIP_GAP : 0) + w;
    row.push({ n, w });
  }
  if (row.length) rows.push(row);
  return { rows, tooWide };
}

/* Cell mode's packing: the names that fit, in start-date order, with the last
   usable row keeping PLUS_W free for the `+N` chip. Everything not placed is
   returned so the count can be exact -- C6 requires N = members - names drawn. */
function packCell(nodes: MapNode[], inner: number, rowsAvail: number, measure: Measure) {
  const rows: { n: MapNode; w: number }[][] = [];
  const skipped: MapNode[] = [];
  let cur: { n: MapNode; w: number }[] = [];
  let used = 0;
  const limFor = (r: number) => inner - (r === rowsAvail - 1 ? PLUS_W + CHIP_GAP : 0);
  for (const n of nodes) {
    if (rows.length >= rowsAvail) { skipped.push(n); continue; }
    const w = chipWidth(n, measure);
    let lim = limFor(rows.length);
    if (used > 0 && used + CHIP_GAP + w > lim) {
      rows.push(cur); cur = []; used = 0;
      if (rows.length >= rowsAvail) { skipped.push(n); continue; }
      lim = limFor(rows.length);
    }
    if (w > lim) { skipped.push(n); continue; }
    used += (cur.length ? CHIP_GAP : 0) + w;
    cur.push({ n, w });
  }
  if (cur.length) rows.push(cur);
  return { rows, skipped };
}

export interface Viewport { w: number; h: number; }

/* ---------------------------------------------------------------------------
   The layout. `forceCells` is the CELLS control; otherwise label mode is tried
   first and cell mode is the answer only when label mode does not fit.
--------------------------------------------------------------------------- */
export function layout(
  data: MapData, vp: Viewport, measure: Measure, forceCells: boolean,
): MapLayout {
  const colW = Math.floor((vp.w - GUTTER - PAD_R) / 5);
  const colX: number[] = [];
  for (let i = 0; i <= 5; i++) colX.push(GUTTER + i * colW);
  const inner = colW - CELL_PAD * 2;
  const gridTop = STRIP_H + HEAD_H;
  const availH = vp.h - BAR_H - gridTop - LEGEND_H - 4;

  /* Pack every cell once: the packing depends on the column width, which is a
     function of the viewport width only, never of the pitch. */
  const packed = new Map<string, ReturnType<typeof pack>>();
  const counts = new Map<string, number>();
  let anyTooWide = 0;
  for (const b of data.bands) {
    for (const e of data.eras) {
      const key = cellKey(b.id, e.id);
      const nodes = ordered(data, key);
      counts.set(key, nodes.length);
      const p = pack(nodes, inner, measure);
      packed.set(key, p);
      anyTooWide += p.tooWide.length;
    }
  }

  const bandRows = data.bands.map((b) => {
    let mx = 0;
    for (const e of data.eras) {
      const p = packed.get(cellKey(b.id, e.id));
      if (p) mx = Math.max(mx, p.rows.length);
    }
    return Math.max(mx, 1);
  });
  const totalRows = bandRows.reduce((a, x) => a + x, 0);

  if (!forceCells && anyTooWide === 0) {
    const startPitch = vp.w >= 2400 ? 26 : 20;
    const startGap = vp.w >= 2400 ? 20 : 12;
    const tries: [number, number][] = [];
    for (let p = startPitch; p >= 18; p--) tries.push([p, startGap]);
    for (let g = startGap - 1; g >= 6; g--) tries.push([18, g]);
    for (const [pitch, gap] of tries) {
      const need = totalRows * pitch + gap * (data.bands.length - 1);
      if (need <= availH) {
        return labelLayout(data, packed, counts, bandRows, pitch, gap,
          colW, colX, gridTop, vp, availH);
      }
    }
  }

  return cellLayout(data, counts, measure, colW, colX, inner, gridTop, vp, availH,
    forceCells ? 'CELLS is on' : anyTooWide
      ? anyTooWide + ' of 125 labels are wider than a column at this width'
      : 'label mode needs more height than the viewport has');
}

function labelLayout(
  data: MapData,
  packed: Map<string, ReturnType<typeof pack>>,
  counts: Map<string, number>,
  bandRows: number[],
  pitch: number, gap: number,
  colW: number, colX: number[], gridTop: number, vp: Viewport, availH: number,
): MapLayout {
  const bands: BandPlace[] = [];
  const cells: CellPlace[] = [];
  const chips: ChipPlace[] = [];
  let y = gridTop;
  data.bands.forEach((b, bi) => {
    const height = bandRows[bi] * pitch;
    bands.push({ id: b.id, label: b.label, top: y, height, rows: bandRows[bi] });
    data.eras.forEach((e, ei) => {
      const key = cellKey(b.id, e.id);
      const p = packed.get(key)!;
      const cell: CellPlace = {
        key, band: b.id, era: e.id, x: colX[ei], y, w: colW, h: height,
        count: counts.get(key) || 0, shown: 0, plus: 0, names: [], plusBox: null,
      };
      let ry = y;
      for (const row of p.rows) {
        let x = colX[ei] + CELL_PAD;
        for (const item of row) {
          const place: ChipPlace = {
            id: item.n.id, x, y: ry + Math.round((pitch - CHIP_H) / 2),
            w: item.w, h: CHIP_H,
          };
          chips.push(place);
          cell.names.push(place);
          x += item.w + CHIP_GAP;
        }
        ry += pitch;
      }
      cell.shown = cell.names.length;
      cell.plus = cell.count - cell.shown;
      cells.push(cell);
    });
    y += height + gap;
  });

  return {
    mode: 'label', reason: 'every one of the 125 labels fits at 11px',
    pitch, gap, colW, gridTop, gridLeft: GUTTER,
    width: vp.w, height: Math.min(y - gap, gridTop + availH),
    bands, cells, chips, chipById: new Map(chips.map((c) => [c.id, c])),
    undrawn: [], colX,
  };
}

function cellLayout(
  data: MapData, counts: Map<string, number>, measure: Measure,
  colW: number, colX: number[], inner: number, gridTop: number,
  vp: Viewport, availH: number, reason: string,
): MapLayout {
  const nb = data.bands.length;
  const room = availH - CELL_GAP * (nb - 1);
  const weights = data.bands.map((b) => {
    let mx = 1;
    for (const e of data.eras) mx = Math.max(mx, counts.get(cellKey(b.id, e.id)) || 0);
    return mx;
  });
  const total = weights.reduce((a, x) => a + x, 0);
  const MIN_H = CELL_HEAD + CELL_ROW + 6;

  let heights = weights.map((w) => Math.max(MIN_H, Math.floor(room * w / total)));
  /* Give back whatever the floor took, from the bands that have slack. */
  let over = heights.reduce((a, x) => a + x, 0) - room;
  while (over > 0) {
    const idx = heights.map((hh, i) => [hh, i] as [number, number])
      .filter(([hh]) => hh > MIN_H)
      .sort((a, b) => b[0] - a[0]);
    if (!idx.length) break;
    for (const [, i] of idx) {
      if (over <= 0) break;
      heights[i] -= 1; over -= 1;
    }
  }

  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  const bands: BandPlace[] = [];
  const cells: CellPlace[] = [];
  const chips: ChipPlace[] = [];
  const undrawn: string[] = [];
  let y = gridTop;

  data.bands.forEach((b, bi) => {
    const height = heights[bi];
    bands.push({ id: b.id, label: b.label, top: y, height, rows: 0 });
    data.eras.forEach((e, ei) => {
      const key = cellKey(b.id, e.id);
      const ids = data.cells[key] || [];
      const nodes = ids.map((i) => byId.get(i)!).filter(Boolean).sort(byStartDate);
      const cell: CellPlace = {
        key, band: b.id, era: e.id, x: colX[ei], y, w: colW, h: height,
        count: nodes.length, shown: 0, plus: 0, names: [], plusBox: null,
      };
      const rowsAvail = Math.max(0, Math.floor((height - CELL_HEAD - 4) / CELL_ROW));
      const p = packCell(nodes, inner, rowsAvail, measure);
      p.rows.forEach((row, ri) => {
        let x = colX[ei] + CELL_PAD;
        for (const item of row) {
          const place: ChipPlace = {
            id: item.n.id,
            x, y: y + CELL_HEAD + ri * CELL_ROW + Math.round((CELL_ROW - CHIP_H) / 2),
            w: item.w, h: CHIP_H,
          };
          chips.push(place); cell.names.push(place);
          x += item.w + CHIP_GAP;
        }
      });
      const skipped = p.skipped.map((n) => n.id);
      /* The `+N` chip needs room on the row it sits on. It goes after the last
         name if it fits, on the next row if there is one, and otherwise the
         last name gives way to it -- the count printed is always
         members - names drawn, which is what C6 re-derives. */
      const left = colX[ei] + CELL_PAD;
      const right = colX[ei] + colW - CELL_PAD;
      const rowY = (r: number) => y + CELL_HEAD + r * CELL_ROW + Math.round((CELL_ROW - CHIP_H) / 2);
      let plusBox: Box | null = null;
      if (cell.count > cell.names.length) {
        const lastRow = p.rows.length - 1;
        for (;;) {
          const last = cell.names[cell.names.length - 1];
          if (!last) { plusBox = { x: left, y: rowY(0), w: PLUS_W, h: CHIP_H }; break; }
          if (last.x + last.w + CHIP_GAP + PLUS_W <= right) {
            plusBox = { x: last.x + last.w + CHIP_GAP, y: last.y, w: PLUS_W, h: CHIP_H };
            break;
          }
          if (lastRow + 1 < rowsAvail) {
            plusBox = { x: left, y: rowY(lastRow + 1), w: PLUS_W, h: CHIP_H };
            break;
          }
          cell.names.pop();
          const i = chips.indexOf(last);
          if (i >= 0) chips.splice(i, 1);
          skipped.push(last.id);
        }
      }
      cell.shown = cell.names.length;
      cell.plus = cell.count - cell.shown;
      cell.plusBox = cell.plus > 0 ? plusBox : null;
      for (const id of skipped) undrawn.push(id);
      cells.push(cell);
    });
    y += height + CELL_GAP;
  });

  return {
    mode: 'cell', reason,
    pitch: CELL_ROW, gap: CELL_GAP, colW, gridTop, gridLeft: GUTTER,
    width: vp.w, height: y - CELL_GAP,
    bands, cells, chips, chipById: new Map(chips.map((c) => [c.id, c])),
    undrawn, colX,
  };
}
