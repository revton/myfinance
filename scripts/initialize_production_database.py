#!/usr/bin/env python3
"""
Script para inicializar o banco de dados em produção
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
        print("❌ DATABASE_URL não está configurada")
        print("💡 Configure a variável DATABASE_URL com a URL do banco de produção")
        return False
    
    if environment != "production":
        print("⚠️  Aviso: Você não está em ambiente de produção")
        response = input("Deseja continuar mesmo assim? (s/N): ").strip().lower()
        if response != 's':
            print("❌ Operação cancelada")
            return False
    
    return True

def initialize_database():
    """Inicializa o banco de dados"""
    print("🎯 Inicializando banco de dados...")
    
    # Verifica se já existem tabelas
    print("🔍 Verificando estado atual do banco...")
    result = run_command("alembic current", "verificando estado do banco")
    
    if not result:
        print("❌ Falha ao verificar estado do banco")
        return False
    
    # Se já houver migrações aplicadas, pergunta se deseja continuar
    # (isso evita aplicar migrações desnecessariamente)
    
    # Aplica todas as migrações
    print("🚀 Aplicando todas as migrações...")
    result = run_command("alembic upgrade head", "aplicando migrações")
    
    if not result:
        print("❌ Falha ao aplicar migrações")
        return False
    
    # Verifica o status final
    print("📊 Verificando status final...")
    result = run_command("alembic current", "verificando status final")
    
    if not result:
        print("❌ Falha ao verificar status final")
        return False
    
    return True

def main():
    """Função principal"""
    print("🚀 Inicialização do Banco de Dados - Produção")
    print("=" * 50)
    
    # Verifica ambiente
    if not check_environment():
        sys.exit(1)
    
    print()
    
    # Confirmação
    print("⚠️  Esta operação irá:")
    print("   1. Verificar o estado atual do banco")
    print("   2. Aplicar todas as migrações pendentes")
    print("   3. Criar tabelas que não existirem")
    print()
    
    response = input("Deseja continuar? (s/N): ").strip().lower()
    if response != 's':
        print("❌ Operação cancelada")
        return
    
    print()
    
    # Inicializa banco
    if initialize_database():
        print("\n✅ Banco de dados inicializado com sucesso!")
        print("💡 Verifique o status acima para confirmar")
    else:
        print("\n❌ Falha ao inicializar banco de dados")
        print("💡 Verifique os logs acima para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()