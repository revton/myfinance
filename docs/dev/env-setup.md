# Configuração de Variáveis de Ambiente

Este documento explica como configurar as variáveis de ambiente necessárias para executar o projeto MyFinance localmente.

## Visão Geral

O projeto MyFinance utiliza variáveis de ambiente para configurar diferentes aspectos da aplicação, incluindo:

- Configurações do Supabase (banco de dados)
- Configurações da API backend
- Configurações do frontend
- Configurações da documentação
- Configurações de logs e debug

## Configuração Inicial

### 1. Copiar o arquivo de exemplo

```bash
cp env.example .env
```

### 2. Configurar as variáveis obrigatórias

Edite o arquivo `.env` e configure as seguintes variáveis:

#### Supabase (Obrigatório)
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
```

Para obter essas credenciais:
1. Acesse o [Supabase Dashboard](https://supabase.com/dashboard)
2. Crie um novo projeto ou selecione um existente
3. Vá para Settings > API
4. Copie a URL do projeto e a anon/public key

### 3. Verificar a configuração

```bash
uv run invoke check-env
```

## Variáveis Disponíveis

### Supabase (Backend)
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `SUPABASE_URL` | URL do projeto Supabase | - | ✅ |
| `SUPABASE_ANON_KEY` | Chave anônima do Supabase | - | ✅ |
| `DATABASE_URL` | URL do banco de dados (opcional) | - | ❌ |

### API Backend
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `API_PORT` | Porta do servidor FastAPI | `8002` | ❌ |
| `API_HOST` | Host do servidor FastAPI | `0.0.0.0` | ❌ |
| `DEBUG` | Modo de debug | `True` | ❌ |

### Frontend
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `VITE_API_URL` | URL da API backend | `http://localhost:8002` | ❌ |
| `VITE_PORT` | Porta do servidor Vite | `5173` | ❌ |

### Documentação
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `DOCS_PORT` | Porta do servidor MkDocs | `8001` | ❌ |

### Ambiente
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `ENVIRONMENT` | Ambiente atual | `development` | ❌ |
| `LOG_LEVEL` | Nível de log | `INFO` | ❌ |
| `SECRET_KEY` | Chave secreta para JWT | - | ❌ |

### Testes
| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `TEST_SUPABASE_URL` | URL do Supabase para testes | `https://test.supabase.co` | ❌ |
| `TEST_SUPABASE_ANON_KEY` | Chave do Supabase para testes | `test-key` | ❌ |

## Comandos Úteis

### Configuração automática
```bash
# Cria o arquivo .env baseado no env.example
uv run invoke setup-env

# Verifica se as variáveis necessárias estão configuradas
uv run invoke check-env
```

### Execução com variáveis configuradas
```bash
# Backend (usa API_PORT e API_HOST do .env)
uv run invoke backend

# Frontend (usa VITE_API_URL do .env)
uv run invoke frontend

# Documentação (usa DOCS_PORT do .env)
uv run invoke docs

# Todos os serviços
uv run invoke run-all
```

## Ambientes

### Development
```bash
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### Testing
```bash
ENVIRONMENT=testing
DEBUG=False
LOG_LEVEL=INFO
```

### Production
```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
```

## Segurança

⚠️ **Importante**: Nunca commite o arquivo `.env` no repositório. Ele contém informações sensíveis como chaves de API.

O arquivo `.env` já está incluído no `.gitignore` para evitar commits acidentais.

## Troubleshooting

### Erro: "SUPABASE_URL e SUPABASE_ANON_KEY devem ser configurados"
- Verifique se o arquivo `.env` existe
- Confirme se as variáveis `SUPABASE_URL` e `SUPABASE_ANON_KEY` estão configuradas
- Execute `uv run invoke check-env` para verificar

### Erro: "Connection refused" no frontend
- Verifique se o backend está rodando na porta correta
- Confirme se `VITE_API_URL` está apontando para a URL correta do backend

### Erro: "Port already in use"
- Altere a porta nas variáveis de ambiente (`API_PORT`, `DOCS_PORT`, `VITE_PORT`)
- Ou pare o processo que está usando a porta

## Exemplo de arquivo .env completo

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key

# API Backend
API_PORT=8002
API_HOST=0.0.0.0
DEBUG=True

# Frontend
VITE_API_URL=http://localhost:8002
VITE_PORT=5173

# Documentação
DOCS_PORT=8001

# Ambiente
ENVIRONMENT=development
LOG_LEVEL=INFO

# Segurança
SECRET_KEY=your-secret-key-here

# Testes
TEST_SUPABASE_URL=https://test.supabase.co
TEST_SUPABASE_ANON_KEY=test-key
``` 