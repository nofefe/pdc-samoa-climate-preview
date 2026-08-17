import { spawn } from 'node:child_process';
import { mkdir } from 'node:fs/promises';
import { chromium } from '@playwright/test';

const url = 'http://127.0.0.1:4322';
const server = spawn('npm', ['run', 'dev', '--', '--host', '127.0.0.1', '--port', '4322'], { stdio: 'pipe' });
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
try {
  for (let i = 0; i < 40; i += 1) {
    try { if ((await fetch(url)).ok) break; } catch { /* server is starting */ }
    await wait(250);
    if (i === 39) throw new Error('Astro server did not become ready');
  }
  await mkdir('artifacts', { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.screenshot({ path: 'artifacts/draft-framework.png', fullPage: true });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: 'artifacts/draft-framework.pdf', format: 'A4', printBackground: true, margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' } });
  await browser.close();
  console.log('Wrote artifacts/draft-framework.png and artifacts/draft-framework.pdf');
} finally {
  server.kill('SIGTERM');
}
