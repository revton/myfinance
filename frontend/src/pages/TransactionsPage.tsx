// src/pages/TransactionsPage.tsx
import React from 'react';
import { Container, Typography } from '@mui/material';
import FilteredTransactionsList from '../components/transactions/FilteredTransactionsList';

const TransactionsPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Typography variant="h4" gutterBottom>
        Transações
      </Typography>
      <FilteredTransactionsList />
    </Container>
  );
};

export default TransactionsPage;