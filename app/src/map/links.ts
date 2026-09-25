/* map/links.ts: orthogonal links on a canvas, behind the chips.
 *
 * Design response 1.4 and 4.8: exit horizontally, one vertical routed in the
 * gutter nearest the source, enter horizontally, a 2px end mark. Denial edges
 * red, derived pairs amber dashed and off by default.
 *
 * The canvas draws lines only. Every label on this page is real DOM text, so a
 * check can read it; nothing here draws a mark that a label would have to
 * explain.
 */
import type { MapLayout, ChipPlace } from './layout';

export type LinkKind = 'direct' | 'denial' | 'derived';

export interface Link { a: string; b: string; kind: LinkKind; }

export interface DrawOpts {
  /** when set, links touching this id are at full opacity and the rest at 35% */
  focus: string | null;
  dpr: number;
}

const COLOUR: Record<LinkKind, string> = {
  direct: '94,212,230',
  denial: '232,112,95',
  derived: '239,181,85',
};

const REST_ALPHA: Record<LinkKind, number> = { direct: 0.34, denial: 0.6, derived: 0.4 };

function nearestGutter(colX: number[], from: number, dir: number): number {
  const side = colX.filter((g) => (dir > 0 ? g > from : g < from));
  if (side.length) return dir > 0 ? Math.min(...side) : Math.max(...side);
  let best = colX[0];
  for (const g of colX) if (Math.abs(g - from) < Math.abs(best - from)) best = g;
  return best;
}

export function drawLinks(
  cv: HTMLCanvasElement, lay: MapLayout, links: Link[], opts: DrawOpts,
): number {
  const w = lay.width;
  const h = Math.max(lay.height, 1);
  const dpr = opts.dpr;
  cv.width = Math.round(w * dpr);
  cv.height = Math.round(h * dpr);
  cv.style.width = w + 'px';
  cv.style.height = h + 'px';
  const ctx = cv.getContext('2d');
  if (!ctx) return 0;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  ctx.lineWidth = 1;

  /* Verticals sharing a gutter are spread across it so two links are two lines
     rather than one. The spread is deterministic, never random. */
  const slot = new Map<number, number>();
  let drawn = 0;

  for (const link of links) {
    const sa: ChipPlace | undefined = lay.chipById.get(link.a);
    const sb: ChipPlace | undefined = lay.chipById.get(link.b);
    if (!sa || !sb) continue;

    const touched = !!opts.focus && (link.a === opts.focus || link.b === opts.focus);
    const alpha = opts.focus ? (touched ? 1 : 0.35 * REST_ALPHA[link.kind]) : REST_ALPHA[link.kind];
    ctx.strokeStyle = 'rgba(' + COLOUR[link.kind] + ',' + alpha.toFixed(3) + ')';
    ctx.setLineDash(link.kind === 'derived' ? [4, 3] : []);

    const sy = Math.round(sa.y + sa.h / 2) + 0.5;
    const ty = Math.round(sb.y + sb.h / 2) + 0.5;

    ctx.beginPath();
    if (Math.abs(sy - ty) < 1) {
      const left = sa.x < sb.x ? sa : sb;
      const right = sa.x < sb.x ? sb : sa;
      ctx.moveTo(Math.round(left.x + left.w) + 0.5, sy);
      ctx.lineTo(Math.round(right.x) + 0.5, ty);
      ctx.stroke();
      endMark(ctx, Math.round(sb.x < sa.x ? sb.x + sb.w : sb.x) + 0.5, ty);
      drawn++;
      continue;
    }

    const dir = sb.x + sb.w / 2 >= sa.x + sa.w / 2 ? 1 : -1;
    const exit = dir > 0 ? sa.x + sa.w : sa.x;
    let gx = nearestGutter(lay.colX, exit, dir);
    const n = (slot.get(gx) || 0);
    slot.set(gx, n + 1);
    gx = gx + ((n % 9) - 4);

    const tx = Math.abs(gx - sb.x) <= Math.abs(gx - (sb.x + sb.w)) ? sb.x : sb.x + sb.w;
    const gxr = Math.round(gx) + 0.5;
    ctx.moveTo(Math.round(exit) + 0.5, sy);
    ctx.lineTo(gxr, sy);
    ctx.lineTo(gxr, ty);
    ctx.lineTo(Math.round(tx) + 0.5, ty);
    ctx.stroke();
    endMark(ctx, Math.round(tx) + 0.5, ty);
    drawn++;
  }
  ctx.setLineDash([]);
  return drawn;
}

/* The 2px end mark: a short tick across the line where it meets the target. */
function endMark(ctx: CanvasRenderingContext2D, x: number, y: number): void {
  ctx.beginPath();
  ctx.moveTo(x, y - 2);
  ctx.lineTo(x, y + 2);
  ctx.stroke();
}
