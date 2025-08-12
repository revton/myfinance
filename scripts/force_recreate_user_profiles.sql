-- Script AGESSIVO para forçar a recriação da tabela user_profiles
-- Execute este script no SQL Editor do Supabase Dashboard
-- https://supabase.com/dashboard/project/[SEU_PROJETO]/sql/new

-- 1. REMOVER TUDO EXISTENTE
DROP POLICY IF EXISTS "Users can view own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can delete own profile" ON public.user_profiles;

-- 2. REMOVER A TABELA COMPLETAMENTE
DROP TABLE IF EXISTS public.user_profiles CASCADE;

-- 3. CRIAR A TABELA NOVA
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

-- 4. CRIAR ÍNDICES
CREATE INDEX idx_user_profiles_user_id ON public.user_profiles(user_id);
CREATE INDEX idx_user_profiles_email ON public.user_profiles(email);
CREATE INDEX idx_user_profiles_created_at ON public.user_profiles(created_at);

-- 5. ADICIONAR CONSTRAINTS
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

-- 6. HABILITAR RLS
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- 7. CRIAR POLÍTICAS RLS
CREATE POLICY "Users can view own profile" ON public.user_profiles
FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own profile" ON public.user_profiles
FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own profile" ON public.user_profiles
FOR DELETE USING (auth.uid()::text = user_id::text);

-- 8. CONFIGURAR PERMISSÕES
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- 9. FORÇAR SINCRONIZAÇÃO MÚLTIPLA
NOTIFY pgrst, 'reload schema';
SELECT pg_sleep(2);
NOTIFY pgrst, 'reload schema';
SELECT pg_sleep(2);
NOTIFY pgrst, 'reload schema';

-- 10. VERIFICAR SE TUDO FOI CRIADO
SELECT 
    'Tabela recriada' as status,
    table_name,
    table_schema
FROM information_schema.tables 
WHERE table_name = 'user_profiles' 
AND table_schema = 'public';

-- 11. VERIFICAR POLÍTICAS
SELECT 
    'Políticas RLS' as status,
    policyname,
    cmd
FROM pg_policies 
WHERE tablename = 'user_profiles';

-- 12. VERIFICAR PERMISSÕES
SELECT 
    'Permissões' as status,
    grantee,
    privilege_type
FROM information_schema.role_table_grants 
WHERE table_name = 'user_profiles'
AND grantee IN ('anon', 'authenticated')
ORDER BY grantee, privilege_type;

-- 13. TESTE DE INSERÇÃO DIRETA
INSERT INTO public.user_profiles (user_id, email, full_name) 
VALUES (
    gen_random_uuid(),
    'teste.direto@example.com',
    'Usuário Teste Direto'
);

-- 14. VERIFICAR SE A INSERÇÃO FUNCIONOU
SELECT COUNT(*) as total_profiles FROM public.user_profiles;

-- 15. LIMPAR DADOS DE TESTE
DELETE FROM public.user_profiles WHERE email = 'teste.direto@example.com'; 