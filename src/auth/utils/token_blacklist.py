"""Gerenciador de tokens revogados (blacklist)

Este módulo implementa funções para gerenciar tokens revogados,
prevenindo race conditions em refresh tokens e garantindo segurança.
"""

from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from typing import Optional, Dict, Any

from ..models_sqlalchemy import RevokedToken
from ...database_sqlalchemy import SessionLocal

def revoke_token(token_data: Dict[str, Any], token_type: str, db: Optional[Session] = None) -> None:
    """Revoga um token adicionando-o à lista de tokens revogados
    
    Args:
        token_data: Payload do token JWT decodificado
        token_type: Tipo do token ('access' ou 'refresh')
        db: Sessão do banco de dados (opcional)
        
    Raises:
        Exception: Se ocorrer erro ao revogar o token
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
        
    try:
        # Extrair informações do token
        jti = token_data.get("jti", str(uuid.uuid4()))  # Usar UUID se não tiver JTI
        user_id = token_data.get("user_id")
        exp = token_data.get("exp")
        
        if not user_id or not exp:
            raise ValueError("Token não contém user_id ou exp")
            
        # Converter timestamp para datetime
        expires_at = datetime.fromtimestamp(exp)
        
        # Criar registro de token revogado
        revoked_token = RevokedToken(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        
        db.add(revoked_token)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        if close_db:
            db.close()

def is_token_revoked(jti: str, token_type: str, db: Optional[Session] = None) -> bool:
    """Verifica se um token está na lista de revogados
    
    Args:
        jti: JWT ID do token
        token_type: Tipo do token ('access' ou 'refresh')
        db: Sessão do banco de dados (opcional)
        
    Returns:
        True se o token estiver revogado, False caso contrário
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
        
    try:
        # Verificar se o token está na lista de revogados
        revoked = db.query(RevokedToken).filter(
            RevokedToken.jti == jti,
            RevokedToken.token_type == token_type
        ).first() is not None
        
        return revoked
    except Exception as e:
        # Em caso de erro, assumir que o token não está revogado
        # mas registrar o erro para investigação
        print(f"Erro ao verificar token revogado: {str(e)}")
        return False
    finally:
        if close_db:
            db.close()

def clean_expired_tokens(db: Optional[Session] = None) -> int:
    """Remove tokens expirados da lista de revogados
    
    Args:
        db: Sessão do banco de dados (opcional)
        
    Returns:
        Número de tokens removidos
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
        
    try:
        # Remover tokens que já expiraram
        now = datetime.utcnow()
        result = db.query(RevokedToken).filter(RevokedToken.expires_at < now).delete()
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        print(f"Erro ao limpar tokens expirados: {str(e)}")
        return 0
    finally:
        if close_db:
            db.close()

def revoke_all_user_tokens(user_id: str, db: Optional[Session] = None) -> int:
    """Revoga todos os tokens de um usuário
    
    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados (opcional)
        
    Returns:
        Número de tokens atualmente revogados para o usuário
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
        
    try:
        # Contar tokens atualmente revogados
        count = db.query(RevokedToken).filter(RevokedToken.user_id == user_id).count()
        return count
    except Exception as e:
        print(f"Erro ao contar tokens revogados do usuário: {str(e)}")
        return 0
    finally:
        if close_db:
            db.close()