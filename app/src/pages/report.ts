/* Report — Design response section 1.10.
 *
 * Paper colours, still monospace, sized to the viewport and printable as it
 * stands. Numbered superscripts in the body, the citations at the foot. Every
 * citation is the source string the board already carries; none is composed here.
 */
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadNode, dateRange, claimSource, type NodeRecord } from '../data';
import { notFound } from './notfound';
import { renderPending } from './pending';

export async function renderNodeReport(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  let rec: NodeRecord;
  try {
    rec = await loadNode(id);
  } catch {
    notFound(view, '#/report/n/' + id, 'No record is served for this node, so there is nothing to report on.');
    return;
  }
  const idx = await loadIndex();
  setTitle('Report', rec.label);

  /* ---- citations, numbered in the order they are first used ------------- */
  const cites: { text: string; url: string | null }[] = [];
  const cite = (text: string, url: string | null): number => {
    const i = cites.findIndex((c) => c.text === text && c.url === url);
    if (i >= 0) return i + 1;
    cites.push({ text, url });
    return cites.length;
  };
  const sup = (nn: number) => h('sup', null, String(nn));

  const paper = h('article', { class: 'report' });

  paper.append(h('div', { class: 'rhead' },
    h('span', null, 'The Legacy Program · brief · node'),
    h('span', null, '#/report/n/' + rec.id + ' · generated ' + (idx.generated || '').slice(0, 10)),
  ));

  paper.append(h('h1', null, rec.label));
  paper.append(h('div', { class: 'rmeta' },
    [rec.cls, 'Tier ' + (rec.tier || '?'),
      'custody ' + (rec.C ?? 0) + '/3', 'access ' + (rec.A ?? 0) + '/3',
      'disclosure ' + (rec.D ?? 0) + '/3', dateRange(rec.dateStart, rec.dateEnd)].join(' · ')));

  const why = (rec.dossier && (rec.dossier.whyImplicated || rec.dossier.narrative)) || rec.desc || '';
  if (why) {
    const nn = cite('Dossier narrative · data/the-program.json · node ' + rec.id, null);
    paper.append(h('p', { class: 'rnarr' }, why, ' ', sup(nn)));
  }

  const claims = (rec.claims || []).slice().sort((a, b) => Number(a.tier) - Number(b.tier));
  if (claims.length) {
    paper.append(h('h2', null, 'Claims by tier'));
    const ol = h('ol', { class: 'rclaims' });
    for (const c of claims) {
      const src = claimSource(c.source);
      const nn = cite(src.text || 'no source recorded on this claim', src.url);
      ol.append(h('li', null,
        h('span', { class: 'rtier n' + c.tier }, 'T' + c.tier), ' ', c.text, ' ', sup(nn)));
    }
    paper.append(ol);
  }

  if (rec.denials.length) {
    paper.append(h('h2', null, 'Denials on the record'));
    for (const d of rec.denials) {
      const s = (d.sources || [])[0];
      const nn = cite(s ? (s.name || s.url || '') : (d.note || 'denial recorded on the edge, no source string'),
        (s && s.url) || null);
      paper.append(h('div', { class: 'rdenial' },
        h('b', null, d.by.label), ' — ', d.label || d.note || '', ' ', sup(nn)));
    }
  }

  if (rec.connections.length) {
    paper.append(h('h2', null, 'Sourced connections (' + rec.connections.length + ')'));
    const cols = h('div', { class: 'rconns' });
    const ordered = [...rec.connections.filter((c) => c.l0), ...rec.connections.filter((c) => !c.l0)];
    for (const c of ordered) {
      cols.append(h('div', null,
        /* the id is a route, so the brief is navigable and C1 has something to
           check on this page; it still prints as its own label on paper */
        h('a', { href: '#/n/' + c.id }, c.label), ' ',
        h('span', { class: 'cm' }, '· ' + (c.l0 ? c.type : 'member') + ' · T' + (c.claimTier ?? '?')),
      ));
    }
    paper.append(cols);
  }

  const cl = h('div', { class: 'rcites' });
  cl.append(h('h2', null, 'Citations'));
  cites.forEach((c, i) => {
    cl.append(h('div', null,
      h('span', { class: 'cn' }, String(i + 1)), ' ',
      c.url ? h('a', { href: c.url, target: '_blank', rel: 'noreferrer noopener' }, c.text || c.url) : c.text,
    ));
  });
  paper.append(cl);

  view.append(h('div', { class: 'report-wrap' }, paper));
}

export function renderThreadReport(view: HTMLElement, id: string): void {
  renderPending(view, 'thread', 'A thread report (#/report/t/' + id + ') is built with the threads, in phase 3.');
}
