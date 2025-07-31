import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch
from src.config import settings
from src.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    """Cliente de teste para a aplicação FastAPI"""
    return TestClient(app)

def test_create_transaction_invalid_type(client):
    """Testa criação de transação com tipo inválido"""
    response = client.post("/transactions/", json={
        "type": "invalid",
        "amount": 100.0,
        "description": "Test transaction"
    })
    
    assert response.status_code == 422  # Pydantic validation error
    assert "type" in response.json()["detail"][0]["loc"]

def test_create_transaction_invalid_amount(client):
    """Testa criação de transação com valor inválido"""
    response = client.post("/transactions/", json={
        "type": "income",
        "amount": -100.0,
        "description": "Test transaction"
    })
    
    assert response.status_code == 422  # Pydantic validation error
    assert "amount" in response.json()["detail"][0]["loc"]

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
    """Testa se a configuração de ambiente está funcionando"""
    assert hasattr(settings, 'ENVIRONMENT')
    assert hasattr(settings, 'SUPABASE_URL')
    assert hasattr(settings, 'SUPABASE_ANON_KEY')

# Testes com mocks mais simples
def test_create_transaction_success_mocked(client):
    """Testa criação bem-sucedida de transação com mock"""
    # Mock da sessão
    mock_session = Mock(spec=Session)
    mock_transaction = Mock()
    mock_transaction.id = uuid.uuid4()
    mock_transaction.type = "income"
    mock_transaction.amount = 100.0
    mock_transaction.description = "Test transaction"
    mock_transaction.created_at = datetime.now()
    mock_transaction.updated_at = datetime.now()
    
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()
    mock_session.refresh(mock_transaction)  # Simula o refresh
    
    def mock_get_db():
        yield mock_session
    
    with patch('src.main.get_db', mock_get_db):
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

def test_list_transactions_success_mocked(client):
    """Testa listagem bem-sucedida de transações com mock"""
    # Mock da sessão
    mock_session = Mock(spec=Session)
    mock_transaction = Mock()
    mock_transaction.id = uuid.uuid4()
    mock_transaction.type = "income"
    mock_transaction.amount = 100.0
    mock_transaction.description = "Test transaction"
    mock_transaction.created_at = datetime.now()
    mock_transaction.updated_at = datetime.now()
    
    mock_query = Mock()
    mock_query.order_by.return_value.all.return_value = [mock_transaction]
    mock_session.query.return_value = mock_query
    
    def mock_get_db():
        yield mock_session
    
    # Patch mais específico para garantir que o mock seja aplicado
    with patch('src.main.get_db', mock_get_db), \
         patch('src.database_sqlalchemy.SessionLocal') as mock_session_local:
        
        # Configura o mock da SessionLocal para retornar nossa sessão mock
        mock_session_local.return_value = mock_session
        
        response = client.get("/transactions/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["type"] == "income"
        assert data[0]["amount"] == 100.0 