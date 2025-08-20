// src/hooks/useTransactions.ts
import { useState } from 'react';

export const useTransactions = () => {
  const [loading, setLoading] = useState(true);

  const balanceData = {
    currentBalance: 1000,
    monthlyIncome: 2000,
    monthlyExpenses: 1000,
    previousMonthBalance: 800,
    percentageChange: 25,
  };

  const recentTransactions = [
    { id: '1', type: 'income', description: 'Salary', date: new Date(), amount: 2000, category: { name: 'Work' } },
    { id: '2', type: 'expense', description: 'Groceries', date: new Date(), amount: 200, category: { name: 'Food' } },
  ];

  const refresh = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1000);
  };

  setTimeout(() => setLoading(false), 1000);

  return { balanceData, recentTransactions, loading, refresh };
};
