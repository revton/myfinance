#!/usr/bin/env python3
"""
Script completo para resolver problemas de email de confirmação
Execute: uv run python scripts/complete_email_fix.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def complete_email_fix():
    """
    Resolve completamente o problema de email de confirmação
    """
    print("🔧 Resolução Completa de Problemas de Email")
    print("=" * 60)
    
    # Configurações
    email = "revtonbr@gmail.com"
    password = "Minha@Senha1"
    api_base_url = "http://localhost:8002"
    
    print(f"🎯 Email: {email}")
    print(f"🔑 Senha: {password}")
    print(f"🌐 API: {api_base_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            # Passo 1: Registrar usuário (se não existir)
            print("1️⃣ Registrando usuário...")
            register_data = {
                "email": email,
                "password": password,
                "full_name": "Revton Teste"
            }
            
            register_response = await client.post(
                f"{api_base_url}/auth/register",
                json=register_data,
                timeout=30.0
            )
            
            if register_response.status_code == 201:
                result = register_response.json()
                print(f"✅ Usuário registrado: {result.get('message', 'Sucesso')}")
            elif register_response.status_code == 400:
                error_data = register_response.json()
                if "already registered" in str(error_data).lower():
                    print("ℹ️ Usuário já registrado")
                else:
                    print(f"❌ Erro no registro: {error_data}")
                    return False
            else:
                print(f"❌ Erro inesperado no registro: {register_response.status_code}")
                return False
            
            # Passo 2: Reenviar email de confirmação
            print("\n2️⃣ Reenviando email de confirmação...")
            resend_response = await client.post(
                f"{api_base_url}/auth/resend-confirmation",
                json={"email": email},
                timeout=30.0
            )
            
            if resend_response.status_code == 200:
                result = resend_response.json()
                print(f"✅ {result.get('message', 'Email reenviado')}")
            else:
                error_data = resend_response.json()
                print(f"ℹ️ {error_data.get('detail', 'Email já confirmado ou erro')}")
            
            # Passo 3: Tentar fazer login
            print("\n3️⃣ Testando login...")
            login_response = await client.post(
                f"{api_base_url}/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=30.0
            )
            
            if login_response.status_code == 200:
                result = login_response.json()
                print("✅ Login bem-sucedido! Email está confirmado.")
                print("🎉 PROBLEMA RESOLVIDO!")
                print(f"🔑 Token: {result.get('access_token', 'Não disponível')[:20]}...")
                return True
            elif login_response.status_code == 400:
                error_data = login_response.json()
                error_message = error_data.get('detail', '').lower()
                
                if "email not confirmed" in error_message:
                    print("❌ Email ainda não confirmado")
                    print("📧 Verifique sua caixa de entrada e spam")
                    print("💡 Se não receber o email, configure o Supabase:")
                    print("   - Settings > Auth > Site URL: http://localhost:3000")
                    print("   - Settings > Auth > Enable email confirmations")
                    print("   - Settings > Auth > SMTP Settings")
                elif "invalid credentials" in error_message:
                    print("ℹ️ Credenciais inválidas")
                else:
                    print(f"ℹ️ Outro erro: {error_message}")
            else:
                print(f"❌ Erro inesperado no login: {login_response.status_code}")
            
            # Passo 4: Tentar forçar confirmação via endpoint
            print("\n4️⃣ Tentando forçar confirmação...")
            force_response = await client.post(
                f"{api_base_url}/auth/force-confirm-email",
                json={"email": email},
                timeout=30.0
            )
            
            if force_response.status_code == 200:
                result = force_response.json()
                print(f"✅ {result.get('message', 'Confirmação forçada')}")
                
                # Testar login novamente
                print("\n5️⃣ Testando login após força confirmação...")
                login_response2 = await client.post(
                    f"{api_base_url}/auth/login",
                    json={
                        "email": email,
                        "password": password
                    },
                    timeout=30.0
                )
                
                if login_response2.status_code == 200:
                    print("✅ Login bem-sucedido após força confirmação!")
                    print("🎉 PROBLEMA RESOLVIDO!")
                    return True
                else:
                    print(f"❌ Login ainda falhou: {login_response2.status_code}")
            else:
                error_data = force_response.json()
                print(f"ℹ️ {error_data.get('detail', 'Endpoint não disponível')}")
            
            return False
            
    except httpx.ConnectError:
        print("❌ Erro: Não foi possível conectar à API local")
        print("💡 Certifique-se de que o backend está rodando: uv run invoke backend")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

async def main():
    """
    Função principal
    """
    print("🚀 Iniciando resolução completa...")
    print()
    
    success = await complete_email_fix()
    
    if success:
        print("\n🎉 SUCESSO TOTAL!")
        print("✅ Email confirmado")
        print("✅ Login funcionando")
        print("✅ Você pode continuar com os testes!")
    else:
        print("\n📋 Resumo e Próximos Passos:")
        print("1. Verifique sua caixa de entrada e spam")
        print("2. Configure o Supabase Dashboard:")
        print("   - Settings > Auth > Site URL: http://localhost:3000")
        print("   - Settings > Auth > Enable email confirmations")
        print("   - Settings > Auth > SMTP Settings (configure um provedor)")
        print("3. Execute manualmente no SQL Editor do Supabase:")
        print("   UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")
        print("4. Teste o login novamente")

if __name__ == "__main__":
    asyncio.run(main()) 