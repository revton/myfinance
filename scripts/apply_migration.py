#!/usr/bin/env python3
"""
Script para aplicar migração no Supabase
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

def apply_migration():
    """Aplica a migração no Supabase"""
    print("🚀 Aplicando migração no Supabase...")
    
    # SQL da migração baseada nos modelos Pydantic
    migration_sql = """
-- =============================================================================
-- MIGRAÇÃO INICIAL - TABELA TRANSACTIONS BASEADA NOS MODELOS PYDANTIC
-- =============================================================================

-- Criar tabela de transações baseada no modelo Transaction
CREATE TABLE IF NOT EXISTS transactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount FLOAT NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL CHECK (length(description) >= 1 AND length(description) <= 500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);

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

-- Habilitar Row Level Security (RLS)
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (pode ser ajustada depois)
DROP POLICY IF EXISTS "Allow all operations" ON transactions;
CREATE POLICY "Allow all operations" ON transactions
    FOR ALL USING (true);

-- Comentários para documentação
COMMENT ON TABLE transactions IS 'Tabela para armazenar receitas e despesas - baseada no modelo Transaction do FastAPI';
COMMENT ON COLUMN transactions.id IS 'ID único da transação (UUID)';
COMMENT ON COLUMN transactions.type IS 'Tipo da transação: income (receita) ou expense (despesa)';
COMMENT ON COLUMN transactions.amount IS 'Valor da transação (sempre positivo, FLOAT)';
COMMENT ON COLUMN transactions.description IS 'Descrição da transação (TEXT, 1-500 caracteres)';
COMMENT ON COLUMN transactions.created_at IS 'Data de criação da transação (TIMESTAMP WITH TIME ZONE)';
COMMENT ON COLUMN transactions.updated_at IS 'Data da última atualização da transação (TIMESTAMP WITH TIME ZONE)';
"""
    
    try:
        # Conecta ao Supabase
        client = get_supabase_client()
        print("✅ Conectado ao Supabase")
        
        # Testa se a tabela já existe
        try:
            client.table("transactions").select("id").limit(1).execute()
            print("✅ Tabela transactions já existe")
            return True
        except Exception as e:
            if "Could not find the table" in str(e):
                print("📝 Tabela não existe, execute o SQL manualmente:")
                print()
                print("=" * 80)
                print(migration_sql)
                print("=" * 80)
                print()
                
                # Extrai o URL do projeto do SUPABASE_URL
                supabase_url = os.getenv("SUPABASE_URL", "")
                if supabase_url:
                    project_id = supabase_url.split("//")[1].split(".")[0]
                    sql_editor_url = f"https://supabase.com/dashboard/project/{project_id}/sql"
                    print(f"🔗 Acesse o SQL Editor: {sql_editor_url}")
                
                return False
            else:
                print(f"❌ Erro ao verificar tabela: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {str(e)}")
        return False

def test_migration():
    """Testa se a migração foi aplicada corretamente"""
    print("🧪 Testando migração aplicada...")
    
    try:
        client = get_supabase_client()
        
        # Testa consulta básica
        result = client.table("transactions").select("*").limit(5).execute()
        print(f"✅ Migração funcionando! Encontradas {len(result.data)} transações")
        
        # Testa inserção
        test_data = {
            "type": "income",
            "amount": 100.00,
            "description": "Teste de migração"
        }
        
        insert_result = client.table("transactions").insert(test_data).execute()
        if insert_result.data:
            print("✅ Inserção funcionando!")
            
            # Remove o teste
            test_id = insert_result.data[0]['id']
            client.table("transactions").delete().eq("id", test_id).execute()
            print("✅ Remoção funcionando!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar migração: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🚀 Sistema de Migração com Pydantic e Alembic")
    print("=" * 50)
    
    environment = os.getenv("ENVIRONMENT", "development")
    print(f"📊 Ambiente: {environment}")
    print()
    
    # Aplica migração
    if apply_migration():
        # Testa migração
        if test_migration():
            print("🎉 Migração aplicada e testada com sucesso!")
        else:
            print("⚠️  Migração aplicada mas teste falhou")
    else:
        print("⚠️  Execute o SQL manualmente no Supabase SQL Editor")
        print("💡 Depois execute: uv run python scripts/apply_migration.py --test")

if __name__ == "__main__":
    main() 