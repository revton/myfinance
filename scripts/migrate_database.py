#!/usr/bin/env python3
"""
Script para gerar e aplicar migrações usando Alembic baseado nos modelos Pydantic
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    print(f"   Comando: {command}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            print(f"✅ {description} concluído com sucesso!")
            if result.stdout:
                print(f"   Saída: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erro ao {description.lower()}:")
            print(f"   Erro: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Exceção ao {description.lower()}: {str(e)}")
        return False

def check_environment():
    """Verifica se o ambiente está configurado"""
    print("🔍 Verificando configuração do ambiente...")
    
    environment = os.getenv("ENVIRONMENT", "development")
    database_url = os.getenv("DATABASE_URL")
    
    print(f"   Ambiente: {environment}")
    print(f"   DATABASE_URL: {'Configurado' if database_url else 'Não configurado'}")
    
    if not database_url:
        print("❌ DATABASE_URL não está configurado no .env")
        print("💡 Configure a variável DATABASE_URL com a URL do banco Supabase")
        return False
    
    return True

def generate_migration(message):
    """Gera uma nova migração baseada nos modelos"""
    print(f"📝 Gerando migração: {message}")
    
    # Comando para gerar migração
    command = f'uv run alembic revision --autogenerate -m "{message}"'
    
    if run_command(command, "Gerando migração"):
        print("✅ Migração gerada com sucesso!")
        return True
    else:
        print("❌ Falha ao gerar migração")
        return False

def apply_migrations():
    """Aplica as migrações pendentes"""
    print("🚀 Aplicando migrações...")
    
    # Comando para aplicar migrações
    command = "uv run alembic upgrade head"
    
    if run_command(command, "Aplicando migrações"):
        print("✅ Migrações aplicadas com sucesso!")
        return True
    else:
        print("❌ Falha ao aplicar migrações")
        return False

def show_migration_status():
    """Mostra o status das migrações"""
    print("📊 Status das migrações:")
    
    # Comando para mostrar status
    command = "uv run alembic current"
    
    if run_command(command, "Verificando status"):
        print("✅ Status verificado!")
    else:
        print("❌ Falha ao verificar status")

def create_initial_migration():
    """Cria a migração inicial baseada nos modelos Pydantic"""
    print("🎯 Criando migração inicial baseada nos modelos Pydantic...")
    
    # Verifica se já existe alguma migração
    versions_dir = Path("alembic/versions")
    existing_migrations = list(versions_dir.glob("*.py"))
    
    if existing_migrations:
        print(f"⚠️  Já existem {len(existing_migrations)} migrações:")
        for migration in existing_migrations:
            print(f"   - {migration.name}")
        
        response = input("Deseja criar uma nova migração? (s/N): ").strip().lower()
        if response != 's':
            print("❌ Operação cancelada")
            return False
    
    # Gera a migração inicial
    return generate_migration("Initial migration - Create transactions table from Pydantic models")

def main():
    """Função principal"""
    print("🚀 Sistema de Migrações com Pydantic e Alembic")
    print("=" * 50)
    
    # Verifica ambiente
    if not check_environment():
        sys.exit(1)
    
    print()
    
    # Menu de opções
    print("Escolha uma opção:")
    print("1. Criar migração inicial (baseada nos modelos Pydantic)")
    print("2. Gerar nova migração")
    print("3. Aplicar migrações pendentes")
    print("4. Verificar status das migrações")
    print("5. Sair")
    
    while True:
        try:
            choice = input("\nOpção (1-5): ").strip()
            
            if choice == "1":
                if create_initial_migration():
                    print("\n🎯 Próximos passos:")
                    print("1. Revise a migração gerada em alembic/versions/")
                    print("2. Execute: uv run python scripts/migrate_database.py")
                    print("3. Escolha opção 3 para aplicar as migrações")
                break
                
            elif choice == "2":
                message = input("Mensagem da migração: ").strip()
                if message:
                    generate_migration(message)
                else:
                    print("❌ Mensagem é obrigatória")
                break
                
            elif choice == "3":
                apply_migrations()
                break
                
            elif choice == "4":
                show_migration_status()
                break
                
            elif choice == "5":
                print("👋 Saindo...")
                break
                
            else:
                print("❌ Opção inválida. Escolha 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Operação cancelada pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            break

if __name__ == "__main__":
    main() 