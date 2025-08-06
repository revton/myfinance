#!/usr/bin/env python3
"""
Script para testar o fluxo completo de autenticação
Execute: uv run python scripts/test_complete_auth_flow.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_complete_auth_flow():
    """
    Testa o fluxo completo de autenticação
    """
    print("🧪 Testando Fluxo Completo de Autenticação")
    print("=" * 50)
    
    api_base_url = "http://localhost:8002"
    test_email = "teste_completo@exemplo.com"
    test_password = "Teste@123"
    test_name = "Usuário Teste Completo"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Testar registro
            print("🔄 1. Testando registro...")
            register_data = {
                "email": test_email,
                "password": test_password,
                "full_name": test_name
            }
            
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json=register_data,
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Registro bem-sucedido!")
                register_result = register_response.json()
                print(f"   User ID: {register_result.get('user_id', 'N/A')}")
                print(f"   Email: {register_result.get('email', 'N/A')}")
                print(f"   Message: {register_result.get('message', 'N/A')}")
                
                # 2. Testar login imediatamente
                print("\n🔄 2. Testando login...")
                login_data = {
                    "email": test_email,
                    "password": test_password
                }
                
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json=login_data,
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("✅ Login bem-sucedido!")
                    login_result = login_response.json()
                    access_token = login_result.get('access_token')
                    print(f"   Token: {access_token[:50]}..." if access_token else "   Token: N/A")
                    print(f"   User ID: {login_result.get('user', {}).get('id', 'N/A')}")
                    print(f"   Email: {login_result.get('user', {}).get('email', 'N/A')}")
                    print(f"   Nome: {login_result.get('user', {}).get('full_name', 'N/A')}")
                    
                    # 3. Testar acesso ao perfil
                    print("\n🔄 3. Testando acesso ao perfil...")
                    if access_token:
                        profile_response = await client.get(
                            f"{api_base_url}/auth/profile",
                            headers={
                                "Authorization": f"Bearer {access_token}"
                            },
                            timeout=30.0
                        )
                        
                        print(f"📊 Profile Status: {profile_response.status_code}")
                        
                        if profile_response.status_code == 200:
                            print("✅ Perfil acessado com sucesso!")
                            profile_data = profile_response.json()
                            print(f"   Email: {profile_data.get('email', 'N/A')}")
                            print(f"   Nome: {profile_data.get('full_name', 'N/A')}")
                            print(f"   Moeda: {profile_data.get('currency', 'N/A')}")
                            print(f"   Timezone: {profile_data.get('timezone', 'N/A')}")
                        else:
                            print(f"❌ Erro ao acessar perfil: {profile_response.status_code}")
                            print(f"   Response: {profile_response.text}")
                    else:
                        print("❌ Token não encontrado no login")
                        
                else:
                    print(f"❌ Login falhou: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            else:
                print(f"❌ Registro falhou: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

async def test_existing_user():
    """
    Testa login com usuário existente
    """
    print("\n🧪 Testando Login com Usuário Existente")
    print("=" * 50)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "4b6e3gmR$"
    
    try:
        async with httpx.AsyncClient() as client:
            # Testar login
            print("🔄 Testando login...")
            login_data = {
                "email": test_email,
                "password": test_password
            }
            
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json=login_data,
                timeout=30.0
            )
            
            print(f"📊 Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Login bem-sucedido!")
                login_result = login_response.json()
                access_token = login_result.get('access_token')
                print(f"   Token: {access_token[:50]}..." if access_token else "   Token: N/A")
                print(f"   User ID: {login_result.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {login_result.get('user', {}).get('email', 'N/A')}")
                print(f"   Nome: {login_result.get('user', {}).get('full_name', 'N/A')}")
                
                # Testar perfil
                if access_token:
                    profile_response = await client.get(
                        f"{api_base_url}/auth/profile",
                        headers={
                            "Authorization": f"Bearer {access_token}"
                        },
                        timeout=30.0
                    )
                    
                    if profile_response.status_code == 200:
                        print("✅ Perfil acessado com sucesso!")
                    else:
                        print(f"❌ Erro ao acessar perfil: {profile_response.status_code}")
                        
            else:
                print(f"❌ Login falhou: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste Completo de Autenticação")
    print("💡 Testa registro, login e acesso ao perfil")
    print()
    
    # Testar usuário existente primeiro
    await test_existing_user()
    
    # Testar fluxo completo
    await test_complete_auth_flow()
    
    print("\n🎉 Teste concluído!")
    print("💡 Se o registro falhar, use o Swagger UI em http://localhost:8002/docs")

if __name__ == "__main__":
    asyncio.run(main()) 