/* The neighbourhood, grouped: redesign phase 11.
 *
 * The entity in the centre; its neighbours in labelled columns, one column per
 * relationship family; every neighbour named once, with the link read from the
 * centre (the predicate's own words where the generator shows it, with the
 * authored sentence on hover and on tap; the family's phrase otherwise, with the
 * sentence shown open, so every row says why without a tap). One
 * orthogonal line runs from the centre to each column. Two steps out opens one
 * family at a time and names, for every node it reaches, the neighbour it is
 * reached through ("via <name>").
 *
 * It replaced a ring whose names were clipped to what fitted, whose far names
 * gave no "via whom", and whose reason for a link was often a family word
 * alone (blind critic, phases 6 and 7). A phone reads the same page stacked.
 *
 * Nothing on this page is written here except the frame's own words. Every node
 * name, predicate, sentence and tier comes from the board's own record.
 */
import { h, clear, mark } from '../dom';
import { setTitle } from '../router';
import { loadHighlights, loadNode, loadIndex, clsColour, dateRange, type Connection, type IndexNode } from '../data';
import { NO_SENTENCE, familyName } from '../vocab';
import { adjacency, groupNeighbours, twoSteps, type FamilyGroup, type Neighbour } from '../hood/model';
import { drawLines } from '../hood/lines';
import { notFound } from './notfound';
import '../styles/hood.css';

/* the family whose two steps are open. It survives a redraw of the same centre
   and resets when the centre changes. */
let openFamily: string | null = null;
let openFor: string | null = null;

let generation = 0;
let observer: ResizeObserver | null = null;

export async function renderHood(view: HTMLElement, id: string | null): Promise<void> {
  const gen = ++generation;
  if (observer) { observer.disconnect(); observer = null; }
  if (!id) { await renderPick(view, gen); return; }
  if (openFor !== id) { openFamily = null; openFor = id; }

  let rec, idx, adj;
  try {
    [rec, idx, adj] = await Promise.all([loadNode(id), loadIndex(), adjacency()]);
  } catch (e) {
    if (gen !== generation) return;
    notFound(view, '#/n/' + id + '/hood',
      "The neighbourhood needs this node's record and the edge list: " + (e as Error).message);
    return;
  }
  if (gen !== generation) return;
  const byId = new Map<string, IndexNode>(idx.nodes.map((n) => [n.id, n]));
  const labelOf = (x: string) => (byId.get(x) || { label: x }).label;
  const groups = groupNeighbours(rec.connections.filter((c) => byId.has(c.id)));
  const hop1 = new Set(groups.flatMap((g) => g.rows.map((r) => r.id)));
  const nNeighbours = hop1.size;

  setTitle(rec.label, 'Neighbourhood');
  clear(view);

  const page = h('div', { class: 'gn', 'data-centre': rec.id });
  page.append(h('div', { class: 'gn-head' },
    h('span', { class: 'eyebrow' }, 'Neighbourhood'),
    h('span', { class: 'dim' }, nNeighbours + ' neighbours in ' + groups.length +
      (groups.length === 1 ? ' family' : ' families') +
      ', each named once and read from ' + rec.label + '. Denials, and links with no precise wording, show their sentence; ' +
      'elsewhere tap the underlined words for it. "Two steps out" opens one family at a time.')));

  const stage = h('div', { class: 'gn-stage' });
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'gn-lines');
  svg.setAttribute('aria-hidden', 'true');
  const grid = h('div', { class: 'gn-grid' });
  const sideL = h('div', { class: 'gn-side gn-l' });
  const sideR = h('div', { class: 'gn-side gn-r' });
  grid.append(sideL, centreCard(rec.id, rec.label, rec.cls, nNeighbours, groups.length), sideR);
  stage.append(svg, grid);
  page.append(stage);
  view.append(page);

  /* the columns go to the side that is shorter so far, in the vocabulary's
     order, so the two sides stay close in height */
  let hl = 0, hr = 0;
  groups.forEach((g, i) => {
    const block = familyBlock(g, i, rec.id, hop1, adj, labelOf, byId, () => redraw());
    const weight = g.rows.length + 3;
    if (hl <= hr) { sideL.append(block); hl += weight; } else { sideR.append(block); hr += weight; }
  });

  const redraw = () => { if (gen === generation) drawLines(stage, svg); };
  redraw();
  observer = new ResizeObserver(() => redraw());
  observer.observe(stage);
  if (document.fonts && document.fonts.ready) void document.fonts.ready.then(redraw);
}

function centreCard(id: string, label: string, cls: string, n: number, fams: number): HTMLElement {
  return h('div', { class: 'gn-centre', 'data-id': id },
    h('div', { class: 'gn-anchor' }, mark(clsColour(cls)), h('span', { class: 'eyebrow' }, cls)),
    h('h1', { class: 'gn-who' }, label),
    h('div', { class: 'dim' }, n + ' neighbours · ' + fams + (fams === 1 ? ' family' : ' families')),
    h('div', { class: 'gn-acts' },
      h('a', { class: 'act key', href: '#/n/' + id }, 'NODE PAGE'),
      h('a', { class: 'act', href: '#/report/n/' + id }, 'REPORT')),
    h('div', { class: 'gn-legend' },
      legend('var(--cyan)', 'a sourced link, one line per family'),
      legend('var(--red)', 'a denial'),
      legend('var(--amber)', 'custody or money')),
  );
}

function legend(colour: string, text: string): HTMLElement {
  return h('div', { class: 'gn-leg' },
    h('i', { class: 'gn-sw', style: 'border-top-color:' + colour, 'aria-hidden': 'true' }),
    h('span', { class: 'faint' }, text));
}

function sentences(links: Connection[]): string {
  return links.map((l) => (l.edgeLabel || l.note || NO_SENTENCE) + ' (' +
    dateRange(l.dateStart, l.dateEnd) + ', Tier ' + (l.claimTier ?? '?') + ')').join('\n');
}

function familyBlock(
  g: FamilyGroup, order: number, centre: string, hop1: Set<string>, adj: Map<string, Set<string>>,
  labelOf: (id: string) => string, byId: Map<string, IndexNode>, redraw: () => void,
): HTMLElement {
  const f = familyName(g.family);
  const block = h('section', {
    class: 'gn-fam' + (g.family === 'denial' ? ' denial' : ''),
    'data-family': g.family, style: 'order:' + order,
  });
  const two = h('div', { class: 'gn-two' });
  const btn = h('button', {
    type: 'button', class: 'gn-two-b', 'aria-expanded': 'false',
    onclick: () => {
      const opening = openFamily !== g.family;
      /* one family at a time: close whichever is open, anywhere on the page */
      for (const b of Array.from(document.querySelectorAll('.gn-fam .gn-two-b'))) {
        b.setAttribute('aria-expanded', 'false');
        b.textContent = 'two steps out ›';
      }
      for (const t of Array.from(document.querySelectorAll('.gn-fam .gn-two'))) clear(t as HTMLElement);
      openFamily = opening ? g.family : null;
      if (opening) fillTwo(two, btn, g, centre, hop1, adj, labelOf, byId);
      redraw();
    },
  }, 'two steps out ›');
  block.append(h('div', { class: 'gn-fhead' },
    h('span', { class: 'eyebrow gn-flabel' + (g.family === 'denial' ? ' red' : '') }, f.label),
    h('span', { class: 'dim' }, ' · ' + g.rows.length + (g.rows.length === 1 ? ' neighbour' : ' neighbours')),
    btn));
  if (f.blurb) block.append(h('div', { class: 'faint gn-fblurb' }, f.blurb));
  const list = h('ul', { class: 'gn-rows' });
  for (const r of g.rows) list.append(rowEl(r));
  block.append(list, two);
  if (openFamily === g.family) fillTwo(two, btn, g, centre, hop1, adj, labelOf, byId);
  return block;
}

function rowEl(r: Neighbour): HTMLElement {
  const said = sentences(r.links);
  /* a row whose reading is only its family's phrase, and every denial (the
     case against, which must say what was denied), shows its sentence open */
  const plain = !r.readings.some((x) => x.shown) || r.family === 'denial';
  const sent = h('div', { class: 'gn-sent', hidden: !plain });
  for (const l of r.links) {
    sent.append(h('div', { class: 'gn-sline' },
      h('span', null, l.edgeLabel || l.note || NO_SENTENCE),
      h('span', { class: 'faint' }, ' · ' + dateRange(l.dateStart, l.dateEnd) + ' · T' + (l.claimTier ?? '?'))));
  }
  const say = h('button', {
    type: 'button', class: 'gn-say', 'aria-expanded': plain ? 'true' : 'false', title: said,
    onclick: () => {
      const open = say.getAttribute('aria-expanded') !== 'true';
      say.setAttribute('aria-expanded', open ? 'true' : 'false');
      sent.hidden = !open;
    },
  });
  r.readings.forEach((x, i) => {
    if (i) say.append(h('span', { class: 'faint' }, ', '));
    say.append(h('span', { class: x.shown ? 'gn-pred' : 'gn-pred dim' }, x.text));
  });
  const also = r.also.length
    ? h('span', { class: 'faint gn-also', title: 'Named once, here; it has links in these families too.' },
      'also ' + r.also.map((f) => familyName(f).phrase.replace(/ to$/, '')).join(', '))
    : null;
  return h('li', { class: 'gn-row', 'data-id': r.id, 'data-family': r.family },
    say,
    h('a', { class: 'gn-name', href: '#/n/' + r.id, title: said },
      mark(clsColour(r.cls)), h('span', { class: 'gn-label' }, r.label)),
    also, sent);
}

function fillTwo(
  host: HTMLElement, btn: HTMLElement, g: FamilyGroup, centre: string, hop1: Set<string>,
  adj: Map<string, Set<string>>, labelOf: (id: string) => string, byId: Map<string, IndexNode>,
): void {
  clear(host);
  btn.setAttribute('aria-expanded', 'true');
  btn.textContent = 'close two steps';
  const vias = twoSteps(centre, g, hop1, adj, labelOf);
  const n = vias.reduce((s, v) => s + v.ids.length, 0);
  host.append(h('div', { class: 'gn-two-head eyebrow' },
    n ? 'Two steps out through ' + familyName(g.family).label.toLowerCase() + ': ' + n + ', each under the neighbour it is reached through'
      : 'Nothing further: every link of these neighbours comes back to this page'));
  for (const v of vias) {
    const box = h('div', { class: 'gn-via', 'data-via': v.via.id });
    box.append(h('div', { class: 'gn-via-head' },
      h('span', { class: 'faint' }, 'via '),
      h('a', { class: 'gn-via-name', href: '#/n/' + v.via.id }, v.via.label),
      h('span', { class: 'faint' }, ' · ' + v.ids.length)));
    const ul = h('ul', { class: 'gn-rows2' });
    for (const m of v.ids) {
      const meta = byId.get(m);
      ul.append(h('li', { class: 'gn-row2', 'data-id': m, 'data-via': v.via.id },
        h('a', { class: 'gn-name', href: '#/n/' + m + '/hood', title: labelOf(m) + ', reached via ' + v.via.label },
          mark(clsColour(meta ? meta.cls : '')), h('span', { class: 'gn-label' }, labelOf(m)))));
    }
    box.append(ul);
    host.append(box);
  }
}

/* Nothing selected: the neighbourhood is about one entity, so this asks for
   one. The start-here ring that used to stand here is the Home tour now. */
async function renderPick(view: HTMLElement, gen: number): Promise<void> {
  const [flags, idx] = await Promise.all([loadHighlights().then((x) => x.flags), loadIndex()]);
  if (gen !== generation) return;
  setTitle('Neighbourhood');
  clear(view);
  const byId = new Map(idx.nodes.map((n) => [n.id, n]));
  const wrap = h('div', { class: 'gn-pick' });
  wrap.append(h('div', { class: 'gn-head' },
    h('span', { class: 'eyebrow' }, 'Neighbourhood'),
    h('span', { class: 'dim' }, 'shows one entity and everything linked to it, grouped by relationship. ' +
      'Search for an entity above, or open one of the owner\'s start-here entries:')));
  const list = h('ol', { class: 'gn-pick-list' });
  for (const f of flags.slice().sort((a, b) => a.rank - b.rank)) {
    const n = byId.get(f.id);
    if (!n) continue;
    list.append(h('li', null,
      h('a', { class: 'gn-name', href: '#/n/' + f.id + '/hood' },
        mark(clsColour(n.cls)), h('span', { class: 'gn-label' }, n.label)),
      h('span', { class: 'amber' }, ' start here ' + f.rank)));
  }
  wrap.append(list);
  view.append(wrap);
}
