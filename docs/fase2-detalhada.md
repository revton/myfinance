# 🔐 Fase 2 - Categorias e Autenticação - Especificação Detalhada

## 📋 **Visão Geral**

A **Fase 2** implementa autenticação e categorização de transações, transformando o MyFinance em uma ferramenta completa de gestão financeira pessoal.

### 🎯 **Objetivos Principais**
- **Autenticação Segura**: Sistema de login/registro com Supabase Auth
- **Categorização Inteligente**: Organização automática e manual de transações
- **Privacidade**: Dados isolados por usuário
- **UX Aprimorada**: Interface intuitiva para gestão de categorias

---

## 🏗️ **Arquitetura da Solução**

### **Backend (FastAPI + Supabase)**

#### **1. Sistema de Autenticação**
```python
# Estrutura de autenticação
├── auth/
│   ├── models.py          # User model
│   ├── routes.py          # Auth endpoints
│   ├── middleware.py      # JWT validation
│   └── utils.py           # Auth utilities
```

#### **2. Sistema de Categorias**
```python
# Estrutura de categorias
├── categories/
│   ├── models.py          # Category model
│   ├── routes.py          # CRUD endpoints
│   ├── services.py        # Business logic
│   └── utils.py           # Category utilities
```

#### **3. Modificações no Modelo de Transações**
```python
class Transaction(BaseModel):
    id: Optional[int] = None
    user_id: str                    # NOVO: ID do usuário
    description: str
    amount: Decimal
    transaction_type: TransactionType
    category_id: Optional[int]      # NOVO: ID da categoria
    date: datetime
    created_at: datetime
    updated_at: datetime
```

### **Frontend (React + TypeScript)**

#### **1. Sistema de Autenticação**
```typescript
// Estrutura de autenticação
├── src/
│   ├── auth/
│   │   ├── AuthContext.tsx         # Context de autenticação
│   │   ├── LoginForm.tsx           # Formulário de login
│   │   ├── RegisterForm.tsx        # Formulário de registro
│   │   ├── ProtectedRoute.tsx      # Rota protegida
│   │   └── useAuth.ts              # Hook de autenticação
```

#### **2. Sistema de Categorias**
```typescript
// Estrutura de categorias
├── src/
│   ├── categories/
│   │   ├── CategoryContext.tsx     # Context de categorias
│   │   ├── CategoryList.tsx        # Lista de categorias
│   │   ├── CategoryForm.tsx        # Formulário de categoria
│   │   ├── CategorySelect.tsx      # Select de categoria
│   │   └── useCategories.ts        # Hook de categorias
```

---

## 🔧 **Implementação Detalhada**

### **Semana 1-2: Sistema de Autenticação**

#### **Backend - Supabase Auth Integration**

1. **Modelo de Usuário**
```python
class User(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

2. **Endpoints de Autenticação**
```python
@router.post("/register")
async def register(user_data: UserCreate):
    """Registra um novo usuário"""
    response = supabase.auth.sign_up({
        "email": user_data.email,
        "password": user_data.password,
        "options": {"data": {"full_name": user_data.full_name}}
    })
    return {"message": "Usuário registrado com sucesso"}

@router.post("/login")
async def login(user_data: UserLogin):
    """Autentica um usuário"""
    response = supabase.auth.sign_in_with_password({
        "email": user_data.email,
        "password": user_data.password
    })
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "user": response.user
    }

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário atual"""
    return current_user
```

3. **Middleware de Autenticação**
```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Valida o token JWT e retorna o usuário atual"""
    try:
        user = supabase.auth.get_user(credentials.credentials)
        return User(**user.user)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")
```

#### **Frontend - Interface de Autenticação**

1. **Context de Autenticação**
```typescript
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error('Credenciais inválidas');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    setUser(data.user);
  };

  const logout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

2. **Formulário de Login**
```typescript
export const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao fazer login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
      <Card sx={{ maxWidth: 400, width: '100%' }}>
        <CardContent>
          <Typography variant="h5" component="h1" gutterBottom>
            Login
          </Typography>
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              margin="normal"
              required
            />
            
            <TextField
              fullWidth
              label="Senha"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              margin="normal"
              required
            />
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{ mt: 3, mb: 2 }}
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};
```

### **Semana 3-4: Modelo e CRUD de Categorias**

#### **Backend - Sistema de Categorias**

1. **Modelo de Categoria**
```python
class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    BOTH = "both"

class Category(BaseModel):
    id: Optional[int] = None
    user_id: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    category_type: CategoryType = CategoryType.BOTH
    is_default: bool = False
    created_at: datetime
    updated_at: datetime

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    category_type: CategoryType = CategoryType.BOTH
```

2. **Endpoints de Categorias**
```python
@router.get("/", response_model=List[Category])
async def get_categories(current_user = Depends(get_current_user)):
    """Lista todas as categorias do usuário"""
    return await CategoryService.get_user_categories(current_user.id)

@router.post("/", response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    current_user = Depends(get_current_user)
):
    """Cria uma nova categoria"""
    return await CategoryService.create_category(current_user.id, category_data)

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user = Depends(get_current_user)
):
    """Atualiza uma categoria"""
    category = await CategoryService.update_category(
        category_id, current_user.id, category_data
    )
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user = Depends(get_current_user)
):
    """Remove uma categoria"""
    success = await CategoryService.delete_category(category_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria removida com sucesso"}
```

3. **Serviço de Categorias**
```python
class CategoryService:
    @staticmethod
    async def get_user_categories(user_id: str) -> List[Category]:
        """Obtém todas as categorias de um usuário"""
        supabase = get_supabase_client()
        response = supabase.table("categories").select("*").eq("user_id", user_id).execute()
        return [Category(**category) for category in response.data]

    @staticmethod
    async def create_category(user_id: str, category_data: CategoryCreate) -> Category:
        """Cria uma nova categoria"""
        supabase = get_supabase_client()
        data = {"user_id": user_id, **category_data.dict()}
        response = supabase.table("categories").insert(data).execute()
        return Category(**response.data[0])

    @staticmethod
    async def create_default_categories(user_id: str) -> List[Category]:
        """Cria categorias padrão para o usuário"""
        default_categories = [
            {"name": "Alimentação", "icon": "🍽️", "color": "#FF6B6B", "category_type": "expense"},
            {"name": "Transporte", "icon": "🚗", "color": "#4ECDC4", "category_type": "expense"},
            {"name": "Moradia", "icon": "🏠", "color": "#45B7D1", "category_type": "expense"},
            {"name": "Saúde", "icon": "🏥", "color": "#96CEB4", "category_type": "expense"},
            {"name": "Educação", "icon": "📚", "color": "#FFEAA7", "category_type": "expense"},
            {"name": "Lazer", "icon": "🎮", "color": "#DDA0DD", "category_type": "expense"},
            {"name": "Salário", "icon": "💰", "color": "#98D8C8", "category_type": "income"},
            {"name": "Freelance", "icon": "💼", "color": "#F7DC6F", "category_type": "income"},
            {"name": "Investimentos", "icon": "📈", "color": "#BB8FCE", "category_type": "income"},
        ]

        supabase = get_supabase_client()
        categories = []
        
        for cat_data in default_categories:
            data = {"user_id": user_id, "is_default": True, **cat_data}
            response = supabase.table("categories").insert(data).execute()
            categories.append(Category(**response.data[0]))

        return categories
```

#### **Frontend - Interface de Categorias**

1. **Context de Categorias**
```typescript
interface Category {
  id: number;
  user_id: string;
  name: string;
  description?: string;
  icon?: string;
  color?: string;
  category_type: 'expense' | 'income' | 'both';
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

interface CategoryContextType {
  categories: Category[];
  loading: boolean;
  error: string | null;
  fetchCategories: () => Promise<void>;
  createCategory: (data: Partial<Category>) => Promise<Category>;
  updateCategory: (id: number, data: Partial<Category>) => Promise<Category>;
  deleteCategory: (id: number) => Promise<void>;
  createDefaultCategories: () => Promise<void>;
}

export const CategoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('/api/categories', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setCategories(data);
      } else {
        throw new Error('Erro ao carregar categorias');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const createCategory = async (data: Partial<Category>): Promise<Category> => {
    const token = localStorage.getItem('access_token');
    const response = await fetch('/api/categories', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Erro ao criar categoria');
    }

    const newCategory = await response.json();
    setCategories(prev => [...prev, newCategory]);
    return newCategory;
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <CategoryContext.Provider value={{
      categories,
      loading,
      error,
      fetchCategories,
      createCategory,
      updateCategory,
      deleteCategory,
      createDefaultCategories
    }}>
      {children}
    </CategoryContext.Provider>
  );
};
```

2. **Lista de Categorias**
```typescript
export const CategoryList: React.FC = () => {
  const { categories, loading, deleteCategory } = useCategories();
  const [editCategory, setEditCategory] = useState<any>(null);
  const [showForm, setShowForm] = useState(false);
  const [deleteDialog, setDeleteDialog] = useState<number | null>(null);

  const handleEdit = (category: any) => {
    setEditCategory(category);
    setShowForm(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteCategory(id);
      setDeleteDialog(null);
    } catch (error) {
      console.error('Erro ao deletar categoria:', error);
    }
  };

  if (loading) {
    return <Typography>Carregando categorias...</Typography>;
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Categorias</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setShowForm(true)}
        >
          Nova Categoria
        </Button>
      </Box>

      <List>
        {categories.map((category) => (
          <ListItem
            key={category.id}
            secondaryAction={
              <Box>
                <IconButton onClick={() => handleEdit(category)}>
                  <Edit />
                </IconButton>
                <IconButton onClick={() => setDeleteDialog(category.id)}>
                  <Delete />
                </IconButton>
              </Box>
            }
          >
            <ListItemIcon>
              <span style={{ fontSize: '1.5rem' }}>{category.icon || '📁'}</span>
            </ListItemIcon>
            <ListItemText
              primary={category.name}
              secondary={category.description}
            />
            <Chip
              label={category.category_type}
              size="small"
              color={category.category_type === 'income' ? 'success' : 'default'}
            />
          </ListItem>
        ))}
      </List>

      {/* Formulário de Categoria */}
      <Dialog open={showForm} onClose={() => setShowForm(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editCategory ? 'Editar Categoria' : 'Nova Categoria'}
        </DialogTitle>
        <DialogContent>
          <CategoryForm
            category={editCategory}
            onSuccess={() => {
              setShowForm(false);
              setEditCategory(null);
            }}
            onCancel={() => {
              setShowForm(false);
              setEditCategory(null);
            }}
          />
        </DialogContent>
      </Dialog>

      {/* Dialog de Confirmação de Exclusão */}
      <Dialog open={!!deleteDialog} onClose={() => setDeleteDialog(null)}>
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja excluir esta categoria? Esta ação não pode ser desfeita.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialog(null)}>Cancelar</Button>
          <Button
            onClick={() => deleteDialog && handleDelete(deleteDialog)}
            color="error"
            variant="contained"
          >
            Excluir
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
```

### **Semana 5: Interface de Categorias**

#### **Integração com Transações**

1. **Atualização do Formulário de Transações**
```typescript
export const TransactionForm: React.FC = () => {
  const { categories } = useCategories();
  const [selectedCategory, setSelectedCategory] = useState<number | ''>('');

  // Filtra categorias por tipo de transação
  const getFilteredCategories = (transactionType: 'income' | 'expense') => {
    return categories.filter(cat => 
      cat.category_type === transactionType || cat.category_type === 'both'
    );
  };

  return (
    <form>
      {/* ... outros campos ... */}
      
      <FormControl fullWidth margin="normal">
        <InputLabel>Categoria</InputLabel>
        <Select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value as number)}
          label="Categoria"
        >
          <MenuItem value="">
            <em>Selecione uma categoria</em>
          </MenuItem>
          {getFilteredCategories(transactionType).map((category) => (
            <MenuItem key={category.id} value={category.id}>
              <Box display="flex" alignItems="center">
                <span style={{ marginRight: 8 }}>{category.icon}</span>
                {category.name}
              </Box>
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      
      {/* ... resto do formulário ... */}
    </form>
  );
};
```

2. **Lista de Transações com Categorias**
```typescript
export const TransactionList: React.FC = () => {
  const { categories } = useCategories();

  const getCategoryById = (categoryId: number) => {
    return categories.find(cat => cat.id === categoryId);
  };

  return (
    <List>
      {transactions.map((transaction) => {
        const category = getCategoryById(transaction.category_id);
        
        return (
          <ListItem key={transaction.id}>
            <ListItemIcon>
              <span style={{ fontSize: '1.5rem' }}>
                {category?.icon || '📁'}
              </span>
            </ListItemIcon>
            <ListItemText
              primary={transaction.description}
              secondary={`${transaction.amount} - ${transaction.date}`}
            />
            {category && (
              <Chip
                label={category.name}
                size="small"
                style={{ backgroundColor: category.color }}
              />
            )}
          </ListItem>
        );
      })}
    </List>
  );
};
```

### **Semana 6: Testes e Refinamentos**

#### **Testes Backend**

1. **Testes de Autenticação**
```python
def test_register_user():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert "message" in response.json()

def test_login_user():
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route():
    # Primeiro faz login
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Testa rota protegida
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

2. **Testes de Categorias**
```python
def test_create_category():
    # Primeiro faz login
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Cria categoria
    response = client.post("/categories", 
        json={
            "name": "Test Category",
            "description": "Test Description",
            "icon": "🧪",
            "color": "#FF0000",
            "category_type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
```

#### **Testes Frontend**

1. **Testes de Componentes**
```typescript
describe('LoginForm', () => {
  beforeEach(() => {
    mockLogin.mockClear();
  });

  it('renders login form', () => {
    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  it('submits form with email and password', async () => {
    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });
});
```

---

## 📊 **Cronograma Detalhado**

### **Semana 1: Configuração de Autenticação**
- [ ] Configurar Supabase Auth no backend
- [ ] Implementar modelos de usuário
- [ ] Criar endpoints de registro e login
- [ ] Implementar middleware de autenticação
- [ ] Testes básicos de autenticação

### **Semana 2: Interface de Autenticação**
- [ ] Criar AuthContext e AuthProvider
- [ ] Implementar formulários de login e registro
- [ ] Criar ProtectedRoute component
- [ ] Integrar autenticação no App principal
- [ ] Testes de interface de autenticação

### **Semana 3: Sistema de Categorias Backend**
- [ ] Criar modelo de categoria
- [ ] Implementar CRUD de categorias
- [ ] Criar categorias padrão
- [ ] Integrar categorias com transações
- [ ] Testes de categorias

### **Semana 4: Interface de Categorias**
- [ ] Criar CategoryContext e CategoryProvider
- [ ] Implementar lista de categorias
- [ ] Criar formulário de categoria
- [ ] Implementar select de categoria
- [ ] Testes de interface de categorias

### **Semana 5: Integração Completa**
- [ ] Integrar categorias no formulário de transações
- [ ] Atualizar lista de transações com categorias
- [ ] Implementar filtros por categoria
- [ ] Criar dashboard básico
- [ ] Testes de integração

### **Semana 6: Refinamentos e Testes**
- [ ] Testes end-to-end completos
- [ ] Otimizações de performance
- [ ] Melhorias de UX
- [ ] Documentação da API
- [ ] Deploy e validação

---

## 🗄️ **Estrutura do Banco de Dados**

### **Tabela: users**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Tabela: categories**
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(10),
    color VARCHAR(7),
    category_type VARCHAR(10) DEFAULT 'both' CHECK (category_type IN ('income', 'expense', 'both')),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, name)
);
```

### **Tabela: transactions (atualizada)**
```sql
ALTER TABLE transactions 
ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE CASCADE,
ADD COLUMN category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL;

-- Índices para performance
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_category_id ON transactions(category_id);
CREATE INDEX idx_categories_user_id ON categories(user_id);
```

---

## 🔒 **Considerações de Segurança**

### **Autenticação**
- JWT tokens com expiração
- Refresh tokens para renovação automática
- Validação de senha forte
- Rate limiting para tentativas de login

### **Autorização**
- Middleware de autenticação em todas as rotas protegidas
- Validação de propriedade dos recursos (user_id)
- Sanitização de inputs
- Validação de dados com Pydantic

### **Dados**
- Isolamento completo por usuário
- Backup automático dos dados
- Criptografia de dados sensíveis
- Logs de auditoria para ações críticas

---

## 📱 **Responsividade e UX**

### **Mobile-First Design**
- Interface adaptável para todos os dispositivos
- Gestos touch-friendly
- Loading states e feedback visual
- Offline-first com sincronização

### **Acessibilidade**
- Navegação por teclado
- Screen reader compatibility
- Contraste adequado
- Textos alternativos para ícones

---

## 🚀 **Próximos Passos**

1. **Revisão da Especificação**: Analise este documento e forneça feedback
2. **Aprovação do Design**: Confirme a arquitetura proposta
3. **Setup do Ambiente**: Configure Supabase Auth e prepare o ambiente
4. **Início do Desenvolvimento**: Comece pela Semana 1 seguindo o cronograma

---

**📅 Criado em**: Agosto 2025  
**👤 Responsável**: Desenvolvedor Full-stack  
**🔄 Status**: Aguardando análise e aprovação 