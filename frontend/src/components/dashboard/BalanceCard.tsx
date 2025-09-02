// src/components/dashboard/BalanceCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Chip,
  IconButton,
  Tooltip,
  Skeleton,
  Divider,
  useTheme
} from '@mui/material';
import { 
  TrendingUp, 
  TrendingDown, 
  Refresh,
  AccountBalanceWallet,
  AttachMoney,
  MoneyOff
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
  
  const theme = useTheme();
  
  if (loading) {
    return (
      <Card elevation={2}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Skeleton variant="text" width={120} height={32} />
            <Skeleton variant="circular" width={24} height={24} />
          </Box>
          <Skeleton variant="rectangular" width="100%" height={60} sx={{ mb: 2 }} />
          <Box display="flex" gap={2} mb={2}>
            <Skeleton variant="rectangular" width="48%" height={32} />
            <Skeleton variant="rectangular" width="48%" height={32} />
          </Box>
          <Skeleton variant="text" width="70%" height={24} />
        </CardContent>
      </Card>
    );
  }

  if (!balanceData) {
    return (
      <Card elevation={2}>
        <CardContent>
          <Box display="flex" alignItems="center" gap={1}>
            <AccountBalanceWallet color="error" />
            <Typography color="error">Não foi possível carregar os dados de saldo.</Typography>
          </Box>
          <Box mt={2}>
            <Tooltip title="Tentar novamente" arrow>
              <IconButton onClick={refresh} color="primary">
                <Refresh />
              </IconButton>
            </Tooltip>
          </Box>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <Card elevation={3} sx={{ borderRadius: 2, overflow: 'hidden' }}>
      <Box sx={{ bgcolor: theme.palette.primary.main, py: 1, px: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={1}>
            <AccountBalanceWallet sx={{ color: 'white' }} />
            <Typography variant="h6" sx={{ color: 'white' }}>
              Saldo Atual
            </Typography>
          </Box>
          <Tooltip title="Atualizar saldo" arrow>
            <IconButton onClick={refresh} size="small" sx={{ color: 'white' }}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      <CardContent sx={{ pt: 2 }}>
        <Typography 
          variant="h3" 
          color={getBalanceColor(balanceData.currentBalance)}
          fontWeight="bold"
          mb={2}
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 1,
            textAlign: 'center'
          }}
        >
          {formatCurrency(balanceData.currentBalance)}
        </Typography>
        
        <Divider sx={{ my: 2 }} />
        
        <Box display="flex" justifyContent="space-between" gap={2} mb={2}>
          <Box 
            sx={{ 
              flex: 1, 
              p: 1.5, 
              bgcolor: 'success.light', 
              borderRadius: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center'
            }}
          >
            <Tooltip title="Total de receitas do mês" arrow>
              <Box display="flex" alignItems="center" gap={0.5} mb={1}>
                <AttachMoney />
                <Typography variant="body2" fontWeight="medium" color="white">
                  Receitas
                </Typography>
              </Box>
            </Tooltip>
            <Typography variant="h6" fontWeight="bold" color="white">
              {formatCurrency(balanceData.monthlyIncome)}
            </Typography>
          </Box>
          
          <Box 
            sx={{ 
              flex: 1, 
              p: 1.5, 
              bgcolor: 'error.light', 
              borderRadius: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center'
            }}
          >
            <Tooltip title="Total de despesas do mês" arrow>
              <Box display="flex" alignItems="center" gap={0.5} mb={1}>
                <MoneyOff />
                <Typography variant="body2" fontWeight="medium" color="white">
                  Despesas
                </Typography>
              </Box>
            </Tooltip>
            <Typography variant="h6" fontWeight="bold" color="white">
              {formatCurrency(balanceData.monthlyExpenses)}
            </Typography>
          </Box>
        </Box>
        
        <Tooltip title="Comparação com o mês anterior" arrow placement="bottom">
          <Box 
            display="flex" 
            alignItems="center" 
            gap={1} 
            sx={{ 
              bgcolor: 'background.paper', 
              p: 1, 
              borderRadius: 1,
              border: '1px dashed',
              borderColor: balanceData.percentageChange >= 0 ? 'success.main' : 'error.main'
            }}
          >
            {getTrendIcon(balanceData.percentageChange)}
            <Typography variant="body2" color="text.secondary">
              <strong>
                {balanceData.percentageChange >= 0 ? '+' : ''}
                {balanceData.percentageChange.toFixed(1)}%
              </strong> em relação ao mês anterior
            </Typography>
          </Box>
        </Tooltip>
      </CardContent>
    </Card>
  );
};