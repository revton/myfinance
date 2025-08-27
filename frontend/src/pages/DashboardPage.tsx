// src/pages/DashboardPage.tsx
import React from 'react';
import { Grid, Container, Paper } from '@mui/material';
import { BalanceCard } from '../components/dashboard/BalanceCard';
import { RecentTransactionsCard } from '../components/dashboard/RecentTransactionsCard';
import { CategorySummaryCard } from '../components/dashboard/CategorySummaryCard';
import { QuickActionsCard } from '../components/dashboard/QuickActionsCard';
import SentryTest from '../components/SentryTest';

export const DashboardPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Grid container spacing={3}>
        {/* Cards principais */}
        <Grid item xs={12} md={8}>
          <BalanceCard />
        </Grid>
        <Grid item xs={12} md={4}>
          <QuickActionsCard />
        </Grid>
        
        {/* Resumos */}
        <Grid item xs={12} md={6}>
          <CategorySummaryCard />
        </Grid>
        <Grid item xs={12} md={6}>
          <RecentTransactionsCard />
        </Grid>
        
        {/* Componente de teste do Sentry */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <SentryTest />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};