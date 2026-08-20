import { test, expect } from '@playwright/test';

test('four-act story renders one thesis and the primary evidence', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle('The Year We Plan For Does Not Exist');
  await expect(page.getByRole('heading', { name: 'The Year We Plan For Does Not Exist' })).toBeVisible();
  await expect(page.getByText('Use history to choose the tests, and local knowledge to choose the response.')).toBeVisible();
  await expect(page.getByText('I grew up in Aotearoa with a Māori mum and a Samoan dad.')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'What these data can and cannot tell us' })).toBeVisible();
  await expect(page.locator('#rainfall-chart svg')).toBeVisible();
  await expect(page.locator('#sst-chart svg')).toBeVisible();
  await expect(page.locator('#seasonal-normal-chart svg')).toBeVisible();
  await expect(page.locator('#rainfall-heatmap svg')).toBeVisible();
  await expect(page.locator('#taro-chart svg')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'National data can identify the tests. Communities help determine the response.' })).toBeVisible();
  await expect(page.getByText('DRAFT FRAMEWORK')).toHaveCount(0);
});

test('meaningful presets update the stress test and keep evidence in separate lanes', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('button', { name: /April 2016/ })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#episode-title')).toHaveText('April 2016 — unusually wet month');
  await expect(page.getByLabel('Year to explore')).toHaveValue('2016');
  await expect(page.getByLabel('Month to inspect')).toHaveValue('4');
  await expect(page.getByRole('radio', { name: 'Departure from monthly normal' })).toBeChecked();

  await page.getByRole('button', { name: /February 1998/ }).click();
  await expect(page.getByLabel('Year to explore')).toHaveValue('1998');
  await expect(page.getByLabel('Month to inspect')).toHaveValue('2');
  await expect(page.locator('#episode-title')).toContainText('unusually dry month');
  await expect(page.locator('#episode-what')).toContainText('211 mm below');
  await expect(page.locator('#selected-monthly')).toContainText('36 mm');
  await expect(page.getByRole('heading', { name: 'National and ocean context' })).toBeVisible();
  await expect(page.getByRole('heading', { name: /February in 1998/ })).toBeVisible();
  await expect(page.getByRole('heading', { name: /Taro yield in 1998/ })).toBeVisible();
});

test('heat map uses one roving keyboard stop and arrow navigation', async ({ page }) => {
  await page.goto('/');
  const cells = page.locator('#rainfall-heatmap rect[role="gridcell"]');
  await expect(cells).toHaveCount(540);
  await expect(page.locator('#rainfall-heatmap rect[role="gridcell"][tabindex="0"]')).toHaveCount(1);
  const active = page.locator('#rainfall-heatmap rect[role="gridcell"][tabindex="0"]');
  await expect(active).toHaveAttribute('aria-label', /2016 Apr/);
  await active.focus();
  await active.press('ArrowRight');
  const moved = page.locator('#rainfall-heatmap rect[role="gridcell"][tabindex="0"]');
  await expect(moved).toHaveAttribute('aria-label', /2016 May/);
  await moved.press('Enter');
  await expect(page.getByLabel('Year to explore')).toHaveValue('2016');
  await expect(page.getByLabel('Month to inspect')).toHaveValue('5');
  await expect(page.locator('#explorer-status')).toContainText('May 2016');
});

test('custom year, month and metric controls redraw the explorer', async ({ page }) => {
  await page.goto('/');
  await page.getByLabel('Year to explore').fill('1993');
  await page.getByLabel('Month to inspect').selectOption('8');
  await page.getByRole('radio', { name: 'Monthly total' }).check();
  await expect(page.locator('#selected-year')).toHaveText('1993');
  await expect(page.locator('#selected-month')).toHaveText('August');
  await expect(page.locator('#explorer-chart')).toHaveAttribute('data-metric', 'total_mm');
  await expect(page.locator('#episode-title')).toHaveText('Custom selection — August 1993');
  await expect(page.locator('#explorer-chart svg')).toBeVisible();
});

test('methods stay secondary and render on demand', async ({ page }) => {
  await page.goto('/');
  const methods = page.locator('#methods');
  await expect(methods).not.toHaveAttribute('open', '');
  await methods.locator('summary').click();
  await expect(methods).toHaveAttribute('open', '');
  await expect(page.locator('#enso-chart svg')).toBeVisible();
  await expect(page.locator('#forecast-chart svg')).toBeVisible();
  await expect(page.locator('#leaf-chart svg')).toBeVisible();
  await expect(page.locator('#scope-map svg')).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Development process' })).toBeVisible();
});

test('mobile story is legible, contained and uses controls as the primary interaction', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await expect(page.getByText('On mobile, use the year and month controls above.')).toBeVisible();
  await expect(page.getByLabel('Year to explore')).toBeVisible();
  await expect(page.getByLabel('Month to inspect')).toBeVisible();
  await page.getByRole('button', { name: /1994/ }).click();
  await expect(page.locator('#selected-taro')).toContainText('1,500');
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
  const chartFontSize = await page.locator('#rainfall-chart svg').evaluate((element) => Number.parseFloat(getComputedStyle(element).fontSize));
  expect(chartFontSize).toBeGreaterThanOrEqual(12);
});
