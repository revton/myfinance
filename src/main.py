from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
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

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
            description=transaction.description
        )
        
        # Adiciona e commita
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação criada: {db_transaction.id}")
        
        # Converte para modelo Pydantic
        return Transaction(
            id=str(db_transaction.id),
            type=db_transaction.type,
            amount=db_transaction.amount,
            description=db_transaction.description,
            created_at=db_transaction.created_at,
            updated_at=db_transaction.updated_at
        )
            
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
        db_transactions = db.query(TransactionModel).order_by(TransactionModel.created_at.desc()).all()
        
        logger.info(f"Listadas {len(db_transactions)} transações")
        
        # Converte para modelos Pydantic
        return [
            Transaction(
                id=str(t.id),
                type=t.type,
                amount=t.amount,
                description=t.description,
                created_at=t.created_at,
                updated_at=t.updated_at
            ) for t in db_transactions
        ]
        
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
        db_transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação encontrada: {transaction_id}")
        
        # Converte para modelo Pydantic
        return Transaction(
            id=str(db_transaction.id),
            type=db_transaction.type,
            amount=db_transaction.amount,
            description=db_transaction.description,
            created_at=db_transaction.created_at,
            updated_at=db_transaction.updated_at
        )
        
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
        if transaction.type is not None:
            db_transaction.type = transaction.type.value
        if transaction.amount is not None:
            db_transaction.amount = transaction.amount
        if transaction.description is not None:
            db_transaction.description = transaction.description
        
        # Commita as mudanças
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação atualizada: {transaction_id}")
        
        # Converte para modelo Pydantic
        return Transaction(
            id=str(db_transaction.id),
            type=db_transaction.type,
            amount=db_transaction.amount,
            description=db_transaction.description,
            created_at=db_transaction.created_at,
            updated_at=db_transaction.updated_at
        )
        
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