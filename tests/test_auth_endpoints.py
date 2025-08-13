import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from src.main import app
from src.auth.dependencies import get_auth_service

client = TestClient(app)

@pytest.fixture
def mock_auth_service():
    mock_auth_service_instance = MagicMock()
    mock_auth_service_instance.register_user = AsyncMock(return_value={
        "user_id": "user-123",
        "email": "test@example.com"
    })
    mock_auth_service_instance.login_user = AsyncMock(return_value={
        "access_token": "token-123",
        "refresh_token": "refresh-123",
        "token_type": "bearer",
        "user": {"id": "user-123", "email": "test@example.com"}
    })
    mock_auth_service_instance.logout_user = AsyncMock(return_value={"message": "Logout realizado com sucesso"})
    mock_auth_service_instance.get_user_profile = AsyncMock(return_value={
        "id": "profile-123",
        "user_id": "user-123",
        "email": "test@example.com",
        "full_name": "Test User",
        "timezone": "America/Sao_Paulo",
        "currency": "BRL",
        "language": "pt-BR"
    })
    mock_auth_service_instance.update_user_profile = AsyncMock(return_value={
        "id": "profile-123",
        "user_id": "user-123",
        "email": "test@example.com",
        "full_name": "Updated Name",
        "timezone": "America/New_York",
        "currency": "USD",
        "language": "pt-BR"
    })
    mock_auth_service_instance.refresh_token = AsyncMock(return_value={
        "access_token": "new-access-token-123",
        "refresh_token": "new-refresh-token-123",
        "token_type": "bearer"
    })

    app.dependency_overrides[get_auth_service] = lambda: mock_auth_service_instance
    yield mock_auth_service_instance
    app.dependency_overrides.clear()

class TestAuthEndpoints:
    def test_register_endpoint_success(self, mock_auth_service):
        """Testa endpoint de registro com sucesso"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "Test User"
        }
        
        
        
        # Act
        response = client.post("/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["user_id"] == "user-123"
        mock_auth_service.register_user.assert_called_once()
    
    def test_register_endpoint_invalid_data(self, mock_auth_service):
        """Testa endpoint de registro com dados inválidos"""
        # Arrange
        user_data = {
            "email": "invalid-email",
            "password": "123"
        }
        
        # Act
        response = client.post("/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_register_endpoint_missing_required_fields(self, mock_auth_service):
        """Testa endpoint de registro com campos obrigatórios ausentes"""
        # Arrange
        user_data = {
            "email": "test@example.com"
            # password ausente
        }
        
        # Act
        response = client.post("/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_login_endpoint_success(self, mock_auth_service):
        """Testa endpoint de login com sucesso"""
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["access_token"] == "token-123"
        assert result["refresh_token"] == "refresh-123"
        assert result["token_type"] == "bearer"
        assert result["user"]["id"] == "user-123"
    
    def test_login_endpoint_invalid_data(self, mock_auth_service):
        """Testa endpoint de login com dados inválidos"""
        # Arrange
        login_data = {
            "email": "invalid-email",
            "password": ""
        }
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_login_endpoint_invalid_credentials(self, mock_auth_service):
        """Testa endpoint de login com credenciais inválidas"""
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        from fastapi import HTTPException
        mock_auth_service.login_user.side_effect = HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 401
        assert "credenciais inválidas" in response.json()["detail"].lower()
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_me_endpoint_success(self, mock_jwt_handler, mock_auth_service):
        """Testa endpoint /me com token válido"""
        # Arrange
        mock_jwt = mock_jwt_handler.return_value
        mock_jwt.verify_token.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        # The mock_auth_service fixture already sets a default return_value for get_user_profile
        # If a different return value is needed for this specific test, it can be set here:
        # mock_auth_service.get_user_profile.return_value = {...}
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/auth/me", headers=headers)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["email"] == "test@example.com"
        assert result["id"] == "user-123"
        assert result["profile"]["full_name"] == "Test User"
    
    def test_me_endpoint_no_token(self):
        """Testa endpoint /me sem token"""
        # Act
        response = client.get("/auth/me")
        
        # Assert
        assert response.status_code == 401
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_me_endpoint_invalid_token(self, mock_jwt_handler):
        """Testa endpoint /me com token inválido"""
        # Arrange
        mock_jwt_handler.return_value.verify_token.side_effect = ValueError("Invalid token")
        headers = {"Authorization": "Bearer invalid-token"}
        
        # Act
        response = client.get("/auth/me", headers=headers)
        
        # Assert
        assert response.status_code == 401
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_logout_endpoint_success(self, mock_jwt_handler, mock_auth_service):
        """Testa endpoint de logout com sucesso"""
        # Arrange
        mock_jwt = mock_jwt_handler.return_value
        mock_jwt.verify_token.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post("/auth/logout", headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Logout realizado com sucesso"
    
    def test_logout_endpoint_no_token(self):
        """Testa endpoint de logout sem token"""
        # Act
        response = client.post("/auth/logout")
        
        # Assert
        assert response.status_code == 401
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_profile_endpoint_success(self, mock_jwt_handler, mock_auth_service):
        """Testa endpoint de perfil com sucesso"""
        # Arrange
        mock_jwt = mock_jwt_handler.return_value
        mock_jwt.verify_token.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/auth/profile", headers=headers)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["email"] == "test@example.com"
        assert result["full_name"] == "Test User"
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_profile_update_endpoint_success(self, mock_jwt_handler, mock_auth_service):
        """Testa endpoint de atualização de perfil com sucesso"""
        # Arrange
        mock_jwt = mock_jwt_handler.return_value
        mock_jwt.verify_token.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        update_data = {
            "full_name": "Updated Name",
            "timezone": "America/New_York",
            "currency": "USD"
        }
        
        
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.put("/auth/profile", json=update_data, headers=headers)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["full_name"] == "Updated Name"
        assert result["timezone"] == "America/New_York"
        assert result["currency"] == "USD"
    
    @patch('src.auth.dependencies.get_jwt_handler')
    def test_profile_update_endpoint_invalid_data(self, mock_jwt_handler, mock_auth_service):
        """Testa endpoint de atualização de perfil com dados inválidos"""
        # Arrange
        mock_jwt = mock_jwt_handler.return_value
        mock_jwt.verify_token.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        update_data = {
            "timezone": "Invalid/Timezone"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.put("/auth/profile", json=update_data, headers=headers)
        
        # Assert
        assert response.status_code == 422
    
    def test_profile_update_endpoint_no_token(self):
        """Testa endpoint de atualização de perfil sem token"""
        # Arrange
        update_data = {
            "full_name": "Updated Name"
        }
        
        # Act
        response = client.put("/auth/profile", json=update_data)
        
        # Assert
        assert response.status_code == 401
    
    def test_refresh_token_endpoint_success(self, mock_auth_service):
        """Testa endpoint de refresh token com sucesso"""
        # Arrange
        refresh_data = {
            "refresh_token": "refresh-token-123"
        }
        
        
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["access_token"] == "new-access-token-123"
        assert result["refresh_token"] == "new-refresh-token-123"
    
    def test_refresh_token_endpoint_invalid_data(self, mock_auth_service):
        """Testa endpoint de refresh token com dados inválidos"""
        # Arrange
        refresh_data = {
            "refresh_token": ""
        }
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 422
    
    def test_refresh_token_endpoint_invalid_token(self, mock_auth_service):
        """Testa endpoint de refresh token com token inválido"""
        # Arrange
        refresh_data = {
            "refresh_token": "invalid-refresh-token"
        }
        
        from fastapi import HTTPException
        mock_auth_service.refresh_token.side_effect = HTTPException(status_code=401, detail="Token de refresh inválido")
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 401
        assert "token de refresh inválido" in response.json()["detail"].lower()
