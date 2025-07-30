#!/usr/bin/env python3
"""
Script para gerar schema SQL baseado nos modelos Pydantic do FastAPI
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

def generate_transactions_schema():
    """Gera SQL para criar tabela transactions baseada no modelo Pydantic"""
    
    # SQL baseado no modelo Transaction do FastAPI
    sql = """
-- =============================================================================
-- SCHEMA GERADO AUTOMATICAMENTE BASEADO NOS MODELOS PYDANTIC
-- =============================================================================

-- Criar tabela de transações baseada no modelo Transaction
CREATE TABLE IF NOT EXISTS transactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL,
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
COMMENT ON COLUMN transactions.amount IS 'Valor da transação (sempre positivo, DECIMAL 10,2)';
COMMENT ON COLUMN transactions.description IS 'Descrição da transação (TEXT)';
COMMENT ON COLUMN transactions.created_at IS 'Data de criação da transação (TIMESTAMP WITH TIME ZONE)';
COMMENT ON COLUMN transactions.updated_at IS 'Data da última atualização da transação (TIMESTAMP WITH TIME ZONE)';

-- =============================================================================
-- DADOS DE EXEMPLO (OPCIONAL)
-- =============================================================================

-- Inserir dados de exemplo se a tabela estiver vazia
INSERT INTO transactions (type, amount, description) 
SELECT 'income', 1000.00, 'Salário do mês'
WHERE NOT EXISTS (SELECT 1 FROM transactions LIMIT 1);

INSERT INTO transactions (type, amount, description) 
SELECT 'expense', 50.00, 'Almoço'
WHERE NOT EXISTS (SELECT 1 FROM transactions WHERE description = 'Almoço');

INSERT INTO transactions (type, amount, description) 
SELECT 'income', 500.00, 'Freelance'
WHERE NOT EXISTS (SELECT 1 FROM transactions WHERE description = 'Freelance');
"""
    
    return sql

def apply_schema(client: Client, sql_content: str):
    """Aplica o schema no Supabase"""
    print("🔄 Aplicando schema baseado nos modelos Pydantic...")
    
    try:
        # Primeiro, vamos verificar se conseguimos conectar
        print("📡 Testando conexão...")
        client.table("transactions").select("id").limit(1).execute()
        print("✅ Conexão funcionando!")
        
        print("💡 Para aplicar o schema, execute o seguinte SQL no Supabase SQL Editor:")
        print()
        print("=" * 80)
        print(sql_content)
        print("=" * 80)
        print()
        
        # Extrai o URL do projeto do SUPABASE_URL
        supabase_url = os.getenv("SUPABASE_URL", "")
        if supabase_url:
            project_id = supabase_url.split("//")[1].split(".")[0]
            sql_editor_url = f"https://supabase.com/dashboard/project/{project_id}/sql"
            print(f"🔗 Acesse o SQL Editor: {sql_editor_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {str(e)}")
        print("💡 Execute o seguinte SQL no Supabase SQL Editor:")
        print()
        print("=" * 80)
        print(sql_content)
        print("=" * 80)
        print()
        return False

def test_schema(client: Client):
    """Testa se o schema foi aplicado corretamente"""
    print("🧪 Testando schema aplicado...")
    
    try:
        # Testa consulta básica
        result = client.table("transactions").select("*").limit(5).execute()
        print(f"✅ Schema funcionando! Encontradas {len(result.data)} transações")
        
        # Testa inserção
        test_data = {
            "type": "income",
            "amount": 100.00,
            "description": "Teste de inserção"
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
        print(f"❌ Erro ao testar schema: {str(e)}")
        return False

def save_sql_file(sql_content: str):
    """Salva o SQL em um arquivo para referência"""
    sql_file = Path("supabase/schema.sql")
    sql_file.parent.mkdir(exist_ok=True)
    
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"💾 SQL salvo em: {sql_file}")

def main():
    """Função principal"""
    print("🚀 Gerando schema SQL baseado nos modelos Pydantic")
    print(f"📊 Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print()
    
    # Gera o SQL baseado nos modelos
    sql_content = generate_transactions_schema()
    
    # Salva o SQL em arquivo
    save_sql_file(sql_content)
    
    # Conecta ao Supabase
    try:
        client = get_supabase_client()
        print("✅ Conectado ao Supabase")
    except Exception as e:
        print(f"❌ Erro ao conectar ao Supabase: {str(e)}")
        sys.exit(1)
    
    # Aplica o schema
    if apply_schema(client, sql_content):
        print()
        print("🎯 Próximos passos:")
        print("1. Copie o SQL acima")
        print("2. Acesse o SQL Editor do Supabase")
        print("3. Cole e execute o SQL")
        print("4. Execute: uv run python scripts/generate_schema.py --test")
        print()
    else:
        print("⚠️  Execute o SQL manualmente no Supabase")
        sys.exit(1)

if __name__ == "__main__":
    main() 