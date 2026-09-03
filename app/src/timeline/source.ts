/* timeline/source.ts — data/timeline.json, the 912 events, fetched once.
 * Same-origin /data only. */

import type { TEvent } from './layout';

const BASE = import.meta.env.BASE_URL;

let p: Promise<TEvent[]> | null = null;

export function loadTimeline(): Promise<TEvent[]> {
  if (!p) {
    p = fetch(BASE + 'data/timeline.json').then((r) => {
      if (!r.ok) throw new Error('timeline.json -> HTTP ' + r.status);
      return r.json() as Promise<TEvent[]>;
    });
  }
  return p;
}
