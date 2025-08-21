// src/hooks/useAdvancedFilters.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { useLocalStorage } from './useLocalStorage';

// Import filter types from the component
import type { CombinedFilters, SavedFilter } from '../components/filters/AdvancedFilters';

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
  
  // Ref to track if we've already loaded filters from localStorage
  const hasLoadedRef = useRef(false);

  const updateFilters = useCallback((newFilters: CombinedFilters) => {
    setFilters(newFilters);
    onFiltersChange?.(newFilters);
  }, [onFiltersChange]);

  const saveFilters = useCallback((filtersToSave: CombinedFilters, name: string) => {
    const newSavedFilter: SavedFilter = {
      id: Date.now().toString(),
      name,
      filters: filtersToSave
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

  // Persist filters ativos
  useEffect(() => {
    if (Object.keys(filters).length > 0) {
      localStorage.setItem(`${storageKey}-active`, JSON.stringify(filters));
    } else {
      localStorage.removeItem(`${storageKey}-active`);
    }
  }, [filters, storageKey]);

  // Carregar filtros ativos ao inicializar (apenas uma vez)
  useEffect(() => {
    if (!hasLoadedRef.current) {
      const savedActiveFilters = localStorage.getItem(`${storageKey}-active`);
      if (savedActiveFilters) {
        try {
          const parsedFilters = JSON.parse(savedActiveFilters);
          setFilters(parsedFilters);
        } catch (error) {
          console.error('Erro ao carregar filtros salvos:', error);
        }
      }
      hasLoadedRef.current = true;
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