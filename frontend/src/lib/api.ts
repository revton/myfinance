import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const token = localStorage.getItem('access_token');
      if (token) {
        console.log('Authentication error: token is invalid or expired. Redirecting to login.');
        localStorage.removeItem('access_token');
        // Use um evento para notificar a aplicação para redirecionar
        window.dispatchEvent(new Event('auth-error'));
      }
    }
    return Promise.reject(error);
  }
);

export default api;
