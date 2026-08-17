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

test('seasonal analysis is usable at phone width', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto('/');
  await expect(page.locator('#rainfall-heatmap svg')).toBeVisible();
  await expect(page.locator('#scope-map svg')).toBeVisible();
});
