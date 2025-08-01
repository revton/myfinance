#!/bin/bash

# MyFinance Database Setup Script
# Script para configuração rápida do banco de dados

echo "🗄️ MyFinance - Configuração do Banco de Dados"
echo "=============================================="

# Verificar se as variáveis estão definidas
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ Variáveis de ambiente não configuradas!"
    echo ""
    echo "Configure as seguintes variáveis:"
    echo "export SUPABASE_URL='https://seu-projeto.supabase.co'"
    echo "export SUPABASE_ANON_KEY='sua-chave-anonima'"
    echo ""
    echo "Para encontrar suas credenciais:"
    echo "1. Acesse https://supabase.com"
    echo "2. Vá para seu projeto MyFinance"
    echo "3. Settings → API"
    echo "4. Copie Project URL e anon public key"
    exit 1
fi

echo "✅ Variáveis de ambiente configuradas"
echo "📍 SUPABASE_URL: ${SUPABASE_URL:0:30}..."
echo "🔑 SUPABASE_ANON_KEY: ${SUPABASE_ANON_KEY:0:20}..."
echo ""

# Verificar se Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale Python3 para continuar"
    exit 1
fi

echo "✅ Python3 encontrado"

# Verificar se o pacote supabase está instalado
if ! python3 -c "import supabase" 2>/dev/null; then
    echo "❌ Pacote supabase não instalado!"
    echo "Instalando supabase..."
    pip3 install supabase
    
    if [ $? -ne 0 ]; then
        echo "❌ Falha ao instalar supabase"
        echo "Execute manualmente: pip3 install supabase"
        exit 1
    fi
    
    echo "✅ Supabase instalado com sucesso"
else
    echo "✅ Pacote supabase já instalado"
fi

echo ""
echo "🔍 Executando verificação do banco de dados..."
echo ""

# Executar o script de verificação
python3 database/verify_database.py

# Verificar o resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Configuração concluída com sucesso!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Se a tabela não existir, execute o SQL no Supabase:"
    echo "   - Abra https://supabase.com → Seu Projeto → SQL Editor"
    echo "   - Cole o conteúdo de database/create_tables.sql"
    echo "   - Execute o script"
    echo ""
    echo "2. Teste sua API:"
    echo "   curl https://myfinance-backend-xcct.onrender.com/health"
    echo ""
    echo "3. Configure as mesmas variáveis no Render:"
    echo "   - Environment Variables:"
    echo "   - SUPABASE_URL=$SUPABASE_URL"
    echo "   - SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY"
else
    echo ""
    echo "🚨 Problemas encontrados na configuração!"
    echo ""
    echo "📋 Soluções comuns:"
    echo "1. Verifique se as credenciais estão corretas"
    echo "2. Execute o script create_tables.sql no Supabase"
    echo "3. Confirme se o projeto Supabase está ativo"
    echo "4. Teste a conexão local primeiro"
fi