-- Script para limpar usuários específicos no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard
-- ⚠️ ATENÇÃO: Este script irá DELETAR usuários específicos!

-- Configurações - MODIFIQUE AQUI os emails dos usuários que deseja limpar
-- Exemplo: ['teste@example.com', 'usuario.teste@email.com']
DO $$
DECLARE
    emails_to_delete TEXT[] := ARRAY[
        'revtonbr@gmail.com'
        -- Adicione mais emails conforme necessário
    ];
    user_email TEXT;
    user_id UUID;
    deleted_count INTEGER := 0;
BEGIN
    -- Verificar se estamos no ambiente correto
    IF current_setting('app.environment', true) IS NULL OR 
       current_setting('app.environment', true) NOT IN ('development', 'test', 'staging') THEN
        RAISE EXCEPTION 'Este script só pode ser executado em ambientes de desenvolvimento, teste ou staging!';
    END IF;

    RAISE NOTICE '🔍 Iniciando limpeza de usuários específicos...';
    RAISE NOTICE '📧 Emails que serão removidos: %', array_to_string(emails_to_delete, ', ');

    -- Para cada email na lista, deletar o usuário e seus dados relacionados
    FOREACH user_email IN ARRAY emails_to_delete
    LOOP
        -- Buscar o user_id pelo email
        SELECT id INTO user_id 
        FROM auth.users 
        WHERE email = user_email;
        
        IF user_id IS NOT NULL THEN
            -- 1. Deletar transações do usuário (se houver user_id na tabela)
            IF EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name = 'transactions' 
                AND column_name = 'user_id'
                AND table_schema = 'public'
            ) THEN
                DELETE FROM public.transactions WHERE user_id = user_id;
                RAISE NOTICE '   ✅ Transações do usuário % removidas', user_email;
            END IF;
            
            -- 2. Deletar perfil do usuário
            DELETE FROM public.user_profiles WHERE user_id = user_id;
            RAISE NOTICE '   ✅ Perfil do usuário % removido', user_email;
            
            -- 3. Deletar usuário do Supabase Auth
            DELETE FROM auth.users WHERE id = user_id;
            RAISE NOTICE '   ✅ Usuário % removido do Supabase Auth', user_email;
            
            deleted_count := deleted_count + 1;
        ELSE
            RAISE NOTICE '   ⚠️ Usuário % não encontrado - pulando', user_email;
        END IF;
    END LOOP;

    RAISE NOTICE '📊 Resumo da limpeza:';
    RAISE NOTICE '   Total de usuários processados: %', array_length(emails_to_delete, 1);
    RAISE NOTICE '   Total de usuários removidos: %', deleted_count;
END $$;

-- Verificar resultado da limpeza
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

-- Notificar PostgREST para recarregar o schema
NOTIFY pgrst, 'reload schema';

RAISE NOTICE '✅ Limpeza de usuários específicos concluída!';
RAISE NOTICE '📋 Próximos passos:';
RAISE NOTICE '   1. Execute os testes novamente';
RAISE NOTICE '   2. Registre novos usuários para teste';
RAISE NOTICE '   3. Verifique se as funcionalidades estão funcionando corretamente'; 