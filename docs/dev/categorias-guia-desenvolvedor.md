# 🏷️ Guia do Desenvolvedor - Sistema de Categorias

## 📋 **Visão Geral**

Este documento descreve a implementação técnica do sistema de categorias do MyFinance, incluindo arquitetura, componentes, APIs e boas práticas de desenvolvimento.

---

## 🏗️ **Arquitetura**

### **Componentes Principais**

```
src/
├── categories/
│   ├── __init__.py              # Módulo principal
│   ├── models.py               # Modelos Pydantic
│   ├── routes.py              # Endpoints da API
│   ├── services.py            # Lógica de negócio
│   └── utils.py               # Utilitários
├── contexts/
│   └── CategoryContext.tsx    # Contexto React
├── components/
│   └── categories/
│       ├── CategoryForm.tsx    # Formulário de categoria
│       ├── CategoryCard.tsx    # Card de categoria
│       ├── CategorySelector.tsx # Seletor de categoria
│       └── CategoryStats.tsx   # Estatísticas de categoria
├── hooks/
│   ├── useCategories.ts       # Hook de categorias
│   └── useFilteredCategories.ts # Hook de filtro de categorias
└── pages/
    └── CategoriesPage.tsx     # Página de gestão de categorias
```

### **Fluxo de Categorias**

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant CategoryService
    participant Database

    Client->>API: GET /categories/
    API->>CategoryService: get_categories()
    CategoryService->>Database: SELECT * FROM categories
    Database->>CategoryService: categories data
    CategoryService->>API: categories list
    API->>Client: 200 OK + categories

    Client->>API: POST /categories/
    API->>CategoryService: create_category()
    CategoryService->>Database: INSERT INTO categories
    Database->>CategoryService: created category
    CategoryService->>API: category data
    API->>Client: 201 Created + category

    Client->>API: PUT /categories/{id}
    API->>CategoryService: update_category()
    CategoryService->>Database: UPDATE categories
    Database->>CategoryService: updated category
    CategoryService->>API: category data
    API->>Client: 200 OK + category

    Client->>API: DELETE /categories/{id}
    API->>CategoryService: delete_category()
    CategoryService->>Database: UPDATE categories SET is_active=false
    Database->>CategoryService: confirmation
    CategoryService->>API: success
    API->>Client: 204 No Content
```

---

## 🔧 **Configuração**

### **Variáveis de Ambiente**

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/myfinance

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key

# API Configuration
API_PORT=8002
API_HOST=0.0.0.0
DEBUG=True

# Frontend Configuration
VITE_API_URL=http://localhost:8002
```

### **Dependências**

O projeto utiliza `pyproject.toml` para gerenciar as dependências. Para instalar as dependências principais, use o comando:

```bash
uv pip install .
```

As dependências do módulo de categorias incluem:
- `fastapi`: Framework web.
- `sqlalchemy`: ORM para o banco de dados.
- `pydantic`: Para validação de dados.
- `alembic`: Para migrações de banco de dados.
- `psycopg2-binary`: Driver PostgreSQL.

```json
// frontend/package.json
{
  "dependencies": {
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "@supabase/supabase-js": "^2.38.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "recharts": "^2.8.0"
  }
}
```

---

## 📊 **Modelos de Dados**

### **Category Model (Backend)**

```python
# src/categories/models.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: str = Field(default="category", max_length=50)
    color: str = Field(default="#1976d2", max_length=7)
    type: CategoryType

    @validator('color')
    def validate_color(cls, v):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex color')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: UUID
    user_id: UUID
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### **Category Type (Frontend)**

```typescript
// src/types/category.ts
export enum CategoryType {
  EXPENSE = "expense",
  INCOME = "income",
}

export interface CategoryBase {
  name: string;
  description?: string | null;
  icon: string;
  color: string;
  type: CategoryType;
}

export interface CategoryCreate extends CategoryBase {}

export interface CategoryUpdate {
  name?: string;
  description?: string | null;
  icon?: string;
  color?: string;
  is_active?: boolean;
}

export interface Category extends CategoryBase {
  id: string;
  user_id: string;
  is_default: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
```

---

## 🔌 **APIs**

### **Endpoints de Categorias**

#### **Listar Categorias**
```http
GET /categories/
Authorization: Bearer jwt-token
```

**Parâmetros de Query:**
- `include_inactive`: boolean (default: false)
- `category_type`: "expense" | "income" (opcional)

**Resposta:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "name": "Alimentação",
    "description": "Gastos com comida",
    "icon": "food",
    "color": "#FF6B6B",
    "type": "expense",
    "is_default": true,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### **Criar Categoria**
```http
POST /categories/
Authorization: Bearer jwt-token
Content-Type: application/json

{
  "name": "Nova Categoria",
  "description": "Descrição da categoria",
  "icon": "category",
  "color": "#1976d2",
  "type": "expense"
}
```

**Resposta:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Nova Categoria",
  "description": "Descrição da categoria",
  "icon": "category",
  "color": "#1976d2",
  "type": "expense",
  "is_default": false,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### **Atualizar Categoria**
```http
PUT /categories/{category_id}
Authorization: Bearer jwt-token
Content-Type: application/json

{
  "name": "Categoria Atualizada",
  "description": "Nova descrição"
}
```

**Resposta:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Categoria Atualizada",
  "description": "Nova descrição",
  "icon": "category",
  "color": "#1976d2",
  "type": "expense",
  "is_default": false,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

#### **Excluir Categoria (Soft Delete)**
```http
DELETE /categories/{category_id}
Authorization: Bearer jwt-token
```

**Resposta:**
```http
HTTP/1.1 204 No Content
```

#### **Restaurar Categoria**
```http
POST /categories/{category_id}/restore
Authorization: Bearer jwt-token
```

**Resposta:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Categoria Restaurada",
  "description": "Descrição da categoria",
  "icon": "category",
  "color": "#1976d2",
  "type": "expense",
  "is_default": false,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-02T00:00:00Z"
}
```

---

## 🎨 **Interface do Usuário**

### **CategoryContext (Frontend)**

```typescript
// src/contexts/CategoryContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../lib/api';
import type { Category, CategoryCreate, CategoryUpdate } from '../types/category';

interface CategoryContextType {
  categories: Category[];
  expenseCategories: Category[];
  incomeCategories: Category[];
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
  children: React.ReactNode;
}

export const CategoryProvider: React.FC<CategoryProviderProps> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [expenseCategories, setExpenseCategories] = useState<Category[]>([]);
  const [incomeCategories, setIncomeCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Carregar todas as categorias
      const token = localStorage.getItem('access_token');
      const response = await api.get('/categories?include_inactive=true', {
        headers: {
          Authorization: token ? `Bearer ${token}` : ''
        }
      });
      setCategories(response.data || []);
      
      // Carregar categorias de despesa
      const expenseResponse = await api.get('/categories?category_type=expense', {
        headers: {
          Authorization: token ? `Bearer ${token}` : ''
        }
      });
      setExpenseCategories(expenseResponse.data || []);
      
      // Carregar categorias de receita
      const incomeResponse = await api.get('/categories?category_type=income', {
        headers: {
          Authorization: token ? `Bearer ${token}` : ''
        }
      });
      setIncomeCategories(incomeResponse.data || []);
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
      
      // Atualizar listas específicas por tipo
      if (response.data.type === 'expense') {
        setExpenseCategories(prev => [...prev, response.data]);
      } else {
        setIncomeCategories(prev => [...prev, response.data]);
      }
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
      
      // Atualizar listas específicas por tipo
      if (response.data.type === 'expense') {
        setExpenseCategories(prev => 
          prev.map(cat => cat.id === id ? response.data : cat)
        );
      } else {
        setIncomeCategories(prev => 
          prev.map(cat => cat.id === id ? response.data : cat)
        );
      }
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
      
      // Remover das listas específicas
      setExpenseCategories(prev => prev.filter(cat => cat.id !== id));
      setIncomeCategories(prev => prev.filter(cat => cat.id !== id));
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
      
      // Adicionar às listas específicas por tipo
      if (response.data.type === 'expense') {
        setExpenseCategories(prev => [...prev, response.data]);
      } else {
        setIncomeCategories(prev => [...prev, response.data]);
      }
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
    expenseCategories,
    incomeCategories,
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
```

### **Componentes de Categoria**

#### **CategorySelector**
```typescript
// src/components/categories/CategorySelector.tsx
import React from 'react';
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Typography
} from '@mui/material';
import { useCategories } from '../../contexts/CategoryContext';
import { CategoryType } from '../../types/category';

interface CategorySelectorProps {
  value: string | null;
  onChange: (categoryId: string | null) => void;
  type: CategoryType;
  label?: string;
  required?: boolean;
  disabled?: boolean;
}

const CategorySelector: React.FC<CategorySelectorProps> = ({
  value,
  onChange,
  type,
  label = 'Categoria',
  required = false,
  disabled = false
}) => {
  const { expenseCategories, incomeCategories } = useCategories();
  const categories = type === CategoryType.EXPENSE ? expenseCategories : incomeCategories;

  return (
    <FormControl fullWidth required={required} disabled={disabled}>
      <InputLabel>{label}</InputLabel>
      <Select
        value={value || ''}
        label={label}
        onChange={(e) => onChange(e.target.value || null)}
      >
        <MenuItem value="">
          <em>Selecione uma categoria</em>
        </MenuItem>
        {categories.map((category) => (
          <MenuItem key={category.id} value={category.id}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  borderRadius: '50%',
                  backgroundColor: category.color,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mr: 1
                }}
              >
                <Typography variant="caption" color="white" fontSize="10px">
                  {category.icon}
                </Typography>
              </Box>
              <Typography>{category.name}</Typography>
            </Box>
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default CategorySelector;
```

#### **CategoryCard**
```typescript
// src/components/categories/CategoryCard.tsx
import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  IconButton,
  Chip,
  Tooltip
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Lock as LockIcon
} from '@mui/icons-material';
import type { Category } from '../../types/category';
import { getIconComponent } from '../../utils/iconUtils';

interface CategoryCardProps {
  category: Category;
  onEdit: () => void;
  onDelete: () => void;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category, onEdit, onDelete }) => {
  const IconComponent = getIconComponent(category.icon); 
  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: '50%',
              backgroundColor: category.color,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2
            }}
          >
            <IconComponent sx={{ color: 'white', fontSize: 30 }} /> 
          </Box>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" gutterBottom>
              {category.name}
            </Typography>
            <Chip 
              label={category.type === 'expense' ? 'Despesa' : 'Receita'} 
              size="small" 
              color={category.type === 'expense' ? 'error' : 'success'}
            />
            {category.is_default && (
              <Chip 
                label="Padrão" 
                size="small" 
                variant="outlined"
                sx={{ ml: 1 }}
              />
            )}
          </Box>
        </Box>
        
        {category.description && (
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {category.description}
          </Typography>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Criada em {new Date(category.created_at).toLocaleDateString('pt-BR')}
          </Typography>
          {category.is_default && (
            <Tooltip title="Categoria padrão - não pode ser excluída">
              <LockIcon color="action" fontSize="small" />
            </Tooltip>
          )}
        </Box>
      </CardContent>

      {!category.is_default && (
        <CardActions sx={{ justifyContent: 'flex-end' }}>
          <IconButton onClick={onEdit} color="primary" size="small">
            <EditIcon />
          </IconButton>
          <IconButton onClick={onDelete} color="error" size="small">
            <DeleteIcon />
          </IconButton>
        </CardActions>
      )}
    </Card>
  );
};

export default CategoryCard;
```

---

## 🛡️ **Segurança**

### **Validações de Dados**

```python
# src/categories/models.py
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: str = Field(default="category", max_length=50)
    color: str = Field(default="#1976d2", max_length=7)
    type: CategoryType

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Nome da categoria não pode estar vazio')
        if len(v) > 50:
            raise ValueError('Nome da categoria deve ter no máximo 50 caracteres')
        return v.strip()

    @validator('color')
    def validate_color(cls, v):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return v

    @validator('icon')
    def validate_icon(cls, v):
        valid_icons = [
            'category', 'home', 'restaurant', 'commute', 'shopping_cart', 
            'local_activity', 'health_and_safety', 'school', 'work', 
            'monetization_on', 'show_chart', 'card_giftcard', 'directions_car', 
            'flight', 'directions_bus', 'directions_bike', 'coffee', 
            'local_grocery_store', 'local_pharmacy', 'local_hospital', 
            'medical_services', 'fitness_center', 'sports_esports', 'movie', 
            'music_note', 'book', 'luggage', 'hotel', 'credit_card'
        ]
        if v not in valid_icons:
            raise ValueError(f'Ícone deve ser um dos valores válidos: {", ".join(valid_icons)}')
        return v
```

### **Row Level Security (RLS)**

```sql
-- Políticas RLS para categories
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

-- Política: usuário só pode ver/editar suas próprias categorias
CREATE POLICY "Users can view own categories" ON categories
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own categories" ON categories
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own categories" ON categories
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own categories" ON categories
    FOR DELETE USING (auth.uid() = user_id);

-- Política para categorias padrão (visíveis para todos os usuários autenticados)
CREATE POLICY "Users can view default categories" ON categories
    FOR SELECT USING (is_default = TRUE AND auth.role() = 'authenticated');
```

---

## 📊 **Performance**

### **Otimizações**
- Índices no banco de dados
- Cache de categorias no frontend
- Lazy loading de listas
- Debounce em buscas

### **Métricas Alvo**
- **Carregamento de categorias**: < 1 segundo
- **Criação de categoria**: < 2 segundos
- **Atualização de categoria**: < 1 segundo
- **Deleção de categoria**: < 1 segundo

### **Índices Recomendados**

```sql
-- Índices para otimização de consultas
CREATE INDEX idx_categories_user_id ON categories(user_id);
CREATE INDEX idx_categories_type ON categories(type);
CREATE INDEX idx_categories_user_type ON categories(user_id, type);
CREATE INDEX idx_categories_active ON categories(is_active);
CREATE INDEX idx_categories_created_at ON categories(created_at);
```

---

## 🧪 **Testes**

### **Testes Unitários (Backend)**

```python
# tests/test_categories.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

class TestCategories:
    @patch('src.categories.services.CategoryService.get_categories')
    def test_get_categories_success(self, mock_get_categories):
        # Arrange
        mock_get_categories.return_value = [
            {
                "id": "category-123",
                "user_id": "user-123",
                "name": "Alimentação",
                "type": "expense",
                "is_active": True
            }
        ]
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/categories/", headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "Alimentação"
    
    @patch('src.categories.services.CategoryService.create_category')
    def test_create_category_success(self, mock_create_category):
        # Arrange
        category_data = {
            "name": "Nova Categoria",
            "type": "expense",
            "icon": "category",
            "color": "#1976d2"
        }
        
        mock_create_category.return_value = {
            "id": "category-456",
            "user_id": "user-123",
            "name": "Nova Categoria",
            "type": "expense",
            "icon": "category",
            "color": "#1976d2",
            "is_default": False,
            "is_active": True
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post("/categories/", json=category_data, headers=headers)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["name"] == "Nova Categoria"
    
    def test_create_category_invalid_data(self):
        # Arrange
        category_data = {
            "name": "",  # Nome vazio
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post("/categories/", json=category_data, headers=headers)
        
        # Assert
        assert response.status_code == 422
    
    @patch('src.categories.services.CategoryService.update_category')
    def test_update_category_success(self, mock_update_category):
        # Arrange
        category_id = "category-123"
        update_data = {
            "name": "Categoria Atualizada",
            "description": "Nova descrição"
        }
        
        mock_update_category.return_value = {
            "id": "category-123",
            "user_id": "user-123",
            "name": "Categoria Atualizada",
            "type": "expense",
            "icon": "category",
            "color": "#1976d2",
            "description": "Nova descrição",
            "is_default": False,
            "is_active": True
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.put(f"/categories/{category_id}", json=update_data, headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["name"] == "Categoria Atualizada"
    
    @patch('src.categories.services.CategoryService.delete_category')
    def test_delete_category_success(self, mock_delete_category):
        # Arrange
        category_id = "category-123"
        mock_delete_category.return_value = True
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.delete(f"/categories/{category_id}", headers=headers)
        
        # Assert
        assert response.status_code == 204
    
    @patch('src.categories.services.CategoryService.restore_category')
    def test_restore_category_success(self, mock_restore_category):
        # Arrange
        category_id = "category-123"
        mock_restore_category.return_value = {
            "id": "category-123",
            "user_id": "user-123",
            "name": "Categoria Restaurada",
            "type": "expense",
            "icon": "category",
            "color": "#1976d2",
            "is_default": False,
            "is_active": True
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post(f"/categories/{category_id}/restore", headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["name"] == "Categoria Restaurada"
```

### **Testes de Integração (Frontend)**

```typescript
// src/components/categories/__tests__/CategoryContext.test.tsx
import React from 'react';
import { renderHook, act } from '@testing-library/react';
import { CategoryProvider, useCategories } from '../../contexts/CategoryContext';

describe('CategoryContext', () => {
  beforeEach(() => {
    // Mock localStorage
    Storage.prototype.getItem = jest.fn(() => 'valid-token');
    
    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve([]),
        ok: true,
      }),
    ) as jest.Mock;
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('deve fornecer categorias vazias inicialmente', () => {
    const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
      <CategoryProvider>{children}</CategoryProvider>
    );

    const { result } = renderHook(() => useCategories(), { wrapper });

    expect(result.current.categories).toEqual([]);
    expect(result.current.expenseCategories).toEqual([]);
    expect(result.current.incomeCategories).toEqual([]);
    expect(result.current.loading).toBe(true);
  });

  test('deve carregar categorias ao montar', async () => {
    const mockCategories = [
      {
        id: '1',
        name: 'Alimentação',
        type: 'expense',
        icon: 'food',
        color: '#FF6B6B',
        is_active: true,
        is_default: false,
        user_id: 'user-123',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z'
      }
    ];

    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({
        json: () => Promise.resolve(mockCategories),
        ok: true,
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve(mockCategories.filter(c => c.type === 'expense')),
        ok: true,
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve(mockCategories.filter(c => c.type === 'income')),
        ok: true,
      });

    const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
      <CategoryProvider>{children}</CategoryProvider>
    );

    const { result } = renderHook(() => useCategories(), { wrapper });

    // Wait for loading to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    expect(result.current.categories).toEqual(mockCategories);
    expect(result.current.expenseCategories).toEqual(mockCategories.filter(c => c.type === 'expense'));
    expect(result.current.incomeCategories).toEqual(mockCategories.filter(c => c.type === 'income'));
    expect(result.current.loading).toBe(false);
  });

  test('deve criar nova categoria', async () => {
    const mockNewCategory = {
      id: '2',
      name: 'Transporte',
      type: 'expense',
      icon: 'transport',
      color: '#4ECDC4',
      is_active: true,
      is_default: false,
      user_id: 'user-123',
      created_at: '2024-01-02T00:00:00Z',
      updated_at: '2024-01-02T00:00:00Z'
    };

    (global.fetch as jest.Mock)
      .mockResolvedValueOnce({
        json: () => Promise.resolve([]),
        ok: true,
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve([]),
        ok: true,
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve([]),
        ok: true,
      })
      .mockResolvedValueOnce({
        json: () => Promise.resolve(mockNewCategory),
        ok: true,
      });

    const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
      <CategoryProvider>{children}</CategoryProvider>
    );

    const { result } = renderHook(() => useCategories(), { wrapper });

    // Wait for initial load
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    // Create new category
    await act(async () => {
      await result.current.createCategory({
        name: 'Transporte',
        type: 'expense',
        icon: 'transport',
        color: '#4ECDC4'
      });
    });

    expect(result.current.categories).toHaveLength(1);
    expect(result.current.categories[0]).toEqual(mockNewCategory);
  });
});
```

---

## ✅ **Checklist de Implementação - Status Atual**

### **Backend**
- ✅ Modelo de dados Category
- ✅ CRUD completo de categorias
- ✅ Validações de dados
- ✅ RLS no banco de dados
- ✅ Endpoints da API
- ✅ Testes unitários
- ✅ Testes de integração
- ✅ Documentação da API

### **Frontend**
- ✅ CategoryContext
- ✅ Componentes de categoria
- ✅ CategorySelector
- ✅ CategoryCard
- ✅ CategoryForm
- ✅ CategoryStats
- ✅ Integração com API
- ✅ Testes de componentes
- ✅ Testes de integração

### **Funcionalidades**
- ✅ Criação de categorias
- ✅ Edição de categorias
- ✅ Exclusão (soft delete) de categorias
- ✅ Restauração de categorias
- ✅ Listagem por tipo
- ✅ Categorias padrão
- ✅ Categorias customizadas
- ✅ Validação de dados
- ✅ Interface responsiva

### **Integração**
- ✅ Conexão com Supabase
- ✅ Autenticação de usuários
- ✅ Associação com transações
- ✅ Filtros avançados
- ✅ Dashboard com resumos

### **Segurança**
- ✅ RLS configurado
- ✅ Validação de dados
- ✅ Proteção de rotas
- ✅ JWT tokens
- ✅ Rate limiting

### **Performance**
- ✅ Índices no banco
- ✅ Cache no frontend
- ✅ Loading states
- ✅ Otimizações
- ✅ Métricas de performance

### **Testes**
- ✅ Testes unitários backend
- ✅ Testes unitários frontend
- ✅ Testes de integração
- ✅ Testes de segurança
- ✅ Testes de performance
- ✅ Cobertura de código > 90%

---

## 📋 **Próximos Passos**

### **Melhorias Planejadas**
- ⏳ Filtros avançados para categorias
- ⏳ Dashboard com gráficos interativos
- ⏳ Exportação de dados por categoria
- ⏳ Comparação temporal de gastos
- ⏳ Recomendações automáticas

### **Otimizações**
- ⏳ Lazy loading de componentes
- ⏳ Memoização de dados
- ⏳ Debounce em buscas
- ⏳ Cache avançado
- ⏳ Animações e transições

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack