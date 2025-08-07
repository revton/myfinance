-- Script para resolver o problema da tabela user_profiles no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard
-- https://supabase.com/dashboard/project/[SEU_PROJETO]/sql/new

-- 1. Verificar se a tabela já existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'user_profiles'
    ) THEN
        -- Criar a tabela se não existir
        CREATE TABLE public.user_profiles (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id UUID NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            avatar_url TEXT,
            timezone VARCHAR(50) DEFAULT 'America/Sao_Paulo' NOT NULL,
            currency VARCHAR(3) DEFAULT 'BRL' NOT NULL,
            language VARCHAR(5) DEFAULT 'pt-BR' NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        
        -- Criar índices
        CREATE INDEX idx_user_profiles_user_id ON public.user_profiles(user_id);
        CREATE INDEX idx_user_profiles_email ON public.user_profiles(email);
        CREATE INDEX idx_user_profiles_created_at ON public.user_profiles(created_at);
        
        -- Adicionar constraints
        ALTER TABLE public.user_profiles 
        ADD CONSTRAINT check_valid_timezone 
        CHECK (timezone IN ('America/Sao_Paulo', 'UTC', 'America/New_York', 'Europe/London'));
        
        ALTER TABLE public.user_profiles 
        ADD CONSTRAINT check_valid_currency 
        CHECK (currency IN ('BRL', 'USD', 'EUR', 'GBP'));
        
        ALTER TABLE public.user_profiles 
        ADD CONSTRAINT check_valid_language 
        CHECK (language IN ('pt-BR', 'en-US', 'es-ES'));
        
        ALTER TABLE public.user_profiles 
        ADD CONSTRAINT check_email_length 
        CHECK (length(email) >= 3);
        
        ALTER TABLE public.user_profiles 
        ADD CONSTRAINT check_full_name_length 
        CHECK (length(full_name) <= 255);
        
        RAISE NOTICE 'Tabela user_profiles criada com sucesso';
    ELSE
        RAISE NOTICE 'Tabela user_profiles já existe';
    END IF;
END $$;

-- 2. Habilitar RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- 3. Remover políticas existentes (se houver)
DROP POLICY IF EXISTS "Users can view own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can delete own profile" ON public.user_profiles;

-- 4. Criar políticas RLS
CREATE POLICY "Users can view own profile" ON public.user_profiles
FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own profile" ON public.user_profiles
FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own profile" ON public.user_profiles
FOR DELETE USING (auth.uid()::text = user_id::text);

-- 5. Configurar permissões
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- 6. Forçar sincronização do PostgREST
NOTIFY pgrst, 'reload schema';

-- 7. Verificar se tudo foi criado corretamente
SELECT 
    'Tabela criada' as status,
    table_name,
    table_schema
FROM information_schema.tables 
WHERE table_name = 'user_profiles' 
AND table_schema = 'public';

-- 8. Verificar políticas RLS
SELECT 
    'Políticas RLS' as status,
    policyname,
    cmd
FROM pg_policies 
WHERE tablename = 'user_profiles';

-- 9. Verificar permissões
SELECT 
    'Permissões' as status,
    grantee,
    privilege_type
FROM information_schema.role_table_grants 
WHERE table_name = 'user_profiles'
AND grantee IN ('anon', 'authenticated')
ORDER BY grantee, privilege_type;

-- 10. Teste de inserção (opcional - remova se não quiser dados de teste)
-- INSERT INTO public.user_profiles (user_id, email, full_name) 
-- VALUES (
--     gen_random_uuid(),
--     'teste@example.com',
--     'Usuário Teste'
-- ) ON CONFLICT (user_id) DO NOTHING;

-- 11. Verificar dados (se o teste foi executado)
-- SELECT COUNT(*) as total_profiles FROM public.user_profiles; 