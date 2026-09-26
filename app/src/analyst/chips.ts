/* analyst/chips.ts: which suggestions belong on which route.
 *
 * The wording lives in data/analyst-suggestions.json, which tools/build_app_data.py
 * copies into app/public/data/analyst.json as a per key map. It is edited only
 * through Stewart's decisions; nothing here writes it.
 *
 * The page accepts BOTH shapes. A file with `byRoute` is read per route; a flat
 * file with only `suggestions` is read as the home list on every route. That is
 * deliberate: a reader holding a cached copy of an older data file gets the old
 * chips, never zero chips.
 */
import { loadAnalyst } from '../data';
import type { Route } from '../router';

export type ChipKey =
  | 'home' | 'node' | 'map' | 'hood' | 'thread'
  | 'timeline' | 'patents' | 'evidence' | 'report';

export const CHIP_KEYS: ChipKey[] = [
  'home', 'node', 'map', 'hood', 'thread', 'timeline', 'patents', 'evidence', 'report',
];

/* Route kind to chip key. The mapping of the plan's section 3, exactly:
   node-map and thread-map use map, node-hood uses hood, both report kinds use
   report, notfound uses home. */
export function chipKey(r: Route): ChipKey {
  switch (r.kind) {
    case 'node': return 'node';
    case 'map': case 'node-map': case 'thread-map': return 'map';
    case 'hood': case 'node-hood': return 'hood';
    case 'thread': return 'thread';
    case 'timeline': return 'timeline';
    case 'patents': return 'patents';
    case 'evidence': return 'evidence';
    case 'report-node': case 'report-thread': return 'report';
    /* the Atlas and topic pages have no chips of their own until Stewart has
       approved some (phase 12); they are front-door pages, so they get Home's */
    case 'home': case 'notfound': case 'atlas': case 'topic': case 'directory': case 'library': case 'source': return 'home';
  }
}

export async function chipsFor(r: Route): Promise<string[]> {
  const f = await loadAnalyst().catch(() => null);
  if (!f) return [];
  const key = chipKey(r);
  const byRoute = f.byRoute;
  if (byRoute && Array.isArray(byRoute[key]) && byRoute[key].length) return byRoute[key];
  if (byRoute && Array.isArray(byRoute.home) && byRoute.home.length) return byRoute.home;
  return Array.isArray(f.suggestions) ? f.suggestions : [];
}
