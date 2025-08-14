import React, { useState, useEffect } from 'react';
import {
  Typography,
  Container,
  Paper,
  Box,
  TextField,
  Button,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  Divider,
  useMediaQuery
} from '@mui/material';
import { useTheme } from '@mui/material/styles';
import axios from 'axios';
import { API_BASE_URL } from '../config';

interface Transaction {
  id: string;
  type: 'income' | 'expense';
  amount: number;
  description: string;
  created_at: string;
}

interface User {
  id: string;
  email: string;
  full_name: string;
}

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [form, setForm] = useState<Omit<Transaction, 'id' | 'created_at'>>({ 
    type: 'income', 
    amount: 0, 
    description: '' 
  });
  const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
  });

  // Interceptor para adicionar token em todas as requisições
  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const response = await api.get('/transactions/');
        const data = Array.isArray(response.data) ? response.data : [];
        setTransactions(data as Transaction[]);
      } catch (error) {
        console.error('Erro ao carregar transações:', error);
        setTransactions([]);
      }
    };

    loadTransactions();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.description || !form.amount) return;
    
    try {
      const res = await api.post('/transactions/', { 
        ...form, 
        amount: Number(form.amount) 
      });
      setTransactions([...transactions, res.data]);
      setForm({ ...form, amount: 0, description: '' });
    } catch (error) {
      console.error('Erro ao criar transação:', error);
    }
  };

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/auth/login';
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const totalIncome = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0);

  const totalExpense = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0);

  const balance = totalIncome - totalExpense;

  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {/* Resumo Financeiro */}
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 2, mb: 4 }}>
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', bgcolor: 'success.light', color: 'white' }}>
            <Typography variant="h6">Receitas</Typography>
            <Typography variant="h4">{formatCurrency(totalIncome)}</Typography>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', bgcolor: 'error.light', color: 'white' }}>
            <Typography variant="h6">Despesas</Typography>
            <Typography variant="h4">{formatCurrency(totalExpense)}</Typography>
          </Paper>
          
          <Paper elevation={2} sx={{ p: 3, textAlign: 'center', bgcolor: balance >= 0 ? 'primary.light' : 'error.main', color: 'white' }}>
            <Typography variant="h6">Saldo</Typography>
            <Typography variant="h4">{formatCurrency(balance)}</Typography>
          </Paper>
        </Box>

        {/* Nova Transação */}
        <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            📝 Nova Transação
          </Typography>
          <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection={isMobile ? 'column' : 'row'} gap={2}>
            <TextField
              select
              label="Tipo"
              name="type"
              value={form.type}
              onChange={handleChange}
              sx={{ minWidth: 120 }}
            >
              <MenuItem value="income">💰 Receita</MenuItem>
              <MenuItem value="expense">💸 Despesa</MenuItem>
            </TextField>
            
            <TextField
              label="Valor"
              name="amount"
              type="number"
              value={form.amount}
              onChange={handleChange}
              inputProps={{ min: 0, step: 0.01 }}
              sx={{ minWidth: 120 }}
            />
            
            <TextField
              label="Descrição"
              name="description"
              value={form.description}
              onChange={handleChange}
              sx={{ flex: 1 }}
            />
            
            <Button type="submit" variant="contained" color="primary">
              Adicionar
            </Button>
          </Box>
        </Paper>

        {/* Lista de Transações */}
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            📊 Transações Recentes
          </Typography>
          
          {transactions.length === 0 ? (
            <Typography color="text.secondary" align="center" sx={{ mt: 4, mb: 4 }}>
              Nenhuma transação cadastrada ainda.
            </Typography>
          ) : (
            <List>
              {transactions.slice().reverse().map((transaction, i) => (
                <React.Fragment key={transaction.id}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Typography variant="body1">
                            {transaction.type === 'income' ? '💰' : '💸'} {transaction.description}
                          </Typography>
                          <Typography 
                            variant="body1" 
                            sx={{ 
                              fontWeight: 'bold',
                              color: transaction.type === 'income' ? 'success.main' : 'error.main'
                            }}
                          >
                            {transaction.type === 'income' ? '+' : '-'} {formatCurrency(transaction.amount)}
                          </Typography>
                        </Box>
                      }
                      secondary={formatDate(transaction.created_at)}
                    />
                  </ListItem>
                  {i < transactions.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </Paper>
      </Container>
    </>
  );
};

export default Dashboard;  