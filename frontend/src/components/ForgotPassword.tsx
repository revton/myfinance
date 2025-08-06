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
import axios from 'axios';
import { API_BASE_URL } from '../config';

const ForgotPassword: React.FC = () => {
  const theme = useTheme();
  
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      setMessage({
        type: 'error',
        text: 'Por favor, digite seu email.'
      });
      return;
    }

    // Validação básica de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setMessage({
        type: 'error',
        text: 'Por favor, digite um email válido.'
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/auth/forgot-password`, {
        email: email
      });

      setMessage({
        type: 'success',
        text: 'Email de recuperação enviado com sucesso! Verifique sua caixa de entrada.'
      });

      // Limpar email após sucesso
      setEmail('');

    } catch (error: any) {
      console.error('Erro ao solicitar recuperação:', error);
      
      let errorMessage = 'Erro ao enviar email de recuperação. Tente novamente.';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.status === 422) {
        errorMessage = 'Email inválido. Verifique o formato.';
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
            🔑 Recuperar Senha
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Digite seu email para receber um link de recuperação de senha
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
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
            required
            disabled={loading}
            placeholder="seu@email.com"
          />

          <Box sx={{ mt: 3, display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              type="button"
              variant="outlined"
              onClick={() => window.location.href = '/auth/login'}
              disabled={loading}
            >
              Voltar ao Login
            </Button>
            
            <Button
              type="submit"
              variant="contained"
              disabled={loading || !email}
              sx={{ minWidth: 120 }}
            >
              {loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Enviar Email'
              )}
            </Button>
          </Box>
        </Box>

        <Box sx={{ mt: 4, p: 3, bgcolor: 'grey.50', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <strong>💡 Dicas:</strong>
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            • Verifique sua caixa de spam se não receber o email
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • O link de recuperação é válido por 24 horas
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • Se não tiver uma conta, você pode se registrar
          </Typography>
        </Box>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Não tem uma conta?{' '}
            <Button
              variant="text"
              size="small"
              onClick={() => window.location.href = '/auth/register'}
            >
              Criar Conta
            </Button>
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default ForgotPassword; 