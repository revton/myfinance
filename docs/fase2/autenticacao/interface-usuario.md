# 🎨 Interface do Usuário - Sistema de Autenticação

## 🎯 **Visão Geral**

Este documento descreve os componentes de interface do usuário para o sistema de autenticação, incluindo páginas de login, registro, perfil do usuário e componentes reutilizáveis.

## 📱 **Páginas Principais**

### **1. Página de Login**

```tsx
// src/pages/LoginPage.tsx
import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  CircularProgress
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Email ou senha inválidos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
          <Typography component="h1" variant="h4" align="center" gutterBottom>
            Entrar no MyFinance
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Senha"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Entrar'}
            </Button>
            <Box textAlign="center">
              <Link href="/register" variant="body2">
                {"Não tem uma conta? Registre-se"}
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage;
```

### **2. Página de Registro**

```tsx
// src/pages/RegisterPage.tsx
import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  CircularProgress,
  Stepper,
  Step,
  StepLabel
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const steps = ['Informações Básicas', 'Configurações', 'Confirmação'];

const RegisterPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    timezone: 'America/Sao_Paulo',
    currency: 'BRL',
    language: 'pt-BR'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleSubmit = async () => {
    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await register(formData.email, formData.password, formData.fullName);
      navigate('/dashboard');
    } catch (err) {
      setError('Erro ao criar conta. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <TextField
              margin="normal"
              required
              fullWidth
              label="Nome Completo"
              value={formData.fullName}
              onChange={(e) => setFormData({...formData, fullName: e.target.value})}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              disabled={loading}
            />
          </Box>
        );
      case 1:
        return (
          <Box>
            <TextField
              margin="normal"
              required
              fullWidth
              label="Senha"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              label="Confirmar Senha"
              type="password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              disabled={loading}
            />
          </Box>
        );
      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Confirme suas informações:
            </Typography>
            <Typography>Nome: {formData.fullName}</Typography>
            <Typography>Email: {formData.email}</Typography>
            <Typography>Fuso Horário: {formData.timezone}</Typography>
            <Typography>Moeda: {formData.currency}</Typography>
          </Box>
        );
      default:
        return null;
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ marginTop: 8 }}>
        <Paper elevation={3} sx={{ padding: 4 }}>
          <Typography component="h1" variant="h4" align="center" gutterBottom>
            Criar Conta
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {renderStepContent(activeStep)}

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
            <Button
              disabled={activeStep === 0}
              onClick={handleBack}
            >
              Voltar
            </Button>
            <Box>
              {activeStep === steps.length - 1 ? (
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Criar Conta'}
                </Button>
              ) : (
                <Button variant="contained" onClick={handleNext}>
                  Próximo
                </Button>
              )}
            </Box>
          </Box>

          <Box textAlign="center" sx={{ mt: 2 }}>
            <Link href="/login" variant="body2">
              {"Já tem uma conta? Faça login"}
            </Link>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPage;
```

### **3. Página de Perfil do Usuário**

```tsx
// src/pages/ProfilePage.tsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Avatar,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const ProfilePage: React.FC = () => {
  const { user, updateProfile } = useAuth();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const [formData, setFormData] = useState({
    fullName: '',
    timezone: 'America/Sao_Paulo',
    currency: 'BRL',
    language: 'pt-BR',
    avatarUrl: ''
  });

  useEffect(() => {
    if (user?.profile) {
      setFormData({
        fullName: user.profile.full_name || '',
        timezone: user.profile.timezone || 'America/Sao_Paulo',
        currency: user.profile.currency || 'BRL',
        language: user.profile.language || 'pt-BR',
        avatarUrl: user.profile.avatar_url || ''
      });
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await updateProfile(formData);
      setSuccess('Perfil atualizado com sucesso!');
    } catch (err) {
      setError('Erro ao atualizar perfil. Tente novamente.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ marginTop: 4, marginBottom: 4 }}>
        <Typography variant="h4" gutterBottom>
          Perfil do Usuário
        </Typography>

        <Paper elevation={3} sx={{ padding: 4 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
            <Avatar
              src={formData.avatarUrl}
              sx={{ width: 80, height: 80, mr: 2 }}
            >
              {user?.profile?.full_name?.charAt(0) || user?.email?.charAt(0)}
            </Avatar>
            <Box>
              <Typography variant="h6">
                {user?.profile?.full_name || 'Usuário'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user?.email}
              </Typography>
            </Box>
          </Box>

          <Box component="form" onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Nome Completo"
                  value={formData.fullName}
                  onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                  disabled={saving}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="URL do Avatar"
                  value={formData.avatarUrl}
                  onChange={(e) => setFormData({...formData, avatarUrl: e.target.value})}
                  disabled={saving}
                  helperText="URL da imagem de perfil (opcional)"
                />
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Fuso Horário</InputLabel>
                  <Select
                    value={formData.timezone}
                    label="Fuso Horário"
                    onChange={(e) => setFormData({...formData, timezone: e.target.value})}
                    disabled={saving}
                  >
                    <MenuItem value="America/Sao_Paulo">São Paulo (GMT-3)</MenuItem>
                    <MenuItem value="America/New_York">Nova York (GMT-5)</MenuItem>
                    <MenuItem value="Europe/London">Londres (GMT+0)</MenuItem>
                    <MenuItem value="Asia/Tokyo">Tóquio (GMT+9)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Moeda</InputLabel>
                  <Select
                    value={formData.currency}
                    label="Moeda"
                    onChange={(e) => setFormData({...formData, currency: e.target.value})}
                    disabled={saving}
                  >
                    <MenuItem value="BRL">Real (R$)</MenuItem>
                    <MenuItem value="USD">Dólar ($)</MenuItem>
                    <MenuItem value="EUR">Euro (€)</MenuItem>
                    <MenuItem value="GBP">Libra (£)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth>
                  <InputLabel>Idioma</InputLabel>
                  <Select
                    value={formData.language}
                    label="Idioma"
                    onChange={(e) => setFormData({...formData, language: e.target.value})}
                    disabled={saving}
                  >
                    <MenuItem value="pt-BR">Português (BR)</MenuItem>
                    <MenuItem value="en-US">English (US)</MenuItem>
                    <MenuItem value="es-ES">Español (ES)</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                disabled={saving}
              >
                {saving ? <CircularProgress size={24} /> : 'Salvar Alterações'}
              </Button>
              <Button
                variant="outlined"
                onClick={() => window.history.back()}
                disabled={saving}
              >
                Cancelar
              </Button>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default ProfilePage;
```

## 🔧 **Componentes Reutilizáveis**

### **1. AuthContext**

```tsx
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '../lib/supabase';
import { User, UserProfile } from '../types/auth';

interface AuthContextType {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => Promise<void>;
  updateProfile: (profile: Partial<UserProfile>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar sessão atual
    const getSession = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user ?? null);
      
      if (session?.user) {
        await fetchProfile(session.user.id);
      }
    };

    getSession();

    // Escutar mudanças de autenticação
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        setUser(session?.user ?? null);
        
        if (session?.user) {
          await fetchProfile(session.user.id);
        } else {
          setProfile(null);
        }
        
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const fetchProfile = async (userId: string) => {
    try {
      const { data, error } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', userId)
        .single();

      if (error) throw error;
      setProfile(data);
    } catch (error) {
      console.error('Erro ao buscar perfil:', error);
    }
  };

  const login = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    
    if (error) throw error;
  };

  const register = async (email: string, password: string, fullName?: string) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
    });
    
    if (error) throw error;

    // Criar perfil do usuário
    if (data.user) {
      const { error: profileError } = await supabase
        .from('user_profiles')
        .insert([
          {
            user_id: data.user.id,
            email: data.user.email,
            full_name: fullName,
          }
        ]);

      if (profileError) throw profileError;
    }
  };

  const logout = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  const updateProfile = async (profileData: Partial<UserProfile>) => {
    if (!user) throw new Error('Usuário não autenticado');

    const { data, error } = await supabase
      .from('user_profiles')
      .update(profileData)
      .eq('user_id', user.id)
      .select()
      .single();

    if (error) throw error;
    setProfile(data);
  };

  const value = {
    user,
    profile,
    loading,
    login,
    register,
    logout,
    updateProfile,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
```

### **2. ProtectedRoute**

```tsx
// src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { CircularProgress, Box } from '@mui/material';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
```

### **3. UserMenu**

```tsx
// src/components/UserMenu.tsx
import React, { useState } from 'react';
import {
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Typography,
  Box,
  Divider
} from '@mui/material';
import { AccountCircle, Settings, Logout } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const UserMenu: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const { user, profile, logout } = useAuth();
  const navigate = useNavigate();

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleProfile = () => {
    handleClose();
    navigate('/profile');
  };

  const handleLogout = async () => {
    handleClose();
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  return (
    <Box>
      <IconButton
        size="large"
        aria-label="menu do usuário"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleMenu}
        color="inherit"
      >
        {profile?.avatar_url ? (
          <Avatar src={profile.avatar_url} sx={{ width: 32, height: 32 }}>
            {profile.full_name?.charAt(0) || user?.email?.charAt(0)}
          </Avatar>
        ) : (
          <AccountCircle />
        )}
      </IconButton>
      <Menu
        id="menu-appbar"
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem disabled>
          <Box>
            <Typography variant="subtitle2">
              {profile?.full_name || 'Usuário'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {user?.email}
            </Typography>
          </Box>
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleProfile}>
          <Settings sx={{ mr: 1 }} />
          Perfil
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <Logout sx={{ mr: 1 }} />
          Sair
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default UserMenu;
```

## 🎨 **Design System**

### **Cores e Temas**

```tsx
// src/theme/index.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
        },
      },
    },
  },
});
```

### **Responsividade**

```tsx
// src/hooks/useResponsive.ts
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

export const useResponsive = () => {
  const theme = useTheme();
  
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  
  return { isMobile, isTablet, isDesktop };
};
```

## 🧪 **Testes de Interface**

### **Teste do LoginPage**

```tsx
// src/pages/__tests__/LoginPage.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { AuthProvider } from '../../contexts/AuthContext';
import { theme } from '../../theme';
import LoginPage from '../LoginPage';

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <AuthProvider>
          {component}
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
};

describe('LoginPage', () => {
  test('renderiza campos de email e senha', () => {
    renderWithProviders(<LoginPage />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
  });

  test('exibe erro quando credenciais são inválidas', async () => {
    renderWithProviders(<LoginPage />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/senha/i);
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/email ou senha inválidos/i)).toBeInTheDocument();
    });
  });
});
```

Esta interface do usuário fornece uma experiência completa e intuitiva para o sistema de autenticação, com componentes reutilizáveis, design responsivo e testes adequados. 