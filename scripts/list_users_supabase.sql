-- Script para listar todos os usuários no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard para verificar usuários existentes

-- Listar todos os usuários do Supabase Auth
SELECT 
    'auth.users' as tabela,
    id,
    email,
    created_at,
    last_sign_in_at,
    CASE 
        WHEN email_confirmed_at IS NOT NULL THEN 'Confirmado'
        ELSE 'Não confirmado'
    END as status_email
FROM auth.users
ORDER BY created_at DESC;

-- Listar todos os perfis de usuários
SELECT 
    'public.user_profiles' as tabela,
    user_id,
    email,
    full_name,
    created_at,
    updated_at
FROM public.user_profiles
ORDER BY created_at DESC;

-- Contar total de registros
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

-- Verificar se há transações com user_id
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'transactions' 
        AND column_name = 'user_id'
        AND table_schema = 'public'
    ) THEN
        RAISE NOTICE '📊 Transações com user_id:';
        PERFORM 
            user_id,
            COUNT(*) as total_transacoes
        FROM public.transactions 
        WHERE user_id IS NOT NULL 
        GROUP BY user_id
        ORDER BY total_transacoes DESC;
    ELSE
        RAISE NOTICE 'ℹ️ Tabela transactions não possui coluna user_id';
    END IF;
END $$; 