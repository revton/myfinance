import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  RadioGroup,
  FormControlLabel,
  Radio,
  Alert,
  CircularProgress,
  Paper
} from '@mui/material';
import { useCategories } from '../contexts/CategoryContext';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';
import { API_BASE_URL, APP_CONFIG } from '../config'; // Import APP_CONFIG

interface TransactionFormData {
  type: 'income' | 'expense';
  amount: string | number;
  description: string;
  category_id: string | '';
}

const TransactionFormPage: React.FC = () => {
  const navigate = useNavigate();
  const { categories, loading: categoriesLoading, error: categoriesError } = useCategories();
  const [formData, setFormData] = useState<TransactionFormData>({
    type: 'expense', // Default to expense
    amount: '',
    description: '',
    category_id: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [success, setSuccess] = useState<string | null>(null);

  const expenseCategories = categories.filter(cat => cat.type === 'expense' && cat.is_active);
  const incomeCategories = categories.filter(cat => cat.type === 'income' && cat.is_active);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | { name?: string; value: unknown }>)=>{
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name as string]: value,
    }));
  };

  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value;
    // Allow only numbers, commas, and a single decimal point/comma
    if (/^[\d,.]*$/.test(value) || value === '') {
      setFormData(prev => ({
        ...prev,
        amount: value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSuccess(null);
    setLoading(true);

    // Basic validation
    if (!formData.type || !formData.amount || !formData.description) {
      setFormError('Por favor, preencha todos os campos obrigatórios.');
      setLoading(false);
      return;
    }

    // Parse amount, replacing comma with dot if present
    const amountString = formData.amount.toString().replace(',', '.');
    const amount = parseFloat(amountString);

    // Validate amount is a positive number
    if (isNaN(amount) || amount <= 0) {
      setFormError('Por favor, insira um valor monetário válido.');
      setLoading(false);
      return;
    }

    try {
      await api.post(`${APP_CONFIG.api.endpoints.transactions}`, {
        type: formData.type,
        amount: amount,
        description: formData.description,
        category_id: formData.category_id || null, // Send null if no category selected
      });
      setSuccess('Transação adicionada com sucesso!');
      setFormData({ // Reset form
        type: 'expense',
        amount: '',
        description: '',
        category_id: '',
      });
      // Optionally redirect after a short delay
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err: any) {
      console.error('Error adding transaction:', err);
      setFormError(err.response?.data?.detail || 'Erro ao adicionar transação.');
    } finally {
      setLoading(false);
    }
  };

  if (categoriesLoading) {
    return (
      <Container maxWidth="md">
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (categoriesError) {
    return (
      <Container maxWidth="md">
        <Alert severity="error">Erro ao carregar categorias: {categoriesError}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Nova Transação
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
          <form onSubmit={handleSubmit}>
            <FormControl component="fieldset" margin="normal" fullWidth>
              <Typography variant="subtitle1" gutterBottom>Tipo de Transação</Typography>
              <RadioGroup
                row
                name="type"
                value={formData.type}
                onChange={handleChange}
              >
                <FormControlLabel value="expense" control={<Radio />} label="Despesa" />
                <FormControlLabel value="income" control={<Radio />} label="Receita" />
              </RadioGroup>
            </FormControl>

            <TextField
              label="Valor"
              name="amount"
              type="text" // Use text to control input format
              value={formData.amount}
              onChange={handleAmountChange}
              fullWidth
              margin="normal"
              required
              inputProps={{ inputMode: 'decimal' }}
              placeholder="0,00"
            />

            <TextField
              label="Descrição"
              name="description"
              value={formData.description}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              multiline
              rows={3}
            />

            <FormControl fullWidth margin="normal">
              <InputLabel id="category-label">Categoria</InputLabel>
              <Select
                labelId="category-label"
                id="category-select"
                name="category_id"
                value={formData.category_id}
                label="Categoria"
                onChange={handleChange}
              >
                <MenuItem value="">
                  <em>Nenhuma</em>
                </MenuItem>
                {(formData.type === 'expense' ? expenseCategories : incomeCategories).map(category => (
                  <MenuItem key={category.id} value={category.id}>
                    {category.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {formError && <Alert severity="error" sx={{ mt: 2 }}>{formError}</Alert>}
            {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}

            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Adicionar Transação'}
              </Button>
              <Button
                variant="outlined"
                color="secondary"
                onClick={() => navigate('/dashboard')}
                disabled={loading}
              >
                Cancelar
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default TransactionFormPage;