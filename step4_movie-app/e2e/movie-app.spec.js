const { test, expect } = require('@playwright/test');

test('loads movies, filters by category, and requests an AI recommendation', async ({ page }) => {
  const failedVendorAssets = [];
  page.on('response', response => {
    if (response.url().includes('/vendor/') && response.status() >= 400) {
      failedVendorAssets.push(`${response.status()} ${response.url()}`);
    }
  });

  await expect.poll(async () => {
    try {
      return (await fetch('http://nginx-proxy')).status;
    } catch {
      return 0;
    }
  }, { timeout: 30000 }).toBe(200);
  await page.goto('/');
  await expect.poll(() => page.evaluate(() => customElements.get('bq-button') !== undefined)).toBe(true);
  expect(failedVendorAssets).toEqual([]);
  await expect(page.getByRole('heading', { name: 'Historias para cada estado de ánimo.' })).toBeVisible();
  await expect(page.locator('.movie')).toHaveCount(24);

  await page.locator('#category').selectOption('drama');
  await page.locator('#filter').click();
  await expect(page.locator('.movie')).toHaveCount(8);
  await expect(page.getByRole('heading', { name: 'The Shawshank Redemption' })).toBeVisible();

  await page.locator('#recommend').click();
  await expect(page.locator('#recommendation-text')).toContainText('una historia emotiva sobre la esperanza');
});
