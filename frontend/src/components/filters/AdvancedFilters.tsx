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

// Import filter types
import type { DateRangeFilters } from './DateRangeFilter';
import type { AmountRangeFilters } from './AmountRangeFilter';
import type { StatusFilters } from './StatusFilter';

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
              <Typography>Filtro de Tipo de Transação</Typography>
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