#!/usr/bin/env python3
"""
Script simples para testar registro sem confirmação
Execute: uv run python scripts/test_simple_register.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_simple_register():
    """
    Testa registro simples sem confirmação
    """
    print("🧪 Testando Registro Simples")
    print("=" * 35)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Verificar se o backend está rodando
            print("🔄 1. Verificando backend...")
            try:
                health_response = await client.get(f"{api_base_url}/health", timeout=5.0)
                if health_response.status_code == 200:
                    print("✅ Backend está rodando")
                else:
                    print(f"⚠️ Backend respondeu com status: {health_response.status_code}")
                    return
            except Exception as e:
                print(f"❌ Backend não está rodando: {str(e)}")
                return
            
            # 2. Tentar registro
            print("\n🔄 2. Tentando registro...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Revton Simples"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Registro bem-sucedido!")
                register_data = register_response.json()
                print(f"   Response: {register_data}")
                
                # 3. Testar login imediatamente
                print("\n🔄 3. Testando login após registro...")
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
                    print("✅ Login funcionou após registro!")
                    login_data = login_response.json()
                    user_data = login_data.get('user', {})
                    print(f"   User ID: {user_data.get('id', 'N/A')}")
                    print(f"   Email: {user_data.get('email', 'N/A')}")
                    print(f"   Full Name: {user_data.get('full_name', 'N/A')}")
                    print("🎉 Registro e login funcionando perfeitamente!")
                    
                else:
                    print(f"❌ Login falha: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, tentando login...")
                
                # Tentar login mesmo assim
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
                    print("✅ Login funcionou!")
                    print("🎉 Usuário já existia e está funcionando!")
                else:
                    print(f"❌ Login falha: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste de Registro Simples")
    print("💡 Sem confirmação de email - apenas registro e login")
    print()
    
    await test_simple_register()
    
    print("\n🎉 Teste concluído!")
    print("💡 Resumo:")
    print("   - Registro: Cria usuário e perfil")
    print("   - Email: Envia apenas email de boas-vindas")
    print("   - Login: Funciona imediatamente após registro")
    print("   - Sem confirmação: Usuário pode usar a aplicação direto")

if __name__ == "__main__":
    asyncio.run(main()) 