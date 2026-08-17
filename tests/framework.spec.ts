import { test, expect } from '@playwright/test';
test('draft framework renders its evidence guardrails', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'The Year We Plan For' })).toBeVisible();
  await expect(page.getByText('What this draft does not do')).toBeVisible();
  await expect(page.locator('#rainfall-chart svg')).toBeVisible();
  await expect(page.locator('#sst-chart svg')).toBeVisible();
});
