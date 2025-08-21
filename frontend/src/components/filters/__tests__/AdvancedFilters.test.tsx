// src/components/filters/__tests__/AdvancedFilters.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from '../../../theme';
import AdvancedFilters from '../AdvancedFilters';
import { vi } from 'vitest';
import { useCategories } from '../../../contexts/CategoryContext';

// Mock @mui/icons-material
vi.mock('@mui/icons-material', () => ({
  FilterList: () => <div data-testid="filter-list-icon" />,
  Clear: () => <div data-testid="clear-icon" />,
  Save: () => <div data-testid="save-icon" />,
  ExpandMore: () => <div data-testid="expand-more-icon" />,
}));

// Mock filter components
vi.mock('../DateRangeFilter', () => ({
  __esModule: true,
  default: ({ onFilterChange, initialFilters }: any) => (
    <div data-testid="date-range-filter">
      <button onClick={() => onFilterChange({ period: 'today' })}>Filter</button>
    </div>
  ),
}));

vi.mock('../../../contexts/CategoryContext');

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('AdvancedFilters', () => {
  beforeEach(() => {
    (useCategories as jest.Mock).mockReturnValue({
      getCategoriesByType: (type: string) => {
        if (type === 'expense') {
          return [{ id: '1', name: 'Food', type: 'expense' }];
        }
        return [{ id: '2', name: 'Salary', type: 'income' }];
      },
    });
  });

  test('renderiza botão de filtros avançados', () => {
    const onFiltersChange = vi.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    expect(screen.getAllByText('Filtros Avançados').length).toBeGreaterThan(0);
  });

  test('mostra/esconde painel de filtros ao clicar no botão', async () => {
    const onFiltersChange = vi.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    const filterButton = screen.getAllByText('Filtros Avançados')[0];
    fireEvent.click(filterButton);
    
    expect(screen.getByTestId('date-range-filter')).toBeInTheDocument();
    
    fireEvent.click(filterButton);
    
    await waitFor(() => {
      expect(screen.queryByTestId('date-range-filter')).not.toBeVisible();
    });
  });

  test('chama onFiltersChange quando filtros são alterados', async () => {
    const onFiltersChange = vi.fn();
    
    renderWithTheme(
      <AdvancedFilters onFiltersChange={onFiltersChange} />
    );
    
    const filterButton = screen.getAllByText('Filtros Avançados')[0];
    fireEvent.click(filterButton);

    const nestedFilterButton = screen.getByText('Filter');
    fireEvent.click(nestedFilterButton);
    
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
    const onFiltersChange = vi.fn();
    const initialFilters = {
      dateRange: { period: 'custom', startDate: new Date(), endDate: new Date() },
      categories: ['cat-1', 'cat-2'],
      amountRange: { minAmount: 100, maxAmount: 200, type: 'all' as const },
      status: { type: 'expense', status: 'all', hasCategory: null, hasNotes: null },
    };
    
    renderWithTheme(
      <AdvancedFilters 
        onFiltersChange={onFiltersChange}
        initialFilters={initialFilters}
      />
    );
    
    expect(screen.getByText('4')).toBeInTheDocument(); // 4 filtros ativos
  });

  test('limpa todos os filtros ao clicar em limpar', () => {
    const onFiltersChange = vi.fn();
    const initialFilters = {
      dateRange: { period: 'today', startDate: new Date(), endDate: new Date() },
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