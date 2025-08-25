// src/components/dashboard/__tests__/BalanceCard.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { BalanceCard } from '../BalanceCard';
import { useTransactions } from '../../../hooks/useTransactions';
import { vi } from 'vitest';

// Mock the useTransactions hook
vi.mock('../../../hooks/useTransactions');

// Mock @mui/icons-material
vi.mock('@mui/icons-material', () => ({
  Refresh: () => <div data-testid="refresh-icon" />,
  TrendingUp: () => <div data-testid="trending-up-icon" />,
  TrendingDown: () => <div data-testid="trending-down-icon" />,
}));

describe('BalanceCard', () => {
  it('should display current balance', () => {
    // Arrange
    (useTransactions as jest.Mock).mockReturnValue({
      balanceData: {
        currentBalance: 1000,
        monthlyIncome: 2000,
        monthlyExpenses: 1000,
        previousMonthBalance: 800,
        percentageChange: 25,
      },
      loading: false,
      refresh: vi.fn(),
    });

    // Act
    render(<BalanceCard />);

    // Assert
    expect(screen.getByText(/Saldo Atual/i)).toBeInTheDocument();
  });
  
  it('should format currency correctly', () => {
    // Arrange
    (useTransactions as jest.Mock).mockReturnValue({
      balanceData: {
        currentBalance: 1000,
        monthlyIncome: 2000,
        monthlyExpenses: 1000,
        previousMonthBalance: 800,
        percentageChange: 25,
      },
      loading: false,
      refresh: vi.fn(),
    });

    // Act
    render(<BalanceCard />);

    // Assert
    expect(screen.getByRole('heading', { level: 3, name: /R\$\s?1\.000,00/i })).toBeInTheDocument();
  });
});