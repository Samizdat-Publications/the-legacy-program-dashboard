// shoot.js — load a built dashboard, capture console errors, and screenshot every view.
// Verifying by looking is the point: a board that parses is not the same as a board that renders.
const { requirePlaywright, launchOptions } = require('./browser_env');
const { chromium } = requirePlaywright();
const path = require('path');

const FILE = process.argv[2] || path.resolve(__dirname, '..', 'dist', 'the-program.html');
const OUTDIR = process.argv[3] || path.resolve(__dirname, '..', 'dist', 'shots');
const TAG = process.argv[4] || 'program';

const VIEWS = ['NETWORK', 'TIMELINE', 'GEOGRAPHY', 'CASES', 'ANALYSIS', 'COVERUP', 'SEARCH', 'REPORT'];

(async () => {
  const browser = await chromium.launch(launchOptions());
  const page = await browser.newPage({ viewport: { width: 2550, height: 1465 }, deviceScaleFactor: 1 });

  const errors = [], warnings = [];
  page.on('console', m => {
    if (m.type() === 'error') errors.push(m.text().slice(0, 300));
    if (m.type() === 'warning') warnings.push(m.text().slice(0, 200));
  });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 400)));

  const t0 = Date.now();
  await page.goto('file://' + FILE, { waitUntil: 'load', timeout: 120000 });
  const loadMs = Date.now() - t0;

  // the force layout runs 900 steps before first paint; give it room
  await page.waitForTimeout(9000);

  const fps = await page.evaluate(() => new Promise(r => {
    const el = document.querySelector('.rmode');
    setTimeout(() => r(el ? el.textContent : 'no badge'), 4000);
  }));
  const stats = await page.evaluate(() => {
    const out = {};
    try {
      const B = window.__board || {}; out.nodes = B.NODES ? B.NODES.length : null;
      out.people = B.PEOPLE ? B.PEOPLE.length : null;
      out.edges = B.EDGES ? B.EDGES.length : null;
      out.programEdges = B.PROGRAM_EDGES ? B.PROGRAM_EDGES.length : null;
      out.timeline = B.TIMELINE ? B.TIMELINE.length : null;
      out.plateDegree = B.PLATE_DEGREE; out.plates = B.NODES ? B.NODES.filter(n=>(n.deg||0)>=B.PLATE_DEGREE && n.cls==='person').length : null; out.labelled = B.NODES ? B.NODES.filter(n=>(n.deg||0)>=6 && n.cls!=='person').length : null;
      out.views = B.VIEWS ? B.VIEWS : null;
      const c = document.querySelector('canvas');
      out.canvas = c ? { w: c.width, h: c.height, cssW: c.clientWidth, cssH: c.clientHeight } : null;
      // is anything actually drawn?
      if (c) {
        const ctx = c.getContext('2d');
        const d = ctx.getImageData(0, 0, c.width, c.height).data;
        let nonbg = 0;
        for (let i = 0; i < d.length; i += 4 * 97) {
          if (d[i] > 40 || d[i + 1] > 45 || d[i + 2] > 52) nonbg++;
        }
        out.canvasInk = nonbg;
        out.canvasSamples = Math.floor(d.length / (4 * 97));
      }
    } catch (e) { out.err = String(e); }
    return out;
  });

  const fs = require('fs');
  fs.mkdirSync(OUTDIR, { recursive: true });

  const shots = [];
  for (const v of VIEWS) {
    try {
      await page.evaluate(view => { if (window.__board) window.__board.CMD.setView(view); }, v);
      await page.waitForTimeout(v === 'NETWORK' ? 3500 : 1400);
      const p = path.join(OUTDIR, `${TAG}-${v.toLowerCase()}.png`);
      await page.screenshot({ path: p });
      shots.push(v);
    } catch (e) { errors.push(`view ${v}: ${e}`); }
  }

  // a selected node, to exercise the dock and the neighbourhood promotion
  try {
    await page.evaluate(() => { window.__board.CMD.setView('NETWORK'); window.__board.CMD.selectNode('david-grusch'); });
    await page.waitForTimeout(2600);
    await page.screenshot({ path: path.join(OUTDIR, `${TAG}-selected.png`) });
    shots.push('SELECTED');
  } catch (e) { errors.push('select: ' + e); }

  console.log(JSON.stringify({ loadMs, fps, stats, shots, errors: errors.slice(0, 25),
                               errorCount: errors.length, warningCount: warnings.length }, null, 1));
  await browser.close();
})();
