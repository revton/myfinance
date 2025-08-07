#!/usr/bin/env python3
"""
Script para testar login após criar usuário manualmente no Supabase
Execute: uv run python scripts/test_login_after_manual_create.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_login():
    """
    Testa login após criar usuário manualmente
    """
    print("🧪 Testando Login Após Criação Manual")
    print("=" * 50)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Testar login
            print("🔄 1. Testando login...")
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json={
                    "email": test_email,
                    "password": test_password
                },
                timeout=60.0
            )
            
            print(f"📊 Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Login bem-sucedido!")
                login_data = login_response.json()
                print(f"   Token: {login_data.get('access_token', 'N/A')[:50]}...")
                print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {login_data.get('user', {}).get('email', 'N/A')}")
                print(f"   Nome: {login_data.get('user', {}).get('full_name', 'N/A')}")
                
                # 2. Testar acesso ao perfil
                print("\n🔄 2. Testando acesso ao perfil...")
                token = login_data.get('access_token')
                if token:
                    profile_response = await client.get(
                        f"{api_base_url}/auth/profile",
                        headers={
                            "Authorization": f"Bearer {token}"
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
                print(f"❌ Login falhou: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                
                # 3. Verificar se usuário existe no Supabase
                print("\n🔄 3. Verificando status do usuário...")
                print("💡 Execute no Supabase Dashboard SQL Editor:")
                print("""
SELECT id, email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';
                """)
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste de Login Após Criação Manual")
    print("💡 Testa login após criar usuário manualmente no Supabase")
    print()
    
    await test_login()
    
    print("\n🎉 Teste concluído!")
    print("💡 Se o login falhar, execute o script SQL para criar o usuário:")
    print("   scripts/create_user_manually.sql")

if __name__ == "__main__":
    asyncio.run(main()) 