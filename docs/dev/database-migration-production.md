# 🔄 Migração de Banco de Dados em Produção

## 📋 **Visão Geral**

Este documento descreve como aplicar migrações de banco de dados no ambiente de produção do MyFinance.

## 🚀 **Como Aplicar Migrações em Produção**

### 1. **Verificar Status das Migrações**

```bash
# Verificar status atual
uv run invoke show-migration-status

# Ou usando o script diretamente
uv run python scripts/check_migration_status.py
```

### 2. **Aplicar Migrações Pendentes**

```bash
# Aplicar migrações em produção
uv run invoke migrate-production

# Ou usando o script diretamente
uv run python scripts/apply_production_migrations.py
```

### 3. **Verificação Manual**

```bash
# Verificar status atual
uv run alembic current

# Aplicar migrações
uv run alembic upgrade head

# Verificar histórico
uv run alembic history --verbose
```

## ⚠️ **Precauções Importantes**

### **Antes de Aplicar Migrações**

1. **Faça backup do banco de dados**
2. **Verifique o ambiente de execução**
3. **Confirme que está usando a DATABASE_URL correta**
4. **Teste em ambiente de staging primeiro**

### **Durante a Aplicação**

1. **Monitore os logs de saída**
2. **Verifique se não há erros**
3. **Confirme o sucesso da operação**

## 🛠️ **Solução de Problemas**

### **Erros Comuns**

#### **"DATABASE_URL não configurada"**
```bash
# Solução: Configure a variável de ambiente
export DATABASE_URL="postgresql://usuario:senha@host:porta/banco"
```

#### **"Conexão recusada"**
```bash
# Solução: Verifique as credenciais e conectividade
# 1. Teste a conexão manualmente
# 2. Verifique firewall e regras de rede
# 3. Confirme que o serviço está online
```

#### **"Migração já aplicada"**
```bash
# Solução: Verifique o status atual
uv run alembic current
# Se necessário, faça downgrade primeiro
uv run alembic downgrade -1
```

## 📊 **Monitoramento**

### **Verificar Status Após Migração**

```bash
# Verificar status atual
uv run alembic current

# Listar todas as migrações
uv run alembic history

# Verificar tabelas criadas
# (Use um cliente de banco de dados para verificar)
```

## 📝 **Checklist de Migração**

- [ ] Verificar ambiente (ENVIRONMENT=production)
- [ ] Confirmar DATABASE_URL configurada corretamente
- [ ] Fazer backup do banco de dados
- [ ] Verificar status atual das migrações
- [ ] Aplicar migrações pendentes
- [ ] Verificar sucesso da operação
- [ ] Monitorar logs de aplicação
- [ ] Testar funcionalidades afetadas

## 🆘 **Suporte**

Se encontrar problemas durante a migração:

1. **Verifique os logs completos**
2. **Confirme as credenciais do banco**
3. **Consulte o histórico de migrações**
4. **Entre em contato com a equipe de desenvolvimento**