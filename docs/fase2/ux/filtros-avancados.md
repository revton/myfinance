# 🔍 Filtros Avançados - Melhorias de UX

## 🎯 **Visão Geral**

Este documento descreve a implementação de filtros avançados para melhorar a experiência do usuário na visualização e análise de transações financeiras.

## 📊 **Tipos de Filtros**

### **1. Filtros Temporais**

#### **Filtro por Período**
```tsx
// src/components/filters/DateRangeFilter.tsx
import React, { useState } from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Chip,
  Typography
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ptBR } from 'date-fns/locale';

interface DateRangeFilterProps {
  onFilterChange: (filters: DateRangeFilters) => void;
  initialFilters?: DateRangeFilters;
}

interface DateRangeFilters {
  period: 'today' | 'week' | 'month' | 'quarter' | 'year' | 'custom';
  startDate?: Date;
  endDate?: Date;
}

const DateRangeFilter: React.FC<DateRangeFilterProps> = ({ onFilterChange, initialFilters }) => {
  const [filters, setFilters] = useState<DateRangeFilters>(initialFilters || {
    period: 'month'
  });

  const handlePeriodChange = (period: string) => {
    const newFilters = { ...filters, period: period as any };
    
    // Calcular datas baseadas no período
    const now = new Date();
    switch (period) {
      case 'today':
        newFilters.startDate = now;
        newFilters.endDate = now;
        break;
      case 'week':
        const weekStart = new Date(now);
        weekStart.setDate(now.getDate() - now.getDay());
        newFilters.startDate = weekStart;
        newFilters.endDate = now;
        break;
      case 'month':
        const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
        newFilters.startDate = monthStart;
        newFilters.endDate = now;
        break;
      case 'quarter':
        const quarter = Math.floor(now.getMonth() / 3);
        const quarterStart = new Date(now.getFullYear(), quarter * 3, 1);
        newFilters.startDate = quarterStart;
        newFilters.endDate = now;
        break;
      case 'year':
        const yearStart = new Date(now.getFullYear(), 0, 1);
        newFilters.startDate = yearStart;
        newFilters.endDate = now;
        break;
    }
    
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleCustomDateChange = (field: 'startDate' | 'endDate', date: Date | null) => {
    const newFilters = { ...filters, [field]: date };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const getPeriodLabel = () => {
    switch (filters.period) {
      case 'today': return 'Hoje';
      case 'week': return 'Esta Semana';
      case 'month': return 'Este Mês';
      case 'quarter': return 'Este Trimestre';
      case 'year': return 'Este Ano';
      case 'custom': return 'Personalizado';
      default: return 'Período';
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ptBR}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <Typography variant="h6">Filtro por Período</Typography>
        
        <FormControl fullWidth>
          <InputLabel>Período</InputLabel>
          <Select
            value={filters.period}
            label="Período"
            onChange={(e) => handlePeriodChange(e.target.value)}
          >
            <MenuItem value="today">Hoje</MenuItem>
            <MenuItem value="week">Esta Semana</MenuItem>
            <MenuItem value="month">Este Mês</MenuItem>
            <MenuItem value="quarter">Este Trimestre</MenuItem>
            <MenuItem value="year">Este Ano</MenuItem>
            <MenuItem value="custom">Personalizado</MenuItem>
          </Select>
        </FormControl>

        {filters.period === 'custom' && (
          <Box sx={{ display: 'flex', gap: 2 }}>
            <DatePicker
              label="Data Inicial"
              value={filters.startDate || null}
              onChange={(date) => handleCustomDateChange('startDate', date)}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
            <DatePicker
              label="Data Final"
              value={filters.endDate || null}
              onChange={(date) => handleCustomDateChange('endDate', date)}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
          </Box>
        )}

        {(filters.startDate || filters.endDate) && (
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {filters.startDate && (
              <Chip
                label={`De: ${filters.startDate.toLocaleDateString('pt-BR')}`}
                onDelete={() => handleCustomDateChange('startDate', null)}
                color="primary"
                variant="outlined"
              />
            )}
            {filters.endDate && (
              <Chip
                label={`Até: ${filters.endDate.toLocaleDateString('pt-BR')}`}
                onDelete={() => handleCustomDateChange('endDate', null)}
                color="primary"
                variant="outlined"
              />
            )}
          </Box>
        )}
      </Box>
    </LocalizationProvider>
  );
};

export default DateRangeFilter;
```

### **2. Filtros por Categoria**

#### **Filtro de Categorias Múltiplas**
```tsx
// src/components/filters/CategoryFilter.tsx
import React, { useState, useEffect } from 'react';
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
              {selected.map((value) => {
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
```

### **3. Filtros por Valor**

#### **Filtro de Faixa de Valores**
```tsx
// src/components/filters/AmountRangeFilter.tsx
import React, { useState } from 'react';
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
  type: 'expense' | 'income' | 'all';
}

const AmountRangeFilter: React.FC<AmountRangeFilterProps> = ({ 
  onFilterChange, 
  initialFilters,
  maxAmount = 10000 
}) => {
  const [filters, setFilters] = useState<AmountRangeFilters>(initialFilters || {
    type: 'all'
  });

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

  const handleTypeChange = (type: string) => {
    const newFilters = { ...filters, type: type as any };
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
      <Typography variant="h6">Filtro por Valor</Typography>
      
      <FormControl fullWidth>
        <InputLabel>Tipo de Transação</InputLabel>
        <Select
          value={filters.type}
          label="Tipo de Transação"
          onChange={(e) => handleTypeChange(e.target.value)}
        >
          <MenuItem value="all">Todas</MenuItem>
          <MenuItem value="expense">Despesas</MenuItem>
          <MenuItem value="income">Receitas</MenuItem>
        </Select>
      </FormControl>

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
```

### **4. Filtros por Status**

#### **Filtro de Status de Transações**
```tsx
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
```

## 🔧 **Componente Principal de Filtros**

### **Filtros Avançados Consolidados**
```tsx
// src/components/filters/AdvancedFilters.tsx
import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Button,
  Divider,
  Chip,
  IconButton,
  Collapse
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  FilterList as FilterListIcon,
  Clear as ClearIcon,
  Save as SaveIcon
} from '@mui/icons-material';
import DateRangeFilter from './DateRangeFilter';
import CategoryFilter from './CategoryFilter';
import AmountRangeFilter from './AmountRangeFilter';
import StatusFilter from './StatusFilter';

interface AdvancedFiltersProps {
  onFiltersChange: (filters: CombinedFilters) => void;
  onSaveFilters?: (filters: CombinedFilters, name: string) => void;
  savedFilters?: SavedFilter[];
  initialFilters?: CombinedFilters;
}

interface CombinedFilters {
  dateRange?: DateRangeFilters;
  categories?: string[];
  amountRange?: AmountRangeFilters;
  status?: StatusFilters;
}

interface SavedFilter {
  id: string;
  name: string;
  filters: CombinedFilters;
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({
  onFiltersChange,
  onSaveFilters,
  savedFilters = [],
  initialFilters
}) => {
  const [filters, setFilters] = useState<CombinedFilters>(initialFilters || {});
  const [expanded, setExpanded] = useState<string | false>(false);
  const [showFilters, setShowFilters] = useState(false);

  const handleFilterChange = (filterType: keyof CombinedFilters, value: any) => {
    const newFilters = { ...filters, [filterType]: value };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleClearAll = () => {
    const emptyFilters: CombinedFilters = {};
    setFilters(emptyFilters);
    onFiltersChange(emptyFilters);
  };

  const handleSaveFilters = () => {
    const name = prompt('Digite um nome para salvar estes filtros:');
    if (name && onSaveFilters) {
      onSaveFilters(filters, name);
    }
  };

  const handleLoadSavedFilter = (savedFilter: SavedFilter) => {
    setFilters(savedFilter.filters);
    onFiltersChange(savedFilter.filters);
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.dateRange?.startDate || filters.dateRange?.endDate) count++;
    if (filters.categories && filters.categories.length > 0) count++;
    if (filters.amountRange?.minAmount || filters.amountRange?.maxAmount) count++;
    if (filters.status?.type !== 'all' || filters.status?.status !== 'all') count++;
    return count;
  };

  const activeFiltersCount = getActiveFiltersCount();

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Button
          variant="outlined"
          startIcon={<FilterListIcon />}
          onClick={() => setShowFilters(!showFilters)}
          color={activeFiltersCount > 0 ? 'primary' : 'inherit'}
        >
          Filtros Avançados
          {activeFiltersCount > 0 && (
            <Chip
              label={activeFiltersCount}
              size="small"
              color="primary"
              sx={{ ml: 1 }}
            />
          )}
        </Button>
        
        {activeFiltersCount > 0 && (
          <Button
            variant="outlined"
            startIcon={<ClearIcon />}
            onClick={handleClearAll}
            size="small"
          >
            Limpar Filtros
          </Button>
        )}
        
        {onSaveFilters && (
          <Button
            variant="outlined"
            startIcon={<SaveIcon />}
            onClick={handleSaveFilters}
            size="small"
          >
            Salvar Filtros
          </Button>
        )}
      </Box>

      <Collapse in={showFilters}>
        <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Filtros Avançados
          </Typography>

          {savedFilters.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Filtros Salvos:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {savedFilters.map((savedFilter) => (
                  <Chip
                    key={savedFilter.id}
                    label={savedFilter.name}
                    onClick={() => handleLoadSavedFilter(savedFilter)}
                    variant="outlined"
                    clickable
                  />
                ))}
              </Box>
              <Divider sx={{ my: 2 }} />
            </Box>
          )}

          <Accordion
            expanded={expanded === 'dateRange'}
            onChange={(_, isExpanded) => setExpanded(isExpanded ? 'dateRange' : false)}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Filtro por Período</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <DateRangeFilter
                onFilterChange={(dateRange) => handleFilterChange('dateRange', dateRange)}
                initialFilters={filters.dateRange}
              />
            </AccordionDetails>
          </Accordion>

          <Accordion
            expanded={expanded === 'categories'}
            onChange={(_, isExpanded) => setExpanded(isExpanded ? 'categories' : false)}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Filtro por Categorias</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <CategoryFilter
                onFilterChange={(categories) => handleFilterChange('categories', categories)}
                initialCategories={filters.categories}
              />
            </AccordionDetails>
          </Accordion>

          <Accordion
            expanded={expanded === 'amountRange'}
            onChange={(_, isExpanded) => setExpanded(isExpanded ? 'amountRange' : false)}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Filtro por Valor</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <AmountRangeFilter
                onFilterChange={(amountRange) => handleFilterChange('amountRange', amountRange)}
                initialFilters={filters.amountRange}
              />
            </AccordionDetails>
          </Accordion>

          <Accordion
            expanded={expanded === 'status'}
            onChange={(_, isExpanded) => setExpanded(isExpanded ? 'status' : false)}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography>Filtro por Status</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <StatusFilter
                onFilterChange={(status) => handleFilterChange('status', status)}
                initialFilters={filters.status}
              />
            </AccordionDetails>
          </Accordion>
        </Paper>
      </Collapse>
    </Box>
  );
};

export default AdvancedFilters;
```

## 🎨 **Hook para Gerenciamento de Filtros**

### **useAdvancedFilters Hook**
```tsx
// src/hooks/useAdvancedFilters.ts
import { useState, useEffect, useCallback } from 'react';
import { useLocalStorage } from './useLocalStorage';

interface UseAdvancedFiltersOptions {
  initialFilters?: CombinedFilters;
  storageKey?: string;
  onFiltersChange?: (filters: CombinedFilters) => void;
}

export const useAdvancedFilters = (options: UseAdvancedFiltersOptions = {}) => {
  const {
    initialFilters = {},
    storageKey = 'myfinance-advanced-filters',
    onFiltersChange
  } = options;

  const [filters, setFilters] = useState<CombinedFilters>(initialFilters);
  const [savedFilters, setSavedFilters] = useLocalStorage<SavedFilter[]>(
    `${storageKey}-saved`,
    []
  );

  const updateFilters = useCallback((newFilters: CombinedFilters) => {
    setFilters(newFilters);
    onFiltersChange?.(newFilters);
  }, [onFiltersChange]);

  const saveFilters = useCallback((filters: CombinedFilters, name: string) => {
    const newSavedFilter: SavedFilter = {
      id: Date.now().toString(),
      name,
      filters
    };
    
    setSavedFilters(prev => [...prev, newSavedFilter]);
  }, [setSavedFilters]);

  const deleteSavedFilter = useCallback((filterId: string) => {
    setSavedFilters(prev => prev.filter(filter => filter.id !== filterId));
  }, [setSavedFilters]);

  const loadSavedFilter = useCallback((savedFilter: SavedFilter) => {
    updateFilters(savedFilter.filters);
  }, [updateFilters]);

  const clearFilters = useCallback(() => {
    updateFilters({});
  }, [updateFilters]);

  // Persistir filtros ativos
  useEffect(() => {
    if (Object.keys(filters).length > 0) {
      localStorage.setItem(`${storageKey}-active`, JSON.stringify(filters));
    } else {
      localStorage.removeItem(`${storageKey}-active`);
    }
  }, [filters, storageKey]);

  // Carregar filtros ativos ao inicializar
  useEffect(() => {
    const savedActiveFilters = localStorage.getItem(`${storageKey}-active`);
    if (savedActiveFilters) {
      try {
        const parsedFilters = JSON.parse(savedActiveFilters);
        setFilters(parsedFilters);
      } catch (error) {
        console.error('Erro ao carregar filtros salvos:', error);
      }
    }
  }, [storageKey]);

  return {
    filters,
    savedFilters,
    updateFilters,
    saveFilters,
    deleteSavedFilter,
    loadSavedFilter,
    clearFilters
  };
};
```

## 📊 **Integração com Lista de Transações**

### **Transações com Filtros Aplicados**
```tsx
// src/components/transactions/FilteredTransactionsList.tsx
import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Skeleton,
  Alert
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useTransactions } from '../../contexts/TransactionContext';
import { useAdvancedFilters } from '../../hooks/useAdvancedFilters';
import AdvancedFilters from '../filters/AdvancedFilters';
import TransactionItem from './TransactionItem';

interface FilteredTransactionsListProps {
  onEditTransaction?: (transaction: Transaction) => void;
  onDeleteTransaction?: (transactionId: string) => void;
}

const FilteredTransactionsList: React.FC<FilteredTransactionsListProps> = ({
  onEditTransaction,
  onDeleteTransaction
}) => {
  const { transactions, loading, error } = useTransactions();
  const { filters, updateFilters } = useAdvancedFilters({
    onFiltersChange: (newFilters) => {
      console.log('Filtros aplicados:', newFilters);
    }
  });

  const filteredTransactions = useMemo(() => {
    if (!transactions) return [];

    return transactions.filter(transaction => {
      // Filtro por período
      if (filters.dateRange?.startDate || filters.dateRange?.endDate) {
        const transactionDate = new Date(transaction.date);
        if (filters.dateRange.startDate && transactionDate < filters.dateRange.startDate) {
          return false;
        }
        if (filters.dateRange.endDate && transactionDate > filters.dateRange.endDate) {
          return false;
        }
      }

      // Filtro por categorias
      if (filters.categories && filters.categories.length > 0) {
        if (!transaction.category_id || !filters.categories.includes(transaction.category_id)) {
          return false;
        }
      }

      // Filtro por valor
      if (filters.amountRange?.minAmount || filters.amountRange?.maxAmount) {
        const amount = Number(transaction.amount);
        if (filters.amountRange.minAmount && amount < filters.amountRange.minAmount) {
          return false;
        }
        if (filters.amountRange.maxAmount && amount > filters.amountRange.maxAmount) {
          return false;
        }
      }

      // Filtro por tipo
      if (filters.amountRange?.type && filters.amountRange.type !== 'all') {
        if (transaction.type !== filters.amountRange.type) {
          return false;
        }
      }

      // Filtro por status
      if (filters.status?.type && filters.status.type !== 'all') {
        if (transaction.type !== filters.status.type) {
          return false;
        }
      }

      // Filtro por categoria (status)
      if (filters.status?.hasCategory === true) {
        if (!transaction.category_id) {
          return false;
        }
      }

      // Filtro por notas (status)
      if (filters.status?.hasNotes === true) {
        if (!transaction.notes) {
          return false;
        }
      }

      return true;
    });
  }, [transactions, filters]);

  if (loading) {
    return (
      <Box>
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
        <Skeleton variant="rectangular" height={60} sx={{ mb: 1 }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Erro ao carregar transações: {error}
      </Alert>
    );
  }

  return (
    <Box>
      <AdvancedFilters
        onFiltersChange={updateFilters}
        onSaveFilters={(filters, name) => {
          console.log('Salvando filtros:', name, filters);
        }}
      />

      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">
          Transações ({filteredTransactions.length})
        </Typography>
        
        {filteredTransactions.length !== transactions?.length && (
          <Chip
            label={`Filtrado de ${transactions?.length || 0} transações`}
            color="primary"
            variant="outlined"
            size="small"
          />
        )}
      </Box>

      {filteredTransactions.length === 0 ? (
        <Alert severity="info">
          Nenhuma transação encontrada com os filtros aplicados.
        </Alert>
      ) : (
        <List>
          {filteredTransactions.map((transaction) => (
            <TransactionItem
              key={transaction.id}
              transaction={transaction}
              onEdit={onEditTransaction}
              onDelete={onDeleteTransaction}
            />
          ))}
        </List>
      )}
    </Box>
  );
};

export default FilteredTransactionsList;
```

## 🧪 **Testes dos Filtros**

### **Teste dos Componentes de Filtro**
```tsx
// src/components/filters/__tests__/AdvancedFilters.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from '../../../theme';
import AdvancedFilters from '../AdvancedFilters';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('AdvancedFilters', () => {
  test('renderiza botão de filtros avançados', () => {
    const onFiltersChange = jest.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    expect(screen.getByText('Filtros Avançados')).toBeInTheDocument();
  });

  test('mostra/esconde painel de filtros ao clicar no botão', () => {
    const onFiltersChange = jest.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    const filterButton = screen.getByText('Filtros Avançados');
    fireEvent.click(filterButton);
    
    expect(screen.getByText('Filtro por Período')).toBeInTheDocument();
    expect(screen.getByText('Filtro por Categorias')).toBeInTheDocument();
    
    fireEvent.click(filterButton);
    
    expect(screen.queryByText('Filtro por Período')).not.toBeInTheDocument();
  });

  test('chama onFiltersChange quando filtros são alterados', async () => {
    const onFiltersChange = jest.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    const filterButton = screen.getByText('Filtros Avançados');
    fireEvent.click(filterButton);
    
    // Expandir filtro de período
    const periodAccordion = screen.getByText('Filtro por Período');
    fireEvent.click(periodAccordion);
    
    // Selecionar período
    const periodSelect = screen.getByLabelText('Período');
    fireEvent.mouseDown(periodSelect);
    
    const todayOption = screen.getByText('Hoje');
    fireEvent.click(todayOption);
    
    await waitFor(() => {
      expect(onFiltersChange).toHaveBeenCalledWith(
        expect.objectContaining({
          dateRange: expect.objectContaining({
            period: 'today'
          })
        })
      );
    });
  });

  test('mostra contador de filtros ativos', () => {
    const onFiltersChange = jest.fn();
    const initialFilters = {
      dateRange: { period: 'today' },
      categories: ['cat-1', 'cat-2']
    };
    
    renderWithTheme(
      <AdvancedFilters 
        onFiltersChange={onFiltersChange}
        initialFilters={initialFilters}
      />
    );
    
    expect(screen.getByText('2')).toBeInTheDocument(); // 2 filtros ativos
  });

  test('limpa todos os filtros ao clicar em limpar', () => {
    const onFiltersChange = jest.fn();
    const initialFilters = {
      dateRange: { period: 'today' },
      categories: ['cat-1']
    };
    
    renderWithTheme(
      <AdvancedFilters 
        onFiltersChange={onFiltersChange}
        initialFilters={initialFilters}
      />
    );
    
    const clearButton = screen.getByText('Limpar Filtros');
    fireEvent.click(clearButton);
    
    expect(onFiltersChange).toHaveBeenCalledWith({});
  });
});
```

## 📋 **Checklist de Implementação - Status Atual**

### **Componentes de Filtro**
- ✅ DateRangeFilter (Filtro por Período) - Implementado parcialmente
- ✅ CategoryFilter (Filtro por Categorias) - Implementado parcialmente
- ⏳ AmountRangeFilter (Filtro por Valor)
- ⏳ StatusFilter (Filtro por Status)

### **Componente Principal**
- ⏳ AdvancedFilters (Componente consolidado)
- ⏳ Hook useAdvancedFilters (Gerenciamento de estado)

### **Integração**
- ⏳ Filtragem de transações
- ⏳ Persistência de filtros
- ⏳ Interface de usuário

### **Testes**
- ⏳ Testes unitários dos componentes
- ⏳ Testes de integração
- ⏳ Testes de usabilidade

### **Status Geral**
- ✅ Estrutura básica dos filtros implementada
- ✅ Componentes de filtro parcialmente implementados
- ⏳ Componente principal de filtros avançados pendente
- ⏳ Integração completa com transações pendente
- ⏳ Testes completos pendentes

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack  

Esta implementação de filtros avançados fornece uma experiência de usuário rica e flexível para análise e visualização de transações financeiras, com persistência de filtros e interface intuitiva. 