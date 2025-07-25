# Documentação para Desenvolvedores

## Estrutura do Projeto

- `src/`: Código-fonte da aplicação (FastAPI)
- `tests/`: Testes automatizados (Pytest)
- `docs/`: Documentação (MkDocs)
- `frontend/`: Interface web (React)

## Ambiente de Desenvolvimento

### Backend (Python)
1. Crie o ambiente virtual:
   ```sh
   uv venv
   ```
2. Instale as dependências principais do projeto:
   ```sh
   uv pip install -r pyproject.toml
   ```
   Para dependências de desenvolvimento (ex: invoke):
   ```sh
   uv pip install -r pyproject.toml --extra dev
   ```
   Para dependências de documentação:
   ```sh
   uv pip install -r pyproject.toml --extra docs
   ```
3. Execute os comandos de automação (sem ativar o ambiente):
   ```sh
   uv run invoke backend
   uv run invoke frontend
   uv run invoke docs
   uv run invoke run-all
   uv run invoke test-backend
   uv run invoke test-frontend
   uv run invoke test-all
   ```
   > **Dica:** No VS Code, abra 3 abas do terminal integrado e execute backend, frontend e docs separadamente para usar o profile padrão da IDE.
   >
   > **Atenção:** Agora backend e docs estão acessíveis na rede local. Descubra o IP do seu computador (ex: 192.168.1.75) e acesse:
   > - Backend: `http://192.168.1.75:8002`
   > - Docs: `http://192.168.1.75:8001`
   > - Frontend: `http://192.168.1.75:5173`

### Frontend (Node.js + React)
1. Instale o Node.js (LTS):
   - Baixe do site oficial: https://nodejs.org/
   - Ou via winget (Windows):
     ```powershell
     winget install OpenJS.NodeJS.LTS -h --accept-package-agreements --accept-source-agreements
     ```
2. Adicione o Node.js ao PATH se necessário.
3. Instale as dependências do frontend:
   ```sh
   cd frontend
   npm install
   ```
4. Execute o frontend:
   ```sh
   npm run dev -- --host
   ```
   O frontend estará disponível em http://localhost:5173

#### Proxy de API
O Vite está configurado para redirecionar `/transactions` para o backend FastAPI em `http://localhost:8000`.

## Documentação (MkDocs)

Para visualizar a documentação localmente:

1. Ative o ambiente virtual Python:
   ```powershell
   .venv\Scripts\activate
   ```
2. Execute o servidor MkDocs em outra porta (ex: 8001) para evitar conflito com o backend:
   ```sh
   mkdocs serve -a 127.0.0.1:8001
   ```
   Acesse a documentação em http://localhost:8001

## Gitflow

- Use branches de feature para cada funcionalidade.
- Commits atômicos e descritivos.
- Pull Requests para validação.

## TDD

- Sempre escreva o teste antes da implementação.
- Use `pytest` para rodar os testes do backend.
- Use `npm test` para rodar os testes do frontend (Vitest).

## Docker

- O projeto será dockerizado para facilitar o deploy e o uso em diferentes ambientes.

## Validação de Segurança das Dependências

- **Backend/Docs (Python):**
  ```sh
  uv pip install -r pyproject.toml --extra security
  uv run invoke security_backend
  uv run invoke security_docs
  ```
- **Frontend (Node.js):**
  ```sh
  cd frontend
  npm audit
  ```
- **Tudo de uma vez:**
  ```sh
  uv run invoke security_all
  ```

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

Os testes estão em `tests/test_transactions.py` (backend) e `frontend/src/App.test.tsx` (frontend) e cobrem:

- Cadastro de receita
- Cadastro de despesa
- Listagem de transações 