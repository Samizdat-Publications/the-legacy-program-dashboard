/* sources.ts: how every surface prints a claim's source and a web address
 * (redesign phase 8).
 *
 * A claim's source is a link to its page in the Library, #/s/<id>, named by the
 * registry's title for it and the claim's own locator ("p.4", "Sec. 7343"). The
 * source page carries the external URL, its archived copies and everything else
 * that cites it. The claim's original source string is never dropped: it is the
 * link's title, and a claim the registry does not resolve prints it as written.
 *
 * A web address is printed with a break opportunity (<wbr>) after each / ? & = # -
 * and before each . _ that follows a letter or digit, plus one inside any run of
 * more than RUN characters with no such point (a hash, a base64 id). The element
 * carries class `url`, whose CSS sets `overflow-wrap: normal; word-break: normal`,
 * so a line only ever breaks at those points: never mid-word, never off the edge.
 * C45 reads the computed style and the break points on the real page.
 */
import { h } from './dom';
import type { SourceRef } from './data';

const RUN = 22;

export function urlText(u: string, cls = 'url'): HTMLElement {
  const el = h('span', { class: cls });
  let run = 0;
  let buf = '';
  const flush = () => { if (buf) { el.append(buf); buf = ''; } };
  const brk = () => { flush(); el.append(document.createElement('wbr')); run = 0; };
  for (let i = 0; i < u.length; i++) {
    const ch = u[i];
    if ((ch === '.' || ch === '_') && i > 0 && /[A-Za-z0-9]/.test(u[i - 1]) && run > 0) brk();
    buf += ch;
    run++;
    /* after a hyphen, where the browser would break a line anyway */
    if (ch === '/' || ch === '?' || ch === '&' || ch === '=' || ch === '#' || ch === '-') brk();
    else if (run >= RUN) brk();
  }
  flush();
  return el;
}

/* Text that may carry web addresses: the addresses become breakable, the rest is
   left as it is. */
export function textWithUrls(s: string): (string | HTMLElement)[] {
  const out: (string | HTMLElement)[] = [];
  const re = /https?:\/\/[^\s"'<>|)\]]+/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(s))) {
    if (m.index > last) out.push(s.slice(last, m.index));
    out.push(urlText(m[0]));
    last = m.index + m[0].length;
  }
  if (last < s.length) out.push(s.slice(last));
  return out;
}

/* A demotion note merge.py writes onto a claim's source string. The link names
   the source; the note must stay visible beside it. */
const DEMOTED = /DEMOTED from Tier 1 \(([^)]*)\)/;

/* A claim's sources: one link per registry source, or the string as written when
   the registry does not resolve it. `cls` is the per-surface class of each item
   (node page `csrc`, topic `cite-src`, evidence `ev-src`). */
export function claimSourceItems(refs: SourceRef[] | undefined, original: string,
  unresolved: string | null | undefined, cls: string): HTMLElement[] {
  const out: HTMLElement[] = [];
  for (const r of refs || []) {
    out.push(h('a', { class: cls + ' src-link', href: '#/s/' + r.id, 'data-sid': r.id, title: original || r.title },
      r.title, r.locator ? h('span', { class: 'src-loc' }, ', ' + r.locator) : null));
  }
  if (!out.length) {
    out.push(h('span', {
      class: cls + ' nolink', 'data-unresolved': unresolved || 'no source recorded', title: original,
    }, original ? 'source: ' : 'no source recorded', ...(original ? textWithUrls(original) : [])));
  } else {
    const d = DEMOTED.exec(original || '');
    if (d) out.push(h('span', { class: cls + '-note src-demoted' }, 'demoted from Tier 1: ' + d[1]));
  }
  return out;
}

export const TYPE_LABEL: Record<string, string> = {
  'document': 'document', 'hearing record': 'hearing record', 'statute': 'statute',
  'regulation': 'regulation', 'report': 'report', 'article': 'article', 'book': 'book',
  'broadcast': 'broadcast', 'transcript': 'transcript', 'web page': 'web page',
  'archive index': 'archive index',
};

/* A {name, url} source's date as printed. The research wrote a bare year as
   YYYY-01-01 in places ("USAF, The Roswell Report (1995)" dated 1995-01-01);
   printing the invented day would state a precision the record does not have,
   so a first of January prints as its year. */
export function sourceDate(d: string | null | undefined): string {
  if (!d) return '';
  return /^\d{4}-01-01$/.test(d) ? d.slice(0, 4) : d;
}

/* The capture date of a Wayback address, as a date, or null. */
export function captured(u: string): string | null {
  const m = /web\.archive\.org\/web\/(\d{4})(\d{2})(\d{2})/.exec(u);
  return m ? m[1] + '-' + m[2] + '-' + m[3] : null;
}
