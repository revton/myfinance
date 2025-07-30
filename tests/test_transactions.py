import pytest
import os
from unittest.mock import Mock, patch
from src.config import settings
from src.main import app
from fastapi.testclient import TestClient

# Configurar variáveis de ambiente para testes
os.environ['ENVIRONMENT'] = 'testing'
os.environ['SUPABASE_TEST_URL'] = os.getenv('SUPABASE_TEST_URL', 'https://test.supabase.co')
os.environ['SUPABASE_TEST_ANON_KEY'] = os.getenv('SUPABASE_TEST_ANON_KEY', 'test-key')

@pytest.fixture
def client():
    """Cliente de teste para a aplicação FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_supabase():
    """Mock do cliente Supabase para testes"""
    mock_client = Mock()
    
    # Mock para inserção de transação
    mock_insert = Mock()
    mock_insert.execute.return_value = Mock(
        data=[{
            'id': 'test-id-123',
            'type': 'income',
            'amount': 100.0,
            'description': 'Test transaction',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z'
        }]
    )
    mock_client.table.return_value.insert.return_value = mock_insert
    
    # Mock para listagem de transações
    mock_select = Mock()
    mock_select.order.return_value.execute.return_value = Mock(
        data=[{
            'id': 'test-id-123',
            'type': 'income',
            'amount': 100.0,
            'description': 'Test transaction',
            'created_at': '2024-01-01T00:00:00Z',
            'updated_at': '2024-01-01T00:00:00Z'
        }]
    )
    mock_client.table.return_value.select.return_value = mock_select
    
    return mock_client

def test_create_transaction_success(client, mock_supabase):
    """Testa criação bem-sucedida de transação"""
    with patch.object(settings, 'supabase_client', mock_supabase):
        response = client.post("/transactions/", json={
            "type": "income",
            "amount": 100.0,
            "description": "Test transaction"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "income"
        assert data["amount"] == 100.0
        assert data["description"] == "Test transaction"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

def test_create_transaction_invalid_type(client):
    """Testa criação de transação com tipo inválido"""
    response = client.post("/transactions/", json={
        "type": "invalid",
        "amount": 100.0,
        "description": "Test transaction"
    })
    
    assert response.status_code == 400
    assert "Tipo deve ser 'income' ou 'expense'" in response.json()["detail"]

def test_create_transaction_invalid_amount(client):
    """Testa criação de transação com valor inválido"""
    response = client.post("/transactions/", json={
        "type": "income",
        "amount": -100.0,
        "description": "Test transaction"
    })
    
    assert response.status_code == 400
    assert "Valor deve ser maior que zero" in response.json()["detail"]

def test_list_transactions_success(client, mock_supabase):
    """Testa listagem bem-sucedida de transações"""
    with patch.object(settings, 'supabase_client', mock_supabase):
        response = client.get("/transactions/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["type"] == "income"
        assert data[0]["amount"] == 100.0

def test_health_check(client):
    """Testa endpoint de health check"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "MyFinance API is running" in data["message"]
    assert "environment" in data
    assert "debug" in data

def test_environment_configuration():
    """Testa se a configuração de ambiente está correta para testes"""
    assert settings.ENVIRONMENT == "testing"
    assert "test" in settings.SUPABASE_URL or settings.SUPABASE_URL == "https://test.supabase.co" 