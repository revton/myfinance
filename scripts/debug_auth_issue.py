#!/usr/bin/env python3
"""
Script para debugar problema de autenticação
Execute: uv run python scripts/debug_auth_issue.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def debug_auth_issue():
    """
    Debuga o problema de autenticação
    """
    print("🔍 Debugando Problema de Autenticação")
    print("=" * 45)
    
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
            
            # 2. Tentar registro com senha diferente
            print("\n🔄 2. Tentando registro com nova senha...")
            new_password = "Nova@Senha123"
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json={
                    "email": test_email,
                    "password": new_password,
                    "full_name": "Revton Debug"
                },
                timeout=30.0
            )
            
            print(f"📊 Register Status: {register_response.status_code}")
            
            if register_response.status_code == 201:
                print("✅ Registro bem-sucedido!")
                register_data = register_response.json()
                print(f"   Response: {register_data}")
                
                # 3. Tentar login com nova senha
                print("\n🔄 3. Testando login com nova senha...")
                login_response = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": test_email,
                        "password": new_password
                    },
                    timeout=30.0
                )
                
                print(f"📊 Login Status: {login_response.status_code}")
                
                if login_response.status_code == 200:
                    print("✅ Login funcionou com nova senha!")
                    login_data = login_response.json()
                    print(f"   User ID: {login_data.get('user', {}).get('id', 'N/A')}")
                    print("🎉 Problema resolvido!")
                    return
                else:
                    print(f"❌ Login ainda falha: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            elif register_response.status_code == 400:
                print("⚠️ Usuário já existe, tentando login...")
                
                # Tentar login com senha original
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
                    print("✅ Login funcionou com senha original!")
                    print("🎉 Usuário já estava correto!")
                    return
                else:
                    print(f"❌ Login falha: {login_response.status_code}")
                    print(f"   Response: {login_response.text}")
                    
            else:
                print(f"❌ Erro no registro: {register_response.status_code}")
                print(f"   Response: {register_response.text}")
                
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def check_supabase_config():
    """
    Verifica configuração do Supabase
    """
    print("\n🔍 Verificando Configuração do Supabase")
    print("=" * 40)
    
    try:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if supabase_url and supabase_key:
            print("✅ Configuração do Supabase encontrada")
            print(f"   URL: {supabase_url}")
            print(f"   Key: {supabase_key[:20]}...")
            
            # Testar conexão com Supabase
            async with httpx.AsyncClient() as client:
                test_response = await client.get(
                    f"{supabase_url}/rest/v1/",
                    headers={
                        "apikey": supabase_key,
                        "Authorization": f"Bearer {supabase_key}"
                    },
                    timeout=10.0
                )
                
                if test_response.status_code == 200:
                    print("✅ Conexão com Supabase OK")
                else:
                    print(f"⚠️ Conexão com Supabase: {test_response.status_code}")
                    
        else:
            print("❌ Configuração do Supabase incompleta")
            print(f"   URL: {'✅' if supabase_url else '❌'}")
            print(f"   Key: {'✅' if supabase_key else '❌'}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def provide_manual_instructions():
    """
    Fornece instruções manuais
    """
    print("\n📋 Instruções Manuais")
    print("=" * 25)
    
    print("🔧 Para resolver o problema:")
    print()
    print("1. 📝 Execute no Supabase Dashboard SQL Editor:")
    print("   - Acesse: https://supabase.com/dashboard")
    print("   - Vá em: SQL Editor")
    print("   - Cole o conteúdo do arquivo: scripts/clean_orphaned_data.sql")
    print("   - Execute o script")
    print()
    print("2. 🔄 Após limpeza, execute:")
    print("   uv run python scripts/fix_orphaned_user.py")
    print()
    print("3. ✅ Verifique se o usuário aparece em:")
    print("   - Authentication > Users")
    print("   - Deve mostrar: revtonbr@gmail.com")
    print()
    print("4. 🧪 Teste o login:")
    print("   curl -X POST 'http://localhost:8002/auth/login' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"email\": \"revtonbr@gmail.com\", \"password\": \"Minha@Senha1\"}'")

async def main():
    """
    Função principal
    """
    print("🚀 Debug de Problema de Autenticação")
    print()
    
    # Debugar problema
    await debug_auth_issue()
    
    # Verificar configuração
    await check_supabase_config()
    
    # Instruções manuais
    await provide_manual_instructions()
    
    print("\n🎉 Debug concluído!")
    print("💡 Resumo:")
    print("   - O problema é dados órfãos no Supabase")
    print("   - Execute a limpeza manual primeiro")
    print("   - Depois teste novamente")

if __name__ == "__main__":
    asyncio.run(main()) 