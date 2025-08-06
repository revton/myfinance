"""
Manipulador de JWT para o sistema de autenticação

Este módulo implementa criação, validação e refresh de tokens JWT
para autenticação segura no sistema.
"""

import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import HTTPException, status

class JWTHandler:
    """Manipulador de tokens JWT"""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    def create_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Cria um token JWT
        
        Args:
            data: Dados a serem incluídos no token
            expires_delta: Tempo de expiração personalizado
            
        Returns:
            Token JWT codificado
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar token: {str(e)}"
            )
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """
        Cria um token de acesso
        
        Args:
            data: Dados do usuário
            
        Returns:
            Token de acesso JWT
        """
        return self.create_token(data, timedelta(minutes=self.access_token_expire_minutes))
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Cria um token de refresh
        
        Args:
            data: Dados do usuário
            
        Returns:
            Token de refresh JWT
        """
        return self.create_token(data, timedelta(days=self.refresh_token_expire_days))
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica e decodifica um token JWT
        
        Args:
            token: Token JWT a ser verificado
            
        Returns:
            Dados decodificados do token
            
        Raises:
            HTTPException: Se o token for inválido
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verificar se o token contém os campos obrigatórios
            if "user_id" not in payload:
                raise ValueError("Token não contém user_id")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (jwt.InvalidSignatureError, jwt.InvalidAlgorithmError, jwt.DecodeError) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token inválido: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token malformado: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Cria um novo token de acesso usando um refresh token
        
        Args:
            refresh_token: Token de refresh válido
            
        Returns:
            Novo token de acesso
            
        Raises:
            HTTPException: Se o refresh token for inválido
        """
        try:
            # Verificar o refresh token
            payload = self.verify_token(refresh_token)
            
            # Criar novo token de acesso
            access_token_data = {
                "user_id": payload["user_id"],
                "email": payload.get("email"),
                "sub": payload.get("sub")
            }
            
            return self.create_access_token(access_token_data)
            
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_token_expiration(self, token: str) -> datetime:
        """
        Obtém a data de expiração de um token
        
        Args:
            token: Token JWT
            
        Returns:
            Data de expiração do token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            exp_timestamp = payload.get("exp")
            
            if exp_timestamp:
                return datetime.fromtimestamp(exp_timestamp)
            else:
                raise ValueError("Token não contém data de expiração")
                
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se um token está expirado
        
        Args:
            token: Token JWT
            
        Returns:
            True se o token estiver expirado, False caso contrário
        """
        try:
            exp = self.get_token_expiration(token)
            return datetime.utcnow() > exp
        except:
            return True
    
    def get_token_payload(self, token: str) -> Dict[str, Any]:
        """
        Obtém o payload de um token sem verificar a assinatura
        
        Args:
            token: Token JWT
            
        Returns:
            Payload do token
        """
        try:
            # Decodificar sem verificar a assinatura (apenas para leitura)
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token malformado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def create_token_pair(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Cria um par de tokens (access + refresh)
        
        Args:
            user_data: Dados do usuário
            
        Returns:
            Dicionário com access_token e refresh_token
        """
        access_token = self.create_access_token(user_data)
        refresh_token = self.create_refresh_token(user_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60  # em segundos
        }
    
    def validate_token_format(self, token: str) -> bool:
        """
        Valida o formato básico de um token JWT
        
        Args:
            token: Token a ser validado
            
        Returns:
            True se o formato for válido, False caso contrário
        """
        if not token:
            return False
        
        # Verificar se tem 3 partes separadas por ponto
        parts = token.split('.')
        if len(parts) != 3:
            return False
        
        # Verificar se cada parte é base64 válido
        import base64
        try:
            for part in parts:
                # Adicionar padding se necessário
                padding = 4 - len(part) % 4
                if padding != 4:
                    part += '=' * padding
                
                base64.urlsafe_b64decode(part)
            return True
        except:
            return False 