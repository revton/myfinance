## 🔧 Fix: Usa pip diretamente nos workflows GitHub Actions

### 🚨 **Problema Identificado**

O comando `uv pip install -e . --extra docs` ainda estava falhando no workflow de documentação com erro:
```
error: Requesting extras requires a `pylock.toml`, `pyproject.toml`, `setup.cfg`, or `setup.py` file
```

### ✅ **Solução Aplicada**

**Substituição do uv por pip direto** para evitar problemas de compatibilidade:

#### **Workflow de Documentação (.github/workflows/deploy-docs.yml)**
- **Antes**: `uv pip install -e . --extra docs`
- **Depois**: `pip install mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin`

- **Antes**: `uv run mkdocs build`
- **Depois**: `mkdocs build`

#### **Workflow Principal (.github/workflows/deploy.yml)**
- **Antes**: `uv pip install -e . --extra backend --extra test`
- **Depois**: `pip install fastapi uvicorn supabase psycopg2-binary sqlalchemy alembic pydantic pytest httpx pytest-cov`

- **Antes**: `uv run pytest --cov=src --cov-report=xml`
- **Depois**: `pytest --cov=src --cov-report=xml`

### 🎯 **Vantagens da Mudança**

1. **✅ Simplicidade**: Usa pip padrão do Python
2. **✅ Confiabilidade**: Não depende de configurações complexas do uv
3. **✅ Compatibilidade**: Funciona em qualquer ambiente Python
4. **✅ Velocidade**: Instalação direta sem overhead do uv

### 📁 **Arquivos Modificados**

- `.github/workflows/deploy.yml` - Comandos backend corrigidos
- `.github/workflows/deploy-docs.yml` - Comandos docs corrigidos

### 🧪 **Teste**

Após o merge, os workflows devem:
1. ✅ Instalar dependências com pip sem erros
2. ✅ Executar testes do backend
3. ✅ Fazer build da documentação
4. ✅ Deploy automático funcionando

### 🔄 **Próximos Passos**

1. **Merge este PR** na develop
2. **Testar workflows** na develop
3. **Criar PR** develop → main
4. **Validar deploy** completo

---

**⚠️ Nota**: Esta abordagem usa pip diretamente para garantir máxima compatibilidade e evitar problemas com configurações do uv nos workflows. 