import React from 'react';
import { Navigate } from 'react-router-dom';
import Layout from './Layout';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    return <Navigate to="/auth/login" replace />;
  }
  
  return <Layout>{children}</Layout>;
};

export default PrivateRoute;
