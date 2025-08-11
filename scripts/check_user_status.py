#!/usr/bin/env python3
"""
Script para verificar o status detalhado do usuário no Supabase
Execute: uv run python scripts/check_user_status.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def check_user_status(email: str):
    """
    Verifica o status detalhado do usuário no Supabase
    """
    try:
        # Configurações do Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Erro: Configuração do Supabase não encontrada")
            return
        
        print(f"🔍 Verificando status do usuário: {email}")
        print(f"   Supabase URL: {supabase_url}")
        
        # Fazer requisição para verificar o usuário
        async with httpx.AsyncClient() as client:
            # Tentar fazer login para verificar status
            response = await client.post(
                f"{supabase_url}/auth/v1/token?grant_type=password",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                },
                json={
                    "email": email,
                    "password": "senha_temporaria_para_teste"  # Senha incorreta para verificar status
                }
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get("error_description", "").lower()
                
                if "email not confirmed" in error_message:
                    print("❌ PROBLEMA: Email não foi confirmado!")
                    print("   Solução: Use o script force_confirm_email.sql")
                elif "invalid login credentials" in error_message:
                    print("ℹ️ Email existe, mas senha incorreta (esperado)")
                    print("   Status: Usuário registrado, mas email pode não estar confirmado")
                else:
                    print(f"ℹ️ Outro erro: {error_message}")
            elif response.status_code == 200:
                print("✅ Usuário logado com sucesso!")
                print("   Status: Email confirmado e credenciais válidas")
            else:
                print(f"❌ Erro inesperado: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro interno: {str(e)}")

async def check_supabase_auth_settings():
    """
    Verifica as configurações de autenticação do Supabase
    """
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        print("\n🔧 Verificando configurações do Supabase...")
        
        async with httpx.AsyncClient() as client:
            # Verificar se a API está respondendo
            response = await client.get(
                f"{supabase_url}/auth/v1/settings",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                settings = response.json()
                print("✅ API do Supabase está respondendo")
                print(f"   Site URL: {settings.get('site_url', 'Não configurado')}")
                print(f"   Enable email confirmations: {settings.get('enable_confirmations', 'Não informado')}")
            else:
                print(f"❌ Erro ao verificar configurações: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro ao verificar configurações: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🔍 Diagnóstico Detalhado do Usuário")
    print("=" * 50)
    
    # Email para verificar
    email = "revtonbr@gmail.com"
    
    print(f"🎯 Email: {email}")
    print()
    
    # Verificar status do usuário
    await check_user_status(email)
    
    # Verificar configurações do Supabase
    await check_supabase_auth_settings()
    
    print("\n📋 Próximos passos:")
    print("   1. Se email não confirmado, execute force_confirm_email.sql")
    print("   2. Verifique configurações no Supabase Dashboard")
    print("   3. Teste registro de novo usuário")
    print("   4. Verifique logs no Supabase Dashboard > Logs > Auth")

if __name__ == "__main__":
    asyncio.run(main()) 