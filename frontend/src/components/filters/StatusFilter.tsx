// src/components/filters/StatusFilter.tsx
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  FormGroup,
  FormControlLabel,
  Checkbox
} from '@mui/material';

interface StatusFilterProps {
  onFilterChange: (filters: StatusFilters) => void;
  initialFilters?: StatusFilters;
}

interface StatusFilters {
  type: 'expense' | 'income' | 'all';
}

const StatusFilter: React.FC<StatusFilterProps> = ({ onFilterChange, initialFilters }) => {
  const [filters, setFilters] = useState<StatusFilters>(initialFilters || {
    type: 'all'
  });
  
  // Ref to track the previous initialFilters value
  const prevInitialFiltersRef = useRef(initialFilters);

  // Reset filters when initialFilters changes (e.g., when filters are cleared)
  useEffect(() => {
    // Only reset if initialFilters has actually changed
    if (JSON.stringify(initialFilters) !== JSON.stringify(prevInitialFiltersRef.current)) {
      setFilters(initialFilters || {
        type: 'all'
      });
      prevInitialFiltersRef.current = initialFilters;
    }
  }, [initialFilters]);

  const handleFilterChange = (field: keyof StatusFilters, value: any) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const getTypeLabel = () => {
    switch (filters.type) {
      case 'expense': return 'Despesas';
      case 'income': return 'Receitas';
      case 'all': return 'Todas';
      default: return 'Tipo';
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Typography variant="h6">Filtro de Tipo de Transação</Typography>
      
      <FormControl fullWidth>
        <InputLabel>Tipo de Transação</InputLabel>
        <Select
          value={filters.type}
          label="Tipo de Transação"
          onChange={(e) => handleFilterChange('type', e.target.value)}
        >
          <MenuItem value="all">Todas</MenuItem>
          <MenuItem value="expense">Despesas</MenuItem>
          <MenuItem value="income">Receitas</MenuItem>
        </Select>
      </FormControl>

      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        {filters.type !== 'all' && (
          <Chip
            label={getTypeLabel()}
            onDelete={() => handleFilterChange('type', 'all')}
            color="primary"
            variant="outlined"
          />
        )}
      </Box>
    </Box>
  );
};

export default StatusFilter;