"""
Modelos SQLAlchemy para o banco de dados
Baseados nos modelos Pydantic para integração com Alembic
"""
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, CheckConstraint, Index, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .custom_types import GUID as UUID
from sqlalchemy.sql import func
from .database_sqlalchemy import Base
import uuid
from src.categories.models import CategoryType

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    icon = Column(String(50), default="category")
    color = Column(String(7), default="#1976d2")  # #RRGGBB format
    type = Column(SQLEnum(CategoryType), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    """Modelo SQLAlchemy para transações"""
    __tablename__ = "transactions"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    type = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(UUID, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name="check_transaction_type"),
        CheckConstraint("amount > 0", name="check_amount_positive"),
        CheckConstraint("length(description) >= 1", name="check_description_not_empty"),
        CheckConstraint("length(description) <= 500", name="check_description_length"),
        Index("idx_transactions_type", "type"),
        Index("idx_transactions_created_at", "created_at"),
        Index("idx_transactions_amount", "amount"),
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.type}, amount={self.amount})>"

class UserProfile(Base):
    """Modelo SQLAlchemy para perfis de usuário"""
    __tablename__ = "user_profiles"
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, nullable=False, unique=True)
    email = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)
    avatar_url = Column(Text, nullable=True)
    timezone = Column(String(50), nullable=False, default="America/Sao_Paulo")
    currency = Column(String(3), nullable=False, default="BRL")
    language = Column(String(5), nullable=False, default="pt-BR")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("timezone IN ('America/Sao_Paulo', 'UTC', 'America/New_York', 'Europe/London')", name="check_valid_timezone"),
        CheckConstraint("currency IN ('BRL', 'USD', 'EUR', 'GBP')", name="check_valid_currency"),
        CheckConstraint("language IN ('pt-BR', 'en-US', 'es-ES')", name="check_valid_language"),
        CheckConstraint("length(email) >= 3", name="check_email_length"),
        CheckConstraint("length(full_name) <= 255", name="check_full_name_length"),
        Index("idx_user_profiles_user_id", "user_id"),
        Index("idx_user_profiles_email", "email"),
        Index("idx_user_profiles_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id}, email={self.email})>"
