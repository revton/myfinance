// src/components/transactions/TransactionItem.tsx
import React from 'react';
import {
  IconButton,
  Chip,
  Box,
  Typography
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
}

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

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return 'Data inválida';
      }
      return date.toLocaleDateString('pt-BR');
    } catch (error) {
      return 'Data inválida';
    }
  };

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        alignItems: 'center',
        p: 2,
        borderBottom: '1px solid',
        borderColor: 'divider',
        width: '100%'
      }}
    >
      <Box sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography component="span">{transaction.description}</Typography>
          {transaction.category && (
            <Chip
              label={transaction.category.name}
              size="small"
              sx={{ 
                backgroundColor: transaction.category.color || '#e0e0e0',
                color: 'white',
                height: '20px'
              }}
            />
          )}
        </Box>
        <Typography variant="body2" color="text.secondary">
          {formatDate(transaction.created_at)}
        </Typography>
      </Box>
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: 2,
        marginLeft: 'auto'
      }}>
        <Chip
          label={formatCurrency(transaction.amount)}
          color={transaction.type === 'income' ? 'success' : 'error'}
          size="small"
        />
        <Box sx={{ display: 'flex', gap: 0.5 }}>
          {onEdit && (
            <IconButton 
              aria-label="edit" 
              onClick={() => onEdit(transaction)} 
              size="small"
              sx={{ 
                color: 'primary.main',
                '&:hover': {
                  backgroundColor: 'primary.light',
                  opacity: 0.8
                }
              }}
            >
              <EditIcon fontSize="small" />
            </IconButton>
          )}
          {onDelete && (
            <IconButton 
              aria-label="delete" 
              onClick={() => onDelete(transaction.id)} 
              size="small"
              sx={{ 
                color: 'error.main',
                '&:hover': {
                  backgroundColor: 'error.light',
                  opacity: 0.8
                }
              }}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default TransactionItem;