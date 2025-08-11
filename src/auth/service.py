"""
Serviço de autenticação do MyFinance

Este módulo implementa a lógica de negócio para autenticação usando Supabase Auth,
incluindo registro, login, logout e gerenciamento de perfis de usuário.
"""

import os
import uuid
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from supabase import create_client, Client
from .models import UserRegister, UserLogin, UserProfileUpdate, ForgotPasswordRequest, ResetPasswordRequest, RefreshTokenRequest
from .utils.password_validator import PasswordValidator
from .utils.jwt_handler import JWTHandler
from src.database import UserProfile
from src.database_sqlalchemy import SessionLocal
from datetime import datetime

class AuthService:
    def __init__(self):
        """
        Inicializa o serviço de autenticação
        """
        # Configurar Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("Configuração do Supabase não encontrada")
        
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
                    detail=f"Senha não atende aos requisitos de segurança: {'; '.join(password_validation.errors)}"
                )
            
            # Registrar usuário no Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "emailRedirectTo": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/auth/confirm",
                    "data": {
                        "full_name": user_data.full_name
                    }
                }
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao registrar usuário no Supabase"
                )
            
            user_id = auth_response.user.id
            
            # Hash da senha para nosso banco
            from .utils.password_validator import hash_password
            hashed_password = hash_password(user_data.password)
            
            # Criar perfil do usuário
            try:
                db = SessionLocal()
                profile = UserProfile(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    email=user_data.email,
                    full_name=user_data.full_name,
                    password_hash=hashed_password,  # Salvar hash da senha
                    avatar_url=None,
                    timezone="America/Sao_Paulo",
                    currency="BRL",
                    language="pt-BR"
                )
                
                db.add(profile)
                db.commit()
                db.refresh(profile)
                db.close()
                
                # Enviar email informativo (sem confirmação)
                try:
                    await self._send_welcome_email(user_data.email, user_data.full_name)
                except Exception as email_error:
                    print(f"Erro ao enviar email de boas-vindas: {email_error}")
                    # Não falhar o registro se o email falhar
                    
            except Exception as profile_error:
                # Se falhar ao criar perfil, deletar o usuário criado
                try:
                    self.supabase.auth.admin.delete_user(user_id)
                except:
                    pass
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Erro ao criar perfil do usuário: {str(profile_error)}"
                )
            
            return {
                "user_id": user_id,
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
    
    async def _send_welcome_email(self, email: str, full_name: str) -> None:
        """
        Envia email de boas-vindas após registro
        
        Args:
            email: Email do usuário
            full_name: Nome completo do usuário
        """
        try:
            import httpx
            
            resend_api_key = os.getenv("RESEND_API_KEY")
            if not resend_api_key:
                print("RESEND_API_KEY não configurada")
                return
            
            # URL da aplicação
            app_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
            
            # Template do email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Bem-vindo ao MyFinance</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Bem-vindo ao MyFinance!</h1>
                    </div>
                    <div class="content">
                        <h2>Olá, {full_name}!</h2>
                        <p>Seu cadastro foi realizado com sucesso no MyFinance.</p>
                        <p>Você já pode acessar sua conta e começar a gerenciar suas finanças!</p>
                        
                        <div style="text-align: center;">
                            <a href="{app_url}" class="button">Acessar MyFinance</a>
                        </div>
                        
                        <p><strong>Dicas para começar:</strong></p>
                        <ul>
                            <li>Configure suas categorias de gastos</li>
                            <li>Adicione suas primeiras transações</li>
                            <li>Visualize seus relatórios financeiros</li>
                        </ul>
                        
                        <p>Se você tiver alguma dúvida, não hesite em entrar em contato conosco.</p>
                        
                        <p>Atenciosamente,<br>Equipe MyFinance</p>
                    </div>
                    <div class="footer">
                        <p>Este é um email automático, não responda a esta mensagem.</p>
                        <p>© 2024 MyFinance. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {resend_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": "MyFinance <onboarding@resend.dev>",
                        "to": [email],
                        "subject": "Bem-vindo ao MyFinance! 🎉",
                        "html": html_content
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    print(f"Email de boas-vindas enviado para {email}")
                else:
                    print(f"Erro ao enviar email: {response.status_code} - {response.text}")
                    
        except Exception as e:
            print(f"Erro ao enviar email de boas-vindas: {str(e)}")
    
    async def login_user(self, user_data: UserLogin) -> Dict[str, Any]:
        """
        Autentica um usuário
        
        Args:
            user_data: Dados de login do usuário
            
        Returns:
            Dados do usuário autenticado com token
            
        Raises:
            HTTPException: Se houver erro na autenticação
        """
        try:
            # Buscar perfil do usuário pelo email
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.email == user_data.email).first()
            db.close()
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas"
                )
            
            # Verificar senha
            from .utils.password_validator import verify_password
            
            if not verify_password(user_data.password, profile.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciais inválidas"
                )
            
            # Gerar token JWT
            token_data = {
                "user_id": str(profile.user_id),
                "email": profile.email,
                "full_name": profile.full_name
            }
            
            token = self.jwt_handler.create_token(token_data)
            
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": {
                    "id": str(profile.user_id),
                    "email": profile.email,
                    "full_name": profile.full_name,
                    "avatar_url": profile.avatar_url,
                    "timezone": profile.timezone,
                    "currency": profile.currency,
                    "language": profile.language,
                    "email_confirmed_at": profile.created_at.isoformat() if profile.created_at else None
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro no login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno do servidor"
            )
    
    async def forgot_password(self, request_data: ForgotPasswordRequest) -> Dict[str, str]:
        """
        Solicita recuperação de senha
        
        Args:
            request_data: Dados da requisição (email)
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro na solicitação
        """
        try:
            # Verificar se o usuário existe no perfil
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.email == request_data.email).first()
            db.close()
            
            if not profile:
                # Não revelar se o email existe ou não por segurança
                return {
                    "message": "Se o email estiver cadastrado, você receberá um link de recuperação"
                }
            
            # Gerar token de recuperação
            import secrets
            from datetime import datetime, timedelta
            
            recovery_token = secrets.token_urlsafe(32)
            token_expiry = datetime.utcnow() + timedelta(hours=24)
            
            # Salvar token no banco (você pode criar uma tabela para isso)
            # Por enquanto, vamos usar uma abordagem simples
            
            # Enviar email via Resend
            try:
                await self._send_recovery_email(request_data.email, profile.full_name, recovery_token)
                return {
                    "message": "Email de recuperação de senha enviado com sucesso"
                }
            except Exception as email_error:
                print(f"Erro ao enviar email de recuperação: {email_error}")
                return {
                    "message": "Se o email estiver cadastrado, você receberá um link de recuperação"
                }
            
        except Exception as e:
            # Não revelar se o email existe ou não por segurança
            return {
                "message": "Se o email estiver cadastrado, você receberá um link de recuperação"
            }
    
    async def _send_recovery_email(self, email: str, full_name: str, token: str) -> None:
        """
        Envia email de recuperação de senha
        
        Args:
            email: Email do usuário
            full_name: Nome completo do usuário
            token: Token de recuperação
        """
        try:
            import httpx
            
            resend_api_key = os.getenv("RESEND_API_KEY")
            if not resend_api_key:
                print("RESEND_API_KEY não configurada")
                return
            
            # URL da aplicação
            app_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
            reset_url = f"{app_url}/auth/reset-password?token={token}&email={email}"
            
            # Template do email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Recuperação de Senha - MyFinance</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Recuperação de Senha</h1>
                    </div>
                    <div class="content">
                        <h2>Olá, {full_name}!</h2>
                        <p>Recebemos uma solicitação para redefinir sua senha no MyFinance.</p>
                        
                        <div style="text-align: center;">
                            <a href="{reset_url}" class="button">Redefinir Senha</a>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Importante:</strong>
                            <ul>
                                <li>Este link é válido por 24 horas</li>
                                <li>Se você não solicitou esta recuperação, ignore este email</li>
                                <li>Nunca compartilhe este link com outras pessoas</li>
                            </ul>
                        </div>
                        
                        <p>Se o botão não funcionar, copie e cole este link no seu navegador:</p>
                        <p style="word-break: break-all; background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px;">
                            {reset_url}
                        </p>
                        
                        <p>Atenciosamente,<br>Equipe MyFinance</p>
                    </div>
                    <div class="footer">
                        <p>Este é um email automático, não responda a esta mensagem.</p>
                        <p>© 2024 MyFinance. Todos os direitos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {resend_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": "MyFinance <onboarding@resend.dev>",
                        "to": [email],
                        "subject": "🔐 Recuperação de Senha - MyFinance",
                        "html": html_content
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    print(f"Email de recuperação enviado para {email}")
                else:
                    print(f"Erro ao enviar email de recuperação: {response.status_code} - {response.text}")
                    
        except Exception as e:
            print(f"Erro ao enviar email de recuperação: {str(e)}")
            raise
    
    async def reset_password(self, request_data: ResetPasswordRequest) -> Dict[str, str]:
        """
        Redefine a senha do usuário
        
        Args:
            request_data: Dados da requisição (token, email, new_password)
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro na redefinição
        """
        try:
            # Por enquanto, vamos implementar uma versão simples
            # que atualiza a senha diretamente no perfil
            # Em produção, você deve validar o token e implementar
            # um sistema mais robusto de tokens de recuperação
            
            db = SessionLocal()
            
            # Buscar perfil pelo email
            profile = db.query(UserProfile).filter(UserProfile.email == request_data.email).first()
            
            if not profile:
                db.close()
                raise HTTPException(
                    status_code=404,
                    detail="Usuário não encontrado"
                )
            
            # Validar senha
            from .utils.password_validator import validate_password
            password_errors = validate_password(request_data.new_password)
            
            if password_errors:
                db.close()
                raise HTTPException(
                    status_code=422,
                    detail=f"Senha inválida: {', '.join(password_errors)}"
                )
            
            # Hash da nova senha
            from .utils.password_validator import hash_password
            hashed_password = hash_password(request_data.new_password)
            
            # Atualizar senha no perfil
            profile.password_hash = hashed_password
            profile.updated_at = datetime.utcnow()
            
            db.commit()
            db.close()
            
            return {
                "message": "Senha redefinida com sucesso"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro ao redefinir senha: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Erro interno do servidor"
            )
    
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Busca o perfil de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dados do perfil do usuário
            
        Raises:
            HTTPException: Se houver erro ao buscar perfil
        """
        try:
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            db.close()
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil do usuário não encontrado"
                )
            
            return {
                "id": profile.id,
                "user_id": profile.user_id,
                "email": profile.email,
                "full_name": profile.full_name,
                "avatar_url": profile.avatar_url,
                "timezone": profile.timezone,
                "currency": profile.currency,
                "language": profile.language,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            }
            
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
            profile_data: Dados para atualização do perfil
            
        Returns:
            Dados do perfil atualizado
            
        Raises:
            HTTPException: Se houver erro na atualização
        """
        try:
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            if not profile:
                db.close()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil do usuário não encontrado"
                )
            
            # Atualizar campos fornecidos
            update_data = profile_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(profile, field, value)
            
            db.commit()
            db.refresh(profile)
            db.close()
            
            return {
                "id": profile.id,
                "user_id": profile.user_id,
                "email": profile.email,
                "full_name": profile.full_name,
                "avatar_url": profile.avatar_url,
                "timezone": profile.timezone,
                "currency": profile.currency,
                "language": profile.language,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def logout_user(self, user_id: str) -> Dict[str, str]:
        """
        Realiza logout do usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro no logout
        """
        try:
            # Em um sistema real, aqui você poderia:
            # 1. Invalidar tokens no banco de dados
            # 2. Adicionar tokens à blacklist
            # 3. Limpar sessões ativas
            
            # Por enquanto, apenas retorna sucesso
            return {"message": "Logout realizado com sucesso"}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            )
    
    async def refresh_token(self, request_data: RefreshTokenRequest) -> Dict[str, str]:
        """
        Atualiza o token de acesso usando refresh token
        
        Args:
            request_data: Dados da requisição contendo refresh token
            
        Returns:
            Novos tokens de acesso e refresh
            
        Raises:
            HTTPException: Se o refresh token for inválido
        """
        try:
            # TODO: Implementar validação real do refresh token
            # Por enquanto, apenas simula a renovação
            new_access_token = "new-access-token-123"
            new_refresh_token = "new-refresh-token-123"
            
            return {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token de refresh inválido")
    
    async def delete_user(self, user_id: str) -> Dict[str, str]:
        """
        Deleta um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Mensagem de confirmação
            
        Raises:
            HTTPException: Se houver erro na exclusão
        """
        try:
            # Deletar perfil do usuário
            db = SessionLocal()
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            if profile:
                db.delete(profile)
                db.commit()
            
            db.close()
            
            # Deletar usuário no Supabase
            try:
                self.supabase.auth.admin.delete_user(user_id)
            except Exception as e:
                print(f"Erro ao deletar usuário no Supabase: {str(e)}")
            
            return {"message": "Usuário deletado com sucesso"}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno do servidor: {str(e)}"
            ) 