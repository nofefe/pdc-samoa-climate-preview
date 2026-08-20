import { test, expect } from '@playwright/test';

test('draft framework renders its evidence guardrails and seasonal analysis', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'The Year We Plan For' })).toBeVisible();
  await expect(page.getByText('What this draft does not do')).toBeVisible();
  await expect(page.locator('#rainfall-chart svg')).toBeVisible();
  await expect(page.locator('#sst-chart svg')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Start with taro' })).toBeVisible();
  await expect(page.locator('#taro-chart svg')).toBeVisible();
  await expect(page.getByText('not evidence that climate caused this pattern')).toBeVisible();
  await expect(page.locator('#leaf-chart svg')).toBeVisible();
  await expect(page.locator('#rainfall-heatmap svg')).toBeVisible();
  await expect(page.locator('#enso-chart svg')).toBeVisible();
  await expect(page.locator('#forecast-chart svg')).toBeVisible();
  await expect(page.locator('#scope-map svg')).toBeVisible();
  await expect(page.getByText('retrospective model evaluation, not a 2026 forecast')).toBeVisible();
  await expect(page.getByText('not a risk map')).toBeVisible();
});

test('linked explorer responds to year, month and metric controls', async ({ page }) => {
  await page.goto('/');

  const year = page.getByLabel('Year to explore');
  const month = page.getByLabel('Month to inspect');
  await expect(year).toHaveValue('2015');
  await expect(page.locator('#explorer-chart svg')).toBeVisible();
  await expect(page.locator('#explorer-status')).toContainText('2015');

  await year.fill('1993');
  await month.selectOption('8');
  await page.getByRole('radio', { name: 'Departure from monthly normal' }).check();

  await expect(year).toHaveValue('1993');
  await expect(page.locator('#selected-year')).toHaveText('1993');
  await expect(page.getByRole('button', { name: '1993', exact: true })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#selected-month')).toHaveText('August');
  await expect(page.locator('#explorer-chart')).toHaveAttribute('data-metric', 'anomaly_mm');
  await expect(page.locator('#explorer-status')).toContainText('August 1993');
});

test('heat-map cells select their year and month in the explorer', async ({ page }) => {
  await page.goto('/');

  const cells = page.locator('#rainfall-heatmap rect[role="button"]');
  await expect(cells).toHaveCount(540);
  await cells.first().click();

  await expect(page.getByLabel('Year to explore')).toHaveValue('1981');
  await expect(page.getByLabel('Month to inspect')).toHaveValue('1');
  await expect(page.locator('#explorer-status')).toContainText('January 1981');
});

test('seasonal analysis and explorer are usable at phone width', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto('/');
  await expect(page.locator('#rainfall-heatmap svg')).toBeVisible();
  await expect(page.locator('#scope-map svg')).toBeVisible();
  await expect(page.locator('#explorer-chart svg')).toBeVisible();
  await page.getByLabel('Year to explore').fill('2020');
  await expect(page.locator('#selected-year')).toHaveText('2020');
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(375);
});
