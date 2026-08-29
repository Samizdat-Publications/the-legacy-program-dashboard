/**
 * test_browser_env.js -- prove tools/browser_env.js resolves, and prove it rejects.
 *
 *   node tools/test_browser_env.js
 *   node tools/test_browser_env.js --self-test
 *
 * WHY THIS IS A TEST AND NOT A COMMENT. browser_env.js decides whether four of the
 * nine gate steps can start at all. Its failure mode is not a wrong answer, it is
 * ENOENT before any assertion runs -- which reads as "the board is broken" when it
 * means "this machine is not that container". `tools/shoot.js` sat dead for exactly
 * this reason and nothing reported it.
 *
 * The interesting case cannot be observed on the machine that needs it least. In the
 * container /opt/pw-browsers always exists, so the "no browser anywhere -> let
 * Playwright decide" branch never fires here, and that branch IS the CI path and
 * Stewart's-laptop path. So the case is reached by hiding the directory from
 * fs.readdirSync rather than by hoping. CLAUDE.md section 5: poison the page, not just
 * the predicate.
 *
 * No browser is launched and nothing is served. This test runs on Windows.
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const SELF_TEST = process.argv.includes('--self-test');
const fails = [], ok = [];
const check = (cond, label, detail = '') =>
  (cond ? ok : fails).push(`${cond ? 'ok  ' : 'FAIL'}  ${label}${detail ? ' :: ' + detail : ''}`);

/** Load a fresh copy of the module, so env changes are actually re-read. */
function fresh() {
  const p = require.resolve('./browser_env');
  delete require.cache[p];
  return require(p);
}

function withEnv(vars, fn) {
  const saved = {};
  for (const [k, v] of Object.entries(vars)) {
    saved[k] = process.env[k];
    if (v === undefined) delete process.env[k]; else process.env[k] = v;
  }
  try { return fn(); } finally {
    for (const [k, v] of Object.entries(saved)) {
      if (v === undefined) delete process.env[k]; else process.env[k] = v;
    }
  }
}

/** Hide a directory prefix from fs.readdirSync, the way it is absent off-container. */
function withHidden(prefix, fn) {
  const real = fs.readdirSync;
  fs.readdirSync = function (p, ...rest) {
    if (String(p).startsWith(prefix)) {
      const e = new Error(`ENOENT: no such file or directory, scandir '${p}'`);
      e.code = 'ENOENT';
      throw e;
    }
    return real.call(this, p, ...rest);
  };
  try { return fn(); } finally { fs.readdirSync = real; }
}

// A browser tree that is real enough to be found, with two builds so ordering shows.
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'pwfake-'));
for (const b of ['chromium-0001', 'chromium-9999']) {
  fs.mkdirSync(path.join(TMP, b, 'chrome-linux'), { recursive: true });
  fs.writeFileSync(path.join(TMP, b, 'chrome-linux', 'chrome'), '');
}
const HIGH = path.join(TMP, 'chromium-9999', 'chrome-linux', 'chrome');
const LOW = path.join(TMP, 'chromium-0001', 'chrome-linux', 'chrome');

// ---------------------------------------------------------------- resolution order

withEnv({ CHROMIUM_PATH: undefined, PLAYWRIGHT_BROWSERS_PATH: TMP }, () => {
  const got = fresh().chromiumPath();
  check(got === HIGH, 'PLAYWRIGHT_BROWSERS_PATH picks the highest build number', got);
});

withEnv({ CHROMIUM_PATH: LOW, PLAYWRIGHT_BROWSERS_PATH: TMP }, () => {
  const got = fresh().chromiumPath();
  check(got === LOW, 'CHROMIUM_PATH outranks PLAYWRIGHT_BROWSERS_PATH', got);
});

withEnv({ CHROMIUM_PATH: path.join(TMP, 'nope', 'chrome'), PLAYWRIGHT_BROWSERS_PATH: TMP }, () => {
  const got = fresh().chromiumPath();
  check(got === HIGH,
    'a CHROMIUM_PATH that does not exist is ignored, not trusted', String(got));
});

withEnv({ CHROMIUM_PATH: undefined, PLAYWRIGHT_BROWSERS_PATH: '0' }, () => {
  // '0' is Playwright's own "browsers live next to the package" sentinel and must not
  // be walked as a directory.
  const got = fresh().chromiumPath();
  check(got === undefined || fs.existsSync(got),
    "PLAYWRIGHT_BROWSERS_PATH='0' does not produce a bogus path", String(got));
});

// -------------------------------------------------- the branch this container hides

withHidden('/opt/pw-browsers', () => {
  withEnv({ CHROMIUM_PATH: undefined, PLAYWRIGHT_BROWSERS_PATH: undefined }, () => {
    const mod = fresh();
    const got = mod.chromiumPath();
    check(got === undefined,
      'no browser anywhere resolves to undefined, not to a guess', String(got));

    const opts = mod.launchOptions({ args: ['--no-sandbox'] });
    check(!('executablePath' in opts),
      'launchOptions omits executablePath entirely when nothing resolved',
      JSON.stringify(opts));
    check(Array.isArray(opts.args) && opts.args[0] === '--no-sandbox',
      'launchOptions preserves the caller options it was given');

    check(mod.describe().includes('Playwright default'),
      'describe() says which way it went', mod.describe());
  });
});

// launchOptions must never drop or overwrite what the caller passed.
withEnv({ CHROMIUM_PATH: LOW }, () => {
  const opts = fresh().launchOptions({ args: ['--a'], timeout: 5 });
  check(opts.executablePath === LOW && opts.timeout === 5 && opts.args[0] === '--a',
    'launchOptions merges rather than replaces', JSON.stringify(opts));
});

// ------------------------------------------------------------------------ self-test
// Each poison must make a specific check above fail. A resolver that always returned
// the container path would pass every test up to here; these are what say otherwise.
if (SELF_TEST) {
  const poisons = [
    ['a resolver that ignored CHROMIUM_PATH',
      () => withEnv({ CHROMIUM_PATH: LOW, PLAYWRIGHT_BROWSERS_PATH: TMP },
        () => fresh().chromiumPath() === HIGH)],
    ['a resolver that took the LOWEST build number',
      () => withEnv({ CHROMIUM_PATH: undefined, PLAYWRIGHT_BROWSERS_PATH: TMP },
        () => fresh().chromiumPath() === LOW)],
    ['a resolver that trusted a nonexistent CHROMIUM_PATH',
      () => withEnv({ CHROMIUM_PATH: '/nope/chrome', PLAYWRIGHT_BROWSERS_PATH: TMP },
        () => fresh().chromiumPath() === '/nope/chrome')],
    ['a resolver that invented a path when nothing is installed',
      () => withHidden('/opt/pw-browsers', () =>
        withEnv({ CHROMIUM_PATH: undefined, PLAYWRIGHT_BROWSERS_PATH: undefined },
          () => fresh().chromiumPath() !== undefined))],
  ];
  console.log('\nself-test -- each line is a defect this file would CATCH:');
  for (const [label, wouldBeWrong] of poisons) {
    const broken = wouldBeWrong();
    check(!broken, `rejects: ${label}`);
    console.log(`  ${broken ? 'FAIL' : 'ok  '}  rejects: ${label}`);
  }
}

fs.rmSync(TMP, { recursive: true, force: true });

for (const line of ok) console.log('  ' + line);
for (const line of fails) console.log('  ' + line);
if (fails.length) {
  console.error(`\nBROWSER ENV CHECK FAILED (${fails.length})`);
  process.exit(1);
}
console.log(`\nbrowser env ok (${ok.length} checks)`);
