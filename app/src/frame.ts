/* frame.ts — the common frame of Design response section 1.1.
 *
 * A 40px bar: the wordmark, the eight routes, the search field, and on the right
 * the current URL fragment and the viewport.
 *
 * Every href here is a route in section 2.1. Two of the eight need an id to point
 * at, so they carry one:
 *   Threads   -> #/t/custody, a thread in Design 1.6 and an entry path in map.json
 *   Patents   -> #/patents/10144532, the patent the Design response and the mockup
 *                use, and the only one of the five whose node is on the board
 *   Report    -> the node in view. With no node in view there is nothing to report
 *                on, so the item is inert rather than pointing at a route that
 *                does not resolve.
 */
import { h, clear } from './dom';
import { searchBox } from './search';
import { fragment, routeNodeId, type Route } from './router';

const PATENT_IN_VIEW = '10144532';
const THREAD_IN_VIEW = 'custody';

interface NavItem { label: string; href: string | null; match: (r: Route) => boolean; }

let lastNodeId: string | null = null;

function items(r: Route): NavItem[] {
  const nid = routeNodeId(r) || lastNodeId;
  return [
    { label: 'HOME', href: '#/', match: (x) => x.kind === 'home' },
    { label: 'MAP', href: '#/map', match: (x) => x.kind === 'map' || x.kind === 'node-map' || x.kind === 'thread-map' },
    { label: 'NEIGHBOURHOOD', href: '#/hood', match: (x) => x.kind === 'hood' || x.kind === 'node-hood' },
    { label: 'THREADS', href: '#/t/' + THREAD_IN_VIEW, match: (x) => x.kind === 'thread' },
    { label: 'TIMELINE', href: '#/timeline', match: (x) => x.kind === 'timeline' },
    { label: 'PATENTS', href: '#/patents/' + PATENT_IN_VIEW, match: (x) => x.kind === 'patents' },
    { label: 'EVIDENCE', href: '#/evidence', match: (x) => x.kind === 'evidence' },
    {
      label: 'REPORT',
      href: nid ? '#/report/n/' + nid : null,
      match: (x) => x.kind === 'report-node' || x.kind === 'report-thread',
    },
  ];
}

let fragEl: HTMLElement | null = null;
let viewEl: HTMLElement | null = null;

export function renderFrame(host: HTMLElement, r: Route): void {
  const nid = routeNodeId(r);
  if (nid) lastNodeId = nid;

  clear(host);
  const bar = h('div', { class: 'bar', role: 'banner' });

  bar.append(h('div', { class: 'wordmark' },
    h('span', { class: 'w-dim' }, 'THE '),
    h('span', { class: 'w-lit' }, 'LEGACY PROGRAM'),
    h('span', { class: 'w-dim' }, ' RESEARCH TERMINAL'),
  ));

  const nav = h('nav', { class: 'nav', 'aria-label': 'Views' });
  for (const it of items(r)) {
    if (!it.href) {
      nav.append(h('span', {
        class: 'nav-inert',
        title: 'A report is written about a node. Open a node first.',
      }, it.label));
      continue;
    }
    nav.append(h('a', {
      href: it.href,
      'aria-current': it.match(r) ? 'page' : null,
    }, it.label));
  }
  bar.append(nav);

  bar.append(h('div', { class: 'bar-search' },
    searchBox({ placeholder: 'search nodes, claims, events' })));

  fragEl = h('span', { class: 'frag' }, fragment());
  viewEl = h('span', { class: 'viewport' }, viewportLabel());
  bar.append(h('div', { class: 'bar-right' }, fragEl, viewEl));

  host.append(bar);
}

function viewportLabel(): string {
  return window.innerWidth + '×' + window.innerHeight;
}

export function refreshFrameStatus(): void {
  if (fragEl) fragEl.textContent = fragment();
  if (viewEl) viewEl.textContent = viewportLabel();
}

window.addEventListener('resize', refreshFrameStatus);
