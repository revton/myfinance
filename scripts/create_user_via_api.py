#!/usr/bin/env python3
"""
Script para criar usuário via API do Supabase
Execute: uv run python scripts/create_user_via_api.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def create_user_via_supabase_api():
    """
    Cria usuário diretamente via API do Supabase
    """
    print("🔧 Criando Usuário via API do Supabase")
    print("=" * 45)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 Supabase URL: {supabase_url}")
    print()
    
    if not supabase_url or not supabase_key:
        print("❌ Configuração do Supabase não encontrada")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Criar usuário via Supabase Auth API
            print("🔄 1. Criando usuário via Supabase Auth...")
            auth_response = await client.post(
                f"{supabase_url}/auth/v1/signup",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                },
                json={
                    "email": test_email,
                    "password": test_password,
                    "data": {
                        "full_name": "Revton Dev API"
                    }
                },
                timeout=30.0
            )
            
            print(f"📊 Auth Status: {auth_response.status_code}")
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                print("✅ Usuário criado via Supabase Auth!")
                print(f"   User ID: {auth_data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email Confirmed: {auth_data.get('user', {}).get('email_confirmed_at', 'N/A')}")
                
                # 2. Testar login via Supabase
                print("\n🔄 2. Testando login via Supabase...")
                login_response = await client.post(
                    f"{supabase_url}/auth/v1/token?grant_type=password",
                    headers={
                        "apikey": supabase_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    login_data = login_response.json()
                    print("✅ Login via Supabase funcionou!")
                    print(f"   Access Token: {login_data.get('access_token', 'N/A')[:20]}...")
                    
                    # 3. Testar login via nosso backend
                    print("\n🔄 3. Testando login via nosso backend...")
                    backend_response = await client.post(
                        "http://localhost:8002/auth/login",
                        json={
                            "email": test_email,
                            "password": test_password
                        },
                        timeout=30.0
                    )
                    
                    print(f"📊 Backend Login Status: {backend_response.status_code}")
                    
                    if backend_response.status_code == 200:
                        print("✅ Login via backend funcionou!")
                        print("🎉 Usuário criado e funcionando!")
                    else:
                        print(f"❌ Login via backend falha: {backend_response.status_code}")
                        print(f"   Response: {backend_response.text}")
                        
                else:
                    print(f"❌ Login via Supabase falha: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            elif auth_response.status_code == 400:
                print("⚠️ Usuário já existe, tentando login...")
                
                # Tentar login mesmo assim
                login_response = await client.post(
                    f"{supabase_url}/auth/v1/token?grant_type=password",
                    headers={
                        "apikey": supabase_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30.0
                )
                
                if login_response.status_code == 200:
                    print("✅ Login funcionou!")
                    print("🎉 Usuário já existia e está funcionando!")
                else:
                    print(f"❌ Login falha: {login_response.status_code}")
                    
            else:
                print(f"❌ Erro na criação: {auth_response.status_code}")
                print(f"   Response: {auth_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_user_status():
    """
    Verifica status do usuário
    """
    print("\n🔍 Verificando Status do Usuário")
    print("=" * 35)
    
    try:
        # Verificar via MCP
        import subprocess
        result = subprocess.run([
            "uv", "run", "python", "-c", 
            "import os; from dotenv import load_dotenv; load_dotenv(); print('SUPABASE_URL:', os.getenv('SUPABASE_URL'))"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Configuração do Supabase encontrada")
            print("💡 Verifique no Supabase Dashboard:")
            print("   1. Authentication > Users")
            print("   2. Deve mostrar: revtonbr@gmail.com")
            print("   3. Email Confirmed deve estar preenchido")
        else:
            print("❌ Erro ao verificar configuração")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Criação de Usuário via API do Supabase")
    print()
    
    # Criar usuário
    await create_user_via_supabase_api()
    
    # Verificar status
    await check_user_status()
    
    print("\n🎉 Processo concluído!")
    print("💡 Resumo:")
    print("   - Se o login funcionar: Usuário criado ✅")
    print("   - Se o login falhar: Pode precisar limpeza manual")
    print("   - Verifique no Supabase Dashboard")

if __name__ == "__main__":
    asyncio.run(main()) 