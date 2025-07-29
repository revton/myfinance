# Script para testar GitHub Actions usando act em container Docker
# Nao requer instalacao do act na maquina local

param(
    [Parameter(Position=0)]
    [ValidateSet("backend", "frontend", "deploy", "all", "help", "install")]
    [string]$Option = "help"
)

Write-Host "MyFinance - Teste Local de GitHub Actions (Docker)" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Funcao para mostrar ajuda
function Show-Help {
    Write-Host "Uso: .\test-actions-docker.ps1 [OPCAO]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opcoes:" -ForegroundColor Yellow
    Write-Host "  backend     Testar apenas backend (Python/FastAPI)" -ForegroundColor White
    Write-Host "  frontend    Testar apenas frontend (React/Node.js)" -ForegroundColor White
    Write-Host "  deploy      Testar apenas deploy (Vercel)" -ForegroundColor White
    Write-Host "  all         Testar tudo" -ForegroundColor White
    Write-Host "  install     Instalar imagem Docker do act" -ForegroundColor White
    Write-Host "  help        Mostrar esta ajuda" -ForegroundColor White
    Write-Host ""
    Write-Host "Exemplos:" -ForegroundColor Yellow
    Write-Host "  .\test-actions-docker.ps1 backend" -ForegroundColor White
    Write-Host "  .\test-actions-docker.ps1 frontend" -ForegroundColor White
    Write-Host "  .\test-actions-docker.ps1 deploy" -ForegroundColor White
    Write-Host "  .\test-actions-docker.ps1 all" -ForegroundColor White
    Write-Host "  .\test-actions-docker.ps1 install" -ForegroundColor White
}

# Funcao para verificar se Docker esta disponivel
function Test-Docker {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "ERRO: Docker nao esta instalado!" -ForegroundColor Red
        Write-Host "Instale Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        return $false
    }
    
    try {
        docker info | Out-Null
    } catch {
        Write-Host "ERRO: Docker nao esta rodando!" -ForegroundColor Red
        Write-Host "Inicie o Docker Desktop" -ForegroundColor Yellow
        return $false
    }
    
    Write-Host "OK: Docker esta disponivel" -ForegroundColor Green
    return $true
}

# Funcao para instalar imagem do act
function Install-Act {
    Write-Host "Baixando imagem Docker do act..." -ForegroundColor Green
    docker pull catthehacker/ubuntu:act-latest
    Write-Host "OK: Imagem do act baixada com sucesso!" -ForegroundColor Green
}

# Funcao para executar act via Docker
function Run-Act {
    param([string]$TestType)
    
    Write-Host "Testando $TestType via Docker..." -ForegroundColor Green
    
    # Criar arquivo temporario com o evento
    $eventJson = @"
{
    "inputs": {
        "test_type": "$TestType"
    }
}
"@
    
    $tempFile = [System.IO.Path]::GetTempFileName()
    $eventJson | Out-File -FilePath $tempFile -Encoding UTF8
    
    try {
        # Comando Docker para executar act
        docker run --rm `
            -v "${PWD}:/workspace" `
            -w /workspace `
            -e GITHUB_TOKEN `
            -e VERCEL_TOKEN `
            catthehacker/ubuntu:act-latest `
            act workflow_dispatch `
            -W .github/workflows/test-local.yml `
            -e $tempFile `
            --container-architecture linux/amd64
    } finally {
        # Limpar arquivo temporario
        if (Test-Path $tempFile) {
            Remove-Item $tempFile -Force
        }
    }
}

# Executar baseado na opcao
switch ($Option) {
    "install" {
        if (Test-Docker) {
            Install-Act
        }
    }
    "backend" {
        if (Test-Docker) {
            Run-Act "backend"
        }
    }
    "frontend" {
        if (Test-Docker) {
            Run-Act "frontend"
        }
    }
    "deploy" {
        if (Test-Docker) {
            Run-Act "deploy"
        }
    }
    "all" {
        if (Test-Docker) {
            Run-Act "all"
        }
    }
    "help" {
        Show-Help
    }
}

Write-Host ""
Write-Host "Teste concluido!" -ForegroundColor Green 