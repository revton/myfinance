#!/usr/bin/env python3
"""
Script para testar o sistema de email com URL correta
Execute: uv run python scripts/test_email_with_correct_url.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_email_system():
    """
    Testa o sistema de email com URL correta
    """
    print("🧪 Testando Sistema de Email com URL Correta")
    print("=" * 50)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    
    # Verificar configurações
    frontend_url = os.getenv("FRONTEND_URL")
    api_port = os.getenv("API_PORT", "8002")
    print(f"🌐 FRONTEND_URL: {frontend_url or 'Não configurado'}")
    print(f"🔌 API_PORT: {api_port}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Registrar usuário
            print("🔄 1. Registrando usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Usuário Teste URL"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                
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
                    
                    # Token para teste
                    if 'token' in resend_data:
                        test_token = resend_data['token']
                        print(f"   Token: {test_token[:20]}...")
                        
                        # Mostrar URL de confirmação
                        if frontend_url:
                            confirmation_url = f"{frontend_url}/auth/custom-confirm-email/{test_token}"
                        else:
                            confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                        
                        print(f"\n🔗 URL de Confirmação:")
                        print(f"   {confirmation_url}")
                        
                        # 3. Testar confirmação
                        print(f"\n🔄 3. Testando confirmação...")
                        confirm_response = await client.get(
                            confirmation_url,
                            timeout=30.0
                        )
                        
                        print(f"📊 Confirm Status: {confirm_response.status_code}")
                        print(f"📊 Response: {confirm_response.text}")
                        
                        if confirm_response.status_code == 200:
                            print("✅ Email confirmado com sucesso!")
                            
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
                                print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                            else:
                                print(f"❌ Erro no login: {login_response.status_code}")
                                print(f"   Response: {login_response.text}")
                        else:
                            print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                            
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    print(f"   Response: {resend_response.text}")
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, testando apenas email...")
                
                # Testar apenas reenvio
                resend_response = await client.post(
                    f"{api_base_url}/auth/custom-resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                if resend_response.status_code == 200:
                    resend_data = resend_response.json()
                    if 'token' in resend_data:
                        test_token = resend_data['token']
                        if frontend_url:
                            confirmation_url = f"{frontend_url}/auth/custom-confirm-email/{test_token}"
                        else:
                            confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                        
                        print(f"\n🔗 URL de Confirmação:")
                        print(f"   {confirmation_url}")
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste do Sistema de Email com URL Correta")
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
    
    # Testar sistema
    await test_email_system()
    
    print("\n🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique o email recebido")
    print("   2. Teste o link de confirmação")
    print("   3. Verifique se a URL está correta")

if __name__ == "__main__":
    asyncio.run(main()) 