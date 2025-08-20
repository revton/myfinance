import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Componentes de autenticação
import Login from './components/Login';
import Register from './components/Register';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';

// Componente principal da aplicação
import { DashboardPage } from './pages/DashboardPage';
import CategoriesPage from './pages/CategoriesPage';
import TransactionsPage from './pages/TransactionsPage';
import PrivateRoute from './components/PrivateRoute';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    background: { default: '#f4f6fa' },
  },
});

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

  return (
    <Routes>
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
      
      {/* Redirecionar raiz para dashboard ou login */}
      <Route 
        path="/" 
        element={
          localStorage.getItem('access_token') ? 
            <Navigate to="/dashboard" replace /> : 
            <Navigate to="/auth/login" replace />
        } 
      />
      
      {/* Rota 404 - redirecionar para login */}
      <Route path="*" element={<Navigate to="/auth/login" replace />} />
    </Routes>
  );
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AppRoutes />
      </Router>
    </ThemeProvider>
  );
}

export default App;
