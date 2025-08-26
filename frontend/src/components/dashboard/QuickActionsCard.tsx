// src/components/dashboard/QuickActionsCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Stack 
} from '@mui/material';
import { 
  Add, 
  Category 
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

export const QuickActionsCard: React.FC = () => {
  const navigate = useNavigate();
  
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
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" color="text.secondary" mb={2}>
          Ações Rápidas
        </Typography>
        
        <Stack spacing={1}>
          {actions.map((action, index) => (
            <Button
              key={index}
              variant="outlined"
              color={action.color}
              startIcon={action.icon}
              onClick={action.onClick}
              fullWidth
              sx={{ justifyContent: 'flex-start' }}
            >
              {action.label}
            </Button>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};