#!/usr/bin/env python3
"""
Script final para resolver problemas de email via SQL direto
Execute: uv run python scripts/final_email_fix.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def fix_email_via_supabase_sql():
    """
    Resolve o problema de email via SQL direto no Supabase
    """
    print("🔧 Resolução Final via SQL Direto")
    print("=" * 50)
    
    # Configurações
    email = "revtonbr@gmail.com"
    password = "Minha@Senha1"
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"🎯 Email: {email}")
    print(f"🔑 Senha: {password}")
    print(f"🌐 Supabase: {supabase_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Passo 1: Verificar se o usuário existe
            print("1️⃣ Verificando se o usuário existe...")
            
            # Usar a API REST do Supabase para verificar usuário
            response = await client.get(
                f"{supabase_url}/rest/v1/auth_users",
                headers={
                    "apikey": supabase_key,
                    "Authorization": f"Bearer {supabase_key}",
                    "Content-Type": "application/json"
                },
                params={"email": f"eq.{email}"}
            )
            
            if response.status_code == 200:
                users = response.json()
                if users:
                    user = users[0]
                    print(f"✅ Usuário encontrado: {user.get('id')}")
                    print(f"   Email confirmado: {user.get('email_confirmed_at')}")
                    
                    if not user.get('email_confirmed_at'):
                        print("❌ Email não confirmado - forçando confirmação...")
                        
                        # Forçar confirmação via SQL
                        update_response = await client.patch(
                            f"{supabase_url}/rest/v1/auth_users",
                            headers={
                                "apikey": supabase_key,
                                "Authorization": f"Bearer {supabase_key}",
                                "Content-Type": "application/json",
                                "Prefer": "return=minimal"
                            },
                            params={"id": f"eq.{user['id']}"},
                            json={
                                "email_confirmed_at": "now()",
                                "updated_at": "now()"
                            }
                        )
                        
                        if update_response.status_code in [200, 204]:
                            print("✅ Email confirmado via SQL!")
                        else:
                            print(f"❌ Erro ao confirmar email: {update_response.status_code}")
                            return False
                    else:
                        print("✅ Email já confirmado")
                else:
                    print("❌ Usuário não encontrado")
                    return False
            else:
                print(f"❌ Erro ao verificar usuário: {response.status_code}")
                return False
            
            # Passo 2: Testar login
            print("\n2️⃣ Testando login...")
            login_response = await client.post(
                f"{supabase_url}/auth/v1/token?grant_type=password",
                headers={
                    "apikey": supabase_key,
                    "Content-Type": "application/json"
                },
                json={
                    "email": email,
                    "password": password
                }
            )
            
            if login_response.status_code == 200:
                result = login_response.json()
                print("✅ Login bem-sucedido!")
                print("🎉 PROBLEMA RESOLVIDO!")
                print(f"🔑 Access Token: {result.get('access_token', '')[:20]}...")
                return True
            elif login_response.status_code == 400:
                error_data = login_response.json()
                error_message = error_data.get("error_description", "").lower()
                
                if "email not confirmed" in error_message:
                    print("❌ Email ainda não confirmado")
                    print("💡 Execute manualmente no SQL Editor do Supabase:")
                    print("   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")
                elif "invalid login credentials" in error_message:
                    print("ℹ️ Credenciais inválidas (senha incorreta)")
                else:
                    print(f"ℹ️ Outro erro: {error_message}")
            else:
                print(f"❌ Erro inesperado no login: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
            
            return False
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False

async def main():
    """
    Função principal
    """
    print("🚀 Resolução Final de Problemas de Email")
    print()
    
    success = await fix_email_via_supabase_sql()
    
    if success:
        print("\n🎉 SUCESSO TOTAL!")
        print("✅ Email confirmado via SQL")
        print("✅ Login funcionando")
        print("✅ Você pode continuar com os testes!")
    else:
        print("\n📋 Solução Manual:")
        print("1. Acesse o Supabase Dashboard")
        print("2. Vá para SQL Editor")
        print("3. Execute este comando:")
        print("   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")
        print("4. Teste o login novamente")
        print("\n🔧 Para evitar problemas futuros:")
        print("- Configure Site URL: http://localhost:3000")
        print("- Ative 'Enable email confirmations'")
        print("- Configure um provedor de email (SMTP/Resend)")

if __name__ == "__main__":
    asyncio.run(main()) 