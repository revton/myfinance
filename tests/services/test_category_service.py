import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.categories.services import CategoryService
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryType
import uuid
from datetime import datetime

class TestCategoryService:
    @pytest.fixture
    def mock_supabase_client(self):
        with patch('src.categories.services.get_supabase_client') as mock:
            yield mock.return_value

    @pytest.fixture
    def category_service(self, mock_supabase_client):
        return CategoryService()

    def test_create_category_success(self, category_service, mock_supabase_client):
        # Arrange
        category_data = CategoryCreate(
            name="Alimentação",
            description="Gastos com comida",
            icon="food",
            color="#FF6B6B",
            type=CategoryType.EXPENSE
        )
        
        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = Mock(
            data=[{
                'id': uuid.uuid4(),
                'name': 'Alimentação',
                'type': 'expense',
                'is_default': False,
                'description': 'Gastos com comida',
                'icon': 'food',
                'color': '#FF6B6B',
                'user_id': uuid.uuid4(),
                'is_active': True,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }],
            error=None
        )
        
        # Act
        result = category_service.create_category(category_data)
        
        # Assert
        assert result.name == 'Alimentação'
        assert result.type == CategoryType.EXPENSE
        mock_supabase_client.table.assert_called_with('categories')
    
    def test_create_category_duplicate_name(self, category_service, mock_supabase_client):
        # Arrange
        category_data = CategoryCreate(
            name="Alimentação",
            type=CategoryType.EXPENSE
        )
        
        mock_supabase_client.table.return_value.insert.return_value.execute.return_value = Mock(
            data=None,
            error=Mock(message='duplicate key value violates unique constraint')
        )
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            category_service.create_category(category_data)
        
        assert "duplicate key" in str(exc_info.value)
    
    def test_get_categories_by_user(self, category_service, mock_supabase_client):
        # Arrange
        user_id = uuid.uuid4()
        mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value = Mock(
            data=[
                {
                    'id': uuid.uuid4(), 'name': 'Alimentação', 'type': 'expense', 'is_default': False, 
                    'description': '', 'icon': 'food', 'color': '#FF6B6B', 'user_id': user_id, 'is_active': True, 
                    'created_at': datetime.now(), 'updated_at': datetime.now()
                },
                {
                    'id': uuid.uuid4(), 'name': 'Salário', 'type': 'income', 'is_default': False,
                    'description': '', 'icon': 'work', 'color': '#32CD32', 'user_id': user_id, 'is_active': True,
                    'created_at': datetime.now(), 'updated_at': datetime.now()
                }
            ],
            error=None
        )
        
        # Act
        result = category_service.get_categories_by_user(user_id)
        
        # Assert
        assert len(result) == 2
        assert result[0].name == 'Alimentação'
        assert result[1].name == 'Salário'
    
    def test_update_category_success(self, category_service, mock_supabase_client):
        # Arrange
        category_id = uuid.uuid4()
        update_data = CategoryUpdate(name="Nova Alimentação")
        
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.select.return_value.single.return_value.execute.return_value = Mock(
            data={
                'id': category_id,
                'name': 'Nova Alimentação',
                'type': 'expense',
                'is_default': False,
                'description': '', 'icon': 'food', 'color': '#FF6B6B', 'user_id': uuid.uuid4(), 'is_active': True,
                'created_at': datetime.now(), 'updated_at': datetime.now()
            },
            error=None
        )
        
        # Act
        result = category_service.update_category(category_id, update_data)
        
        # Assert
        assert result.name == 'Nova Alimentação'
        mock_supabase_client.table.assert_called_with('categories')
    
    def test_delete_category_success(self, category_service, mock_supabase_client):
        # Arrange
        category_id = uuid.uuid4()
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock(
            data=None,
            error=None
        )
        
        # Act
        result = category_service.delete_category(category_id)
        
        # Assert
        assert result is True
        mock_supabase_client.table.assert_called_with('categories')
    
    def test_restore_category_success(self, category_service, mock_supabase_client):
        # Arrange
        category_id = uuid.uuid4()
        mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock(
            data=None,
            error=None
        )
        
        # Act
        result = category_service.restore_category(category_id)
        
        # Assert
        assert result is True
        mock_supabase_client.table.assert_called_with('categories')