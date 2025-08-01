# 🗄️ Configuração do Banco de Dados - MyFinance

## 📋 **Configuração do Supabase**

### 🚀 **Passo a Passo**

#### **1. Acesse o SQL Editor no Supabase**
1. Vá para [supabase.com](https://supabase.com)
2. Faça login na sua conta
3. Selecione seu projeto MyFinance
4. No menu lateral, clique em **"SQL Editor"**

#### **2. Execute o Script de Criação**
1. Clique em **"New Query"**
2. Copie todo o conteúdo do arquivo `create_tables.sql`
3. Cole no editor SQL
4. Clique em **"Run"** ou pressione `Ctrl+Enter`

#### **3. Verificar se a Tabela foi Criada**
Execute no SQL Editor:
```sql
SELECT * FROM public.transactions;
```

### 📊 **Estrutura da Tabela `transactions`**

| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| `id` | UUID | Identificador único | PRIMARY KEY, auto-gerado |
| `type` | VARCHAR(10) | Tipo da transação | 'income' ou 'expense' |
| `amount` | DECIMAL(12,2) | Valor em reais | > 0 |
| `description` | TEXT | Descrição da transação | NOT NULL |
| `created_at` | TIMESTAMP | Data de criação | Auto-gerado |
| `updated_at` | TIMESTAMP | Data de atualização | Auto-atualizado |

### 🔧 **Funcionalidades Automáticas**

#### **Triggers**
- **Auto Update**: `updated_at` é atualizado automaticamente em toda modificação

#### **Índices**
- **Performance**: Índices em `type`, `created_at` e `amount` para consultas rápidas

#### **Validações**
- **Tipo**: Apenas 'income' ou 'expense'
- **Valor**: Sempre maior que zero
- **UUID**: Geração automática de IDs únicos

### 🧪 **Dados de Exemplo**

O script inclui dados de exemplo:
- ✅ 1 salário (income): R$ 2.500,00
- ✅ 3 despesas: Supermercado, Combustível, Aluguel
- ✅ 1 freelance (income): R$ 200,00

**⚠️ Em produção, remova a seção de dados de exemplo do script.**

---

## 🔗 **Configuração da API**

### **Variáveis de Ambiente no Render**

Certifique-se de que as seguintes variáveis estão configuradas no Render:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anonima
```

### **Como Encontrar as Credenciais**

1. **Supabase Dashboard** → Seu Projeto
2. **Settings** → **API**
3. Copie:
   - **Project URL** → `SUPABASE_URL`
   - **anon public key** → `SUPABASE_ANON_KEY`

---

## 🧪 **Testando a API**

### **1. Health Check**
```bash
curl https://myfinance-backend-xcct.onrender.com/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "message": "MyFinance API is running"
}
```

### **2. Listar Transações**
```bash
curl -X 'GET' \
  'https://myfinance-backend-xcct.onrender.com/transactions/' \
  -H 'accept: application/json'
```

**Resposta esperada:**
```json
[
  {
    "id": "uuid-aqui",
    "type": "income",
    "amount": 2500.00,
    "description": "Salário Janeiro",
    "created_at": "2025-01-27T...",
    "updated_at": "2025-01-27T..."
  }
]
```

### **3. Criar Nova Transação**
```bash
curl -X 'POST' \
  'https://myfinance-backend-xcct.onrender.com/transactions/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "expense",
    "amount": 50.00,
    "description": "Café da manhã"
  }'
```

---

## 🚨 **Troubleshooting**

### **Erro: "Could not find the table 'public.transactions'"**

**Causa**: Tabela não existe no banco
**Solução**: Execute o script `create_tables.sql` no SQL Editor

### **Erro: "Invalid API key"**

**Causa**: Credenciais incorretas no Render
**Solução**: 
1. Verifique `SUPABASE_URL` e `SUPABASE_ANON_KEY`
2. Re-deploy no Render após corrigir

### **Erro: "Connection failed"**

**Causa**: Rede ou configuração do Supabase
**Solução**:
1. Verifique se o projeto Supabase está ativo
2. Confirme se as variáveis estão corretas
3. Teste a conexão localmente primeiro

---

## 📊 **Monitoramento**

### **Supabase Dashboard**
- **Database** → **Tables** → `transactions`
- **API** → **Logs** para debug
- **Authentication** (para futuras features)

### **Render Logs**
```bash
render logs myfinance-backend-xcct
```

---

**📅 Última Atualização**: Janeiro 2025  
**🔄 Versão**: 1.0  
**📋 Status**: Produção Ready