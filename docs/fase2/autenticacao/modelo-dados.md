# 📊 Modelo de Dados - Sistema de Autenticação

## 🗄️ **Estrutura do Banco de Dados**

### **Tabela: user_profiles**

```sql
-- Criação da tabela user_profiles
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    currency TEXT DEFAULT 'BRL',
    language TEXT DEFAULT 'pt-BR',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_email ON user_profiles(email);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- RLS (Row Level Security)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Política: usuário só pode ver/editar seu próprio perfil
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile" ON user_profiles
    FOR DELETE USING (auth.uid() = user_id);
```

### **Atualização da Tabela: transactions**

```sql
-- Adicionar user_id à tabela transactions
ALTER TABLE transactions ADD COLUMN user_id UUID REFERENCES auth.users(id);

-- Criar índice para performance
CREATE INDEX idx_transactions_user_id ON transactions(user_id);

-- Atualizar RLS para transactions
CREATE POLICY "Users can view own transactions" ON transactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions" ON transactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transactions" ON transactions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions" ON transactions
    FOR DELETE USING (auth.uid() = user_id);
```

## 🔧 **Modelos Pydantic**

### **UserProfile Model**

```python
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserProfileBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    timezone: str = "America/Sao_Paulo"
    currency: str = "BRL"
    language: str = "pt-BR"

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None

class UserProfile(UserProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### **Auth Models**

```python
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    profile: Optional[UserProfile] = None
```

## 🔄 **Relacionamentos**

### **Diagrama de Relacionamentos**

```
auth.users (Supabase Auth)
    ↓ (1:1)
user_profiles
    ↓ (1:N)
transactions
```

### **Relacionamentos SQLAlchemy**

```python
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    avatar_url = Column(String)
    timezone = Column(String, default="America/Sao_Paulo")
    currency = Column(String, default="BRL")
    language = Column(String, default="pt-BR")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    transactions = relationship("Transaction", back_populates="user_profile")

class Transaction(Base):
    __tablename__ = "transactions"
    
    # ... campos existentes ...
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.user_id"), nullable=False)
    
    # Relacionamentos
    user_profile = relationship("UserProfile", back_populates="transactions")
```

## 📊 **Dados de Exemplo**

### **Inserção de Perfil de Usuário**

```sql
-- Exemplo de inserção de perfil
INSERT INTO user_profiles (user_id, email, full_name, timezone, currency, language)
VALUES (
    '123e4567-e89b-12d3-a456-426614174000',
    'usuario@exemplo.com',
    'João Silva',
    'America/Sao_Paulo',
    'BRL',
    'pt-BR'
);
```

### **Consulta de Transações por Usuário**

```sql
-- Buscar transações do usuário logado
SELECT t.*, up.full_name as user_name
FROM transactions t
JOIN user_profiles up ON t.user_id = up.user_id
WHERE t.user_id = auth.uid()
ORDER BY t.date DESC;
```

## 🔒 **Segurança e Validação**

### **Validações de Dados**

```python
from pydantic import validator
import pytz

class UserProfileBase(BaseModel):
    # ... campos existentes ...
    
    @validator('timezone')
    def validate_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError('Timezone inválida')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        valid_currencies = ['BRL', 'USD', 'EUR', 'GBP']
        if v not in valid_currencies:
            raise ValueError('Moeda inválida')
        return v
    
    @validator('language')
    def validate_language(cls, v):
        valid_languages = ['pt-BR', 'en-US', 'es-ES']
        if v not in valid_languages:
            raise ValueError('Idioma inválido')
        return v
```

### **Políticas de Segurança**

```sql
-- Política adicional para garantir que apenas usuários autenticados podem acessar
CREATE POLICY "Only authenticated users" ON user_profiles
    FOR ALL USING (auth.role() = 'authenticated');

-- Política para transactions
CREATE POLICY "Only authenticated users" ON transactions
    FOR ALL USING (auth.role() = 'authenticated');
```

## 📈 **Métricas e Performance**

### **Índices Recomendados**

```sql
-- Índices para otimização de consultas
CREATE INDEX idx_user_profiles_created_at ON user_profiles(created_at);
CREATE INDEX idx_transactions_user_date ON transactions(user_id, date);
CREATE INDEX idx_transactions_user_amount ON transactions(user_id, amount);
```

### **Consultas Otimizadas**

```sql
-- Consulta otimizada para dashboard
SELECT 
    COUNT(*) as total_transactions,
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses,
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income
FROM transactions 
WHERE user_id = auth.uid() 
    AND date >= CURRENT_DATE - INTERVAL '30 days';
```

## 🔄 **Migrações**

### **Alembic Migration**

```python
# migrations/versions/0002_add_user_profiles.py
"""Add user profiles table

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Criar tabela user_profiles
    op.create_table('user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('timezone', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Adicionar user_id à tabela transactions
    op.add_column('transactions', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'transactions', 'auth.users', ['user_id'], ['id'])

def downgrade():
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'user_id')
    op.drop_table('user_profiles')
```

Este modelo de dados garante que cada usuário tenha seu próprio perfil e que todas as transações sejam associadas ao usuário correto, mantendo a segurança e integridade dos dados. 