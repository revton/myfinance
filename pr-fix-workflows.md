## 🔧 Correções nos Workflows GitHub Actions

### 🚨 **Problema Identificado**

Os workflows estavam falhando com o erro:
```
Run uv pip install --extra docs -e .
error: Requesting extras requires a `pylock.toml`, `pyproject.toml`, `setup.cfg`, or `setup.py` file. Use `<dir>[extra]` syntax or `-r <file>` instead.
```

### ✅ **Correções Aplicadas**

#### **1. Comandos uv corrigidos**
- **Antes**: `uv pip install -r pyproject.toml --extra docs`
- **Depois**: `uv pip install -e . --extra docs`

- **Antes**: `uv pip install -r pyproject.toml --extra backend --extra test`
- **Depois**: `uv pip install -e . --extra backend --extra test`

#### **2. Build System adicionado**
Adicionado `[build-system]` no `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### 📁 **Arquivos Modificados**

- `.github/workflows/deploy.yml` - Comando de instalação backend corrigido
- `.github/workflows/deploy-docs.yml` - Comando de instalação docs corrigido
- `pyproject.toml` - Build system adicionado

### 🧪 **Teste**

Após o merge, os workflows devem:
1. ✅ Instalar dependências corretamente
2. ✅ Executar testes sem erros
3. ✅ Fazer deploy da documentação
4. ✅ Permitir merge da develop → main

### 🔄 **Próximos Passos**

1. **Merge este PR** na develop
2. **Testar workflows** na develop
3. **Criar novo PR** develop → main
4. **Validar deploy** completo

---

**⚠️ Nota**: Esta correção resolve o problema de instalação de dependências que estava impedindo o merge da develop na main. 