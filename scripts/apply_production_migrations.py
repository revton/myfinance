#!/usr/bin/env python3
"""
Script para aplicar migrações no banco de dados de produção
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    print("🔍 Verificando configuração do ambiente...")
    
    environment = os.getenv("ENVIRONMENT", "development")
    database_url = os.getenv("DATABASE_URL")
    
    print(f"   Ambiente: {environment}")
    print(f"   DATABASE_URL: {'Configurado' if database_url else 'Não configurado'}")
    
    if not database_url:
        print("❌ DATABASE_URL não está configurada")
        print("💡 Configure a variável DATABASE_URL com a URL do banco de produção")
        return False
    
    return True

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

def show_current_status():
    """Mostra o status atual das migrações"""
    print("📊 Status atual das migrações:")
    return run_command("alembic current", "Verificando status das migrações")

def apply_migrations():
    """Aplica as migrações pendentes"""
    print("🚀 Aplicando migrações...")
    return run_command("alembic upgrade head", "Aplicando migrações")

def main():
    """Função principal"""
    print("🚀 Migração de Banco de Dados - Produção")
    print("=" * 50)
    
    # Verifica ambiente
    if not check_environment():
        sys.exit(1)
    
    print()
    
    # Mostra status atual
    if not show_current_status():
        print("❌ Falha ao verificar status das migrações")
        sys.exit(1)
    
    print()
    
    # Confirmação
    environment = os.getenv("ENVIRONMENT", "development")
    if environment != "production":
        print("⚠️  Atenção: Você não está em ambiente de produção!")
        response = input("Deseja continuar mesmo assim? (s/N): ").strip().lower()
        if response != 's':
            print("❌ Operação cancelada")
            return
    
    print()
    
    # Aplica migrações
    if apply_migrations():
        print("\n✅ Migrações aplicadas com sucesso!")
        print("💡 Verifique o status acima para confirmar")
    else:
        print("\n❌ Falha ao aplicar migrações")
        print("💡 Verifique os logs acima para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()