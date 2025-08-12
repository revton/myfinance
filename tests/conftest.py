"""
Configuração de fixtures para testes
"""
import pytest
import os
from fastapi.testclient import TestClient
from src.main import app
from src.database_sqlalchemy import Base, get_db, test_engine
from sqlalchemy.orm import Session
from src.database import UserProfile
from src.auth.dependencies import get_current_user
from uuid import uuid4

# Configurar ambiente de teste
os.environ["TESTING"] = "true"

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=test_engine)
    db = next(get_db())
    yield db
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def client(test_db: Session):
    """
    Fixture que fornece um cliente de teste para a aplicação FastAPI
    
    Returns:
        TestClient: Cliente de teste configurado
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def authenticated_client(client: TestClient, test_db: Session):
    """
    Fixture that provides an authenticated test client.
    """
    # Create a user in the test database
    user_id = uuid4()
    test_user = UserProfile(id=user_id, user_id=user_id, email="test@example.com", password_hash="hashedpassword")
    test_db.add(test_user)
    test_db.commit()

    from unittest.mock import MagicMock

    async def override_get_current_user():
        mock_user = MagicMock()
        mock_user.id = test_user.user_id
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    return client
