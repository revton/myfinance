// src/hooks/useTransactions.ts
import { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, APP_CONFIG } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  description: string;
  created_at: string;
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

      // Calcular dados do saldo atual
      const currentBalance = fetchedTransactions.reduce((sum, t) => 
        t.type === 'income' ? sum + t.amount : sum - t.amount, 0);

      // Filtrar transações do mês atual
      const currentDate = new Date();
      const currentMonth = currentDate.getMonth();
      const currentYear = currentDate.getFullYear();
      
      const monthlyTransactions = fetchedTransactions.filter(t => {
        const transactionDate = new Date(t.created_at);
        return transactionDate.getMonth() === currentMonth && 
               transactionDate.getFullYear() === currentYear;
      });

      const monthlyIncome = monthlyTransactions
        .filter(t => t.type === 'income')
        .reduce((sum, t) => sum + t.amount, 0);
        
      const monthlyExpenses = monthlyTransactions
        .filter(t => t.type === 'expense')
        .reduce((sum, t) => sum + t.amount, 0);

      // Calcular transações do mês anterior
      const previousMonth = currentMonth === 0 ? 11 : currentMonth - 1;
      const previousYear = currentMonth === 0 ? currentYear - 1 : currentYear;
      
      const previousMonthTransactions = fetchedTransactions.filter(t => {
        const transactionDate = new Date(t.created_at);
        return transactionDate.getMonth() === previousMonth && 
               transactionDate.getFullYear() === previousYear;
      });

      const previousMonthBalance = previousMonthTransactions.reduce((sum, t) => 
        t.type === 'income' ? sum + t.amount : sum - t.amount, 0);

      // Calcular variação percentual
      let percentageChange = 0;
      if (previousMonthBalance !== 0) {
        percentageChange = ((currentBalance - previousMonthBalance) / Math.abs(previousMonthBalance)) * 100;
      } else if (currentBalance > 0) {
        percentageChange = 100; // Se não havia saldo no mês anterior mas há agora
      }

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
      setRecentTransactions([]);
      setBalanceData(null);
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
