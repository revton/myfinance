// src/components/filters/CategoryFilter.tsx
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  OutlinedInput,
  Checkbox,
  ListItemText,
  Button,
  Tooltip
} from '@mui/material';
import { useCategories } from '../../contexts/CategoryContext';
import { Category, FilterList, CheckCircle, Cancel } from '@mui/icons-material';

interface CategoryFilterProps {
  onFilterChange: (categoryIds: string[]) => void;
  initialCategories?: string[];
  type?: 'expense' | 'income' | 'all';
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({ 
  onFilterChange, 
  initialCategories = [], 
  type = 'all' 
}) => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(initialCategories);
  const { getCategoriesByType } = useCategories();
  
  // Ref to track the previous initialCategories value
  const prevInitialCategoriesRef = useRef(initialCategories);

  // Reset selected categories when initialCategories changes (e.g., when filters are cleared)
  useEffect(() => {
    // Only reset if initialCategories has actually changed
    if (JSON.stringify(initialCategories) !== JSON.stringify(prevInitialCategoriesRef.current)) {
      setSelectedCategories(initialCategories || []);
      prevInitialCategoriesRef.current = initialCategories;
    }
  }, [initialCategories]);

  const categories = type === 'all' 
    ? [...getCategoriesByType('expense'), ...getCategoriesByType('income')]
    : getCategoriesByType(type);

  const handleCategoryChange = (categoryIds: string[]) => {
    setSelectedCategories(categoryIds);
    onFilterChange(categoryIds);
  };

  const handleSelectAll = () => {
    const allIds = categories.map(cat => cat.id);
    handleCategoryChange(allIds);
  };

  const handleClearAll = () => {
    handleCategoryChange([]);
  };

  const getSelectedCategoryNames = () => {
    return categories
      .filter(cat => selectedCategories.includes(cat.id))
      .map(cat => cat.name);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Category color="primary" />
        <Typography variant="h6">Filtro por Categorias</Typography>
      </Box>
      
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Tooltip title="Selecionar todas as categorias" arrow>
          <Button
            size="small"
            variant="outlined"
            onClick={handleSelectAll}
            startIcon={<CheckCircle />}
            color="primary"
          >
            Selecionar Todas
          </Button>
        </Tooltip>
        <Tooltip title="Limpar seleção de categorias" arrow>
          <Button
            size="small"
            variant="outlined"
            onClick={handleClearAll}
            startIcon={<Cancel />}
            color="error"
          >
            Limpar Todas
          </Button>
        </Tooltip>
      </Box>

      <FormControl fullWidth>
        <InputLabel>Categorias</InputLabel>
        <Select
          multiple
          value={selectedCategories}
          onChange={(e) => handleCategoryChange(e.target.value as string[])}
          input={<OutlinedInput label="Categorias" />}
          startAdornment={<FilterList color="action" sx={{ ml: 1, mr: -0.5 }} />}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {(selected as string[]).length > 0 ? (
                (selected as string[]).map((value) => {
                  const category = categories.find(cat => cat.id === value);
                  return (
                    <Chip
                      key={value}
                      label={category?.name || value}
                      size="small"
                      sx={{
                        backgroundColor: category?.color,
                        color: 'white',
                        borderRadius: 1.5,
                        '& .MuiChip-label': {
                          fontWeight: 500
                        }
                      }}
                    />
                  );
                })
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Nenhuma categoria selecionada
                </Typography>
              )}
            </Box>
          )}
        >
          {categories.map((category) => (
            <MenuItem key={category.id} value={category.id} dense>
              <Checkbox 
                checked={selectedCategories.indexOf(category.id) > -1} 
                color={category.type === 'expense' ? 'error' : 'success'}
                size="small"
              />
              <ListItemText 
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <span>{category.name}</span>
                    <Chip 
                      label={category.type === 'expense' ? 'Despesa' : 'Receita'}
                      size="small"
                      color={category.type === 'expense' ? 'error' : 'success'}
                      variant="outlined"
                      sx={{ height: 20, '& .MuiChip-label': { px: 1, py: 0, fontSize: '0.7rem' } }}
                    />
                  </Box>
                }
              />
              <Tooltip title={`Cor: ${category.color}`} arrow>
                <Box
                  sx={{
                    width: 20,
                    height: 20,
                    borderRadius: '50%',
                    backgroundColor: category.color,
                    ml: 1,
                    border: '1px solid rgba(0,0,0,0.1)'
                  }}
                />
              </Tooltip>
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {selectedCategories.length > 0 && (
        <Box sx={{ mt: 1 }}>
          <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
            <FilterList fontSize="small" />
            Categorias selecionadas ({selectedCategories.length}):
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {categories
              .filter(cat => selectedCategories.includes(cat.id))
              .map((category) => (
                <Tooltip key={category.id} title={`Remover ${category.name}`} arrow>
                  <Chip
                    label={category.name}
                    size="small"
                    onDelete={() => {
                      handleCategoryChange(
                        selectedCategories.filter(id => id !== category.id)
                      );
                    }}
                    sx={{
                      backgroundColor: category.color,
                      color: 'white',
                      borderRadius: 1.5,
                      '& .MuiChip-deleteIcon': {
                        color: 'rgba(255, 255, 255, 0.7)',
                        '&:hover': { color: 'white' }
                      }
                    }}
                  />
                </Tooltip>
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default CategoryFilter;