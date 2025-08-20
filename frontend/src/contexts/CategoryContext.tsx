// src/contexts/CategoryContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../lib/api';
import { API_BASE_URL, APP_CONFIG } from '../config';

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
  transaction_count?: number; // From backend CategoryWithTransactionCount
}

interface CategoryContextData {
  categories: Category[];
  loading: boolean;
  error: string | null;
  createCategory: (category: Omit<Category, 'id' | 'is_active' | 'is_default' | 'created_at' | 'updated_at' | 'transaction_count'>) => Promise<void>;
  updateCategory: (id: string, category: Partial<Category>) => Promise<void>;
  deleteCategory: (id: string) => Promise<void>;
  restoreCategory: (id: string) => Promise<void>;
  refreshCategories: () => void;
}

const CategoryContext = createContext<CategoryContextData>({} as CategoryContextData);

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Category[]>(`${APP_CONFIG.api.endpoints.categories}`);
      setCategories(response.data);
    } catch (err) {
      console.error('Error fetching categories:', err);
      setError('Failed to load categories.');
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const createCategory = async (categoryData: Omit<Category, 'id' | 'is_active' | 'is_default' | 'created_at' | 'updated_at' | 'transaction_count'>) => {
    try {
      await api.post(`${APP_CONFIG.api.endpoints.categories}`, categoryData);
      fetchCategories(); // Refresh list after creation
    } catch (err: any) {
      console.error('Error creating category:', err);
      throw new Error(err.response?.data?.detail || 'Failed to create category.');
    }
  };

  const updateCategory = async (id: string, categoryData: Partial<Category>) => {
    try {
      await api.put(`${APP_CONFIG.api.endpoints.categories}/${id}`, categoryData);
      fetchCategories(); // Refresh list after update
    } catch (err: any) {
      console.error('Error updating category:', err);
      throw new Error(err.response?.data?.detail || 'Failed to update category.');
    }c
  };

  const deleteCategory = async (id: string) => {
    try {
      await api.delete(`${APP_CONFIG.api.endpoints.categories}/${id}`);
      fetchCategories(); // Refresh list after deletion
    } catch (err: any) {
      console.error('Error deleting category:', err);
      throw new Error(err.response?.data?.detail || 'Failed to delete category.');
    }
  };

  const restoreCategory = async (id: string) => {
    try {
      await api.post(`${APP_CONFIG.api.endpoints.categories}/${id}/restore`);
      fetchCategories(); // Refresh list after restore
    } catch (err: any) {
      console.error('Error restoring category:', err);
      throw new Error(err.response?.data?.detail || 'Failed to restore category.');
    }
  };

  const refreshCategories = () => {
    fetchCategories();
  };

  return (
    <CategoryContext.Provider value={{ 
      categories, 
      loading, 
      error, 
      createCategory, 
      updateCategory, 
      deleteCategory, 
      restoreCategory,
      refreshCategories
    }}>
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategories = () => useContext(CategoryContext);