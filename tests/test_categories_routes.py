from fastapi.testclient import TestClient

class TestCategoriesRoutes:
    def test_create_category_success(self, authenticated_client: TestClient):
        """Testa a criação de uma categoria com sucesso"""
        # Arrange
        category_data = {
            "name": "Alimentação",
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF5733",
            "type": "expense"
        }

        # Act
        response = authenticated_client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == category_data["name"]
        assert data["description"] == category_data["description"]
        assert "id" in data
        assert "user_id" in data

    def test_create_category_invalid_data(self, authenticated_client: TestClient):
        """Testa a criação de uma categoria com dados inválidos"""
        # Arrange
        category_data = {
            "name": "",  # Invalid name
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF5733",
            "type": "expense"
        }

        # Act
        response = authenticated_client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 422
