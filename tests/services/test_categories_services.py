
import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from src.categories.services import CategoryService
from src.categories.models import CategoryCreate, CategoryUpdate
from src.database import Category, Transaction

@pytest.fixture
def mock_db_session():
    return MagicMock()

class TestCategoryService:
    def test_create_category(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        service = CategoryService(mock_db_session, user_id)
        category_data = CategoryCreate(
            name="Test Category",
            description="Test Description",
            icon="home",
            color="#FFFFFF",
            type="expense"
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        service.create_category(category_data)

        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_get_categories(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        service = CategoryService(mock_db_session, user_id)

        # Act
        service.get_categories()

        # Assert
        mock_db_session.query.assert_called_once()

    def test_get_category(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        service = CategoryService(mock_db_session, user_id)
        category_id = uuid4()

        # Act
        service.get_category(category_id)

        # Assert
        mock_db_session.query.assert_called_once()

    def test_update_category(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        service = CategoryService(mock_db_session, user_id)
        category_id = uuid4()
        category_data = CategoryUpdate(name="Updated Name")
        mock_category = MagicMock()
        mock_category.name = "Old Name"
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [mock_category, None]

        # Act
        service.update_category(category_id, category_data)

        # Assert
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_delete_category(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        service = CategoryService(mock_db_session, user_id)
        category_id = uuid4()
        mock_category = MagicMock()
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_category
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0

        # Act
        service.delete_category(category_id)

        # Assert
        assert not mock_category.is_active
        mock_db_session.commit.assert_called_once()
