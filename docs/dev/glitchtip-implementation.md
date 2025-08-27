# 🐘 Implementação de Monitoramento de Erros com Sentry.io

## 📋 **Visão Geral**

Este documento descreve os passos para implementar o **Sentry.io**, uma solução líder de mercado para monitoramento de erros e performance. A captura de erros em tempo real é crucial para identificar e resolver problemas rapidamente, melhorando a estabilidade e a experiência do usuário no MyFinance.

Como os projetos de backend e frontend já foram criados na sua conta (`revton-solucoes-tecnologicas.sentry.io`), este guia focará na obtenção da chave DSN e na integração com o código-fonte.

### 🎯 **Objetivos Principais**
- **Centralização de Erros**: Capturar todos os erros do backend (FastAPI) e do frontend (React) no painel do Sentry.
- **Monitoramento Proativo**: Identificar e corrigir problemas antes que os usuários os reportem.
- **Facilidade de Manutenção**: Usar uma solução gerenciada (SaaS) para evitar a necessidade de manter uma infraestrutura própria de monitoramento.

---

## 🔧 **Passos para Implementação**

### **Parte 1: Obter a Chave DSN do Sentry**

A chave **DSN** (Data Source Name) é uma URL única que diz ao SDK do Sentry para onde enviar os eventos de erro. Cada projeto (frontend e backend) terá sua própria DSN.

1.  **Acesse sua conta Sentry**:
    Faça login em [sentry.io](https://sentry.io/) e navegue até sua organização `revton-solucoes-tecnologicas`.

2.  **Selecione o Projeto**:
    Vá para a lista de projetos e selecione um dos que você criou (ex: `myfinance-backend`).

3.  **Encontre a Chave DSN**:
    - No menu lateral do projeto, vá para **Settings** (Configurações).
    - Na seção **SDK Setup**, clique em **Client Keys (DSN)**.
    - Copie o valor do campo **DSN**. Ele se parecerá com `https://<chave_publica>@oXXXXXX.ingest.sentry.io/<id_do_projeto>`.

4.  **Repita para o outro projeto**:
    Faça o mesmo para o projeto do frontend (ex: `myfinance-frontend`) para obter a segunda chave DSN.

---

### **Parte 2: Integração com a Aplicação MyFinance**

Agora, vamos configurar as chaves DSN no código da aplicação.

#### **1. Backend (FastAPI)**

1.  **Adicionar Dependência (se ainda não foi adicionada)**:
    Verifique se o SDK do Sentry está no seu `pyproject.toml`.

    ```toml
    # pyproject.toml
    [project.dependencies]
    sentry-sdk = {extras = ["fastapi"], version = "^1.0"}
    ```
    Se não estiver, adicione e rode `uv pip install -e .`

2.  **Configurar Variável de Ambiente**:
    Adicione a DSN do projeto **backend** do Sentry ao seu arquivo `.env`.

    ```bash
    # .env
    SENTRY_DSN_BACKEND="COLE_A_SUA_DSN_DO_BACKEND_AQUI"
    ```

3.  **Inicializar o SDK**:
    No arquivo `src/main.py`, configure a inicialização do Sentry para usar a nova variável de ambiente.

    ```python
    # src/main.py
    import sentry_sdk
    from src.config import settings # Supondo que suas configs carreguem o .env

    # Inicializa o Sentry
    if settings.SENTRY_DSN_BACKEND:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN_BACKEND,
            # Defina traces_sample_rate como 1.0 para capturar 100%
            # das transações para monitoramento de performance.
            # Ajuste em produção se necessário.
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            environment=settings.ENVIRONMENT, # "development" ou "production"
        )

    app = FastAPI()

    # ... resto da sua aplicação
    ```

4.  **Testar a Integração**:
    Crie um endpoint de teste temporário para gerar um erro e verificar se ele aparece no seu painel do Sentry.

    ```python
    @app.get("/sentry-debug")
    async def trigger_error():
        division_by_zero = 1 / 0
    ```
    Acesse `http://localhost:8002/sentry-debug` e, em alguns instantes, o erro deverá aparecer no projeto `myfinance-backend` no Sentry.

#### **2. Frontend (React)**

1.  **Adicionar Dependências (se ainda não foram adicionadas)**:
    Verifique se os pacotes do Sentry estão no `frontend/package.json`.

    ```bash
    cd frontend
    npm install --save @sentry/react @sentry/tracing
    ```

2.  **Configurar Variável de Ambiente**:
    Adicione a DSN do projeto **frontend** do Sentry ao seu arquivo `frontend/.env`.

    ```bash
    # frontend/.env
    VITE_SENTRY_DSN_FRONTEND="COLE_A_SUA_DSN_DO_FRONTEND_AQUI"
    ```

3.  **Inicializar o SDK**:
    No arquivo `frontend/src/main.tsx`, inicialize o Sentry.

    ```typescript
    // frontend/src/main.tsx
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';
    import * as Sentry from '@sentry/react';

    if (import.meta.env.VITE_SENTRY_DSN_FRONTEND) {
        Sentry.init({
            dsn: import.meta.env.VITE_SENTRY_DSN_FRONTEND,
            integrations: [
                new Sentry.BrowserTracing({
                    // opcional: configure tracing origins se necessário
                }),
                new Sentry.Replay(),
            ],
            // Performance Monitoring
            traces_sample_rate: 1.0, // Capture 100% of the transactions
            // Session Replay
            replays_session_sample_rate: 0.1, // Capture 10% of sessions
            replays_on_error_sample_rate: 1.0, // Capture 100% of sessions with an error
            environment: import.meta.env.VITE_ENVIRONMENT,
        });
    }

    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    );
    ```

4.  **Testar a Integração**:
    Adicione um botão em um componente para gerar um erro de teste.

    ```tsx
    const ErrorButton = () => {
      const handleThrowError = () => {
        throw new Error("Erro de teste do Frontend para o Sentry!");
      };

      return <button onClick={handleThrowError}>Gerar Erro de Teste</button>;
    };
    ```
    Clique no botão e verifique o painel do projeto `myfinance-frontend` no Sentry.

---

## ✅ **Conclusão**

Com estes passos, o Sentry.io estará totalmente integrado ao MyFinance. Você terá uma visão clara e centralizada de todos os erros que ocorrerem na aplicação, permitindo uma resposta rápida e eficaz para garantir a qualidade do software.

---

### 📚 **Opções Futuras (Self-Hosting)**

Para referência futura, caso haja a necessidade de migrar para uma solução auto-hospedada, o **GlitchTip** é uma alternativa open-source compatível com a API do Sentry. A migração envolveria:
1.  Hospedar o GlitchTip (por exemplo, na **Oracle Cloud Free Tier**).
2.  Atualizar as variáveis de ambiente `SENTRY_DSN_BACKEND` e `VITE_SENTRY_DSN_FRONTEND` com a nova DSN do GlitchTip.

Nenhuma alteração no código seria necessária, pois os SDKs são os mesmos.