// src/contexts/CategoryContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface Category {
  id: string;
  name: string;
  icon: string;
  color: string;
  type: 'expense' | 'income';
}

interface CategoryContextData {
  expenseCategories: Category[];
  incomeCategories: Category[];
  getCategoriesByType: (type: 'expense' | 'income') => Category[];
}

const CategoryContext = createContext<CategoryContextData>({} as CategoryContextData);

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const expenseCategories: Category[] = [
    { id: '1', name: 'Food', icon: 'Fastfood', color: '#FF6384', type: 'expense' },
    { id: '2', name: 'Transport', icon: 'DirectionsCar', color: '#36A2EB', type: 'expense' },
  ];

  const incomeCategories: Category[] = [
    { id: '3', name: 'Salary', icon: 'MonetizationOn', color: '#4BC0C0', type: 'income' },
  ];

  const getCategoriesByType = (type: 'expense' | 'income') => {
    if (type === 'expense') {
      return expenseCategories;
    }
    return incomeCategories;
  };

  return (
    <CategoryContext.Provider value={{ expenseCategories, incomeCategories, getCategoriesByType }}>
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategories = () => useContext(CategoryContext);