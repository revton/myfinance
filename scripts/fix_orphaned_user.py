#!/usr/bin/env python3
"""
Script para corrigir usuário órfão automaticamente
Execute: uv run python scripts/fix_orphaned_user.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def fix_orphaned_user():
    """
    Corrige usuário órfão recriando o registro
    """
    print("🔧 Corrigindo Usuário Órfão")
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
            
            # 2. Tentar registrar novamente (pode falhar se já existe)
            print("\n🔄 2. Tentando registrar usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Revton Dev Corrigido"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                register_data = register_response.json()
                user_data = register_data.get('user', {})
                print(f"   User ID: {user_data.get('id', 'N/A')}")
                
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
                    print("🎉 Usuário corrigido com sucesso!")
                else:
                    print(f"❌ Login ainda falha: {login_response.status_code}")
                    print("   Response: ", login_response.text)
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, testando login...")
                
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
                    print("🎉 Usuário já estava correto!")
                else:
                    print(f"❌ Login falha: {login_response.status_code}")
                    print("   Response: ", login_response.text)
                    print("💡 Pode ser necessário limpeza manual no Supabase")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print("   Response: ", register_response.text)
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_confirmation_after_fix():
    """
    Testa confirmação após correção
    """
    print("\n🔄 Testando Confirmação Após Correção")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Reenviar email
            print("🔄 1. Reenviando email...")
            resend_response = await client.post(
                f"{api_base_url}/auth/custom-resend-confirmation",
                json={"email": test_email},
                timeout=30.0
            )
            
            if resend_response.status_code == 200:
                resend_data = resend_response.json()
                test_token = resend_data.get('token', '')
                
                if test_token:
                    print("✅ Email reenviado!")
                    print(f"   Token: {test_token[:20]}...")
                    
                    # 2. Construir URL
                    confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                    print(f"\n🔗 URL de Confirmação:")
                    print(f"   {confirmation_url}")
                    
                    # 3. Testar confirmação
                    print(f"\n🔄 2. Testando confirmação...")
                    confirm_response = await client.get(confirmation_url, timeout=30.0)
                    
                    print(f"📊 Confirm Status: {confirm_response.status_code}")
                    
                    if confirm_response.status_code == 200:
                        print("✅ Confirmação realizada com sucesso!")
                        confirm_data = confirm_response.json()
                        print(f"   Message: {confirm_data.get('message', 'N/A')}")
                        
                        # 4. Verificar login após confirmação
                        print(f"\n🔄 3. Verificando login após confirmação...")
                        login_response = await client.post(
                            f"{api_base_url}/auth/login",
                            json={
                                "email": test_email,
                                "password": "Minha@Senha1"
                            },
                            timeout=30.0
                        )
                        
                        if login_response.status_code == 200:
                            print("✅ Login funcionou após confirmação!")
                            print("🎉 Processo completo funcionou!")
                        else:
                            print(f"❌ Login ainda falha: {login_response.status_code}")
                            
                    else:
                        print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                        print(f"   Response: {confirm_response.text}")
                        
                else:
                    print("❌ Token não encontrado")
                    
            else:
                print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Correção de Usuário Órfão")
    print()
    
    # Corrigir usuário
    await fix_orphaned_user()
    
    # Testar confirmação
    await test_confirmation_after_fix()
    
    print("\n🎉 Processo concluído!")
    print("💡 Resumo:")
    print("   - Se o login funcionar: Usuário corrigido ✅")
    print("   - Se o login falhar: Pode precisar limpeza manual")
    print("   - O link de confirmação funcionará após correção")

if __name__ == "__main__":
    asyncio.run(main()) 