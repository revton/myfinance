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

    def test_update_category_success(self, authenticated_client, test_db: Session):
        """Testa o sucesso na atualização de uma categoria"""
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
        response = client.post(f"/categories/", json=category_data)
        category_id = response.json()["id"]

        update_data = {
            "name": "Alimentação Editado",
            "description": "Nova descrição",
            "icon": "home",
            "color": "#000000"
        }

        # Act
        response = client.put(f"/categories/{category_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["icon"] == update_data["icon"]
        assert data["color"] == update_data["color"]
