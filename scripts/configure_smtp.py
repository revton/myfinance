#!/usr/bin/env python3
"""
Script para configurar SMTP via API do Supabase
Execute: uv run python scripts/configure_smtp.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def configure_smtp():
    """
    Configura SMTP via API do Supabase
    """
    print("🔧 Configurando SMTP via API do Supabase")
    print("=" * 50)
    
    # Configurações
    project_ref = "qgkifpsimkcsfrwwyqsd"
    
    # Obter Access Token do .env
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    if not access_token:
        print("❌ SUPABASE_ACCESS_TOKEN não encontrada no arquivo .env")
        print("💡 Adicione SUPABASE_ACCESS_TOKEN=sbp_sua_token no arquivo .env")
        print("🔗 Obtenha o token em: https://supabase.com/dashboard/account/tokens")
        return
    
    if not access_token.startswith("sbp_"):
        print("❌ Token inválido. Deve começar com 'sbp_'")
        return
    
    print(f"🌐 Project Reference: {project_ref}")
    print()
    
    # Obter API Key do Resend do .env
    resend_api_key = os.getenv("RESEND_API_KEY")
    if not resend_api_key:
        print("❌ RESEND_API_KEY não encontrada no arquivo .env")
        print("💡 Adicione RESEND_API_KEY=sua_api_key no arquivo .env")
        return
    
    # Configuração do Resend (gratuito)
    smtp_config = {
        "external_email_enabled": True,
        "mailer_secure_email_change_enabled": True,
        "mailer_autoconfirm": False,
        "smtp_admin_email": "no-reply@myfinance.com",
        "smtp_host": "smtp.resend.com",
        "smtp_port": "587",
        "smtp_user": "resend",
        "smtp_pass": resend_api_key,
        "smtp_sender_name": "MyFinance"
    }
    
    print("\n📧 Configuração SMTP:")
    print(f"   Host: {smtp_config['smtp_host']}")
    print(f"   Port: {smtp_config['smtp_port']}")
    print(f"   User: {smtp_config['smtp_user']}")
    print(f"   From: {smtp_config['smtp_admin_email']}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Configurar SMTP
            print("🔄 Configurando SMTP...")
            response = await client.patch(
                f"https://api.supabase.com/v1/projects/{project_ref}/config/auth",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json=smtp_config,
                timeout=30.0
            )
            
            if response.status_code == 200:
                print("✅ SMTP configurado com sucesso!")
                
                # Verificar configuração
                print("\n🔍 Verificando configuração...")
                verify_response = await client.get(
                    f"https://api.supabase.com/v1/projects/{project_ref}/config/auth",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=30.0
                )
                
                if verify_response.status_code == 200:
                    config = verify_response.json()
                    print("✅ Configuração verificada:")
                    print(f"   External email enabled: {config.get('external_email_enabled', False)}")
                    print(f"   SMTP host: {config.get('smtp_host', 'Não configurado')}")
                    print(f"   SMTP port: {config.get('smtp_port', 'Não configurado')}")
                    print(f"   From email: {config.get('smtp_admin_email', 'Não configurado')}")
                else:
                    print(f"⚠️ Não foi possível verificar a configuração: {verify_response.status_code}")
                
            else:
                print(f"❌ Erro ao configurar SMTP: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_email_configuration():
    """
    Testa a configuração de email
    """
    print("\n🧪 Testando Configuração de Email")
    print("=" * 40)
    
    print("📋 Para testar a configuração:")
    print("1. Acesse o Supabase Dashboard")
    print("2. Vá para Settings > Auth > Email Templates")
    print("3. Clique em 'Send test email' no template 'Confirm signup'")
    print("4. Verifique se o email chega na caixa de entrada")
    print()
    print("🔧 Próximos passos:")
    print("1. Registre um novo usuário para testar o fluxo completo")
    print("2. Verifique os logs em Dashboard > Logs > Auth")
    print("3. Se necessário, ajuste as configurações")

async def main():
    """
    Função principal
    """
    print("🚀 Configuração de SMTP via API")
    print()
    
    # Configurar SMTP
    await configure_smtp()
    
    # Testar configuração
    await test_email_configuration()
    
    print("\n🎉 Configuração concluída!")
    print("💡 Lembre-se de configurar também:")
    print("   - Site URL: http://localhost:3000")
    print("   - Redirect URLs: http://localhost:3000/auth/confirm")
    print("   - Enable email confirmations: true")

if __name__ == "__main__":
    asyncio.run(main()) 