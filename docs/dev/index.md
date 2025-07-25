# Documentação de Desenvolvimento

## Qualidade e Cobertura

- **Cobertura de testes automatizada** para backend (Python) e frontend (React/TypeScript)
- **Integração com SonarQube** para análise de qualidade, duplicidade, code smells e cobertura
- **Task coverage_all_reports**: gera todos os relatórios necessários para o SonarQube
- **Lockfile uv.lock**: garante reprodutibilidade do ambiente Python
- **Testes de entrypoint**: `frontend/src/main.test.tsx` garante cobertura total do React

### Como rodar a análise de qualidade

1. Gere os relatórios:
   ```bash
   uv run invoke coverage-all-reports
   ```
2. Rode o SonarScanner (com o token gerado no SonarQube):
   ```bash
   sonar-scanner -Dsonar.login=SEU_TOKEN_AQUI
   ```
3. Veja o resultado em [http://localhost:9000](http://localhost:9000)

> **Atenção:** Nunca versionar o token do SonarQube no repositório. Use a opção `-Dsonar.login=SEU_TOKEN_AQUI` na linha de comando ou defina a variável de ambiente `SONAR_TOKEN`.

### Fluxo de commits recomendados

- Commit dos testes de entrypoint do frontend:
  ```bash
  git commit -m "test(frontend): adiciona main.test.tsx para cobertura total do entrypoint React" frontend/src/main.test.tsx
  ```
- Commit do lockfile Python:
  ```bash
  git commit -m "chore(python): adiciona uv.lock para reprodutibilidade de ambiente" uv.lock
  ```
- Commit dos ajustes de dependências e testes:
  ```bash
  git commit -m "chore: atualiza dependências e testes do frontend e backend\n\n- Atualiza package.json e package-lock.json\n- Ajusta App.test.tsx para cobertura total\n- Atualiza testes do backend em tests/test_transactions.py\n- Ajusta .gitignore para ignorar arquivos temporários do SonarQube" .gitignore frontend/package-lock.json frontend/package.json frontend/src/App.test.tsx tests/test_transactions.py
  ```

### Troubleshooting de cobertura no SonarQube

- **Backend Python:**
  - Garanta que o coverage é gerado com caminhos relativos (`src/main.py`)
  - Rode sempre do root do projeto
  - Verifique se o coverage.xml tem `<class filename="src/main.py" ...>`
- **Frontend React/TypeScript:**
  - O arquivo lcov.info deve estar em `reports/coverage-frontend/lcov.info`
  - Os caminhos devem ser relativos ao root (ex: `SF:frontend/src/App.tsx`)
  - Rode o SonarScanner sempre do root do projeto

### SonarQube via Docker

Para rodar o SonarQube localmente:
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts
```
Acesse em [http://localhost:9000](http://localhost:9000) (usuário/senha padrão: admin/admin)

---

Se precisar de mais detalhes ou exemplos, consulte o README.md do projeto ou peça por mais exemplos de integração! 