# 🧪 Testes e Validação - Sistema de Autenticação

## 🎯 **Visão Geral**

Este documento descreve a estratégia de testes e validação para o sistema de autenticação, incluindo testes unitários, de integração, end-to-end e validações de segurança.

## 🧪 **Estratégia de Testes**

### **Pirâmide de Testes**

```
    /\
   /  \     E2E Tests (Poucos)
  /____\    
 /      \   Integration Tests (Alguns)
/________\  Unit Tests (Muitos)
```

### **Cobertura de Testes**

- **Testes Unitários**: 90% de cobertura
- **Testes de Integração**: 80% de cobertura
- **Testes E2E**: Cenários críticos
- **Testes de Segurança**: 100% dos endpoints

## 🔧 **Testes Unitários**

### **1. Testes do AuthService**

```python
# tests/services/test_auth_service.py
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.models.auth import UserRegister, UserLogin, UserProfile

class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService()
    
    @pytest.fixture
    def mock_supabase(self):
        with patch('app.services.auth_service.supabase') as mock:
            yield mock
    
    def test_register_user_success(self, auth_service, mock_supabase):
        # Arrange
        user_data = UserRegister(
            email="test@example.com",
            password="securepassword123",
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
        # Arrange
        user_data = UserRegister(
            email="existing@example.com",
            password="securepassword123"
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
    
    def test_login_user_success(self, auth_service, mock_supabase):
        # Arrange
        login_data = UserLogin(
            email="test@example.com",
            password="securepassword123"
        )
        
        mock_supabase.auth.sign_in_with_password.return_value = {
            'data': {
                'session': {
                    'access_token': 'token-123',
                    'user': {'id': 'user-123', 'email': 'test@example.com'}
                }
            },
            'error': None
        }
        
        # Act
        result = auth_service.login_user(login_data)
        
        # Assert
        assert result['access_token'] == 'token-123'
        assert result['user']['id'] == 'user-123'
    
    def test_login_user_invalid_credentials(self, auth_service, mock_supabase):
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
```

### **2. Testes dos Modelos Pydantic**

```python
# tests/models/test_auth_models.py
import pytest
from pydantic import ValidationError
from app.models.auth import UserRegister, UserLogin, UserProfile

class TestUserRegister:
    def test_valid_user_register(self):
        # Arrange & Act
        user_data = UserRegister(
            email="test@example.com",
            password="securepassword123",
            full_name="Test User"
        )
        
        # Assert
        assert user_data.email == "test@example.com"
        assert user_data.password == "securepassword123"
        assert user_data.full_name == "Test User"
    
    def test_invalid_email_format(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                email="invalid-email",
                password="securepassword123"
            )
        
        assert "email" in str(exc_info.value)
    
    def test_password_too_short(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserRegister(
                email="test@example.com",
                password="123"
            )
        
        assert "password" in str(exc_info.value)

class TestUserProfile:
    def test_valid_user_profile(self):
        # Arrange & Act
        profile = UserProfile(
            id="profile-123",
            user_id="user-123",
            email="test@example.com",
            full_name="Test User",
            timezone="America/Sao_Paulo",
            currency="BRL",
            language="pt-BR"
        )
        
        # Assert
        assert profile.email == "test@example.com"
        assert profile.timezone == "America/Sao_Paulo"
        assert profile.currency == "BRL"
    
    def test_invalid_timezone(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserProfile(
                id="profile-123",
                user_id="user-123",
                email="test@example.com",
                timezone="Invalid/Timezone"
            )
        
        assert "timezone" in str(exc_info.value)
```

### **3. Testes dos Endpoints**

```python
# tests/api/test_auth_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

class TestAuthEndpoints:
    @patch('app.services.auth_service.AuthService.register_user')
    def test_register_endpoint_success(self, mock_register):
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
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
        # Arrange
        user_data = {
            "email": "invalid-email",
            "password": "123"
        }
        
        # Act
        response = client.post("/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 422
    
    @patch('app.services.auth_service.AuthService.login_user')
    def test_login_endpoint_success(self, mock_login):
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "securepassword123"
        }
        
        mock_login.return_value = {
            "access_token": "token-123",
            "token_type": "bearer",
            "user": {"id": "user-123", "email": "test@example.com"}
        }
        
        # Act
        response = client.post("/auth/login", json=login_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["access_token"] == "token-123"
    
    @patch('app.services.auth_service.AuthService.get_current_user')
    def test_me_endpoint_success(self, mock_get_user):
        # Arrange
        mock_get_user.return_value = {
            "id": "user-123",
            "email": "test@example.com",
            "profile": {
                "full_name": "Test User",
                "timezone": "America/Sao_Paulo"
            }
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/auth/me", headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
```

## 🔗 **Testes de Integração**

### **1. Testes de Integração com Supabase**

```python
# tests/integration/test_supabase_integration.py
import pytest
from app.services.auth_service import AuthService
from app.database import get_supabase_client

class TestSupabaseIntegration:
    @pytest.fixture
    def auth_service(self):
        return AuthService()
    
    @pytest.fixture
    def supabase_client(self):
        return get_supabase_client()
    
    def test_user_registration_flow(self, auth_service, supabase_client):
        """Testa o fluxo completo de registro de usuário"""
        # Arrange
        email = f"test_{pytest.time.time()}@example.com"
        password = "securepassword123"
        full_name = "Integration Test User"
        
        # Act
        result = auth_service.register_user({
            "email": email,
            "password": password,
            "full_name": full_name
        })
        
        # Assert
        assert result["user_id"] is not None
        assert result["email"] == email
        
        # Verificar se o perfil foi criado
        profile = supabase_client.table("user_profiles").select("*").eq("user_id", result["user_id"]).execute()
        assert len(profile.data) == 1
        assert profile.data[0]["full_name"] == full_name
    
    def test_user_login_flow(self, auth_service, supabase_client):
        """Testa o fluxo completo de login"""
        # Arrange - Criar usuário primeiro
        email = f"login_test_{pytest.time.time()}@example.com"
        password = "securepassword123"
        
        auth_service.register_user({
            "email": email,
            "password": password,
            "full_name": "Login Test User"
        })
        
        # Act
        result = auth_service.login_user({
            "email": email,
            "password": password
        })
        
        # Assert
        assert result["access_token"] is not None
        assert result["user"]["email"] == email
    
    def test_user_profile_update(self, auth_service, supabase_client):
        """Testa a atualização do perfil do usuário"""
        # Arrange - Criar usuário e fazer login
        email = f"profile_test_{pytest.time.time()}@example.com"
        password = "securepassword123"
        
        register_result = auth_service.register_user({
            "email": email,
            "password": password,
            "full_name": "Profile Test User"
        })
        
        login_result = auth_service.login_user({
            "email": email,
            "password": password
        })
        
        # Act - Atualizar perfil
        updated_profile = {
            "full_name": "Updated Name",
            "timezone": "America/New_York",
            "currency": "USD"
        }
        
        result = auth_service.update_profile(
            login_result["access_token"],
            updated_profile
        )
        
        # Assert
        assert result["full_name"] == "Updated Name"
        assert result["timezone"] == "America/New_York"
        assert result["currency"] == "USD"
```

### **2. Testes de Integração com Banco de Dados**

```python
# tests/integration/test_database_integration.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user_profile import UserProfile
from app.services.user_profile_service import UserProfileService

class TestDatabaseIntegration:
    @pytest.fixture
    def engine(self):
        # Usar banco de dados de teste
        engine = create_engine("postgresql://test:test@localhost/test_db")
        Base.metadata.create_all(bind=engine)
        yield engine
        Base.metadata.drop_all(bind=engine)
    
    @pytest.fixture
    def session(self, engine):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def profile_service(self, session):
        return UserProfileService(session)
    
    def test_create_user_profile(self, profile_service, session):
        """Testa a criação de perfil de usuário no banco"""
        # Arrange
        profile_data = {
            "user_id": "test-user-123",
            "email": "test@example.com",
            "full_name": "Test User",
            "timezone": "America/Sao_Paulo",
            "currency": "BRL"
        }
        
        # Act
        profile = profile_service.create_profile(profile_data)
        
        # Assert
        assert profile.id is not None
        assert profile.email == "test@example.com"
        assert profile.full_name == "Test User"
        
        # Verificar no banco
        db_profile = session.query(UserProfile).filter_by(user_id="test-user-123").first()
        assert db_profile is not None
        assert db_profile.email == "test@example.com"
    
    def test_update_user_profile(self, profile_service, session):
        """Testa a atualização de perfil de usuário"""
        # Arrange - Criar perfil primeiro
        profile_data = {
            "user_id": "test-user-456",
            "email": "test@example.com",
            "full_name": "Original Name"
        }
        
        profile = profile_service.create_profile(profile_data)
        
        # Act - Atualizar perfil
        updated_data = {
            "full_name": "Updated Name",
            "timezone": "America/New_York"
        }
        
        updated_profile = profile_service.update_profile(profile.id, updated_data)
        
        # Assert
        assert updated_profile.full_name == "Updated Name"
        assert updated_profile.timezone == "America/New_York"
        
        # Verificar no banco
        db_profile = session.query(UserProfile).filter_by(id=profile.id).first()
        assert db_profile.full_name == "Updated Name"
```

## 🌐 **Testes End-to-End**

### **1. Testes E2E com Playwright**

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should register new user successfully', async ({ page }) => {
    // Arrange
    const email = `test-${Date.now()}@example.com`;
    const password = 'securepassword123';
    const fullName = 'Test User';

    // Act
    await page.goto('/register');
    
    await page.fill('[data-testid="full-name-input"]', fullName);
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    await page.fill('[data-testid="confirm-password-input"]', password);
    
    await page.click('[data-testid="register-button"]');

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-name"]')).toContainText(fullName);
  });

  test('should login existing user successfully', async ({ page }) => {
    // Arrange
    const email = 'existing@example.com';
    const password = 'securepassword123';

    // Act
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-email"]')).toContainText(email);
  });

  test('should show error for invalid credentials', async ({ page }) => {
    // Arrange
    const email = 'invalid@example.com';
    const password = 'wrongpassword';

    // Act
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', email);
    await page.fill('[data-testid="password-input"]', password);
    
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page.locator('[data-testid="error-message"]')).toContainText('Email ou senha inválidos');
    await expect(page).toHaveURL('/login');
  });

  test('should logout user successfully', async ({ page }) => {
    // Arrange - Login first
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'securepassword123');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/dashboard');

    // Act
    await page.click('[data-testid="user-menu-button"]');
    await page.click('[data-testid="logout-button"]');

    // Assert
    await expect(page).toHaveURL('/login');
  });
});
```

### **2. Testes de API E2E**

```python
# tests/e2e/test_auth_api_e2e.py
import pytest
import requests
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestAuthAPIE2E:
    def test_complete_auth_flow(self):
        """Testa o fluxo completo de autenticação via API"""
        # 1. Registrar usuário
        register_data = {
            "email": f"e2e_test_{pytest.time.time()}@example.com",
            "password": "securepassword123",
            "full_name": "E2E Test User"
        }
        
        register_response = client.post("/auth/register", json=register_data)
        assert register_response.status_code == 201
        
        user_id = register_response.json()["user_id"]
        assert user_id is not None
        
        # 2. Fazer login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        
        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        assert token is not None
        
        # 3. Acessar perfil do usuário
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        
        user_data = me_response.json()
        assert user_data["email"] == register_data["email"]
        assert user_data["profile"]["full_name"] == register_data["full_name"]
        
        # 4. Atualizar perfil
        update_data = {
            "full_name": "Updated E2E User",
            "timezone": "America/New_York",
            "currency": "USD"
        }
        
        update_response = client.put("/auth/profile", json=update_data, headers=headers)
        assert update_response.status_code == 200
        
        updated_profile = update_response.json()
        assert updated_profile["full_name"] == "Updated E2E User"
        assert updated_profile["timezone"] == "America/New_York"
        
        # 5. Fazer logout
        logout_response = client.post("/auth/logout", headers=headers)
        assert logout_response.status_code == 200
        
        # 6. Verificar que o token não funciona mais
        me_response_after_logout = client.get("/auth/me", headers=headers)
        assert me_response_after_logout.status_code == 401
```

## 🔒 **Testes de Segurança**

### **1. Testes de Validação de Senha**

```python
# tests/security/test_password_validation.py
import pytest
from app.utils.password_validator import PasswordValidator

class TestPasswordValidation:
    def test_strong_password(self):
        """Testa senha forte"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass123!")
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_weak_password_too_short(self):
        """Testa senha muito curta"""
        validator = PasswordValidator()
        result = validator.validate("123")
        
        assert result.is_valid is False
        assert "mínimo de 8 caracteres" in result.errors[0]
    
    def test_weak_password_no_uppercase(self):
        """Testa senha sem maiúscula"""
        validator = PasswordValidator()
        result = validator.validate("securepass123!")
        
        assert result.is_valid is False
        assert "pelo menos uma letra maiúscula" in result.errors[0]
    
    def test_weak_password_no_number(self):
        """Testa senha sem número"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass!")
        
        assert result.is_valid is False
        assert "pelo menos um número" in result.errors[0]
    
    def test_weak_password_no_special_char(self):
        """Testa senha sem caractere especial"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass123")
        
        assert result.is_valid is False
        assert "pelo menos um caractere especial" in result.errors[0]
```

### **2. Testes de Rate Limiting**

```python
# tests/security/test_rate_limiting.py
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRateLimiting:
    def test_login_rate_limiting(self):
        """Testa rate limiting no endpoint de login"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        # Tentar login várias vezes rapidamente
        for i in range(5):
            response = client.post("/auth/login", json=login_data)
            assert response.status_code in [401, 429]  # 401 = credenciais inválidas, 429 = rate limit
        
        # Verificar se o rate limiting foi aplicado
        response = client.post("/auth/login", json=login_data)
        assert response.status_code == 429
        assert "rate limit" in response.json()["detail"].lower()
    
    def test_register_rate_limiting(self):
        """Testa rate limiting no endpoint de registro"""
        register_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "full_name": "Test User"
        }
        
        # Tentar registrar várias vezes rapidamente
        for i in range(3):
            response = client.post("/auth/register", json=register_data)
            # Primeira tentativa pode ser 201, as outras 400 (email já existe) ou 429 (rate limit)
        
        # Verificar se o rate limiting foi aplicado
        response = client.post("/auth/register", json=register_data)
        assert response.status_code == 429
```

### **3. Testes de JWT**

```python
# tests/security/test_jwt_security.py
import pytest
import jwt
from datetime import datetime, timedelta
from app.utils.jwt_handler import JWTHandler

class TestJWTSecurity:
    def test_valid_jwt_token(self):
        """Testa token JWT válido"""
        handler = JWTHandler()
        user_data = {"user_id": "test-123", "email": "test@example.com"}
        
        token = handler.create_token(user_data)
        decoded = handler.verify_token(token)
        
        assert decoded["user_id"] == "test-123"
        assert decoded["email"] == "test@example.com"
    
    def test_expired_jwt_token(self):
        """Testa token JWT expirado"""
        handler = JWTHandler()
        user_data = {"user_id": "test-123", "email": "test@example.com"}
        
        # Criar token com expiração no passado
        payload = {
            **user_data,
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        
        token = jwt.encode(payload, handler.secret_key, algorithm=handler.algorithm)
        
        with pytest.raises(jwt.ExpiredSignatureError):
            handler.verify_token(token)
    
    def test_invalid_jwt_signature(self):
        """Testa token JWT com assinatura inválida"""
        handler = JWTHandler()
        
        # Criar token com chave secreta diferente
        payload = {"user_id": "test-123", "email": "test@example.com"}
        token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")
        
        with pytest.raises(jwt.InvalidSignatureError):
            handler.verify_token(token)
```

## 📊 **Métricas de Qualidade**

### **1. Cobertura de Código**

```bash
# Executar testes com cobertura
pytest --cov=app --cov-report=html --cov-report=term-missing

# Resultado esperado:
# Name                           Stmts   Miss  Cover   Missing
# -------------------------------------------------------------
# app/services/auth_service.py     45      2    96%   45-46
# app/models/auth.py               32      0   100%
# app/api/auth.py                  28      1    96%   67
# -------------------------------------------------------------
# TOTAL                          105      3    97%
```

### **2. Métricas de Performance**

```python
# tests/performance/test_auth_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAuthPerformance:
    def test_login_response_time(self):
        """Testa tempo de resposta do login"""
        login_data = {
            "email": "test@example.com",
            "password": "securepassword123"
        }
        
        start_time = time.time()
        response = client.post("/auth/login", json=login_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code in [200, 401]  # 200 = sucesso, 401 = credenciais inválidas
        assert response_time < 1.0  # Deve responder em menos de 1 segundo
    
    def test_register_response_time(self):
        """Testa tempo de resposta do registro"""
        register_data = {
            "email": f"perf_test_{time.time()}@example.com",
            "password": "securepassword123",
            "full_name": "Performance Test User"
        }
        
        start_time = time.time()
        response = client.post("/auth/register", json=register_data)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code in [201, 400]  # 201 = criado, 400 = erro de validação
        assert response_time < 2.0  # Deve responder em menos de 2 segundos
```

## 🚀 **Automação de Testes**

### **1. GitHub Actions para Testes**

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ --cov=app --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ --cov=app --cov-report=xml
    
    - name: Run security tests
      run: |
        pytest tests/security/ --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### **2. Scripts de Teste**

```bash
#!/bin/bash
# scripts/run-tests.sh

echo "🧪 Executando testes do sistema de autenticação..."

# Executar testes unitários
echo "📦 Testes Unitários..."
pytest tests/unit/ -v --tb=short

# Executar testes de integração
echo "🔗 Testes de Integração..."
pytest tests/integration/ -v --tb=short

# Executar testes de segurança
echo "🔒 Testes de Segurança..."
pytest tests/security/ -v --tb=short

# Executar testes de performance
echo "⚡ Testes de Performance..."
pytest tests/performance/ -v --tb=short

# Gerar relatório de cobertura
echo "📊 Gerando relatório de cobertura..."
pytest --cov=app --cov-report=html --cov-report=term-missing

echo "✅ Todos os testes concluídos!"
```

Esta estratégia de testes garante que o sistema de autenticação seja robusto, seguro e confiável, com cobertura abrangente de todos os cenários críticos. 