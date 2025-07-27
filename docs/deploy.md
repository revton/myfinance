# Deploy Gratuito - MyFinance

Este documento descreve como fazer o deploy gratuito do MyFinance usando plataformas gratuitas.

## 🚀 Arquitetura de Deploy

### Plataformas Utilizadas:
- **Backend (FastAPI)**: Render
- **Frontend (React)**: Vercel
- **Database**: Supabase
- **Documentação**: GitHub Pages
- **CI/CD**: GitHub Actions

## 📋 Pré-requisitos

### 1. Contas Necessárias:
- [GitHub](https://github.com) (gratuito)
- [Render](https://render.com) (gratuito - 750h/mês)
- [Vercel](https://vercel.com) (gratuito)
- [Supabase](https://supabase.com) (gratuito - 500MB)

### 2. Configuração do Render (Backend):

1. **Criar conta no Render**:
   - Acesse https://render.com
   - Faça login com GitHub

2. **Criar novo Web Service**:
   - Clique em "New +" > "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name**: myfinance-backend
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
     - **Python Version**: 3.11.0 (será detectado automaticamente)

   > **Nota**: O projeto usa Python 3.11.0 para compatibilidade. Se preferir usar uv, use o comando: `uv pip install -r pyproject.toml --extra backend`

3. **Configurar variáveis de ambiente**:
   ```
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_ANON_KEY=sua_supabase_anon_key
   ```

4. **Configurar Health Check**:
   - Health Check Path: `/health`
   - Auto-Deploy: Enabled

### 3. Configuração do Vercel (Frontend):

1. **Criar conta no Vercel**:
   - Acesse https://vercel.com
   - Faça login com GitHub

2. **Importar projeto**:
   - Clique em "New Project"
   - Importe o repositório
   - Configure o diretório como `frontend`

3. **Configurar variáveis de ambiente**:
   ```
   VITE_API_URL=https://seu-backend.railway.app
   ```

4. **Obter tokens do Vercel**:
   - Vá em Account Settings > Tokens
   - Crie um novo token
   - Anote o Org ID e Project ID

### 4. Configuração do Supabase (Database):

1. **Criar conta no Supabase**:
   - Acesse https://supabase.com
   - Faça login com GitHub

2. **Criar novo projeto**:
   - Clique em "New Project"
   - Escolha uma organização
   - Configure nome e senha

3. **Executar migrations**:
   ```bash
   # Instalar Supabase CLI
   npm install -g supabase
   
   # Login
   supabase login
   
   # Link do projeto
   supabase link --project-ref seu-project-ref
   
   # Executar migrations
   supabase db push
   ```

4. **Obter credenciais**:
   - Vá em Settings > API
   - Copie URL e anon key

### 5. Configuração do GitHub Pages (Documentação):

1. **Habilitar GitHub Pages**:
   - Vá em Settings > Pages
   - Source: "GitHub Actions"
   - Branch: `gh-pages` (criado automaticamente)

2. **Configuração automática**:
   - O workflow `.github/workflows/deploy-docs.yml` fará o deploy automático
   - Documentação será atualizada a cada push na pasta `docs/`

3. **URL da documentação**:
   - `https://revton.github.io/myfinance/`
   - Substitua `revton` pelo seu username do GitHub

## 🔧 Configuração dos Secrets do GitHub

Adicione os seguintes secrets no seu repositório GitHub:

1. **Settings > Secrets and variables > Actions**

```
RAILWAY_TOKEN=sua_railway_token
VERCEL_TOKEN=sua_vercel_token
VERCEL_ORG_ID=seu_org_id
VERCEL_PROJECT_ID=seu_project_id
SUPABASE_URL=sua_supabase_url
SUPABASE_ANON_KEY=sua_supabase_anon_key
```

## 🚀 Deploy Automático

### Fluxo de Deploy:
1. **Push para `main`** → Trigger do GitHub Actions
2. **Testes** → Executa testes do backend e frontend
3. **Deploy Backend** → Railway (se testes passarem)
4. **Deploy Frontend** → Vercel (se testes passarem)

### URLs de Deploy:
- **Backend**: `https://myfinance-backend.onrender.com`
- **Frontend**: `https://myfinance.vercel.app`
- **Documentação**: `https://revton.github.io/myfinance/`
- **Database**: `https://supabase.com/dashboard/project/seu-project`

## 📊 Monitoramento

### Railway:
- Logs em tempo real
- Métricas de uso
- Health checks automáticos

### Vercel:
- Analytics de performance
- Logs de build
- Preview deployments

### Supabase:
- Dashboard de database
- Logs de queries
- Métricas de uso

## 🔒 Segurança

### Variáveis de Ambiente:
- Nunca commitar secrets no código
- Usar sempre GitHub Secrets
- Rotacionar tokens regularmente

### CORS:
- Configurado para permitir apenas domínios específicos
- Headers de segurança configurados

### Database:
- Row Level Security (RLS) habilitado
- Políticas de acesso configuradas

## 💰 Custos

### Gratuito:
- **Render**: 750h/mês (31 dias completos)
- **Vercel**: Deploy ilimitado
- **Supabase**: 500MB database, 50MB/mês
- **GitHub Pages**: Totalmente gratuito
- **GitHub**: Actions ilimitados para repositórios públicos

### Limitações:
- Render: Sleep após 15min inativo
- Supabase: Limite de storage
- Vercel: Limite de bandwidth

## 🛠️ Troubleshooting

### Problemas Comuns:

1. **Render não conecta**:
   - Verificar SUPABASE_URL e SUPABASE_ANON_KEY
   - Verificar logs no dashboard do Render

2. **Vercel build falha**:
   - Verificar dependências
   - Verificar variáveis de ambiente

3. **Supabase connection error**:
   - Verificar URL e anon key
   - Verificar políticas RLS

### Logs:
- Render: Dashboard do projeto
- Vercel: Deploy logs
- GitHub Actions: Actions tab

## 📈 Próximos Passos

1. **Implementar autenticação** com Supabase Auth
2. **Adicionar mais funcionalidades** (categorias, relatórios)
3. **Configurar domínio customizado**
4. **Implementar backup automático**
5. **Adicionar monitoramento** (Sentry, LogRocket)

## 🔗 Links Úteis

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions) 