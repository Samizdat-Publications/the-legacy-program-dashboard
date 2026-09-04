/* history.ts: the reader's own trail through the board.
 *
 * Stewart's condition on the new shell: a back button on every page that steps
 * backwards through the pages visited while researching, and that the browser's
 * own back does the same thing. So this module never navigates by hash and never
 * pushes an entry. It calls history.back(), and nothing else.
 *
 * All it has to work out is whether there is an in-app page to go back to, which
 * the browser will not tell you. Each entry carries its own depth in
 * history.state.tpDepth, written with replaceState so no entry is created:
 *
 *   first load          no tpDepth on the entry -> depth 0, and the button is off
 *   a link is followed  hashchange with no tpDepth -> a fresh push, depth + 1
 *   back or forward     hashchange with a tpDepth -> adopt it
 *
 * Chrome keeps history.state across a reload and across back and forward, so the
 * button is right after either. The per-depth trail of { hash, title } is kept in
 * sessionStorage for the tooltip alone, and is truncated at the current depth on
 * a fresh push, the way a browser drops the forward stack on a new branch.
 */

const KEY = 'tp.trail';
const SITE = 'The Legacy Program Research Terminal';

interface Step { hash: string; title: string }
interface Stamp { tpDepth?: number }

let trail: Step[] = [];
let depth = 0;

function readTrail(): Step[] {
  try {
    const raw = sessionStorage.getItem(KEY);
    const v: unknown = raw ? JSON.parse(raw) : null;
    return Array.isArray(v) ? (v as Step[]) : [];
  } catch { return []; }
}

function writeTrail(): void {
  try { sessionStorage.setItem(KEY, JSON.stringify(trail)); } catch { /* private mode */ }
}

function here(): string { return location.hash || '#/'; }

function stamp(d: number): void {
  const st = (history.state || {}) as Stamp;
  history.replaceState({ ...st, tpDepth: d }, '');
}

/* A page's name for the tooltip only: the document title where the page sets one,
   else the route's own label. The view's heading is deliberately not read, because
   setTitle runs before the new page has cleared the old one out of #view. */
function routeLabel(hash: string): string {
  const p = hash.replace(/^#/, '').split(/[/?]/).filter(Boolean);
  if (!p.length) return 'Home';
  switch (p[0]) {
    case 'n': return p[2] === 'map' ? 'Map' : p[2] === 'hood' ? 'Neighbourhood' : 'Node';
    case 'hood': return 'Neighbourhood';
    case 'map': return 'Map';
    case 't': return 'Thread';
    case 'timeline': return 'Timeline';
    case 'patents': return 'Patents';
    case 'evidence': return 'Evidence';
    case 'report': return 'Report';
    default: return 'Page';
  }
}

function pageTitle(): string {
  const doc = (document.title || '').trim();
  let head = doc === SITE ? '' : doc;
  const tail = ' · ' + SITE;
  if (head.endsWith(tail)) head = head.slice(0, head.length - tail.length);
  head = head.split(' · ')[0].trim();
  return head || routeLabel(here());
}

function onHash(): void {
  const st = history.state as Stamp | null;
  if (st && typeof st.tpDepth === 'number') {
    depth = st.tpDepth;                 /* the reader used back or forward */
    return;
  }
  depth = depth + 1;                    /* a fresh push, so a new branch */
  stamp(depth);
  trail = trail.slice(0, depth);
  trail[depth] = { hash: here(), title: '' };
  writeTrail();
}

export function initHistory(): void {
  const st = history.state as Stamp | null;
  if (st && typeof st.tpDepth === 'number') {
    depth = st.tpDepth;
    trail = readTrail();
  } else {
    depth = 0;
    stamp(0);
    trail = [{ hash: here(), title: '' }];
    writeTrail();
  }
  window.addEventListener('hashchange', onHash);
}

/* Called once a route has rendered, so the title it set is the one recorded. */
export function noteHere(): void {
  trail[depth] = { hash: here(), title: pageTitle() };
  writeTrail();
}

export function canGoBack(): boolean {
  return depth > 0;
}

export function previousTitle(): string {
  const prev = depth > 0 ? trail[depth - 1] : null;
  return prev && prev.title ? prev.title : '';
}

/* The only navigation this module performs. No entry is created, so the browser's
   own back button and this one do the same thing and forward still works. */
export function goBack(): void {
  if (canGoBack()) history.back();
}
