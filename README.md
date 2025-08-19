# MyFinance

Sistema de finanças pessoais desenvolvido com FastAPI, React e Supabase.

## 🚀 Configuração Rápida

### 1. Configurar variáveis de ambiente
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Configurar credenciais do Supabase no arquivo .env
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your-supabase-anon-key
```

### 2. Verificar configuração
```bash
uv run invoke check-env
```

### 3. Executar aplicação
```bash
# Todos os serviços (backend, frontend, docs)
uv run invoke run-all

# Ou individualmente:
uv run invoke backend    # API na porta 8002
uv run invoke frontend   # React na porta 5173
uv run invoke docs       # Documentação na porta 8001
```

### 4. Aplicar migrações (se necessário)
```bash
# Verificar status das migrações
uv run invoke show-migration-status

# Aplicar migrações pendentes
uv run invoke migrate-production
```

## 📚 Documentação

- [Configuração de Ambiente](docs/dev/env-setup.md)
- [Guia do Desenvolvedor](docs/dev/index.md)
- [Guia do Usuário](docs/user/index.md)

## 🛠️ Tecnologias

- **Backend**: FastAPI, Supabase
- **Frontend**: React, Vite, Material-UI
- **Documentação**: MkDocs
- **Deploy**: Vercel (Frontend) + Local (Backend)
- **Testes**: pytest, Vitest 