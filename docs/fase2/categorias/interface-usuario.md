# 🎨 Interface do Usuário - Sistema de Categorias

## 🎯 **Visão Geral**

Este documento descreve os componentes de interface do usuário para o sistema de categorias, incluindo páginas de gerenciamento, componentes reutilizáveis e integração com transações.

## 📱 **Páginas Principais**

### **1. Página de Gerenciamento de Categorias**

```tsx
// src/pages/CategoriesPage.tsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  IconButton,
  Button,
  Chip,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  RestoreFromTrash as RestoreIcon
} from '@mui/icons-material';
import { useCategories } from '../contexts/CategoryContext';
import CategoryForm from '../components/categories/CategoryForm';
import CategoryCard from '../components/categories/CategoryCard';
import CategoryStats from '../components/categories/CategoryStats';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`category-tabpanel-${index}`}
      aria-labelledby={`category-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const CategoriesPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingCategory, setEditingCategory] = useState<any>(null);
  const [showDeleted, setShowDeleted] = useState(false);
  
  const { 
    categories, 
    loading, 
    error, 
    createCategory, 
    updateCategory, 
    deleteCategory, 
    restoreCategory 
  } = useCategories();

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleOpenDialog = (category?: any) => {
    setEditingCategory(category || null);
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingCategory(null);
  };

  const handleSubmit = async (categoryData: any) => {
    try {
      if (editingCategory) {
        await updateCategory(editingCategory.id, categoryData);
      } else {
        await createCategory(categoryData);
      }
      handleCloseDialog();
    } catch (error) {
      console.error('Erro ao salvar categoria:', error);
    }
  };

  const handleDelete = async (categoryId: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta categoria?')) {
      try {
        await deleteCategory(categoryId);
      } catch (error) {
        console.error('Erro ao excluir categoria:', error);
      }
    }
  };

  const handleRestore = async (categoryId: string) => {
    try {
      await restoreCategory(categoryId);
    } catch (error) {
      console.error('Erro ao restaurar categoria:', error);
    }
  };

  const expenseCategories = categories.filter(c => c.type === 'expense' && c.is_active);
  const incomeCategories = categories.filter(c => c.type === 'income' && c.is_active);
  const deletedCategories = categories.filter(c => !c.is_active);

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ marginTop: 4, marginBottom: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" gutterBottom>
            Gerenciar Categorias
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => handleOpenDialog()}
          >
            Nova Categoria
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Paper elevation={3}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="category tabs">
              <Tab label="Despesas" />
              <Tab label="Receitas" />
              <Tab label="Estatísticas" />
              <Tab label="Excluídas" />
            </Tabs>
          </Box>

          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              {expenseCategories.map((category) => (
                <Grid item xs={12} sm={6} md={4} key={category.id}>
                  <CategoryCard
                    category={category}
                    onEdit={() => handleOpenDialog(category)}
                    onDelete={() => handleDelete(category.id)}
                  />
                </Grid>
              ))}
              {expenseCategories.length === 0 && (
                <Grid item xs={12}>
                  <Box textAlign="center" py={4}>
                    <Typography variant="body1" color="text.secondary">
                      Nenhuma categoria de despesa encontrada.
                    </Typography>
                  </Box>
                </Grid>
              )}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={3}>
              {incomeCategories.map((category) => (
                <Grid item xs={12} sm={6} md={4} key={category.id}>
                  <CategoryCard
                    category={category}
                    onEdit={() => handleOpenDialog(category)}
                    onDelete={() => handleDelete(category.id)}
                  />
                </Grid>
              ))}
              {incomeCategories.length === 0 && (
                <Grid item xs={12}>
                  <Box textAlign="center" py={4}>
                    <Typography variant="body1" color="text.secondary">
                      Nenhuma categoria de receita encontrada.
                    </Typography>
                  </Box>
                </Grid>
              )}
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <CategoryStats categories={categories} />
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <Grid container spacing={3}>
              {deletedCategories.map((category) => (
                <Grid item xs={12} sm={6} md={4} key={category.id}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Box
                          sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '50%',
                            backgroundColor: category.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            mr: 2
                          }}
                        >
                          <Typography variant="h6" color="white">
                            {category.icon}
                          </Typography>
                        </Box>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="h6">{category.name}</Typography>
                          <Chip 
                            label={category.type === 'expense' ? 'Despesa' : 'Receita'} 
                            size="small" 
                            color={category.type === 'expense' ? 'error' : 'success'}
                          />
                        </Box>
                        <IconButton
                          onClick={() => handleRestore(category.id)}
                          color="primary"
                          title="Restaurar categoria"
                        >
                          <RestoreIcon />
                        </IconButton>
                      </Box>
                      {category.description && (
                        <Typography variant="body2" color="text.secondary">
                          {category.description}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
              {deletedCategories.length === 0 && (
                <Grid item xs={12}>
                  <Box textAlign="center" py={4}>
                    <Typography variant="body1" color="text.secondary">
                      Nenhuma categoria excluída.
                    </Typography>
                  </Box>
                </Grid>
              )}
            </Grid>
          </TabPanel>
        </Paper>
      </Box>

      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingCategory ? 'Editar Categoria' : 'Nova Categoria'}
        </DialogTitle>
        <DialogContent>
          <CategoryForm
            category={editingCategory}
            onSubmit={handleSubmit}
            onCancel={handleCloseDialog}
          />
        </DialogContent>
      </Dialog>
    </Container>
  );
};

export default CategoriesPage;
```

### **2. Componente CategoryCard**

```tsx
// src/components/categories/CategoryCard.tsx
import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  IconButton,
  Chip,
  Tooltip
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Lock as LockIcon
} from '@mui/icons-material';
import { Category } from '../../types/category';

interface CategoryCardProps {
  category: Category;
  onEdit: () => void;
  onDelete: () => void;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category, onEdit, onDelete }) => {
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: '50%',
              backgroundColor: category.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2
            }}
          >
            <Typography variant="h6" color="white">
              {category.icon}
            </Typography>
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" gutterBottom>
              {category.name}
            </Typography>
            <Chip 
              label={category.type === 'expense' ? 'Despesa' : 'Receita'} 
              size="small" 
              color={category.type === 'expense' ? 'error' : 'success'}
            />
            {category.is_default && (
              <Chip 
                label="Padrão" 
                size="small" 
                variant="outlined"
                sx={{ ml: 1 }}
              />
            )}
          </Box>
        </Box>
        
        {category.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {category.description}
          </Typography>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Criada em {new Date(category.created_at).toLocaleDateString('pt-BR')}
          </Typography>
          {category.is_default && (
            <Tooltip title="Categoria padrão - não pode ser excluída">
              <LockIcon color="action" fontSize="small" />
            </Tooltip>
          )}
        </Box>
      </CardContent>

      {!category.is_default && (
        <CardActions sx={{ justifyContent: 'flex-end' }}>
          <IconButton onClick={onEdit} color="primary" size="small">
            <EditIcon />
          </IconButton>
          <IconButton onClick={onDelete} color="error" size="small">
            <DeleteIcon />
          </IconButton>
        </CardActions>
      )}
    </Card>
  );
};

export default CategoryCard;
```

### **3. Componente CategoryForm**

```tsx
// src/components/categories/CategoryForm.tsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Grid,
  FormHelperText
} from '@mui/material';
import { Category, CategoryType } from '../../types/category';

interface CategoryFormProps {
  category?: Category | null;
  onSubmit: (data: any) => void;
  onCancel: () => void;
}

const CategoryForm: React.FC<CategoryFormProps> = ({ category, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    icon: 'category',
    color: '#1976d2',
    type: CategoryType.EXPENSE
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (category) {
      setFormData({
        name: category.name,
        description: category.description || '',
        icon: category.icon,
        color: category.color,
        type: category.type
      });
    }
  }, [category]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome é obrigatório';
    } else if (formData.name.length > 50) {
      newErrors.name = 'Nome deve ter no máximo 50 caracteres';
    }

    if (formData.description && formData.description.length > 200) {
      newErrors.description = 'Descrição deve ter no máximo 200 caracteres';
    }

    if (!/^#[0-9A-Fa-f]{6}$/.test(formData.color)) {
      newErrors.color = 'Cor deve estar no formato hexadecimal (#RRGGBB)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const iconOptions = [
    { value: 'category', label: 'Categoria' },
    { value: 'home', label: 'Casa' },
    { value: 'food', label: 'Comida' },
    { value: 'transport', label: 'Transporte' },
    { value: 'shopping', label: 'Compras' },
    { value: 'entertainment', label: 'Entretenimento' },
    { value: 'health', label: 'Saúde' },
    { value: 'education', label: 'Educação' },
    { value: 'work', label: 'Trabalho' },
    { value: 'salary', label: 'Salário' },
    { value: 'investment', label: 'Investimento' },
    { value: 'gift', label: 'Presente' },
    { value: 'restaurant', label: 'Restaurante' },
    { value: 'car', label: 'Carro' },
    { value: 'plane', label: 'Avião' },
    { value: 'train', label: 'Trem' },
    { value: 'bus', label: 'Ônibus' },
    { value: 'bike', label: 'Bicicleta' },
    { value: 'walk', label: 'Caminhada' },
    { value: 'coffee', label: 'Café' },
    { value: 'beer', label: 'Cerveja' },
    { value: 'wine', label: 'Vinho' },
    { value: 'pizza', label: 'Pizza' },
    { value: 'burger', label: 'Hambúrguer' },
    { value: 'sushi', label: 'Sushi' },
    { value: 'grocery', label: 'Supermercado' },
    { value: 'pharmacy', label: 'Farmácia' },
    { value: 'hospital', label: 'Hospital' },
    { value: 'doctor', label: 'Médico' },
    { value: 'gym', label: 'Academia' },
    { value: 'sports', label: 'Esportes' },
    { value: 'movie', label: 'Cinema' },
    { value: 'music', label: 'Música' },
    { value: 'book', label: 'Livro' },
    { value: 'game', label: 'Jogo' },
    { value: 'travel', label: 'Viagem' },
    { value: 'hotel', label: 'Hotel' },
    { value: 'beach', label: 'Praia' },
    { value: 'mountain', label: 'Montanha' },
    { value: 'shopping_cart', label: 'Carrinho' },
    { value: 'credit_card', label: 'Cartão' },
    { value: 'cash', label: 'Dinheiro' },
    { value: 'bank', label: 'Banco' },
    { value: 'wallet', label: 'Carteira' }
  ];

  const colorOptions = [
    { value: '#1976d2', label: 'Azul' },
    { value: '#dc004e', label: 'Rosa' },
    { value: '#ff6b6b', label: 'Vermelho' },
    { value: '#4ecdc4', label: 'Verde-água' },
    { value: '#45b7d1', label: 'Azul claro' },
    { value: '#96ceb4', label: 'Verde' },
    { value: '#ffeaa7', label: 'Amarelo' },
    { value: '#dda0dd', label: 'Lavanda' },
    { value: '#ffb347', label: 'Laranja' },
    { value: '#ff8c69', label: 'Salmão' },
    { value: '#87ceeb', label: 'Azul céu' },
    { value: '#c0c0c0', label: 'Prata' },
    { value: '#32cd32', label: 'Verde lima' },
    { value: '#228b22', label: 'Verde floresta' },
    { value: '#ffd700', label: 'Dourado' },
    { value: '#ff69b4', label: 'Rosa quente' },
    { value: '#90ee90', label: 'Verde claro' },
    { value: '#98fb98', label: 'Verde pálido' }
  ];

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Nome da Categoria"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            error={!!errors.name}
            helperText={errors.name}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Descrição (opcional)"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            error={!!errors.description}
            helperText={errors.description}
            multiline
            rows={3}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>Tipo</InputLabel>
            <Select
              value={formData.type}
              label="Tipo"
              onChange={(e) => handleChange('type', e.target.value)}
            >
              <MenuItem value={CategoryType.EXPENSE}>Despesa</MenuItem>
              <MenuItem value={CategoryType.INCOME}>Receita</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>Ícone</InputLabel>
            <Select
              value={formData.icon}
              label="Ícone"
              onChange={(e) => handleChange('icon', e.target.value)}
            >
              {iconOptions.map((icon) => (
                <MenuItem key={icon.value} value={icon.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box
                      sx={{
                        width: 24,
                        height: 24,
                        borderRadius: '50%',
                        backgroundColor: formData.color,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        mr: 1
                      }}
                    >
                      <Typography variant="caption" color="white">
                        {icon.value}
                      </Typography>
                    </Box>
                    {icon.label}
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl fullWidth error={!!errors.color}>
            <InputLabel>Cor</InputLabel>
            <Select
              value={formData.color}
              label="Cor"
              onChange={(e) => handleChange('color', e.target.value)}
            >
              {colorOptions.map((color) => (
                <MenuItem key={color.value} value={color.value}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box
                      sx={{
                        width: 20,
                        height: 20,
                        borderRadius: '50%',
                        backgroundColor: color.value,
                        mr: 1,
                        border: '1px solid #ccc'
                      }}
                    />
                    {color.label} ({color.value})
                  </Box>
                </MenuItem>
              ))}
            </Select>
            {errors.color && <FormHelperText>{errors.color}</FormHelperText>}
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
        <Button onClick={onCancel} variant="outlined">
          Cancelar
        </Button>
        <Button type="submit" variant="contained">
          {category ? 'Atualizar' : 'Criar'} Categoria
        </Button>
      </Box>
    </Box>
  );
};

export default CategoryForm;
```

### **4. Componente CategoryStats**

```tsx
// src/components/categories/CategoryStats.tsx
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
```

## 🔧 **Componentes Reutilizáveis**

### **1. CategoryContext**

```tsx
// src/contexts/CategoryContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import { Category, CategoryCreate, CategoryUpdate } from '../types/category';

interface CategoryContextType {
  categories: Category[];
  loading: boolean;
  error: string | null;
  createCategory: (data: CategoryCreate) => Promise<void>;
  updateCategory: (id: string, data: CategoryUpdate) => Promise<void>;
  deleteCategory: (id: string) => Promise<void>;
  restoreCategory: (id: string) => Promise<void>;
  getCategoriesByType: (type: 'expense' | 'income') => Category[];
  getCategoryById: (id: string) => Category | undefined;
}

const CategoryContext = createContext<CategoryContextType | undefined>(undefined);

export const useCategories = () => {
  const context = useContext(CategoryContext);
  if (context === undefined) {
    throw new Error('useCategories must be used within a CategoryProvider');
  }
  return context;
};

interface CategoryProviderProps {
  children: ReactNode;
}

export const CategoryProvider: React.FC<CategoryProviderProps> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: fetchError } = await supabase
        .from('categories')
        .select('*')
        .order('name');

      if (fetchError) throw fetchError;

      setCategories(data || []);
    } catch (err) {
      setError('Erro ao carregar categorias');
      console.error('Erro ao buscar categorias:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const createCategory = async (categoryData: CategoryCreate) => {
    try {
      setError(null);

      const { data, error: createError } = await supabase
        .from('categories')
        .insert([categoryData])
        .select()
        .single();

      if (createError) throw createError;

      setCategories(prev => [...prev, data]);
    } catch (err) {
      setError('Erro ao criar categoria');
      throw err;
    }
  };

  const updateCategory = async (id: string, categoryData: CategoryUpdate) => {
    try {
      setError(null);

      const { data, error: updateError } = await supabase
        .from('categories')
        .update(categoryData)
        .eq('id', id)
        .select()
        .single();

      if (updateError) throw updateError;

      setCategories(prev => 
        prev.map(cat => cat.id === id ? data : cat)
      );
    } catch (err) {
      setError('Erro ao atualizar categoria');
      throw err;
    }
  };

  const deleteCategory = async (id: string) => {
    try {
      setError(null);

      const { error: deleteError } = await supabase
        .from('categories')
        .update({ is_active: false })
        .eq('id', id);

      if (deleteError) throw deleteError;

      setCategories(prev => 
        prev.map(cat => cat.id === id ? { ...cat, is_active: false } : cat)
      );
    } catch (err) {
      setError('Erro ao excluir categoria');
      throw err;
    }
  };

  const restoreCategory = async (id: string) => {
    try {
      setError(null);

      const { error: restoreError } = await supabase
        .from('categories')
        .update({ is_active: true })
        .eq('id', id);

      if (restoreError) throw restoreError;

      setCategories(prev => 
        prev.map(cat => cat.id === id ? { ...cat, is_active: true } : cat)
      );
    } catch (err) {
      setError('Erro ao restaurar categoria');
      throw err;
    }
  };

  const getCategoriesByType = (type: 'expense' | 'income') => {
    return categories.filter(cat => cat.type === type && cat.is_active);
  };

  const getCategoryById = (id: string) => {
    return categories.find(cat => cat.id === id);
  };

  const value = {
    categories,
    loading,
    error,
    createCategory,
    updateCategory,
    deleteCategory,
    restoreCategory,
    getCategoriesByType,
    getCategoryById,
  };

  return (
    <CategoryContext.Provider value={value}>
      {children}
    </CategoryContext.Provider>
  );
};
```

### **2. CategorySelector**

```tsx
// src/components/categories/CategorySelector.tsx
import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography
} from '@mui/material';
import { useCategories } from '../../contexts/CategoryContext';
import { CategoryType } from '../../types/category';

interface CategorySelectorProps {
  value: string | null;
  onChange: (categoryId: string | null) => void;
  type: CategoryType;
  label?: string;
  required?: boolean;
  disabled?: boolean;
}

const CategorySelector: React.FC<CategorySelectorProps> = ({
  value,
  onChange,
  type,
  label = 'Categoria',
  required = false,
  disabled = false
}) => {
  const { getCategoriesByType } = useCategories();
  const categories = getCategoriesByType(type);

  return (
    <FormControl fullWidth required={required} disabled={disabled}>
      <InputLabel>{label}</InputLabel>
      <Select
        value={value || ''}
        label={label}
        onChange={(e) => onChange(e.target.value || null)}
      >
        <MenuItem value="">
          <em>Selecione uma categoria</em>
        </MenuItem>
        {categories.map((category) => (
          <MenuItem key={category.id} value={category.id}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  borderRadius: '50%',
                  backgroundColor: category.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mr: 1
                }}
              >
                <Typography variant="caption" color="white" fontSize="10px">
                  {category.icon}
                </Typography>
              </Box>
              <Typography>{category.name}</Typography>
            </Box>
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default CategorySelector;
```

## 🎨 **Design System**

### **Cores e Ícones**

```tsx
// src/theme/categoryTheme.ts
export const categoryColors = {
  expense: {
    primary: '#FF6B6B',
    secondary: '#FF8C69',
    light: '#FFB3B3',
    dark: '#E53E3E'
  },
  income: {
    primary: '#32CD32',
    secondary: '#228B22',
    light: '#90EE90',
    dark: '#228B22'
  }
};

export const categoryIcons = {
  expense: [
    'home', 'food', 'transport', 'shopping', 'entertainment',
    'health', 'education', 'restaurant', 'travel', 'car',
    'plane', 'train', 'bus', 'bike', 'coffee', 'beer',
    'wine', 'pizza', 'burger', 'sushi', 'grocery',
    'pharmacy', 'hospital', 'doctor', 'gym', 'sports',
    'movie', 'music', 'book', 'game', 'hotel', 'beach'
  ],
  income: [
    'work', 'salary', 'investment', 'gift', 'cash',
    'bank', 'wallet', 'credit_card', 'shopping_cart'
  ]
};

export const getCategoryIconColor = (type: 'expense' | 'income') => {
  return categoryColors[type].primary;
};
```

### **Responsividade**

```tsx
// src/hooks/useCategoryResponsive.ts
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

export const useCategoryResponsive = () => {
  const theme = useTheme();
  
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  
  const getGridSize = () => {
    if (isMobile) return 12;
    if (isTablet) return 6;
    return 4;
  };
  
  const getCardHeight = () => {
    if (isMobile) return 'auto';
    return '200px';
  };
  
  return { 
    isMobile, 
    isTablet, 
    isDesktop, 
    getGridSize, 
    getCardHeight 
  };
};
```

## 🧪 **Testes de Interface**

### **Teste do CategoryCard**

```tsx
// src/components/categories/__tests__/CategoryCard.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from '../../../theme';
import CategoryCard from '../CategoryCard';

const mockCategory = {
  id: '1',
  name: 'Alimentação',
  description: 'Gastos com comida',
  icon: 'food',
  color: '#FF6B6B',
  type: 'expense' as const,
  is_default: false,
  is_active: true,
  user_id: 'user-1',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z'
};

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('CategoryCard', () => {
  test('renderiza informações da categoria', () => {
    const onEdit = jest.fn();
    const onDelete = jest.fn();
    
    renderWithTheme(
      <CategoryCard 
        category={mockCategory} 
        onEdit={onEdit} 
        onDelete={onDelete} 
      />
    );
    
    expect(screen.getByText('Alimentação')).toBeInTheDocument();
    expect(screen.getByText('Gastos com comida')).toBeInTheDocument();
    expect(screen.getByText('Despesa')).toBeInTheDocument();
  });

  test('chama onEdit quando botão de editar é clicado', () => {
    const onEdit = jest.fn();
    const onDelete = jest.fn();
    
    renderWithTheme(
      <CategoryCard 
        category={mockCategory} 
        onEdit={onEdit} 
        onDelete={onDelete} 
      />
    );
    
    const editButton = screen.getByLabelText('edit');
    fireEvent.click(editButton);
    
    expect(onEdit).toHaveBeenCalledTimes(1);
  });

  test('chama onDelete quando botão de excluir é clicado', () => {
    const onEdit = jest.fn();
    const onDelete = jest.fn();
    
    renderWithTheme(
      <CategoryCard 
        category={mockCategory} 
        onEdit={onEdit} 
        onDelete={onDelete} 
      />
    );
    
    const deleteButton = screen.getByLabelText('delete');
    fireEvent.click(deleteButton);
    
    expect(onDelete).toHaveBeenCalledTimes(1);
  });

  test('não mostra botões de ação para categorias padrão', () => {
    const onEdit = jest.fn();
    const onDelete = jest.fn();
    const defaultCategory = { ...mockCategory, is_default: true };
    
    renderWithTheme(
      <CategoryCard 
        category={defaultCategory} 
        onEdit={onEdit} 
        onDelete={onDelete} 
      />
    );
    
    expect(screen.queryByLabelText('edit')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('delete')).not.toBeInTheDocument();
    expect(screen.getByText('Padrão')).toBeInTheDocument();
  });
});
```

Esta interface do usuário fornece uma experiência completa e intuitiva para o gerenciamento de categorias, com componentes reutilizáveis, design responsivo e testes adequados. 