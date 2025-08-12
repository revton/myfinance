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
  useTheme,
  Link as MuiLink
} from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const Login: React.FC = () => {
  const theme = useTheme();
  
  const [formData, setFormData] = useState({
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
    
    if (!formData.email || !formData.password) {
      setMessage({
        type: 'error',
        text: 'Por favor, preencha todos os campos.'
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        email: formData.email,
        password: formData.password
      });

      // Salvar token no localStorage
      const { access_token, user } = response.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(user));

      setMessage({
        type: 'success',
        text: 'Login realizado com sucesso! Redirecionando...'
      });

      // Redirecionar para dashboard após 2 segundos
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 2000);

    } catch (error: any) {
      console.error('Erro no login:', error);
      
      let errorMessage = 'Erro ao fazer login. Verifique suas credenciais.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.status === 401) {
        errorMessage = 'Email ou senha incorretos.';
      } else if (error.response?.status === 422) {
        errorMessage = 'Dados inválidos. Verifique o formato do email.';
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
            🔐 Login
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Entre com suas credenciais para acessar sua conta
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
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
            placeholder="seu@email.com"
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
            placeholder="Sua senha"
          />

          <Box sx={{ mt: 2, textAlign: 'right' }}>
            <MuiLink
              component={Link}
              to="/auth/forgot-password"
              variant="body2"
              sx={{ cursor: 'pointer' }}
            >
              Esqueceu sua senha?
            </MuiLink>
          </Box>

          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              component={Link}
              to="/auth/register"
              variant="outlined"
              disabled={loading}
            >
              Criar Conta
            </Button>
            
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !formData.email || !formData.password}
              sx={{ minWidth: 120 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Entrar'
              )}
            </Button>
          </Box>
        </Box>

        <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <strong>💡 Dica:</strong> Use as credenciais da sua conta MyFinance
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login; 