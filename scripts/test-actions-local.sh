#!/bin/bash

# Script para testar GitHub Actions localmente (sem act)
# Alternativa para quando o act-cli não está disponível

set -e

echo "🚀 MyFinance - Teste Local de GitHub Actions (Alternativo)"
echo "=========================================================="

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  backend     Testar apenas backend (Python/FastAPI)"
    echo "  frontend    Testar apenas frontend (React/Node.js)"
    echo "  deploy      Testar apenas deploy (Vercel)"
    echo "  all         Testar tudo"
    echo "  help        Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 backend"
    echo "  $0 frontend"
    echo "  $0 deploy"
    echo "  $0 all"
}

# Função para testar backend
test_backend() {
    echo "🧪 Testando Backend..."
    echo "📁 Verificando estrutura do projeto..."
    
    # Verificar se os arquivos principais existem
    if [ ! -f "src/main.py" ]; then
        echo "❌ src/main.py não encontrado"
        return 1
    fi
    
    if [ ! -f "requirements.txt" ]; then
        echo "❌ requirements.txt não encontrado"
        return 1
    fi
    
    echo "✅ Estrutura do projeto OK"
    
    # Verificar se Python está disponível
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        echo "❌ Python não encontrado"
        return 1
    fi
    
    echo "🐍 Python encontrado"
    
    # Verificar se pip está disponível
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        echo "❌ pip não encontrado"
        return 1
    fi
    
    echo "📦 pip encontrado"
    
    # Verificar se os testes existem
    if [ ! -d "tests" ]; then
        echo "⚠️  Diretório tests não encontrado"
    else
        echo "✅ Diretório tests encontrado"
    fi
    
    echo "✅ Backend - Verificações básicas concluídas"
}

# Função para testar frontend
test_frontend() {
    echo "🧪 Testando Frontend..."
    echo "📁 Verificando estrutura do frontend..."
    
    # Verificar se o diretório frontend existe
    if [ ! -d "frontend" ]; then
        echo "❌ Diretório frontend não encontrado"
        return 1
    fi
    
    echo "✅ Diretório frontend encontrado"
    
    # Verificar se package.json existe
    if [ ! -f "frontend/package.json" ]; then
        echo "❌ frontend/package.json não encontrado"
        return 1
    fi
    
    echo "✅ package.json encontrado"
    
    # Verificar se Node.js está disponível
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js não encontrado"
        return 1
    fi
    
    echo "🟢 Node.js encontrado: $(node --version)"
    
    # Verificar se npm está disponível
    if ! command -v npm &> /dev/null; then
        echo "❌ npm não encontrado"
        return 1
    fi
    
    echo "📦 npm encontrado: $(npm --version)"
    
    # Verificar se os arquivos principais do React existem
    if [ ! -f "frontend/src/App.tsx" ]; then
        echo "⚠️  frontend/src/App.tsx não encontrado"
    else
        echo "✅ App.tsx encontrado"
    fi
    
    if [ ! -f "frontend/vite.config.ts" ]; then
        echo "⚠️  frontend/vite.config.ts não encontrado"
    else
        echo "✅ vite.config.ts encontrado"
    fi
    
    echo "✅ Frontend - Verificações básicas concluídas"
}

# Função para testar deploy
test_deploy() {
    echo "🧪 Testando Deploy..."
    echo "📁 Verificando arquivos de deploy..."
    
    # Verificar se vercel.json existe
    if [ ! -f "frontend/vercel.json" ]; then
        echo "⚠️  frontend/vercel.json não encontrado"
    else
        echo "✅ vercel.json encontrado"
    fi
    
    # Verificar se Procfile existe
    if [ ! -f "Procfile" ]; then
        echo "⚠️  Procfile não encontrado"
    else
        echo "✅ Procfile encontrado"
    fi
    
    # Verificar se runtime.txt existe
    if [ ! -f "runtime.txt" ]; then
        echo "⚠️  runtime.txt não encontrado"
    else
        echo "✅ runtime.txt encontrado"
    fi
    
    # Verificar se requirements-render.txt existe
    if [ ! -f "requirements-render.txt" ]; then
        echo "⚠️  requirements-render.txt não encontrado"
    else
        echo "✅ requirements-render.txt encontrado"
    fi
    
    echo "✅ Deploy - Verificações básicas concluídas"
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "❌ Nenhuma opção especificada"
    show_help
    exit 1
fi

case $1 in
    "backend")
        test_backend
        ;;
    "frontend")
        test_frontend
        ;;
    "deploy")
        test_deploy
        ;;
    "all")
        echo "🧪 Testando Tudo..."
        test_backend
        echo ""
        test_frontend
        echo ""
        test_deploy
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Opção inválida: $1"
        show_help
        exit 1
        ;;
esac

echo ""
echo "✅ Teste concluído!"
echo ""
echo "💡 Para instalar o act-cli e testar os workflows completos:"
echo "   Windows (PowerShell como Admin): Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')); choco install act-cli"
echo "   Ou baixe manualmente: https://github.com/nektos/act/releases" 