
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app

client = TestClient(app)

class TestCategoryEndpoints:
    @patch('src.categories.services.CategoryService.create_category')
    def test_create_category_endpoint_success(self, mock_create):
        # Arrange
        category_data = {
            "name": "Alimentação",
            "description": "Gastos com comida",
            "icon": "food",
            "color": "#FF6B6B",
            "type": "expense"
        }
        
        mock_create.return_value = {
            "id": "category-123",
            "name": "Alimentação",
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post("/categories/", json=category_data, headers=headers)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["name"] == "Alimentação"
        mock_create.assert_called_once()
    
    def test_create_category_endpoint_invalid_data(self):
        # Arrange
        category_data = {
            "name": "",  # Nome vazio
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.post("/categories/", json=category_data, headers=headers)
        
        # Assert
        assert response.status_code == 422
    
    @patch('src.categories.services.CategoryService.get_categories_by_user')
    def test_get_categories_endpoint_success(self, mock_get):
        # Arrange
        mock_get.return_value = [
            {"id": "cat-1", "name": "Alimentação", "type": "expense"},
            {"id": "cat-2", "name": "Salário", "type": "income"}
        ]
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.get("/categories/", headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "Alimentação"
    
    @patch('src.categories.services.CategoryService.update_category')
    def test_update_category_endpoint_success(self, mock_update):
        # Arrange
        category_id = "category-123"
        update_data = {
            "name": "Nova Alimentação",
            "description": "Novos gastos"
        }
        
        mock_update.return_value = {
            "id": "category-123",
            "name": "Nova Alimentação",
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.put(f"/categories/{category_id}", json=update_data, headers=headers)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["name"] == "Nova Alimentação"
        mock_update.assert_called_once()
    
    @patch('src.categories.services.CategoryService.delete_category')
    def test_delete_category_endpoint_success(self, mock_delete):
        # Arrange
        category_id = "category-123"
        mock_delete.return_value = True
        
        headers = {"Authorization": "Bearer valid-token"}
        
        # Act
        response = client.delete(f"/categories/{category_id}", headers=headers)
        
        # Assert
        assert response.status_code == 204
        mock_delete.assert_called_once()
