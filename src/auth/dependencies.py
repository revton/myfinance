"""
Dependências de autenticação para FastAPI

Este módulo implementa as dependências necessárias para autenticação
e autorização nas rotas da API.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .service import AuthService

# Configurar HTTPBearer para autenticação
security = HTTPBearer()

# Função para obter instância do serviço de autenticação (lazy loading)
def get_auth_service_instance() -> AuthService:
    """Retorna uma instância do AuthService"""
    return AuthService()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependência para obter o usuário atual baseado no token
    
    Args:
        credentials: Credenciais de autorização
        
    Returns:
        Dados do usuário atual
        
    Raises:
        HTTPException: Se o token for inválido
    """
    try:
        token = credentials.credentials
        auth_service = get_auth_service_instance()
        user = await auth_service.get_current_user(token)
        return user
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[dict]:
    """
    Dependência opcional para obter o usuário atual
    
    Args:
        credentials: Credenciais de autorização (opcional)
        
    Returns:
        Dados do usuário atual ou None se não autenticado
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        auth_service = get_auth_service_instance()
        user = await auth_service.get_current_user(token)
        return user
    except HTTPException:
        return None

async def get_current_user_id(
    current_user: dict = Depends(get_current_user)
) -> str:
    """
    Dependência para obter apenas o ID do usuário atual
    
    Args:
        current_user: Usuário atual
        
    Returns:
        ID do usuário atual
    """
    return current_user["id"]

async def get_current_user_email(
    current_user: dict = Depends(get_current_user)
) -> str:
    """
    Dependência para obter apenas o email do usuário atual
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Email do usuário atual
    """
    return current_user["email"]

async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
) -> Optional[dict]:
    """
    Dependência para obter o perfil do usuário atual
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Perfil do usuário atual ou None se não existir
    """
    return current_user.get("profile")

async def require_authenticated_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependência que requer usuário autenticado
    
    Args:
        current_user: Usuário atual
        
    Returns:
        Dados do usuário autenticado
        
    Raises:
        HTTPException: Se o usuário não estiver autenticado
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

async def get_auth_service() -> AuthService:
    """
    Dependência para obter o serviço de autenticação
    
    Returns:
        Instância do AuthService
    """
    return auth_service

# Função para verificar se o usuário tem permissão específica
def require_permission(permission: str):
    """
    Decorator para verificar permissão específica
    
    Args:
        permission: Permissão necessária
        
    Returns:
        Função de dependência
    """
    async def check_permission(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        """
        Verifica se o usuário tem a permissão necessária
        
        Args:
            current_user: Usuário atual
            
        Returns:
            Dados do usuário se tiver permissão
            
        Raises:
            HTTPException: Se não tiver permissão
        """
        # Por enquanto, todos os usuários autenticados têm todas as permissões
        # Em uma implementação mais avançada, você verificaria as permissões
        # no perfil do usuário ou em uma tabela de permissões
        
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Aqui você implementaria a lógica de verificação de permissões
        # Por exemplo:
        # user_permissions = current_user.get("profile", {}).get("permissions", [])
        # if permission not in user_permissions:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail=f"Permissão '{permission}' necessária"
        #     )
        
        return current_user
    
    return check_permission

# Função para verificar se o usuário é o proprietário do recurso
def require_ownership(resource_user_id_field: str = "user_id"):
    """
    Decorator para verificar se o usuário é o proprietário do recurso
    
    Args:
        resource_user_id_field: Campo que contém o user_id no recurso
        
    Returns:
        Função de dependência
    """
    async def check_ownership(
        current_user: dict = Depends(get_current_user),
        resource: dict = None
    ) -> dict:
        """
        Verifica se o usuário é o proprietário do recurso
        
        Args:
            current_user: Usuário atual
            resource: Recurso a ser verificado
            
        Returns:
            Dados do usuário se for o proprietário
            
        Raises:
            HTTPException: Se não for o proprietário
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if resource and resource.get(resource_user_id_field) != current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado: você não é o proprietário deste recurso"
            )
        
        return current_user
    
    return check_ownership

# Função para verificar se o usuário é admin
def require_admin():
    """
    Decorator para verificar se o usuário é administrador
    
    Returns:
        Função de dependência
    """
    async def check_admin(
        current_user: dict = Depends(get_current_user)
    ) -> dict:
        """
        Verifica se o usuário é administrador
        
        Args:
            current_user: Usuário atual
            
        Returns:
            Dados do usuário se for admin
            
        Raises:
            HTTPException: Se não for admin
        """
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticação necessária",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar se o usuário é admin
        # Por enquanto, vamos considerar que não há admins
        # Em uma implementação real, você verificaria isso no perfil do usuário
        profile = current_user.get("profile", {})
        is_admin = profile.get("is_admin", False)
        
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado: permissão de administrador necessária"
            )
        
        return current_user
    
    return check_admin 