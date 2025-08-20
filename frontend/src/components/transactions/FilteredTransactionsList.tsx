// src/components/transactions/FilteredTransactionsList.tsx
import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Skeleton,
  Alert
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useTransactions } from '../../contexts/TransactionContext';
import { useAdvancedFilters } from '../../hooks/useAdvancedFilters';
import AdvancedFilters from '../filters/AdvancedFilters';
import TransactionItem from './TransactionItem';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  created_at: string;
  category_id?: string;
  notes?: string;
}

interface FilteredTransactionsListProps {
  onEditTransaction?: (transaction: Transaction) => void;
  onDeleteTransaction?: (transactionId: string) => void;
}

const FilteredTransactionsList: React.FC<FilteredTransactionsListProps> = ({
  onEditTransaction,
  onDeleteTransaction
}) => {
  const { transactions, loading, error } = useTransactions();
  const { filters, updateFilters } = useAdvancedFilters({
    onFiltersChange: (newFilters) => {
      console.log('Filtros aplicados:', newFilters);
    }
  });

  const filteredTransactions = useMemo(() => {
    if (!transactions) return [];

    return transactions.filter(transaction => {
      // Filtro por período
      if (filters.dateRange?.startDate || filters.dateRange?.endDate) {
        const transactionDate = new Date(transaction.created_at);
        if (filters.dateRange.startDate && transactionDate < filters.dateRange.startDate) {
          return false;
        }
        if (filters.dateRange.endDate && transactionDate > filters.dateRange.endDate) {
          return false;
        }
      }

      // Filtro por categorias
      if (filters.categories && filters.categories.length > 0) {
        if (!transaction.category_id || !filters.categories.includes(transaction.category_id)) {
          return false;
        }
      }

      // Filtro por valor
      if (filters.amountRange?.minAmount || filters.amountRange?.maxAmount) {
        const amount = Number(transaction.amount);
        if (filters.amountRange.minAmount && amount < filters.amountRange.minAmount) {
          return false;
        }
        if (filters.amountRange.maxAmount && amount > filters.amountRange.maxAmount) {
          return false;
        }
      }

      // Filtro por tipo
      if (filters.amountRange?.type && filters.amountRange.type !== 'all') {
        if (transaction.type !== filters.amountRange.type) {
          return false;
        }
      }

      // Filtro por status
      if (filters.status?.type && filters.status.type !== 'all') {
        if (transaction.type !== filters.status.type) {
          return false;
        }
      }

      // Filtro por categoria (status)
      if (filters.status?.hasCategory === true) {
        if (!transaction.category_id) {
          return false;
        }
      }

      // Filtro por notas (status)
      if (filters.status?.hasNotes === true) {
        if (!transaction.notes) {
          return false;
        }
      }

      return true;
    });
  }, [transactions, filters]);

  if (loading) {
    return (
      <Box>
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Erro ao carregar transações: {error}
      </Alert>
    );
  }

  return (
    <Box>
      <AdvancedFilters
        onFiltersChange={updateFilters}
        onSaveFilters={(filters, name) => {
          console.log('Salvando filtros:', name, filters);
        }}
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">
          Transações ({filteredTransactions.length})
        </Typography>
        
        {filteredTransactions.length !== transactions?.length && (
          <Chip
            label={`Filtrado de ${transactions?.length || 0} transações`}
            color="primary"
            variant="outlined"
            size="small"
          />
        )}
      </Box>

      {filteredTransactions.length === 0 ? (
        <Alert severity="info">
          Nenhuma transação encontrada com os filtros aplicados.
        </Alert>
      ) : (
        <List>
          {filteredTransactions.map((transaction) => (
            <TransactionItem
              key={transaction.id}
              transaction={transaction}
              onEdit={onEditTransaction}
              onDelete={onDeleteTransaction}
            />
          ))}
        </List>
      )}
    </Box>
  );
};

export default FilteredTransactionsList;