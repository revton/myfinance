from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir CORS para facilitar o desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    type: str  # 'income' ou 'expense'
    amount: float
    description: str

# Armazenamento em memória (temporário)
transactions: List[Transaction] = []

@app.post("/transactions/", status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return transaction

@app.get("/transactions/")
def list_transactions():
    return transactions 