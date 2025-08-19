#!/usr/bin/env python3
"""
Script para verificar o status das migrações do banco de dados
"""
import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    
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

def main():
    """Função principal"""
    print("📊 Verificação de Status das Migrações")
    print("=" * 50)
    
    # Verifica ambiente
    environment = os.getenv("ENVIRONMENT", "development")
    database_url = os.getenv("DATABASE_URL")
    
    print(f"   Ambiente: {environment}")
    print(f"   Banco de dados: {'Configurado' if database_url else 'Não configurado'}")
    
    print()
    
    # Mostra status atual
    print("📊 Status atual das migrações:")
    if not run_command("alembic current", "Verificando status das migrações"):
        print("❌ Falha ao verificar status das migrações")
        return
    
    print()
    
    # Mostra histórico
    print("📋 Histórico de migrações:")
    if not run_command("alembic history --verbose", "Verificando histórico de migrações"):
        print("❌ Falha ao verificar histórico de migrações")
        return

if __name__ == "__main__":
    main()