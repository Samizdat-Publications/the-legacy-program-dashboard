/* router.ts: the hash scheme of the Design response section 2.1, exactly.
 *
 *   #/                          home
 *   #/n/<id>                    node page
 *   #/n/<id>/hood               neighbourhood of <id>     (alias #/hood/<id>)
 *   #/hood                      neighbourhood, nothing selected
 *   #/t/<id>                    thread
 *   #/map  #/n/<id>/map  #/t/<id>/map
 *                               the program map, retired in redesign phase 11:
 *                               #/map goes to #/atlas, the other two to the node
 *                               or thread they named, so an old link still lands
 *   #/timeline                  ?era=<era>  ?scope=n:<id>|t:<id>
 *   #/patents/<number>          ?sheet=<k>
 *   #/evidence                  ?tier=&cls=&cluster=&domain=&denied=1&open=1
 *   #/report/n/<id>             #/report/t/<id>
 *   #/atlas                     the Atlas of topics (redesign phase 6)
 *   #/topic/<id>                a topic (redesign phase 6)
 *   #/people #/orgs #/programmes #/laws #/places #/events
 *                               the directories (redesign phase 9), filters in the query
 *   #/timeline                  also ?strand= ?topic= (redesign phase 9)
 *   #/library                   the Library of sources (redesign phase 8)
 *                               ?type=&issuer=&era=&ip=1|0&q=&sort=
 *   #/s/<id>                    one source (redesign phase 8)
 *
 * Anything else is not-found, and the not-found page names the route it was given.
 * Every route is shareable; back always works because every state is a hash.
 */
import { noteHere } from './history';

export type Route =
  | { kind: 'home' }
  | { kind: 'node'; id: string }
  | { kind: 'node-map'; id: string }
  | { kind: 'node-hood'; id: string }
  | { kind: 'hood' }
  | { kind: 'map'; cell: string | null }
  | { kind: 'thread'; id: string }
  | { kind: 'thread-map'; id: string }
  | { kind: 'timeline'; era: string | null; scope: string | null; strand: string | null; topic: string | null }
  | { kind: 'patents'; number: string; sheet: string | null }
  | { kind: 'evidence'; q: URLSearchParams }
  | { kind: 'report-node'; id: string }
  | { kind: 'report-thread'; id: string }
  | { kind: 'atlas' }
  | { kind: 'topic'; id: string }
  | { kind: 'directory'; dir: string; q: URLSearchParams }
  | { kind: 'library'; q: URLSearchParams }
  | { kind: 'source'; id: string }
  | { kind: 'notfound'; raw: string };

/* The six directories of redesign phase 9, by route word. */
export const DIRECTORIES = ['people', 'orgs', 'programmes', 'laws', 'places', 'events'];

/* Board ids are lower-case words joined by hyphens, sometimes with digits or a
   dot. Anything outside that shape is not an id and must not resolve. */
const ID = /^[a-z0-9][a-z0-9._-]*$/;
const NUM = /^[0-9][0-9,]*$/;

export function parseRoute(hash: string): Route {
  const raw = hash.replace(/^#/, '') || '/';
  const qi = raw.indexOf('?');
  const path = (qi < 0 ? raw : raw.slice(0, qi)).replace(/\/+$/, '') || '/';
  const q = new URLSearchParams(qi < 0 ? '' : raw.slice(qi + 1));
  const p = path.split('/').filter(Boolean);

  const bad = (): Route => ({ kind: 'notfound', raw: '#' + raw });

  if (p.length === 0) return { kind: 'home' };

  if (p[0] === 'n') {
    if (!p[1] || !ID.test(p[1])) return bad();
    if (p.length === 2) return { kind: 'node', id: p[1] };
    if (p.length === 3 && p[2] === 'map') return { kind: 'node-map', id: p[1] };
    if (p.length === 3 && p[2] === 'hood') return { kind: 'node-hood', id: p[1] };
    return bad();
  }

  if (p[0] === 'hood') {
    if (p.length === 1) return { kind: 'hood' };
    if (p.length === 2 && ID.test(p[1])) return { kind: 'node-hood', id: p[1] };
    return bad();
  }

  if (p[0] === 'map') {
    if (p.length !== 1) return bad();
    return { kind: 'map', cell: q.get('cell') };
  }

  if (p[0] === 't') {
    if (!p[1] || !ID.test(p[1])) return bad();
    if (p.length === 2) return { kind: 'thread', id: p[1] };
    if (p.length === 3 && p[2] === 'map') return { kind: 'thread-map', id: p[1] };
    return bad();
  }

  if (p[0] === 'timeline') {
    if (p.length !== 1) return bad();
    return { kind: 'timeline', era: q.get('era'), scope: q.get('scope'), strand: q.get('strand'), topic: q.get('topic') };
  }

  if (p[0] === 'patents') {
    if (p.length !== 2 || !NUM.test(p[1])) return bad();
    return { kind: 'patents', number: p[1], sheet: q.get('sheet') };
  }

  if (p[0] === 'evidence') {
    if (p.length !== 1) return bad();
    return { kind: 'evidence', q };
  }

  if (p[0] === 'atlas') {
    if (p.length !== 1) return bad();
    return { kind: 'atlas' };
  }

  if (p[0] === 'topic') {
    if (p.length !== 2 || !ID.test(p[1])) return bad();
    return { kind: 'topic', id: p[1] };
  }

  if (DIRECTORIES.indexOf(p[0]) >= 0) {
    if (p.length !== 1) return bad();
    return { kind: 'directory', dir: p[0], q };
  }

  if (p[0] === 'library') {
    if (p.length !== 1) return bad();
    return { kind: 'library', q };
  }

  if (p[0] === 's') {
    if (p.length !== 2 || !ID.test(p[1])) return bad();
    return { kind: 'source', id: p[1] };
  }

  if (p[0] === 'report') {
    if (p.length === 3 && p[1] === 'n' && ID.test(p[2])) return { kind: 'report-node', id: p[2] };
    if (p.length === 3 && p[1] === 't' && ID.test(p[2])) return { kind: 'report-thread', id: p[2] };
    return bad();
  }

  return bad();
}

/* The id a route is about, if it is about one. The frame uses it to keep the
   Report and Neighbourhood links pointed somewhere real. */
export function routeNodeId(r: Route): string | null {
  switch (r.kind) {
    case 'node': case 'node-map': case 'node-hood': case 'report-node': return r.id;
    default: return null;
  }
}

export function currentRoute(): Route {
  return parseRoute(location.hash);
}

export function fragment(): string {
  return location.hash || '#/';
}

type Handler = (r: Route) => void | Promise<void>;

export function startRouter(handler: Handler): void {
  const go = () => { void handler(currentRoute()); };
  window.addEventListener('hashchange', go);
  go();
}

export function setTitle(...parts: string[]): void {
  const suffix = 'The Legacy Program Research Terminal';
  const head = parts.filter(Boolean).join(' · ');
  document.title = head ? head + ' · ' + suffix : suffix;
  /* pages render asynchronously, so this, not the dispatch, is when the trail
     learns what to call the entry the reader is on */
  noteHere();
}
