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