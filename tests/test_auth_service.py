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
    @patch('src.auth.service.SessionLocal')
    async def test_register_user_success(self, mock_session_local, auth_service, mock_supabase):
        """Testa registro de usuário com sucesso"""
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Mock para sign_up
        mock_user = Mock()
        mock_user.id = '550e8400-e29b-41d4-a716-446655440000'  # UUID válido
        mock_user.email = 'test@example.com'
        
        mock_auth_response = Mock()
        mock_auth_response.error = None
        mock_auth_response.user = mock_user
        
        mock_supabase.auth.sign_up.return_value = mock_auth_response
        
        # Mock para banco de dados
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        # Act
        result = await auth_service.register_user(user_data)
        
        # Assert
        assert result['user_id'] == '550e8400-e29b-41d4-a716-446655440000'
        assert result['email'] == 'test@example.com'
        mock_supabase.auth.sign_up.assert_called_once()
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.auth.service.SessionLocal')
    async def test_register_user_email_exists(self, mock_session_local, auth_service, mock_supabase):
        """Testa registro com email já existente"""
        # Arrange
        user_data = UserRegister(
            email="existing@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Mock para sign_up com erro
        mock_auth_response = Mock()
        mock_auth_response.error = Mock()
        mock_auth_response.error.message = 'User already registered'
        mock_auth_response.user = None
        
        mock_supabase.auth.sign_up.return_value = mock_auth_response
        
        # Mock para banco de dados
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.register_user(user_data)
        
        assert exc_info.value.status_code == 500  # O service retorna 500 para erro do Supabase
        assert "erro ao registrar usuário" in str(exc_info.value.detail).lower()
    
    @pytest.mark.asyncio
    @patch('src.auth.service.SessionLocal')
    async def test_login_user_success(self, mock_session_local, auth_service, mock_supabase):
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
        mock_user.id = '550e8400-e29b-41d4-a716-446655440000'
        mock_user.email = 'test@example.com'
        
        mock_auth_response = Mock()
        mock_auth_response.error = None
        mock_auth_response.session = mock_session
        mock_auth_response.user = mock_user
        
        mock_supabase.auth.sign_in_with_password.return_value = mock_auth_response
        
        # Mock para banco de dados
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        # Mock para query do perfil
        mock_profile = Mock()
        mock_profile.id = 'profile-123'
        mock_profile.user_id = '550e8400-e29b-41d4-a716-446655440000'
        mock_profile.email = 'test@example.com'
        mock_profile.full_name = 'Test User'
        mock_profile.password_hash = '$2b$12$PN4.7VRTVpV/dGCMpOO9keBO6CoG477tnC69byYfbxwA5aN6HeI1G'  # Hash válido
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_profile
        
        mock_db.query.return_value = mock_query
        
        # Act
        result = await auth_service.login_user(login_data)
        
        # Assert
        assert 'access_token' in result
        assert result['access_token'] is not None
        assert result['user']['id'] == '550e8400-e29b-41d4-a716-446655440000'
        mock_db.close.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.auth.service.SessionLocal')
    async def test_login_user_invalid_credentials(self, mock_session_local, auth_service, mock_supabase):
        """Testa login com credenciais inválidas"""
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="wrongpassword"
        )
        
        # Mock para banco de dados - perfil não encontrado
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None  # Perfil não encontrado
        
        mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login_user(login_data)
        
        assert exc_info.value.status_code == 401
        assert "Credenciais inválidas" in str(exc_info.value.detail)
    

    
    @pytest.mark.asyncio
    async def test_logout_user_success(self, auth_service, mock_supabase):
        """Testa logout de usuário com sucesso"""
        # Arrange
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        
        # Act
        result = await auth_service.logout_user(user_id)
        
        # Assert
        assert result['message'] == 'Logout realizado com sucesso'
    
    @pytest.mark.asyncio
    @patch('src.auth.service.SessionLocal')
    async def test_get_user_profile_success(self, mock_session_local, auth_service, mock_supabase):
        """Testa obtenção do perfil do usuário"""
        # Arrange
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        
        # Mock para banco de dados
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        # Mock para query do perfil
        mock_profile = Mock()
        mock_profile.id = 'profile-123'
        mock_profile.user_id = '550e8400-e29b-41d4-a716-446655440000'
        mock_profile.email = 'test@example.com'
        mock_profile.full_name = 'Test User'
        mock_profile.timezone = 'America/Sao_Paulo'
        mock_profile.currency = 'BRL'
        mock_profile.language = 'pt-BR'
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_profile
        
        mock_db.query.return_value = mock_query
        
        # Act
        result = await auth_service.get_user_profile(user_id)
        
        # Assert
        assert result['email'] == 'test@example.com'
        assert result['full_name'] == 'Test User'
        assert result['timezone'] == 'America/Sao_Paulo'
        mock_db.close.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('src.auth.service.SessionLocal')
    async def test_update_user_profile_success(self, mock_session_local, auth_service, mock_supabase):
        """Testa atualização do perfil do usuário"""
        # Arrange
        user_id = "550e8400-e29b-41d4-a716-446655440000"
        profile_data = UserProfileUpdate(
            full_name='Updated Name',
            timezone='America/New_York',
            currency='USD'
        )
        
        # Mock para banco de dados
        mock_db = Mock()
        mock_session_local.return_value = mock_db
        
        # Mock para query do perfil
        mock_profile = Mock()
        mock_profile.id = 'profile-123'
        mock_profile.user_id = '550e8400-e29b-41d4-a716-446655440000'
        mock_profile.email = 'test@example.com'
        mock_profile.full_name = 'Updated Name'
        mock_profile.timezone = 'America/New_York'
        mock_profile.currency = 'USD'
        mock_profile.language = 'pt-BR'
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_profile
        
        mock_db.query.return_value = mock_query
        
        # Act
        result = await auth_service.update_user_profile(user_id, profile_data)
        
        # Assert
        assert result['full_name'] == 'Updated Name'
        assert result['timezone'] == 'America/New_York'
        assert result['currency'] == 'USD'
        mock_db.commit.assert_called_once()
        mock_db.close.assert_called_once() 