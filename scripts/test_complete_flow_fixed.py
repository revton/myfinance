#!/usr/bin/env python3
"""
Script para testar o fluxo completo após correções
Execute: uv run python scripts/test_complete_flow_fixed.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_complete_flow():
    """
    Testa o fluxo completo de registro e confirmação
    """
    print("🧪 Teste do Fluxo Completo - Versão Corrigida")
    print("=" * 55)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    
    # Verificar configurações
    frontend_url = os.getenv("FRONTEND_URL")
    print(f"🌐 FRONTEND_URL: {frontend_url or 'Não configurado (usará API backend)'}")
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
            
            # 2. Registrar usuário
            print("\n🔄 2. Registrando usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Usuário Teste Corrigido"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                register_data = register_response.json()
                print(f"   User ID: {register_data.get('user', {}).get('id', 'N/A')}")
                
                # 3. Tentar login (deve falhar sem confirmação)
                print("\n🔄 3. Testando login sem confirmação...")
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": test_email,
                        "password": test_password
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                if login_response.status_code == 401:
                    print("✅ Login falhou como esperado (email não confirmado)")
                elif login_response.status_code == 200:
                    print("⚠️ Login funcionou sem confirmação (auto-confirmação habilitada)")
                else:
                    print(f"❌ Status inesperado: {login_response.status_code}")
                
                # 4. Reenviar email customizado
                print("\n🔄 4. Reenviando email customizado...")
                resend_response = await client.post(
                    f"{api_base_url}/auth/custom-resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                print(f"📊 Resend Status: {resend_response.status_code}")
                
                if resend_response.status_code == 200:
                    resend_data = resend_response.json()
                    print("✅ Email customizado reenviado!")
                    print(f"   Message: {resend_data.get('message', 'N/A')}")
                    
                    if 'token' in resend_data:
                        test_token = resend_data['token']
                        print(f"   Token: {test_token[:20]}...")
                        
                        # 5. Construir URL de confirmação
                        if frontend_url:
                            confirmation_url = f"{frontend_url}/auth/custom-confirm-email/{test_token}"
                        else:
                            confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                        
                        print(f"\n🔗 URL de Confirmação:")
                        print(f"   {confirmation_url}")
                        
                        # 6. Testar confirmação
                        print(f"\n🔄 5. Testando confirmação...")
                        confirm_response = await client.get(
                            confirmation_url,
                            timeout=30.0
                        )
                        
                        print(f"📊 Confirm Status: {confirm_response.status_code}")
                        
                        if confirm_response.status_code == 200:
                            print("✅ Email confirmado com sucesso!")
                            confirm_data = confirm_response.json()
                            print(f"   Message: {confirm_data.get('message', 'N/A')}")
                            
                            # 7. Testar login após confirmação
                            print(f"\n🔄 6. Testando login após confirmação...")
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
                                print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                                print(f"   Access Token: {login_data.get('access_token', 'N/A')[:20]}...")
                            else:
                                print(f"❌ Erro no login: {login_response.status_code}")
                                print(f"   Response: {login_response.text}")
                        else:
                            print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                            print(f"   Response: {confirm_response.text}")
                            
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    print(f"   Response: {resend_response.text}")
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, testando apenas email...")
                
                # Testar apenas reenvio
                resend_response = await client.post(
                    f"{api_base_url}/auth/custom-resend-confirmation",
                    json={"email": test_email},
                    timeout=30.0
                )
                
                if resend_response.status_code == 200:
                    resend_data = resend_response.json()
                    if 'token' in resend_data:
                        test_token = resend_data['token']
                        if frontend_url:
                            confirmation_url = f"{frontend_url}/auth/custom-confirm-email/{test_token}"
                        else:
                            confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                        
                        print(f"\n🔗 URL de Confirmação:")
                        print(f"   {confirmation_url}")
                else:
                    print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste do Fluxo Completo - Versão Corrigida")
    print()
    
    # Testar fluxo completo
    await test_complete_flow()
    
    print("\n🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Execute o script SQL para limpar dados órfãos")
    print("   2. Teste o registro novamente")
    print("   3. Verifique se o email de confirmação é obrigatório")

if __name__ == "__main__":
    asyncio.run(main()) 