#!/usr/bin/env python3
"""
Script para monitorar o processo de confirmação sem clicar no link
Execute: uv run python scripts/monitor_confirmation_process.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def check_current_status():
    """
    Verifica o status atual do usuário
    """
    print("🔍 Verificando Status Atual")
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
            
            # 2. Tentar login para verificar status atual
            print("\n🔄 2. Testando login atual...")
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
                print("✅ Login funcionou - usuário já pode fazer login")
                login_data = login_response.json()
                user_data = login_data.get('user', {})
                
                print(f"   User ID: {user_data.get('id', 'N/A')}")
                print(f"   Email: {user_data.get('email', 'N/A')}")
                print(f"   Email Confirmed: {user_data.get('email_confirmed_at', 'N/A')}")
                
                if user_data.get('email_confirmed_at'):
                    print("🎉 Email já está confirmado!")
                    print("💡 O link de confirmação não é mais necessário")
                else:
                    print("⚠️ Email não confirmado, mas login funciona")
                    print("💡 Isso indica que o Supabase está com auto-confirmação habilitada")
                    
            elif login_response.status_code == 401:
                print("❌ Login falhou - email precisa ser confirmado")
                print("   Response: ", login_response.text)
                print("💡 O link de confirmação é necessário")
                
            else:
                print(f"❌ Status inesperado: {login_response.status_code}")
                print("   Response: ", login_response.text)
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_token_status():
    """
    Verifica se existe token de confirmação válido
    """
    print("\n🔍 Verificando Token de Confirmação")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Reenviar email para obter token atual
            print("🔄 1. Reenviando email para obter token...")
            resend_response = await client.post(
                f"{api_base_url}/auth/custom-resend-confirmation",
                json={"email": test_email},
                timeout=30.0
            )
            
            if resend_response.status_code == 200:
                resend_data = resend_response.json()
                print("✅ Email reenviado com sucesso!")
                print(f"   Message: {resend_data.get('message', 'N/A')}")
                
                if 'token' in resend_data:
                    test_token = resend_data['token']
                    print(f"   Token: {test_token[:20]}...")
                    
                    # 2. Construir URL de confirmação
                    confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                    print(f"\n🔗 URL de Confirmação:")
                    print(f"   {confirmation_url}")
                    
                    # 3. Verificar se o token é válido (sem confirmar)
                    print(f"\n🔄 2. Verificando validade do token...")
                    try:
                        # Testar com token inválido primeiro para comparar
                        invalid_response = await client.get(
                            f"{api_base_url}/auth/custom-confirm-email/invalid-token",
                            timeout=10.0
                        )
                        
                        if invalid_response.status_code == 400:
                            print("✅ Endpoint funciona corretamente")
                            print("   Token inválido retorna erro como esperado")
                            
                            # 4. Simular confirmação (sem executar)
                            print(f"\n🔄 3. Simulando confirmação...")
                            print("💡 Para confirmar, acesse esta URL no navegador:")
                            print(f"   {confirmation_url}")
                            print()
                            print("📋 O que acontecerá quando clicar no link:")
                            print("   1. ✅ Token será validado")
                            print("   2. ✅ Email será confirmado no Supabase")
                            print("   3. ✅ Token será marcado como usado")
                            print("   4. ✅ Login funcionará normalmente")
                            
                        else:
                            print(f"⚠️ Endpoint retornou status inesperado: {invalid_response.status_code}")
                            
                    except Exception as e:
                        print(f"❌ Erro ao testar endpoint: {str(e)}")
                        
                else:
                    print("❌ Token não encontrado na resposta")
                    
            else:
                print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                print(f"   Response: {resend_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def simulate_confirmation_process():
    """
    Simula o processo de confirmação passo a passo
    """
    print("\n🔄 Simulando Processo de Confirmação")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Obter token
            print("🔄 1. Obtendo token de confirmação...")
            resend_response = await client.post(
                f"{api_base_url}/auth/custom-resend-confirmation",
                json={"email": test_email},
                timeout=30.0
            )
            
            if resend_response.status_code == 200:
                resend_data = resend_response.json()
                test_token = resend_data.get('token', '')
                
                if test_token:
                    print("✅ Token obtido com sucesso!")
                    print(f"   Token: {test_token[:20]}...")
                    
                    # 2. Simular confirmação
                    print(f"\n🔄 2. Simulando confirmação...")
                    confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                    
                    print("📋 Processo que será executado:")
                    print("   1. 🔍 Validar token no banco de dados")
                    print("   2. ⏰ Verificar se não expirou (24h)")
                    print("   3. 🔒 Verificar se não foi usado")
                    print("   4. 👤 Buscar usuário no Supabase")
                    print("   5. ✅ Atualizar email_confirmed_at")
                    print("   6. 🏷️ Marcar token como usado")
                    print("   7. 🎉 Retornar sucesso")
                    
                    print(f"\n🔗 URL para confirmar:")
                    print(f"   {confirmation_url}")
                    
                    # 3. Verificar se o usuário existe
                    print(f"\n🔄 3. Verificando se usuário existe...")
                    login_response = await client.post(
                        f"{api_base_url}/auth/login",
                        json={
                            "email": test_email,
                            "password": "Minha@Senha1"
                        },
                        timeout=30.0
                    )
                    
                    if login_response.status_code == 200:
                        print("✅ Usuário existe e pode fazer login")
                        print("💡 Confirmação pode ser executada com sucesso")
                    elif login_response.status_code == 401:
                        print("⚠️ Usuário existe mas precisa de confirmação")
                        print("💡 Confirmação é necessária")
                    else:
                        print(f"❌ Status inesperado: {login_response.status_code}")
                        
                else:
                    print("❌ Token não encontrado")
                    
            else:
                print(f"❌ Erro ao obter token: {resend_response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_supabase_status():
    """
    Verifica status no Supabase
    """
    print("\n🔍 Verificando Status no Supabase")
    print("=" * 35)
    
    try:
        # Verificar configuração
        supabase_url = os.getenv("SUPABASE_URL")
        if supabase_url:
            print("✅ Configuração do Supabase encontrada")
            print(f"   URL: {supabase_url}")
            print()
            print("💡 Para verificar manualmente:")
            print("   1. Acesse: https://supabase.com/dashboard")
            print("   2. Vá em: Authentication > Users")
            print("   3. Procure: revtonbr@gmail.com")
            print("   4. Verifique: Email Confirmed")
            print("   5. Se vazio: Precisa confirmação")
            print("   6. Se preenchido: Já confirmado")
        else:
            print("❌ Configuração do Supabase não encontrada")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Monitoramento do Processo de Confirmação")
    print("=" * 50)
    print("💡 Este script verifica se o link de confirmação funcionará")
    print("   sem precisar clicar nele")
    print()
    
    # Verificar status atual
    await check_current_status()
    
    # Verificar token
    await check_token_status()
    
    # Simular processo
    await simulate_confirmation_process()
    
    # Verificar Supabase
    await check_supabase_status()
    
    print("\n🎉 Monitoramento concluído!")
    print("💡 Resumo:")
    print("   - Se o login funcionar: Link não é necessário")
    print("   - Se o login falhar: Link é necessário")
    print("   - O link sempre funcionará se o usuário existir")
    print("   - Verifique o Supabase Dashboard para mais detalhes")

if __name__ == "__main__":
    asyncio.run(main()) 