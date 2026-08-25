/*
 * capture_strip.js — writes tools/runtime-strip.txt from the built board.
 *
 * audit_independent.py compares the figures a reader ACTUALLY SEES against its own
 * re-derivation. It cannot read them out of dist/the-program.html, because the stats
 * strip is assembled by script at runtime. So the strip has to come off a real DOM.
 *
 * The file this writes is a CAPTURE, not a source. Regenerate it whenever the board
 * is rebuilt; a stale capture makes the audit report a data defect that is really
 * just an old file. That has already happened once, on 25 August 2026, and cost a
 * handoff two "findings" that were not there.
 *
 * The board is wrapped in an IIFE, so page internals are unreachable from evaluate().
 * Read the DOM. And file:// does not work for a 13MB page: serve it over HTTP.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.dirname(__dirname);
const URL_ = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  });
  const page = await browser.newPage();
  await page.goto(URL_, { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(
    () => document.body && /ENTITIES/.test(document.body.innerText),
    null, { timeout: 180000 });
  const strip = await page.evaluate(() => {
    const el = document.querySelector('.stats') ||
               [...document.querySelectorAll('div')]
                 .find(d => /ENTITIES/.test(d.textContent) && d.textContent.length < 600);
    if (!el) return null;
    const parts = [el.textContent.replace(/\s+/g, ' ').trim()];
    // The L0 breadcrumb is a SEPARATE element from the stats strip, and it carries the
    // only rendered copy of the program-map object count. Leaving it out does not fail
    // the audit -- it makes audit_independent skip `breadcrumb object count` in silence,
    // which is how that check sat dead while the count was wrong.
    const crumb = document.querySelector('.l0crumb');
    if (crumb) parts.push(crumb.textContent.replace(/\s+/g, ' ').trim());
    return parts.join(' ');
  });
  await browser.close();
  if (!strip) { console.error('capture_strip: could not find the stats strip'); process.exit(1); }
  fs.writeFileSync(path.join(ROOT, 'tools', 'runtime-strip.txt'), strip + '\n');
  console.log(strip);
})();
