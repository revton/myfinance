import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from src.main import app

# Mock das variáveis de ambiente para teste
os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'test-key'

client = TestClient(app)

def test_create_income():
    response = client.post("/transactions/", json={
        "type": "income",
        "amount": 100.0,
        "description": "Salário"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "income"
    assert data["amount"] == 100.0
    assert data["description"] == "Salário"

def test_create_expense():
    response = client.post("/transactions/", json={
        "type": "expense",
        "amount": 50.0,
        "description": "Mercado"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "expense"
    assert data["amount"] == 50.0
    assert data["description"] == "Mercado"

def test_list_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "MyFinance API is running" in data["message"] 