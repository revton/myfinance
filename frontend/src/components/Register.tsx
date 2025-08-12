import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  useTheme
} from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const Register: React.FC = () => {
  const theme = useTheme();
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.full_name || !formData.email || !formData.password) {
      setMessage({
        type: 'error',
        text: 'Por favor, preencha todos os campos.'
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      await axios.post(`${API_BASE_URL}/auth/register`, formData);

      setMessage({
        type: 'success',
        text: 'Cadastro realizado com sucesso! Você será redirecionado para o login.'
      });

      setTimeout(() => {
        window.location.href = '/auth/login';
      }, 3000);

    } catch (error: any) {
      console.error('Erro no cadastro:', error);
      
      let errorMessage = 'Erro ao realizar cadastro. Tente novamente.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      }
      
      setMessage({
        type: 'error',
        text: errorMessage
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ color: theme.palette.primary.main }}>
            📝 Criar Conta
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Crie sua conta para começar a usar o MyFinance
          </Typography>
        </Box>

        {message && (
          <Alert severity={message.type} sx={{ mb: 3 }}>
            {message.text}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Nome Completo"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
          />
          <TextField
            fullWidth
            label="Senha"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
          />

          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              component={Link}
              to="/auth/login"
              variant="outlined"
              disabled={loading}
            >
              Voltar para Login
            </Button>
            
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !formData.email || !formData.password || !formData.full_name}
              sx={{ minWidth: 120 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Criar Conta'
              )}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;
