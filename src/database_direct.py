"""
Configuração de banco de dados direto com SQLAlchemy
Alternativa ao Supabase para resolver problemas de cache
"""
from sqlalchemy import create_engine, Column, String, Float, Text, DateTime, CheckConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL deve estar configurado no .env")

# Criar engine
engine = create_engine(DATABASE_URL)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

class Transaction(Base):
    """Modelo de transação usando SQLAlchemy diretamente"""
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("type IN ('income', 'expense')", name="check_type"),
        CheckConstraint("amount > 0", name="check_amount"),
        Index("idx_transactions_type", "type"),
        Index("idx_transactions_created_at", "created_at"),
    )

def get_db():
    """Dependency para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Remover todas as tabelas"""
    Base.metadata.drop_all(bind=engine) 