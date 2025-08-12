
import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from src.categories.services import CategoryService
from src.categories.models import CategoryCreate, CategoryUpdate

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def category_service(mock_db_session):
    user_id = uuid4()
    return CategoryService(mock_db_session, user_id)

class TestCategoryService:
    def test_create_category(self, category_service, mock_db_session):
        # Arrange
        category_data = CategoryCreate(
            name="Test Category",
            description="Test Description",
            icon="home",
            color="#FFFFFF",
            type="expense"
        )

        # Act
        category_service.create_category(category_data)

        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_get_categories(self, category_service, mock_db_session):
        # Act
        category_service.get_categories()

        # Assert
        mock_db_session.query.assert_called_once()

    def test_get_category(self, category_service, mock_db_session):
        # Arrange
        category_id = uuid4()

        # Act
        category_service.get_category(category_id)

        # Assert
        mock_db_session.query.assert_called_once()

    def test_update_category(self, category_service, mock_db_session):
        # Arrange
        category_id = uuid4()
        category_data = CategoryUpdate(name="Updated Name")
        mock_category = MagicMock()
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_category

        # Act
        category_service.update_category(category_id, category_data)

        # Assert
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_delete_category(self, category_service, mock_db_session):
        # Arrange
        category_id = uuid4()
        mock_category = MagicMock()
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_category

        # Act
        category_service.delete_category(category_id)

        # Assert
        mock_db_session.commit.assert_called_once()
