// src/components/dashboard/DashboardLayout.tsx
import React from 'react';
import { Grid, useTheme, useMediaQuery, Box } from '@mui/material';

export const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  return (
    <Grid container spacing={isMobile ? 2 : 3}>
      {React.Children.map(children, (child, index) => (
        <Grid 
          item 
          key={index}
          xs={12} 
          md={6} 
          lg={4} 
          sx={{ 
            transition: 'all 0.3s ease-in-out',
            animation: `fadeIn ${300 + index * 100}ms ease-out forwards`,
            opacity: 0,
            '@keyframes fadeIn': {
              '0%': {
                opacity: 0,
                transform: 'translateY(20px)'
              },
              '100%': {
                opacity: 1,
                transform: 'translateY(0)'
              }
            }
          }}
        >
          <Box 
            sx={{ 
              height: '100%',
              transition: 'transform 0.2s ease-in-out',
              '&:hover': {
                transform: 'translateY(-4px)'
              }
            }}
          >
            {child}
              </Box>
            </Grid>
          </CSSTransition>
        ))}
      </TransitionGroup>
    </Grid>
  );
};