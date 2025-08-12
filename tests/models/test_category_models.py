import pytest
from pydantic import ValidationError
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryType

class TestCategoryCreate:
    def test_valid_category_create(self):
        # Arrange & Act
        category_data = CategoryCreate(
            name="Alimentação",
            description="Gastos com comida",
            icon="food",
            color="#FF6B6B",
            type=CategoryType.EXPENSE
        )
        
        # Assert
        assert category_data.name == "Alimentação"
        assert category_data.description == "Gastos com comida"
        assert category_data.icon == "food"
        assert category_data.color == "#FF6B6B"
        assert category_data.type == CategoryType.EXPENSE
    
    def test_invalid_name_empty(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreate(
                name="",
                type=CategoryType.EXPENSE
            )
        
        assert "name" in str(exc_info.value)
    
    def test_invalid_name_too_long(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreate(
                name="A" * 51,  # 51 caracteres
                type=CategoryType.EXPENSE
            )
        
        assert "name" in str(exc_info.value)
    
    def test_invalid_color_format(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreate(
                name="Alimentação",
                color="invalid-color",
                type=CategoryType.EXPENSE
            )
        
        assert "color" in str(exc_info.value)
    
    def test_invalid_icon(self):
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            CategoryCreate(
                name="Alimentação",
                icon="invalid-icon",
                type=CategoryType.EXPENSE
            )
        
        assert "icon" in str(exc_info.value)

class TestCategoryUpdate:
    def test_valid_category_update(self):
        # Arrange & Act
        update_data = CategoryUpdate(
            name="Nova Alimentação",
            description="Novos gastos com comida"
        )
        
        # Assert
        assert update_data.name == "Nova Alimentação"
        assert update_data.description == "Novos gastos com comida"
    
    def test_partial_update(self):
        # Arrange & Act
        update_data = CategoryUpdate(name="Nova Alimentação")
        
        # Assert
        assert update_data.name == "Nova Alimentação"
        assert update_data.description is None
        assert update_data.icon is None
