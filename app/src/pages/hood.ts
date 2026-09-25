/* The neighbourhood: Design response 1.5, 2.2 and 2.4.
 *
 * The selected node in the centre, hop 1 on a ring whose positions are assigned
 * by y in 15px label slots on each side, hop 2 (and 3) in two outer columns.
 * Every name is DOM text at the one label size; the canvas draws only lines.
 *
 * Nothing on this page is written here except the frame's own words. Every node
 * name, edge type and tier comes from the board's own record.
 */
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadHighlights, loadNode, loadIndex, clsColour, type IndexNode } from '../data';
import { groupConnections, renderConnGroups } from './connections';
import { buildHood, startHereHood, edgeColour, type Entry, type Hood } from '../hood/model';
import { layout, type Layout, type Placed } from '../hood/layout';
import { animate, resolve, type Line, type Scene } from '../hood/canvas';
import { notFound } from './notfound';
import '../styles/hood.css';

/* ---- state that survives a change of centre (Design 2.4) ----------------- */
let chosenHops: 1 | 2 | 3 | null = null;
let derivedOn = true;
let expanded = false;

function defaultHops(): 1 | 2 | 3 {
  /* one hop by default below 1600px, two at and above */
  return window.innerWidth >= 1600 ? 2 : 1;
}
function hops(): 1 | 2 | 3 {
  return chosenHops || defaultHops();
}

/* ---- what the checks read (spec section 6) ------------------------------- */
export interface RingEntry { id: string; hop: number; x: number; y: number; labelled: boolean }
interface HoodApi {
  ring(): RingEntry[];
  centre(): { id: string | null; label: string; x: number; y: number };
}
interface AppWindow extends Window { __app?: Record<string, unknown> }

let ring: RingEntry[] = [];
let centreOut = { id: null as string | null, label: '', x: 0, y: 0 };
let installed = false;
function publish(): void {
  if (installed) return;
  installed = true;
  const w = window as AppWindow;
  const app = (w.__app = w.__app || {});
  const api: HoodApi = { ring: () => ring.slice(), centre: () => ({ ...centreOut }) };
  app.hood = api;
}

/* ---- one live page at a time -------------------------------------------- */
let generation = 0;
let stopPaint: (() => void) | null = null;
let relayout: (() => void) | null = null;
let resizeTimer = 0;

window.addEventListener('resize', () => {
  if (!relayout) return;
  window.clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(() => { if (relayout) relayout(); }, 120);
});

export async function renderHood(view: HTMLElement, id: string | null): Promise<void> {
  const gen = ++generation;
  if (stopPaint) { stopPaint(); stopPaint = null; }
  relayout = null;
  publish();
  if (window.innerWidth <= 760) { await renderHoodPhone(view, id, gen); return; }

  let hood: Hood;
  try {
    if (id) hood = await buildHood(id, hops(), derivedOn);
    else hood = await startHereHood((await loadHighlights()).flags);
  } catch (e) {
    if (gen !== generation) return;
    notFound(view, id ? '#/hood/' + id : '#/hood',
      'The neighbourhood needs this node\'s record and the edge list: ' + (e as Error).message);
    return;
  }
  if (gen !== generation) return;

  setTitle(hood.centre ? hood.centre.label : 'Neighbourhood', 'Neighbourhood');

  clear(view);
  const wrap = h('div', { class: 'hood' });
  const strip = h('div', { class: 'hood-strip' });
  const stage = h('div', { class: 'hood-stage' });
  const legend = h('div', { class: 'hood-legend' });
  wrap.append(strip, stage, legend);
  view.append(wrap);

  buildLegend(legend);

  const canvas = h('canvas', { class: 'hood-canvas', 'aria-hidden': 'true' });
  stage.append(canvas);

  const draw = () => {
    if (gen !== generation) return;
    if (stopPaint) { stopPaint(); stopPaint = null; }
    paintStage(stage, canvas, hood, id);
    buildStrip(strip, hood, id);
  };
  relayout = draw;
  draw();

  /* the hop and derived controls rebuild the data, keeping the centre */
  strip.addEventListener('hood:reload', () => { void renderHood(view, id); });
}

/* ------------------------------------------------------------------------- */

function buildStrip(strip: HTMLElement, hood: Hood, id: string | null): void {
  clear(strip);
  const l = lastLayout;
  const line = h('div', { class: 'hood-say' });
  line.append(h('span', { class: 'eyebrow' }, 'Neighbourhood'));
  /* the board's own short label, as Design's capture has it: the full name goes
     in the title attribute and on the node page, and the strip must not clip */
  line.append(h('span', {
    class: 'hood-who',
    title: hood.centre ? hood.centre.label : '',
  }, hood.centre ? hood.centreLabel : 'nothing selected'));

  const bits: string[] = [];
  if (l) {
    if (id) {
      bits.push(l.total.one + ' linked, ' + l.named.one + ' named');
      bits.push(hops() >= 2
        ? l.total.two + ' two steps away, ' + l.named.two + ' named'
        : 'two steps away: off at this width');
      if (hops() >= 3) bits.push(l.total.three + ' three steps away, ' + l.named.three + ' named');
      bits.push('shared-member links ' + (derivedOn ? 'on' : 'off'));
    } else {
      bits.push(l.total.one + ' start-here nodes, ' + l.named.one + ' named');
      bits.push('pick one to open its neighbourhood');
    }
  }
  for (const b of bits) {
    line.append(h('span', { class: 'sep' }, '·'));
    line.append(h('span', { class: 'dim' }, b));
  }
  strip.append(line);

  const ctl = h('div', { class: 'hood-ctl' });
  const hopBtn = (n: 1 | 2 | 3, label: string) => h('button', {
    class: 'hood-b' + (hops() === n ? ' on' : ''),
    type: 'button',
    'aria-pressed': hops() === n ? 'true' : 'false',
    onclick: () => { chosenHops = n; expanded = false; strip.dispatchEvent(new CustomEvent('hood:reload')); },
  }, label);
  ctl.append(hopBtn(1, '1 HOP'), hopBtn(2, '2 HOPS'), hopBtn(3, '3 HOPS'));
  ctl.append(h('button', {
    class: 'hood-b' + (derivedOn ? ' on' : ''),
    type: 'button',
    'aria-pressed': derivedOn ? 'true' : 'false',
    title: 'Links between two map nodes that share a member too minor for the map.',
    onclick: () => { derivedOn = !derivedOn; strip.dispatchEvent(new CustomEvent('hood:reload')); },
  }, 'SHARED MEMBERS'));
  ctl.append(id
    ? h('a', { class: 'hood-b', href: '#/n/' + id + '/map' }, 'SHOW ON MAP')
    : h('a', { class: 'hood-b', href: '#/map' }, 'SHOW THE MAP'));
  strip.append(ctl);
}

let lastLayout: Layout | null = null;

function paintStage(stage: HTMLElement, canvas: HTMLCanvasElement, hood: Hood, id: string | null): void {
  for (const el of Array.from(stage.querySelectorAll('.hood-el'))) el.remove();

  const rect = stage.getBoundingClientRect();
  const w = Math.max(320, Math.round(rect.width));
  const hgt = Math.max(240, Math.round(rect.height));

  const outer = hops() >= 2 ? [...hood.hop2, ...(hops() >= 3 ? hood.hop3 : [])] : [];
  const lay = layout(hood.hop1, outer, w, hgt, hops());
  lastLayout = lay;
  const g = lay.geom;

  /* ---- the centre ------------------------------------------------------- */
  const cwrap = h('div', {
    class: 'hood-el hood-centre' + (hood.centre ? '' : ' empty'),
    style: 'left:' + g.cx + 'px;top:' + g.cy + 'px',
  });
  cwrap.append(mark(hood.centre ? clsColour(hood.centre.cls) : 'var(--faint)'));
  stage.append(cwrap);
  stage.append(h('div', {
    class: 'hood-el hood-centre-name' + (hood.centre ? '' : ' empty'),
    style: 'left:' + g.cx + 'px;top:' + (g.cy + 14) + 'px',
  }, hood.centreLabel));

  /* ---- the names -------------------------------------------------------- */
  for (const p of lay.placed) stage.append(nodeEl(p, hood));

  /* ---- the +N chip and its expansion ------------------------------------ */
  const missOne = lay.total.one - lay.named.one;
  const missTwo = lay.total.two - lay.named.two;
  const missThree = lay.total.three - lay.named.three;
  if (missOne + missTwo + missThree > 0) {
    let text = missOne + ' more linked directly';
    if (hops() >= 2) text += ', ' + missTwo + ' more two steps away';
    if (hops() >= 3) text += ', ' + missThree + ' more three steps away';
    text += ': no room on the ring for their full names';
    const chip = h('div', {
      class: 'hood-el hood-chip',
      style: 'left:' + g.cx + 'px;top:' + (g.cy + g.R + 34) + 'px',
    },
      h('span', { class: 'dim' }, text),
      h('span', { class: 'sep' }, '·'),
      h('button', {
        class: 'hood-expand-b', type: 'button',
        onclick: () => { expanded = !expanded; if (relayout) relayout(); },
      }, expanded ? 'close' : 'expand ›'),
    );
    stage.append(chip);

    if (expanded) {
      const panel = h('div', {
        class: 'hood-el hood-expanded',
        style: 'left:' + g.cx + 'px;top:' + g.cy + 'px',
      });
      panel.append(h('div', { class: 'eyebrow hood-exp-head' },
        'Not drawn on the ring, because the whole name does not fit there'));
      const list = h('div', { class: 'hood-exp-list' });
      for (const e of lay.unnamed) {
        list.append(h('a', { class: 'hood-exp-row', href: '#/n/' + e.id },
          mark(clsColour(e.cls)),
          h('span', { class: 'hood-exp-label' }, e.full),
          h('span', { class: 'hood-exp-meta' }, e.suffix),
        ));
      }
      panel.append(list);
      stage.append(panel);
    }
  }

  /* ---- the lines -------------------------------------------------------- */
  const lines: Line[] = [];
  const grey = resolve('var(--faint)');
  for (const p of lay.placed) {
    if (p.e.hop === 1) {
      if (!id) continue;            /* nothing selected: no line asserts anything */
      const isMember = p.e.kind === 'member';
      lines.push({
        x1: g.cx, y1: g.cy, x2: p.x, y2: p.y,
        style: isMember ? 'solid' : 'dash',
        colour: resolve(isMember ? 'var(--cyan)' : edgeColour(p.e.edgeType)),
        animate: !isMember,
      });
    } else {
      /* stops at the ring: a hop-2 line is not a claim of a direct edge */
      const dx = p.x - g.cx, dy = p.y - g.cy;
      const d = Math.hypot(dx, dy) || 1;
      lines.push({
        x1: p.x, y1: p.y,
        x2: g.cx + (dx / d) * g.R, y2: g.cy + (dy / d) * g.R,
        style: 'dot', colour: grey, animate: false,
      });
    }
  }
  const scene: Scene = { w, h: hgt, cx: g.cx, cy: g.cy, r: g.R, lines };
  stopPaint = animate(canvas, scene);

  /* ---- what the checks read --------------------------------------------- */
  ring = lay.placed.map((p) => ({
    id: p.e.id, hop: p.e.hop,
    x: Math.round(rect.left + p.x), y: Math.round(rect.top + p.y),
    labelled: true,
  }));
  centreOut = {
    id: hood.centre ? hood.centre.id : null,
    label: hood.centreLabel,
    x: Math.round(rect.left + g.cx),
    y: Math.round(rect.top + g.cy),
  };
}

function nodeEl(p: Placed, hood: Hood): HTMLElement {
  const e: Entry = p.e;
  const left = p.side < 0;
  const el = h('a', {
    class: 'hood-el hood-n hop' + e.hop + (left ? ' l' : ' r') +
      (e.derived ? ' derived' : '') + (e.edgeType === 'denial' ? ' denial' : ''),
    href: '#/n/' + e.id,
    style: 'left:' + p.x + 'px;top:' + p.y + 'px',
    title: e.full + ': ' + e.suffix,
  });
  const m = mark(clsColour(e.cls));
  const name = h('span', { class: 'hood-label' }, e.label);
  const suf = h('span', { class: suffixClass(e, hood) }, e.suffix);
  if (left) el.append(name, suf, m);
  else el.append(m, name, suf);
  return el;
}

function suffixClass(e: Entry, hood: Hood): string {
  if (e.hop !== 1) return 'hood-suffix faint';
  if (!hood.centre) return 'hood-suffix amber';
  if (e.edgeType === 'denial') return 'hood-suffix red';
  if (e.edgeType === 'custody' || e.edgeType === 'funding') return 'hood-suffix amber';
  return 'hood-suffix faint';
}

function buildLegend(el: HTMLElement): void {
  const item = (cls: string, text: string) =>
    h('span', { class: 'hood-leg' }, h('i', { class: 'sw ' + cls }), h('span', { class: 'dim' }, text));
  el.append(
    item('solid cyan', 'part of this node, not on the map itself'),
    item('dash cyan', 'a sourced link, coloured by kind'),
    item('dash red', 'a denial'),
    item('dash amber', 'custody or funding'),
    item('dot grey', 'two steps away, via a shared member'),
  );
}

/* IndexNode is used through Hood; naming it keeps the import honest. */
export type HoodCentre = IndexNode | null;

/* ---- the phone ------------------------------------------------------------ */
/* A ring of names needs room a phone does not have; what it would show is the
   node's neighbours and why each is there. So on a phone the neighbourhood is
   that list: every neighbour by name, grouped by relationship, each link with
   its own sentence where the record carries one. */
async function renderHoodPhone(view: HTMLElement, id: string | null, gen: number): Promise<void> {
  ring = [];
  if (!id) {
    const [flags, idx] = await Promise.all([loadHighlights().then((x) => x.flags), loadIndex()]);
    if (gen !== generation) return;
    setTitle('Neighbourhood');
    clear(view);
    const byId = new Map(idx.nodes.map((n) => [n.id, n]));
    const wrap = h('div', { class: 'hood-phone' });
    wrap.append(h('div', { class: 'hp-head' },
      h('span', { class: 'eyebrow' }, 'Neighbourhood'), ' ',
      h('span', { class: 'dim' }, '· nothing selected · pick a start-here node to open its neighbourhood')));
    const list = h('div', { class: 'hp-list' });
    for (const f of flags.slice().sort((a, b) => a.rank - b.rank)) {
      const n = byId.get(f.id);
      list.append(h('a', { class: 'hp-row', href: '#/n/' + f.id + '/hood' },
        mark(clsColour(n ? n.cls : '')), h('span', { class: 'hp-name' }, n ? n.label : f.id),
        h('span', { class: 'amber' }, 'start here ' + f.rank)));
    }
    wrap.append(list);
    view.append(wrap);
    return;
  }
  let rec;
  try { rec = await loadNode(id); } catch (e) {
    if (gen !== generation) return;
    notFound(view, '#/hood/' + id, "The neighbourhood needs this node's record: " + (e as Error).message);
    return;
  }
  if (gen !== generation) return;
  setTitle(rec.label, 'Neighbourhood');
  clear(view);
  const groups = groupConnections(rec.connections);
  const counterparts = new Set(rec.connections.map((c) => c.id)).size;
  const wrap = h('div', { class: 'hood-phone' });
  wrap.append(h('div', { class: 'hp-head' },
    h('span', { class: 'eyebrow' }, 'Neighbourhood'), ' ',
    h('a', { class: 'hp-who', href: '#/n/' + rec.id }, rec.label)));
  wrap.append(h('div', { class: 'dim' },
    counterparts + ' neighbours, linked ' + rec.connections.length + ' times, grouped by relationship. ' +
    'A wider screen draws them as a ring.'));
  wrap.append(h('div', { class: 'hp-ctl' },
    h('a', { class: 'hood-b', href: '#/n/' + rec.id }, 'NODE PAGE'),
    h('a', { class: 'hood-b', href: '#/n/' + rec.id + '/map' }, 'SHOW ON MAP')));
  wrap.append(renderConnGroups(groups));
  view.append(wrap);
}
