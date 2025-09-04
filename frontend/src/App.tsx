import React, { Suspense, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { CircularProgress, Box } from '@mui/material';

// Contexto de notificações
import { NotificationProvider } from './contexts/NotificationContext';
import Toast from './components/common/Toast';

// Importando estilos de transição
import './styles/transitions.css';
import PageTransition from './components/common/PageTransition';

// Componentes de autenticação (lazy loaded)
const Login = React.lazy(() => import('./components/Login'));
const Register = React.lazy(() => import('./components/Register'));
const ForgotPassword = React.lazy(() => import('./components/ForgotPassword'));
const ResetPassword = React.lazy(() => import('./components/ResetPassword'));

// Componente principal da aplicação (lazy loaded)
const DashboardPage = React.lazy(() => import('./pages/DashboardPage'));
const CategoriesPage = React.lazy(() => import('./pages/CategoriesPage'));
const TransactionsPage = React.lazy(() => import('./pages/TransactionsPage'));
const TransactionFormPage = React.lazy(() => import('./pages/TransactionFormPage'));
import PrivateRoute from './components/PrivateRoute';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    background: { default: '#f4f6fa' },
  },
});

const LoadingFallback = () => (
  <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
    <CircularProgress />
  </Box>
);

const AppRoutes: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleAuthError = () => {
      console.log('Redirecting to login due to auth error.');
      navigate('/auth/login');
    };

    window.addEventListener('auth-error', handleAuthError);

    return () => {
      window.removeEventListener('auth-error', handleAuthError);
    };
  }, [navigate]);

  const location = useLocation();

  return (
    <PageTransition>
      <Suspense fallback={<LoadingFallback />}>
        <Routes location={location}>
          {/* Rotas públicas de autenticação */}
          <Route path="/auth/login" element={<Login />} />
          <Route path="/auth/register" element={<Register />} />
          <Route path="/auth/forgot-password" element={<ForgotPassword />} />
          <Route path="/auth/reset-password" element={<ResetPassword />} />

          {/* Rotas protegidas */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/categories"
            element={
              <PrivateRoute>
                <CategoriesPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/transactions"
            element={
              <PrivateRoute>
                <TransactionsPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/transactions/new"
            element={
              <PrivateRoute>
                <TransactionFormPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/transactions/:id/edit"
            element={
              <PrivateRoute>
                <TransactionFormPage />
              </PrivateRoute>
            }
          />

          {/* Redirecionar raiz para dashboard ou login */}
          <Route
            path="/"
            element={
              localStorage.getItem('access_token') ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <Navigate to="/auth/login" replace />
              )
            }
          />

          {/* Rota 404 - redirecionar para login */}
          <Route path="*" element={<Navigate to="/auth/login" replace />} />
        </Routes>
      </Suspense>
    </PageTransition>
  );
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NotificationProvider>
        <Router>
          <AppRoutes />
          <Toast />
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
}

export default App;
