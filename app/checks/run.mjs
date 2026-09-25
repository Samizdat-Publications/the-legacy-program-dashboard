/* app/checks/run.mjs: C1 to C16 of notes/DESIGN-RESPONSE-SHELL-2026-09-02.md
 * section 3, plus C17 for the back button Stewart made a condition of the new
 * shell and C18 for the analyst dock and its per-route chips, C19 to C21 for the
 * analyst's tools, search ranking and the thread report, and C22 to C26 for
 * redesign phase 1 (notes/PLAN-2026-09-24.md): grouped connections with their
 * sentences, every authored field, search over events and threads, the
 * node-level denial flag, and a node page at phone width. All against the built
 * app served by `npm run preview`.
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
 * Note on `window.__app.*`: the map, hood and timeline publish probes, and this
 * file deliberately does NOT use the ones that report layout intentions
 * (map.cells() returns the layout's own counts). Where a figure matters it is
 * re-read from the DOM: cell heads are read as text, boxes as
 * getBoundingClientRect. The one thing taken from the renderer is
 * `.map-grid[data-mode]`, which is an attribute on the rendered element and is
 * cross-checked against an independent re-derivation of the label rule (C5).
 */
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const APP = (process.env.APP_URL || 'http://127.0.0.1:4173').replace(/\/+$/, '') + '/';
const POISON = (process.env.POISON || '').trim().toLowerCase();
const SELF = fileURLToPath(import.meta.url);

const NODE_FOCUS = 'aawsap';       /* start-here 1, the richest record on the board */
const PERSON_FOCUS = 'david-grusch'; /* the richest person record: unverified, chronology, affiliations */
const PATENT = '10144532';

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
    return {
      text: document.body.innerText,
      hrefs: Array.prototype.map.call(document.querySelectorAll('a[href]'), (a) => a.getAttribute('href')),
      notfound: !!(h2 && /No such route/.test(h2.textContent || '')),
      title: document.title,
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
      out.push({
        text: el.textContent || '',
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

  /* The map, entirely off the rendered DOM. */
  map() {
    const grid = document.querySelector('.map-grid');
    const stat = document.querySelector('.map-stat');
    const legend = document.querySelector('.map-legend');
    const chips = Array.prototype.map.call(document.querySelectorAll('a.chip'), (c) => {
      const r = c.getBoundingClientRect();
      const lab = c.querySelector('.clabel');
      const lr = lab ? lab.getBoundingClientRect() : null;
      const hl = c.querySelector('.chl');
      return {
        id: c.getAttribute('data-id'), href: c.getAttribute('href'),
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
        label: lab ? lab.textContent : null, labW: lr ? lr.width : 0,
        labIn: lr ? (lr.left >= r.left - 0.5 && lr.right <= r.right + 0.5) : false,
        hl: hl ? hl.textContent : null, isHl: c.classList.contains('hl'),
      };
    });
    const cells = Array.prototype.map.call(document.querySelectorAll('.cell[data-cell]'), (c) => {
      const r = c.getBoundingClientRect();
      const head = c.querySelector('.cell-head span');
      return {
        key: c.getAttribute('data-cell'), head: head ? head.textContent : null,
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
      };
    });
    const plus = Array.prototype.map.call(document.querySelectorAll('.plus'), (p) => {
      const r = p.getBoundingClientRect();
      return { text: p.textContent, x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
    });
    return {
      mode: grid ? grid.getAttribute('data-mode') : null,
      stat: stat ? stat.textContent : '', reason: stat ? stat.getAttribute('title') : '',
      legendTop: legend ? legend.getBoundingClientRect().top + scrollY : null,
      vh: window.innerHeight, vw: window.innerWidth,
      chips, cells, plus,
    };
  },

  /* The label rule of Design 2.2, re-derived here from the rendered font and
     the viewport -- deliberately NOT from the renderer's layout object. */
  rederive(nodes, cellsMap, bands, eras) {
    const BAR = 40, STRIP = 30, HEAD = 42, LEGEND = 26, GUTTER = 152, PAD_R = 12;
    const CHIP_GAP = 6, CELL_PAD = 6, EXTRA = 30, HL = 16;
    const meas = document.createElement('span');
    meas.style.cssText = 'position:absolute;visibility:hidden;top:-9999px;left:0;white-space:pre';
    meas.style.font = '';
    const probe = document.querySelector('.clabel') || document.querySelector('.hood-label');
    const cs = probe ? getComputedStyle(probe) : null;
    meas.style.fontFamily = cs ? cs.fontFamily : "'IBM Plex Mono', monospace";
    meas.style.fontSize = cs ? cs.fontSize : '11px';
    meas.style.fontWeight = cs ? cs.fontWeight : '400';
    meas.style.letterSpacing = cs ? cs.letterSpacing : 'normal';
    document.body.appendChild(meas);
    const W = (s) => { meas.textContent = s; return meas.getBoundingClientRect().width; };

    const byId = new Map(nodes.map((n) => [n.id, n]));
    const colW = Math.floor((window.innerWidth - GUTTER - PAD_R) / 5);
    const inner = colW - CELL_PAD * 2;
    const availH = window.innerHeight - BAR - (STRIP + HEAD) - LEGEND - 4;

    let tooWide = 0; const wideIds = [];
    let totalRows = 0;
    for (const b of bands) {
      let mx = 1;
      for (const e of eras) {
        const ids = cellsMap[b + '.' + e] || [];
        let rows = 0, used = 0;
        for (const id of ids) {
          const n = byId.get(id); if (!n) continue;
          const w = Math.ceil(W(n.short)) + EXTRA + (n.hl ? HL : 0);
          if (w > inner) { tooWide++; if (wideIds.length < 4) wideIds.push(n.short); continue; }
          if (rows === 0) { rows = 1; used = w; continue; }
          if (used + CHIP_GAP + w > inner) { rows++; used = w; } else { used += CHIP_GAP + w; }
        }
        if (rows > mx) mx = rows;
      }
      totalRows += mx;
    }
    meas.remove();
    const minNeed = totalRows * 17 + 6 * (bands.length - 1);  /* pitch floor 17 since 25 Sept 2026 */
    return {
      tooWide, wideIds, totalRows, minNeed, availH, colW,
      fits: tooWide === 0 && minNeed <= availH,
    };
  },

  /* The node page's claims and denials. */
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
        type: g.getAttribute('data-type') || '',
        head: txt(g.querySelector('.conn-ghead .eyebrow')),
        rows: Array.prototype.map.call(g.querySelectorAll('.conn'), (r) => ({
          id: r.getAttribute('data-id') || '',
          lines: Array.prototype.map.call(r.querySelectorAll('.conn-line .conn-text'), txt),
          metas: Array.prototype.map.call(r.querySelectorAll('.conn-line .cmeta'), txt),
        })),
      })),
    };
  },

  /* The same, on the printable node report. */
  rconns() {
    return Array.prototype.map.call(document.querySelectorAll('.rconns .rconn'), (r) => ({
      id: r.getAttribute('data-id') || '',
      type: r.getAttribute('data-type') || '',
      sent: ((r.querySelector('.rsent') || {}).textContent || '').trim(),
      text: r.textContent || '',
    }));
  },

  /* How many of each authored field a node page draws, and its crumb. */
  fields() {
    const n = (sel) => document.querySelectorAll(sel).length;
    return {
      oq: n('.node .oq'), unv: n('.node .unv'), chron: n('.node .chron .ev'),
      aff: n('.node .affs .aff'), nsrc: n('.node .nsrcs .nsrc'),
      crumb: ((document.querySelector('.node .crumb-l') || {}).textContent || ''),
      /* the three axis bars, as the boxes the browser laid out: three cells side
         by side, never stacked on one another */
      axes: Array.prototype.map.call(document.querySelectorAll('.node .axis .cells'), (c) =>
        Array.prototype.map.call(c.children, (x) => { const b = x.getBoundingClientRect(); return [b.left, b.right]; })),
    };
  },

  /* Neighbourhood ring entries, from the DOM. */
  hood() {
    return Array.prototype.map.call(document.querySelectorAll('a.hood-n'), (a) => {
      const r = a.getBoundingClientRect();
      const m = a.querySelector('.mark');
      const mr = m ? m.getBoundingClientRect() : null;
      const lab = a.querySelector('.hood-label');
      return {
        id: (a.getAttribute('href') || '').slice(4),
        hop: (a.className.match(/hop(\d)/) || [0, '?'])[1],
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
        mw: mr ? Math.round(mr.width) : 0, mh: mr ? Math.round(mr.height) : 0,
        label: lab ? lab.textContent : null,
      };
    });
  },

  /* Timeline, from the rendered items and the rendered lane boxes. */
  timeline() {
    const packs = Array.prototype.map.call(document.querySelectorAll('.tl-pack'), (p) => {
      const r = p.getBoundingClientRect();
      return {
        strand: p.getAttribute('data-strand'), era: p.getAttribute('data-era'),
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
      };
    });
    const items = Array.prototype.map.call(document.querySelectorAll('[data-tl-item]'), (el) => {
      const r = el.getBoundingClientRect();
      return {
        id: el.getAttribute('data-id'), kind: el.getAttribute('data-kind'),
        era: el.getAttribute('data-era'), strand: el.getAttribute('data-strand'),
        x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
      };
    });
    const open = document.querySelector('.tl-era.open');
    return {
      packs, items,
      openEraSub: open ? (open.querySelector('.tl-era-sub') || {}).textContent || '' : '',
    };
  },

  /* Home's start-here register, in the order it is drawn. */
  starthere() {
    return Array.prototype.map.call(document.querySelectorAll('.starthere .chips a.chip'), (a) => ({
      id: (a.getAttribute('href') || '').slice(4),
      n: (a.querySelector('.chip-n') || {}).textContent || '',
      label: (a.querySelector('.label') || {}).textContent || '',
    }));
  },

  /* Thread chain, in the order it is drawn. */
  thread() {
    return {
      steps: Array.prototype.map.call(document.querySelectorAll('.th-step'), (s) => s.getAttribute('data-node')),
      chips: Array.prototype.map.call(document.querySelectorAll('.tm-chip'), (c) => {
        const r = c.getBoundingClientRect();
        return {
          id: c.getAttribute('data-node'), step: c.getAttribute('data-step'),
          x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
        };
      }),
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
    stops: ['home', 'map', 'hood0', 'thread:custody', 'timeline', 'patents', 'evidence', 'report'],
    what: 'rewrites the first #/n/ href on every page to an id the board does not carry',
    fn: async (page) => page.evaluate(() => {
      const a = document.querySelector('a[href^="#/n/"]');
      if (a) a.setAttribute('href', '#/n/ghost-node-not-on-the-board');
    }),
  },
  c2: {
    stops: ['map'],
    what: 'truncates one real chip label: 9px, clipped to 24px, with an ellipsis',
    fn: async (page) => page.evaluate(() => {
      const l = document.querySelectorAll('a.chip .clabel')[3];
      if (!l) return;
      l.style.fontSize = '9px';
      l.style.display = 'inline-block';
      l.style.maxWidth = '24px';
      l.style.overflow = 'hidden';
      l.style.textOverflow = 'ellipsis';
      l.textContent = l.textContent.slice(0, 6) + '…';
    }),
  },
  c3: {
    stops: ['map'],
    what: 'empties one chip label, leaving its class mark drawn: an anonymous dot',
    fn: async (page) => page.evaluate(() => {
      const l = document.querySelectorAll('a.chip .clabel')[7];
      if (l) l.textContent = '';
    }),
  },
  c4: {
    stops: ['map'],
    what: 'moves one real chip onto another chip, so two labels share a box',
    fn: async (page) => page.evaluate(() => {
      const cs = document.querySelectorAll('a.chip');
      if (cs.length < 12) return;
      /* the chips are absolutely positioned in the grid, so copying one's
         left/top onto another puts two real labels in one box */
      cs[11].style.left = cs[10].style.left;
      cs[11].style.top = cs[10].style.top;
    }),
  },
  c5: {
    stops: ['map'],
    what: 'turns the CELLS control on at 1920, where every label fits',
    fn: async (page) => {
      const b = page.locator('button.ctl', { hasText: 'CELLS' }).first();
      await b.click();
      await page.waitForTimeout(700);
    },
  },
  c6: {
    stops: ['map1366'],
    what: 'rewrites one cell head so its printed count is not its membership',
    fn: async (page) => page.evaluate(() => {
      const s = document.querySelector('.cell .cell-head span');
      if (s) s.textContent = '99 nodes';
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
  c10: {
    stops: ['hood0'],
    what: 'draws a node on the start-here ring that the owner did not flag',
    fn: async (page) => page.evaluate(() => {
      const one = document.querySelector('a.hood-n');
      if (!one) return;
      const c = one.cloneNode(true);
      c.setAttribute('href', '#/n/lockheed-martin');
      one.parentElement.appendChild(c);
    }),
  },
  c11: {
    stops: ['home'],
    what: 'swaps two numbers in the start-here register',
    fn: async (page) => page.evaluate(() => {
      const ns = document.querySelectorAll('.starthere .chips a.chip .chip-n');
      if (ns.length < 3) return;
      const t = ns[1].textContent; ns[1].textContent = ns[2].textContent; ns[2].textContent = t;
    }),
  },
  c12: {
    stops: ['map'],
    what: 'grows every chip by its own degree, so size encodes connectedness',
    fn: async (page, ctx) => page.evaluate((deg) => {
      for (const c of document.querySelectorAll('a.chip')) {
        const d = deg[c.getAttribute('data-id')] || 0;
        c.style.height = (16 + Math.min(10, Math.round(d / 6))) + 'px';
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
    what: 'moves one event chip into another strand lane',
    fn: async (page) => page.evaluate(() => {
      const packs = document.querySelectorAll('.tl-pack');
      if (packs.length < 2) return;
      const chip = packs[0].querySelector('.tl-chip');
      if (chip) packs[1].appendChild(chip);
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
    stops: ['map'],
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
    what: 'redraws one connection the old way: its sentence gone, its relationship replaced by "member"',
    fn: async (page) => page.evaluate(() => {
      const t = document.querySelector('.node-side .conn-line .conn-text');
      if (t) t.textContent = '';
      const m = document.querySelector('.node-side .conn-line .cmeta');
      if (m) m.textContent = 'member · T1';
      const r = document.querySelector('.rconns .rconn .rsent');
      if (r) r.textContent = 'member';
    }),
  },
  c23: {
    stops: ['person'],
    what: 'hides one of the unverified notes on the person page, and stacks its axis cells as the map\'s .cell rule once did',
    fn: async (page) => page.evaluate(() => {
      const u = document.querySelectorAll('.node .unv');
      if (u.length) u[u.length - 1].remove();
      for (const c of document.querySelectorAll('.node .axis .acell')) c.style.position = 'absolute';
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
    stops: ['phone'],
    what: 'puts the desktop two-column grid back at phone width',
    fn: async (page) => page.evaluate(() => {
      const n = document.querySelector('.node');
      if (n) n.style.gridTemplateColumns = 'minmax(0, 1fr) 520px';
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
  const jget = async (p) => {
    const r = await fetch(APP + p);
    if (!r.ok) throw new Error(p + ' -> HTTP ' + r.status);
    return r.json();
  };
  let index, mapData, edges, threadsFile, highlights, tlEvents, focusRec, patentsFile, analystFile,
      claimRows, foiaFile, personRec;
  try {
    [index, mapData, edges, threadsFile, highlights, tlEvents, focusRec, patentsFile, analystFile,
     claimRows, foiaFile, personRec] =
      await Promise.all([
        jget('data/index.json'), jget('data/map.json'), jget('data/edges.json'),
        jget('data/threads.json'), jget('data/highlights.json'), jget('data/timeline.json'),
        jget('data/nodes/' + NODE_FOCUS + '.json'), jget('data/patents.json'), jget('data/analyst.json'),
        jget('data/claims.json'), jget('data/foia.json'), jget('data/nodes/' + PERSON_FOCUS + '.json'),
      ]);
  } catch (e) {
    console.error('HARNESS: the app is not being served at ' + APP + ' (' + e.message + ').');
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
    if ((mapData.summarised || []).some((s) => (s.a === a && s.b === b) || (s.a === b && s.b === a))) return 'derived';
    for (const x of adj.get(a) || []) if ((adj.get(b) || new Set()).has(x)) return 'derived';
    return null;
  };
  /* a node with no join at all to the last custody step, for the c7 poison */
  const custody = threads.find((t) => t.id === 'custody');
  const lastStep = custody ? custody.steps[custody.steps.length - 1].node : null;
  const unjoined = index.nodes.map((n) => n.id)
    .find((id) => id !== lastStep && !joined(lastStep, id)) || 'no-such-node';

  const ctx = { deg, unjoined };

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
    if (POISONS[POISON] && POISONS[POISON].stops.includes(id)) await POISONS[POISON].fn(p, ctx);
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

  await stop('node', '#/n/' + NODE_FOCUS, 1200);
  S.node.node = await ev(IN_PAGE.node);
  S.node.conns = await ev(IN_PAGE.conns);
  S.node.fields = await ev(IN_PAGE.fields);

  await stop('person', '#/n/' + PERSON_FOCUS, 1200);
  S.person.fields = await ev(IN_PAGE.fields);

  await stop('map', '#/map', 2400);
  S.map.map = await ev(IN_PAGE.map);
  S.map.labels = await ev(IN_PAGE.labels, 'a.chip .clabel', 'a.chip');
  S.map.rederive = await ev(IN_PAGE.rederive, mapData.nodes, mapData.cells,
    mapData.bands.map((b) => b.id), mapData.eras.map((e) => e.id));

  await stop('hood0', '#/hood', 2000);
  S.hood0.hood = await ev(IN_PAGE.hood);

  await stop('hood3', '#/hood/' + NODE_FOCUS, 2200, async (p) => {
    const b = p.locator('button.hood-b', { hasText: '3 HOPS' }).first();
    if (await b.count()) { await b.click(); await p.waitForTimeout(2200); }
  });
  S.hood3.hood = await ev(IN_PAGE.hood);
  S.hood3.labels = await ev(IN_PAGE.labels, '.hood-label', 'a.hood-n');

  /* A poison run only has to prove its own check fails, so it walks the shortest
     itinerary that still reaches that check. C7 needs all eight threads, and C17
     asks after every screen the itinerary reaches, so both walk the whole thing. */
  const walkAll = !POISON || POISON === 'c7' || POISON === 'c17';
  for (const t of (walkAll ? threads : threads.filter((x) => x.id === 'custody'))) {
    const id = 'thread:' + t.id;
    await stop(id, '#/t/' + t.id, 1400);
    S[id].thread = await ev(IN_PAGE.thread);
  }

  await stop('timeline', '#/timeline', 2400);
  S.timeline.timeline = await ev(IN_PAGE.timeline);

  await stop('patents', '#/patents/' + PATENT, 2000);
  await stop('evidence', '#/evidence', 3200);
  S.evidence.den = await page.evaluate(() =>
    Array.from(document.querySelectorAll('td.c-den')).map((td) => (td.textContent || '').trim()));
  await stop('report', '#/report/n/' + NODE_FOCUS, 1600);
  S.report.rconns = await ev(IN_PAGE.rconns);

  /* the map again, at the width Design says is below the label floor */
  await page.setViewportSize({ width: 1366, height: 768 });
  current = null;
  await stop('map1366', '#/map', 2600);
  S.map1366.map = await ev(IN_PAGE.map);
  S.map1366.rederive = await ev(IN_PAGE.rederive, mapData.nodes, mapData.cells,
    mapData.bands.map((b) => b.id), mapData.eras.map((e) => e.id));

  /* a node page at phone width */
  await page.setViewportSize({ width: 375, height: 812 });
  current = null;
  await stop('phone', '#/n/' + NODE_FOCUS, 1600);
  S.phone.phone = await page.evaluate(() => {
    const m = document.querySelector('.node-main');
    return {
      mainW: m ? m.getBoundingClientRect().width : 0,
      scrollW: document.documentElement.scrollWidth,
      vw: window.innerWidth,
    };
  });
  await page.setViewportSize({ width: 1920, height: 1080 });

  /* ---- C9's route sweep ------------------------------------------------- */
  const ROUTES = [
    '#/', '#/n/' + NODE_FOCUS, '#/n/' + NODE_FOCUS + '/map', '#/n/' + NODE_FOCUS + '/hood',
    '#/hood/' + NODE_FOCUS, '#/hood', '#/map', '#/map?cell=oversight.2017-2026',
    '#/t/custody', '#/t/custody/map', '#/timeline', '#/timeline?era=3',
    '#/timeline?scope=n:' + NODE_FOCUS, '#/timeline?scope=t:custody',
    '#/patents/' + PATENT, '#/patents/' + PATENT + '?sheet=2',
    '#/evidence?tier=1&cls=person&cluster=other&denied=1&open=1',
    '#/report/n/' + NODE_FOCUS, '#/report/t/custody',
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
    ['map', '#/map'],
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
      }, null, { timeout: 10000 }).catch(() => {});
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

    const driveSearch = !POISON || POISON === 'c20' || POISON === 'c24';
    if (driveSearch && word) {
      const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
      p.on('request', (r) => requests.push(r.url()));
      p.on('pageerror', (e) => pageErrors.push(e.message.slice(0, 160)));
      await p.goto(APP + '#/', { waitUntil: 'load' });
      await p.waitForTimeout(1600);
      const type = async (q) => {
        await p.locator('.searchbox input').first().fill(q);
        await p.waitForTimeout(1600);          /* claims.json loads on the first query */
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
      await p.close();
    }
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
      ['onmap', 'nodes', { on_map: true, count_only: true }],
      ['byband', 'nodes', { on_map: true, group_by: 'band' }],
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
      /* The guard, on the same page: a real node id, a real map cell, a real
         thread, a plain word in backticks that is not an id at all, and one
         fabricated id that must be caught. The cell is here because the first
         live question cited `disclosure.3` and the guard called it "not a node
         on this board", which was true and useless. */
      const cellId = Object.keys(mapData.cells || {})[0] || 'custody.0';
      TOOLS.cite = await p.evaluate(IN_PAGE.cite,
        'The node `' + NODE_FOCUS + '` sits in cell `' + cellId + '` on the '
        + '`' + (threads[0] || { id: 'custody' }).id + '` thread, a `program`, '
        + 'sourced to `www.govinfo.gov` and `archive.org`, '
        + 'unlike `ghost-node-not-on-the-board`.');
      TOOLS.citeWant = { node: NODE_FOCUS, cell: cellId, thread: (threads[0] || { id: 'custody' }).id };
      TOOLS.want = {
        all: index.nodes.length,
        people: index.nodes.filter((n) => n.cls === 'person').length,
        onmap: index.nodes.filter((n) => n.l0).length,
        claims: claimRows.length,
        t1: claimRows.filter((c) => c.tier === 1).length,
        tl: tlEvents.length,
        tl2004: tlEvents.filter((e) => e.date.slice(0, 4) === '2004').length,
        edges: edges.length,
        edgesof: edges.filter((e) => e.a === NODE_FOCUS || e.b === NODE_FOCUS).length,
        bands: Object.fromEntries(index.bands.map((b) => [b.id, index.nodes.filter((n) => n.l0 && n.band === b.id).length])),
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
      await p.locator('.starthere .chips a.chip[href="#/n/' + NODE_FOCUS + '"]').first().click();
      out.push(await rest(p, 1400));
      await p.locator('a[href="#/n/' + NODE_FOCUS + '/map"]').first().click();
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

  const C1_PAGES = ['home', 'map', 'hood0', 'thread:custody', 'timeline', 'patents', 'evidence', 'report'];
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
    const all = [...S.map.labels.map((l) => ({ ...l, where: 'map' })),
                 ...S.hood3.labels.map((l) => ({ ...l, where: 'hood' }))];
    const sizes = [...new Set(all.map((l) => l.fs))];
    check('c2', sizes.length === 1, 'C2  one label size on the map and the neighbourhood',
      `${all.length} labels at ${sizes.join(', ')}`);
    const ell = all.filter((l) => l.to === 'ellipsis' || /[…]|\.\.\.$/.test(l.text));
    check('c2', ell.length === 0, 'C2  no text-overflow and no ellipsis character in any label',
      ell.length ? clip(ell.map((l) => l.where + ':' + l.text)) : `${all.length} labels clean`);
    const narrow = all.filter((l) => l.w + 0.5 < l.nat);
    check('c2', narrow.length === 0, 'C2  no label box narrower than its own text at its own font',
      narrow.length ? clip(narrow.map((l) => `${l.text} ${l.w.toFixed(0)}<${l.nat.toFixed(0)}`))
        : `${all.length} labels measured against their natural width`);
    const clipped = S.map.map.chips.filter((c) => c.label && !c.labIn);
    check('c2', clipped.length === 0, 'C2  every chip label sits inside its own chip',
      clipped.length ? clip(clipped.map((c) => c.id)) : `${S.map.map.chips.length} chips`);
  }

  /* ---- C3 --------------------------------------------------------------- */
  {
    const short = new Map(mapData.nodes.map((n) => [n.id, n.short]));
    const anon = S.map.map.chips.filter((c) => !c.label || !c.label.trim() || c.labW <= 0);
    check('c3', anon.length === 0, 'C3  no chip is drawn on the map without a rendered label',
      anon.length ? clip(anon.map((c) => c.id || '(no id)')) : `${S.map.map.chips.length} chips, all named`);
    const wrong = S.map.map.chips.filter((c) => c.label && short.has(c.id) && c.label !== short.get(c.id));
    check('c3', wrong.length === 0, 'C3  every chip label is the board\'s own short label for that node',
      wrong.length ? clip(wrong.map((c) => c.id)) : 'matched against map.json');
    const ringAnon = S.hood3.hood.filter((e) => !e.label || !e.label.trim());
    check('c3', ringAnon.length === 0, 'C3  no ring entry is drawn without a rendered label',
      ringAnon.length ? clip(ringAnon.map((e) => e.id)) : `${S.hood3.hood.length} ring entries, all named`);
  }

  /* ---- C4 --------------------------------------------------------------- */
  {
    const cases = [
      ['map, label mode 1920', S.map.map.chips.map((c) => ({ id: c.id, x: c.x, y: c.y, w: c.w, h: c.h }))],
      ['map, cell mode 1366', S.map1366.map.chips.map((c) => ({ id: c.id, x: c.x, y: c.y, w: c.w, h: c.h }))],
      ['neighbourhood ring', S.hood3.hood],
      ['timeline chips', S.timeline.timeline.items.filter((i) => i.kind === 'chip')],
      ['thread small map', S['thread:custody'].thread.chips],
    ];
    for (const [name, boxes] of cases) {
      const bad = pairsOverlapping(boxes);
      check('c4', bad.length === 0, 'C4  no two label boxes intersect · ' + name,
        bad.length ? `${bad.length}+ overlapping pairs: ` + clip(bad, 3) : `${boxes.length} boxes, none intersecting`);
    }
  }

  /* ---- C5 --------------------------------------------------------------- */
  {
    for (const [w, id] of [[1920, 'map'], [1366, 'map1366']]) {
      const m = S[id].map, d = S[id].rederive;
      const want = d.fits ? 'label' : 'cell';
      check('c5', m.mode === want, `C5  map mode at ${w} is the one the label rule allows`,
        `mode ${m.mode}, re-derived ${want} (${d.tooWide} labels wider than a ${d.colW}px column, ` +
        `${d.totalRows} rows need ${d.minNeed}px of ${d.availH}px)`);
      if (m.mode === 'label') {
        const bottom = Math.max(...m.chips.map((c) => c.y + c.h));
        check('c5', bottom <= m.legendTop + 0.5, `C5  label mode at ${w} fits the viewport height`,
          `lowest chip ends at ${bottom.toFixed(0)}, legend starts at ${(m.legendTop || 0).toFixed(0)}, viewport ${m.vh}`);
      }
    }
  }

  /* ---- C6 --------------------------------------------------------------- */
  {
    const m = S.map1366.map;
    const inside = (b, cell) => {
      const cx = b.x + b.w / 2, cy = b.y + b.h / 2;
      return cx >= cell.x && cx <= cell.x + cell.w && cy >= cell.y && cy <= cell.y + cell.h;
    };
    const badCount = [], badPlus = [];
    let checked = 0;
    for (const cell of m.cells) {
      const members = (mapData.cells[cell.key] || []).length;
      if (cell.head !== null) {
        checked++;
        const printed = Number((cell.head.match(/(\d+)/) || [])[1]);
        if (printed !== members) badCount.push(`${cell.key} shows ${printed}, holds ${members}`);
      }
      const shown = m.chips.filter((c) => inside(c, cell)).length;
      const pl = m.plus.filter((p) => inside(p, cell));
      const printedPlus = pl.length ? Number((pl[0].text.match(/(\d+)/) || [])[1]) : 0;
      if (printedPlus !== members - shown) {
        badPlus.push(`${cell.key} +${printedPlus} but ${members}-${shown}=${members - shown}`);
      }
    }
    check('c6', badCount.length === 0 && checked > 0,
      'C6  every cell head prints its own membership from map.json',
      badCount.length ? clip(badCount, 3) : `${checked} cell heads at 1366`);
    check('c6', badPlus.length === 0, 'C6  every +N equals members minus names drawn',
      badPlus.length ? clip(badPlus, 3) : `${m.cells.length} cells, ${m.plus.length} +N chips, ${m.chips.length} names`);
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
    const m = n.head.match(/Claims\s*·?\s*(\d+)[\s\S]*Tier 1 · (\d+)[\s\S]*Tier 2 · (\d+)[\s\S]*Tier 3 · (\d+)/);
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
      }
    }
    check('c9', offScheme.length === 0, 'C9  every rendered in-app href is a route in the 2.1 scheme',
      offScheme.length ? clip(offScheme, 4) : `${seen.size} distinct hrefs over ${Object.keys(S).length} screens`);
    check('c9', deadIds.length === 0, 'C9  every rendered #/t/ and #/patents/ link names something the board carries',
      deadIds.length ? `${deadIds.length} dead: ` + clip(deadIds, 5) : 'all resolve to a thread or a patent');
  }

  /* ---- C10 -------------------------------------------------------------- */
  {
    const drawn = S.hood0.hood.map((e) => e.id);
    const want = flags.map((f) => f.id);
    const extra = drawn.filter((d) => !want.includes(d));
    const missing = want.filter((w) => !drawn.includes(w));
    check('c10', extra.length === 0 && missing.length === 0 && drawn.length === want.length,
      'C10 #/hood draws exactly the ' + want.length + ' start-here nodes and nothing else',
      extra.length || missing.length ? `extra ${clip(extra, 3)} · missing ${clip(missing, 3)}`
        : `${drawn.length} entries, set-equal to highlights.json`);

    let f = new Set([NODE_FOCUS]);
    const allowed = new Set([NODE_FOCUS]);
    for (let hop = 1; hop <= 3; hop++) {
      const next = new Set();
      for (const a of f) for (const b of adj.get(a) || []) if (!allowed.has(b)) { allowed.add(b); next.add(b); }
      f = next;
    }
    for (const s of mapData.summarised || []) {
      if (s.a === NODE_FOCUS) allowed.add(s.b);
      if (s.b === NODE_FOCUS) allowed.add(s.a);
    }
    const over = S.hood3.hood.map((e) => e.id).filter((id) => !allowed.has(id));
    check('c10', over.length === 0,
      'C10 the 3-hop neighbourhood never leaves the hop 1∪2∪3 sets of edges.json',
      over.length ? `${over.length} outside: ` + clip(over, 4)
        : `${S.hood3.hood.length} drawn, all inside a set of ${allowed.size}`);
  }

  /* ---- C11 -------------------------------------------------------------- */
  {
    const home = S.home.starthere || [];
    const wantIds = flags.map((f) => f.id).join('|');
    check('c11', home.map((c) => c.id).join('|') === wantIds,
      'C11 Home\'s start-here register is highlights.json, in rank order',
      `${home.length} chips: ` + (home.map((c) => c.id).join('|') === wantIds ? 'order matches'
        : 'drawn ' + clip(home.map((c) => c.id), 4)));
    const numBad = home.filter((c, i) => flags[i] && Number(c.n) !== flags[i].rank)
      .map((c) => c.id + ' numbered ' + c.n);
    check('c11', numBad.length === 0, 'C11 every Home start-here number is the owner\'s rank',
      numBad.length ? clip(numBad, 4) : `${home.length} numbers match highlights.json`);
    const mapHl = S.map.map.chips.filter((c) => c.isHl);
    const mapBad = mapHl.filter((c) => {
      const f = flags.find((x) => x.id === c.id);
      return !f || String(f.rank) !== String(c.hl);
    });
    check('c11', mapHl.length === flags.length && mapBad.length === 0,
      'C11 the map\'s numbered chips are the same register with the same numbers',
      mapBad.length || mapHl.length !== flags.length
        ? `${mapHl.length} numbered chips, ${mapBad.length} disagree: ` + clip(mapBad.map((c) => c.id + '=' + c.hl), 3)
        : `${mapHl.length} amber chips, numbers match`);
  }

  /* ---- C12 -------------------------------------------------------------- */
  {
    const chips = S.map.map.chips;
    const heights = [...new Set(chips.map((c) => Math.round(c.h)))];
    check('c12', heights.length === 1, 'C12 every map chip is the same height, whatever its degree',
      `${chips.length} chips at ${heights.join(', ')}px` +
      (heights.length > 1 ? ': degree of the tallest: ' +
        clip(chips.filter((c) => Math.round(c.h) === Math.max(...heights)).map((c) => c.id + '/' + deg[c.id]), 3) : ''));
    /* width is a pure function of the label: chip = ceil(text) + 30 (+16 numbered).
       If anything else got into it -- degree, tier, claims -- the residual moves. */
    const resid = chips.map((c) => ({
      id: c.id, r: c.w - c.labW - (c.isHl ? 46 : 30),
    })).filter((x) => x.r < -0.5 || x.r > 1.5);
    check('c12', resid.length === 0, 'C12 chip width is its text plus one constant, nothing else',
      resid.length ? `${resid.length} chips off the constant: ` + clip(resid.map((x) => x.id + ' ' + x.r.toFixed(1)), 3)
        : `${chips.length} chips within [0,1.5]px of text+${'30/46'}`);
    const marks = [...new Set(S.hood3.hood.map((e) => e.mw + '×' + e.mh))];
    check('c12', marks.length === 1, 'C12 every ring mark is the same size',
      `${S.hood3.hood.length} marks at ${marks.join(', ')}`);
    const tmw = [...new Set(S['thread:custody'].thread.chips.map((c) => Math.round(c.w) + '×' + Math.round(c.h)))];
    check('c12', tmw.length === 1, 'C12 every thread small-map chip is the same size',
      `${S['thread:custody'].thread.chips.length} chips at ${tmw.join(', ')}`);
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
      [edges.length],
      [claimRows.length, ...tier],
      [tlEvents.length],
      [(mapData.nodes || []).length, (mapData.bands || []).length, (mapData.eras || []).length],
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
  /* Every sourced connection is drawn once, under its own relationship, with its
     own sentence; no group is headed by a raw type id; nothing says "member".
     Restated, not imported, from app/src/vocab.ts. */
  {
    const READER = {
      custody: 'Custody', funding: 'Money', programmatic: 'Programme links',
      institutional: 'Institutional ties', legislative: 'Law and oversight',
      research: 'Research and authorship', investigative: 'Investigations',
      'witness-chain': 'Testimony', behavioral: 'Conduct', denial: 'Denials',
      temporal: 'Sequence in time', geographic: 'Place',
    };
    const NO_SENTENCE = 'no sentence recorded for this link';
    const recC = focusRec.connections || [];
    const want = recC.map((c) => c.type + '|' + c.id + '|' + (c.edgeLabel || c.note || NO_SENTENCE)).sort();
    const got = [];
    for (const g of S.node.conns.groups) for (const r of g.rows) for (const l of r.lines) got.push(g.type + '|' + r.id + '|' + l);
    got.sort();
    const missing = want.filter((x) => !got.includes(x));
    const extra = got.filter((x) => !want.includes(x));
    check('c22', want.length === got.length && missing.length === 0 && extra.length === 0,
      'C22 every sourced connection on #/n/' + NODE_FOCUS + ' is drawn once, under its relationship, with its own sentence',
      `record ${want.length} · page ${got.length}` +
      (missing.length ? ' · missing ' + clip(missing, 2) : '') + (extra.length ? ' · extra ' + clip(extra, 2) : ''));
    const badHead = S.node.conns.groups.filter((g) => READER[g.type] ? g.head !== READER[g.type] : !g.head);
    check('c22', S.node.conns.groups.length > 0 && badHead.length === 0, 'C22 every group is headed by its reader name',
      badHead.length ? clip(badHead.map((g) => g.type + '="' + g.head + '"'), 4) : S.node.conns.groups.length + ' groups');
    const bucket = S.node.conns.groups.flatMap((g) => g.rows.flatMap((r) => r.metas)).filter((m) => /^member\b/i.test(m));
    check('c22', bucket.length === 0, 'C22 no connection is labelled with the bucket word "member"',
      bucket.length ? bucket.length + ' rows' : 'none');
    const rWant = recC.map((c) => c.type + '|' + c.id + '|' + (c.edgeLabel || c.note || NO_SENTENCE)).sort();
    const rGot = S.report.rconns.map((r) => r.type + '|' + r.id + '|' + r.sent).sort();
    check('c22', rWant.length === rGot.length && rWant.every((x, i) => x === rGot[i]),
      'C22 the node report lists every connection with its sentence',
      `record ${rWant.length} · report ${rGot.length}`);
    const rBucket = S.report.rconns.filter((r) => /·\s*member\b/i.test(r.text));
    check('c22', rBucket.length === 0, 'C22 the node report never says "member"',
      rBucket.length ? rBucket.length + ' rows' : 'none');
  }

  /* ---- C23 -------------------------------------------------------------- */
  /* Nothing authored is hidden: every field a researcher wrote on the record has a
     place on the page. The chronology rule is restated here, not imported. */
  {
    const list = (v) => (Array.isArray(v) ? v.filter(Boolean) : (v ? [v] : []));
    for (const [stopId, rec] of [['node', focusRec], ['person', personRec]]) {
      const f = S[stopId].fields;
      const chron = new Set([...(rec.chronology || []), ...(rec.sequenceChain || [])]
        .map((e) => String(e.date) + '|' + String(e.event || '').trim().toLowerCase()));
      const want = {
        oq: ((rec.dossier && rec.dossier.openQuestions) || []).length,
        unv: list(rec.unverified).length, chron: chron.size,
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
  {
    const p = S.phone.phone;
    check('c26', p.mainW >= 300 && p.scrollW <= p.vw + 1,
      'C26 a node page reads at 375px: a real main column and no sideways scroll',
      `main ${Math.round(p.mainW)}px · page ${p.scrollW}px in ${p.vw}px`);
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
  {
    const t = S.timeline.timeline;
    const byEv = new Map(tlEvents.map((e) => [e.id, e]));
    const packOf = new Map(t.packs.map((p) => [p.strand + '|' + p.era, p]));
    const wrongLane = [], wrongEra = [], outside = [];
    for (const it of t.items) {
      const e = byEv.get(it.id);
      if (!e) { wrongEra.push(it.id + ' (not in timeline.json)'); continue; }
      if (e.strand !== it.strand) wrongLane.push(`${it.id} drawn in ${it.strand}, is ${e.strand}`);
      if (String(e.era) !== String(it.era)) wrongEra.push(`${it.id} drawn in era ${it.era}, is ${e.era}`);
      const p = packOf.get(e.strand + '|' + e.era);
      if (!p) { outside.push(it.id + ' (no lane for ' + e.strand + '/' + e.era + ')'); continue; }
      const cx = it.x + it.w / 2, cy = it.y + it.h / 2;
      if (cx < p.x - 1 || cx > p.x + p.w + 1 || cy < p.y - 1 || cy > p.y + p.h + 1) {
        outside.push(`${it.id} at ${cx.toFixed(0)},${cy.toFixed(0)} outside ${e.strand} lane`);
      }
    }
    check('c15', wrongLane.length === 0 && wrongEra.length === 0,
      'C15 every timeline item carries the era and strand its event has in timeline.json',
      wrongLane.length + wrongEra.length ? clip([...wrongLane, ...wrongEra], 3) : `${t.items.length} items`);
    check('c15', outside.length === 0, 'C15 every item is drawn inside its own era column and strand lane',
      outside.length ? clip(outside, 3) : `${t.items.length} items inside ${t.packs.length} lane boxes`);
    const openEra = t.packs.length ? t.packs[0].era : null;
    const want = tlEvents.filter((e) => String(e.era) === String(openEra)).length;
    const printed = Number((t.openEraSub.match(/(\d+)\s+events/) || [])[1]);
    check('c15', t.items.length === want && printed === want,
      'C15 the open era draws a chip or a mark for every one of its events',
      `era ${openEra}: ${t.items.length} drawn (${t.items.filter((i) => i.kind === 'chip').length} chips, ` +
      `${t.items.filter((i) => i.kind === 'mark').length} marks), header says ${printed}, timeline.json has ${want}`);
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

    const HOME = '#/', NODE = '#/n/' + NODE_FOCUS, NMAP = '#/n/' + NODE_FOCUS + '/map';
    check('c17', !!B.fresh && B.fresh.present && B.fresh.disabled === true && B.fresh.aria === 'true',
      'C17 on a cold deep link the button is disabled, so it can never leave the site',
      B.fresh ? `${NODE} cold: disabled=${B.fresh.disabled}, aria-disabled=${B.fresh.aria}`
        : 'the cold load was not reached');

    const walked = B.trail.map((x) => x.hash);
    check('c17', walked.join(' ') === [HOME, NODE, NMAP].join(' '),
      "C17 the trail is built by clicking the pages' own links",
      'walked ' + (walked.join(' \u2192 ') || '(nothing)') + ' \u00b7 wanted ' + [HOME, NODE, NMAP].join(' \u2192 '));
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

    check('c17', !!B.forward && B.forward.hash === NMAP,
      'C17 the button creates no history entry: forward twice reaches the map again',
      B.forward ? 'forward, forward landed ' + B.forward.hash + ', wanted ' + NMAP
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
          : CH.length + ' routes, strip ' + CH[0].strip.h + 'px at the foot of each');

      const covered = CH.filter((r) => r.strip.present && !r.strip.unobstructed).map((r) => r.hash);
      check('c18', covered.length === 0, 'C18 nothing is drawn over the analyst strip',
        covered.length ? 'covered on ' + clip(covered, 3) : 'the strip is the topmost element at its own centre everywhere');

      /* Only where the reader cannot scroll it out of the way. On the map and
         the neighbourhood that is the whole point: both take the viewport and
         neither can give the dock any height, so the tab overlays, and the only
         strip it may overlay is the map's band-label gutter, which carries
         nothing. The first build took 30px of height from both instead and put
         the map's lowest chip 23px into its own legend on CI. */
      const fixedRoutes = CH.filter((r) => r.strip.present && !r.strip.scrolls);
      const covering = fixedRoutes.filter((r) => r.strip.covers.length)
        .map((r) => r.hash + ' covers ' + r.strip.covers.length + ': ' + r.strip.covers[0]);
      check('c18', covering.length === 0 && fixedRoutes.length > 0,
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
        ['nodes on the program map', 'onmap', w.onmap],
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

      /* grouping: every band's own total, read back out of the tool's table.
         A regex LITERAL, not a string-built RegExp: the string form lost its
         escapes on the way into this file and matched nothing, which read as
         all seven bands wrong. */
      const bandSaid = {};
      for (const row of String(o.byband || '').split(/\r?\n/)) {
        const m = /^\s+(\d+)\s\s(\S.*)$/.exec(row);
        if (m) bandSaid[m[2].trim()] = Number(m[1]);
      }
      const bandOff = Object.entries(w.bands)
        .filter(([id, n]) => bandSaid[id] !== n)
        .map(([id, n]) => id + ': tool says ' + bandSaid[id] + ', the index has ' + n);
      check('c19', bandOff.length === 0, "C19 group_by band totals are the map bands' own memberships",
        bandOff.length ? clip(bandOff, 3)
          : index.bands.length + ' bands: ' + Object.entries(bandSaid).map(([k, v]) => k + ' ' + v).join(' \u00b7 '));

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
          'C19 the guard does not cry wolf over a cell, a thread, a class or a hostname',
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
    const seen = (failsByCheck.get(POISON) || 0) > 0;
    const line = (seen ? 'ok    ' : 'FAIL  ') + `POISON=${POISON} the ${POISON.toUpperCase()} check sees the poisoned page`
      + ' :: ' + POISONS[POISON].what + ' → '
      + (seen ? `${failsByCheck.get(POISON)} of its assertions failed` : 'every assertion still passed, so the check is blind');
    console.log('  ' + line);
    const others = [...failsByCheck.keys()].filter((k) => k !== POISON);
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
