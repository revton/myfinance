import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.auth.service import AuthService
from src.auth.models import UserRegister, UserLogin, UserProfile, UserProfileUpdate

class TestAuthService:
    @pytest.fixture
    def mock_supabase(self):
        with patch('src.auth.service.create_client') as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client
            yield mock_client
    
    @pytest.fixture
    def auth_service(self, mock_supabase):
        return AuthService()
    
    @pytest.mark.asyncio
    async def test_register_user_success(self, auth_service, mock_supabase):
        """Testa registro de usuário com sucesso"""
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Mock para sign_up
        mock_user = Mock()
        mock_user.id = 'user-123'
        mock_user.email = 'test@example.com'
        
        mock_auth_response = Mock()
        mock_auth_response.error = None
        mock_auth_response.user = mock_user
        
        mock_supabase.auth.sign_up.return_value = mock_auth_response
        
        # Mock para table insert
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()
        
        mock_execute.data = [{'id': 'profile-123'}]
        mock_execute.error = None
        
        mock_insert.execute.return_value = mock_execute
        mock_table.insert.return_value = mock_insert
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = await auth_service.register_user(user_data)
        
        # Assert
        assert result['user_id'] == 'user-123'
        assert result['email'] == 'test@example.com'
        mock_supabase.auth.sign_up.assert_called_once()
        mock_supabase.table.assert_called_with('user_profiles')
    
    @pytest.mark.asyncio
    async def test_register_user_email_exists(self, auth_service, mock_supabase):
        """Testa registro com email já existente"""
        # Arrange
        user_data = UserRegister(
            email="existing@example.com",
            password="SecurePass123!"
        )
        
        # Mock para sign_up com erro
        mock_auth_response = Mock()
        mock_auth_response.error = Mock()
        mock_auth_response.error.message = 'User already registered'
        mock_auth_response.user = None
        
        mock_supabase.auth.sign_up.return_value = mock_auth_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.register_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "já registrado" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_register_user_weak_password(self, auth_service, mock_supabase):
        """Testa registro com senha fraca"""
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!"  # Senha válida para passar na validação do modelo
        )
        
        # Mock para sign_up com erro de senha fraca
        mock_auth_response = Mock()
        mock_auth_response.error = Mock()
        mock_auth_response.error.message = 'Password is too weak'
        mock_auth_response.user = None
        
        mock_supabase.auth.sign_up.return_value = mock_auth_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.register_user(user_data)
        
        assert exc_info.value.status_code == 400
        assert "erro no registro" in str(exc_info.value.detail).lower()
    
    @pytest.mark.asyncio
    async def test_login_user_success(self, auth_service, mock_supabase):
        """Testa login de usuário com sucesso"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        # Mock para sign_in_with_password
        mock_session = Mock()
        mock_session.access_token = 'token-123'
        mock_session.refresh_token = 'refresh-123'
        mock_session.expires_in = 3600
        
        mock_user = Mock()
        mock_user.id = 'user-123'
        mock_user.email = 'test@example.com'
        
        mock_auth_response = Mock()
        mock_auth_response.error = None
        mock_auth_response.session = mock_session
        mock_auth_response.user = mock_user
        
        mock_supabase.auth.sign_in_with_password.return_value = mock_auth_response
        
        # Mock para table select
        mock_table = Mock()
        mock_select = Mock()
        mock_eq = Mock()
        mock_execute = Mock()
        
        mock_execute.data = [{'id': 'profile-123', 'user_id': 'user-123'}]
        
        mock_eq.execute.return_value = mock_execute
        mock_select.eq.return_value = mock_eq
        mock_table.select.return_value = mock_select
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = await auth_service.login_user(login_data)
        
        # Assert
        assert result['access_token'] == 'token-123'
        assert result['refresh_token'] == 'refresh-123'
        assert result['user']['id'] == 'user-123'
    
    @pytest.mark.asyncio
    async def test_login_user_invalid_credentials(self, auth_service, mock_supabase):
        """Testa login com credenciais inválidas"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="wrongpassword"
        )
        
        # Mock para sign_in_with_password com erro
        mock_auth_response = Mock()
        mock_auth_response.error = Mock()
        mock_auth_response.error.message = 'Invalid login credentials'
        
        mock_supabase.auth.sign_in_with_password.return_value = mock_auth_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login_user(login_data)
        
        assert exc_info.value.status_code == 401
        assert "Email ou senha inválidos" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_get_current_user_success(self, auth_service, mock_supabase):
        """Testa obtenção do usuário atual com token válido"""
        # Arrange
        token = "valid-token"
        
        # Mock para get_user
        mock_user = Mock()
        mock_user.id = 'user-123'
        mock_user.email = 'test@example.com'
        
        mock_user_response = Mock()
        mock_user_response.error = None
        mock_user_response.user = mock_user
        
        mock_supabase.auth.get_user.return_value = mock_user_response
        
        # Mock para table select
        mock_table = Mock()
        mock_select = Mock()
        mock_eq = Mock()
        mock_execute = Mock()
        
        mock_execute.data = [{'id': 'profile-123', 'user_id': 'user-123'}]
        
        mock_eq.execute.return_value = mock_execute
        mock_select.eq.return_value = mock_eq
        mock_table.select.return_value = mock_select
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = await auth_service.get_current_user(token)
        
        # Assert
        assert result['id'] == 'user-123'
        assert result['email'] == 'test@example.com'
    
    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, auth_service, mock_supabase):
        """Testa obtenção do usuário atual com token inválido"""
        # Arrange
        token = "invalid-token"
        
        # Mock para get_user com erro
        mock_user_response = Mock()
        mock_user_response.error = Mock()
        mock_user_response.error.message = 'Invalid token'
        
        mock_supabase.auth.get_user.return_value = mock_user_response
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.get_current_user(token)
        
        assert exc_info.value.status_code == 401
        assert "Token inválido" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_logout_user_success(self, auth_service, mock_supabase):
        """Testa logout de usuário com sucesso"""
        # Arrange
        mock_supabase.auth.sign_out.return_value = None
        
        # Act
        result = await auth_service.logout_user()
        
        # Assert
        assert result['message'] == 'Logout realizado com sucesso'
        mock_supabase.auth.sign_out.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_profile_success(self, auth_service, mock_supabase):
        """Testa obtenção do perfil do usuário"""
        # Arrange
        user_id = "user-123"
        
        # Mock para table select
        mock_table = Mock()
        mock_select = Mock()
        mock_eq = Mock()
        mock_execute = Mock()
        
        mock_execute.data = [{
            'id': 'profile-123',
            'user_id': 'user-123',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'timezone': 'America/Sao_Paulo',
            'currency': 'BRL',
            'language': 'pt-BR'
        }]
        mock_execute.error = None
        
        mock_eq.execute.return_value = mock_execute
        mock_select.eq.return_value = mock_eq
        mock_table.select.return_value = mock_select
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = await auth_service.get_user_profile(user_id)
        
        # Assert
        assert result['email'] == 'test@example.com'
        assert result['full_name'] == 'Test User'
        assert result['timezone'] == 'America/Sao_Paulo'
    
    @pytest.mark.asyncio
    async def test_update_user_profile_success(self, auth_service, mock_supabase):
        """Testa atualização do perfil do usuário"""
        # Arrange
        user_id = "user-123"
        profile_data = UserProfileUpdate(
            full_name='Updated Name',
            timezone='America/New_York',
            currency='USD'
        )
        
        # Mock para table update
        mock_table = Mock()
        mock_update = Mock()
        mock_eq = Mock()
        mock_execute = Mock()
        
        mock_execute.data = [{
            'id': 'profile-123',
            'user_id': 'user-123',
            'email': 'test@example.com',
            'full_name': 'Updated Name',
            'timezone': 'America/New_York',
            'currency': 'USD'
        }]
        mock_execute.error = None
        
        mock_eq.execute.return_value = mock_execute
        mock_update.eq.return_value = mock_eq
        mock_table.update.return_value = mock_update
        mock_supabase.table.return_value = mock_table
        
        # Act
        result = await auth_service.update_user_profile(user_id, profile_data)
        
        # Assert
        assert result['full_name'] == 'Updated Name'
        assert result['timezone'] == 'America/New_York'
        assert result['currency'] == 'USD' 