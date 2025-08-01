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
    RefreshTokenRequest,
    UserResponse,
    Token
)
from .service import AuthService
from .dependencies import (
    get_current_user,
    get_current_user_id,
    get_auth_service
)

# Configurar router
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Registra um novo usuário
    
    Args:
        user_data: Dados do usuário para registro
        auth_service: Serviço de autenticação
        
    Returns:
        Dados do usuário registrado
    """
    try:
        result = await auth_service.register_user(user_data)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.post("/login", response_model=Dict[str, Any])
async def login(
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Autentica um usuário
    
    Args:
        login_data: Dados de login
        auth_service: Serviço de autenticação
        
    Returns:
        Dados da sessão do usuário
    """
    try:
        result = await auth_service.login_user(login_data)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.post("/logout", response_model=Dict[str, str])
async def logout(
    current_user: Dict[str, Any] = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Desconecta o usuário atual
    
    Args:
        current_user: Usuário atual
        auth_service: Serviço de autenticação
        
    Returns:
        Mensagem de confirmação
    """
    try:
        result = await auth_service.logout_user()
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtém informações do usuário atual
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Informações do usuário atual
    """
    return current_user

@router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Obtém o perfil do usuário atual
    
    Args:
        current_user: Usuário atual
        auth_service: Serviço de autenticação
        
    Returns:
        Perfil do usuário
    """
    try:
        user_id = current_user["id"]
        profile = await auth_service.get_user_profile(user_id)
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.put("/profile", response_model=Dict[str, Any])
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Atualiza o perfil do usuário atual
    
    Args:
        profile_data: Dados para atualização do perfil
        current_user: Usuário atual
        auth_service: Serviço de autenticação
        
    Returns:
        Perfil atualizado
    """
    try:
        user_id = current_user["id"]
        updated_profile = await auth_service.update_user_profile(user_id, profile_data)
        return updated_profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Renova um token de acesso usando refresh token
    
    Args:
        refresh_data: Dados do refresh token
        auth_service: Serviço de autenticação
        
    Returns:
        Novo par de tokens
    """
    try:
        result = await auth_service.refresh_token(refresh_data.refresh_token)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    current_password: str,
    new_password: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Altera a senha do usuário atual
    
    Args:
        current_password: Senha atual
        new_password: Nova senha
        current_user: Usuário atual
        auth_service: Serviço de autenticação
        
    Returns:
        Mensagem de confirmação
    """
    try:
        user_id = current_user["id"]
        result = await auth_service.change_password(user_id, current_password, new_password)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.delete("/account", response_model=Dict[str, str])
async def delete_account(
    current_user: Dict[str, Any] = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Deleta a conta do usuário atual
    
    Args:
        current_user: Usuário atual
        auth_service: Serviço de autenticação
        
    Returns:
        Mensagem de confirmação
    """
    try:
        user_id = current_user["id"]
        result = await auth_service.delete_user(user_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, str])
async def auth_health_check():
    """
    Verificação de saúde do sistema de autenticação
    
    Returns:
        Status do sistema de autenticação
    """
    return {"status": "healthy", "message": "Sistema de autenticação funcionando"}

# Endpoints adicionais para funcionalidades específicas

@router.post("/validate-password")
async def validate_password(password: str):
    """
    Valida uma senha sem registrar usuário
    
    Args:
        password: Senha a ser validada
        
    Returns:
        Resultado da validação
    """
    from .utils.password_validator import PasswordValidator
    
    validator = PasswordValidator()
    result = validator.validate(password)
    
    return {
        "is_valid": result.is_valid,
        "score": result.score,
        "strength": validator.get_strength_description(result.score),
        "errors": result.errors,
        "suggestions": validator.suggest_improvements(password)
    }

@router.get("/session-info")
async def get_session_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtém informações da sessão atual
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Informações da sessão
    """
    return {
        "user_id": current_user["id"],
        "email": current_user["email"],
        "authenticated": True,
        "profile_exists": current_user.get("profile") is not None
    } 