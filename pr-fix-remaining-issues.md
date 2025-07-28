## 🔧 Fix: Corrige problemas restantes nos workflows GitHub Actions

### 🚨 **Problemas Identificados**

Após a correção anterior, ainda havia 2 erros nos workflows do [PR #15](https://github.com/revton/myfinance/pull/15):

1. **Instalação desnecessária do uv** - Estava instalando mas não usando
2. **Comando pytest incorreto** - Pode não encontrar módulos
3. **Formato do comando Vercel** - Melhor formatação

### ✅ **Correções Aplicadas**

#### **1. Remoção da instalação desnecessária do uv**
- **Removido** do `.github/workflows/deploy.yml`
- **Removido** do `.github/workflows/deploy-docs.yml`
- **Economia de tempo** no build

#### **2. Correção do comando pytest**
- **Antes**: `pytest --cov=src --cov-report=xml`
- **Depois**: `python -m pytest --cov=src --cov-report=xml`
- **Garante** que o pytest encontre os módulos corretamente

#### **3. Melhoria no comando Vercel**
- **Formatação** melhorada para o deploy do frontend
- **Estrutura** mais clara do comando

### 📁 **Arquivos Modificados**

- `.github/workflows/deploy.yml` - Removido uv, corrigido pytest
- `.github/workflows/deploy-docs.yml` - Removido uv desnecessário

### 🎯 **Benefícios**

1. **✅ Build mais rápido** - Sem instalação desnecessária do uv
2. **✅ Testes mais confiáveis** - pytest com módulos encontrados
3. **✅ Código mais limpo** - Remove dependências não utilizadas
4. **✅ Deploy mais estável** - Comandos otimizados

### 🧪 **Teste**

Após o merge, os workflows devem:
1. ✅ Instalar apenas dependências necessárias
2. ✅ Executar testes do backend sem erros
3. ✅ Fazer build da documentação
4. ✅ Deploy do frontend no Vercel

### 🔄 **Próximos Passos**

1. **Merge este PR** na develop
2. **Verificar workflows** no PR #15
3. **Criar PR** develop → main
4. **Validar deploy** completo

---

**⚠️ Nota**: Estas correções otimizam os workflows removendo dependências desnecessárias e garantindo que os comandos funcionem corretamente. 