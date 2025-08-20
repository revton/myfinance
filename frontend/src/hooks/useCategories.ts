// src/hooks/useCategories.ts
import { useState } from 'react';

export const useCategories = () => {
  const [loading, setLoading] = useState(true);

  const categorySummary = [
    { id: '1', name: 'Food', icon: 'Fastfood', color: '#FF6384', amount: 500, percentage: 50 },
    { id: '2', name: 'Transport', icon: 'DirectionsCar', color: '#36A2EB', amount: 200, percentage: 20 },
    { id: '3', name: 'Shopping', icon: 'ShoppingCart', color: '#FFCE56', amount: 150, percentage: 15 },
    { id: '4', name: 'Health', icon: 'Favorite', color: '#4BC0C0', amount: 100, percentage: 10 },
    { id: '5', name: 'Other', icon: 'MoreHoriz', color: '#9966FF', amount: 50, percentage: 5 },
  ];

  setTimeout(() => setLoading(false), 1000);

  return { categorySummary, loading };
};
