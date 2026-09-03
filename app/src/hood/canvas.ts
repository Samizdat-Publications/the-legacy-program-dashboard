/* hood/canvas.ts — the lines only. Every name on this screen is DOM text; the
 * canvas draws no text at all, so nothing here can be an anonymous mark.
 *
 * Design response 1.5: solid cyan from the centre to a member below the L0
 * floor; dashed and type-coloured to a map node (denial red, custody and
 * funding amber); a dash-offset animation on the selected node's edges; hop-2
 * and derived lines dotted grey.
 *
 * The animation is the treatment the owner kept from the old board's
 * `drawParticle2D` (tools/l0_patches.py, ~2418): motion ONLY on the selected
 * node's own edges, running away from the reader. Nothing is ported verbatim —
 * that renderer moves a dot along a polyline, this one offsets a dash pattern
 * along a straight line — but the rule is the same one, and it is the reason
 * hop-2 lines never move: the board makes no directional claim about them.
 */
export type LineStyle = 'solid' | 'dash' | 'dot';

export interface Line {
  x1: number; y1: number; x2: number; y2: number;
  style: LineStyle;
  colour: string;
  animate: boolean;
}

export interface Scene {
  w: number; h: number;
  cx: number; cy: number; r: number;
  lines: Line[];
}

/* CSS custom properties are the palette; the canvas needs the resolved value. */
export function resolve(token: string): string {
  const m = token.match(/^var\((--[a-z0-9-]+)\)$/);
  if (!m) return token;
  const v = getComputedStyle(document.documentElement).getPropertyValue(m[1]).trim();
  return v || '#8d97a4';
}

const DASH = [7, 5];
const DOT = [1, 4];

export function paint(canvas: HTMLCanvasElement, scene: Scene, phase: number): void {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  if (canvas.width !== Math.round(scene.w * dpr) || canvas.height !== Math.round(scene.h * dpr)) {
    canvas.width = Math.round(scene.w * dpr);
    canvas.height = Math.round(scene.h * dpr);
  }
  canvas.style.width = scene.w + 'px';
  canvas.style.height = scene.h + 'px';

  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, scene.w, scene.h);
  ctx.lineCap = 'butt';
  ctx.lineJoin = 'miter';

  /* the ring itself, faint: it is the structure the slots sit on */
  if (scene.r > 0) {
    ctx.save();
    ctx.strokeStyle = resolve('var(--line)');
    ctx.globalAlpha = 0.6;
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 5]);
    ctx.beginPath();
    ctx.arc(scene.cx, scene.cy, scene.r, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  /* dotted first, so the sourced lines from the centre sit above them */
  const order: LineStyle[] = ['dot', 'solid', 'dash'];
  for (const style of order) {
    for (const l of scene.lines) {
      if (l.style !== style) continue;
      ctx.save();
      ctx.strokeStyle = l.colour;
      ctx.lineWidth = 1;
      if (style === 'dash') {
        ctx.setLineDash(DASH);
        ctx.globalAlpha = 0.9;
        if (l.animate) ctx.lineDashOffset = -phase;
      } else if (style === 'dot') {
        ctx.setLineDash(DOT);
        ctx.globalAlpha = 0.5;
      } else {
        ctx.globalAlpha = 0.8;
      }
      ctx.beginPath();
      ctx.moveTo(l.x1, l.y1);
      ctx.lineTo(l.x2, l.y2);
      ctx.stroke();
      ctx.restore();
    }
  }
}

/* Runs the dash-offset animation. Returns the stopper; the page calls it before
   every re-layout and on every route change, so no two loops ever run. */
export function animate(canvas: HTMLCanvasElement, scene: Scene): () => void {
  let raf = 0;
  let stopped = false;
  const moving = scene.lines.some((l) => l.animate);
  const start = performance.now();

  const frame = (now: number) => {
    if (stopped) return;
    paint(canvas, scene, ((now - start) * 0.024) % 12);
    raf = requestAnimationFrame(frame);
  };

  if (moving && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    raf = requestAnimationFrame(frame);
  } else {
    paint(canvas, scene, 0);
  }
  return () => { stopped = true; if (raf) cancelAnimationFrame(raf); };
}
