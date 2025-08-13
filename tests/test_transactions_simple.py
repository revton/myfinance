
import pytest
from fastapi.testclient import TestClient


def test_create_transaction_success_mocked(test_client: TestClient):
    """Testa criação bem-sucedida de transação com mock"""
    response = test_client.post("/transactions/", json={
        "type": "income",
        "amount": 100.0,
        "description": "[TEST] Mocked success transaction - should not save to DB"
    })

    assert response.status_code == 201


def test_list_transactions_success_mocked(test_client: TestClient):
    """Testa listagem bem-sucedida de transações com mock"""
    response = test_client.get("/transactions/")

    assert response.status_code == 200
