#!/usr/bin/env python3
"""
Script para testar recuperação de senha
Execute: uv run python scripts/test_forgot_password.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_forgot_password():
    """
    Testa recuperação de senha
    """
    print("🧪 Testando Recuperação de Senha")
    print("=" * 40)
    
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. Testar solicitação de recuperação de senha
            print("🔄 1. Solicitando recuperação de senha...")
            forgot_response = await client.post(
                f"{api_base_url}/auth/forgot-password",
                json={
                    "email": test_email
                },
                timeout=60.0
            )
            
            print(f"📊 Forgot Password Status: {forgot_response.status_code}")
            
            if forgot_response.status_code == 200:
                print("✅ Solicitação de recuperação enviada!")
                forgot_data = forgot_response.json()
                print(f"   Response: {forgot_data}")
                print("📧 Verifique seu email para o link de recuperação")
                
            else:
                print(f"❌ Erro na solicitação: {forgot_response.status_code}")
                print(f"   Response: {forgot_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")

async def main():
    """
    Função principal
    """
    print("🚀 Teste de Recuperação de Senha")
    print("💡 Testa o fluxo de 'Esqueci minha senha'")
    print()
    
    await test_forgot_password()
    
    print("\n🎉 Teste concluído!")
    print("💡 Resumo:")
    print("   - Solicitação: Envia email de recuperação")
    print("   - Email: Contém link para redefinir senha")
    print("   - Segurança: Não revela se email existe")
    print("   - Frontend: Deve implementar página de reset")

if __name__ == "__main__":
    asyncio.run(main()) 