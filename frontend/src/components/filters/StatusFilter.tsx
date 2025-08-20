// src/components/filters/StatusFilter.tsx
import React, { useState } from 'react';
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
  status: 'all' | 'pending' | 'completed' | 'cancelled';
  hasCategory: boolean | null;
  hasNotes: boolean | null;
}

const StatusFilter: React.FC<StatusFilterProps> = ({ onFilterChange, initialFilters }) => {
  const [filters, setFilters] = useState<StatusFilters>(initialFilters || {
    type: 'all',
    status: 'all',
    hasCategory: null,
    hasNotes: null
  });

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

  const getStatusLabel = () => {
    switch (filters.status) {
      case 'pending': return 'Pendente';
      case 'completed': return 'Concluída';
      case 'cancelled': return 'Cancelada';
      case 'all': return 'Todos';
      default: return 'Status';
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Typography variant="h6">Filtro por Status</Typography>
      
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

      <FormControl fullWidth>
        <InputLabel>Status</InputLabel>
        <Select
          value={filters.status}
          label="Status"
          onChange={(e) => handleFilterChange('status', e.target.value)}
        >
          <MenuItem value="all">Todos</MenuItem>
          <MenuItem value="pending">Pendente</MenuItem>
          <MenuItem value="completed">Concluída</MenuItem>
          <MenuItem value="cancelled">Cancelada</MenuItem>
        </Select>
      </FormControl>

      <FormGroup>
        <FormControlLabel
          control={
            <Checkbox
              checked={filters.hasCategory === true}
              indeterminate={filters.hasCategory === null}
              onChange={(e) => {
                const value = e.target.checked ? true : null;
                handleFilterChange('hasCategory', value);
              }}
            />
          }
          label="Com categoria"
        />
        <FormControlLabel
          control={
            <Checkbox
              checked={filters.hasNotes === true}
              indeterminate={filters.hasNotes === null}
              onChange={(e) => {
                const value = e.target.checked ? true : null;
                handleFilterChange('hasNotes', value);
              }}
            />
          }
          label="Com notas"
        />
      </FormGroup>

      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        {filters.type !== 'all' && (
          <Chip
            label={getTypeLabel()}
            onDelete={() => handleFilterChange('type', 'all')}
            color="primary"
            variant="outlined"
          />
        )}
        {filters.status !== 'all' && (
          <Chip
            label={getStatusLabel()}
            onDelete={() => handleFilterChange('status', 'all')}
            color="primary"
            variant="outlined"
          />
        )}
        {filters.hasCategory === true && (
          <Chip
            label="Com categoria"
            onDelete={() => handleFilterChange('hasCategory', null)}
            color="primary"
            variant="outlined"
          />
        )}
        {filters.hasNotes === true && (
          <Chip
            label="Com notas"
            onDelete={() => handleFilterChange('hasNotes', null)}
            color="primary"
            variant="outlined"
          />
        )}
      </Box>
    </Box>
  );
};

export default StatusFilter;