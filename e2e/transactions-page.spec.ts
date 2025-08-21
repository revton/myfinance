import { test, expect } from '@playwright/test';

test('should display transactions without infinite loop error', async ({ page }) => {
  // Navigate to the transactions page
  await page.goto('/transactions');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Check that the page title is correct
  await expect(page.getByRole('heading', { name: 'Transações' })).toBeVisible();
  
  // Check for any console errors
  const errorLogs: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      errorLogs.push(msg.text());
      console.log('Browser console error:', msg.text());
    }
  });
  
  // Wait a bit to allow any potential infinite loop errors to occur
  await page.waitForTimeout(2000);
  
  // Check that there are no "Maximum update depth exceeded" errors
  const infiniteLoopErrors = errorLogs.filter(log => 
    log.includes('Maximum update depth exceeded')
  );
  
  expect(infiniteLoopErrors).toHaveLength(0);
  
  // Check that the page content is visible (not blank)
  // This could be checking for the filter button, transaction list, or "no transactions" message
  const filterButton = page.getByRole('button', { name: 'Filtros Avançados' });
  await expect(filterButton).toBeVisible();
  
  // Check if either transactions are displayed or a "no transactions" message
  const transactionsList = page.locator('ul[role="list"]');
  const noTransactionsMessage = page.getByText('Nenhuma transação encontrada');
  
  // Either the transactions list or the "no transactions" message should be visible
  const hasTransactionsList = await transactionsList.isVisible();
  const hasNoTransactionsMessage = await noTransactionsMessage.isVisible();
  
  expect(hasTransactionsList || hasNoTransactionsMessage).toBeTruthy();
});