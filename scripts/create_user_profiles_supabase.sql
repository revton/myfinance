-- Script para criar a tabela user_profiles no Supabase
-- Execute este script no SQL Editor do Supabase Dashboard

-- Criar a tabela user_profiles
CREATE TABLE IF NOT EXISTS public.user_profiles (
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

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON public.user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON public.user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_created_at ON public.user_profiles(created_at);

-- Adicionar constraints de validação
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

-- Habilitar Row Level Security (RLS)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

-- Criar políticas RLS
CREATE POLICY "Users can view own profile" ON public.user_profiles
FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update own profile" ON public.user_profiles
FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete own profile" ON public.user_profiles
FOR DELETE USING (auth.uid()::text = user_id::text);

-- Configurar permissões
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Notificar PostgREST para recarregar o schema
NOTIFY pgrst, 'reload schema';

-- Verificar se a tabela foi criada
SELECT 
    table_name,
    table_schema
FROM information_schema.tables 
WHERE table_name = 'user_profiles' 
AND table_schema = 'public'; 