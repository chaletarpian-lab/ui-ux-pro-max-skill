import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));
const slides = [
  ['slide-00-intro.html', 'output/arpian-carousel-0-intro.png'],
  ['slide-01-okapi.html', 'output/arpian-carousel-1-okapi.png'],
  ['slide-02-family-room.html', 'output/arpian-carousel-2-family-room.png'],
  ['slide-03-cloture.html', 'output/arpian-carousel-3-cloture.png'],
];

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const [html, out] of slides) {
  await page.goto('file://' + path.join(dir, html));
  await page.waitForFunction(() => document.fonts.ready.then(() => true));
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: path.join(dir, out) });
  console.log('saved', out);
}
await browser.close();
