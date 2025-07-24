# Manual do Usuário

Bem-vindo ao MyFinance!

Este sistema permite o cadastro e visualização de receitas e despesas de forma simples e eficiente.

## Funcionalidades Iniciais

- Cadastro de receitas
- Cadastro de despesas
- Visualização de receitas e despesas

## Como Usar

### Cadastrar Receita ou Despesa

1. Acesse o endpoint `/transactions/` usando um cliente HTTP (ex: Postman, Insomnia) ou a interface interativa do FastAPI (`/docs`).
2. Envie uma requisição POST com os dados:
   - `type`: "income" para receita ou "expense" para despesa
   - `amount`: valor numérico
   - `description`: descrição da transação

Exemplo:
```json
{
  "type": "income",
  "amount": 100.0,
  "description": "Salário"
}
```

### Visualizar Receitas e Despesas

1. Acesse o endpoint `/transactions/` com uma requisição GET.
2. Você verá a lista de todas as receitas e despesas cadastradas.

A documentação será atualizada conforme novas funcionalidades forem implementadas. 