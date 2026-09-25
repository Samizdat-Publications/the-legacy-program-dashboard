/* Node page: Design response section 1.3, and redesign phase 1.
 *
 * Header, the three axes as 3-cell bars, the roles, the three actions, what it
 * is and why it matters, the case against (conflicts, unverified notes, denial
 * posture), the claims grouped by tier each with its source as a link, the
 * denials, the timeline slice, every open question, the chronology, the
 * affiliations, the node's own sources, and the right column of sourced
 * connections grouped by relationship, each with its own sentence.
 *
 * Nothing on this page is written here. Every string comes from the node record.
 */
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import {
  loadIndex, loadNode, clsColour, dateRange, claimSource, asList,
  type NodeRecord, type IndexNode,
} from '../data';
import { notFound } from './notfound';
import { groupConnections, renderConnGroups } from './connections';

const AXES: [keyof Pick<NodeRecord, 'C' | 'A' | 'D'>, string][] = [
  ['C', 'custody proximity'],
  ['A', 'access'],
  ['D', 'disclosure role'],
];

export async function renderNode(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  const idx = await loadIndex();
  const meta: IndexNode | undefined = idx.nodes.find((x) => x.id === id);

  let rec: NodeRecord;
  try {
    rec = await loadNode(id);
  } catch {
    notFound(view, '#/n/' + id, meta
      ? 'The board carries this node, but its record is not served on this deployment yet: data/nodes/' + id + '.json'
      : 'No node with this id is on the board.');
    return;
  }
  setTitle(rec.label);

  const wrap = h('div', { class: 'node' });
  const main = h('div', { class: 'node-main' });
  const side = h('div', { class: 'node-side' });
  const third = h('div', { class: 'node-third' });
  wrap.append(main, side, third);
  view.append(wrap);

  /* ---- header ----------------------------------------------------------- */
  const crumbL = h('div', { class: 'crumb-l' },
    h('span', { style: 'color:' + clsColour(rec.cls), 'class': 'eyebrow' }, rec.cls),
    h('span', { class: 'sep' }, '·'),
    h('span', { class: 'dim' }, dateRange(rec.dateStart, rec.dateEnd)),
  );
  const crumbR = h('div', null,
    meta && meta.hl
      ? h('span', null, h('span', { class: 'amber eyebrow' }, 'Start here'), ' ',
          h('span', { class: 'sep' }, '·'), ' ', h('span', { class: 'amber' }, String(meta.hl)))
      : null,
  );
  main.append(h('div', { class: 'crumb' }, crumbL, crumbR));
  main.append(h('h1', { class: 'node-h1' }, rec.label));

  /* ---- axes: position, never size --------------------------------------- */
  const axes = h('div', { class: 'axes' });
  for (const [key, label] of AXES) {
    const v = Number(rec[key] ?? 0);
    const cells = h('span', { class: 'cells' });
    for (let i = 1; i <= 3; i++) cells.append(h('span', { class: 'cell' + (i <= v ? ' on' : '') }));
    axes.append(h('span', { class: 'axis' }, label, cells, h('span', { class: 'num' }, v + '/3')));
  }
  const roles = (rec.dossier && rec.dossier.roles) || [];
  if (roles.length) {
    const rc = h('span', { class: 'roles' });
    for (const r of roles) rc.append(h('span', { class: 'role' }, r));
    axes.append(rc);
  }
  main.append(axes);

  /* ---- the three actions ------------------------------------------------ */
  main.append(h('div', { class: 'actions' },
    h('a', { class: 'act key', href: '#/n/' + rec.id + '/map' }, 'SHOW ON THE MAP'),
    h('a', { class: 'act key', href: '#/n/' + rec.id + '/hood' }, 'OPEN THE NEIGHBOURHOOD'),
    h('a', { class: 'act', href: '#/report/n/' + rec.id }, 'REPORT'),
    h('span', { class: 'idline' },
      'id ' + rec.id +
      (meta ? ' · degree ' + meta.deg + ' distinct neighbours' : '') +
      (rec.members ? ' · ' + rec.members.length + ' members' : '')),
  ));

  /* ---- about: what it is, why it matters, and the case against ----------- */
  /* tierRationale is machine-generated and explains the tier letter this page no
     longer prints; it stays in the data for the analyst. */
  const what = rec.dossier && rec.dossier.whatItIs;
  const why = (rec.dossier && (rec.dossier.whyImplicated || rec.dossier.narrative)) || rec.desc || rec.narrative || '';
  if (what || why) {
    main.append(h('div', { class: 'sec eyebrow' }, 'About'));
    if (what) main.append(h('div', { class: 'narrative' }, h('p', null, what)));
    if (why) main.append(h('div', { class: 'narrative' }, h('p', null, why)));
  }
  for (const c of asList(rec.conflicts)) {
    main.append(h('div', { class: 'narrative', style: 'margin-top:8px' },
      h('p', null, h('span', { class: 'red eyebrow' }, 'Conflict on the record '), c)));
  }
  for (const u of asList(rec.unverified)) {
    main.append(h('div', { class: 'narrative unv', style: 'margin-top:8px' },
      h('p', null, h('span', { class: 'amber eyebrow' }, 'Not verified '), u)));
  }
  const posture = rec.dossier && rec.dossier.denialPosture;
  if (posture) {
    main.append(h('div', { class: 'narrative dim', style: 'margin-top:8px' },
      h('p', null, h('span', { class: 'eyebrow' }, 'Denial posture '), posture)));
  }

  /* ---- claims, grouped by tier ------------------------------------------ */
  const claims = rec.claims || [];
  const byTier: Record<number, typeof claims> = { 1: [], 2: [], 3: [] };
  for (const c of claims) {
    const t = Number(c.tier);
    if (byTier[t]) byTier[t].push(c);
  }
  main.append(h('div', { class: 'sec sechead' },
    h('div', null,
      h('span', { class: 'eyebrow' }, 'Claims'), ' ',
      h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(claims.length)),
      '   ',
      h('span', { class: 't1' }, 'Tier 1 · ' + byTier[1].length), '  ',
      h('span', { class: 't2' }, 'Tier 2 · ' + byTier[2].length), '  ',
      h('span', { class: 't3' }, 'Tier 3 · ' + byTier[3].length),
    ),
    h('span', { class: 'faint' }, 'each claim → its source, as a link'),
  ));
  const list = h('div', { class: 'claims' });
  for (const tier of [1, 2, 3]) {
    for (const c of byTier[tier]) {
      const src = claimSource(c.source);
      list.append(h('div', { class: 'claim' },
        h('span', { class: 'ct t' + tier }, 'T' + tier),
        h('span', { class: 'ctext' }, c.text),
        src.url
          ? h('a', { class: 'csrc', href: src.url, target: '_blank', rel: 'noreferrer noopener', title: src.text }, 'source ↗')
          : h('span', { class: 'csrc nolink', title: src.text }, src.text ? 'source, not a link' : 'no source recorded'),
      ));
    }
  }
  main.append(list);

  /* ---- denials on the record -------------------------------------------- */
  if (rec.denials.length) {
    main.append(h('div', { class: 'sec' },
      h('span', { class: 'red eyebrow' }, 'Denials on the record'), ' ',
      h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(rec.denials.length))));
    const dl = h('div', { class: 'denials' });
    for (const d of rec.denials) {
      const other = d.by.id === rec.id ? d.of : d.by;
      dl.append(h('div', { class: 'denial' },
        h('span', null,
          h('a', { href: '#/n/' + other.id }, other.label), ' ',
          h('span', null, d.label || d.note || '')),
        h('span', { class: 'dim' },
          'T' + (d.claimTier ?? '?') + ' · ' + (d.denialKind || (d.by.id === rec.id ? 'issued here' : 'directed here'))),
      ));
    }
    main.append(dl);
  }

  /* ---- timeline slice and FOIA ------------------------------------------ */
  const extra = h('div', { class: 'twocol' });

  const slice = h('div', null);
  slice.append(h('div', { class: 'sec' },
    h('span', { class: 'eyebrow' }, 'Timeline slice'), ' ',
    h('span', { class: 'sep dim' }, '· ' + dateRange(rec.dateStart, rec.dateEnd))));
  const events = rec.timeline.slice().sort((a, b) => String(a.date).localeCompare(String(b.date)));
  if (events.length) {
    const sl = h('div', { class: 'slice' });
    for (const e of events) {
      sl.append(h('div', { class: 'ev' },
        mark(clsColour(rec.cls)),
        h('span', { class: 'yr' }, String(e.date).slice(0, 4)),
        h('span', { class: 'label' }, e.label),
      ));
    }
    slice.append(sl);
  }
  /* neighbours by start date, as the mockup's slice does when the node itself
     carries few events */
  const neigh = rec.connections
    .filter((c) => c.l0 && c.dateStart)
    .sort((a, b) => String(a.dateStart).localeCompare(String(b.dateStart)));
  if (neigh.length) {
    slice.append(h('div', { class: 'faint', style: 'margin-top:8px' }, 'map neighbours by start date'));
    const sl2 = h('div', { class: 'slice' });
    for (const c of neigh) {
      sl2.append(h('div', { class: 'ev' },
        mark(clsColour(c.cls)),
        h('span', { class: 'yr' }, String(c.dateStart).slice(0, 4)),
        h('a', { href: '#/n/' + c.id }, c.label),
      ));
    }
    slice.append(sl2);
  }
  extra.append(slice);

  const foia = h('div', null);
  const openQ = (rec.dossier && rec.dossier.openQuestions) || [];
  const reqs = rec.foia.requests || [];
  foia.append(h('div', { class: 'sec' },
    h('span', { class: 'eyebrow' }, 'Open questions'), ' ',
    h('span', { class: 'sep dim' }, '· ' + openQ.length +
      (reqs.length ? ' · ' + reqs.length + ' FOIA request' + (reqs.length === 1 ? '' : 's') + ' drafted' : ''))));
  if (openQ.length) {
    /* a request's `questions` are indices into the dossier's own open questions */
    const fl = h('div', { class: 'foia' });
    openQ.forEach((text, qi) => {
      const closing = reqs.find((r) => (r.questions || []).includes(qi));
      fl.append(h('div', { class: 'q oq' },
        h('span', null, text),
        h('span', { class: 'rq' }, closing ? closing.request + (closing.status ? ' · ' + closing.status : '') : 'no request drafted'),
      ));
    });
    foia.append(fl);
  } else {
    foia.append(h('div', { class: 'faint' }, 'no open question is recorded against this node'));
  }
  for (const r of reqs) {
    foia.append(h('div', { class: 'q' },
      h('span', { class: 'dim' }, (r.agency ? r.agency + ' - ' : '') + (r.title || '')),
      h('span', { class: 'rq' }, r.request + (r.status ? ' · ' + r.status : '')),
    ));
  }
  extra.append(foia);

  (window.innerWidth >= 2200 ? third : main).append(extra);

  /* ---- chronology, affiliations and the node's own sources --------------- */
  const seen = new Set<string>();
  const chron = [...(rec.chronology || []), ...(rec.sequenceChain || [])]
    .filter((e) => {
      const k = String(e.date) + '|' + String(e.event || '').trim().toLowerCase();
      if (seen.has(k)) return false;
      seen.add(k); return true;
    })
    .sort((a, b) => String(a.date).localeCompare(String(b.date)));
  if (chron.length) {
    main.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Chronology'), ' ',
      h('span', { class: 'sep dim' }, '· ' + chron.length)));
    const cl = h('div', { class: 'slice chron' });
    for (const e of chron) {
      cl.append(h('div', { class: 'ev' }, mark(clsColour(rec.cls)),
        h('span', { class: 'yr' }, String(e.date).slice(0, 4)), h('span', { class: 'label' }, e.event)));
    }
    main.append(cl);
  }
  const affs = rec.affiliations || [];
  if (affs.length) {
    main.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Affiliations'), ' ',
      h('span', { class: 'sep dim' }, '· ' + affs.length)));
    const al = h('div', { class: 'affs' });
    for (const a of affs) al.append(h('div', { class: 'aff' }, a));
    main.append(al);
  }
  const nsrc = rec.sources || [];
  if (nsrc.length) {
    const d = h('details', { class: 'nsrcs' }, h('summary', { class: 'eyebrow' }, 'Sources on file · ' + nsrc.length));
    for (const s of nsrc) {
      const text = (s.name || s.url || '') + (s.date ? ' (' + s.date + ')' : '');
      d.append(s.url ? h('a', { class: 'nsrc', href: s.url, target: '_blank', rel: 'noreferrer noopener' }, text)
        : h('span', { class: 'nsrc' }, text));
    }
    main.append(d);
  }

  /* ---- right column: sourced connections, grouped by relationship -------- */
  const groups = groupConnections(rec.connections);
  const counterparts = new Set(rec.connections.map((c) => c.id)).size;
  side.append(h('div', { class: 'crumb', style: 'margin-bottom:6px' },
    h('span', { class: 'eyebrow' }, 'Sourced connections'),
    h('span', { class: 'dim' }, rec.connections.length + ' links · ' + counterparts + ' counterparts · ' + groups.length + ' kinds')));
  side.append(renderConnGroups(groups));
}
