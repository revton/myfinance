import pytest
from unittest.mock import MagicMock, patch, ANY
from uuid import uuid4
from src.categories.services import CategoryService
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryType
from src.database import Category, Transaction
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime

class TestCategoryService:

    @pytest.fixture
    def mock_db_session(self):
        return MagicMock(spec=Session)

    def test_create_category_success(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        category_data = CategoryCreate(
            name="Alimentação",
            description="Gastos com comida",
            icon="food",
            color="#FF6B6B",
            type=CategoryType.EXPENSE
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = category_service.create_category(category_data)

        # Assert
        assert result.name == 'Alimentação'
        assert result.type == CategoryType.EXPENSE
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_create_category_duplicate_name(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        category_data = CategoryCreate(
            name="Alimentação",
            type=CategoryType.EXPENSE
        )
        mock_db_session.query.return_value.filter.return_value.first.return_value = Category(id=uuid4(), name="Alimentação", user_id=user_id, type=CategoryType.EXPENSE, is_default=False, is_active=True, created_at=datetime.now(), updated_at=datetime.now())

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            category_service.create_category(category_data)

        assert "Já existe uma categoria com o nome 'Alimentação'" in str(exc_info.value)

    @patch('src.categories.services.func')
    def test_get_categories(self, mock_func, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        mock_categories = [
            (Category(id=uuid4(), name='Alimentação', type='expense', user_id=user_id, is_default=False, is_active=True, created_at=datetime.now(), updated_at=datetime.now()), 0),
            (Category(id=uuid4(), name='Salário', type='income', user_id=user_id, is_default=False, is_active=True, created_at=datetime.now(), updated_at=datetime.now()), 0)
        ]
        
        # Mock func.count().label()
        mock_count_result = MagicMock()
        mock_func.count.return_value = mock_count_result
        mock_count_result.label.return_value = "mocked_transaction_count_label" # This can be any unique identifier

        mock_query = mock_db_session.query.return_value
        mock_outerjoin = mock_query.outerjoin.return_value
        mock_filtered_1 = mock_outerjoin.filter.return_value
        mock_filtered_2 = mock_filtered_1.filter.return_value
        mock_group_by = mock_filtered_2.group_by.return_value
        mock_ordered = mock_group_by.order_by.return_value
        mock_ordered.all.return_value = mock_categories

        # Act
        result = category_service.get_categories()

        # Assert
        mock_func.count.assert_called_once_with(Transaction.id)
        mock_count_result.label.assert_called_once_with('transaction_count')
        mock_db_session.query.assert_called_once_with(Category, "mocked_transaction_count_label")
        mock_query.outerjoin.assert_called_once_with(Transaction, ANY)
        mock_outerjoin.filter.assert_called_with(ANY)
        mock_filtered_1.filter.assert_called_with(ANY)
        mock_filtered_2.group_by.assert_called_once_with(Category.id)
        mock_group_by.order_by.assert_called_once_with(Category.name)
        mock_ordered.all.assert_called_once()
        assert len(result) == 2
        assert result[0].name == 'Alimentação'
        assert result[1].name == 'Salário'

    def test_update_category_success(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        update_data = CategoryUpdate(name="Nova Alimentação")
        mock_category = Category(id=category_id, name="Alimentação", user_id=user_id, type=CategoryType.EXPENSE, is_default=False, is_active=True, created_at=datetime.now(), updated_at=datetime.now())
        
        mock_db_session.query.return_value.filter.return_value.first.side_effect = [
            mock_category,
            None
        ]

        # Act
        result = category_service.update_category(category_id, update_data)

        # Assert
        assert result.name == 'Nova Alimentação'
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()

    def test_delete_category_success(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        mock_category = Category(id=category_id, name="Alimentação", user_id=user_id, type=CategoryType.EXPENSE, is_default=False, is_active=True, created_at=datetime.now(), updated_at=datetime.now())
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_category
        mock_db_session.query.return_value.filter.return_value.count.return_value = 0

        # Act
        result = category_service.delete_category(category_id)

        # Assert
        assert result is True
        mock_db_session.commit.assert_called_once()

    def test_restore_category_success(self, mock_db_session):
        # Arrange
        user_id = uuid4()
        category_id = uuid4()
        category_service = CategoryService(mock_db_session, user_id)
        mock_category = Category(id=category_id, name="Alimentação", user_id=user_id, type=CategoryType.EXPENSE, is_default=False, is_active=False, created_at=datetime.now(), updated_at=datetime.now())
        mock_db_session.query.return_value.filter.return_value.first.return_value = mock_category

        # Act
        result = category_service.restore_category(category_id)

        # Assert
        assert result.is_active is True
        mock_db_session.commit.assert_called_once()