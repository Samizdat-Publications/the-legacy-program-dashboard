/* The packed-cell layout, checked by reading the pixels it actually drew.
 *
 * WHY THIS EXISTS
 * ---------------
 * notes/PACKED-LAYOUT-COST-2026-08-25.md said a cloud session could not verify
 * this work, and gave a table of properties with "nothing here" in the second
 * column: chips overlapping, a band clipping, labels unreadable at the opening
 * fit, the map opening on empty space. The reason given was that mountL0 draws to
 * a canvas and tools/runtime_check.js reads the DOM.
 *
 * That reason was half right. runtime_check.js cannot read a canvas because it
 * asserts through text nodes. But getImageData can, in the same headless browser,
 * and the packed layout is the one surface where that is worth the trouble --
 * every chip's position is stated in data/l0-layout-model.json, so the drawn
 * pixels can be compared against an independent statement of where they belong
 * rather than against the renderer's own opinion.
 *
 * So this file does the thing the note said could not be done, for the properties
 * where it can be done, and says plainly which ones remain out of reach:
 *
 *   caught here      chips drawn at the model's coordinates, in the model's class
 *                    colours; no chip overlapping another on screen; the opening
 *                    view landing on chips rather than on empty world; the row and
 *                    column labels surviving a pan; the edge budget at rest; all
 *                    three options on; the canvas carrying ink at all
 *   NOT caught here  whether a truncated label is still a useful label, and
 *                    whether the whole thing looks good. Those need eyes.
 *
 * Every check below has a poison in --self-test, because CLAUDE.md section 5 is
 * about this exact file's ancestor: `canvasInk` reported zero ink on a visibly
 * drawing canvas and had never once fired.
 *
 * Run it:
 *   node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
 *   node tools/test_packed_layout.js
 *   node tools/test_packed_layout.js --self-test
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const URL = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';
const SELFTEST = process.argv.includes('--self-test');

/* ---- the assertions, as data ------------------------------------------------
 * Each one is a pure function of a probe taken from the page, so the SAME
 * function runs against the real probe and against a poisoned one. A check that
 * is only ever fed good input is the failure mode this repo keeps hitting; here
 * there is no second code path for it to hide in. */
const CHECKS = [
  {
    id: 'mounted',
    label: 'the program map mounts as the packed grid',
    test: p => p.hasCanvas && p.packedNodes === p.l0Nodes && p.l0Nodes > 0,
    detail: p => `canvas=${p.hasCanvas} packed=${p.packedNodes} l0=${p.l0Nodes}`,
    poison: p => ({ ...p, packedNodes: p.packedNodes - 1 }),
  },
  {
    id: 'geometry',
    label: 'every node carries a chip rect from the model',
    test: p => p.withRect === p.l0Nodes && p.distinctSizes === 1,
    detail: p => `${p.withRect}/${p.l0Nodes} with x,y,w,h · ${p.distinctSizes} chip size(s)`,
    /* Two sizes is the poison, not zero: size must never encode importance, and
       the way that rule breaks is one node quietly getting a bigger plate. */
    poison: p => ({ ...p, distinctSizes: 2 }),
  },
  {
    id: 'no-overlap',
    label: 'no chip overlaps another on screen',
    test: p => p.overlaps === 0,
    detail: p => `${p.overlaps} overlapping pairs of ${p.onScreen} on screen`,
    poison: p => ({ ...p, overlaps: 1 }),
  },
  {
    id: 'ink',
    label: 'the canvas is drawn on',
    /* An upper bound as well as a lower one. Zero ink is the historic bug; a
       canvas that is 100% ink is the other way to pass a naive version of this
       check, and it is what a single fillRect over the whole surface looks like. */
    test: p => p.inkPct >= 2 && p.inkPct <= 80,
    detail: p => `${p.inkPct}% of sampled pixels are content rather than ground`,
    poison: p => ({ ...p, inkPct: 0 }),
  },
  {
    id: 'chips-where-the-model-says',
    label: 'chips are drawn at the model coordinates, in their class colours',
    /* The load-bearing one. For each on-screen chip it samples the class rule at
       the chip's own left edge and asks whether that pixel is nearer the node's
       class colour than the chip fill. Shift the layout by a chip width and these
       samples land on band fill instead, so the count collapses. */
    test: p => p.classHits === p.classProbes && p.classUnprobed === 0
               && p.classProbes === p.l0Nodes,
    detail: p => `${p.classHits}/${p.classProbes} probes matched their class colour`
               + ` · ${p.classUnprobed} node(s) never reached by the camera`
               + (p.classMiss.length ? ' · missed ' + p.classMiss.slice(0, 6).join(' ') : ''),
    poison: p => ({ ...p, classHits: p.classProbes - 1 }),
  },
  {
    id: 'opens-on-content',
    label: 'the map opens on chips, not on empty world',
    test: p => p.openingChips >= 20 && p.labelsLegible,
    detail: p => `${p.openingChips} chips in the opening view · k=${p.k} · labels ${p.labelsLegible ? 'drawn' : 'DROPPED'}`,
    poison: p => ({ ...p, openingChips: 0 }),
  },
  {
    id: 'furniture-pinned',
    label: 'row and column labels survive a pan to the far corner',
    /* The rows are ordered by measured mean C and that order IS the argument, so
       a band label that scrolls away takes the argument with it. Panned to the
       bottom-right of a 2200x912 world, the gutter and head row must still carry
       ink -- which they only do because they are pinned to the viewport. */
    test: p => p.gutterInkPanned && p.headInkPanned,
    detail: p => `gutter=${p.gutterInkPanned} headRow=${p.headInkPanned} after pan`,
    poison: p => ({ ...p, gutterInkPanned: false }),
  },
  {
    id: 'edge-budget',
    label: 'the edges drawn at rest are the ones the model budgeted',
    test: p => p.restCount === p.restDrawnFigure && p.restCount < p.allEdges,
    detail: p => `${p.restCount} at rest vs figures.restDrawn ${p.restDrawnFigure}, of ${p.allEdges}`,
    poison: p => ({ ...p, restCount: p.allEdges }),
  },
  {
    id: 'options-on',
    label: 'all three view options ship on, each with a control',
    /* Stewart's call, 25 August 2026, having looked at the comp with all three
       on. If a later change flips a default this says so rather than letting the
       board quietly ship a different reading surface than the one signed off. */
    test: p => p.optRest && p.optFlags && p.optLabels && p.optControls === 3
               && p.controlsOn === 3,
    detail: p => `rest=${p.optRest} flags=${p.optFlags} labels=${p.optLabels}`
               + ` · ${p.controlsOn}/${p.optControls} controls lit`,
    poison: p => ({ ...p, optRest: false }),
  },
  {
    id: 'pointers-offset',
    label: 'start-here pointers are drawn beside chips, never on them',
    /* The flags must stay a separate layer. The moment the flag becomes a
       property of the chip it can be read as a tier, and AARO gets promoted by
       being pointed at. Probing the gutter strip to the LEFT of each flagged chip
       is how that separation is held to. */
    test: p => p.flagHits === p.flagProbes && p.flagProbes >= 3,
    detail: p => `${p.flagHits}/${p.flagProbes} flagged chips have amber ink offset to their left`
               + (p.flagMiss.length ? ' · no pointer on ' + p.flagMiss.join(' ') : ''),
    poison: p => ({ ...p, flagHits: 0 }),
  },
  {
    id: 'head-row-clear',
    label: 'no era column head is painted under the map controls',
    /* The eras are the horizontal argument exactly as the bands are the vertical
       one, and a head a reader cannot read takes its column's claim with it. */
    test: p => p.eraHeads >= 2 && p.headClear >= 0,
    detail: p => `${p.eraHeads} era heads · text starts ${p.headClear}px below the`
               + ` control row (strip ${p.headStrip}px, controls end at ${p.ctlBottom}px)`,
    poison: p => ({ ...p, headClear: -12 }),
  },
];

/* ---- probing the page ------------------------------------------------------ */
async function probe(page, opts = {}) {
  return await page.evaluate(async (o) => {
    const B = window.__board;
    const near = (px, hex, tol) => {
      const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
      return Math.abs(px[0] - r) + Math.abs(px[1] - g) + Math.abs(px[2] - b) <= tol;
    };
    const dist = (px, hex) => {
      const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
      return Math.abs(px[0] - r) + Math.abs(px[1] - g) + Math.abs(px[2] - b);
    };
    const CLS = {
      institution: '#a795e8', document: '#f0d264', program: '#66d69f',
      event: '#7fb4e8', legislation: '#e08ad0', person: '#c9d2dd',
      location: '#7fb4e8', domain: '#e08ad0',
    };
    const CHIP_FILL = '#12171d', AMBER = '#efb555';

    const D = B.L0DATA, PK = D.packed || {}, MAP = B.MAP;
    /* PAGE-LEVEL POISON. The predicate poisons at the bottom of this file prove
       each test() rejects bad input. They do NOT prove the probe measures the
       right pixels -- a probe that always returned the class colour would sail
       through them, which is precisely how six verify checks were once born
       broken and silently passing.

       So: snapshot the coordinates FIRST, then shift what the renderer draws, and
       keep measuring against the snapshot. The chips move; the expectation does
       not. Anything that still reports 110/110 is not reading the canvas. */
    const ORIG = {};
    for (const n of (D.l0 || [])) ORIG[n.id] = { x: n.x, y: n.y, w: n.w, h: n.h };
    if (o.shiftX) {
      for (const n of D.l0) n.x += o.shiftX;
      if (B.MAP) B.MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }
    const cvs = document.querySelector('.l0wrap canvas');
    const out = {
      hasCanvas: !!cvs,
      l0Nodes: (D.l0 || []).length,
      packedNodes: 0, withRect: 0, distinctSizes: 0,
      overlaps: 0, onScreen: 0, inkPct: 0,
      classProbes: 0, classHits: 0, classUnprobed: -1, classMiss: [],
      flagProbes: 0, flagHits: 0, flagMiss: [],
      openingChips: 0, labelsLegible: false, k: 0,
      gutterInkPanned: false, headInkPanned: false,
      restCount: (PK.rest || []).length,
      restDrawnFigure: o.restDrawnFigure,
      allEdges: (D.directEdges || []).length + (D.summarised || []).length,
      optRest: false, optFlags: false, optLabels: false,
      optControls: 0, controlsOn: 0,
    };
    if (!cvs || !MAP) return out;

    const sizes = new Set();
    for (const n of D.l0) {
      if (n.x != null && n.y != null && n.w && n.h) { out.withRect++; sizes.add(n.w + 'x' + n.h); }
    }
    out.packedNodes = out.withRect;
    out.distinctSizes = sizes.size;

    const v = MAP.view;
    out.k = Math.round(v.k * 100) / 100;
    out.optRest = !!MAP.opt.rest; out.optFlags = !!MAP.opt.flags;
    out.optLabels = !!MAP.opt.labels;
    const ctrls = [...document.querySelectorAll('.l0ctl [data-opt]')];
    out.optControls = ctrls.length;
    out.controlsOn = ctrls.filter(b => b.className.indexOf('on') >= 0).length;

    const host = cvs.parentElement.getBoundingClientRect();
    const Wc = host.width, Hc = host.height;
    /* The map reserves these two strips for the row and column labels and clips
       itself out of them, so a "visible" chip means visible in the CONTENT rect.
       Counting the chrome as map is how the first cut of this file managed to
       probe six chips that the renderer had correctly refused to draw there. */
    /* geo is published at PK.config.geo. This file read PK.geo -- undefined --
       and fell through to the literals below, which happened to match while the
       renderer had the same bug. When geo.headRow moved from 46 to 76 the check
       went on measuring a 46px strip and agreed with a renderer it was no longer
       describing. A check that shares the implementation's mistake cannot see it. */
    const geo0 = (PK.config || {}).geo || PK.geo || { gutter: 148, headRow: 46 };
    const PADL = geo0.gutter, PADT = geo0.headRow;
    const rect = n => { const g = ORIG[n.id] || n;
      return { x: g.x * v.k + v.ox, y: g.y * v.k + v.oy,
               w: g.w * v.k, h: g.h * v.k }; };
    const vis = D.l0.map(n => ({ n, r: rect(n) }))
      .filter(({ r }) => r.x >= PADL && r.y >= PADT && r.x + r.w <= Wc && r.y + r.h <= Hc);
    out.onScreen = vis.length;
    out.openingChips = vis.length;
    out.labelsLegible = MAP.opt.labels && v.k >= 0.62;

    for (let i = 0; i < vis.length; i++) {
      for (let j = i + 1; j < vis.length; j++) {
        const a = vis[i].r, b = vis[j].r;
        if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h)
          out.overlaps++;
      }
    }

    const ctx = cvs.getContext('2d');
    const dpr = cvs.width / Wc;
    const px = (cx, cy) => {
      const d = ctx.getImageData(Math.round(cx * dpr), Math.round(cy * dpr), 1, 1).data;
      return [d[0], d[1], d[2]];
    };

    /* Ink means CONTENT ink. Counting any opaque pixel would score 95% on a
       canvas painted entirely in band fills with not one chip on it, which is the
       exact shape of the bug this check exists for -- `canvasInk` once reported
       zero on a drawing canvas and had never fired either way. So the grounds are
       named and excluded, and what is left is chips, edges, labels and furniture. */
    const GROUNDS = ['#141920', '#12161c', '#11141a', '#12171d'];
    let inked = 0, total = 0;
    const grid = ctx.getImageData(0, 0, cvs.width, cvs.height).data;
    for (let y = 0; y < cvs.height; y += 4) {
      for (let x = 0; x < cvs.width; x += 4) {
        const i = (y * cvs.width + x) * 4;
        total++;
        if (grid[i + 3] < 8) continue;
        const q = [grid[i], grid[i + 1], grid[i + 2]];
        if (GROUNDS.every(g => dist(q, g) > 14)) inked++;
      }
    }
    out.inkPct = total ? Math.round(inked / total * 100) : 0;

    /* The class rule runs down the chip's left edge, 3px wide at k=1. Column x is
       the border stroke, so x+1 is the first pixel of the rule itself.
       The camera is walked across the whole world in overlapping steps so that
       EVERY node gets probed, not only the ~32 that happen to be in the opening
       view. A layout bug that spares the top-left corner and wrecks the 2017-2026
       column is exactly the kind a single-viewport check waves through. */
    const FLAGS = new Set(PK.flags || []);
    const seen = new Set();
    /* Integral camera steps ON PURPOSE. At a fractional offset the chip's 3px
       class rule lands across pixel boundaries and antialiases into the chip fill,
       and the probe then measures the browser's blending rather than the
       renderer's placement. The rule being sampled is 3px wide; the check is about
       where it is, not how it resolves at a half-pixel. */
    /* The camera is aimed at each node in turn rather than swept in a grid.
       A grid sweep left 20 nodes unreached at the world's right and bottom edges
       once the frozen chrome narrowed the content rect -- and a check that quietly
       skips the far column is worse than no check, because the far column is
       2017-2026, the densest part of the board. */
    for (const target of D.l0) {
      if (seen.has(target.id)) continue;
      v.ox = Math.round((PADL + Wc) / 2 - (target.x + target.w / 2) * v.k);
      v.oy = Math.round((PADT + Hc) / 2 - (target.y + target.h / 2) * v.k);
      MAP.repaint();
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      {
        for (const n of D.l0) {
          if (seen.has(n.id)) continue;
          const r = rect(n);
          if (r.x < PADL + 2 || r.y < PADT + 2
              || r.x + r.w > Wc - 2 || r.y + r.h > Hc - 2) continue;
          seen.add(n.id);
          const want = CLS[n.cls] || CLS.person;
          const q = px(r.x + 1.5, r.y + r.h / 2);
          out.classProbes++;
          if (dist(q, want) < dist(q, CHIP_FILL)) out.classHits++;
          else out.classMiss.push(n.id + ':' + n.cls + ':' + q.join(','));
          if (FLAGS.has(n.id) && r.x > 20) {
            out.flagProbes++;
            let hit = false;
            for (let d = 4; d <= 15 && !hit; d++) {
              if (near(px(r.x - d, r.y + r.h / 2), AMBER, 90)) hit = true;
            }
            if (hit) out.flagHits++; else out.flagMiss.push(n.id);
          }
        }
      }
    }
    out.classUnprobed = D.l0.length - seen.size;

    /* The start-here pointer sits in the gap to the LEFT of the chip, between
       9 and 14px out. Amber there and nowhere on the chip is the separation. */

    /* Pan to the far bottom-right of the world and look again at the two strips
       the model reserves for furniture: geo.gutter on the left, geo.headRow on
       top. World-space labels would have left the viewport by now. */
    v.ox = -(PK.worldW * v.k - Wc) - 4;
    v.oy = -(PK.worldH * v.k - Hc) - 4;
    MAP.repaint();
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    /* LABEL ink specifically. The strips are painted opaque so nothing shows
       through them, which means "the strip has ink" would pass on an empty strip.
       What must be true is that TEXT is on them, so this counts only pixels that
       differ from the strip's own ground, and stays clear of the two 1px rules at
       the strip borders so a rule alone cannot carry the check. */
    const STRIP_BG = '#11141a';
    const strip = (x0, y0, x1, y1) => {
      let n = 0;
      for (let y = y0; y < y1; y += 2)
        for (let x = x0; x < x1; x += 2) if (dist(px(x, y), STRIP_BG) > 30) n++;
      return n;
    };
    out.gutterInkPanned = strip(6, PADT + 2, PADL - 14, Hc - 2) > 20;
    out.headInkPanned = strip(PADL + 2, 4, Wc - 2, PADT - 14) > 20;

    /* The head strip is shared: the canvas paints the era labels on it and the
       map's own DOM controls (.l0crumb, .l0ctl) are positioned on top of it. Ink
       alone cannot see the difference -- headInkPanned above passed happily for
       the whole of the first build, while two of the five era heads were drawn
       underneath PROGRAM MAP and LINES AT REST and rendered as a smear. So
       measure the CLEARANCE: the lowest pixel any control occupies, against the
       highest pixel the era label reaches. mountL0 draws that label on the
       baseline PAD.t - 22, and 9px covers the cap height of its 9px face. */
    const wrapEl = document.querySelector('.l0wrap');
    const wrTop = wrapEl.getBoundingClientRect().top;
    let ctlBottom = 0;
    for (const el of document.querySelectorAll('.l0crumb, .l0crumb *, .l0ctl, .l0ctl *')) {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      ctlBottom = Math.max(ctlBottom, r.bottom - wrTop);
    }
    out.ctlBottom = Math.round(ctlBottom);
    out.headStrip = PADT;
    out.headClear = Math.round((PADT - 22 - 9) - ctlBottom);
    out.eraHeads = (PK.eras || []).length;

    if (o.shiftX) {           /* put the board back the way it was found */
      for (const n of D.l0) n.x = ORIG[n.id].x;
      if (B.MAP) B.MAP.repaint();
    }
    return out;
  }, opts);
}

(async () => {
  const layout = JSON.parse(fs.readFileSync(
    path.join(ROOT, 'data', 'l0-layout-model.json'), 'utf8'));
  const restDrawnFigure = layout.current.figures.restDrawn;

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message.slice(0, 200)));

  await page.goto(URL, { waitUntil: 'load', timeout: 180000 });
  await page.waitForSelector('[data-view="CASES"]', { timeout: 120000 });
  await page.waitForTimeout(6000);

  /* The map is the rest state of the NETWORK view, and the entry surface sits on
     top of it until a reader picks a way in. Both have to be got past before
     there is a canvas to read. */
  await page.click('[data-view="NETWORK"]');
  await page.waitForTimeout(2500);
  const skip = await page.$('.l0entry [data-entry-skip], .l0entry [data-skip]');
  if (skip) { await skip.click(); await page.waitForTimeout(1200); }
  else {
    await page.evaluate(() => {
      const e = document.querySelector('.l0entry');
      if (e) e.remove();
    });
  }
  await page.waitForSelector('.l0wrap canvas', { timeout: 30000 });
  await page.waitForTimeout(1500);

  const p = await probe(page, { restDrawnFigure });

  const hard = errs.filter(e => !/font|ERR_CONNECTION_RESET|404|favicon/i.test(e));
  const lines = [], fails = [];
  const record = (pass, label, detail) => {
    lines.push(`${pass ? 'ok  ' : 'FAIL'}  ${label}${detail ? ' :: ' + detail : ''}`);
    if (!pass) fails.push(label);
  };
  record(hard.length === 0, 'no page errors while the map is mounted',
         hard.slice(0, 2).join(' | '));
  for (const c of CHECKS) record(c.test(p), c.label, c.detail(p));

  console.log(lines.join('\n'));

  if (SELFTEST) {
    /* Every check, shown rejecting the input it exists to reject. A check that has
       never been demonstrated failing is indistinguishable from a broken one, and
       the poison is applied to the probe rather than to the page so that the SAME
       predicate is exercised both ways. */
    console.log('\n--- self-test: each check against input it must reject ---');
    let bad = 0;
    for (const c of CHECKS) {
      const poisoned = c.poison(p);
      const stillPasses = c.test(poisoned);
      console.log(`${stillPasses ? 'BROKEN' : 'ok    '}  ${c.id} rejects its poison`);
      if (stillPasses) bad++;
    }
    /* And the one that matters most, run against the real page rather than against
       a doctored object: move every chip 60px right of where the check expects it
       and require the pixel probe to notice. */
    console.log('\n--- self-test: the pixel probe against a moved layout ---');
    const shifted = await probe(page, { restDrawnFigure, shiftX: 60 });
    const noticed = !CHECKS.find(c => c.id === 'chips-where-the-model-says').test(shifted);
    console.log(`${noticed ? 'ok    ' : 'BROKEN'}  the probe reads the canvas`
      + ` :: ${shifted.classHits}/${shifted.classProbes} still matched after a 60px shift`);
    if (!noticed) bad++;

    /* And the head strip, poisoned on the page rather than in the object: put the
       control row back where it used to sit relative to the labels and require the
       clearance check to collapse. This is the defect itself, reproduced. */
    console.log('\n--- self-test: the head strip against a control row moved onto it ---');
    await page.addStyleTag({ content: '.l0ctl{top:44px !important}' });
    await page.waitForTimeout(400);
    const collided = await probe(page, { restDrawnFigure });
    const caught = !CHECKS.find(c => c.id === 'head-row-clear').test(collided);
    console.log(`${caught ? 'ok    ' : 'BROKEN'}  the clearance check sees a control row on the labels`
      + ` :: clearance became ${collided.headClear}px`);
    if (!caught) bad++;

    if (bad) { console.error(`\n${bad} check(s) accept input they must reject`); process.exit(1); }
    console.log('all checks reject their poison');
  }

  await browser.close();
  if (fails.length) {
    console.error(`\n${fails.length} FAILED: ${fails.join(' | ')}`);
    process.exit(1);
  }
  console.log(`\nPACKED LAYOUT CHECK PASSED — ${CHECKS.length + 1} assertions`);
})().catch(e => { console.error(e); process.exit(1); });
