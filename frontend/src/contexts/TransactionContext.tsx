// src/contexts/TransactionContext.tsx
import React, { createContext, useContext } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
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
  isLoading: boolean;
  error: Error | null;
  refetchTransactions: () => void;
}

const TransactionContext = createContext<TransactionContextData>({} as TransactionContextData);

const fetchTransactions = async (): Promise<Transaction[]> => {
  const response = await api.get<Transaction[]>(APP_CONFIG.api.endpoints.transactions);
  return response.data;
};

export const TransactionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = useQueryClient();

  const { data: transactions = [], isLoading, error, refetch } = useQuery<Transaction[], Error>({
    queryKey: ['transactions'],
    queryFn: fetchTransactions,
  });

  const refetchTransactions = () => {
    queryClient.invalidateQueries({ queryKey: ['transactions'] });
  };

  return (
    <TransactionContext.Provider value={{ transactions, isLoading, error, refetchTransactions }}>
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => useContext(TransactionContext);
