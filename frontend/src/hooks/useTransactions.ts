// src/hooks/useTransactions.ts
import { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, APP_CONFIG } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  description: string;
  date: string; // Changed to string to match API response
  amount: number;
  category?: {
    name: string;
  };
}

interface BalanceData {
  currentBalance: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  previousMonthBalance: number;
  percentageChange: number;
}

export const useTransactions = () => {
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [balanceData, setBalanceData] = useState<BalanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<Transaction[]>(`${API_BASE_URL}${APP_CONFIG.api.endpoints.transactions}`);
      const fetchedTransactions = response.data;

      // Calculate balance data from fetched transactions
      const currentBalance = fetchedTransactions.reduce((sum, t) => 
        t.type === 'income' ? sum + t.amount : sum - t.amount, 0);
      const monthlyIncome = fetchedTransactions
        .filter(t => t.type === 'income' && new Date(t.date).getMonth() === new Date().getMonth())
        .reduce((sum, t) => sum + t.amount, 0);
      const monthlyExpenses = fetchedTransactions
        .filter(t => t.type === 'expense' && new Date(t.date).getMonth() === new Date().getMonth())
        .reduce((sum, t) => sum + t.amount, 0);
      
      // Placeholder for previousMonthBalance and percentageChange - requires more complex logic
      // For now, setting to dummy values or 0
      const previousMonthBalance = 0; // This would require fetching previous month's transactions
      const percentageChange = 0; // This would require previous month's balance

      setRecentTransactions(fetchedTransactions);
      setBalanceData({
        currentBalance,
        monthlyIncome,
        monthlyExpenses,
        previousMonthBalance,
        percentageChange,
      });
    } catch (err) {
      console.error('Error fetching transactions:', err);
      setError('Failed to load transactions.');
      setRecentTransactions([]); // Clear transactions on error
      setBalanceData(null); // Clear balance data on error
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const refresh = () => {
    fetchTransactions();
  };

  return { balanceData, recentTransactions, loading, error, refresh };
};
