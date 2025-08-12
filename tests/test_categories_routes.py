from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.database import UserProfile
from uuid import UUID

class TestCategoriesRoutes:
    def test_create_category_success(self, authenticated_client, test_db: Session):
        """Testa a criação de uma categoria com sucesso"""
        # Arrange
        client, user_id = authenticated_client
        test_user = UserProfile(id=user_id, user_id=user_id, email="test@example.com", password_hash="hashedpassword")
        test_db.add(test_user)
        test_db.commit()

        category_data = {
            "name": "Alimentação",
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF5733",
            "type": "expense"
        }

        # Act
        response = client.post(f"/categories/", json=category_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["description"] == category_data["description"]
        assert "id" in data
        assert data["user_id"] == str(user_id)

    def test_create_category_invalid_data(self, authenticated_client, test_db: Session):
        """Testa a criação de uma categoria com dados inválidos"""
        # Arrange
        client, user_id = authenticated_client
        test_user = UserProfile(id=user_id, user_id=user_id, email="test@example.com", password_hash="hashedpassword")
        test_db.add(test_user)
        test_db.commit()

        category_data = {
            "name": "",  # Invalid name
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF5733",
            "type": "expense"
        }

        # Act
        response = client.post(f"/categories/", json=category_data)

        # Assert
        assert response.status_code == 422

    def test_get_categories_success(self, authenticated_client, test_db: Session):
        """Testa o sucesso na listagem de categorias"""
        # Arrange
        client, user_id = authenticated_client
        test_user = UserProfile(id=user_id, user_id=user_id, email="test@example.com", password_hash="hashedpassword")
        test_db.add(test_user)
        test_db.commit()

        category_data1 = {
            "name": "Alimentação",
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF5733",
            "type": "expense"
        }
        category_data2 = {
            "name": "Salário",
            "description": "Recebimento de salário",
            "icon": "work",
            "color": "#00FF00",
            "type": "income"
        }
        client.post(f"/categories/", json=category_data1)
        client.post(f"/categories/", json=category_data2)

        # Act
        response = client.get(f"/categories/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == category_data1["name"]
        assert data[1]["name"] == category_data2["name"]
