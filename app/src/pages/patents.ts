/* Patents: Design response section 1.8, route #/patents/<number> with ?sheet=<k>.
 *
 * Left: one section per patent (number, title, status as the record gives it, the
 * granted or filed date, and the node link where the board carries the node), then
 * the five observables with their attribution and their tier.
 *
 * Right: the selected patent's header, the drawing sheets as a grid in the order the
 * data gives them, the unmatched sheet under its own heading with the reason it is
 * unmatched, the prosecution timeline with the wrapper papers where they are held and
 * the papers recorded as not obtained, and the authored quotes and findings that
 * concern this patent.
 *
 * ?sheet=<k> opens the lightbox on the sheet whose `k` is that number: the sheet at
 * reading height (the viewport less 160px), its caption, prev, next and ESC.
 *
 * Nothing on this page is written here. Where a record has no value for a field the
 * page says so rather than filling it in.
 */
import '../styles/patents.css';
import { h, clear } from '../dom';
import { setTitle } from '../router';
import { loadIndex } from '../data';
import { notFound } from './notfound';
import {
  loadPatents, findPatent, patentKey, allSheets, matchedSheets,
  quotesFor, findingsFor, sheetSrc, thumbSrc,
  type PatentsFile, type Patent, type Sheet, type Cite,
} from '../patents/model';

/* One ESC handler, replaced on every render so a closed lightbox leaves nothing
   listening. */
let escHandler: ((e: KeyboardEvent) => void) | null = null;
function setEsc(fn: ((e: KeyboardEvent) => void) | null): void {
  if (escHandler) window.removeEventListener('keydown', escHandler);
  escHandler = fn;
  if (fn) window.addEventListener('keydown', fn);
}

const ABSENT = 'not on the board';

/* A node is named by its label, never by its raw id (blind critic round 0). */
const labels = new Map<string, string>();
const nodeName = (id: string): string => 'on the board: ' + (labels.get(id) || id);

function cite(c: Cite | null | undefined): HTMLElement {
  if (!c || !c.name) return h('span', { class: 'faint' }, 'source ' + ABSENT);
  if (c.url) return h('a', { href: c.url, rel: 'noreferrer', target: '_blank' }, c.name);
  return h('span', { class: 'dim' }, c.name);
}

function statusLine(p: Patent): string {
  return (p.status || []).join(' · ');
}

/* The one date the section line shows: granted where the record has one, filed
   otherwise, and labelled as whichever it is. */
function keyDate(p: Patent): string {
  if (p.granted) return 'granted ' + p.granted;
  if (p.published) return 'published ' + p.published;
  if (p.filed) return 'filed ' + p.filed;
  return 'date ' + ABSENT;
}

export async function renderPatents(view: HTMLElement, number: string, sheet: string | null): Promise<void> {
  clear(view);
  setEsc(null);

  let file: PatentsFile;
  try {
    file = await loadPatents();
  } catch (e) {
    view.append(h('section', { class: 'notice' },
      h('h2', null, 'The patents file is not being served'),
      h('p', null, 'data/patents.json could not be read: ' + (e as Error).message)));
    setTitle('Patents');
    return;
  }

  const sel = findPatent(file, number);
  if (!sel) {
    notFound(view, '#/patents/' + number,
      'No filing with that number is on the board. The five are ' +
      file.patents.map((p) => p.number).join(', ') + '.');
    return;
  }
  setTitle(sel.number, 'Patents');

  const idx = await loadIndex();
  const known = new Set(idx.nodes.map((n) => n.id));
  labels.clear();
  for (const n of idx.nodes) labels.set(n.id, n.label);

  const wrap = h('div', { class: 'pt' });
  const left = h('div', { class: 'pt-left' });
  const right = h('div', { class: 'pt-right' });
  wrap.append(left, right);
  view.append(wrap);

  renderLeft(left, file, sel, known);
  renderRight(right, file, sel, known);

  /* ---- the lightbox --------------------------------------------------- */
  const sheets = allSheets(file);
  const k = sheet == null ? null : Number(sheet);
  const at = k == null || Number.isNaN(k) ? -1 : sheets.findIndex((s) => s.k === k);
  if (at >= 0) view.append(lightbox(file, sel, sheets, at));
}

/* ===================================================================== */
/* Left: the five sections and the five observables                       */
/* ===================================================================== */

function renderLeft(left: HTMLElement, file: PatentsFile, sel: Patent, known: Set<string>): void {
  left.append(h('div', { class: 'eyebrow' }, file.eyebrow));
  left.append(h('h1', { class: 'pt-h1' }, file.title));
  left.append(h('p', { class: 'pt-stand' }, file.standfirst));

  const list = h('div', { class: 'pt-list' });
  for (const p of file.patents) {
    const key = patentKey(p.number);
    const on = p.number === sel.number;
    const card = h('div', { class: 'pt-card' + (on ? ' on' : ''), 'aria-current': on ? 'true' : null });
    card.append(h('div', { class: 'pt-card-head' },
      h('a', { class: 'pt-num', href: '#/patents/' + key }, p.number),
      h('span', { class: 'pt-title' }, p.title)));
    const meta = h('div', { class: 'pt-card-meta' });
    meta.append(h('span', { class: 'pt-status' }, statusLine(p)));
    meta.append(h('span', { class: 'sep' }, '·'));
    meta.append(h('span', { class: 'dim' }, keyDate(p)));
    if (p.node && known.has(p.node)) {
      meta.append(h('span', { class: 'sep' }, '·'));
      meta.append(h('a', { href: '#/n/' + p.node }, nodeName(p.node)));
    } else {
      meta.append(h('span', { class: 'sep' }, '·'));
      meta.append(h('span', { class: 'faint' }, 'no node ' + ABSENT));
    }
    card.append(meta);
    list.append(card);
  }
  left.append(list);

  /* ---- the five observables ------------------------------------------- */
  const ob = file.observables;
  left.append(h('div', { class: 'pt-sec eyebrow' }, ob.title));
  const head = h('div', { class: 'pt-obhead' },
    h('span', { class: 't' + ob.tier }, 'Tier ' + ob.tier),
    h('span', { class: 'sep' }, '·'),
    ob.node && known.has(ob.node)
      ? h('a', { href: '#/n/' + ob.node }, nodeName(ob.node))
      : h('span', { class: 'faint' }, 'no node ' + ABSENT));
  left.append(head);
  left.append(h('p', { class: 'pt-attr' }, ob.attribution));
  left.append(h('p', { class: 'pt-attr dim' }, ob.caveat));

  const obs = h('div', { class: 'pt-obs' });
  let n = 0;
  for (const o of ob.observables) {
    n += 1;
    const row = h('div', { class: 'pt-ob' });
    row.append(h('div', { class: 'pt-ob-head' },
      h('span', { class: 'pt-ob-n' }, String(n)),
      h('span', { class: 'pt-ob-label' }, o.label),
      o.unsettled ? h('span', { class: 'amber' }, 'wording unsettled') : null));
    for (const w of o.wordings || []) {
      row.append(h('div', { class: 'pt-ob-w' },
        h('span', null, '“' + w.text + '”'), ' ',
        h('span', { class: 'faint' }, w.where)));
    }
    if (o.note) row.append(h('div', { class: 'pt-ob-note dim' }, o.note));
    obs.append(row);
  }
  left.append(obs);
  for (const s of ob.sources || []) left.append(h('div', { class: 'pt-obsrc' }, cite(s)));
}

/* ===================================================================== */
/* Right: header, sheets, prosecution, quotes, findings                   */
/* ===================================================================== */

function renderRight(right: HTMLElement, file: PatentsFile, p: Patent, known: Set<string>): void {
  const crumb = h('div', { class: 'crumb-l' },
    h('span', { class: 'cyan' }, p.number),
    h('span', { class: 'sep' }, '·'),
    p.node && known.has(p.node)
      ? h('a', { href: '#/n/' + p.node }, nodeName(p.node))
      : h('span', { class: 'faint' }, 'no node ' + ABSENT),
    h('span', { class: 'sep' }, '·'),
    h('span', { class: 'pt-status' }, statusLine(p)));
  right.append(h('div', { class: 'crumb' }, crumb));
  right.append(h('h1', { class: 'pt-h1' }, p.title));
  if (p.sub) right.append(h('p', { class: 'pt-sub' }, p.sub));

  const facts = h('div', { class: 'pt-facts' });
  const fact = (k: string, v: Node | string): void => {
    facts.append(h('span', { class: 'pt-k' }, k));
    facts.append(h('span', { class: 'pt-v' }, v));
  };
  fact('application', p.application || ABSENT);
  fact('filed', p.filed || ABSENT);
  fact('granted', p.granted || (p.published ? 'not granted · published ' + p.published : ABSENT));
  fact('expired', p.expired || ABSENT);
  fact('maintenance fee', p.fee
    ? (p.fee.lapsed ? 'lapsed ' + p.fee.lapsed : 'recorded') + (p.fee.title ? ' · ' + p.fee.title : '')
    : ABSENT);
  fact('examiner', p.examiner || ABSENT);
  fact('supervisor', p.supervisor || ABSENT);
  fact('art units', (p.artUnits && p.artUnits.length) ? p.artUnits.join(', ') : ABSENT);
  fact('docket', p.docket || ABSENT);
  fact('record', cite(p.source));
  right.append(facts);
  right.append(h('p', { class: 'pt-note faint' },
    'Inventor and assignee are not carried as fields on these records, so they are not ' +
    'printed as ones. The assignment is stated in the line above and in the standfirst.'));

  renderSheets(right, file, p);
  renderProsecution(right, p);
  renderQuotes(right, file, p);
  renderFindings(right, file, p);
}

function sheetTile(s: Sheet, own: boolean, pageKey: string): HTMLElement {
  const a = h('a', {
    class: 'pt-tile' + (own ? ' own' : ''),
    href: '#/patents/' + pageKey + '?sheet=' + s.k,
  });
  a.append(h('img', { class: 'pt-thumb', src: thumbSrc(s.thumb), alt: s.patent + ' figure ' + s.fig, loading: 'lazy' }));
  a.append(h('div', { class: 'pt-tile-cap' },
    h('span', { class: 'cyan' }, s.patent),
    h('span', { class: 'sep' }, '·'),
    h('span', null, 'FIG ' + s.fig),
    h('span', { class: 'sep' }, '·'),
    h('span', { class: 'dim' }, s.caption)));
  return a;
}

function renderSheets(right: HTMLElement, file: PatentsFile, p: Patent): void {
  const matched = matchedSheets(file);
  const unmatched = file.drawings.unmatchedSheets;

  right.append(h('div', { class: 'pt-sec sechead' },
    h('span', { class: 'eyebrow' }, 'Drawing sheets · ' + matched.length +
      ' across the five filings · in order'),
    h('span', { class: 'faint' }, p.sheets.length + ' of them are this filing’s')));
  right.append(h('p', { class: 'pt-note dim' }, file.drawings.standfirst));

  const pageKey = patentKey(p.number);
  const grid = h('div', { class: 'pt-grid' });
  for (const s of matched) grid.append(sheetTile(s, s.patent === p.number, pageKey));
  right.append(grid);

  for (const s of unmatched) {
    right.append(h('div', { class: 'pt-sec eyebrow' }, 'Unmatched sheet'));
    right.append(h('p', { class: 'pt-note dim' },
      'This sheet is not one of the five filings’ own: its record is ' + s.patent +
      ', ' + s.caption + '. It is drawn here rather than dropped, so the eleventh sheet ' +
      'is accounted for.'));
    const g2 = h('div', { class: 'pt-grid one' });
    g2.append(sheetTile(s, false, pageKey));
    right.append(g2);
  }
  right.append(h('p', { class: 'pt-note faint' }, file.drawings.treatment));
  right.append(h('p', { class: 'pt-note faint' }, 'Provenance: ' + file.drawings.provenance));
}

function renderProsecution(right: HTMLElement, p: Patent): void {
  right.append(h('div', { class: 'pt-sec eyebrow' },
    'Prosecution' + (p.docket ? ' · file wrapper of ' + p.docket : '') +
    (p.application ? ' · application ' + p.application : '')));

  if (!p.prosecution || !p.prosecution.length) {
    right.append(h('p', { class: 'pt-note dim' },
      'No prosecution record for this filing is on the board: its file wrapper has not ' +
      'been pulled.'));
  } else {
    /* One step to a line, in date order as the record holds them. The eleven
       steps of PAX 205 do not fit across a column without clipping a label, and
       a clipped label is the one thing this board never draws. */
    const track = h('div', { class: 'pt-steps' });
    for (const st of p.prosecution) {
      const row = h('div', { class: 'pt-step k-' + st.kind });
      row.append(h('span', { class: 'pt-step-date dim' }, st.date));
      row.append(h('span', { class: 'pt-step-label' }, st.label));
      row.append(st.note
        ? h('span', { class: 'pt-step-note dim' }, st.note)
        : h('span', { class: 'pt-step-note' }));
      row.append(st.file
        ? h('span', { class: 'pt-step-file' }, 'paper held · ' + st.file)
        : h('span', { class: 'pt-step-file faint' }, 'paper ' + ABSENT));
      track.append(row);
    }
    right.append(track);
  }

  const absent = p.absent || [];
  if (absent.length) {
    right.append(h('div', { class: 'pt-sec eyebrow' }, 'Papers not obtained'));
    for (const a of absent) {
      right.append(h('div', { class: 'pt-absent' },
        h('span', { class: 'pt-absent-label' }, a.label),
        h('span', { class: 'red' }, 'NOT OBTAINED'),
        h('div', { class: 'dim' }, a.why)));
    }
  }
}

function renderQuotes(right: HTMLElement, file: PatentsFile, p: Patent): void {
  const qs = quotesFor(file, p);
  right.append(h('div', { class: 'pt-sec eyebrow' }, 'Quotes · ' + qs.length));
  if (!qs.length) {
    right.append(h('p', { class: 'pt-note dim' },
      'No quote on this board is taken from this filing’s own papers.'));
    return;
  }
  for (const q of qs) {
    const box = h('div', { class: 'pt-quote' });
    box.append(h('div', { class: 'pt-q-head' },
      h('span', { class: 'cyan' }, q.speaker),
      h('span', { class: 'sep' }, '·'),
      h('span', { class: 'dim' }, q.date),
      h('span', { class: 'sep' }, '·'),
      h('span', { class: 't' + q.tier }, 'Tier ' + q.tier)));
    box.append(h('div', { class: 'pt-q-text' }, '“' + q.text + '”'));
    if (q.gloss) box.append(h('div', { class: 'pt-q-gloss dim' }, q.gloss));
    box.append(h('div', { class: 'pt-q-src' }, cite(q.source)));
    right.append(box);
  }
}

function renderFindings(right: HTMLElement, file: PatentsFile, p: Patent): void {
  const fs = findingsFor(file, p);
  right.append(h('div', { class: 'pt-sec eyebrow' }, 'Findings · ' + fs.length));
  if (!fs.length) {
    right.append(h('p', { class: 'pt-note dim' },
      'No authored finding on this board names this filing.'));
    return;
  }
  for (const f of fs) {
    const box = h('div', { class: 'pt-finding' });
    box.append(h('div', { class: 'pt-q-head' },
      h('span', null, f.title),
      h('span', { class: 'sep' }, '·'),
      h('span', { class: 't' + f.tier }, 'Tier ' + f.tier)));
    box.append(h('div', { class: 'pt-f-text' }, f.text));
    const rows = h('div', { class: 'pt-f-rows' });
    for (const r of f.rows || []) {
      rows.append(h('div', null,
        h('span', { class: 'cyan' }, r.number), ' ',
        h('span', { class: 'dim' }, r.date)));
    }
    box.append(rows);
    if (f.coda) box.append(h('div', { class: 'pt-q-gloss dim' }, f.coda));
    box.append(h('div', { class: 'pt-q-src' }, cite(f.source)));
    right.append(box);
  }
}

/* ===================================================================== */
/* The lightbox                                                           */
/* ===================================================================== */

function lightbox(file: PatentsFile, sel: Patent, sheets: Sheet[], at: number): HTMLElement {
  const s = sheets[at];
  const key = patentKey(sel.number);
  const close = '#/patents/' + key;
  const href = (i: number): string => '#/patents/' + key + '?sheet=' + sheets[i].k;
  const prev = at > 0 ? href(at - 1) : null;
  const next = at < sheets.length - 1 ? href(at + 1) : null;

  setEsc((e: KeyboardEvent) => {
    if (e.key === 'Escape') { e.preventDefault(); location.hash = close; }
    if (e.key === 'ArrowLeft' && prev) { e.preventDefault(); location.hash = prev; }
    if (e.key === 'ArrowRight' && next) { e.preventDefault(); location.hash = next; }
  });

  const box = h('div', { class: 'pt-lb', role: 'dialog', 'aria-label': 'Sheet ' + (at + 1) + ' of ' + sheets.length });
  box.append(h('a', { class: 'pt-lb-back', href: close, 'aria-label': 'close' }));

  const fig = h('figure', { class: 'pt-lb-fig' });
  fig.append(h('img', { class: 'pt-lb-img', src: sheetSrc(s.file), alt: s.patent + ' figure ' + s.fig }));
  box.append(fig);

  const side = h('div', { class: 'pt-lb-side' });
  side.append(h('div', { class: 'pt-lb-h' }, 'Sheet ' + (at + 1) + ' of ' + sheets.length));
  side.append(h('div', { class: 'cyan' }, s.patent + ' · FIG ' + s.fig));
  side.append(h('div', { class: 'pt-lb-cap' }, s.caption));
  side.append(h('div', { class: 'pt-lb-file faint' }, s.file));
  const nav = h('div', { class: 'pt-lb-nav' });
  nav.append(prev ? h('a', { href: prev }, '← previous sheet') : h('span', { class: 'faint' }, '← previous sheet'));
  nav.append(next ? h('a', { href: next }, 'next sheet →') : h('span', { class: 'faint' }, 'next sheet →'));
  nav.append(h('a', { href: close }, 'ESC closes'));
  side.append(nav);
  const owner = file.patents.find((p) => p.number === s.patent);
  if (owner && owner.node) {
    side.append(h('div', null, h('a', { href: '#/n/' + owner.node }, 'the filing’s node · ' + owner.node)));
  } else {
    side.append(h('div', { class: 'faint' },
      'This sheet’s filing, ' + s.patent + ', has no node on the board.'));
  }
  box.append(side);
  return box;
}
