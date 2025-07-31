"""
FastAPI com SQLAlchemy direto - alternativa ao Supabase
"""
from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .models import TransactionCreate, Transaction, TransactionUpdate
from .database_direct import get_db, create_tables, Transaction as DBTransaction
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

@app.on_event("startup")
async def startup_event():
    """Criar tabelas na inicialização"""
    create_tables()
    logger.info("Tabelas criadas/verificadas")

@app.post("/transactions/", status_code=status.HTTP_201_CREATED, response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        # Criar objeto do banco
        db_transaction = DBTransaction(
            id=uuid.uuid4(),
            type=transaction.type.value,
            amount=transaction.amount,
            description=transaction.description
        )
        
        # Salvar no banco
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação criada: {db_transaction.id}")
        
        # Converter para modelo de resposta
        return Transaction(
            id=str(db_transaction.id),
            type=db_transaction.type,
            amount=db_transaction.amount,
            description=db_transaction.description,
            created_at=db_transaction.created_at,
            updated_at=db_transaction.updated_at
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao criar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/", response_model=List[Transaction])
async def list_transactions(db: Session = Depends(get_db)):
    try:
        # Buscar todas as transações ordenadas por data
        db_transactions = db.query(DBTransaction).order_by(DBTransaction.created_at.desc()).all()
        
        logger.info(f"Listadas {len(db_transactions)} transações")
        
        # Converter para modelos de resposta
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
        
    except Exception as e:
        logger.error(f"Erro ao listar transações: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    try:
        # Buscar transação específica
        db_transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação encontrada: {transaction_id}")
        
        # Converter para modelo de resposta
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
        # Buscar transação existente
        db_transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        # Atualizar campos fornecidos
        if transaction.type is not None:
            db_transaction.type = transaction.type.value
        if transaction.amount is not None:
            db_transaction.amount = transaction.amount
        if transaction.description is not None:
            db_transaction.description = transaction.description
        
        # Atualizar timestamp
        db_transaction.updated_at = datetime.utcnow()
        
        # Salvar alterações
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(f"Transação atualizada: {transaction_id}")
        
        # Converter para modelo de resposta
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
        # Buscar transação existente
        db_transaction = db.query(DBTransaction).filter(DBTransaction.id == transaction_id).first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        # Deletar transação
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
        "message": "MyFinance API is running (SQLAlchemy Direct)",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "debug": settings.DEBUG
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main_direct:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 