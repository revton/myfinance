import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { CategoryProvider } from './contexts/CategoryContext'
import { TransactionProvider } from './contexts/TransactionContext'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TransactionProvider>
      <CategoryProvider>
        <App />
      </CategoryProvider>
    </TransactionProvider>
  </StrictMode>,
)
