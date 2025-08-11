-- Script para limpar dados órfãos do usuário revtonbr@gmail.com
-- Execute este script no Supabase Dashboard SQL Editor

-- 1. Limpar tokens de confirmação
DELETE FROM email_confirmation_tokens 
WHERE email = 'revtonbr@gmail.com';

-- 2. Limpar perfis órfãos (sem usuário correspondente em auth.users)
DELETE FROM user_profiles 
WHERE email = 'revtonbr@gmail.com';

-- 3. Verificar se a limpeza foi bem-sucedida
SELECT 
    'auth.users' as tabela,
    COUNT(*) as registros
FROM auth.users 
WHERE email = 'revtonbr@gmail.com'

UNION ALL

SELECT 
    'user_profiles' as tabela,
    COUNT(*) as registros
FROM user_profiles 
WHERE email = 'revtonbr@gmail.com'

UNION ALL

SELECT 
    'email_confirmation_tokens' as tabela,
    COUNT(*) as registros
FROM email_confirmation_tokens 
WHERE email = 'revtonbr@gmail.com'; 