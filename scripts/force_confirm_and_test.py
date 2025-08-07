#!/usr/bin/env python3
"""
Script para forçar confirmação de email e testar login
Execute: uv run python scripts/force_confirm_and_test.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def force_confirm_email():
    """
    Força a confirmação do email via endpoint do backend
    """
    print("🔧 Forçando Confirmação de Email")
    print("=" * 35)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Forçar confirmação
            print("🔄 Forçando confirmação de email...")
            confirm_response = await client.post(
                f"{api_base_url}/auth/force-confirm-email",
                json={"email": test_email},
                timeout=30.0
            )
            
            print(f"📊 Status Code: {confirm_response.status_code}")
            
            if confirm_response.status_code == 200:
                print("✅ Email confirmado com sucesso!")
                print(f"   Response: {confirm_response.json()}")
            else:
                print(f"❌ Erro ao confirmar email: {confirm_response.status_code}")
                print(f"   Response: {confirm_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False
    
    return True

async def test_login():
    """
    Testa o login após confirmação
    """
    print("\n🧪 Testando Login")
    print("=" * 20)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    try:
        async with httpx.AsyncClient() as client:
            # Tentar login
            print("🔄 Tentando login...")
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json={
                    "email": test_email,
                    "password": test_password
                },
                timeout=30.0
            )
            
            print(f"📊 Status Code: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Login realizado com sucesso!")
                data = login_response.json()
                print(f"   Access Token: {data.get('access_token', 'N/A')[:30]}...")
                print(f"   Refresh Token: {data.get('refresh_token', 'N/A')[:30]}...")
                print(f"   User ID: {data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {data.get('user', {}).get('email', 'N/A')}")
                
                # Testar endpoint protegido
                print("\n🔄 Testando endpoint protegido...")
                headers = {"Authorization": f"Bearer {data.get('access_token')}"}
                me_response = await client.get(
                    f"{api_base_url}/auth/me",
                    headers=headers,
                    timeout=30.0
                )
                
                print(f"📊 Me Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    print("✅ Endpoint protegido acessado com sucesso!")
                    me_data = me_response.json()
                    print(f"   User: {me_data.get('email', 'N/A')}")
                else:
                    print(f"❌ Erro no endpoint protegido: {me_response.status_code}")
                
                return True
                
            else:
                print(f"❌ Erro no login: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

async def test_user_profile():
    """
    Testa o perfil do usuário
    """
    print("\n👤 Testando Perfil do Usuário")
    print("=" * 30)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    try:
        async with httpx.AsyncClient() as client:
            # Fazer login primeiro
            print("🔄 Fazendo login para testar perfil...")
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json={
                    "email": test_email,
                    "password": test_password
                },
                timeout=30.0
            )
            
            if login_response.status_code != 200:
                print("❌ Falha no login para testar perfil")
                return
            
            data = login_response.json()
            headers = {"Authorization": f"Bearer {data.get('access_token')}"}
            
            # Testar perfil
            print("🔄 Obtendo perfil do usuário...")
            profile_response = await client.get(
                f"{api_base_url}/auth/profile",
                headers=headers,
                timeout=30.0
            )
            
            print(f"📊 Profile Status: {profile_response.status_code}")
            
            if profile_response.status_code == 200:
                print("✅ Perfil obtido com sucesso!")
                profile_data = profile_response.json()
                print(f"   ID: {profile_data.get('id', 'N/A')}")
                print(f"   Email: {profile_data.get('email', 'N/A')}")
                print(f"   Full Name: {profile_data.get('full_name', 'N/A')}")
                print(f"   Created At: {profile_data.get('created_at', 'N/A')}")
            else:
                print(f"❌ Erro ao obter perfil: {profile_response.status_code}")
                print(f"   Response: {profile_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Forçar Confirmação e Testar Login")
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
    
    # Forçar confirmação
    success = await force_confirm_email()
    
    if success:
        # Testar login
        login_success = await test_login()
        
        if login_success:
            # Testar perfil
            await test_user_profile()
    
    print("\n🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique se o email chegou")
    print("   2. Teste o frontend se estiver rodando")
    print("   3. Verifique os logs do Supabase se necessário")

if __name__ == "__main__":
    asyncio.run(main()) 