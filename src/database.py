"""
Modelos SQLAlchemy para o banco de dados
Baseados nos modelos Pydantic para integração com Alembic
"""
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database_sqlalchemy import Base
import uuid

class Transaction(Base):
    """Modelo SQLAlchemy para transações"""
    __tablename__ = "transactions"
    
    # Campos baseados no modelo Pydantic
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Constraints baseados na validação Pydantic
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name="check_transaction_type"),
        CheckConstraint("amount > 0", name="check_amount_positive"),
        CheckConstraint("length(description) >= 1", name="check_description_not_empty"),
        CheckConstraint("length(description) <= 500", name="check_description_length"),
        
        # Índices para performance
        Index("idx_transactions_type", "type"),
        Index("idx_transactions_created_at", "created_at"),
        Index("idx_transactions_amount", "amount"),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount})>" 