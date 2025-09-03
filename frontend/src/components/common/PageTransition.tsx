import React from 'react';
import { useLocation } from 'react-router-dom';
import { Box } from '@mui/material';
import '../../styles/transitions.css';

interface PageTransitionProps {
  children: React.ReactNode;
}

const PageTransition: React.FC<PageTransitionProps> = ({ children }) => {
  const location = useLocation();

  return (
    <Box
      key={location.key}
      className="page"
      sx={{
        animation: 'fadeIn 300ms ease-out forwards',
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
      {children}
    </Box>
  );
};

export default PageTransition;