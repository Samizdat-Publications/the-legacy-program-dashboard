#!/usr/bin/env node
/**
 * probe_browser.js -- does THIS machine have what the four browser gate steps need?
 *
 *   node tools/probe_browser.js
 *
 * This is a PROBE, not a check. It asserts nothing about the board and is not part
 * of the gate. It answers one question the self-tested resolver test deliberately
 * cannot: `test_browser_env.js` builds synthetic `pwfake-*` fixtures precisely so it
 * needs no browser, so passing it proves the RESOLVER is right and proves nothing
 * about whether Playwright and a Chromium are actually installed here.
 *
 * `describe()` printing "(Playwright default)" is not a failure. It means our
 * resolver found no explicit binary and is ceding to Playwright's own cache --
 * which is the correct answer on a normal `npm i playwright` install, where the
 * browsers live under the platform default (%LOCALAPPDATA%\ms-playwright on
 * Windows) that PLAYWRIGHT_BROWSERS_PATH does not name. The only way to know is
 * to launch one, so this launches one.
 */
'use strict';

const { requirePlaywright, describe, httpServerBin } = require('./browser_env');

(async () => {
  let pw;
  try {
    pw = requirePlaywright();
  } catch (e) {
    console.log('FAIL  Playwright module:');
    for (const line of String(e.message).split('\n')) console.log('      ' + line);
    console.log('\n      Fix: npm i playwright');
    console.log('      Then: npx playwright install chromium');
    process.exit(1);
  }
  console.log('ok    Playwright module loaded');
  console.log('      ' + describe());

  let browser;
  try {
    browser = await pw.chromium.launch({ args: ['--no-sandbox'] });
  } catch (e) {
    console.log('FAIL  chromium.launch: ' + e.message.split('\n')[0]);
    console.log('\n      Fix: npx playwright install chromium');
    process.exit(1);
  }
  console.log('ok    chromium launched, version ' + browser.version());

  const page = await browser.newPage();
  await page.setContent('<p id="x">probe</p>');
  const got = await page.$eval('#x', el => el.textContent);
  await browser.close();
  if (got !== 'probe') {
    console.log('FAIL  DOM read back ' + JSON.stringify(got) + ', expected "probe"');
    process.exit(1);
  }
  console.log('ok    page loaded and DOM read back through the same channel the gate uses');

  const hs = httpServerBin();
  console.log(hs ? 'ok    http-server: ' + hs
                 : 'note  http-server not installed locally; the browser steps will need');
  if (!hs) console.log('      npx http-server dist -p 8899 --silent   in a second window.');

  console.log('\nThe four browser gate steps can run on this machine.');
})();
