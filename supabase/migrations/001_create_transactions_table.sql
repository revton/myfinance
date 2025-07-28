-- Criar tabela de transações
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

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at
CREATE TRIGGER update_transactions_updated_at 
    BEFORE UPDATE ON transactions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Habilitar Row Level Security (RLS)
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (pode ser ajustada depois)
CREATE POLICY "Allow all operations" ON transactions
    FOR ALL USING (true);

-- Comentários para documentação
COMMENT ON TABLE transactions IS 'Tabela para armazenar receitas e despesas';
COMMENT ON COLUMN transactions.id IS 'ID único da transação';
COMMENT ON COLUMN transactions.type IS 'Tipo da transação: income (receita) ou expense (despesa)';
COMMENT ON COLUMN transactions.amount IS 'Valor da transação (sempre positivo)';
COMMENT ON COLUMN transactions.description IS 'Descrição da transação';
COMMENT ON COLUMN transactions.created_at IS 'Data de criação da transação';
COMMENT ON COLUMN transactions.updated_at IS 'Data da última atualização da transação'; 