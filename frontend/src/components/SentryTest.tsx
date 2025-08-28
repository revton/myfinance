import { useState } from 'react';
import { Button, Box, Typography, Alert } from '@mui/material';
import * as Sentry from '@sentry/react';

/**
 * Componente para testar a integração com o Sentry no frontend
 */
const SentryTest = () => {
  const [errorTriggered, setErrorTriggered] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleTestError = () => {
    try {
      // Gera um erro de teste
      console.log('Gerando erro de teste para o Sentry');
      throw new Error('Erro de teste do Frontend para o Sentry!');
    } catch (error) {
      // Captura o erro com o Sentry
      if (error instanceof Error) {
        Sentry.captureException(error);
        setErrorMessage(error.message);
      } else {
        setErrorMessage('Erro desconhecido');
      }
      setErrorTriggered(true);
    }
  };

  return (
    <Box sx={{ mt: 2, p: 2, border: '1px dashed #ccc', borderRadius: 2 }}>
      <Typography variant="h6" gutterBottom>
        Teste de Integração com Sentry
      </Typography>
      
      <Button 
        variant="contained" 
        color="warning" 
        onClick={handleTestError}
        sx={{ mb: 2 }}
      >
        Gerar Erro de Teste
      </Button>
      
      {errorTriggered && (
        <Alert severity="success" sx={{ mt: 2 }}>
          Erro gerado com sucesso: "{errorMessage}". Verifique o painel do Sentry.
        </Alert>
      )}
    </Box>
  );
};

export default SentryTest;