#!/bin/bash

# Script para testar token Vercel localmente
# Não requer act, testa diretamente

set -e

echo "🔐 MyFinance - Teste Local do Token Vercel"
echo "=========================================="

# Verificar se Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não está instalado!"
    echo "💡 Instale com: npm install -g vercel"
    exit 1
fi

# Verificar se token está definido
if [ -z "$VERCEL_TOKEN" ]; then
    echo "❌ VERCEL_TOKEN não está definido!"
    echo "💡 Configure a variável de ambiente:"
    echo "   export VERCEL_TOKEN='seu-token-aqui'"
    echo ""
    echo "🔗 Gere um token em: https://vercel.com/account/tokens"
    exit 1
fi

echo "✅ Token encontrado (length: ${#VERCEL_TOKEN})"

# Testar autenticação
echo "🔐 Testando autenticação..."
if vercel whoami --token "$VERCEL_TOKEN" > /dev/null 2>&1; then
    echo "✅ Token válido!"
    USER=$(vercel whoami --token "$VERCEL_TOKEN")
    echo "👤 Usuário: $USER"
else
    echo "❌ Token inválido ou expirado!"
    echo "💡 Gere um novo token em: https://vercel.com/account/tokens"
    exit 1
fi

# Testar se o projeto existe
echo "📁 Verificando projeto..."
cd frontend

if [ -f ".vercel/project.json" ]; then
    echo "✅ Projeto Vercel configurado"
    PROJECT_ID=$(cat .vercel/project.json | grep -o '"projectId":"[^"]*"' | cut -d'"' -f4)
    echo "🆔 Project ID: $PROJECT_ID"
else
    echo "⚠️  Projeto não configurado, mas isso é normal para testes"
fi

# Simular deploy (dry run)
echo "🚀 Simulando deploy..."
echo "Comando que seria executado:"
echo "vercel --prod --token \$VERCEL_TOKEN --yes"
echo ""
echo "✅ Simulação concluída!"
echo ""
echo "💡 Para fazer deploy real, execute:"
echo "   cd frontend && vercel --prod --token \$VERCEL_TOKEN --yes" 