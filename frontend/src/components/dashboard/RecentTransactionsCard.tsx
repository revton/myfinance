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
  Button,
  useTheme
} from '@mui/material';
import { 
  TrendingUp, 
  TrendingDown,
  Category,
  Receipt
} from '@mui/icons-material';
import { useTransactions } from '../../hooks/useTransactions';
import { useNavigate } from 'react-router-dom';
import AdvancedLoadingState from '../common/AdvancedLoadingState';
import AnimatedList from '../common/AnimatedList';

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
  const { recentTransactions, loading, refresh } = useTransactions();
  const navigate = useNavigate();
  const theme = useTheme();
  
  // Card header that's consistent across all states
  const cardHeader = (
    <Box sx={{ bgcolor: theme.palette.primary.main, py: 1, px: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Box display="flex" alignItems="center" gap={1}>
          <Receipt sx={{ color: 'white' }} />
          <Typography variant="h6" sx={{ color: 'white' }}>
            Transações Recentes
          </Typography>
        </Box>
        <Button 
          size="small" 
          onClick={() => navigate('/transactions')} 
          variant="outlined"
          sx={{ 
            color: 'white', 
            borderColor: 'white',
            '&:hover': {
              borderColor: 'rgba(255,255,255,0.8)',
              backgroundColor: 'rgba(255,255,255,0.1)'
            }
          }}
        >
          Ver Todas
        </Button>
      </Box>
    </Box>
  );

  // Transaction list content
  const transactionsContent = (
    <CardContent>
      {recentTransactions && recentTransactions.length > 0 ? (
        <AnimatedList>
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
                      {formatDate(new Date(transaction.created_at))}
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
                secondaryTypographyProps={{ component: 'span' }}
              />
              <Chip
                label={formatCurrency(transaction.amount)}
                color={transaction.type === 'income' ? 'success' : 'error'}
                variant="outlined"
                size="small"
              />
            </ListItem>
          ))}
        </AnimatedList>
      ) : (
        <Box display="flex" flexDirection="column" alignItems="center" py={3}>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            Nenhuma transação recente encontrada
          </Typography>
          <Button 
            variant="outlined" 
            size="small" 
            onClick={() => navigate('/transactions/new')}
            sx={{ mt: 1 }}
          >
            Adicionar Transação
          </Button>
        </Box>
      )}
    </CardContent>
  );

  return (
    <Card elevation={3} sx={{ borderRadius: 2, overflow: 'hidden' }}>
      {cardHeader}
      
      <AdvancedLoadingState
        isLoading={loading}
        error={!recentTransactions && !loading ? new Error("Falha ao carregar transações") : null}
        onRetry={refresh}
        loadingText="Carregando transações..."
        errorText="Não foi possível carregar as transações recentes."
        height="auto"
        showSkeleton={true}
      >
        {transactionsContent}
      </AdvancedLoadingState>
    </Card>
  );
};