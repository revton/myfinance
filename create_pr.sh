#!/bin/bash

echo "🚀 Criando PR para corrigir erros das GitHub Actions..."
echo ""
echo "📋 Branch atual: $(git branch --show-current)"
echo "📋 Commits na branch:"
git log --oneline develop..HEAD
echo ""

# Comando para criar o PR
gh pr create \
  --title "fix: Corrige erros nos testes das GitHub Actions do PR #15" \
  --body "## 🔧 Correções para GitHub Actions

Este PR resolve os **2 erros nas actions** que estavam falhando na branch develop, conforme identificado no PR #15.

## 🚨 Problemas Resolvidos

1. **Testes Backend falhando** - Falta de variáveis de ambiente do Supabase
2. **Testes Frontend com problemas** - Configuração inadequada do Vitest
3. **Dependências mal configuradas** - Instalação não otimizada
4. **Permissões insuficientes** - Workflows sem permissões adequadas
5. **Configuração TypeScript** - Falta de setup específico para testes

## ✅ Correções Aplicadas

### Backend
- ✅ Adicionadas variáveis de ambiente de teste (SUPABASE_URL, SUPABASE_ANON_KEY)
- ✅ Melhorada instalação de dependências usando requirements.txt
- ✅ Corrigidos imports nos testes Python

### Frontend  
- ✅ Configuradas variáveis de ambiente (CI, VITE_API_URL)
- ✅ Atualizada configuração do Vitest com plugins e coverage
- ✅ Adicionado setup adequado (@testing-library/jest-dom)
- ✅ Criada configuração TypeScript específica para testes

### Workflows
- ✅ Adicionadas permissões adequadas (contents, checks, pull-requests, pages)
- ✅ Otimizada instalação de dependências
- ✅ Configuradas variáveis de ambiente necessárias

## 🎯 Resultado Esperado

Após estas correções:
- ✅ **Backend tests** executarão sem erros
- ✅ **Frontend tests** executarão com cobertura 
- ✅ **Workflows** terão todas as permissões necessárias
- ✅ **PR #15** poderá ser merged sem problemas

## 📋 Arquivos Modificados

- \`.github/workflows/deploy.yml\` - Principais correções nos testes
- \`.github/workflows/deploy-docs.yml\` - Permissões para GitHub Pages
- \`tests/test_transactions.py\` - Imports e env vars melhorados
- \`frontend/vitest.config.ts\` - Configuração completa de testes
- \`frontend/src/setupTests.ts\` - Setup para jest-dom
- \`frontend/tsconfig.test.json\` - Config TypeScript para testes
- \`frontend/tsconfig.json\` - Referência para config de testes

## 🚀 Como Testar

1. Merge este PR na develop
2. Verificar se o PR #15 passa nos checks
3. Proceder com merge develop → main

---

**Closes**: Falhas nos 2 actions da branch develop  
**Related**: PR #15" \
  --base develop \
  --head fix/github-actions-test-errors

echo ""
echo "✅ PR criado com sucesso!"
echo "🔗 Acesse o link do PR que apareceu acima para revisar e aprovar"