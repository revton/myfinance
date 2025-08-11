#!/usr/bin/env python3
"""
Script para resolver automaticamente problemas de email de confirmação
Execute: uv run python scripts/auto_fix_email_confirmation.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class EmailConfirmationFixer:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Configuração do Supabase não encontrada no .env")
    
    async def force_confirm_email_via_api(self, email: str):
        """
        Força a confirmação de email via API do Supabase
        """
        try:
            print(f"🔧 Forçando confirmação de email para: {email}")
            
            # Primeiro, buscar o user_id
            async with httpx.AsyncClient() as client:
                # Buscar usuário pelo email
                response = await client.get(
                    f"{self.supabase_url}/auth/v1/admin/users",
                    headers={
                        "apikey": self.supabase_service_key or self.supabase_key,
                        "Authorization": f"Bearer {self.supabase_service_key or self.supabase_key}",
                        "Content-Type": "application/json"
                    },
                    params={"filter": f"email.eq.{email}"}
                )
                
                if response.status_code == 200:
                    users = response.json()
                    if users:
                        user_id = users[0].get('id')
                        if user_id:
                            # Forçar confirmação
                            confirm_response = await client.put(
                                f"{self.supabase_url}/auth/v1/admin/users/{user_id}",
                                headers={
                                    "apikey": self.supabase_service_key or self.supabase_key,
                                    "Authorization": f"Bearer {self.supabase_service_key or self.supabase_key}",
                                    "Content-Type": "application/json"
                                },
                                json={
                                    "email_confirm": True
                                }
                            )
                            
                            if confirm_response.status_code == 200:
                                print("✅ Email confirmado com sucesso via API!")
                                return True
                            else:
                                print(f"❌ Erro ao confirmar email: {confirm_response.status_code}")
                                return False
                        else:
                            print("❌ User ID não encontrado")
                            return False
                    else:
                        print("❌ Usuário não encontrado")
                        return False
                else:
                    print(f"❌ Erro ao buscar usuário: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro ao forçar confirmação: {str(e)}")
            return False
    
    async def force_confirm_email_via_direct_sql(self, email: str):
        """
        Força a confirmação de email via SQL direto (fallback)
        """
        try:
            print(f"🔧 Tentando confirmação via SQL direto...")
            
            # Usar a API REST para executar SQL
            sql_query = f"""
            UPDATE auth.users 
            SET email_confirmed_at = NOW(), updated_at = NOW()
            WHERE email = '{email}';
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supabase_url}/rest/v1/rpc/exec_sql",
                    headers={
                        "apikey": self.supabase_service_key or self.supabase_key,
                        "Authorization": f"Bearer {self.supabase_service_key or self.supabase_key}",
                        "Content-Type": "application/json"
                    },
                    json={"sql": sql_query}
                )
                
                if response.status_code in [200, 201]:
                    print("✅ Email confirmado via SQL direto!")
                    return True
                else:
                    print(f"❌ Erro no SQL direto: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro no SQL direto: {str(e)}")
            return False
    
    async def test_user_login(self, email: str, password: str):
        """
        Testa se o usuário consegue fazer login
        """
        try:
            print(f"🧪 Testando login do usuário...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supabase_url}/auth/v1/token?grant_type=password",
                    headers={
                        "apikey": self.supabase_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "email": email,
                        "password": password
                    }
                )
                
                if response.status_code == 200:
                    print("✅ Login bem-sucedido! Email está confirmado.")
                    return True
                elif response.status_code == 400:
                    error_data = response.json()
                    error_message = error_data.get("error_description", "").lower()
                    
                    if "email not confirmed" in error_message:
                        print("❌ Email ainda não confirmado")
                        return False
                    elif "invalid login credentials" in error_message:
                        print("ℹ️ Credenciais inválidas (senha incorreta)")
                        return False
                    else:
                        print(f"ℹ️ Outro erro: {error_message}")
                        return False
                else:
                    print(f"❌ Erro inesperado no login: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro ao testar login: {str(e)}")
            return False
    
    async def resend_confirmation_email(self, email: str):
        """
        Reenvia o email de confirmação
        """
        try:
            print(f"📧 Reenviando email de confirmação...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.supabase_url}/auth/v1/resend",
                    headers={
                        "apikey": self.supabase_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "type": "signup",
                        "email": email
                    }
                )
                
                if response.status_code == 200:
                    print("✅ Email de confirmação reenviado!")
                    return True
                else:
                    print(f"❌ Erro ao reenviar email: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro ao reenviar email: {str(e)}")
            return False

async def main():
    """
    Função principal
    """
    print("🔧 Resolução Automática de Problemas de Email")
    print("=" * 60)
    
    try:
        # Configurações
        email = "revtonbr@gmail.com"
        password = "senha123"  # Senha que você usou no registro
        
        # Criar instância do fixer
        fixer = EmailConfirmationFixer()
        
        print(f"🎯 Email: {email}")
        print(f"🔑 Senha: {password}")
        print()
        
        # Passo 1: Tentar forçar confirmação via API
        print("1️⃣ Tentando forçar confirmação via API...")
        success = await fixer.force_confirm_email_via_api(email)
        
        if not success:
            print("\n2️⃣ Tentando confirmação via SQL direto...")
            success = await fixer.force_confirm_email_via_direct_sql(email)
        
        # Passo 3: Testar login
        print("\n3️⃣ Testando login...")
        login_success = await fixer.test_user_login(email, password)
        
        if not login_success:
            print("\n4️⃣ Reenviando email de confirmação...")
            await fixer.resend_confirmation_email(email)
        
        # Resumo final
        print("\n📋 Resumo:")
        if login_success:
            print("✅ PROBLEMA RESOLVIDO! Usuário pode fazer login.")
            print("🎉 Você pode continuar com os testes!")
        else:
            print("⚠️ Problema parcialmente resolvido.")
            print("📧 Verifique sua caixa de entrada para o email de confirmação.")
            print("🔧 Se necessário, configure manualmente no Supabase Dashboard:")
            print("   - Settings > Auth > Site URL: http://localhost:3000")
            print("   - Settings > Auth > Enable email confirmations")
            print("   - Settings > Auth > SMTP Settings (configure um provedor)")
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        print("\n📋 Solução manual:")
        print("1. Acesse Supabase Dashboard > SQL Editor")
        print("2. Execute: UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = 'revtonbr@gmail.com';")

if __name__ == "__main__":
    asyncio.run(main()) 