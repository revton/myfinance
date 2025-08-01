# 🚀 Configuração de Ambiente - Fase 2

## 📋 **Visão Geral**

Este documento detalha a configuração de ambiente necessária para a implementação da Fase 2 do MyFinance, incluindo autenticação e sistema de categorias.

### 🎯 **Objetivos**
- Configurar ambiente de desenvolvimento
- Preparar ambiente de produção
- Configurar variáveis de ambiente
- Implementar migrações de banco

---

## 🛠️ **Configuração de Desenvolvimento**

### **1. Dependências Backend**

#### **requirements.txt (Atualizado)**
```txt
# Dependências existentes
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2

# Novas dependências para Fase 2
supabase==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
alembic==1.13.0
psycopg2-binary==2.9.9
```

#### **Instalação**
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
python -c "import supabase; print('Supabase OK')"
```

### **2. Dependências Frontend**

#### **package.json (Atualizado)**
```json
{
  "dependencies": {
    // Dependências existentes
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    
    // Novas dependências para Fase 2
    "@supabase/supabase-js": "^2.38.0",
    "react-router-dom": "^6.20.0",
    "recharts": "^2.8.0",
    "date-fns": "^2.30.0",
    "react-hook-form": "^7.48.0",
    "@hookform/resolvers": "^3.3.0",
    "yup": "^1.3.0"
  },
  "devDependencies": {
    // Dependências existentes
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.1.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    
    // Novas dependências para Fase 2
    "@types/node": "^20.10.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
```

#### **Instalação**
```bash
cd frontend
npm install

# Verificar instalação
npm run build
```

---

## 🔧 **Configuração de Variáveis de Ambiente**

### **1. Backend (.env)**
```bash
# Configurações existentes
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]
SUPABASE_SERVICE_ROLE_KEY=[your-service-role-key]

# Novas configurações para Fase 2
ENVIRONMENT=development
JWT_SECRET=[your-jwt-secret]
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Configurações de CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
CORS_ALLOW_CREDENTIALS=true

# Configurações de Log
LOG_LEVEL=INFO
LOG_FORMAT=json

# Configurações de Performance
CACHE_TTL=300
MAX_CONNECTIONS=20
```

### **2. Frontend (.env)**
```bash
# Configurações existentes
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://[project].supabase.co
VITE_SUPABASE_ANON_KEY=[your-anon-key]

# Novas configurações para Fase 2
VITE_APP_NAME=MyFinance
VITE_APP_VERSION=2.0.0
VITE_ENVIRONMENT=development

# Configurações de Analytics (opcional)
VITE_ANALYTICS_ID=[your-analytics-id]

# Configurações de Feature Flags
VITE_ENABLE_CATEGORIES=true
VITE_ENABLE_AUTH=true
VITE_ENABLE_DASHBOARD=true
```

### **3. Produção (.env.production)**
```bash
# Backend
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
SUPABASE_URL=https://[project].supabase.co
SUPABASE_ANON_KEY=[your-anon-key]
SUPABASE_SERVICE_ROLE_KEY=[your-service-role-key]
ENVIRONMENT=production
JWT_SECRET=[your-production-jwt-secret]
ALLOWED_ORIGINS=https://your-app.vercel.app
LOG_LEVEL=WARNING

# Frontend
VITE_API_URL=https://your-backend.onrender.com
VITE_SUPABASE_URL=https://[project].supabase.co
VITE_SUPABASE_ANON_KEY=[your-anon-key]
VITE_ENVIRONMENT=production
```

---

## 🗄️ **Configuração do Banco de Dados**

### **1. Migrações Alembic**

#### **Estrutura de Migrações**
```bash
alembic/
├── versions/
│   ├── 0001_initial_migration.py
│   ├── 0002_add_user_profiles.py
│   ├── 0003_add_categories.py
│   └── 0004_add_user_id_to_transactions.py
├── env.py
└── alembic.ini
```

#### **Migração 0002 - User Profiles**
```python
# alembic/versions/0002_add_user_profiles.py
"""Add user profiles

Revision ID: 0002
Revises: 0001
Create Date: 2025-08-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade():
    # Criar tabela user_profiles
    op.create_table('user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['auth.users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Criar índices
    op.create_index(op.f('ix_user_profiles_email'), 'user_profiles', ['email'], unique=True)
    op.create_index(op.f('ix_user_profiles_created_at'), 'user_profiles', ['created_at'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_user_profiles_created_at'), table_name='user_profiles')
    op.drop_index(op.f('ix_user_profiles_email'), table_name='user_profiles')
    op.drop_table('user_profiles')
```

#### **Migração 0003 - Categories**
```python
# alembic/versions/0003_add_categories.py
"""Add categories

Revision ID: 0003
Revises: 0002
Create Date: 2025-08-01 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    # Criar tabela categories
    op.create_table('categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'name', name='unique_user_category_name')
    )
    
    # Criar índices
    op.create_index(op.f('ix_categories_user_id'), 'categories', ['user_id'], unique=False)
    op.create_index(op.f('ix_categories_is_default'), 'categories', ['is_default'], unique=False)
    op.create_index(op.f('ix_categories_is_active'), 'categories', ['is_active'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_categories_is_active'), table_name='categories')
    op.drop_index(op.f('ix_categories_is_default'), table_name='categories')
    op.drop_index(op.f('ix_categories_user_id'), table_name='categories')
    op.drop_table('categories')
```

#### **Migração 0004 - User ID to Transactions**
```python
# alembic/versions/0004_add_user_id_to_transactions.py
"""Add user_id to transactions

Revision ID: 0004
Revises: 0003
Create Date: 2025-08-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

def upgrade():
    # Adicionar user_id e category_id às transações
    op.add_column('transactions', sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column('transactions', sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Criar foreign keys
    op.create_foreign_key(None, 'transactions', 'auth.users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'transactions', 'categories', ['category_id'], ['id'])
    
    # Criar índices
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_transactions_category_id'), 'transactions', ['category_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_transactions_category_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'category_id')
    op.drop_column('transactions', 'user_id')
```

### **2. Execução de Migrações**

#### **Comandos de Migração**
```bash
# Verificar status das migrações
alembic current
alembic history

# Executar migrações pendentes
alembic upgrade head

# Criar nova migração
alembic revision --autogenerate -m "description"

# Reverter última migração
alembic downgrade -1

# Reverter para versão específica
alembic downgrade 0002
```

#### **Script de Setup**
```bash
#!/bin/bash
# scripts/setup_database.sh

echo "🚀 Configurando banco de dados..."

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Ambiente virtual não está ativo"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Executar migrações
echo "🗄️ Executando migrações..."
alembic upgrade head

# Criar categorias padrão
echo "🏷️ Criando categorias padrão..."
python scripts/create_default_categories.py

echo "✅ Configuração concluída!"
```

---

## 🔐 **Configuração de Segurança**

### **1. Row Level Security (RLS)**

#### **Políticas RLS**
```sql
-- Habilitar RLS em todas as tabelas
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Políticas para user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = id);

-- Políticas para categories
CREATE POLICY "Users can view own categories" ON categories
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own categories" ON categories
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own categories" ON categories
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own categories" ON categories
    FOR DELETE USING (auth.uid() = user_id);

-- Políticas para transactions
CREATE POLICY "Users can view own transactions" ON transactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions" ON transactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transactions" ON transactions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions" ON transactions
    FOR DELETE USING (auth.uid() = user_id);
```

### **2. Configuração de CORS**

#### **Backend CORS**
```python
# src/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de hosts confiáveis
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]  # Configurar hosts específicos em produção
)
```

---

## 📊 **Configuração de Monitoramento**

### **1. Logging**

#### **Configuração de Logs**
```python
# src/config/logging.py
import logging
import sys
from typing import Any, Dict
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
            
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
            
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger("myfinance")
    logger.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # Handler para arquivo (produção)
    if os.getenv("ENVIRONMENT") == "production":
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)
    
    return logger
```

### **2. Health Checks**

#### **Endpoint de Health Check**
```python
# src/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.config import get_settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "environment": get_settings().environment
    }

@router.get("/database")
async def database_health_check(db: Session = Depends(get_db)):
    """Health check do banco de dados"""
    try:
        # Testar conexão com banco
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

---

## 🚀 **Scripts de Deploy**

### **1. Script de Deploy Backend (Render)**
```bash
#!/bin/bash
# scripts/deploy_backend.sh

echo "🚀 Deployando backend..."

# Verificar se estamos no branch correto
if [[ "$(git branch --show-current)" != "main" ]]; then
    echo "❌ Deploy deve ser feito do branch main"
    exit 1
fi

# Executar testes
echo "🧪 Executando testes..."
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo "❌ Testes falharam"
    exit 1
fi

# Executar migrações
echo "🗄️ Executando migrações..."
alembic upgrade head

if [ $? -ne 0 ]; then
    echo "❌ Migrações falharam"
    exit 1
fi

echo "✅ Deploy concluído!"
```

### **2. Script de Deploy Frontend (Vercel)**
```bash
#!/bin/bash
# scripts/deploy_frontend.sh

echo "🚀 Deployando frontend..."

cd frontend

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

# Executar testes
echo "🧪 Executando testes..."
npm test -- --coverage --run

if [ $? -ne 0 ]; then
    echo "❌ Testes falharam"
    exit 1
fi

# Build de produção
echo "🔨 Criando build..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build falhou"
    exit 1
fi

echo "✅ Deploy concluído!"
```

---

## 📋 **Checklist de Configuração**

### **Desenvolvimento**
- [ ] Instalar dependências backend
- [ ] Instalar dependências frontend
- [ ] Configurar variáveis de ambiente
- [ ] Executar migrações
- [ ] Criar categorias padrão
- [ ] Testar conexão com Supabase

### **Produção**
- [ ] Configurar variáveis de produção
- [ ] Executar migrações em produção
- [ ] Configurar RLS
- [ ] Configurar CORS
- [ ] Configurar logging
- [ ] Configurar health checks

### **Segurança**
- [ ] Configurar JWT secrets
- [ ] Configurar RLS policies
- [ ] Configurar CORS
- [ ] Configurar rate limiting
- [ ] Configurar backup

### **Monitoramento**
- [ ] Configurar logs
- [ ] Configurar health checks
- [ ] Configurar alertas
- [ ] Configurar métricas
- [ ] Configurar dashboards

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack 