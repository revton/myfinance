
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.main import app
from src.auth.models import User
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def mock_db_session():
    with patch('src.database.get_db') as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        yield mock_db

@pytest.fixture
def mock_current_user():
    user = User(id=uuid4(), email="test@example.com")
    with patch('src.auth.dependencies.get_current_user') as mock_get_user:
        mock_get_user.return_value = user
        yield user

class TestCategoriesEndpoints:
    def test_create_category_success(self, mock_db_session, mock_current_user):
        # Arrange
        category_data = {
            "name": "Test Category",
            "description": "Test Description",
            "icon": "home",
            "color": "#FFFFFF",
            "type": "expense"
        }

        # Act
        response = client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 200


    def test_get_categories_success(self, mock_db_session, mock_current_user):
        # Act
        response = client.get("/categories/")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_category_success(self, mock_db_session, mock_current_user):
        # Arrange
        category_id = uuid4()

        # Act
        response = client.get(f"/categories/{category_id}")

        # Assert
        assert response.status_code == 200

    def test_update_category_success(self, mock_db_session, mock_current_user):
        // Arrange
        category_id = uuid4()
        update_data = {"name": "Updated Name"}

        # Act
        response = client.put(f"/categories/{category_id}", json=update_data)

        # Assert
        assert response.status_code == 200

    def test_delete_category_success(self, mock_db_session, mock_current_user):
        # Arrange
        category_id = uuid4()

        # Act
        response = client.delete(f"/categories/{category_id}")

        # Assert
        assert response.status_code == 200
