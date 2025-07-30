# Configuração de Ambientes no Supabase

Este documento explica como configurar e gerenciar ambientes (desenvolvimento e produção) no Supabase para o projeto MyFinance.

## 🎯 Visão Geral

O projeto MyFinance suporta dois ambientes distintos:

- **Development**: Para desenvolvimento local
- **Production**: Para ambiente de produção

Cada ambiente tem seu próprio projeto Supabase com dados isolados. Os testes usam mocks completos e não requerem conexão real com o Supabase.

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

-- Política para permitir todas as operações (para desenvolvimento)
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

# Para produção
uv run invoke switch-env production
```

### Verificar Configuração
```bash
uv run invoke check-env
```

### Executar em Ambiente Específico
```bash
# Backend em ambiente de desenvolvimento
uv run invoke backend --env=development

# Backend em ambiente de produção
uv run invoke backend --env=production
```

## 🧪 Testes com Mocks

### Executar Testes
```bash
# Testes usam mocks completos (sem conexão real com Supabase)
uv run invoke test-backend
uv run invoke test-all
```

### Configuração de Testes
Os testes automaticamente:
- Usam mocks completos do Supabase
- Não requerem configuração de ambiente de teste
- Não afetam dados de desenvolvimento ou produção
- São rápidos e confiáveis

## 📊 Diferentes Configurações por Ambiente

### Development
- **Debug**: `True`
- **Log Level**: `DEBUG`
- **Dados**: Dados de desenvolvimento
- **Performance**: Não crítica
- **Políticas RLS**: Permissivas

### Production
- **Debug**: `False`
- **Log Level**: `WARNING`
- **Dados**: Dados reais dos usuários
- **Performance**: Crítica
- **Políticas RLS**: Restritivas

## 🔒 Segurança por Ambiente

### Development
- Políticas RLS permissivas
- Dados de exemplo
- Acesso amplo para desenvolvimento
- Debug habilitado

### Production
- Políticas RLS restritivas
- Dados reais dos usuários
- Backup regular
- Monitoramento de segurança
- Debug desabilitado

## 📈 Migrações entre Ambientes

### Desenvolvimento → Produção
1. Execute migrações no projeto de produção
2. Valide todas as funcionalidades
3. Configure políticas de segurança restritivas
4. Faça backup antes de deploy
5. Teste em produção com dados reais

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

### Testes falhando
- Os testes usam mocks, não precisam de conexão real
- Verifique se os mocks estão configurados corretamente
- Execute `uv run invoke test-backend` para ver detalhes

## 📝 Próximos Passos

- [ ] Configurar backup automático para produção
- [ ] Implementar monitoramento de performance
- [ ] Configurar alertas de segurança
- [ ] Implementar migrações automatizadas
- [ ] Configurar CI/CD para diferentes ambientes
- [ ] Implementar políticas RLS mais restritivas para produção 