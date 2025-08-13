"""
Modelos Pydantic para o sistema de autenticação

Este módulo define os modelos de dados para registro, login, perfis de usuário
e respostas da API de autenticação.
"""

from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
import pytz

class UserRegister(BaseModel):
    """Modelo para registro de usuário"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Valida a força da senha"""
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        if len(v) > 128:
            raise ValueError('A senha deve ter no máximo 128 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('A senha deve conter pelo menos um número')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('A senha deve conter pelo menos um caractere especial')
        return v

class UserLogin(BaseModel):
    """Modelo para login de usuário"""
    email: EmailStr
    password: str

class UserProfileBase(BaseModel):
    """Modelo base para perfil de usuário"""
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    timezone: str = "America/Sao_Paulo"
    currency: str = "BRL"
    language: str = "pt-BR"
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v):
        """Valida se a timezone é válida"""
        if v not in pytz.all_timezones:
            raise ValueError('Timezone inválida')
        return v
    
    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        """Valida se a moeda é suportada"""
        valid_currencies = ['BRL', 'USD', 'EUR', 'GBP']
        if v not in valid_currencies:
            raise ValueError('Moeda inválida')
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        """Valida se o idioma é suportado"""
        valid_languages = ['pt-BR', 'en-US', 'es-ES']
        if v not in valid_languages:
            raise ValueError('Idioma inválido')
        return v

class UserProfileCreate(UserProfileBase):
    """Modelo para criação de perfil de usuário"""
    pass

class UserProfileUpdate(BaseModel):
    """Modelo para atualização de perfil de usuário"""
    full_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v):
        """Valida se a timezone é válida"""
        if v is not None and v not in pytz.all_timezones:
            raise ValueError('Timezone inválida')
        return v
    
    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        """Valida se a moeda é suportada"""
        if v is not None:
            valid_currencies = ['BRL', 'USD', 'EUR', 'GBP']
            if v not in valid_currencies:
                raise ValueError('Moeda inválida')
        return v
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v):
        """Valida se o idioma é suportado"""
        if v is not None:
            valid_languages = ['pt-BR', 'en-US', 'es-ES']
            if v not in valid_languages:
                raise ValueError('Idioma inválido')
        return v

class UserProfile(UserProfileBase):
    """Modelo completo de perfil de usuário"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class Token(BaseModel):
    """Modelo para token de autenticação"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    """Modelo para resposta de usuário"""
    id: UUID
    email: EmailStr
    profile: Optional[UserProfile] = None

class RefreshTokenRequest(BaseModel):
    """Modelo para requisição de refresh token"""
    refresh_token: str
    
    @field_validator('refresh_token')
    @classmethod
    def validate_refresh_token(cls, v):
        """Valida se o refresh token não está vazio"""
        if not v or not v.strip():
            raise ValueError('Refresh token não pode estar vazio')
        return v.strip() 

class ForgotPasswordRequest(BaseModel):
    """Modelo para solicitação de recuperação de senha"""
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    """Modelo para redefinição de senha"""
    email: EmailStr
    new_password: str
    token: str
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Valida a força da senha"""
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        if len(v) > 128:
            raise ValueError('A senha deve ter no máximo 128 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('A senha deve conter pelo menos um número')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('A senha deve conter pelo menos um caractere especial')
        return v 

class User(BaseModel):
    id: UUID
    email: EmailStr
