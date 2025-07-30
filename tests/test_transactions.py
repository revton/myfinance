import pytest
import os
import uuid
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from src.config import settings
from src.main import app
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    """Cliente de teste para a aplicação FastAPI"""
    return TestClient(app)

@pytest.fixture
def mock_db_session():
    """Mock da sessão SQLAlchemy para testes"""
    mock_session = Mock(spec=Session)
    
    # Mock para transação de teste com UUID válido
    mock_transaction = Mock()
    mock_transaction.id = uuid.uuid4()
    mock_transaction.type = "income"
    mock_transaction.amount = 100.0
    mock_transaction.description = "Test transaction"
    mock_transaction.created_at = datetime.now()
    mock_transaction.updated_at = datetime.now()
    
    # Mock para query
    mock_query = Mock()
    mock_query.order_by.return_value.all.return_value = [mock_transaction]
    mock_query.filter.return_value.first.return_value = mock_transaction
    
    mock_session.query.return_value = mock_query
    mock_session.add = Mock()
    mock_session.commit = Mock()
    mock_session.refresh = Mock()
    mock_session.delete = Mock()
    mock_session.rollback = Mock()
    
    return mock_session

@pytest.fixture
def mock_get_db(mock_db_session):
    """Mock da dependência get_db"""
    def _mock_get_db():
        yield mock_db_session
    return _mock_get_db

# Desabilita completamente a conexão com banco durante testes
@pytest.fixture(autouse=True)
def disable_database():
    """Desabilita conexão com banco durante todos os testes"""
    with patch('src.database_sqlalchemy.engine') as mock_engine:
        with patch('src.database_sqlalchemy.SessionLocal') as mock_session_local:
            mock_session = Mock(spec=Session)
            mock_session_local.return_value = mock_session
            yield

def test_create_transaction_success(client, mock_get_db):
    """Testa criação bem-sucedida de transação"""
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

def test_list_transactions_success(client, mock_get_db):
    """Testa listagem bem-sucedida de transações"""
    with patch('src.main.get_db', mock_get_db):
        response = client.get("/transactions/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["type"] == "income"
        assert data[0]["amount"] == 100.0

def test_get_transaction_success(client, mock_get_db):
    """Testa busca bem-sucedida de transação específica"""
    # Cria um UUID válido para o teste
    test_uuid = str(uuid.uuid4())
    
    with patch('src.main.get_db', mock_get_db):
        response = client.get(f"/transactions/{test_uuid}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "income"
        assert data["amount"] == 100.0

def test_get_transaction_not_found(client):
    """Testa busca de transação inexistente"""
    # Mock para transação não encontrada
    mock_session = Mock(spec=Session)
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_session.query.return_value = mock_query
    
    def _mock_get_db_not_found():
        yield mock_session
    
    test_uuid = str(uuid.uuid4())
    
    with patch('src.main.get_db', _mock_get_db_not_found):
        response = client.get(f"/transactions/{test_uuid}")
        
        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"]

def test_update_transaction_success(client, mock_get_db):
    """Testa atualização bem-sucedida de transação"""
    test_uuid = str(uuid.uuid4())
    
    with patch('src.main.get_db', mock_get_db):
        response = client.put(f"/transactions/{test_uuid}", json={
            "amount": 150.0,
            "description": "Updated transaction"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 150.0
        assert data["description"] == "Updated transaction"

def test_delete_transaction_success(client, mock_get_db):
    """Testa exclusão bem-sucedida de transação"""
    test_uuid = str(uuid.uuid4())
    
    with patch('src.main.get_db', mock_get_db):
        response = client.delete(f"/transactions/{test_uuid}")
        
        assert response.status_code == 204

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