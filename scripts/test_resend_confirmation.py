#!/usr/bin/env python3
"""
Script para testar o reenvio de email de confirmação via API
Execute: python scripts/test_resend_confirmation.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def test_resend_confirmation(email: str):
    """
    Testa o reenvio de email de confirmação
    """
    try:
        # Configurações do Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Erro: Configuração do Supabase não encontrada")
            print("   Verifique as variáveis SUPABASE_URL e SUPABASE_ANON_KEY no .env")
            return
        
        print(f"🔍 Testando reenvio de confirmação para: {email}")
        print(f"   Supabase URL: {supabase_url}")
        
        # Fazer requisição para a API de reenvio de confirmação
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{supabase_url}/auth/v1/resend",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                },
                json={
                    "type": "signup",
                    "email": email
                }
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Email de confirmação reenviado com sucesso!")
                print("   Verifique sua caixa de entrada e spam")
            elif response.status_code == 404:
                print("❌ Usuário não encontrado com este email")
            elif response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get("error_description", "").lower()
                if "already confirmed" in error_message:
                    print("ℹ️ Email já foi confirmado")
                else:
                    print(f"❌ Erro ao reenviar email: {error_data.get('error_description', 'Erro desconhecido')}")
            else:
                print(f"❌ Erro inesperado: Status {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro interno: {str(e)}")

async def test_api_endpoint(email: str):
    """
    Testa o endpoint da API local para reenvio de confirmação
    """
    try:
        api_url = "http://localhost:8002/auth/resend-confirmation"
        
        print(f"🔍 Testando endpoint local: {api_url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                json={"email": email}
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Sucesso: {result.get('message', 'Email reenviado')}")
            else:
                error_data = response.json()
                print(f"❌ Erro: {error_data.get('detail', 'Erro desconhecido')}")
                
    except Exception as e:
        print(f"❌ Erro ao testar endpoint local: {str(e)}")

async def main():
    """
    Função principal
    """
    print("📧 Teste de Reenvio de Email de Confirmação")
    print("=" * 50)
    
    # Email para testar (modifique conforme necessário)
    email = "revtonbr@gmail.com"
    
    print(f"🎯 Email de teste: {email}")
    print()
    
    # Teste 1: Reenvio direto via Supabase
    print("1️⃣ Testando reenvio direto via Supabase...")
    await test_resend_confirmation(email)
    print()
    
    # Teste 2: Reenvio via API local
    print("2️⃣ Testando reenvio via API local...")
    await test_api_endpoint(email)
    print()
    
    print("📋 Próximos passos:")
    print("   1. Verifique sua caixa de entrada")
    print("   2. Verifique a pasta de spam")
    print("   3. Se não receber, verifique configurações de SMTP no Supabase")
    print("   4. Use o script force_confirm_email.sql se necessário")

if __name__ == "__main__":
    asyncio.run(main()) 