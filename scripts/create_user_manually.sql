-- Script para criar usuário manualmente no Supabase Auth
-- Execute no SQL Editor do Supabase Dashboard

-- 1. Criar usuário na tabela auth.users
INSERT INTO auth.users (
    id, 
    instance_id, 
    aud, 
    role, 
    email, 
    encrypted_password, 
    email_confirmed_at, 
    created_at, 
    updated_at,
    confirmation_token,
    email_change_token_new,
    recovery_token
) VALUES (
    '5cf56f65-c8c2-4de2-861e-cfe16c8d5052'::uuid,  -- user_id do perfil existente
    '00000000-0000-0000-0000-000000000000'::uuid,  -- instance_id padrão
    'authenticated',                                -- aud
    'authenticated',                                -- role
    'revtonbr@gmail.com',                          -- email
    crypt('Minha@Senha1', gen_salt('bf')),         -- senha criptografada
    NOW(),                                          -- email_confirmed_at (já confirmado)
    NOW(),                                          -- created_at
    NOW(),                                          -- updated_at
    '',                                             -- confirmation_token
    '',                                             -- email_change_token_new
    ''                                              -- recovery_token
);

-- 2. Verificar se foi criado
SELECT id, email, email_confirmed_at, created_at 
FROM auth.users 
WHERE email = 'revtonbr@gmail.com';

-- 3. Verificar se o perfil existe
SELECT * FROM user_profiles 
WHERE email = 'revtonbr@gmail.com'; 