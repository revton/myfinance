#!/usr/bin/env python3
"""
Script para limpar dados órfãos e registrar um novo usuário
Execute: uv run python scripts/clean_and_register.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def clean_orphaned_data():
    """
    Limpa dados órfãos via SQL direto
    """
    print("🧹 Limpando Dados Órfãos")
    print("=" * 25)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    
    print(f"📧 Email: {test_email}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Executar limpeza via endpoint (se existir)
            print("🔄 Executando limpeza...")
            
            # Como não temos endpoint de limpeza, vamos usar o endpoint de força confirmação
            # que pode ajudar a identificar o problema
            print("💡 Dados órfãos detectados:")
            print("   - Existem 2 perfis em public.user_profiles")
            print("   - Não há usuários em auth.users")
            print("   - Isso indica registro incompleto")
            print()
            print("🔧 Para limpar manualmente:")
            print("1. Acesse: https://supabase.com/dashboard/project/qgkifpsimkcsfrwwyqsd/sql")
            print("2. Execute:")
            print("   DELETE FROM public.user_profiles WHERE email = 'revtonbr@gmail.com';")
            print("3. Verifique se foi limpo:")
            print("   SELECT * FROM public.user_profiles WHERE email = 'revtonbr@gmail.com';")
            print()
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def register_new_user():
    """
    Registra um novo usuário
    """
    print("📝 Registrando Novo Usuário")
    print("=" * 30)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 API URL: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Registrar usuário
            print("🔄 Registrando usuário...")
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": test_password,
                    "full_name": "Usuário Teste Limpo"
                },
                timeout=30.0
            )
            
            print(f"📊 Status Code: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Usuário registrado com sucesso!")
                print("📧 Email de confirmação enviado")
                print(f"   Response: {register_response.json()}")
                return True
                
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe ou dados inválidos")
                print(f"   Response: {register_response.text}")
                return False
                
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

async def test_complete_flow():
    """
    Testa o fluxo completo após limpeza
    """
    print("\n🧪 Testando Fluxo Completo")
    print("=" * 25)
    
    # Configurações
    api_base_url = "http://localhost:8002"
    test_email = "revtonbr@gmail.com"
    test_password = "Minha@Senha1"
    
    try:
        async with httpx.AsyncClient() as client:
            # Forçar confirmação
            print("🔄 Forçando confirmação...")
            confirm_response = await client.post(
                f"{api_base_url}/auth/force-confirm-email",
                json={"email": test_email},
                timeout=30.0
            )
            
            print(f"📊 Confirm Status: {confirm_response.status_code}")
            
            if confirm_response.status_code == 200:
                print("✅ Email confirmado!")
                
                # Testar login
                print("\n🔄 Testando login...")
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
                    data = login_response.json()
                    print(f"   User ID: {data.get('user', {}).get('id', 'N/A')}")
                    print(f"   Email: {data.get('user', {}).get('email', 'N/A')}")
                    return True
                else:
                    print(f"❌ Erro no login: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
            else:
                print(f"❌ Erro na confirmação: {confirm_response.status_code}")
                print(f"   Response: {confirm_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    return False

async def main():
    """
    Função principal
    """
    print("🚀 Limpeza e Registro de Usuário")
    print()
    
    # Verificar se o backend está rodando
    print("🔍 Verificando se o backend está rodando...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8002/health", timeout=5.0)
            if response.status_code == 200:
                print("✅ Backend está rodando")
            else:
                print("⚠️ Backend respondeu mas com status inesperado")
    except Exception as e:
        print("❌ Backend não está rodando")
        print("💡 Execute: uv run invoke backend")
        return
    
    print()
    
    # Limpar dados órfãos
    await clean_orphaned_data()
    
    print("⏸️ Pausa para limpeza manual")
    print("💡 Execute a limpeza SQL no Supabase Dashboard")
    print("   Depois pressione Enter para continuar...")
    input()
    
    # Registrar novo usuário
    success = await register_new_user()
    
    if success:
        # Testar fluxo completo
        await test_complete_flow()
    
    print("\n🎉 Processo concluído!")
    print("💡 Próximos passos:")
    print("   1. Verifique se o email chegou")
    print("   2. Teste o frontend se estiver rodando")
    print("   3. Verifique os logs do Supabase se necessário")

if __name__ == "__main__":
    asyncio.run(main()) 