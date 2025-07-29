# Script para testar GitHub Actions localmente (sem act) - Versao PowerShell
# Alternativa para quando o act-cli nao esta disponivel

param(
    [Parameter(Position=0)]
    [ValidateSet("backend", "frontend", "deploy", "all", "help")]
    [string]$Option = "help"
)

Write-Host "MyFinance - Teste Local de GitHub Actions (Alternativo)" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

# Funcao para mostrar ajuda
function Show-Help {
    Write-Host "Uso: .\test-actions-local.ps1 [OPCAO]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opcoes:" -ForegroundColor Yellow
    Write-Host "  backend     Testar apenas backend (Python/FastAPI)" -ForegroundColor White
    Write-Host "  frontend    Testar apenas frontend (React/Node.js)" -ForegroundColor White
    Write-Host "  deploy      Testar apenas deploy (Vercel)" -ForegroundColor White
    Write-Host "  all         Testar tudo" -ForegroundColor White
    Write-Host "  help        Mostrar esta ajuda" -ForegroundColor White
    Write-Host ""
    Write-Host "Exemplos:" -ForegroundColor Yellow
    Write-Host "  .\test-actions-local.ps1 backend" -ForegroundColor White
    Write-Host "  .\test-actions-local.ps1 frontend" -ForegroundColor White
    Write-Host "  .\test-actions-local.ps1 deploy" -ForegroundColor White
    Write-Host "  .\test-actions-local.ps1 all" -ForegroundColor White
}

# Funcao para testar backend
function Test-Backend {
    Write-Host "Testando Backend..." -ForegroundColor Green
    Write-Host "Verificando estrutura do projeto..." -ForegroundColor White
    
    # Verificar se os arquivos principais existem
    if (-not (Test-Path "src\main.py")) {
        Write-Host "ERRO: src\main.py nao encontrado" -ForegroundColor Red
        return $false
    }
    
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "ERRO: requirements.txt nao encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "OK: Estrutura do projeto OK" -ForegroundColor Green
    
    # Verificar se Python esta disponivel
    $pythonCmd = $null
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonCmd = "python"
    } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
    }
    
    if (-not $pythonCmd) {
        Write-Host "ERRO: Python nao encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "OK: Python encontrado" -ForegroundColor Green
    
    # Verificar se pip esta disponivel
    $pipCmd = $null
    if (Get-Command pip -ErrorAction SilentlyContinue) {
        $pipCmd = "pip"
    } elseif (Get-Command pip3 -ErrorAction SilentlyContinue) {
        $pipCmd = "pip3"
    }
    
    if (-not $pipCmd) {
        Write-Host "ERRO: pip nao encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "OK: pip encontrado" -ForegroundColor Green
    
    # Verificar se os testes existem
    if (-not (Test-Path "tests")) {
        Write-Host "AVISO: Diretorio tests nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: Diretorio tests encontrado" -ForegroundColor Green
    }
    
    Write-Host "OK: Backend - Verificacoes basicas concluidas" -ForegroundColor Green
    return $true
}

# Funcao para testar frontend
function Test-Frontend {
    Write-Host "Testando Frontend..." -ForegroundColor Green
    Write-Host "Verificando estrutura do frontend..." -ForegroundColor White
    
    # Verificar se o diretorio frontend existe
    if (-not (Test-Path "frontend")) {
        Write-Host "ERRO: Diretorio frontend nao encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "OK: Diretorio frontend encontrado" -ForegroundColor Green
    
    # Verificar se package.json existe
    if (-not (Test-Path "frontend\package.json")) {
        Write-Host "ERRO: frontend\package.json nao encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "OK: package.json encontrado" -ForegroundColor Green
    
    # Verificar se Node.js esta disponivel
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Host "ERRO: Node.js nao encontrado" -ForegroundColor Red
        return $false
    }
    
    $nodeVersion = node --version
    Write-Host "OK: Node.js encontrado: $nodeVersion" -ForegroundColor Green
    
    # Verificar se npm esta disponivel
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
        Write-Host "ERRO: npm nao encontrado" -ForegroundColor Red
        return $false
    }
    
    $npmVersion = npm --version
    Write-Host "OK: npm encontrado: $npmVersion" -ForegroundColor Green
    
    # Verificar se os arquivos principais do React existem
    if (-not (Test-Path "frontend\src\App.tsx")) {
        Write-Host "AVISO: frontend\src\App.tsx nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: App.tsx encontrado" -ForegroundColor Green
    }
    
    if (-not (Test-Path "frontend\vite.config.ts")) {
        Write-Host "AVISO: frontend\vite.config.ts nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: vite.config.ts encontrado" -ForegroundColor Green
    }
    
    Write-Host "OK: Frontend - Verificacoes basicas concluidas" -ForegroundColor Green
    return $true
}

# Funcao para testar deploy
function Test-Deploy {
    Write-Host "Testando Deploy..." -ForegroundColor Green
    Write-Host "Verificando arquivos de deploy..." -ForegroundColor White
    
    # Verificar se vercel.json existe
    if (-not (Test-Path "frontend\vercel.json")) {
        Write-Host "AVISO: frontend\vercel.json nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: vercel.json encontrado" -ForegroundColor Green
    }
    
    # Verificar se Procfile existe
    if (-not (Test-Path "Procfile")) {
        Write-Host "AVISO: Procfile nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: Procfile encontrado" -ForegroundColor Green
    }
    
    # Verificar se runtime.txt existe
    if (-not (Test-Path "runtime.txt")) {
        Write-Host "AVISO: runtime.txt nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: runtime.txt encontrado" -ForegroundColor Green
    }
    
    # Verificar se requirements-render.txt existe
    if (-not (Test-Path "requirements-render.txt")) {
        Write-Host "AVISO: requirements-render.txt nao encontrado" -ForegroundColor Yellow
    } else {
        Write-Host "OK: requirements-render.txt encontrado" -ForegroundColor Green
    }
    
    Write-Host "OK: Deploy - Verificacoes basicas concluidas" -ForegroundColor Green
    return $true
}

# Executar baseado na opcao
switch ($Option) {
    "backend" {
        Test-Backend
    }
    "frontend" {
        Test-Frontend
    }
    "deploy" {
        Test-Deploy
    }
    "all" {
        Write-Host "Testando Tudo..." -ForegroundColor Green
        Test-Backend
        Write-Host ""
        Test-Frontend
        Write-Host ""
        Test-Deploy
    }
    "help" {
        Show-Help
    }
}

Write-Host ""
Write-Host "Teste concluido!" -ForegroundColor Green
Write-Host ""
Write-Host "Para instalar o act-cli:" -ForegroundColor Cyan
Write-Host "Baixe manualmente: https://github.com/nektos/act/releases" -ForegroundColor White 