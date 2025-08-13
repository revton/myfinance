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
