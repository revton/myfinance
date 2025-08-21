// src/hooks/useCategories.ts
import { useContext, useMemo } from 'react';
import { useCategories as useCategoriesContext } from '../contexts/CategoryContext';
import { useTransactions } from '../contexts/TransactionContext';

interface CategorySummary {
  id: string;
  name: string;
  icon: string;
  color: string;
  amount: number;
  percentage: number;
}

export const useCategories = () => {
  const { categories, loading: categoriesLoading } = useCategoriesContext();
  const { transactions, loading: transactionsLoading } = useTransactions();
  
  const loading = categoriesLoading || transactionsLoading;
  
  const categorySummary = useMemo(() => {
    if (loading || !categories.length || !transactions.length) {
      return [];
    }
    
    // Calculate expenses by category
    const expenseTransactions = transactions.filter(t => t.type === 'expense');
    
    if (expenseTransactions.length === 0) {
      return [];
    }
    
    // Group transactions by category and calculate totals
    const categoryTotals: Record<string, number> = {};
    expenseTransactions.forEach(transaction => {
      const categoryId = transaction.category_id || 'uncategorized';
      if (!categoryTotals[categoryId]) {
        categoryTotals[categoryId] = 0;
      }
      categoryTotals[categoryId] += transaction.amount;
    });
    
    // Create summary array with category details
    const summary: CategorySummary[] = [];
    let totalExpenses = 0;
    
    Object.entries(categoryTotals).forEach(([categoryId, amount]) => {
      totalExpenses += amount;
      
      if (categoryId === 'uncategorized') {
        summary.push({
          id: 'uncategorized',
          name: 'Sem Categoria',
          icon: 'HelpOutline',
          color: '#999999',
          amount,
          percentage: 0 // Will be calculated below
        });
      } else {
        const category = categories.find(c => c.id === categoryId);
        if (category) {
          summary.push({
            id: category.id,
            name: category.name,
            icon: category.icon,
            color: category.color,
            amount,
            percentage: 0 // Will be calculated below
          });
        }
      }
    });
    
    // Calculate percentages
    summary.forEach(item => {
      item.percentage = totalExpenses > 0 ? (item.amount / totalExpenses) * 100 : 0;
    });
    
    // Sort by amount descending
    summary.sort((a, b) => b.amount - a.amount);
    
    return summary;
  }, [categories, transactions, loading]);
  
  return { categorySummary, loading };
};
