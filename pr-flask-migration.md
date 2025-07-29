## 🚀 Sistema de Migração Flask com SQLAlchemy

### 📋 **Resumo das Mudanças**

Este PR implementa um sistema completo de migração usando Flask + SQLAlchemy + Alembic, incluindo:

- **Backend Flask**: Substituição do FastAPI por Flask
- **ORM SQLAlchemy**: Mapeamento objeto-relacional
- **Migrações Alembic**: Sistema de versionamento de banco
- **Documentação**: Guias completos de setup e uso

### 🏗️ **Arquitetura**

#### **Backend (Flask)**
- ✅ Flask com SQLAlchemy
- ✅ Sistema de migrações Alembic
- ✅ Endpoints REST para transações
- ✅ Configuração de banco PostgreSQL

#### **Database**
- ✅ Modelos SQLAlchemy
- ✅ Migrações automáticas
- ✅ Sistema de versionamento
- ✅ Rollback de mudanças

### 📁 **Arquivos Principais**

- `app.py` - Aplicação Flask principal
- `models.py` - Modelos SQLAlchemy
- `migrations/` - Sistema de migrações Alembic
- `requirements.txt` - Dependências Flask
- `docs/flask-migration.md` - Documentação completa

### 🔧 **Funcionalidades**

- ✅ CRUD completo de transações
- ✅ Sistema de migrações
- ✅ Configuração de ambiente
- ✅ Documentação detalhada

### 🧪 **Teste**

Após o merge, o sistema deve:
1. ✅ Executar migrações automaticamente
2. ✅ Funcionar com PostgreSQL
3. ✅ Manter compatibilidade com frontend
4. ✅ Documentação acessível

### 🔄 **Próximos Passos**

1. **Review e merge** na develop
2. **Testar migrações** em ambiente de desenvolvimento
3. **Validar integração** com frontend
4. **Deploy em produção**

---

**⚠️ Nota**: Esta é uma migração significativa do FastAPI para Flask. Recomenda-se testar cuidadosamente antes do merge. 