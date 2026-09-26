/* Places: redesign phase 11, task 3. #/places, the Places directory drawn as
 * the board's places on a plain longitude and latitude grid, beside a list of
 * every place grouped by country and region, each with its events and topics.
 *
 * There is no coastline and no basemap on purpose: none has been sourced, and a
 * downloaded one would be a sourcing claim nobody has checked. The coordinates
 * are the board's own table (research/_places.json), and the page says so. A
 * cited basemap and gazetteer are a research item (phase R).
 *
 * Every marker is named: its label sits beside it, at the one label size, or a
 * short way off with a leader where its neighbours are close. Labels are placed
 * by measuring them, so none overlaps another, a marker or a grid label, and
 * none is cut. A place without coordinates is
 * listed and says it has none; it is never placed by guesswork.
 */
import '../styles/directory.css';
import '../styles/places.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadPlaces, clsColour, type Place, type PlaceEvent } from '../data';
import { dirTabs } from './directory';

const NS = 'http://www.w3.org/2000/svg';
const MARGIN = 72;       /* each side of the grid: its latitudes, and room for names near its edge */

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
  root.append(h('p', { class: 'pl-note faint' },
    'The grid is plain longitude and latitude, with no coastline: no map of coastlines has been sourced for the board, ' +
    'so none is drawn. Every coordinate here comes from the board’s own table, typed in without a recorded source; ' +
    'each is marked "uncited" in the list. None has been checked against a cited gazetteer yet.'));

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
  /* the grid takes the width, less a margin each side that names near its
     edge can use; its height follows from the projection */
  const X0 = MARGIN, Y0 = 18;
  const plotW = Math.max(200, width - 2 * MARGIN);
  const plotH = Math.max(140, Math.round(plotW * (lat1 - lat0) / ((lon1 - lon0) * k)));
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

  /* the grid's own labels, outside the frame so nothing sits on them:
     latitudes in the left margin, longitudes under the frame, as many as fit */
  const every = (n: number, span: number, room: number) => Math.max(1, Math.ceil(room / (span / n)));
  const latK = every((lat1 - lat0) / step, plotH, 16);
  for (let i = 0, v = lat0; v <= lat1; v += step, i++) {
    if (i % latK) continue;
    stage.append(h('span', { class: 'pl-deg pl-deg-lat faint', style: 'left:' + (X0 - 6) + 'px;top:' + (py(v) - 6) + 'px' }, degLabel(v, 'N', 'S')));
  }
  const lonK = every((lon1 - lon0) / step, plotW, 58);
  for (let i = 0, v = lon0; v <= lon1; v += step, i++) {
    if (i % lonK) continue;
    stage.append(h('span', { class: 'pl-deg pl-deg-lon faint', style: 'left:' + px(v) + 'px;top:' + (Y0 + plotH + 3) + 'px' }, degLabel(v, 'E', 'W')));
  }

  /* markers first; then each name beside its own marker. A name tries the
     places nearest its marker first (right, left, above, below, then further
     out in every direction), and takes the first where it overlaps no other
     name, no marker and no grid label. A name set away from its marker gets a
     short leader. Nothing is shrunk or cut: a name that cannot sit close sits
     further out. */
  type Box = { x: number; y: number; w: number; h: number };
  const hit = (a: Box, b: Box) => a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
  const taken: Box[] = [];
  const names: Box[] = [];                        /* the names placed so far */
  const leads: [number, number, number, number][] = [];   /* and their leaders */
  /* does the segment (x1,y1)-(x2,y2) pass through box b? (Liang-Barsky) */
  const cuts = (x1: number, y1: number, x2: number, y2: number, b: Box) => {
    let t0 = 0, t1 = 1;
    const dx = x2 - x1, dy = y2 - y1;
    const edges: [number, number][] = [[-dx, x1 - b.x], [dx, b.x + b.w - x1], [-dy, y1 - b.y], [dy, b.y + b.h - y1]];
    for (const [pp, q] of edges) {
      if (pp === 0) { if (q < 0) return false; continue; }
      const r = q / pp;
      if (pp < 0) { if (r > t1) return false; if (r > t0) t0 = r; } else { if (r < t0) return false; if (r < t1) t1 = r; }
    }
    return t0 < t1;
  };
  const near = (b: Box, x: number, y: number): [number, number] =>
    [Math.max(b.x, Math.min(x, b.x + b.w)), Math.max(b.y, Math.min(y, b.y + b.h))];
  const sr = stage.getBoundingClientRect();
  for (const d of Array.from(stage.querySelectorAll('.pl-deg'))) {
    const r = d.getBoundingClientRect();
    taken.push({ x: r.left - sr.left - 2, y: r.top - sr.top - 1, w: r.width + 4, h: r.height + 2 });
  }
  const pts = places.map((p) => ({ p, x: px(p.lon as number), y: py(p.lat as number) }));
  for (const m of pts) {
    stage.append(h('a', {
      class: 'pl-mark', href: '#/n/' + m.p.id, 'data-id': m.p.id,
      style: 'left:' + m.x + 'px;top:' + m.y + 'px', 'aria-label': m.p.label,
      title: m.p.label + ': ' + fmtLat(m.p.lat as number) + ', ' + fmtLon(m.p.lon as number),
    }, mark(clsColour('location'))));
    taken.push({ x: m.x - 5, y: m.y - 5, w: 10, h: 10 });
  }
  /* the most crowded markers choose first, while there is still room near them */
  const crowd = (m: { x: number; y: number }) => pts.filter((o) => Math.hypot(o.x - m.x, o.y - m.y) < 80).length;
  const order = pts.slice().sort((a, b) => crowd(b) - crowd(a) || a.y - b.y || a.p.id.localeCompare(b.p.id));
  let bottom = Y0 + plotH + 22;
  const RINGS = [6, 16, 30, 48, 70, 96, 128, 166, 210, 260, 320, 390];
  const ANGLES = [0, 180, -90, 90, -30, 30, -150, 150, -60, 60, -120, 120];
  for (const m of order) {
    const el = h('a', {
      class: 'pl-label', href: '#/n/' + m.p.id, 'data-id': m.p.id,
      title: fmtLat(m.p.lat as number) + ', ' + fmtLon(m.p.lon as number) + ' (uncited: the board’s own table)',
    }, m.p.label);
    stage.append(el);
    const r = el.getBoundingClientRect();
    const w = Math.ceil(r.width), hh = Math.ceil(r.height);
    /* every free spot within reach is scored: its distance, plus a price for a
       leader crossing a name or a name sitting on a leader. The cheapest wins,
       so a name moves far only when every near spot is taken. */
    let best: Box | null = null, dist = 0, score = Infinity;
    for (const d of RINGS) {
      if (d > score) break;
      for (const a of ANGLES) {
        const c = Math.cos(a * Math.PI / 180), s = Math.sin(a * Math.PI / 180);
        /* the box's near edge sits d from the marker along the angle */
        const bx = m.x + d * c - (c < -0.3 ? w : c > 0.3 ? 0 : w / 2);
        const by = m.y + d * s - (s < -0.3 ? hh : s > 0.3 ? 0 : hh / 2);
        const b = { x: Math.round(bx), y: Math.round(by), w, h: hh };
        if (b.x < 0 || b.x + w > width || b.y < 0) continue;
        if (taken.some((t) => hit(t, { x: b.x - 2, y: b.y - 1, w: b.w + 4, h: b.h + 2 }))) continue;
        let sc = d;
        if (d > 10) {
          const [tx, ty] = near(b, m.x, m.y);
          sc += 120 * names.filter((t) => cuts(m.x, m.y, tx, ty, t)).length;
        }
        sc += 120 * leads.filter(([a1, b1, a2, b2]) => cuts(a1, b1, a2, b2, { x: b.x - 1, y: b.y - 1, w: b.w + 2, h: b.h + 2 })).length;
        if (sc < score) { score = sc; best = b; dist = d; }
      }
    }
    if (!best) {
      /* nowhere near: under everything else, in a row of its own */
      best = { x: Math.max(0, Math.min(width - w, Math.round(m.x - w / 2))), y: Math.round(bottom), w, h: hh };
      dist = 999;
    }
    el.style.left = best.x + 'px';
    el.style.top = best.y + 'px';
    taken.push(best);
    names.push(best);
    bottom = Math.max(bottom, best.y + hh + 4);
    if (dist > 10) {
      const [tx, ty] = near(best, m.x, m.y);
      leads.push([m.x, m.y, tx, ty]);
      line('M' + m.x + ' ' + m.y + ' L' + tx + ' ' + ty, 'pl-lead');
    }
  }
  const H = Math.ceil(Math.max(bottom, Y0 + plotH + 22) + 4);
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
    p.lat != null && p.lon != null ? fmtLat(p.lat) + ', ' + fmtLon(p.lon) + (p.coordSource === 'board table' ? ' · uncited' : '')
      : 'no coordinates on the board'));
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
