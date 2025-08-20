import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const TransactionFormPage: React.FC = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Nova Transação
        </Typography>
        <Typography variant="body1">
          Formulário para adicionar nova transação será implementado aqui.
        </Typography>
      </Box>
    </Container>
  );
};

export default TransactionFormPage;