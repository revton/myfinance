import React, { useState, useEffect, useRef } from 'react';
import { Grid as GridComponent } from 'react-window';
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
import { useToast } from '../hooks/useToast';
import CategoryForm from '../components/categories/CategoryForm';
import CategoryCard from '../components/categories/CategoryCard';
import CategoryStats from '../components/categories/CategoryStats';
import { getIconComponent } from '../utils/iconUtils';
import * as Sentry from '@sentry/react';

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
  const toast = useToast();
  
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
        toast.success('Categoria atualizada com sucesso!');
      } else {
        await createCategory(categoryData);
        toast.success('Categoria criada com sucesso!');
      }
      handleCloseDialog();
    } catch (error: any) {
      console.error('Erro ao salvar categoria:', error);
      Sentry.captureException(error);
      toast.error(error.response?.data?.detail || 'Erro ao salvar categoria.');
    }
  };

  const handleDelete = async (categoryId: string) => {
    if (window.confirm('Tem certeza que deseja excluir esta categoria?')) {
      try {
        await deleteCategory(categoryId);
        toast.success('Categoria excluída com sucesso!');
      } catch (error: any) {
        console.error('Erro ao excluir categoria:', error);
        Sentry.captureException(error);
        toast.error(error.response?.data?.detail || 'Erro ao excluir categoria.');
      }
    }
  };

  const handleRestore = async (categoryId: string) => {
    try {
      await restoreCategory(categoryId);
      toast.success('Categoria restaurada com sucesso!');
    } catch (error: any) {
      console.error('Erro ao restaurar categoria:', error);
      Sentry.captureException(error);
      toast.error(error.response?.data?.detail || 'Erro ao restaurar categoria.');
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
            {expenseCategories.length === 0 ? (
              <Box textAlign="center" py={4}>
                <Typography variant="body1" color="text.secondary">
                  Nenhuma categoria de despesa encontrada.
                </Typography>
              </Box>
            ) : (
              <Box sx={{ height: 600, width: '100%' }}>
                <VirtualizedCategoryGrid 
                  categories={expenseCategories} 
                  onEdit={handleOpenDialog} 
                  onDelete={handleDelete} 
                />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            {incomeCategories.length === 0 ? (
              <Box textAlign="center" py={4}>
                <Typography variant="body1" color="text.secondary">
                  Nenhuma categoria de receita encontrada.
                </Typography>
              </Box>
            ) : (
              <Box sx={{ height: 600, width: '100%' }}>
                <VirtualizedCategoryGrid 
                  categories={incomeCategories} 
                  onEdit={handleOpenDialog} 
                  onDelete={handleDelete} 
                />
              </Box>
            )}
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <CategoryStats categories={categories} />
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            {deletedCategories.length === 0 ? (
              <Box textAlign="center" py={4}>
                <Typography variant="body1" color="text.secondary">
                  Nenhuma categoria excluída.
                </Typography>
              </Box>
            ) : (
              <Box sx={{ height: 600, width: '100%' }}>
                <VirtualizedDeletedCategoryGrid 
                  categories={deletedCategories} 
                  onRestore={handleRestore} 
                />
              </Box>
            )}
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



// Componente para renderizar categorias em uma grade virtualizada
interface VirtualizedCategoryGridProps {
  categories: any[];
  onEdit: (category: any) => void;
  onDelete: (categoryId: string) => void;
}

const VirtualizedCategoryGrid: React.FC<VirtualizedCategoryGridProps> = ({ categories, onEdit, onDelete }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 600 });
  
  // Número de colunas com base na largura disponível
  const columnCount = Math.max(1, Math.floor(dimensions.width / 350));
  const rowCount = Math.ceil(categories.length / columnCount);
  
  // Tamanho de cada célula
  const cellWidth = dimensions.width / columnCount;
  const cellHeight = 250; // Altura estimada para cada card de categoria
  
  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.offsetWidth,
        height: 600
      });
    }
    
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: 600
        });
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  const Cell = ({ columnIndex, rowIndex, style }: { columnIndex: number, rowIndex: number, style: React.CSSProperties }) => {
    const index = rowIndex * columnCount + columnIndex;
    if (index >= categories.length) return null;
    
    const category = categories[index];
    
    return (
      <div style={{ ...style, padding: 8 }}>
        <CategoryCard
          category={category}
          onEdit={() => onEdit(category)}
          onDelete={() => onDelete(category.id)}
        />
      </div>
    );
  };
  
  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%' }}>
      {dimensions.width > 0 && (
        <GridComponent
          cellComponent={Cell}
          cellProps={{}}
          columnCount={columnCount}
          columnWidth={cellWidth}
          defaultHeight={dimensions.height}
          defaultWidth={dimensions.width}
          height={dimensions.height}
          rowCount={rowCount}
          rowHeight={cellHeight}
          width={dimensions.width}
          overscanCount={2}
        />
      )}
    </div>
  );
};

// Componente para renderizar categorias excluídas em uma grade virtualizada
interface VirtualizedDeletedCategoryGridProps {
  categories: any[];
  onRestore: (categoryId: string) => void;
}

const VirtualizedDeletedCategoryGrid: React.FC<VirtualizedDeletedCategoryGridProps> = ({ categories, onRestore }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 600 });
  
  // Número de colunas com base na largura disponível
  const columnCount = Math.max(1, Math.floor(dimensions.width / 350));
  const rowCount = Math.ceil(categories.length / columnCount);
  
  // Tamanho de cada célula
  const cellWidth = dimensions.width / columnCount;
  const cellHeight = 200; // Altura estimada para cada card de categoria excluída
  
  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.offsetWidth,
        height: 600
      });
    }
    
    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: 600
        });
      }
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  const Cell = ({ columnIndex, rowIndex, style }: { columnIndex: number, rowIndex: number, style: React.CSSProperties }) => {
    const index = rowIndex * columnCount + columnIndex;
    if (index >= categories.length) return null;
    
    const category = categories[index];
    const IconComponent = getIconComponent(category.icon);
    
    return (
      <div style={{ ...style, padding: 8 }}>
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
                onClick={() => onRestore(category.id)}
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
      </div>
    );
  };
  
  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%' }}>
      {dimensions.width > 0 && (
        <GridComponent
          cellComponent={Cell}
          cellProps={{}}
          columnCount={columnCount}
          columnWidth={cellWidth}
          defaultHeight={dimensions.height}
          defaultWidth={dimensions.width}
          height={dimensions.height}
          rowCount={rowCount}
          rowHeight={cellHeight}
          width={dimensions.width}
          overscanCount={2}
        />
      )}
    </div>
  );
};

export default CategoriesPage;