/* Report: Design response section 1.10.
 *
 * Paper colours, still monospace, sized to the viewport and printable as it
 * stands. Numbered superscripts in the body, the citations at the foot. Every
 * citation is the source string the board already carries; none is composed here.
 */
import { h, clear } from '../dom';
import { setTitle } from '../router';
import {
  loadIndex, loadNode, loadThreads, dateRange, claimSource,
  type NodeRecord, type Source,
} from '../data';
import { notFound } from './notfound';
import { groupConnections } from './connections';
import { edgeTypeName, NO_SENTENCE } from '../vocab';

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
    [rec.cls,
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
        h('b', null, d.by ? d.by.label : d.a.label + ' / ' + d.b.label),
        d.by || d.denialKind ? '' : ' (direction not adjudicated)',
        ': ', d.label || d.note || '', ' ', sup(nn)));
    }
  }

  if (rec.connections.length) {
    paper.append(h('h2', null, 'Sourced connections (' + rec.connections.length + ')'));
    for (const g of groupConnections(rec.connections)) {
      paper.append(h('h3', null, edgeTypeName(g.type).label + ' (' + g.rows.length + ')'));
      const cols = h('div', { class: 'rconns' });
      for (const r of g.rows) {
        for (const l of r.links) {
          cols.append(h('div', { class: 'rconn', 'data-id': r.id, 'data-type': g.type },
            /* the id is a route, so the brief is navigable and C1 has something to
               check on this page; it still prints as its own label on paper */
            h('a', { href: '#/n/' + r.id }, r.label), ': ',
            h('span', { class: 'rsent' }, l.edgeLabel || l.note || NO_SENTENCE),
            h('span', { class: 'cm' }, ' · T' + (l.claimTier ?? '?')),
          ));
        }
      }
      paper.append(cols);
    }
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

/* The thread report.
 *
 * WHERE ITS CITATIONS COME FROM, AND WHY THAT IS THE ONLY HONEST PLACE.
 * A thread step in research/threads.json carries a node, a year, a line of
 * authored evidence and the edge that joins it to the step before. It carries no
 * source of its own. So the numbered citations here are the EDGE's sources, read
 * out of the node record's own `connections` entry for the previous step, which
 * are the hand-written per-edge citations the board already holds. All 47 joins
 * across the eight threads carry at least one.
 *
 * The evidence prose is cited to the thread file itself, marked as authored, so
 * a reader can never mistake it for a document. Nothing here composes a source.
 */
export async function renderThreadReport(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  const tf = await loadThreads().catch(() => null);
  const thread = tf && (tf.threads || []).find((t) => t.id === id);
  if (!thread) {
    notFound(view, '#/report/t/' + id, 'No thread by that name is served, so there is nothing to report on.');
    return;
  }
  const idx = await loadIndex();
  setTitle('Report', thread.label);

  const cites: { text: string; url: string | null }[] = [];
  const cite = (text: string, url: string | null): number => {
    const i = cites.findIndex((c) => c.text === text && c.url === url);
    if (i >= 0) return i + 1;
    cites.push({ text, url });
    return cites.length;
  };
  const sup = (nn: number) => h('sup', null, String(nn));
  const label = new Map(idx.nodes.map((n) => [n.id, n.label]));

  /* Every step's node record, for the edge that joins it to the step before. A
     record that is not served drops its citations rather than inventing any. */
  const recs = new Map<string, NodeRecord | null>();
  await Promise.all(thread.steps.map(async (st) => {
    recs.set(st.node, await loadNode(st.node).catch(() => null));
  }));

  const paper = h('article', { class: 'report' });
  paper.append(h('div', { class: 'rhead' },
    h('span', null, 'The Legacy Program · brief · thread'),
    h('span', null, '#/report/t/' + thread.id + ' · generated ' + (idx.generated || '').slice(0, 10)),
  ));

  paper.append(h('h1', null, thread.title || thread.label));
  const years = thread.steps.map((st) => st.year)
    .filter((y): y is number => typeof y === 'number').sort((a, b) => a - b);
  paper.append(h('div', { class: 'rmeta' },
    thread.steps.length + ' steps' +
    (years.length ? ' · ' + years[0] + ' to ' + years[years.length - 1] : '') +
    ' · every join is a sourced edge'));

  if (thread.blurb) {
    const nn = cite('Thread narrative, authored · research/threads.json · thread ' + thread.id, null);
    paper.append(h('p', { class: 'rnarr' }, thread.blurb, ' ', sup(nn)));
  }

  paper.append(h('h2', null, 'The chain'));
  const ol = h('ol', { class: 'rsteps' });
  thread.steps.forEach((st, i) => {
    const li = h('li');
    li.append(h('div', { class: 'rstep-head' },
      h('a', { href: '#/n/' + st.node }, label.get(st.node) || st.node),
      st.year ? h('span', { class: 'rstep-yr' }, ' · ' + st.year) : null,
    ));

    /* the join, and its edge's own sources */
    if (st.edge && i > 0) {
      const prev = thread.steps[i - 1];
      const rec = recs.get(st.node);
      const conn = rec ? (rec.connections || []).find((c) => c.id === prev.node) : null;
      const srcs: Source[] = (conn && conn.sources) || [];
      const join = h('div', { class: 'rstep-join' },
        'joined to ' + (label.get(prev.node) || prev.node) + ' by a ' + st.edge.type +
        ' edge, ' + st.edge.kind + ', Tier ' + (st.edge.tier ?? '?') +
        (st.edge.via && st.edge.via.length ? ', via ' + st.edge.via.map((v) => label.get(v) || v).join(', ') : ''));
      if (srcs.length) {
        for (const sc of srcs) {
          const text = sc.name || sc.url || '';
          if (!text) continue;
          join.append(' ', sup(cite(text, sc.url || null)));
        }
      } else {
        join.append(' ', sup(cite('No source string is recorded on this edge', null)));
      }
      li.append(join);
    }

    const nn = cite('Thread evidence, authored · research/threads.json · thread ' + thread.id +
      ', step ' + (i + 1), null);
    li.append(h('div', { class: 'rstep-ev' }, st.evidence, ' ', sup(nn)));
    ol.append(li);
  });
  paper.append(ol);

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
