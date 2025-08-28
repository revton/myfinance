# 🎨 Dashboard - Melhorias de UX

## 📋 **Visão Geral**

O dashboard da Fase 2 será a página inicial do MyFinance, fornecendo uma visão geral rápida e intuitiva das finanças pessoais da família.

### 🎯 **Objetivos**
- Visão geral rápida das finanças
- Resumos visuais e intuitivos
- Acesso rápido às funcionalidades principais
- Interface responsiva para todos os dispositivos

---

## 🏗️ **Arquitetura da Interface**

### **Layout Principal**
```typescript
// src/pages/DashboardPage.tsx
import React from 'react';
import { Grid, Container, Paper } from '@mui/material';
import { 
  BalanceCard, 
  RecentTransactionsCard, 
  CategorySummaryCard,
  QuickActionsCard 
} from '../components/dashboard';

export const DashboardPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Grid container spacing={3}>
        {/* Cards principais */}
        <Grid item xs={12} md={8}>
          <BalanceCard />
        </Grid>
        <Grid item xs={12} md={4}>
          <QuickActionsCard />
        </Grid>
        
        {/* Resumos */}
        <Grid item xs={12} md={6}>
          <CategorySummaryCard />
        </Grid>
        <Grid item xs={12} md={6}>
          <RecentTransactionsCard />
        </Grid>
      </Grid>
    </Container>
  );
};
```

---

## 🎯 **Componentes do Dashboard**

### **1. BalanceCard - Card de Saldo**

#### **Funcionalidades**
- Saldo atual (receitas - despesas)
- Receitas do mês atual
- Despesas do mês atual
- Comparação com mês anterior
- Indicador visual (verde/vermelho)

#### **Implementação**
```typescript
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
```

### **2. QuickActionsCard - Ações Rápidas**

#### **Funcionalidades**
- Botões para ações principais
- Adicionar transação
- Ver relatórios
- Gerenciar categorias
- Configurações

#### **Implementação**
```typescript
// src/components/dashboard/QuickActionsCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Stack 
} from '@mui/material';
import { 
  Add, 
  Assessment, 
  Category, 
  Settings 
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export const QuickActionsCard: React.FC = () => {
  const navigate = useNavigate();
  
  const actions = [
    {
      label: 'Nova Transação',
      icon: <Add />,
      color: 'primary' as const,
      onClick: () => navigate('/transactions/new')
    },
    {
      label: 'Relatórios',
      icon: <Assessment />,
      color: 'secondary' as const,
      onClick: () => navigate('/reports')
    },
    {
      label: 'Categorias',
      icon: <Category />,
      color: 'success' as const,
      onClick: () => navigate('/categories')
    },
    {
      label: 'Configurações',
      icon: <Settings />,
      color: 'info' as const,
      onClick: () => navigate('/settings')
    }
  ];
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" color="text.secondary" mb={2}>
          Ações Rápidas
        </Typography>
        
        <Stack spacing={1}>
          {actions.map((action, index) => (
            <Button
              key={index}
              variant="outlined"
              color={action.color}
              startIcon={action.icon}
              onClick={action.onClick}
              fullWidth
              sx={{ justifyContent: 'flex-start' }}
            >
              {action.label}
            </Button>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};
```

### **3. CategorySummaryCard - Resumo por Categorias**

#### **Funcionalidades**
- Top 5 categorias com mais gastos
- Gráfico de pizza simples
- Valores e percentuais
- Link para detalhes

#### **Implementação**
```typescript
// src/components/dashboard/CategorySummaryCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  ListItemIcon,
  Box,
  Button 
} from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { useCategories } from '../../hooks/useCategories';
import { CategoryIcon } from '../categories/CategoryIcon';

interface CategorySummary {
  id: string;
  name: string;
  icon: string;
  color: string;
  amount: number;
  percentage: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export const CategorySummaryCard: React.FC = () => {
  const { categorySummary, loading } = useCategories();
  
  if (loading) {
    return <Card><CardContent><Typography>Carregando...</Typography></CardContent></Card>;
  }
  
  const chartData = categorySummary.map((cat, index) => ({
    name: cat.name,
    value: cat.amount,
    color: COLORS[index % COLORS.length]
  }));
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" color="text.secondary">
            Gastos por Categoria
          </Typography>
          <Button size="small" onClick={() => navigate('/categories')}>
            Ver Todas
          </Button>
        </Box>
        
        <Box display="flex" gap={2}>
          {/* Gráfico */}
          <Box flex={1} height={200}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </Box>
          
          {/* Lista */}
          <Box flex={1}>
            <List dense>
              {categorySummary.slice(0, 5).map((category) => (
                <ListItem key={category.id}>
                  <ListItemIcon>
                    <CategoryIcon 
                      icon={category.icon} 
                      color={category.color} 
                      size="small" 
                    />
                  </ListItemIcon>
                  <ListItemText
                    primary={category.name}
                    secondary={`${category.percentage.toFixed(1)}% - ${formatCurrency(category.amount)}`}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};
```

### **4. RecentTransactionsCard - Transações Recentes**

#### **Funcionalidades**
- Últimas 5 transações
- Informações essenciais
- Status visual (receita/despesa)
- Link para ver todas

#### **Implementação**
```typescript
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
import { formatCurrency, formatDate } from '../../utils/formatters';

export const RecentTransactionsCard: React.FC = () => {
  const { recentTransactions, loading } = useTransactions();
  
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
                    <Typography variant="body2" color="text.secondary">
                      {formatDate(transaction.date)}
                    </Typography>
                    {transaction.category && (
                      <>
                        <Category fontSize="small" />
                        <Typography variant="body2" color="text.secondary">
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
```

---

## 🎨 **Design System**

### **Cores**
```typescript
// src/theme/colors.ts
export const dashboardColors = {
  success: '#4CAF50',
  error: '#F44336',
  warning: '#FF9800',
  info: '#2196F3',
  primary: '#1976D2',
  secondary: '#9C27B0',
  background: '#FAFAFA',
  surface: '#FFFFFF',
  text: {
    primary: '#212121',
    secondary: '#757575',
    disabled: '#BDBDBD'
  }
};
```

### **Tipografia**
```typescript
// src/theme/typography.ts
export const dashboardTypography = {
  h3: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2
  },
  h6: {
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4
  },
  body1: {
    fontSize: '1rem',
    lineHeight: 1.5
  },
  body2: {
    fontSize: '0.875rem',
    lineHeight: 1.4
  }
};
```

---

## 📱 **Responsividade**

### **Breakpoints**
```typescript
// src/theme/breakpoints.ts
export const breakpoints = {
  xs: 0,    // Extra small devices (phones)
  sm: 600,  // Small devices (tablets)
  md: 960,  // Medium devices (desktops)
  lg: 1280, // Large devices (large desktops)
  xl: 1920  // Extra large devices
};
```

### **Layout Responsivo**
```typescript
// src/components/dashboard/DashboardLayout.tsx
import React from 'react';
import { Grid, useTheme, useMediaQuery } from '@mui/material';

export const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  return (
    <Grid container spacing={isMobile ? 2 : 3}>
      {React.Children.map(children, (child) => (
        <Grid item xs={12} md={6} lg={4}>
          {child}
        </Grid>
      ))}
    </Grid>
  );
};
```

---

## ⚡ **Performance**

### **Otimizações**
- Lazy loading de componentes
- Memoização de dados
- Debounce em atualizações
- Cache de dados

### **Loading States**
```typescript
// src/components/common/LoadingCard.tsx
import React from 'react';
import { Card, CardContent, Skeleton } from '@mui/material';

export const LoadingCard: React.FC = () => (
  <Card>
    <CardContent>
      <Skeleton variant="text" width="60%" height={32} />
      <Skeleton variant="text" width="40%" height={24} />
      <Skeleton variant="rectangular" width="100%" height={100} />
    </CardContent>
  </Card>
);
```

---

## 🧪 **Testes**

### **Testes de Componente**
```typescript
// src/components/dashboard/__tests__/BalanceCard.test.tsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { BalanceCard } from '../BalanceCard';

describe('BalanceCard', () => {
  it('should display current balance', () => {
    render(<BalanceCard />);
    expect(screen.getByText(/Saldo Atual/i)).toBeInTheDocument();
  });
  
  it('should format currency correctly', () => {
    render(<BalanceCard />);
    expect(screen.getByText(/R\$/)).toBeInTheDocument();
  });
});
```

---

## 📋 **Checklist de Implementação - Status Atual**

### **Componentes**
- ✅ BalanceCard (corrigido e funcional)
- ✅ QuickActionsCard
- ✅ CategorySummaryCard (com gráficos interativos)
- ✅ RecentTransactionsCard
- ✅ LoadingCard

### **Funcionalidades**
- ✅ Layout responsivo
- ✅ Loading states
- ✅ Error handling
- ✅ Refresh data
- ✅ Navigation

### **Design**
- ✅ Tema consistente
- ✅ Cores padronizadas
- ✅ Tipografia
- ✅ Ícones
- ⏳ Animações

### **Performance**
- ✅ Lazy loading
- ✅ Memoização
- ✅ Debounce
- ✅ Cache
- ⏳ Otimizações avançadas

### **Funcionalidades Completas**
- ✅ Gráficos interativos
- ✅ Filtros avançados no dashboard
- ⏳ Exportação de dados
- ⏳ Comparação temporal avançada

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack 