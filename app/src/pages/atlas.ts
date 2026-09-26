/* The Atlas: redesign section 5, "Atlas", and phase 6 task 2.
 *
 *   #/atlas
 *
 * Sections are rows and the four eras of index.json are columns. One chip per
 * topic, in its section and in the era its story centres on (`focusEra`),
 * ordered by date. A topic whose span runs into other eras carries a thin line
 * across them to the year it reaches, named at its end ("to 1997"), so no mark
 * is drawn without words. The chip is the same height for every topic: the
 * height of the longest title at this width, so a label is wrapped onto more
 * lines rather than cut, and a crowded cell grows taller rather than spill.
 * Nothing about a chip's size says anything about the topic.
 *
 * At rest there are no lines between topics. Focusing a chip, by mouse or by
 * keyboard, draws its links to the topics its record names as related, with
 * the animated directional line of the program map.
 *
 * Filters: kind, contested (the topic has contested items), has open
 * questions. A filtered-out chip stays where it is, faded, so the grid never
 * jumps under the reader.
 *
 * At phone width (760 or less) the Atlas is the same topics as stacked lists,
 * one per section.
 *
 * app/checks/run.mjs C37 holds all of this to topics.json.
 */
import '../styles/atlas.css';
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadTopics, spanText, type TopicRow, type TopicsFile, type Era } from '../data';
import { TOPIC_KINDS } from '../vocab';

const PHONE = 760;
const PAD = 6;          /* a cell's inner margin; the link channels run in it */
const GAP = 4;          /* between lanes */
const LH = 15;          /* the label's line height at 11px */
const CHIP_PX = 7;      /* a chip's inner horizontal padding */
const CHIP_PY = 4;

interface Filters { kind: string; contested: boolean; questions: boolean; }

const year = (s: string | null | undefined): number | null => {
  const m = String(s || '').match(/\d{4}/);
  return m ? Number(m[0]) : null;
};

let state: Filters = { kind: '', contested: false, questions: false };
let resizeHook: (() => void) | null = null;

export async function renderAtlas(view: HTMLElement): Promise<void> {
  setTitle('Atlas');
  clear(view);
  const [tf, idx] = await Promise.all([loadTopics(), loadIndex()]);
  const eras = idx.eras.filter((e) => e.start != null || e.end != null).slice(0, 4);
  state = { kind: '', contested: false, questions: false };

  const root = h('div', { class: 'atlas' });
  view.append(root);
  root.append(h('div', { class: 'atlas-top' },
    h('h1', { class: 'atlas-h1' }, 'Atlas'),
    h('p', { class: 'atlas-intro' },
      'The board\'s ' + tf.topics.length + ' topics in ' + tf.sections.length + ' sections. Each topic sits in its ' +
      'section (the rows) and in the era its story centres on (the columns). A thin line carries a topic ' +
      'across the years it runs to. Point at a topic, or tab to it, to draw its links to related topics; ' +
      'open it to read what the record shows, what is claimed and what is contested.'),
  ));

  const count = h('span', { class: 'af-count dim' });
  const kinds = TOPIC_KINDS.filter((k) => tf.topics.some((t) => t.kind === k.id));
  const sel = h('select', { class: 'af-kind', 'aria-label': 'Filter by kind' },
    h('option', { value: '' }, 'every kind'),
    ...kinds.map((k) => h('option', { value: k.id },
      k.id + ' (' + tf.topics.filter((t) => t.kind === k.id).length + ')')));
  const btn = (cls: string, label: string, key: 'contested' | 'questions') => {
    const b = h('button', { type: 'button', class: 'af-btn ' + cls, 'aria-pressed': 'false' }, label);
    b.addEventListener('click', () => {
      state[key] = !state[key];
      b.setAttribute('aria-pressed', state[key] ? 'true' : 'false');
      apply();
    });
    return b;
  };
  sel.addEventListener('change', () => { state.kind = (sel as HTMLSelectElement).value; apply(); });
  root.append(h('div', { class: 'atlas-filters' },
    h('span', { class: 'eyebrow' }, 'Show'), sel,
    btn('af-contested', 'contested', 'contested'),
    btn('af-questions', 'with open questions', 'questions'),
    count,
  ));

  const body = h('div', { class: 'atlas-body' });
  root.append(body);

  const draw = () => {
    clear(body);
    if (window.innerWidth <= PHONE) drawList(body, tf);
    else drawGrid(body, tf, eras);
    apply();
  };
  const apply = () => {
    let shown = 0;
    for (const el of body.querySelectorAll<HTMLElement>('[data-id]')) {
      const t = tf.topics.find((x) => x.id === el.getAttribute('data-id'));
      const on = !!t && passes(t);
      el.setAttribute('data-off', on ? '0' : '1');
      if (on && el.classList.contains('atlas-chip')) shown++;
      if (on && el.classList.contains('atlas-li')) shown++;
    }
    count.textContent = 'showing ' + shown + ' of ' + tf.topics.length;
  };

  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  draw();

  let wasPhone = window.innerWidth <= PHONE;
  let lastW = window.innerWidth;
  let timer = 0;
  if (resizeHook) window.removeEventListener('resize', resizeHook);
  resizeHook = () => {
    if (!document.body.contains(root)) { window.removeEventListener('resize', resizeHook!); resizeHook = null; return; }
    window.clearTimeout(timer);
    timer = window.setTimeout(() => {
      const phone = window.innerWidth <= PHONE;
      if (phone !== wasPhone || Math.abs(window.innerWidth - lastW) > 4) { wasPhone = phone; lastW = window.innerWidth; draw(); }
    }, 150);
  };
  window.addEventListener('resize', resizeHook);
}

function passes(t: TopicRow): boolean {
  if (state.kind && t.kind !== state.kind) return false;
  if (state.contested && !(t.counts.contested > 0)) return false;
  if (state.questions && !(t.counts.questions > 0)) return false;
  return true;
}

function sortTopics(xs: TopicRow[]): TopicRow[] {
  return xs.slice().sort((a, b) =>
    Number(a.focusEra) - Number(b.focusEra) ||
    (year(a.span && a.span.from) ?? 9999) - (year(b.span && b.span.from) ?? 9999) ||
    a.title.localeCompare(b.title));
}

/* ---- phone: stacked lists ------------------------------------------------ */
function drawList(host: HTMLElement, tf: TopicsFile): void {
  const wrap = h('div', { class: 'atlas-list' });
  for (const s of tf.sections) {
    const ts = sortTopics(tf.topics.filter((t) => t.section === s.id));
    const sec = h('section', { class: 'al-sec' },
      h('h2', { class: 'al-head' }, s.title, ' ', h('span', { class: 'faint' }, String(ts.length))));
    const ol = h('div', { class: 'al-items' });
    for (const t of ts) {
      ol.append(h('a', { class: 'atlas-li', href: '#/topic/' + t.id, 'data-id': t.id },
        h('span', { class: 'al-title' }, t.title),
        h('span', { class: 'al-meta dim' }, t.kind + ' · ' + spanText(t.span) +
          (t.researchGap ? ' · research gap' : ''))));
    }
    sec.append(ol);
    wrap.append(sec);
  }
  host.append(wrap);
}

/* ---- the grid ------------------------------------------------------------- */
function drawGrid(host: HTMLElement, tf: TopicsFile, eras: Era[]): void {
  const W = Math.floor(host.getBoundingClientRect().width);
  const G = Math.round(Math.max(128, Math.min(190, W * 0.1)));
  const cw = (W - G) / eras.length;
  const chipW = cw - 2 * PAD;

  /* measure every title at the chip's width: the tallest sets the one height */
  const meas = h('div', { class: 'atlas-label atlas-meas' });
  meas.style.width = (chipW - 2 * CHIP_PX - 2) + 'px';
  host.append(meas);
  let lines = 1;
  for (const t of tf.topics) {
    meas.textContent = t.title;
    lines = Math.max(lines, Math.round(meas.getBoundingClientRect().height / LH));
  }
  const secMeas = h('div', { class: 'atlas-sec-title atlas-meas' });
  secMeas.style.width = (G - 14) + 'px';
  host.append(secMeas);
  const CH = lines * LH + 2 * CHIP_PY + 2;

  /* years to x, inside each era's column */
  const allFrom = tf.topics.map((t) => year(t.span && t.span.from)).filter((y): y is number => y != null);
  const allTo = tf.topics.map((t) => year(t.span && (t.span.to || t.span.from))).filter((y): y is number => y != null);
  const lo = Math.min(...allFrom, 1940), hi = Math.max(...allTo, 2026);
  const eraStart = (i: number) => (eras[i].start ?? lo);
  const eraEnd = (i: number) => Math.min(eras[i].end ?? hi, i === eras.length - 1 ? hi : 1e9);
  const eraOf = (y: number) => { for (let i = 0; i < eras.length; i++) if (y <= eraEnd(i)) return i; return eras.length - 1; };
  const xOf = (y: number) => {
    const i = eraOf(y);
    const a = eraStart(i), b = eraEnd(i);
    const f = Math.max(0, Math.min(1, (y - a + 0.5) / (b - a + 1)));
    return G + i * cw + PAD + f * chipW;
  };

  /* era heads, sticky under the bar */
  const head = h('div', { class: 'atlas-head' });
  head.style.gridTemplateColumns = G + 'px repeat(' + eras.length + ', ' + cw + 'px)';
  head.append(h('div', { class: 'ah-corner faint' }, 'section / era'));
  for (const e of eras) head.append(h('div', { class: 'ah-era' }, h('span', { class: 'ah-label' }, e.label), ' ', h('span', { class: 'faint' }, e.sub)));
  host.append(head);

  const grid = h('div', { class: 'atlas-grid' });
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'atlas-links');
  svg.setAttribute('aria-hidden', 'true');
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  marker.setAttribute('id', 'atlas-arrow');
  marker.setAttribute('viewBox', '0 0 8 8');
  marker.setAttribute('refX', '7'); marker.setAttribute('refY', '4');
  marker.setAttribute('markerWidth', '7'); marker.setAttribute('markerHeight', '7');
  marker.setAttribute('orient', 'auto');
  const tip = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  tip.setAttribute('d', 'M0,0 L8,4 L0,8 z');
  tip.setAttribute('class', 'atlas-arrow');
  marker.append(tip); defs.append(marker); svg.append(defs);
  const linkLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  svg.append(linkLayer);

  const boxes = new Map<string, { x: number; y: number; w: number; h: number; era: number }>();
  let top = 0;
  for (const s of tf.sections) {
    const ts = sortTopics(tf.topics.filter((t) => t.section === s.id));
    /* lanes: a topic holds its lane across every era its span touches */
    const laneEnd: number[] = [];
    const placed: { t: TopicRow; lane: number; f: number; s: number; e: number }[] = [];
    for (const t of ts) {
      const f = Number(t.focusEra);
      const yf = year(t.span && t.span.from), yt = year(t.span && (t.span.to || t.span.from));
      const s0 = Math.min(f, yf == null ? f : eraOf(yf));
      const e0 = Math.max(f, yt == null ? f : eraOf(yt));
      let lane = laneEnd.findIndex((end) => end < s0);
      if (lane < 0) { lane = laneEnd.length; laneEnd.push(e0); } else laneEnd[lane] = e0;
      placed.push({ t, lane, f, s: s0, e: e0 });
    }
    secMeas.textContent = s.title;
    const secH = secMeas.getBoundingClientRect().height + LH + 2 * PAD;
    const rowH = Math.max(laneEnd.length * (CH + GAP) - GAP + 2 * PAD, secH);

    grid.append(h('div', {
      class: 'atlas-sec', style: `left:0;top:${top}px;width:${G}px;height:${rowH}px`,
    }, h('div', { class: 'atlas-sec-title' }, s.title),
      h('div', { class: 'faint' }, ts.length + (ts.length === 1 ? ' topic' : ' topics'))));
    eras.forEach((e, i) => {
      grid.append(h('div', {
        class: 'atlas-cell', 'data-section': s.id, 'data-era': e.id,
        style: `left:${G + i * cw}px;top:${top}px;width:${cw}px;height:${rowH}px`,
      }));
    });

    for (const p of placed) {
      const x = G + p.f * cw + PAD, y = top + PAD + p.lane * (CH + GAP);
      const t = p.t;
      boxes.set(t.id, { x, y, w: chipW, h: CH, era: p.f });
      const mid = y + CH / 2;
      /* the tail: the years the topic runs on, named at its end */
      const yt = year(t.span && (t.span.to || t.span.from));
      const yf = year(t.span && t.span.from);
      if (p.e > p.f && yt != null) {
        const x2 = xOf(yt);
        grid.append(h('div', { class: 'atlas-tail', 'data-for': t.id, style: `left:${x + chipW}px;top:${mid}px;width:${Math.max(2, x2 - x - chipW)}px` }));
        tailLabel(grid, t.id, 'to ' + yt, x2, mid, G + (p.e + 1) * cw - 2, G + p.e * cw + 2, 'end');
      }
      if (p.s < p.f && yf != null) {
        const x1 = xOf(yf);
        grid.append(h('div', { class: 'atlas-tail', 'data-for': t.id, style: `left:${x1}px;top:${mid}px;width:${Math.max(2, x - x1)}px` }));
        tailLabel(grid, t.id, 'from ' + yf, x1, mid, G + (p.s + 1) * cw - 2, G + p.s * cw + 2, 'start');
      }
      const chip = h('a', {
        class: 'atlas-chip' + (t.researchGap ? ' gap' : ''), href: '#/topic/' + t.id,
        'data-id': t.id, 'data-section': s.id, 'data-era': String(p.f),
        title: (t.lead || t.title) + ' (' + t.kind + ', ' + spanText(t.span) + ')',
        style: `left:${x}px;top:${y}px;width:${chipW}px;height:${CH}px`,
      }, h('span', { class: 'atlas-label' }, t.title));
      grid.append(chip);
    }
    top += rowH;
  }
  meas.remove(); secMeas.remove();
  grid.style.height = top + 'px';
  svg.setAttribute('width', String(W));
  svg.setAttribute('height', String(top));
  grid.prepend(svg);
  host.append(grid);

  /* focus: draw this chip's related-topic links, and only on focus */
  const byId = new Map(tf.topics.map((t) => [t.id, t]));
  const show = (id: string) => {
    clearLinks();
    const t = byId.get(id), a = boxes.get(id);
    if (!t || !a) return;
    grid.classList.add('focusing');
    grid.querySelector(`a.atlas-chip[data-id="${id}"]`)?.classList.add('focus');
    for (const r of t.related || []) {
      const b = boxes.get(r);
      if (!b) continue;
      grid.querySelector(`a.atlas-chip[data-id="${r}"]`)?.classList.add('rel');
      const sy = a.y + a.h / 2, ty = b.y + b.h / 2;
      let d: string;
      if (b.era === a.era) {
        const sx = a.x + a.w, tx = b.x + b.w, mx = a.x + a.w + PAD - 2;
        d = `M${sx},${sy} H${mx} V${ty} H${tx + 1}`;
      } else if (b.era > a.era) {
        const sx = a.x + a.w, tx = b.x, mx = b.x - PAD + 2;
        d = `M${sx},${sy} H${mx} V${ty} H${tx - 1}`;
      } else {
        const sx = a.x, tx = b.x + b.w, mx = b.x + b.w + PAD - 2;
        d = `M${sx},${sy} H${mx} V${ty} H${tx + 1}`;
      }
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', d);
      path.setAttribute('class', 'atlas-link');
      path.setAttribute('data-to', r);
      path.setAttribute('marker-end', 'url(#atlas-arrow)');
      linkLayer.append(path);
    }
  };
  const clearLinks = () => {
    while (linkLayer.firstChild) linkLayer.removeChild(linkLayer.firstChild);
    grid.classList.remove('focusing');
    for (const c of grid.querySelectorAll('a.atlas-chip.focus, a.atlas-chip.rel')) c.classList.remove('focus', 'rel');
  };
  for (const c of grid.querySelectorAll<HTMLElement>('a.atlas-chip')) {
    const id = c.getAttribute('data-id') || '';
    c.addEventListener('mouseenter', () => show(id));
    c.addEventListener('mouseleave', () => { if (document.activeElement !== c) clearLinks(); });
    c.addEventListener('focus', () => show(id));
    c.addEventListener('blur', () => clearLinks());
  }
}

/* A tail's words, at its end: outside the line where the era column has room,
   otherwise just above the line, inside it. */
function tailLabel(grid: HTMLElement, id: string, text: string, x: number, mid: number,
  colRight: number, colLeft: number, side: 'end' | 'start'): void {
  const w = text.length * 6.6 + 2;
  let left: number, top = mid - 8;
  if (side === 'end') {
    if (x + 5 + w <= colRight) left = x + 5;
    else { left = x - w; top = mid - LH - 1; }
  } else {
    if (x - 5 - w >= colLeft) left = x - 5 - w;
    else { left = x; top = mid - LH - 1; }
  }
  grid.append(h('span', { class: 'atlas-tail-label', 'data-for': id, style: `left:${left}px;top:${top}px` }, text));
}
