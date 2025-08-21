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
  Button
} from '@mui/material';
import { useCategories } from '../../contexts/CategoryContext';

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
      <Typography variant="h6">Filtro por Categorias</Typography>
      
      <Box sx={{ display: 'flex', gap: 1 }}>
        <Button
          size="small"
          variant="outlined"
          onClick={handleSelectAll}
        >
          Selecionar Todas
        </Button>
        <Button
          size="small"
          variant="outlined"
          onClick={handleClearAll}
        >
          Limpar Todas
        </Button>
      </Box>

      <FormControl fullWidth>
        <InputLabel>Categorias</InputLabel>
        <Select
          multiple
          value={selectedCategories}
          onChange={(e) => handleCategoryChange(e.target.value as string[])}
          input={<OutlinedInput label="Categorias" />}
          renderValue={(selected) => (
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
              {(selected as string[]).map((value) => {
                const category = categories.find(cat => cat.id === value);
                return (
                  <Chip
                    key={value}
                    label={category?.name || value}
                    size="small"
                    sx={{
                      backgroundColor: category?.color,
                      color: 'white'
                    }}
                  />
                );
              })}
            </Box>
          )}
        >
          {categories.map((category) => (
            <MenuItem key={category.id} value={category.id}>
              <Checkbox checked={selectedCategories.indexOf(category.id) > -1} />
              <ListItemText 
                primary={category.name}
                secondary={category.type === 'expense' ? 'Despesa' : 'Receita'}
              />
              <Box
                sx={{
                  width: 16,
                  height: 16,
                  borderRadius: '50%',
                  backgroundColor: category.color,
                  ml: 1
                }}
              />
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {selectedCategories.length > 0 && (
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Categorias selecionadas:
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {getSelectedCategoryNames().map((name) => (
              <Chip
                key={name}
                label={name}
                size="small"
                onDelete={() => {
                  const category = categories.find(cat => cat.name === name);
                  if (category) {
                    handleCategoryChange(
                      selectedCategories.filter(id => id !== category.id)
                    );
                  }
                }}
              />
            ))}
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default CategoryFilter;