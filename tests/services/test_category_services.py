
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from src.categories.services import CategoryService
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryType

class TestCategoryService:
    @pytest.fixture
    def category_service(self):
        return CategoryService()
    
    @pytest.fixture
    def mock_supabase(self):
        with patch('src.categories.services.supabase') as mock:
            yield mock
    
    def test_create_category_success(self, category_service, mock_supabase):
        # Arrange
        category_data = CategoryCreate(
            name="Alimentação",
            description="Gastos com comida",
            icon="food",
            color="#FF6B6B",
            type=CategoryType.EXPENSE
        )
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value = {
            'data': [{
                'id': 'category-123',
                'name': 'Alimentação',
                'type': 'expense',
                'is_default': False
            }],
            'error': None
        }
        
        # Act
        result = category_service.create_category(category_data)
        
        # Assert
        assert result.name == 'Alimentação'
        assert result.type == CategoryType.EXPENSE
        mock_supabase.table.assert_called_with('categories')
    
    def test_create_category_duplicate_name(self, category_service, mock_supabase):
        # Arrange
        category_data = CategoryCreate(
            name="Alimentação",
            type=CategoryType.EXPENSE
        )
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value = {
            'data': None,
            'error': {'message': 'duplicate key value violates unique constraint'}
        }
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            category_service.create_category(category_data)
        
        assert "duplicate key" in str(exc_info.value)
    
    def test_get_categories_by_user(self, category_service, mock_supabase):
        # Arrange
        user_id = "user-123"
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = {
            'data': [
                {'id': 'cat-1', 'name': 'Alimentação', 'type': 'expense'},
                {'id': 'cat-2', 'name': 'Salário', 'type': 'income'}
            ],
            'error': None
        }
        
        # Act
        result = category_service.get_categories_by_user(user_id)
        
        # Assert
        assert len(result) == 2
        assert result[0].name == 'Alimentação'
        assert result[1].name == 'Salário'
    
    def test_update_category_success(self, category_service, mock_supabase):
        # Arrange
        category_id = "category-123"
        update_data = CategoryUpdate(name="Nova Alimentação")
        
        mock_supabase.table.return_value.update.return_value.eq.return_value.select.return_value.single.return_value = {
            'data': {
                'id': 'category-123',
                'name': 'Nova Alimentação',
                'type': 'expense'
            },
            'error': None
        }
        
        # Act
        result = category_service.update_category(category_id, update_data)
        
        # Assert
        assert result.name == 'Nova Alimentação'
        mock_supabase.table.assert_called_with('categories')
    
    def test_delete_category_success(self, category_service, mock_supabase):
        # Arrange
        category_id = "category-123"
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = {
            'data': None,
            'error': None
        }
        
        # Act
        result = category_service.delete_category(category_id)
        
        # Assert
        assert result is True
        mock_supabase.table.assert_called_with('categories')
    
    def test_restore_category_success(self, category_service, mock_supabase):
        # Arrange
        category_id = "category-123"
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = {
            'data': None,
            'error': None
        }
        
        # Act
        result = category_service.restore_category(category_id)
        
        # Assert
        assert result is True
        mock_supabase.table.assert_called_with('categories')
