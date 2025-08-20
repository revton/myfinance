// src/components/transactions/TransactionItem.tsx
import React from 'react';
import {
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Box,
  Typography
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  date: Date;
  category_id?: string;
  notes?: string;
}

interface TransactionItemProps {
  transaction: Transaction;
  onEdit?: (transaction: Transaction) => void;
  onDelete?: (transactionId: string) => void;
}

const TransactionItem: React.FC<TransactionItemProps> = ({ transaction, onEdit, onDelete }) => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <ListItem divider>
      <ListItemText
        primary={transaction.description}
        secondary={new Date(transaction.date).toLocaleDateString('pt-BR')}
      />
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Chip
          label={formatCurrency(transaction.amount)}
          color={transaction.type === 'income' ? 'success' : 'error'}
          size="small"
        />
        <ListItemSecondaryAction>
          {onEdit && (
            <IconButton edge="end" aria-label="edit" onClick={() => onEdit(transaction)}>
              <EditIcon />
            </IconButton>
          )}
          {onDelete && (
            <IconButton edge="end" aria-label="delete" onClick={() => onDelete(transaction.id)}>
              <DeleteIcon />
            </IconButton>
          )}
        </ListItemSecondaryAction>
      </Box>
    </ListItem>
  );
};

export default TransactionItem;