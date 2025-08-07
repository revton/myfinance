#!/usr/bin/env python3
"""
Script para verificar o status de confirmação do email
Execute: uv run python scripts/check_confirmation_status.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def check_confirmation_status():
    """
    Verifica o status de confirmação do email
    """
    print("🔍 Verificando Status de Confirmação")
    print("=" * 40)
    
    # Configurações
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
            
            # 2. Tentar login para verificar status
            print("\n🔄 2. Testando login...")
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
                user_data = login_data.get('user', {})
                
                print(f"   User ID: {user_data.get('id', 'N/A')}")
                print(f"   Email: {user_data.get('email', 'N/A')}")
                print(f"   Email Confirmed: {user_data.get('email_confirmed_at', 'N/A')}")
                
                if user_data.get('email_confirmed_at'):
                    print("🎉 Email confirmado com sucesso!")
                else:
                    print("⚠️ Email ainda não confirmado")
                    
            elif login_response.status_code == 401:
                print("❌ Login falhou - credenciais inválidas ou email não confirmado")
                print("   Response: ", login_response.text)
                
            else:
                print(f"❌ Status inesperado: {login_response.status_code}")
                print("   Response: ", login_response.text)
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_supabase_directly():
    """
    Verifica diretamente no Supabase (se possível)
    """
    print("\n🔍 Verificando no Supabase (via MCP)")
    print("=" * 40)
    
    try:
        # Usar MCP para verificar
        import subprocess
        result = subprocess.run([
            "uv", "run", "python", "-c", 
            "import os; from dotenv import load_dotenv; load_dotenv(); print('SUPABASE_URL:', os.getenv('SUPABASE_URL'))"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Configuração do Supabase encontrada")
            print("💡 Use o Supabase Dashboard para verificar:")
            print("   1. Acesse: https://supabase.com/dashboard")
            print("   2. Vá em: Authentication > Users")
            print("   3. Procure pelo email: revtonbr@gmail.com")
            print("   4. Verifique se 'Email Confirmed' está preenchido")
        else:
            print("❌ Erro ao verificar configuração")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_confirmation_flow():
    """
    Testa o fluxo completo de confirmação
    """
    print("\n🔄 Testando Fluxo de Confirmação")
    print("=" * 35)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Reenviar email para obter novo token
            print("🔄 1. Reenviando email...")
            resend_response = await client.post(
                f"{api_base_url}/auth/custom-resend-confirmation",
                json={"email": test_email},
                timeout=30.0
            )
            
            if resend_response.status_code == 200:
                resend_data = resend_response.json()
                print("✅ Email reenviado!")
                
                if 'token' in resend_data:
                    test_token = resend_data['token']
                    print(f"   Token: {test_token[:20]}...")
                    
                    # 2. Construir URL de confirmação
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
                        
                        # 4. Verificar se funcionou tentando login
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
                            print("🎉 Email confirmado com sucesso!")
                        else:
                            print(f"❌ Login ainda falha: {login_response.status_code}")
                            
                    else:
                        print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                        print(f"   Response: {confirm_response.text}")
                        
                else:
                    print("❌ Token não encontrado na resposta")
                    
            else:
                print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Verificação de Status de Confirmação")
    print()
    
    # Verificar status atual
    await check_confirmation_status()
    
    # Verificar no Supabase
    await check_supabase_directly()
    
    # Testar fluxo completo
    await test_confirmation_flow()
    
    print("\n🎉 Verificação concluída!")
    print("💡 Resumo:")
    print("   - Se o login funcionar: Email confirmado ✅")
    print("   - Se o login falhar: Email não confirmado ❌")
    print("   - Verifique também no Supabase Dashboard")

if __name__ == "__main__":
    asyncio.run(main()) 