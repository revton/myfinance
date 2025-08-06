"""
Configuração de fixtures para testes
"""
import pytest
import os
from fastapi.testclient import TestClient
from src.main import app

# Configurar ambiente de teste
os.environ["TESTING"] = "true"

@pytest.fixture
def client():
    """
    Fixture que fornece um cliente de teste para a aplicação FastAPI
    
    Returns:
        TestClient: Cliente de teste configurado
    """
    return TestClient(app) 