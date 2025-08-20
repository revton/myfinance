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
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3';
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
              renderInput={(params: any) => <TextField {...params} fullWidth />}
            />
            <DatePicker
              label="Data Final"
              value={filters.endDate || null}
              onChange={(date) => handleCustomDateChange('endDate', date)}
              renderInput={(params: any) => <TextField {...params} fullWidth />}
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