import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

class TestAuthEndpoints:
    @patch('src.auth.service.AuthService.register_user')
    def test_register_endpoint_success(self, mock_register):
        """Testa endpoint de registro com sucesso"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "Test User"
        }
        
        mock_register.return_value = {
            "user_id": "user-123",
            "email": "test@example.com"
        }
        
        # Act
        response = client.post("/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["user_id"] == "user-123"
        mock_register.assert_called_once()
    
    def test_register_endpoint_invalid_data(self):
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
    
    def test_register_endpoint_missing_required_fields(self):
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
    
    @patch('src.auth.service.AuthService.login_user')
    def test_login_endpoint_success(self, mock_login):
        """Testa endpoint de login com sucesso"""
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        mock_login.return_value = {
            "access_token": "token-123",
            "refresh_token": "refresh-123",
            "token_type": "bearer",
            "user": {"id": "user-123", "email": "test@example.com"}
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
    
    def test_login_endpoint_invalid_data(self):
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
    
    @patch('src.auth.service.AuthService.login_user')
    def test_login_endpoint_invalid_credentials(self, mock_login):
        """Testa endpoint de login com credenciais inválidas"""
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        from fastapi import HTTPException
        mock_login.side_effect = HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 401
        assert "credenciais inválidas" in response.json()["detail"].lower()
    
    @patch('src.auth.service.AuthService.get_current_user')
    def test_me_endpoint_success(self, mock_get_user):
        """Testa endpoint /me com token válido"""
        # Arrange
        mock_get_user.return_value = {
            "id": "user-123",
            "email": "test@example.com",
            "profile": {
                "full_name": "Test User",
                "timezone": "America/Sao_Paulo",
                "currency": "BRL"
            }
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/auth/me", headers=headers)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["email"] == "test@example.com"
        assert result["profile"]["full_name"] == "Test User"
    
    def test_me_endpoint_no_token(self):
        """Testa endpoint /me sem token"""
        # Act
        response = client.get("/auth/me")
        
        # Assert
        assert response.status_code == 401
    
    def test_me_endpoint_invalid_token(self):
        """Testa endpoint /me com token inválido"""
        # Arrange
        headers = {"Authorization": "Bearer invalid-token"}
        
        # Act
        response = client.get("/auth/me", headers=headers)
        
        # Assert
        assert response.status_code == 401
    
    @patch('src.auth.service.AuthService.logout_user')
    def test_logout_endpoint_success(self, mock_logout):
        """Testa endpoint de logout com sucesso"""
        # Arrange
        mock_logout.return_value = {"message": "Logout realizado com sucesso"}
        
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
    
    @patch('src.auth.service.AuthService.get_user_profile')
    def test_profile_endpoint_success(self, mock_get_profile):
        """Testa endpoint de perfil com sucesso"""
        # Arrange
        mock_get_profile.return_value = {
            "id": "profile-123",
            "user_id": "user-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "timezone": "America/Sao_Paulo",
            "currency": "BRL",
            "language": "pt-BR"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/auth/profile", headers=headers)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["email"] == "test@example.com"
        assert result["full_name"] == "Test User"
    
    @patch('src.auth.service.AuthService.update_user_profile')
    def test_profile_update_endpoint_success(self, mock_update_profile):
        """Testa endpoint de atualização de perfil com sucesso"""
        # Arrange
        update_data = {
            "full_name": "Updated Name",
            "timezone": "America/New_York",
            "currency": "USD"
        }
        
        mock_update_profile.return_value = {
            "id": "profile-123",
            "user_id": "user-123",
            "email": "test@example.com",
            "full_name": "Updated Name",
            "timezone": "America/New_York",
            "currency": "USD",
            "language": "pt-BR"
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
    
    def test_profile_update_endpoint_invalid_data(self):
        """Testa endpoint de atualização de perfil com dados inválidos"""
        # Arrange
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
    
    @patch('src.auth.service.AuthService.refresh_token')
    def test_refresh_token_endpoint_success(self, mock_refresh):
        """Testa endpoint de refresh token com sucesso"""
        # Arrange
        refresh_data = {
            "refresh_token": "refresh-token-123"
        }
        
        mock_refresh.return_value = {
            "access_token": "new-access-token-123",
            "refresh_token": "new-refresh-token-123",
            "token_type": "bearer"
        }
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["access_token"] == "new-access-token-123"
        assert result["refresh_token"] == "new-refresh-token-123"
    
    def test_refresh_token_endpoint_invalid_data(self):
        """Testa endpoint de refresh token com dados inválidos"""
        # Arrange
        refresh_data = {
            "refresh_token": ""
        }
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 422
    
    @patch('src.auth.service.AuthService.refresh_token')
    def test_refresh_token_endpoint_invalid_token(self, mock_refresh):
        """Testa endpoint de refresh token com token inválido"""
        # Arrange
        refresh_data = {
            "refresh_token": "invalid-refresh-token"
        }
        
        from fastapi import HTTPException
        mock_refresh.side_effect = HTTPException(status_code=401, detail="Token de refresh inválido")
        
        # Act
        response = client.post("/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 401
        assert "token de refresh inválido" in response.json()["detail"].lower() 