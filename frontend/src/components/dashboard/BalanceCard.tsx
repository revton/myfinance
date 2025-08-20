// src/components/dashboard/BalanceCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Chip,
  IconButton 
} from '@mui/material';
import { 
  TrendingUp, 
  TrendingDown, 
  Refresh 
} from '@mui/icons-material';
import { useTransactions } from '../../hooks/useTransactions';

interface BalanceData {
  currentBalance: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  previousMonthBalance: number;
  percentageChange: number;
}

export const BalanceCard: React.FC = () => {
  const { balanceData, loading, refresh } = useTransactions();
  
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };
  
  const getBalanceColor = (balance: number) => {
    return balance >= 0 ? 'success.main' : 'error.main';
  };
  
  const getTrendIcon = (percentageChange: number) => {
    return percentageChange >= 0 ? <TrendingUp /> : <TrendingDown />;
  };
  
  if (loading) {
    return <Card><CardContent><Typography>Carregando...</Typography></CardContent></Card>;
  }
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" color="text.secondary">
            Saldo Atual
          </Typography>
          <IconButton onClick={refresh} size="small">
            <Refresh />
          </IconButton>
        </Box>
        
        <Typography 
          variant="h3" 
          color={getBalanceColor(balanceData.currentBalance)}
          fontWeight="bold"
          mb={2}
        >
          {formatCurrency(balanceData.currentBalance)}
        </Typography>
        
        <Box display="flex" gap={2} mb={2}>
          <Chip
            icon={<TrendingUp />}
            label={`Receitas: ${formatCurrency(balanceData.monthlyIncome)}`}
            color="success"
            variant="outlined"
          />
          <Chip
            icon={<TrendingDown />}
            label={`Despesas: ${formatCurrency(balanceData.monthlyExpenses)}`}
            color="error"
            variant="outlined"
          />
        </Box>
        
        <Box display="flex" alignItems="center" gap={1}>
          {getTrendIcon(balanceData.percentageChange)}
          <Typography variant="body2" color="text.secondary">
            {balanceData.percentageChange >= 0 ? '+' : ''}
            {balanceData.percentageChange.toFixed(1)}% em relação ao mês anterior
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};