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
import { getIconComponent } from '../utils/iconUtils';

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
    restoreCategory,
    refreshCategories
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
    } catch (error: any) {
      console.error('Erro ao salvar categoria:', error);
      // Optionally, set a local error state to display to the user
    }
  };

  const handleDelete = async (categoryId: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta categoria?')) {
      try {
        await deleteCategory(categoryId);
      } catch (error: any) {
        console.error('Erro ao excluir categoria:', error);
        // Optionally, set a local error state to display to the user
      }
    }
  };

  const handleRestore = async (categoryId: string) => {
    try {
      await restoreCategory(categoryId);
    } catch (error: any) {
      console.error('Erro ao restaurar categoria:', error);
      // Optionally, set a local error state to display to the user
    }
  };

  const expenseCategories = (categories ?? []).filter(c => c.type === 'expense' && c.is_active);
  const incomeCategories = (categories ?? []).filter(c => c.type === 'income' && c.is_active);
  const deletedCategories = (categories ?? []).filter(c => !c.is_active);

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
              {deletedCategories.map((category) => {
                const IconComponent = getIconComponent(category.icon);
                return (
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
                            <IconComponent sx={{ color: 'white', fontSize: 24 }} /> 
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
                );
              })}
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

