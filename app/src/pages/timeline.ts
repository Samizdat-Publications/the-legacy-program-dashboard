/* Timeline: routes #/timeline, ?era= ?scope= ?strand= ?topic=.
 *
 * Redesign phase 9. The lanes are the ten topic sections (an event belongs to
 * the section of its node's primary topic; an event whose node is in no topic,
 * or that names no node, is in the last lane), and the four strands the lanes
 * used to be are a filter. Columns are the eras of index.json. A closed era shows
 * one count per lane and opens on click. The open era shows year gridlines and
 * its events as 11px chips packed so that no two overlap; the events a year
 * cannot place are COUNTED ("+N"), and the count opens their named list. There
 * are no unnamed marks. A year opens wider on click.
 *
 * Clicking an event (a chip, or a row of a counted list) shows its text, date,
 * grade and node in the panel over the grid. A same-day repeat (same node, same
 * day, near-identical label: build_app_data.py) is not drawn a second time: the
 * event it repeats carries it, with both sets of sources. An event dated after
 * the board's own date is marked as scheduled.
 *
 * Scope chips ALL / NODE / THREAD / TOPIC are drawn when the route carries one.
 *
 * Nothing here is written: every string is an event's own label or text, a
 * section's or era's own title, or a count. The page publishes
 * window.__app.timeline.placed(), which measures the rendered DOM.
 */
import '../styles/timeline.css';
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadTopics, clsColour, type IndexNode, type TopicsFile } from '../data';
import { loadThreads, threadById } from '../thread/data';
import { loadTimeline } from '../timeline/source';
import {
  lanes, packLane, eraYears, yearSlots, textWidth, STRANDS,
  CHIP_H, ROW_PITCH,
  type TEvent, type EraDef, type LaneLayout, type YearSlot, type Lane,
} from '../timeline/layout';

const CLOSED_COL = 112;          /* px per closed era column                  */
const LANE_LABEL_COL = 176;      /* px of the section-name column             */
const OPEN_YEAR_WEIGHT = 6;      /* an opened year against a closed one       */

/* Years the reader has opened, kept per era, and what the panel shows. Not in
   the URL: they are views of the page, not places a reader links to. */
const openYears = new Map<string, Set<number>>();
type Pick = { kind: 'event'; id: string } | { kind: 'list'; ids: string[]; lane: string; year: number } | null;
let pick: Pick = null;

interface Ctx {
  view: HTMLElement;
  events: TEvent[];        /* drawn: after scope and strand, repeats removed */
  all: TEvent[];           /* every event, for the header and the repeats     */
  byEv: Map<string, TEvent>;
  repeats: Map<string, TEvent[]>;
  lanes: Lane[];
  eras: EraDef[];
  byId: Map<string, IndexNode>;
  eraId: string;
  scope: string | null;
  strand: string | null;
  topic: string | null;
  scopeLabel: string | null;
  topicLabel: string | null;
  present: string;         /* the board's own date, yyyy-mm-dd */
  route: { era: string | null; scope: string | null; strand: string | null; topic: string | null };
}

export async function renderTimeline(
  view: HTMLElement, era: string | null, scope: string | null,
  strand: string | null = null, topic: string | null = null,
): Promise<void> {
  clear(view);
  setTitle('Timeline');

  const [idx, all, topics] = await Promise.all([loadIndex(), loadTimeline(), loadTopics()]);
  const byId = new Map<string, IndexNode>();
  for (const n of idx.nodes) byId.set(n.id, n);
  const byEv = new Map<string, TEvent>();
  for (const e of all) byEv.set(e.id, e);

  /* the repeats, under the event each repeats */
  const repeats = new Map<string, TEvent[]>();
  for (const e of all) {
    if (!e.sameAs) continue;
    const l = repeats.get(e.sameAs);
    if (l) l.push(e); else repeats.set(e.sameAs, [e]);
  }

  /* ---- scope ----------------------------------------------------------- */
  let events = all.filter((e) => !e.sameAs);
  let scopeLabel: string | null = null;
  const bad: string[] = [];
  if (scope && scope.indexOf('n:') === 0) {
    const id = scope.slice(2);
    const n = byId.get(id);
    if (!n) bad.push('No node with the id ' + id + ' is on the board.');
    else { scopeLabel = n.label; events = events.filter((e) => e.node === id); }
  } else if (scope && scope.indexOf('t:') === 0) {
    const id = scope.slice(2);
    const tf = await loadThreads();
    const th = threadById(tf, id);
    if (!th) bad.push('No thread with the id ' + id + ' is authored.');
    else {
      scopeLabel = th.label;
      const ids = new Set(th.steps.map((s) => s.node));
      events = events.filter((e) => !!e.node && ids.has(e.node));
    }
  } else if (scope) {
    bad.push('A scope is n:<node id> or t:<thread id>. This route carries ' + scope + '.');
  }
  let topicLabel: string | null = null;
  if (topic) {
    const t = topics.topics.filter((x) => x.id === topic)[0];
    if (!t) bad.push('No topic with the id ' + topic + ' is on the board.');
    else {
      topicLabel = t.title;
      events = events.filter((e) => !!e.node && inTopic(topics, e.node, topic));
    }
  }
  if (strand && !STRANDS.some((s) => s.id === strand)) bad.push('No strand is called ' + strand + '.');
  else if (strand) events = events.filter((e) => e.strand === strand);

  /* The NO DATE column is drawn only when it holds an event. */
  const undatedEra = (e: EraDef) => e.start == null && e.end == null;
  const eras = (idx.eras as EraDef[]).filter((e) => !undatedEra(e) || events.some((x) => x.era === e.id));
  const present = String(idx.generated || '').slice(0, 10) || new Date().toISOString().slice(0, 10);

  /* The route's era wins; otherwise the era with the most events in view. */
  let eraId = '';
  if (era && eras.some((x) => x.id === era)) eraId = era;
  else {
    let best = -1;
    for (const e of eras) {
      const n = events.filter((x) => x.era === e.id).length;
      if (n > best) { best = n; eraId = e.id; }
    }
  }

  /* every section lane when nothing narrows the view; only the lanes holding
     something when a scope, a topic or a strand does */
  let laneList = lanes(topics.sections);
  if (scope || topic || strand) laneList = laneList.filter((l) => events.some((e) => e.section === l.id));
  if (!laneList.length) laneList = lanes(topics.sections).slice(0, 1);

  const ctx: Ctx = {
    view, events, all, byEv, repeats, lanes: laneList, eras, byId, eraId, scope, strand, topic,
    scopeLabel, topicLabel, present, route: { era, scope, strand, topic },
  };
  /* a pick from another era or scope does not survive into this one */
  const inView = new Set(events.filter((e) => e.era === eraId).map((e) => e.id));
  if (pick && pick.kind === 'event' && !inView.has(pick.id)) pick = null;
  if (pick && pick.kind === 'list' && !pick.ids.every((id) => inView.has(id))) pick = null;

  view.append(header(ctx, bad));
  if (window.innerWidth <= 760) { view.append(phoneList(ctx)); publish(); return; }
  const panel = h('div', { class: 'tl-detail', 'aria-live': 'polite' });
  view.append(panel);
  const grid = buildGrid(ctx);
  view.append(grid);
  /* Two passes: the skeleton establishes the column widths the viewport allows,
     then the packing runs against the measured numbers. */
  fill(ctx, panel);
  drawPanel(ctx, panel);
  publish();
}

function inTopic(topics: TopicsFile, node: string, topic: string): boolean {
  const ai = topics.appearsIn[node];
  return !!ai && ai.some((x) => x[0] === topic);
}

/* ---- header ------------------------------------------------------------- */

function header(c: Ctx, bad: string[]): HTMLElement {
  const openEra = c.eras.filter((e) => e.id === c.eraId)[0];
  const nRep = c.all.filter((e) => !!e.sameAs).length;
  const bits: string[] = [
    c.all.length + ' events' + (nRep ? ', ' + nRep + ' of them same-day repeats shown once' : '') +
      ', in ' + c.lanes.length + ' section lanes',
  ];
  if (c.scopeLabel || c.topicLabel || c.strand) bits.push(c.events.length + ' in view');
  if (openEra) bits.push('era ' + openEra.label + ' open');
  const later = c.events.filter((e) => e.era === c.eraId && scheduled(c, e)).length;
  if (later) bits.push(later + (later === 1 ? ' event is' : ' events are') + ' dated after the board’s date of ' + c.present + ': scheduled, marked in amber');
  bits.push('click an event to read it; a count opens the events it stands for');

  const line = h('div', { class: 'tl-head' },
    h('span', { class: 'eyebrow' }, 'Timeline'),
    h('span', { class: 'tl-head-bits dim' }, bits.join('  ·  ')),
  );
  const chips = scopeChips(c);
  if (chips) line.append(chips);
  const wrap = h('div', { class: 'tl-top' }, line, strandChips(c));
  for (const b of bad) wrap.append(h('div', { class: 'tl-bad red' }, b));
  return wrap;
}

function href(c: Ctx, over: Partial<Ctx['route']>): string {
  const r = { ...c.route, era: c.eraId, ...over };
  const q: string[] = [];
  if (r.era) q.push('era=' + encodeURIComponent(r.era));
  if (r.scope) q.push('scope=' + encodeURIComponent(r.scope));
  if (r.topic) q.push('topic=' + encodeURIComponent(r.topic));
  if (r.strand) q.push('strand=' + encodeURIComponent(r.strand));
  return '#/timeline' + (q.length ? '?' + q.join('&') : '');
}

/* The strands, as a filter. */
function strandChips(c: Ctx): HTMLElement {
  const wrap = h('div', { class: 'tl-strands', role: 'group', 'aria-label': 'Filter by strand' });
  wrap.append(h('span', { class: 'eyebrow' }, 'Strand'));
  wrap.append(c.strand
    ? h('a', { class: 'tl-sc', href: href(c, { strand: null }), 'data-strand': '' }, 'ALL')
    : h('span', { class: 'tl-sc on', 'data-strand': '' }, 'ALL'));
  for (const s of STRANDS) {
    const on = c.strand === s.id;
    wrap.append(on
      ? h('span', { class: 'tl-sc on', 'data-strand': s.id }, s.label)
      : h('a', { class: 'tl-sc', href: href(c, { strand: s.id }), 'data-strand': s.id }, s.label));
  }
  return wrap;
}

/* ALL and the scope in force. They exist only when the route carries one,
   because a scope chip with nothing to scope to is a control that cannot be
   honest. */
function scopeChips(c: Ctx): HTMLElement | null {
  if (!c.scope && !c.topic) return null;
  const wrap = h('div', { class: 'tl-scope' });
  wrap.append(h('a', { class: 'tl-sc', href: href(c, { scope: null, topic: null }) }, 'SCOPE · ALL'));
  if (c.scope) {
    const isNode = c.scope.indexOf('n:') === 0;
    wrap.append(h('span', { class: 'tl-sc on' },
      'SCOPE · ' + (isNode ? 'NODE' : 'THREAD') + ' · ' + (c.scopeLabel || c.scope.slice(2))));
  }
  if (c.topic) {
    wrap.append(h('span', { class: 'tl-sc on', 'data-topic': c.topic },
      'SCOPE · TOPIC · ' + (c.topicLabel || c.topic)));
  }
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
  const grid = h('div', { class: 'tl-grid', style: 'grid-template-columns:' + cols.join(' ') });

  grid.append(h('div', { class: 'tl-corner' }));
  for (const e of c.eras) {
    const open = e.id === c.eraId;
    const n = c.events.filter((x) => x.era === e.id).length;
    const head: HTMLElement = open
      ? h('div', { class: 'tl-era open' })
      : h('a', { class: 'tl-era', href: href(c, { era: e.id }) });
    head.append(h('div', { class: 'tl-era-label' }, e.label));
    head.append(h('div', { class: 'tl-era-sub dim' },
      e.sub + ' · ' + n + (open ? ' events · a year widens on click' : ' events · click to open')));
    if (open) {
      const yh = h('div', { class: 'tl-years' });
      head.append(yh);
      cells.yearHead = yh;
    }
    grid.append(head);
  }

  for (const lane of c.lanes) {
    const laneEvents = c.events.filter((x) => x.section === lane.id);
    grid.append(h('div', { class: 'tl-lane-name', 'data-section': lane.id },
      h('div', { class: 'tl-lane-label' }, lane.label),
      h('div', { class: 'dim tl-lane-n' }, laneEvents.length + ' of ' + c.events.length),
    ));
    for (const e of c.eras) {
      const n = laneEvents.filter((x) => x.era === e.id).length;
      if (e.id === c.eraId) {
        const pack = h('div', { class: 'tl-pack', 'data-section': lane.id, 'data-era': e.id });
        cells.packs.set(lane.id, pack);
        grid.append(h('div', { class: 'tl-cell open' }, pack));
      } else {
        grid.append(h('div', { class: 'tl-cell' },
          n ? h('a', { class: 'tl-count', href: href(c, { era: e.id }) },
            h('b', null, String(n)), ' ', h('span', { class: 'dim' }, n === 1 ? 'event' : 'events'))
            : h('span', { class: 'tl-none faint' }, 'none')));
      }
    }
  }
  return grid;
}

/* ---- the packing pass --------------------------------------------------- */

function fill(c: Ctx, panel: HTMLElement): void {
  const first = cells.packs.get(c.lanes[0].id);
  if (!first) return;

  const width = Math.max(120, Math.floor(first.getBoundingClientRect().width));
  const top = first.getBoundingClientRect().top;
  const room = Math.max(240, window.innerHeight - top - 28);
  const perLane = room / c.lanes.length;
  /* at least eight rows a lane: with eleven lanes the page scrolls rather than
     leaving most events behind a count */
  const chipRowBudget = Math.max(8, Math.min(14, Math.floor((perLane - 30) / ROW_PITCH)));

  const era = c.eras.filter((e) => e.id === c.eraId)[0];
  const inEra = c.events.filter((e) => e.era === c.eraId);
  /* The year axis is the era's own shape, taken from every event the board has
     in it, not from the scoped subset. It stops at the last year that has an
     event: a year after the board's own date with nothing in it is not drawn. */
  const eraAll = c.all.filter((e) => e.era === c.eraId);
  const hasEvent = new Set(eraAll.map((e) => Number(e.date.slice(0, 4))));
  const presentYear = Number(c.present.slice(0, 4));
  const years = (era ? eraYears(era, eraAll) : []).filter((y) => y <= presentYear || hasEvent.has(y));
  let open = openYears.get(c.eraId);
  if (!open) { open = new Set<number>(); openYears.set(c.eraId, open); }
  const inAxis = new Set(years);
  for (const y of Array.from(open)) if (!inAxis.has(y)) open.delete(y);

  const slots = yearSlots(years, open, width, OPEN_YEAR_WEIGHT);
  drawYearHead(c, slots);

  for (const lane of c.lanes) {
    const pack = cells.packs.get(lane.id);
    if (!pack) continue;
    const evs = inEra.filter((e) => e.section === lane.id);
    const lay = packLane(lane, evs, { width, slots, chipRowBudget });
    paintLane(c, pack, lay, slots, lane, panel);
  }
}

function drawYearHead(c: Ctx, slots: YearSlot[]): void {
  const yh = cells.yearHead;
  if (!yh) return;
  clear(yh);
  const presentYear = Number(c.present.slice(0, 4));
  for (const s of slots) {
    const txt = String(s.year);
    const fits = s.w >= textWidth(txt) + 8;
    const later = s.year > presentYear;
    const b = h('button', {
      class: 'tl-year' + (s.open ? ' on' : '') + (later ? ' later' : ''),
      style: 'left:' + s.x.toFixed(1) + 'px;width:' + Math.max(1, s.w - 1).toFixed(1) + 'px',
      'aria-pressed': s.open ? 'true' : 'false',
      'aria-label': (s.open ? 'narrow ' : 'widen ') + txt,
      title: (s.open ? 'narrow ' : 'widen ') + txt + (later ? ": after the board's date, so scheduled events only" : ''),
      'data-year': txt,
    }, fits || s.open ? txt : null);
    b.addEventListener('click', () => {
      const set = openYears.get(c.eraId);
      if (!set) return;
      if (set.has(s.year)) set.delete(s.year); else set.add(s.year);
      void renderTimeline(c.view, c.route.era, c.scope, c.strand, c.topic);
    });
    yh.append(b);
  }
}

const scheduled = (c: Ctx, e: TEvent): boolean => e.date.slice(0, 10) > c.present;

function paintLane(c: Ctx, pack: HTMLElement, lay: LaneLayout, slots: YearSlot[], lane: Lane, panel: HTMLElement): void {
  clear(pack);
  pack.style.height = Math.max(28, lay.height + 4) + 'px';

  for (const s of slots) {
    pack.append(h('i', { class: 'tl-gl' + (s.open ? ' on' : ''), style: 'left:' + s.x.toFixed(1) + 'px', 'aria-hidden': 'true' }));
  }

  for (const it of lay.items) {
    const pos = 'left:' + it.x.toFixed(1) + 'px;top:' + it.y + 'px;width:' + it.w + 'px;height:' + CHIP_H + 'px';
    if (it.kind === 'chip' && it.ev) {
      const ev = it.ev;
      const n = ev.node ? c.byId.get(ev.node) : undefined;
      const colour = n ? clsColour(n.cls) : 'var(--line2)';
      const sched = scheduled(c, ev);
      const b = h('button', {
        type: 'button',
        class: 'tl-chip' + (it.right ? ' right' : '') + (sched ? ' sched' : '') + (pick && pick.kind === 'event' && pick.id === ev.id ? ' on' : ''),
        style: pos + ';' + (it.right ? 'border-right-color:' : 'border-left-color:') + colour,
        title: when(ev) + (sched ? ' · scheduled' : '') + (n ? ' · ' + n.label : ''),
        'data-tl-item': '1', 'data-kind': 'chip', 'data-id': ev.id, 'data-era': ev.era,
        'data-section': lane.id, 'data-scheduled': sched ? '1' : null,
      }, ev.label || '');
      b.addEventListener('click', () => { pick = { kind: 'event', id: ev.id }; drawPanel(c, panel, true); markPick(); });
      pack.append(b);
    } else {
      const ids = it.evs.map((e) => e.id);
      const b = h('button', {
        type: 'button',
        class: 'tl-more' + (it.evs.some((e) => scheduled(c, e)) ? ' sched' : ''),
        style: pos,
        title: it.evs.length + ' more ' + (it.evs.length === 1 ? 'event' : 'events') + ' in ' + it.year + ', ' + lane.label + ': click for the list',
        'aria-label': it.evs.length + ' more events in ' + it.year + ', ' + lane.label + ': open the list',
        'data-tl-more': '1', 'data-kind': 'more', 'data-era': c.eraId, 'data-section': lane.id,
        'data-year': String(it.year), 'data-ids': ids.join(' '),
      }, '+' + it.evs.length);
      b.addEventListener('click', () => { pick = { kind: 'list', ids, lane: lane.label, year: it.year }; drawPanel(c, panel, true); markPick(); });
      pack.append(b);
    }
  }
}

/* the event in the panel is the chip marked on the grid */
function markPick(): void {
  const els = document.querySelectorAll('.tl-chip');
  for (let i = 0; i < els.length; i++) {
    const el = els[i] as HTMLElement;
    el.classList.toggle('on', !!pick && pick.kind === 'event' && pick.id === el.getAttribute('data-id'));
  }
}

function when(ev: TEvent): string {
  const d = ev.date.slice(0, ev.precision === 'year' ? 4 : ev.precision === 'month' ? 7 : 10);
  return d + (ev.precision && ev.precision !== 'day' ? ' (' + ev.precision + ')' : '');
}

/* ---- the panel: one event, or the named list behind a count ------------- */

function drawPanel(c: Ctx, panel: HTMLElement, reveal = false): void {
  clear(panel);
  panel.removeAttribute('data-mode');
  panel.removeAttribute('data-id');
  if (!pick) { panel.hidden = true; return; }
  panel.hidden = false;
  const close = h('button', { type: 'button', class: 'tl-d-close' }, 'close');
  close.addEventListener('click', () => { pick = null; drawPanel(c, panel); markPick(); });

  if (pick.kind === 'list') {
    const p = pick;
    panel.setAttribute('data-mode', 'list');
    panel.append(h('div', { class: 'tl-d-head' },
      h('span', { class: 'eyebrow' }, p.year + ' · ' + p.lane),
      h('span', { class: 'dim tl-d-count' }, p.ids.length + (p.ids.length === 1 ? ' event' : ' events') + ' the lane had no room to name'),
      close));
    const ul = h('div', { class: 'tl-d-list' });
    for (const id of p.ids) {
      const ev = c.byEv.get(id);
      if (!ev) continue;
      const sched = scheduled(c, ev);
      const b = h('button', { type: 'button', class: 'tl-li', 'data-id': id, 'data-scheduled': sched ? '1' : null },
        h('span', { class: 'tl-li-date dim' }, when(ev)),
        h('span', { class: 'tl-li-label' }, ev.label || 'no label on this event'),
        sched ? h('span', { class: 'tl-sched' }, 'scheduled') : null);
      b.addEventListener('click', () => { pick = { kind: 'event', id }; drawPanel(c, panel, true); markPick(); });
      ul.append(b);
    }
    panel.append(ul);
  } else {
    const ev = c.byEv.get(pick.id);
    if (!ev) { pick = null; panel.hidden = true; return; }
    panel.setAttribute('data-mode', 'event');
    panel.setAttribute('data-id', ev.id);
    const sched = scheduled(c, ev);
    const n = ev.node ? c.byId.get(ev.node) : undefined;
    panel.append(h('div', { class: 'tl-d-head' },
      h('span', { class: 'tl-d-date' }, when(ev)),
      sched ? h('span', { class: 'tl-sched' }, 'scheduled: after the board’s date of ' + c.present) : null,
      h('span', { class: 'tl-d-grade dim' }, gradeText(ev)),
      close));
    panel.append(h('div', { class: 'tl-d-label' }, ev.label || 'no label on this event'));
    if (ev.text) panel.append(h('p', { class: 'tl-d-text' }, ev.text));
    const nodeLine = h('div', { class: 'tl-d-node' });
    if (n) nodeLine.append(h('span', { class: 'dim' }, 'node '), h('a', { class: 'tl-d-nodelink', href: '#/n/' + n.id }, n.label));
    else nodeLine.append(h('span', { class: 'faint' }, 'this event names no node'));
    panel.append(nodeLine);
    const reps = c.repeats.get(ev.id) || [];
    srcList(panel, ev, reps.length ? 'sources of this entry' : 'sources');
    if (reps.length) {
      const box = h('div', { class: 'tl-d-also' },
        h('div', { class: 'eyebrow' }, 'the same event, recorded again on the same day'));
      for (const r of reps) {
        box.append(h('div', { class: 'tl-d-rep', 'data-id': r.id },
          h('div', { class: 'tl-d-replabel' }, r.label || ''),
          r.text ? h('p', { class: 'tl-d-text dim' }, r.text) : null));
        srcList(box, r, 'sources of that entry');
      }
      panel.append(box);
    }
  }
  if (reveal) {
    const r = panel.getBoundingClientRect();
    if (r.top < 48 || r.top > window.innerHeight - 80) panel.scrollIntoView({ block: 'start', behavior: 'auto' });
  }
}

function gradeText(ev: TEvent): string {
  const bits: string[] = [];
  if (ev.grade) bits.push('event grade ' + ev.grade);
  if (ev.claimTier) bits.push('Tier ' + ev.claimTier);
  return bits.length ? bits.join(' · ') : 'no grade recorded';
}

function srcList(host: HTMLElement, ev: TEvent, head: string): void {
  const src = ev.sources || [];
  if (!src.length) {
    host.append(h('div', { class: 'tl-d-src faint' }, 'no source recorded on this entry; its node’s page carries the sources of its claims'));
    return;
  }
  const box = h('div', { class: 'tl-d-src' }, h('span', { class: 'dim' }, head + ': '));
  src.forEach((s, i) => {
    if (i) box.append(h('span', { class: 'faint' }, ' · '));
    box.append(s.url ? h('a', { href: s.url, rel: 'noreferrer', target: '_blank' }, s.text || s.url) : h('span', null, s.text));
  });
  host.append(box);
}

/* ---- what the checks read ----------------------------------------------- */

export interface PlacedItem {
  id: string; era: string; section: string;
  x: number; y: number; w: number; h: number;
  kind: 'chip' | 'more';
}

/* Measured off the rendered DOM, not off the layout's own numbers. */
function placed(): PlacedItem[] {
  const out: PlacedItem[] = [];
  const els = document.querySelectorAll('[data-tl-item], [data-tl-more]');
  for (let i = 0; i < els.length; i++) {
    const el = els[i] as HTMLElement;
    const r = el.getBoundingClientRect();
    out.push({
      id: el.getAttribute('data-id') || el.getAttribute('data-ids') || '',
      era: el.getAttribute('data-era') || '',
      section: el.getAttribute('data-section') || '',
      x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height,
      kind: (el.getAttribute('data-kind') as 'chip' | 'more') || 'chip',
    });
  }
  return out;
}

function publish(): void {
  const w = window as unknown as { __app?: Record<string, unknown> };
  w.__app = w.__app || {};
  (w.__app as Record<string, unknown>).timeline = { placed };
}

/* ---- the phone ---------------------------------------------------------- */
/* At phone width the grid cannot fit, so the open era is a list: the eras as
   links, then each section's events in date order, every one named, each
   opening in place to its text, grade, node and repeats. */
function phoneList(c: Ctx): HTMLElement {
  const wrap = h('div', { class: 'tlp' });
  const eraRow = h('div', { class: 'tlp-eras' });
  for (const e of c.eras) {
    const n = c.events.filter((x) => x.era === e.id).length;
    const on = e.id === c.eraId;
    eraRow.append(h(on ? 'span' : 'a', {
      class: 'tlp-era' + (on ? ' on' : ''),
      href: on ? null : href(c, { era: e.id }),
      'aria-current': on ? 'true' : null,
    }, e.label + ' · ' + n));
  }
  wrap.append(eraRow);
  const inEra = c.events.filter((e) => e.era === c.eraId)
    .slice().sort((a, b) => String(a.date).localeCompare(String(b.date)));
  for (const lane of c.lanes) {
    const evs = inEra.filter((e) => e.section === lane.id);
    if (!evs.length) continue;
    const sec = h('section', { class: 'tlp-lane', 'data-section': lane.id });
    sec.append(h('div', { class: 'tlp-head' },
      h('span', { class: 'tlp-title' }, lane.label), ' ',
      h('span', { class: 'dim' }, '· ' + evs.length + (evs.length === 1 ? ' event' : ' events'))));
    for (const ev of evs) {
      const n = ev.node ? c.byId.get(ev.node) : undefined;
      const colour = n ? clsColour(n.cls) : 'var(--line2)';
      const sched = scheduled(c, ev);
      const body = h('div', { class: 'tlp-body' },
        h('div', { class: 'dim' }, gradeText(ev) + (sched ? ' · scheduled' : '')),
        ev.text ? h('p', { class: 'tl-d-text' }, ev.text) : null);
      if (n) body.append(h('div', null, h('span', { class: 'dim' }, 'node '), h('a', { href: '#/n/' + n.id }, n.label)));
      else body.append(h('div', { class: 'faint' }, 'this event names no node'));
      for (const r of c.repeats.get(ev.id) || []) {
        body.append(h('div', { class: 'tl-d-rep dim' }, 'recorded again the same day: ' + (r.label || '')));
      }
      sec.append(h('details', { class: 'tlp-row', style: 'border-left-color:' + colour, 'data-id': ev.id },
        h('summary', null,
          h('span', { class: 'tlp-date dim' }, when(ev)),
          h('span', { class: 'tlp-label' }, ev.label || 'no label on this event')),
        body));
    }
    wrap.append(sec);
  }
  return wrap;
}
