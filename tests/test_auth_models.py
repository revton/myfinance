import pytest
from pydantic import ValidationError
from src.auth.models import UserRegister, UserLogin, UserProfile, UserProfileUpdate, Token, UserResponse
from datetime import datetime
from uuid import uuid4

class TestUserRegister:
    def test_valid_user_register(self):
        """Testa criação de UserRegister válido"""
        # Arrange & Act
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Assert
        assert user_data.email == "test@example.com"
        assert user_data.password == "SecurePass123!"
        assert user_data.full_name == "Test User"
    
    def test_user_register_without_full_name(self):
        """Testa criação de UserRegister sem full_name"""
        # Arrange & Act
        user_data = UserRegister(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        # Assert
        assert user_data.email == "test@example.com"
        assert user_data.password == "SecurePass123!"
        assert user_data.full_name is None
    
    def test_invalid_email_format(self):
        """Testa email com formato inválido"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                email="invalid-email",
                password="SecurePass123!"
            )
        
        assert "email" in str(exc_info.value)
    
    def test_empty_email(self):
        """Testa email vazio"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                email="",
                password="SecurePass123!"
            )
        
        assert "email" in str(exc_info.value)
    
    def test_empty_password(self):
        """Testa senha vazia"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                email="test@example.com",
                password=""
            )
        
        assert "password" in str(exc_info.value)

class TestUserLogin:
    def test_valid_user_login(self):
        """Testa criação de UserLogin válido"""
        # Arrange & Act
        login_data = UserLogin(
            email="test@example.com",
            password="SecurePass123!"
        )
        
        # Assert
        assert login_data.email == "test@example.com"
        assert login_data.password == "SecurePass123!"
    
    def test_invalid_email_format_login(self):
        """Testa email inválido no login"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserLogin(
                email="invalid-email",
                password="SecurePass123!"
            )
        
        assert "email" in str(exc_info.value)
    
    def test_empty_password_login(self):
        """Testa senha vazia no login"""
        # Act & Assert
        # Pydantic não valida senha vazia por padrão, apenas o tipo
        login = UserLogin(
            email="test@example.com",
            password=""
        )
        
        assert login.email == "test@example.com"
        assert login.password == ""

class TestUserProfile:
    def test_valid_user_profile(self):
        """Testa criação de UserProfile válido"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            email="test@example.com",
            full_name="Test User",
            timezone="America/Sao_Paulo",
            currency="BRL",
            language="pt-BR",
            created_at=now,
            updated_at=now
        )
        
        # Assert
        assert profile.id == profile_id
        assert profile.user_id == user_id
        assert profile.email == "test@example.com"
        assert profile.full_name == "Test User"
        assert profile.timezone == "America/Sao_Paulo"
        assert profile.currency == "BRL"
        assert profile.language == "pt-BR"
    
    def test_user_profile_with_defaults(self):
        """Testa criação de UserProfile com valores padrão"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            email="test@example.com",
            created_at=now,
            updated_at=now
        )
        
        # Assert
        assert profile.timezone == "America/Sao_Paulo"
        assert profile.currency == "BRL"
        assert profile.language == "pt-BR"
        assert profile.full_name is None
        assert profile.avatar_url is None
    
    def test_invalid_timezone(self):
        """Testa timezone inválida"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(
                id=profile_id,
                user_id=user_id,
                email="test@example.com",
                timezone="Invalid/Timezone",
                created_at=now,
                updated_at=now
            )
        
        assert "timezone" in str(exc_info.value)
    
    def test_invalid_currency(self):
        """Testa moeda inválida"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(
                id=profile_id,
                user_id=user_id,
                email="test@example.com",
                currency="INVALID",
                created_at=now,
                updated_at=now
            )
        
        assert "currency" in str(exc_info.value)
    
    def test_invalid_language(self):
        """Testa idioma inválido"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(
                id=profile_id,
                user_id=user_id,
                email="test@example.com",
                language="invalid",
                created_at=now,
                updated_at=now
            )
        
        assert "language" in str(exc_info.value)
    
    def test_valid_avatar_url(self):
        """Testa URL de avatar válida"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        # Act
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            email="test@example.com",
            avatar_url="https://example.com/avatar.jpg",
            created_at=now,
            updated_at=now
        )
        
        # Assert
        assert str(profile.avatar_url) == "https://example.com/avatar.jpg"
    
    def test_invalid_avatar_url(self):
        """Testa URL de avatar inválida"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(
                id="profile-123",
                user_id="user-123",
                email="test@example.com",
                avatar_url="not-a-url"
            )
        
        assert "avatar_url" in str(exc_info.value)

class TestUserProfileUpdate:
    def test_valid_user_profile_update(self):
        """Testa criação de UserProfileUpdate válido"""
        # Arrange & Act
        update_data = UserProfileUpdate(
            full_name="Updated Name",
            timezone="America/New_York",
            currency="USD",
            language="en-US"
        )
        
        # Assert
        assert update_data.full_name == "Updated Name"
        assert update_data.timezone == "America/New_York"
        assert update_data.currency == "USD"
        assert update_data.language == "en-US"
    
    def test_partial_user_profile_update(self):
        """Testa atualização parcial do perfil"""
        # Arrange & Act
        update_data = UserProfileUpdate(
            full_name="Updated Name"
        )
        
        # Assert
        assert update_data.full_name == "Updated Name"
        assert update_data.timezone is None
        assert update_data.currency is None
        assert update_data.language is None
    
    def test_invalid_timezone_update(self):
        """Testa timezone inválida na atualização"""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfileUpdate(
                timezone="Invalid/Timezone"
            )
        
        assert "timezone" in str(exc_info.value)

class TestToken:
    def test_valid_token(self):
        """Testa criação de Token válido"""
        # Arrange & Act
        token = Token(
            access_token="access-token-123",
            expires_in=3600
        )
        
        # Assert
        assert token.access_token == "access-token-123"
        assert token.token_type == "bearer"
        assert token.expires_in == 3600
    
    def test_token_with_custom_type(self):
        """Testa token com tipo personalizado"""
        # Arrange & Act
        token = Token(
            access_token="access-token-123",
            token_type="custom",
            expires_in=3600
        )
        
        # Assert
        assert token.token_type == "custom"

class TestUserResponse:
    def test_valid_user_response(self):
        """Testa criação de UserResponse válido"""
        # Arrange
        profile_id = uuid4()
        user_id = uuid4()
        now = datetime.now()
        
        profile = UserProfile(
            id=profile_id,
            user_id=user_id,
            email="test@example.com",
            full_name="Test User",
            created_at=now,
            updated_at=now
        )
        
        # Act
        user_response = UserResponse(
            id=user_id,
            email="test@example.com",
            profile=profile
        )
        
        # Assert
        assert user_response.id == user_id
        assert user_response.email == "test@example.com"
        assert user_response.profile == profile
    
    def test_user_response_without_profile(self):
        """Testa UserResponse sem perfil"""
        # Arrange
        user_id = uuid4()
        
        # Act
        user_response = UserResponse(
            id=user_id,
            email="test@example.com"
        )
        
        # Assert
        assert user_response.id == user_id
        assert user_response.email == "test@example.com"
        assert user_response.profile is None 