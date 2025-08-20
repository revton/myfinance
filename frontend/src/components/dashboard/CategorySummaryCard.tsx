// src/components/dashboard/CategorySummaryCard.tsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  ListItemIcon,
  Box,
  Button 
} from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { useCategories } from '../../hooks/useCategories';
import { CategoryIcon } from '../categories/CategoryIcon';
import { useNavigate } from 'react-router-dom';

interface CategorySummary {
  id: string;
  name: string;
  icon: string;
  color: string;
  amount: number;
  percentage: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export const CategorySummaryCard: React.FC = () => {
  const { categorySummary, loading } = useCategories();
  const navigate = useNavigate();

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };
  
  if (loading) {
    return <Card><CardContent><Typography>Carregando...</Typography></CardContent></Card>;
  }
  
  const chartData = categorySummary.map((cat, index) => ({
    name: cat.name,
    value: cat.amount,
    color: COLORS[index % COLORS.length]
  }));
  
  return (
    <Card elevation={2}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" color="text.secondary">
            Gastos por Categoria
          </Typography>
          <Button size="small" onClick={() => navigate('/categories')}>
            Ver Todas
          </Button>
        </Box>
        
        <Box display="flex" gap={2}>
          {/* Gráfico */}
          <Box flex={1} height={200}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </Box>
          
          {/* Lista */}
          <Box flex={1}>
            <List dense>
              {categorySummary.slice(0, 5).map((category) => (
                <ListItem key={category.id}>
                  <ListItemIcon>
                    <CategoryIcon 
                      icon={category.icon} 
                      color={category.color} 
                      size="small" 
                    />
                  </ListItemIcon>
                  <ListItemText
                    primary={category.name}
                    secondary={`${category.percentage.toFixed(1)}% - ${formatCurrency(category.amount)}`}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};