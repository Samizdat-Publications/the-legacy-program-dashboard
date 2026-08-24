/* Runtime verification of dist/the-program.html, in a real browser.
 *
 * WHY THIS EXISTS, separately from tools/verify.py.
 *
 * verify.py asserts properties of the DATA. This asserts what the BROWSER
 * renders, because on this board the two have come apart badly. Every one of the
 * eleven sequence chains rendered the word "undefined" under an undefined date,
 * on Grusch, Elizondo, Davis, Puthoff and Marcel among others, while every count
 * in the gate was correct and nothing threw. Fifty-four affiliations printed raw
 * slugs like "dod-sapco" where an institution's name belonged. Neither defect is
 * visible to a check that reads JSON.
 *
 * NOTE: the board is wrapped in an IIFE, so NODES, CMD, chainHtml and tabDossier
 * are module-private and CANNOT be reached from page.evaluate. That is correct
 * design and it is why every assertion here goes through the DOM and through
 * real clicks, which is what a reader actually gets.
 *
 * Run it:
 *   node /opt/node22/lib/node_modules/http-server/bin/http-server dist -p 8899 --silent &
 *   node tools/runtime_check.js
 *
 * file:// does not work for this page -- a 13MB document served over file://
 * never finished parsing in the container. Serve it over HTTP.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const URL = process.argv[2] || 'http://127.0.0.1:8899/the-program.html';
const SHOTS = process.env.RUNTIME_SHOTS || '';

const fails = [], ok = [];
const check = (c, label, detail = '') => {
  (c ? ok : fails).push(`${c ? 'ok  ' : 'FAIL'}  ${label}${detail ? ' :: ' + detail : ''}`);
};

(async () => {
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message.slice(0, 160)));
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text().slice(0, 160)); });

  await page.goto(URL, { waitUntil: 'load', timeout: 180000 });
  await page.waitForSelector('[data-view="CASES"]', { timeout: 120000 });
  await page.waitForTimeout(8000);

  // A font CDN failure offline is expected and documented; anything else is not.
  const hard = errs.filter(e => !/font|ERR_CONNECTION_RESET|404|favicon/i.test(e));
  check(hard.length === 0, 'no unexplained console errors', hard.slice(0, 2).join(' | '));

  // The stats strip is the board's own claim about itself. If it disagrees with
  // the data, the merge and the build have diverged.
  //
  // The expected values are READ FROM tools/GOLDEN.json rather than written here.
  // The first version of this file hardcoded them and went stale the moment two
  // claims were added, which made the check fail on a correct build -- a check
  // that cries wolf gets switched off, and then it is no check. Golden is already
  // the one place where a count change has to be accepted deliberately, so it is
  // the right source of truth for this too.
  const g = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools', 'GOLDEN.json'), 'utf8')).counts;
  const expEntities = g.people + g.entities;
  const expClaims = Object.values(g.claim_tiers).reduce((a, b) => a + b, 0);
  const strip = await page.evaluate(() => document.body.innerText.slice(0, 700));
  const num = re => { const m = strip.match(re); return m ? m[1] : '?'; };
  check(num(/ENTITIES\s+(\d+)/) === String(expEntities), 'stats strip ENTITIES',
        `${num(/ENTITIES\s+(\d+)/)} vs golden ${expEntities}`);
  check(num(/SOURCED LINKS\s+(\d+)/) === String(g.edges), 'stats strip SOURCED LINKS',
        `${num(/SOURCED LINKS\s+(\d+)/)} vs golden ${g.edges}`);
  check(num(/of (\d+) claims/) === String(expClaims), 'stats strip claim total',
        `${num(/of (\d+) claims/)} vs golden ${expClaims}`);
  check(num(/Case files\s*\.*\s*(\d+)/) === String(g.people), 'CASE FILES count',
        `${num(/Case files\s*\.*\s*(\d+)/)} vs golden ${g.people}`);

  await page.click('[data-view="CASES"]');
  await page.waitForTimeout(2500);
  const cases = await page.evaluate(() => document.body.innerText);
  check(/278 of 278 records shown/.test(cases), 'case view shows every record');
  check(!/jesse-marcel-sr|ndaa24-sec1687|aaro-fy2025-report\b/.test(cases),
        'ids collapsed on 22 Aug do not reappear');
  check(!/Re-pointed from a collapsed duplicate/.test(cases),
        'no build placeholder is shown to a reader');

  // Open a dossier that carries a rebuilt sequence chain.
  await page.evaluate(() => {
    const e = [...document.querySelectorAll('*')]
      .filter(x => x.children.length === 0 && /Grusch/.test(x.textContent || ''))[0];
    let n = e; for (let i = 0; i < 6 && n; i++) { n.click(); n = n.parentElement; }
  });
  await page.waitForTimeout(3000);

  // THE SEQUENCE CHAIN. Before the 22 Aug fix every step here read "undefined".
  const chain = await page.evaluate(() => {
    const c = document.querySelector('.chain');
    if (!c) return { found: false };
    return {
      found: true,
      steps: c.querySelectorAll('.chain-step').length,
      anomalous: c.querySelectorAll('.chain-step.anom').length,
      dated: [...c.querySelectorAll('.chain-d')].filter(d => /\d{4}/.test(d.textContent)).length,
      text: (c.innerText || '').slice(0, 300),
    };
  });
  check(chain.found, 'the selected dossier renders a sequence chain');
  check(chain.steps >= 5, 'chain has its steps', 'steps=' + chain.steps);
  check(chain.dated === chain.steps, 'every chain step shows a real date',
        `${chain.dated}/${chain.steps}`);
  check(!/undefined|NaN|Invalid Date/.test(chain.text || ''), 'chain text is clean');

  const body = await page.evaluate(() => document.body.innerText);
  check(!/undefined/.test(body), 'no "undefined" anywhere in the rendered page');
  check(!/\bNaN\b|Invalid Date/.test(body), 'no NaN or Invalid Date rendered');
  check(!/\[object Object\]/.test(body), 'no [object Object] rendered');

  // AFFILIATIONS: an id-shaped entry must resolve to a node label and be clickable,
  // never print as the raw slug.
  const links = await page.evaluate(() =>
    [...document.querySelectorAll('a[data-goto]')].map(a => a.textContent.trim()));
  const slugs = links.filter(t => /^[a-z0-9]+(-[a-z0-9]+)+$/.test(t));
  check(slugs.length === 0, 'no navigable link shows a raw slug', slugs.slice(0, 4).join(','));

  if (SHOTS) {
    await page.screenshot({ path: SHOTS + '/cases.png' });
    await page.click('[data-view="NETWORK"]');
    await page.waitForTimeout(6000);
    await page.screenshot({ path: SHOTS + '/network.png' });
  }

  await browser.close();
  ok.forEach(l => console.log('  ' + l));
  fails.forEach(l => console.log('  ' + l));
  console.log('\n' + (fails.length ? `RUNTIME CHECK FAILED (${fails.length})` : 'RUNTIME CHECK PASSED'));
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR', e.message); process.exit(2); });
