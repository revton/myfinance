# Scripts de Limpeza de Usuários - Supabase

Este diretório contém scripts SQL para limpar dados de usuários no Supabase durante o desenvolvimento e testes.

## ⚠️ ATENÇÃO

**Estes scripts são destrutivos e irão DELETAR dados permanentemente!**
- Use apenas em ambientes de desenvolvimento, teste ou staging
- Nunca execute em produção
- Sempre faça backup antes de executar

## Scripts Disponíveis

### 1. `list_users_supabase.sql`
**Propósito:** Listar todos os usuários existentes antes da limpeza
**Uso:** Execute primeiro para verificar quais usuários existem
**Segurança:** ✅ Apenas leitura, não modifica dados

### 2. `clean_specific_users_supabase.sql`
**Propósito:** Limpar usuários específicos por email
**Uso:** Ideal para limpeza seletiva durante testes
**Segurança:** ⚠️ Modifica dados - configure os emails antes de executar

### 3. `clean_users_supabase.sql`
**Propósito:** Limpar TODOS os usuários do sistema
**Uso:** Para reset completo do banco de dados
**Segurança:** ⚠️ Muito destrutivo - use com cuidado

## Como Usar

### Passo 1: Verificar Usuários Existentes
1. Acesse o Supabase Dashboard
2. Vá para SQL Editor
3. Execute o script `list_users_supabase.sql`
4. Anote os emails dos usuários que deseja remover

### Passo 2: Configurar Limpeza Específica (Recomendado)
1. Abra o arquivo `clean_specific_users_supabase.sql`
2. Modifique o array `emails_to_delete` com os emails desejados:
```sql
emails_to_delete TEXT[] := ARRAY[
    'teste@example.com',
    'usuario.teste@email.com'
    -- Adicione mais emails conforme necessário
];
```
3. Execute o script no SQL Editor

### Passo 3: Limpeza Completa (Se Necessário)
1. Execute o script `clean_users_supabase.sql`
2. ⚠️ **CUIDADO:** Isso remove TODOS os usuários!

## O que os Scripts Fazem

### Limpeza de Dados
1. **Transações:** Remove transações associadas aos usuários (se houver `user_id`)
2. **Perfis:** Remove registros da tabela `public.user_profiles`
3. **Usuários:** Remove registros da tabela `auth.users` (Supabase Auth)

### Verificações de Segurança
- ✅ Verifica se está em ambiente de desenvolvimento/teste
- ✅ Notifica PostgREST para recarregar o schema
- ✅ Exibe relatório de limpeza
- ✅ Reseta sequências automaticamente

### Relatórios
Após a execução, os scripts exibem:
- Total de registros em cada tabela
- Confirmação de cada operação
- Próximos passos recomendados

## Fluxo Recomendado para Testes

1. **Antes dos testes:**
   ```sql
   -- Execute para verificar estado atual
   -- scripts/list_users_supabase.sql
   ```

2. **Limpeza seletiva:**
   ```sql
   -- Configure emails e execute
   -- scripts/clean_specific_users_supabase.sql
   ```

3. **Após os testes:**
   ```sql
   -- Execute novamente para verificar limpeza
   -- scripts/list_users_supabase.sql
   ```

## Troubleshooting

### Erro: "Este script só pode ser executado em ambientes de desenvolvimento"
- Verifique se a variável `app.environment` está configurada
- Ou remova a verificação de ambiente (não recomendado)

### Erro: "Could not find the table"
- Execute primeiro o script `create_user_profiles_supabase.sql`
- Verifique se as tabelas existem

### Dados não foram removidos
- Verifique se há constraints de foreign key
- Execute `NOTIFY pgrst, 'reload schema';` manualmente
- Verifique logs do Supabase

## Próximos Passos Após Limpeza

1. Execute os testes novamente
2. Registre novos usuários para teste
3. Verifique se as funcionalidades estão funcionando
4. Se necessário, execute migrações do Alembic

## 🔧 Resolução de Problemas com Email de Confirmação

### Problema: Email de confirmação não chega após registro

#### Diagnóstico
1. **Execute o script de diagnóstico:**
   ```sql
   -- scripts/diagnose_email_confirmation.sql
   ```

2. **Verifique no Supabase Dashboard:**
   - Settings > Auth > Email Templates
   - Settings > Auth > SMTP Settings
   - Logs > Auth (para ver erros de email)

#### Soluções

##### 1. Reenviar Email de Confirmação
```bash
# Via script Python
python scripts/test_resend_confirmation.py

# Ou via API local (se o backend estiver rodando)
curl -X POST http://localhost:8002/auth/resend-confirmation \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com"}'
```

##### 2. Forçar Confirmação Manual (Desenvolvimento)
```sql
-- scripts/force_confirm_email.sql
-- ⚠️ Use apenas em desenvolvimento/teste!
```

##### 3. Verificar Configurações do Supabase
- **Email Provider:** Configure SMTP ou use Resend/SendGrid
- **Email Templates:** Personalize os templates de confirmação
- **Site URL:** Configure a URL de redirecionamento após confirmação

##### 4. Configurações Recomendadas
```sql
-- No Supabase Dashboard > Settings > Auth:
-- Site URL: http://localhost:3000 (ou sua URL de frontend)
-- Redirect URLs: http://localhost:3000/auth/confirm
-- Enable email confirmations: ✅ Ativado
```

## Backup e Restauração

### Antes da Limpeza
```sql
-- Backup dos usuários (opcional)
CREATE TABLE backup_users AS SELECT * FROM auth.users;
CREATE TABLE backup_user_profiles AS SELECT * FROM public.user_profiles;
```

### Restauração (se necessário)
```sql
-- Restaurar dados (use com cuidado)
INSERT INTO auth.users SELECT * FROM backup_users;
INSERT INTO public.user_profiles SELECT * FROM backup_user_profiles;
```

---

**Lembre-se:** Estes scripts são para desenvolvimento e testes. Nunca use em produção! 