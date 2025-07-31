# Sistema de Finanças Pessoais - MyFinance

Bem-vindo à documentação do MyFinance, um sistema completo para controle de finanças pessoais.

## 📋 Funcionalidades

- ✅ Controle de receitas e despesas
- ✅ Categorização de transações
- ✅ Relatórios financeiros detalhados
- ✅ Interface web moderna e responsiva
- ✅ Deploy automático no Vercel (Frontend)

## 📚 Navegação

- [🗺️ Roadmap](roadmap.md) - Planejamento e fases do projeto
- [Guia do Usuário](user/index.md) - Como usar o sistema
- [Guia do Desenvolvedor](dev/index.md) - Configuração e desenvolvimento
- [Deploy](deploy.md) - Instruções de implantação

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy + Supabase
- **Frontend**: React 18 + TypeScript + Material-UI
- **Documentação**: MkDocs + Material Theme
- **Deploy**: Vercel (Frontend) + Local (Backend)

## 🔧 Status das Correções

- ⚠️ **GitHub Actions**: Problemas conhecidos (ver seção abaixo)
- ✅ **Backend Tests**: Supabase mocking funcionando
- ✅ **Frontend Tests**: Vitest + React funcionando
- ✅ **GitHub Pages**: Deploy moderno configurado

## ⚠️ Problemas Conhecidos

### GitHub Actions
- **Status**: ⚠️ **Parcialmente Funcionando**
- **Problemas**: Alguns workflows com erros que foram ignorados para continuar o desenvolvimento
- **Impacto**: Deploy e testes automatizados podem falhar
- **Prioridade**: Baixa (funcionalidades core funcionando)
- **Plano**: Corrigir em iteração futura

### Deploy Automático
- **Status**: ⚠️ **Parcialmente Funcionando**
- **Frontend (Vercel)**: ✅ Funcionando - Deploy automático ativo
- **Backend (Render)**: ❌ Não funcionando - Deploy manual necessário
- **Impacto**: Backend precisa ser executado localmente para desenvolvimento
- **Prioridade**: Média (funcionalidades core funcionando localmente)
- **Plano**: Configurar deploy do backend em iteração futura

## 📊 Status do Projeto

| Métrica | Valor |
|---------|-------|
| **Fase Atual** | ✅ Fase 1 - MVP (Concluída) |
| **Próxima Fase** | 📋 Fase 2 - Categorias e Autenticação (Ago/25) |
| **Tecnologias** | FastAPI + React + Supabase |
| **Deploy** | Vercel (Frontend) + Local (Backend) |

---

*Documentação gerada automaticamente via GitHub Actions*

<!-- Trigger para roadmap update - 2025-01-27 22:00 UTC -->
