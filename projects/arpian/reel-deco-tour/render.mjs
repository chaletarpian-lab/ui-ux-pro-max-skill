// Rendu du reel : capture frame par frame via Chromium, assemblage MP4 via ffmpeg.
// Usage : node render.mjs [fps] [framesDir] [ffmpegPath]
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FPS = Number(process.argv[2] || 30);
const FRAMES = process.argv[3] || path.join(__dirname, 'frames');
const FFMPEG = process.argv[4] || 'ffmpeg';
const OUT = path.join(__dirname, 'output', 'arpian-reel-deco-tour.mp4');

mkdirSync(FRAMES, { recursive: true });
mkdirSync(path.join(__dirname, 'output'), { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto('file://' + path.join(__dirname, 'reel.html'));
await page.waitForFunction('window.READY === true', null, { timeout: 60000 });

const total = await page.evaluate('window.TOTAL_MS');
const nFrames = Math.ceil(total / 1000 * FPS);
console.log(`Durée ${(total / 1000).toFixed(1)}s → ${nFrames} frames @ ${FPS}fps`);

for (let i = 0; i < nFrames; i++) {
  const t = i * 1000 / FPS;
  await page.evaluate(`window.seek(${t})`);
  await page.screenshot({
    path: path.join(FRAMES, `f${String(i).padStart(5, '0')}.jpg`),
    type: 'jpeg', quality: 92,
  });
  if (i % 100 === 0) console.log(`frame ${i}/${nFrames}`);
}
await browser.close();

console.log('Encodage MP4…');
execFileSync(FFMPEG, [
  '-y', '-framerate', String(FPS),
  '-i', path.join(FRAMES, 'f%05d.jpg'),
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
  '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
  OUT,
], { stdio: 'inherit' });
console.log('OK →', OUT);
