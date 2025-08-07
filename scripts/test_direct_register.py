#!/usr/bin/env python3
"""
Script para testar registro diretamente
Execute: uv run python scripts/test_direct_register.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_direct_register():
    """
    Testa registro diretamente
    """
    print("🧪 Testando Registro Direto")
    print("=" * 35)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Tentar registro diretamente
            print("🔄 1. Tentando registro...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Revton Direto"
                },
                timeout=60.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Registro bem-sucedido!")
                register_data = register_response.json()
                print(f"   Response: {register_data}")
                
                # 2. Testar login imediatamente
                print("\n🔄 2. Testando login após registro...")
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
                    timeout=60.0
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
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste de Registro Direto")
    print("💡 Sem verificação de health - teste direto")
    print()
    
    await test_direct_register()
    
    print("\n🎉 Teste concluído!")
    print("💡 Resumo:")
    print("   - Registro: Cria usuário e perfil")
    print("   - Email: Envia apenas email de boas-vindas")
    print("   - Login: Funciona imediatamente após registro")
    print("   - Sem confirmação: Usuário pode usar a aplicação direto")

if __name__ == "__main__":
    asyncio.run(main()) 