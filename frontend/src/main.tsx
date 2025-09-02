import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { CategoryProvider } from './contexts/CategoryContext'
import { TransactionProvider } from './contexts/TransactionContext'
import * as Sentry from '@sentry/react'

// Inicialização do Sentry
if (import.meta.env.VITE_SENTRY_DSN_FRONTEND) {
  console.log('Inicializando Sentry para monitoramento de erros');
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN_FRONTEND as string,
    integrations: [
      new Sentry.BrowserTracing(),
      new Sentry.Replay(),
    ],
    // Performance Monitoring
    traces_sample_rate: 1.0, // Capture 100% of the transactions
    // Session Replay
    replays_session_sample_rate: 0.1, // Capture 10% of sessions
    replays_on_error_sample_rate: 1.0, // Capture 100% of sessions with an error
    environment: import.meta.env.VITE_ENVIRONMENT as string,
  });
  console.log(`Sentry inicializado com sucesso no ambiente: ${import.meta.env.VITE_ENVIRONMENT}`);

  // Global error handler for unhandled promise rejections
  window.addEventListener('unhandledrejection', event => {
    Sentry.captureException(event.reason);
  });

} else {
  console.warn('Variável VITE_SENTRY_DSN_FRONTEND não configurada. Monitoramento de erros desativado.');
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Sentry.ErrorBoundary fallback={"<p>An error has occurred</p>"}>
      <TransactionProvider>
        <CategoryProvider>
          <App />
        </CategoryProvider>
      </TransactionProvider>
    </Sentry.ErrorBoundary>
  </StrictMode>,
)
