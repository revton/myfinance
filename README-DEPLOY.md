# 🚀 Deploy Gratuito - MyFinance

Deploy completo usando plataformas gratuitas: **Render** (Backend) + **Vercel** (Frontend) + **Supabase** (Database) + **GitHub Pages** (Docs)

## ⚡ Setup Rápido (5 minutos)

### 1. Criar Contas
- [Render](https://render.com) - Backend
- [Vercel](https://vercel.com) - Frontend  
- [Supabase](https://supabase.com) - Database
- [GitHub](https://github.com) - Documentação (já tem)

### 2. Configurar Supabase
```bash
# Criar projeto no Supabase
# Executar migration:
supabase db push
```

### 3. Configurar Render
- Conectar repositório GitHub
- Criar Web Service
- Adicionar variáveis:
  ```
  SUPABASE_URL=sua_url
  SUPABASE_ANON_KEY=sua_key
  ```

### 4. Configurar Vercel
- Importar repositório
- Diretório: `frontend`
- Variáveis:
  ```
  VITE_API_URL=https://seu-backend.railway.app
  ```

### 5. GitHub Secrets
```
VERCEL_TOKEN=xxx
VERCEL_ORG_ID=xxx
VERCEL_PROJECT_ID=xxx
SUPABASE_URL=xxx
SUPABASE_ANON_KEY=xxx
```

## 📁 Arquivos de Configuração

- `Dockerfile` - Container do backend
- `render.yaml` - Config Render
- `frontend/vercel.json` - Config Vercel
- `supabase/migrations/` - Schema database
- `.github/workflows/deploy.yml` - CI/CD

## 🔗 URLs Finais

- **Frontend**: `https://myfinance.vercel.app`
- **Backend**: `https://myfinance-backend.onrender.com`
- **Documentação**: `https://revton.github.io/myfinance/`
- **Database**: Dashboard Supabase

## 💰 Custo: $0/mês

- Render: 750h/mês gratuito
- Vercel: Gratuito
- Supabase: 500MB gratuito
- GitHub Pages: Gratuito
- GitHub Actions: Gratuito

## 📖 Documentação Completa

Veja `docs/deploy.md` para instruções detalhadas. 