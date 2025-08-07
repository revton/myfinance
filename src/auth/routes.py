"""
Rotas de autenticação para a API

Este módulo implementa os endpoints de autenticação incluindo registro,
login, logout, gerenciamento de perfis e refresh de tokens.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, Any

from .models import (
    UserRegister,
    UserLogin,
    UserProfileUpdate,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from .service import AuthService
from .dependencies import (
    get_current_user,
    get_current_user_id,
    get_auth_service
)

# Configurar router
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    """
    Registra um novo usuário
    """
    auth_service = AuthService()
    return await auth_service.register_user(user_data)

@router.post("/login")
async def login_user(user_data: UserLogin):
    """
    Autentica um usuário
    """
    auth_service = AuthService()
    return await auth_service.login_user(user_data)

@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest):
    """
    Solicita recuperação de senha
    """
    auth_service = AuthService()
    return await auth_service.forgot_password(request_data)

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest):
    """
    Redefine a senha do usuário
    """
    auth_service = AuthService()
    return await auth_service.reset_password(request_data)

@router.post("/logout")
async def logout_user(current_user: dict = Depends(get_current_user)):
    """
    Realiza logout do usuário
    """
    auth_service = AuthService()
    return await auth_service.logout_user(current_user["user_id"])

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Obtém informações do usuário atual
    """
    auth_service = AuthService()
    profile = await auth_service.get_user_profile(current_user["user_id"])
    
    return {
        "id": current_user["user_id"],
        "email": current_user.get("email"),
        "profile": profile
    }

@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Obtém o perfil do usuário atual
    """
    auth_service = AuthService()
    return await auth_service.get_user_profile(current_user["user_id"])

@router.put("/profile")
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza o perfil do usuário atual
    """
    auth_service = AuthService()
    return await auth_service.update_user_profile(current_user["user_id"], profile_data)

@router.delete("/profile")
async def delete_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Deleta o perfil do usuário atual
    """
    auth_service = AuthService()
    return await auth_service.delete_user(current_user["user_id"]) 