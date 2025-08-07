#!/usr/bin/env python3
"""
Script para testar o link de confirmação e capturar erros detalhados
Execute: uv run python scripts/test_confirmation_link_debug.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_confirmation_link():
    """
    Testa o link de confirmação e captura erros detalhados
    """
    print("🔍 Testando Link de Confirmação - Debug")
    print("=" * 50)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    
    # Verificar configurações
    frontend_url = os.getenv("FRONTEND_URL")
    api_port = os.getenv("API_PORT", "8002")
    print(f"🌐 FRONTEND_URL: {frontend_url or 'Não configurado'}")
    print(f"🔌 API_PORT: {api_port}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Verificar se o backend está rodando
            print("🔄 1. Verificando backend...")
            try:
                health_response = await client.get(f"{api_base_url}/health", timeout=5.0)
                print(f"📊 Health Status: {health_response.status_code}")
                if health_response.status_code == 200:
                    print("✅ Backend está rodando")
                else:
                    print(f"⚠️ Backend respondeu com status: {health_response.status_code}")
            except Exception as e:
                print(f"❌ Backend não está rodando: {str(e)}")
                return
            
            # 2. Reenviar email para obter token
            print("\n🔄 2. Reenviando email para obter token...")
            resend_response = await client.post(
                f"{api_base_url}/auth/custom-resend-confirmation",
                json={"email": test_email},
                timeout=30.0
            )
            
            print(f"📊 Resend Status: {resend_response.status_code}")
            
            if resend_response.status_code == 200:
                resend_data = resend_response.json()
                print("✅ Email reenviado com sucesso!")
                print(f"   Message: {resend_data.get('message', 'N/A')}")
                
                if 'token' in resend_data:
                    test_token = resend_data['token']
                    print(f"   Token: {test_token[:20]}...")
                    
                    # 3. Construir URL de confirmação
                    if frontend_url:
                        confirmation_url = f"{frontend_url}/auth/custom-confirm-email/{test_token}"
                    else:
                        confirmation_url = f"{api_base_url}/auth/custom-confirm-email/{test_token}"
                    
                    print(f"\n🔗 URL de Confirmação:")
                    print(f"   {confirmation_url}")
                    
                    # 4. Testar confirmação com detalhes
                    print(f"\n🔄 3. Testando confirmação...")
                    try:
                        confirm_response = await client.get(
                            confirmation_url,
                            timeout=30.0,
                            follow_redirects=True
                        )
                        
                        print(f"📊 Confirm Status: {confirm_response.status_code}")
                        print(f"📊 Headers: {dict(confirm_response.headers)}")
                        print(f"📊 Response: {confirm_response.text}")
                        
                        if confirm_response.status_code == 200:
                            print("✅ Email confirmado com sucesso!")
                        elif confirm_response.status_code == 404:
                            print("❌ Endpoint não encontrado (404)")
                            print("💡 Verifique se o endpoint está registrado nas rotas")
                        elif confirm_response.status_code == 500:
                            print("❌ Erro interno do servidor (500)")
                            print("💡 Verifique os logs do backend")
                        else:
                            print(f"❌ Status inesperado: {confirm_response.status_code}")
                            
                    except httpx.ConnectError as e:
                        print(f"❌ Erro de conexão: {str(e)}")
                        print("💡 Verifique se o servidor está rodando na porta correta")
                    except httpx.TimeoutException as e:
                        print(f"❌ Timeout: {str(e)}")
                    except Exception as e:
                        print(f"❌ Erro inesperado: {str(e)}")
                        
                else:
                    print("❌ Token não encontrado na resposta")
                    
            else:
                print(f"❌ Erro ao reenviar email: {resend_response.status_code}")
                print(f"   Response: {resend_response.text}")
                
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")

async def test_endpoint_directly():
    """
    Testa o endpoint diretamente sem token
    """
    print("\n🔍 Testando Endpoint Diretamente")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    
    try:
        async with httpx.AsyncClient() as client:
            # Testar endpoint com token inválido
            test_url = f"{api_base_url}/auth/custom-confirm-email/invalid-token"
            print(f"🔗 Testando: {test_url}")
            
            response = await client.get(test_url, timeout=10.0)
            print(f"📊 Status: {response.status_code}")
            print(f"📊 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_backend_routes():
    """
    Verifica as rotas disponíveis no backend
    """
    print("\n🔍 Verificando Rotas do Backend")
    print("=" * 35)
    
    api_base_url = "http://localhost:8002"
    
    try:
        async with httpx.AsyncClient() as client:
            # Testar documentação da API
            docs_url = f"{api_base_url}/docs"
            print(f"🔗 Documentação: {docs_url}")
            
            response = await client.get(docs_url, timeout=10.0)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Documentação disponível")
                print("💡 Acesse a documentação para ver as rotas disponíveis")
            else:
                print("❌ Documentação não disponível")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Debug do Link de Confirmação")
    print()
    
    # Testar link de confirmação
    await test_confirmation_link()
    
    # Testar endpoint diretamente
    await test_endpoint_directly()
    
    # Verificar rotas
    await check_backend_routes()
    
    print("\n🎉 Debug concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique os logs do backend")
    print("   2. Confirme se o endpoint está registrado")
    print("   3. Teste manualmente no navegador")

if __name__ == "__main__":
    asyncio.run(main()) 