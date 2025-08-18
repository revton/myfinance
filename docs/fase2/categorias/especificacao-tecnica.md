# 🏷️ Sistema de Categorias - Especificação Técnica

## 📋 **Visão Geral**

O sistema de categorias do MyFinance permitirá organizar transações financeiras de forma intuitiva, facilitando o controle e análise dos gastos e receitas.

### 🎯 **Objetivos**
- Categorização automática e manual de transações
- Categorias padrão pré-definidas
- Categorias customizadas por usuário
- Interface intuitiva para gestão
- Filtros e busca por categoria

---

## 🏗️ **Arquitetura**

### **Backend (FastAPI)**
```python
# Estrutura de categorias
├── src/
│   ├── categories/
│   │   ├── __init__.py
│   │   ├── models.py           # Modelos de categoria
│   │   ├── routes.py           # Endpoints CRUD
│   │   ├── services.py         # Lógica de negócio
│   │   └── utils.py            # Utilitários
│   └── main.py
```

### **Frontend (React)**
```typescript
// Estrutura de categorias
├── src/
│   ├── categories/
│   │   ├── CategoryContext.tsx # Contexto de categorias
│   │   ├── CategoryService.ts  # Serviços de API
│   │   ├── types.ts            # Tipos TypeScript
│   │   └── utils.ts            # Utilitários
│   ├── components/
│   │   ├── CategoryForm.tsx    # Formulário de categoria
│   │   ├── CategoryList.tsx    # Lista de categorias
│   │   ├── CategorySelect.tsx  # Seletor de categoria
│   │   └── CategoryIcon.tsx    # Ícone de categoria
│   └── pages/
│       └── CategoriesPage.tsx  # Página de gestão
```

---

## 🔧 **Implementação Técnica**

### **1. Modelo de Dados**

#### **Tabela Categories**
```sql
-- Tabela de categorias
CREATE TABLE categories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50) DEFAULT 'category',
    color VARCHAR(7) DEFAULT '#1976d2', -- Hex color
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT unique_user_category_name UNIQUE (user_id, name),
    CONSTRAINT valid_color_format CHECK (color ~ '^#[0-9A-Fa-f]{6}$')
);

-- Índices para performance
CREATE INDEX idx_categories_user_id ON categories(user_id);
CREATE INDEX idx_categories_is_default ON categories(is_default);
CREATE INDEX idx_categories_is_active ON categories(is_active);

-- RLS (Row Level Security)
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

-- Políticas RLS
CREATE POLICY "Users can view own categories" ON categories
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own categories" ON categories
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own categories" ON categories
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own categories" ON categories
    FOR DELETE USING (auth.uid() = user_id);

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_categories_updated_at 
    BEFORE UPDATE ON categories 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

#### **Tabela Transactions (Atualizada)**
```sql
-- Adicionar category_id às transações
ALTER TABLE transactions ADD COLUMN category_id UUID REFERENCES categories(id);

-- Índice para performance
CREATE INDEX idx_transactions_category_id ON transactions(category_id);

-- Política RLS atualizada para incluir categoria
CREATE POLICY "Users can view own transactions with categories" ON transactions
    FOR ALL USING (
        auth.uid() = user_id AND 
        (category_id IS NULL OR category_id IN (
            SELECT id FROM categories WHERE user_id = auth.uid()
        ))
    );
```

### **2. Modelos Pydantic**

#### **Category Models**
```python
# src/categories/models.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import re

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: str = Field(default="category", max_length=50)
    color: str = Field(default="#1976d2", max_length=7)
    
    @validator('color')
    def validate_color(cls, v):
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex color')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=7)
    is_active: Optional[bool] = None
    
    @validator('color')
    def validate_color(cls, v):
        if v is not None and not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be a valid hex color')
        return v

class CategoryResponse(CategoryBase):
    id: UUID
    user_id: UUID
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CategoryWithTransactionCount(CategoryResponse):
    transaction_count: int
```

### **3. Endpoints da API**

#### **CRUD de Categorias**
```python
# src/categories/routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.database import get_db
from .models import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithTransactionCount
from .services import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryWithTransactionCount])
async def get_categories(
    include_inactive: bool = Query(False, description="Include inactive categories"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lista todas as categorias do usuário"""
    service = CategoryService(db, current_user.id)
    return service.get_categories(include_inactive=include_inactive)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtém uma categoria específica"""
    service = CategoryService(db, current_user.id)
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cria uma nova categoria"""
    service = CategoryService(db, current_user.id)
    return service.create_category(category_data)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Atualiza uma categoria"""
    service = CategoryService(db, current_user.id)
    category = service.update_category(category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Deleta uma categoria (soft delete)"""
    service = CategoryService(db, current_user.id)
    success = service.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria deletada com sucesso"}

@router.post("/{category_id}/restore")
async def restore_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Restaura uma categoria deletada"""
    service = CategoryService(db, current_user.id)
    category = service.restore_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category
```

### **4. Serviços de Negócio**

#### **CategoryService**
```python
# src/categories/services.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from uuid import UUID
from .models import Category, CategoryCreate, CategoryUpdate, CategoryWithTransactionCount
from src.transactions.models import Transaction

class CategoryService:
    def __init__(self, db: Session, user_id: UUID):
        self.db = db
        self.user_id = user_id
    
    def get_categories(self, include_inactive: bool = False) -> List[CategoryWithTransactionCount]:
        """Lista categorias com contagem de transações"""
        query = self.db.query(
            Category,
            func.count(Transaction.id).label('transaction_count')
        ).outerjoin(Transaction, Category.id == Transaction.category_id)
        
        if not include_inactive:
            query = query.filter(Category.is_active == True)
        
        query = query.filter(Category.user_id == self.user_id)
        query = query.group_by(Category.id)
        query = query.order_by(Category.name)
        
        results = query.all()
        
        categories = []
        for category, transaction_count in results:
            category_dict = category.__dict__.copy()
            category_dict['transaction_count'] = transaction_count
            categories.append(CategoryWithTransactionCount(**category_dict))
        
        return categories
    
    def get_category(self, category_id: UUID) -> Optional[Category]:
        """Obtém uma categoria específica"""
        return self.db.query(Category).filter(
            and_(
                Category.id == category_id,
                Category.user_id == self.user_id
            )
        ).first()
    
    def create_category(self, category_data: CategoryCreate) -> Category:
        """Cria uma nova categoria"""
        # Verificar se já existe categoria com mesmo nome
        existing = self.db.query(Category).filter(
            and_(
                Category.name == category_data.name,
                Category.user_id == self.user_id
            )
        ).first()
        
        if existing:
            raise ValueError(f"Já existe uma categoria com o nome '{category_data.name}'")
        
        category = Category(
            user_id=self.user_id,
            **category_data.dict()
        )
        
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def update_category(self, category_id: UUID, category_data: CategoryUpdate) -> Optional[Category]:
        """Atualiza uma categoria"""
        category = self.get_category(category_id)
        if not category:
            return None
        
        # Verificar se o novo nome já existe (se estiver sendo alterado)
        if category_data.name and category_data.name != category.name:
            existing = self.db.query(Category).filter(
                and_(
                    Category.name == category_data.name,
                    Category.user_id == self.user_id,
                    Category.id != category_id
                )
            ).first()
            
            if existing:
                raise ValueError(f"Já existe uma categoria com o nome '{category_data.name}'")
        
        # Atualizar campos
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def delete_category(self, category_id: UUID) -> bool:
        """Soft delete de uma categoria"""
        category = self.get_category(category_id)
        if not category:
            return False
        
        # Verificar se há transações usando esta categoria
        transaction_count = self.db.query(Transaction).filter(
            Transaction.category_id == category_id
        ).count()
        
        if transaction_count > 0:
            raise ValueError(f"Não é possível deletar categoria com {transaction_count} transações")
        
        category.is_active = False
        self.db.commit()
        
        return True
    
    def restore_category(self, category_id: UUID) -> Optional[Category]:
        """Restaura uma categoria deletada"""
        category = self.db.query(Category).filter(
            and_(
                Category.id == category_id,
                Category.user_id == self.user_id
            )
        ).first()
        
        if not category:
            return None
        
        category.is_active = True
        self.db.commit()
        self.db.refresh(category)
        
        return category
```

---

## 🎨 **Interface do Usuário**

### **CategoryContext**
```typescript
// src/categories/CategoryContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { CategoryService } from './CategoryService';
import { Category } from './types';

interface CategoryContextType {
  categories: Category[];
  loading: boolean;
  error: string | null;
  createCategory: (data: CreateCategoryData) => Promise<Category>;
  updateCategory: (id: string, data: UpdateCategoryData) => Promise<Category>;
  deleteCategory: (id: string) => Promise<void>;
  refreshCategories: () => Promise<void>;
}

const CategoryContext = createContext<CategoryContextType | undefined>(undefined);

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const categoryService = new CategoryService();
  
  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await categoryService.getCategories();
      setCategories(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar categorias');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadCategories();
  }, []);
  
  const createCategory = async (data: CreateCategoryData): Promise<Category> => {
    try {
      const category = await categoryService.createCategory(data);
      setCategories(prev => [...prev, category]);
      return category;
    } catch (err) {
      throw err;
    }
  };
  
  const updateCategory = async (id: string, data: UpdateCategoryData): Promise<Category> => {
    try {
      const category = await categoryService.updateCategory(id, data);
      setCategories(prev => prev.map(cat => cat.id === id ? category : cat));
      return category;
    } catch (err) {
      throw err;
    }
  };
  
  const deleteCategory = async (id: string): Promise<void> => {
    try {
      await categoryService.deleteCategory(id);
      setCategories(prev => prev.filter(cat => cat.id !== id));
    } catch (err) {
      throw err;
    }
  };
  
  const refreshCategories = async (): Promise<void> => {
    await loadCategories();
  };
  
  return (
    <CategoryContext.Provider value={{
      categories,
      loading,
      error,
      createCategory,
      updateCategory,
      deleteCategory,
      refreshCategories
    }}>
      {children}
    </CategoryContext.Provider>
  );
};

export const useCategories = () => {
  const context = useContext(CategoryContext);
  if (context === undefined) {
    throw new Error('useCategories must be used within a CategoryProvider');
  }
  return context;
};
```

---

## 🎯 **Categorias Padrão**

### **Categorias de Despesas**
```typescript
// src/categories/defaultCategories.ts
export const DEFAULT_EXPENSE_CATEGORIES = [
  { name: 'Alimentação', icon: 'restaurant', color: '#FF6B6B' },
  { name: 'Transporte', icon: 'directions_car', color: '#4ECDC4' },
  { name: 'Moradia', icon: 'home', color: '#45B7D1' },
  { name: 'Saúde', icon: 'local_hospital', color: '#96CEB4' },
  { name: 'Educação', icon: 'school', color: '#FFEAA7' },
  { name: 'Lazer', icon: 'sports_esports', color: '#DDA0DD' },
  { name: 'Vestuário', icon: 'checkroom', color: '#FFB347' },
  { name: 'Serviços', icon: 'build', color: '#87CEEB' },
  { name: 'Impostos', icon: 'receipt', color: '#F0E68C' },
  { name: 'Outros', icon: 'more_horiz', color: '#D3D3D3' }
];

export const DEFAULT_INCOME_CATEGORIES = [
  { name: 'Salário', icon: 'work', color: '#32CD32' },
  { name: 'Freelance', icon: 'computer', color: '#20B2AA' },
  { name: 'Investimentos', icon: 'trending_up', color: '#FFD700' },
  { name: 'Presentes', icon: 'card_giftcard', color: '#FF69B4' },
  { name: 'Outros', icon: 'more_horiz', color: '#D3D3D3' }
];
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

---

## 🧪 **Testes**

### **Testes Unitários**
```python
# tests/test_categories.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.categories.models import Category

client = TestClient(app)

def test_create_category():
    response = client.post("/categories/", json={
        "name": "Test Category",
        "description": "Test description",
        "icon": "test_icon",
        "color": "#FF0000"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"

def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

---

## ✅ **Checklist de Implementação - Status Atual**

### **Backend**
- ✅ Criar modelo de dados Category
- ✅ Implementar CRUD de categorias
- ✅ Configurar RLS no banco
- ✅ Criar categorias padrão
- ✅ Implementar validações
- ✅ Adicionar testes unitários

### **Frontend**
- ✅ Criar CategoryContext
- ✅ Implementar CategoryService
- ✅ Criar componentes de categoria
- ✅ Implementar formulários
- ✅ Adicionar ícones e cores
- ✅ Implementar filtros

### **Integração**
- ✅ Conectar categorias com transações
- ✅ Implementar migração de dados
- ✅ Testar fluxo completo
- ⏳ Validar performance

### **Status Geral**
- ✅ Sistema de categorias funcional e completo
- ✅ Integração com transações funcionando
- ✅ Interface do usuário implementada
- ⏳ Otimizações de performance pendentes
- ⏳ Testes de performance avançados pendentes

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack 