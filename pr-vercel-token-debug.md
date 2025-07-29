## 🔍 Hotfix: Debug e Correção do Token Vercel

### 🐛 **Problema Atual**
O deploy do frontend no Vercel continua falhando com erro:
```
ArgError: option requires argument: --token
```

### 🔍 **Análise do Erro**
O erro indica que o `$VERCEL_TOKEN` está vazio ou não está sendo passado corretamente para o comando Vercel.

### 🛠️ **Solução Proposta**

#### **1. Debug do Token**
Adicionado comando para verificar se o token está sendo passado:
```bash
echo "Token length: ${#VERCEL_TOKEN}"
```

#### **2. Possíveis Causas**
- ❌ Token não configurado no GitHub Secrets
- ❌ Token vazio ou inválido
- ❌ Variável de ambiente não sendo passada corretamente
- ❌ Problema de sintaxe no workflow

#### **3. Alternativas de Correção**
Se o debug mostrar token vazio, implementaremos:

**Opção A: Usar sintaxe direta**
```yaml
run: |
  vercel --prod --token ${{ secrets.VERCEL_TOKEN }} --yes
```

**Opção B: Verificar token antes do deploy**
```yaml
run: |
  if [ -z "$VERCEL_TOKEN" ]; then
    echo "❌ VERCEL_TOKEN está vazio!"
    exit 1
  fi
  vercel --prod --token $VERCEL_TOKEN --yes
```

**Opção C: Usar arquivo de configuração**
```yaml
run: |
  echo "{\"token\": \"$VERCEL_TOKEN\"}" > .vercel/project.json
  vercel --prod --yes
```

### 🧪 **Teste**
Após o merge, vamos:
1. ✅ Verificar o log do debug (token length)
2. ✅ Identificar a causa raiz do problema
3. ✅ Aplicar a correção adequada
4. ✅ Confirmar deploy funcionando

### 🚀 **Impacto**
- **Crítico**: Corrige deploy automático do frontend
- **Urgente**: Deve ser mergeado na main imediatamente
- **Baixo risco**: Apenas adiciona debug e correções

### 📋 **Checklist**
- [ ] Verificar se `VERCEL_TOKEN` está configurado no GitHub Secrets
- [ ] Confirmar que o token é válido no Vercel
- [ ] Testar deploy após correção
- [ ] Remover logs de debug após confirmação

---

**⚠️ Hotfix para produção - merge direto na main** 