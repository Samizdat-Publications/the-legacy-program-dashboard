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
const { requirePlaywright, launchOptions } = require('./browser_env');
const { chromium } = requirePlaywright();
const fs = require('fs'), path = require('path');
const ROOT = path.dirname(__dirname);
const URL_ = process.env.BOARD_URL || 'http://127.0.0.1:8899/the-program.html';

(async () => {
  const browser = await chromium.launch(launchOptions({
  }));
  const page = await browser.newPage();
  await page.goto(URL_, { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(
    () => document.body && /ENTITIES/.test(document.body.innerText),
    null, { timeout: 180000 });

  /* THE PROGRAM MAP IS A TAB NOW, so its breadcrumb is no longer on screen at rest.
     Before the 29 August inversion the packed map WAS the NETWORK rest state and
     this file captured its crumb without navigating anywhere. Left alone, that
     would not have failed: `.l0crumb` would simply have been absent, the crumb
     would have dropped out of the strip, and audit_independent would have skipped
     `breadcrumb object count` in silence -- which is the exact failure the comment
     below already describes, and the exact shape CLAUDE.md section 5 is about.
     So: navigate, then REQUIRE the crumb. */
  await page.click('[data-view="PROGRAM"]');
  await page.waitForSelector('.l0wrap canvas', { timeout: 60000 });
  await page.waitForTimeout(2500);
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
    if (!crumb) return { err: 'the program map breadcrumb (.l0crumb) is not on the page' };
    parts.push(crumb.textContent.replace(/\s+/g, ' ').trim());
    return { strip: parts.join(' ') };
  });
  await browser.close();
  if (!strip) { console.error('capture_strip: could not find the stats strip'); process.exit(1); }
  if (strip.err) { console.error('capture_strip: ' + strip.err); process.exit(1); }
  fs.writeFileSync(path.join(ROOT, 'tools', 'runtime-strip.txt'), strip.strip + '\n');
  console.log(strip.strip);
})();
