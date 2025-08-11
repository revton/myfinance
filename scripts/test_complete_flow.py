#!/usr/bin/env python3
"""
Script para testar o fluxo completo de registro e confirmação de email
Execute: uv run python scripts/test_complete_flow.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_user_registration():
    """
    Testa o registro de usuário
    """
    print("🧪 Testando Registro de Usuário")
    print("=" * 35)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Registrar usuário
            print("🔄 Registrando usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Usuário Teste"
                },
                timeout=30.0
            )
            
            print(f"📊 Status Code: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                print("📧 Email de confirmação enviado")
                
                # Tentar login (deve falhar sem confirmação)
                print("\n🔄 Tentando login sem confirmação...")
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 401:
                    print("✅ Login bloqueado corretamente (email não confirmado)")
                else:
                    print(f"⚠️ Login inesperado: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                
                # Reenviar email de confirmação
                print("\n🔄 Reenviando email de confirmação...")
                resend_response = await client.post(
                    f"{api_base_url}/auth/resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                print(f"📊 Resend Status: {resend_response.status_code}")
                
                if resend_response.status_code == 200:
                    print("✅ Email de confirmação reenviado!")
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    print(f"   Response: {resend_response.text}")
                
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe ou dados inválidos")
                print(f"   Response: {register_response.text}")
                
                # Tentar login para verificar status
                print("\n🔄 Verificando status do usuário existente...")
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("✅ Usuário já está logado (email confirmado)")
                    data = login_response.json()
                    print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
                elif login_response.status_code == 401:
                    print("⚠️ Usuário existe mas email não confirmado")
                    
                    # Reenviar confirmação
                    print("\n🔄 Reenviando email de confirmação...")
                    resend_response = await client.post(
                        f"{api_base_url}/auth/resend-confirmation",
                        json={"email": test_email},
                        timeout=30.0
                    )
                    
                    print(f"📊 Resend Status: {resend_response.status_code}")
                    
                    if resend_response.status_code == 200:
                        print("✅ Email de confirmação reenviado!")
                    else:
                        print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_supabase_logs():
    """
    Verifica logs do Supabase
    """
    print("\n📋 Verificação de Logs")
    print("=" * 25)
    
    print("🔍 Para verificar os logs:")
    print("1. Acesse: https://supabase.com/dashboard/project/qgkifpsimkcsfrwwyqsd/logs")
    print("2. Filtre por 'Auth'")
    print("3. Verifique se há erros de envio de email")
    print("4. Verifique se há tentativas de login")
    print()

async def test_email_templates():
    """
    Testa templates de email
    """
    print("📧 Teste de Templates de Email")
    print("=" * 30)
    
    print("🧪 Para testar os templates:")
    print("1. Acesse: https://supabase.com/dashboard/project/qgkifpsimkcsfrwwyqsd/auth/templates")
    print("2. Clique em 'Confirm signup'")
    print("3. Clique em 'Send test email'")
    print("4. Digite: revtonbr@gmail.com")
    print("5. Verifique se o email chega")
    print()

async def main():
    """
    Função principal
    """
    print("🚀 Teste Completo do Fluxo de Autenticação")
    print()
    
    # Verificar se o backend está rodando
    print("🔍 Verificando se o backend está rodando...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8002/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Backend está rodando")
            else:
                print("⚠️ Backend respondeu mas com status inesperado")
    except Exception as e:
        print("❌ Backend não está rodando")
        print("💡 Execute: uv run invoke backend")
        return
    
    print()
    
    # Testar registro
    await test_user_registration()
    
    # Verificar logs
    await check_supabase_logs()
    
    # Testar templates
    await test_email_templates()
    
    print("🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique sua caixa de email")
    print("   2. Clique no link de confirmação")
    print("   3. Tente fazer login novamente")
    print("   4. Verifique os logs do Supabase se necessário")

if __name__ == "__main__":
    asyncio.run(main()) 