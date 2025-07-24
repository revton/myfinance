from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

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