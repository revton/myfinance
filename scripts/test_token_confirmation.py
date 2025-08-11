#!/usr/bin/env python3
"""
Script para testar confirmação com token específico
Execute: uv run python scripts/test_token_confirmation.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_token_confirmation():
    """
    Testa a confirmação com um token específico
    """
    print("🧪 Testando Confirmação com Token")
    print("=" * 35)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_token = "aDns6XYz-GxJLQkxy_AIanz1HOr58Da2yKdmq054HMs"  # Token mais recente
    
    print(f"🔑 Token: {test_token[:20]}...")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Testar confirmação com token
            print("🔄 Testando confirmação com token...")
            confirm_response = await client.post(
                f"{api_base_url}/auth/custom-confirm-email",
                json={"token": test_token},
                timeout=30.0
            )
            
            print(f"📊 Confirm Status: {confirm_response.status_code}")
            print(f"📊 Response: {confirm_response.text}")
            
            if confirm_response.status_code == 200:
                print("✅ Email confirmado com sucesso!")
                confirm_data = confirm_response.json()
                print(f"   Message: {confirm_data.get('message', 'N/A')}")
                print(f"   Email: {confirm_data.get('email', 'N/A')}")
                
                # Testar login após confirmação
                print(f"\n🔄 Testando login após confirmação...")
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": "revtonbr@gmail.com",
                        "password": "Minha@Senha1"
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("✅ Login realizado com sucesso!")
                    login_data = login_response.json()
                    print(f"   Access Token: {login_data.get('access_token', 'N/A')[:30]}...")
                    print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                else:
                    print(f"❌ Erro no login: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            else:
                print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                print(f"   Response: {confirm_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_user_status():
    """
    Testa o status do usuário
    """
    print("\n👤 Testando Status do Usuário")
    print("=" * 30)
    
    try:
        async with httpx.AsyncClient() as client:
            # Tentar login para ver status
            print("🔄 Tentando login para verificar status...")
            login_response = await client.post(
                "http://localhost:8002/auth/login",
                json={
                    "email": "revtonbr@gmail.com",
                    "password": "Minha@Senha1"
                },
                timeout=30.0
            )
            
            print(f"📊 Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("✅ Usuário já está logado (email confirmado)")
                login_data = login_response.json()
                print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                print(f"   Email: {login_data.get('user', {}).get('email', 'N/A')}")
            elif login_response.status_code == 401:
                print("⚠️ Usuário existe mas email não confirmado")
            else:
                print(f"❌ Erro no login: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste de Confirmação com Token")
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
    
    # Testar status do usuário
    await test_user_status()
    
    # Testar confirmação com token
    await test_token_confirmation()
    
    print("\n🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique se o email chegou")
    print("   2. Teste o link de confirmação")
    print("   3. Verifique se o login funciona após confirmação")

if __name__ == "__main__":
    asyncio.run(main()) 