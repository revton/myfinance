# Manual do Usuário

Bem-vindo ao MyFinance!

Este sistema permite o cadastro e visualização de receitas e despesas de forma simples e eficiente.

## Como Usar

1. Acesse a interface web em http://localhost:5173
2. Preencha o formulário para cadastrar uma nova receita ou despesa:
   - Selecione o tipo (Receita ou Despesa)
   - Informe o valor
   - Descreva a transação
   - Clique em "Adicionar"
3. Veja a lista de receitas e despesas cadastradas logo abaixo do formulário.

> **Observação:** Os dados são armazenados temporariamente enquanto o sistema está em execução. Ao reiniciar o backend, os dados são perdidos.

### Screenshots da Aplicação

#### Página Inicial (Login)
![Página Inicial](../screenshot_01_initial_page.png)

#### Esqueci Minha Senha
![Esqueci Minha Senha](../screenshot_04_forgot_password.png)

#### Tela Principal da Aplicação
![Tela Principal](../screenshot_05_main_application_screen.png)

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