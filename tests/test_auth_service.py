import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.auth.service import AuthService
from src.auth.models import UserRegister, UserLogin, UserProfile

class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService()
    
    @pytest.fixture
    def mock_supabase(self):
        with patch('src.auth.service.supabase') as mock:
            yield mock
    
    def test_register_user_success(self, auth_service, mock_supabase):
        """Testa registro de usuário com sucesso"""
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        mock_supabase.auth.sign_up.return_value = {
            'data': {'user': {'id': 'user-123', 'email': 'test@example.com'}},
            'error': None
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value = {
            'data': [{'id': 'profile-123'}],
            'error': None
        }
        
        # Act
        result = auth_service.register_user(user_data)
        
        # Assert
        assert result['user_id'] == 'user-123'
        assert result['email'] == 'test@example.com'
        mock_supabase.auth.sign_up.assert_called_once()
        mock_supabase.table.assert_called_with('user_profiles')
    
    def test_register_user_email_exists(self, auth_service, mock_supabase):
        """Testa registro com email já existente"""
        # Arrange
        user_data = UserRegister(
            email="existing@example.com",
            password="SecurePass123!"
        )
        
        mock_supabase.auth.sign_up.return_value = {
            'data': None,
            'error': {'message': 'User already registered'}
        }
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "já registrado" in str(exc_info.value.detail)
    
    def test_register_user_weak_password(self, auth_service, mock_supabase):
        """Testa registro com senha fraca"""
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="123"
        )
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "senha" in str(exc_info.value.detail).lower()
    
    def test_login_user_success(self, auth_service, mock_supabase):
        """Testa login de usuário com sucesso"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        mock_supabase.auth.sign_in_with_password.return_value = {
            'data': {
                'session': {
                    'access_token': 'token-123',
                    'refresh_token': 'refresh-123',
                    'user': {'id': 'user-123', 'email': 'test@example.com'}
                }
            },
            'error': None
        }
        
        # Act
        result = auth_service.login_user(login_data)
        
        # Assert
        assert result['access_token'] == 'token-123'
        assert result['refresh_token'] == 'refresh-123'
        assert result['user']['id'] == 'user-123'
    
    def test_login_user_invalid_credentials(self, auth_service, mock_supabase):
        """Testa login com credenciais inválidas"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="wrongpassword"
        )
        
        mock_supabase.auth.sign_in_with_password.return_value = {
            'data': None,
            'error': {'message': 'Invalid login credentials'}
        }
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_service.login_user(login_data)
        
        assert exc_info.value.status_code == 401
        assert "credenciais inválidas" in str(exc_info.value.detail)
    
    def test_get_current_user_success(self, auth_service, mock_supabase):
        """Testa obtenção do usuário atual com token válido"""
        # Arrange
        token = "valid-token"
        mock_supabase.auth.get_user.return_value = {
            'data': {'user': {'id': 'user-123', 'email': 'test@example.com'}},
            'error': None
        }
        
        # Act
        result = auth_service.get_current_user(token)
        
        # Assert
        assert result['id'] == 'user-123'
        assert result['email'] == 'test@example.com'
    
    def test_get_current_user_invalid_token(self, auth_service, mock_supabase):
        """Testa obtenção do usuário atual com token inválido"""
        # Arrange
        token = "invalid-token"
        mock_supabase.auth.get_user.return_value = {
            'data': None,
            'error': {'message': 'Invalid token'}
        }
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            auth_service.get_current_user(token)
        
        assert exc_info.value.status_code == 401
        assert "token inválido" in str(exc_info.value.detail)
    
    def test_logout_user_success(self, auth_service, mock_supabase):
        """Testa logout de usuário com sucesso"""
        # Arrange
        mock_supabase.auth.sign_out.return_value = {
            'error': None
        }
        
        # Act
        result = auth_service.logout_user()
        
        # Assert
        assert result['message'] == 'Logout realizado com sucesso'
        mock_supabase.auth.sign_out.assert_called_once()
    
    def test_get_user_profile_success(self, auth_service, mock_supabase):
        """Testa obtenção do perfil do usuário"""
        # Arrange
        user_id = "user-123"
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = {
            'data': [{
                'id': 'profile-123',
                'user_id': 'user-123',
                'email': 'test@example.com',
                'full_name': 'Test User',
                'timezone': 'America/Sao_Paulo',
                'currency': 'BRL',
                'language': 'pt-BR'
            }],
            'error': None
        }
        
        # Act
        result = auth_service.get_user_profile(user_id)
        
        # Assert
        assert result['email'] == 'test@example.com'
        assert result['full_name'] == 'Test User'
        assert result['timezone'] == 'America/Sao_Paulo'
    
    def test_update_user_profile_success(self, auth_service, mock_supabase):
        """Testa atualização do perfil do usuário"""
        # Arrange
        user_id = "user-123"
        profile_data = {
            'full_name': 'Updated Name',
            'timezone': 'America/New_York',
            'currency': 'USD'
        }
        
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = {
            'data': [{
                'id': 'profile-123',
                'user_id': 'user-123',
                'email': 'test@example.com',
                'full_name': 'Updated Name',
                'timezone': 'America/New_York',
                'currency': 'USD'
            }],
            'error': None
        }
        
        # Act
        result = auth_service.update_user_profile(user_id, profile_data)
        
        # Assert
        assert result['full_name'] == 'Updated Name'
        assert result['timezone'] == 'America/New_York'
        assert result['currency'] == 'USD' 