// src/pages/DashboardPage.tsx
import React from 'react';
import { Container, Paper } from '@mui/material';
import { BalanceCard } from '../components/dashboard/BalanceCard';
import { RecentTransactionsCard } from '../components/dashboard/RecentTransactionsCard';
import { CategorySummaryCard } from '../components/dashboard/CategorySummaryCard';
import { QuickActionsCard } from '../components/dashboard/QuickActionsCard';
import SentryTest from '../components/SentryTest';
import { DashboardLayout } from '../components/dashboard/DashboardLayout';

export const DashboardPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <DashboardLayout>
        <BalanceCard />
        <QuickActionsCard />
        <CategorySummaryCard />
        <RecentTransactionsCard />
        <Paper sx={{ p: 2 }}>
          <SentryTest />
        </Paper>
      </DashboardLayout>
    </Container>
  );
};