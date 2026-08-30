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
 *   npx http-server dist -p 8899 --silent &   # or the container copy under /opt/node22
 *   node tools/runtime_check.js
 *
 * file:// does not work for this page -- a 13MB document served over file://
 * never finished parsing in the container. Serve it over HTTP.
 */
const { requirePlaywright, launchOptions } = require('./browser_env');
const { chromium } = requirePlaywright();
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
// argv wins over the env so a one-off can be pointed anywhere; BOARD_URL is
// what the gate runner sets, and capture_strip.js already read it.
const URL = process.argv[2] || process.env.BOARD_URL
          || 'http://127.0.0.1:8899/the-program.html';
const SHOTS = process.env.RUNTIME_SHOTS || '';

const fails = [], ok = [];
const check = (c, label, detail = '') => {
  (c ? ok : fails).push(`${c ? 'ok  ' : 'FAIL'}  ${label}${detail ? ' :: ' + detail : ''}`);
};

(async () => {
  const browser = await chromium.launch(launchOptions({
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=swiftshader'],
  }));
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
  // Read from golden, like the four stats-strip checks above. This line used to
  // hardcode '278 of 278', which is the exact staleness the comment at the top of
  // this block warns about -- it survived only because no person node was added
  // between the day it was written and 28 August 2026. Asserting shown === total ===
  // golden is strictly stronger than the literal was: it still catches a dropped
  // record, and it also catches the two numbers disagreeing with each other.
  const m = cases.match(/(\d+) of (\d+) records shown/);
  check(!!m && m[1] === String(g.people) && m[2] === String(g.people),
        'case view shows every record',
        m ? `${m[1]} of ${m[2]} vs golden ${g.people}` : 'no "N of N records shown" text found');
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
    await page.click('[data-view="PROGRAM"]');
    await page.waitForTimeout(6000);
    await page.screenshot({ path: SHOTS + '/program.png' });
    await page.click('[data-view="CASES"]');
    await page.waitForTimeout(1200);
  }

  /* ---- THE SEARCH GRAMMAR ---------------------------------------------------
     Design specified key:value filters and `via:`; the parent board shipped a
     plain substring match, so `via:bigelow` returned "0 of 956 entities". That is
     an answer about the board rather than about the query, and the only way to
     tell the difference is to run one and count.

     Every expectation below is derived INDEPENDENTLY from the layout model on
     disk, never from the page, so agreeing with the renderer is not enough. */
  try {
    const M = JSON.parse(fs.readFileSync(
      path.join(ROOT, 'data', 'l0-layout-model.json'), 'utf8')).current;
    const L0 = M.nodes || [];
    const want = {
      'band:custody':  L0.filter(n => n.band === 'custody').length,
      'era:nd':        L0.filter(n => String(n.col) === 'nd').length,
      'isolated:1':    L0.filter(n => n.isolated).length,
      'flag:1':        (((M.highlights || {}).flags) || []).length,
      'role:oversight': L0.filter(n => (n.roles || []).indexOf('oversight') >= 0).length,
    };
    /* via: reaches the shared members who are NOT on the map, which is the case
       Design called out by name. Derive the expected set the same way. */
    const viaHits = new Set();
    for (const e of (M.edges || [])) {
      if (!(e.via || []).some(m => String(m).toLowerCase().indexOf('bigelow') >= 0)) continue;
      viaHits.add(e.a); viaHits.add(e.b);
    }
    want['via:bigelow'] = viaHits.size;

    await page.click('[data-view="SEARCH"]');
    await page.waitForTimeout(700);
    for (const q of Object.keys(want)) {
      const got = await page.evaluate(async x => {
        window.__board.S.query = x;
        window.__board.CMD.setView('SEARCH');
        await new Promise(r => setTimeout(r, 250));
        return document.querySelectorAll('.res').length;
      }, q);
      check(got === want[q], `search grammar: ${q}`, `${got} rows, model says ${want[q]}`);
    }
    /* And the no-result state must say what it did NOT search. It used to say
       only "No entity matches that query", which reads as a fact about the board. */
    const nores = await page.evaluate(async () => {
      window.__board.S.query = 'zzzznotathing';
      window.__board.CMD.setView('SEARCH');
      await new Promise(r => setTimeout(r, 250));
      return document.body.innerText;
    });
    check(/Searched all \d+ entities/.test(nores) && /connectivity floor/.test(nores),
          'the no-result state names what it did not search',
          (nores.match(/Searched all[^\n]*/) || ['(nothing)'])[0].slice(0, 110));
    await page.evaluate(() => { window.__board.S.query = ''; });
  } catch (e) {
    check(false, 'the search grammar could be exercised', e.message.slice(0, 120));
  }

  /* ---- THE PATENTS TAB ------------------------------------------------------
     The tab's CONTENT is checked by verify.py, against the transcripts it cites.
     This checks what the browser does with it, which is a different question and
     the one CLAUDE.md section 5 is about: reading the source is not verification.

     Two defects were found here by looking, on the first cut, and neither was
     visible to any data check:

     1. Every quotation printed a stray box and a capital letter beside its quote
        marks. The stylesheet said `quotes:'\201C' '\201D'` and the module that
        carries it was a NON-RAW Python string, so \201 was read as a Python octal
        escape -- U+0081 -- and the C survived as a literal. The CSS was correct;
        the file that emitted it was not.
     2. The prosecution lane labels overprinted into a smear. PAX 205 has ten events
        inside three years, and 'NON-FINAL', 'ALLOWED — PRIOR ART' and 'GRANTED'
        rendered as 'NON-ALLOWED — PRIORARTED'.

     POISON=patents puts the second one back on the live page: every label is
     returned to row 0, which is where they sat before the stagger, and the overlap
     count must rise. It moves the real labels on the real page rather than
     corrupting the probe -- a probe that reported 0 regardless would pass a
     predicate poison and fail this. */
  try {
    await page.evaluate(() => window.__board.CMD.setView('PATENTS'));
    await page.waitForTimeout(2500);
    const POIS = process.env.POISON === 'patents';
    if (POIS) await page.evaluate(() => {
      document.querySelectorAll('.patlane .ev b').forEach(b => { b.style.top = '18px'; });
    });
    const pat = await page.evaluate(() => {
      const q = s => document.querySelectorAll(s).length;
      const lanes = [...document.querySelectorAll('.patlane .lane')].map(lane => {
        const ls = [...lane.querySelectorAll('.ev b')].map(e => e.getBoundingClientRect());
        let hit = 0;
        for (let i = 0; i < ls.length; i++) for (let j = i + 1; j < ls.length; j++) {
          const a = ls[i], c = ls[j];
          if (!(c.left >= a.right || c.right <= a.left || c.top >= a.bottom || c.bottom <= a.top)) hit++;
        }
        return { labels: ls.length, overlaps: hit };
      });
      const view = document.querySelector('#surface .view');
      return {
        boxes: q('.patbox'),
        quotes: q('.patq blockquote'),
        lit: q('.patq q em'),
        filings: q('.patfil > div'),
        drawings: [...document.querySelectorAll('.patdraw img')].filter(i => i.naturalWidth > 0).length,
        struck: q('.patwrap li.gone'),
        obsRows: q('.patobs tr'),
        lanes,
        overlaps: lanes.reduce((n, l) => n + l.overlaps, 0),
        labels: lanes.reduce((n, l) => n + l.labels, 0),
        /* the header strip, which must be DERIVED. The mockup's read "5 FILINGS ·
           2 GRANTED" and the data says three are granted. */
        strip: (document.querySelector('.patfil') || {}).previousElementSibling
                 ? document.querySelector('.patbox .lede').textContent.trim() : '',
        /* what the data itself says, recounted here rather than trusted */
        want: (() => {
          const F = (window.PATDATA && window.PATDATA.filings) || [];
          return { n: F.length,
                   g: F.filter(f => (f.status || []).indexOf('GRANTED') >= 0).length,
                   e: F.filter(f => (f.status || []).indexOf('EXPIRED') >= 0).length };
        })(),
        /* no stray CSS escape reached the page as text */
        boxGlyph: /[\u0080-\u009f]/.test(document.querySelector('.pat').textContent),
        scrollable: view ? view.scrollHeight > view.clientHeight : false,
        hOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      };
    });
    check(pat.boxes >= 6 && pat.filings === 5 && pat.quotes === 4,
          'the patents tab draws its sections',
          `${pat.boxes} panels · ${pat.filings} filings · ${pat.quotes} quotes`);
    check(pat.lit === pat.quotes, 'every quotation lights the phrase it means to',
          `${pat.lit} of ${pat.quotes} quotations carry a highlight`);
    check(pat.boxGlyph === false, 'no CSS escape reaches the page as a literal glyph',
          pat.boxGlyph ? 'a C1 control character is being rendered as text'
                       : 'no C1 control characters in the rendered tab');
    check(pat.overlaps === 0 || POIS, 'no prosecution lane label overprints another',
          `${pat.labels} labels across ${pat.lanes.length} lanes, ${pat.overlaps} overlapping`
          + (POIS ? ' [POISON=patents: all labels forced to row 0]' : ''));
    if (POIS) check(pat.overlaps > 0, 'the lane-label check can see an overprint',
                    `${pat.overlaps} overlaps with the stagger removed — must be > 0`);
    check(pat.drawings === 11, 'every drawing sheet loads',
          `${pat.drawings} of 11 sheets decoded`);
    check(pat.struck >= 2, 'the wrapper prints what it does not have',
          `${pat.struck} papers drawn as absent`);
    check(pat.obsRows === 5, 'all five observables are on the tab, met or not',
          `${pat.obsRows} rows`);
    check(pat.hOverflow === false, 'the patents tab never scrolls sideways',
          pat.hOverflow ? 'the document is wider than the window' : 'no horizontal overflow');
  } catch (e) {
    check(false, 'the patents tab could be exercised', e.message.slice(0, 120));
  }

  /* ---- THE INVERSION, 29 August 2026 ----------------------------------------
     Stewart's call after using the live board: the force-directed full graph is
     the primary network map, and Design's packed program map moves to a tab of
     its own. Both survive; they swap roles.

     Asserted through the DOM rather than through S.l0full, because the flag is
     what the code sets and the wrapper is what the reader gets. The two renderers
     are distinguishable there without ambiguity: mountL0's host carries `.l0wrap`
     and draws its own `.l0crumb` breadcrumb; mountNetwork's carries neither and
     leaves the inherited hop/legend chrome in #netchrome.

     THE FAILURE THIS IS AIMED AT is a half-applied inversion, and it is silent.
     If VIEWS gains PROGRAM but the dispatch map does not, `[S.view] || viewNetwork`
     catches the miss and the new tab renders THE NETWORK MAP -- a "Program map"
     button that shows the wrong map, no error, nothing in the console. So the
     check is not "PROGRAM draws something"; it is that the two views draw
     DIFFERENT renderers, and that each draws the right one.

     POISON=inversion navigates to NETWORK where the check expects PROGRAM, so the
     two samples come from the same renderer. Everything the check reads is real
     page state; what the poison changes is which page state it reads. The match
     must collapse. */
  try {
    const renderer = async () => await page.evaluate(() => ({
      l0wrap:  !!document.querySelector('.l0wrap'),
      crumb:   !!document.querySelector('.l0crumb'),
      chrome:  (document.getElementById('netchrome') || {}).innerHTML ?
                 (document.getElementById('netchrome').innerHTML.length > 0) : false,
      canvas:  [...document.querySelectorAll('canvas')].some(c => c.width > 200),
    }));
    await page.evaluate(() => window.__board.CMD.setView('CASES'));
    await page.waitForTimeout(700);
    await page.click('[data-view="NETWORK"]');
    await page.waitForTimeout(4000);
    const net = await renderer();
    check(net.canvas && !net.l0wrap && !net.crumb,
          'network map is the full graph at rest',
          `l0wrap=${net.l0wrap} crumb=${net.crumb} canvas=${net.canvas}`);
    check(net.chrome, 'the full graph keeps its own hop and legend chrome',
          '#netchrome ' + (net.chrome ? 'has content' : 'is empty'));

    const POIS = process.env.POISON === 'inversion';
    await page.click(POIS ? '[data-view="NETWORK"]' : '[data-view="PROGRAM"]');
    await page.waitForTimeout(4000);
    const prog = await renderer();
    check(prog.canvas && prog.l0wrap && prog.crumb,
          'the program map tab draws the packed map',
          `l0wrap=${prog.l0wrap} crumb=${prog.crumb} canvas=${prog.canvas}`
          + (POIS ? ' [POISON=inversion]' : ''));
    check(prog.l0wrap !== net.l0wrap,
          'the two map views draw different renderers',
          POIS ? 'POISON=inversion: both samples taken from NETWORK, must collapse'
               : 'NETWORK has no .l0wrap, PROGRAM has one');
  } catch (e) {
    check(false, 'the two map views could be exercised', e.message.slice(0, 120));
  }

  /* ---- THE FULL GRAPH'S PARTICLE LAYER --------------------------------------
     mountNetwork is the inherited parent-board renderer. It drew a particle on
     every visible edge, flipped by comparing the two nodes' dates. That is a
     time-direction flow on every line, which Design named and rejected: it states
     the relationship runs from the earlier node to the later one, and for most of
     these edges the board makes no such claim.

     THIS BLOCK MATTERS MORE THAN IT DID. Until 29 August 2026 this renderer was a
     fallback that mounted only when a path or a frame was live, and reaching it at
     all took three attempts. It is now the board's DEFAULT SURFACE -- the rule it
     is held to has been promoted from a corner case to the first thing every
     reader sees. The route below is kept exactly as it was, frame-first from
     another view, because it exercises the reframe path as well as the rest
     state; `network map is the full graph at rest` above covers the plain case. */
  try {
    await page.evaluate(() => window.__board.CMD.setView('CASES'));
    await page.waitForTimeout(900);
    await page.evaluate(() => {
      const B = window.__board;
      B.CMD.frameNodes((B.L0DATA.l0 || []).slice(0, 10).map(n => n.id));
    });
    await page.waitForTimeout(6000);
    const isFull = await page.evaluate(() => !!window.__board.S.l0full);
    check(isFull, 'the full-graph renderer can be reached at all',
          'S.l0full=' + isFull + ' after frameNodes from another view');
    /* SETTLE FIRST, THEN MEASURE. The first cut of this counted distinct frames in
       a fixed window and read 1. That was luck: this renderer eases its camera on
       a reframe (`cam.k += (camTo.k - cam.k) * 0.12`), so for the first second or
       two the canvas changes for reasons that have nothing to do with motion. The
       moment anything shifted the boot timing it read 2 and failed, and the trace
       was 330, 32, 310, 310, 310, 310 -- a settle, not a flow.
       So: wait for the canvas to go quiet, THEN require it to stay quiet. This is
       strictly stronger than the original, because a time-direction flow never
       goes quiet and now fails on the settle timeout instead of passing on a
       lucky sample. */
    const hashOnce = async () => await page.evaluate(() => {
      const cs = [...document.querySelectorAll('canvas')].filter(c => c.width > 200);
      const hs = [];
      for (const c of cs) {
        let cx; try { cx = c.getContext('2d'); } catch (e) { continue; }
        if (!cx) continue;
        const d = cx.getImageData(0, 0, c.width, c.height).data;
        let h = 0;
        for (let i = 0; i < d.length; i += 4*53) h = (h*31 + d[i] + d[i+1]*3 + d[i+2]*7) >>> 0;
        hs.push(h);
      }
      return hs.join('|');
    });
    /* Quiet has to be ESTABLISHED, not glimpsed. This used to return on the first
       pair of matching samples, and a force layout still converging can hand you two
       identical frames in a row -- alpha dips, or a frame boundary -- and then carry
       on moving, which holdsStill() below then caught as "settled and then started
       moving again". Intermittently: 7 new nodes on 28 August 2026 made it fail about
       one run in two. Requiring several consecutive matches does not weaken the check,
       because a genuine time-direction flow never produces ANY run of identical frames
       and still fails here on the settle timeout. */
    const QUIET_RUN = 3;
    const SETTLE_TRIES = 45;
    const settle = async (tries = SETTLE_TRIES) => {
      let prev = await hashOnce();
      let run = 0;
      for (let i = 0; i < tries; i++) {
        await page.waitForTimeout(400);
        const now = await hashOnce();
        run = (now === prev) ? run + 1 : 0;
        prev = now;
        if (run >= QUIET_RUN) return true;
      }
      return false;
    };
    const holdsStill = async (n = 5) => {
      const first = await hashOnce();
      for (let i = 0; i < n; i++) {
        await page.waitForTimeout(400);
        if (await hashOnce() !== first) return false;
      }
      return true;
    };
    const settled = await settle();
    const still = settled && await holdsStill();
    check(settled && still, 'the full graph asserts no time direction at rest',
          settled ? (still ? 'settled, then held still for 2s'
                           : 'settled and then started moving again')
                  : `never settled within ${SETTLE_TRIES * 400 / 1000}s, which is what a flow on every line looks like`);
    await page.evaluate(() => {
      const B = window.__board; B.S.sel = (B.L0DATA.l0 || [])[0].id;
    });
    await page.waitForTimeout(1400);
    /* And the other half: with a node selected it must NOT hold still, or the
       particle layer has been switched off rather than made honest. */
    const movesOnSelect = !(await holdsStill(4));
    check(movesOnSelect, "the full graph moves on the selected node's edges",
          movesOnSelect ? 'canvas keeps changing while a node is selected'
                        : 'canvas held still, so no particle is running at all');
    await page.evaluate(() => { window.__board.CMD.clearSelection(); });
  } catch (e) {
    check(false, 'the full-graph particle layer could be exercised', e.message.slice(0, 120));
  }

  /* ---- the head strip, at the width where it used to break ---------------
   *
   * .l0crumb and .l0ctl were two absolutely positioned boxes on the same line at
   * the same z-index, and the crumb's max-width was calc(100% - 24px) -- the full
   * width. So the moment the dock opened and took half the window, the crumb ran
   * straight under the control row and printed on top of it. Six buttons, every
   * one overlapped, at every viewport size where a reader had a node selected.
   *
   * NOTHING IN THE GATE COULD SEE IT. runtime_check asserts through text nodes and
   * every one of them was present and correct. test_packed_layout reads the canvas
   * and this is DOM. head-row-clear measures the control row against the ERA
   * LABELS and never asked whether the crumb and the controls clear EACH OTHER.
   *
   * Two assertions, because the report was two things and only one of them was
   * true: the overlap was real, and the buttons were NOT dead -- they hit-test and
   * fire, they just looked inert because the map they affect was 798px wide and
   * dimmed to 16%. Assert both, so a regression in either is named for what it is. */
  try {
    /* Back to the packed map, which is the PROGRAM tab as of 29 August 2026. The
       block above leaves the reader on the full graph, so the packed map is not
       mounted at this point -- the first cut of this check measured 0 buttons on a
       0px canvas and reported success-shaped nonsense until it was made to fail
       loudly, and the waitForSelector below is what keeps it loud.

       S.l0full is no longer set by hand here. It used to be, because the two
       renderers shared the NETWORK view and the flag was the only thing choosing
       between them; now the view chooses, viewProgramMap sets the flag, and
       setting it from outside would be a test arranging the state it means to
       observe. */
    await page.evaluate(() => {
      const B = window.__board;
      B.S.sel = null;
      B.S.l0open = [];
    });
    await page.click('[data-view="CASES"]');
    await page.waitForTimeout(800);
    await page.click('[data-view="PROGRAM"]');
    await page.waitForTimeout(2500);
    const skip2 = await page.$('.l0entry [data-entry-skip], .l0entry [data-skip]');
    if (skip2) { await skip2.click(); await page.waitForTimeout(1000); }
    await page.waitForSelector('.l0wrap canvas', { timeout: 30000 });
    await page.waitForTimeout(1500);
    /* Reproduce the reported state FIRST -- a node selected and the dock at its
       open width, which is where the map gets narrow enough for the strip to
       break. The poisons below then apply to the layout as it finally sits; the
       first cut applied POISON=clicks to the pre-dock positions and the overlay
       landed 400px from the buttons it was meant to cover, so the check passed and
       proved nothing. */
    await page.evaluate(() => {
      const B = window.__board;
      B.CMD.selectNode((B.L0DATA.l0 || [])[3].id);
      /* A selection is required, not incidental: it is what brings the selection
         bar onto the surface at all. */
      const d = document.getElementById('dock');
      if (d) {
        const w = Math.max(560, Math.round(innerWidth * 0.5));
        d.style.width = w + 'px';
        d.classList.add('open', 'dock-wide');
        document.documentElement.style.setProperty('--dock-w', w + 'px');
      }
    });
    await page.waitForTimeout(1600);

    /* POISON=head restores the exact CSS that shipped: two absolutely positioned
       boxes on one line, the crumb allowed the full width. Both assertions must go
       red. A check never shown failing is indistinguishable from a broken one, and
       this one guards a defect that four other check families could not see. */
    if (process.env.POISON === 'head') {
      await page.addStyleTag({ content:
        '.l0head{display:block !important;pointer-events:auto !important}'
      + '.l0crumb{position:absolute !important;left:12px;top:10px;z-index:4;'
      + 'max-width:calc(100% - 24px) !important;width:calc(100% - 24px) !important;'
      + 'pointer-events:auto !important;background:#141920 !important}'
      + '.l0ctl{position:absolute !important;right:12px;top:10px;z-index:4}' });
      await page.waitForTimeout(500);
    }
    /* And a SECOND poison, because the two assertions guard different properties
       and POISON=head only breaks one of them. That is the point: in the real
       defect the crumb overlapped the buttons and they stayed clickable, so a
       single poison proving "something went red" would leave the reachability
       check untested. This one puts a transparent sheet over the control row --
       nothing looks different, every button is dead. */
    if (process.env.POISON === 'clicks') {
      await page.evaluate(() => {
        const z = document.querySelector('.l0ctl');
        if (!z) return;
        const r = z.getBoundingClientRect();
        const v = document.createElement('div');
        v.style.cssText = 'position:fixed;z-index:99;pointer-events:auto;background:transparent;'
          + 'left:' + r.x + 'px;top:' + r.y + 'px;width:' + r.width + 'px;height:' + r.height + 'px';
        document.body.appendChild(v);
      });
      await page.waitForTimeout(400);
    }
    const geom = await page.evaluate(() => {
      return new Promise(r => setTimeout(() => {
        const crumb = document.querySelector('.l0crumb');
        const cr = crumb ? crumb.getBoundingClientRect() : null;
        /* EVERY control on the map surface, not just the head row. This started as
           a check on .l0ctl after the breadcrumb overlapped it. The selection bar
           then shipped and four of its five buttons hit-tested to the ledger panel
           sitting on top of them -- a check scoped to one container could not see
           it, and the same collision has now happened four times in this file in
           four different places. So the scope is the surface. */
        const btns = [...document.querySelectorAll(
          '.l0ctl button, .l0selbar button, .l0legend [data-legend], .l0crumb [data-close]')];
        const hit = (a, b) => a.x < b.x + b.width && b.x < a.x + a.width
                           && a.y < b.y + b.height && b.y < a.y + a.height;
        let overlapped = 0, unreachable = 0;
        for (const el of btns) {
          const r2 = el.getBoundingClientRect();
          /* The crumb's own controls are inside it and overlap it by definition.
             Counting them made the widened button set report 1 of 14 overlapping
             the moment reachability grew past .l0ctl -- a false positive that says
             nothing about the defect this half guards, which is the crumb running
             UNDER controls that are not its own. */
          if (cr && !crumb.contains(el) && hit(cr, r2)) overlapped++;
          /* Across the whole button, not just its centre: the first probe of this
             only sampled the middle and would have passed with the left half
             buried. */
          for (let fx = 0.08; fx <= 0.92; fx += 0.12)
            for (let fy = 0.2; fy <= 0.8; fy += 0.3) {
              const t = document.elementFromPoint(
                Math.round(r2.x + r2.width * fx), Math.round(r2.y + r2.height * fy));
              if (!(t && (t === el || el.contains(t)))) { unreachable++;
                if (!window.__deadWhy) window.__deadWhy = [];
                window.__deadWhy.push(el.textContent.trim().slice(0,14) + ' @' + fx.toFixed(2)
                  + ' blocked by ' + (t ? (t.className || t.tagName) : 'nothing')); }
            }
        }
        const cvs = document.querySelector('.l0wrap canvas');
        r({ buttons: btns.length, overlapped, unreachable, why: (window.__deadWhy||[]).slice(0,6),
            mapW: cvs ? Math.round(cvs.parentElement.getBoundingClientRect().width) : 0 });
      }, 1600));
    });
    check(geom.buttons > 0 && geom.overlapped === 0,
          'the breadcrumb never prints on the map controls',
          `${geom.overlapped} of ${geom.buttons} buttons overlapped at ${geom.mapW}px of map`);
    check(geom.buttons > 0 && geom.unreachable === 0,
          'every map control is clickable across its whole face',
          geom.unreachable === 0
            ? `${geom.buttons} buttons, every sample point reaches its own button`
            : `${geom.unreachable} sample points hit something else :: ${(geom.why||[]).join(' | ')}`);
    await page.evaluate(() => { window.__board.CMD.clearSelection(); });
  } catch (e) {
    check(false, 'the head strip could be measured with the dock open', e.message.slice(0, 120));
  }

  await browser.close();
  ok.forEach(l => console.log('  ' + l));
  fails.forEach(l => console.log('  ' + l));
  console.log('\n' + (fails.length ? `RUNTIME CHECK FAILED (${fails.length})` : 'RUNTIME CHECK PASSED'));
  process.exit(fails.length ? 1 : 0);
})().catch(e => { console.error('HARNESS ERROR', e.message); process.exit(2); });
