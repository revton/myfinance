// src/components/dashboard/QuickActionsCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Stack,
  Tooltip,
  Box
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
        <Box display="flex" alignItems="center" mb={2}>
          <Speed sx={{ mr: 1, color: 'text.secondary' }} />
          <Typography variant="h6" color="text.secondary">
            Ações Rápidas
          </Typography>
        </Box>
        
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
                   py: 1,
                   transition: 'all 0.2s',
                   '&:hover': {
                     transform: 'translateY(-2px)',
                     boxShadow: 2
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