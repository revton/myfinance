"""
Modelos Pydantic para o banco de dados
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class TransactionType(str, Enum):
    """Tipos de transação"""
    INCOME = "income"
    EXPENSE = "expense"

class TransactionBase(BaseModel):
    """Modelo base para transações"""
    type: TransactionType = Field(..., description="Tipo da transação: income ou expense")
    amount: float = Field(..., gt=0, description="Valor da transação (sempre positivo)")
    description: str = Field(..., min_length=1, max_length=500, description="Descrição da transação")

class TransactionCreate(TransactionBase):
    """Modelo para criação de transações"""
    pass

class TransactionUpdate(BaseModel):
    """Modelo para atualização de transações"""
    type: Optional[TransactionType] = Field(None, description="Tipo da transação")
    amount: Optional[float] = Field(None, gt=0, description="Valor da transação")
    description: Optional[str] = Field(None, min_length=1, max_length=500, description="Descrição da transação")

class Transaction(TransactionBase):
    """Modelo completo de transação com campos do banco"""
    id: str = Field(..., description="ID único da transação")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data da última atualização")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "type": "income",
                "amount": 1000.00,
                "description": "Salário do mês",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    )

class TransactionList(BaseModel):
    """Modelo para listagem de transações"""
    transactions: list[Transaction] = Field(..., description="Lista de transações")
    total: int = Field(..., description="Total de transações")
    page: int = Field(1, description="Página atual")
    per_page: int = Field(10, description="Itens por página")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transactions": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "type": "income",
                        "amount": 1000.00,
                        "description": "Salário do mês",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "per_page": 10
            }
        }
    )

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid
from src.categories.models import CategoryType

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    icon = Column(String(50), default="category")
    color = Column(String(7), default="#1976d2")  # #RRGGBB format
    type = Column(SQLEnum(CategoryType), nullable=False)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    # transactions = relationship("Transaction", back_populates="category")
    # user = relationship("UserProfile", back_populates="categories")
