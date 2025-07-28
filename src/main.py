from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
import uuid
from datetime import datetime

app = FastAPI(title=settings.PROJECT_NAME)

# Permitir CORS para facilitar o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    type: str  # 'income' ou 'expense'
    amount: float
    description: str

class TransactionResponse(BaseModel):
    id: str
    type: str
    amount: float
    description: str
    created_at: datetime
    updated_at: datetime

@app.post("/transactions/", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
async def create_transaction(transaction: Transaction):
    try:
        supabase = settings.supabase_client
        
        # Validar tipo
        if transaction.type not in ['income', 'expense']:
            raise HTTPException(status_code=400, detail="Tipo deve ser 'income' ou 'expense'")
        
        # Validar valor
        if transaction.amount <= 0:
            raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")
        
        # Inserir no Supabase
        data = {
            "id": str(uuid.uuid4()),
            "type": transaction.type,
            "amount": transaction.amount,
            "description": transaction.description
        }
        
        result = supabase.table("transactions").insert(data).execute()
        
        if result.data:
            return TransactionResponse(**result.data[0])
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar transação")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/transactions/", response_model=List[TransactionResponse])
async def list_transactions():
    try:
        supabase = settings.supabase_client
        
        result = supabase.table("transactions").select("*").order("created_at", desc=True).execute()
        
        return [TransactionResponse(**transaction) for transaction in result.data]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "MyFinance API is running"} 