/* Timeline — Design response section 1.7, routes #/timeline, ?era=, ?scope=.
 *
 * Four strand lanes (the board's own `strand` values) by five era columns (the
 * eras of index.json). A closed era shows one count per lane and opens on click.
 * The open era shows year gridlines and its events as 11px chips packed into
 * rows so that no two overlap; an event that cannot be placed at 11px is a 5px
 * mark until its year is opened, and a year opens on click.
 *
 * Scope chips ALL / NODE / THREAD are drawn when the route carries an id.
 *
 * Nothing here is written: every string is an event's own label, an era's own
 * label, or a count. The page publishes window.__app.timeline.placed(), which
 * measures the rendered DOM rather than reporting what the layout intended.
 */
import '../styles/timeline.css';
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex, clsColour, type IndexNode } from '../data';
import { loadThreads, threadById } from '../thread/data';
import { loadTimeline } from '../timeline/source';
import {
  lanes, packLane, eraYears, yearSlots, textWidth,
  CHIP_H, ROW_PITCH, MARK_W, MARK_H,
  type TEvent, type EraDef, type LaneLayout, type YearSlot,
} from '../timeline/layout';

const CLOSED_COL = 132;          /* px per closed era column                  */
const LANE_LABEL_COL = 168;      /* px of the strand-name column              */
const OPEN_YEAR_WEIGHT = 6;      /* an opened year against a closed one       */

/* Years the reader has opened, kept per era. Not in the URL: section 2.1
   defines ?era= and ?scope= for this route and nothing else, and inventing a
   third parameter would put a route in the page that 2.1 does not carry. */
const openYears = new Map<string, Set<number>>();

interface Ctx {
  view: HTMLElement;
  events: TEvent[];        /* after scope filtering */
  all: TEvent[];           /* every event, for the header count */
  eras: EraDef[];
  byId: Map<string, IndexNode>;
  eraId: string;
  scope: string | null;
  scopeLabel: string | null;
}

export async function renderTimeline(
  view: HTMLElement, era: string | null, scope: string | null,
): Promise<void> {
  clear(view);
  setTitle('Timeline');

  const [idx, all] = await Promise.all([loadIndex(), loadTimeline()]);
  const byId = new Map<string, IndexNode>();
  for (const n of idx.nodes) byId.set(n.id, n);

  /* ---- scope ----------------------------------------------------------- */
  let events = all;
  let scopeLabel: string | null = null;
  let scopeBad: string | null = null;
  if (scope && scope.indexOf('n:') === 0) {
    const id = scope.slice(2);
    const n = byId.get(id);
    if (!n) scopeBad = 'No node with the id ' + id + ' is on the board.';
    else {
      scopeLabel = n.label;
      events = all.filter((e) => e.node === id);
    }
  } else if (scope && scope.indexOf('t:') === 0) {
    const id = scope.slice(2);
    const tf = await loadThreads();
    const th = threadById(tf, id);
    if (!th) scopeBad = 'No thread with the id ' + id + ' is authored.';
    else {
      scopeLabel = th.label;
      const ids = new Set(th.steps.map((s) => s.node));
      events = all.filter((e) => !!e.node && ids.has(e.node));
    }
  } else if (scope) {
    scopeBad = 'A scope is n:<node id> or t:<thread id>. This route carries ' + scope + '.';
  }

  const eras = idx.eras as EraDef[];

  /* Which era is open. The route wins; with no era in the route the era
     carrying the most events in the current scope opens, so the page never
     opens on an empty column. */
  let eraId = '';
  if (era && eras.some((x) => x.id === era)) eraId = era;
  else {
    let best = -1;
    for (const e of eras) {
      const n = events.filter((x) => x.era === e.id).length;
      if (n > best) { best = n; eraId = e.id; }
    }
  }

  const ctx: Ctx = { view, events, all, eras, byId, eraId, scope, scopeLabel };
  view.append(header(ctx, scopeBad));
  const grid = buildGrid(ctx);
  view.append(grid);
  /* Two passes: the skeleton establishes the column widths and the lane
     heights the viewport actually allows, then the packing runs against the
     measured numbers rather than against an assumed viewport. */
  fill(ctx, grid);
  publish();
}

/* ---- header ------------------------------------------------------------- */

function header(c: Ctx, bad: string | null): HTMLElement {
  const openEra = c.eras.filter((e) => e.id === c.eraId)[0];
  const strands = lanes(c.all).length;
  const bits: string[] = [
    c.all.length + ' events in ' + strands + ' strands',
  ];
  if (c.scopeLabel) bits.push('scope ' + c.scopeLabel + ' · ' + c.events.length + ' events');
  if (openEra) bits.push('era ' + openEra.label + ' open');
  bits.push('a closed era opens on click');
  bits.push('an event that will not fit at 11px is a mark until its year is opened');

  const line = h('div', { class: 'tl-head' },
    h('span', { class: 'eyebrow' }, 'Timeline'),
    h('span', { class: 'tl-head-bits dim' }, bits.join('  ·  ')),
  );
  const chips = scopeChips(c);
  if (chips) line.append(chips);
  if (bad) {
    return h('div', null, line, h('div', { class: 'tl-bad red' }, bad));
  }
  return line;
}

function href(era: string | null, scope: string | null): string {
  const q: string[] = [];
  if (era) q.push('era=' + encodeURIComponent(era));
  if (scope) q.push('scope=' + encodeURIComponent(scope));
  return '#/timeline' + (q.length ? '?' + q.join('&') : '');
}

/* ALL · NODE · THREAD. They exist only when the route carries an id, because a
   scope chip with nothing to scope to is a control that cannot be honest. */
function scopeChips(c: Ctx): HTMLElement | null {
  if (!c.scope) return null;
  const isNode = c.scope.indexOf('n:') === 0;
  const wrap = h('div', { class: 'tl-scope' });
  wrap.append(h('a', {
    class: 'tl-sc',
    href: href(c.eraId, null),
  }, 'SCOPE · ALL'));
  wrap.append(isNode
    ? h('span', { class: 'tl-sc on' }, 'SCOPE · NODE · ' + (c.scopeLabel || c.scope.slice(2)))
    : h('span', { class: 'tl-sc off', title: 'No node id is carried by this route.' }, 'SCOPE · NODE'));
  wrap.append(!isNode
    ? h('span', { class: 'tl-sc on' }, 'SCOPE · THREAD · ' + (c.scopeLabel || c.scope.slice(2)))
    : h('span', { class: 'tl-sc off', title: 'No thread id is carried by this route.' }, 'SCOPE · THREAD'));
  return wrap;
}

/* ---- the grid skeleton -------------------------------------------------- */

interface Cells { packs: Map<string, HTMLElement>; yearHead: HTMLElement | null }
const cells: Cells = { packs: new Map(), yearHead: null };

function buildGrid(c: Ctx): HTMLElement {
  cells.packs = new Map();
  cells.yearHead = null;

  const cols = [LANE_LABEL_COL + 'px'];
  for (const e of c.eras) cols.push(e.id === c.eraId ? 'minmax(300px, 1fr)' : CLOSED_COL + 'px');

  const grid = h('div', {
    class: 'tl-grid',
    style: 'grid-template-columns:' + cols.join(' '),
  });

  /* era head row */
  grid.append(h('div', { class: 'tl-corner' }));
  for (const e of c.eras) {
    const open = e.id === c.eraId;
    const n = c.events.filter((x) => x.era === e.id).length;
    const head: HTMLElement = open
      ? h('div', { class: 'tl-era open' })
      : h('a', { class: 'tl-era', href: href(e.id, c.scope) });
    head.append(h('div', { class: 'tl-era-label' }, e.label));
    head.append(h('div', { class: 'tl-era-sub dim' },
      e.sub + ' · ' + n + (open ? ' events · years below open on click' : ' events · click to open')));
    if (open) {
      const yh = h('div', { class: 'tl-years' });
      head.append(yh);
      cells.yearHead = yh;
    }
    grid.append(head);
  }

  /* one row per lane */
  for (const lane of lanes(c.all)) {
    const laneEvents = c.events.filter((x) => x.strand === lane.id);
    grid.append(h('div', { class: 'tl-lane-name' },
      h('div', { class: 'eyebrow' }, lane.label),
      h('div', { class: 'dim tl-lane-n' }, laneEvents.length + ' of ' + c.events.length),
    ));
    for (const e of c.eras) {
      const n = laneEvents.filter((x) => x.era === e.id).length;
      if (e.id === c.eraId) {
        const pack = h('div', { class: 'tl-pack', 'data-strand': lane.id, 'data-era': e.id });
        cells.packs.set(lane.id, pack);
        grid.append(h('div', { class: 'tl-cell open' }, pack));
      } else {
        grid.append(h('div', { class: 'tl-cell' },
          h('a', { class: 'tl-count', href: href(e.id, c.scope) },
            h('b', null, String(n)), ' ', h('span', { class: 'dim' }, n === 1 ? 'event' : 'events'))));
      }
    }
  }
  return grid;
}

/* ---- the packing pass --------------------------------------------------- */

function fill(c: Ctx, grid: HTMLElement): void {
  const laneList = lanes(c.all);
  const first = cells.packs.get(laneList[0].id);
  if (!first) return;

  const width = Math.max(120, Math.floor(first.getBoundingClientRect().width));
  const top = first.getBoundingClientRect().top + window.scrollY;
  const room = Math.max(240, window.innerHeight - (top - window.scrollY) - 28);
  const perLane = room / laneList.length;
  const chipRowBudget = Math.max(3, Math.min(14, Math.floor((perLane - 30) / ROW_PITCH)));

  const era = c.eras.filter((e) => e.id === c.eraId)[0];
  const inEra = c.events.filter((e) => e.era === c.eraId);
  /* The year axis is the era's own shape, taken from every event the board has
     in it, not from the scoped subset: a scope filters what is drawn, it does
     not move an event's date along the axis. */
  const eraAll = c.all.filter((e) => e.era === c.eraId);
  const years = era ? eraYears(era, eraAll) : [];
  let open = openYears.get(c.eraId);
  if (!open) { open = new Set<number>(); openYears.set(c.eraId, open); }
  const present = new Set(years);
  for (const y of Array.from(open)) if (!present.has(y)) open.delete(y);

  const slots = yearSlots(years, open, width, OPEN_YEAR_WEIGHT);
  drawYearHead(c, slots);

  for (const lane of laneList) {
    const pack = cells.packs.get(lane.id);
    if (!pack) continue;
    const evs = inEra.filter((e) => e.strand === lane.id);
    const lay = packLane(lane, evs, { width, slots, chipRowBudget });
    paintLane(c, pack, lay, slots);
  }
  void grid;
}

function drawYearHead(c: Ctx, slots: YearSlot[]): void {
  const yh = cells.yearHead;
  if (!yh) return;
  clear(yh);
  for (const s of slots) {
    const txt = String(s.year);
    const fits = s.w >= textWidth(txt) + 8;
    const b = h('button', {
      class: 'tl-year' + (s.open ? ' on' : ''),
      style: 'left:' + s.x.toFixed(1) + 'px;width:' + Math.max(1, s.w - 1).toFixed(1) + 'px',
      'aria-pressed': s.open ? 'true' : 'false',
      'aria-label': (s.open ? 'close ' : 'open ') + txt,
      title: (s.open ? 'close ' : 'open ') + txt,
      'data-year': txt,
    }, fits || s.open ? txt : null);
    b.addEventListener('click', () => {
      const set = openYears.get(c.eraId);
      if (!set) return;
      if (set.has(s.year)) set.delete(s.year); else set.add(s.year);
      void renderTimeline(c.view, c.eraId, c.scope);
    });
    yh.append(b);
  }
}

function paintLane(c: Ctx, pack: HTMLElement, lay: LaneLayout, slots: YearSlot[]): void {
  clear(pack);
  pack.style.height = Math.max(28, lay.height + 6) + 'px';

  for (const s of slots) {
    pack.append(h('i', {
      class: 'tl-gl' + (s.open ? ' on' : ''),
      style: 'left:' + s.x.toFixed(1) + 'px',
      'aria-hidden': 'true',
    }));
  }

  for (const it of lay.items) {
    const ev = it.ev;
    const n = ev.node ? c.byId.get(ev.node) : undefined;
    const colour = n ? clsColour(n.cls) : 'var(--line2)';
    const when = ev.date + (ev.precision && ev.precision !== 'day' ? ' (' + ev.precision + ')' : '');

    if (it.kind === 'chip') {
      const attrs: Record<string, string> = {
        class: 'tl-chip',
        style: 'left:' + it.x.toFixed(1) + 'px;top:' + it.y + 'px;width:' + it.w + 'px;height:' +
          CHIP_H + 'px;border-left-color:' + colour,
        title: when + (n ? ' · ' + n.label : ''),
        'data-tl-item': '1',
        'data-kind': 'chip',
        'data-id': ev.id,
        'data-era': ev.era,
        'data-strand': ev.strand,
      };
      if (ev.node) {
        pack.append(h('a', { ...attrs, href: '#/n/' + ev.node }, ev.label || ''));
      } else {
        pack.append(h('span', attrs, ev.label || ''));
      }
    } else {
      const attrs: Record<string, string> = {
        class: 'tl-mark',
        style: 'left:' + it.x.toFixed(1) + 'px;top:' + it.y + 'px;width:' + MARK_W + 'px;height:' +
          MARK_H + 'px;background:' + colour,
        title: when + (ev.label ? ' · ' + ev.label : ' · no label on this event') +
          ' · open ' + ev.date.slice(0, 4) + ' to place it',
        'data-tl-item': '1',
        'data-kind': 'mark',
        'data-id': ev.id,
        'data-era': ev.era,
        'data-strand': ev.strand,
      };
      if (ev.node) pack.append(h('a', { ...attrs, href: '#/n/' + ev.node }));
      else pack.append(h('i', attrs));
    }
  }
}

/* ---- what the checks read ----------------------------------------------- */

export interface PlacedItem {
  id: string; era: string; strand: string;
  x: number; y: number; w: number; h: number;
  kind: 'chip' | 'mark';
}

/* Measured off the rendered DOM, not off the layout's own numbers. C4 and C15
   need to know what a reader sees, and this repo has been burned by checks that
   agreed with the implementation while the pixels disagreed. */
function placed(): PlacedItem[] {
  const out: PlacedItem[] = [];
  const els = document.querySelectorAll('[data-tl-item]');
  for (let i = 0; i < els.length; i++) {
    const el = els[i] as HTMLElement;
    const r = el.getBoundingClientRect();
    out.push({
      id: el.getAttribute('data-id') || '',
      era: el.getAttribute('data-era') || '',
      strand: el.getAttribute('data-strand') || '',
      x: r.left + window.scrollX,
      y: r.top + window.scrollY,
      w: r.width,
      h: r.height,
      kind: (el.getAttribute('data-kind') as 'chip' | 'mark') || 'chip',
    });
  }
  return out;
}

function publish(): void {
  const w = window as unknown as { __app?: Record<string, unknown> };
  w.__app = w.__app || {};
  (w.__app as Record<string, unknown>).timeline = { placed };
}
