/* Display derivatives for the patent drawing sheets.
 *
 * WHY THIS IS NOT A BUILD STEP. research/patents/drawings/PROVENANCE.md says these
 * are 7112x9167 print-resolution renders, roughly 3MB in total, and that they must
 * be downsampled before they go anywhere near the page -- shipping them whole into
 * a document that is already 15MB would undo notes/FIRST-PAINT-2026-08-26.md.
 *
 * It says "generate display derivatives at build time". They are generated HERE
 * instead, once, and committed, for three reasons:
 *   1. There is no PIL, no ImageMagick and no sharp in this environment. The only
 *      resampler available is a browser, and putting a browser in the build would
 *      make `python3 tools/build_dashboard.py` need Chromium.
 *   2. `verify.py --idempotent` requires two builds to produce identical bytes. A
 *      re-encode through a canvas is not guaranteed to be bit-identical run to run.
 *   3. The originals stay archival, which is what PROVENANCE.md asks for.
 *
 * Re-run it if the sheet list changes:
 *   node /opt/node22/lib/node_modules/http-server/bin/http-server . -p 8897 --silent &
 *   node tools/make_drawing_thumbs.mjs
 *
 * It serves the originals over HTTP because a 15MB-class file:// load is exactly
 * what the rest of this repo's tooling refuses to rely on.
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/* fileURLToPath, not new URL(...).pathname -- CLAUDE.md section 3: the repo path
   contains three spaces on Stewart's machine and pathname percent-encodes them. */
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(HERE);
const require = createRequire(import.meta.url);
const { requirePlaywright, launchOptions } = require(path.join(HERE, 'browser_env.js'));
const { chromium } = requirePlaywright();

const SRC = path.join(ROOT, 'research', 'patents', 'drawings');
const OUT = path.join(SRC, 'thumbs');
const BASE = process.env.DRAW_URL || 'http://127.0.0.1:8897';
/* 2x the largest slot the tab draws (the 2560 six-up strip), so the tile stays
   sharp on a retina panel and still costs well under a percent of the page. */
const MAX_W = 168, MAX_H = 216;

const sheets = fs.readdirSync(SRC).filter(f => /\.png$/i.test(f)).sort();
if (!sheets.length) { console.error('no source sheets in ' + SRC); process.exit(1); }
fs.mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch(launchOptions({ args: ['--no-sandbox'] }));
const page = await browser.newPage();
/* SAME ORIGIN, deliberately. An about:blank page has no origin, so an <img> from
   http://127.0.0.1 is cross-origin: it needs CORS headers http-server does not send
   without --cors, and without them the canvas is tainted and toDataURL throws. */
await page.goto(BASE + '/', { waitUntil: 'load', timeout: 60000 });
let total = 0;
for (const f of sheets) {
  const url = `${BASE}/research/patents/drawings/${encodeURIComponent(f)}`;
  const dataUrl = await page.evaluate(async ([u, mw, mh]) => {
    const img = new Image();
    await new Promise((res, rej) => { img.onload = res; img.onerror = () => rej(new Error('load ' + u)); img.src = u; });
    /* Contain, not cover: a patent sheet cropped is a different document. */
    const s = Math.min(mw / img.naturalWidth, mh / img.naturalHeight);
    const w = Math.max(1, Math.round(img.naturalWidth * s));
    const h = Math.max(1, Math.round(img.naturalHeight * s));
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const x = c.getContext('2d');
    x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
    /* White ground painted explicitly. The source is greyscale with no alpha, but
       a transparent ground would put the board's #12171d behind black line art and
       the drawing would vanish. These ship as facsimiles of a paper document and
       they look like one. */
    x.fillStyle = '#ffffff'; x.fillRect(0, 0, w, h);
    x.drawImage(img, 0, 0, w, h);
    return c.toDataURL('image/png');
  }, [url, MAX_W, MAX_H]);
  const buf = Buffer.from(dataUrl.split(',')[1], 'base64');
  fs.writeFileSync(path.join(OUT, f), buf);
  total += buf.length;
  console.log(`  ${f}  ${(buf.length / 1024).toFixed(1)} KB`);
}
await browser.close();
console.log(`\n${sheets.length} thumbnails, ${(total / 1024).toFixed(1)} KB total -> ${path.relative(ROOT, OUT)}`);
