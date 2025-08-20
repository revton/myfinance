// src/contexts/TransactionContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: Date;
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
  const [transactions, setTransactions] = useState<Transaction[]>([
    { id: '1', type: 'income', description: 'Salary', date: new Date(), amount: 2000, category_id: '3' },
    { id: '2', type: 'expense', description: 'Groceries', date: new Date(), amount: 200, category_id: '1' },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <TransactionContext.Provider value={{ transactions, loading, error }}>
      {children}
    </TransactionContext.Provider>
  );
};

export const useTransactions = () => useContext(TransactionContext);
