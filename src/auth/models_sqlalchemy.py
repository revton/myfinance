"""Modelos SQLAlchemy para o sistema de autenticação

Este módulo define os modelos de banco de dados para o sistema de autenticação,
incluindo a tabela de tokens revogados para prevenir race conditions.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from ..database_sqlalchemy import Base

class RevokedToken(Base):
    """Modelo para tokens revogados
    
    Esta tabela armazena tokens que foram revogados antes de sua expiração natural,
    como em casos de logout ou refresh token. Isso previne race conditions onde
    um token revogado ainda poderia ser usado em outra sessão.
    """
    __tablename__ = "revoked_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jti = Column(String, nullable=False, unique=True, index=True, comment="JWT ID único do token")
    token_type = Column(String, nullable=False, comment="Tipo do token: access ou refresh")
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True, comment="ID do usuário associado ao token")
    revoked_at = Column(DateTime, nullable=False, server_default=func.now(), comment="Data e hora da revogação")
    expires_at = Column(DateTime, nullable=False, comment="Data e hora de expiração original do token")
    
    # Índice composto para consultas rápidas por jti e tipo
    __table_args__ = (
        Index('idx_revoked_tokens_jti_type', jti, token_type),
    )
    
    def __repr__(self):
        return f"<RevokedToken(jti='{self.jti}', type='{self.token_type}', user_id='{self.user_id}')>"