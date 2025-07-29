#!/bin/bash

# Script para testar GitHub Actions localmente
# Requer: https://github.com/nektos/act

set -e

echo "🚀 MyFinance - Teste Local de GitHub Actions"
echo "=============================================="

# Verificar se act está instalado
if ! command -v act &> /dev/null; then
    echo "❌ 'act' não está instalado!"
    echo "💡 Instale em: https://github.com/nektos/act"
    echo "   Windows: choco install act-cli"
    echo "   macOS: brew install act"
    echo "   Linux: curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash"
    exit 1
fi

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

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "❌ Nenhuma opção especificada"
    show_help
    exit 1
fi

case $1 in
    "backend")
        echo "🧪 Testando Backend..."
        act workflow_dispatch -W .github/workflows/test-local.yml -e <(echo '{"inputs": {"test_type": "backend"}}') --container-architecture linux/amd64
        ;;
    "frontend")
        echo "🧪 Testando Frontend..."
        act workflow_dispatch -W .github/workflows/test-local.yml -e <(echo '{"inputs": {"test_type": "frontend"}}') --container-architecture linux/amd64
        ;;
    "deploy")
        echo "🧪 Testando Deploy..."
        act workflow_dispatch -W .github/workflows/test-local.yml -e <(echo '{"inputs": {"test_type": "deploy"}}') --container-architecture linux/amd64
        ;;
    "all")
        echo "🧪 Testando Tudo..."
        act workflow_dispatch -W .github/workflows/test-local.yml -e <(echo '{"inputs": {"test_type": "all"}}') --container-architecture linux/amd64
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

echo "✅ Teste concluído!" 