# Configuração de Múltiplos Ambientes no Supabase

Este documento explica como configurar e gerenciar múltiplos ambientes (desenvolvimento, teste, produção) no Supabase para o projeto MyFinance.

## 🎯 Visão Geral

O projeto MyFinance suporta três ambientes distintos:

- **Development**: Para desenvolvimento local
- **Testing**: Para testes automatizados e QA
- **Production**: Para ambiente de produção

Cada ambiente tem seu próprio projeto Supabase com dados isolados.

## 🏗️ Configuração no Supabase

### 1. Criar Projetos no Supabase

#### Projeto de Desenvolvimento
1. Acesse o [Supabase Dashboard](https://supabase.com/dashboard)
2. Clique em "New Project"
3. Configure:
   - **Name**: `myfinance-dev`
   - **Database Password**: Senha forte
   - **Region**: Escolha a região mais próxima
4. Clique em "Create new project"

#### Projeto de Teste
1. Repita o processo acima
2. Configure:
   - **Name**: `myfinance-test`
   - **Database Password**: Senha forte (pode ser a mesma)
   - **Region**: Mesma região do projeto de desenvolvimento

#### Projeto de Produção
1. Repita o processo acima
2. Configure:
   - **Name**: `myfinance-prod`
   - **Database Password**: Senha forte e única
   - **Region**: Escolha a região mais adequada para seus usuários

### 2. Configurar Tabelas em Cada Projeto

Para cada projeto, execute as migrações SQL:

#### Tabela de Transações
```sql
-- Execute no SQL Editor de cada projeto
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_created_at ON transactions(created_at DESC);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_transactions_updated_at 
    BEFORE UPDATE ON transactions 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### 3. Configurar Políticas de Segurança (RLS)

Para cada projeto, configure as políticas de segurança:

```sql
-- Habilitar RLS
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Política para permitir todas as operações (para desenvolvimento/teste)
-- Em produção, configure políticas mais restritivas
CREATE POLICY "Allow all operations" ON transactions
    FOR ALL USING (true);
```

## 🔧 Configuração Local

### 1. Obter Credenciais

Para cada projeto, obtenha as credenciais:

1. Vá para **Settings > API** no projeto
2. Copie:
   - **Project URL**
   - **anon public** key

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env`:

```bash
# Ambiente atual
ENVIRONMENT=development

# =============================================================================
# SUPABASE - DESENVOLVIMENTO
# =============================================================================
SUPABASE_URL=https://your-dev-project.supabase.co
SUPABASE_ANON_KEY=your-dev-supabase-anon-key

# =============================================================================
# SUPABASE - TESTE
# =============================================================================
SUPABASE_TEST_URL=https://your-test-project.supabase.co
SUPABASE_TEST_ANON_KEY=your-test-supabase-anon-key

# =============================================================================
# SUPABASE - PRODUÇÃO
# =============================================================================
SUPABASE_PROD_URL=https://your-prod-project.supabase.co
SUPABASE_PROD_ANON_KEY=your-prod-supabase-anon-key
```

## 🚀 Comandos para Gerenciar Ambientes

### Verificar Ambiente Atual
```bash
uv run invoke show-env
```

### Alterar Ambiente
```bash
# Para desenvolvimento
uv run invoke switch-env development

# Para teste
uv run invoke switch-env testing

# Para produção
uv run invoke switch-env production
```

### Verificar Configuração
```bash
uv run invoke check-env
```

### Executar em Ambiente Específico
```bash
# Backend em ambiente de teste
uv run invoke backend --env=testing

# Backend em ambiente de produção
uv run invoke backend --env=production
```

## 🧪 Testes com Ambientes

### Executar Testes
```bash
# Testes sempre usam ambiente de teste automaticamente
uv run invoke test-backend
uv run invoke test-all
```

### Configuração Automática
Os testes automaticamente:
- Definem `ENVIRONMENT=testing`
- Usam `SUPABASE_TEST_URL` e `SUPABASE_TEST_ANON_KEY`
- Não afetam dados de desenvolvimento ou produção

## 📊 Diferentes Configurações por Ambiente

### Development
- **Debug**: `True`
- **Log Level**: `DEBUG`
- **Dados**: Dados de desenvolvimento
- **Performance**: Não crítica

### Testing
- **Debug**: `False`
- **Log Level**: `INFO`
- **Dados**: Dados de teste (podem ser resetados)
- **Performance**: Moderada

### Production
- **Debug**: `False`
- **Log Level**: `WARNING`
- **Dados**: Dados reais dos usuários
- **Performance**: Crítica

## 🔒 Segurança por Ambiente

### Development
- Políticas RLS permissivas
- Dados de exemplo
- Acesso amplo para desenvolvimento

### Testing
- Políticas RLS permissivas
- Dados de teste
- Pode ser resetado frequentemente

### Production
- Políticas RLS restritivas
- Dados reais dos usuários
- Backup regular
- Monitoramento de segurança

## 📈 Migrações entre Ambientes

### Desenvolvimento → Teste
1. Execute migrações no projeto de teste
2. Copie estrutura de dados se necessário
3. Execute testes para validar

### Teste → Produção
1. Execute migrações no projeto de produção
2. Valide todas as funcionalidades
3. Configure políticas de segurança
4. Faça backup antes de deploy

## 🐛 Troubleshooting

### Erro: "Configuração do Supabase não encontrada"
- Verifique se as variáveis de ambiente estão configuradas
- Execute `uv run invoke show-env` para verificar
- Confirme se o ambiente está correto

### Erro: "Connection refused"
- Verifique se as URLs do Supabase estão corretas
- Confirme se as chaves anônimas estão válidas
- Teste a conexão no Supabase Dashboard

### Dados não aparecem
- Verifique se está no ambiente correto
- Confirme se as tabelas foram criadas
- Verifique as políticas RLS

## 📝 Próximos Passos

- [ ] Configurar backup automático para produção
- [ ] Implementar monitoramento de performance
- [ ] Configurar alertas de segurança
- [ ] Implementar migrações automatizadas
- [ ] Configurar CI/CD para diferentes ambientes 