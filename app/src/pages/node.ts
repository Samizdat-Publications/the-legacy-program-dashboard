/* Node page: Design response section 1.3, and redesign phase 1.
 *
 * Header, the three axes as 3-cell bars, the roles, the actions, what it
 * is and why it matters, the case against (conflicts, unverified notes, denial
 * posture), the claims grouped by tier each with its source as a link, the
 * denials, the timeline slice, every open question, the chronology, the
 * affiliations, the node's own sources, and the right column of sourced
 * connections grouped by relationship, each with its own sentence.
 *
 * Nothing on this page is written here. Every string comes from the node record.
 */
import { claimSourceItems, textWithUrls, sourceLine } from '../sources';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import {
  loadIndex, loadNode, loadTopics, clsColour, dateRange, claimSource, asList,
  type NodeRecord, type IndexNode, type TopicsFile,
} from '../data';
import { notFound } from './notfound';
import { groupConnections, renderConnGroups } from './connections';
import { saidKind, saidMark, saidKey } from '../attrib';

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
  const tf: TopicsFile | null = await loadTopics().catch(() => null);
  const topicTitle = new Map((tf ? tf.topics : []).map((t) => [t.id, t.title]));

  const wrap = h('div', { class: 'node' });
  const main = h('div', { class: 'node-main' });
  const side = h('div', { class: 'node-side' });
  const third = h('div', { class: 'node-third' });
  wrap.append(main, side, third);
  view.append(wrap);

  /* ---- an absorbed domain node points at its topic, before anything else --
     (phase 6: the redirect the plan intends, done as a visible pointer so a
     shared old link still shows the node) */
  const absorbedBy = (rec as NodeRecord & { absorbedBy?: string }).absorbedBy;
  if (absorbedBy) {
    main.append(h('div', { class: 'absorbed' },
      h('span', { class: 'amber eyebrow' }, 'Now a topic'),
      h('span', null, 'The board has folded this entry into a topic, where its claims, its links and the case ' +
        'for and against are gathered: '),
      h('a', { href: '#/topic/' + absorbedBy }, (topicTitle.get(absorbedBy) || absorbedBy) + ' ›')));
  }

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
    for (let i = 1; i <= 3; i++) cells.append(h('span', { class: 'acell' + (i <= v ? ' on' : '') }));
    axes.append(h('span', { class: 'axis' }, label, cells, h('span', { class: 'num' }, v + '/3')));
  }
  const roles = (rec.dossier && rec.dossier.roles) || [];
  if (roles.length) {
    const rc = h('span', { class: 'roles' });
    for (const r of roles) rc.append(h('span', { class: 'role' }, r));
    axes.append(rc);
  }
  main.append(axes);

  /* ---- the actions ------------------------------------------------------ */
  main.append(h('div', { class: 'actions' },
    h('a', { class: 'act key', href: '#/n/' + rec.id + '/hood' }, 'OPEN THE NEIGHBOURHOOD'),
    h('a', { class: 'act', href: '#/report/n/' + rec.id }, 'REPORT'),
    h('span', { class: 'idline' },
      meta ? meta.deg + ' distinct neighbours on the board' : ''),
  ));

  /* ---- appears in: the topics this node belongs to, primary first ---------- */
  const inTopics = (tf && tf.appearsIn[rec.id]) || [];
  if (inTopics.length) {
    /* a phone shows three before the control, so the case against stays near the top */
    const SHOW = window.innerWidth <= 760 ? 3 : 6;
    const row = h('div', { class: 'appears' },
      h('span', { class: 'eyebrow' }, 'Appears in ' + inTopics.length + (inTopics.length === 1 ? ' topic' : ' topics')));
    const chips = h('div', { class: 'appears-chips' });
    inTopics.forEach(([tid, role, anchor], i) => {
      chips.append(h('a', {
        class: 'appears-chip' + (i >= SHOW ? ' extra' : '') + (anchor ? ' anchor' : ''),
        href: '#/topic/' + tid, 'data-role': role,
        title: anchor ? 'a principal subject of this topic' : 'a member of this topic',
      }, h('span', { class: 'label' }, topicTitle.get(tid) || tid), h('span', { class: 'faint' }, ' · ' + role)));
    });
    if (inTopics.length > SHOW) {
      const more = h('button', { type: 'button', class: 'appears-more', 'aria-expanded': 'false' },
        'show all ' + inTopics.length);
      more.addEventListener('click', () => {
        const open = row.classList.toggle('open');
        more.setAttribute('aria-expanded', open ? 'true' : 'false');
        more.textContent = open ? 'show fewer' : 'show all ' + inTopics.length;
      });
      chips.append(more);
    }
    row.append(chips);
    main.append(row);
  }

  /* ---- about: what it is, and the board's own analysis, folded ----------- */
  /* tierRationale is machine-generated and explains the tier letter this page no
     longer prints; it stays in the data for the analyst.
     The long prose is the board's own analysis, not a record, so it is labelled
     as such and folded to its first lines behind a control (blind critic round
     0, item 5). Folding hides nothing from the DOM: every word is still here. */
  const what = rec.dossier && rec.dossier.whatItIs;
  const why = (rec.dossier && (rec.dossier.whyImplicated || rec.dossier.narrative)) || rec.desc || rec.narrative || '';
  if (what || why) {
    main.append(h('div', { class: 'sec eyebrow' }, 'About'));
    if (what) main.append(h('div', { class: 'narrative lead' }, h('p', null, what)));
    if (why) main.append(analysis(why));
  }

  /* ---- the case against: conflicts, unverified notes, the denial posture --- */
  /* It sits where the first screen can see it: its own column at 1600 and
     wider, the top of the right column on a laptop, and straight after the
     About lead on a phone. Where it goes is decided once, at render, as the
     slice and open questions already are. */
  const conflicts = asList(rec.conflicts);
  const unverified = asList(rec.unverified);
  const posture = rec.dossier && rec.dossier.denialPosture;
  const against = h('section', { class: 'against' });
  if (conflicts.length || unverified.length || posture) {
    const bits: string[] = [];
    if (conflicts.length) bits.push(conflicts.length + (conflicts.length === 1 ? ' conflict' : ' conflicts'));
    if (unverified.length) bits.push(unverified.length + ' not verified');
    if (posture) bits.push('denial posture');
    against.append(h('div', { class: 'against-head' },
      h('span', { class: 'red eyebrow' }, 'The case against'), ' ',
      h('span', { class: 'sep' }, '·'), ' ', h('span', { class: 'dim' }, bits.join(' · '))));
    for (const c of conflicts) {
      against.append(h('div', { class: 'against-row cnf' },
        h('span', { class: 'red eyebrow' }, 'Conflict on the record'), h('span', null, c)));
    }
    for (const u of unverified) {
      against.append(h('div', { class: 'against-row unv' },
        h('span', { class: 'amber eyebrow' }, 'Not verified'), h('span', null, u)));
    }
    if (posture) {
      against.append(h('div', { class: 'against-row posture' },
        h('span', { class: 'eyebrow' }, 'Denial posture'), h('span', null, posture)));
    }
    const vw = window.innerWidth;
    if (vw >= 1600) { wrap.classList.add('with-against'); wrap.insertBefore(against, side); }
    else if (vw > 760) side.append(against);
    else main.append(against);
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
      h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(claims.length)), ' in all ',
      h('span', { class: 'sep' }, '·'), ' ',
      h('span', { class: 't1' }, byTier[1].length + ' at Tier 1'), ' ', h('span', { class: 'sep' }, '·'), ' ',
      h('span', { class: 't2' }, byTier[2].length + ' at Tier 2'), ' ', h('span', { class: 'sep' }, '·'), ' ',
      h('span', { class: 't3' }, byTier[3].length + ' at Tier 3'),
    ),
    h('span', { class: 'faint' }, 'each claim with its source; a linked source opens its page in the Library'),
  ));
  /* the key to the mark, where the page carries one (attrib.ts) */
  const kinds = new Set(claims.map((c) => { const s = claimSource(c.source); return saidKind(Number(c.tier), c.text, s.text, s.url); }).filter(Boolean));
  const key = saidKey(kinds);
  if (key) main.append(key);
  const list = h('div', { class: 'claims' });
  for (const tier of [1, 2, 3]) {
    for (const c of byTier[tier]) {
      const src = claimSource(c.source);
      /* phase 8: the source is a link to its page in the Library, which carries the
         external URL; a claim the registry does not resolve keeps its string */
      list.append(h('div', { class: 'claim', 'data-cid': (c as { id?: string }).id || null },
        h('span', { class: 'ct t' + tier }, 'T' + tier),
        h('span', { class: 'ctext' }, saidMark(saidKind(tier, c.text, src.text, src.url)), c.text),
        h('span', { class: 'csrcs' }, ...claimSourceItems(c.sources, src.text, c.unresolved, 'csrc')),
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
      /* A direction is printed only where the adjudication names the denier.
         An edge it has not reached says so; it is never given one by guessing
         from the order its ends were written in (redesign phase 3). */
      const other = d.by && d.of
        ? (d.by.id === rec.id ? d.of : d.by)
        : (d.a.id === rec.id ? d.b : d.a);
      const adjudicated = !!d.denialKind;
      const how = d.by
        ? (d.denialKind || (d.by.id === rec.id ? 'issued here' : 'directed here'))
        : (d.denialKind || 'direction not adjudicated');
      dl.append(h('div', { class: 'denial', 'data-adjudicated': adjudicated ? 'yes' : 'no' },
        h('span', null,
          h('a', { href: '#/n/' + other.id }, other.label), ' ',
          h('span', null, d.label || d.note || '')),
        h('span', { class: 'dim dkind' }, 'T' + (d.claimTier ?? '?') + ' · ' + how),
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
  /* The "map neighbours by start date" list that stood here listed the
     neighbours that were on the program map; it went with the map in phase 11.
     Every neighbour is on the neighbourhood page, grouped by relationship. */
  extra.append(slice);

  const foia = h('div', null);
  /* the dossier's open questions first, because FOIA request indices point into
     them; then the node's own (an entity's, carried since phase 3) */
  const dossierQ = (rec.dossier && rec.dossier.openQuestions) || [];
  const openQ = [...dossierQ, ...(rec.openQuestions || [])];
  const reqs = rec.foia.requests || [];
  foia.append(h('div', { class: 'sec' },
    h('span', { class: 'eyebrow' }, 'Open questions'), ' ',
    h('span', { class: 'sep dim' }, '· ' + openQ.length +
      (reqs.length ? ' · ' + reqs.length + ' FOIA request' + (reqs.length === 1 ? '' : 's') + ' drafted' : ''))));
  if (openQ.length) {
    /* a request's `questions` are indices into the dossier's own open questions */
    const fl = h('div', { class: 'foia' });
    openQ.forEach((text, qi) => {
      const closing = qi < dossierQ.length ? reqs.find((r) => (r.questions || []).includes(qi)) : undefined;
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
      const text = sourceLine(s.name || s.url || '', s.date);
      d.append(s.url ? h('a', { class: 'nsrc', href: s.url, target: '_blank', rel: 'noreferrer noopener' }, ...textWithUrls(text))
        : h('span', { class: 'nsrc' }, ...textWithUrls(text)));
    }
    main.append(d);
  }

  /* ---- right column: sourced connections, grouped by relationship family --- */
  const groups = groupConnections(rec.connections);
  const counterparts = new Set(rec.connections.map((c) => c.id)).size;
  side.append(h('div', { class: 'crumb conn-crumb', style: 'margin-bottom:6px' },
    h('span', { class: 'eyebrow' }, 'Sourced connections'),
    h('span', { class: 'dim' }, rec.connections.length + ' links · ' + counterparts + ' counterparts · ' + groups.length + (groups.length === 1 ? ' family' : ' families'))));
  side.append(renderConnGroups(groups));
}

/* The board's analysis: labelled as the board's own voice and folded to its
   first six lines. The control appears only when there is more to read. */
function analysis(text: string): HTMLElement {
  const box = h('div', { class: 'analysis' });
  const p = h('p', { class: 'analysis-text folded' }, text);
  box.append(h('div', { class: 'analysis-head eyebrow' }, "The board's analysis"),
    h('div', { class: 'narrative' }, p));
  const btn = h('button', { type: 'button', class: 'analysis-more', 'aria-expanded': 'false' },
    'Read the whole analysis');
  btn.addEventListener('click', () => {
    const open = p.classList.toggle('folded') === false;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.textContent = open ? 'Fold the analysis' : 'Read the whole analysis';
  });
  box.append(btn);
  requestAnimationFrame(() => {
    if (p.scrollHeight <= p.clientHeight + 2) { p.classList.remove('folded'); btn.remove(); }
  });
  return box;
}
