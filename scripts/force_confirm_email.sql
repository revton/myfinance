-- Script para forçar confirmação de email manualmente no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard
-- ⚠️ ATENÇÃO: Use apenas em desenvolvimento/teste!

-- Configurações - MODIFIQUE AQUI o email que deseja confirmar
DO $$
DECLARE
    target_email TEXT := 'revtonbr@gmail.com'; -- MODIFIQUE AQUI o email
    user_id UUID;
    current_time TIMESTAMP WITH TIME ZONE := NOW();
BEGIN
    -- Verificar se estamos no ambiente correto
    IF current_setting('app.environment', true) IS NULL OR 
       current_setting('app.environment', true) NOT IN ('development', 'test', 'staging') THEN
        RAISE EXCEPTION 'Este script só pode ser executado em ambientes de desenvolvimento, teste ou staging!';
    END IF;

    -- Buscar o user_id pelo email
    SELECT id INTO user_id 
    FROM auth.users 
    WHERE email = target_email;
    
    IF user_id IS NOT NULL THEN
        -- Verificar status atual
        RAISE NOTICE '🔍 Status atual do usuário %:', target_email;
        PERFORM 
            id,
            email,
            email_confirmed_at,
            CASE 
                WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
                ELSE 'Confirmado'
            END as status
        FROM auth.users 
        WHERE id = user_id;
        
        -- Forçar confirmação de email
        UPDATE auth.users 
        SET 
            email_confirmed_at = current_time,
            updated_at = current_time
        WHERE id = user_id;
        
        RAISE NOTICE '✅ Email confirmado manualmente para: %', target_email;
        RAISE NOTICE '   Timestamp: %', current_time;
        
        -- Verificar status após confirmação
        RAISE NOTICE '🔍 Status após confirmação:';
        PERFORM 
            id,
            email,
            email_confirmed_at,
            CASE 
                WHEN email_confirmed_at IS NULL THEN 'Não confirmado'
                ELSE 'Confirmado'
            END as status
        FROM auth.users 
        WHERE id = user_id;
        
    ELSE
        RAISE NOTICE '❌ Usuário com email % não encontrado', target_email;
    END IF;
END $$;

-- Verificar resultado
SELECT 
    'auth.users' as tabela,
    COUNT(*) as total_usuarios,
    COUNT(email_confirmed_at) as usuarios_confirmados,
    COUNT(*) - COUNT(email_confirmed_at) as usuarios_nao_confirmados
FROM auth.users; 