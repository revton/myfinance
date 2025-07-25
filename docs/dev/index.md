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
2. Instale as dependências necessárias:
   - Backend:
     ```sh
     uv pip install -r pyproject.toml --extra backend
     ```
   - Desenvolvimento:
     ```sh
     uv pip install -r pyproject.toml --extra dev
     ```
   - Testes:
     ```sh
     uv pip install -r pyproject.toml --extra test
     ```
   - Documentação:
     ```sh
     uv pip install -r pyproject.toml --extra docs
     ```
   - Segurança:
     ```sh
     uv pip install -r pyproject.toml --extra security
     ```
   - Para instalar tudo:
     ```sh
     uv pip install -r pyproject.toml --extra backend --extra dev --extra test --extra docs --extra security
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
   uv run invoke test-coverage
   uv run invoke security-backend
   uv run invoke security-frontend
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
O Vite está configurado para redirecionar `/transactions` para o backend FastAPI em `http://localhost:8002`.

## Documentação (MkDocs)

Para visualizar a documentação localmente:

1. Instale as dependências de docs (veja acima).
2. Execute:
   ```sh
   uv run invoke docs
   ```
   Acesse a documentação em http://localhost:8001

## Testes Automatizados

- **Backend:**
  ```sh
  uv run invoke test-backend
  uv run invoke test-coverage  # Com relatório de cobertura
  ```
- **Frontend:**
  ```sh
  uv run invoke test-frontend
  ```
- **Todos:**
  ```sh
  uv run invoke test-all
  ```

## Validação de Segurança das Dependências

- **Backend/Docs (Python):**
  ```sh
  uv run invoke security-backend
  ```
- **Frontend (Node.js):**
  ```sh
  uv run invoke security-frontend
  ```

## Métricas e Qualidade de Código

- **Ruff (Python):**
  ```sh
  uv pip install -r pyproject.toml --extra quality
  uv run invoke quality-ruff
  ```
- **Radon (Python):**
  ```sh
  uv pip install -r pyproject.toml --extra quality
  uv run invoke quality-radon-cc   # Complexidade ciclomática
  uv run invoke quality-radon-mi   # Índice de manutenibilidade
  uv run invoke quality-radon-raw  # Métricas brutas
  uv run invoke quality-radon-all  # Todas as métricas
  ```

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