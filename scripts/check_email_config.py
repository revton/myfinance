#!/usr/bin/env python3
"""
Script para verificar e configurar as configurações de email no Supabase
Execute: uv run python scripts/check_email_config.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def check_email_configuration():
    """
    Verifica as configurações de email no Supabase
    """
    try:
        # Configurações do Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Erro: Configuração do Supabase não encontrada")
            return
        
        print("🔧 Verificando configurações de email no Supabase...")
        print(f"   Supabase URL: {supabase_url}")
        
        async with httpx.AsyncClient() as client:
            # Verificar configurações de autenticação
            response = await client.get(
                f"{supabase_url}/auth/v1/settings",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                settings = response.json()
                print("✅ Configurações obtidas com sucesso")
                print(f"   Site URL: {settings.get('site_url', '❌ Não configurado')}")
                print(f"   Enable confirmations: {settings.get('enable_confirmations', '❌ Não informado')}")
                print(f"   Enable signup: {settings.get('enable_signup', '❌ Não informado')}")
                
                # Verificar se as configurações estão corretas
                issues = []
                if not settings.get('site_url'):
                    issues.append("Site URL não configurado")
                if not settings.get('enable_confirmations'):
                    issues.append("Email confirmations não habilitado")
                
                if issues:
                    print("\n❌ Problemas encontrados:")
                    for issue in issues:
                        print(f"   - {issue}")
                    print("\n📋 Soluções:")
                    print("   1. Acesse Supabase Dashboard > Settings > Auth")
                    print("   2. Configure Site URL: http://localhost:3000")
                    print("   3. Ative 'Enable email confirmations'")
                    print("   4. Configure Email Provider (SMTP/Resend/SendGrid)")
                else:
                    print("\n✅ Configurações parecem estar corretas")
                    
            else:
                print(f"❌ Erro ao obter configurações: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro interno: {str(e)}")

async def test_email_template():
    """
    Testa o template de email de confirmação
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        print("\n📧 Testando template de email...")
        
        async with httpx.AsyncClient() as client:
            # Tentar obter informações sobre templates
            response = await client.get(
                f"{supabase_url}/auth/v1/settings",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                print("ℹ️ Para verificar templates de email:")
                print("   1. Acesse Supabase Dashboard > Settings > Auth > Email Templates")
                print("   2. Verifique se o template 'Confirm signup' está configurado")
                print("   3. Teste o template clicando em 'Send test email'")
            else:
                print(f"❌ Erro ao verificar templates: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro ao testar template: {str(e)}")

async def check_email_provider():
    """
    Verifica o provedor de email configurado
    """
    try:
        print("\n📮 Verificando provedor de email...")
        print("ℹ️ Para configurar provedor de email:")
        print("   1. Acesse Supabase Dashboard > Settings > Auth > SMTP Settings")
        print("   2. Configure um dos provedores:")
        print("      - SMTP (Gmail, Outlook, etc.)")
        print("      - Resend (recomendado)")
        print("      - SendGrid")
        print("      - Mailgun")
        print("   3. Teste a configuração")
        
    except Exception as e:
        print(f"❌ Erro ao verificar provedor: {str(e)}")

async def main():
    """
    Função principal
    """
    print("📧 Verificação de Configurações de Email")
    print("=" * 50)
    
    # Verificar configurações
    await check_email_configuration()
    
    # Testar template
    await test_email_template()
    
    # Verificar provedor
    await check_email_provider()
    
    print("\n📋 Resumo e Próximos Passos:")
    print("   1. Execute o script diagnose_email_confirmation.sql no Supabase")
    print("   2. Configure Site URL e Email Provider no Dashboard")
    print("   3. Teste o template de email")
    print("   4. Se necessário, force confirmação com force_confirm_email.sql")
    print("   5. Verifique logs em Dashboard > Logs > Auth")

if __name__ == "__main__":
    asyncio.run(main()) 