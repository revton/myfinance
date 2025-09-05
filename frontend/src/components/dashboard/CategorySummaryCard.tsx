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
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { useCategories } from '../../hooks/useCategories';
import { CategoryIcon } from '../categories/CategoryIcon';
import { useNavigate } from 'react-router-dom';
import AdvancedLoadingState from '../common/AdvancedLoadingState';
import AnimatedList from '../common/AnimatedList';

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
  const { categorySummary, loading, refresh } = useCategories();
  const navigate = useNavigate();

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };
  
  // Card header content that's common across all states
  const cardHeader = (
    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
      <Typography variant="h6" color="text.secondary">
        Gastos por Categoria
      </Typography>
      <Button size="small" onClick={() => navigate('/categories')}>
        Ver Todas
      </Button>
    </Box>
  );
  
  const chartData = categorySummary.map((cat, index) => ({
    name: cat.name,
    value: cat.amount,
    color: COLORS[index % COLORS.length]
  }));
  
  // Content to show when data is loaded
  const contentWithData = (
    <>
      <Box height={200} mb={2}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              nameKey="name"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
              labelLine={false}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => formatCurrency(Number(value))} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </Box>
      
      <AnimatedList>
        {categorySummary.map((category) => (
          <ListItem key={category.id} divider>
            <ListItemIcon>
              <CategoryIcon icon={category.icon} color={category.color} />
            </ListItemIcon>
            <ListItemText primary={category.name} />
            <Box display="flex" alignItems="center" gap={1}>
              <Typography variant="body2" color="text.secondary">
                {category.percentage.toFixed(1)}%
              </Typography>
              <Typography variant="body2" fontWeight="bold">
                {formatCurrency(category.amount)}
              </Typography>
            </Box>
          </ListItem>
        ))}
      </AnimatedList>
    </>
  );
  
  // Use AdvancedLoadingState to handle loading, error, and content states
  return (
    <Card elevation={2}>
      <CardContent>
        {cardHeader}
        <AdvancedLoadingState 
          isLoading={loading} 
          loadingText="Carregando dados de categorias..." 
          showSkeleton={true}
          height={200}
          onRetry={refresh}
        >
          {categorySummary.length === 0 ? (
            <Typography color="text.secondary">
              Nenhum gasto registrado ainda.
            </Typography>
          ) : contentWithData}
        </AdvancedLoadingState>
      </CardContent>
    </Card>
  );
};