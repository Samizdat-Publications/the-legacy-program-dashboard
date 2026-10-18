// Stills of the live board for the README and showcase.json.
//   node tools/showcase/stills.mjs [base-url]
// Writes docs/media/*.jpg at 1280x720 (1x). Defaults to production.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const out = path.join(root, 'docs', 'media');
mkdirSync(out, { recursive: true });
const base = (process.argv[2] || 'https://the-program-zxz.pages.dev').replace(/\/$/, '');

const shots = [
  ['hero', '#/'],
  ['atlas', '#/atlas'],
  ['node', '#/n/david-grusch'],
  ['topic', '#/topic/grusch-allegations'],
  ['map', '#/map'],
  ['questions', '#/questions'],
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
for (const [name, hash] of shots) {
  await page.goto(`${base}/${hash}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(out, `${name}.jpg`), type: 'jpeg', quality: 85 });
  console.log(name, hash);
}
await browser.close();
if (errors.length) { console.error('page errors:', errors); process.exitCode = 1; }
