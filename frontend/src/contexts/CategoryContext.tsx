import React, { createContext, useContext } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';
import { APP_CONFIG } from '../config';
import * as Sentry from '@sentry/react';

interface Category {
  id: string;
  name: string;
  description?: string;
  icon: string;
  color: string;
  type: 'expense' | 'income';
  is_active: boolean;
  is_default: boolean;
  created_at: string;
  updated_at: string;
  transaction_count?: number;
}

interface CategoryContextData {
  categories: Category[];
  isLoading: boolean;
  error: Error | null;
  createCategory: (category: Omit<Category, 'id' | 'is_active' | 'is_default' | 'created_at' | 'updated_at' | 'transaction_count'>) => Promise<void>;
  updateCategory: (id: string, category: Partial<Category>) => Promise<void>;
  deleteCategory: (id: string) => Promise<void>;
  restoreCategory: (id: string) => Promise<void>;
  refetchCategories: () => void;
  getCategoriesByType: (type: 'expense' | 'income') => Category[];
}

const CategoryContext = createContext<CategoryContextData>({} as CategoryContextData);

const fetchCategories = async (): Promise<Category[]> => {
  const response = await api.get<Category[]>(`${APP_CONFIG.api.endpoints.categories}`);
  return response.data;
};

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = useQueryClient();

  const { data: categories = [], isLoading, error, refetch } = useQuery<Category[], Error>({
    queryKey: ['categories'],
    queryFn: fetchCategories,
  });

  const mutationOptions = {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
    },
    onError: (err: any) => {
      console.error(err);
      Sentry.captureException(err);
      throw new Error(err.response?.data?.detail || 'An error occurred');
    },
  };

  const createCategoryMutation = useMutation({
    mutationFn: (categoryData: Omit<Category, 'id' | 'is_active' | 'is_default' | 'created_at' | 'updated_at' | 'transaction_count'>) =>
      api.post(`${APP_CONFIG.api.endpoints.categories}`, categoryData),
    ...mutationOptions,
  });

  const updateCategoryMutation = useMutation({
    mutationFn: ({ id, categoryData }: { id: string; categoryData: Partial<Category> }) =>
      api.put(`${APP_CONFIG.api.endpoints.categories}/${id}`, categoryData),
    ...mutationOptions,
  });

  const deleteCategoryMutation = useMutation({
    mutationFn: (id: string) => api.delete(`${APP_CONFIG.api.endpoints.categories}/${id}`),
    ...mutationOptions,
  });

  const restoreCategoryMutation = useMutation({
    mutationFn: (id: string) => api.post(`${APP_CONFIG.api.endpoints.categories}/${id}/restore`),
    ...mutationOptions,
  });

  const getCategoriesByType = (type: 'expense' | 'income') => {
    return categories.filter(cat => cat.type === type);
  };

  return (
    <CategoryContext.Provider
      value={{
        categories,
        isLoading,
        error,
        createCategory: createCategoryMutation.mutateAsync,
        updateCategory: (id, data) => updateCategoryMutation.mutateAsync({ id, categoryData: data }),
        deleteCategory: deleteCategoryMutation.mutateAsync,
        restoreCategory: restoreCategoryMutation.mutateAsync,
        refetchCategories: refetch,
        getCategoriesByType,
      }}
    >
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategories = () => useContext(CategoryContext);