"""
Serviço de autenticação do MyFinance

Este módulo implementa a lógica de negócio para autenticação usando Supabase Auth,
incluindo registro, login, logout e gerenciamento de perfis de usuário.
"""

import os
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from supabase import create_client, Client
from .models import UserRegister, UserLogin, UserProfileUpdate
from .utils.password_validator import PasswordValidator
from .utils.jwt_handler import JWTHandler

class AuthService:
    """Serviço de autenticação"""
    
    def __init__(self):
        # Configurar Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_ANON_KEY devem ser configurados")
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
        self.password_validator = PasswordValidator()
        self.jwt_handler = JWTHandler()
    
    async def register_user(self, user_data: UserRegister) -> Dict[str, Any]:
        """
        Registra um novo usuário
        
        Args:
            user_data: Dados do usuário para registro
            
        Returns:
            Dados do usuário registrado
            
        Raises:
            HTTPException: Se houver erro no registro
        """
        try:
            # Validar senha
            password_validation = self.password_validator.validate(user_data.password)
            if not password_validation.is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Senha inválida: {'; '.join(password_validation.errors)}"
                )
            
            # Registrar usuário no Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })
            
            if auth_response.error:
                error_message = auth_response.error.message
                if "already registered" in error_message.lower():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Usuário já registrado com este email"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Erro no registro: {error_message}"
                    )
            
            user = auth_response.user
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar usuário"
                )
            
            # Criar perfil do usuário
            profile_data = {
                "user_id": user.id,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "timezone": "America/Sao_Paulo",
                "currency": "BRL",
                "language": "pt-BR"
            }
            
            profile_response = self.supabase.table("user_profiles").insert(profile_data).execute()
            
            if profile_response.error:
                # Se falhar ao criar perfil, deletar o usuário criado
                self.supabase.auth.admin.delete_user(user.id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao criar perfil do usuário"
                )
            
            return {
                "user_id": user.id,
                "email": user_data.email,
                "message": "Usuário registrado com sucesso"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """
        Autentica um usuário
        
        Args:
            login_data: Dados de login
            
        Returns:
            Dados da sessão do usuário
            
        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        try:
            # Fazer login no Supabase Auth
            auth_response = self.supabase.auth.sign_in_with_password({
                "email": login_data.email,
                "password": login_data.password
            })
            
            if auth_response.error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email ou senha inválidos"
                )
            
            session = auth_response.session
            user = auth_response.user
            
            if not session or not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Erro na autenticação"
                )
            
            # Buscar perfil do usuário
            profile_response = self.supabase.table("user_profiles").select("*").eq("user_id", user.id).execute()
            
            profile = None
            if profile_response.data:
                profile = profile_response.data[0]
            
            return {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "token_type": "bearer",
                "expires_in": session.expires_in,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "profile": profile
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def get_current_user(self, token: str) -> Dict[str, Any]:
        """
        Obtém o usuário atual baseado no token
        
        Args:
            token: Token de autenticação
            
        Returns:
            Dados do usuário atual
            
        Raises:
            HTTPException: Se o token for inválido
        """
        try:
            # Verificar token no Supabase
            user_response = self.supabase.auth.get_user(token)
            
            if user_response.error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )
            
            user = user_response.user
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuário não encontrado"
                )
            
            # Buscar perfil do usuário
            profile_response = self.supabase.table("user_profiles").select("*").eq("user_id", user.id).execute()
            
            profile = None
            if profile_response.data:
                profile = profile_response.data[0]
            
            return {
                "id": user.id,
                "email": user.email,
                "profile": profile
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def logout_user(self) -> Dict[str, str]:
        """
        Desconecta o usuário atual
        
        Returns:
            Mensagem de confirmação
        """
        try:
            # Fazer logout no Supabase
            self.supabase.auth.sign_out()
            
            return {"message": "Logout realizado com sucesso"}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao fazer logout: {str(e)}"
            )
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém o perfil de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dados do perfil do usuário
            
        Raises:
            HTTPException: Se o perfil não for encontrado
        """
        try:
            profile_response = self.supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
            
            if not profile_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil de usuário não encontrado"
                )
            
            return profile_response.data[0]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def update_user_profile(self, user_id: str, profile_data: UserProfileUpdate) -> Dict[str, Any]:
        """
        Atualiza o perfil de um usuário
        
        Args:
            user_id: ID do usuário
            profile_data: Dados para atualização
            
        Returns:
            Dados do perfil atualizado
            
        Raises:
            HTTPException: Se houver erro na atualização
        """
        try:
            # Filtrar apenas campos não nulos
            update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
            
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nenhum dado fornecido para atualização"
                )
            
            # Atualizar perfil
            profile_response = self.supabase.table("user_profiles").update(update_data).eq("user_id", user_id).execute()
            
            if profile_response.error:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao atualizar perfil"
                )
            
            if not profile_response.data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil de usuário não encontrado"
                )
            
            return profile_response.data[0]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Renova um token de acesso usando refresh token
        
        Args:
            refresh_token: Token de refresh
            
        Returns:
            Novo par de tokens
            
        Raises:
            HTTPException: Se o refresh token for inválido
        """
        try:
            # Renovar token no Supabase
            auth_response = self.supabase.auth.refresh_session(refresh_token)
            
            if auth_response.error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token de refresh inválido"
                )
            
            session = auth_response.session
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Erro ao renovar token"
                )
            
            return {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "token_type": "bearer",
                "expires_in": session.expires_in
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def change_password(self, user_id: str, current_password: str, new_password: str) -> Dict[str, str]:
        """
        Altera a senha do usuário
        
        Args:
            user_id: ID do usuário
            current_password: Senha atual
            new_password: Nova senha
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro na alteração
        """
        try:
            # Validar nova senha
            password_validation = self.password_validator.validate(new_password)
            if not password_validation.is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Nova senha inválida: {'; '.join(password_validation.errors)}"
                )
            
            # Alterar senha no Supabase
            auth_response = self.supabase.auth.update_user({
                "password": new_password
            })
            
            if auth_response.error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro ao alterar senha: {auth_response.error.message}"
                )
            
            return {"message": "Senha alterada com sucesso"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def delete_user(self, user_id: str) -> Dict[str, str]:
        """
        Deleta um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro na deleção
        """
        try:
            # Deletar usuário no Supabase (requer admin)
            # Em produção, isso deve ser feito com permissões adequadas
            auth_response = self.supabase.auth.admin.delete_user(user_id)
            
            if auth_response.error:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro ao deletar usuário: {auth_response.error.message}"
                )
            
            return {"message": "Usuário deletado com sucesso"}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            ) 