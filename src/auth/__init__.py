"""
Módulo de autenticação do MyFinance

Este módulo implementa o sistema de autenticação seguro usando Supabase Auth,
incluindo registro, login, logout e gerenciamento de perfis de usuário.
"""

from .models import (
    UserRegister,
    UserLogin,
    UserProfile,
    UserProfileUpdate,
    Token,
    UserResponse
)
from .service import AuthService
from .dependencies import get_current_user
from .routes import router as auth_router

__all__ = [
    "UserRegister",
    "UserLogin", 
    "UserProfile",
    "UserProfileUpdate",
    "Token",
    "UserResponse",
    "AuthService",
    "get_current_user",
    "auth_router"
] 