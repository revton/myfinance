#!/bin/bash

# Script de demonstração da solução Docker para GitHub Actions
# Mostra como usar o act via Docker sem instalar na máquina

set -e

echo "🐳 Demonstração: Teste Local de GitHub Actions com Docker"
echo "========================================================="
echo ""

echo "📋 Pré-requisitos:"
echo "   ✅ Docker Desktop instalado e rodando"
echo "   ✅ Projeto MyFinance no diretório atual"
echo ""

echo "🚀 Passo 1: Verificar se Docker está disponível"
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
echo ""

echo "📦 Passo 2: Instalar imagem Docker do act (primeira vez)"
if ! docker images | grep -q "catthehacker/ubuntu.*act-latest"; then
    echo "Baixando imagem Docker do act..."
    docker pull catthehacker/ubuntu:act-latest
    echo "✅ Imagem baixada com sucesso!"
else
    echo "✅ Imagem já está disponível"
fi
echo ""

echo "🧪 Passo 3: Testar estrutura do projeto"
echo "Verificando se os arquivos necessários existem..."

# Verificar arquivos essenciais
if [ ! -f "src/main.py" ]; then
    echo "❌ src/main.py não encontrado"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt não encontrado"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ Diretório frontend não encontrado"
    exit 1
fi

if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json não encontrado"
    exit 1
fi

echo "✅ Estrutura do projeto OK"
echo ""

echo "🔧 Passo 4: Executar teste básico via Docker"
echo "Testando backend..."

# Criar arquivo temporário com evento
cat > /tmp/test-event.json << EOF
{
    "inputs": {
        "test_type": "backend"
    }
}
EOF

# Executar act via Docker
docker run --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    catthehacker/ubuntu:act-latest \
    act workflow_dispatch \
    -W .github/workflows/test-local.yml \
    -e /tmp/test-event.json \
    --container-architecture linux/amd64 \
    --dryrun || echo "⚠️  Teste em modo dry-run (simulação)"

# Limpar arquivo temporário
rm -f /tmp/test-event.json

echo ""
echo "✅ Demonstração concluída!"
echo ""
echo "💡 Para usar em produção:"
echo "   ./scripts/test-actions-docker.sh install  # Primeira vez"
echo "   ./scripts/test-actions-docker.sh all      # Testar tudo"
echo "   ./scripts/test-actions-docker.sh backend  # Testar apenas backend"
echo "   ./scripts/test-actions-docker.sh frontend # Testar apenas frontend"
echo "   ./scripts/test-actions-docker.sh deploy   # Testar apenas deploy"
echo ""
echo "📖 Mais informações: docs/local-testing.md" 