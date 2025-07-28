# 🔄 Guia de Migração: FastAPI → Flask + Migrações

**MyFinance v2.0 - Sistema de Gestão de Banco de Dados**

---

## 🎯 **Objetivo da Migração**

Migrar o MyFinance de **FastAPI + Supabase** para **Flask + SQLAlchemy + Migrações**, permitindo que a aplicação gerencie completamente o banco de dados, incluindo:

- ✅ **Criação automática de tabelas**
- ✅ **Sistema de migrações versionadas**
- ✅ **Comandos CLI para gestão do banco**
- ✅ **Controle total da estrutura de dados**
- ✅ **Suporte a múltiplos ambientes**

---

## 📊 **Comparação: Antes vs Depois**

| Aspecto | FastAPI (Antes) | Flask (Depois) |
|---------|-----------------|----------------|
| **Framework** | FastAPI + Pydantic | Flask + SQLAlchemy |
| **Banco** | Supabase (externo) | PostgreSQL (controlado) |
| **Migrações** | Manual via SQL | Automático via Alembic |
| **Modelos** | Pydantic BaseModel | SQLAlchemy Models |
| **CLI** | Limitado | Comandos personalizados |
| **Deploy** | Dependente do Supabase | Independente |

---

## 🗄️ **Nova Arquitetura do Banco**

### **Estrutura de Arquivos**

```
src/
├── app.py              # Aplicação Flask principal
├── models.py           # Modelos SQLAlchemy
├── routes.py           # Rotas da API
└── config.py           # Configurações (mantido)

migrations/             # Sistema de migrações (novo)
├── versions/           # Versões das migrações
├── alembic.ini         # Configuração do Alembic
└── env.py              # Ambiente das migrações

tests/
└── test_flask_app.py   # Testes para Flask

requirements-flask.txt  # Dependências Flask
run_flask.py           # Script de desenvolvimento
```

### **Modelos de Dados**

#### **Transaction Model**
```python
class Transaction(BaseModel):
    id = UUID (Primary Key, auto-gerado)
    type = String(10) - 'income' ou 'expense'
    amount = Numeric(12,2) - valor positivo
    description = Text - descrição obrigatória
    category_id = UUID (FK para Category) - futuro
    user_id = UUID (FK para User) - futuro
    created_at = DateTime - auto
    updated_at = DateTime - auto-update
```

#### **Category Model (Futuro)**
```python
class Category(BaseModel):
    id = UUID (Primary Key)
    name = String(100) - único
    description = Text
    color = String(7) - hex color
    is_active = Boolean
    created_at/updated_at = DateTime
```

#### **User Model (Futuro)**
```python
class User(BaseModel):
    id = UUID (Primary Key)
    email = String(255) - único
    name = String(255)
    password_hash = String(255)
    is_active = Boolean
    created_at/updated_at = DateTime
```

---

## 🚀 **Processo de Migração**

### **Fase 1: Preparação**

```bash
# 1. Instalar dependências Flask
pip install -r requirements-flask.txt

# 2. Configurar variáveis de ambiente
export DATABASE_URL="postgresql://user:password@localhost/myfinance"
export FLASK_ENV="development"
export SECRET_KEY="sua-chave-secreta"
```

### **Fase 2: Inicialização do Banco**

```bash
# 1. Inicializar sistema de migrações
flask --app src.app db init

# 2. Criar primeira migração
flask --app src.app db migrate -m "Initial migration"

# 3. Aplicar migração
flask --app src.app db upgrade

# 4. Verificar estrutura
flask --app src.app status
```

### **Fase 3: Migração de Dados (Se necessário)**

```python
# Script de migração de dados do Supabase
from src.app import create_app, db
from src.models import Transaction
import supabase

app = create_app()
with app.app_context():
    # Conectar ao Supabase atual
    supabase_client = supabase.create_client(URL, KEY)
    
    # Buscar dados existentes
    result = supabase_client.table("transactions").select("*").execute()
    
    # Migrar para SQLAlchemy
    for item in result.data:
        transaction = Transaction(
            type=item['type'],
            amount=item['amount'],
            description=item['description']
        )
        db.session.add(transaction)
    
    db.session.commit()
    print(f"✅ {len(result.data)} transações migradas!")
```

### **Fase 4: Teste da Nova API**

```bash
# Executar aplicação Flask
python run_flask.py

# Testar endpoints
curl http://localhost:5000/api/v1/health
curl http://localhost:5000/api/v1/transactions/
curl http://localhost:5000/api/v1/summary
```

---

## 🎮 **Comandos CLI Disponíveis**

### **Gestão do Banco de Dados**

```bash
# Inicializar banco (primeira vez)
flask --app src.app init_db

# Resetar banco (CUIDADO!)
flask --app src.app reset_db

# Adicionar dados de exemplo
flask --app src.app seed_db

# Ver status da aplicação
flask --app src.app status
```

### **Sistema de Migrações**

```bash
# Inicializar migrações (primeira vez)
flask --app src.app db init

# Criar nova migração
flask --app src.app db migrate -m "Descrição da mudança"

# Aplicar migrações pendentes
flask --app src.app db upgrade

# Reverter última migração
flask --app src.app db downgrade

# Ver histórico de migrações
flask --app src.app db history

# Ver migração atual
flask --app src.app db current
```

---

## 🔧 **Configuração de Ambientes**

### **Desenvolvimento Local**

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/myfinance_dev
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key
```

### **Teste**

```bash
# Usa SQLite em memória
DATABASE_URL=sqlite:///:memory:
FLASK_ENV=testing
```

### **Produção (Render.com)**

```bash
# Variáveis no Render
DATABASE_URL=postgresql://... (URL do PostgreSQL)
FLASK_ENV=production
SECRET_KEY=chave-segura-gerada
```

---

## 📋 **API Endpoints (Compatibilidade)**

### **Mantidos (Compatíveis)**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/transactions/` | Listar transações |
| POST | `/api/v1/transactions/` | Criar transação |
| GET | `/api/v1/transactions/{id}` | Buscar por ID |
| PUT | `/api/v1/transactions/{id}` | Atualizar transação |
| DELETE | `/api/v1/transactions/{id}` | Deletar transação |

### **Novos Endpoints**

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/status` | Status detalhado |
| GET | `/api/v1/summary` | Resumo financeiro |
| GET | `/api/v1/balance` | Saldo atual |
| GET | `/api/v1/categories/` | Listar categorias |
| POST | `/api/v1/categories/` | Criar categoria |

### **Melhorias na API**

- ✅ **Paginação** em listagens
- ✅ **Filtros** por tipo de transação
- ✅ **Validação robusta** de dados
- ✅ **Tratamento de erros** padronizado
- ✅ **Logs** de operações

---

## 🧪 **Sistema de Testes**

### **Executar Testes**

```bash
# Todos os testes
pytest tests/test_flask_app.py -v

# Com cobertura
pytest tests/test_flask_app.py --cov=src --cov-report=html

# Testes específicos
pytest tests/test_flask_app.py::TestTransactionAPI -v
```

### **Tipos de Teste Incluídos**

- ✅ **Testes de API** (endpoints)
- ✅ **Testes de Modelos** (SQLAlchemy)
- ✅ **Testes de CLI** (comandos)
- ✅ **Testes de Validação** (dados)
- ✅ **Testes de Integração** (banco)

---

## 📈 **Benefícios da Migração**

### **Para Desenvolvimento**

- 🔧 **Controle total** do esquema do banco
- 🚀 **Migrações automáticas** versionadas
- 🎯 **Ambiente local** independente
- 📊 **Comandos CLI** poderosos
- 🧪 **Testes** mais robustos

### **Para Produção**

- 🏗️ **Deploy independente** (sem Supabase)
- 💰 **Custo reduzido** (PostgreSQL gratuito)
- 🔒 **Segurança** controlada
- 📊 **Performance** otimizada
- 🔄 **Backup** e restore simplificados

### **Para o Futuro**

- 👥 **Autenticação** preparada
- 📂 **Categorias** estruturadas
- 🔍 **Relatórios** avançados
- 📱 **Multi-tenant** possível
- 🌐 **Escalabilidade** ilimitada

---

## 🚨 **Checklist de Migração**

### **Pré-Migração**

- [ ] Backup dos dados do Supabase
- [ ] Configurar PostgreSQL local
- [ ] Testar conexão com banco
- [ ] Revisar variáveis de ambiente

### **Durante a Migração**

- [ ] Instalar dependências Flask
- [ ] Executar migrações
- [ ] Migrar dados existentes
- [ ] Testar todos endpoints
- [ ] Verificar funcionamento do frontend

### **Pós-Migração**

- [ ] Deploy em ambiente de teste
- [ ] Validar integração frontend
- [ ] Configurar monitoramento
- [ ] Atualizar documentação
- [ ] Treinar equipe nos novos comandos

---

## 🎯 **Próximos Passos**

1. **🔄 Revisar este PR** e aprovar
2. **🧪 Testar localmente** a nova estrutura
3. **📊 Migrar dados** do Supabase (se necessário)
4. **🚀 Deploy** em ambiente de teste
5. **✅ Validar** funcionamento completo
6. **📋 Planejar** features das próximas fases

---

**🎉 Com esta migração, o MyFinance ganha total autonomia sobre seus dados e estrutura, preparando-se para as próximas fases do roadmap!**