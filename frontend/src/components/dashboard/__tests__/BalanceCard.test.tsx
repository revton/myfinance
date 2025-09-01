// src/components/dashboard/__tests__/BalanceCard.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { BalanceCard } from '../BalanceCard';
import { vi } from 'vitest';

// Mock the useTransactions hook
vi.mock('../../../hooks/useTransactions', () => ({
  useTransactions: () => ({
    balanceData: {
      currentBalance: 1000,
      monthlyIncome: 2000,
      monthlyExpenses: 1000,
      previousMonthBalance: 800,
      percentageChange: 25,
    },
    loading: false,
    refresh: vi.fn(),
  }),
}));

// Mock all MUI icons to prevent EMFILE errors
vi.mock('@mui/icons-material', () => ({
  TrendingUp: () => <div data-testid="trending-up">TrendingUp</div>,
  TrendingDown: () => <div data-testid="trending-down">TrendingDown</div>,
  Refresh: () => <div data-testid="refresh">Refresh</div>,
  AccountBalanceWallet: () => <div data-testid="account-balance-wallet">AccountBalanceWallet</div>,
  AttachMoney: () => <div data-testid="attach-money">AttachMoney</div>,
  MoneyOff: () => <div data-testid="money-off">MoneyOff</div>,
}));

describe('BalanceCard', () => {
  it('should display current balance', () => {
    // Act
    render(<BalanceCard />);

    // Assert
    expect(screen.getByText(/Saldo Atual/i)).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 3 })).toBeInTheDocument();
  });
  
  it('should format currency correctly for current balance', () => {
    // Act
    render(<BalanceCard />);

    // Assert - Using a more specific selector to target the main balance
    const balanceElement = screen.getByRole('heading', { level: 3 });
    expect(balanceElement).toHaveTextContent(/R\$\s?1\.000,00/i);
  });
  
  it('should display income and expenses', () => {
    // Act
    render(<BalanceCard />);

    // Assert
    expect(screen.getByText(/R\$\s?2\.000,00/i)).toBeInTheDocument(); // Income
    expect(screen.getByText(/Despesas/i)).toBeInTheDocument();
    expect(screen.getByText(/Receitas/i)).toBeInTheDocument();
  });
});