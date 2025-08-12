-- Script para limpeza completa e recriação do usuário
-- Execute este script no Supabase Dashboard SQL Editor
-- ⚠️ ATENÇÃO: Este script limpa todos os dados do usuário

-- 1. LIMPEZA COMPLETA
-- Limpar tokens de confirmação
DELETE FROM email_confirmation_tokens 
WHERE email = 'revtonbr@gmail.com';

-- Limpar perfis órfãos
DELETE FROM user_profiles 
WHERE email = 'revtonbr@gmail.com';

-- 2. VERIFICAR LIMPEZA
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

-- 3. VERIFICAR CONFIGURAÇÃO DO SUPABASE
-- Verificar se o schema auth está acessível
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'auth' 
AND tablename = 'users';

-- 4. VERIFICAR PERMISSÕES
-- Verificar se temos acesso à tabela auth.users
SELECT 
    grantee,
    privilege_type,
    is_grantable
FROM information_schema.role_table_grants 
WHERE table_schema = 'auth' 
AND table_name = 'users'; 