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

**IMPORTANTE: Para evitar o erro typing-inspection**

- Conectar repositório GitHub
- Criar Web Service 
- **MANUALMENTE configurar:**
  - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
  - **Start Command:** `python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT`
  - **Python Version:** `3.11` (no Advanced settings)
- Adicionar variáveis de ambiente:
  ```
  SUPABASE_URL=sua_url
  SUPABASE_ANON_KEY=sua_key
  DISABLE_UV=1
  PIP_DISABLE_PIP_VERSION_CHECK=1
  ```

**Não usar** o arquivo de configuração automático - configurar manualmente para forçar pip!

**Nota importante:** O projeto está configurado para usar Python 3.11 para evitar problemas de compatibilidade com Python 3.13 e dependências descontinuadas.

### 4. Configurar Vercel
- Importar repositório
- Diretório: `frontend`
- Variáveis:
  ```
  VITE_API_URL=https://seu-backend.onrender.com
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

- `Dockerfile` - Container do backend (Python 3.11)
- `render.yaml` - Config Render (Python 3.11, pip-only)
- `requirements.txt` - Dependências Python (Pydantic 2.5.3 para compatibilidade)
- `frontend/vercel.json` - Config Vercel
- `supabase/migrations/` - Schema database
- `.github/workflows/deploy.yml` - CI/CD

## 🔧 Soluções de Problemas

### Erro: typing_inspection-0.4.1 (Read-only file system)
**Solução:** Atualizado Pydantic de 2.5.0 para 2.5.3, que removeu a dependência descontinuada `typing-inspection`. Configurado Python 3.11 nos arquivos de deploy para evitar problemas de compatibilidade.

### Versões de Dependências
- FastAPI: 0.104.1
- Pydantic: 2.5.3 (sem typing-inspection)
- Python: 3.11 (especificado no runtime)

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