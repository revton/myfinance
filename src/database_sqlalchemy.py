"""
Configuração SQLAlchemy direta para Supabase
Substitui o cliente Supabase por SQLAlchemy para operações de banco
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .config import settings
import logging
import os
from unittest.mock import Mock

logger = logging.getLogger(__name__)

# Configuração do engine SQLAlchemy
def get_database_url():
    """Constrói a URL do banco a partir das configurações do Supabase"""
    if not settings.DATABASE_URL:
        # Constrói a URL a partir do SUPABASE_URL se DATABASE_URL não estiver definido
        supabase_url = settings.SUPABASE_URL
        if not supabase_url:
            raise ValueError("SUPABASE_URL não configurado")
        
        # Extrai o host do SUPABASE_URL e constrói a DATABASE_URL
        # Exemplo: https://xyz.supabase.co -> postgresql://postgres:[password]@xyz.supabase.co:5432/postgres
        host = supabase_url.replace("https://", "").replace("http://", "")
        
        # Para desenvolvimento, você pode usar uma senha padrão ou configurar via env
        password = os.getenv("SUPABASE_DB_PASSWORD", "postgres")
        database_url = f"postgresql://postgres:{password}@{host}:5432/postgres"
        
        logger.info(f"URL do banco construída: {database_url}")
        return database_url
    
    return settings.DATABASE_URL

# Engine SQLAlchemy
engine = create_engine(
    get_database_url(),
    pool_size=5,           # Pool de conexões
    max_overflow=10,       # Conexões extras permitidas
    pool_pre_ping=True,    # Verifica conexão antes de usar
    pool_recycle=3600,     # Recicla conexões a cada hora
    echo=settings.DEBUG    # Log SQL em modo debug
)

# Sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Engine para o banco de dados de teste em memória (SQLite)
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def get_db() -> Session:
    """Dependency para obter sessão do banco"""
    if os.getenv("TESTING") == "true":
        logger.info("Modo de teste detectado - usando banco de dados em memória")
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # Modo normal - retorna sessão real
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

def create_tables():
    """Cria todas as tabelas definidas nos modelos"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas criadas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        raise

def drop_tables():
    """Remove todas as tabelas (apenas para desenvolvimento)"""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Tabelas removidas com sucesso")
    except Exception as e:
        logger.error(f"Erro ao remover tabelas: {e}")
        raise

def test_connection():
    """Testa a conexão com o banco"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("Conexão com banco testada com sucesso")
            return True
    except Exception as e:
        logger.error(f"Erro ao testar conexão: {e}")
        return False 