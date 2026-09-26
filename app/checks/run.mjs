/* app/checks/run.mjs: C1 to C16 of notes/DESIGN-RESPONSE-SHELL-2026-09-02.md
 * section 3, plus C17 for the back button Stewart made a condition of the new
 * shell and C18 for the analyst dock and its per-route chips, C19 to C21 for the
 * analyst's tools, search ranking and the thread report, and C22 to C26 for
 * redesign phase 1 (notes/PLAN-2026-09-24.md): grouped connections with their
 * sentences, every authored field, search over events and threads, the
 * node-level denial flag, and a node page at phone width; C27 to C29 carried from
 * the retired shell; and C30 for redesign phase 3, a denial the record does not
 * adjudicate printed as such; and C31 to C35 for redesign phase 5b (the reader
 * fixes of blind critic round 0): the mark on a Tier 1 claim that records that
 * something was said, the analyst tab covering no text, the thread's timeline
 * slice in year order, the timeline's axis and its NO DATE column, and no
 * internal jargon or debug chrome on any screen. C26 became a phone check over
 * every surface in the critic sweep. Redesign phase 9 rewrote C15 (the timeline
 * by section, every event named) and added C50 to C53: the directories, their
 * person facets against research/_person_facets.json, search over everything
 * with its keys, and the timeline's panel, counts, repeats, scopes and strand
 * filter. Redesign phase 11 retired C10 with the neighbourhood's ring and added
 * C70: the grouped neighbourhood (every neighbour named once, in its family's
 * column, two steps out one family at a time, each via named). The same phase
 * retired the program map: C3, C5 and C6 went with it, and C2, C4, C11 and C12
 * lost their map halves (the Atlas's own C37 covers its chips); C72 holds that
 * the map's old routes land on what replaced them; C71 is #/places (every place
 * listed once under its country, every place with coordinates plotted once, in
 * the order its longitude and latitude give). All against the built app
 * served by `npm run preview`.
 *
 * WHY IT IS SHAPED LIKE THIS.
 *
 * CLAUDE.md section 5: a check that has never been shown to fail is
 * indistinguishable from a broken one, and a poison must corrupt THE PAGE, not
 * the predicate. So every check here reads the rendered DOM or the boxes the
 * browser actually laid out -- never a renderer's private state -- and every
 * check has a poison that damages the real page and must make that check fail.
 *
 *   POISON=c4 node checks/run.mjs      one poison; exits 0 only if c4 FAILED
 *   node checks/run.mjs                the plain run; exits non-zero on any FAIL
 *   node checks/run.mjs --all-poisons  every poison in turn, each must be seen
 *
 * APP_URL points at the preview server (default http://127.0.0.1:4173).
 *
 * Note on `window.__app.*`: the timeline publishes a probe, and this file
 * deliberately does NOT use probes that report layout intentions. Where a figure
 * matters it is re-read from the DOM, boxes as getBoundingClientRect.
 */
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const APP = (process.env.APP_URL || 'http://127.0.0.1:4173').replace(/\/+$/, '') + '/';
const POISON = (process.env.POISON || '').trim().toLowerCase();
const SELF = fileURLToPath(import.meta.url);

const NODE_FOCUS = 'aawsap';       /* start-here 1, the richest record on the board */
const PERSON_FOCUS = 'david-grusch'; /* the richest person record: unverified, chronology, affiliations */
/* Entities whose conflicts, unverified notes and open questions merge.py dropped
   until redesign phase 3: S-4 carries the restored case against it, CEFAA its own
   open questions (an entity's, not a dossier's). */
const ENTITY_FOCUS = 's-4-papoose-lake';
const ENTITY_OQ_FOCUS = 'cefaa';
/* A node with denials the adjudication has reached AND denials it has not (C30). */
const DENIAL_FOCUS = 'cia';
const PATENT = '10144532';
/* Phase 6: two topics the plan names (the anchor of the early record, and the
   richest claimant topic), one research gap, and an absorbed domain node. */
const TOPIC_A = 'roswell-1947';
const TOPIC_B = 'grusch-allegations';
const TOPIC_GAP = 'pre-roswell-claims';
const DOMAIN_FOCUS = 'd-roswell';
/* Phase 8: a well-cited source with a node, identifier and web addresses, and
   a Library state with two facets on. */
const SOURCE_FOCUS = 'gao-nsiad-95-187';
const LIB_FILTER = '#/library?type=report&ip=0';
const LIB_SEARCH = 'roswell';

/* ---- C31's rule, restated ------------------------------------------------ */
/* app/src/attrib.ts decides which Tier 1 claims record that something was SAID.
   This is the same rule written out again here, not imported, so the check is a
   second statement of it rather than the implementation agreeing with itself.
   In words: a Tier 1 claim is "said on the record" when its text opens with an
   attribution (Sworn, Testified, Stated, Said, Told, According to, Asked,
   Elicited, Alleged, ...); or a capitalised speaker is followed within six words
   by a speech verb, that speaker not being a document and the word before the
   verb not an article or possessive; or its source (URLs aside) is a record of
   speech (sworn, testimony, a spokesperson, an opening / written / departmental
   statement, a statement for the record, remarks, a press conference) and the
   claim is not about the record itself; or it is a quotation sourced to a
   transcript, hearing, statement or interview. It is "the office's own account"
   when none of that holds and its source is AARO or the Department itself
   (aaro.mil, defense.gov, war.gov, or a source string that starts with AARO). */
function saidRule(tier, text, sourceText, url) {
  if (Number(tier) !== 1) return null;
  const t = text || '';
  const raw = sourceText || '';
  const s = raw.replace(/https?:\/\/\S+/g, ' ');
  const opens = /^['"‘“]?(?:Sworn\b|Under oath\b|Testif(?:ied|ies|ying)\b|In (?:sworn |his |her |their |written )?testimony\b|Stated\b|States:|Said\b|Says\b|Told\b|Tells\b|According to\b|Asked\b|Answering\b|Attributed\b|Elicited\b|Claimed\b|Claims\b|Alleged\b|Alleges\b)/i;
  if (opens.test(t)) return 'said';
  const speaker = /^(?:[A-Z][\w.'’&()-]*\s){0,4}(?!(?:The|A|An|Its|Their|His|Her|This|That|These|Those)\s)[A-Z][\w.'’&()-]*\s(?:said|says|stated|states|testified|testifies|told|tells|swore|alleged|alleges|claimed|claims|asserted|asserts|declared|declares|responded|replied|answered)\b/.exec(t);
  if (speaker && !/\b(?:Report|Paper|Assessment|Memo|Memorandum|Brief|Charter|Act|Volume|Document|Instruction|Directive|Manual|Order|FAQ|JANAP|Condon|NSDD|DIA-\d)/.test(speaker[0])) return 'said';
  const aboutRecord = /^(?:Held\b|Official hearing record|The (?:hearing|transcript|document|record|report|letter|memo)\b|Its core|Page \d|Sole witness|Witness of record|Called as|Appeared as|Listed in|Written testimony filed)/i.test(t);
  if (!aboutRecord && /\b(?:sworn|testimony|testified|deposition|affidavit|spokes(?:man|woman|person)|(?:opening|written|prepared|emailed|joint|DoD|Navy|NASA|Pentagon|federal) statement|statement (?:for the record|to|following|by|attributed)|remarks|press conference(?! photographs)|media roundtable|media engagement)\b/i.test(s)) return 'said';
  if (/^['"‘“]/.test(t) && /\b(?:transcript|hearing|statement(?! of work)|interview)\b/i.test(s)) return 'said';
  const host = ((url || raw).match(/https?:\/\/([^/?#:\s)\]]+)/i) || [])[1] || '';
  if (/(^|\.)(?:aaro\.mil|defense\.gov|war\.gov)$/i.test(host.toLowerCase()) ||
      /^(?:AARO|All-domain Anomaly Resolution Office)\b/i.test(s.trim())) return 'office';
  return null;
}
/* a node record's claim source is a string or {name, url}; claims.json's is {text, url} */
function srcOf(src) {
  if (!src) return { text: '', url: null };
  if (typeof src === 'object') return { text: src.text || src.name || src.url || '', url: src.url || null };
  const m = String(src).match(/https?:\/\/[^\s)\]]+/);
  return { text: String(src), url: m ? m[0] : null };
}

/* ---- C35's words ---------------------------------------------------------- */
/* Internal vocabulary the reader was shown until phase 5b, and the debug chrome
   the bar carried. None of it may reach any screen. */
const JARGON = [
  /row pitch \d/i, /band gap \d/i, /scale 1:1/i, /\bL0 floor\b/i, /below the (?:label )?floor/i,
  /derived pairs/i, /never the whole graph/i, /\bdegree \d+ distinct/i,
  /\bnode [a-z0-9]+(?:-[a-z0-9]+)+\b/, /\bid [a-z0-9]+(?:-[a-z0-9]+)* ·/, /no room at 11px/i,
  /all labels at 11px/i, /data\/the-program\.json/,
];

/* ---- reporting ---------------------------------------------------------- */
const failsByCheck = new Map();
let nFail = 0, nOk = 0;
function check(id, cond, label, detail = '') {
  const line = (cond ? 'ok    ' : 'FAIL  ') + label + (detail ? ' :: ' + detail : '');
  console.log('  ' + line);
  if (cond) nOk++;
  else { nFail++; failsByCheck.set(id, (failsByCheck.get(id) || 0) + 1); }
}
function skip(label, why) { console.log('  skip  ' + label + ' :: ' + why); }
const clip = (a, n = 5) => a.slice(0, n).join(', ') + (a.length > n ? ` … +${a.length - n}` : '');

/* ---- geometry ----------------------------------------------------------- */
function overlap(a, b) {
  const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
  const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
  return ox > 0.5 && oy > 0.5;
}
function pairsOverlapping(boxes, cap = 6) {
  const bad = [];
  const s = boxes.slice().sort((p, q) => p.y - q.y);
  for (let i = 0; i < s.length; i++) {
    for (let k = i + 1; k < s.length; k++) {
      if (s[k].y >= s[i].y + s[i].h) break;
      if (overlap(s[i], s[k])) {
        bad.push(`${s[i].id}×${s[k].id}`);
        if (bad.length >= cap) return bad;
      }
    }
  }
  return bad;
}

/* ---- in-page collectors (stringified into the browser) ------------------ */
/* Everything below runs in the page. They read the DOM and nothing else. */

const IN_PAGE = {
  /* the not-found page names the route it was given; that is how it is spotted */
  page() {
    const h2 = document.querySelector('.notice h2');
    const b = document.querySelector('button.nav-back');
    const bar = document.querySelector('.bar');
    return {
      text: document.body.innerText,
      bar: bar ? bar.innerText : '',
      hrefs: Array.prototype.map.call(document.querySelectorAll('a[href]'), (a) => a.getAttribute('href')),
      notfound: !!(h2 && /No such route/.test(h2.textContent || '')),
      title: document.title,
      /* the bar's routes (C40): the row a reader sees, and what sits under More */
      nav: {
        primary: Array.prototype.map.call(document.querySelectorAll('.bar .nav > a, .bar .nav > .nav-inert'),
          (a) => ({ label: (a.textContent || '').trim(), href: a.getAttribute('href') })),
        more: Array.prototype.map.call(document.querySelectorAll('.bar .nav .nav-more-list a, .bar .nav .nav-more-list .nav-inert'),
          (a) => ({ label: (a.textContent || '').trim(), href: a.getAttribute('href') })),
        moreBtn: !!document.querySelector('.bar .nav button.nav-more-btn'),
      },
      back: b ? {
        tag: b.tagName, type: b.getAttribute('type') || '',
        text: (b.textContent || '').trim(),
        disabled: b.disabled === true, aria: b.getAttribute('aria-disabled'),
        title: b.getAttribute('title') || '', label: b.getAttribute('aria-label') || '',
      } : null,
    };
  },

  /* Labels, measured against the natural width of their own text at their own
     computed font. A label narrower than its text is a truncated label. */
  labels(sel, boxSel) {
    const meas = document.createElement('span');
    meas.style.cssText = 'position:absolute;visibility:hidden;top:-9999px;left:0;white-space:pre';
    document.body.appendChild(meas);
    const out = [];
    for (const el of document.querySelectorAll(sel)) {
      const cs = getComputedStyle(el);
      for (const k of ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'letterSpacing', 'textTransform', 'fontVariant']) {
        meas.style[k] = cs[k];
      }
      meas.textContent = el.textContent || '';
      const nat = meas.getBoundingClientRect().width;
      const r = el.getBoundingClientRect();
      const box = boxSel ? el.closest(boxSel) : null;
      const br = box ? box.getBoundingClientRect() : null;
      /* a label that wraps (the grouped neighbourhood lets a long name take a
         second line rather than cutting it) is whole when its line boxes add up
         to its natural width, less the space swallowed at each break */
      const rg = document.createRange();
      rg.selectNodeContents(el);
      const lb = Array.prototype.filter.call(rg.getClientRects(), (q) => q.width > 0);
      out.push({
        text: el.textContent || '',
        lines: lb.length, sumW: lb.reduce((s, q) => s + q.width, 0),
        fs: cs.fontSize, to: cs.textOverflow, nat,
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
        bid: box ? (box.getAttribute('data-id') || box.getAttribute('href') || '') : '',
        bx: br ? br.left + scrollX : null, by: br ? br.top + scrollY : null,
        bw: br ? br.width : null, bh: br ? br.height : null,
      });
    }
    meas.remove();
    return out;
  },

  node() {
    const claims = Array.prototype.map.call(document.querySelectorAll('.claim'), (c) => {
      const t = c.querySelector('.ct');
      const s = c.querySelector('.csrc');
      return {
        tier: t ? t.textContent.trim() : '',
        text: (c.querySelector('.ctext') || {}).textContent || '',
        srcTag: s ? s.tagName : null,
        srcHref: s ? s.getAttribute('href') : null,
        srcTitle: s ? (s.getAttribute('title') || '') : '',
        srcText: s ? (s.textContent || '') : '',
      };
    });
    const head = document.querySelector('.sechead');
    const denials = Array.prototype.map.call(document.querySelectorAll('.denials > .denial'), (d) => {
      const a = d.querySelector('a[href^="#/n/"]');
      return { other: a ? a.getAttribute('href').slice(4) : null, text: d.textContent };
    });
    return { claims, head: head ? head.textContent : '', denials };
  },

  /* Home's figures, as printed: the counts panel row by row, and the prose. */
  home() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    return {
      rows: Array.prototype.map.call(document.querySelectorAll('.panel.counts tr'), (tr) =>
        [txt(tr.querySelector('td.n')), txt(tr.querySelector('td.k'))]),
      para: txt(document.querySelector('.home-para')),
    };
  },

  /* Sourced connections on a node page, grouped as drawn. */
  conns() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    return {
      groups: Array.prototype.map.call(document.querySelectorAll('.node-side .conn-group'), (g) => ({
        family: g.getAttribute('data-family') || '',
        head: txt(g.querySelector('.conn-ghead .eyebrow')),
        rows: Array.prototype.map.call(g.querySelectorAll('.conn'), (r) => ({
          id: r.getAttribute('data-id') || '',
          verb: txt(r.querySelector('.conn-verb')),
          /* the arrow as DRAWN: its glyph, not its data attribute */
          dir: txt(r.querySelector('.conn-head .conn-dir')),
          lines: Array.prototype.map.call(r.querySelectorAll('.conn-line .conn-text'), txt),
          metas: Array.prototype.map.call(r.querySelectorAll('.conn-line .cmeta'), txt),
        })),
      })),
    };
  },

  /* The same, on the printable node report. */
  rconns() {
    return Array.prototype.map.call(document.querySelectorAll('.rconns .rconn'), (r) => {
      /* the family is read from the heading the row sits under, as printed */
      let hd = r.parentElement ? r.parentElement.previousElementSibling : null;
      while (hd && hd.tagName !== 'H3') hd = hd.previousElementSibling;
      return {
        id: r.getAttribute('data-id') || '',
        head: ((hd && hd.textContent) || '').replace(/\s*\(\d+\)\s*$/, '').trim(),
        verb: ((r.querySelector('.rverb') || {}).textContent || '').trim(),
        dir: ((r.querySelector('.conn-dir') || {}).textContent || '').trim(),
        sent: ((r.querySelector('.rsent') || {}).textContent || '').trim(),
        text: r.textContent || '',
      };
    });
  },

  /* How many of each authored field a node page draws, and its crumb. */
  fields() {
    const n = (sel) => document.querySelectorAll(sel).length;
    return {
      oq: n('.node .oq'), unv: n('.node .unv'), cnf: n('.node .cnf'), chron: n('.node .chron .ev'),
      aff: n('.node .affs .aff'), nsrc: n('.node .nsrcs .nsrc'),
      crumb: ((document.querySelector('.node .crumb-l') || {}).textContent || ''),
      /* the three axis bars, as the boxes the browser laid out: three cells side
         by side, never stacked on one another */
      axes: Array.prototype.map.call(document.querySelectorAll('.node .axis .cells'), (c) =>
        Array.prototype.map.call(c.children, (x) => { const b = x.getBoundingClientRect(); return [b.left, b.right]; })),
    };
  },

  /* The node page's first screen (C23, phase 5b): where the About lead, the
     case against and the first claim sit against the fold, whether the board's
     own analysis is labelled and folded with every word still in the DOM, and
     how much of the main column the prose uses. */
  firstScreen() {
    const vh = innerHeight;
    const top = (el) => (el ? el.getBoundingClientRect().top : 1e9);
    const main = document.querySelector('.node .node-main');
    const ana = document.querySelector('.node .analysis-text');
    const lead = document.querySelector('.node .narrative.lead') || ana;
    const lh = ana ? parseFloat(getComputedStyle(ana).lineHeight) || 19 : 19;
    return {
      vh,
      leadTop: top(lead), againstTop: top(document.querySelector('.node .against-row')),
      claimTop: top(document.querySelector('.node .claim')),
      head: ((document.querySelector('.node .analysis-head') || {}).textContent || '').trim(),
      folded: !!ana && ana.classList.contains('folded'),
      foldedLines: ana ? Math.round(ana.clientHeight / lh) : 0,
      more: ((document.querySelector('.node .analysis-more') || {}).textContent || '').trim(),
      chars: ana ? (ana.textContent || '').length : 0,
      proseW: ana ? ana.getBoundingClientRect().width : 0,
      mainW: main ? main.getBoundingClientRect().width : 0,
    };
  },

  /* The node page's denial rows, in page order, as the reader sees them. */
  denials() {
    return Array.prototype.map.call(document.querySelectorAll('.node .denials .denial'), (r) => ({
      kind: ((r.querySelector('.dkind') || r.lastElementChild || {}).textContent || '').trim(),
      other: ((r.querySelector('a') || {}).getAttribute ? r.querySelector('a').getAttribute('href') : '') || '',
    }));
  },

  /* The grouped neighbourhood (phase 11), from the DOM: every neighbour row as
     drawn, the column each sits in and that column's printed head, the lines,
     and whatever "two steps out" list is open, with the via each group names. */
  gn() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    const idOf = (a) => ((a && a.getAttribute('href')) || '').replace(/^#\/n\//, '').replace(/\/hood$/, '');
    const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    const rows = Array.prototype.map.call(document.querySelectorAll('.gn li.gn-row'), (li) => {
      const fam = li.closest('.gn-fam');
      const a = li.querySelector('a.gn-name');
      const m = a ? a.querySelector('.mark') : null;
      const say = li.querySelector('.gn-say');
      return {
        id: idOf(a), family: fam ? fam.getAttribute('data-family') : null,
        head: fam ? txt(fam.querySelector('.gn-flabel')) : '',
        name: txt(a && a.querySelector('.gn-label')), say: txt(say),
        title: (say && say.getAttribute('title')) || '',
        mw: m ? Math.round(m.getBoundingClientRect().width) : 0, mh: m ? Math.round(m.getBoundingClientRect().height) : 0,
        ...(a ? box(a) : { x: 0, y: 0, w: 0, h: 0 }),
      };
    });
    const fams = Array.prototype.map.call(document.querySelectorAll('.gn .gn-fam'), (f) => f.getAttribute('data-family'));
    const lines = Array.prototype.map.call(document.querySelectorAll('.gn .gn-lines path'), (p) => ({
      family: p.getAttribute('data-family'), d: p.getAttribute('d') || '',
    }));
    const open = Array.prototype.filter.call(document.querySelectorAll('.gn .gn-fam'), (f) => !!f.querySelector('.gn-two .gn-two-head'))
      .map((f) => ({
        family: f.getAttribute('data-family'),
        groups: Array.prototype.map.call(f.querySelectorAll('.gn-two .gn-via'), (v) => {
          const va = v.querySelector('.gn-via-head a.gn-via-name');
          return {
            via: idOf(va), viaText: txt(va), head: txt(v.querySelector('.gn-via-head')),
            ids: Array.prototype.map.call(v.querySelectorAll('li.gn-row2 a.gn-name'), (a) => idOf(a)),
            names: Array.prototype.map.call(v.querySelectorAll('li.gn-row2 .gn-label'), (e) => txt(e)),
          };
        }),
      }));
    const c = document.querySelector('.gn .gn-centre');
    return { centre: c ? c.getAttribute('data-id') : null, centreName: txt(c && c.querySelector('.gn-who')), rows, fams, lines, open };
  },

  /* #/places (phase 11): the markers on the grid, the labels beside it, and
     the list rows with the country group each sits under. */
  places() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    const plotOf = (el) => { const p = el.closest('.pl-plot'); return p ? p.getAttribute('data-plot') : null; };
    return {
      present: !!document.querySelector('.pl'),
      marks: Array.prototype.map.call(document.querySelectorAll('.pl .pl-mark'), (a) => {
        const b = box(a);
        return { id: a.getAttribute('data-id'), plot: plotOf(a), cx: b.x + b.w / 2, cy: b.y + b.h / 2, w: b.w, h: b.h };
      }),
      labels: Array.prototype.map.call(document.querySelectorAll('.pl .pl-label'), (a) => ({
        id: a.getAttribute('data-id'), plot: plotOf(a), text: txt(a), ...box(a),
      })),
      rows: Array.prototype.map.call(document.querySelectorAll('.pl li.pl-row'), (li) => {
        const a = li.querySelector('a.pl-name');
        const g = li.closest('.pl-country');
        return {
          id: li.getAttribute('data-id'), href: a ? a.getAttribute('href') : null, name: txt(a),
          group: g ? txt(g.querySelector('.pl-chead .eyebrow')) : '', coord: txt(li.querySelector('.pl-coord')),
        };
      }),
    };
  },

  /* Timeline, from the rendered items and the rendered lane boxes (phase 9:
     the lanes are sections, and an event a lane cannot name is in a count). */
  timeline() {
    const packs = Array.prototype.map.call(document.querySelectorAll('.tl-pack'), (p) => {
      const r = p.getBoundingClientRect();
      return {
        section: p.getAttribute('data-section'), era: p.getAttribute('data-era'),
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
      };
    });
    const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    const items = Array.prototype.map.call(document.querySelectorAll('[data-tl-item]'), (el) => ({
      id: el.getAttribute('data-id'), kind: el.getAttribute('data-kind'),
      era: el.getAttribute('data-era'), section: el.getAttribute('data-section'),
      text: (el.textContent || '').trim(), scheduled: el.getAttribute('data-scheduled') === '1', ...box(el),
    }));
    const mores = Array.prototype.map.call(document.querySelectorAll('[data-tl-more]'), (el) => ({
      id: 'more:' + el.getAttribute('data-section') + ':' + el.getAttribute('data-year'), kind: 'more',
      ids: (el.getAttribute('data-ids') || '').split(' ').filter(Boolean),
      era: el.getAttribute('data-era'), section: el.getAttribute('data-section'),
      year: el.getAttribute('data-year'), text: (el.textContent || '').trim(), ...box(el),
    }));
    const marks = document.querySelectorAll('[data-kind="mark"], .tl-mark').length;
    const open = document.querySelector('.tl-era.open');
    return {
      packs, items, mores, marks,
      openEraSub: open ? (open.querySelector('.tl-era-sub') || {}).textContent || '' : '',
      scopeText: ((document.querySelector('.tl-scope') || {}).textContent || ''),
    };
  },

  /* The timeline's panel as drawn (C53). */
  tlPanel() {
    const p = document.querySelector('.tl-detail');
    const t = (sel) => ((p && p.querySelector(sel)) || {}).textContent || '';
    const a = p && p.querySelector('a.tl-d-nodelink');
    return {
      shown: !!p && !p.hidden, mode: p ? p.getAttribute('data-mode') : null, id: p ? p.getAttribute('data-id') : null,
      date: t('.tl-d-date'), grade: t('.tl-d-grade'), label: t('.tl-d-label').trim(), text: t('.tl-d-text').trim(),
      node: a ? a.getAttribute('href') : null, nodeText: t('.tl-d-node'),
      reps: Array.prototype.map.call(p ? p.querySelectorAll('.tl-d-rep') : [], (r) => ({
        id: r.getAttribute('data-id'), label: ((r.querySelector('.tl-d-replabel') || {}).textContent || '').trim() })),
      srcs: p ? p.querySelectorAll('.tl-d-src a').length : 0,
      sched: t('.tl-sched'),
      list: Array.prototype.map.call(p ? p.querySelectorAll('.tl-li') : [], (li) => ({
        id: li.getAttribute('data-id'), label: ((li.querySelector('.tl-li-label') || {}).textContent || '').trim(),
        scheduled: li.getAttribute('data-scheduled') === '1' })),
    };
  },

  /* A directory as drawn (C50, C51): its rows, their links, its chips and counts. */
  directory() {
    const root = document.querySelector('.dir');
    const rows = Array.prototype.map.call(document.querySelectorAll('.dir-table tr.dir-row'), (tr) => {
      const a = tr.querySelector('.c-name a');
      return { id: tr.getAttribute('data-id'), href: a ? a.getAttribute('href') : null, name: a ? (a.textContent || '').trim() : '' };
    });
    const chips = Array.prototype.map.call(document.querySelectorAll('a.dir-chip'), (c) => ({
      key: c.getAttribute('data-key'), val: c.getAttribute('data-val'),
      n: Number(((c.querySelector('.dir-chip-n') || {}).textContent || '').trim()),
      on: c.getAttribute('aria-pressed') === 'true',
    }));
    return {
      present: !!root, dir: root ? root.getAttribute('data-dir') : null, rows, chips,
      count: Number(((document.querySelector('.dir-count') || {}).textContent || '').trim()),
    };
  },

  /* Every visible run of text as the browser laid it out: one box per line
     fragment of every text node, clipped by any ancestor that clips it (the
     folded analysis, a scrolling chip box), skipping what matches skipSel. */
  texts(skipSel) {
    const out = [];
    const clipOf = new Map();
    const clip = (el) => {
      if (clipOf.has(el)) return clipOf.get(el);
      let box = { l: -1e9, t: -1e9, r: 1e9, b: 1e9 };
      for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
        const cs = getComputedStyle(a);
        if (cs.display === 'contents') continue;
        if (cs.overflowX !== 'visible' || cs.overflowY !== 'visible') {
          const q = a.getBoundingClientRect();
          box = { l: Math.max(box.l, q.left), t: Math.max(box.t, q.top), r: Math.min(box.r, q.right), b: Math.min(box.b, q.bottom) };
        }
      }
      clipOf.set(el, box);
      return box;
    };
    const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let n, i = 0;
    while ((n = w.nextNode())) {
      if (!n.nodeValue || !n.nodeValue.trim()) continue;
      const el = n.parentElement;
      if (!el || (skipSel && el.closest(skipSel))) continue;
      /* a closed <details> keeps its content laid out in Chromium, unseen */
      const det = el.closest('details');
      if (det && !det.open && !el.closest('summary')) continue;
      if (el.checkVisibility && !el.checkVisibility({ visibilityProperty: true, opacityProperty: true })) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || Number(cs.opacity) === 0) continue;
      /* the ink of a line is its em box, not the taller content area the
         browser reports: 11px text on a 12px line does not overprint */
      const fs = parseFloat(cs.fontSize) || 11;
      const c = clip(el);
      const r = document.createRange();
      r.selectNodeContents(n);
      for (const q of r.getClientRects()) {
        const inset = Math.max(0, (q.height - fs) / 2);
        const l = Math.max(q.left, c.l), t = Math.max(q.top + inset, c.t);
        const rr = Math.min(q.right, c.r), b = Math.min(q.bottom - inset, c.b);
        if (rr - l < 1 || b - t < 1) continue;
        out.push({ id: (i++) + ':' + n.nodeValue.trim().slice(0, 22), x: l + scrollX, y: t + scrollY, w: rr - l, h: b - t,
          vx: l, vy: t });
      }
    }
    return out;
  },

  /* The closed analyst tab, and every text box it sits on (C32). */
  tabOver() {
    const host = document.getElementById('analyst');
    const bar = host && host.querySelector('.an-bar');
    if (!host || !bar) return { present: false };
    const r = bar.getBoundingClientRect();
    return { present: true, open: host.getAttribute('data-open'), x: r.left, y: r.top, w: r.width, h: r.height };
  },

  /* Claim rows and the mark each carries (C31). */
  said(rowSel) {
    return Array.prototype.map.call(document.querySelectorAll(rowSel), (r) => {
      const m = r.querySelector('.said-mark');
      const b = m ? m.getBoundingClientRect() : null;
      return {
        cid: r.getAttribute('data-cid') || '',
        kind: m ? m.getAttribute('data-said') : null,
        text: m ? (m.textContent || '').trim() : '',
        title: m ? (m.getAttribute('title') || '') : '',
        shown: !!b && b.width > 0 && b.height > 0,
      };
    });
  },

  /* The thread page's timeline slice, as laid out (C33). */
  slice() {
    const axis = document.querySelector('.ts-axis');
    const ar = axis ? axis.getBoundingClientRect() : null;
    return {
      axisR: ar ? ar.right + scrollX : 0, axisL: ar ? ar.left + scrollX : 0,
      labs: Array.prototype.map.call(document.querySelectorAll('.ts-lab'), (l, i) => {
        const r = l.getBoundingClientRect();
        const y = Number(((l.querySelector('.ts-year b') || {}).textContent || '').trim());
        return { id: i + ':' + y, year: y, x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
      }),
    };
  },

  /* The timeline's year axis and its era heads (C34). */
  tlAxis() {
    return {
      years: Array.prototype.map.call(document.querySelectorAll('.tl-years .tl-year'), (b) => Number(b.getAttribute('data-year'))),
      heads: Array.prototype.map.call(document.querySelectorAll('.tl-grid .tl-era .tl-era-label'), (e) => (e.textContent || '').trim()),
      openEra: ((document.querySelector('.tl-era.open .tl-era-label') || {}).textContent || '').trim(),
    };
  },

  /* A surface at phone width: its sideways overflow, and whether the thing
     the surface exists to show is there to read (C26). */
  phone(kind) {
    const vw = innerWidth, vh = innerHeight;
    const seen = (el, minW) => {
      const r = el.getBoundingClientRect();
      return r.width >= (minW || 1) && r.height > 0 && r.left >= -1 && r.right <= vw + 1;
    };
    const onFirst = (el) => { const r = el.getBoundingClientRect(); return r.top < vh && r.bottom > 0; };
    const txt = (el) => ((el && el.textContent) || '').trim();
    const all = (sel) => Array.prototype.slice.call(document.querySelectorAll(sel));
    const out = { scrollW: document.documentElement.scrollWidth, vw, kind, have: 0, want: 1, what: '' };
    if (kind === 'evidence') {
      const c = all('.ev-table td.c-claim').filter((td) => seen(td, 200) && onFirst(td) && txt(td).length > 20);
      out.have = c.length; out.what = 'claim texts readable on the first screen';
    } else if (kind === 'hood') {
      const rows = all('.gn li.gn-row .gn-label');
      out.want = Math.max(1, rows.length);
      out.have = rows.filter((e) => seen(e) && txt(e)).length;
      out.what = 'neighbours named and inside the screen';
    } else if (kind === 'node') {
      out.have = all('.claim .ctext').filter((e) => seen(e, 150) && txt(e)).length;
      out.what = 'claim rows readable';
    } else if (kind === 'home') {
      const p = document.querySelector('.home-para');
      out.have = p && seen(p, 300) && onFirst(p) ? 1 : 0;
      out.what = 'the introduction at a readable width on the first screen';
    } else if (kind === 'people' || kind === 'events') {
      out.have = all('.dir-row .c-name a').filter((e) => seen(e) && txt(e)).length;
      out.what = 'directory rows named';
    } else if (kind === 'timeline') {
      out.have = all('.tlp-row').filter((e) => seen(e, 200) && txt(e)).length;
      out.what = 'timeline events named';
    } else if (kind === 'thread') {
      out.have = all('.th-step .th-label').filter((e) => seen(e) && txt(e)).length;
      out.what = 'thread steps named';
    } else if (kind === 'patent') {
      out.have = all('.pt-card .pt-title').filter((e) => seen(e) && txt(e)).length;
      out.what = 'patents named';
    } else if (kind === 'report') {
      out.have = all('.report h1').filter((e) => seen(e) && txt(e)).length;
      out.what = 'the report headed';
    } else if (kind === 'atlas') {
      const li = all('.atlas-list a.atlas-li');
      out.want = Math.max(1, document.querySelectorAll('.atlas-list').length ? li.length : 1);
      out.have = li.filter((e) => seen(e) && txt(e)).length;
      out.what = 'topics named in the stacked lists';
    } else if (kind === 'library') {
      out.have = all('.lib-list a.lib-title').filter((e) => seen(e, 150) && txt(e)).length;
      out.what = 'sources named in the Library';
    } else if (kind === 'source') {
      out.have = all('.src-claims .src-claim-text').filter((e) => seen(e, 150) && txt(e)).length;
      out.what = 'claims citing the source readable';
    } else if (kind === 'topic') {
      out.have = all('.topic .ti .ti-text').filter((e) => seen(e, 150) && txt(e)).length;
      out.what = 'topic sentences readable';
    }
    return out;
  },

  /* The phone's VIEWS list, opened: every route a reader can reach from it. */
  /* The Library as drawn (C42): the count, the rows in order, every facet chip. */
  library() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    const cnt = document.querySelector('.lib-count');
    return {
      n: cnt ? Number(cnt.getAttribute('data-n')) : null,
      rows: Array.prototype.map.call(document.querySelectorAll('.lib-list > li.lib-row'), (r) => ({
        id: r.getAttribute('data-sid') || '',
        href: (r.querySelector('a.lib-title') || { getAttribute: () => '' }).getAttribute('href') || '',
        title: txt(r.querySelector('a.lib-title')),
      })),
      chips: Array.prototype.map.call(document.querySelectorAll('.lib-facet'), (f) => ({
        facet: f.getAttribute('data-facet') || '',
        chips: Array.prototype.map.call(f.querySelectorAll('a.lib-chip'), (c) => ({
          value: c.getAttribute('data-value'), n: Number(c.getAttribute('data-n')),
          shown: Number(txt(c.querySelector('.lib-chip-n')).replace(/[^0-9]/g, '')),
          on: c.classList.contains('on'),
        })),
      })),
    };
  },

  /* A source page as drawn (C43). */
  source() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    const root = document.querySelector('.srcpage');
    return {
      id: root ? root.getAttribute('data-sid') : null,
      h1: txt(document.querySelector('.srcpage h1')),
      urls: Array.prototype.map.call(document.querySelectorAll('.src-read a.src-url'), (a) => a.getAttribute('href')),
      archived: Array.prototype.map.call(document.querySelectorAll('.src-read a.src-arch'), (a) => a.getAttribute('href')),
      node: (document.querySelector('.src-read a.src-node') || { getAttribute: () => null }).getAttribute('href'),
      ip: !!document.querySelector('.src-ip'),
      claims: Array.prototype.map.call(document.querySelectorAll('.src-claims .src-claim'), (c) => ({
        id: c.getAttribute('data-cid') || '', tier: txt(c.querySelector('.ct')),
        text: txt(c.querySelector('.src-claim-text')), cited: txt(c.querySelector('.src-cited')),
        node: (c.closest('.src-group') || { getAttribute: () => '' }).getAttribute('data-node'),
      })),
      edges: Array.prototype.map.call(document.querySelectorAll('.src-edges .src-edge'), (e) => e.getAttribute('data-eid')),
    };
  },

  /* Every claim row's source links (C44): for rows matched by `sel`, the
     #/s/ targets it links, and its unlinked citation when it has none. */
  claimLinks(sel) {
    return Array.prototype.map.call(document.querySelectorAll(sel), (r) => ({
      cid: r.getAttribute('data-cid') || '',
      links: Array.prototype.map.call(r.querySelectorAll('a.src-link'), (a) => a.getAttribute('href')),
      nolink: !!r.querySelector('.nolink'),
      nolinkText: ((r.querySelector('.nolink') || {}).textContent || '').trim(),
    }));
  },

  /* Every printed web address (C45): its wrapping style, whether it stays
     inside the screen, and whether any stretch of it between two break points
     was itself broken across lines (a mid-word break). */
  urlWrap() {
    const vw = innerWidth;
    /* the folded copies too: an address is measured where a reader opens it */
    for (const d of document.querySelectorAll('details.src-more')) d.open = true;
    return Array.prototype.map.call(document.querySelectorAll('.url'), (el) => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      let split = 0, segs = 0;
      for (const n of el.childNodes) {
        if (n.nodeType !== 3 || !n.textContent) continue;
        segs++;
        const rg = document.createRange();
        rg.selectNodeContents(n);
        const tops = new Set(Array.prototype.map.call(rg.getClientRects(), (x) => Math.round(x.top)));
        if (tops.size > 1) split++;
      }
      return {
        text: (el.textContent || '').slice(0, 60), ow: cs.overflowWrap, wb: cs.wordBreak,
        wbr: el.querySelectorAll('wbr').length, len: (el.textContent || '').length,
        right: Math.round(r.right), vw, split, segs,
      };
    });
  },

  navOpen() {
    const vw = innerWidth, vh = innerHeight;
    const items = Array.prototype.slice.call(document.querySelectorAll('.bar .nav a, .bar .nav .nav-inert'));
    return items.map((el) => {
      const r = el.getBoundingClientRect();
      const top = r.width > 0 ? document.elementFromPoint(Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)) : null;
      return {
        label: (el.textContent || '').trim(), link: el.tagName === 'A',
        reachable: r.width > 0 && r.height > 0 && r.left >= 0 && r.right <= vw + 1 && r.bottom <= vh &&
          !!top && (top === el || el.contains(top)),
      };
    });
  },

  /* Home's start-here tour, in the order it is drawn (phase 6): each step's
     number, the flagged node it goes through and the topic it opens. */
  starthere() {
    return Array.prototype.map.call(document.querySelectorAll('.starthere .tour-step'), (s) => ({
      id: ((s.querySelector('a.tour-node') || { getAttribute: () => '' }).getAttribute('href') || '').slice(4),
      n: ((s.querySelector('.tour-n') || {}).textContent || '').trim(),
      topic: ((s.querySelector('a.tour-topic') || { getAttribute: () => '' }).getAttribute('href') || ''),
      label: ((s.querySelector('a.tour-topic') || {}).textContent || '').trim(),
    }));
  },

  /* Home's sections (C38): each section as drawn, with the topics it links. */
  homeSections() {
    return Array.prototype.map.call(document.querySelectorAll('.home-sections .hsec'), (s) => ({
      section: s.getAttribute('data-section') || '',
      topics: Array.prototype.map.call(s.querySelectorAll('a.hsec-topic'), (a) => (a.getAttribute('href') || '')),
    }));
  },

  /* A topic page as drawn (C36): every item of every block with each cite it
     renders, the members by role, the blocks, the research-gap label. */
  topic() {
    const txt = (el) => ((el && el.textContent) || '').trim();
    const root = document.querySelector('.topic');
    const items = Array.prototype.map.call(document.querySelectorAll('.topic .ti'), (it) => ({
      block: it.getAttribute('data-block') || '',
      text: txt(it.querySelector('.ti-text')),
      refs: it.querySelectorAll('.ti-text .ref').length,
      cites: Array.prototype.map.call(it.querySelectorAll('.cite'), (c) => {
        const m = c.querySelector('.said-mark');
        return {
          cid: c.getAttribute('data-cid') || '', kind: c.getAttribute('data-kind') || '',
          tier: txt(c.querySelector('.cite-tier')),
          said: m ? m.getAttribute('data-said') : null,
          words: txt(c.querySelector('.cite-words')),
          srcs: Array.prototype.map.call(c.querySelectorAll('.cite-src'), (s) => ({
            href: s.tagName === 'A' ? s.getAttribute('href') : null, text: txt(s),
          })),
          nodes: Array.prototype.map.call(c.querySelectorAll('a.cite-node'), (a) => a.getAttribute('href')),
        };
      }),
    }));
    return {
      id: root ? root.getAttribute('data-id') : null,
      h1: txt(document.querySelector('.topic h1')),
      items,
      members: Array.prototype.map.call(document.querySelectorAll('.topic .role-group'), (g) => ({
        role: g.getAttribute('data-role') || '',
        ids: Array.prototype.map.call(g.querySelectorAll('a.member'), (a) => (a.getAttribute('href') || '').replace(/^#\/n\//, '')),
      })),
      blocks: Array.prototype.map.call(document.querySelectorAll('.topic .tblock'), (b) => b.getAttribute('data-block')),
      gap: document.querySelector('.topic .topic-gap') ? txt(document.querySelector('.topic .topic-gap')) : null,
      scrollW: document.documentElement.scrollWidth, vw: innerWidth,
    };
  },

  /* The Atlas as the browser laid it out (C37): every chip with its label
     measured against its own box, every cell, and the links drawn. */
  atlas() {
    const box = (el) => { const r = el.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height }; };
    const chips = Array.prototype.map.call(document.querySelectorAll('.atlas-grid a.atlas-chip'), (c) => {
      const lab = c.querySelector('.atlas-label');
      const cs = lab ? getComputedStyle(lab) : null;
      const lb = lab ? box(lab) : null;
      const cb = box(c);
      return {
        id: c.getAttribute('data-id'), section: c.getAttribute('data-section'), era: c.getAttribute('data-era'),
        off: c.getAttribute('data-off') === '1', href: c.getAttribute('href'),
        ...cb,
        label: lab ? lab.textContent : null, fs: cs ? cs.fontSize : null, to: cs ? cs.textOverflow : null,
        lh: cs ? parseFloat(cs.lineHeight) : 0,
        labIn: !!lb && lb.x >= cb.x - 0.5 && lb.x + lb.w <= cb.x + cb.w + 0.5 && lb.y >= cb.y - 0.5 && lb.y + lb.h <= cb.y + cb.h + 0.5,
        labH: lb ? lb.h : 0,
        clipped: !!lab && (lab.scrollWidth > lab.clientWidth + 1 || lab.scrollHeight > lab.clientHeight + 1),
      };
    });
    const cells = Array.prototype.map.call(document.querySelectorAll('.atlas-grid .atlas-cell'), (c) => ({
      section: c.getAttribute('data-section'), era: c.getAttribute('data-era'), ...box(c),
    }));
    return {
      chips, cells,
      links: Array.prototype.map.call(document.querySelectorAll('.atlas-links .atlas-link'), (l) => l.getAttribute('data-to')),
      mode: (document.querySelector('.atlas-grid') || { getAttribute: () => null }).getAttribute('data-mode'),
      list: Array.prototype.map.call(document.querySelectorAll('.atlas-list a.atlas-li'), (a) => {
        const r = a.getBoundingClientRect();
        return { href: a.getAttribute('href'), named: ((a.textContent || '').trim().length > 0) && r.width > 0 && r.left >= -1 && r.right <= innerWidth + 1 };
      }),
      shown: document.querySelectorAll('.atlas-grid a.atlas-chip:not([data-off="1"])').length,
      scrollW: document.documentElement.scrollWidth, vw: innerWidth,
    };
  },

  /* The entity page's Appears in row (C39), and where it sits. */
  appears() {
    const row = document.querySelector('.node .appears');
    const about = Array.prototype.find.call(document.querySelectorAll('.node .sec.eyebrow'), (e) => /About/.test(e.textContent || ''));
    return {
      present: !!row,
      chips: Array.prototype.map.call(document.querySelectorAll('.node .appears a.appears-chip'), (a) => ({
        href: a.getAttribute('href') || '', role: a.getAttribute('data-role') || '',
        text: (a.textContent || '').trim(),
      })),
      top: row ? row.getBoundingClientRect().top : null,
      aboutTop: about ? about.getBoundingClientRect().top : null,
    };
  },

  /* The pointer on an absorbed domain node's page (C41), and where it sits. */
  absorbed() {
    const p = document.querySelector('.node .absorbed');
    const a = p && p.querySelector('a[href^="#/topic/"]');
    const h1 = document.querySelector('.node h1');
    return {
      present: !!p, href: a ? a.getAttribute('href') : null, text: p ? (p.textContent || '').trim() : '',
      top: p ? p.getBoundingClientRect().top : null, h1Top: h1 ? h1.getBoundingClientRect().top : null,
      vh: innerHeight,
    };
  },

  /* Thread chain, in the order it is drawn. */
  thread() {
    return {
      steps: Array.prototype.map.call(document.querySelectorAll('.th-step'), (s) => s.getAttribute('data-node')),
    };
  },
  /* the analyst dock, closed: the strip a reader has to be able to reach on
     every route, measured as the browser laid it out */
  dock() {
    const host = document.getElementById('analyst');
    const bar = host && host.querySelector('.an-bar');
    if (!host || !bar) return { present: false };
    const r = bar.getBoundingClientRect();
    const hr = host.getBoundingClientRect();
    return {
      present: true,
      open: host.getAttribute('data-open'),
      key: host.getAttribute('data-chipkey'),
      h: Math.round(r.height),
      /* on screen, not merely in the document */
      onScreen: r.height > 0 && r.width > 0 && r.bottom > 0 && r.top < innerHeight,
      /* nothing is drawn over the strip: the topmost element at its centre is
         the strip itself or something inside it */
      unobstructed: (() => {
        const el = document.elementFromPoint(Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2));
        return !!el && (el === bar || bar.contains(el));
      })(),
      hostBottom: Math.round(hr.bottom),
      viewport: innerHeight,
      /* A page that scrolls can bring anything out from under the tab, and
         #view pads its foot so the page's END is never trapped. A page that
         does NOT scroll cannot, so on those the tab has to cover nothing. */
      scrolls: document.documentElement.scrollHeight > innerHeight + 1,
      /* What the CLOSED tab is sitting on top of. It has to cover nothing: the
         map and the neighbourhood take the whole viewport and cannot give the
         dock any height, so the tab overlays instead, and the only place it may
         overlay is the map's band-label gutter, which carries nothing. The
         first build took 30px of height from both pages instead and put the
         map's lowest chip 23px into its own legend on CI. */
      covers: Array.prototype.map.call(
        document.querySelectorAll('a.chip, .map-legend > *, .cell-head, .hood-n, a[href], button'),
        (el) => {
          if (el.closest('#analyst')) return null;
          const q = el.getBoundingClientRect();
          if (q.width === 0 || q.height === 0) return null;
          if (q.left >= r.right || q.right <= r.left || q.top >= r.bottom || q.bottom <= r.top) return null;
          return (el.className || el.tagName) + ' "' + (el.textContent || '').trim().slice(0, 24) + '"';
        }).filter(Boolean),
    };
  },

  /* Drive every analyst tool and bring back what it answered. The tools draw
     nothing, so there is no DOM to read; window.__app.analyst.run is a pure
     function of the /data files and C19 re-derives every figure it checks. */
  /* An arrow, not a shorthand method like its neighbours, and passed to
     page.evaluate directly rather than through the `(function ${...})` template
     the rest of this file uses: an async shorthand stringifies as
     `async tools(calls){...}`, which that template turns into a syntax error. */
  tools: async (calls) => {
    const a = (window.__app || {}).analyst;
    if (!a) return { present: false };
    const out = {};
    for (const [key, name, args] of calls) {
      try { out[key] = await a.run(name, args); }
      catch (e) { out[key] = 'THREW: ' + (e && e.message ? e.message : String(e)); }
    }
    return { present: true, version: a.version, names: a.names, out };
  },

  /* The cited-id guard. It decides what a reader is told is not on the board,
     and it reaches the DOM only through an answer, so there is nothing to read
     unless the model has just spoken. This drives it directly. */
  cite: async (text) => {
    const a = (window.__app || {}).analyst;
    if (!a || !a.cite) return null;
    try { return await a.cite(text); } catch (e) { return { threw: String(e && e.message) }; }
  },

  /* Every citation the report at this route printed, in order. */
  cites() {
    const rows = Array.prototype.slice.call(document.querySelectorAll('.report .rcites div'));
    return {
      present: !!document.querySelector('.report'),
      h1: (document.querySelector('.report h1') || {}).textContent || '',
      steps: document.querySelectorAll('.report ol.rsteps li').length,
      sups: Array.prototype.map.call(document.querySelectorAll('.report .rsteps sup'), (e) => e.textContent),
      cites: rows.map((r) => {
        const a = r.querySelector('a');
        const n = r.querySelector('.cn');
        return {
          n: n ? n.textContent : '',
          text: (r.textContent || '').replace(/^\s*\d+\s*/, '').trim(),
          url: a ? a.getAttribute('href') : null,
        };
      }),
    };
  },

  /* Type into the bar's search and read back what it drew. The control is the
     same on every screen; this drives the one on Home. */
  search(q) {
    const box = document.querySelector('.searchbox input');
    if (!box) return { present: false };
    const panel = document.querySelector('.searchbox .results');
    const rows = Array.prototype.slice.call(panel ? panel.querySelectorAll('a.res') : []);
    return {
      present: true,
      q,
      heads: Array.prototype.map.call(panel ? panel.querySelectorAll('.res-head') : [], (e) => e.textContent),
      nodes: rows.filter((r) => !['claim', 'thread', 'event'].some((k) => r.classList.contains(k)))
        .map((r) => (r.getAttribute('href') || '').replace('#/n/', '')),
      claims: rows.filter((r) => r.classList.contains('claim')).map((r) => ({
        tier: Number(r.getAttribute('data-tier')),
        node: (r.getAttribute('href') || '').replace('#/n/', ''),
        hit: ((r.querySelector('.hit') || {}).textContent || ''),
        marked: ((r.querySelector('mark') || {}).textContent || ''),
      })),
    };
  },

  /* the chips as drawn, and the health line */
  chips() {
    const host = document.getElementById('analyst');
    const els = Array.prototype.slice.call(document.querySelectorAll('#analyst .an-chip'));
    const vis = els.filter((e) => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0; });
    return {
      key: host ? host.getAttribute('data-chipkey') : null,
      open: host ? host.getAttribute('data-open') : null,
      chips: vis.map((e) => {
        const t = e.querySelector('.an-chip-text');
        return (t ? t.textContent : e.textContent) || '';
      }),
      drawn: els.length,
      status: (document.querySelector('#analyst .an-status') || {}).textContent || '',
      where: (document.querySelector('#analyst .an-where') || {}).textContent || '',
    };
  },
};

/* ---- the poisons -------------------------------------------------------- */
/* Each damages the REAL page at one stop of the itinerary. None of them touches
   a predicate, a fixture or a probe: they change what the browser has drawn. */
const POISONS = {
  c1: {
    stops: ['home', 'topic', 'hood0', 'thread:custody', 'timeline', 'patents', 'evidence', 'report'],
    what: 'rewrites the first #/n/ href on every page to an id the board does not carry',
    fn: async (page) => page.evaluate(() => {
      const a = document.querySelector('a[href^="#/n/"]');
      if (a) a.setAttribute('href', '#/n/ghost-node-not-on-the-board');
    }),
  },
  c2: {
    stops: ['hood'],
    what: 'truncates one real neighbour name: 9px, clipped to 24px, with an ellipsis',
    fn: async (page) => page.evaluate(() => {
      const l = document.querySelectorAll('.gn li.gn-row .gn-label')[3];
      if (!l) return;
      l.style.fontSize = '9px';
      l.style.display = 'inline-block';
      l.style.maxWidth = '24px';
      l.style.overflow = 'hidden';
      l.style.textOverflow = 'ellipsis';
      l.textContent = l.textContent.slice(0, 6) + '…';
    }),
  },
  /* C3, C5 and C6 were the map's chips, its label and cell modes and its cell
     heads; they retired with the map in phase 11. */
  c4: {
    stops: ['hood'],
    what: 'moves one neighbour name up onto the name above it, so two share a box',
    fn: async (page) => page.evaluate(() => {
      const ns = document.querySelectorAll('.gn li.gn-row a.gn-name');
      if (ns.length < 2) return;
      const a = ns[0].getBoundingClientRect(), b = ns[1].getBoundingClientRect();
      ns[1].style.position = 'relative';
      ns[1].style.left = (a.left - b.left) + 'px';
      ns[1].style.top = (a.top - b.top) + 'px';
    }),
  },
  c7: {
    stops: ['thread:custody'],
    what: 'repoints the last thread step at a node with no join to the one before it',
    fn: async (page, ctx) => page.evaluate((id) => {
      const steps = document.querySelectorAll('.th-step');
      if (steps.length) steps[steps.length - 1].setAttribute('data-node', id);
    }, ctx.unjoined),
  },
  c8: {
    stops: ['node'],
    what: 'strips the source from one claim row, leaving the claim standing',
    fn: async (page) => page.evaluate(() => {
      const s = document.querySelector('.claim .csrc');
      if (!s) return;
      s.removeAttribute('href'); s.removeAttribute('title'); s.textContent = '';
    }),
  },
  c9: {
    stops: ['home'],
    what: 'adds a link to a path the URL scheme of section 2.1 does not carry',
    fn: async (page) => page.evaluate(() => {
      const a = document.createElement('a');
      a.setAttribute('href', '#/dossier/aawsap');
      a.textContent = 'dossier';
      document.querySelector('#view').appendChild(a);
    }),
  },
  /* C10 (the start-here ring and the 3-hop ring) retired with the ring in
     phase 11; C70 is the grouped neighbourhood that replaced it. */
  c70: {
    stops: ['hood'],
    what: 'names one neighbour twice: a copy of its row under its own column',
    fn: async (page) => page.evaluate(() => {
      const r = document.querySelector('.gn li.gn-row');
      if (r) r.parentElement.appendChild(r.cloneNode(true));
    }),
  },
  c70b: {
    check: 'c70',
    stops: ['hood'],
    what: 'moves one neighbour into the column of a family it does not sit in',
    fn: async (page) => page.evaluate(() => {
      const fams = Array.from(document.querySelectorAll('.gn .gn-fam'));
      if (fams.length < 2) return;
      const r = fams[0].querySelector('li.gn-row');
      const to = fams[1].querySelector('ul.gn-rows');
      if (r && to) to.appendChild(r);
    }),
  },
  c70c: {
    check: 'c70',
    stops: ['hood2'],
    what: 'strips the name from one "via" line of the open two-steps list',
    fn: async (page) => page.evaluate(() => {
      const v = document.querySelector('.gn .gn-two .gn-via .gn-via-name');
      if (v) v.remove();
    }),
  },
  c72: {
    stops: ['maprd'],
    what: 'puts the retired #/map back in the address bar, as if the old route had stayed where it was',
    fn: async (page) => page.evaluate(() => { history.replaceState(history.state, '', '#/map'); }),
  },
  c71: {
    stops: ['places'],
    what: 'drops one marker from the grid, leaving its label and its list row',
    fn: async (page) => page.evaluate(() => {
      const m = document.querySelectorAll('.pl .pl-mark')[4];
      if (m) m.remove();
    }),
  },
  c71b: {
    check: 'c71',
    stops: ['places'],
    what: 'lists one place a second time, under another country',
    fn: async (page) => page.evaluate(() => {
      const gs = document.querySelectorAll('.pl .pl-country');
      const r = document.querySelector('.pl li.pl-row');
      if (gs.length > 1 && r) (gs[1].querySelector('ul.pl-rows') || gs[1]).appendChild(r.cloneNode(true));
    }),
  },
  c71c: {
    check: 'c71',
    stops: ['places'],
    what: 'swaps two markers on the United States grid, so each stands where the other is',
    fn: async (page) => page.evaluate(() => {
      const ms = Array.from(document.querySelectorAll('.pl .pl-plot[data-plot="us"] .pl-mark'));
      let a = null, b = null;
      for (const x of ms) for (const y of ms) {
        if (!a && x !== y && Math.abs(x.offsetLeft - y.offsetLeft) > 40 && Math.abs(x.offsetTop - y.offsetTop) > 40) { a = x; b = y; }
      }
      if (!a) return;
      const al = a.style.left, at = a.style.top;
      a.style.left = b.style.left; a.style.top = b.style.top;
      b.style.left = al; b.style.top = at;
    }),
  },
  c11: {
    stops: ['home'],
    what: 'swaps two numbers in the start-here tour',
    fn: async (page) => page.evaluate(() => {
      const ns = document.querySelectorAll('.starthere .tour-step .tour-n');
      if (ns.length < 3) return;
      const t = ns[1].textContent; ns[1].textContent = ns[2].textContent; ns[2].textContent = t;
    }),
  },
  c12: {
    stops: ['hood'],
    what: "grows every neighbour's mark by its own degree, so size encodes connectedness",
    fn: async (page, ctx) => page.evaluate((deg) => {
      for (const r of document.querySelectorAll('.gn li.gn-row')) {
        const m = r.querySelector('.mark');
        const d = deg[r.getAttribute('data-id')] || 0;
        if (m) { m.style.width = m.style.height = (7 + Math.min(10, Math.round(d / 6))) + 'px'; }
      }
    }, ctx.deg),
  },
  c13: {
    stops: ['node'],
    what: 'drops one denial row from the node page, leaving it on the record',
    fn: async (page) => page.evaluate(() => {
      const d = document.querySelector('.denial');
      if (d) d.remove();
    }),
  },
  c14: {
    stops: ['home'],
    what: 'adds the Google Fonts stylesheet the spec forbids, and the page fetches it',
    fn: async (page) => {
      await page.evaluate(() => {
        const l = document.createElement('link');
        l.rel = 'stylesheet';
        l.href = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap';
        document.head.appendChild(l);
      });
      await page.waitForTimeout(900);
    },
  },
  c15: {
    stops: ['timeline'],
    what: 'moves one event chip into another section lane, relabelled as that lane',
    fn: async (page) => page.evaluate(() => {
      const packs = Array.prototype.slice.call(document.querySelectorAll('.tl-pack'));
      const from = packs.find((p) => p.querySelector('.tl-chip'));
      const to = packs.find((p) => p !== from);
      if (!from || !to) return;
      const chip = from.querySelector('.tl-chip');
      chip.setAttribute('data-section', to.getAttribute('data-section'));
      to.appendChild(chip);
    }),
  },
  c17: {
    /* 'back' is the C17 trail's own stop, re-applied after every render there,
       because the frame draws a fresh button on each route. */
    stops: ['back'],
    what: 'rewires the rendered back button to set location.hash instead of calling history.back()',
    fn: async (page) => page.evaluate(() => {
      const b = document.querySelector('button.nav-back');
      if (!b) return;
      const c = b.cloneNode(true);
      c.disabled = false;
      c.setAttribute('aria-disabled', 'false');
      c.addEventListener('click', () => { location.hash = '#/'; });
      b.replaceWith(c);
    }),
  },
  c16: {
    stops: ['atlas'],
    what: 'prints one of the mockup placeholder strings into the page',
    fn: async (page) => page.evaluate(() => {
      const d = document.createElement('div');
      d.textContent = '[placeholder: the band rule is not in the extract]';
      document.querySelector('#view').appendChild(d);
    }),
  },
  c18: {
    stops: ['chips'],
    what: "rewrites the chips the page drew into the home list, so every route's chips read as home's",
    fn: async (page) => page.evaluate(async () => {
      /* the page's own data file, so the poison plants real home chips rather
         than strings nothing would ever render */
      const r = await fetch('data/analyst.json');
      const j = await r.json();
      const home = (j.byRoute && j.byRoute.home) || j.suggestions || [];
      const chips = document.querySelectorAll('#analyst .an-chip .an-chip-text');
      chips.forEach((el, i) => { if (home[i % home.length]) el.textContent = home[i % home.length]; });
    }),
  },
  c19: {
    stops: ['tools'],
    what: 'makes the page fetch a short timeline.json, so the tools answer from 100 fewer events than the board has',
    fn: async (page) => page.evaluate(() => {
      /* the page's OWN fetch, patched before any tool has run and therefore
         before data.ts has cached anything: the tools then read a real
         response that is genuinely 100 events short */
      const real = window.fetch;
      window.fetch = async (input, init) => {
        const url = String(typeof input === 'string' ? input : input.url || '');
        const r = await real(input, init);
        if (!/timeline\.json/.test(url)) return r;
        const rows = await r.clone().json();
        return new Response(JSON.stringify(rows.slice(0, Math.max(0, rows.length - 100))),
          { status: 200, headers: { 'content-type': 'application/json' } });
      };
    }),
  },
  c21: {
    stops: ['threadreport'],
    what: "puts a source on a thread report's citation list that no edge on the board carries",
    fn: async (page) => page.evaluate(() => {
      const rows = document.querySelectorAll('.report .rcites div');
      const row = rows[rows.length - 1];
      if (!row) return;
      const a = row.querySelector('a');
      if (a) {
        a.textContent = 'Memorandum for the Record, 11 Feb 1954, RG 341 entry 214 box 9';
        a.setAttribute('href', 'https://www.archives.gov/no-such-record-11-feb-1954');
      } else {
        row.append(' Memorandum for the Record, 11 Feb 1954, RG 341 entry 214 box 9');
      }
    }),
  },
  c22: {
    stops: ['node', 'report'],
    what: 'turns one drawn arrow round on the node page and in the report, the way the board read before direction was recorded',
    fn: async (page) => page.evaluate(() => {
      for (const d of [document.querySelector('.node-side .conn-dir'), document.querySelector('.rconns .conn-dir')]) {
        if (d) d.textContent = d.textContent === '→' ? '←' : '→';
      }
    }),
  },
  c23: {
    stops: ['person', 'entity', 'entityq'],
    what: 'hides one unverified note on the person page, one conflict on S-4 and one of CEFAA\'s own open questions, and stacks the axis cells as the map\'s .cell rule once did',
    fn: async (page, _ctx, id) => page.evaluate((stopId) => {
      const sel = stopId === 'entity' ? '.node .cnf' : stopId === 'entityq' ? '.node .oq' : '.node .unv';
      const u = document.querySelectorAll(sel);
      if (u.length) u[u.length - 1].remove();
      if (stopId === 'person') for (const c of document.querySelectorAll('.node .axis .acell')) c.style.position = 'absolute';
      /* and puts the case against back where it was: below the whole About text */
      if (stopId === 'person') {
        const a = document.querySelector('.node .against');
        const m = document.querySelector('.node .node-main');
        const t = document.querySelector('.node .analysis-text');
        if (t) t.classList.remove('folded');
        if (a && m) m.append(a);
      }
    }, id),
  },
  c30: {
    stops: ['denial'],
    what: 'prints the old guessed direction on a denial the record does not adjudicate',
    fn: async (page) => page.evaluate(() => {
      const r = document.querySelector('.node .denials .denial[data-adjudicated="no"] .dkind');
      if (r) r.textContent = r.textContent.replace('direction not adjudicated', 'issued here');
    }),
  },
  c24: {
    stops: ['search'],
    what: 'removes the event and thread rows from the search results',
    fn: async (page) => page.evaluate(() => {
      for (const a of document.querySelectorAll('.results a.res.event, .results a.res.thread')) a.remove();
    }),
  },
  c25: {
    stops: ['evidence'],
    what: 'rewrites one node-level flag back to the claim-level word "denied"',
    fn: async (page) => page.evaluate(() => {
      const td = Array.from(document.querySelectorAll('td.c-den')).find((x) => x.textContent.trim());
      if (td) td.textContent = 'denied';
    }),
  },
  c27: {
    stops: ['home'],
    what: 'changes one figure in the counts panel by one, the way a stale index would',
    fn: async (page) => page.evaluate(() => {
      const td = document.querySelector('.panel.counts td.n');
      if (td) td.textContent = td.textContent.replace(/\d(?=\D*$)/, (d) => String((Number(d) + 1) % 10));
    }),
  },
  c28: {
    stops: ['home'],
    what: "puts one of the sibling board's sentences back into Home's prose",
    fn: async (page) => page.evaluate(() => {
      const p = document.querySelector('.home-para');
      if (p) p.append(' Fifty-two entities are listed who disappeared within three months.');
    }),
  },
  c29: {
    stops: ['analyst'],
    what: "rewrites the analyst's outgoing brief to name the sibling board's axes",
    fn: async (page) => page.evaluate(() => {
      const f = window.fetch;
      window.fetch = (u, o) => {
        if (o && typeof o.body === 'string' && /\/api\/analyst$/.test(String(u))) {
          o = Object.assign({}, o, { body: o.body.split('custody proximity').join('axes S, P and I') });
        }
        return f(u, o);
      };
    }),
  },
  c26: {
    stops: ['phone:evidence', 'phone:home', 'phone:node', 'phone:hood'],
    what: 'at phone width: forces a wide element into the evidence page, hides the VIEWS button, puts the desktop grid back on the node page, and empties the neighbourhood',
    fn: async (page, _ctx, id) => page.evaluate((stopId) => {
      if (stopId === 'phone:evidence') {
        const d = document.createElement('div');
        d.style.cssText = 'width:620px;height:4px';
        const m = document.querySelector('.ev-main');
        if (m) m.prepend(d);
      } else if (stopId === 'phone:home') {
        const t = document.querySelector('.nav-toggle');
        if (t) t.style.display = 'none';
      } else if (stopId === 'phone:node') {
        const n = document.querySelector('.node');
        if (n) n.style.gridTemplateColumns = 'minmax(0, 1fr) 520px';
      } else if (stopId === 'phone:hood') {
        for (const g of document.querySelectorAll('.gn .gn-rows')) g.remove();
      }
    }, id),
  },
  c31: {
    stops: ['person', 'evidence'],
    what: 'takes the said-on-the-record mark off one sworn claim and puts it on one documentary Tier 1 claim',
    fn: async (page, _ctx, id) => page.evaluate((stopId) => {
      const rows = Array.from(document.querySelectorAll(stopId === 'person' ? '.claim' : '.ev-table tbody tr[data-cid]'));
      const marked = rows.find((r) => r.querySelector('.said-mark'));
      const plain = rows.find((r) => !r.querySelector('.said-mark') && /T1/.test((r.querySelector('.ct, .c-tier') || {}).textContent || ''));
      if (marked) marked.querySelector('.said-mark').remove();
      if (plain) {
        const s = document.createElement('span');
        s.className = 'said-mark'; s.setAttribute('data-said', 'said'); s.textContent = 'said on the record';
        const host = plain.querySelector('.ctext, .c-claim');
        if (host) host.prepend(s);
      }
    }, id),
  },
  c32: {
    stops: ['tab:1920:node', 'tab:375:evidence'],
    what: 'puts the closed analyst tab back at the foot of the window, where it sat until phase 5b',
    fn: async (page) => page.evaluate(() => {
      const a = document.getElementById('analyst');
      if (a) { a.style.top = 'auto'; a.style.bottom = '0px'; a.style.left = '0px'; }
    }),
  },
  c33: {
    stops: ['thread:custody'],
    what: 'redraws the thread slice the way the old packing drew it: a later year on the row above an earlier one',
    fn: async (page) => page.evaluate(() => {
      const labs = document.querySelectorAll('.ts-lab');
      if (labs.length < 2) return;
      const t0 = labs[0].style.top, t1 = labs[1].style.top;
      labs[0].style.top = t1; labs[1].style.top = t0;
    }),
  },
  c34: {
    stops: ['timeline'],
    what: 'adds an empty future year to the axis and an empty NO DATE column head',
    fn: async (page) => page.evaluate(() => {
      const yh = document.querySelector('.tl-years');
      const last = yh && yh.lastElementChild;
      if (last) {
        const b = last.cloneNode(true);
        b.setAttribute('data-year', String(Number(last.getAttribute('data-year')) + 1));
        yh.append(b);
      }
      const g = document.querySelector('.tl-grid');
      const head = g && g.querySelector('.tl-era:not(.open)');
      if (head) {
        const c = head.cloneNode(true);
        const l = c.querySelector('.tl-era-label');
        if (l) l.textContent = 'NO DATE';
        head.after(c);
      }
    }),
  },
  c35: {
    stops: ['atlas', 'home'],
    what: "prints the map's old strip wording, and the raw route and viewport badge, back into the page",
    fn: async (page, _ctx, id) => page.evaluate((stopId) => {
      if (stopId === 'atlas') {
        const s = document.createElement('div');
        s.textContent = 'row pitch 18, band gap 12 · scale 1:1';
        document.querySelector('#view').appendChild(s);
      } else {
        const b = document.querySelector('.bar');
        if (b) {
          const f = document.createElement('span');
          f.textContent = location.hash + '  ' + innerWidth + '×' + innerHeight;
          b.append(f);
        }
      }
    }, id),
  },
  /* ---- phase 6. A check may carry several poisons: `check` names the check
     each must be seen by, so three different damages to one page each have to
     be caught on their own rather than one of them carrying the other two. */
  c36: {
    stops: ['topic'],
    what: 'drops one cite from one item of the record block of #/topic/roswell-1947',
    fn: async (page) => page.evaluate(() => {
      const c = document.querySelector('.topic .tblock[data-block="record"] .ti .cite');
      if (c) c.remove();
    }),
  },
  c36b: {
    check: 'c36',
    stops: ['topic2'],
    what: 'redraws one Tier 1 cite on #/topic/grusch-allegations as Tier 3',
    fn: async (page) => page.evaluate(() => {
      const t = Array.from(document.querySelectorAll('.topic .cite .cite-tier')).find((x) => (x.textContent || '').trim() === 'T1');
      if (t) { t.textContent = 'T3'; t.className = 'cite-tier t3'; }
    }),
  },
  c36c: {
    check: 'c36',
    stops: ['topic'],
    what: 'moves one member of #/topic/roswell-1947 into a role group it does not hold',
    fn: async (page) => page.evaluate(() => {
      const gs = Array.from(document.querySelectorAll('.topic .role-group'));
      const from = gs.find((g) => g.querySelectorAll('a.member').length > 1);
      const to = gs.find((g) => g !== from);
      if (from && to) (to.querySelector('.role-members') || to).append(from.querySelector('a.member'));
    }),
  },
  c37: {
    stops: ['atlas1366'],
    what: 'drops one chip from the Atlas',
    fn: async (page) => page.evaluate(() => {
      const c = document.querySelectorAll('.atlas-grid a.atlas-chip')[5];
      if (c) c.remove();
    }),
  },
  c37b: {
    check: 'c37',
    stops: ['atlas1920'],
    what: 'shrinks one Atlas label to 9px on one line, clipped with an ellipsis',
    fn: async (page) => page.evaluate(() => {
      const l = document.querySelectorAll('.atlas-grid a.atlas-chip .atlas-label')[3];
      if (!l) return;
      l.style.fontSize = '9px'; l.style.whiteSpace = 'nowrap'; l.style.overflow = 'hidden';
      l.style.textOverflow = 'ellipsis'; l.style.display = 'block'; l.style.maxWidth = '60px';
    }),
  },
  c37c: {
    check: 'c37',
    stops: ['atlas1366'],
    what: 'grows one Atlas chip by its member count, so size encodes membership',
    fn: async (page, ctx) => page.evaluate((members) => {
      const c = Array.from(document.querySelectorAll('.atlas-grid a.atlas-chip'))
        .find((x) => (members[x.getAttribute('data-id')] || 0) > 10);
      if (c) c.style.height = (c.getBoundingClientRect().height + members[c.getAttribute('data-id')]) + 'px';
    }, ctx.topicMembers),
  },
  c38: {
    stops: ['home'],
    what: "moves one topic link on Home into a section that is not the topic's own",
    fn: async (page) => page.evaluate(() => {
      const ss = document.querySelectorAll('.home-sections .hsec');
      if (ss.length < 2) return;
      const a = ss[0].querySelector('a.hsec-topic');
      const host = ss[1].querySelector('.hsec-topics') || ss[1];
      if (a) host.append(a.closest('li') || a);
    }),
  },
  c39: {
    stops: ['person'],
    what: "drops one topic from an entity's Appears in row and moves its primary topic last",
    fn: async (page) => page.evaluate(() => {
      const cs = Array.from(document.querySelectorAll('.node .appears a.appears-chip'));
      if (cs.length < 3) return;
      cs[cs.length - 1].remove();
      cs[0].parentElement.append(cs[0]);
    }),
  },
  c40: {
    stops: ['home'],
    what: 'puts THREADS back in the main row of the bar, out of More',
    fn: async (page) => page.evaluate(() => {
      const m = Array.from(document.querySelectorAll('.bar .nav .nav-more-list a')).find((a) => /THREADS/.test(a.textContent || ''));
      const nav = document.querySelector('.bar .nav');
      if (m && nav) nav.insertBefore(m, nav.firstChild.nextSibling);
    }),
  },
  c42: {
    stops: ['library'],
    what: 'drops the third row of the Library, leaving the count standing',
    fn: async (page) => page.evaluate(() => {
      const r = document.querySelectorAll('.lib-list > li.lib-row')[2];
      if (r) r.remove();
    }),
  },
  c42b: {
    check: 'c42',
    stops: ['libraryf'],
    what: 'raises one type chip of the filtered Library by one',
    fn: async (page) => page.evaluate(() => {
      const c = document.querySelector('.lib-facet[data-facet="type"] a.lib-chip');
      if (!c) return;
      const n = Number(c.getAttribute('data-n')) + 1;
      c.setAttribute('data-n', String(n));
      c.querySelector('.lib-chip-n').textContent = String(n);
    }),
  },
  c43: {
    stops: ['source'],
    what: 'removes one claim from the source page',
    fn: async (page) => page.evaluate(() => {
      const c = document.querySelectorAll('.src-claims .src-claim')[1];
      if (c) c.remove();
    }),
  },
  c43b: {
    check: 'c43',
    stops: ['source'],
    what: "repoints the source page's first web address at another page",
    fn: async (page) => page.evaluate(() => {
      const a = document.querySelector('.src-read a.src-url');
      if (a) a.setAttribute('href', 'https://www.gao.gov/');
    }),
  },
  c44: {
    stops: ['person'],
    what: "repoints one claim's source link at another source's page",
    fn: async (page) => page.evaluate(() => {
      const links = document.querySelectorAll('.claim a.src-link');
      if (links.length < 2) return;
      links[0].setAttribute('href', links[links.length - 1].getAttribute('href') === links[0].getAttribute('href')
        ? '#/s/gao-nsiad-95-187' : links[links.length - 1].getAttribute('href'));
    }),
  },
  c45: {
    stops: ['wrap375'],
    what: 'prints every web address on a phone source page as one unbroken string that may break anywhere',
    fn: async (page) => page.evaluate(() => {
      for (const u of document.querySelectorAll('.url')) {
        const t = u.textContent;
        u.textContent = t;
        u.style.overflowWrap = 'anywhere';
      }
    }),
  },
  c41: {
    stops: ['domain'],
    what: "repoints an absorbed domain node's topic pointer at a topic that did not absorb it",
    fn: async (page) => page.evaluate(() => {
      const a = document.querySelector('.node .absorbed a[href^="#/topic/"]');
      if (a) a.setAttribute('href', '#/topic/grusch-allegations');
    }),
  },
  c50: {
    stops: ['dir:people'],
    what: 'drops one row from the people directory and draws another twice',
    fn: async (page) => page.evaluate(() => {
      const rows = document.querySelectorAll('.dir-table tr.dir-row');
      if (rows.length < 3) return;
      rows[0].remove();
      rows[1].parentNode.appendChild(rows[1].cloneNode(true));
    }),
  },
  c51: {
    stops: ['dir:people:claimant'],
    what: 'adds one to the count on the dead chip and drops one claimant from the filtered rows',
    fn: async (page) => page.evaluate(() => {
      const c = document.querySelector('a.dir-chip[data-key="vital"][data-val="dead"] .dir-chip-n');
      if (c) c.textContent = String(Number(c.textContent) + 1);
      const r = document.querySelector('.dir-table tr.dir-row');
      if (r) r.remove();
    }),
  },
  c52: {
    stops: ['search52'],
    what: 'takes the topic rows out of the search list, and marks a row the keys did not reach',
    fn: async (page) => page.evaluate(() => {
      for (const r of document.querySelectorAll('.results a.res[data-type="topic"]')) r.remove();
    }),
  },
  c53: {
    stops: ['tl53'],
    what: 'puts another event\'s label in the timeline panel and takes its node link away',
    fn: async (page) => page.evaluate(() => {
      const l = document.querySelector('.tl-detail .tl-d-label');
      if (l) l.textContent = 'Some other event entirely';
      const a = document.querySelector('.tl-detail a.tl-d-nodelink');
      if (a) a.remove();
      const t = document.querySelector('.tl-detail .tl-d-text');
      if (t) t.textContent = 'x';
    }),
  },
  c20: {
    stops: ['search'],
    what: 'redraws the claim rows as the unranked code drew them: the first twelve matches in file order',
    fn: async (page) => page.evaluate(async () => {
      /* The exact defect this check exists for. Claim hits used to be
         `filter(...).slice(0, 12)` -- the first twelve in file order, which is
         alphabetical by node id -- so a search showed whichever claims sat
         early in the alphabet rather than the strongest. Reordering the drawn
         rows would not reproduce that: the ranked selection is twelve Tier 1
         rows and permuting them leaves twelve Tier 1 rows. So this recomputes
         the OLD SELECTION from the page's own claims.json and rewrites the
         rendered rows to it, tier attribute, link and excerpt together. */
      const box = document.querySelector('.searchbox input');
      const q = (box ? box.value : '').trim().toLowerCase();
      const rows = Array.prototype.slice.call(document.querySelectorAll('.searchbox .results a.res.claim'));
      if (!q || !rows.length) return;
      const all = await (await fetch('data/claims.json')).json();
      const old = all.filter((c) => c.text.toLowerCase().includes(q)).slice(0, rows.length);
      rows.forEach((row, i) => {
        const c = old[i];
        if (!c) return;
        row.setAttribute('data-tier', String(c.tier));
        row.setAttribute('href', '#/n/' + c.node);
        const meta = row.querySelector('.meta');
        if (meta) meta.textContent = 'T' + c.tier;
        const label = row.querySelector('.label');
        if (label) label.textContent = c.label;
        const hit = row.querySelector('.hit');
        if (hit) hit.textContent = c.text.slice(0, 150);
      });
    }),
  },
};

/* ---- the run ------------------------------------------------------------ */

async function main() {
  if (POISON && !POISONS[POISON]) {
    console.error('unknown poison: ' + POISON + '. One of ' + Object.keys(POISONS).join(', '));
    process.exit(2);
  }

  /* the board's own data, read straight off the server the browser is reading */
  /* Three tries, a second apart. On a Windows machine that has run hundreds of
     these in a night, a first connection to the preview is sometimes refused
     outright; a server that is really down still fails all three. */
  const jget = async (p) => {
    let last;
    for (let i = 0; i < 3; i++) {
      try {
        const r = await fetch(APP + p);
        if (!r.ok) throw new Error(p + ' -> HTTP ' + r.status);
        return await r.json();
      } catch (e) {
        last = e;
        await new Promise((res) => setTimeout(res, 1000));
      }
    }
    throw last;
  };
  let index, edges, threadsFile, highlights, tlEvents, focusRec, patentsFile, analystFile,
      claimRows, foiaFile, personRec, entityRec, entityQRec, denialRec,
      topicsFile, vocabFile, domainRec, topicRecs, libFile, srcRec, wrapRec, placesFile;
  try {
    [index, edges, threadsFile, highlights, tlEvents, focusRec, patentsFile, analystFile,
     claimRows, foiaFile, personRec, entityRec, entityQRec, denialRec, vocabFile] =
      await Promise.all([
        jget('data/index.json'), jget('data/edges.json'),
        jget('data/threads.json'), jget('data/highlights.json'), jget('data/timeline.json'),
        jget('data/nodes/' + NODE_FOCUS + '.json'), jget('data/patents.json'), jget('data/analyst.json'),
        jget('data/claims.json'), jget('data/foia.json'), jget('data/nodes/' + PERSON_FOCUS + '.json'),
        jget('data/nodes/' + ENTITY_FOCUS + '.json'), jget('data/nodes/' + ENTITY_OQ_FOCUS + '.json'),
        jget('data/nodes/' + DENIAL_FOCUS + '.json'), jget('data/vocab.json'),
      ]);
    [topicsFile, vocabFile, domainRec] = await Promise.all([
      jget('data/topics.json'), jget('data/vocab.json'), jget('data/nodes/' + DOMAIN_FOCUS + '.json'),
    ]);
    [libFile, srcRec] = await Promise.all([jget('data/sources.json'), jget('data/sources/' + SOURCE_FOCUS + '.json')]);
    placesFile = await jget('data/places.json');
    /* C45's page: the identified source with the most web addresses, archived
       copies included, chosen from the data so it follows the registry */
    const wrapRow = libFile.sources.filter((r) => r.archived > 0 && !/^[ut]-/.test(r.id))
      .sort((a, b) => (b.urls + b.archived) - (a.urls + a.archived) || (a.id < b.id ? -1 : 1))[0];
    wrapRec = wrapRow ? await jget('data/sources/' + wrapRow.id + '.json') : null;
    topicRecs = Object.fromEntries(await Promise.all(topicsFile.topics.map(async (t) =>
      [t.id, await jget('data/topics/' + t.id + '.json')])));
  } catch (e) {
    console.error('HARNESS: the app is not being served at ' + APP + ' (' + e.message +
      (e.cause ? ': ' + (e.cause.code || e.cause.message || e.cause) : '') + ').');
    console.error('Run `npm run build` then `npm run preview` in app/, or set APP_URL.');
    process.exit(2);
  }

  const ids = new Set(index.nodes.map((n) => n.id));
  const deg = Object.fromEntries(index.nodes.map((n) => [n.id, n.deg || 0]));
  const flags = highlights.flags.slice().sort((a, b) => a.rank - b.rank);
  const threads = threadsFile.threads || threadsFile;
  const threadIds = new Set(threads.map((t) => t.id));
  const patentNums = new Set((patentsFile.patents || []).map((p) => String(p.number).replace(/[^0-9]/g, '')));

  /* adjacency, once, from the sourced edge list */
  const adj = new Map();
  const put = (a, b) => { let s = adj.get(a); if (!s) { s = new Set(); adj.set(a, s); } s.add(b); };
  for (const e of edges) { put(e.a, e.b); put(e.b, e.a); }
  const joined = (a, b) => {
    if ((adj.get(a) || new Set()).has(b)) return 'direct';
    for (const x of adj.get(a) || []) if ((adj.get(b) || new Set()).has(x)) return 'derived';
    return null;
  };
  /* a node with no join at all to the last custody step, for the c7 poison */
  const custody = threads.find((t) => t.id === 'custody');
  const lastStep = custody ? custody.steps[custody.steps.length - 1].node : null;
  const unjoined = index.nodes.map((n) => n.id)
    .find((id) => id !== lastStep && !joined(lastStep, id)) || 'no-such-node';

  /* Phase 6: an entity's topics, re-derived here from the topic files
     themselves, not from topics.json's appearsIn: every topic whose members
     hold the node, the topics it anchors first, then by its role in the order
     vocab.json lists the roles, then by topic id. */
  const ROLE_ORDER = (vocabFile.topicRoles || []).map((r) => r.id);
  const topicsOf = (nid) => Object.values(topicRecs)
    .flatMap((t) => (t.members || []).filter((m) => m.id === nid).map((m) => ({
      topic: t.id, role: m.role, anchor: (t.anchors || []).includes(nid) ? 0 : 1,
    })))
    .sort((a, b) => a.anchor - b.anchor || ROLE_ORDER.indexOf(a.role) - ROLE_ORDER.indexOf(b.role) ||
      (a.topic < b.topic ? -1 : a.topic > b.topic ? 1 : 0));
  const topicIds = new Set(topicsFile.topics.map((t) => t.id));
  const sourceIds = new Set(libFile.sources.map((r) => r.id));
  const topicMembers = Object.fromEntries(topicsFile.topics.map((t) => [t.id, (topicRecs[t.id].members || []).length]));

  /* ---- C70's rule, restated ---------------------------------------------- */
  /* The grouped neighbourhood (phase 11) names each neighbour of the node ONCE,
     in the column of one relationship family: denials if any of its links is a
     denial, otherwise the first family, in vocab.json's order, among its links.
     Two steps out through a family are the nodes linked (edges.json) to one of
     that family's neighbours that are neither the node nor a neighbour. This is
     written again here from the record, not imported from the app. */
  const FAM_ORDER = (vocabFile.predicateFamilies || []).map((f) => f.id);
  const FAM_LABEL = Object.fromEntries((vocabFile.predicateFamilies || []).map((f) => [f.id, f.label]));
  const famRank = (f) => { const i = FAM_ORDER.indexOf(f); return i < 0 ? 99 : i; };
  const GN = (() => {
    const links = new Map();
    for (const c of focusRec.connections || []) {
      if (!ids.has(c.id)) continue;
      if (!links.has(c.id)) links.set(c.id, []);
      links.get(c.id).push(c.family || 'other');
    }
    const famOf = new Map();
    for (const [nid, fs] of links) {
      famOf.set(nid, fs.includes('denial') ? 'denial'
        : fs.slice().sort((a, b) => famRank(a) - famRank(b) || (a < b ? -1 : 1))[0]);
    }
    const byFam = new Map();
    for (const [nid, f] of famOf) { if (!byFam.has(f)) byFam.set(f, []); byFam.get(f).push(nid); }
    const two = (f) => {
      const out = new Set();
      for (const n of byFam.get(f) || []) for (const m of adj.get(n) || []) {
        if (m !== NODE_FOCUS && !famOf.has(m)) out.add(m);
      }
      return out;
    };
    /* the two families the drive opens: the largest columns that reach further */
    const twoFams = [...byFam.keys()].filter((f) => two(f).size > 0)
      .sort((a, b) => byFam.get(b).length - byFam.get(a).length || famRank(a) - famRank(b)).slice(0, 2);
    return { famOf, byFam, two, twoFams };
  })();
  const labelOf = new Map(index.nodes.map((n) => [n.id, n.label]));

  const ctx = { deg, unjoined, topicMembers };

  /* ---- browser ---------------------------------------------------------- */
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const requests = [];
  const pageErrors = [];
  page.on('request', (r) => requests.push(r.url()));
  page.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));

  const S = {};                       /* stop id -> snapshot                  */
  let current = null;
  async function poisonAt(p, id) {
    if (POISONS[POISON] && POISONS[POISON].stops.includes(id)) await POISONS[POISON].fn(p, ctx, id);
  }
  async function stop(id, hash, settle = 900, extra = null) {
    if (current === null) await page.goto(APP + hash, { waitUntil: 'load' });
    else if (current !== hash) await page.evaluate((h) => { location.hash = h; }, hash);
    current = hash;
    await page.waitForTimeout(settle);
    if (extra) await extra(page);
    await poisonAt(page, id);
    const s = await page.evaluate(`(function ${IN_PAGE.page})()`);
    S[id] = s;
    return s;
  }
  const ev = (fn, ...args) => page.evaluate(`(function ${fn})(${args.map((a) => JSON.stringify(a)).join(',')})`);

  /* ---- itinerary -------------------------------------------------------- */
  await stop('home', '#/', 1600);
  S.home.starthere = await ev(IN_PAGE.starthere);
  S.home.home = await ev(IN_PAGE.home);
  S.home.sections = await ev(IN_PAGE.homeSections);

  await stop('node', '#/n/' + NODE_FOCUS, 1200);
  S.node.node = await ev(IN_PAGE.node);
  S.node.conns = await ev(IN_PAGE.conns);
  S.node.fields = await ev(IN_PAGE.fields);
  S.node.appears = await ev(IN_PAGE.appears);
  S.node.absorbed = await ev(IN_PAGE.absorbed);
  S.node.links = await ev(IN_PAGE.claimLinks, '.claim[data-cid]');

  await stop('person', '#/n/' + PERSON_FOCUS, 1200);
  S.person.fields = await ev(IN_PAGE.fields);
  S.person.first = await ev(IN_PAGE.firstScreen);
  S.person.said = await ev(IN_PAGE.said, '.claim');
  S.person.appears = await ev(IN_PAGE.appears);
  S.person.links = await ev(IN_PAGE.claimLinks, '.claim[data-cid]');

  /* phase 6: the topic pages, a research gap, an absorbed domain node, the Atlas */
  await stop('topic', '#/topic/' + TOPIC_A, 1400);
  S.topic.topic = await ev(IN_PAGE.topic);
  await stop('topic2', '#/topic/' + TOPIC_B, 1400);
  S.topic2.topic = await ev(IN_PAGE.topic);
  await stop('topicgap', '#/topic/' + TOPIC_GAP, 1200);
  S.topicgap.topic = await ev(IN_PAGE.topic);
  await stop('domain', '#/n/' + DOMAIN_FOCUS, 1200);
  S.domain.absorbed = await ev(IN_PAGE.absorbed);
  await stop('atlas', '#/atlas', 1600);

  await stop('entity', '#/n/' + ENTITY_FOCUS, 1200);
  S.entity.fields = await ev(IN_PAGE.fields);

  await stop('entityq', '#/n/' + ENTITY_OQ_FOCUS, 1200);
  S.entityq.fields = await ev(IN_PAGE.fields);

  await stop('denial', '#/n/' + DENIAL_FOCUS, 1200);
  S.denial.rows = await ev(IN_PAGE.denials);

  /* phase 11: the program map's three routes land on what replaced them */
  await stop('maprd', '#/map', 1600);
  S.maprd.rd = await page.evaluate(() => ({ hash: location.hash, atlas: document.querySelectorAll('.atlas-grid a.atlas-chip, .atlas-list a.atlas-li').length }));
  await stop('maprdn', '#/n/' + NODE_FOCUS + '/map', 1200);
  S.maprdn.rd = await page.evaluate(() => ({ hash: location.hash, h1: (document.querySelector('#view h1') || {}).textContent || '' }));
  await stop('maprdt', '#/t/custody/map', 1200);
  S.maprdt.rd = await page.evaluate(() => ({ hash: location.hash, steps: document.querySelectorAll('.th-step').length }));

  await stop('hood0', '#/hood', 2000);

  /* phase 11: the grouped neighbourhood at rest, then two steps out through
     one family, then through another (only one may be open at a time) */
  await stop('hood', '#/hood/' + NODE_FOCUS, 2200);
  S.hood.gn = await ev(IN_PAGE.gn);
  S.hood.labels = await ev(IN_PAGE.labels, '.gn li.gn-row .gn-label', 'li.gn-row');
  const openTwo = (fam) => async (p) => {
    const b = p.locator('.gn .gn-fam[data-family="' + fam + '"] button.gn-two-b').first();
    if (await b.count()) { await b.click(); await p.waitForTimeout(700); }
  };
  await stop('hood2', '#/hood/' + NODE_FOCUS, 200, openTwo(GN.twoFams[0]));
  S.hood2.gn = await ev(IN_PAGE.gn);
  await stop('hood2b', '#/hood/' + NODE_FOCUS, 200, openTwo(GN.twoFams[1]));
  S.hood2b.gn = await ev(IN_PAGE.gn);

  /* A poison run only has to prove its own check fails, so it walks the shortest
     itinerary that still reaches that check. C7 needs all eight threads, and C17
     asks after every screen the itinerary reaches, so both walk the whole thing. */
  const walkAll = !POISON || POISON === 'c7' || POISON === 'c17';
  for (const t of (walkAll ? threads : threads.filter((x) => x.id === 'custody'))) {
    const id = 'thread:' + t.id;
    await stop(id, '#/t/' + t.id, 1400);
    S[id].thread = await ev(IN_PAGE.thread);
    S[id].slice = await ev(IN_PAGE.slice);
  }

  /* phase 9: an event's node is a link in the panel a click opens, so the
     itinerary opens it (C1 reads the node links a screen renders) */
  await stop('timeline', '#/timeline', 2400, async (p) => {
    const c = p.locator('.tl-chip').first();
    if (await c.count()) { await c.click(); await p.waitForTimeout(200); }
  });
  S.timeline.timeline = await ev(IN_PAGE.timeline);
  S.timeline.axis = await ev(IN_PAGE.tlAxis);

  /* phase 9: the six directories, and the people directory filtered by the
     side-car's own values (C50, C51) */
  const DIRCLS = { people: 'person', orgs: 'institution', programmes: 'program', laws: 'legislation', places: 'location', events: 'event' };
  const walkDirs = !POISON || POISON === 'c50' || POISON === 'c51' || POISON === 'c9' || POISON === 'c17';
  for (const d of (walkDirs ? Object.keys(DIRCLS) : [])) {
    await stop('dir:' + d, '#/' + d, 1400);
    S['dir:' + d].dir = await ev(IN_PAGE.directory);
  }
  if (walkDirs) {
    for (const [k, qs] of [['claimant', 'claimant=yes'], ['dead', 'vital=dead'], ['oath', 'oath=yes'], ['witness', 'role=witness']]) {
      await stop('dir:people:' + k, '#/people?' + qs, 1200);
      S['dir:people:' + k].dir = await ev(IN_PAGE.directory);
    }
  }

  /* phase 11: #/places, the grid and the list */
  await stop('places', '#/places', 1800);
  S.places.pl = await ev(IN_PAGE.places);

  await stop('patents', '#/patents/' + PATENT, 2000);
  await stop('evidence', '#/evidence', 3200);
  S.evidence.den = await page.evaluate(() =>
    Array.from(document.querySelectorAll('td.c-den')).map((td) => (td.textContent || '').trim()));
  S.evidence.said = await ev(IN_PAGE.said, '.ev-table tbody tr[data-cid]');
  /* phase 8: the Library, unfiltered, filtered and searched, and two source pages */
  await stop('library', '#/library', 1600);
  S.library.lib = await ev(IN_PAGE.library);
  await stop('libraryf', LIB_FILTER, 1200);
  S.libraryf.lib = await ev(IN_PAGE.library);
  await stop('libraryq', '#/library?q=' + LIB_SEARCH, 1200);
  S.libraryq.lib = await ev(IN_PAGE.library);
  await stop('source', '#/s/' + SOURCE_FOCUS, 1400);
  S.source.src = await ev(IN_PAGE.source);
  S.source.wrap = await ev(IN_PAGE.urlWrap);
  await stop('evidence2', '#/evidence?tier=1', 3200);
  S.evidence2.links = await ev(IN_PAGE.claimLinks, '.ev-table tbody tr[data-cid]');

  await stop('report', '#/report/n/' + NODE_FOCUS, 1600);
  S.report.rconns = await ev(IN_PAGE.rconns);
  S.report.said = await ev(IN_PAGE.said, '.report ol.rclaims li');

  await page.setViewportSize({ width: 1366, height: 768 });
  current = null;
  await stop('person1366', '#/n/' + PERSON_FOCUS, 1400);
  S.person1366.first = await ev(IN_PAGE.firstScreen);

  /* ---- C26's phone sweep and C32's tab sweep ------------------------------ */
  /* Every surface of the blind critic's sweep (tools/look.js --critic), at the
     three widths the critic is shown. At 375 each is a phone check (C26): no
     sideways scroll, no two text boxes on top of each other, the VIEWS list
     reaching every route, and the thing the surface exists for there to read.
     At every width the closed analyst tab must sit on no text at all (C32). */
  const CRITIC = [
    ['home', '#/'], ['node', '#/n/' + PERSON_FOCUS],
    ['hood', '#/n/' + PERSON_FOCUS + '/hood'], ['timeline', '#/timeline'], ['evidence', '#/evidence'],
    ['thread', '#/t/' + threads[0].id],
    ['patent', '#/patents/' + String((patentsFile.patents || [])[0].number).replace(/[^0-9]/g, '')],
    ['report', '#/report/n/' + PERSON_FOCUS],
    ['atlas', '#/atlas'], ['topic', '#/topic/' + TOPIC_A],
    ['people', '#/people'], ['events', '#/events'],
    ['library', '#/library'], ['source', '#/s/' + SOURCE_FOCUS],
  ];
  const settleOf = (hash) => hash.startsWith('#/evidence') ? 3200
    : /^#\/timeline/.test(hash) ? 2400 : /hood/.test(hash) ? 2200 : 1600;
  const PHONE = [], TAB = [];
  const WRAP375 = [];
  const sweepPhone = !POISON || POISON === 'c26' || POISON === 'c32' || POISON.startsWith('c45');
  for (const [w, hgt] of (sweepPhone ? [[375, 812], [1366, 768], [1920, 1080]] : [])) {
    if ((POISON === 'c26' || POISON.startsWith('c45')) && w !== 375) continue;
    const p = await browser.newPage({ viewport: { width: w, height: hgt } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    let first = true;
    for (const [name, hash] of CRITIC) {
      if (first) { await p.goto(APP + hash, { waitUntil: 'load' }); first = false; }
      else await p.evaluate((x) => { location.hash = x; }, hash);
      await p.waitForTimeout(settleOf(hash));
      await p.waitForFunction(() => {
        const a = document.getElementById('analyst');
        return !!(a && a.querySelector('.an-bar'));
      }, null, { timeout: 5000 }).catch(() => {});
      await poisonAt(p, 'tab:' + w + ':' + name);
      const tab = await p.evaluate(`(function ${IN_PAGE.tabOver})()`);
      const texts = await p.evaluate(`(function ${IN_PAGE.texts})(${JSON.stringify('#analyst')})`);
      TAB.push({ w, name, hash, tab, texts: tab.present ? texts.filter((t) =>
        t.vx < tab.x + tab.w && t.vx + t.w > tab.x && t.vy < tab.y + tab.h && t.vy + t.h > tab.y).map((t) => t.id) : [] });
      if (w !== 375) continue;
      await poisonAt(p, 'phone:' + name);
      const got = await p.evaluate(`(function ${IN_PAGE.phone})(${JSON.stringify(name)})`);
      if (name === 'source') WRAP375.push(...await p.evaluate(`(function ${IN_PAGE.urlWrap})()`));
      got.overlaps = pairsOverlapping(await p.evaluate(`(function ${IN_PAGE.texts})(${JSON.stringify('#analyst')})`), 4);
      /* the VIEWS list: one tap opens it, and every route is then one tap away */
      const tog = p.locator('.bar .nav-toggle').first();
      got.toggle = (await tog.count()) ? await tog.isVisible() : false;
      if (got.toggle) {
        await tog.click();
        await p.waitForTimeout(150);
        got.nav = await p.evaluate(`(function ${IN_PAGE.navOpen})()`);
        await tog.click();
        await p.waitForTimeout(100);
      } else got.nav = [];
      PHONE.push({ name, hash, ...got });
    }
    await p.close();
  }

  /* ---- C45's phone source page -------------------------------------------- */
  const WRAPX = [];
  if (wrapRec && (!POISON || POISON.startsWith('c45'))) {
    const p = await browser.newPage({ viewport: { width: 375, height: 812 } });
    await p.goto(APP + '#/s/' + wrapRec.id, { waitUntil: 'load' });
    await p.waitForTimeout(1400);
    await poisonAt(p, 'wrap375');
    WRAPX.push(...await p.evaluate(`(function ${IN_PAGE.urlWrap})()`));
    await p.close();
  }

  /* ---- C37's Atlas drive -------------------------------------------------- */
  /* At the two laptop sizes the plan names, on fresh pages: the chips at rest,
     then one chip focused by the mouse and one by the keyboard, then each
     filter on and off. Then the phone's stacked lists. */
  const AT = { sizes: {}, focus: null, filters: null, phone: null };
  const driveAtlas = !POISON || POISON.startsWith('c37');
  if (driveAtlas) {
    for (const [key, w, hgt] of [['atlas1366', 1366, 768], ['atlas1920', 1920, 950]]) {
      const p = await browser.newPage({ viewport: { width: w, height: hgt } });
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + '#/atlas', { waitUntil: 'load' });
      await p.waitForTimeout(1800);
      await poisonAt(p, key);
      AT.sizes[key] = await p.evaluate(`(function ${IN_PAGE.atlas})()`);
      if (key === 'atlas1920') {
        /* focus: the first chip whose topic names related topics */
        const withRel = topicsFile.topics.find((t) => (t.related || []).some((r) => topicIds.has(r)));
        const chip = withRel ? p.locator('.atlas-grid a.atlas-chip[data-id="' + withRel.id + '"]').first() : null;
        if (chip && await chip.count()) {
          await chip.hover(); await p.waitForTimeout(300);
          const hover = await p.evaluate(`(function ${IN_PAGE.atlas})()`);
          await p.mouse.move(2, 2); await p.waitForTimeout(250);
          const after = await p.evaluate(`(function ${IN_PAGE.atlas})()`);
          await chip.focus(); await p.waitForTimeout(300);
          const keyb = await p.evaluate(`(function ${IN_PAGE.atlas})()`);
          await p.evaluate(() => { if (document.activeElement) document.activeElement.blur(); });
          await p.waitForTimeout(200);
          AT.focus = { id: withRel.id, want: withRel.related.filter((r) => topicIds.has(r)),
            hover: hover.links, after: after.links, keyb: keyb.links };
        }
        /* filters: kind, contested, has open questions */
        const kind = topicsFile.topics[0].kind;
        const read = async () => (await p.evaluate(`(function ${IN_PAGE.atlas})()`)).shown;
        const f = { kind, want: {
          kind: topicsFile.topics.filter((t) => t.kind === kind).length,
          contested: topicsFile.topics.filter((t) => (t.counts.contested || 0) > 0).length,
          questions: topicsFile.topics.filter((t) => (t.counts.questions || 0) > 0).length,
        }, got: {} };
        const sel = p.locator('.atlas-filters select.af-kind').first();
        if (await sel.count()) {
          await sel.selectOption(kind); await p.waitForTimeout(200); f.got.kind = await read();
          await sel.selectOption(''); await p.waitForTimeout(200);
        }
        for (const [name, css] of [['contested', 'button.af-contested'], ['questions', 'button.af-questions']]) {
          const b = p.locator('.atlas-filters ' + css).first();
          if (!(await b.count())) continue;
          await b.click(); await p.waitForTimeout(200); f.got[name] = await read();
          await b.click(); await p.waitForTimeout(200);
        }
        f.reset = await read();
        AT.filters = f;
      }
      await p.close();
    }
    const p = await browser.newPage({ viewport: { width: 375, height: 812 } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    await p.goto(APP + '#/atlas', { waitUntil: 'load' });
    await p.waitForTimeout(1600);
    await poisonAt(p, 'atlas375');
    AT.phone = await p.evaluate(`(function ${IN_PAGE.atlas})()`);
    await p.close();
  }

  /* ---- C36's topic pages at phone width ----------------------------------- */
  const TP = [];
  if (!POISON || POISON.startsWith('c36')) {
    const p = await browser.newPage({ viewport: { width: 375, height: 812 } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    let first = true;
    for (const id of [TOPIC_A, TOPIC_B, TOPIC_GAP]) {
      if (first) { await p.goto(APP + '#/topic/' + id, { waitUntil: 'load' }); first = false; }
      else await p.evaluate((x) => { location.hash = x; }, '#/topic/' + id);
      await p.waitForTimeout(1400);
      await poisonAt(p, 'topic375');
      const t = await p.evaluate(`(function ${IN_PAGE.topic})()`);
      TP.push({ id, scrollW: t.scrollW, vw: t.vw, items: t.items.length, gap: !!t.gap });
    }
    await p.close();
  }

  /* ---- C40's More menu ------------------------------------------------------ */
  /* The routes that left the main row are one click away under More. */
  let MORE = null;
  if (!POISON || POISON === 'c40') {
    const p = await browser.newPage({ viewport: { width: 1366, height: 768 } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    await p.goto(APP + '#/atlas', { waitUntil: 'load' });
    await p.waitForTimeout(1400);
    const btn = p.locator('.bar .nav button.nav-more-btn').first();
    MORE = { btn: await btn.count() > 0, before: false, open: [], map: 0, hash: '' };
    if (MORE.btn) {
      MORE.before = await p.locator('.bar .nav .nav-more-list a').first().isVisible().catch(() => false);
      await btn.click(); await p.waitForTimeout(200);
      MORE.open = await p.evaluate(() => Array.from(document.querySelectorAll('.bar .nav .nav-more-list a')).map((a) => {
        const r = a.getBoundingClientRect();
        const top = r.width > 0 ? document.elementFromPoint(Math.round(r.left + r.width / 2), Math.round(r.top + r.height / 2)) : null;
        return { label: (a.textContent || '').trim(), href: a.getAttribute('href'), reachable: r.width > 0 && !!top && (top === a || a.contains(top)) };
      }));
    }
    await p.close();
  }

  /* ---- C9's route sweep ------------------------------------------------- */
  const ROUTES = [
    '#/', '#/n/' + NODE_FOCUS, '#/n/' + NODE_FOCUS + '/map', '#/n/' + NODE_FOCUS + '/hood',
    '#/hood/' + NODE_FOCUS, '#/hood', '#/map', '#/map?cell=oversight.2017-2026',
    '#/t/custody', '#/t/custody/map', '#/timeline', '#/timeline?era=3',
    '#/timeline?scope=n:' + NODE_FOCUS, '#/timeline?scope=t:custody',
    '#/patents/' + PATENT, '#/patents/' + PATENT + '?sheet=2',
    '#/evidence?tier=1&cls=person&cluster=other&denied=1&open=1',
    '#/report/n/' + NODE_FOCUS, '#/report/t/custody',
    '#/atlas', '#/topic/' + TOPIC_A, '#/topic/' + TOPIC_GAP, '#/n/' + DOMAIN_FOCUS,
    '#/people', '#/people?claimant=yes&sort=name', '#/orgs?era=1', '#/programmes', '#/laws', '#/places', '#/events',
    '#/timeline?topic=' + TOPIC_A, '#/timeline?strand=witness',
    '#/library', LIB_FILTER, '#/s/' + SOURCE_FOCUS,
  ];
  const deadRoutes = [];
  const sweepRoutes = !POISON || POISON === 'c9' || POISON === 'c17';
  current = null;
  for (const r of (sweepRoutes ? ROUTES : [])) {
    await page.goto(APP + r, { waitUntil: 'load' });
    await page.waitForTimeout(r.startsWith('#/evidence') ? 2600 : 1100);
    const nf = await page.evaluate(`(function ${IN_PAGE.page})()`);
    if (nf.notfound) deadRoutes.push(r);
    /* the swept routes are screens too: C9's href scan and C16's placeholder
       scan both walk everything in S, so the query-string states count. */
    if (!S[r]) S['route ' + r] = nf;
  }

  /* ---- C18's chip sweep -------------------------------------------------- */
  /* One route of every chip kind. The dock is opened by clicking the strip the
     reader clicks, so this proves the control works as well as the wiring. */
  const CHIP_ROUTES = [
    ['home', '#/'],
    ['node', '#/n/' + NODE_FOCUS],
    ['hood', '#/hood/' + NODE_FOCUS],
    ['thread', '#/t/custody'],
    ['timeline', '#/timeline'],
    ['patents', '#/patents/' + PATENT],
    ['evidence', '#/evidence'],
    ['report', '#/report/n/' + NODE_FOCUS],
  ];
  /* On a FRESH context per route, and that is not fussiness: `page.goto` to a
     URL that differs only in its hash is a same-document navigation, so the
     dock would still be open from the route before and every second click
     would close it rather than open it. The first cut of this check did
     exactly that and reported four routes broken that were not. A cold arrival
     is also the honest case: it is what a shared deep link is. */
  const CH = [];
  {
    const sweepChips = !POISON || POISON === 'c18';
    for (const [key, hash] of (sweepChips ? CHIP_ROUTES : [])) {
      const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + hash, { waitUntil: 'load' });
      await p.waitForTimeout(hash.startsWith('#/evidence') ? 3000 : 1500);
      /* a cold load on a busy machine can take longer than the settle above to
         mount the dock; wait for its chip key rather than read an empty dock */
      await p.waitForFunction(() => {
        const a = document.getElementById('analyst');
        return !!(a && a.getAttribute('data-chipkey'));
      }, null, { timeout: 10000 }).catch(() => {});
      const strip = await p.evaluate(`(function ${IN_PAGE.dock})()`);
      const opener = p.locator('#analyst .an-bar').first();
      if (await opener.count()) { await opener.click(); await p.waitForTimeout(400); }
      /* The health line asks the Worker over the network. A slow answer is not a
         broken one, so wait for the line to settle; one that never settles still
         reads "checking" and still fails C18. */
      await p.waitForFunction(() => {
        const s = document.querySelector('#analyst .an-status');
        return !s || !/^checking/.test(s.textContent || '');
      }, null, { timeout: 20000 }).catch(() => {});   /* the page gives up after 8s per candidate */
      await poisonAt(p, 'chips');
      const read = await p.evaluate(`(function ${IN_PAGE.chips})()`);
      CH.push({ key, hash, strip, ...read });
      await p.close();
    }
  }

  /* ---- C21's thread report ----------------------------------------------- */
  /* THE ONE RULE THAT NEVER BENDS, checked on the one page that composes a
     citation list out of two different places. Every citation a thread report
     prints must either be marked as the authored thread file, or be a source
     string that the board itself carries on the edge that step is joined by.
     Nothing may be composed here. */
  let TR = { present: false };
  {
    const tid = 'custody';
    const th = threads.find((t) => t.id === tid);
    const driveReport = !POISON || POISON === 'c21';
    if (driveReport && th) {
      const p = await browser.newPage({ viewport: { width: 1400, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + '#/report/t/' + tid, { waitUntil: 'load' });
      await p.waitForTimeout(2200);
      await poisonAt(p, 'threadreport');
      TR = await p.evaluate(`(function ${IN_PAGE.cites})()`);
      await p.close();

      /* every source string the board carries on this thread's own joins, read
         from the node records rather than from the page */
      const allowed = new Set();
      for (let i = 1; i < th.steps.length; i++) {
        const rec = await jget('data/nodes/' + th.steps[i].node + '.json').catch(() => null);
        if (!rec) continue;
        const conn = (rec.connections || []).find((c) => c.id === th.steps[i - 1].node);
        for (const sc of (conn && conn.sources) || []) {
          if (sc.name) allowed.add(sc.name);
          if (sc.url) allowed.add(sc.url);
        }
      }
      TR.allowed = allowed;
      TR.thread = th;
    }
  }

  /* ---- C20's search drive ------------------------------------------------ */
  /* Search is on every screen and had no check at all until 12 September 2026,
     which is how its claim hits stayed unranked -- the first twelve matches in
     file order, alphabetical by node id -- through every gate this repo runs.
     The query and both expectations are derived here from claims.json and
     index.json, never written down. */
  let SEARCH = { present: false };
  {
    /* a word with plenty of Tier 1 matches and some weaker ones, so a ranked
       result and a file-ordered one cannot look the same */
    const WORDS = ['roswell', 'battelle', 'grusch', 'aawsap', 'nimitz'];
    let word = null, t1 = 0, other = 0;
    for (const w of WORDS) {
      const m = claimRows.filter((c) => c.text.toLowerCase().includes(w));
      const a = m.filter((c) => c.tier === 1).length;
      if (a >= 14 && m.length - a >= 3) { word = w; t1 = a; other = m.length - a; break; }
    }
    /* and a two-word query taken out of a hyphenated label, which the old
       substring-only matcher could not answer at all */
    const hy = index.nodes.find((n) => /^[A-Za-z]{4,}-[A-Za-z]{4,}$/.test(
      (n.label.match(/[A-Za-z]{4,}-[A-Za-z]{4,}/) || [''])[0]) && n.label.match(/[A-Za-z]{4,}-[A-Za-z]{4,}/));
    const pair = hy ? hy.label.match(/([A-Za-z]{4,})-([A-Za-z]{4,})/) : null;
    const twoWord = pair ? (pair[1] + ' ' + pair[2]).toLowerCase() : null;

    const driveSearch = !POISON || POISON === 'c20' || POISON === 'c24' || POISON === 'c52';
    if (driveSearch && word) {
      const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + '#/', { waitUntil: 'load' });
      await p.waitForTimeout(1600);
      const type = async (q) => {
        await p.locator('.searchbox input').first().fill(q);
        await p.waitForTimeout(1600);          /* claims.json loads on the first query */
        /* and on a loaded machine it can take longer than that: wait (up to 10s)
           until the panel no longer says it is loading claim text */
        await p.waitForFunction(() => !Array.from(document.querySelectorAll('.searchbox .res-empty'))
          .some((e) => /loading claim text/.test(e.textContent || '')), null, { timeout: 10000 }).catch(() => {});
      };
      await type(word);
      await poisonAt(p, 'search');
      SEARCH = await p.evaluate(IN_PAGE.search, word);
      SEARCH.want = { word, t1, other, twoWord, twoWordId: hy ? hy.id : null };
      if (twoWord) {
        await type(twoWord);
        SEARCH.two = await p.evaluate(IN_PAGE.search, twoWord);
      }
      /* C24: timeline events and threads are searchable too */
      await type('scandinavia');
      if (POISON === 'c24') await poisonAt(p, 'search');
      SEARCH.events = await p.evaluate(() => document.querySelectorAll('.results a.res.event').length);
      await type('wilson davis');
      if (POISON === 'c24') await poisonAt(p, 'search');
      SEARCH.threads = await p.evaluate(() => document.querySelectorAll('.results a.res.thread').length);
      /* C52: a topic's own title finds the topic first; a directory's name finds
         the directory; every row says what it is; the keys move and open */
      const rowsNow = () => p.evaluate(() => Array.from(document.querySelectorAll('.results a.res')).map((a) => ({
        href: a.getAttribute('href'), type: a.getAttribute('data-type'),
        badge: ((a.querySelector('.badge') || {}).textContent || '').trim(), sel: a.getAttribute('aria-selected') })));
      const tA = topicsFile.topics.find((t) => t.id === TOPIC_A);
      await type(tA.title);
      await poisonAt(p, 'search52');
      SEARCH.topic = { q: tA.title, rows: await rowsNow() };
      await type('people');
      SEARCH.dir = await rowsNow();
      await type('roswell');
      const inp = p.locator('.searchbox input').first();
      await inp.press('ArrowDown'); await inp.press('ArrowDown'); await p.waitForTimeout(150);
      SEARCH.keys = { rows: await rowsNow() };
      if (POISON === 'c52') await poisonAt(p, 'search52');
      await inp.press('Enter'); await p.waitForTimeout(900);
      SEARCH.keys.hash = await p.evaluate(() => location.hash);
      await p.locator('.searchbox input').first().fill('roswell'); await p.waitForTimeout(600);
      await p.locator('.searchbox input').first().press('Escape'); await p.waitForTimeout(150);
      SEARCH.escape = await p.evaluate(() => {
        const i = document.querySelector('.searchbox input'), r = document.querySelector('.searchbox .results');
        return { value: i ? i.value : null, hidden: r ? r.hidden : null };
      });
      await p.close();
    }
  }

  /* ---- C53's timeline drive -------------------------------------------- */
  /* The panel (a chip, then a count's named list, then a same-day repeat), the
     scheduled mark, the topic scope and the strand filter, on fresh pages. */
  let TL = null;
  if (!POISON || POISON === 'c53') {
    const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    await p.goto(APP + '#/timeline', { waitUntil: 'load' });
    await p.waitForTimeout(2400);
    const panel = () => p.evaluate(`(function ${IN_PAGE.tlPanel})()`);
    TL = { base: await p.evaluate(`(function ${IN_PAGE.timeline})()`) };
    /* the first chip whose event names a node and carries text */
    const pickChip = TL.base.items.find((i) => { const e = tlEvents.find((x) => x.id === i.id); return e && e.node && e.text; });
    if (pickChip) {
      await p.locator('.tl-chip[data-id="' + pickChip.id + '"]').first().click(); await p.waitForTimeout(250);
      await poisonAt(p, 'tl53');
      TL.chip = { id: pickChip.id, panel: await panel() };
    }
    const more = TL.base.mores.slice().sort((a, b) => b.ids.length - a.ids.length)[0];
    if (more) {
      await p.locator('.tl-more[data-section="' + more.section + '"][data-year="' + more.year + '"]').first().click();
      await p.waitForTimeout(250);
      TL.more = { more, panel: await panel() };
    }
    /* a kept event with a repeat, in the open era */
    const openIds = new Set([...TL.base.items.map((i) => i.id), ...TL.base.mores.flatMap((m) => m.ids)]);
    const keep = tlEvents.find((e) => openIds.has(e.id) && tlEvents.some((x) => x.sameAs === e.id));
    if (keep) {
      const onChip = TL.base.items.find((i) => i.id === keep.id);
      if (onChip) await p.locator('.tl-chip[data-id="' + keep.id + '"]').first().click();
      else {
        const m = TL.base.mores.find((x) => x.ids.includes(keep.id));
        await p.locator('.tl-more[data-section="' + m.section + '"][data-year="' + m.year + '"]').first().click();
        await p.waitForTimeout(200);
        await p.locator('.tl-detail .tl-li[data-id="' + keep.id + '"]').first().click();
      }
      await p.waitForTimeout(250);
      TL.rep = { keep, panel: await panel() };
    }
    /* every scheduled event in the open era, where it is drawn */
    TL.sched = [];
    for (const e of tlEvents.filter((x) => openIds.has(x.id) && String(x.date).slice(0, 10) > String(index.generated).slice(0, 10))) {
      const onChip = TL.base.items.find((i) => i.id === e.id);
      if (onChip) { TL.sched.push({ id: e.id, marked: onChip.scheduled }); continue; }
      const m = TL.base.mores.find((x) => x.ids.includes(e.id));
      await p.locator('.tl-more[data-section="' + m.section + '"][data-year="' + m.year + '"]').first().click();
      await p.waitForTimeout(200);
      const pn = await panel();
      const li = pn.list.find((x) => x.id === e.id);
      TL.sched.push({ id: e.id, marked: !!li && li.scheduled });
    }
    await p.evaluate((x) => { location.hash = x; }, '#/timeline?topic=' + TOPIC_A);
    await p.waitForTimeout(2000);
    TL.topic = await p.evaluate(`(function ${IN_PAGE.timeline})()`);
    await p.evaluate((x) => { location.hash = x; }, '#/timeline?strand=witness');
    await p.waitForTimeout(2000);
    TL.strand = await p.evaluate(`(function ${IN_PAGE.timeline})()`);
    await p.close();
  }

  /* ---- C29's analyst brief ----------------------------------------------- */
  /* What the analyst is told about the board is the request the page sends, so
     that is what is read: the Worker route is intercepted and answered here, and
     no question reaches the model or spends a token. */
  let BRIEF = null;
  if (!POISON || POISON === 'c29') {
    const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
    let body = null;
    await p.route('**/api/analyst', async (route) => {
      try { body = JSON.parse(route.request().postData() || 'null'); } catch { body = null; }
      await route.fulfill({
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ content: [{ type: 'text', text: 'Check reply.' }], stop_reason: 'end_turn',
          usage: { input_tokens: 1, output_tokens: 1 } }),
      });
    });
    await p.goto(APP + '#/', { waitUntil: 'load' });
    await p.waitForTimeout(1500);
    await poisonAt(p, 'analyst');
    const bar = p.locator('#analyst .an-bar').first();
    if (await bar.count()) { await bar.click(); await p.waitForTimeout(400); }
    const input = p.locator('#analyst input[type="text"]').first();
    if (await input.count()) {
      await input.fill('What is on this board?');
      await input.press('Enter');
      for (let i = 0; i < 40 && !body; i++) await p.waitForTimeout(250);
    }
    const sys = body ? body.system : null;
    BRIEF = {
      sent: !!body,
      text: typeof sys === 'string' ? sys
        : Array.isArray(sys) ? sys.map((b) => (b && b.text) || '').join('\n') : '',
    };
    await p.close();
  }

  /* ---- C19's tool drive -------------------------------------------------- */
  /* The twelve analyst tools are its whole reach over the board and they draw
     nothing, so C18's DOM reading cannot see whether one of them is answering
     from the data or from nowhere. This drives each one on a cold page and
     compares what it said with a figure derived here, in this file, from the
     same JSON the browser is reading. */
  let TOOLS = { present: false };
  {
    /* two nodes the sourced edge list joins directly, and one pair it does not
       join at all, both derived rather than written down */
    const firstEdge = edges[0];
    const pairA = firstEdge.a, pairB = firstEdge.b;
    const noJoin = index.nodes.map((n) => n.id).find((id) => id !== pairA && !joined(pairA, id)) || 'no-such-node';
    const CALLS = [
      ['all', 'nodes', { count_only: true }],
      ['people', 'nodes', { cls: 'person', count_only: true }],
      ['byera', 'nodes', { group_by: 'era' }],
      ['bandgone', 'nodes', { band: 'custody', count_only: true }],
      ['claims', 'claims', { count_only: true }],
      ['t1', 'claims', { tier: 1, count_only: true }],
      ['tl', 'timeline', { count_only: true }],
      ['tl2004', 'timeline', { from: '2004', to: '2004', count_only: true }],
      ['edges', 'edges', { count_only: true }],
      ['edgesof', 'edges', { node: NODE_FOCUS, count_only: true }],
      ['path1', 'path', { from: pairA, to: pairB }],
      ['path0', 'path', { from: pairA, to: noJoin, max_hops: 1 }],
      ['find', 'find', { query: NODE_FOCUS, limit: 5 }],
      ['node', 'node', { ids: [NODE_FOCUS], sections: ['dossier'] }],
      ['threads', 'thread', {}],
      ['patents', 'patent', {}],
      ['foia', 'foia', {}],
      ['map', 'map', {}],
      ['overview', 'overview', {}],
      ['bogus', 'node', { ids: ['ghost-node-not-on-the-board'] }],
    ];
    const driveTools = !POISON || POISON === 'c19';
    if (driveTools) {
      const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + '#/', { waitUntil: 'load' });
      await p.waitForTimeout(1500);
      await poisonAt(p, 'tools');       /* before any tool has run, so nothing is cached yet */
      TOOLS = await p.evaluate(IN_PAGE.tools, CALLS);
      /* The guard, on the same page: a real node id, a real cluster, a real
         thread, a plain word in backticks that is not an id at all, and one
         fabricated id that must be caught. (It named a map cell until the map
         retired in phase 11: the first live question cited `disclosure.3` and
         the guard called it "not a node on this board", true and useless.) */
      const cellId = (index.clusters[0] || { id: 'legacy' }).id;
      TOOLS.cite = await p.evaluate(IN_PAGE.cite,
        'The node `' + NODE_FOCUS + '` sits in cluster `' + cellId + '` on the '
        + '`' + (threads[0] || { id: 'custody' }).id + '` thread, a `program`, '
        + 'sourced to `www.govinfo.gov` and `archive.org`, '
        + 'unlike `ghost-node-not-on-the-board`.');
      TOOLS.citeWant = { node: NODE_FOCUS, cell: cellId, thread: (threads[0] || { id: 'custody' }).id };
      TOOLS.want = {
        all: index.nodes.length,
        people: index.nodes.filter((n) => n.cls === 'person').length,
        claims: claimRows.length,
        t1: claimRows.filter((c) => c.tier === 1).length,
        tl: tlEvents.length,
        tl2004: tlEvents.filter((e) => e.date.slice(0, 4) === '2004').length,
        edges: edges.length,
        edgesof: edges.filter((e) => e.a === NODE_FOCUS || e.b === NODE_FOCUS).length,
        eras: Object.fromEntries(index.eras.map((e) => [e.id + ' ' + e.label, index.nodes.filter((n) => n.era === e.id).length])),
        threadIds: threads.map((t) => t.id),
        patentNums: (patentsFile.patents || []).map((x) => String(x.number)),
        foia: (foiaFile.requests || []).length,
        pairA, pairB, noJoin,
      };
      await p.close();
    }
  }

  /* ---- C17's back trail ------------------------------------------------- */
  /* On fresh contexts, because the history this reads has to be the reader's own
     and the itinerary above has filled this one with a hundred entries. */
  const B = { fresh: null, trail: [], clicks: [], forward: null, parity: {} };
  {
    const mkPage = async () => {
      const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      return p;
    };
    /* the control as the browser has it: its state, and where the page ended up */
    const readBack = (p) => p.evaluate(() => {
      const b = document.querySelector('button.nav-back');
      return {
        hash: location.hash || '#/', present: !!b,
        disabled: b ? b.disabled === true : null,
        aria: b ? b.getAttribute('aria-disabled') : null,
        title: b ? (b.getAttribute('title') || '') : '',
      };
    });
    const rest = async (p, ms) => { await p.waitForTimeout(ms); await poisonAt(p, 'back'); return readBack(p); };
    const hit = (p) => p.locator('button.nav-back').first().click({ force: true });
    /* Home, then a node, then that node's map, by clicking the pages' own links */
    const walk = async (p) => {
      const out = [];
      await p.goto(APP + '#/', { waitUntil: 'load' });
      out.push(await rest(p, 1600));
      await p.locator('.starthere a.tour-node[href="#/n/' + NODE_FOCUS + '"]').first().click({ timeout: 5000 }).catch(() => {});
      out.push(await rest(p, 1400));
      await p.locator('a[href="#/n/' + NODE_FOCUS + '/hood"]').first().click({ timeout: 5000 }).catch(() => {});
      out.push(await rest(p, 2400));
      return out;
    };

    /* a deep link opened cold has nothing in the session to go back to */
    const p0 = await mkPage();
    await p0.goto(APP + '#/n/' + NODE_FOCUS, { waitUntil: 'load' });
    B.fresh = await rest(p0, 1600);
    await p0.close();

    /* the trail, two clicks of the button, then the forward stack */
    const p1 = await mkPage();
    B.trail = await walk(p1);
    await hit(p1); B.clicks.push(await rest(p1, 1400));
    await hit(p1); B.clicks.push(await rest(p1, 1600));
    await p1.goForward(); await rest(p1, 1400);
    await p1.goForward(); B.forward = await rest(p1, 2400);
    await p1.close();

    /* the same trail again, walked by the browser's own back and forward */
    const p2 = await mkPage();
    await walk(p2);
    await p2.goBack(); B.parity.b1 = await rest(p2, 1400);
    await p2.goBack(); B.parity.b2 = await rest(p2, 1600);
    await p2.goForward(); B.parity.f1 = await rest(p2, 1400);
    await hit(p2); B.parity.click = await rest(p2, 1400);
    await p2.close();
  }

  await browser.close();

  /* ====================================================================== */
  /* the assertions                                                          */
  /* ====================================================================== */

  console.log('\n  ' + (POISON ? 'POISON=' + POISON + ': ' + POISONS[POISON].what : 'clean run')
    + '  ·  ' + APP + '\n');

  const C1_PAGES = ['home', 'topic', 'hood0', 'thread:custody', 'timeline', 'patents', 'evidence', 'report'];
  const nodeIdsOn = (id) => (S[id] ? S[id].hrefs : [])
    .filter((h) => h && h.startsWith('#/n/'))
    .map((h) => h.slice(4).replace(/\/(map|hood)$/, ''));

  /* ---- C1 --------------------------------------------------------------- */
  {
    let total = 0; const bad = [];
    for (const p of C1_PAGES) {
      const list = p === 'evidence' ? nodeIdsOn(p).slice(0, 60) : nodeIdsOn(p);
      total += list.length;
      for (const id of list) if (!ids.has(id)) bad.push(p + ':' + id);
    }
    check('c1', bad.length === 0 && total > 0,
      'C1  every #/n/<id> on the eight screens is an id in index.json',
      `${total} hrefs over ${C1_PAGES.length} screens, ${bad.length} unknown` + (bad.length ? ': ' + clip(bad) : ''));
    const empty = C1_PAGES.filter((p) => nodeIdsOn(p).length === 0);
    check('c1', empty.length === 0, 'C1  every one of the eight screens actually renders node links',
      empty.length ? 'no #/n/ href on: ' + empty.join(', ') : 'all eight carry at least one');
  }

  /* ---- C2 --------------------------------------------------------------- */
  {
    const all = S.hood.labels.map((l) => ({ ...l, where: 'hood' }));
    const sizes = [...new Set(all.map((l) => l.fs))];
    check('c2', sizes.length === 1 && all.length > 0, 'C2  one label size across the neighbourhood',
      `${all.length} labels at ${sizes.join(', ')}`);
    const ell = all.filter((l) => l.to === 'ellipsis' || /[…]|\.\.\.$/.test(l.text));
    check('c2', ell.length === 0, 'C2  no text-overflow and no ellipsis character in any label',
      ell.length ? clip(ell.map((l) => l.where + ':' + l.text)) : `${all.length} labels clean`);
    /* one line: its box is its text. Wrapped (the neighbourhood's long names):
       its line boxes add up to its text, less up to one space per break */
    const narrow = all.filter((l) => ((l.lines || 1) > 1
      ? l.sumW + 0.5 + 8 * (l.lines - 1) < l.nat : l.w + 0.5 < l.nat));
    check('c2', narrow.length === 0, 'C2  no label box narrower than its own text at its own font',
      narrow.length ? clip(narrow.map((l) => `${l.text} ${l.w.toFixed(0)}<${l.nat.toFixed(0)}`))
        : `${all.length} labels measured against their natural width`);
  }

  /* ---- C4 --------------------------------------------------------------- */
  {
    const cases = [
      ['neighbourhood names', S.hood.gn.rows.map((r) => ({ id: r.id, x: r.x, y: r.y, w: r.w, h: r.h }))],
      ['timeline chips and counts', [...S.timeline.timeline.items, ...S.timeline.timeline.mores]],
    ];
    for (const [name, boxes] of cases) {
      const bad = pairsOverlapping(boxes);
      check('c4', bad.length === 0, 'C4  no two label boxes intersect · ' + name,
        bad.length ? `${bad.length}+ overlapping pairs: ` + clip(bad, 3) : `${boxes.length} boxes, none intersecting`);
    }
  }

  /* ---- C7 --------------------------------------------------------------- */
  {
    const bad = []; let pairs = 0; let walked = 0;
    for (const t of threads) {
      if (!S['thread:' + t.id]) continue;
      walked++;
      const steps = (S['thread:' + t.id].thread || {}).steps || [];
      for (let i = 1; i < steps.length; i++) {
        pairs++;
        if (!joined(steps[i - 1], steps[i])) bad.push(`${t.id}: ${steps[i - 1]} → ${steps[i]}`);
      }
    }
    check('c7', bad.length === 0 && pairs > 0,
      'C7  every rendered thread step joins the last by an edge or a shared member',
      bad.length ? clip(bad, 3) : `${pairs} consecutive pairs over ${walked} of ${threads.length} threads, all joined`);
  }

  /* ---- C8 --------------------------------------------------------------- */
  {
    const n = S.node.node;
    const noSrc = n.claims.filter((c) => {
      if (c.srcTag === 'A' && c.srcHref) return false;
      const cite = (c.srcTitle || '').trim() || (c.srcText || '').trim();
      return !cite || /^no source recorded$/i.test(cite);
    });
    check('c8', noSrc.length === 0 && n.claims.length > 0,
      'C8  every claim row on #/n/' + NODE_FOCUS + ' carries a source link or citation text',
      noSrc.length ? `${noSrc.length} of ${n.claims.length} with neither: ` + clip(noSrc.map((c) => c.text.slice(0, 40)), 2)
        : `${n.claims.length} claims, ${n.claims.filter((c) => c.srcTag === 'A').length} as links`);
    const m = n.head.match(/Claims\s*·?\s*(\d+) in all[\s\S]*?(\d+) at Tier 1[\s\S]*?(\d+) at Tier 2[\s\S]*?(\d+) at Tier 3/);
    const tot = m ? Number(m[1]) : NaN, sum = m ? Number(m[2]) + Number(m[3]) + Number(m[4]) : NaN;
    check('c8', !!m && tot === sum && tot === n.claims.length,
      'C8  the claims header T1+T2+T3 equals the claim count and the rows drawn',
      m ? `${m[2]}+${m[3]}+${m[4]}=${sum}, header says ${tot}, ${n.claims.length} rows`
        : 'the claims header could not be parsed: ' + n.head.slice(0, 60));
  }

  /* ---- C9 --------------------------------------------------------------- */
  {
    if (!sweepRoutes) skip('C9  every route in the spec section 3 scheme resolves',
      'not walked under POISON=' + POISON + '; the c9 run walks all ' + ROUTES.length);
    else check('c9', deadRoutes.length === 0, 'C9  every route in the spec section 3 scheme resolves',
      deadRoutes.length ? deadRoutes.join(', ') : `${ROUTES.length} routes, none reached the not-found page`);

    /* the URL scheme of Design 2.1, re-implemented here so the check does not
       borrow the router's own opinion of what a route is */
    const ID = /^[a-z0-9][a-z0-9._-]*$/;
    const shape = (h) => {
      const raw = h.replace(/^#/, '');
      const qi = raw.indexOf('?');
      const p = (qi < 0 ? raw : raw.slice(0, qi)).replace(/\/+$/, '').split('/').filter(Boolean);
      if (!p.length) return true;
      if (p[0] === 'n') return ID.test(p[1] || '') && (p.length === 2 || (p.length === 3 && /^(map|hood)$/.test(p[2])));
      if (p[0] === 'hood') return p.length === 1 || (p.length === 2 && ID.test(p[1]));
      if (p[0] === 'map') return p.length === 1;
      if (p[0] === 't') return ID.test(p[1] || '') && (p.length === 2 || (p.length === 3 && p[2] === 'map'));
      if (p[0] === 'timeline') return p.length === 1;
      if (p[0] === 'patents') return p.length === 2 && /^[0-9][0-9,]*$/.test(p[1]);
      if (p[0] === 'evidence') return p.length === 1;
      if (p[0] === 'report') return p.length === 3 && /^[nt]$/.test(p[1]) && ID.test(p[2]);
      /* phase 6 */
      if (p[0] === 'atlas') return p.length === 1;
      if (p[0] === 'topic') return p.length === 2 && ID.test(p[1]);
      /* phase 9 */
      if (['people', 'orgs', 'programmes', 'laws', 'places', 'events'].includes(p[0])) return p.length === 1;
      /* phase 8 */
      if (p[0] === 'library') return p.length === 1;
      if (p[0] === 's') return p.length === 2 && ID.test(p[1]);
      return false;
    };
    const seen = new Set(), offScheme = [], deadIds = [];
    for (const k of Object.keys(S)) {
      for (const h of S[k].hrefs || []) {
        if (!h || !h.startsWith('#')) continue;
        if (seen.has(h)) continue;
        seen.add(h);
        if (!shape(h)) { offScheme.push(k + ':' + h); continue; }
        const p = h.replace(/^#\//, '').split(/[/?]/);
        if (p[0] === 't' && !threadIds.has(p[1])) deadIds.push(k + ':' + h);
        if (p[0] === 'patents' && !patentNums.has(p[1].replace(/[^0-9]/g, ''))) deadIds.push(k + ':' + h);
        if (p[0] === 'topic' && !topicIds.has(p[1])) deadIds.push(k + ':' + h);
        if (p[0] === 's' && !sourceIds.has(p[1])) deadIds.push(k + ':' + h);
      }
    }
    check('c9', offScheme.length === 0, 'C9  every rendered in-app href is a route in the 2.1 scheme',
      offScheme.length ? clip(offScheme, 4) : `${seen.size} distinct hrefs over ${Object.keys(S).length} screens`);
    check('c9', deadIds.length === 0, 'C9  every rendered #/t/, #/patents/ and #/topic/ link names something the board carries',
      deadIds.length ? `${deadIds.length} dead: ` + clip(deadIds, 5) : 'all resolve to a thread, a patent or a topic');
  }

  /* ---- C70 -------------------------------------------------------------- */
  /* The grouped neighbourhood (phase 11) against C70's rule restated above:
     every neighbour named once, in its family's column under that family's own
     label, with a reading and a sentence; one orthogonal line per column; two
     steps out one family at a time, every node reached listed once under a
     named neighbour it is really linked to. C10 retired with the ring. */
  {
    const g = S.hood.gn;
    const want = [...GN.famOf.keys()];
    const count = new Map();
    for (const r of g.rows) count.set(r.id, (count.get(r.id) || 0) + 1);
    const twice = [...count].filter(([, n]) => n > 1).map(([id, n]) => id + ' x' + n);
    const missing = want.filter((id) => !count.has(id));
    const extra = [...count.keys()].filter((id) => !GN.famOf.has(id));
    check('c70', g.centre === NODE_FOCUS && twice.length === 0 && missing.length === 0 && extra.length === 0 && want.length > 0,
      `C70 #/hood/${NODE_FOCUS} names every neighbour exactly once`,
      twice.length || missing.length || extra.length
        ? `named twice ${clip(twice, 3)} · missing ${clip(missing, 3)} · not a neighbour ${clip(extra, 3)}`
        : `${g.rows.length} rows, ${want.length} neighbours in the record`);
    const wrongFam = g.rows.filter((r) => GN.famOf.has(r.id) && (r.family !== GN.famOf.get(r.id) || r.head !== FAM_LABEL[r.family]))
      .map((r) => r.id + ' under ' + (r.head || r.family) + ', sits in ' + GN.famOf.get(r.id));
    check('c70', wrongFam.length === 0,
      'C70 each neighbour is in the column of its family, and the column is headed with that family\'s label',
      wrongFam.length ? clip(wrongFam, 3) : `${g.fams.length} columns: ${g.fams.join(', ')}`);
    const unsaid = g.rows.filter((r) => r.name !== labelOf.get(r.id) || !r.say || !r.title)
      .map((r) => r.id + (r.name !== labelOf.get(r.id) ? ' named "' + r.name + '"' : '') + (!r.say ? ' no reading' : '') + (!r.title ? ' no sentence' : ''));
    check('c70', unsaid.length === 0, 'C70 every row carries the node\'s whole name, the link\'s reading and its sentence',
      unsaid.length ? clip(unsaid, 3) : `${g.rows.length} rows read`);
    const ortho = /^M[\d.-]+ [\d.-]+( [HV][\d.-]+)+$/;
    const badLine = g.lines.filter((l) => !ortho.test(l.d)).map((l) => l.family);
    const lineFams = g.lines.map((l) => l.family).sort().join('|');
    check('c70', badLine.length === 0 && lineFams === g.fams.slice().sort().join('|') && g.lines.length > 0,
      'C70 one orthogonal line from the centre to each family column',
      `${g.lines.length} lines for ${g.fams.length} columns` + (badLine.length ? ', not orthogonal: ' + clip(badLine, 3) : ''));
    /* two steps out, through the drive's two families in turn */
    for (const [key, fam] of [['hood2', GN.twoFams[0]], ['hood2b', GN.twoFams[1]]]) {
      if (!fam) { check('c70', false, 'C70 two steps out', 'the record offers no family that reaches further'); continue; }
      const s = S[key].gn;
      const open = s.open.map((o) => o.family);
      check('c70', open.length === 1 && open[0] === fam, `C70 two steps out opens one family at a time (${fam})`,
        'open: ' + (open.join(', ') || 'none'));
      const o = s.open.find((x) => x.family === fam);
      if (!o) continue;
      const wantTwo = GN.two(fam);
      const got = o.groups.flatMap((v) => v.ids);
      const n2 = new Map();
      for (const id of got) n2.set(id, (n2.get(id) || 0) + 1);
      const dup = [...n2].filter(([, n]) => n > 1).map(([id]) => id);
      const miss = [...wantTwo].filter((id) => !n2.has(id));
      const stray = got.filter((id) => !wantTwo.has(id));
      check('c70', dup.length === 0 && miss.length === 0 && stray.length === 0 && got.length > 0,
        `C70 two steps out through ${fam} lists every node it reaches, once`,
        dup.length || miss.length || stray.length
          ? `twice ${clip(dup, 3)} · missing ${clip(miss, 3)} · not two steps out ${clip(stray, 3)}`
          : `${got.length} nodes under ${o.groups.length} vias`);
      const colIds = new Set(GN.byFam.get(fam) || []);
      const badVia = o.groups.filter((v) => !v.via || !colIds.has(v.via) || v.viaText !== labelOf.get(v.via) ||
          !/^via /.test(v.head) || v.ids.some((m) => !(adj.get(v.via) || new Set()).has(m)))
        .map((v) => (v.via || '(no via named)') + (v.viaText ? '' : ' unnamed'));
      check('c70', badVia.length === 0,
        `C70 every two-step group says "via" and names a ${fam} neighbour each of its nodes is linked to`,
        badVia.length ? clip(badVia, 3) : `${o.groups.length} vias named`);
    }
  }

  /* ---- C71 -------------------------------------------------------------- */
  /* #/places against places.json and index.json: every location node listed
     once, linked, under its own country; every place with coordinates plotted
     once with its label beside the grid; nothing plotted that has none; the
     markers in the order longitude and latitude put them; no two labels on
     top of each other. */
  if (!S.places || !S.places.pl) skip('C71 #/places', 'poison ' + POISON + ' does not reach it');
  else {
    const pl = S.places.pl;
    const want = new Map(placesFile.places.map((p) => [p.id, p]));
    const locIds = index.nodes.filter((n) => n.cls === 'location').map((n) => n.id).sort();
    const nRow = new Map();
    for (const r of pl.rows) nRow.set(r.id, (nRow.get(r.id) || 0) + 1);
    const twice = [...nRow].filter(([, n]) => n > 1).map(([id]) => id);
    const miss = locIds.filter((id) => !nRow.has(id));
    const extra = [...nRow.keys()].filter((id) => !locIds.includes(id));
    const wrongRow = pl.rows.filter((r) => {
      const p = want.get(r.id);
      return !p || r.href !== '#/n/' + r.id || r.name !== labelOf.get(r.id) || r.group !== (p.country || 'Not located on the board');
    }).map((r) => r.id + ' under ' + r.group);
    check('c71', pl.present && twice.length === 0 && miss.length === 0 && extra.length === 0 && wrongRow.length === 0 && locIds.length > 0,
      'C71 #/places lists every place once, linked, under its own country',
      twice.length || miss.length || extra.length || wrongRow.length
        ? `twice ${clip(twice, 3)} · missing ${clip(miss, 3)} · not a place ${clip(extra, 3)} · wrong ${clip(wrongRow, 3)}`
        : `${pl.rows.length} rows for ${locIds.length} places`);
    const coord = placesFile.places.filter((p) => p.lat != null && p.lon != null);
    const count = (list) => { const m = new Map(); for (const x of list) m.set(x.id, (m.get(x.id) || 0) + 1); return m; };
    const nm = count(pl.marks), nl = count(pl.labels);
    const plotBad = coord.filter((p) => nm.get(p.id) !== 1 || nl.get(p.id) !== 1).map((p) => p.id + ' marks ' + (nm.get(p.id) || 0) + ' labels ' + (nl.get(p.id) || 0));
    const stray = [...new Set([...nm.keys(), ...nl.keys()])].filter((id) => !want.has(id) || want.get(id).lat == null);
    check('c71', plotBad.length === 0 && stray.length === 0 && coord.length > 0,
      'C71 every place with coordinates is plotted once and named once beside the grid, and nothing else is',
      plotBad.length || stray.length ? `${clip(plotBad, 3)} · plotted without coordinates ${clip(stray, 3)}`
        : `${coord.length} plotted of ${placesFile.places.length}`);
    const order = [];
    for (const a of pl.marks) for (const b of pl.marks) {
      if (a.plot !== b.plot || a.id >= b.id) continue;
      const pa = want.get(a.id), pb = want.get(b.id);
      if (!pa || !pb) continue;
      if ((pa.lon < pb.lon - 0.05 && !(a.cx < b.cx)) || (pa.lon > pb.lon + 0.05 && !(a.cx > b.cx)) ||
          (pa.lat > pb.lat + 0.05 && !(a.cy < b.cy)) || (pa.lat < pb.lat - 0.05 && !(a.cy > b.cy))) order.push(a.id + '/' + b.id);
    }
    check('c71', order.length === 0 && pl.marks.length > 1, 'C71 every marker sits where its longitude and latitude put it relative to the others',
      order.length ? order.length + ' pairs out of order: ' + clip(order, 3) : pl.marks.length + ' markers in order');
    const labBad = pl.labels.filter((l) => l.text !== labelOf.get(l.id)).map((l) => l.id);
    const over = pairsOverlapping(pl.labels.map((l) => ({ id: l.id, x: l.x, y: l.y, w: l.w, h: l.h })));
    check('c71', labBad.length === 0 && over.length === 0, 'C71 each label beside the grid is its place\'s whole name, and no two overlap',
      labBad.length || over.length ? `wrong ${clip(labBad, 3)} · overlapping ${clip(over, 3)}` : pl.labels.length + ' labels');
  }

  /* ---- C72 -------------------------------------------------------------- */
  /* The program map retired in phase 11. Its three routes still land: #/map on
     the Atlas, #/n/<id>/map on that node, #/t/<id>/map on that thread, each
     drawn, with the address rewritten to where the reader now is. */
  {
    const rd = [
      ['#/map', S.maprd && S.maprd.rd, '#/atlas', (r) => r.atlas > 0, 'the Atlas drawn'],
      ['#/n/' + NODE_FOCUS + '/map', S.maprdn && S.maprdn.rd, '#/n/' + NODE_FOCUS, (r) => r.h1.trim() === focusRec.label, 'the node headed'],
      ['#/t/custody/map', S.maprdt && S.maprdt.rd, '#/t/custody', (r) => r.steps > 0, 'the thread drawn'],
    ];
    for (const [from, r, to, drawn, what] of rd) {
      check('c72', !!r && r.hash === to && drawn(r),
        `C72 the retired ${from} lands on ${to}, ${what}`, r ? 'landed on ' + r.hash : 'not reached');
    }
  }

  /* ---- C11 -------------------------------------------------------------- */
  {
    const home = S.home.starthere || [];
    const wantIds = flags.map((f) => f.id).join('|');
    check('c11', home.map((c) => c.id).join('|') === wantIds,
      'C11 Home\'s start-here tour goes through highlights.json\'s nodes, in rank order',
      `${home.length} steps: ` + (home.map((c) => c.id).join('|') === wantIds ? 'order matches'
        : 'drawn ' + clip(home.map((c) => c.id), 4)));
    const numBad = home.filter((c, i) => flags[i] && Number(c.n) !== flags[i].rank)
      .map((c) => c.id + ' numbered ' + c.n);
    check('c11', numBad.length === 0 && home.length === flags.length, 'C11 every Home start-here number is the owner\'s rank',
      numBad.length ? clip(numBad, 4) : `${home.length} numbers match highlights.json`);
    /* phase 6: each step opens the flagged node's primary topic, re-derived
       from the topic files (the first of topicsOf) */
    const topicBad = home.map((c) => {
      const p = topicsOf(c.id)[0];
      const want = p ? '#/topic/' + p.topic : '';
      return c.topic === want ? null : c.id + ' opens ' + (c.topic || 'nothing') + ', primary topic ' + (want || 'none');
    }).filter(Boolean);
    check('c11', topicBad.length === 0 && home.length > 0, "C11 each start-here step opens its node's primary topic",
      topicBad.length ? clip(topicBad, 3) : `${home.length} steps, each on its node's first topic`);
  }

  /* ---- C12 -------------------------------------------------------------- */
  /* Size never encodes importance. The map's chip half and the thread small
     map's went with them in phase 11; the neighbourhood's marks remain. */
  {
    const marks = [...new Set(S.hood.gn.rows.map((e) => e.mw + '×' + e.mh))];
    check('c12', marks.length === 1, 'C12 every neighbourhood mark is the same size',
      `${S.hood.gn.rows.length} marks at ${marks.join(', ')}`);
  }

  /* ---- C13 -------------------------------------------------------------- */
  {
    const want = (focusRec.denials || []).map((d) => (d.by.id === NODE_FOCUS ? d.of.id : d.by.id)).sort();
    const got = S.node.node.denials.map((d) => d.other).sort();
    check('c13', want.length === got.length && want.every((x, i) => x === got[i]),
      'C13 the denial rows on #/n/' + NODE_FOCUS + ' are exactly its denialPairs',
      `page ${got.length} [${got.join(', ')}] · record ${want.length} [${want.join(', ')}]`);
  }

  /* ---- C27 -------------------------------------------------------------- */
  /* Home's figures, re-derived from the raw files the app serves and never from
     index.json's own counts block. Replaces the twelve figure checks that
     tools/audit_independent.py scraped off the old shell. */
  {
    const fmt = (x) => Number(x).toLocaleString('en-US');
    const people = index.nodes.filter((x) => x.cls === 'person').length;
    const tier = [1, 2, 3].map((t) => claimRows.filter((c) => c.tier === t).length);
    const pats = patentsFile.patents || [];
    const sheets = pats.reduce((a, x) => a + (Array.isArray(x.sheets) ? x.sheets.length : 0), 0) +
      ((patentsFile.drawings || {}).unmatchedSheets || []).length;
    const qPairs = new Set();
    for (const r of foiaFile.requests || []) for (const x of r.nodes || []) {
      for (const q of [...(x.questions || []), ...(x.partial || [])]) qPairs.add(x.node + '#' + q);
    }
    const qNodes = Object.values(foiaFile.byNode || {}).filter((v) => (v || []).length).length;
    const want = [
      [index.nodes.length, people, index.nodes.length - people],
      /* phase 6: the topics and their sections, counted from the topic files */
      [Object.keys(topicRecs).length, new Set(Object.values(topicRecs).map((t) => t.section)).size],
      [edges.length],
      [claimRows.length, ...tier],
      [tlEvents.length],
      [threads.length],
      [pats.length, sheets],
      [(foiaFile.requests || []).length, qPairs.size, qNodes],
    ];
    const nums = (t) => (t.replace(/\bT[123]\b/g, '').match(/\d[\d,]*/g) || []).map((x) => Number(x.replace(/,/g, '')));
    const got = S.home.home.rows.map(([a, b]) => nums(a + ' ' + b));
    const bad = want.map((w, i) => [w, got[i] || []]).filter(([w, g]) => w.join(',') !== g.join(','))
      .map(([w, g]) => 'wanted ' + w.join('/') + ' drew ' + g.join('/'));
    check('c27', got.length === want.length && bad.length === 0,
      "C27 every figure in Home's counts panel re-derives from the served data files",
      bad.length ? clip(bad, 3) : want.map((w) => w.join('/')).join(' · '));
    const para = S.home.home.para;
    const phrases = [fmt(index.nodes.length) + ' people', fmt(edges.length) + ' hand-written',
      fmt(claimRows.length) + ' claims', 'documented (' + fmt(tier[0]) + ')',
      'on the record (' + fmt(tier[1]) + ')', 'inference (' + fmt(tier[2]) + ')'];
    const miss = phrases.filter((x) => !para.includes(x));
    check('c27', miss.length === 0, "C27 every figure in Home's prose re-derives from the served data files",
      miss.length ? 'missing ' + clip(miss, 3) : phrases.join(' · '));
  }

  /* ---- C28 -------------------------------------------------------------- */
  /* This board was built by porting a sibling board's shell, and its copy leaked
     through more than once (CLAUDE.md section 8). The nine strings are verify.py's
     old #438 list, carried over when the old shell retired. */
  {
    const BANNED = ['NeuroLogica', 'matched denominator', 'left everything behind', 'departure kit',
      'the leftBehind array', 'Fifty-two entities', 'who disappeared within three months',
      'derived from the case records', 'after April 2026 is a fact about reporting attention'];
    const hits = [];
    for (const [id, snap] of Object.entries(S)) {
      for (const b of BANNED) if (snap && snap.text && snap.text.includes(b)) hits.push(id + ': "' + b + '"');
    }
    check('c28', hits.length === 0, "C28 no screen carries the sibling board's wording",
      hits.length ? clip(hits, 3) : Object.keys(S).length + ' screens clean of ' + BANNED.length + ' strings');
    check('c28', /The Legacy Program/.test(S.home.title || ''), 'C28 the page title names this board',
      '"' + (S.home.title || '') + '"');
  }

  /* ---- C29 -------------------------------------------------------------- */
  if (!BRIEF) {
    skip('C29 the analyst is briefed about this board', 'poison ' + POISON + ' does not drive it');
  } else {
    const NEED = ['custody proximity', 'access', 'disclosure role'];
    const BAN = ['axes S, P and I', 'deaths and disappearances', 'real missing people', 'who disappeared'];
    /* the standing instructions only: the case index after them is the board's own
       data, and a node about missing scientists may say "disappearances" */
    const t = BRIEF.text.split('CASE INDEX.')[0];
    const lacks = NEED.filter((x) => !t.includes(x));
    const has = BAN.filter((x) => t.includes(x));
    check('c29', BRIEF.sent && t.length > 0 && lacks.length === 0 && has.length === 0,
      "C29 the analyst's brief names this board's axes and none of the sibling board's",
      !BRIEF.sent ? 'no request reached the analyst route'
        : (lacks.length ? 'lacks ' + lacks.join(', ') + ' ' : '') + (has.length ? 'carries ' + has.join(', ') : '') ||
          t.length + ' characters, axes named');
  }

  /* ---- C22 -------------------------------------------------------------- */
  /* Phase 7. Every sourced connection is drawn once, under its relationship
     FAMILY, with its own sentence; the families are headed by their reader names
     in the vocabulary's order (both RESTATED here, not imported); each row reads
     from this node, and the arrow is read against edges.json's own `subject`,
     not against the node file the page was drawn from: drawn only where the
     predicate is shown, "→" where this node is the subject, "←" where it is the
     object. The report must say the same. Nothing says "member". */
  {
    const FAMILY = [
      ['role', 'Roles'], ['organisation', 'Organisation'], ['money', 'Money'], ['custody', 'Custody'],
      ['law', 'Law'], ['oversight', 'Oversight'], ['testimony', 'Testimony'], ['denial', 'Denials'],
      ['documents', 'Documents'], ['media', 'Media'], ['place-time', 'Place and time'],
      ['conduct', 'Conduct'], ['analysis', "The board's reading"], ['other', 'Other links'],
    ];
    const READER = Object.fromEntries(FAMILY);
    const ORDER = FAMILY.map(([f]) => f);
    const NO_SENTENCE = 'no sentence recorded for this link';
    const sentence = (c) => c.edgeLabel || c.note || NO_SENTENCE;
    const recC = focusRec.connections || [];
    const want = recC.map((c) => c.family + '|' + c.id + '|' + sentence(c)).sort();
    const got = [];
    for (const g of S.node.conns.groups) for (const r of g.rows) for (const l of r.lines) got.push(g.family + '|' + r.id + '|' + l);
    got.sort();
    const missing = want.filter((x) => !got.includes(x));
    const extra = got.filter((x) => !want.includes(x));
    check('c22', want.length === got.length && missing.length === 0 && extra.length === 0,
      'C22 every sourced connection on #/n/' + NODE_FOCUS + ' is drawn once, under its family, with its own sentence',
      `record ${want.length} · page ${got.length}` +
      (missing.length ? ' · missing ' + clip(missing, 2) : '') + (extra.length ? ' · extra ' + clip(extra, 2) : ''));
    const groups = S.node.conns.groups;
    const badHead = groups.filter((g) => g.head !== READER[g.family]);
    const order = groups.map((g) => ORDER.indexOf(g.family));
    const inOrder = order.every((x, k) => x >= 0 && (k === 0 || x > order[k - 1]));
    check('c22', groups.length > 0 && badHead.length === 0 && inOrder,
      'C22 every group is a family headed by its reader name, in the vocabulary order',
      badHead.length ? clip(badHead.map((g) => g.family + '="' + g.head + '"'), 4)
        : groups.map((g) => g.head).join(' · '));

    /* direction, re-derived from edges.json and the served vocabulary */
    const byEdge = new Map(edges.map((e) => [e.id, e]));
    const pv = new Map((vocabFile.predicates || []).map((x) => [x.id, x]));
    const phrase = new Map((vocabFile.predicateFamilies || []).map((f) => [f.id, f.phrase]));
    const expect = new Map();      /* id|verb -> arrow ('', '→', '←') */
    const bad = [];
    let arrows = 0;
    for (const c of recC) {
      const e = byEdge.get(c.edgeId);
      const p = e && pv.get(e.predicate);
      if (!e || !p) { bad.push('no predicate on ' + c.edgeId); continue; }
      const isSubject = e[e.subject] === NODE_FOCUS && e.a !== e.b;
      let verb, dir;
      if (!e.shown) { verb = phrase.get(p.family); dir = ''; }
      else if (p.symmetric) { verb = p.forward; dir = ''; }
      else { verb = isSubject ? p.forward : p.inverse; dir = isSubject ? '→' : '←'; }
      if (p.family !== c.family) bad.push(c.edgeId + ' family ' + c.family + ' vs ' + p.family);
      expect.set(c.id + '|' + verb, dir);
    }
    for (const g of groups) for (const r of g.rows) {
      if (r.dir) arrows++;
      const k = r.id + '|' + r.verb;
      if (!expect.has(k)) bad.push(r.id + ' reads "' + r.verb + '", which no edge to it says from here');
      else if (expect.get(k) !== r.dir) bad.push(r.id + ' "' + r.verb + '" drawn "' + r.dir + '", wanted "' + expect.get(k) + '"');
    }
    check('c22', bad.length === 0 && arrows > 0,
      'C22 each row reads from this node, and its arrow agrees with the edge\'s recorded subject',
      bad.length ? clip(bad, 3) : arrows + ' arrows drawn, every one where edges.json puts this node');
    const bucket = groups.flatMap((g) => g.rows.flatMap((r) => r.metas)).filter((m) => /^member\b/i.test(m));
    check('c22', bucket.length === 0, 'C22 no connection is labelled with the bucket word "member"',
      bucket.length ? bucket.length + ' rows' : 'none');

    const rWant = recC.map((c) => READER[c.family] + '|' + c.id + '|' + sentence(c)).sort();
    const rGot = S.report.rconns.map((r) => r.head + '|' + r.id + '|' + r.sent).sort();
    check('c22', rWant.length === rGot.length && rWant.every((x, i) => x === rGot[i]),
      'C22 the node report lists every connection under its family, with its sentence',
      `record ${rWant.length} · report ${rGot.length}`);
    const rBad = S.report.rconns.filter((r) => !expect.has(r.id + '|' + r.verb) || expect.get(r.id + '|' + r.verb) !== r.dir)
      .map((r) => r.id + ' "' + r.verb + '" "' + r.dir + '"');
    check('c22', rBad.length === 0, 'C22 the report reads each link from this node with the same arrow',
      rBad.length ? clip(rBad, 3) : S.report.rconns.length + ' links');
    const rBucket = S.report.rconns.filter((r) => /·\s*member\b/i.test(r.text));
    check('c22', rBucket.length === 0, 'C22 the node report never says "member"',
      rBucket.length ? rBucket.length + ' rows' : 'none');
  }

  /* ---- C23 -------------------------------------------------------------- */
  /* Nothing authored is hidden: every field a researcher wrote on the record has a
     place on the page. The chronology rule is restated here, not imported. */
  {
    const list = (v) => (Array.isArray(v) ? v.filter(Boolean) : (v ? [v] : []));
    for (const [stopId, rec] of [['node', focusRec], ['person', personRec],
      ['entity', entityRec], ['entityq', entityQRec]]) {
      const f = S[stopId].fields;
      const chron = new Set([...(rec.chronology || []), ...(rec.sequenceChain || [])]
        .map((e) => String(e.date) + '|' + String(e.event || '').trim().toLowerCase()));
      /* open questions: the dossier's, then the node's own (phase 3) */
      const want = {
        oq: ((rec.dossier && rec.dossier.openQuestions) || []).length + list(rec.openQuestions).length,
        unv: list(rec.unverified).length, cnf: list(rec.conflicts).length, chron: chron.size,
        aff: (rec.affiliations || []).length, nsrc: (rec.sources || []).length,
      };
      const bad = Object.keys(want).filter((k) => want[k] !== f[k]);
      check('c23', bad.length === 0, `C23 #/n/${rec.id} renders every authored field it carries`,
        Object.keys(want).map((k) => `${k} ${f[k]}/${want[k]}`).join(' · '));
      check('c23', !/\bTier [ABC]\b|\bcluster\b/.test(f.crumb),
        `C23 #/n/${rec.id} prints neither the node tier letter nor the cluster`, f.crumb.trim().slice(0, 80));
      const stacked = f.axes.filter((cells) => cells.length !== 3 ||
        cells.some((b, i) => i > 0 && b[0] < cells[i - 1][1] - 0.5));
      check('c23', f.axes.length === 3 && stacked.length === 0,
        `C23 #/n/${rec.id} draws each of the three axes as three cells side by side`,
        f.axes.length + ' axes' + (stacked.length ? ', ' + stacked.length + ' with cells stacked or missing' : ''));
    }
  }

  /* ---- C23, the first screen (phase 5b) ---------------------------------- */
  /* A reader arriving on a node sees what it is, the case against it and the
     start of its claims without scrolling; the board's long analysis is named
     as the board's and folded, with nothing taken out of the page; and at 1920
     the prose uses its column rather than leaving a hole beside it. */
  {
    const d = personRec.dossier || {};
    const prose = String(d.whyImplicated || d.narrative || personRec.desc || personRec.narrative || '').length;
    for (const [w, f] of [[1920, S.person && S.person.first], [1366, S.person1366 && S.person1366.first]]) {
      if (!f) { skip('C23 first screen at ' + w, 'not reached'); continue; }
      const bad = [];
      if (!(f.leadTop < f.vh)) bad.push('About lead at ' + Math.round(f.leadTop));
      if (!(f.againstTop < f.vh)) bad.push('case against at ' + Math.round(f.againstTop));
      if (!(f.claimTop < f.vh - 20)) bad.push('first claim at ' + Math.round(f.claimTop));
      check('c23', bad.length === 0,
        `C23 #/n/${PERSON_FOCUS} at ${w}: the About lead, the case against and the first claim are on the first screen`,
        bad.length ? bad.join(' · ') + ` (screen ${f.vh}px)` :
          `lead ${Math.round(f.leadTop)} · case against ${Math.round(f.againstTop)} · first claim ${Math.round(f.claimTop)} of ${f.vh}px`);
      check('c23', f.head === "The board's analysis" && f.folded && f.foldedLines <= 7 &&
        /^Read the whole analysis$/.test(f.more) && f.chars === prose,
        `C23 #/n/${PERSON_FOCUS} at ${w}: the analysis is labelled as the board's, folded to its first lines, every word kept`,
        `"${f.head}" · ${f.folded ? 'folded to ' + f.foldedLines + ' lines' : 'not folded'} · control "${f.more}" · ${f.chars} of ${prose} characters in the page`);
    }
    const f = S.person && S.person.first;
    if (f) check('c23', f.proseW >= 0.75 * f.mainW,
      `C23 #/n/${PERSON_FOCUS} at 1920: the prose uses its column, no dead gap beside it`,
      `prose ${Math.round(f.proseW)}px of a ${Math.round(f.mainW)}px column`);
  }

  /* ---- C30 -------------------------------------------------------------- */
  /* A denial is given a direction only where data/denial-adjudication.json names
     the denier. Every row the record does not adjudicate says so, in so many
     words, and never prints the old guess ("issued here", "directed here") that
     came from the order the edge's ends were written in. Read row by row against
     the record, in page order; the page's own data-adjudicated flag is not used. */
  {
    const recD = denialRec.denials || [];
    const rows = S.denial.rows || [];
    const un = recD.filter((d) => !d.denialKind).length;
    const wrong = [];
    recD.forEach((d, i) => {
      const k = (rows[i] || {}).kind || '';
      const says = /direction not adjudicated/.test(k);
      const guesses = /issued here|directed here/.test(k);
      if (!d.denialKind && (!says || guesses)) wrong.push(i + ':' + k);
      if (d.denialKind && says) wrong.push(i + ':' + k);
      if (!d.by && guesses) wrong.push(i + ':' + k);
    });
    check('c30', un > 0 && rows.length === recD.length && wrong.length === 0,
      `C30 every denial on #/n/${DENIAL_FOCUS} that the record does not adjudicate says so`,
      `record ${recD.length} (${un} unadjudicated) · page ${rows.length}` +
      (un ? '' : ' · the subject no longer carries an unadjudicated denial: choose another, or retire C30 once phase R has cleared them') +
      (wrong.length ? ' · wrong ' + clip(wrong, 2) : ''));
  }

  /* ---- C25 -------------------------------------------------------------- */
  /* The denial flag on the Evidence table is the NODE's (the node is the object
     of some denial), so no claim may be painted with the claim-level word. */
  {
    const claimWord = S.evidence.den.filter((t) => /^denied$/i.test(t)).length;
    const flagged = S.evidence.den.filter(Boolean).length;
    check('c25', claimWord === 0 && flagged > 0,
      'C25 no claim is labelled "denied": the flag belongs to the node, and says so',
      claimWord ? claimWord + ' cells say "denied"' : flagged + ' flagged cells, all node-level');
  }

  /* ---- C26 -------------------------------------------------------------- */
  if (!PHONE.length) skip('C26 every surface reads at 375px', 'poison ' + POISON + ' does not drive it');
  else {
    check('c26', PHONE.length === CRITIC.length, 'C26 the phone sweep reached every surface of the critic sweep',
      PHONE.length + ' of ' + CRITIC.length);
    for (const r of PHONE) {
      const routes = r.nav.filter((x) => x.link);
      const unreach = r.nav.filter((x) => !x.reachable).map((x) => x.label);
      const bad = [];
      if (r.scrollW > r.vw + 1) bad.push(`page ${r.scrollW}px wide in ${r.vw}px`);
      if (r.overlaps.length) bad.push(r.overlaps.length + '+ text boxes overprinted: ' + clip(r.overlaps, 2));
      if (!r.toggle) bad.push('no VIEWS button to reach the routes');
      else if (r.nav.length < 8 || routes.length < 7 || unreach.length) {
        bad.push('VIEWS opens ' + r.nav.length + ' items, ' + routes.length + ' routes' +
          (unreach.length ? ', not reachable: ' + clip(unreach, 3) : ''));
      }
      if (r.have < r.want) bad.push(`${r.what}: ${r.have} of ${r.want}`);
      check('c26', bad.length === 0, `C26 ${r.name} reads at 375px (${r.hash})`,
        bad.length ? bad.join(' · ') : `no sideways scroll · no overprint · ${r.nav.length} routes in VIEWS · ${r.have} ${r.what}`);
    }
  }

  /* ---- C31 -------------------------------------------------------------- */
  /* A Tier 1 claim that records what someone said is marked as such wherever it
     is drawn, and only those claims are: the rows on the Grusch page, in the
     evidence table and on a node report, against the rule restated at the top
     of this file applied to the record. */
  {
    const want = (claims, key) => new Map(claims.map((c) => {
      const s = srcOf(c.source);
      return [c.id, saidRule(c.tier, c.text, s.text, s.url)];
    }));
    const recWant = want(personRec.claims || []);
    const evWant = want(claimRows);
    const repWant = want(focusRec.claims || []);
    for (const [where, rows, map, total] of [
      ['#/n/' + PERSON_FOCUS, (S.person && S.person.said) || [], recWant, (personRec.claims || []).length],
      ['#/evidence (rows drawn)', (S.evidence && S.evidence.said) || [], evWant, null],
      ['#/report/n/' + NODE_FOCUS, (S.report && S.report.said) || [], repWant, (focusRec.claims || []).length],
    ]) {
      const wrong = rows.filter((r) => !map.has(r.cid) || (map.get(r.cid) || null) !== (r.kind || null))
        .map((r) => (r.cid || '(no id)') + ' page ' + (r.kind || '-') + ' rule ' + (map.get(r.cid) || '-'));
      const marked = rows.filter((r) => r.kind).length;
      const words = rows.filter((r) => r.kind && (!r.shown || !r.title ||
        r.text !== (r.kind === 'said' ? 'said on the record' : "the office's own account"))).length;
      check('c31', rows.length > 0 && (total == null || rows.length === total) && wrong.length === 0 && words === 0 &&
        (where.startsWith('#/n/') ? marked > 0 : true),
        `C31 ${where}: the claims marked as said on the record are exactly the ones the rule picks`,
        `${rows.length} rows · ${marked} marked` + (total != null ? ` · record ${total}` : '') +
        (wrong.length ? ' · wrong ' + clip(wrong, 2) : '') + (words ? ` · ${words} marks unshown or mis-worded` : ''));
    }
    const all = claimRows.filter((c) => c.tier === 1);
    const n = all.filter((c) => saidRule(c.tier, c.text, c.source && c.source.text, c.source && c.source.url)).length;
    console.log(`  info  C31 the rule marks ${n} of ${all.length} Tier 1 claims on the board`);
  }

  /* ---- C32 -------------------------------------------------------------- */
  if (!TAB.length) skip('C32 the closed analyst tab covers no text', 'poison ' + POISON + ' does not drive it');
  else {
    const bad = TAB.filter((t) => !t.tab.present || t.tab.open !== '0' || t.texts.length)
      .map((t) => `${t.w} ${t.name}: ` + (t.tab.present ? t.texts.length + ' text boxes under it (' + clip(t.texts, 2) + ')' : 'no tab'));
    check('c32', bad.length === 0 && TAB.length >= CRITIC.length,
      'C32 the closed analyst tab sits on no text, on every critic surface at 1920, 1366 and 375',
      bad.length ? clip(bad, 3) : TAB.length + ' screens, the tab over no text on any');
  }

  /* ---- C33 -------------------------------------------------------------- */
  {
    const done = threads.filter((t) => S['thread:' + t.id] && S['thread:' + t.id].slice);
    for (const t of done) {
      const sl = S['thread:' + t.id].slice;
      const want = [...new Set(t.steps.map((x) => x.year).filter((y) => y != null).map(Number))].sort((a, b) => a - b);
      const order = sl.labs.slice().sort((a, b) => a.y - b.y || a.x - b.x).map((l) => l.year);
      const inOrder = order.every((y, i) => i === 0 || y > order[i - 1]);
      const same = order.length === want.length && want.every((y) => order.includes(y));
      const over = pairsOverlapping(sl.labs, 3);
      const out = sl.labs.filter((l) => l.x < sl.axisL - 1 || l.x + l.w > sl.axisR + 1).length;
      check('c33', inOrder && same && over.length === 0 && out === 0,
        `C33 #/t/${t.id}: the timeline slice reads in year order and names every year`,
        'reads ' + order.join(' ') + ' · steps carry ' + want.join(' ') +
        (over.length ? ' · overlapping ' + clip(over, 2) : '') + (out ? ` · ${out} outside the slice` : ''));
    }
  }

  /* ---- C34 -------------------------------------------------------------- */
  {
    const ax = S.timeline.axis;
    const present = Number(String(index.generated || '').slice(0, 4));
    const era = (index.eras || []).find((e) => e.label === ax.openEra);
    const inEra = era ? tlEvents.filter((e) => e.era === era.id) : [];
    const yrs = new Set(inEra.map((e) => Number(String(e.date).slice(0, 4))));
    const empty = ax.years.filter((y) => y > present && !yrs.has(y));
    const last = Math.max(...yrs);
    check('c34', ax.years.length > 0 && empty.length === 0 && Math.max(...ax.years) === last,
      'C34 the timeline axis stops at the last year that has an event, with no empty future year',
      `open era ${ax.openEra} · axis ${ax.years[0]} to ${Math.max(...ax.years)} · last event ${last} · board dated ${present}` +
      (empty.length ? ' · empty future years ' + empty.join(', ') : ''));
    const undated = (index.eras || []).filter((e) => e.start == null && e.end == null);
    const hasUndated = undated.some((e) => tlEvents.some((x) => x.era === e.id));
    const drawn = ax.heads.filter((l) => undated.some((e) => e.label === l)).length;
    check('c34', hasUndated ? drawn === 1 : drawn === 0,
      'C34 the NO DATE column is drawn only when it holds an event',
      `${tlEvents.filter((x) => undated.some((e) => e.id === x.era)).length} undated events · ${drawn} NO DATE heads drawn`);
  }

  /* ---- C35 -------------------------------------------------------------- */
  {
    const hits = [];
    for (const [id, snap] of Object.entries(S)) {
      const text = (snap && snap.text) || '';
      for (const re of JARGON) {
        const m = text.match(re);
        if (m) hits.push(id + ': "' + m[0] + '"');
      }
    }
    check('c35', hits.length === 0, 'C35 no screen shows the internal vocabulary the reader was shown until phase 5b',
      hits.length ? clip(hits, 3) : Object.keys(S).length + ' screens read');
    const chrome = [];
    for (const [id, snap] of Object.entries(S)) {
      const bar = (snap && snap.bar) || '';
      if (/#\//.test(bar) || /\d{3,4}\s*[×x]\s*\d{3,4}/.test(bar)) chrome.push(id + ': "' + bar.slice(-40) + '"');
    }
    check('c35', chrome.length === 0 && Object.values(S).some((x) => x && x.bar),
      'C35 the bar carries no raw route and no viewport badge', chrome.length ? clip(chrome, 2) : 'clean on every screen');
  }

  /* ---- C36 -------------------------------------------------------------- */
  /* A topic page is its record: every item of every block, each cite it
     renders exactly once with the tier, words, source, node and mark the
     record gives that id; members in the role the record gives them; the
     three blocks there whenever the record fills them; a research gap says so;
     and nothing runs off the side of a phone. */
  {
    for (const [stopId, tid] of [['topic', TOPIC_A], ['topic2', TOPIC_B], ['topicgap', TOPIC_GAP]]) {
      const rec = topicRecs[tid];
      const got = S[stopId] && S[stopId].topic;
      if (!got || got.id !== tid) {
        check('c36', false, `C36 #/topic/${tid} draws the topic`, got ? 'drew ' + got.id : 'not reached');
        continue;
      }
      const blocks = [['lead', rec.lead ? [rec.lead] : []], ['summary', rec.summary || []],
        ['record', rec.record || []], ['claimed', rec.claimed || []], ['contested', rec.contested || []]];
      const bad = [];
      let nItems = 0, nCites = 0;
      for (const [b, list] of blocks) {
        const drawn = got.items.filter((i) => i.block === b);
        if (drawn.length !== list.length) { bad.push(`${b}: ${drawn.length} items drawn, record ${list.length}`); continue; }
        list.forEach((it, k) => {
          const d = drawn[k];
          nItems++;
          if (!d.text.startsWith(String(it.text).slice(0, 60))) bad.push(`${b}[${k}] words differ from the record`);
          const ids = d.cites.map((c) => c.cid);
          const want = it.cite || [];
          nCites += ids.length;
          const missing = want.filter((x) => !ids.includes(x));
          const extra = ids.filter((x) => !want.includes(x));
          const twice = ids.filter((x, i) => ids.indexOf(x) !== i);
          if (missing.length || extra.length || twice.length) {
            bad.push(`${b}[${k}]` + (missing.length ? ' missing ' + clip(missing, 2) : '') +
              (extra.length ? ' extra ' + clip(extra, 2) : '') + (twice.length ? ' twice ' + clip(twice, 2) : ''));
          }
          if (d.refs !== want.length) bad.push(`${b}[${k}] ${d.refs} numbered references for ${want.length} cites`);
        });
      }
      check('c36', bad.length === 0, `C36 #/topic/${tid}: every item renders each of its cites exactly once`,
        bad.length ? clip(bad, 3) : `${nItems} items, ${nCites} cites, as the record has them`);

      const cb = [];
      for (const d of got.items) for (const c of d.cites) {
        const r = rec.cites[c.cid];
        if (!r) { cb.push(c.cid + ' is not in the record'); continue; }
        if (c.tier !== 'T' + r.tier) cb.push(`${c.cid} drawn ${c.tier || 'untiered'}, record T${r.tier}`);
        if (!c.words.includes(String(r.text || '').slice(0, 50))) cb.push(c.cid + ' words not shown');
        if (r.kind === 'claim') {
          const s = r.source || {};
          /* phase 8: a resolved claim links each of its registry sources' pages */
          const shown = (r.sourceRefs || []).length
            ? r.sourceRefs.every((x) => c.srcs.some((y) => y.href === '#/s/' + x.id))
            : s.url ? c.srcs.some((x) => x.text.includes(String(s.text || '').slice(0, 40)) || x.href === s.url)
              : c.srcs.some((x) => x.text.includes(String(s.text || '').slice(0, 40)));
          if (!shown) cb.push(c.cid + ' source not shown');
          const want = saidRule(r.tier, r.text, s.text, s.url);
          if ((want || null) !== (c.said || null)) cb.push(`${c.cid} mark ${c.said || 'none'}, rule ${want || 'none'}`);
          if (r.node && !c.nodes.includes('#/n/' + r.node)) cb.push(c.cid + ' no link to ' + r.node);
        } else {
          if (c.said) cb.push(c.cid + ' is an edge and carries the mark');
          for (const s of r.sources || []) {
            const shown = s.url ? c.srcs.some((x) => x.href === s.url) : c.srcs.some((x) => x.text.includes(String(s.name || '').slice(0, 40)));
            if (!shown) { cb.push(c.cid + ' source ' + (s.name || s.url) + ' not shown'); break; }
          }
          for (const e of r.endpoints || []) if (!c.nodes.includes('#/n/' + e.id)) cb.push(c.cid + ' no link to ' + e.id);
        }
      }
      check('c36', cb.length === 0, `C36 #/topic/${tid}: every cite shows its tier, its words, its source and its node, marked by the rule`,
        cb.length ? `${cb.length} wrong: ` + clip(cb, 3) : 'all as the record has them');

      const want = new Map();
      for (const m of rec.members || []) { if (!want.has(m.role)) want.set(m.role, []); want.get(m.role).push(m.id); }
      const gotM = new Map(got.members.map((g) => [g.role, g.ids.slice().sort()]));
      const mb = [];
      for (const [role, ids] of want) {
        const g = gotM.get(role) || [];
        if (ids.slice().sort().join('|') !== g.join('|')) mb.push(`${role}: drew ${g.length}, record ${ids.length}`);
      }
      for (const role of gotM.keys()) if (!want.has(role)) mb.push(role + ': drawn, not in the record');
      check('c36', mb.length === 0, `C36 #/topic/${tid}: members by role are the record's`,
        mb.length ? clip(mb, 3) : `${(rec.members || []).length} members in ${want.size} roles`);

      const needB = ['record', 'claimed', 'contested'].filter((b) => (rec[b] || []).length);
      const missB = needB.filter((b) => !got.blocks.includes(b));
      const gapWant = rec.researchGap ? String(rec.researchGap) : '';
      const gapOk = gapWant ? !!got.gap && /research gap/i.test(got.gap) && got.gap.includes(gapWant.slice(0, 60)) : got.gap === null;
      check('c36', missB.length === 0 && gapOk, `C36 #/topic/${tid}: its blocks are there, and a research gap says so`,
        (missB.length ? 'missing ' + missB.join(', ') + ' · ' : '') + 'blocks ' + (got.blocks.join(', ') || 'none') +
        ' · gap ' + (gapWant ? (gapOk ? 'labelled' : 'NOT labelled') : (gapOk ? 'none, rightly' : 'labelled on a topic that is not one')));
    }
    if (TP.length) {
      const wide = TP.filter((t) => t.scrollW > t.vw + 1 || (!t.items && !t.gap)).map((t) => t.id + ' ' + t.scrollW + 'px, ' + t.items + ' items');
      check('c36', wide.length === 0 && TP.length === 3, 'C36 every topic page reads at 375px with no sideways scroll',
        wide.length ? clip(wide, 3) : TP.map((t) => t.id).join(', '));
    }
  }

  /* ---- C37 -------------------------------------------------------------- */
  /* The Atlas: one chip per topic in its own section and era, every label
     whole at 11px at both laptop sizes with no cell mode, no two chips on each
     other, every chip one height; no lines at rest and the related links on
     focus; the filters count what they say; a phone lists every topic. */
  if (!driveAtlas) skip('C37 the Atlas', 'poison ' + POISON + ' does not drive it');
  else {
    const want = topicsFile.topics;
    const byId = new Map(want.map((t) => [t.id, t]));
    for (const key of ['atlas1366', 'atlas1920']) {
      const a = AT.sizes[key];
      if (!a) { check('c37', false, 'C37 ' + key + ' reached', 'no'); continue; }
      const ids = a.chips.map((c) => c.id);
      const miss = want.filter((t) => !ids.includes(t.id)).map((t) => t.id);
      const twice = ids.filter((x, i) => ids.indexOf(x) !== i);
      const stray = ids.filter((x) => !byId.has(x));
      const wrongCell = a.chips.filter((c) => {
        const t = byId.get(c.id);
        if (!t) return false;
        const cell = a.cells.find((x) => x.section === t.section && x.era === String(t.focusEra));
        if (!cell || c.section !== t.section || c.era !== String(t.focusEra)) return true;
        const cx = c.x + Math.min(c.w, 20) / 2, cy = c.y + c.h / 2;
        return cx < cell.x - 1 || cx > cell.x + cell.w + 1 || cy < cell.y - 1 || cy > cell.y + cell.h + 1;
      }).map((c) => c.id);
      check('c37', !miss.length && !twice.length && !stray.length && !wrongCell.length && a.chips.length === want.length,
        `C37 ${key}: every topic has exactly one chip, in its own section and era`,
        miss.length || twice.length || stray.length || wrongCell.length
          ? `missing ${clip(miss, 2)} · twice ${clip(twice, 2)} · stray ${clip(stray, 2)} · wrong cell ${clip(wrongCell, 2)}`
          : `${a.chips.length} chips for ${want.length} topics`);
      const lab = a.chips.filter((c) => {
        const t = byId.get(c.id);
        return !t || c.label !== t.title || c.fs !== '11px' || c.clipped || !c.labIn || (c.to && c.to !== 'clip');
      }).map((c) => c.id + (c.fs !== '11px' ? ' at ' + c.fs : '') + (c.clipped ? ' clipped' : '') + (!c.labIn ? ' outside its chip' : ''));
      check('c37', lab.length === 0 && !a.mode, `C37 ${key}: every label is the whole title at 11px, drawn in full, no cell mode`,
        lab.length ? `${lab.length} bad: ` + clip(lab, 3) : `${a.chips.length} labels whole` + (a.mode ? ' · mode ' + a.mode : ''));
      const over = pairsOverlapping(a.chips, 4);
      const hs = [...new Set(a.chips.map((c) => Math.round(c.h)))];
      check('c37', over.length === 0 && hs.length === 1, `C37 ${key}: no two chips overlap, and every chip is one height`,
        (over.length ? 'overlapping ' + clip(over, 3) + ' · ' : '') + 'heights ' + hs.join(', ') + 'px');
      check('c37', a.links.length === 0, `C37 ${key}: no lines at rest`, a.links.length + ' drawn');
    }
    const f = AT.focus;
    if (f) {
      const same = (x) => x.slice().sort().join('|') === f.want.slice().sort().join('|');
      check('c37', same(f.hover) && f.after.length === 0 && same(f.keyb),
        'C37 focusing a chip, by mouse or keyboard, draws exactly its related-topic links, and leaving it clears them',
        `${f.id}: related ${f.want.length} · hover drew ${f.hover.length} · after ${f.after.length} · keyboard drew ${f.keyb.length}`);
    } else check('c37', false, 'C37 focusing a chip draws its related-topic links', 'no topic with related topics was driven');
    const fl = AT.filters;
    if (fl) {
      const bad = ['kind', 'contested', 'questions'].filter((k) => fl.got[k] !== fl.want[k]);
      check('c37', bad.length === 0 && fl.reset === want.length,
        'C37 the three filters (kind, contested, open questions) show exactly the topics they name',
        ['kind', 'contested', 'questions'].map((k) => `${k} ${fl.got[k]}/${fl.want[k]}`).join(' · ') + ` · reset ${fl.reset}`);
    }
    const ph = AT.phone;
    if (ph) {
      const named = ph.list.filter((x) => x.named).map((x) => x.href.replace('#/topic/', ''));
      const miss = want.filter((t) => !named.includes(t.id)).map((t) => t.id);
      check('c37', miss.length === 0 && ph.list.length === want.length && ph.scrollW <= ph.vw + 1,
        'C37 at 375px the Atlas is stacked lists that name every topic, with no sideways scroll',
        `${named.length} of ${want.length} named` + (miss.length ? ' · missing ' + clip(miss, 3) : '') + ` · page ${ph.scrollW}px`);
    }
  }

  /* ---- C38 -------------------------------------------------------------- */
  /* Home lists the ten sections in their order, each with its own topics as
     links, every topic exactly once. */
  {
    const got = S.home.sections || [];
    const secs = topicsFile.sections.map((s) => s.id);
    const orderOk = got.map((g) => g.section).join('|') === secs.join('|');
    const bad = [];
    const all = [];
    for (const g of got) {
      const want = topicsFile.topics.filter((t) => t.section === g.section).map((t) => '#/topic/' + t.id).sort();
      if (g.topics.slice().sort().join('|') !== want.join('|')) bad.push(`${g.section}: ${g.topics.length} drawn, ${want.length} topics`);
      all.push(...g.topics);
    }
    const twice = all.filter((x, i) => all.indexOf(x) !== i);
    check('c38', orderOk && bad.length === 0 && twice.length === 0 && all.length === topicsFile.topics.length,
      "C38 Home lists the ten sections in order, each with exactly its own topics",
      (orderOk ? '' : 'sections drawn ' + clip(got.map((g) => g.section), 3) + ' · ') +
      (bad.length ? clip(bad, 3) : `${got.length} sections, ${all.length} topic links`) + (twice.length ? ' · twice ' + clip(twice, 2) : ''));
  }

  /* ---- C39 -------------------------------------------------------------- */
  /* An entity's Appears in row is its topic memberships, primary first, and
     it sits above About. */
  {
    for (const [stopId, nid] of [['node', NODE_FOCUS], ['person', PERSON_FOCUS]]) {
      const a = S[stopId] && S[stopId].appears;
      const want = topicsOf(nid);
      if (!a) { check('c39', false, 'C39 #/n/' + nid + ' Appears in', 'not reached'); continue; }
      const gotIds = a.chips.map((c) => c.href.replace('#/topic/', ''));
      const wantIds = want.map((w) => w.topic);
      const roleBad = a.chips.filter((c, i) => want[i] && c.role !== want[i].role).length;
      const above = a.top != null && a.aboutTop != null && a.top < a.aboutTop;
      check('c39', a.present && gotIds.join('|') === wantIds.join('|') && roleBad === 0 && above,
        `C39 #/n/${nid}: Appears in is its ${wantIds.length} topics, primary first, above About`,
        `drew ${gotIds.length} [${clip(gotIds, 3)}] · want [${clip(wantIds, 3)}]` +
        (roleBad ? ` · ${roleBad} roles wrong` : '') + (above ? '' : ' · NOT above About'));
    }
  }

  /* ---- C40 -------------------------------------------------------------- */
  /* The bar: HOME, ATLAS, TIMELINE, EVIDENCE, PATENTS in the row, DIRECTORIES,
     THREADS, NEIGHBOURHOOD, REPORT and LIBRARY under More, on every screen
     walked; More opens to them. (MAP left the bar with the map in phase 11.) */
  {
    const ROW = ['HOME', 'ATLAS', 'TIMELINE', 'EVIDENCE', 'PATENTS'];
    const MOREL = ['DIRECTORIES', 'THREADS', 'NEIGHBOURHOOD', 'REPORT', 'LIBRARY'];
    const bad = [];
    let n = 0;
    for (const [k, s] of Object.entries(S)) {
      if (!s || !s.nav) continue;
      n++;
      const row = s.nav.primary.map((x) => x.label);
      const more = s.nav.more.map((x) => x.label);
      if (row.join('|') !== ROW.join('|') || more.join('|') !== MOREL.join('|') || !s.nav.moreBtn) {
        bad.push(`${k}: row ${row.join(' ')} · more ${more.join(' ')}`);
      }
      const atlas = s.nav.primary.find((x) => x.label === 'ATLAS');
      if (!atlas || atlas.href !== '#/atlas') bad.push(k + ': ATLAS is not #/atlas');
    }
    check('c40', bad.length === 0 && n > 0, 'C40 the bar carries HOME ATLAS TIMELINE EVIDENCE PATENTS, and DIRECTORIES THREADS NEIGHBOURHOOD REPORT LIBRARY under More',
      bad.length ? clip(bad, 2) : `${n} screens`);
    if (MORE) {
      const unreach = MORE.open.filter((x) => x.href && !x.reachable).map((x) => x.label);
      check('c40', MORE.btn && !MORE.before && MORE.open.length >= 3 && unreach.length === 0,
        'C40 More opens to its routes, every one reachable',
        `button ${MORE.btn} · shown before opening ${MORE.before} · ${MORE.open.length} items` +
        (unreach.length ? ' · unreachable ' + unreach.join(', ') : ''));
    } else skip('C40 More opens to its routes', 'poison ' + POISON + ' does not drive it');
  }

  /* ---- C41 -------------------------------------------------------------- */
  /* An absorbed domain node's page opens with a pointer to the topic that
     absorbed it, above its title; a node that is not absorbed carries none. */
  {
    const d = S.domain && S.domain.absorbed;
    const want = domainRec.absorbedBy ? '#/topic/' + domainRec.absorbedBy : null;
    check('c41', !!d && !!want && d.present && d.href === want && d.top != null && d.h1Top != null && d.top < d.h1Top && d.top < d.vh,
      `C41 #/n/${DOMAIN_FOCUS} opens with a pointer to the topic that absorbed it`,
      d ? `pointer ${d.present ? d.href : 'absent'} · record ${want} · ${d.top != null && d.h1Top != null && d.top < d.h1Top ? 'above' : 'NOT above'} the title` : 'not reached');
    const n = S.node && S.node.absorbed;
    check('c41', !!n && !n.present && !focusRec.absorbedBy, `C41 #/n/${NODE_FOCUS}, which no topic absorbed, carries no pointer`,
      n ? (n.present ? 'carries ' + n.href : 'none') : 'not reached');
  }

  /* ---- C42 -------------------------------------------------------------- */
  /* The Library holds every source in sources.json: the count, the first page
     of rows in the order stated (most cited first, then title), each row a
     link to its page, every facet chip's count re-derived from the file with
     the other filters applied; a filtered and a searched state hold exactly
     the rows the file gives for them. */
  {
    const rows = libFile.sources;
    const KEYS = ['type', 'issuer', 'era', 'ip'];
    const val = (r, k) => k === 'type' ? r.type : k === 'issuer' ? (r.issuer || '-') : k === 'era' ? r.era : (r.interestedParty ? '1' : '0');
    const hit = (r, f, q, skip) => KEYS.every((k) => k === skip || !f[k] || val(r, k) === f[k]) &&
      (!q || q.toLowerCase().split(/\s+/).filter(Boolean).every((w) =>
        (r.title + ' ' + (r.issuer || '') + ' ' + r.identifiers.join(' ') + ' ' + r.id).toLowerCase().includes(w)));
    const order = (a, b) => (b.claims + b.edges) - (a.claims + a.edges) ||
      a.title.localeCompare(b.title, 'en', { sensitivity: 'base' });
    const judge = (key, hash, f, q) => {
      const L = S[key] && S[key].lib;
      if (!L) { check('c42', false, `C42 ${hash} draws the Library`, 'not reached'); return; }
      const want = rows.filter((r) => hit(r, f, q, null)).sort(order);
      const got = L.rows.map((r) => r.id);
      const first = want.slice(0, got.length).map((r) => r.id);
      const bad = [];
      if (L.n !== want.length) bad.push(`count ${L.n}, file ${want.length}`);
      if (got.length !== Math.min(100, want.length)) bad.push(`${got.length} rows drawn, want ${Math.min(100, want.length)}`);
      const wrong = got.filter((id, i) => id !== first[i]);
      if (wrong.length) bad.push(`${wrong.length} rows out of place or foreign: ` + clip(wrong, 3));
      const badHref = L.rows.filter((r) => r.href !== '#/s/' + r.id);
      if (badHref.length) bad.push(badHref.length + ' rows not linked to their page');
      check('c42', bad.length === 0, `C42 ${hash} draws the rows sources.json gives, in order, each linked`,
        bad.length ? bad.join(' · ') : `${L.n} sources, first ${got.length} drawn in order`);
      const cb = [];
      for (const fc of L.chips) {
        for (const c of fc.chips) {
          const n = rows.filter((r) => hit(r, f, q, fc.facet) && val(r, fc.facet) === c.value).length;
          if (c.n !== n || c.shown !== n) cb.push(`${fc.facet}=${c.value} shows ${c.shown}, file ${n}`);
          if (c.on !== (f[fc.facet] === c.value)) cb.push(`${fc.facet}=${c.value} ${c.on ? 'on' : 'off'} wrongly`);
        }
      }
      const facets = L.chips.map((x) => x.facet).join(',');
      check('c42', cb.length === 0 && facets === KEYS.join(','), `C42 ${hash}: every facet chip's count is the file's, with the other filters applied`,
        cb.length ? clip(cb, 3) : `${L.chips.reduce((a, x) => a + x.chips.length, 0)} chips over ${facets}`);
    };
    judge('library', '#/library', {}, '');
    const fq = new URLSearchParams(LIB_FILTER.split('?')[1]);
    judge('libraryf', LIB_FILTER, Object.fromEntries(KEYS.map((k) => [k, fq.get(k) || ''])), '');
    judge('libraryq', '#/library?q=' + LIB_SEARCH, {}, LIB_SEARCH);
  }

  /* ---- C43 -------------------------------------------------------------- */
  /* A source page is its record: the title, every web address and archived
     copy linked exactly, its node, and every claim that cites it, where "the
     claims that cite it" is re-derived from claims.json (every row whose
     sources name this id), not read from the page's own file. */
  {
    const P = S.source && S.source.src;
    if (!P) check('c43', false, 'C43 #/s/' + SOURCE_FOCUS + ' draws the source', 'not reached');
    else {
      const bad = [];
      if (P.id !== srcRec.id) bad.push('drew ' + P.id);
      if (P.h1 !== srcRec.title) bad.push('title differs');
      if (P.urls.join('|') !== srcRec.urls.join('|')) bad.push(`addresses ${P.urls.length}, record ${srcRec.urls.length}`);
      if (P.archived.join('|') !== srcRec.archived.join('|')) bad.push(`archived ${P.archived.length}, record ${srcRec.archived.length}`);
      if ((P.node || null) !== (srcRec.node ? '#/n/' + srcRec.node.id : null)) bad.push('node link ' + P.node);
      if (P.ip !== !!srcRec.interestedParty) bad.push('interested-party notice ' + (P.ip ? 'shown' : 'missing'));
      check('c43', bad.length === 0, `C43 #/s/${SOURCE_FOCUS} prints its record: title, addresses, archived copies, node`,
        bad.length ? bad.join(' · ') : `${P.urls.length} addresses, ${P.archived.length} archived, node ${P.node}`);
      const want = claimRows.filter((r) => (r.sources || []).some((x) => x.id === SOURCE_FOCUS));
      const wantIds = want.map((r) => r.id).sort();
      const gotIds = P.claims.map((c) => c.id).sort();
      const cb = [];
      if (wantIds.join('|') !== gotIds.join('|')) {
        cb.push(`drew ${gotIds.length}, claims.json names ${wantIds.length}: missing ` +
          clip(wantIds.filter((x) => !gotIds.includes(x)), 2) + ', extra ' + clip(gotIds.filter((x) => !wantIds.includes(x)), 2));
      }
      const byId = new Map(want.map((r) => [r.id, r]));
      for (const c of P.claims) {
        const r = byId.get(c.id);
        if (!r) continue;
        if (c.tier !== 'T' + r.tier) cb.push(`${c.id} drawn ${c.tier}, record T${r.tier}`);
        if (!c.text.includes(String(r.text).slice(0, 50))) cb.push(c.id + ' words not shown');
        if (c.node !== r.node) cb.push(`${c.id} grouped under ${c.node}, sits on ${r.node}`);
        if (!c.cited.includes(String(r.source.text || '').slice(0, 30))) cb.push(c.id + ' citation as written not shown');
      }
      check('c43', cb.length === 0, `C43 #/s/${SOURCE_FOCUS} shows every claim claims.json resolves to it, under its node, with the citation as written`,
        cb.length ? clip(cb, 3) : `${gotIds.length} claims`);
      const eWant = srcRec.edges.map((e) => e.id).sort().join('|');
      check('c43', P.edges.slice().sort().join('|') === eWant, `C43 #/s/${SOURCE_FOCUS} lists the links citing it`,
        `${P.edges.length} drawn, record ${srcRec.edges.length}`);
    }
  }

  /* ---- C44 -------------------------------------------------------------- */
  /* Every claim row links each of its registry sources' pages and nothing
     else, on the node page, the person page and the evidence table; a claim
     the registry does not resolve prints its citation as written instead. */
  {
    const want = new Map(claimRows.map((r) => [r.id, r]));
    for (const [key, where] of [['node', '#/n/' + NODE_FOCUS], ['person', '#/n/' + PERSON_FOCUS], ['evidence2', '#/evidence?tier=1']]) {
      const L = S[key] && S[key].links;
      if (!L || !L.length) { check('c44', false, `C44 ${where}: claim rows carry their source links`, 'no rows read'); continue; }
      const bad = [];
      let linked = 0;
      for (const r of L) {
        const w = want.get(r.cid);
        if (!w) { bad.push(r.cid + ' not in claims.json'); continue; }
        const ids = (w.sources || []).map((x) => '#/s/' + x.id);
        if (ids.join('|') !== r.links.join('|')) bad.push(`${r.cid} links ${clip(r.links, 2)}, record ${clip(ids, 2)}`);
        if (!ids.length && (!r.nolink || (w.source.text && !r.nolinkText.includes(String(w.source.text).slice(0, 30)))))
          bad.push(r.cid + ' unresolved but its citation is not printed');
        if (ids.length) linked++;
      }
      check('c44', bad.length === 0, `C44 ${where}: every claim row links exactly its registry sources, or prints its citation`,
        bad.length ? `${bad.length} wrong: ` + clip(bad, 3) : `${L.length} rows, ${linked} linked to the Library`);
    }
  }

  /* ---- C45 -------------------------------------------------------------- */
  /* A web address breaks only at its break points: the element does not let
     the browser break inside a word (overflow-wrap and word-break normal),
     carries break points, stays inside the screen, and no stretch of it
     between two break points is itself split across lines. On the source page
     at 1920, and at 375 on the same page and on the source with the most
     addresses. */
  {
    for (const [where, W] of [['#/s/' + SOURCE_FOCUS + ' at 1920', S.source && S.source.wrap],
      ['#/s/' + SOURCE_FOCUS + ' at 375', WRAP375], ['#/s/' + (wrapRec ? wrapRec.id : '?') + ' at 375', WRAPX]]) {
      if (!W || !W.length) {
        if (POISON && !POISON.startsWith('c45') && !W) skip('C45 ' + where, 'poison ' + POISON + ' does not drive it');
        else if (POISON && !POISON.startsWith('c45')) skip('C45 ' + where, 'poison ' + POISON + ' does not drive it');
        else check('c45', false, `C45 ${where}: web addresses break only at their break points`, 'no addresses read');
        continue;
      }
      const bad = [];
      for (const u of W) {
        if (u.ow !== 'normal' || u.wb !== 'normal') bad.push(`${u.text}: wraps ${u.ow}/${u.wb}`);
        if (u.len > 24 && u.wbr === 0) bad.push(`${u.text}: no break points`);
        if (u.right > u.vw + 1) bad.push(`${u.text}: runs to ${u.right}px in ${u.vw}`);
        if (u.split) bad.push(`${u.text}: ${u.split} stretches broken mid-word`);
      }
      check('c45', bad.length === 0, `C45 ${where}: web addresses break only at their break points`,
        bad.length ? `${bad.length} wrong: ` + clip(bad, 2) : `${W.length} addresses`);
    }
  }

  /* ---- C24 -------------------------------------------------------------- */
  if (!SEARCH || SEARCH.events === undefined) {
    skip('C24 search reaches timeline events and threads', 'poison ' + POISON + ' does not drive it');
  } else {
    const wantEv = tlEvents.filter((e) => /scandinavia/i.test((e.label || '') + ' ' + (e.text || ''))).length;
    check('c24', wantEv > 0 && SEARCH.events > 0,
      'C24 search reaches timeline events', `record ${wantEv} · results ${SEARCH.events}`);
    const wantTh = threads.filter((t) => /wilson.?davis/i.test((t.title || t.label || '') + ' ' + t.id)).length;
    check('c24', wantTh > 0 && SEARCH.threads > 0,
      'C24 search reaches threads', `record ${wantTh} · results ${SEARCH.threads}`);
  }

  /* ---- C14 -------------------------------------------------------------- */
  {
    const origin = new URL(APP).origin;
    const worker = (analystFile.worker || '').replace(/\/+$/, '');
    const bad = [];
    for (const u of requests) {
      if (/^(data|blob):/.test(u)) continue;
      if (worker && u.startsWith(worker + '/api/analyst')) continue;
      if (!u.startsWith(origin)) { bad.push(u); continue; }
      const p = new URL(u).pathname;
      if (p === '/' || p === '/index.html') continue;
      if (/^\/(data|fonts|patents|assets)\//.test(p)) continue;
      if (/^\/api\/analyst(\/|$)/.test(p)) continue;      /* the analyst, same-origin first */
      bad.push(u);
    }
    const uniq = [...new Set(bad)];
    check('c14', uniq.length === 0,
      'C14 every runtime request is /data /fonts /patents /assets or the analyst',
      uniq.length ? `${uniq.length} off-list: ` + clip(uniq.map((u) => u.slice(0, 70)), 3)
        : `${requests.length} requests over ${Object.keys(S).length} screens, all on the list`);
    check('c14', pageErrors.length === 0, 'C14 no uncaught page error while the screens were walked',
      pageErrors.length ? clip(pageErrors, 2) : 'clean');
  }

  /* ---- C15 -------------------------------------------------------------- */
  /* Phase 9: the lanes are the topic sections. The section an event belongs to
     is re-derived HERE from the topic files (its node's primary topic, by
     topicsOf, the same order the node page's "Appears in" is held to), never read
     from timeline.json's own `section`. Every event of the open era is either a
     named chip or one of the events a count stands for, and nothing is drawn
     without a name. */
  {
    const t = S.timeline.timeline;
    const byEv = new Map(tlEvents.map((e) => [e.id, e]));
    const secOf = (e) => {
      if (!e.node) return 'other';
      const f = topicsOf(e.node)[0];
      return f && topicRecs[f.topic] ? topicRecs[f.topic].section : 'other';
    };
    const packOf = new Map(t.packs.map((p) => [p.section + '|' + p.era, p]));
    const wrongLane = [], wrongEra = [], outside = [], repeats = [];
    const inside = (it, p) => it.x >= p.x - 1 && it.x + it.w <= p.x + p.w + 1 && it.y >= p.y - 1 && it.y + it.h <= p.y + p.h + 1;
    const drawn = [];
    for (const it of [...t.items, ...t.mores]) {
      const ids = it.kind === 'more' ? it.ids : [it.id];
      for (const id of ids) {
        const e = byEv.get(id);
        if (!e) { wrongEra.push(id + ' (not in timeline.json)'); continue; }
        drawn.push(id);
        if (e.sameAs) repeats.push(id + ' repeats ' + e.sameAs);
        if (secOf(e) !== it.section) wrongLane.push(`${id} drawn in ${it.section}, belongs in ${secOf(e)}`);
        if (String(e.era) !== String(it.era)) wrongEra.push(`${id} drawn in era ${it.era}, is ${e.era}`);
      }
      const p = packOf.get(it.section + '|' + it.era);
      if (!p || !inside(it, p)) outside.push(`${it.id} outside the ${it.section} lane`);
    }
    check('c15', wrongLane.length === 0 && wrongEra.length === 0,
      'C15 every timeline event is in the lane of its node\'s primary topic section, re-derived from the topic files, and in its own era',
      wrongLane.length + wrongEra.length ? clip([...wrongLane, ...wrongEra], 3) : `${drawn.length} events`);
    check('c15', outside.length === 0, 'C15 every chip and every count is drawn inside its own lane box',
      outside.length ? clip(outside, 3) : `${t.items.length} chips and ${t.mores.length} counts inside ${t.packs.length} lane boxes`);
    const openEra = t.packs.length ? t.packs[0].era : null;
    const want = tlEvents.filter((e) => String(e.era) === String(openEra) && !e.sameAs).map((e) => e.id).sort();
    const got = drawn.slice().sort();
    const dup = got.filter((x, i) => i && got[i - 1] === x);
    const printed = Number((t.openEraSub.match(/(\d+)\s+events/) || [])[1]);
    /* a count reads "+N", or "YYYY +N" where its year has room: the number and, when printed, the year must be its own */
    const cnt = (m) => { const x = /^(?:(\d{4}) )?\+(\d+)$/.exec(m.text); return x && Number(x[2]) === m.ids.length && (!x[1] || x[1] === m.year); };
    const miscount = t.mores.filter((m) => !cnt(m)).map((m) => m.id + ' says ' + m.text + ', holds ' + m.ids.length);
    check('c15', got.join('|') === want.join('|') && dup.length === 0 && printed === want.length && repeats.length === 0 && miscount.length === 0,
      'C15 the open era names every one of its events once, on a chip or behind a count that says how many',
      `era ${openEra}: ${t.items.length} chips + ${t.mores.reduce((a, m) => a + m.ids.length, 0)} counted = ${got.length}, ` +
      `timeline.json has ${want.length} less its repeats, header says ${printed}` +
      (dup.length ? ' · twice: ' + clip(dup, 3) : '') + (repeats.length ? ' · repeats drawn: ' + clip(repeats, 2) : '') +
      (miscount.length ? ' · ' + clip(miscount, 2) : ''));
    const unnamed = t.items.filter((i) => !i.text).map((i) => i.id);
    check('c15', t.marks === 0 && unnamed.length === 0, 'C15 nothing on the timeline is drawn without a name',
      `${t.marks} unnamed marks · ${unnamed.length} chips without text`);
  }

  /* ---- C50 -------------------------------------------------------------- */
  {
    /* #/places is the places page since phase 11: C71 holds its list */
    const want = { people: 'person', orgs: 'institution', programmes: 'program', laws: 'legislation', events: 'event' };
    const bad = [];
    let n = 0;
    for (const [d, cls] of Object.entries(want)) {
      const s = S['dir:' + d];
      if (!s || !s.dir) continue;
      n++;
      const ids = index.nodes.filter((x) => x.cls === cls).map((x) => x.id).sort();
      const got = s.dir.rows.map((r) => r.id).sort();
      const dup = got.filter((x, i) => i && got[i - 1] === x);
      const miss = ids.filter((x) => !got.includes(x));
      const extra = got.filter((x) => !ids.includes(x));
      const unlinked = s.dir.rows.filter((r) => r.href !== '#/n/' + r.id || !r.name).map((r) => r.id);
      if (dup.length || miss.length || extra.length || unlinked.length || s.dir.count !== ids.length) {
        bad.push(`#/${d}: ${got.length} rows for ${ids.length} ${cls} nodes, header ${s.dir.count}` +
          (dup.length ? ', twice ' + clip(dup, 2) : '') + (miss.length ? ', missing ' + clip(miss, 2) : '') +
          (extra.length ? ', not ' + cls + ' ' + clip(extra, 2) : '') + (unlinked.length ? ', unlinked ' + clip(unlinked, 2) : ''));
      }
    }
    if (!n) skip('C50 every directory lists every node of its class once', 'poison ' + POISON + ' does not walk the directories');
    else check('c50', bad.length === 0 && n === 5, 'C50 every directory lists every node of its class exactly once, each row linking its node',
      bad.length ? clip(bad, 2) : n + ' directories, every row linked');
  }

  /* ---- C51 -------------------------------------------------------------- */
  /* The people directory's facet counts and filters against the side-car read
     off the disk, not against what the server ships. */
  {
    const s = S['dir:people'];
    if (!s || !s.dir) skip('C51 the people facets match research/_person_facets.json', 'poison ' + POISON + ' does not walk the directories');
    else {
      const ROOT = resolve(dirname(SELF), '..', '..');
      const side = JSON.parse(readFileSync(resolve(ROOT, 'research', '_person_facets.json'), 'utf8')).people;
      const rows = Object.entries(side);
      const tally = {};
      const add = (k, v) => { tally[k + '=' + v] = (tally[k + '=' + v] || 0) + 1; };
      for (const [, r] of rows) {
        const roles = r.roles.filter((x) => x !== 'claimant');
        for (const x of (roles.length ? roles : ['none'])) add('role', x);
        add('claimant', r.roles.includes('claimant') ? 'yes' : 'no');
        add('vital', r.vitalStatus); add('rstatus', r.roleStatus); add('oath', r.underOath);
      }
      const all = [];
      for (const k of ['dir:people', 'dir:people:claimant', 'dir:people:dead', 'dir:people:oath', 'dir:people:witness']) {
        for (const c of (S[k] && S[k].dir ? S[k].dir.chips : [])) {
          if (!['role', 'claimant', 'vital', 'rstatus', 'oath'].includes(c.key)) continue;
          const w = tally[c.key + '=' + c.val] || 0;
          if (c.n !== w) all.push(`${k} chip ${c.key}=${c.val} says ${c.n}, the side-car has ${w}`);
        }
      }
      const missing = Object.keys(tally).filter((k) => !s.dir.chips.some((c) => c.key + '=' + c.val === k));
      check('c51', all.length === 0 && missing.length === 0 && s.dir.chips.length > 0,
        'C51 every people facet count equals research/_person_facets.json, and every value there has its chip',
        all.length || missing.length ? clip([...all, ...missing.map((m) => 'no chip for ' + m)], 3) : s.dir.chips.length + ' chips');
      const filt = [
        ['dir:people:claimant', ([, r]) => r.roles.includes('claimant'), 'claimant=yes'],
        ['dir:people:dead', ([, r]) => r.vitalStatus === 'dead', 'vital=dead'],
        ['dir:people:oath', ([, r]) => r.underOath === 'yes', 'oath=yes'],
        ['dir:people:witness', ([, r]) => r.roles.includes('witness'), 'role=witness'],
      ];
      for (const [k, f, qs] of filt) {
        const want = rows.filter(f).map(([id]) => id).sort();
        const got = S[k] && S[k].dir ? S[k].dir.rows.map((r) => r.id).sort() : [];
        check('c51', want.length > 0 && got.join('|') === want.join('|'),
          `C51 #/people?${qs} lists exactly the side-car's ${want.length}`,
          got.join('|') === want.join('|') ? got.length + ' rows' : `${got.length} rows, side-car ${want.length}: ` +
            clip([...want.filter((x) => !got.includes(x)).map((x) => 'missing ' + x), ...got.filter((x) => !want.includes(x)).map((x) => 'extra ' + x)], 3));
      }
    }
  }

  /* ---- C52 -------------------------------------------------------------- */
  if (!SEARCH || !SEARCH.topic) skip('C52 search reaches topics and directories, with keys', 'poison ' + POISON + ' does not drive it');
  else {
    const first = SEARCH.topic.rows[0];
    const tRow = SEARCH.topic.rows.find((r) => r.href === '#/topic/' + TOPIC_A);
    check('c52', !!first && first.href === '#/topic/' + TOPIC_A && !!tRow && /TOPIC/.test(tRow.badge),
      'C52 a topic\'s own title finds the topic, first, badged as a topic',
      `"${SEARCH.topic.q}": first row ${first ? first.href + ' (' + first.badge + ')' : 'none'}`);
    const dfirst = SEARCH.dir[0];
    check('c52', !!dfirst && dfirst.href === '#/people' && /DIRECTORY/.test(dfirst.badge),
      'C52 "people" finds the people directory first', dfirst ? dfirst.href + ' (' + dfirst.badge + ')' : 'no rows');
    const unbadged = [...SEARCH.topic.rows, ...SEARCH.dir].filter((r) => !r.badge || !r.type).map((r) => r.href);
    check('c52', unbadged.length === 0, 'C52 every search row carries a badge naming what it is',
      unbadged.length ? clip(unbadged, 3) : (SEARCH.topic.rows.length + SEARCH.dir.length) + ' rows');
    const sel = SEARCH.keys.rows.map((r, i) => (r.sel === 'true' ? i : -1)).filter((i) => i >= 0);
    const second = SEARCH.keys.rows[1];
    check('c52', sel.length === 1 && sel[0] === 1 && !!second && SEARCH.keys.hash === second.href,
      'C52 ArrowDown twice marks the second row, and Enter opens it',
      `marked ${JSON.stringify(sel)} · second row ${second ? second.href : 'none'} · landed ${SEARCH.keys.hash}`);
    check('c52', SEARCH.escape.value === '' && SEARCH.escape.hidden === true, 'C52 Escape clears the field and closes the list',
      JSON.stringify(SEARCH.escape));
  }

  /* ---- C53 -------------------------------------------------------------- */
  if (!TL) skip('C53 the timeline panel, counts, repeats, scope and strand', 'poison ' + POISON + ' does not drive it');
  else {
    const byEv = new Map(tlEvents.map((e) => [e.id, e]));
    if (TL.chip) {
      const e = byEv.get(TL.chip.id), pn = TL.chip.panel;
      const ok = pn.shown && pn.mode === 'event' && pn.id === e.id && pn.label === e.label && pn.text === e.text &&
        pn.date.startsWith(String(e.date).slice(0, 4)) && pn.node === '#/n/' + e.node &&
        (!e.grade || pn.grade.includes('grade ' + e.grade));
      check('c53', ok, 'C53 clicking an event shows its own label, text, date, grade and node',
        `${e.id}: label ${pn.label === e.label} · text ${pn.text === e.text} · date ${pn.date} · node ${pn.node} · grade "${pn.grade}"`);
    } else check('c53', false, 'C53 clicking an event shows its own label, text, date, grade and node', 'no chip with a node and text to click');
    if (TL.more) {
      const m = TL.more.more, pn = TL.more.panel;
      const got = pn.list.map((x) => x.id);
      const named = pn.list.every((x) => x.label && x.label === (byEv.get(x.id) || {}).label);
      check('c53', pn.mode === 'list' && got.length === m.ids.length && got.join('|') === m.ids.join('|') && named && m.text.endsWith('+' + m.ids.length),
        'C53 a count opens the named list of exactly the events it counts',
        `${m.text} in ${m.section} ${m.year}: list of ${got.length}, all named ${named}`);
    } else skip('C53 a count opens its named list', 'the open era placed every event on a chip');
    if (TL.rep) {
      const reps = tlEvents.filter((x) => x.sameAs === TL.rep.keep.id);
      const pn = TL.rep.panel;
      const got = pn.reps.map((r) => r.id).sort().join('|');
      check('c53', pn.id === TL.rep.keep.id && got === reps.map((r) => r.id).sort().join('|') &&
        pn.reps.every((r) => r.label === (byEv.get(r.id) || {}).label),
        'C53 a same-day repeat is shown once, under the event it repeats, with its own label',
        `${TL.rep.keep.id} carries ${pn.reps.length} of ${reps.length} repeats`);
    } else check('c53', false, 'C53 a same-day repeat is shown once, under the event it repeats', 'no kept event with a repeat in the open era');
    const unmarked = TL.sched.filter((x) => !x.marked).map((x) => x.id);
    check('c53', unmarked.length === 0, 'C53 every event after the board\'s date is marked scheduled where it is drawn',
      TL.sched.length + ' scheduled' + (unmarked.length ? ', unmarked ' + clip(unmarked, 3) : ''));
    const members = new Set((topicRecs[TOPIC_A].members || []).map((m) => m.id));
    const tIds = [...TL.topic.items.map((i) => i.id), ...TL.topic.mores.flatMap((m) => m.ids)];
    const tEra = TL.topic.packs.length ? TL.topic.packs[0].era : null;
    const tWant = tlEvents.filter((e) => !e.sameAs && e.node && members.has(e.node) && String(e.era) === String(tEra)).map((e) => e.id).sort();
    check('c53', tIds.length > 0 && tIds.slice().sort().join('|') === tWant.join('|') && TL.topic.scopeText.includes(topicRecs[TOPIC_A].title),
      'C53 ?topic= shows exactly the events whose node is a member of that topic, and says so',
      `${tIds.length} drawn, ${tWant.length} members' events in era ${tEra} · scope line "${TL.topic.scopeText.slice(0, 60)}"`);
    const sIds = [...TL.strand.items.map((i) => i.id), ...TL.strand.mores.flatMap((m) => m.ids)];
    const sEra = TL.strand.packs.length ? TL.strand.packs[0].era : null;
    const sWant = tlEvents.filter((e) => !e.sameAs && e.strand === 'witness' && String(e.era) === String(sEra)).map((e) => e.id).sort();
    check('c53', sIds.length > 0 && sIds.slice().sort().join('|') === sWant.join('|'),
      'C53 the strand filter shows exactly that strand\'s events', `${sIds.length} drawn, ${sWant.length} witness events in era ${sEra}`);
  }

  /* ---- C16 -------------------------------------------------------------- */
  {
    const hits = [];
    for (const k of Object.keys(S)) {
      const m = (S[k].text || '').match(new RegExp('.{0,30}(\\[placeholder|not in the extract).{0,40}', 'i'));
      if (m) hits.push(k + ': …' + m[0].replace(/\s+/g, ' ').trim() + '…');
    }
    check('c16', hits.length === 0, 'C16 no mockup placeholder string survives into any rendered page',
      hits.length ? `${hits.length} screen(s): ` + clip(hits, 2) : `${Object.keys(S).length} screens clean`);
  }

  /* ---- C17 -------------------------------------------------------------- */
  {
    const stops = Object.keys(S);
    const none = stops.filter((k) => !S[k].back);
    check('c17', none.length === 0 && stops.length > 0,
      'C17 a back control is drawn in the chrome of every screen walked',
      none.length ? `${none.length} without one: ` + clip(none, 4) : `${stops.length} screens, all carry one`);
    const wrong = stops.filter((k) => S[k].back &&
      (S[k].back.tag !== 'BUTTON' || S[k].back.type !== 'button' || !/back/i.test(S[k].back.text)));
    check('c17', wrong.length === 0 && stops.length > 0,
      'C17 it is a <button type="button"> reading Back, never a link',
      wrong.length ? clip(wrong.map((k) => k + ':' + S[k].back.tag + '/' + S[k].back.type), 4)
        : `${stops.length} screens, all button type=button`);

    const HOME = '#/', NODE = '#/n/' + NODE_FOCUS, NHOOD = '#/n/' + NODE_FOCUS + '/hood';
    check('c17', !!B.fresh && B.fresh.present && B.fresh.disabled === true && B.fresh.aria === 'true',
      'C17 on a cold deep link the button is disabled, so it can never leave the site',
      B.fresh ? `${NODE} cold: disabled=${B.fresh.disabled}, aria-disabled=${B.fresh.aria}`
        : 'the cold load was not reached');

    const walked = B.trail.map((x) => x.hash);
    check('c17', walked.join(' ') === [HOME, NODE, NHOOD].join(' '),
      "C17 the trail is built by clicking the pages' own links",
      'walked ' + (walked.join(' \u2192 ') || '(nothing)') + ' \u00b7 wanted ' + [HOME, NODE, NHOOD].join(' \u2192 '));
    check('c17', B.trail.length === 3 && B.trail[0].disabled === true && B.trail[2].disabled === false,
      "C17 disabled on the session's first page, enabled once a page has been left",
      B.trail.map((x) => x.hash + ' disabled=' + x.disabled).join(' \u00b7 ') || 'the trail was not reached');

    const clicked = B.clicks.map((x) => x.hash);
    check('c17', clicked.join(' ') === [NODE, HOME].join(' '),
      'C17 two clicks of the button step back over the trail, newest first',
      'the clicks landed ' + (clicked.join(' \u2192 ') || '(nowhere)') + ' \u00b7 wanted ' + [NODE, HOME].join(' \u2192 '));
    check('c17', B.clicks.length === 2 && B.clicks[1].disabled === true && B.clicks[1].aria === 'true',
      'C17 back at the first page of the session the button is disabled again',
      B.clicks.length === 2 ? `${B.clicks[1].hash}: disabled=${B.clicks[1].disabled}, aria-disabled=${B.clicks[1].aria}`
        : 'the second click was not reached');

    check('c17', !!B.forward && B.forward.hash === NHOOD,
      'C17 the button creates no history entry: forward twice reaches the neighbourhood again',
      B.forward ? 'forward, forward landed ' + B.forward.hash + ', wanted ' + NHOOD
        : 'the forward stack was not reached');

    const par = [B.parity.b1, B.parity.b2].map((x) => (x ? x.hash : '(nowhere)'));
    check('c17', par.join(' ') === [NODE, HOME].join(' '),
      "C17 the browser's own back walks the same two hashes in the same order",
      'goBack twice landed ' + par.join(' \u2192 ') + ' \u00b7 the button landed ' + (clicked.join(' \u2192 ') || '(nowhere)'));
    check('c17', !!B.parity.f1 && B.parity.f1.hash === NODE && B.parity.f1.disabled === false
      && !!B.parity.click && B.parity.click.hash === HOME,
      'C17 after a browser forward the button is enabled and one click returns home',
      (B.parity.f1 ? 'forward landed ' + B.parity.f1.hash + ' disabled=' + B.parity.f1.disabled : 'no forward')
      + ', then the button landed ' + (B.parity.click ? B.parity.click.hash : '(nowhere)'));

    const tips = B.trail.map((x) => x.title);
    check('c17', tips[0] === 'Back' && tips[1] === 'Back to Home' && tips[2] === 'Back to ' + focusRec.label,
      'C17 the tooltip names the page the button will return to',
      B.trail.map((x, i) => x.hash + ' says "' + tips[i] + '"').join(' \u00b7 ') || 'the trail was not reached');
  }

  /* ---- C18 -------------------------------------------------------------- */
  /* The analyst is on every route, its chips are the ones its data file gives
     that route, and the health line says which of its two states it is in. */
  {
    const byRoute = analystFile.byRoute || null;
    if (!CH.length) {
      skip("C18 the analyst chips are this route's chips", 'poison ' + POISON + ' does not reach the chip sweep');
    } else if (!byRoute) {
      check('c18', false, 'C18 analyst.json carries per-route chips',
        'shape=' + (analystFile.shape || 'none') + ', no byRoute map: the generator did not read data/analyst-suggestions.json');
    } else {
      const wrong = [], missing = [];
      for (const row of CH) {
        const want = byRoute[row.key] || [];
        const got = row.chips;
        if (!want.length) { missing.push(row.key); continue; }
        if (want.length !== got.length || want.some((x, i) => x !== got[i])) {
          wrong.push(row.key + ' ' + row.hash + ' drew [' + clip(got, 2) + '] wanted [' + clip(want, 2) + ']');
        }
      }
      check('c18', missing.length === 0, 'C18 every chip key the sweep visits is in the data file',
        missing.length ? 'no chips for ' + missing.join(', ') : CHIP_ROUTES.map((r) => r[0]).join(', '));
      check('c18', wrong.length === 0, "C18 the chips on screen are exactly that route kind's chips",
        wrong.length ? wrong.length + ' of ' + CH.length + ' wrong: ' + clip(wrong, 2)
          : CH.map((r) => r.key + ':' + r.chips.length).join(' · '));

      const thin = CH.filter((r) => r.chips.length < 3).map((r) => r.key + ' has ' + r.chips.length);
      check('c18', thin.length === 0, 'C18 every route kind offers at least three chips',
        thin.length ? thin.join(', ') : 'floor is 3, thinnest is ' + Math.min(...CH.map((r) => r.chips.length)));

      /* distinct route kinds must not all show the same list: that is exactly
         what the poison does, and what a key that always resolves home does */
      const sets = new Set(CH.map((r) => r.chips.join('')));
      check('c18', sets.size === CH.length, 'C18 no two route kinds show the same chips',
        sets.size + ' distinct lists over ' + CH.length + ' route kinds');

      const offScreen = CH.filter((r) => !r.strip.present || !r.strip.onScreen).map((r) => r.hash);
      check('c18', offScreen.length === 0, 'C18 the analyst strip is on screen on every route kind',
        offScreen.length ? 'not reachable on ' + clip(offScreen, 3)
          : CH.length + ' routes, tab ' + CH[0].strip.h + 'px in the bar on each');

      const covered = CH.filter((r) => r.strip.present && !r.strip.unobstructed).map((r) => r.hash);
      check('c18', covered.length === 0, 'C18 nothing is drawn over the analyst strip',
        covered.length ? 'covered on ' + clip(covered, 3) : 'the strip is the topmost element at its own centre everywhere');

      /* Only where the reader cannot scroll it out of the way. That was the
         map and the ring neighbourhood, which took the whole viewport; both
         went in phase 11 and every page scrolls now, so this holds for any page
         that does not, and says so when none is left. */
      const fixedRoutes = CH.filter((r) => r.strip.present && !r.strip.scrolls);
      const covering = fixedRoutes.filter((r) => r.strip.covers.length)
        .map((r) => r.hash + ' covers ' + r.strip.covers.length + ': ' + r.strip.covers[0]);
      check('c18', covering.length === 0,
        'C18 on a page that cannot scroll, the closed tab covers nothing the page drew',
        covering.length ? clip(covering, 2)
          : fixedRoutes.length + ' of ' + CH.length + ' routes do not scroll ('
            + fixedRoutes.map((r) => r.hash).join(', ') + '), and the tab is over nothing on them');

      const shut = CH.filter((r) => r.open !== '1').map((r) => r.hash);
      check('c18', shut.length === 0, 'C18 clicking the strip opens the dock',
        shut.length ? 'stayed shut on ' + clip(shut, 3) : 'opened on all ' + CH.length);

      const LIVE = 'live · no key needed';
      const DEAD = 'endpoint not reachable from here · the board works by hand';
      const states = new Set(CH.map((r) => r.status));
      const okState = states.size === 1 && (states.has(LIVE) || states.has(DEAD));
      check('c18', okState, 'C18 the health line reads live, or reads the unreachable line',
        [...states].map((x) => '"' + x + '"').join(' / ') || '(no health line)');
    }
  }

  /* ---- C19 -------------------------------------------------------------- */
  /* Every figure on the right of these comparisons is derived in this file from
     the same JSON the browser is reading. None is written down. */
  {
    if (!TOOLS.present) {
      if (POISON && POISON !== 'c19') skip('C19 the analyst tools answer from the board', 'poison ' + POISON + ' does not drive them');
      else check('c19', false, 'C19 window.__app.analyst is published', 'the probe is not on the page');
    } else {
      const o = TOOLS.out, w = TOOLS.want;
      const head1 = (k) => ((o[k] || '').split('\n')[0] || '').slice(0, 120);
      /* a count printed by a tool: "NODES matching <em dash> 311 of 1,057" */
      const said = (key) => {
        const m = /\u2014\s*([0-9,]+)\s+of\s+([0-9,]+)/.exec(o[key] || '');
        return m ? Number(m[1].replace(/,/g, '')) : NaN;
      };

      check('c19', TOOLS.names.length === 12, 'C19 the page publishes all twelve tools',
        TOOLS.names.length + ' at version ' + TOOLS.version + ': ' + TOOLS.names.join(' '));

      const threw = Object.entries(o).filter(([, v]) => /^THREW: /.test(String(v))).map(([k, v]) => k + ' ' + v);
      check('c19', threw.length === 0, 'C19 no tool throws on a real call',
        threw.length ? clip(threw, 3) : Object.keys(o).length + ' calls over all twelve tools, none threw');

      const empty = Object.entries(o).filter(([, v]) => !String(v).trim()).map(([k]) => k);
      check('c19', empty.length === 0, 'C19 no tool answers with nothing',
        empty.length ? empty.join(', ') : 'every call returned text');

      const counts = [
        ['every node', 'all', w.all],
        ['people', 'people', w.people],
        ['claims', 'claims', w.claims],
        ['Tier 1 claims', 't1', w.t1],
        ['timeline events', 'tl', w.tl],
        ['events dated 2004', 'tl2004', w.tl2004],
        ['sourced edges', 'edges', w.edges],
        ['edges touching ' + NODE_FOCUS, 'edgesof', w.edgesof],
      ];
      const off = counts.filter(([, k, want]) => said(k) !== want)
        .map(([label, k, want]) => label + ': tool says ' + said(k) + ', the data has ' + want);
      check('c19', off.length === 0, 'C19 every count a tool prints re-derives from the data file',
        off.length ? off.length + ' of ' + counts.length + ' wrong \u2014 ' + clip(off, 3)
          : counts.map(([label, k]) => label + ' ' + said(k)).join(' \u00b7 '));

      /* grouping: every era's own total, read back out of the tool's table.
         A regex LITERAL, not a string-built RegExp: the string form lost its
         escapes on the way into this file and matched nothing. (This read the
         map's bands until the map retired in phase 11.) */
      const eraSaid = {};
      for (const row of String(o.byera || '').split(/\r?\n/)) {
        const m = /^\s+(\d+)\s\s(\S.*)$/.exec(row);
        if (m) eraSaid[m[2].trim()] = Number(m[1]);
      }
      const eraOff = Object.entries(w.eras).filter(([, n]) => n > 0)
        .filter(([id, n]) => eraSaid[id] !== n)
        .map(([id, n]) => id + ': tool says ' + eraSaid[id] + ', the index has ' + n);
      check('c19', eraOff.length === 0, "C19 group_by era totals are the index's own",
        eraOff.length ? clip(eraOff, 3)
          : Object.entries(eraSaid).map(([k, v]) => k + ' ' + v).join(' \u00b7 '));
      check('c19', /retired/.test(o.map || '') && /retired/.test(o.bandgone || ''),
        'C19 the map tool and the band filter say the program map is retired, rather than answer from nothing',
        head1('map') + ' :: ' + head1('bandgone'));

      check('c19', /\bPATH\b/.test(o.path1 || '') && /1 hop/.test(o.path1 || ''),
        'C19 path finds the one-hop chain the edge list carries',
        w.pairA + ' -> ' + w.pairB + ': ' + head1('path1'));
      check('c19', /does not join them/.test(o.path0 || ''),
        'C19 path says so rather than inventing one when the board joins nothing',
        w.pairA + ' -> ' + w.noJoin + ' at one hop: ' + head1('path0'));

      check('c19', (o.find || '').includes(NODE_FOCUS) && /FIND/.test(o.find || ''),
        'C19 find reaches a node the board carries', head1('find'));
      check('c19', (o.node || '').includes(focusRec.label),
        'C19 node returns the record, by its own label', head1('node'));
      check('c19', /no such node/.test(o.bogus || ''),
        'C19 node says so rather than inventing one for an id the board does not carry', head1('bogus'));

      const missThread = w.threadIds.filter((id) => !(o.threads || '').includes(id));
      check('c19', missThread.length === 0, 'C19 thread names every thread threads.json carries',
        missThread.length ? 'missing ' + missThread.join(', ') : w.threadIds.join(' '));
      const missPat = w.patentNums.filter((n) => !(o.patents || '').includes(n));
      check('c19', missPat.length === 0, 'C19 patent names every patent patents.json carries',
        missPat.length ? 'missing ' + missPat.join(', ') : w.patentNums.join(' \u00b7 '));
      check('c19', (o.foia || '').includes(w.foia + ' drafted requests'),
        'C19 foia reports the drafted requests foia.json carries',
        w.foia + ' expected :: ' + head1('foia'));
      check('c19', (o.overview || '').includes('nodes ' + w.all) && (o.overview || '').includes('timeline events ' + w.tl),
        "C19 overview reports the board's own counts",
        'nodes ' + w.all + ', timeline events ' + w.tl);

      /* the cited-id guard */
      const g = TOOLS.cite, gw = TOOLS.citeWant;
      if (!g || g.threw) {
        check('c19', false, 'C19 the cited-id guard runs', g ? 'threw ' + g.threw : 'not published on the probe');
      } else {
        check('c19', g.ok.length === 1 && g.ok[0] === gw.node,
          'C19 the guard passes the node id the board carries, and links it',
          'ok=[' + g.ok.join(', ') + '] wanted [' + gw.node + ']');
        check('c19', g.bad.length === 1 && g.bad[0] === 'ghost-node-not-on-the-board',
          'C19 the guard catches an id the board does not carry, and only that one',
          'bad=[' + g.bad.join(', ') + ']');
        const wolf = [gw.cell, gw.thread, 'program', 'www.govinfo.gov', 'archive.org']
          .filter((x) => g.bad.includes(x));
        check('c19', wolf.length === 0,
          'C19 the guard does not cry wolf over a cluster, a thread, a class or a hostname',
          wolf.length ? 'flagged ' + wolf.join(', ')
            : 'cell ' + gw.cell + ', thread ' + gw.thread + ', class program, and two hostnames: none flagged');
      }
    }
  }

  /* ---- C20 -------------------------------------------------------------- */
  {
    if (!SEARCH.present) {
      if (POISON && POISON !== 'c20') skip('C20 search ranks claim text', 'poison ' + POISON + ' does not drive it');
      else check('c20', false, 'C20 the search control draws results', 'no .searchbox input, or no query qualified');
    } else {
      const w = SEARCH.want;
      const sq = (x) => String(x || '').toLowerCase().replace(/[^a-z0-9]+/g, '');

      check('c20', SEARCH.claims.length > 0, 'C20 a query with ' + (w.t1 + w.other) + ' matching claims draws claim rows',
        SEARCH.claims.length + ' rows for "' + w.word + '" :: ' + clip(SEARCH.heads, 2));

      /* Every shown claim really contains what was typed. Checked on the
         punctuation-free form, because that is the form that lets "usc" reach
         "U.S.C."; a row that does not contain the query at all is the failure
         this is looking for. */
      const notThere = SEARCH.claims.filter((c) => !sq(c.hit).includes(sq(w.word)) && !sq(c.node).includes(sq(w.word)));
      check('c20', notThere.length === 0, 'C20 every claim row drawn actually contains the query',
        notThere.length ? notThere.length + ' do not \u2014 ' + clip(notThere.map((c) => c.node), 3)
          : SEARCH.claims.length + ' rows, all of them');

      /* THE RANKING. The board carries at least 14 Tier 1 claims whose text
         contains this word, and tier strictly dominates the score, so a ranked
         result of 12 is all Tier 1. A result in file order is not: the same
         word matches " + w.other + " weaker claims that sort early by node id. */
      const tiers = SEARCH.claims.map((c) => c.tier);
      const allT1 = tiers.every((t) => t === 1);
      check('c20', allT1, 'C20 the claim rows are ranked, so Tier 1 fills them before Tier 2 does',
        'tiers drawn [' + tiers.join(',') + ']: the board has ' + w.t1 + ' Tier 1 and '
        + w.other + ' weaker claims containing "' + w.word + '"');

      const marked = SEARCH.claims.filter((c) => c.marked).length;
      check('c20', marked === SEARCH.claims.length, 'C20 every claim row highlights the words it matched on',
        marked + ' of ' + SEARCH.claims.length + ' carry a <mark>');

      /* The two-word query. "wilson davis" must reach "The Wilson-Davis Notes",
         which a substring match on the raw label cannot do. */
      if (SEARCH.two && w.twoWord) {
        check('c20', SEARCH.two.nodes.includes(w.twoWordId),
          'C20 two words reach a hyphenated name: "' + w.twoWord + '" finds ' + w.twoWordId,
          SEARCH.two.nodes.length ? 'drew ' + clip(SEARCH.two.nodes, 3) : 'drew no node at all');
      } else {
        skip('C20 two words reach a hyphenated name', 'no hyphenated label in the index to derive one from');
      }
    }
  }

  /* ---- C21 -------------------------------------------------------------- */
  {
    if (!TR.present) {
      if (POISON && POISON !== 'c21') skip('C21 a thread report cites only what the board carries', 'poison ' + POISON + ' does not open one');
      else check('c21', false, 'C21 the thread report renders', 'no .report at #/report/t/custody');
    } else {
      check('c21', TR.steps === TR.thread.steps.length,
        'C21 the thread report draws every step the thread has',
        TR.steps + ' drawn, threads.json has ' + TR.thread.steps.length);

      /* Authored evidence is allowed and must SAY it is authored, so a reader
         can never read it as a document. Everything else must be a source the
         board carries on one of this thread's own joins. */
      /* ANCHORED AT BOTH ENDS. Anchored only at the start, this pattern let
         anything be appended to an authored citation and still pass, and the
         c21 poison walked straight through the first version of this check. */
      const AUTHORED = /^Thread (narrative|evidence), authored \u00b7 research\/threads\.json \u00b7 thread [a-z0-9-]+(, step \d+)?$/;
      const NOSOURCE = /^No source string is recorded on this edge$/;
      const invented = TR.cites.filter((c) => {
        if (AUTHORED.test(c.text) || NOSOURCE.test(c.text)) return false;
        if (c.url && TR.allowed.has(c.url)) return false;
        return !TR.allowed.has(c.text);
      });
      check('c21', invented.length === 0,
        'C21 every citation is the authored thread file or a source the board carries on that join',
        invented.length
          ? invented.length + ' of ' + TR.cites.length + ' is on neither list \u2014 ' + clip(invented.map((c) => c.text.slice(0, 70)), 2)
          : TR.cites.length + ' citations, ' + TR.allowed.size + ' edge sources on this thread to draw from');

      const authored = TR.cites.filter((c) => AUTHORED.test(c.text)).length;
      check('c21', authored >= TR.thread.steps.length,
        'C21 every step\u2019s authored evidence is cited as authored, never as a document',
        authored + ' authored citations for ' + TR.thread.steps.length + ' steps');

      const linked = TR.cites.filter((c) => c.url).length;
      check('c21', linked > 0 && TR.sups.length >= TR.thread.steps.length,
        'C21 the body carries numbered superscripts and the citations carry links',
        TR.sups.length + ' superscripts, ' + linked + ' of ' + TR.cites.length + ' citations linked');
    }
  }

  /* ---- verdict ---------------------------------------------------------- */
  console.log('');
  if (POISON) {
    /* a poison is seen by the check it names (`check`), or by its own id */
    const CID = POISONS[POISON].check || POISON;
    const seen = (failsByCheck.get(CID) || 0) > 0;
    const line = (seen ? 'ok    ' : 'FAIL  ') + `POISON=${POISON} the ${CID.toUpperCase()} check sees the poisoned page`
      + ' :: ' + POISONS[POISON].what + ' → '
      + (seen ? `${failsByCheck.get(CID)} of its assertions failed` : 'every assertion still passed, so the check is blind');
    console.log('  ' + line);
    const others = [...failsByCheck.keys()].filter((k) => k !== CID);
    if (others.length) console.log('  note  other checks also failing on this build: ' + others.join(', '));
    console.log('\n' + (seen ? `POISON ${POISON} SEEN` : `POISON ${POISON} NOT SEEN`));
    process.exit(seen ? 0 : 1);
  }
  console.log(`  ${nOk} passed, ${nFail} failed`);
  console.log('\n' + (nFail ? `APP CHECKS FAILED (${nFail}): ` + [...failsByCheck.keys()].join(', ')
    : 'APP CHECKS PASSED'));
  process.exit(nFail ? 1 : 0);
}

/* ---- --all-poisons: every poison in turn, each must fail its own check --- */
function allPoisons() {
  /* --shard k/n runs the poisons whose index i satisfies i % n === k - 1, so n
     parallel CI jobs cover every poison exactly once between them. Without it,
     every poison runs. */
  const all = Object.keys(POISONS);
  const si = process.argv.indexOf('--shard');
  let names = all, shard = '';
  if (si >= 0) {
    const m = /^(\d+)\/(\d+)$/.exec(process.argv[si + 1] || '');
    const k = m ? Number(m[1]) : 0, n = m ? Number(m[2]) : 0;
    if (!m || n < 1 || k < 1 || k > n) {
      console.error('--shard wants k/n with 1 <= k <= n, got ' + (process.argv[si + 1] || 'nothing'));
      process.exit(2);
    }
    names = all.filter((_, i) => i % n === k - 1);
    shard = ` in shard ${k}/${n}`;
    if (!names.length) {
      console.error(`shard ${k}/${n} holds no poisons (there are ${all.length})`);
      process.exit(2);
    }
  }
  const bad = [];
  for (const n of names) {
    const r = spawnSync(process.execPath, [SELF], {
      env: { ...process.env, POISON: n }, encoding: 'utf8',
    });
    const out = (r.stdout || '') + (r.stderr || '');
    const line = out.split('\n').filter((l) => /POISON=/.test(l)).pop();
    if (line) console.log(line.trim());
    else {
      /* a run that died before its verdict: say why, rather than only that it did */
      const tail = out.trim().split('\n').slice(-4).map((l) => '      ' + l.trim()).join('\n');
      console.log(`POISON=${n} no verdict line (exit ${r.status}${r.signal ? ', ' + r.signal : ''})` +
        (r.error ? ': ' + r.error.message : '') + (tail ? '\n' + tail : ''));
    }
    if (r.status !== 0) bad.push(n);
  }
  console.log('\n' + (bad.length
    ? `POISON SWEEP FAILED (${bad.length} of ${names.length}${shard} blind): ` + bad.join(', ')
    : `POISON SWEEP PASSED, all ${names.length} poisons${shard} were seen by their own check`));
  process.exit(bad.length ? 1 : 0);
}

if (process.argv.includes('--all-poisons')) allPoisons();
else main().catch((e) => { console.error('HARNESS ERROR', e.stack || e.message); process.exit(2); });
