#!/usr/bin/env python3
"""
Script para testar após limpeza completa
Execute: uv run python scripts/test_after_cleanup.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_after_cleanup():
    """
    Testa após limpeza completa
    """
    print("🧪 Testando Após Limpeza Completa")
    print("=" * 40)
    
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
            
            # 2. Tentar registro limpo
            print("\n🔄 2. Tentando registro limpo...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Revton Limpo"
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
                    print(f"   Email Confirmed: {user_data.get('email_confirmed_at', 'N/A')}")
                    print("🎉 Usuário criado e funcionando!")
                    
                    # 4. Testar confirmação de email
                    print("\n🔄 4. Testando confirmação de email...")
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
                            
                            # Testar confirmação
                            confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                            confirm_response = await client.get(confirmation_url, timeout=30.0)
                            
                            print(f"📊 Confirm Status: {confirm_response.status_code}")
                            
                            if confirm_response.status_code == 200:
                                print("✅ Confirmação funcionou!")
                                print("🎉 Processo completo funcionando!")
                            else:
                                print(f"❌ Confirmação falha: {confirm_response.status_code}")
                                print(f"   Response: {confirm_response.text}")
                        else:
                            print("❌ Token não encontrado")
                    else:
                        print(f"❌ Reenvio falha: {resend_response.status_code}")
                        
                else:
                    print(f"❌ Login ainda falha: {login_response.status_code}")
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

async def provide_final_instructions():
    """
    Fornece instruções finais
    """
    print("\n📋 Instruções Finais")
    print("=" * 25)
    
    print("🔧 Se o problema persistir:")
    print()
    print("1. 📝 Execute no Supabase Dashboard SQL Editor:")
    print("   - Cole o conteúdo do arquivo: scripts/complete_cleanup_and_fix.sql")
    print("   - Execute o script")
    print()
    print("2. 🔄 Após limpeza, execute:")
    print("   uv run python scripts/test_after_cleanup.py")
    print()
    print("3. ✅ Verifique no Supabase Dashboard:")
    print("   - Authentication > Users")
    print("   - Deve mostrar: revtonbr@gmail.com")
    print()
    print("4. 🧪 Teste o link de confirmação:")
    print("   - Acesse o email recebido")
    print("   - Clique no link de confirmação")
    print("   - Verifique se funciona")

async def main():
    """
    Função principal
    """
    print("🚀 Teste Após Limpeza Completa")
    print()
    
    # Testar após limpeza
    await test_after_cleanup()
    
    # Instruções finais
    await provide_final_instructions()
    
    print("\n🎉 Teste concluído!")
    print("💡 Resumo:")
    print("   - Se funcionar: Problema resolvido ✅")
    print("   - Se falhar: Execute a limpeza manual")
    print("   - Verifique sempre no Supabase Dashboard")

if __name__ == "__main__":
    asyncio.run(main()) 