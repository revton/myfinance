from fastapi import FastAPI, status, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import TransactionCreate, Transaction, TransactionList, TransactionUpdate
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

@app.post("/transactions/", status_code=status.HTTP_201_CREATED, response_model=Transaction)
async def create_transaction(transaction: TransactionCreate):
    try:
        supabase = settings.supabase_client
        
        # Inserir no Supabase
        data = {
            "id": str(uuid.uuid4()),
            "type": transaction.type.value,  # Usa o valor do enum
            "amount": transaction.amount,
            "description": transaction.description
        }
        
        result = supabase.table("transactions").insert(data).execute()
        
        if result.data:
            logger.info(f"Transação criada: {result.data[0]['id']}")
            return Transaction(**result.data[0])
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar transação")
            
    except HTTPException:
        # Re-raise HTTPException para manter o status code correto
        raise
    except Exception as e:
        logger.error(f"Erro ao criar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/", response_model=List[Transaction])
async def list_transactions():
    try:
        supabase = settings.supabase_client
        
        result = supabase.table("transactions").select("*").order("created_at", desc=True).execute()
        
        logger.info(f"Listadas {len(result.data)} transações")
        return [Transaction(**transaction) for transaction in result.data]
        
    except HTTPException:
        # Re-raise HTTPException para manter o status code correto
        raise
    except Exception as e:
        logger.error(f"Erro ao listar transações: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: str):
    try:
        supabase = settings.supabase_client
        
        result = supabase.table("transactions").select("*").eq("id", transaction_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação encontrada: {transaction_id}")
        return Transaction(**result.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.put("/transactions/{transaction_id}", response_model=Transaction)
async def update_transaction(transaction_id: str, transaction: TransactionUpdate):
    try:
        supabase = settings.supabase_client
        
        # Prepara dados para atualização
        update_data = {}
        if transaction.type is not None:
            update_data["type"] = transaction.type.value
        if transaction.amount is not None:
            update_data["amount"] = transaction.amount
        if transaction.description is not None:
            update_data["description"] = transaction.description
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        result = supabase.table("transactions").update(update_data).eq("id", transaction_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação atualizada: {transaction_id}")
        return Transaction(**result.data[0])
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar transação: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: str):
    try:
        supabase = settings.supabase_client
        
        result = supabase.table("transactions").delete().eq("id", transaction_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        
        logger.info(f"Transação deletada: {transaction_id}")
        
    except HTTPException:
        raise
    except Exception as e:
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