#!/usr/bin/env python3
"""
Script para testar diretamente o serviço de email Resend
Execute: uv run python scripts/test_resend_direct.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_resend_direct():
    """
    Testa diretamente a API do Resend
    """
    print("🧪 Testando API do Resend Diretamente")
    print("=" * 40)
    
    # Configurações
    resend_api_key = os.getenv("RESEND_API_KEY")
    test_email = "revtonbr@gmail.com"
    
    if not resend_api_key:
        print("❌ RESEND_API_KEY não encontrada no arquivo .env")
        return
    
    print(f"📧 Email: {test_email}")
    print(f"🔑 API Key: {resend_api_key[:10]}...")
    print()
    
    # Template simples de teste
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste MyFinance</title>
    </head>
    <body>
        <h1>Teste de Email</h1>
        <p>Este é um teste do sistema de email do MyFinance.</p>
        <p>Se você recebeu este email, o sistema está funcionando!</p>
    </body>
    </html>
    """
    
    try:
        async with httpx.AsyncClient() as client:
            print("🔄 Enviando email de teste...")
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": "MyFinance <no-reply@myfinance.com>",
                    "to": [test_email],
                    "subject": "Teste de Email - MyFinance",
                    "html": html_content
                },
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📊 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ Email enviado com sucesso!")
                response_data = response.json()
                print(f"   ID: {response_data.get('id', 'N/A')}")
                print(f"   From: {response_data.get('from', 'N/A')}")
                print(f"   To: {response_data.get('to', 'N/A')}")
                print(f"   Subject: {response_data.get('subject', 'N/A')}")
            else:
                print("❌ Erro ao enviar email")
                print(f"   Response: {response.text}")
                
                # Tentar obter mais detalhes do erro
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Raw Response: {response.text}")
                    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def test_resend_domains():
    """
    Testa os domínios configurados no Resend
    """
    print("\n🌐 Testando Domínios do Resend")
    print("=" * 30)
    
    resend_api_key = os.getenv("RESEND_API_KEY")
    
    if not resend_api_key:
        print("❌ RESEND_API_KEY não encontrada")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            print("🔄 Listando domínios...")
            response = await client.get(
                "https://api.resend.com/domains",
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                domains_data = response.json()
                print("✅ Domínios encontrados:")
                for domain in domains_data.get('data', []):
                    print(f"   - {domain.get('name', 'N/A')} ({domain.get('status', 'N/A')})")
            else:
                print("❌ Erro ao listar domínios")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste Direto do Resend")
    print()
    
    # Testar envio direto
    await test_resend_direct()
    
    # Testar domínios
    await test_resend_domains()
    
    print("\n🎉 Teste concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique sua caixa de email")
    print("   2. Se não recebeu, verifique a configuração do Resend")
    print("   3. Verifique se o domínio está configurado corretamente")

if __name__ == "__main__":
    asyncio.run(main()) 