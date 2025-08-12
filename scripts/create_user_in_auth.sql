-- Script para criar usuário manualmente na tabela auth.users
-- Execute este script no Supabase Dashboard SQL Editor
-- ⚠️ ATENÇÃO: Este script modifica o schema auth diretamente

-- 1. Primeiro, verificar se o usuário já existe
SELECT id, email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- 2. Se não existir, criar o usuário manualmente
-- Usando o user_id do perfil existente: f88cce88-af36-4149-b783-d0bb7107a4d2
INSERT INTO auth.users (
    id,
    instance_id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    recovery_sent_at,
    last_sign_in_at,
    raw_app_meta_data,
    raw_user_meta_data,
    created_at,
    updated_at,
    confirmation_token,
    email_change,
    email_change_token_new,
    recovery_token
) VALUES (
    'f88cce88-af36-4149-b783-d0bb7107a4d2'::uuid,  -- ID do perfil existente
    '00000000-0000-0000-0000-000000000000'::uuid,  -- instance_id padrão
    'authenticated',                                -- aud
    'authenticated',                                -- role
    'revtonbr@gmail.com',                          -- email
    crypt('Minha@Senha1', gen_salt('bf')),         -- senha criptografada
    NOW(),                                         -- email_confirmed_at (já confirmado)
    NULL,                                          -- recovery_sent_at
    NULL,                                          -- last_sign_in_at
    '{"provider": "email", "providers": ["email"]}', -- raw_app_meta_data
    '{"full_name": "Revton Dev Corrigido"}',       -- raw_user_meta_data
    NOW(),                                         -- created_at
    NOW(),                                         -- updated_at
    '',                                            -- confirmation_token
    '',                                            -- email_change
    '',                                            -- email_change_token_new
    ''                                             -- recovery_token
) ON CONFLICT (id) DO UPDATE SET
    email_confirmed_at = NOW(),
    updated_at = NOW();

-- 3. Verificar se foi criado com sucesso
SELECT id, email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- 4. Verificar se o perfil está correto
SELECT * FROM user_profiles 
WHERE email = 'revtonbr@gmail.com'; 