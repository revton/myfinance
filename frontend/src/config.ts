// Configuração da API
export const API_BASE_URL = process.env.VITE_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://myfinance-backend.onrender.com' 
    : 'http://localhost:8002');

// Configuração da aplicação
export const APP_CONFIG = {
  name: 'MyFinance',
  version: '1.0.0',
  api: {
    baseUrl: API_BASE_URL,
    endpoints: {
      transactions: '/transactions',
      categories: '/categories',
      health: '/health',
    },
  },
  features: {
    enableNotifications: true,
    enableOfflineMode: false,
  },
} as const;

// Tipos de transação
export const TRANSACTION_TYPES = {
  INCOME: 'income',
  EXPENSE: 'expense',
} as const;

// Configuração de validação
export const VALIDATION_CONFIG = {
  minAmount: 0.01,
  maxAmount: 999999.99,
  maxDescriptionLength: 255,
} as const; 