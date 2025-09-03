// src/components/dashboard/QuickActionsCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Stack,
  Tooltip,
  Box,
  useTheme
} from '@mui/material';
import { 
  Add, 
  Category,
  Assessment,
  Settings,
  Speed
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export const QuickActionsCard: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  
  const actions = [
    {
      label: 'Nova Transação',
      icon: <Add />,
      color: 'primary' as const,
      onClick: () => navigate('/transactions/new')
    },
    {
      label: 'Categorias',
      icon: <Category />,
      color: 'success' as const,
      onClick: () => navigate('/categories')
    }
  ];
  
  // Card header that's consistent with other cards
  const cardHeader = (
    <Box sx={{ bgcolor: theme.palette.primary.main, py: 1, px: 2 }}>
      <Box display="flex" alignItems="center">
        <Speed sx={{ mr: 1, color: 'white' }} />
        <Typography variant="h6" sx={{ color: 'white' }}>
          Ações Rápidas
        </Typography>
      </Box>
    </Box>
  );

  return (
    <Card elevation={3} sx={{ borderRadius: 2, overflow: 'hidden' }}>
      {cardHeader}
      
      <CardContent>
        <Stack spacing={1}>
          {actions.map((action, index) => (
            <Tooltip 
              key={index}
              title={`Ir para ${action.label}`}
              placement="right"
            >
              <Button
                variant="outlined"
                color={action.color}
                startIcon={action.icon}
                onClick={action.onClick}
                fullWidth
                sx={{ 
                  justifyContent: 'flex-start',
                  borderRadius: 2,
                  py: 1.5,
                  transition: 'all 0.3s ease',
                  animation: `fadeIn ${300 + index * 100}ms ease-out forwards`,
                  '@keyframes fadeIn': {
                    '0%': {
                      opacity: 0,
                      transform: 'translateY(10px)'
                    },
                    '100%': {
                      opacity: 1,
                      transform: 'translateY(0)'
                    }
                  },
                  '&:hover': {
                    transform: 'translateY(-3px)',
                    boxShadow: 3,
                    backgroundColor: `${action.color}.50`
                  },
                  '&:active': {
                    transform: 'translateY(0)',
                    transition: 'all 0.1s'
                  }
                }}
              >
                {action.label}
              </Button>
            </Tooltip>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};