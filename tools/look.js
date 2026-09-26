/* Look at the new shell. Screenshots, at real viewport sizes, from any session.
 *
 * WHAT IT POINTS AT
 * -----------------
 * The Vite app in `app/`, served by `npx vite preview` (default
 * http://127.0.0.1:4173, override with APP_URL). It used to point at
 * `dist/the-program.html`, the single-file board with `[data-view]` tabs, a
 * canvas map, `.l0ctl` controls and `window.__board`. None of those exist in
 * the new shell: it is hash-routed, the routes are in `app/src/router.ts`, the
 * map is DOM rather than canvas, and the pages publish `window.__app.map`,
 * `window.__app.hood` and `window.__app.timeline`. `BOARD_URL` is gone with the
 * board it named.
 *
 * WHY THIS EXISTS
 * ---------------
 * CLAUDE.md section 3 carried a table saying a cloud session "can look at the
 * dashboard: no". The row was wrong. Chromium is installed, the app serves over
 * HTTP, and page.screenshot() writes a PNG that a session can open and read
 * like any other image. The first run of the old version found four defects in
 * one pass, two of which no check could have stated. See
 * notes/LOOKING-2026-08-26.md.
 *
 * WHAT IT IS AND IS NOT
 * ---------------------
 * This is not a gate check and must never become one. It asserts nothing about
 * the app and cannot report a defect. It is a camera: it puts the rendered
 * shell on disk so a human, or a session that can open an image, can exercise
 * the judgement the checks cannot. `app/checks/run.mjs` is the check; this is
 * the eyes. The one thing it does exit non-zero for is a harness problem, the
 * same as run.mjs does: nothing serving the app is not a finding about the app.
 *
 * The sweep is fixed and is one shot per surface a reader meets, plus the map a
 * second time at 1366 wide, which is the width Design's own note puts below the
 * label floor. Every id in it is read from the data the preview is serving
 * (`app/public/data/`) at run time. Nothing here is written down by hand: the
 * node is the highest-degree node in index.json, the thread is the first in
 * threads.json, the patent is the first in patents.json.
 *
 * Output stays in `dist/shots/` so the `shots` artifact step in
 * .github/workflows/gate.yml keeps finding it. `dist/shots/` is gitignored.
 *
 * Run it:
 *   cd app && npm run build && npx vite preview --host 127.0.0.1 --port 4173
 *   node tools/look.js                 # the standard sweep -> dist/shots/
 *   node tools/look.js --out /tmp/x    # somewhere other than dist/shots
 *   APP_URL=http://127.0.0.1:5000 node tools/look.js
 */
const { requirePlaywright, launchOptions, describe } = require('./browser_env');
const { chromium } = requirePlaywright();
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const APP = (process.env.APP_URL || 'http://127.0.0.1:4173').replace(/\/+$/, '') + '/';

const argv = process.argv.slice(2);
const argOf = f => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };
const OUT = argOf('--out') || path.join(ROOT, 'dist', 'shots');

/* 1920 is the size the app is designed against and the one app/checks/run.mjs
   walks. 1366 is the commonest narrow desktop and, per the label rule in
   app/src/map/layout.ts, is where the map has to decide whether the labels
   still fit. The point of taking the map twice is that those are two different
   pictures of the same route. */
const WIDE = [1920, 1080];
const NARROW = [1366, 768];

/* Pages settle at very different speeds: the evidence table paints in blocks,
   the map measures every label before it lays out, the hood runs a force pass.
   These are the same waits app/checks/run.mjs uses for the same routes. */
function settleFor(hash) {
  if (hash.startsWith('#/evidence')) return 3200;
  if (hash.startsWith('#/map')) return 2400;
  if (hash.startsWith('#/timeline')) return 2400;
  if (/hood/.test(hash)) return 2200;
  if (hash === '#/') return 1600;
  return 1600;
}

async function jget(p) {
  const r = await fetch(APP + p);
  if (!r.ok) throw new Error(p + ' -> HTTP ' + r.status);
  return r.json();
}

/* The ids, from the data the preview is serving. Never a literal: an id typed
   into this file is an id nothing keeps true. */
async function realIds() {
  const [index, threadsFile, patentsFile] = await Promise.all([
    jget('data/index.json'), jget('data/threads.json'), jget('data/patents.json'),
  ]);
  const nodes = index.nodes.slice().sort((a, b) => (b.deg || 0) - (a.deg || 0));
  const threads = threadsFile.threads || threadsFile;
  const patents = patentsFile.patents || [];
  if (!nodes.length || !threads.length || !patents.length) {
    throw new Error('the served data has no nodes, threads or patents to point at');
  }
  return {
    node: nodes[0].id,
    nodeDeg: nodes[0].deg || 0,
    thread: threads[0].id,
    /* app/src/patents/model.ts keys a filing by its digits alone */
    patent: String(patents[0].number).replace(/[^0-9]/g, ''),
    patentLabel: String(patents[0].number),
  };
}

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

  /* --critic: the shots the blind critic reviews (tools/critic/BRIEF.md). Every
     surface a reader meets, at a common laptop, a small laptop and a phone, at
     1x so a label is the size a reader sees it. The critic gets these and the
     brief, never the code. */
  const CRITIC = argv.includes('--critic');
  const PHONE = [375, 812], SMALL = [1366, 768], BIG = [1920, 1080];
  const criticSweep = () => {
    const routes = [
      ['home', '#/'], ['node', '#/n/' + ids.node], ['person', '#/n/david-grusch'],
      ['map', '#/map'], ['hood', '#/n/' + ids.node + '/hood'], ['timeline', '#/timeline'],
      ['evidence', '#/evidence'], ['thread', '#/t/' + ids.thread], ['patent', '#/patents/' + ids.patent],
      ['report', '#/report/n/' + ids.node],
    ];
    /* name=#/hash, or name=#/hash@selector to shoot with that element scrolled
       to the top of the screen (phase 10: a section below the first screen) */
    for (const extra of (argOf('--routes') || '').split(',').filter(Boolean)) {
      const [name, rest] = extra.split('=');
      const [hash, scroll] = (rest || '').split('@');
      if (name && hash) routes.push([name, hash, scroll || null]);
    }
    const out = [];
    for (const [size, tag] of [[BIG, '1920'], [SMALL, '1366'], [PHONE, '375']]) {
      for (const [name, hash, scroll] of routes) out.push({ file: tag + '-' + name, hash, size, dpr: 1, scroll: scroll || null });
    }
    return out;
  };

  const SWEEP = CRITIC ? criticSweep() : [
    { file: '01-home',        hash: '#/',                          size: WIDE },
    { file: '02-map',         hash: '#/map',                       size: WIDE },
    { file: '03-map-1366',    hash: '#/map',                       size: NARROW },
    { file: '04-node',        hash: '#/n/' + ids.node,             size: WIDE },
    { file: '05-node-hood',   hash: '#/n/' + ids.node + '/hood',   size: WIDE },
    { file: '06-timeline',    hash: '#/timeline',                  size: WIDE },
    { file: '07-evidence',    hash: '#/evidence',                  size: WIDE },
    { file: '08-thread',      hash: '#/t/' + ids.thread,           size: WIDE },
    { file: '09-patent',      hash: '#/patents/' + ids.patent,     size: WIDE },
  ];

  const browser = await chromium.launch(launchOptions({
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  }));
  fs.mkdirSync(OUT, { recursive: true });

  const rows = [];
  /* One page per viewport size: deviceScaleFactor is fixed when the page is
     made, and the whole point of the 1366 shot is that it is the same capture
     settings at a different width. */
  const pages = new Map();
  const pageFor = async ([w, h], dpr = 2) => {
    const key = w + 'x' + h + '@' + dpr;
    if (!pages.has(key)) {
      const p = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
      const errs = [];
      p.on('pageerror', e => errs.push(String(e.message).slice(0, 160)));
      p.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)); });
      pages.set(key, { page: p, errs, loaded: false });
    }
    return pages.get(key);
  };

  for (const stop of SWEEP) {
    const slot = await pageFor(stop.size, stop.dpr || 2);
    const before = slot.errs.length;
    if (!slot.loaded) {
      await slot.page.goto(APP + stop.hash, { waitUntil: 'load' });
      slot.loaded = true;
    } else {
      await slot.page.evaluate(h => { location.hash = h; }, stop.hash);
    }
    await slot.page.waitForTimeout(settleFor(stop.hash));
    if (stop.scroll) {
      await slot.page.evaluate((sel) => { const el = document.querySelector(sel); if (el) { el.scrollIntoView({ block: 'start' }); window.scrollBy(0, -96); } }, stop.scroll);
      await slot.page.waitForTimeout(300);
    }

    const file = path.join(OUT, stop.file + '.png');
    await slot.page.screenshot({ path: file });
    const title = await slot.page.title();
    rows.push({
      file: stop.file + '.png', hash: stop.hash,
      size: stop.size[0] + 'x' + stop.size[1], title,
      errs: slot.errs.slice(before).filter(e => !/favicon|ERR_CONNECTION_RESET/i.test(e)),
    });
  }

  for (const { page } of pages.values()) await page.close();
  await browser.close();

  const pad = (s, n) => String(s).padEnd(n);
  console.log('the new shell, as rendered  ->  ' + OUT);
  console.log(APP + '  ·  ' + describe());
  console.log('node ' + ids.node + ' (degree ' + ids.nodeDeg + ') · thread ' + ids.thread
    + ' · patent ' + ids.patentLabel + ', all read from the served data');
  console.log('');
  console.log('  ' + pad('shot', 16) + pad('route', 30) + pad('viewport', 11) + 'title');
  for (const r of rows) {
    console.log('  ' + pad(r.file, 16) + pad(r.hash, 30) + pad(r.size, 11) + r.title);
  }
  const bad = rows.filter(r => r.errs.length);
  if (bad.length) {
    console.log('');
    for (const r of bad) console.log('  ! ' + r.file + ': ' + r.errs.slice(0, 2).join(' | '));
  }
  console.log('');
  console.log(rows.length + ' screenshots written.');
  console.log('Nothing here is a check. Open the PNGs and use your judgement.');
})();
