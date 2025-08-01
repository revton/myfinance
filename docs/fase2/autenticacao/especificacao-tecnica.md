# 🔐 Sistema de Autenticação - Especificação Técnica

## 📋 **Visão Geral**

O sistema de autenticação do MyFinance será baseado no **Supabase Auth**, proporcionando uma solução segura e escalável para uso doméstico.

### 🎯 **Objetivos**
- Autenticação segura com email/senha
- Proteção de dados por usuário
- Interface intuitiva para família
- Performance otimizada (< 3s login)

---

## 🏗️ **Arquitetura**

### **Backend (FastAPI)**
```python
# Estrutura de autenticação
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # Middleware de autenticação
│   │   ├── models.py           # Modelos de usuário
│   │   ├── routes.py           # Endpoints de auth
│   │   └── utils.py            # Utilitários JWT
│   └── main.py
```

### **Frontend (React)**
```typescript
// Estrutura de autenticação
├── src/
│   ├── auth/
│   │   ├── AuthContext.tsx     # Contexto de autenticação
│   │   ├── AuthProvider.tsx    # Provider do contexto
│   │   ├── useAuth.ts          # Hook personalizado
│   │   └── types.ts            # Tipos TypeScript
│   ├── components/
│   │   ├── LoginForm.tsx       # Formulário de login
│   │   ├── RegisterForm.tsx    # Formulário de registro
│   │   └── ProtectedRoute.tsx  # Rota protegida
│   └── pages/
│       ├── LoginPage.tsx       # Página de login
│       └── RegisterPage.tsx    # Página de registro
```

---

## 🔧 **Implementação Técnica**

### **1. Configuração Supabase Auth**

#### **Backend - Dependências**
```python
# requirements.txt
supabase==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

#### **Configuração**
```python
# src/config.py
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
```

### **2. Modelos de Dados**

#### **Tabela Users (Supabase)**
```sql
-- Extensão da tabela auth.users do Supabase
CREATE TABLE public.user_profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS (Row Level Security)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- Política: usuário só vê seu próprio perfil
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = id);
```

#### **Tabela Transactions (Atualizada)**
```sql
-- Adicionar user_id às transações existentes
ALTER TABLE transactions ADD COLUMN user_id UUID REFERENCES auth.users(id);

-- RLS para transações
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Política: usuário só vê suas transações
CREATE POLICY "Users can view own transactions" ON transactions
    FOR ALL USING (auth.uid() = user_id);
```

### **3. Endpoints da API**

#### **Autenticação**
```python
# src/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register(user_data: UserRegister):
    """Registra novo usuário"""
    try:
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        return {"message": "Usuário registrado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    """Autentica usuário"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Desconecta usuário"""
    supabase.auth.sign_out()
    return {"message": "Logout realizado com sucesso"}

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário atual"""
    return current_user
```

#### **Dependência de Autenticação**
```python
# src/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase_client)
) -> User:
    """Valida token e retorna usuário atual"""
    try:
        token = credentials.credentials
        user = supabase.auth.get_user(token)
        return user.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### **4. Frontend - Contexto de Autenticação**

#### **AuthContext**
```typescript
// src/auth/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { createClient, SupabaseClient, User } from '@supabase/supabase-js';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [supabase] = useState(() => createClient(
    import.meta.env.VITE_SUPABASE_URL,
    import.meta.env.VITE_SUPABASE_ANON_KEY
  ));

  useEffect(() => {
    // Verificar sessão atual
    const { data: { session } } = supabase.auth.getSession();
    setUser(session?.user ?? null);
    setLoading(false);

    // Listener para mudanças de auth
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, [supabase]);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
  };

  const signUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

---

## 🔒 **Segurança**

### **Políticas de Senha**
- Mínimo 8 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 número
- Pelo menos 1 caractere especial

### **Proteção de Rotas**
```typescript
// src/components/ProtectedRoute.tsx
import { useAuth } from '../auth/useAuth';
import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

### **Headers de Segurança**
```python
# src/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
```

---

## 📊 **Performance**

### **Otimizações**
- Cache de sessão no frontend
- Lazy loading de componentes
- Debounce em formulários
- Loading states otimizados

### **Métricas Alvo**
- **Tempo de Login**: < 3 segundos
- **Tempo de Registro**: < 5 segundos
- **Tempo de Logout**: < 1 segundo
- **Disponibilidade**: > 99.5%

---

## 🧪 **Testes**

### **Testes Unitários**
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "Test123!"
    })
    assert response.status_code == 200

def test_login_user():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "Test123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### **Testes de Integração**
- Fluxo completo de registro/login
- Validação de tokens
- Proteção de rotas
- Logout e limpeza de sessão

---

## 📋 **Checklist de Implementação**

### **Backend**
- [ ] Configurar Supabase Auth
- [ ] Criar modelos de usuário
- [ ] Implementar endpoints de auth
- [ ] Configurar RLS no banco
- [ ] Adicionar middleware de autenticação
- [ ] Implementar validação de tokens

### **Frontend**
- [ ] Configurar Supabase client
- [ ] Criar AuthContext
- [ ] Implementar formulários de login/registro
- [ ] Criar ProtectedRoute
- [ ] Adicionar loading states
- [ ] Implementar error handling

### **DevOps**
- [ ] Configurar variáveis de ambiente
- [ ] Atualizar documentação
- [ ] Implementar testes
- [ ] Configurar monitoramento

---

**📅 Última Atualização**: Agosto 2025  
**📍 Versão**: 1.0  
**👤 Responsável**: Desenvolvedor Full-stack 