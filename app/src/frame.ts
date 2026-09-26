/* frame.ts: the common frame of Design response section 1.1.
 *
 * A 40px bar: the wordmark, five routes and More (four more), and the search field. The raw URL
 * fragment and the viewport size used to sit on the right; they were debugging
 * aids, not reader chrome, and went in redesign phase 5b. The route is on the
 * bar as `data-route` for anything that needs to read it.
 *
 * On a phone (760 wide or less) the bar is two rows: the wordmark, the back
 * control and a VIEWS button that opens the eight routes as a list, then the
 * search field. Every route is two taps away.
 *
 * Every href here is a route in section 2.1. Two of the eight need an id to point
 * at, so they carry one:
 *   Threads   -> #/t/custody, a thread in Design 1.6 and an entry path in map.json
 *   Patents   -> #/patents/10144532, the patent the Design response and the mockup
 *                use, and the only one of the five whose node is on the board
 *   Report    -> the node in view. With no node in view there is nothing to report
 *                on, so the item is inert rather than pointing at a route that
 *                does not resolve.
 *
 * Left of the routes is the back control. It is a button, not a link, because it
 * goes nowhere of its own: it calls history.back(). See src/history.ts.
 */
import { h, clear } from './dom';
import { searchBox } from './search';
import { fragment, routeNodeId, type Route } from './router';
import { canGoBack, goBack, previousTitle } from './history';

const PATENT_IN_VIEW = '10144532';
const THREAD_IN_VIEW = 'custody';

interface NavItem { label: string; href: string | null; match: (r: Route) => boolean; more?: boolean; }

let lastNodeId: string | null = null;

/* Redesign phase 6: five routes in the row, the Atlas among them; the map,
   threads, the neighbourhood and the report under More until phase 11 decides
   what becomes of them. Every one of them still resolves. */
function items(r: Route): NavItem[] {
  const nid = routeNodeId(r) || lastNodeId;
  return [
    { label: 'HOME', href: '#/', match: (x) => x.kind === 'home' },
    { label: 'ATLAS', href: '#/atlas', match: (x) => x.kind === 'atlas' || x.kind === 'topic' },
    { label: 'TIMELINE', href: '#/timeline', match: (x) => x.kind === 'timeline' },
    { label: 'EVIDENCE', href: '#/evidence', match: (x) => x.kind === 'evidence' },
    { label: 'PATENTS', href: '#/patents/' + PATENT_IN_VIEW, match: (x) => x.kind === 'patents' },
    { label: 'MAP', more: true, href: '#/map', match: (x) => x.kind === 'map' || x.kind === 'node-map' || x.kind === 'thread-map' },
    { label: 'THREADS', more: true, href: '#/t/' + THREAD_IN_VIEW, match: (x) => x.kind === 'thread' },
    { label: 'NEIGHBOURHOOD', more: true, href: '#/hood', match: (x) => x.kind === 'hood' || x.kind === 'node-hood' },
    {
      label: 'REPORT', more: true,
      href: nid ? '#/report/n/' + nid : null,
      match: (x) => x.kind === 'report-node' || x.kind === 'report-thread',
    },
  ];
}

let barEl: HTMLElement | null = null;
let backEl: HTMLButtonElement | null = null;

/* The back control's state is the reader's trail, not the route, so it is set
   here after the frame is drawn and again after the route has rendered. */
export function refreshFrameBack(): void {
  if (!backEl) return;
  const can = canGoBack();
  const prev = can ? previousTitle() : '';
  const label = prev ? 'Back to ' + prev : 'Back';
  backEl.disabled = !can;
  backEl.setAttribute('aria-disabled', can ? 'false' : 'true');
  backEl.setAttribute('aria-label', label);
  backEl.setAttribute('title', label);
}

export function renderFrame(host: HTMLElement, r: Route): void {
  const nid = routeNodeId(r);
  if (nid) lastNodeId = nid;

  clear(host);
  const bar = h('div', { class: 'bar', role: 'banner', 'data-route': fragment(), 'data-open': '0' });
  barEl = bar;

  bar.append(h('div', { class: 'wordmark' },
    h('span', { class: 'w-dim' }, 'THE '),
    h('span', { class: 'w-lit' }, 'LEGACY PROGRAM'),
    h('span', { class: 'w-dim' }, ' RESEARCH TERMINAL'),
  ));

  backEl = h('button', {
    type: 'button',
    class: 'nav-back',
    onclick: () => { goBack(); },
  }, h('span', { class: 'nav-back-chev', 'aria-hidden': 'true' }, '‹'), 'Back');
  bar.append(backEl);
  refreshFrameBack();

  const nav = h('nav', { class: 'nav', id: 'nav-views', 'aria-label': 'Views', 'data-more': '0' });
  const toggle = h('button', {
    type: 'button', class: 'nav-toggle', 'aria-controls': 'nav-views', 'aria-expanded': 'false',
    onclick: () => {
      const open = bar.getAttribute('data-open') !== '1';
      bar.setAttribute('data-open', open ? '1' : '0');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    },
  }, 'VIEWS ', h('span', { class: 'nav-toggle-chev', 'aria-hidden': 'true' }, '▾'));
  bar.append(toggle);
  const moreList = h('div', { class: 'nav-more-list', id: 'nav-more' });
  const moreBtn = h('button', {
    type: 'button', class: 'nav-more-btn', 'aria-controls': 'nav-more', 'aria-expanded': 'false',
    onclick: (e: Event) => {
      e.stopPropagation();
      const open = nav.getAttribute('data-more') !== '1';
      nav.setAttribute('data-more', open ? '1' : '0');
      moreBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    },
  }, 'MORE ', h('span', { class: 'nav-toggle-chev', 'aria-hidden': 'true' }, '▾'));
  let moreCurrent = false;
  for (const it of items(r)) {
    const host = it.more ? moreList : nav;
    if (!it.href) {
      host.append(h('span', {
        class: 'nav-inert',
        title: 'A report is written about a node. Open a node first.',
      }, it.label));
      continue;
    }
    const cur = it.match(r);
    if (cur && it.more) moreCurrent = true;
    host.append(h('a', {
      href: it.href,
      'aria-current': cur ? 'page' : null,
    }, it.label));
  }
  if (moreCurrent) moreBtn.classList.add('current');
  nav.append(h('div', { class: 'nav-more' }, moreBtn, moreList));
  bar.append(nav);

  bar.append(h('div', { class: 'bar-search' },
    searchBox({ placeholder: 'search the board' })));

  /* The slot the closed analyst tab sits in. The tab used to be fixed to the
     foot of the window, where it covered a line of text on every scrolling page
     (blind critic round 0). In the bar it covers nothing and takes no height
     from the map or the neighbourhood, which have none to give. */
  bar.append(h('span', { class: 'bar-dock', 'aria-hidden': 'true' }));

  host.append(bar);
  placeDock();
}

/* Put the closed tab exactly over its slot. The bar is fixed, so the slot only
   moves when the window is resized or the bar is redrawn. */
export function placeDock(): void {
  const slot = document.querySelector('.bar .bar-dock') as HTMLElement | null;
  const dock = document.getElementById('analyst');
  if (!slot || !dock) return;
  const r = slot.getBoundingClientRect();
  dock.style.setProperty('--dock-x', Math.round(r.left) + 'px');
  dock.style.setProperty('--dock-y', Math.round(r.top) + 'px');
}
window.addEventListener('resize', placeDock);
/* More closes on any click elsewhere, and on Escape */
document.addEventListener('click', () => {
  const n = document.querySelector('.bar .nav[data-more="1"]');
  if (n) { n.setAttribute('data-more', '0'); const b = n.querySelector('.nav-more-btn'); if (b) b.setAttribute('aria-expanded', 'false'); }
});
document.addEventListener('keydown', (e) => {
  if ((e as KeyboardEvent).key !== 'Escape') return;
  const n = document.querySelector('.bar .nav[data-more="1"]');
  if (n) n.setAttribute('data-more', '0');
});
if (document.fonts && document.fonts.ready) void document.fonts.ready.then(placeDock);

export function refreshFrameStatus(): void {
  if (barEl) barEl.setAttribute('data-route', fragment());
}
