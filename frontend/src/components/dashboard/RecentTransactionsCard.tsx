// src/components/dashboard/RecentTransactionsCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  ListItemIcon,
  Chip,
  Box,
  Button 
} from '@mui/material';
import { 
  TrendingUp, 
  TrendingDown,
  Category 
} from '@mui/icons-material';
import { useTransactions } from '../../hooks/useTransactions';
import { useNavigate } from 'react-router-dom';

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('pt-BR').format(date);
};

export const RecentTransactionsCard: React.FC = () => {
  const { recentTransactions, loading } = useTransactions();
  const navigate = useNavigate();
  
  if (loading) {
    return <Card><CardContent><Typography>Carregando...</Typography></CardContent></Card>;
  }
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" color="text.secondary">
            Transações Recentes
          </Typography>
          <Button size="small" onClick={() => navigate('/transactions')}>
            Ver Todas
          </Button>
        </Box>
        
        <List dense>
          {recentTransactions.map((transaction) => (
            <ListItem key={transaction.id} divider>
              <ListItemIcon>
                {transaction.type === 'income' ? (
                  <TrendingUp color="success" />
                ) : (
                  <TrendingDown color="error" />
                )}
              </ListItemIcon>
              <ListItemText
                primary={transaction.description}
                secondary={
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body2" color="text.secondary" component="span">
                      {formatDate(transaction.date)}
                    </Typography>
                    {transaction.category && (
                      <>
                        <Category fontSize="small" />
                        <Typography variant="body2" color="text.secondary" component="span">
                          {transaction.category.name}
                        </Typography>
                      </>
                    )}
                  </Box>
                }
              />
              <Chip
                label={formatCurrency(transaction.amount)}
                color={transaction.type === 'income' ? 'success' : 'error'}
                variant="outlined"
                size="small"
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};