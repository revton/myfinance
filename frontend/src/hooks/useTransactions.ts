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
      const response = await axios.get(`${API_BASE_URL}${APP_CONFIG.api.endpoints.transactions}`);
      // Assuming the API returns an object with recentTransactions and balanceData
      setRecentTransactions(response.data.recentTransactions || []);
      setBalanceData(response.data.balanceData || null);
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
