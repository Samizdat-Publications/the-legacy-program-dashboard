/**
 * browser_env.js -- where Playwright and Chromium actually are, resolved at run time.
 *
 * WHY THIS EXISTS. Every browser tool in this repo used to open with two absolute
 * paths baked into the source:
 *
 *     require('/opt/node22/lib/node_modules/playwright')
 *     executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
 *
 * Both are facts about ONE container, not about this project. Three costs followed,
 * and the first one had already been paid before anybody looked:
 *
 *   1. `tools/shoot.js` pinned `/opt/pw-browsers/chromium/chrome-linux/chrome`. That
 *      path does not exist. The tool was dead and nothing said so -- the same shape as
 *      every other failure in CLAUDE.md section 5, one rung further out: not a check
 *      that passes while broken, a check that cannot start.
 *   2. `chromium-1194` is a pinned Playwright build number. The day the image ships
 *      1200, FOUR of the nine gate steps stop starting at once, and the gate reports
 *      an environment problem as though it were a board problem.
 *   3. Nothing outside that container can run the gate. Stewart on Windows cannot;
 *      GitHub Actions cannot. So "the gate is green" was a sentence only a cloud
 *      session could say, which makes the gate a single point of failure rather than
 *      a shared standard.
 *
 * The rule this file encodes: a tool may depend on Chromium EXISTING. It may not
 * depend on where. Resolution is ordered from most explicit to most automatic, and
 * every step is a real filesystem check rather than an assumption.
 *
 * Returning `undefined` from chromiumPath() is deliberate and is the CI path: pass it
 * straight to `chromium.launch({ executablePath })` and Playwright resolves its own
 * downloaded browser. `executablePath: undefined` is exactly "you choose".
 */
'use strict';

const fs = require('fs');
const path = require('path');

const CONTAINER_NODE_MODULES = '/opt/node22/lib/node_modules';
const CONTAINER_BROWSERS = '/opt/pw-browsers';

/** Highest-numbered chromium-<n> under dir that has a real chrome binary, or null. */
function newestChromiumUnder(dir) {
  let entries;
  try {
    entries = fs.readdirSync(dir);
  } catch {
    return null;
  }
  const cands = entries
    .map(name => {
      const m = /^chromium-(\d+)$/.exec(name);
      return m ? { build: Number(m[1]), name } : null;
    })
    .filter(Boolean)
    .sort((a, b) => b.build - a.build);

  for (const c of cands) {
    for (const rel of ['chrome-linux/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
                       'chrome-win/chrome.exe']) {
      const p = path.join(dir, c.name, rel);
      if (fs.existsSync(p)) return p;
    }
  }
  return null;
}

/**
 * The Playwright module, wherever it is installed.
 * Local node_modules first, so a contributor's own install wins over the container's.
 */
function requirePlaywright() {
  const tried = [];
  for (const spec of ['playwright', path.join(CONTAINER_NODE_MODULES, 'playwright')]) {
    try {
      return require(spec);
    } catch (e) {
      tried.push(`${spec}: ${e.code || e.message}`);
    }
  }
  throw new Error(
    'browser_env: cannot load Playwright. Tried:\n  ' + tried.join('\n  ') +
    '\nInstall it (npm i playwright) or run where the container copy is on the path.');
}

/**
 * Absolute path to a Chromium binary, or `undefined` to mean "let Playwright decide".
 * Never throws: a missing browser is Playwright's error to report, with its own
 * install instructions, not ours to guess at.
 */
function chromiumPath() {
  const explicit = process.env.CHROMIUM_PATH;
  if (explicit && fs.existsSync(explicit)) return explicit;

  const pwRoot = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (pwRoot && pwRoot !== '0') {
    const found = newestChromiumUnder(pwRoot);
    if (found) return found;
  }

  const container = newestChromiumUnder(CONTAINER_BROWSERS);
  if (container) return container;

  return undefined;
}

/** Launch options every browser tool in this repo shares. Merge, do not replace. */
function launchOptions(extra = {}) {
  const opts = { ...extra };
  const exe = chromiumPath();
  if (exe) opts.executablePath = exe;
  return opts;
}

/**
 * The http-server entry script, for tools that spawn their own server.
 * Returns null when it is not installed, so a caller can fall back to `npx`.
 */
function httpServerBin() {
  const candidates = [
    path.join(CONTAINER_NODE_MODULES, 'http-server/bin/http-server'),
    path.resolve(__dirname, '..', 'node_modules/http-server/bin/http-server'),
  ];
  for (const p of candidates) if (fs.existsSync(p)) return p;
  return null;
}

/** One line naming what was actually resolved. Print it; a silent tool teaches nothing. */
function describe() {
  const exe = chromiumPath();
  return `chromium: ${exe || '(Playwright default)'}`;
}

module.exports = { requirePlaywright, chromiumPath, launchOptions, httpServerBin, describe };
