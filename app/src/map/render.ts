/* map/render.ts: the program map. Design response 1.4, 2.2, 2.3, 2.4 and 4.
 *
 * Chips are DOM anchors, so every label on the map is real text a check can read
 * and every chip is a `#/n/<id>` route. Links are drawn on a canvas behind them.
 *
 * What this file must never do: truncate a label, shrink one, or draw a mark
 * without one. A chip whose label does not fit is not drawn; it is counted, and
 * the count is what is drawn instead.
 */
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { clsColour, clsLetter } from '../data';
import {
  loadMapData, restEdges, denialKeys, edgeKey, resolveCellKey, urlCellKey,
  byStartDate, startYear, REST_BUDGET,
  type MapData, type MapNode,
} from './model';
import {
  layout, BAR_H, STRIP_H, HEAD_H, LEGEND_H, GUTTER, CELL_HEAD,
  type MapLayout, type CellPlace,
} from './layout';
import { drawLinks, type Link } from './links';

/* ---- controls, kept across re-layouts and route changes ------------------ */
let showRest = true;
let showStart = true;
let showDerived = false;
let forceCells = false;

export interface MapRequest {
  cell?: string | null;
  node?: string | null;
  thread?: string | null;
}

interface ThreadStep { node: string; year?: number | string; evidence?: string; }
interface Thread { id: string; label?: string; title?: string; steps: ThreadStep[]; }

let threadsCache: Promise<Thread[]> | null = null;
function loadThreads(): Promise<Thread[]> {
  if (!threadsCache) {
    threadsCache = fetch(import.meta.env.BASE_URL + 'data/threads.json')
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status))))
      .then((j: { threads?: Thread[] } | Thread[]) => (Array.isArray(j) ? j : j.threads || []))
      .catch(() => [] as Thread[]);
  }
  return threadsCache;
}

/* ---- the mounted map, so a resize can re-lay it out --------------------- */
let mounted: { root: HTMLElement; paint: () => void } | null = null;
let pending = 0;
window.addEventListener('resize', () => {
  if (!mounted || !document.body.contains(mounted.root)) { mounted = null; return; }
  if (pending) cancelAnimationFrame(pending);
  pending = requestAnimationFrame(() => { pending = 0; if (mounted) mounted.paint(); });
});

/* Text is measured with the real font at the real size, in the document, and
   the chip is then given exactly that width. Nothing is estimated. */
const widthCache = new Map<string, number>();

export async function renderMap(view: HTMLElement, req: MapRequest): Promise<void> {
  const data = await loadMapData();
  const threads = req.thread ? await loadThreads() : [];
  const thread = req.thread ? threads.find((t) => t.id === req.thread) || null : null;

  try {
    if (document.fonts) {
      await document.fonts.load("400 11px 'IBM Plex Mono'");
      await document.fonts.ready;
    }
  } catch { /* the fallback stack is metrically different; measurement still reads it */ }

  const byId = new Map(data.nodes.map((n) => [n.id, n]));
  const focus = req.node && byId.has(req.node) ? req.node : null;
  const den = denialKeys(data);
  const rest = restEdges(data);

  setTitle(
    thread ? 'Map · ' + (thread.title || thread.label || thread.id)
      : focus ? 'Map · ' + (byId.get(focus)!.label)
        : 'The program map',
  );

  clear(view);
  const root = h('div', { class: 'map-root' });
  view.append(root);

  const meas = h('span', { class: 'chip-measure', 'aria-hidden': 'true' });
  root.append(meas);
  const measure = (s: string): number => {
    let v = widthCache.get(s);
    if (v === undefined) {
      meas.textContent = s;
      v = meas.getBoundingClientRect().width;
      widthCache.set(s, v);
    }
    return v;
  };

  let hover: string | null = null;
  const chipEls = new Map<string, HTMLElement>();
  let lay: MapLayout;

  const baseHref = (): string =>
    thread ? '#/t/' + thread.id + '/map' : focus ? '#/n/' + focus + '/map' : '#/map';

  function paint(): void {
    /* keep the measuring span; rebuild everything else */
    dropPanelListeners();
    clear(root);
    root.append(meas);
    chipEls.clear();
    hover = null;

    const vp = { w: window.innerWidth, h: window.innerHeight };
    lay = layout(data, vp, measure, forceCells);

    const openKey = lay.mode === 'cell' && focus
      ? cellOf(data, focus)
      : resolveCellKey(req.cell || null, data);
    const open = openKey ? lay.cells.find((c) => c.key === openKey) || null : null;

    /* ---- the control strip -------------------------------------------- */
    const strip = h('div', { class: 'map-strip' });
    strip.append(h('span', { class: 'eyebrow' }, 'PROGRAM MAP'));
    const links = buildLinks(open);
    strip.append(h('span', { class: 'map-stat', title: lay.reason }, statLine(lay, links.length, data)));
    if (thread) {
      const on = thread.steps.filter((s) => lay.chipById.has(s.node)).length;
      strip.append(h('span', { class: 'map-note' },
        (thread.title || thread.label || thread.id) + ': ' + on + ' of ' +
        thread.steps.length + ' steps are on the map'));
    }
    const ctl = h('div', { class: 'map-ctrls' });
    ctl.append(button('FIT', true, () => paint(), 'the layout is computed for this viewport'));
    ctl.append(button('LINES AT REST', showRest, () => { showRest = !showRest; paint(); }));
    ctl.append(button('START HERE', showStart, () => { showStart = !showStart; paint(); }));
    ctl.append(button('DERIVED', showDerived, () => { showDerived = !showDerived; paint(); }));
    ctl.append(button('CELLS', forceCells, () => { forceCells = !forceCells; paint(); }));
    strip.append(ctl);
    root.append(strip);

    /* ---- era column heads ---------------------------------------------- */
    const head = h('div', { class: 'map-head', style: 'top:' + STRIP_H + 'px;height:' + HEAD_H + 'px' });
    data.eras.forEach((e, i) => {
      head.append(h('div', {
        class: 'era-head',
        style: 'left:' + lay.colX[i] + 'px;width:' + lay.colW + 'px',
      }, h('b', null, e.label), h('i', null, e.sub)));
    });
    root.append(head);

    /* ---- the grid ------------------------------------------------------- */
    const grid = h('div', { class: 'map-grid' });
    root.append(grid);

    const cv = h('canvas', { class: 'map-links', 'aria-hidden': 'true' }) as HTMLCanvasElement;
    grid.append(cv);

    const bandCount = new Map<string, number>();
    for (const n of data.nodes) bandCount.set(n.band, (bandCount.get(n.band) || 0) + 1);

    for (const b of lay.bands) {
      grid.append(h('div', {
        class: 'band-lab',
        style: 'top:' + b.top + 'px;height:' + b.height + 'px;width:' + (GUTTER - 12) + 'px',
      }, h('b', null, b.label.toUpperCase()), h('i', null, (bandCount.get(b.id) || 0) + ' nodes')));
    }

    for (const cell of lay.cells) {
      const isOpen = !!open && open.key === cell.key;
      const el = h('div', {
        class: 'cell' + (isOpen ? ' open' : '') + (cell.count === 0 ? ' empty' : ''),
        style: 'left:' + cell.x + 'px;top:' + cell.y + 'px;width:' + cell.w + 'px;height:' + cell.h + 'px',
        'data-cell': cell.key,
        role: cell.count ? 'button' : null,
        tabindex: cell.count ? '0' : null,
        'aria-expanded': cell.count ? String(isOpen) : null,
      });
      if (cell.count) {
        const go = (): void => { location.hash = isOpen ? baseHref() : '#/map?cell=' + urlCellKey(cell.key, data); };
        el.addEventListener('click', (ev) => {
          if ((ev.target as HTMLElement).closest('a.chip')) return;
          go();
        });
        el.addEventListener('keydown', (ev) => {
          const k = ev as KeyboardEvent;
          if (k.key === 'Enter' || k.key === ' ') { k.preventDefault(); go(); }
        });
      }
      if (lay.mode === 'cell' && cell.count) {
        el.append(h('div', { class: 'cell-head', style: 'height:' + CELL_HEAD + 'px' },
          h('span', null, cell.count + (cell.count === 1 ? ' node' : ' nodes')),
          h('span', { class: 'cell-cta' }, isOpen ? 'open' : 'click to expand')));
      }
      grid.append(el);
    }

    for (const place of lay.chips) {
      const n = byId.get(place.id);
      if (!n) continue;
      const el = chip(n, place.w, thread, focus);
      el.setAttribute('style',
        'left:' + place.x + 'px;top:' + place.y + 'px;width:' + place.w + 'px;height:' + place.h + 'px');
      el.addEventListener('mouseenter', () => { hover = n.id; applyFocus(); });
      el.addEventListener('mouseleave', () => { hover = null; applyFocus(); });
      chipEls.set(n.id, el);
      grid.append(el);
    }

    for (const cell of lay.cells) {
      if (!cell.plusBox || cell.plus <= 0) continue;
      const b = cell.plusBox;
      grid.append(h('span', {
        class: 'plus',
        style: 'left:' + b.x + 'px;top:' + b.y + 'px;height:' + b.h + 'px',
        title: cell.plus + ' more in this cell; open it to read them',
      }, '+' + cell.plus));
    }

    /* ---- legend, at the bottom edge ------------------------------------ */
    const present: string[] = [];
    for (const n of data.nodes) if (!present.includes(n.cls)) present.push(n.cls);
    present.sort();
    const legend = h('div', { class: 'map-legend', style: 'height:' + LEGEND_H + 'px' });
    for (const c of present) {
      legend.append(h('span', { class: 'leg' },
        h('i', { style: 'background:' + clsColour(c) }), c));
    }
    root.append(legend);

    /* ---- the expansion panel, Design 2.3 -------------------------------- */
    if (open) root.append(panel(open, data, byId, focus, baseHref()));

    drawLinks(cv, lay, links, { focus: null, dpr: window.devicePixelRatio || 1 });
    grid.setAttribute('data-mode', lay.mode);

    if (focus) {
      const el = chipEls.get(focus);
      if (el) el.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    }

    function applyFocus(): void {
      grid.classList.toggle('is-dim', !!hover);
      for (const [id, el] of chipEls) el.classList.toggle('rel', !!hover && related(id, hover));
      drawLinks(cv, lay, links, { focus: hover, dpr: window.devicePixelRatio || 1 });
    }

    function related(id: string, to: string): boolean {
      if (id === to) return true;
      for (const l of links) if ((l.a === to && l.b === id) || (l.b === to && l.a === id)) return true;
      return false;
    }
  }

  /* ---- which links are drawn ------------------------------------------- */
  function buildLinks(open: CellPlace | null): Link[] {
    const out: Link[] = [];
    const seen = new Set<string>();
    const kindOf = (a: string, b: string): Link['kind'] =>
      (den.has(edgeKey(a, b)) ? 'denial' : 'direct');
    const push = (a: string, b: string, kind: Link['kind']): void => {
      const k = kind + '|' + edgeKey(a, b);
      if (seen.has(k)) return;
      seen.add(k);
      out.push({ a, b, kind });
    };

    if (lay.mode === 'label' && showRest) {
      for (const e of rest) push(e.a, e.b, kindOf(e.a, e.b));
    }
    if (lay.mode === 'label' && showDerived) {
      for (const s of data.summarised) push(s.a, s.b, 'derived');
    }
    /* the node the reader arrived on gets all of its edges, budget or not */
    if (focus) {
      for (const e of data.direct) if (e.a === focus || e.b === focus) push(e.a, e.b, kindOf(e.a, e.b));
      if (showDerived) for (const s of data.summarised) if (s.a === focus || s.b === focus) push(s.a, s.b, 'derived');
    }
    /* an open cell draws its members' edges: Design 2.2, cell mode */
    if (open) {
      const members = new Set(data.cells[open.key] || []);
      for (const e of data.direct) {
        if (members.has(e.a) || members.has(e.b)) push(e.a, e.b, kindOf(e.a, e.b));
      }
    }
    if (thread) {
      for (let i = 1; i < thread.steps.length; i++) {
        const a = thread.steps[i - 1].node;
        const b = thread.steps[i].node;
        const s = data.summarised.find((x) => edgeKey(x.a, x.b) === edgeKey(a, b));
        push(a, b, den.has(edgeKey(a, b)) ? 'denial' : s ? 'derived' : 'direct');
      }
    }
    return out;
  }

  mounted = { root, paint };
  paint();
  publish(data, chipEls, () => lay);
}

/* -------------------------------------------------------------------------- */

function cellOf(data: MapData, id: string): string | null {
  for (const [k, ids] of Object.entries(data.cells)) if (ids.includes(id)) return k;
  return null;
}

function statLine(lay: MapLayout, drawn: number, data: MapData): string {
  const total = data.direct.length + data.summarised.length;
  if (lay.mode === 'label') {
    return data.nodes.length + ' nodes · ' + drawn + ' of ' + total +
      ' links at rest · all labels at 11px · row pitch ' + lay.pitch +
      ', band gap ' + lay.gap + ' · scale 1:1';
  }
  return data.nodes.length + ' nodes · ' + drawn +
    ' links · below the label floor: cells show counts · select a cell';
}

function button(label: string, on: boolean, fn: () => void, title?: string): HTMLElement {
  return h('button', {
    class: 'ctl' + (on ? ' on' : ''),
    type: 'button',
    'aria-pressed': String(on),
    title: title || null,
    onclick: fn,
  }, label);
}

function chip(n: MapNode, w: number, thread: Thread | null, focus: string | null): HTMLElement {
  const isStep = !!thread && thread.steps.some((s) => s.node === n.id);
  const cls = 'chip'
    + (n.hl && showStart ? ' hl' : '')
    + (isStep ? ' step' : '')
    + (focus === n.id ? ' sel' : '');
  const el = h('a', {
    class: cls,
    href: '#/n/' + n.id,
    'data-id': n.id,
    'data-w': String(w),
    style: 'border-left-color:' + clsColour(n.cls),
  });
  el.append(h('i', { class: 'cletter', 'aria-hidden': 'true' }, clsLetter(n.cls)));
  el.append(h('span', { class: 'clabel' }, n.short));
  if (n.hl && showStart) el.append(h('i', { class: 'chl' }, String(n.hl)));
  return el;
}

/* The expansion panel: every member as a 20px row, in start-date order. */
function panel(
  cell: CellPlace, data: MapData, byId: Map<string, MapNode>,
  focus: string | null, back: string,
): HTMLElement {
  const band = data.bands.find((b) => b.id === cell.band);
  const era = data.eras.find((e) => e.id === cell.era);
  const members = (data.cells[cell.key] || [])
    .map((id) => byId.get(id)!).filter(Boolean).sort(byStartDate);

  const wide = Math.min(Math.max(cell.w * 2, 380), 560);
  const bodyH = Math.ceil(members.length / (wide > 500 ? 2 : 1)) * 20 + 8;
  const panelH = bodyH + 26;
  const vpH = window.innerHeight - BAR_H;
  let top = cell.y + cell.h + 4;
  if (top + panelH > vpH - LEGEND_H) top = Math.max(STRIP_H + HEAD_H, cell.y - panelH - 4);
  let left = cell.x;
  if (left + wide > window.innerWidth - 8) left = Math.max(GUTTER, window.innerWidth - 8 - wide);

  const p = h('div', {
    class: 'cell-panel',
    role: 'dialog',
    'aria-label': (band ? band.label : cell.band) + ' × ' + (era ? era.label : cell.era),
    style: 'left:' + left + 'px;top:' + top + 'px;width:' + wide + 'px',
  });
  p.append(h('div', { class: 'cp-head' },
    h('b', null, (band ? band.label : cell.band).toUpperCase() + ' × ' + (era ? era.label : cell.era)),
    h('span', null, members.length + (members.length === 1 ? ' node' : ' nodes') + ' · sorted by start date'),
    h('a', { class: 'cp-close', href: back, title: 'ESC' }, 'ESC ×')));

  const list = h('div', { class: 'cp-list' + (wide > 500 ? ' two' : '') });
  for (const m of members) {
    const row = h('a', {
      class: 'cell-row' + (focus === m.id ? ' sel' : ''),
      href: '#/n/' + m.id,
      'data-id': m.id,
    });
    row.append(h('i', { class: 'mark', style: 'background:' + clsColour(m.cls), 'aria-hidden': 'true' }));
    row.append(h('span', { class: 'yr' }, startYear(m) || '-'));
    row.append(h('span', { class: 'nm' }, m.short));
    if (m.hl) row.append(h('i', { class: 'chl' }, String(m.hl)));
    list.append(row);
  }
  p.append(list);

  const esc = (ev: Event): void => {
    if ((ev as KeyboardEvent).key === 'Escape') location.hash = back;
  };
  /* A click outside closes it -- but never by overriding a link the reader has
     just followed, which would swallow every chip click on the page. */
  const away = (ev: Event): void => {
    const t = ev.target as HTMLElement;
    if (t.closest('a[href^="#/"]') || t.closest('.cell-panel') || t.closest('.cell')) return;
    location.hash = back;
  };
  document.addEventListener('keydown', esc);
  setTimeout(() => document.addEventListener('click', away), 0);
  panelCleanup.push(() => {
    document.removeEventListener('keydown', esc);
    document.removeEventListener('click', away);
  });
  return p;
}

/* Listeners the open panel installed; dropped whenever the map repaints. */
const panelCleanup: (() => void)[] = [];
function dropPanelListeners(): void {
  while (panelCleanup.length) (panelCleanup.pop() as () => void)();
}

/* -------------------------------------------------------------------------- */
/* What phase 5's checks read. Every figure is measured off what rendered, not
   off the layout's own intentions: C4 is about boxes on the screen.            */
interface ChipProbe { id: string; x: number; y: number; w: number; h: number; mode: string; labelled: boolean; }
interface CellProbe { key: string; count: number; shown: number; plus: number; }

function publish(
  data: MapData, els: Map<string, HTMLElement>, get: () => MapLayout,
): void {
  const w = window as unknown as { __app?: Record<string, unknown> };
  w.__app = w.__app || {};
  (w.__app as Record<string, unknown>).map = {
    chips(): ChipProbe[] {
      const lay = get();
      const out: ChipProbe[] = [];
      for (const n of data.nodes) {
        const el = els.get(n.id);
        if (!el) {
          out.push({ id: n.id, x: 0, y: 0, w: 0, h: 0, mode: lay.mode, labelled: false });
          continue;
        }
        const r = el.getBoundingClientRect();
        const span = el.querySelector('.clabel') as HTMLElement | null;
        const sw = span ? span.getBoundingClientRect().width : 0;
        out.push({
          id: n.id,
          x: r.left + window.scrollX,
          y: r.top + window.scrollY,
          w: r.width, h: r.height,
          mode: lay.mode,
          labelled: !!span && span.textContent === n.short && sw > 0 && sw <= r.width - 30 + 0.5,
        });
      }
      return out;
    },
    cells(): CellProbe[] {
      return get().cells.map((c) => ({ key: c.key, count: c.count, shown: c.shown, plus: c.plus }));
    },
    budget: REST_BUDGET,
  };
}
