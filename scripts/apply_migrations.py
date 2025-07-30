#!/usr/bin/env python3
"""
Script para aplicar migrações do Supabase
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega variáveis de ambiente
load_dotenv()

def get_supabase_client() -> Client:
    """Retorna cliente do Supabase"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("❌ Erro: SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados no .env")
        sys.exit(1)
    
    return create_client(url, key)

def read_migration_file(migration_path: Path) -> str:
    """Lê arquivo de migração"""
    try:
        with open(migration_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo de migração não encontrado: {migration_path}")
        sys.exit(1)

def apply_migration(client: Client, migration_name: str, sql_content: str):
    """Aplica uma migração no Supabase"""
    try:
        print(f"🔄 Aplicando migração: {migration_name}")
        
        # Executa o SQL da migração
        result = client.rpc('exec_sql', {'sql': sql_content}).execute()
        
        print(f"✅ Migração {migration_name} aplicada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aplicar migração {migration_name}: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando aplicação de migrações do Supabase")
    print(f"📊 Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print()
    
    # Conecta ao Supabase
    try:
        client = get_supabase_client()
        print("✅ Conectado ao Supabase")
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {str(e)}")
        sys.exit(1)
    
    # Diretório de migrações
    migrations_dir = Path("supabase/migrations")
    
    if not migrations_dir.exists():
        print(f"❌ Diretório de migrações não encontrado: {migrations_dir}")
        sys.exit(1)
    
    # Lista arquivos de migração
    migration_files = sorted(migrations_dir.glob("*.sql"))
    
    if not migration_files:
        print("❌ Nenhum arquivo de migração encontrado")
        sys.exit(1)
    
    print(f"📁 Encontradas {len(migration_files)} migrações:")
    for migration_file in migration_files:
        print(f"   - {migration_file.name}")
    print()
    
    # Aplica cada migração
    success_count = 0
    for migration_file in migration_files:
        migration_name = migration_file.stem
        sql_content = read_migration_file(migration_file)
        
        if apply_migration(client, migration_name, sql_content):
            success_count += 1
        print()
    
    # Resumo
    print("📊 Resumo:")
    print(f"   ✅ Migrações aplicadas: {success_count}/{len(migration_files)}")
    
    if success_count == len(migration_files):
        print("🎉 Todas as migrações foram aplicadas com sucesso!")
    else:
        print("⚠️  Algumas migrações falharam. Verifique os logs acima.")
        sys.exit(1)

if __name__ == "__main__":
    main() 