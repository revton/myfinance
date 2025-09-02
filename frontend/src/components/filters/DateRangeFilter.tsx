// src/components/filters/DateRangeFilter.tsx
import React, { useState, useEffect, useRef } from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Chip,
  Typography,
  Tooltip
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFnsV3';
import { ptBR } from 'date-fns/locale';
import { CalendarMonth, CalendarToday, DateRange } from '@mui/icons-material';

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
  
  // Ref to track the previous initialFilters value
  const prevInitialFiltersRef = useRef(initialFilters);

  // Reset filters when initialFilters changes (e.g., when filters are cleared)
  useEffect(() => {
    // Only reset if initialFilters has actually changed
    if (JSON.stringify(initialFilters) !== JSON.stringify(prevInitialFiltersRef.current)) {
      setFilters(initialFilters || {
        period: 'month'
      });
      prevInitialFiltersRef.current = initialFilters;
    }
  }, [initialFilters]);

  const handlePeriodChange = (period: string) => {
    const newFilters = { ...filters, period: period as any };
    
    // Calcular datas baseadas no período
    const now = new Date();
    switch (period) {
      case 'today':
        const todayStart = new Date(now);
        todayStart.setHours(0, 0, 0, 0); // Start of day
        const todayEnd = new Date(now);
        todayEnd.setHours(23, 59, 59, 999); // End of day
        newFilters.startDate = todayStart;
        newFilters.endDate = todayEnd;
        break;
      case 'week':
        const weekStart = new Date(now);
        weekStart.setDate(now.getDate() - now.getDay());
        weekStart.setHours(0, 0, 0, 0); // Start of week
        const weekEnd = new Date(now);
        weekEnd.setHours(23, 59, 59, 999); // End of current day
        newFilters.startDate = weekStart;
        newFilters.endDate = weekEnd;
        break;
      case 'month':
        const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
        monthStart.setHours(0, 0, 0, 0); // Start of month
        const monthEnd = new Date(now);
        monthEnd.setHours(23, 59, 59, 999); // End of current day
        newFilters.startDate = monthStart;
        newFilters.endDate = monthEnd;
        break;
      case 'quarter':
        const quarter = Math.floor(now.getMonth() / 3);
        const quarterStart = new Date(now.getFullYear(), quarter * 3, 1);
        quarterStart.setHours(0, 0, 0, 0); // Start of quarter
        const quarterEnd = new Date(now);
        quarterEnd.setHours(23, 59, 59, 999); // End of current day
        newFilters.startDate = quarterStart;
        newFilters.endDate = quarterEnd;
        break;
      case 'year':
        const yearStart = new Date(now.getFullYear(), 0, 1);
        yearStart.setHours(0, 0, 0, 0); // Start of year
        const yearEnd = new Date(now);
        yearEnd.setHours(23, 59, 59, 999); // End of current day
        newFilters.startDate = yearStart;
        newFilters.endDate = yearEnd;
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
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <DateRange color="primary" />
          <Typography variant="h6">Filtro por Período</Typography>
        </Box>
        
        <FormControl fullWidth>
          <InputLabel>Período</InputLabel>
          <Select
            value={filters.period}
            label="Período"
            onChange={(e) => handlePeriodChange(e.target.value)}
            startAdornment={filters.period === 'custom' ? <DateRange color="action" sx={{ ml: 1 }} /> : <CalendarMonth color="action" sx={{ ml: 1 }} />}
          >
            <MenuItem value="today">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarToday fontSize="small" />
                <span>Hoje</span>
              </Box>
            </MenuItem>
            <MenuItem value="week">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarMonth fontSize="small" />
                <span>Esta Semana</span>
              </Box>
            </MenuItem>
            <MenuItem value="month">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarMonth fontSize="small" />
                <span>Este Mês</span>
              </Box>
            </MenuItem>
            <MenuItem value="quarter">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarMonth fontSize="small" />
                <span>Este Trimestre</span>
              </Box>
            </MenuItem>
            <MenuItem value="year">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <CalendarMonth fontSize="small" />
                <span>Este Ano</span>
              </Box>
            </MenuItem>
            <MenuItem value="custom">
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <DateRange fontSize="small" />
                <span>Personalizado</span>
              </Box>
            </MenuItem>
          </Select>
        </FormControl>

        {filters.period === 'custom' && (
          <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
            <Tooltip title="Selecione a data inicial do período" arrow placement="top">
              <Box sx={{ width: '100%' }}>
                <DatePicker
                  label="Data Inicial"
                  value={filters.startDate || null}
                  onChange={(date) => handleCustomDateChange('startDate', date)}
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      InputProps: {
                        startAdornment: (
                          <CalendarToday color="action" sx={{ mr: 1 }} />
                        ),
                      },
                    },
                  }}
                />
              </Box>
            </Tooltip>
            <Tooltip title="Selecione a data final do período" arrow placement="top">
              <Box sx={{ width: '100%' }}>
                <DatePicker
                  label="Data Final"
                  value={filters.endDate || null}
                  onChange={(date) => handleCustomDateChange('endDate', date)}
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      InputProps: {
                        startAdornment: (
                          <CalendarToday color="action" sx={{ mr: 1 }} />
                        ),
                      },
                    },
                  }}
                />
              </Box>
            </Tooltip>
          </Box>
        )}

        {(filters.startDate || filters.endDate) && (
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
            <Typography variant="body2" color="text.secondary" sx={{ width: '100%', mb: 0.5 }}>
              Período selecionado:
            </Typography>
            {filters.startDate && (
              <Tooltip title="Remover data inicial" arrow>
                <Chip
                  icon={<CalendarToday fontSize="small" />}
                  label={`De: ${filters.startDate.toLocaleDateString('pt-BR')}`}
                  onDelete={() => handleCustomDateChange('startDate', null)}
                  color="primary"
                  variant="outlined"
                  sx={{ borderRadius: 1.5 }}
                />
              </Tooltip>
            )}
            {filters.endDate && (
              <Tooltip title="Remover data final" arrow>
                <Chip
                  icon={<CalendarToday fontSize="small" />}
                  label={`Até: ${filters.endDate.toLocaleDateString('pt-BR')}`}
                  onDelete={() => handleCustomDateChange('endDate', null)}
                  color="primary"
                  variant="outlined"
                  sx={{ borderRadius: 1.5 }}
                />
              </Tooltip>
            )}
          </Box>
        )}
      </Box>
    </LocalizationProvider>
  );
};

export default DateRangeFilter;