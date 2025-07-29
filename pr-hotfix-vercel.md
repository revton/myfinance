## 🚨 Hotfix: Correção do Deploy Vercel

### 🐛 **Problema**
O deploy do frontend no Vercel estava falhando com erro:
```
ArgError: option requires argument: --token
```

### 🔍 **Causa**
O workflow estava tentando usar variáveis de ambiente que não existem:
- `VERCEL_ORG_ID` ❌
- `VERCEL_PROJECT_ID` ❌

### ✅ **Solução**
- Removidas as variáveis desnecessárias
- Mantido apenas `VERCEL_TOKEN` que é o único necessário
- Corrigida a sintaxe do comando Vercel

### 📋 **Alterações**
```yaml
# ANTES:
vercel --prod --token ${{ secrets.VERCEL_TOKEN }} --yes
env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}      # ❌ Não existe
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }} # ❌ Não existe

# DEPOIS:
vercel --prod --token $VERCEL_TOKEN --yes
env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}        # ✅ Único necessário
```

### 🧪 **Teste**
Após o merge, o deploy do frontend deve:
1. ✅ Executar sem erros de token
2. ✅ Fazer deploy no Vercel automaticamente
3. ✅ Manter a integração CI/CD funcionando

### 🚀 **Impacto**
- **Crítico**: Corrige deploy automático do frontend
- **Urgente**: Deve ser mergeado na main imediatamente
- **Baixo risco**: Apenas remove variáveis desnecessárias

---

**⚠️ Hotfix para produção - merge direto na main** 