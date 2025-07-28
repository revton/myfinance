## 🔧 Fix: Corrige problema do pytest não encontrar módulos src

### 🚨 **Problema Identificado**

O workflow de testes estava falhando no [PR #15](https://github.com/revton/myfinance/actions/runs/16570879759/job/46862493266?pr=15) com erro no comando pytest:

```
Process completed with exit code 1
```

**Causa**: O pytest não conseguia encontrar os módulos do `src/` no ambiente do GitHub Actions.

### ✅ **Correções Aplicadas**

#### **1. Correção do comando pytest no workflow**
- **Antes**: `python -m pytest --cov=src --cov-report=xml`
- **Depois**: `PYTHONPATH=$PYTHONPATH:. python -m pytest tests/ --cov=src --cov-report=xml`

**Mudanças**:
- **Adicionado PYTHONPATH**: Inclui o diretório atual no path do Python
- **Especificado diretório**: `tests/` para executar apenas testes
- **Garante** que o módulo `src` seja encontrado

#### **2. Correção do import no arquivo de teste**
- **Adicionado** configuração de path no `tests/test_transactions.py`
- **Import robusto**: `sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))`
- **Compatibilidade**: Funciona em diferentes ambientes

### 📁 **Arquivos Modificados**

- `.github/workflows/deploy.yml` - Comando pytest corrigido
- `tests/test_transactions.py` - Import robusto adicionado

### 🎯 **Benefícios**

1. **✅ Testes funcionais** - pytest encontra módulos corretamente
2. **✅ Compatibilidade** - Funciona em diferentes ambientes
3. **✅ Cobertura correta** - Relatórios de cobertura gerados
4. **✅ Deploy estável** - Workflows não falham mais

### 🧪 **Teste**

Após o merge, o workflow deve:
1. ✅ Instalar dependências sem erros
2. ✅ Executar testes do backend com sucesso
3. ✅ Gerar relatório de cobertura XML
4. ✅ Continuar para deploy do frontend

### 🔄 **Próximos Passos**

1. **Merge este PR** na develop
2. **Verificar workflows** no PR #15
3. **Criar PR** develop → main
4. **Validar deploy** completo

---

**⚠️ Nota**: Esta correção resolve o problema fundamental do pytest não encontrar os módulos do projeto no ambiente do GitHub Actions. 