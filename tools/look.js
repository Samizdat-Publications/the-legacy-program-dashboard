/* Look at the program map. Screenshots, at real viewport sizes, from any session.
 *
 * WHY THIS EXISTS
 * ---------------
 * CLAUDE.md section 3 carried a table saying a cloud session "can look at the
 * dashboard: no", and notes/PACKED-LAYOUT-COST-2026-08-25.md built a whole cost
 * argument on it. The row was wrong. Chromium is installed, the board serves over
 * HTTP, and page.screenshot() writes a PNG that a session can open and read like
 * any other image. Nothing about that needs a local machine.
 *
 * That mattered because the packed-cell layout shipped on 25 August with eleven
 * canvas assertions green and the top of the priority list reading LOOK AT THE
 * MAP -- a task six sessions had recorded as impossible from here. It was not.
 * The first run of this file found four defects in one pass, two of which no
 * check could have stated: two of the five era column heads drawn underneath the
 * DOM control row at every viewport size, and the absent-link cross printed on
 * top of its own chip's label. See notes/LOOKING-2026-08-26.md.
 *
 * WHAT IT IS AND IS NOT
 * ---------------------
 * This is not a gate check and must never become one. It asserts nothing and
 * cannot fail. It is a camera: it puts the rendered map on disk so a human -- or
 * a session that can open an image -- can exercise the judgement the checks
 * cannot. tools/test_packed_layout.js is the check; this is the eyes.
 *
 * It sweeps viewport sizes on purpose. The map's opening state is a function of
 * how much room it gets: mountL0 opens fitted only when fitScale() clears
 * L0_LABEL_DROP, and otherwise at 1:1 in the top-left corner. Which branch runs
 * flips between common monitor sizes, so one screenshot at one size is not a
 * look at the map, it is a look at one of its two opening states.
 *
 * Run it:
 *   node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
 *   node tools/look.js                 # the standard sweep -> dist/shots/
 *   node tools/look.js --size 1920x1080
 *   node tools/look.js --out /tmp/x    # somewhere other than dist/shots
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const URL = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';

const argv = process.argv.slice(2);
const argOf = f => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };
const OUT = argOf('--out') || path.join(ROOT, 'dist', 'shots');

/* 1366 and 1920 are the two commonest desktop widths; 1600 is what the earlier
   captures used; 2560 is the size at which the fitted branch actually runs. The
   point of the sweep is to show that those are different pictures. */
const SIZES = (argOf('--size') ? [argOf('--size')] : ['1366x768', '1600x1000', '1920x1080', '2560x1440'])
  .map(s => s.split('x').map(Number));

/* Mirrors mountL0's own constants so the report can say WHY a size opened the way
   it did. If either moves in tools/l0_patches.py, move it here -- this is a
   description of the renderer, not a second source of truth for it. */
const LABEL_DROP = 0.62;

function readGeo() {
  const m = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'l0-layout-model.json'), 'utf8')).current;
  const g = (m.config && m.config.geo) || {};
  return { worldW: m.worldW, worldH: m.worldH, gutter: g.gutter || 148, headRow: g.headRow || 46 };
}

async function openMap(page) {
  await page.goto(URL, { waitUntil: 'load', timeout: 180000 });
  await page.waitForSelector('[data-view="CASES"]', { timeout: 120000 });
  await page.waitForTimeout(6000);
  await page.click('[data-view="NETWORK"]');
  await page.waitForTimeout(2200);
  /* The entry surface sits on top of the map until a reader picks a way in, and
     it re-renders, so removing the node once is not enough -- hide the class. */
  await page.addStyleTag({ content: '.l0entry{display:none !important}' });
  await page.waitForSelector('.l0wrap canvas', { timeout: 30000 });
  await page.waitForTimeout(2500);
}

const clickCtl = async (page, label) => {
  const ok = await page.evaluate(l => {
    const el = [...document.querySelectorAll('.l0ctl *')]
      .find(e => e.children.length === 0 && e.textContent.trim() === l);
    if (el) { el.click(); return true; }
    return false;
  }, label);
  await page.waitForTimeout(1800);
  return ok;
};

(async () => {
  const GEO = readGeo();
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  });
  fs.mkdirSync(OUT, { recursive: true });
  const rows = [];

  for (const [w, h] of SIZES) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    const errs = [];
    page.on('pageerror', e => errs.push(e.message.slice(0, 160)));
    await openMap(page);

    const d = await page.evaluate(() => {
      const wr = document.querySelector('.l0wrap');
      const r = wr.getBoundingClientRect();
      const m = document.querySelector('.l0meta');
      return { mapW: Math.round(r.width), mapH: Math.round(r.height),
               meta: (m && m.textContent || '').trim() };
    });
    /* The same arithmetic mountL0 does, restated here so the report can name the
       branch rather than leaving the reader to infer it from the screenshot. */
    const fit = Math.min((d.mapW - GEO.gutter - 16) / (GEO.worldW - GEO.gutter),
                         (d.mapH - GEO.headRow - 16) / (GEO.worldH - GEO.headRow));
    const branch = fit >= LABEL_DROP ? 'fitted, labels kept' : 'corner at 1:1, labels only where you pan';

    const tag = `${w}x${h}`;
    const wrap = await page.$('.l0wrap');
    await wrap.screenshot({ path: path.join(OUT, `map-${tag}-open.png`) });
    if (await clickCtl(page, 'OVERVIEW')) await wrap.screenshot({ path: path.join(OUT, `map-${tag}-overview.png`) });

    rows.push({ tag, map: `${d.mapW}x${d.mapH}`, fit: fit.toFixed(3), branch, meta: d.meta,
                errs: errs.filter(e => !/font|ERR_CONNECTION_RESET|404|favicon/i.test(e)) });
    await page.close();
  }

  /* One detail crop at the size where the whole map fits, because two of the
     defects this file was written to find live in a 60px strip that is easy to
     scroll past in a full-page shot. */
  const page = await browser.newPage({ viewport: { width: 2560, height: 1440 }, deviceScaleFactor: 2 });
  await openMap(page);
  const bb = await (await page.$('.l0wrap canvas')).boundingBox();
  /* Height from the model's own head row plus a few pixels of the first chip
     row, so the crop always shows the whole strip and where it ends. A constant
     here silently truncated the note line the first time geo.headRow moved. */
  const strip = GEO.headRow + 14;
  await page.screenshot({ path: path.join(OUT, 'head-strip-left.png'),
    clip: { x: bb.x, y: bb.y, width: 760, height: strip } });
  await page.screenshot({ path: path.join(OUT, 'head-strip-right.png'),
    clip: { x: bb.x + bb.width - 800, y: bb.y, width: 800, height: strip } });
  await page.close();
  await browser.close();

  const pad = (s, n) => String(s).padEnd(n);
  console.log(`the program map, as rendered  ->  ${OUT}`);
  console.log(`world ${GEO.worldW}x${GEO.worldH} · gutter ${GEO.gutter} · head row ${GEO.headRow} · labels drop below ${LABEL_DROP}`);
  console.log('');
  console.log(`  ${pad('viewport', 11)}${pad('map area', 11)}${pad('fit', 7)}opening state`);
  for (const r of rows) console.log(`  ${pad(r.tag, 11)}${pad(r.map, 11)}${pad(r.fit, 7)}${r.branch}`);
  const bad = rows.filter(r => r.errs.length);
  if (bad.length) for (const r of bad) console.log(`  ! ${r.tag}: ${r.errs.slice(0, 2).join(' | ')}`);
  console.log('');
  console.log('Nothing here is a check. Open the PNGs and use your judgement.');
})();
