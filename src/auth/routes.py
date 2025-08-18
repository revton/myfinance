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
    ResetPasswordRequest,
    RefreshTokenRequest,
    User # Import the User model
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
async def register_user(user_data: UserRegister, auth_service: AuthService = Depends(get_auth_service)):
    """
    Registra um novo usuário
    """
    try:
        user = await auth_service.register_user(user_data)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.post("/login")
async def login_user(user_data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    """
    Autentica um usuário
    """
    return await auth_service.login_user(user_data)

@router.post("/forgot-password")
async def forgot_password(request_data: ForgotPasswordRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Solicita recuperação de senha
    """
    return await auth_service.forgot_password(request_data)

@router.post("/reset-password")
async def reset_password(request_data: ResetPasswordRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Redefine a senha do usuário
    """
    return await auth_service.reset_password(request_data)

@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user), auth_service: AuthService = Depends(get_auth_service)):
    """
    Realiza logout do usuário
    """
    return await auth_service.logout_user(current_user.id)

@router.post("/refresh")
async def refresh_token(request_data: RefreshTokenRequest, auth_service: AuthService = Depends(get_auth_service)):
    """
    Atualiza o token de acesso usando refresh token
    """
    return await auth_service.refresh_token(request_data)

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user), auth_service: AuthService = Depends(get_auth_service)):
    """
    Obtém informações do usuário atual
    """
    profile = await auth_service.get_user_profile(current_user.id)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "profile": profile
    }

@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user), auth_service: AuthService = Depends(get_auth_service)):
    """
    Obtém o perfil do usuário atual
    """
    return await auth_service.get_user_profile(current_user.id)

@router.put("/profile")
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Atualiza o perfil do usuário atual
    """
    return await auth_service.update_user_profile(current_user.id, profile_data)

@router.delete("/profile")
async def delete_user_profile(current_user: User = Depends(get_current_user), auth_service: AuthService = Depends(get_auth_service)):
    """
    Deleta o perfil do usuário atual
    """
    return await auth_service.delete_user(current_user.id)
 