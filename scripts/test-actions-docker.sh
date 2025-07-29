#!/bin/bash

# Script para testar GitHub Actions usando act em container Docker
# Não requer instalação do act na máquina local

set -e

echo "🚀 MyFinance - Teste Local de GitHub Actions (Docker)"
echo "====================================================="

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
    echo "  install     Instalar imagem Docker do act"
    echo ""
    echo "Exemplos:"
    echo "  $0 backend"
    echo "  $0 frontend"
    echo "  $0 deploy"
    echo "  $0 all"
    echo "  $0 install"
}

# Função para verificar se Docker está disponível
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker não está instalado!"
        echo "💡 Instale Docker Desktop: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo "❌ Docker não está rodando!"
        echo "💡 Inicie o Docker Desktop"
        exit 1
    fi
    
    echo "✅ Docker está disponível"
}

# Função para instalar imagem do act
install_act() {
    echo "📦 Baixando imagem Docker do act..."
    docker pull catthehacker/ubuntu:act-latest
    echo "✅ Imagem do act baixada com sucesso!"
}

# Função para executar act via Docker
run_act() {
    local test_type=$1
    
    echo "🧪 Testando $test_type via Docker..."
    
    # Comando Docker para executar act
    docker run --rm \
        -v "$(pwd):/workspace" \
        -w /workspace \
        -e GITHUB_TOKEN \
        -e VERCEL_TOKEN \
        catthehacker/ubuntu:act-latest \
        act workflow_dispatch \
        -W .github/workflows/test-local.yml \
        -e <(echo "{\"inputs\": {\"test_type\": \"$test_type\"}}") \
        --container-architecture linux/amd64
}

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "❌ Nenhuma opção especificada"
    show_help
    exit 1
fi

case $1 in
    "install")
        check_docker
        install_act
        ;;
    "backend")
        check_docker
        run_act "backend"
        ;;
    "frontend")
        check_docker
        run_act "frontend"
        ;;
    "deploy")
        check_docker
        run_act "deploy"
        ;;
    "all")
        check_docker
        run_act "all"
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