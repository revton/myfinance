// src/components/dashboard/DashboardLayout.tsx
import React from 'react';
import { Grid, useTheme, useMediaQuery } from '@mui/material';

export const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  return (
    <Grid container spacing={isMobile ? 2 : 3}>
      {React.Children.map(children, (child) => (
        <Grid item xs={12} md={6} lg={4}>
          {child}
        </Grid>
      ))}
    </Grid>
  );
};