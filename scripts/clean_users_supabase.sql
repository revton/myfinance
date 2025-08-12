-- Script para limpar usuários no Supabase para testes
-- Execute este script no SQL Editor do Supabase Dashboard
-- ⚠️ ATENÇÃO: Este script irá DELETAR TODOS os dados de usuários!

-- Verificar se estamos no ambiente correto
DO $$
BEGIN
    -- Verificar se estamos em um ambiente de desenvolvimento/teste
    IF current_setting('app.environment', true) IS NULL OR 
       current_setting('app.environment', true) NOT IN ('development', 'test', 'staging') THEN
        RAISE EXCEPTION 'Este script só pode ser executado em ambientes de desenvolvimento, teste ou staging!';
    END IF;
END $$;

-- 1. Limpar dados de transações (se houver user_id)
-- Primeiro, verificar se a coluna user_id existe na tabela transactions
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'transactions' 
        AND column_name = 'user_id'
        AND table_schema = 'public'
    ) THEN
        -- Se a coluna user_id existe, limpar transações de usuários
        DELETE FROM public.transactions WHERE user_id IS NOT NULL;
        RAISE NOTICE 'Transações de usuários removidas';
    ELSE
        RAISE NOTICE 'Tabela transactions não possui coluna user_id - pulando limpeza de transações';
    END IF;
END $$;

-- 2. Limpar perfis de usuários
DELETE FROM public.user_profiles;
RAISE NOTICE 'Perfis de usuários removidos';

-- 3. Limpar usuários do Supabase Auth
-- ⚠️ IMPORTANTE: Esta operação é irreversível!
-- Deletar todos os usuários da tabela auth.users
DELETE FROM auth.users;
RAISE NOTICE 'Usuários do Supabase Auth removidos';

-- 4. Resetar sequências (se houver)
DO $$
DECLARE
    seq_record RECORD;
BEGIN
    FOR seq_record IN 
        SELECT sequence_name 
        FROM information_schema.sequences 
        WHERE sequence_schema = 'public'
    LOOP
        EXECUTE format('ALTER SEQUENCE %I RESTART WITH 1', seq_record.sequence_name);
    END LOOP;
    RAISE NOTICE 'Sequências resetadas';
END $$;

-- 5. Verificar limpeza
SELECT 
    'auth.users' as tabela,
    COUNT(*) as total_registros
FROM auth.users
UNION ALL
SELECT 
    'public.user_profiles' as tabela,
    COUNT(*) as total_registros
FROM public.user_profiles
UNION ALL
SELECT 
    'public.transactions' as tabela,
    COUNT(*) as total_registros
FROM public.transactions;

-- 6. Notificar PostgREST para recarregar o schema
NOTIFY pgrst, 'reload schema';

RAISE NOTICE '✅ Limpeza de usuários concluída com sucesso!';
RAISE NOTICE '📋 Próximos passos:';
RAISE NOTICE '   1. Execute os testes novamente';
RAISE NOTICE '   2. Registre novos usuários para teste';
RAISE NOTICE '   3. Verifique se as funcionalidades estão funcionando corretamente'; 