// src/components/filters/AmountRangeFilter.tsx
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  Typography,
  TextField,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip
} from '@mui/material';

interface AmountRangeFilterProps {
  onFilterChange: (filters: AmountRangeFilters) => void;
  initialFilters?: AmountRangeFilters;
  maxAmount?: number;
}

interface AmountRangeFilters {
  minAmount?: number;
  maxAmount?: number;
}

const AmountRangeFilter: React.FC<AmountRangeFilterProps> = ({ 
  onFilterChange, 
  initialFilters,
  maxAmount = 10000 
}) => {
  const [filters, setFilters] = useState<AmountRangeFilters>(initialFilters || {});
  
  // Ref to track the previous initialFilters value
  const prevInitialFiltersRef = useRef(initialFilters);

  // Reset filters when initialFilters changes (e.g., when filters are cleared)
  useEffect(() => {
    // Only reset if initialFilters has actually changed
    if (JSON.stringify(initialFilters) !== JSON.stringify(prevInitialFiltersRef.current)) {
      setFilters(initialFilters || {});
      prevInitialFiltersRef.current = initialFilters;
    }
  }, [initialFilters]);

  const handleAmountChange = (field: 'minAmount' | 'maxAmount', value: string) => {
    const numValue = value === '' ? undefined : parseFloat(value);
    const newFilters = { ...filters, [field]: numValue };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    const [min, max] = newValue as number[];
    const newFilters = { 
      ...filters, 
      minAmount: min === 0 ? undefined : min,
      maxAmount: max === maxAmount ? undefined : max
    };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Typography variant="h6">Filtro por Valor</Typography>
      
      <Box sx={{ display: 'flex', gap: 2 }}>
        <TextField
          label="Valor Mínimo"
          type="number"
          value={filters.minAmount || ''}
          onChange={(e) => handleAmountChange('minAmount', e.target.value)}
          InputProps={{
            startAdornment: <span>R$</span>
          }}
          fullWidth
        />
        <TextField
          label="Valor Máximo"
          type="number"
          value={filters.maxAmount || ''}
          onChange={(e) => handleAmountChange('maxAmount', e.target.value)}
          InputProps={{
            startAdornment: <span>R$</span>
          }}
          fullWidth
        />
      </Box>

      <Box>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Faixa de Valores
        </Typography>
        <Slider
          value={[
            filters.minAmount || 0,
            filters.maxAmount || maxAmount
          ]}
          onChange={handleSliderChange}
          valueLabelDisplay="auto"
          min={0}
          max={maxAmount}
          step={100}
          valueLabelFormat={(value) => `R$ ${value.toLocaleString('pt-BR')}`}
        />
      </Box>

      {(filters.minAmount || filters.maxAmount) && (
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          {filters.minAmount && (
            <Chip
              label={`Mín: R$ ${filters.minAmount.toLocaleString('pt-BR')}`}
              onDelete={() => handleAmountChange('minAmount', '')}
              color="primary"
              variant="outlined"
            />
          )}
          {filters.maxAmount && (
            <Chip
              label={`Máx: R$ ${filters.maxAmount.toLocaleString('pt-BR')}`}
              onDelete={() => handleAmountChange('maxAmount', '')}
              color="primary"
              variant="outlined"
            />
          )}
        </Box>
      )}
    </Box>
  );
};

export default AmountRangeFilter;