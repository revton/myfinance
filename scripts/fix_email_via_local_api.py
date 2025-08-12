#!/usr/bin/env python3
"""
Script para resolver problemas de email usando a API local
Execute: uv run python scripts/fix_email_via_local_api.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def fix_email_confirmation():
    """
    Resolve o problema de email de confirmação usando a API local
    """
    print("🔧 Resolvendo Problema de Email via API Local")
    print("=" * 50)
    
    # Configurações
    email = "revtonbr@gmail.com"
    api_base_url = "http://localhost:8002"
    
    print(f"🎯 Email: {email}")
    print(f"🌐 API: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Passo 1: Reenviar email de confirmação
            print("1️⃣ Reenviando email de confirmação...")
            response = await client.post(
                f"{api_base_url}/auth/resend-confirmation",
                json={"email": email},
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result.get('message', 'Email reenviado com sucesso')}")
            else:
                error_data = response.json()
                print(f"❌ Erro: {error_data.get('detail', 'Erro desconhecido')}")
            
            # Passo 2: Tentar fazer login para verificar status
            print("\n2️⃣ Testando login...")
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json={
                    "email": email,
                    "password": "senha123"  # Ajuste para a senha correta
                },
                timeout=30.0
            )
            
            if login_response.status_code == 200:
                print("✅ Login bem-sucedido! Email está confirmado.")
                print("🎉 PROBLEMA RESOLVIDO!")
                return True
            elif login_response.status_code == 400:
                error_data = login_response.json()
                error_message = error_data.get('detail', '').lower()
                
                if "email not confirmed" in error_message:
                    print("❌ Email ainda não confirmado")
                    print("📧 Verifique sua caixa de entrada e spam")
                elif "invalid credentials" in error_message:
                    print("ℹ️ Credenciais inválidas (senha incorreta)")
                    print("💡 Ajuste a senha no script se necessário")
                else:
                    print(f"ℹ️ Outro erro: {error_message}")
            else:
                print(f"❌ Erro inesperado no login: {login_response.status_code}")
            
            # Passo 3: Se ainda não funcionou, tentar forçar confirmação via SQL
            print("\n3️⃣ Tentando forçar confirmação via SQL...")
            
            # Usar a API local para executar SQL (se disponível)
            sql_response = await client.post(
                f"{api_base_url}/admin/force-confirm-email",
                json={"email": email},
                timeout=30.0
            )
            
            if sql_response.status_code == 200:
                print("✅ Confirmação forçada com sucesso!")
                return True
            else:
                print("ℹ️ Endpoint de força confirmação não disponível")
                print("📋 Execute manualmente no Supabase Dashboard:")
                print("   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")
            
            return False
            
    except httpx.ConnectError:
        print("❌ Erro: Não foi possível conectar à API local")
        print("💡 Certifique-se de que o backend está rodando em http://localhost:8002")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

async def test_backend_connection():
    """
    Testa se o backend está rodando
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8002/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Backend está rodando")
                return True
            else:
                print("⚠️ Backend respondeu, mas com status inesperado")
                return True
    except:
        print("❌ Backend não está rodando")
        return False

async def main():
    """
    Função principal
    """
    print("🚀 Iniciando resolução automática...")
    print()
    
    # Verificar se o backend está rodando
    backend_ok = await test_backend_connection()
    
    if not backend_ok:
        print("\n📋 Para resolver o problema:")
        print("1. Inicie o backend: uv run invoke backend")
        print("2. Execute este script novamente")
        return
    
    # Resolver o problema
    success = await fix_email_confirmation()
    
    if success:
        print("\n🎉 SUCESSO! Você pode continuar com os testes.")
    else:
        print("\n📋 Próximos passos:")
        print("1. Verifique sua caixa de entrada e spam")
        print("2. Configure o Supabase Dashboard:")
        print("   - Settings > Auth > Site URL: http://localhost:3000")
        print("   - Settings > Auth > Enable email confirmations")
        print("3. Execute manualmente no SQL Editor:")
        print("   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")

if __name__ == "__main__":
    asyncio.run(main()) 