# 🧪 Teste Local de GitHub Actions

Este guia explica como testar as GitHub Actions localmente sem precisar fazer push para o repositório.

## 🛠️ Ferramentas Necessárias

### 1. Act (GitHub Actions Local)
```bash
# Windows (Chocolatey)
choco install act-cli

# macOS (Homebrew)
brew install act

# Linux
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### 2. Vercel CLI
```bash
npm install -g vercel
```

## 🚀 Como Usar

### Teste Completo (Recomendado)
```bash
# Testar tudo
./scripts/test-actions.sh all

# Testar apenas backend
./scripts/test-actions.sh backend

# Testar apenas frontend
./scripts/test-actions.sh frontend

# Testar apenas deploy
./scripts/test-actions.sh deploy
```

### Teste Específico do Token Vercel
```bash
# Configurar token
export VERCEL_TOKEN='seu-token-aqui'

# Testar token
./scripts/test-vercel-token.sh
```

## 📋 Workflows Disponíveis

### 1. `test-local.yml`
Workflow específico para testes locais com:
- ✅ Teste de backend (Python/FastAPI)
- ✅ Teste de frontend (React/Node.js)
- ✅ Teste de deploy (Vercel)
- ✅ Validação de token
- ✅ Simulação de deploy

### 2. Scripts de Conveniência
- `scripts/test-actions.sh` - Testa workflows completos
- `scripts/test-vercel-token.sh` - Testa apenas token Vercel

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Token Vercel (obrigatório para deploy)
export VERCEL_TOKEN='seu-token-aqui'

# Outras variáveis (opcionais)
export SUPABASE_URL='https://test.supabase.co'
export SUPABASE_ANON_KEY='test-key'
```

### Obter Token Vercel
1. Acesse: https://vercel.com/account/tokens
2. Clique em "Create Token"
3. Dê um nome (ex: "MyFinance Deploy")
4. Copie o token gerado
5. Configure no GitHub Secrets ou localmente

## 🧪 Exemplos de Uso

### Teste Rápido do Backend
```bash
./scripts/test-actions.sh backend
```

### Teste Rápido do Frontend
```bash
./scripts/test-actions.sh frontend
```

### Verificar Token Vercel
```bash
export VERCEL_TOKEN='seu-token'
./scripts/test-vercel-token.sh
```

### Teste Completo
```bash
./scripts/test-actions.sh all
```

## 🔍 Debug e Troubleshooting

### Problemas Comuns

#### 1. Act não encontrado
```bash
# Verificar instalação
act --version

# Reinstalar se necessário
# Windows: choco uninstall act-cli && choco install act-cli
# macOS: brew uninstall act && brew install act
```

#### 2. Token Vercel inválido
```bash
# Testar token
vercel whoami --token $VERCEL_TOKEN

# Gerar novo token se necessário
# https://vercel.com/account/tokens
```

#### 3. Docker não disponível
```bash
# Act requer Docker
docker --version

# Instalar Docker se necessário
# https://docs.docker.com/get-docker/
```

### Logs Detalhados
```bash
# Verbose mode
act -v

# Debug mode
act -d
```

## 📊 Benefícios

### ✅ Vantagens
- **Rápido**: Teste local sem push/pull
- **Seguro**: Não afeta repositório
- **Flexível**: Teste partes específicas
- **Debug**: Logs detalhados
- **Economia**: Não consome minutos do GitHub Actions

### ⚠️ Limitações
- **Docker**: Requer Docker instalado
- **Recursos**: Usa recursos locais
- **Diferenças**: Pode ter pequenas diferenças do ambiente real

## 🎯 Próximos Passos

1. **Instalar ferramentas** (act, vercel-cli)
2. **Configurar token** Vercel
3. **Testar localmente** antes de fazer PR
4. **Corrigir problemas** identificados
5. **Fazer PR** apenas quando tudo estiver OK

---

**💡 Dica**: Use sempre o teste local antes de fazer PR para economizar tempo e recursos! 