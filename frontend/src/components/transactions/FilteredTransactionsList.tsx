// src/components/transactions/FilteredTransactionsList.tsx
import React, { useState, useEffect, useMemo, useCallback } from 'react';
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
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useTransactions } from '../../contexts/TransactionContext';
import { useAdvancedFilters } from '../../hooks/useAdvancedFilters';
import AdvancedFilters from '../filters/AdvancedFilters';
import TransactionItem from './TransactionItem';
import { useNavigate } from 'react-router-dom';
import api from '../../lib/api';
import { APP_CONFIG } from '../../config';

interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
}

// Import filter types from the component
interface DateRangeFilters {
  startDate?: Date;
  endDate?: Date;
}

interface AmountRangeFilters {
  minAmount?: number;
  maxAmount?: number;
}

interface StatusFilters {
  type: 'all' | 'income' | 'expense';
  status: 'all' | 'pending' | 'completed';
}

interface CombinedFilters {
  dateRange?: DateRangeFilters;
  categories?: string[];
  amountRange?: AmountRangeFilters;
  status?: StatusFilters;
}

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  created_at: string;
  category_id?: string;
  category?: Category | null;
  notes?: string;
}

interface FilteredTransactionsListProps {
  onDeleteTransaction?: (transactionId: string) => void;
}

const FilteredTransactionsList: React.FC<FilteredTransactionsListProps> = ({
  onDeleteTransaction
}) => {
  const navigate = useNavigate();
  const { transactions, loading, error, fetchTransactions } = useTransactions();
  const { filters, updateFilters } = useAdvancedFilters();
  
  const handleFiltersChange = useCallback((newFilters: CombinedFilters) => {
    updateFilters(newFilters);
  }, [updateFilters]);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [transactionToDelete, setTransactionToDelete] = useState<string | null>(null);

  const handleDeleteClick = (transactionId: string) => {
    setTransactionToDelete(transactionId);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!transactionToDelete) return;
    
    try {
      await api.delete(`${APP_CONFIG.api.endpoints.transactions}${transactionToDelete}`);
      // Refresh transactions list
      fetchTransactions();
      setDeleteDialogOpen(false);
      setTransactionToDelete(null);
    } catch (err: any) {
      console.error('Error deleting transaction:', err);
      alert(err.response?.data?.detail || 'Erro ao deletar transação.');
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setTransactionToDelete(null);
  };

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
      if (filters.status?.type && filters.status.type !== 'all') {
        if (transaction.type !== filters.status.type) {
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
        initialFilters={filters}
        onFiltersChange={handleFiltersChange}
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
              onEdit={() => navigate(`/transactions/${transaction.id}/edit`)}
              onDelete={() => handleDeleteClick(transaction.id)}
            />
          ))}
        </List>
      )}

      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="delete-transaction-dialog-title"
        aria-describedby="delete-transaction-dialog-description"
      >
        <DialogTitle id="delete-transaction-dialog-title">
          Confirmar exclusão
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-transaction-dialog-description">
            Tem certeza que deseja excluir esta transação? Esta ação não pode ser desfeita.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} color="primary">
            Cancelar
          </Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Excluir
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default FilteredTransactionsList;