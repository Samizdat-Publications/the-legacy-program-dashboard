/* Walk the board. Click everything, screenshot each state, report what looks wrong.
 *
 * WHY THIS EXISTS
 * ---------------
 * notes/HANDOFF-2026-08-26-UX.md section 5 asked for this by name. Stewart's
 * question was what would let a session "click everything, see how it looks, write
 * notes", and the answer was that nothing needed downloading -- Playwright and
 * Chromium are already here -- what was missing was a harness.
 *
 * tools/look.js photographs a handful of states somebody chose in advance.
 * Every defect Stewart has reported was in a state nobody chose in advance:
 *
 *   - the era heads printing through the toolbar, which needs an entry path OPEN
 *     (its chip widens the left group) and the dossier OUT (it squeezes the row)
 *     before `.l0ctl` wraps far enough to overlap them
 *   - the dossier at half the window, which only shows once something is selected
 *   - FIT landing in the count matrix, which depends on the window size
 *
 * One state each, and no check was looking at any of them. This file enumerates
 * the controls and visits them instead of guessing which ones matter.
 *
 * WHAT IT IS AND IS NOT
 * ---------------------
 * A CAMERA WITH A NOTEBOOK. It asserts nothing, exits 0 whatever it finds, and must
 * never enter the gate. Its findings are leads for a human, not verdicts: an
 * "overlap" here may be a deliberate stack, and a "clipped" element may be a label
 * that is meant to ellipsize. tools/test_packed_layout.js is where a finding goes
 * once somebody has looked and decided it is real.
 *
 * The two columns that earn it are OVERLAP and MAP SHARE. Both are what Stewart
 * sees and neither is visible from reading source.
 *
 * THE HONEST LIMIT, unchanged from look.js: a screenshot is one moment, captures
 * are at deviceScaleFactor 2 so small type reads larger than it will on a 1x
 * monitor, and nothing here can say whether the board READS. It widens the net.
 * It does not replace Stewart looking.
 *
 * Run it:
 *   node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
 *   node tools/walk.js
 *   node tools/walk.js --size 1366x768 --out /tmp/walk
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const URL = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';
const argv = process.argv.slice(2);
const argOf = f => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };
const OUT = argOf('--out') || path.join(ROOT, 'dist', 'shots', 'walk');
const SIZE = (argOf('--size') || '1600x900').split('x').map(Number);

/* The controls, in the order a reader meets them. `pre` runs before the click and
 * is how a state that needs setting up gets set up -- the wrapping control row
 * needs a path open AND a selection, and no amount of clicking one button reaches
 * it. */
const STOPS = [
  { id: 'load',        label: 'the board as it opens' },
  { id: 'start',       label: 'the START menu',            sel: '[data-entry]' },
  { id: 'path-money',  label: 'follow the money',          sel: '[data-path="money"]' },
  /* The entry surface closes when a path is picked, so the second path needs the
     START menu reopening first. */
  { id: 'path-custody',label: 'the custody chain',         sel: '[data-path="custody"]',
                       pre: '[data-entry]' },
  { id: 'fit',         label: 'FIT',                       sel: '.l0ctl [data-fit]' },
  { id: 'fitall',      label: 'FIT ALL',                   sel: '.l0ctl [data-fitall]' },
  { id: 'one',         label: '1:1',                       sel: '.l0ctl [data-one]' },
  { id: 'opt-rest',    label: 'LINES AT REST off',         sel: '.l0ctl [data-opt="rest"]' },
  { id: 'opt-flags',   label: 'START HERE off',            sel: '.l0ctl [data-opt="flags"]' },
  { id: 'opt-labels',  label: 'LABELS off',                sel: '.l0ctl [data-opt="labels"]' },
  { id: 'opt-cells',   label: 'CELLS on',                  sel: '.l0ctl [data-opt="cells"]' },
  { id: 'opt-cells-off', label: 'CELLS off again',         sel: '.l0ctl [data-opt="cells"]' },
  { id: 'select',      label: 'a node selected',           run: 'CMD.selectNode("aawsap")' },
  { id: 'wrapped',     label: 'path open AND dossier out — the row wraps',
                       run: 'CMD.openPath("money")' },
  /* Re-select first: openPath clears the selection, which folds the dossier by the
     rule in renderDock, so there is no fold tab to click until something is picked
     again. */
  { id: 'fold',        label: 'the dossier folded by its tab', sel: '.dock-fold',
                       run: 'CMD.selectNode("aatip")' },
  { id: 'legend',      label: 'the legend',                sel: '[data-legend="toggle"]' },
  /* EVERY STOP BELOW NEEDS THE RAIL BACK. FIT ALL folds it -- that is the point of
     FIT ALL -- and a folded rail takes the view list with it, so Playwright reports
     "element is not visible" and the walk quietly stops covering half the board.
     Worth knowing as a fact about the board, not just about the walker: after FIT
     ALL the only way back to the views is the header's Rail button. */
  { id: 'view-timeline', label: 'TIMELINE',                sel: '[data-view="TIMELINE"]',
                         pre: '#railbtn' },
  { id: 'view-coverup',  label: 'THE COVER-UP',            sel: '[data-view="COVERUP"]' },
  { id: 'view-report',   label: 'REPORT',                  sel: '[data-view="REPORT"]' },
  { id: 'view-network',  label: 'back to NETWORK',         sel: '[data-view="NETWORK"]' },
];

/* Everything measured after a click, in one pass in the page. */
const INSPECT = () => {
  const out = { errors: [], overlaps: [], clipped: [], scale: null, mapShare: null,
                offscreen: [] };
  const R = e => e.getBoundingClientRect();
  const named = e => (e.getAttribute('data-view') || e.getAttribute('data-opt')
    || e.getAttribute('data-path') || (e.className && String(e.className).split(' ')[0])
    || e.tagName).slice(0, 28) + '"' + (e.textContent || '').trim().slice(0, 18) + '"';

  /* INTERACTIVE RECTS THAT SIT ON EACH OTHER. Two controls a reader can both aim
     at, occupying the same pixels, is the defect class Stewart keeps reporting and
     the one no unit check looks for. Only visible, non-nested pairs count: a button
     inside a toolbar overlaps its toolbar by construction. */
  /* VISIBLE MEANS VISIBLE RIGHT NOW, INCLUDING CLIPPING.
     The first run of this file reported 33 overlaps in THE COVER-UP view and eight
     controls "outside the window", and every one was wrong. They were the left
     rail's filter chips, sitting below the fold of `.rail-scroll` -- a container
     with overflow-y:auto, scrollHeight 943 against clientHeight 363, working
     exactly as intended. getBoundingClientRect reports where a scrolled-away
     element WOULD be, so the raw rects put them on top of the analyst's suggestion
     chips and off the bottom of the screen. Nothing was wrong with the board.

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
  const hits = [...document.querySelectorAll(
    'button,[role=button],a[href],[data-view],[data-opt],[data-path],[data-entry],'
    + '[data-fit],[data-fitall],[data-one],[data-legend],[data-dockfold],[data-dockoff]')]
    .filter(visibleNow);
  for (let i = 0; i < hits.length; i++) {
    for (let j = i + 1; j < hits.length; j++) {
      const a = hits[i], b = hits[j];
      if (a.contains(b) || b.contains(a)) continue;
      const ra = R(a), rb = R(b);
      const ox = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
      const oy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
      if (ox > 2 && oy > 2)
        out.overlaps.push(`${named(a)} × ${named(b)} (${Math.round(ox)}×${Math.round(oy)}px)`);
    }
  }

  /* TEXT CUT OFF BY ITS OWN BOX. scrollWidth beyond clientWidth on an element that
     is not a scroller. Ellipsis is legitimate and common here, so this is a lead. */
  for (const e of document.querySelectorAll('button,.l0chip,.eyebrow,.turn-t,.cl,h1,h2,h5')) {
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
  const scrollableAncestor = e => {
    for (let a = e.parentElement; a && a !== document.documentElement; a = a.parentElement) {
      const acs = getComputedStyle(a);
      if (/auto|scroll/.test(acs.overflowY + acs.overflowX)
          && (a.scrollHeight > a.clientHeight + 2 || a.scrollWidth > a.clientWidth + 2))
        return true;
    }
    return false;
  };
  for (const e of hits) {
    const r = R(e);
    if ((r.right < 0 || r.bottom < 0 || r.left > innerWidth || r.top > innerHeight)
        && !scrollableAncestor(e))
      out.offscreen.push(named(e));
  }

  /* HOW MUCH OF THE WINDOW THE MAP ACTUALLY HAS. The number behind "you never
     actually get to see the full map". */
  const wrap = document.querySelector('.l0wrap');
  if (wrap) {
    const r = R(wrap);
    out.mapShare = Math.round(100 * (r.width * r.height) / (innerWidth * innerHeight));
    out.mapBox = Math.round(r.width) + '×' + Math.round(r.height);
  }
  try { out.scale = +window.__board.MAP.view.k.toFixed(3); } catch (e) {}
  try { out.cells = !!window.__board.MAP.opt.cells; } catch (e) {}
  return out;
};

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  });
  const page = await browser.newPage({ viewport: { width: SIZE[0], height: SIZE[1] } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e.message).slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });

  await page.goto(URL, { waitUntil: 'load', timeout: 180000 });
  await page.waitForSelector('[data-view="CASES"]', { timeout: 120000 });
  await page.waitForTimeout(6000);
  await page.click('[data-view="NETWORK"]');
  await page.waitForTimeout(3000);

  const rows = [];
  let n = 0;
  for (const stop of STOPS) {
    n++;
    const before = errors.length;
    let reached = true;
    try {
      if (stop.pre) {
        const pe = await page.$(stop.pre);
        if (pe) { await pe.click({ force: true }); await page.waitForTimeout(1200); }
      }
      if (stop.run) {
        await page.evaluate(js => eval('window.__board.' + js), stop.run);
        await page.waitForTimeout(1200);
      }
      if (stop.sel) {
        const el = await page.$(stop.sel);
        if (el) await el.click({ force: true });
        else reached = false;
      }
    } catch (e) { reached = false; errors.push(`${stop.id}: ${String(e).slice(0, 120)}`); }
    await page.waitForTimeout(stop.sel && /view/.test(stop.id) ? 2200 : 1500);

    const tag = String(n).padStart(2, '0') + '-' + stop.id;
    await page.screenshot({ path: path.join(OUT, tag + '.png') });
    const info = await page.evaluate(INSPECT);
    rows.push({ tag, label: stop.label, reached, info,
                newErrors: errors.slice(before) });
    process.stdout.write(`${tag}  ${reached ? '' : '(not reached) '}`
      + `map ${info.mapShare}% ${info.mapBox}  k=${info.scale}`
      + `  overlaps ${info.overlaps.length}  clipped ${info.clipped.length}\n`);
  }

  /* THE REPORT. A table first, because the point is to scan it. */
  const esc = s => String(s).replace(/\|/g, '\\|');
  let md = `# Walk of the board\n\n`;
  md += `Captured at ${SIZE[0]}x${SIZE[1]} from \`${URL}\`. `;
  md += `${rows.length} states.\n\n`;
  md += `**This file asserts nothing.** Every row is a lead for somebody to look at, not\n`;
  md += `a verdict. An overlap may be a deliberate stack; a clipped element may be a label\n`;
  md += `that is meant to ellipsize. What it is good at is finding the states nobody\n`;
  md += `thought to check.\n\n`;
  md += `| # | state | map share | scale | cells | overlaps | clipped | offscreen | errors |\n`;
  md += `|---|---|---|---|---|---|---|---|---|\n`;
  for (const r of rows) {
    md += `| ${r.tag} | ${esc(r.label)}${r.reached ? '' : ' **(control not found)**'} `
       + `| ${r.info.mapShare == null ? '-' : r.info.mapShare + '% ' + r.info.mapBox} `
       + `| ${r.info.scale == null ? '-' : r.info.scale} `
       + `| ${r.info.cells === undefined ? '-' : (r.info.cells ? 'ON' : 'off')} `
       + `| ${r.info.overlaps.length} | ${r.info.clipped.length} `
       + `| ${r.info.offscreen.length} | ${r.newErrors.length} |\n`;
  }
  const detail = rows.filter(r => r.info.overlaps.length || r.newErrors.length
                                || r.info.offscreen.length);
  if (detail.length) {
    md += `\n## What to look at\n`;
    for (const r of detail) {
      md += `\n### ${r.tag} — ${r.label}\n\n![${r.tag}](${r.tag}.png)\n\n`;
      if (r.info.overlaps.length) {
        md += `**Interactive rects overlapping (${r.info.overlaps.length}):**\n\n`;
        for (const o of r.info.overlaps.slice(0, 12)) md += `- ${esc(o)}\n`;
        if (r.info.overlaps.length > 12) md += `- …and ${r.info.overlaps.length - 12} more\n`;
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
    md += `\n No overlaps, no offscreen controls and no console errors in any state.\n`;
  }
  const worst = rows.reduce((a, b) => (b.info.mapShare || 0) < (a.info.mapShare || 0) ? b : a);
  md += `\n## Map share\n\nSmallest the map got: **${worst.info.mapShare}%** of the window `;
  md += `at \`${worst.tag}\` (${worst.label}).\n`;

  fs.writeFileSync(path.join(OUT, 'REPORT.md'), md);
  console.log(`\n${rows.length} states -> ${OUT}\nREPORT.md written`);
  await browser.close();
})();
