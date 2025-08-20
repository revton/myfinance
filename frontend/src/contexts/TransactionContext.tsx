// src/contexts/TransactionContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, APP_CONFIG } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  created_at: string;
  category_id?: string;
  notes?: string;
}

interface TransactionContextData {
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
}

const TransactionContext = createContext<TransactionContextData>({} as TransactionContextData);

export const TransactionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      // Note: The API endpoint requires a trailing slash
      const response = await axios.get<Transaction[]>(`${API_BASE_URL}${APP_CONFIG.api.endpoints.transactions}/`);
      setTransactions(response.data);
    } catch (err: any) {
      console.error('Error fetching transactions:', err);
      setError(err.response?.data?.detail || 'Failed to load transactions.');
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <TransactionContext.Provider value={{ transactions, loading, error }}>
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => useContext(TransactionContext);
