import { spawn } from 'node:child_process';
import { mkdir } from 'node:fs/promises';
import { chromium } from '@playwright/test';

const url = 'http://127.0.0.1:4324';
const server = spawn('npm', ['run', 'dev', '--', '--host', '127.0.0.1', '--port', '4324'], { stdio: 'pipe' });
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const panels = [
  ['#rainfall-section', 'artifacts/chart-rainfall.png'],
  ['#sst-section', 'artifacts/chart-sst.png'],
  ['#taro-section', 'artifacts/chart-taro.png'],
];
try {
  for (let i = 0; i < 40; i += 1) {
    try { if ((await fetch(url)).ok) break; } catch { /* server is starting */ }
    await wait(250);
    if (i === 39) throw new Error('Astro server did not become ready');
  }
  await mkdir('artifacts', { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: 'networkidle' });
  for (const [selector, file] of panels) {
    await page.locator(selector).screenshot({ path: file });
  }
  await browser.close();
  console.log('Wrote individual rainfall, SST and taro chart panels.');
} finally {
  server.kill('SIGTERM');
}
