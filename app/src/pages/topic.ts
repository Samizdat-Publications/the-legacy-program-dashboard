/* Topic page: redesign section 5, "Topic", and phase 6 task 1.
 *
 *   #/topic/<id>
 *
 * Header (kind, section, span, the cites by tier), the lead, the summary, then
 * the three blocks side by side: what the record shows, what is claimed, what
 * is contested. Every sentence carries numbered references, and under it each
 * cite is printed in full: its number, its tier, the "said on the record" mark
 * where the rule in attrib.ts gives one, the claim's or link's own words, the
 * node it sits on, and its source, linked where the source gives a URL. A cite
 * keeps one number for the whole page. Then the members by role, the open
 * questions and the related topics. A research gap says so at the top.
 *
 * Nothing on this page is written here. Every string comes from the topic file
 * (tools/build_app_data.py topic_record) or from vocab.json.
 * app/checks/run.mjs C36 holds the page to its record.
 */
import '../styles/topic.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import {
  loadTopic, loadTopics, clsColour, spanText,
  type TopicRecord, type TopicCite, type TopicItem, type TopicsFile,
} from '../data';
import { notFound } from './notfound';
import { saidKind, saidMark, saidKey, type Said } from '../attrib';
import { TOPIC_ROLES, ROLE_HEAD, edgeTypeName } from '../vocab';

type Block = 'lead' | 'summary' | 'record' | 'claimed' | 'contested';

const BLOCKS: { id: 'record' | 'claimed' | 'contested'; head: string; blurb: string; cls: string }[] = [
  { id: 'record', head: 'What the record shows', blurb: 'documented by a primary record', cls: 'b-record' },
  { id: 'claimed', head: 'What is claimed', blurb: 'testimony, allegation and inference, with who says so', cls: 'b-claimed' },
  { id: 'contested', head: 'What is contested', blurb: 'conflicts, denials and the case against', cls: 'b-contested' },
];

export async function renderTopic(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  let rec: TopicRecord;
  let idx: TopicsFile;
  try {
    [rec, idx] = await Promise.all([loadTopic(id), loadTopics()]);
  } catch {
    notFound(view, '#/topic/' + id, 'No topic with this id is on the board.');
    return;
  }
  setTitle(rec.title);
  const section = idx.sections.find((s) => s.id === rec.section);
  const titleOf = new Map(idx.topics.map((t) => [t.id, t.title]));

  /* one number per cited id, in reading order, for the whole page */
  const num = new Map<string, number>();
  const numberOf = (cid: string): number => {
    let n = num.get(cid);
    if (n == null) { n = num.size + 1; num.set(cid, n); }
    return n;
  };
  const kinds = new Set<Said>();

  const page = h('article', { class: 'topic', 'data-id': rec.id });
  view.append(page);

  /* ---- header ----------------------------------------------------------- */
  const tiers = [0, 0, 0];
  for (const c of Object.values(rec.cites)) if (c && c.tier >= 1 && c.tier <= 3) tiers[c.tier - 1]++;
  page.append(h('div', { class: 'crumb topic-crumb' },
    h('div', { class: 'crumb-l' },
      h('a', { class: 'eyebrow', href: '#/atlas' }, 'Atlas'),
      h('span', { class: 'sep' }, '›'),
      h('span', { class: 'eyebrow' }, section ? section.title : rec.section),
    ),
  ));
  page.append(h('h1', { class: 'topic-h1' }, rec.title));
  const facts = h('div', { class: 'topic-facts' },
    h('span', null, h('span', { class: 'dim' }, 'kind '), rec.kind),
    h('span', null, h('span', { class: 'dim' }, 'span '), spanText(rec.span)),
    h('span', null, h('span', { class: 'dim' }, 'members '), String(rec.members.length)),
  );
  if (tiers[0] + tiers[1] + tiers[2]) {
    facts.append(h('span', null, h('span', { class: 'dim' }, 'sources cited '),
      h('span', { class: 't1' }, tiers[0] + ' at Tier 1'), ' · ',
      h('span', { class: 't2' }, tiers[1] + ' at Tier 2'), ' · ',
      h('span', { class: 't3' }, tiers[2] + ' at Tier 3')));
  }
  page.append(facts);

  /* ---- a research gap says so, first ------------------------------------ */
  if (rec.researchGap) {
    page.append(h('section', { class: 'topic-gap' },
      h('div', { class: 'amber eyebrow' }, 'Research gap'),
      h('p', null, 'The board does not yet carry the record for this topic. ' + String(rec.researchGap)),
    ));
  }

  /* ---- lead and summary: prose first ------------------------------------ */
  const prose = h('div', { class: 'topic-prose' });
  if (rec.lead) prose.append(item(rec.lead, 'lead', rec, numberOf, kinds));
  for (const s of rec.summary || []) prose.append(item(s, 'summary', rec, numberOf, kinds));
  if (prose.childNodes.length) page.append(prose);

  /* ---- the three blocks, side by side ----------------------------------- */
  const present = BLOCKS.filter((b) => (rec[b.id] || []).length);
  const grid = h('div', { class: 'tblocks' });
  if (present.length) {
    for (const b of present) {
      const list = rec[b.id];
      const col = h('section', { class: 'tblock ' + b.cls, 'data-block': b.id },
        h('div', { class: 'tblock-head' },
          h('span', { class: 'eyebrow' }, b.head), ' ',
          h('span', { class: 'dim' }, '· ' + list.length + ' · ' + b.blurb)));
      for (const it of list) col.append(item(it, b.id, rec, numberOf, kinds));
      grid.append(col);
    }
    page.append(grid);
  }
  /* the key to the mark, once, where the reader first meets the cites */
  const key = saidKey(kinds);
  if (key) {
    key.classList.add('topic-key');
    if (prose.parentNode === page) page.insertBefore(key, prose);
    else if (grid.parentNode === page) page.insertBefore(key, grid);
  }

  /* ---- members by role --------------------------------------------------- */
  if (rec.members.length) {
    const roles = new Map<string, TopicRecord['members']>();
    for (const m of rec.members) {
      if (!roles.has(m.role)) roles.set(m.role, []);
      roles.get(m.role)!.push(m);
    }
    const order = TOPIC_ROLES.map((r) => r.id);
    const sorted = [...roles.keys()].sort((a, b) =>
      (order.indexOf(a) < 0 ? 99 : order.indexOf(a)) - (order.indexOf(b) < 0 ? 99 : order.indexOf(b)));
    const who = h('section', { class: 'topic-members' },
      h('div', { class: 'sec eyebrow' }, 'Who and what · ' + rec.members.length + ' on the board, by their part in this topic'));
    const grid = h('div', { class: 'role-grid' });
    for (const role of sorted) {
      const ms = roles.get(role)!;
      const g = h('div', { class: 'role-group', 'data-role': role },
        h('div', { class: 'role-head' }, h('span', { class: 'eyebrow' }, ROLE_HEAD[role] || role), ' ',
          h('span', { class: 'faint' }, String(ms.length))));
      const list = h('div', { class: 'role-members' });
      for (const m of ms) {
        list.append(h('a', { class: 'member', href: '#/n/' + m.id },
          mark(clsColour(m.cls || '')), h('span', { class: 'label' }, m.label || m.id)));
      }
      g.append(list);
      grid.append(g);
    }
    who.append(grid);
    page.append(who);
  }

  /* ---- open questions, related topics ----------------------------------- */
  const tail = h('div', { class: 'topic-tail' });
  if ((rec.questions || []).length) {
    const q = h('section', { class: 'topic-questions' },
      h('div', { class: 'sec eyebrow' }, 'Open questions · ' + rec.questions.length));
    const ol = h('ol', { class: 'tq' });
    for (const x of rec.questions) ol.append(h('li', null, x));
    q.append(ol);
    tail.append(q);
  }
  const rel = (rec.related || []).filter((r) => titleOf.has(r));
  if (rel.length) {
    const r = h('section', { class: 'topic-related' },
      h('div', { class: 'sec eyebrow' }, 'Related topics · ' + rel.length));
    const ul = h('div', { class: 'related-list' });
    for (const t of rel) ul.append(h('a', { class: 'related', href: '#/topic/' + t }, titleOf.get(t)!));
    r.append(ul);
    tail.append(r);
  }
  if (tail.childNodes.length) page.append(tail);
}

/* One sentence of the topic, with its numbered references and, under it, each
   of its cites in full. */
function item(it: TopicItem, block: Block, rec: TopicRecord,
  numberOf: (c: string) => number, kinds: Set<Said>): HTMLElement {
  const box = h('div', { class: 'ti ti-' + block, 'data-block': block });
  const cites = it.cite || [];
  const text = h('p', { class: 'ti-text' }, it.text);
  const list = h('div', { class: 'cites' });
  for (const cid of cites) {
    const n = numberOf(cid);
    const ref = h('button', { type: 'button', class: 'ref', title: 'show source ' + n }, '[' + n + ']');
    const c = cite(n, cid, rec.cites[cid], kinds);
    ref.addEventListener('click', () => {
      c.classList.remove('flash');
      void c.offsetWidth;
      c.classList.add('flash');
      c.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    });
    text.append(' ', ref);
    list.append(c);
  }
  box.append(text);
  if (cites.length) box.append(list);
  return box;
}

function cite(n: number, cid: string, c: TopicCite | undefined, kinds: Set<Said>): HTMLElement {
  if (!c || c.missing || !c.kind) {
    return h('div', { class: 'cite missing', 'data-cid': cid, 'data-kind': 'missing' },
      h('span', { class: 'cite-n' }, String(n)),
      h('span', { class: 'cite-tier red' }, '?'),
      h('div', { class: 'cite-body' }, h('span', { class: 'cite-words red' }, 'This citation does not resolve on the board.')));
  }
  const tier = Number(c.tier);
  const body = h('div', { class: 'cite-body' });
  const meta = h('div', { class: 'cite-meta' });
  if (c.kind === 'claim') {
    const s = c.source || { text: '', url: null };
    const said = saidKind(tier, c.text, s.text, s.url);
    if (said) kinds.add(said);
    body.append(h('span', { class: 'cite-words' }, saidMark(said), c.text));
    if (c.node) {
      meta.append(h('span', { class: 'dim' }, 'claim on '),
        h('a', { class: 'cite-node', href: '#/n/' + c.node }, c.nodeLabel || c.node));
    } else meta.append(h('span', { class: 'dim' }, 'a claim not yet placed on a node'));
    meta.append(h('span', { class: 'sep' }, ' · '));
    if (s.url) {
      meta.append(h('a', { class: 'cite-src', href: s.url, target: '_blank', rel: 'noreferrer noopener', title: s.url },
        (s.text || s.url) + ' ↗'));
    } else {
      meta.append(h('span', { class: 'cite-src' }, s.text ? 'source: ' + s.text : 'no source recorded'));
    }
  } else {
    const ends = c.endpoints || [];
    const words = [c.label, c.text].filter(Boolean).join('. ');
    body.append(h('span', { class: 'cite-words' }, words));
    meta.append(h('span', { class: 'dim' }, (c.type ? edgeTypeName(c.type).label.toLowerCase() + ' link' : 'link') + ' between '));
    ends.forEach((e, i) => {
      if (i) meta.append(h('span', { class: 'dim' }, ' and '));
      meta.append(h('a', { class: 'cite-node', href: '#/n/' + e.id }, e.label || e.id));
    });
    for (const s of c.sources || []) {
      meta.append(h('span', { class: 'sep' }, ' · '));
      const t = (s.name || s.url || '') + (s.date ? ' (' + s.date + ')' : '');
      meta.append(s.url
        ? h('a', { class: 'cite-src', href: s.url, target: '_blank', rel: 'noreferrer noopener', title: s.url }, t + ' ↗')
        : h('span', { class: 'cite-src' }, 'source: ' + t));
    }
    if (!(c.sources || []).length) meta.append(h('span', { class: 'sep' }, ' · '), h('span', { class: 'cite-src' }, 'no source recorded'));
  }
  body.append(meta);
  return h('div', { class: 'cite', 'data-cid': cid, 'data-kind': c.kind },
    h('span', { class: 'cite-n' }, String(n)),
    h('span', { class: 'cite-tier t' + tier }, 'T' + tier),
    body);
}
