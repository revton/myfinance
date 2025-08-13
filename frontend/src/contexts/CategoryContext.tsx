import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import { Category, CategoryCreate, CategoryUpdate } from '../types/category';

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

      const { data, error: fetchError } = await supabase
        .from('categories')
        .select('*')
        .order('name');

      if (fetchError) throw fetchError;

      setCategories(data || []);
    } catch (err) {
      setError('Erro ao carregar categorias');
      console.error('Erro ao buscar categorias:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  const createCategory = async (categoryData: CategoryCreate) => {
    try {
      setError(null);

      const { data, error: createError } = await supabase
        .from('categories')
        .insert([categoryData])
        .select()
        .single();

      if (createError) throw createError;

      setCategories(prev => [...prev, data]);
    } catch (err) {
      setError('Erro ao criar categoria');
      throw err;
    }
  };

  const updateCategory = async (id: string, categoryData: CategoryUpdate) => {
    try {
      setError(null);

      const { data, error: updateError } = await supabase
        .from('categories')
        .update(categoryData)
        .eq('id', id)
        .select()
        .single();

      if (updateError) throw updateError;

      setCategories(prev => 
        prev.map(cat => cat.id === id ? data : cat)
      );
    } catch (err) {
      setError('Erro ao atualizar categoria');
      throw err;
    }
  };

  const deleteCategory = async (id: string) => {
    try {
      setError(null);

      const { error: deleteError } = await supabase
        .from('categories')
        .update({ is_active: false })
        .eq('id', id);

      if (deleteError) throw deleteError;

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

      const { error: restoreError } = await supabase
        .from('categories')
        .update({ is_active: true })
        .eq('id', id);

      if (restoreError) throw restoreError;

      setCategories(prev => 
        prev.map(cat => cat.id === id ? { ...cat, is_active: true } : cat)
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
