# 📊 Modelo de Dados - Sistema de Categorias

## 🗄️ **Estrutura do Banco de Dados**

### **Tabela: categories**

```sql
-- Criação da tabela categories
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT 'category',
    color TEXT DEFAULT '#1976d2',
    type TEXT NOT NULL CHECK (type IN ('expense', 'income')),
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_categories_user_id ON categories(user_id);
CREATE INDEX idx_categories_type ON categories(type);
CREATE INDEX idx_categories_user_type ON categories(user_id, type);
CREATE INDEX idx_categories_active ON categories(is_active);

-- Trigger para atualizar updated_at
CREATE TRIGGER update_categories_updated_at 
    BEFORE UPDATE ON categories 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RLS (Row Level Security)
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

-- Políticas: usuário só pode ver/editar suas próprias categorias
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

### **Atualização da Tabela: transactions**

```sql
-- Adicionar category_id à tabela transactions
ALTER TABLE transactions ADD COLUMN category_id UUID REFERENCES categories(id);

-- Criar índice para performance
CREATE INDEX idx_transactions_category_id ON transactions(category_id);
CREATE INDEX idx_transactions_user_category ON transactions(user_id, category_id);

-- Atualizar RLS para transactions (incluindo category_id)
CREATE POLICY "Users can view own transactions with categories" ON transactions
    FOR SELECT USING (
        auth.uid() = user_id AND 
        (category_id IS NULL OR EXISTS (
            SELECT 1 FROM categories c 
            WHERE c.id = transactions.category_id 
            AND (c.user_id = auth.uid() OR c.is_default = TRUE)
        ))
    );

CREATE POLICY "Users can insert own transactions with valid category" ON transactions
    FOR INSERT WITH CHECK (
        auth.uid() = user_id AND 
        (category_id IS NULL OR EXISTS (
            SELECT 1 FROM categories c 
            WHERE c.id = transactions.category_id 
            AND (c.user_id = auth.uid() OR c.is_default = TRUE)
        ))
    );

CREATE POLICY "Users can update own transactions with valid category" ON transactions
    FOR UPDATE USING (
        auth.uid() = user_id AND 
        (category_id IS NULL OR EXISTS (
            SELECT 1 FROM categories c 
            WHERE c.id = transactions.category_id 
            AND (c.user_id = auth.uid() OR c.is_default = TRUE)
        ))
    );
```

## 🔧 **Modelos Pydantic**

### **Category Models**

```python
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "category"
    color: str = "#1976d2"
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
        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return v

    @validator('icon')
    def validate_icon(cls, v):
        valid_icons = [
            'category', 'home', 'food', 'transport', 'shopping', 'entertainment',
            'health', 'education', 'work', 'salary', 'investment', 'gift',
            'restaurant', 'car', 'plane', 'train', 'bus', 'bike', 'walk',
            'coffee', 'beer', 'wine', 'pizza', 'burger', 'sushi', 'grocery',
            'pharmacy', 'hospital', 'doctor', 'gym', 'sports', 'movie',
            'music', 'book', 'game', 'travel', 'hotel', 'beach', 'mountain',
            'shopping_cart', 'credit_card', 'cash', 'bank', 'wallet'
        ]
        if v not in valid_icons:
            raise ValueError(f'Ícone deve ser um dos valores válidos: {", ".join(valid_icons)}')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Nome da categoria não pode estar vazio')
            if len(v) > 50:
                raise ValueError('Nome da categoria deve ter no máximo 50 caracteres')
            return v.strip()
        return v

    @validator('color')
    def validate_color(cls, v):
        if v is not None:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
                raise ValueError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return v

class Category(CategoryBase):
    id: UUID
    user_id: UUID
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryWithStats(Category):
    transaction_count: int = 0
    total_amount: float = 0.0
    percentage: float = 0.0

class CategoryList(BaseModel):
    categories: list[Category]
    total: int
    page: int
    per_page: int
    total_pages: int
```

### **Transaction Models (Atualizados)**

```python
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class TransactionBase(BaseModel):
    description: str
    amount: Decimal
    type: TransactionType
    date: date
    category_id: Optional[UUID] = None
    notes: Optional[str] = None

    @validator('description')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Descrição não pode estar vazia')
        if len(v) > 200:
            raise ValueError('Descrição deve ter no máximo 200 caracteres')
        return v.strip()

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @validator('notes')
    def validate_notes(cls, v):
        if v is not None and len(v) > 500:
            raise ValueError('Notas devem ter no máximo 500 caracteres')
        return v

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    date: Optional[date] = None
    category_id: Optional[UUID] = None
    notes: Optional[str] = None

    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Descrição não pode estar vazia')
            if len(v) > 200:
                raise ValueError('Descrição deve ter no máximo 200 caracteres')
            return v.strip()
        return v

    @validator('amount')
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

class Transaction(TransactionBase):
    id: UUID
    user_id: UUID
    category: Optional[Category] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## 🔄 **Relacionamentos**

### **Diagrama de Relacionamentos**

```
auth.users (Supabase Auth)
    ↓ (1:N)
categories
    ↓ (1:N)
transactions
```

### **Relacionamentos SQLAlchemy**

```python
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

class CategoryType(enum.Enum):
    EXPENSE = "expense"
    INCOME = "income"

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    icon = Column(String(50), default="category")
    color = Column(String(7), default="#1976d2")  # #RRGGBB format
    type = Column(SQLEnum(CategoryType), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    transactions = relationship("Transaction", back_populates="category")
    user = relationship("UserProfile", back_populates="categories")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(SQLEnum(TransactionType), nullable=False)
    date = Column(Date, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    category = relationship("Category", back_populates="transactions")
    user_profile = relationship("UserProfile", back_populates="transactions")
```

## 📊 **Dados de Exemplo**

### **Inserção de Categorias Padrão**

```sql
-- Categorias padrão de despesas
INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
(NULL, 'Alimentação', 'Gastos com comida e bebida', 'food', '#FF6B6B', 'expense', TRUE),
(NULL, 'Transporte', 'Combustível, transporte público, táxi', 'transport', '#4ECDC4', 'expense', TRUE),
(NULL, 'Moradia', 'Aluguel, contas de casa, manutenção', 'home', '#45B7D1', 'expense', TRUE),
(NULL, 'Saúde', 'Médico, farmácia, plano de saúde', 'health', '#96CEB4', 'expense', TRUE),
(NULL, 'Educação', 'Cursos, livros, material escolar', 'education', '#FFEAA7', 'expense', TRUE),
(NULL, 'Entretenimento', 'Cinema, shows, hobbies', 'entertainment', '#DDA0DD', 'expense', TRUE),
(NULL, 'Compras', 'Roupas, eletrônicos, outros', 'shopping', '#FFB347', 'expense', TRUE),
(NULL, 'Restaurante', 'Refeições fora de casa', 'restaurant', '#FF8C69', 'expense', TRUE),
(NULL, 'Viagem', 'Passagens, hospedagem, turismo', 'travel', '#87CEEB', 'expense', TRUE),
(NULL, 'Outros', 'Despesas diversas', 'category', '#C0C0C0', 'expense', TRUE);

-- Categorias padrão de receitas
INSERT INTO categories (user_id, name, description, icon, color, type, is_default) VALUES
(NULL, 'Salário', 'Rendimento do trabalho principal', 'work', '#32CD32', 'income', TRUE),
(NULL, 'Freelance', 'Trabalhos extras e projetos', 'work', '#228B22', 'income', TRUE),
(NULL, 'Investimentos', 'Rendimentos de aplicações', 'investment', '#FFD700', 'income', TRUE),
(NULL, 'Presentes', 'Dinheiro recebido como presente', 'gift', '#FF69B4', 'income', TRUE),
(NULL, 'Reembolso', 'Valores reembolsados', 'cash', '#90EE90', 'income', TRUE),
(NULL, 'Outros', 'Receitas diversas', 'category', '#98FB98', 'income', TRUE);
```

### **Consulta de Categorias com Estatísticas**

```sql
-- Buscar categorias do usuário com estatísticas
SELECT 
    c.*,
    COUNT(t.id) as transaction_count,
    COALESCE(SUM(t.amount), 0) as total_amount,
    CASE 
        WHEN SUM(t.amount) OVER (PARTITION BY c.type) > 0 
        THEN (SUM(t.amount) * 100.0 / SUM(t.amount) OVER (PARTITION BY c.type))
        ELSE 0 
    END as percentage
FROM categories c
LEFT JOIN transactions t ON c.id = t.category_id 
    AND t.user_id = auth.uid()
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
WHERE (c.user_id = auth.uid() OR c.is_default = TRUE)
    AND c.is_active = TRUE
    AND c.type = 'expense'
GROUP BY c.id, c.type
ORDER BY total_amount DESC;
```

### **Consulta de Transações por Categoria**

```sql
-- Buscar transações agrupadas por categoria
SELECT 
    c.name as category_name,
    c.icon as category_icon,
    c.color as category_color,
    COUNT(t.id) as transaction_count,
    SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) as total_expenses,
    SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) as total_income
FROM categories c
LEFT JOIN transactions t ON c.id = t.category_id 
    AND t.user_id = auth.uid()
    AND t.date >= CURRENT_DATE - INTERVAL '30 days'
WHERE (c.user_id = auth.uid() OR c.is_default = TRUE)
    AND c.is_active = TRUE
GROUP BY c.id, c.name, c.icon, c.color
ORDER BY total_expenses DESC;
```

## 🔒 **Segurança e Validação**

### **Validações de Dados**

```python
from pydantic import validator
import re

class CategoryBase(BaseModel):
    # ... campos existentes ...
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Nome da categoria não pode estar vazio')
        if len(v) > 50:
            raise ValueError('Nome da categoria deve ter no máximo 50 caracteres')
        # Verificar se não contém caracteres especiais perigosos
        if re.search(r'[<>"\']', v):
            raise ValueError('Nome da categoria não pode conter caracteres especiais')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            if len(v) > 200:
                raise ValueError('Descrição deve ter no máximo 200 caracteres')
            # Verificar se não contém scripts maliciosos
            if re.search(r'<script|javascript:', v, re.IGNORECASE):
                raise ValueError('Descrição contém conteúdo inválido')
        return v
```

### **Políticas de Segurança**

```sql
-- Política adicional para garantir que apenas usuários autenticados podem acessar
CREATE POLICY "Only authenticated users" ON categories
    FOR ALL USING (auth.role() = 'authenticated');

-- Política para garantir que categorias padrão sejam apenas de leitura
CREATE POLICY "Default categories are read-only" ON categories
    FOR UPDATE USING (is_default = FALSE);

CREATE POLICY "Default categories are read-only" ON categories
    FOR DELETE USING (is_default = FALSE);

-- Política para transactions com validação de categoria
CREATE POLICY "Transactions with valid category only" ON transactions
    FOR ALL USING (
        auth.uid() = user_id AND 
        (category_id IS NULL OR EXISTS (
            SELECT 1 FROM categories c 
            WHERE c.id = transactions.category_id 
            AND (c.user_id = auth.uid() OR c.is_default = TRUE)
            AND c.is_active = TRUE
        ))
    );
```

## 📈 **Métricas e Performance**

### **Índices Recomendados**

```sql
-- Índices para otimização de consultas
CREATE INDEX idx_categories_user_type_active ON categories(user_id, type, is_active);
CREATE INDEX idx_categories_default_type ON categories(is_default, type);
CREATE INDEX idx_transactions_user_date_category ON transactions(user_id, date, category_id);
CREATE INDEX idx_transactions_category_amount ON transactions(category_id, amount);

-- Índice parcial para categorias ativas
CREATE INDEX idx_categories_active_partial ON categories(user_id, type) 
WHERE is_active = TRUE;

-- Índice para consultas de estatísticas
CREATE INDEX idx_transactions_user_type_date ON transactions(user_id, type, date);
```

### **Consultas Otimizadas**

```sql
-- Consulta otimizada para dashboard de categorias
WITH category_stats AS (
    SELECT 
        c.id,
        c.name,
        c.icon,
        c.color,
        c.type,
        COUNT(t.id) as transaction_count,
        COALESCE(SUM(t.amount), 0) as total_amount
    FROM categories c
    LEFT JOIN transactions t ON c.id = t.category_id 
        AND t.user_id = auth.uid()
        AND t.date >= CURRENT_DATE - INTERVAL '30 days'
    WHERE (c.user_id = auth.uid() OR c.is_default = TRUE)
        AND c.is_active = TRUE
    GROUP BY c.id, c.name, c.icon, c.color, c.type
)
SELECT 
    *,
    CASE 
        WHEN SUM(total_amount) OVER (PARTITION BY type) > 0 
        THEN (total_amount * 100.0 / SUM(total_amount) OVER (PARTITION BY type))
        ELSE 0 
    END as percentage
FROM category_stats
ORDER BY type, total_amount DESC;
```

## 🔄 **Migrações**

### **Alembic Migration**

```python
# migrations/versions/0003_add_categories.py
"""Add categories table

Revision ID: 0003
Revises: 0002
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Criar enum para tipo de categoria
    category_type_enum = postgresql.ENUM('expense', 'income', name='categorytype')
    category_type_enum.create(op.get_bind())
    
    # Criar tabela categories
    op.create_table('categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(50), nullable=True),
        sa.Column('color', sa.String(7), nullable=True),
        sa.Column('type', sa.Enum('expense', 'income', name='categorytype'), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Adicionar category_id à tabela transactions
    op.add_column('transactions', sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'transactions', 'categories', ['category_id'], ['id'])
    
    # Criar índices
    op.create_index('idx_categories_user_id', 'categories', ['user_id'])
    op.create_index('idx_categories_type', 'categories', ['type'])
    op.create_index('idx_categories_user_type', 'categories', ['user_id', 'type'])
    op.create_index('idx_categories_active', 'categories', ['is_active'])
    op.create_index('idx_transactions_category_id', 'transactions', ['category_id'])

def downgrade():
    op.drop_index('idx_transactions_category_id', 'transactions')
    op.drop_index('idx_categories_active', 'categories')
    op.drop_index('idx_categories_user_type', 'categories')
    op.drop_index('idx_categories_type', 'categories')
    op.drop_index('idx_categories_user_id', 'categories')
    
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'category_id')
    op.drop_table('categories')
    
    # Remover enum
    category_type_enum = postgresql.ENUM('expense', 'income', name='categorytype')
    category_type_enum.drop(op.get_bind())
```

Este modelo de dados garante que as categorias sejam organizadas, seguras e eficientes, permitindo uma gestão financeira estruturada e personalizada para cada usuário. 