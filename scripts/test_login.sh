#!/bin/bash

# Script para testar login após confirmação de email
# Execute: bash scripts/test_login.sh

echo "🧪 Testando Login após Confirmação de Email"
echo "=========================================="

# Configurações
EMAIL="revtonbr@gmail.com"
PASSWORD="Minha@Senha1"
API_URL="http://localhost:8002"

echo "🎯 Email: $EMAIL"
echo "🔑 Senha: $PASSWORD"
echo "🌐 API: $API_URL"
echo ""

# Testar login
echo "📡 Fazendo requisição de login..."
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

# Separar resposta e status code
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

echo "📊 Status Code: $http_code"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo "✅ SUCESSO! Login realizado com sucesso!"
    echo "🎉 Email confirmado e funcionando!"
    echo ""
    echo "📋 Resposta:"
    echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
else
    echo "❌ ERRO! Login falhou."
    echo ""
    echo "📋 Resposta de erro:"
    echo "$response_body" | jq '.' 2>/dev/null || echo "$response_body"
    echo ""
    echo "💡 Se o erro for 'email not confirmed', execute o script SQL no Supabase Dashboard:"
    echo "   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';"
fi 