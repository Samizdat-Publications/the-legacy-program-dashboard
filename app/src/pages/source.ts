/* One source (redesign phase 8, task 4).
 *
 *   #/s/<id>
 *
 * The source's record (type, issuer, date, identifiers), where to read it (its
 * web addresses and archived copies, printed so they break only at / . - and the
 * like), the board node it is where there is one, every claim that cites it,
 * grouped by the node the claim sits on or by the topic that cites the claim,
 * each with its locator and the citation exactly as the research wrote it, then
 * the links (edges) that cite it and the nodes that list it among their sources.
 * An interested party's source says so at the top.
 *
 * Every string comes from app/public/data/sources/<id>.json
 * (tools/source_pages.py). app/checks/run.mjs C43 holds the page to that file.
 */
import '../styles/library.css';
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadIndex, loadSource, clsColour, type SourceRecord, type Era } from '../data';
import { saidKind, saidMark } from '../attrib';
import { edgeTypeName } from '../vocab';
import { urlText, textWithUrls, captured, citationText, demotedWhy, TYPE_LABEL } from '../sources';
import { notFound } from './notfound';

type Claim = SourceRecord['claims'][number];
let groupBy: 'node' | 'topic' = 'node';

export async function renderSource(view: HTMLElement, id: string): Promise<void> {
  clear(view);
  let rec: SourceRecord;
  let eras: Record<string, Era>;
  try {
    const [r, idx] = await Promise.all([loadSource(id), loadIndex()]);
    rec = r;
    eras = Object.fromEntries(idx.eras.map((e) => [e.id, e]));
  } catch {
    notFound(view, '#/s/' + id);
    return;
  }
  setTitle(rec.title, 'Library');
  const page = h('div', { class: 'srcpage', 'data-sid': rec.id });
  view.append(page);

  page.append(h('div', { class: 'crumb' },
    h('div', { class: 'crumb-l' },
      h('a', { class: 'eyebrow', href: '#/library' }, 'Library'), h('span', { class: 'sep' }, '›'),
      h('a', { class: 'eyebrow', href: '#/library?type=' + encodeURIComponent(rec.type) }, TYPE_LABEL[rec.type] || rec.type))));
  page.append(h('h1', { class: 'src-h1' }, rec.title));

  const facts = h('div', { class: 'src-facts' });
  const fact = (k: string, v: string | Node) => facts.append(h('span', { class: 'src-fact' }, h('span', { class: 'dim' }, k + ' '), v));
  fact('type', TYPE_LABEL[rec.type] || rec.type);
  fact('issued by', rec.issuer || (rec.host ? 'not recorded (the copy on file is hosted by ' + rec.host + ')' : 'not recorded'));
  fact('date', rec.date || 'not recorded');
  if (eras[rec.era] && rec.era !== 'nd') fact('era', eras[rec.era].label.toLowerCase());
  if (rec.identifiers.length) fact(rec.identifiers.length === 1 ? 'identifier' : 'identifiers', rec.identifiers.join(', '));
  fact('cited by', rec.claims.length + (rec.claims.length === 1 ? ' claim' : ' claims') + ', ' +
    rec.edges.length + (rec.edges.length === 1 ? ' link' : ' links'));
  page.append(facts);

  if (rec.interestedParty) {
    page.append(h('div', { class: 'src-ip' },
      h('span', { class: 'ip-mark' }, 'interested party'),
      h('p', null, 'Published by the office this board investigates, or by its parent department. It is a primary ' +
        'record of what that office said, not of whether what it says is true: a claim that rests on it alone is ' +
        'held at Tier 2 unless the claim is about what the office said.')));
  }

  /* ---- where to read it -------------------------------------------------- */
  const read = h('div', { class: 'src-read' });
  page.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Where to read it')), read);
  if (rec.node) {
    read.append(h('div', { class: 'src-line' }, h('span', { class: 'dim' }, 'on the board: '),
      mark(clsColour(rec.node.cls || '')), ' ',
      h('a', { class: 'src-node', href: '#/n/' + rec.node.id }, rec.node.label)));
  }
  /* the first copy is the issuer's own where the registry has it (tools/
     build_source_registry.py orders them); the rest, and the archived captures,
     fold away so the claims are not pushed below a wall of addresses */
  const urlLine = (u: string) => h('div', { class: 'src-line' },
    h('a', { class: 'src-url', href: u, target: '_blank', rel: 'noreferrer noopener' }, urlText(u), ' ↗'));
  if (rec.urls.length) read.append(urlLine(rec.urls[0]));
  if (rec.urls.length > 1) {
    read.append(h('details', { class: 'src-more' },
      h('summary', null, (rec.urls.length - 1) + (rec.urls.length === 2 ? ' more copy' : ' more copies') + ' on file'),
      ...rec.urls.slice(1).map(urlLine)));
  }
  if (rec.archived.length) {
    read.append(h('details', { class: 'src-more' },
      h('summary', null, rec.archived.length + (rec.archived.length === 1 ? ' archived capture' : ' archived captures')),
      ...rec.archived.map((u) => {
        const when = captured(u);
        return h('div', { class: 'src-line' },
          h('span', { class: 'dim' }, 'captured ' + (when || 'on an unrecorded date') + ': '),
          h('a', { class: 'src-arch', href: u, target: '_blank', rel: 'noreferrer noopener' }, urlText(u), ' ↗'));
      })));
  }
  if (!rec.urls.length && !rec.archived.length) {
    read.append(h('p', { class: 'dim src-nourl' },
      'No web address on file. The board cites this source by name only' +
      (rec.node ? '; its node on the board says what is known of it.' : '.')));
  }

  /* ---- the claims -------------------------------------------------------- */
  const head = h('div', { class: 'sec sechead' },
    h('div', null, h('span', { class: 'eyebrow' }, 'Claims citing it'), ' ',
      h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(rec.claims.length))));
  const toggle = h('span', { class: 'src-group-by' }, h('span', { class: 'dim' }, 'group by '));
  const list = h('div', { class: 'src-claims' });
  const btns: Record<string, HTMLElement> = {};
  for (const g of ['node', 'topic'] as const) {
    btns[g] = h('button', {
      type: 'button', class: 'src-gb', 'data-by': g, 'aria-pressed': groupBy === g ? 'true' : 'false',
      onclick: () => { groupBy = g; for (const k of Object.keys(btns)) btns[k].setAttribute('aria-pressed', k === g ? 'true' : 'false'); drawClaims(list, rec); },
    }, g);
    toggle.append(btns[g]);
  }
  if (rec.claims.length) head.append(toggle);
  page.append(head, h('p', { class: 'dim src-count-note' },
    'Every claim whose citation the Library matches to this source. A citation it could not match ' +
    '(a different spelling, or two sources in one line) stays on its claim as written and is not counted here.'), list);
  drawClaims(list, rec);
  if (!rec.claims.length) list.append(h('p', { class: 'dim' }, 'No claim cites this source directly.'));

  /* ---- topics ------------------------------------------------------------- */
  if (rec.topics.length) {
    page.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Topics whose sentences cite these claims'),
      ' ', h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(rec.topics.length))));
    page.append(h('div', { class: 'src-topics' }, ...rec.topics.map((t) => h('div', { class: 'src-topic' },
      h('a', { href: '#/topic/' + t.id }, t.title),
      h('span', { class: 'dim' }, ' · ' + t.claims.length + (t.claims.length === 1 ? ' claim' : ' claims'))))));
  }

  /* ---- links -------------------------------------------------------------- */
  if (rec.edges.length) {
    page.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Links citing it'),
      ' ', h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(rec.edges.length))));
    const el = h('div', { class: 'src-edges' });
    for (const e of rec.edges) {
      el.append(h('div', { class: 'src-edge', 'data-eid': e.id },
        h('span', { class: 'ct t' + (e.claimTier || 3) }, 'T' + (e.claimTier || '?')),
        h('div', { class: 'src-edge-body' },
          h('div', null, h('a', { href: '#/n/' + e.a.id }, e.a.label), ' ',
            h('span', { class: 'dim' }, e.label || edgeTypeName(e.type).label.toLowerCase()), ' ',
            h('a', { href: '#/n/' + e.b.id }, e.b.label)),
          e.note ? h('div', { class: 'dim src-edge-note' }, ...textWithUrls(e.note)) : null)));
    }
    page.append(el);
  }

  /* ---- listed on ---------------------------------------------------------- */
  if (rec.listedOn.length) {
    page.append(h('div', { class: 'sec' }, h('span', { class: 'eyebrow' }, 'Listed among the sources of'),
      ' ', h('span', { class: 'sep' }, '·'), ' ', h('b', null, String(rec.listedOn.length))));
    page.append(h('div', { class: 'src-listed' }, ...rec.listedOn.map((n) => h('span', { class: 'src-listed-i' },
      mark(clsColour(n.cls || '')), ' ', h('a', { href: '#/n/' + n.id }, n.label)))));
  }
}

function claimRow(c: Claim): HTMLElement {
  const tier = Number(c.tier);
  return h('div', { class: 'src-claim', 'data-cid': c.id },
    h('span', { class: 'ct t' + tier }, 'T' + tier),
    h('div', { class: 'src-claim-body' },
      h('div', { class: 'src-claim-text' }, saidMark(saidKind(tier, c.text, c.sourceText, null)), c.text),
      h('div', { class: 'src-claim-meta' },
        c.locator ? h('span', { class: 'src-locator' }, h('span', { class: 'dim' }, 'where: '), c.locator) : null,
        c.locator ? h('span', { class: 'sep' }, ' · ') : null,
        h('span', { class: 'src-cited' }, h('span', { class: 'dim' }, 'as cited: '), ...textWithUrls(citationText(c.sourceText || ''), true))),
      demotedWhy(c.sourceText || '') ? h('div', { class: 'src-demoted' }, 'held at Tier 2: ' + demotedWhy(c.sourceText || '')) : null));
}

function drawClaims(list: HTMLElement, rec: SourceRecord): void {
  clear(list);
  if (!rec.claims.length) return;
  const byId = new Map(rec.claims.map((c) => [c.id, c]));
  if (groupBy === 'topic') {
    const placed = new Set<string>();
    for (const t of rec.topics) {
      const g = h('div', { class: 'src-group', 'data-topic': t.id },
        h('div', { class: 'src-group-h' }, h('span', { class: 'dim' }, 'topic '), h('a', { href: '#/topic/' + t.id }, t.title)));
      for (const cid of t.claims) { const c = byId.get(cid); if (c) { g.append(claimRow(c)); placed.add(cid); } }
      list.append(g);
    }
    const rest = rec.claims.filter((c) => !placed.has(c.id));
    if (rest.length) {
      const g = h('div', { class: 'src-group', 'data-topic': '' },
        h('div', { class: 'src-group-h dim' }, 'not cited by a topic sentence'));
      for (const c of rest) g.append(claimRow(c));
      list.append(g);
    }
    return;
  }
  let cur: HTMLElement | null = null;
  let curNode = '';
  for (const c of rec.claims) {
    if (c.node !== curNode) {
      curNode = c.node;
      cur = h('div', { class: 'src-group', 'data-node': c.node },
        h('div', { class: 'src-group-h' }, mark(clsColour(c.cls)), ' ', h('a', { href: '#/n/' + c.node }, c.nodeLabel)));
      list.append(cur);
    }
    cur!.append(claimRow(c));
  }
}
