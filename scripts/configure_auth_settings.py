#!/usr/bin/env python3
"""
Script para configurar Site URL e Redirect URLs via API do Supabase
Execute: uv run python scripts/configure_auth_settings.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def configure_auth_settings():
    """
    Configura Site URL e Redirect URLs via API do Supabase
    """
    print("🔧 Configurando Auth Settings via API do Supabase")
    print("=" * 55)
    
    # Configurações
    project_ref = "qgkifpsimkcsfrwwyqsd"
    
    # Obter Access Token do .env
    access_token = os.getenv("SUPABASE_ACCESS_TOKEN")
    if not access_token:
        print("❌ SUPABASE_ACCESS_TOKEN não encontrada no arquivo .env")
        return
    
    print(f"🌐 Project Reference: {project_ref}")
    print()
    
    # Configurações de Auth
    auth_config = {
        "site_url": "http://localhost:3000",
        "redirect_urls": [
            "http://localhost:3000/auth/confirm",
            "http://localhost:3000/auth/callback",
            "http://localhost:3000/auth/reset-password"
        ],
        "enable_confirmations": True,
        "enable_signup": True,
        "enable_email_change": True,
        "enable_email_confirmations": True
    }
    
    print("📋 Configurações de Auth:")
    print(f"   Site URL: {auth_config['site_url']}")
    print(f"   Redirect URLs: {auth_config['redirect_urls']}")
    print(f"   Enable confirmations: {auth_config['enable_confirmations']}")
    print(f"   Enable signup: {auth_config['enable_signup']}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Configurar Auth Settings
            print("🔄 Configurando Auth Settings...")
            response = await client.patch(
                f"https://api.supabase.com/v1/projects/{project_ref}/config/auth",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json=auth_config,
                timeout=30.0
            )
            
            if response.status_code == 200:
                print("✅ Auth Settings configurados com sucesso!")
                
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
                    print(f"   Site URL: {config.get('site_url', 'Não configurado')}")
                    print(f"   Redirect URLs: {config.get('redirect_urls', [])}")
                    print(f"   Enable confirmations: {config.get('enable_confirmations', False)}")
                    print(f"   Enable signup: {config.get('enable_signup', False)}")
                    print(f"   Enable email confirmations: {config.get('enable_email_confirmations', False)}")
                else:
                    print(f"⚠️ Não foi possível verificar a configuração: {verify_response.status_code}")
                
            else:
                print(f"❌ Erro ao configurar Auth Settings: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_email_templates():
    """
    Testa os templates de email
    """
    print("\n🧪 Testando Templates de Email")
    print("=" * 35)
    
    print("📋 Para testar os templates:")
    print("1. Acesse: https://supabase.com/dashboard/project/qgkifpsimkcsfrwwyqsd/auth/templates")
    print("2. Clique em 'Confirm signup'")
    print("3. Clique em 'Send test email'")
    print("4. Digite seu email: revtonbr@gmail.com")
    print("5. Verifique se o email chega na caixa de entrada")
    print()
    print("🔧 Próximos passos:")
    print("1. Registre um novo usuário para testar o fluxo completo")
    print("2. Verifique os logs em Dashboard > Logs > Auth")
    print("3. Se necessário, ajuste as configurações")

async def main():
    """
    Função principal
    """
    print("🚀 Configuração de Auth Settings via API")
    print()
    
    # Configurar Auth Settings
    await configure_auth_settings()
    
    # Testar templates
    await test_email_templates()
    
    print("\n🎉 Configuração concluída!")
    print("💡 Agora você pode:")
    print("   1. Testar os templates de email")
    print("   2. Registrar um novo usuário")
    print("   3. Verificar se o email de confirmação chega")

if __name__ == "__main__":
    asyncio.run(main()) 