#!/usr/bin/env python3
"""
Script para testar o sistema de email customizado
Execute: uv run python scripts/test_custom_email.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_custom_email_system():
    """
    Testa o sistema de email customizado completo
    """
    print("🧪 Testando Sistema de Email Customizado")
    print("=" * 45)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Registrar usuário (com email customizado)
            print("🔄 1. Registrando usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Usuário Email Customizado"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                register_data = register_response.json()
                print(f"   User ID: {register_data.get('user', {}).get('id', 'N/A')}")
                
                # 2. Reenviar email customizado
                print("\n🔄 2. Reenviando email customizado...")
                resend_response = await client.post(
                    f"{api_base_url}/auth/custom-resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                print(f"📊 Resend Status: {resend_response.status_code}")
                
                if resend_response.status_code == 200:
                    print("✅ Email customizado reenviado!")
                    resend_data = resend_response.json()
                    print(f"   Message: {resend_data.get('message', 'N/A')}")
                    
                    # Token para teste (se retornado)
                    if 'token' in resend_data:
                        test_token = resend_data['token']
                        print(f"   Token: {test_token[:20]}...")
                        
                        # 3. Testar confirmação com token
                        print(f"\n🔄 3. Testando confirmação com token...")
                        confirm_response = await client.post(
                            f"{api_base_url}/auth/custom-confirm-email",
                            json={"token": test_token},
                            timeout=30.0
                        )
                        
                        print(f"📊 Confirm Status: {confirm_response.status_code}")
                        
                        if confirm_response.status_code == 200:
                            print("✅ Email confirmado com sucesso!")
                            confirm_data = confirm_response.json()
                            print(f"   Message: {confirm_data.get('message', 'N/A')}")
                            print(f"   Email: {confirm_data.get('email', 'N/A')}")
                            
                            # 4. Testar login após confirmação
                            print(f"\n🔄 4. Testando login após confirmação...")
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
                                print("✅ Login realizado com sucesso!")
                                login_data = login_response.json()
                                print(f"   Access Token: {login_data.get('access_token', 'N/A')[:30]}...")
                                print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                                
                                # 5. Testar endpoint protegido
                                print(f"\n🔄 5. Testando endpoint protegido...")
                                headers = {"Authorization": f"Bearer {login_data.get('access_token')}"}
                                me_response = await client.get(
                                    f"{api_base_url}/auth/me",
                                    headers=headers,
                                    timeout=30.0
                                )
                                
                                print(f"📊 Me Status: {me_response.status_code}")
                                
                                if me_response.status_code == 200:
                                    print("✅ Endpoint protegido acessado!")
                                    me_data = me_response.json()
                                    print(f"   User: {me_data.get('email', 'N/A')}")
                                else:
                                    print(f"❌ Erro no endpoint protegido: {me_response.status_code}")
                                    
                            else:
                                print(f"❌ Erro no login: {login_response.status_code}")
                                print(f"   Response: {login_response.text}")
                                
                        else:
                            print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                            print(f"   Response: {confirm_response.text}")
                            
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    print(f"   Response: {resend_response.text}")
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, testando apenas email customizado...")
                
                # Testar apenas reenvio de email
                print("\n🔄 Reenviando email customizado...")
                resend_response = await client.post(
                    f"{api_base_url}/auth/custom-resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                print(f"📊 Resend Status: {resend_response.status_code}")
                
                if resend_response.status_code == 200:
                    print("✅ Email customizado reenviado!")
                    resend_data = resend_response.json()
                    print(f"   Message: {resend_data.get('message', 'N/A')}")
                    
                    if 'token' in resend_data:
                        print(f"   Token: {resend_data['token'][:20]}...")
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    print(f"   Response: {resend_response.text}")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_email_templates():
    """
    Testa os templates de email
    """
    print("\n📧 Teste de Templates de Email")
    print("=" * 30)
    
    print("🧪 Para testar os templates:")
    print("1. Verifique sua caixa de email")
    print("2. Clique no link de confirmação")
    print("3. Verifique se o email tem o design correto")
    print("4. Teste o link de confirmação")
    print()

async def main():
    """
    Função principal
    """
    print("🚀 Teste do Sistema de Email Customizado")
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
    
    # Testar sistema de email
    await test_custom_email_system()
    
    # Testar templates
    await test_email_templates()
    
    print("🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique sua caixa de email")
    print("   2. Teste o link de confirmação")
    print("   3. Verifique se o login funciona após confirmação")
    print("   4. Teste o frontend se estiver rodando")

if __name__ == "__main__":
    asyncio.run(main()) 