-- MyFinance Database Setup
-- Script para criar as tabelas necessárias no Supabase

-- Criar a tabela transactions
CREATE TABLE IF NOT EXISTS public.transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_transactions_type ON public.transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON public.transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON public.transactions(amount);

-- Criar função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Criar trigger para atualizar updated_at
DROP TRIGGER IF EXISTS update_transactions_updated_at ON public.transactions;
CREATE TRIGGER update_transactions_updated_at
    BEFORE UPDATE ON public.transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Inserir dados de exemplo (opcional - remover em produção)
INSERT INTO public.transactions (type, amount, description) VALUES
    ('income', 2500.00, 'Salário Janeiro'),
    ('expense', 350.00, 'Supermercado'),
    ('expense', 80.00, 'Combustível'),
    ('income', 200.00, 'Freelance'),
    ('expense', 1200.00, 'Aluguel')
ON CONFLICT (id) DO NOTHING;

-- Comentários para documentação
COMMENT ON TABLE public.transactions IS 'Tabela para armazenar todas as transações financeiras (receitas e despesas)';
COMMENT ON COLUMN public.transactions.id IS 'Identificador único da transação';
COMMENT ON COLUMN public.transactions.type IS 'Tipo da transação: income (receita) ou expense (despesa)';
COMMENT ON COLUMN public.transactions.amount IS 'Valor da transação em reais (sempre positivo)';
COMMENT ON COLUMN public.transactions.description IS 'Descrição detalhada da transação';
COMMENT ON COLUMN public.transactions.created_at IS 'Data e hora de criação da transação';
COMMENT ON COLUMN public.transactions.updated_at IS 'Data e hora da última atualização da transação';