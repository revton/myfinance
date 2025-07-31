#!/usr/bin/env python3
"""
Script para configurar a tabela transactions no Supabase
"""
import os
import sys
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

def setup_transactions_table(client: Client):
    """Configura a tabela transactions"""
    print("🔄 Configurando tabela transactions...")
    
    # SQL para criar a tabela
    create_table_sql = """
    -- Criar tabela de transações
    CREATE TABLE IF NOT EXISTS transactions (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
        amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
        description TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    # SQL para criar índices
    create_indexes_sql = """
    -- Criar índices para melhor performance
    CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
    CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);
    """
    
    # SQL para criar função e trigger
    create_trigger_sql = """
    -- Função para atualizar updated_at automaticamente
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    -- Trigger para atualizar updated_at
    DROP TRIGGER IF EXISTS update_transactions_updated_at ON transactions;
    CREATE TRIGGER update_transactions_updated_at 
        BEFORE UPDATE ON transactions 
        FOR EACH ROW 
        EXECUTE FUNCTION update_updated_at_column();
    """
    
    # SQL para configurar RLS
    setup_rls_sql = """
    -- Habilitar Row Level Security (RLS)
    ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

    -- Política para permitir todas as operações (pode ser ajustada depois)
    DROP POLICY IF EXISTS "Allow all operations" ON transactions;
    CREATE POLICY "Allow all operations" ON transactions
        FOR ALL USING (true);
    """
    
    try:
        # Executa os comandos SQL
        print("📝 Criando tabela...")
        client.table("transactions").select("id").limit(1).execute()
        print("✅ Tabela já existe")
        
    except Exception as e:
        print("❌ Tabela não existe ou erro de acesso")
        print("💡 Execute o seguinte SQL no Supabase SQL Editor:")
        print()
        print("=" * 60)
        print(create_table_sql)
        print(create_indexes_sql)
        print(create_trigger_sql)
        print(setup_rls_sql)
        print("=" * 60)
        print()
        print("🔗 Acesse: https://supabase.com/dashboard/project/[SEU_PROJETO]/sql")
        return False
    
    return True

def test_table_access(client: Client):
    """Testa acesso à tabela"""
    print("🧪 Testando acesso à tabela...")
    
    try:
        # Tenta fazer uma consulta simples
        result = client.table("transactions").select("id").limit(1).execute()
        print("✅ Acesso à tabela funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao acessar tabela: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🚀 Configurando banco de dados do Supabase")
    print(f"📊 Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print()
    
    # Conecta ao Supabase
    try:
        client = get_supabase_client()
        print("✅ Conectado ao Supabase")
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {str(e)}")
        sys.exit(1)
    
    # Configura tabela
    if setup_transactions_table(client):
        # Testa acesso
        if test_table_access(client):
            print("🎉 Banco de dados configurado com sucesso!")
        else:
            print("⚠️  Problemas de acesso à tabela")
            sys.exit(1)
    else:
        print("⚠️  Execute o SQL manualmente no Supabase")
        sys.exit(1)

if __name__ == "__main__":
    main() 