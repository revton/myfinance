-- Script para diagnosticar problemas com email de confirmação no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard

-- 1. Verificar configurações de email no Supabase
SELECT 
    'Configurações de Email' as secao,
    'Verifique no Dashboard > Settings > Auth > Email Templates' as instrucao;

-- 2. Verificar usuários não confirmados
SELECT 
    'Usuários Não Confirmados' as secao,
    id,
    email,
    created_at,
    email_confirmed_at,
    CASE 
        WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
        ELSE 'Confirmado'
    END as status_email,
    last_sign_in_at,
    CASE 
        WHEN last_sign_in_at IS NULL THEN 'Nunca fez login'
        ELSE 'Já fez login'
    END as status_login
FROM auth.users 
WHERE email_confirmed_at IS NULL
ORDER BY created_at DESC;

-- 3. Verificar todos os usuários recentes
SELECT 
    'Todos os Usuários Recentes' as secao,
    id,
    email,
    created_at,
    email_confirmed_at,
    last_sign_in_at,
    CASE 
        WHEN email_confirmed_at IS NULL THEN '❌ Não confirmado'
        ELSE '✅ Confirmado'
    END as status_email
FROM auth.users 
ORDER BY created_at DESC
LIMIT 10;

-- 4. Verificar se há problemas com o email específico
DO $$
DECLARE
    target_email TEXT := 'revtonbr@gmail.com'; -- MODIFIQUE AQUI o email
    user_record RECORD;
BEGIN
    SELECT * INTO user_record 
    FROM auth.users 
    WHERE email = target_email;
    
    IF user_record IS NOT NULL THEN
        RAISE NOTICE '🔍 Diagnóstico para o email: %', target_email;
        RAISE NOTICE '   ID: %', user_record.id;
        RAISE NOTICE '   Criado em: %', user_record.created_at;
        RAISE NOTICE '   Email confirmado em: %', user_record.email_confirmed_at;
        RAISE NOTICE '   Último login: %', user_record.last_sign_in_at;
        
        IF user_record.email_confirmed_at IS NULL THEN
            RAISE NOTICE '   ❌ PROBLEMA: Email não foi confirmado!';
            RAISE NOTICE '   📧 Soluções:';
            RAISE NOTICE '      1. Verifique a caixa de spam';
            RAISE NOTICE '      2. Use o endpoint /auth/resend-confirmation';
            RAISE NOTICE '      3. Verifique configurações de SMTP no Supabase';
        ELSE
            RAISE NOTICE '   ✅ Email já foi confirmado';
        END IF;
    ELSE
        RAISE NOTICE '❌ Usuário com email % não encontrado', target_email;
    END IF;
END $$;

-- 5. Verificar configurações de autenticação
SELECT 
    'Configurações de Auth' as secao,
    'Verifique no Dashboard > Settings > Auth:' as instrucao;

-- 6. Verificar se há logs de email (se disponível)
DO $$
BEGIN
    RAISE NOTICE '📋 Próximos passos para resolver:';
    RAISE NOTICE '   1. Acesse Supabase Dashboard > Settings > Auth';
    RAISE NOTICE '   2. Verifique se "Enable email confirmations" está ativado';
    RAISE NOTICE '   3. Verifique configurações de SMTP/Email Provider';
    RAISE NOTICE '   4. Teste o template de email de confirmação';
    RAISE NOTICE '   5. Use o endpoint /auth/resend-confirmation para reenviar';
    RAISE NOTICE '   6. Verifique logs em Dashboard > Logs > Auth';
END $$; 