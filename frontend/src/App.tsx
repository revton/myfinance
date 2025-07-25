import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
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
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    background: { default: '#f4f6fa' },
  },
});

interface Transaction {
  type: 'income' | 'expense';
  amount: number;
  description: string;
}

function App() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [form, setForm] = useState<Transaction>({ type: 'income', amount: 0, description: '' });
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    axios.get('/transactions/').then(res => {
      const data = Array.isArray(res.data) ? res.data : [];
      setTransactions(data as Transaction[]);
    }).catch(() => setTransactions([]));
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.description || !form.amount) return;
    const res = await axios.post('/transactions/', { ...form, amount: Number(form.amount) });
    setTransactions([...transactions, res.data]);
    setForm({ ...form, amount: 0, description: '' });
  };

  return (
    <ThemeProvider theme={theme}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            MyFinance
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Nova Transação
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
              <MenuItem value="income">Receita</MenuItem>
              <MenuItem value="expense">Despesa</MenuItem>
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
        <Paper elevation={3} sx={{ p: 2, mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Transações
          </Typography>
          <List>
            {transactions.map((t, i) => (
              <React.Fragment key={i}>
                <ListItem>
                  <ListItemText
                    primary={`${t.type === 'income' ? 'Receita' : 'Despesa'}: R$ ${t.amount.toFixed(2)}`}
                    secondary={t.description}
                  />
                </ListItem>
                {i < transactions.length - 1 && <Divider />}
              </React.Fragment>
            ))}
            {transactions.length === 0 && (
              <Typography color="text.secondary" align="center" sx={{ mt: 2 }}>
                Nenhuma transação cadastrada.
              </Typography>
            )}
          </List>
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App;
