-- Script rápido para resolver problema de email de confirmação
-- Execute este script no SQL Editor do Supabase Dashboard

-- 1. Verificar usuários existentes
SELECT 
    id,
    email,
    email_confirmed_at,
    created_at,
    CASE 
        WHEN email_confirmed_at IS NULL THEN '❌ Não confirmado'
        ELSE '✅ Confirmado'
    END as status
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- 2. Forçar confirmação de email
UPDATE auth.users 
SET 
    email_confirmed_at = NOW(),
    updated_at = NOW()
WHERE email = 'revtonbr@gmail.com';

-- 3. Verificar resultado
SELECT 
    id,
    email,
    email_confirmed_at,
    CASE 
        WHEN email_confirmed_at IS NULL THEN '❌ Não confirmado'
        ELSE '✅ Confirmado'
    END as status
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- 4. Mensagem de sucesso
DO $$
BEGIN
    RAISE NOTICE '✅ Email confirmado com sucesso!';
    RAISE NOTICE '🎉 Agora você pode fazer login normalmente.';
    RAISE NOTICE '📋 Credenciais:';
    RAISE NOTICE '   Email: revtonbr@gmail.com';
    RAISE NOTICE '   Senha: Minha@Senha1';
END $$; 