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
import AdvancedLoadingState from '../common/AdvancedLoadingState';

interface BalanceData {
  currentBalance: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  previousMonthBalance: number;
  percentageChange: number;
}

export const BalanceCard: React.FC = () => {
  const { balanceData, loading, refresh } = useTransactions();
  const theme = useTheme();
  
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
  
  // Card header that's consistent across all states
  const cardHeader = (
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
  );
  
  // Balance content to display when data is loaded
  const balanceContent = (
    <CardContent sx={{ pt: 2 }}>
      <Typography 
        variant="h3" 
        color={getBalanceColor(balanceData?.currentBalance || 0)}
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
        {formatCurrency(balanceData?.currentBalance || 0)}
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
            {formatCurrency(balanceData?.monthlyIncome || 0)}
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
            {formatCurrency(balanceData?.monthlyExpenses || 0)}
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
            borderColor: (balanceData?.percentageChange || 0) >= 0 ? 'success.main' : 'error.main'
          }}
        >
          {getTrendIcon(balanceData?.percentageChange || 0)}
          <Typography variant="body2" color="text.secondary">
            <strong>
              {(balanceData?.percentageChange || 0) >= 0 ? '+' : ''}
              {(balanceData?.percentageChange || 0).toFixed(1)}%
            </strong> em relação ao mês anterior
          </Typography>
        </Box>
      </Tooltip>
    </CardContent>
  );
  
  return (
    <Card elevation={3} sx={{ borderRadius: 2, overflow: 'hidden' }}>
      {cardHeader}
      
      <AdvancedLoadingState
        isLoading={loading}
        error={!balanceData && !loading ? new Error("Falha ao carregar dados") : null}
        onRetry={refresh}
        loadingText="Carregando dados financeiros..."
        errorText="Não foi possível carregar os dados de saldo."
        height="auto"
        showSkeleton={true}
      >
        {balanceContent}
      </AdvancedLoadingState>
    </Card>
  );
};