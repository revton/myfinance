import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../lib/api';
import type { Category, CategoryCreate, CategoryUpdate } from '../types/category';

interface CategoryContextType {
  categories: Category[];
  loading: boolean;
  error: string | null;
  createCategory: (data: CategoryCreate) => Promise<void>;
  updateCategory: (id: string, data: CategoryUpdate) => Promise<void>;
  deleteCategory: (id: string) => Promise<void>;
  restoreCategory: (id: string) => Promise<void>;
  getCategoriesByType: (type: 'expense' | 'income') => Category[];
  getCategoryById: (id: string) => Category | undefined;
}

const CategoryContext = createContext<CategoryContextType | undefined>(undefined);

export const useCategories = () => {
  const context = useContext(CategoryContext);
  if (context === undefined) {
    throw new Error('useCategories must be used within a CategoryProvider');
  }
  return context;
};

interface CategoryProviderProps {
  children: ReactNode;
}

export const CategoryProvider: React.FC<CategoryProviderProps> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const token = localStorage.getItem('access_token'); // Get token here
      const response = await api.get('/categories?include_inactive=true', {
        headers: {
          Authorization: token ? `Bearer ${token}` : '' // Set header explicitly
        }
      });
      setCategories(response.data || []);
    } catch (err) {
      setError('Erro ao carregar categorias');
      console.error('Erro ao buscar categorias:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchCategories();
    }
  }, [localStorage.getItem('access_token')]);

  const createCategory = async (categoryData: CategoryCreate) => {
    try {
      setError(null);
      const response = await api.post('/categories/', categoryData);
      setCategories(prev => [...prev, response.data]);
    } catch (err) {
      setError('Erro ao criar categoria');
      throw err;
    }
  };

  const updateCategory = async (id: string, categoryData: CategoryUpdate) => {
    try {
      setError(null);
      const response = await api.put(`/categories/${id}`, categoryData);
      setCategories(prev => 
        prev.map(cat => cat.id === id ? response.data : cat)
      );
    } catch (err) {
      setError('Erro ao atualizar categoria');
      throw err;
    }
  };

  const deleteCategory = async (id: string) => {
    try {
      setError(null);
      await api.delete(`/categories/${id}`);
      setCategories(prev => 
        prev.map(cat => cat.id === id ? { ...cat, is_active: false } : cat)
      );
    } catch (err) {
      setError('Erro ao excluir categoria');
      throw err;
    }
  };

  const restoreCategory = async (id: string) => {
    try {
      setError(null);
      const response = await api.post(`/categories/${id}/restore`);
      setCategories(prev => 
        prev.map(cat => cat.id === id ? response.data : cat)
      );
    } catch (err) {
      setError('Erro ao restaurar categoria');
      throw err;
    }
  };

  const getCategoriesByType = (type: 'expense' | 'income') => {
    return categories.filter(cat => cat.type === type && cat.is_active);
  };

  const getCategoryById = (id: string) => {
    return categories.find(cat => cat.id === id);
  };

  const value = {
    categories,
    loading,
    error,
    createCategory,
    updateCategory,
    deleteCategory,
    restoreCategory,
    getCategoriesByType,
    getCategoryById,
  };

  return (
    <CategoryContext.Provider value={value}>
      {children}
    </CategoryContext.Provider>
  );
};
