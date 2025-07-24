# Documentação para Desenvolvedores

## Estrutura do Projeto

- `src/`: Código-fonte da aplicação
- `tests/`: Testes automatizados (Pytest)
- `docs/`: Documentação (MkDocs)

## Ambiente de Desenvolvimento

1. Crie o ambiente virtual:
   ```sh
   uv venv
   .venv\Scripts\activate  # Windows
   ```
2. Instale as dependências:
   ```sh
   uv pip install -r requirements.txt  # ou use os comandos individuais
   ```

## Gitflow

- Use branches de feature para cada funcionalidade.
- Commits atômicos e descritivos.
- Pull Requests para validação.

## TDD

- Sempre escreva o teste antes da implementação.
- Use `pytest` para rodar os testes.

## Docker

- O projeto será dockerizado para facilitar o deploy e o uso em diferentes ambientes.

## Endpoints de Receitas e Despesas

### Criar Receita ou Despesa

`POST /transactions/`

**Exemplo de payload:**
```json
{
  "type": "income", // ou "expense"
  "amount": 100.0,
  "description": "Salário"
}
```

**Resposta:**
- 201 Created
- JSON com os dados cadastrados

### Listar Receitas e Despesas

`GET /transactions/`

**Resposta:**
- 200 OK
- Lista de receitas e despesas cadastradas

## Testes Automatizados

Os testes estão em `tests/test_transactions.py` e cobrem:
- Cadastro de receita
- Cadastro de despesa
- Listagem de transações 