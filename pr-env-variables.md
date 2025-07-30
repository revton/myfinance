# Implementação de Variáveis de Ambiente Locais

## 📋 Resumo

Este PR implementa um sistema de variáveis de ambiente local para o projeto MyFinance, permitindo configuração flexível e segura para diferentes ambientes (desenvolvimento, testes, produção).

## 🎯 Objetivos

- ✅ Centralizar configurações em arquivo `.env`
- ✅ Permitir configuração flexível de portas e hosts
- ✅ Melhorar segurança (não commitar credenciais)
- ✅ Facilitar setup para novos desenvolvedores
- ✅ Manter compatibilidade com código existente

## 🔧 Mudanças Implementadas

### 1. Arquivos de Configuração
- **`env.example`**: Template com todas as variáveis disponíveis
- **`.gitignore`**: Adicionado `.env` para evitar commits acidentais
- **`pyproject.toml`**: Adicionado `python-dotenv` como dependência

### 2. Backend (FastAPI)
- **`src/config.py`**: 
  - Carregamento automático de `.env`
  - Novas configurações: `API_PORT`, `API_HOST`, `DEBUG`, `LOG_LEVEL`
  - Melhor tratamento de variáveis de ambiente
- **`src/main.py`**:
  - Configuração de logging baseada em `LOG_LEVEL`
  - Endpoint `/health` melhorado com informações de ambiente
  - Execução direta com configurações do `.env`

### 3. Tasks (Invoke)
- **`tasks.py`**:
  - Novos comandos: `setup-env`, `check-env`
  - Tasks existentes agora usam variáveis de ambiente
  - Configuração automática de portas e hosts

### 4. Testes
- **`tests/test_transactions.py`**:
  - Refatorado para usar variáveis de teste
  - Melhor estrutura com fixtures pytest
  - Testes mais robustos e organizados

### 5. Documentação
- **`docs/dev/env-setup.md`**: Guia completo de configuração
- **`mkdocs.yml`**: Adicionado link para nova documentação
- **`README.md`**: Atualizado com instruções rápidas

## 🚀 Como Usar

### Configuração Inicial
```bash
# 1. Copiar arquivo de exemplo
cp env.example .env

# 2. Configurar credenciais do Supabase
# Editar .env e adicionar:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your-supabase-anon-key

# 3. Verificar configuração
uv run invoke check-env
```

### Execução
```bash
# Todos os serviços (usa configurações do .env)
uv run invoke run-all

# Individualmente
uv run invoke backend    # Porta configurada em API_PORT
uv run invoke frontend   # URL da API em VITE_API_URL
uv run invoke docs       # Porta configurada em DOCS_PORT
```

## 📊 Variáveis de Ambiente

### Obrigatórias
- `SUPABASE_URL`: URL do projeto Supabase
- `SUPABASE_ANON_KEY`: Chave anônima do Supabase

### Opcionais (com valores padrão)
- `API_PORT`: Porta do backend (8002)
- `API_HOST`: Host do backend (0.0.0.0)
- `DEBUG`: Modo debug (True)
- `VITE_API_URL`: URL da API para frontend
- `DOCS_PORT`: Porta da documentação (8001)
- `LOG_LEVEL`: Nível de logs (INFO)
- `ENVIRONMENT`: Ambiente atual (development)

## 🔒 Segurança

- ✅ Arquivo `.env` adicionado ao `.gitignore`
- ✅ Template `env.example` sem credenciais reais
- ✅ Validação de variáveis obrigatórias
- ✅ Configurações separadas para testes

## 🧪 Testes

- ✅ Testes atualizados para usar variáveis de teste
- ✅ Mock do Supabase melhorado
- ✅ Fixtures pytest organizadas
- ✅ Cobertura mantida

## 📈 Benefícios

1. **Flexibilidade**: Configuração fácil para diferentes ambientes
2. **Segurança**: Credenciais não são commitadas
3. **Manutenibilidade**: Configurações centralizadas
4. **Onboarding**: Setup simplificado para novos devs
5. **Compatibilidade**: Não quebra código existente

## 🔄 Compatibilidade

- ✅ Mantém todas as funcionalidades existentes
- ✅ Valores padrão garantem funcionamento sem `.env`
- ✅ Comandos existentes continuam funcionando
- ✅ Não requer mudanças em CI/CD existente

## 📝 Próximos Passos

- [ ] Configurar variáveis de ambiente no CI/CD
- [ ] Adicionar validação de schema para `.env`
- [ ] Implementar configuração para produção
- [ ] Adicionar mais variáveis conforme necessário

## 🐛 Troubleshooting

Se encontrar problemas:
1. Execute `uv run invoke check-env` para verificar configuração
2. Verifique se o arquivo `.env` existe e está configurado
3. Confirme se as credenciais do Supabase estão corretas
4. Consulte a documentação em `docs/dev/env-setup.md` 