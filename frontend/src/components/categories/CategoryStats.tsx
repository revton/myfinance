import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  LinearProgress
} from '@mui/material';
import { Category } from '../../types/category';

interface CategoryStatsProps {
  categories: Category[];
}

const CategoryStats: React.FC<CategoryStatsProps> = ({ categories }) => {
  const expenseCategories = categories.filter(c => c.type === 'expense' && c.is_active);
  const incomeCategories = categories.filter(c => c.type === 'income' && c.is_active);

  const totalExpenseCategories = expenseCategories.length;
  const totalIncomeCategories = incomeCategories.length;
  const totalCategories = totalExpenseCategories + totalIncomeCategories;

  const defaultExpenseCategories = expenseCategories.filter(c => c.is_default).length;
  const defaultIncomeCategories = incomeCategories.filter(c => c.is_default).length;
  const customExpenseCategories = totalExpenseCategories - defaultExpenseCategories;
  const customIncomeCategories = totalIncomeCategories - defaultIncomeCategories;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Estatísticas das Categorias
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Categorias de Despesa
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total: {totalExpenseCategories} categorias
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Padrão: {defaultExpenseCategories} | Personalizadas: {customExpenseCategories}
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={(totalExpenseCategories / Math.max(totalCategories, 1)) * 100}
                sx={{ height: 8, borderRadius: 4 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Categorias de Receita
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Total: {totalIncomeCategories} categorias
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Padrão: {defaultIncomeCategories} | Personalizadas: {customIncomeCategories}
                </Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={(totalIncomeCategories / Math.max(totalCategories, 1)) * 100}
                sx={{ height: 8, borderRadius: 4 }}
                color="success"
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resumo Geral
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} sm={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="primary">
                      {totalCategories}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total de Categorias
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="error">
                      {totalExpenseCategories}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Despesas
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="success">
                      {totalIncomeCategories}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Receitas
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Box textAlign="center">
                    <Typography variant="h4" color="info">
                      {customExpenseCategories + customIncomeCategories}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Personalizadas
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CategoryStats;
