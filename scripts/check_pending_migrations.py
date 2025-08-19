#!/usr/bin/env python3
"""
Script para verificar se há migrações pendentes antes de aplicar
"""
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def run_command(command, description):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path.cwd()
        )
        return result
    except Exception as e:
        print(f"❌ Erro ao executar {description}: {str(e)}")
        return None

def check_pending_migrations():
    """Verifica se há migrações pendentes"""
    print("🔍 Verificando migrações pendentes...")
    
    # Verifica o status atual
    result = run_command("uv run alembic current", "verificar status das migrações")
    if not result:
        return False
    
    if result.returncode != 0:
        print(f"❌ Erro ao verificar status: {result.stderr}")
        return False
    
    current_revision = result.stdout.strip()
    print(f"   Revisão atual: {current_revision if current_revision else 'Nenhuma'}")
    
    # Verifica o head
    result = run_command("uv run alembic heads", "verificar head das migrações")
    if not result:
        return False
    
    if result.returncode != 0:
        print(f"❌ Erro ao verificar head: {result.stderr}")
        return False
    
    head_revision = result.stdout.strip()
    print(f"   Head: {head_revision if head_revision else 'Nenhuma'}")
    
    # Compara as revisões
    if current_revision == head_revision:
        print("✅ Nenhuma migração pendente")
        return False
    else:
        print("⚠️  Há migrações pendentes")
        return True

def main():
    """Função principal"""
    print("🚀 Verificação de Migrações Pendentes")
    print("=" * 50)
    
    # Verifica ambiente
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL não está configurada")
        sys.exit(1)
    
    print(f"   Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   Banco de dados: Configurado")
    
    print()
    
    # Verifica migrações pendentes
    if check_pending_migrations():
        print("\n💡 Execute 'uv run alembic upgrade head' para aplicar as migrações")
        sys.exit(0)  # Exit code 0 indica que há migrações pendentes (não é erro)
    else:
        print("\n✅ Nenhuma migração pendente")
        sys.exit(0)

if __name__ == "__main__":
    main()