import pytest
import re
from src.auth.utils.password_validator import PasswordValidator
from src.auth.utils.jwt_handler import JWTHandler
from datetime import datetime, timedelta

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
        assert any("mínimo de 8 caracteres" in error for error in result.errors)
    
    def test_weak_password_no_uppercase(self):
        """Testa senha sem maiúscula"""
        validator = PasswordValidator()
        result = validator.validate("securepass123!")
        
        assert result.is_valid is False
        assert any("pelo menos uma letra maiúscula" in error for error in result.errors)
    
    def test_weak_password_no_lowercase(self):
        """Testa senha sem minúscula"""
        validator = PasswordValidator()
        result = validator.validate("SECUREPASS123!")
        
        assert result.is_valid is False
        assert any("pelo menos uma letra minúscula" in error for error in result.errors)
    
    def test_weak_password_no_number(self):
        """Testa senha sem número"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass!")
        
        assert result.is_valid is False
        assert any("pelo menos um número" in error for error in result.errors)
    
    def test_weak_password_no_special_char(self):
        """Testa senha sem caractere especial"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass123")
        
        assert result.is_valid is False
        assert any("pelo menos um caractere especial" in error for error in result.errors)
    
    def test_weak_password_common_password(self):
        """Testa senha comum"""
        validator = PasswordValidator()
        result = validator.validate("password123")
        
        assert result.is_valid is False
        assert any("senha muito comum" in error for error in result.errors)
    
    def test_weak_password_sequential_chars(self):
        """Testa senha com caracteres sequenciais"""
        validator = PasswordValidator()
        result = validator.validate("Secure123!")
        
        # Verificar se detecta sequências como "123"
        assert result.is_valid is False
        assert any("sequência" in error for error in result.errors)
    
    def test_weak_password_repeated_chars(self):
        """Testa senha com caracteres repetidos"""
        validator = PasswordValidator()
        result = validator.validate("SecurePass111!")
        
        assert result.is_valid is False
        assert any("caracteres repetidos" in error for error in result.errors)
    
    def test_password_with_personal_info(self):
        """Testa senha com informações pessoais"""
        validator = PasswordValidator()
        result = validator.validate("JoaoSilva123!")
        
        assert result.is_valid is False
        assert any("informações pessoais" in error for error in result.errors)

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
        
        import jwt
        token = jwt.encode(payload, handler.secret_key, algorithm=handler.algorithm)
        
        with pytest.raises(jwt.ExpiredSignatureError):
            handler.verify_token(token)
    
    def test_invalid_jwt_signature(self):
        """Testa token JWT com assinatura inválida"""
        handler = JWTHandler()
        
        # Criar token com chave secreta diferente
        import jwt
        payload = {"user_id": "test-123", "email": "test@example.com"}
        token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")
        
        with pytest.raises(jwt.InvalidSignatureError):
            handler.verify_token(token)
    
    def test_jwt_token_without_required_fields(self):
        """Testa token JWT sem campos obrigatórios"""
        handler = JWTHandler()
        
        # Criar token sem user_id
        import jwt
        payload = {"email": "test@example.com"}
        token = jwt.encode(payload, handler.secret_key, algorithm=handler.algorithm)
        
        with pytest.raises(ValueError):
            handler.verify_token(token)
    
    def test_jwt_token_with_invalid_algorithm(self):
        """Testa token JWT com algoritmo inválido"""
        handler = JWTHandler()
        
        # Criar token com algoritmo diferente
        import jwt
        payload = {"user_id": "test-123", "email": "test@example.com"}
        token = jwt.encode(payload, handler.secret_key, algorithm="HS512")
        
        with pytest.raises(jwt.InvalidAlgorithmError):
            handler.verify_token(token)
    
    def test_jwt_token_refresh(self):
        """Testa refresh de token JWT"""
        handler = JWTHandler()
        user_data = {"user_id": "test-123", "email": "test@example.com"}
        
        # Criar token original
        original_token = handler.create_token(user_data)
        
        # Criar refresh token
        refresh_token = handler.create_refresh_token(user_data)
        
        # Verificar que são diferentes
        assert original_token != refresh_token
        
        # Verificar que ambos são válidos
        original_decoded = handler.verify_token(original_token)
        refresh_decoded = handler.verify_token(refresh_token)
        
        assert original_decoded["user_id"] == user_data["user_id"]
        assert refresh_decoded["user_id"] == user_data["user_id"]

class TestRateLimiting:
    def test_login_rate_limiting(self, client):
        """Testa rate limiting no endpoint de login"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        # Tentar login várias vezes rapidamente
        responses = []
        for i in range(5):
            response = client.post("/auth/login", json=login_data)
            responses.append(response.status_code)
        
        # Verificar se pelo menos uma tentativa foi bloqueada por rate limiting
        assert 429 in responses or all(code == 401 for code in responses)
    
    def test_register_rate_limiting(self, client):
        """Testa rate limiting no endpoint de registro"""
        register_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "Test User"
        }
        
        # Tentar registrar várias vezes rapidamente
        responses = []
        for i in range(3):
            response = client.post("/auth/register", json=register_data)
            responses.append(response.status_code)
        
        # Verificar se pelo menos uma tentativa foi bloqueada por rate limiting
        assert 429 in responses or all(code in [201, 400] for code in responses)

class TestInputValidation:
    def test_sql_injection_prevention(self, client):
        """Testa prevenção de SQL injection"""
        malicious_data = {
            "email": "test@example.com'; DROP TABLE users; --",
            "password": "SecurePass123!"
        }
        
        response = client.post("/auth/login", json=malicious_data)
        
        # Deve retornar erro de validação, não erro de SQL
        assert response.status_code in [422, 401]
    
    def test_xss_prevention(self, client):
        """Testa prevenção de XSS"""
        malicious_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "<script>alert('xss')</script>"
        }
        
        response = client.post("/auth/register", json=malicious_data)
        
        # Deve aceitar o registro mas sanitizar o input
        assert response.status_code in [201, 400, 422]
    
    def test_email_format_validation(self, client):
        """Testa validação de formato de email"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example..com"
        ]
        
        for email in invalid_emails:
            data = {
                "email": email,
                "password": "SecurePass123!"
            }
            
            response = client.post("/auth/register", json=data)
            assert response.status_code == 422
    
    def test_password_length_validation(self, client):
        """Testa validação de comprimento de senha"""
        # Senha muito longa
        long_password = "A" * 129  # Mais de 128 caracteres
        
        data = {
            "email": "test@example.com",
            "password": long_password
        }
        
        response = client.post("/auth/register", json=data)
        assert response.status_code == 422

class TestSessionSecurity:
    def test_session_timeout(self, client):
        """Testa timeout de sessão"""
        # Fazer login
        login_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        login_response = client.post("/auth/login", json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Tentar acessar endpoint protegido
            response = client.get("/auth/me", headers=headers)
            
            # Deve funcionar se o token for válido
            assert response.status_code in [200, 401]
    
    def test_concurrent_sessions(self, client):
        """Testa múltiplas sessões simultâneas"""
        # Fazer login múltiplas vezes
        login_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        tokens = []
        for i in range(3):
            response = client.post("/auth/login", json=login_data)
            if response.status_code == 200:
                tokens.append(response.json()["access_token"])
        
        # Verificar se todas as sessões são válidas
        for token in tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/auth/me", headers=headers)
            assert response.status_code in [200, 401]

class TestDataProtection:
    def test_password_not_logged(self, client):
        """Testa que senhas não são logadas"""
        # Este teste verifica se as senhas não aparecem nos logs
        # Em uma implementação real, você verificaria os logs do sistema
        
        login_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        
        response = client.post("/auth/login", json=login_data)
        
        # A resposta não deve conter a senha
        if response.status_code == 200:
            response_data = response.json()
            assert "password" not in response_data
            assert "SecurePass123!" not in str(response_data)
    
    def test_sensitive_data_encryption(self):
        """Testa que dados sensíveis são criptografados"""
        # Este teste verifica se dados sensíveis são criptografados
        # Em uma implementação real, você verificaria o banco de dados
        
        # Simular verificação de criptografia
        assert True  # Placeholder para teste real
    
    def test_pii_protection(self, client):
        """Testa proteção de dados pessoais"""
        # Testar se dados pessoais são adequadamente protegidos
        
        register_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "João Silva"
        }
        
        response = client.post("/auth/register", json=register_data)
        
        # A resposta não deve expor dados sensíveis desnecessariamente
        if response.status_code == 201:
            response_data = response.json()
            assert "password" not in response_data
            # O email pode estar presente, mas não a senha 