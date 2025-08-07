#!/usr/bin/env python3
"""
Script para configurar variáveis de ambiente necessárias
Execute: uv run python scripts/setup_env_variables.py
"""

import os
from pathlib import Path

def setup_env_variables():
    """
    Configura as variáveis de ambiente necessárias
    """
    print("🔧 Configurando Variáveis de Ambiente")
    print("=" * 40)
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    # Verificar se .env existe
    if not env_file.exists():
        print("📄 Arquivo .env não encontrado")
        
        if env_example.exists():
            print("📋 Copiando env.example para .env...")
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Arquivo .env criado a partir do env.example")
        else:
            print("❌ Arquivo env.example não encontrado")
            return
    else:
        print("✅ Arquivo .env já existe")
    
    # Ler conteúdo atual
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar variáveis necessárias
    missing_vars = []
    
    if "SUPABASE_ACCESS_TOKEN" not in content:
        missing_vars.append("SUPABASE_ACCESS_TOKEN")
    
    if "RESEND_API_KEY" not in content:
        missing_vars.append("RESEND_API_KEY")
    
    if missing_vars:
        print(f"\n⚠️ Variáveis faltando: {', '.join(missing_vars)}")
        print("\n📝 Adicione as seguintes linhas ao arquivo .env:")
        print()
        
        for var in missing_vars:
            if var == "SUPABASE_ACCESS_TOKEN":
                print("# Token de acesso do Supabase (obtenha em: https://supabase.com/dashboard/account/tokens)")
                print("SUPABASE_ACCESS_TOKEN=sbp_sua_token_aqui")
            elif var == "RESEND_API_KEY":
                print("# API Key do Resend (obtenha em: https://resend.com)")
                print("RESEND_API_KEY=re_sua_api_key_aqui")
            print()
        
        print("🔗 Links úteis:")
        print("   - Supabase Access Token: https://supabase.com/dashboard/account/tokens")
        print("   - Resend API Key: https://resend.com")
        print()
        print("💡 Após adicionar as variáveis, execute novamente o script de configuração SMTP")
        return False
    else:
        print("✅ Todas as variáveis necessárias estão configuradas")
        return True

def main():
    """
    Função principal
    """
    print("🚀 Setup de Variáveis de Ambiente")
    print()
    
    success = setup_env_variables()
    
    if success:
        print("\n🎉 Setup concluído!")
        print("💡 Agora você pode executar: uv run python scripts/configure_smtp.py")
    else:
        print("\n⚠️ Setup incompleto")
        print("💡 Configure as variáveis no arquivo .env e execute novamente")

if __name__ == "__main__":
    main() 