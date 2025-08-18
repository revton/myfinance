import React, { useState, useEffect, ReactNode } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Avatar,
  Menu,
  MenuItem as MenuItemComponent,
  Container
} from '@mui/material';
import { Link } from 'react-router-dom';

interface User {
  id: string;
  email: string;
  full_name: string;
}

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    const loadUser = () => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        setUser(JSON.parse(userStr));
      }
    };
    loadUser();
  }, []);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/auth/login';
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography 
            variant="h6" 
            component={Link} 
            to="/dashboard" 
            sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }} 
          >
            💰 MyFinance
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="body2" sx={{ display: { xs: 'none', sm: 'block' } }}>
              Olá, {user?.full_name || 'Usuário'}
            </Typography>
            
            <IconButton
              onClick={handleMenuOpen}
              sx={{ color: 'white' }}
            >
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'rgba(255,255,255,0.2)' }}>
                {user?.full_name?.charAt(0) || 'U'}
              </Avatar>
            </IconButton>
            
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItemComponent onClick={handleMenuClose} component={Link} to="/dashboard">
                Dashboard
              </MenuItemComponent>
              <MenuItemComponent onClick={handleMenuClose}>
                Perfil
              </MenuItemComponent>
              <MenuItemComponent onClick={handleMenuClose} component={Link} to="/categories">
                Categorias
              </MenuItemComponent>
              <MenuItemComponent onClick={handleLogout}>
                Sair
              </MenuItemComponent>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {children}
      </Container>
    </>
  );
};

export default Layout;
