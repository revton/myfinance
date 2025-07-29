# Teste Local de GitHub Actions

Este documento explica como testar os GitHub Actions localmente no projeto MyFinance.

## Opções de Teste

### 1. Usando Docker (Recomendado) ⭐

A solução mais limpa e isolada - usa `act` em um container Docker sem instalar nada na sua máquina.

#### Pré-requisitos
- Docker Desktop instalado e rodando

#### Uso

**Bash (Linux/macOS/Git Bash):**
```bash
# Instalar imagem Docker do act (primeira vez)
./scripts/test-actions-docker.sh install

# Testar tudo
./scripts/test-actions-docker.sh all

# Testar apenas backend
./scripts/test-actions-docker.sh backend

# Testar apenas frontend
./scripts/test-actions-docker.sh frontend

# Testar apenas deploy
./scripts/test-actions-docker.sh deploy
```

**PowerShell (Windows):**
```powershell
# Instalar imagem Docker do act (primeira vez)
.\scripts\test-actions-docker.ps1 install

# Testar tudo
.\scripts\test-actions-docker.ps1 all

# Testar apenas backend
.\scripts\test-actions-docker.ps1 backend

# Testar apenas frontend
.\scripts\test-actions-docker.ps1 frontend

# Testar apenas deploy
.\scripts\test-actions-docker.ps1 deploy
```

#### Vantagens
- ✅ **Isolado**: Não afeta seu sistema
- ✅ **Limpo**: Não instala nada na máquina
- ✅ **Consistente**: Mesmo ambiente sempre
- ✅ **Fácil**: Apenas Docker necessário

### 2. Usando act-cli (Avançado)

O `act` é uma ferramenta que permite executar GitHub Actions localmente usando Docker.

#### Instalação

**Windows:**
```powershell
# Como administrador
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install act-cli
```

**macOS:**
```bash
brew install act
```

**Linux:**
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

#### Uso

```bash
# Testar backend
./scripts/test-actions.sh backend

# Testar frontend
./scripts/test-actions.sh frontend

# Testar deploy
./scripts/test-actions.sh deploy

# Testar tudo
./scripts/test-actions.sh all
```

### 3. Scripts Alternativos (Básico)

Se você não conseguir instalar o `act-cli` ou Docker, use os scripts alternativos que fazem verificações básicas:

#### Bash (Linux/macOS/Git Bash)
```bash
# Testar tudo
./scripts/test-actions-local.sh all

# Testar apenas backend
./scripts/test-actions-local.sh backend

# Testar apenas frontend
./scripts/test-actions-local.sh frontend

# Testar apenas deploy
./scripts/test-actions-local.sh deploy
```

#### PowerShell (Windows)
```powershell
# Testar tudo
.\scripts\test-actions-local.ps1 all

# Testar apenas backend
.\scripts\test-actions-local.ps1 backend

# Testar apenas frontend
.\scripts\test-actions-local.ps1 frontend

# Testar apenas deploy
.\scripts\test-actions-local.ps1 deploy
```

## O que os Scripts Verificam

### Backend
- ✅ Existência de `src/main.py`
- ✅ Existência de `requirements.txt`
- ✅ Python instalado
- ✅ pip instalado
- ✅ Diretório `tests/`

### Frontend
- ✅ Diretório `frontend/`
- ✅ `frontend/package.json`
- ✅ Node.js instalado
- ✅ npm instalado
- ✅ `frontend/src/App.tsx`
- ✅ `frontend/vite.config.ts`

### Deploy
- ✅ `frontend/vercel.json`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `requirements-render.txt`

## Comparação das Opções

| Aspecto | Docker | act-cli | Scripts Locais |
|---------|--------|---------|----------------|
| **Instalação** | Apenas Docker | act + Docker | Nenhuma |
| **Isolamento** | ✅ Completo | ✅ Completo | ❌ Sistema local |
| **Consistência** | ✅ Sempre igual | ✅ Sempre igual | ⚠️ Depende do sistema |
| **Facilidade** | ✅ Muito fácil | ⚠️ Média | ✅ Muito fácil |
| **Funcionalidade** | ✅ Completa | ✅ Completa | ⚠️ Básica |
| **Recomendação** | ⭐ **Principal** | 🔧 **Avançado** | 🆘 **Fallback** |

## Troubleshooting

### Problemas com Docker

1. **Docker não encontrado:**
   - Instale Docker Desktop: https://www.docker.com/products/docker-desktop
   - Certifique-se de que está rodando

2. **Erro de permissão:**
   - Execute como administrador (Windows)
   - Adicione usuário ao grupo docker (Linux)

### Problemas com act-cli no Windows

1. **Erro de permissão:**
   - Execute PowerShell como administrador
   - Verifique se a política de execução permite scripts

2. **Docker não encontrado:**
   - Instale Docker Desktop para Windows
   - Certifique-se de que o Docker está rodando

3. **Chocolatey não funciona:**
   - Use o download manual: https://github.com/nektos/act/releases
   - Ou use os scripts alternativos

### Problemas com Scripts Alternativos

1. **Permissão negada (Bash):**
   ```bash
   chmod +x scripts/test-actions-local.sh
   ```

2. **Política de execução (PowerShell):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Próximos Passos

Após os testes locais, você pode:

1. Fazer commit das mudanças
2. Fazer push para o repositório
3. Verificar se os GitHub Actions passam no GitHub
4. Criar um Pull Request

## Workflows Disponíveis

- `test-local.yml` - Testes locais para backend, frontend e deploy
- `test.yml` - Testes automatizados no GitHub
- `deploy.yml` - Deploy automático

## Configuração de Variáveis de Ambiente

Para testes completos, configure as variáveis de ambiente:

```bash
# Token Vercel (para deploy)
export VERCEL_TOKEN='seu-token-aqui'

# Token GitHub (opcional)
export GITHUB_TOKEN='seu-token-aqui'
```

**Obter Token Vercel:**
1. Acesse: https://vercel.com/account/tokens
2. Clique em "Create Token"
3. Dê um nome (ex: "MyFinance Deploy")
4. Copie o token gerado 