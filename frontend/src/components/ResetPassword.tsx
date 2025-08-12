import React, { useState, useEffect } from 'react';
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
import { useSearchParams, Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const theme = useTheme();
  
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  
  const token = searchParams.get('token');
  const email = searchParams.get('email');

  useEffect(() => {
    // Validar se token e email estão presentes
    if (!token || !email) {
      setMessage({
        type: 'error',
        text: 'Link inválido. Token ou email não encontrados.'
      });
    }
  }, [token, email]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validatePassword = (password: string): string[] => {
    const errors: string[] = [];
    
    if (password.length < 8) {
      errors.push('A senha deve ter pelo menos 8 caracteres');
    }
    
    if (!/(?=.*[a-z])/.test(password)) {
      errors.push('A senha deve conter pelo menos uma letra minúscula');
    }
    
    if (!/(?=.*[A-Z])/.test(password)) {
      errors.push('A senha deve conter pelo menos uma letra maiúscula');
    }
    
    if (!/(?=.*\d)/.test(password)) {
      errors.push('A senha deve conter pelo menos um número');
    }
    
    if (!/(?=.*[@$!%*?&])/.test(password)) {
      errors.push('A senha deve conter pelo menos um caractere especial (@$!%*?&)');
    }
    
    return errors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token || !email) {
      setMessage({
        type: 'error',
        text: 'Dados inválidos para reset de senha.'
      });
      return;
    }

    // Validar senhas
    if (formData.password !== formData.confirmPassword) {
      setMessage({
        type: 'error',
        text: 'As senhas não coincidem.'
      });
      return;
    }

    const passwordErrors = validatePassword(formData.password);
    if (passwordErrors.length > 0) {
      setMessage({
        type: 'error',
        text: `Senha inválida: ${passwordErrors.join(', ')}`
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/reset-password`, {
        token: token,
        email: email,
        new_password: formData.password
      });

      setMessage({
        type: 'success',
        text: 'Senha redefinida com sucesso! Você será redirecionado para o login.'
      });

      // Redirecionar para login após 3 segundos
      setTimeout(() => {
        window.location.href = '/auth/login';
      }, 3000);

    } catch (error: any) {
      console.error('Erro ao resetar senha:', error);
      
      let errorMessage = 'Erro ao redefinir senha. Tente novamente.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.status === 422) {
        errorMessage = 'Dados inválidos. Verifique as informações fornecidas.';
      } else if (error.response?.status === 400) {
        errorMessage = 'Token inválido ou expirado. Solicite um novo link de recuperação.';
      }
      
      setMessage({
        type: 'error',
        text: errorMessage
      });
    } finally {
      setLoading(false);
    }
  };

  if (!token || !email) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" color="error" gutterBottom>
            Link Inválido
          </Typography>
          <Typography variant="body1" color="text.secondary">
            O link de recuperação de senha é inválido ou expirou.
          </Typography>
          <Button
            variant="contained"
            sx={{ mt: 3 }}
            onClick={() => window.location.href = '/auth/forgot-password'}
          >
            Solicitar Novo Link
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h4" gutterBottom sx={{ color: theme.palette.primary.main }}>
            🔐 Redefinir Senha
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Digite sua nova senha para a conta <strong>{email}</strong>
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
            label="Nova Senha"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            required
            disabled={loading}
            helperText="Mínimo 8 caracteres, com letras, números e símbolos"
          />
          
          <TextField
            fullWidth
            label="Confirmar Nova Senha"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
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
              Cancelar
            </Button>
            
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !formData.password || !formData.confirmPassword}
              sx={{ minWidth: 120 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Redefinir Senha'
              )}
            </Button>
          </Box>
        </Box>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Lembrou sua senha?{' '}
            <Button
              component={Link}
              to="/auth/login"
              variant="text"
              size="small"
            >
              Fazer Login
            </Button>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default ResetPassword; 