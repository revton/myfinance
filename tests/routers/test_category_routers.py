import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.auth.models import User
from uuid import uuid4, UUID # Import UUID
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryType

class TestCategoryEndpoints:

    @patch('src.categories.routes.CategoryService')
    def test_create_category_endpoint_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_data = {
            "name": "Alimentação",
            "description": "Gastos com comida",
            "icon": "restaurant",
            "color": "#FF6B6B",
            "type": "expense"
        }
        mock_service = MockCategoryService.return_value

        # Create a mock Category object that resembles the actual model
        mock_category_instance = MagicMock()
        mock_category_instance.id = str(uuid4())
        mock_category_instance.name = category_data["name"]
        mock_category_instance.description = category_data["description"]
        mock_category_instance.icon = category_data["icon"]
        mock_category_instance.color = category_data["color"]
        mock_category_instance.type = category_data["type"]
        mock_category_instance.user_id = str(user_id) # Add user_id

        mock_service.create_category.return_value = mock_category_instance

        # Act
        response = client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 201
        # Assert that the response body matches the mock category data
        response_json = response.json()
        assert response_json["name"] == category_data["name"]
        assert response_json["description"] == category_data["description"]
        assert response_json["icon"] == category_data["icon"]
        assert response_json["color"] == category_data["color"]
        assert response_json["type"] == category_data["type"]
        assert "id" in response_json # Ensure ID is present
        assert response_json["user_id"] == str(user_id) # Assert user_id

        # Create an instance of CategoryCreate for assertion
        expected_category_create = CategoryCreate(
            name=category_data["name"],
            description=category_data["description"],
            icon=category_data["icon"],
            color=category_data["color"],
            type=CategoryType(category_data["type"]) # Convert string to enum
        )
        # Removed user_id from assert_called_once_with
        mock_service.create_category.assert_called_once_with(expected_category_create)

    def test_create_category_endpoint_invalid_data(self, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_data = {
            "name": "",  # Nome vazio
            "type": "expense"
        }

        # Act
        response = client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 422

    @patch('src.categories.routes.CategoryService')
    def test_get_categories_endpoint_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        mock_service = MockCategoryService.return_value

        # Create mock Category objects
        mock_category_1 = MagicMock()
        mock_category_1.id = str(uuid4())
        mock_category_1.name = "Alimentação"
        mock_category_1.description = "Gastos com comida"
        mock_category_1.icon = "restaurant"
        mock_category_1.color = "#FF6B6B"
        mock_category_1.type = "expense"
        mock_category_1.user_id = str(user_id) # Add user_id

        mock_category_2 = MagicMock()
        mock_category_2.id = str(uuid4())
        mock_category_2.name = "Salário"
        mock_category_2.description = "Recebimento de salário"
        mock_category_2.icon = "credit_card" # Changed to a valid icon
        mock_category_2.color = "#6BFF6B"
        mock_category_2.type = "income"
        mock_category_2.user_id = str(user_id) # Add user_id

        mock_service.get_categories.return_value = [mock_category_1, mock_category_2]

        # Act
        response = client.get("/categories/")

        # Assert
        assert response.status_code == 200
        response_json = response.json()
        assert len(response_json) == 2
        assert response_json[0]["name"] == "Alimentação"
        assert response_json[1]["name"] == "Salário"
        assert response_json[0]["user_id"] == str(user_id) # Assert user_id
        assert response_json[1]["user_id"] == str(user_id) # Assert user_id
        # Removed user_id from assert_called_once_with
        mock_service.get_categories.assert_called_once_with(include_inactive=False, category_type=None)


    @patch('src.categories.routes.CategoryService')
    def test_update_category_endpoint_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_id = uuid4() # Keep as UUID object
        update_data = {
            "name": "Nova Alimentação",
            "description": "Novos gastos",
            "icon": "restaurant", # Changed to a valid icon
            "color": "#ABCDEF",
            "type": "expense"
        }
        mock_service = MockCategoryService.return_value

        # Create a mock Category object for the updated category
        mock_updated_category = MagicMock()
        mock_updated_category.id = str(category_id) # Store as string for mock
        mock_updated_category.name = update_data["name"]
        mock_updated_category.description = update_data["description"]
        mock_updated_category.icon = update_data["icon"]
        mock_updated_category.color = update_data["color"]
        mock_updated_category.type = update_data["type"]
        mock_updated_category.user_id = str(user_id) # Add user_id

        mock_service.update_category.return_value = mock_updated_category

        # Act
        response = client.put(f"/categories/{category_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["name"] == update_data["name"]
        assert response_json["description"] == update_data["description"]
        assert response_json["icon"] == update_data["icon"]
        assert response_json["color"] == update_data["color"]
        assert response_json["type"] == update_data["type"]
        assert response_json["user_id"] == str(user_id) # Assert user_id

        # Create an instance of CategoryUpdate for assertion
        expected_update_data = CategoryUpdate(
            name=update_data["name"],
            description=update_data["description"],
            icon=update_data["icon"],
            color=update_data["color"],
            type=CategoryType(update_data["type"]) # Convert string to enum
        )
        # Pass category_id as UUID object
        mock_service.update_category.assert_called_once_with(category_id, expected_update_data)

    @patch('src.categories.routes.CategoryService')
    def test_delete_category_endpoint_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_id = uuid4() # Keep as UUID object
        mock_service = MockCategoryService.return_value
        mock_service.delete_category.return_value = True

        # Act
        response = client.delete(f"/categories/{category_id}")

        # Assert
        assert response.status_code == 200 # Changed from 204 to 200
        # Pass category_id as UUID object
        mock_service.delete_category.assert_called_once_with(category_id)