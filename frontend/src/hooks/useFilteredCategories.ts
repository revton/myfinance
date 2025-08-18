import { useCategories } from '../contexts/CategoryContext';
import type { Category } from '../types/category';

export const useFilteredCategories = (type: 'expense' | 'income') => {
  const { expenseCategories, incomeCategories } = useCategories();
  
  const filteredCategories = type === 'expense' ? expenseCategories : incomeCategories;
  
  return { filteredCategories };
};