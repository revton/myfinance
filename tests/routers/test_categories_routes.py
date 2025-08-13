import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.auth.models import User
from uuid import uuid4
from datetime import datetime
from src.categories.models import CategoryResponse, CategoryWithTransactionCount, CategoryType

class TestCategoriesEndpoints:

    @patch('src.categories.routes.CategoryService')
    def test_create_category_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_data = {
            "name": "Test Category",
            "description": "Test Description",
            "icon": "home",
            "color": "#FFFFFF",
            "type": "expense"
        }
        mock_service = MockCategoryService.return_value
        mock_category_instance = CategoryResponse(
            id=uuid4(),
            user_id=user_id,
            name=category_data["name"],
            description=category_data["description"],
            icon=category_data["icon"],
            color=category_data["color"],
            type=CategoryType(category_data["type"]),
            is_default=False,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_service.create_category.return_value = mock_category_instance

        # Act
        response = client.post("/categories/", json=category_data)

        # Assert
        assert response.status_code == 201
        mock_service.create_category.assert_called_once()

    @patch('src.categories.routes.CategoryService')
    def test_get_categories_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        mock_service = MockCategoryService.return_value
        mock_category_list = [
            CategoryWithTransactionCount(
                id=uuid4(),
                user_id=user_id,
                name="Category 1",
                description="Desc 1",
                icon="home",
                color="#000000",
                type=CategoryType.EXPENSE,
                is_default=False,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                transaction_count=0,
                total_amount=0.0,
                percentage=0.0
            ),
            CategoryWithTransactionCount(
                id=uuid4(),
                user_id=user_id,
                name="Category 2",
                description="Desc 2",
                icon="food",
                color="#111111",
                type=CategoryType.INCOME,
                is_default=False,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                transaction_count=0,
                total_amount=0.0,
                percentage=0.0
            )
        ]
        mock_service.get_categories.return_value = mock_category_list

        # Act
        response = client.get("/categories/")

        # Assert
        assert response.status_code == 200

    @patch('src.categories.routes.CategoryService')
    def test_get_category_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_id = uuid4()
        mock_service = MockCategoryService.return_value
        mock_category_instance = CategoryResponse(
            id=category_id,
            user_id=user_id,
            name="Test Category",
            description="Test Description",
            icon="home",
            color="#FFFFFF",
            type=CategoryType.EXPENSE,
            is_default=False,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_service.get_category.return_value = mock_category_instance

        # Act
        response = client.get(f"/categories/{category_id}")

        # Assert
        assert response.status_code == 200

    @patch('src.categories.routes.CategoryService')
    def test_update_category_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_id = uuid4()
        update_data = {"name": "Updated Name"}
        mock_service = MockCategoryService.return_value
        mock_category_instance = CategoryResponse(
            id=category_id,
            user_id=user_id,
            name=update_data["name"],
            description="Original Description",
            icon="home",
            color="#FFFFFF",
            type=CategoryType.EXPENSE,
            is_default=False,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        mock_service.update_category.return_value = mock_category_instance

        # Act
        response = client.put(f"/categories/{category_id}", json=update_data)

        # Assert
        assert response.status_code == 200

    @patch('src.categories.routes.CategoryService')
    def test_delete_category_success(self, MockCategoryService, authenticated_client: tuple):
        # Arrange
        client, user_id = authenticated_client
        category_id = uuid4()
        mock_service = MockCategoryService.return_value
        mock_service.delete_category.return_value = True

        # Act
        response = client.delete(f"/categories/{category_id}")

        # Assert
        assert response.status_code == 200