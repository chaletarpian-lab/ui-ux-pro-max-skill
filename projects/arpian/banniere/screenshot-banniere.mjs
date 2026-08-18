import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const dir = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ viewport: { width: 1584, height: 396 }, deviceScaleFactor: 2 });
await page.goto('file://' + path.join(dir, 'banniere-linkedin.html'));
await page.waitForFunction(() => document.fonts.ready.then(() => true));
await page.waitForLoadState('networkidle');
await page.screenshot({ path: path.join(dir, 'output/banniere-linkedin-arpian.png') });
console.log('saved output/banniere-linkedin-arpian.png');
await browser.close();
