#!/usr/bin/env python3
"""
Script para limpar dados do usuário para testes
Execute: uv run python scripts/clean_user_data.py
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

async def clean_user_data():
    """
    Limpa dados do usuário revtonbr@gmail.com
    """
    print("🧹 Limpando dados do usuário para testes")
    print("=" * 45)
    
    # Configurações
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    test_email = "revtonbr@gmail.com"
    
    if not supabase_url or not supabase_key:
        print("❌ Configuração do Supabase não encontrada")
        return
    
    print(f"📧 Email: {test_email}")
    print(f"🔗 Supabase URL: {supabase_url}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            }
            
            # 1. Limpar tokens de confirmação
            print("🔄 1. Limpando tokens de confirmação...")
            response = await client.delete(
                f"{supabase_url}/rest/v1/email_confirmation_tokens",
                headers=headers,
                params={"email": f"eq.{test_email}"},
                timeout=30.0
            )
            
            print(f"📊 Tokens Status: {response.status_code}")
            if response.status_code in [200, 204]:
                print("✅ Tokens removidos com sucesso")
            else:
                print(f"⚠️ Erro ao remover tokens: {response.text}")
            
            # 2. Limpar perfis de usuário
            print("\n🔄 2. Limpando perfis de usuário...")
            response = await client.delete(
                f"{supabase_url}/rest/v1/user_profiles",
                headers=headers,
                params={"email": f"eq.{test_email}"},
                timeout=30.0
            )
            
            print(f"📊 Profiles Status: {response.status_code}")
            if response.status_code in [200, 204]:
                print("✅ Perfis removidos com sucesso")
            else:
                print(f"⚠️ Erro ao remover perfis: {response.text}")
            
            # 3. Verificar se ainda há dados
            print("\n🔄 3. Verificando dados restantes...")
            
            # Verificar tokens
            response = await client.get(
                f"{supabase_url}/rest/v1/email_confirmation_tokens",
                headers=headers,
                params={"email": f"eq.{test_email}"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                tokens = response.json()
                print(f"📊 Tokens restantes: {len(tokens)}")
            
            # Verificar perfis
            response = await client.get(
                f"{supabase_url}/rest/v1/user_profiles",
                headers=headers,
                params={"email": f"eq.{test_email}"},
                timeout=30.0
            )
            
            if response.status_code == 200:
                profiles = response.json()
                print(f"📊 Perfis restantes: {len(profiles)}")
            
            print("\n✅ Limpeza concluída!")
            print("💡 Agora você pode testar o registro novamente")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

async def verify_cleanup():
    """
    Verifica se a limpeza foi bem-sucedida
    """
    print("\n🔍 Verificando limpeza...")
    print("=" * 25)
    
    try:
        async with httpx.AsyncClient() as client:
            # Tentar login para verificar se o usuário ainda existe
            response = await client.post(
                "http://localhost:8002/auth/login",
                json={
                    "email": "revtonbr@gmail.com",
                    "password": "Minha@Senha1"
                },
                timeout=30.0
            )
            
            if response.status_code == 401:
                print("✅ Usuário removido com sucesso - login falhou como esperado")
            elif response.status_code == 200:
                print("⚠️ Usuário ainda existe - pode ser necessário limpeza manual")
            else:
                print(f"📊 Status inesperado: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Erro na verificação: {str(e)}")

async def main():
    """
    Função principal
    """
    print("🚀 Limpeza de Dados do Usuário")
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
    
    # Limpar dados
    await clean_user_data()
    
    # Verificar limpeza
    await verify_cleanup()
    
    print("\n🎉 Processo concluído!")
    print("💡 Próximos passos:")
    print("   1. Execute o script SQL no Supabase Dashboard se necessário")
    print("   2. Teste o registro novamente")
    print("   3. Verifique se o email de confirmação é obrigatório")

if __name__ == "__main__":
    asyncio.run(main()) 