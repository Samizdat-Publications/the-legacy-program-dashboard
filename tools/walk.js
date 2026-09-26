/* Walk the new shell. Visit every route kind, screenshot each one, report what
 * looks wrong.
 *
 * WHAT IT POINTS AT
 * -----------------
 * The Vite app in `app/`, served by `npx vite preview` (default
 * http://127.0.0.1:4173, override with APP_URL). It used to point at
 * `dist/the-program.html` and click a table of `.l0ctl` controls, `[data-view]`
 * tabs and `[data-path]` entry chips, driving the board through
 * `window.__board`. The new shell has none of those. It is hash-routed, every
 * state is a URL, and the itinerary below is therefore a list of ROUTES rather
 * than a list of clicks: one per route kind in `app/src/router.ts`, home
 * through not-found. `BOARD_URL` is gone with the board it named.
 *
 * WHY THIS EXISTS
 * ---------------
 * notes/HANDOFF-2026-08-26-UX.md section 5 asked for it by name. Stewart's
 * question was what would let a session "click everything, see how it looks,
 * write notes". tools/look.js photographs a handful of states somebody chose in
 * advance, and every defect Stewart has reported was in a state nobody chose in
 * advance. This file enumerates the states instead of guessing which ones
 * matter, and on the new shell the enumeration is exact, because the router
 * says how many kinds of state there are.
 *
 * WHAT IT IS AND IS NOT
 * ---------------------
 * A CAMERA WITH A NOTEBOOK. It asserts nothing about the app, exits 0 whatever
 * it finds, and must never enter the gate. Its findings are leads for a human,
 * not verdicts: an "overlap" here may be a deliberate stack, and a "clipped"
 * element may be a label that is meant to ellipsize. `app/checks/run.mjs` is
 * where a finding goes once somebody has looked and decided it is real. The one
 * thing it exits non-zero for is a harness problem: nothing serving the app is
 * not a finding about the app.
 *
 * The columns that earn it are OVERLAP and MAP SHARE. Both are what Stewart
 * sees and neither is visible from reading source. The element inventory earns
 * its place for a narrower reason: `button.nav-back` is rendered by the frame on
 * every route and Stewart made it a condition of the new shell, so a route that
 * has lost it should show up here as a zero rather than as a screenshot nobody
 * looked closely at.
 *
 * THE HONEST LIMIT, unchanged from look.js: a screenshot is one moment, and
 * nothing here can say whether the shell READS. It widens the net. It does not
 * replace Stewart looking.
 *
 * Every id in the itinerary is read from the data the preview is serving
 * (`app/public/data/`) at run time: the node is the highest-degree node in
 * index.json, the thread is the first in threads.json, the patent is the first
 * in patents.json and the era is the era with the most events in
 * timeline.json. Nothing is written down here. (The map cell, the fullest cell
 * in map.json, went with the L0 map in phase 11: map.json is no longer written.)
 *
 * Run it:
 *   cd app && npm run build && npx vite preview --host 127.0.0.1 --port 4173
 *   node tools/walk.js
 *   node tools/walk.js --size 1366x768 --out /tmp/walk
 */
const { requirePlaywright, launchOptions, describe } = require('./browser_env');
const { chromium } = requirePlaywright();
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const APP = (process.env.APP_URL || 'http://127.0.0.1:4173').replace(/\/+$/, '') + '/';
const argv = process.argv.slice(2);
const argOf = f => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };
const OUT = argOf('--out') || path.join(ROOT, 'dist', 'shots', 'walk');
const SIZE = (argOf('--size') || '1600x900').split('x').map(Number);

async function jget(p) {
  const r = await fetch(APP + p);
  if (!r.ok) throw new Error(p + ' -> HTTP ' + r.status);
  return r.json();
}

/* The itinerary's ids, from the data the preview is serving. */
async function realIds() {
  const [index, threadsFile, patentsFile, events] = await Promise.all([
    jget('data/index.json'), jget('data/threads.json'), jget('data/patents.json'),
    jget('data/timeline.json'),
  ]);
  const nodes = index.nodes.slice().sort((a, b) => (b.deg || 0) - (a.deg || 0));
  const threads = threadsFile.threads || threadsFile;
  const patents = patentsFile.patents || [];
  const eraCount = {};
  for (const e of events) eraCount[e.era] = (eraCount[e.era] || 0) + 1;
  const era = Object.keys(eraCount).sort((a, b) => eraCount[b] - eraCount[a])[0];
  if (!nodes.length || !threads.length || !patents.length || !era) {
    throw new Error('the served data has no nodes, threads, patents or eras to point at');
  }
  return {
    node: nodes[0].id, nodeDeg: nodes[0].deg || 0,
    thread: threads[0].id,
    patent: String(patents[0].number).replace(/[^0-9]/g, ''),
    patentLabel: String(patents[0].number),
    era, eraCount: eraCount[era],
  };
}

/* Pages settle at very different speeds. These are the waits
   app/checks/run.mjs uses for the same routes. */
function settleFor(hash) {
  if (hash.startsWith('#/evidence')) return 3200;
  if (hash.startsWith('#/map')) return 2400;
  if (hash.startsWith('#/timeline')) return 2400;
  if (/hood/.test(hash)) return 2200;
  if (hash === '#/') return 1600;
  return 1500;
}

/* Every route kind in app/src/router.ts, in the order the type union declares
   them, plus the two query-string states that change what a route draws
   (a map cell, an evidence filter) and the not-found page, which the router
   reaches from anything it cannot parse. */
function itinerary(ids) {
  return [
    { id: 'home',         label: 'home',                       hash: '#/' },
    { id: 'node',         label: 'a node page',                hash: '#/n/' + ids.node },
    { id: 'node-map',     label: 'the map centred on it',      hash: '#/n/' + ids.node + '/map' },
    { id: 'node-hood',    label: 'its neighbourhood',          hash: '#/n/' + ids.node + '/hood' },
    { id: 'hood',         label: 'the neighbourhood, nothing selected', hash: '#/hood' },
    { id: 'map',          label: 'the map at fit',             hash: '#/map' },
    { id: 'thread',       label: 'a thread',                   hash: '#/t/' + ids.thread },
    { id: 'thread-map',   label: 'that thread on the map',     hash: '#/t/' + ids.thread + '/map' },
    { id: 'timeline-era', label: 'the timeline with an era open', hash: '#/timeline?era=' + ids.era },
    { id: 'patents',      label: 'a patent',                   hash: '#/patents/' + ids.patent },
    { id: 'evidence',     label: 'the evidence table, filtered', hash: '#/evidence?tier=1' },
    { id: 'report-node',  label: 'the report for a node',      hash: '#/report/n/' + ids.node },
    { id: 'report-thread',label: 'the report for a thread',    hash: '#/report/t/' + ids.thread },
    { id: 'notfound',     label: 'not found',                  hash: '#/no-such-route-at-all' },
  ];
}

/* The per-stop element inventory. `button.nav-back` is first because it is the
   one a missing zero must be impossible to miss. */
const INVENTORY = [
  ['back', 'button.nav-back'],
  ['nav', 'nav.nav a[href]'],
  ['links', 'a[href^="#/"]'],
  ['buttons', 'button'],
  ['chips', 'a.chip'],
  ['notice', '.notice'],
];

/* Everything measured after a route settles, in one pass in the page.
 *
 * The geometry below is carried over from the old walker unchanged in what it
 * measures. Two things did have to change and both are named where they are:
 * the selectors, which named the old board's controls and do not exist here,
 * and the rect cache, because the old double loop called
 * getBoundingClientRect twice per PAIR and the new shell puts an order of
 * magnitude more interactive elements on a page than the old one did. The
 * cache changes the cost, not the answer: rects do not move during the pass. */
const INSPECT = (inventory) => {
  const out = { errors: [], overlaps: [], clipped: [], mapShare: null, mapBox: null,
                offscreen: [], inv: {}, probe: null, back: null };
  const R = e => e.getBoundingClientRect();
  const named = e => {
    const id = e.getAttribute('data-id') || e.getAttribute('data-cell')
      || e.getAttribute('href') || '';
    const cls = (typeof e.className === 'string' && e.className.trim())
      ? '.' + e.className.trim().split(/\s+/)[0] : '';
    const head = (e.tagName.toLowerCase() + cls + (id ? '[' + id + ']' : '')).slice(0, 34);
    return head + '"' + (e.textContent || '').trim().slice(0, 18) + '"';
  };

  /* INTERACTIVE RECTS THAT SIT ON EACH OTHER. Two controls a reader can both aim
     at, occupying the same pixels, is the defect class Stewart keeps reporting and
     the one no unit check looks for. Only visible, non-nested pairs count: a button
     inside a toolbar overlaps its toolbar by construction. */
  /* VISIBLE MEANS VISIBLE RIGHT NOW, INCLUDING CLIPPING.
     The first run of the old version of this file reported 33 overlaps in one
     view and eight controls "outside the window", and every one was wrong. They
     were chips sitting below the fold of a container with overflow-y:auto,
     working exactly as intended. getBoundingClientRect reports where a
     scrolled-away element WOULD be, so the raw rects put them on top of their
     neighbours and off the bottom of the screen. Nothing was wrong with the
     board.

     That is this repo's own lesson pointed at its newest tool: a stale
     runtime-strip once cost a handoff two findings that did not exist, and a
     camera that cries wolf 33 times is worse than no camera, because the next
     person learns to skim it. So an element counts only if its rect still
     intersects every clipping ancestor between it and the document. */
  const visibleNow = e => {
    const r = R(e);
    if (r.width <= 3 || r.height <= 3) return false;
    const cs = getComputedStyle(e);
    if (cs.visibility === 'hidden' || cs.opacity === '0' || cs.display === 'none') return false;
    for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const acs = getComputedStyle(a);
      const clips = /auto|scroll|hidden/.test(acs.overflow + acs.overflowX + acs.overflowY);
      if (!clips) continue;
      const ra = R(a);
      if (r.bottom <= ra.top + 1 || r.top >= ra.bottom - 1
       || r.right <= ra.left + 1 || r.left >= ra.right - 1) return false;
    }
    return true;
  };
  /* The new shell's interactive surface: links, buttons, the map's cells (which
     carry role=button and a tabindex) and anything else with a button role.
     There are no [data-view], [data-opt], [data-path] or [data-fit] attributes
     on this shell. */
  const hits = [...document.querySelectorAll(
    'a[href],button,[role=button],input,select,summary,[data-cell]')]
    .filter(visibleNow);
  /* THE MAP'S CELLS ARE CONTAINERS THAT ARE NOT DOM ANCESTORS. `a.chip` and
     `.cell[data-cell]` are siblings under `.map-grid`, both absolutely
     positioned, and every chip is drawn inside its own cell's box. That is the
     same "by construction" relation the `contains` test already excludes for a
     button inside a toolbar, so it is excluded on the same grounds -- otherwise
     the map reports 81 overlaps that are the layout working, and a camera that
     cries wolf 81 times teaches the next reader to skim it. */
  const stacked = (a, b, ra, rb) => {
    const pair = (c, chip, rc, rch) =>
      c.hasAttribute('data-cell') && chip.classList.contains('chip')
      && rch.left >= rc.left - 1 && rch.right <= rc.right + 1
      && rch.top >= rc.top - 1 && rch.bottom <= rc.bottom + 1;
    return pair(a, b, ra, rb) || pair(b, a, rb, ra);
  };
  const rects = hits.map(R);
  const order = hits.map((_, i) => i).sort((i, j) => rects[i].top - rects[j].top);
  for (let ii = 0; ii < order.length; ii++) {
    const i = order[ii], ra = rects[i];
    for (let jj = ii + 1; jj < order.length; jj++) {
      const j = order[jj], rb = rects[j];
      if (rb.top >= ra.bottom) break;      /* sorted by top: nothing below can overlap */
      const a = hits[i], b = hits[j];
      if (a.contains(b) || b.contains(a)) continue;
      if (stacked(a, b, ra, rb)) continue;
      const ox = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
      const oy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      if (ox > 2 && oy > 2)
        out.overlaps.push(`${named(a)} × ${named(b)} (${Math.round(ox)}×${Math.round(oy)}px)`);
    }
  }

  /* TEXT CUT OFF BY ITS OWN BOX. scrollWidth beyond clientWidth on an element that
     is not a scroller. Ellipsis is legitimate and common here, so this is a lead. */
  for (const e of document.querySelectorAll(
    'button,a.chip,.clabel,.hood-label,.eyebrow,.cell-head span,.pt-num,h1,h2,h3')) {
    if (!visibleNow(e)) continue;
    const cs = getComputedStyle(e);
    if (cs.overflow === 'auto' || cs.overflowX === 'auto' || cs.overflow === 'scroll') continue;
    if (e.scrollWidth > e.clientWidth + 2 && e.clientWidth > 0)
      out.clipped.push(`${named(e)} +${e.scrollWidth - e.clientWidth}px`);
  }

  /* CONTROLS PUSHED OUT OF THE WINDOW -- and genuinely unreachable, meaning no
     scrollable ancestor could bring them back. A chip below the fold of a working
     scroller is not a defect; a control the layout has pushed past the viewport
     with nothing to scroll is. */
  /* AND THE DOCUMENT IS ONE OF THEM HERE. The old board was a fixed shell whose
     panels each had their own overflow:auto, so the ancestor walk stopped short
     of documentElement and never needed to look at it. The new shell's pages are
     long and scroll the DOCUMENT, so leaving it out reported every link below
     the fold of a node page as a control pushed out of the window: 96 of them on
     one page, none of them a defect. The rule is unchanged -- a control counts
     only when nothing could scroll it back -- the page scroller is simply one of
     the things that can. */
  const scrollableAncestor = e => {
    for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const acs = getComputedStyle(a);
      if (/auto|scroll/.test(acs.overflowY + acs.overflowX)
          && (a.scrollHeight > a.clientHeight + 2 || a.scrollWidth > a.clientWidth + 2))
        return true;
    }
    const de = document.scrollingElement || document.documentElement;
    if (de && (de.scrollHeight > de.clientHeight + 2 || de.scrollWidth > de.clientWidth + 2))
      return true;
    return false;
  };
  for (const e of hits) {
    const r = R(e);
    if ((r.right < 0 || r.bottom < 0 || r.left > innerWidth || r.top > innerHeight)
        && !scrollableAncestor(e))
      out.offscreen.push(named(e));
  }

  /* HOW MUCH OF THE WINDOW THE MAP ACTUALLY HAS. The number behind "you never
     actually get to see the full map". `.map-grid` is the new shell's map; there
     is no `.l0wrap` and no canvas. */
  const grid = document.querySelector('.map-grid');
  if (grid) {
    const r = R(grid);
    out.mapShare = Math.round(100 * (r.width * r.height) / (innerWidth * innerHeight));
    out.mapBox = Math.round(r.width) + '×' + Math.round(r.height);
  }

  /* THE ELEMENT INVENTORY, back button first. */
  for (const [name, sel] of inventory) out.inv[name] = document.querySelectorAll(sel).length;
  const b = document.querySelector('button.nav-back');
  out.back = b ? {
    text: (b.textContent || '').trim(),
    disabled: b.disabled === true,
    aria: b.getAttribute('aria-disabled'),
    label: b.getAttribute('aria-label') || '',
  } : null;

  /* WHAT THE PAGE ITSELF SAYS IT DREW. The three publishers of the new shell:
     window.__app.map.chips()/.cells(), .hood.ring()/.centre(), .timeline.placed().
     A lead, not a measurement -- everything above is read off the DOM instead. */
  const app = window.__app || {};
  const bits = [];
  try {
    if (app.map && document.querySelector('.map-grid')) {
      const chips = app.map.chips();
      const cells = app.map.cells();
      bits.push('map ' + chips.length + ' chips/' + cells.length + ' cells, '
        + (chips[0] ? chips[0].mode : '?') + ' mode');
    }
  } catch (e) { bits.push('map probe threw'); }
  try {
    if (app.hood && document.querySelector('.hood-label, a.hood-n')) {
      const c = app.hood.centre();
      bits.push('hood ring ' + app.hood.ring().length + ', centre ' + (c.id || 'none'));
    }
  } catch (e) { bits.push('hood probe threw'); }
  try {
    if (app.timeline && location.hash.indexOf('timeline') >= 0) {
      bits.push('timeline ' + app.timeline.placed().length + ' placed');
    }
  } catch (e) { bits.push('timeline probe threw'); }
  out.probe = bits.join('; ') || null;
  return out;
};

(async () => {
  let ids;
  try {
    ids = await realIds();
  } catch (e) {
    console.error('HARNESS: the app is not being served at ' + APP + ' (' + e.message + ').');
    console.error('Run `npm run build` then `npx vite preview --host 127.0.0.1 --port 4173`');
    console.error('in app/, or set APP_URL.');
    process.exit(2);
  }
  const STOPS = itinerary(ids);

  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch(launchOptions({
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  }));
  const page = await browser.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });

  const rows = [];
  let n = 0;
  let loaded = false;
  for (const stop of STOPS) {
    n++;
    const before = errors.length;
    let reached = true;
    try {
      /* The first stop loads the app; every later one moves by hash, which is
         how a reader moves and is what keeps the back button's history real. */
      if (!loaded) { await page.goto(APP + stop.hash, { waitUntil: 'load' }); loaded = true; }
      else await page.evaluate(h => { location.hash = h; }, stop.hash);
    } catch (e) { reached = false; errors.push(`${stop.id}: ${String(e).slice(0, 120)}`); }
    await page.waitForTimeout(settleFor(stop.hash));

    const tag = String(n).padStart(2, '0') + '-' + stop.id;
    await page.screenshot({ path: path.join(OUT, tag + '.png') });
    const info = await page.evaluate(`(${INSPECT})(${JSON.stringify(INVENTORY)})`);
    const title = await page.title();
    rows.push({ tag, label: stop.label, hash: stop.hash, title, reached, info,
                newErrors: errors.slice(before) });
    process.stdout.write(`${tag}  ${reached ? '' : '(not reached) '}`
      + `map ${info.mapShare == null ? '-' : info.mapShare + '%'}`
      + `  back ${info.inv.back}  overlaps ${info.overlaps.length}`
      + `  clipped ${info.clipped.length}  offscreen ${info.offscreen.length}\n`);
  }

  /* THE REPORT. A table first, because the point is to scan it. */
  const esc = s => String(s).replace(/\|/g, '\\|');
  let md = `# Walk of the new shell\n\n`;
  md += `Captured at ${SIZE[0]}x${SIZE[1]} from \`${APP}\`. `;
  md += `${rows.length} stops, one per route kind in \`app/src/router.ts\` plus the two\n`;
  md += `query-string states that change what a route draws.\n\n`;
  md += `Ids, all read from the data the preview is serving: node \`${ids.node}\` `;
  md += `(degree ${ids.nodeDeg}, the highest on the board), thread \`${ids.thread}\`, `;
  md += `patent \`${ids.patentLabel}\`, `;
  md += `era \`${ids.era}\` (${ids.eraCount} events).\n\n`;
  md += `**This file asserts nothing.** Every row is a lead for somebody to look at, not\n`;
  md += `a verdict. An overlap may be a deliberate stack; a clipped element may be a label\n`;
  md += `that is meant to ellipsize. What it is good at is finding the states nobody\n`;
  md += `thought to check.\n\n`;
  md += `| # | stop | route | map share | overlaps | clipped | offscreen | errors |\n`;
  md += `|---|---|---|---|---|---|---|---|\n`;
  for (const r of rows) {
    md += `| ${r.tag} | ${esc(r.label)}${r.reached ? '' : ' **(not reached)**'} `
       + `| \`${esc(r.hash)}\` `
       + `| ${r.info.mapShare == null ? '-' : r.info.mapShare + '% ' + r.info.mapBox} `
       + `| ${r.info.overlaps.length} | ${r.info.clipped.length} `
       + `| ${r.info.offscreen.length} | ${r.newErrors.length} |\n`;
  }

  /* THE ELEMENT INVENTORY. The back button is a condition of the new shell and
     is rendered by the frame on every route, so a 0 in that column is a finding
     on its own. */
  md += `\n## Element inventory\n\n`;
  md += `\`button.nav-back\` is rendered by the frame on every route. A zero in the **back**\n`;
  md += `column is a missing back button, not a quiet screenshot.\n\n`;
  md += `| # | stop | ${INVENTORY.map(([k]) => k).join(' | ')} | back state |\n`;
  md += `|---|---|${INVENTORY.map(() => '---').join('|')}|---|\n`;
  for (const r of rows) {
    const state = r.info.back
      ? (r.info.back.disabled || r.info.back.aria === 'true' ? 'disabled' : 'live')
        + (r.info.back.label ? ' · ' + esc(r.info.back.label) : '')
      : '**absent**';
    md += `| ${r.tag} | ${esc(r.label)} | `
       + INVENTORY.map(([k]) => {
         const v = r.info.inv[k];
         return k === 'back' && !v ? '**0**' : String(v);
       }).join(' | ')
       + ` | ${state} |\n`;
  }
  const noBack = rows.filter(r => !r.info.inv.back);
  md += `\n`;
  md += noBack.length
    ? `**${noBack.length} route(s) drew no back button:** ${noBack.map(r => r.tag).join(', ')}.\n`
    : `Every route drew exactly one back button.\n`;

  const detail = rows.filter(r => r.info.overlaps.length || r.newErrors.length
                                || r.info.offscreen.length || !r.info.inv.back);
  if (detail.length) {
    md += `\n## What to look at\n`;
    for (const r of detail) {
      md += `\n### ${r.tag} - ${r.label}\n\n\`${esc(r.hash)}\` · ${esc(r.title)}\n\n`;
      md += `![${r.tag}](${r.tag}.png)\n\n`;
      if (!r.info.inv.back) md += `**No \`button.nav-back\` on this route.**\n\n`;
      if (r.info.overlaps.length) {
        md += `**Interactive rects overlapping (${r.info.overlaps.length}):**\n\n`;
        for (const o of r.info.overlaps.slice(0, 12)) md += `- ${esc(o)}\n`;
        if (r.info.overlaps.length > 12) md += `- and ${r.info.overlaps.length - 12} more\n`;
      }
      if (r.info.offscreen.length) {
        md += `\n**Controls outside the window:** ${r.info.offscreen.slice(0, 8).map(esc).join(', ')}\n`;
      }
      if (r.newErrors.length) {
        md += `\n**Console:**\n\n`;
        for (const e of r.newErrors.slice(0, 6)) md += `- \`${esc(e)}\`\n`;
      }
    }
  } else {
    md += `\nNo overlaps, no offscreen controls, no missing back button and no console\n`;
    md += `errors in any state.\n`;
  }

  const probed = rows.filter(r => r.info.probe);
  if (probed.length) {
    md += `\n## What the pages say they drew\n\n`;
    md += `From the page publishers, \`window.__app.map\`, \`.hood\` and \`.timeline\`. Leads,\n`;
    md += `not measurements: everything in the tables above is read off the DOM instead.\n\n`;
    for (const r of probed) md += `- **${r.tag}** ${esc(r.info.probe)}\n`;
  }

  const withMap = rows.filter(r => r.info.mapShare != null);
  if (withMap.length) {
    const worst = withMap.reduce((a, b) => (b.info.mapShare < a.info.mapShare ? b : a));
    md += `\n## Map share\n\nSmallest the map got: **${worst.info.mapShare}%** of the window `;
    md += `at \`${worst.tag}\` (${worst.label}).\n`;
  } else {
    md += `\n## Map share\n\nNo stop drew a \`.map-grid\`, which is itself worth a look.\n`;
  }

  fs.writeFileSync(path.join(OUT, 'REPORT.md'), md);
  console.log(`\n${rows.length} stops -> ${OUT}`);
  console.log(describe());
  console.log('REPORT.md written');
  await browser.close();
})();
