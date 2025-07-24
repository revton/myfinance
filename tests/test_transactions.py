import pytest
from fastapi.testclient import TestClient
from src.main import app

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