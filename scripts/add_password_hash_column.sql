-- Script para adicionar coluna password_hash à tabela user_profiles
-- Execute no SQL Editor do Supabase Dashboard

-- 1. Adicionar coluna password_hash
ALTER TABLE user_profiles 
ADD COLUMN password_hash VARCHAR(255);

-- 2. Verificar se a coluna foi adicionada
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
AND column_name = 'password_hash';

-- 3. Verificar estrutura atual da tabela
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
ORDER BY ordinal_position; 