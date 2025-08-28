# 🎯 Correção do BalanceCard - Plano de Implementação

## 📋 **Visão Geral**

Este documento descreve o plano para corrigir a implementação do componente `BalanceCard` no dashboard da Fase 2, que atualmente está tentando acessar uma propriedade `balanceData` que não existe no hook `useTransactions`.

## 🎯 **Objetivos**

- Corrigir o hook `useTransactions` para fornecer dados financeiros completos
- Atualizar o componente `BalanceCard` para usar os dados corretamente
- Garantir cálculos precisos de saldo, receitas, despesas e comparações mensais
- Manter a compatibilidade com o restante da aplicação

## 📊 **Problema Atual**

O componente `BalanceCard` está tentando acessar uma propriedade `balanceData` do hook `useTransactions`, mas esta propriedade não está sendo retornada corretamente. Além disso, os cálculos financeiros atuais estão incompletos, usando valores fixos para `previousMonthBalance` e `percentageChange`.

## 🛠️ **Solução Proposta**

### **1. Atualizar o hook `useTransactions`**

Vamos modificar o hook para:
1. Retornar uma propriedade `balanceData` com todos os dados necessários
2. Implementar cálculos completos para saldo atual, receitas mensais, despesas mensais
3. Calcular corretamente o saldo do mês anterior e a variação percentual
4. Adicionar tratamento de erros apropriado

### **2. Corrigir o componente `BalanceCard`**

Vamos atualizar o componente para:
1. Usar corretamente os dados fornecidos pelo hook
2. Tratar casos em que os dados estão carregando ou são nulos
3. Manter a interface de usuário existente

## 🏗️ **Implementação Detalhada**

### **Passo 1: Atualizar `useTransactions.ts`**

```typescript
// src/hooks/useTransactions.ts
import { useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL, APP_CONFIG } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  description: string;
  created_at: string;
  amount: number;
  category?: {
    name: string;
  };
}

interface BalanceData {
  currentBalance: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  previousMonthBalance: number;
  percentageChange: number;
}

export const useTransactions = () => {
  const [recentTransactions, setRecentTransactions] = useState<Transaction[]>([]);
  const [balanceData, setBalanceData] = useState<BalanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<Transaction[]>(`${API_BASE_URL}${APP_CONFIG.api.endpoints.transactions}`);
      const fetchedTransactions = response.data;

      // Calcular dados do saldo atual
      const currentBalance = fetchedTransactions.reduce((sum, t) => 
        t.type === 'income' ? sum + t.amount : sum - t.amount, 0);

      // Filtrar transações do mês atual
      const currentDate = new Date();
      const currentMonth = currentDate.getMonth();
      const currentYear = currentDate.getFullYear();
      
      const monthlyTransactions = fetchedTransactions.filter(t => {
        const transactionDate = new Date(t.created_at);
        return transactionDate.getMonth() === currentMonth && 
               transactionDate.getFullYear() === currentYear;
      });

      const monthlyIncome = monthlyTransactions
        .filter(t => t.type === 'income')
        .reduce((sum, t) => sum + t.amount, 0);
        
      const monthlyExpenses = monthlyTransactions
        .filter(t => t.type === 'expense')
        .reduce((sum, t) => sum + t.amount, 0);

      // Calcular transações do mês anterior
      const previousMonth = currentMonth === 0 ? 11 : currentMonth - 1;
      const previousYear = currentMonth === 0 ? currentYear - 1 : currentYear;
      
      const previousMonthTransactions = fetchedTransactions.filter(t => {
        const transactionDate = new Date(t.created_at);
        return transactionDate.getMonth() === previousMonth && 
               transactionDate.getFullYear() === previousYear;
      });

      const previousMonthBalance = previousMonthTransactions.reduce((sum, t) => 
        t.type === 'income' ? sum + t.amount : sum - t.amount, 0);

      // Calcular variação percentual
      let percentageChange = 0;
      if (previousMonthBalance !== 0) {
        percentageChange = ((currentBalance - previousMonthBalance) / Math.abs(previousMonthBalance)) * 100;
      } else if (currentBalance > 0) {
        percentageChange = 100; // Se não havia saldo no mês anterior mas há agora
      }

      setRecentTransactions(fetchedTransactions);
      setBalanceData({
        currentBalance,
        monthlyIncome,
        monthlyExpenses,
        previousMonthBalance,
        percentageChange,
      });
    } catch (err) {
      console.error('Error fetching transactions:', err);
      setError('Failed to load transactions.');
      setRecentTransactions([]);
      setBalanceData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const refresh = () => {
    fetchTransactions();
  };

  return { balanceData, recentTransactions, loading, error, refresh };
};
```

### **Passo 2: Verificar `BalanceCard.tsx`**

O componente `BalanceCard` já está implementado corretamente para usar o `balanceData` do hook, mas vamos verificar se está tratando corretamente os casos de erro:

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

  if (!balanceData) {
    return (
      <Card>
        <CardContent>
          <Typography color="error">Não foi possível carregar os dados de saldo.</Typography>
        </CardContent>
      </Card>
    );
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

## ✅ **Critérios de Aceitação**

- [ ] O hook `useTransactions` retorna corretamente a propriedade `balanceData`
- [ ] Todos os cálculos financeiros estão implementados (saldo atual, receitas mensais, despesas mensais)
- [ ] A comparação com o mês anterior é calculada corretamente
- [ ] A variação percentual é calculada corretamente
- [ ] O componente `BalanceCard` exibe todos os dados corretamente
- [ ] O componente trata adequadamente os estados de carregamento e erro
- [ ] A funcionalidade de refresh funciona corretamente

## 🧪 **Testes**

1. **Teste de Dados Válidos**
   - Verificar que o saldo atual é calculado corretamente
   - Verificar que as receitas mensais são calculadas corretamente
   - Verificar que as despesas mensais são calculadas corretamente
   - Verificar que a comparação com o mês anterior funciona

2. **Teste de Estados**
   - Verificar o estado de carregamento
   - Verificar o estado de erro
   - Verificar o estado com dados vazios

3. **Teste de Refresh**
   - Verificar que o botão de refresh atualiza os dados corretamente

## 📅 **Cronograma**

- **Estimativa de tempo**: 2-3 horas
- **Data de início**: Imediato
- **Data de conclusão**: Prevista para hoje

## 🔧 **Dependências**

- Nenhuma dependência externa necessária
- O hook `useTransactions` já existe e será atualizado
- O componente `BalanceCard` já existe e será verificado

## ⚠️ **Riscos**

1. **Dados inconsistentes**: Se os dados da API não estiverem formatados corretamente, os cálculos podem falhar
   - **Mitigação**: Adicionar validação de dados no hook

2. **Performance**: Calcular dados de vários meses pode impactar a performance
   - **Mitigação**: Otimizar os filtros e cálculos

3. **Edge cases**: Meses com valores zero ou negativos podem causar problemas nos cálculos percentuais
   - **Mitigação**: Adicionar tratamento específico para esses casos

---

**📅 Última Atualização**: 26 de agosto de 2025
**📍 Versão**: 1.0
**👤 Responsável**: Desenvolvedor Full-stack