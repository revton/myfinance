import sys
import os
from unittest.mock import patch, MagicMock

# Ensure the project root is in the Python path
project_root = os.path.join(os.path.dirname(__file__), '..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set test environment variables before importing the app
os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'test-key'

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@patch('src.main.settings.supabase_client')
def test_create_income(mock_supabase):
    # Mock da resposta do Supabase
    mock_result = MagicMock()
    mock_result.data = [{
        "id": "test-id",
        "type": "income",
        "amount": 100.0,
        "description": "Salário",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_result
    
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

@patch('src.main.settings.supabase_client')
def test_create_expense(mock_supabase):
    # Mock da resposta do Supabase
    mock_result = MagicMock()
    mock_result.data = [{
        "id": "test-id",
        "type": "expense",
        "amount": 50.0,
        "description": "Mercado",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }]
    mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_result
    
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

@patch('src.main.settings.supabase_client')
def test_list_transactions(mock_supabase):
    # Mock da resposta do Supabase
    mock_result = MagicMock()
    mock_result.data = [
        {
            "id": "test-id-1",
            "type": "income",
            "amount": 100.0,
            "description": "Salário",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        },
        {
            "id": "test-id-2",
            "type": "expense",
            "amount": 50.0,
            "description": "Mercado",
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value = mock_result
    
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "MyFinance API is running" in data["message"] 