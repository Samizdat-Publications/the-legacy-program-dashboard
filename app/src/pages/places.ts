/* Places: redesign phase 11, task 3. #/places, the Places directory drawn as
 * the board's places on a plain longitude and latitude grid, beside a list of
 * every place grouped by country and region, each with its events and topics.
 *
 * There is no coastline and no basemap on purpose: none has been sourced, and a
 * downloaded one would be a sourcing claim nobody has checked. The coordinates
 * are the board's own table (research/_places.json), and the page says so. A
 * cited basemap and gazetteer are a research item (phase R).
 *
 * Every marker is named: each has its label in a column beside the grid, joined
 * to it by a leader line, at the one label size. Labels are placed by measuring
 * them, so none overlaps another and none is cut. A place without coordinates is
 * listed and says it has none; it is never placed by guesswork.
 */
import '../styles/directory.css';
import '../styles/places.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadPlaces, clsColour, type Place, type PlaceEvent } from '../data';
import { dirTabs } from './directory';

const NS = 'http://www.w3.org/2000/svg';
const COL_W = 200;        /* each label column */
const GAP = 14;           /* between a label column and the grid */
const LAB_GAP = 3;        /* between two labels in a column */

let generation = 0;
let observer: ResizeObserver | null = null;

export async function renderPlaces(view: HTMLElement): Promise<void> {
  const gen = ++generation;
  if (observer) { observer.disconnect(); observer = null; }
  clear(view);
  setTitle('Places');
  let idx, pf;
  try {
    [idx, pf] = await Promise.all([loadIndex(), loadPlaces()]);
  } catch (e) {
    view.append(h('section', { class: 'notice' },
      h('h2', null, 'The places data is not being served'), h('p', null, (e as Error).message)));
    return;
  }
  if (gen !== generation) return;
  const places = pf.places;
  const plotted = places.filter((p) => p.lat != null && p.lon != null);
  const us = plotted.filter((p) => p.country === 'USA');
  const abroad = plotted.filter((p) => p.country !== 'USA');

  const root = h('div', { class: 'dir pl', 'data-dir': 'places' });
  root.append(h('div', { class: 'dir-top' },
    h('div', { class: 'eyebrow' }, 'Directories'),
    h('h1', { class: 'dir-h1' }, 'Places'),
    h('p', { class: 'dir-blurb dim' },
      'Every place on the board: ' + places.length + ', of which ' + plotted.length +
      ' carry coordinates and are plotted. Each is listed by country and region with the events tied to it and the topics that hold it.'),
    dirTabs(idx.nodes, 'places')));
  const sources = Object.entries(pf.coordSources || {});
  root.append(h('p', { class: 'pl-note faint' },
    'The grid is plain longitude and latitude, with no coastline: no basemap has been sourced for the board. ',
    ...sources.map(([k, v]) => h('span', null, 'Coordinates marked "' + k + '": ' + v + ' '))));

  const body = h('div', { class: 'pl-body' });
  const plots = h('section', { class: 'pl-plots', 'aria-label': 'The places on a longitude and latitude grid' });
  const list = h('section', { class: 'pl-list', 'aria-label': 'Every place, by country and region' });
  body.append(plots, list);
  root.append(body);
  view.append(root);

  plots.append(h('p', { class: 'pl-phone dim' },
    'The grid needs a wider screen. Every place is in the list below, with its coordinates where the board has them.'));
  const blocks: { el: HTMLElement; places: Place[]; step: number }[] = [];
  if (us.length) blocks.push({ el: plotBlock('us', 'The United States', us.length), places: us, step: 5 });
  if (abroad.length) blocks.push({ el: plotBlock('abroad', 'Outside the United States', abroad.length), places: abroad, step: 20 });
  for (const b of blocks) plots.append(b.el);

  list.append(placeList(places));

  const draw = () => { if (gen === generation) for (const b of blocks) drawPlot(b.el, b.places, b.step); };
  draw();
  observer = new ResizeObserver(() => draw());
  observer.observe(plots);
  if (document.fonts && document.fonts.ready) void document.fonts.ready.then(draw);
}

function plotBlock(id: string, title: string, n: number): HTMLElement {
  return h('div', { class: 'pl-plot', 'data-plot': id },
    h('div', { class: 'eyebrow pl-plot-head' }, title + ' · ' + n + ' plotted'),
    h('div', { class: 'pl-stage' }));
}

const fmtLat = (v: number) => Math.abs(v).toFixed(2) + '° ' + (v >= 0 ? 'N' : 'S');
const fmtLon = (v: number) => Math.abs(v).toFixed(2) + '° ' + (v >= 0 ? 'E' : 'W');
const degLabel = (v: number, pos: string, neg: string) => Math.abs(v) + '°' + (v === 0 ? '' : ' ' + (v > 0 ? pos : neg));

function drawPlot(block: HTMLElement, places: Place[], step: number): void {
  const stage = block.querySelector('.pl-stage') as HTMLElement;
  clear(stage);
  const width = Math.floor(stage.getBoundingClientRect().width);
  if (width < 400) return;                        /* a phone: the list carries it */

  /* the extent: the places' own bounds, padded and snapped to the grid step */
  const lats = places.map((p) => p.lat as number), lons = places.map((p) => p.lon as number);
  const lat0 = Math.floor((Math.min(...lats) - step / 4) / step) * step;
  const lat1 = Math.ceil((Math.max(...lats) + step / 4) / step) * step;
  const lon0 = Math.floor((Math.min(...lons) - step / 4) / step) * step;
  const lon1 = Math.ceil((Math.max(...lons) + step / 4) / step) * step;
  const k = Math.cos(((lat0 + lat1) / 2) * Math.PI / 180);
  const plotW = Math.max(160, width - 2 * (COL_W + GAP));
  const plotH = Math.max(120, Math.round(plotW * (lat1 - lat0) / ((lon1 - lon0) * k)));
  const X0 = COL_W + GAP, Y0 = 18;
  const px = (lon: number) => X0 + (lon - lon0) / (lon1 - lon0) * plotW;
  const py = (lat: number) => Y0 + (lat1 - lat) / (lat1 - lat0) * plotH;

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'pl-svg');
  svg.setAttribute('aria-hidden', 'true');
  stage.append(svg);
  const line = (d: string, cls: string) => {
    const p = document.createElementNS(NS, 'path');
    p.setAttribute('d', d); p.setAttribute('class', cls);
    svg.appendChild(p);
  };
  line('M' + X0 + ' ' + Y0 + ' h' + plotW + ' v' + plotH + ' h' + (-plotW) + ' Z', 'pl-frame');
  for (let v = lat0 + step; v < lat1; v += step) line('M' + X0 + ' ' + py(v) + ' h' + plotW, 'pl-grat');
  for (let v = lon0 + step; v < lon1; v += step) line('M' + px(v) + ' ' + Y0 + ' v' + plotH, 'pl-grat');
  /* the grid's own labels: latitudes above their line at the grid's left edge,
     longitudes under the frame */
  for (let v = lat0; v <= lat1; v += step) {
    stage.append(h('span', { class: 'pl-deg faint', style: 'left:' + (X0 + 3) + 'px;top:' + (py(v) - 14) + 'px' }, degLabel(v, 'N', 'S')));
  }
  for (let v = lon0; v <= lon1; v += step) {
    stage.append(h('span', { class: 'pl-deg pl-deg-lon faint', style: 'left:' + px(v) + 'px;top:' + (Y0 + plotH + 3) + 'px' }, degLabel(v, 'E', 'W')));
  }

  /* markers, then their labels in two columns, then the leaders */
  type Lab = { p: Place; x: number; y: number; el: HTMLElement; side: -1 | 1; top: number; h: number };
  const labs: Lab[] = [];
  for (const p of places) {
    const x = px(p.lon as number), y = py(p.lat as number);
    stage.append(h('a', {
      class: 'pl-mark', href: '#/n/' + p.id, 'data-id': p.id,
      'data-lat': String(p.lat), 'data-lon': String(p.lon),
      style: 'left:' + x + 'px;top:' + y + 'px', 'aria-label': p.label,
      title: p.label + ': ' + fmtLat(p.lat as number) + ', ' + fmtLon(p.lon as number),
    }, mark(clsColour('location'))));
    const side: -1 | 1 = x < X0 + plotW / 2 ? -1 : 1;
    const el = h('a', {
      class: 'pl-label ' + (side < 0 ? 'l' : 'r'), href: '#/n/' + p.id, 'data-id': p.id,
      style: 'width:' + COL_W + 'px;left:' + (side < 0 ? 0 : X0 + plotW + GAP) + 'px;top:0px',
      title: fmtLat(p.lat as number) + ', ' + fmtLon(p.lon as number) + ' (coordinates: ' + (p.coordSource || 'source not recorded') + ')',
    }, p.label);
    stage.append(el);
    labs.push({ p, x, y, el, side, top: 0, h: 0 });
  }
  let bottom = Y0 + plotH + 20;
  for (const side of [-1, 1] as const) {
    const col = labs.filter((l) => l.side === side).sort((a, b) => a.y - b.y || a.p.label.localeCompare(b.p.label));
    let next = Y0;
    for (const l of col) {
      l.h = l.el.getBoundingClientRect().height;
      l.top = Math.max(next, Math.round(l.y - l.h / 2));
      next = l.top + l.h + LAB_GAP;
    }
    /* a column that ran past the grid is pulled back up where it has room */
    let limit = Math.max(next, Y0 + plotH) - LAB_GAP;
    for (let i = col.length - 1; i >= 0; i--) {
      const l = col[i];
      if (l.top + l.h > limit) l.top = Math.max(Y0, limit - l.h);
      limit = l.top - LAB_GAP;
    }
    for (const l of col) {
      l.el.style.top = l.top + 'px';
      bottom = Math.max(bottom, l.top + l.h + 4);
      const ax = l.side < 0 ? COL_W + 2 : X0 + plotW + GAP - 2;
      line('M' + l.x + ' ' + l.y + ' L' + ax + ' ' + (l.top + Math.min(l.h, 14) / 2), 'pl-lead');
    }
  }
  const H = Math.ceil(bottom + 4);
  stage.style.height = H + 'px';
  svg.setAttribute('width', String(width));
  svg.setAttribute('height', String(H));
  svg.setAttribute('viewBox', '0 0 ' + width + ' ' + H);
}

function placeList(places: Place[]): HTMLElement {
  const NOWHERE = 'Not located on the board';
  const byCountry = new Map<string, Place[]>();
  for (const p of places) {
    const c = p.country || NOWHERE;
    if (!byCountry.has(c)) byCountry.set(c, []);
    byCountry.get(c)!.push(p);
  }
  const countries = [...byCountry.keys()].sort((a, b) =>
    (a === NOWHERE ? 1 : 0) - (b === NOWHERE ? 1 : 0) || byCountry.get(b)!.length - byCountry.get(a)!.length || a.localeCompare(b));
  const wrap = h('div', { class: 'pl-groups' });
  for (const c of countries) {
    const ps = byCountry.get(c)!;
    const g = h('section', { class: 'pl-country', 'data-country': c });
    g.append(h('h2', { class: 'pl-chead' }, h('span', { class: 'eyebrow' }, c), h('span', { class: 'dim' }, ' · ' + ps.length)));
    if (c === NOWHERE) {
      g.append(h('p', { class: 'faint pl-cnote' },
        'The board carries no coordinates and no country for these. They are not placed on the grid.'));
    }
    const byRegion = new Map<string, Place[]>();
    for (const p of ps) {
      const r = p.region || '';
      if (!byRegion.has(r)) byRegion.set(r, []);
      byRegion.get(r)!.push(p);
    }
    const regions = [...byRegion.keys()].sort((a, b) => (a === '' ? 1 : 0) - (b === '' ? 1 : 0) || a.localeCompare(b));
    for (const r of regions) {
      const rows = byRegion.get(r)!.sort((a, b) => a.label.localeCompare(b.label));
      if (r) g.append(h('h3', { class: 'pl-rhead dim' }, r));
      const ul = h('ul', { class: 'pl-rows' });
      for (const p of rows) ul.append(placeRow(p));
      g.append(ul);
    }
    wrap.append(g);
  }
  return wrap;
}

function evLink(e: PlaceEvent, place: string): HTMLElement {
  const when = e.date ? String(e.date).slice(0, 10) : 'no date';
  return h('li', null, h('span', { class: 'faint' }, when + ' '),
    e.kind === 'node'
      ? h('a', { href: '#/n/' + e.id }, e.label)
      : h('a', { href: '#/timeline?scope=n:' + place }, e.label));
}

function placeRow(p: Place): HTMLElement {
  const li = h('li', { class: 'pl-row', 'data-id': p.id, 'data-country': p.country || '' });
  li.append(h('a', { class: 'pl-name', href: '#/n/' + p.id }, mark(clsColour('location')), h('span', null, p.label)));
  li.append(h('span', { class: 'pl-coord ' + (p.lat != null ? 'dim' : 'faint') },
    p.lat != null && p.lon != null ? fmtLat(p.lat) + ', ' + fmtLon(p.lon) : 'no coordinates on the board'));
  if (p.events.length) {
    const ul = h('ul', { class: 'pl-evs' });
    for (const e of p.events) ul.append(evLink(e, p.id));
    if (p.events.length > 4) {
      li.append(h('details', { class: 'pl-more' }, h('summary', null, p.events.length + ' events'), ul));
    } else {
      li.append(h('div', { class: 'pl-sub' }, h('span', { class: 'eyebrow' }, 'Events'), ul));
    }
  }
  if (p.topics.length) {
    const t = h('div', { class: 'pl-sub' }, h('span', { class: 'eyebrow' }, 'Topics'));
    const ul = h('ul', { class: 'pl-tops' });
    for (const x of p.topics) ul.append(h('li', null, h('a', { href: '#/topic/' + x.id }, x.title)));
    t.append(ul);
    li.append(t);
  }
  return li;
}
