from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from .config import settings
from .models import TransactionCreate, Transaction, TransactionList, TransactionUpdate
from .database_sqlalchemy import get_db, create_tables, test_connection
from .database import Transaction as TransactionModel
from .auth import auth_router
from .categories import routes as category_router
import uuid
from datetime import datetime
import logging
import os
import sentry_sdk

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicialização do Sentry
if settings.SENTRY_DSN_BACKEND:
    logger.info("Inicializando Sentry para monitoramento de erros")
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN_BACKEND,
        # Defina traces_sample_rate como 1.0 para capturar 100%
        # das transações para monitoramento de performance.
        # Ajuste em produção se necessário.
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        environment=settings.ENVIRONMENT,
    )
    logger.info(f"Sentry inicializado com sucesso no ambiente: {settings.ENVIRONMENT}")
else:
    logger.warning("Variável SENTRY_DSN_BACKEND não configurada. Monitoramento de erros desativado.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)

# Permitir CORS para facilitar o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de autenticação
app.include_router(auth_router)
app.include_router(category_router.router)

# Endpoint de teste para o Sentry
@app.get("/sentry-debug")
async def trigger_error():
    """Endpoint para testar a integração com o Sentry"""
    logger.info("Gerando erro de teste para o Sentry")
    try:
        # Gera um erro de divisão por zero
        division_by_zero = 1 / 0
        return {"message": "Este código nunca será executado"}
    except Exception as e:
        logger.error(f"Erro capturado: {str(e)}")
        # O Sentry capturará automaticamente esta exceção
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro de teste gerado com sucesso e enviado ao Sentry"
        )

@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    try:
        # Pula a inicialização do banco se estiver em modo de teste
        if os.getenv("TESTING") == "true":
            logger.info("Modo de teste detectado - pulando inicialização do banco")
            return
            
        # Testa conexão com banco
        if test_connection():
            logger.info("Conexão com banco estabelecida com sucesso")
        else:
            logger.error("Falha ao conectar com banco")
        
        # Cria tabelas se não existirem
        create_tables()
        logger.info("Aplicação inicializada com sucesso")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")
        raise

@app.post("/transactions/", status_code=status.HTTP_201_CREATED, response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        # Cria instância do modelo SQLAlchemy
        db_transaction = TransactionModel(
            id=uuid.uuid4(),
            type=transaction.type.value,
            amount=transaction.amount,
            description=transaction.description,
            category_id=transaction.category_id
        )
        
        # Adiciona e commita
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação criada: {db_transaction.id}")
        
        # Converte para modelo Pydantic
        return db_transaction
            
    except HTTPException:
        # Re-raise HTTPException para manter o status code correto
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/", response_model=List[Transaction])
async def list_transactions(db: Session = Depends(get_db)):
    try:
        # Busca todas as transações ordenadas por data de criação
        db_transactions = db.query(TransactionModel).options(joinedload(TransactionModel.category)).order_by(TransactionModel.created_at.desc()).all()
        
        logger.info(f"Listadas {len(db_transactions)} transações")
        
        # Converte para modelos Pydantic
        return db_transactions
        
    except HTTPException:
        # Re-raise HTTPException para manter o status code correto
        raise
    except Exception as e:
        logger.error(f"Erro ao listar transações: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    try:
        # Busca transação por ID
        db_transaction = db.query(TransactionModel).options(joinedload(TransactionModel.category)).filter(TransactionModel.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação encontrada: {transaction_id}")
        
        # Converte para modelo Pydantic
        return db_transaction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: str, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    try:
        # Busca transação existente
        db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        # Atualiza campos fornecidos
        update_data = transaction.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_transaction, key, value)
        
        # Commita as mudanças
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação atualizada: {transaction_id}")
        
        # Converte para modelo Pydantic
        return db_transaction
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao atualizar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    try:
        # Busca transação para deletar
        db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        # Remove e commita
        db.delete(db_transaction)
        db.commit()
        
        logger.info(f"Transação deletada: {transaction_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao deletar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "message": "MyFinance API is running",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": settings.DEBUG
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )