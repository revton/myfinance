-- Script para limpar dados do usuário revtonbr@gmail.com para testes
-- Execute este script no Supabase Dashboard SQL Editor

-- Limpar tokens de confirmação de email
DELETE FROM email_confirmation_tokens 
WHERE email = 'revtonbr@gmail.com';

-- Limpar perfis de usuário
DELETE FROM user_profiles 
WHERE email = 'revtonbr@gmail.com';

-- Limpar usuário do auth (se existir)
-- Nota: Esta operação pode falhar se o usuário não existir, mas não é problema
DELETE FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- Verificar se a limpeza foi bem-sucedida
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