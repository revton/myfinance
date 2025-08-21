// src/contexts/TransactionContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../lib/api';
import { APP_CONFIG } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  created_at: string;
  updated_at: string;
  category_id?: string;
  category?: Category | null;
  notes?: string;
}

interface TransactionContextData {
  transactions: Transaction[];
  loading: boolean;
  error: string | null;
  fetchTransactions: () => Promise<void>;
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
      const response = await api.get<Transaction[]>(APP_CONFIG.api.endpoints.transactions);
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
    <TransactionContext.Provider value={{ transactions, loading, error, fetchTransactions }}>
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => useContext(TransactionContext);
