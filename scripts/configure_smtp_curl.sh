#!/bin/bash

# Script para configurar SMTP via API do Supabase
# Execute: bash scripts/configure_smtp_curl.sh

echo "🔧 Configuração de SMTP via API do Supabase"
echo "=========================================="

# Configurações
PROJECT_REF="qgkifpsimkcsfrwwyqsd"

# Solicitar credenciais
echo -n "🔑 Digite seu Supabase Access Token (sbp_...): "
read ACCESS_TOKEN

echo -n "🔑 Digite sua API Key do Resend: "
read RESEND_API_KEY

echo -n "📧 Digite o email de origem (ex: no-reply@myfinance.com): "
read FROM_EMAIL

echo ""
echo "🌐 Project Reference: $PROJECT_REF"
echo "📧 From Email: $FROM_EMAIL"
echo ""

# Configuração SMTP
echo "🔄 Configurando SMTP..."

response=$(curl -s -w "\n%{http_code}" -X PATCH \
  "https://api.supabase.com/v1/projects/$PROJECT_REF/config/auth" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"external_email_enabled\": true,
    \"mailer_secure_email_change_enabled\": true,
    \"mailer_autoconfirm\": false,
    \"smtp_admin_email\": \"$FROM_EMAIL\",
    \"smtp_host\": \"smtp.resend.com\",
    \"smtp_port\": 587,
    \"smtp_user\": \"resend\",
    \"smtp_pass\": \"$RESEND_API_KEY\",
    \"smtp_sender_name\": \"MyFinance\"
  }")

# Separar resposta e status code
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | head -n -1)

echo "📊 Status Code: $http_code"
echo ""

if [ "$http_code" -eq 200 ]; then
    echo "✅ SMTP configurado com sucesso!"
    
    # Verificar configuração
    echo ""
    echo "🔍 Verificando configuração..."
    verify_response=$(curl -s -X GET \
      "https://api.supabase.com/v1/projects/$PROJECT_REF/config/auth" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json")
    
    echo "✅ Configuração atual:"
    echo "$verify_response" | jq -r '. | "   External email enabled: \(.external_email_enabled)"'
    echo "$verify_response" | jq -r '. | "   SMTP host: \(.smtp_host // "Não configurado")"'
    echo "$verify_response" | jq -r '. | "   SMTP port: \(.smtp_port // "Não configurado")"'
    echo "$verify_response" | jq -r '. | "   From email: \(.smtp_admin_email // "Não configurado")"'
    
else
    echo "❌ Erro ao configurar SMTP:"
    echo "$response_body"
fi

echo ""
echo "🧪 Para testar a configuração:"
echo "1. Acesse o Supabase Dashboard"
echo "2. Vá para Settings > Auth > Email Templates"
echo "3. Clique em 'Send test email' no template 'Confirm signup'"
echo ""
echo "🔧 Próximos passos:"
echo "1. Configure Site URL: http://localhost:3000"
echo "2. Configure Redirect URLs: http://localhost:3000/auth/confirm"
echo "3. Ative 'Enable email confirmations'"
echo "4. Registre um novo usuário para testar" 