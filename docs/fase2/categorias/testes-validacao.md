# 🧪 Testes e Validação - Sistema de Categorias

## 🎯 **Visão Geral**

Este documento descreve a estratégia de testes e validação para o sistema de categorias, incluindo testes unitários, de integração, end-to-end e validações de negócio.

## 🧪 **Estratégia de Testes**

### **Pirâmide de Testes**

```
    /\
   /  \     E2E Tests (Poucos)
  /____\    
 /      \   Integration Tests (Alguns)
/________\  Unit Tests (Muitos)
```

### **Cobertura de Testes**

- **Testes Unitários**: 95% de cobertura
- **Testes de Integração**: 85% de cobertura
- **Testes E2E**: Cenários críticos
- **Testes de Validação**: 100% dos modelos

## 🔧 **Testes Unitários**

### **1. Testes do CategoryService**

```python
# tests/services/test_category_service.py
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from app.services.category_service import CategoryService
from app.models.category import CategoryCreate, CategoryUpdate, CategoryType

class TestCategoryService:
    @pytest.fixture
    def category_service(self):
        return CategoryService()
    
    @pytest.fixture
    def mock_supabase(self):
        with patch('app.services.category_service.supabase') as mock:
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
```

### **2. Testes dos Modelos Pydantic**

```python
# tests/models/test_category_models.py
import pytest
from pydantic import ValidationError
from app.models.category import CategoryCreate, CategoryUpdate, CategoryType

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
```

### **3. Testes dos Endpoints**

```python
# tests/api/test_category_endpoints.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

class TestCategoryEndpoints:
    @patch('app.services.category_service.CategoryService.create_category')
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
    
    @patch('app.services.category_service.CategoryService.get_categories_by_user')
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
    
    @patch('app.services.category_service.CategoryService.update_category')
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
    
    @patch('app.services.category_service.CategoryService.delete_category')
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
```

## 🔗 **Testes de Integração**

### **1. Testes de Integração com Supabase**

```python
# tests/integration/test_category_supabase_integration.py
import pytest
from app.services.category_service import CategoryService
from app.database import get_supabase_client

class TestCategorySupabaseIntegration:
    @pytest.fixture
    def category_service(self):
        return CategoryService()
    
    @pytest.fixture
    def supabase_client(self):
        return get_supabase_client()
    
    def test_category_crud_flow(self, category_service, supabase_client):
        """Testa o fluxo completo de CRUD de categorias"""
        # Arrange
        user_id = "test-user-123"
        
        # Act - Criar categoria
        category_data = {
            "name": "Test Category",
            "description": "Test Description",
            "icon": "category",
            "color": "#1976d2",
            "type": "expense"
        }
        
        created_category = category_service.create_category(category_data)
        
        # Assert - Verificar se foi criada
        assert created_category.name == "Test Category"
        assert created_category.type == "expense"
        
        # Act - Buscar categorias do usuário
        user_categories = category_service.get_categories_by_user(user_id)
        
        # Assert - Verificar se a categoria está na lista
        assert any(cat.name == "Test Category" for cat in user_categories)
        
        # Act - Atualizar categoria
        update_data = {
            "name": "Updated Test Category",
            "description": "Updated Description"
        }
        
        updated_category = category_service.update_category(created_category.id, update_data)
        
        # Assert - Verificar se foi atualizada
        assert updated_category.name == "Updated Test Category"
        assert updated_category.description == "Updated Description"
        
        # Act - Excluir categoria (soft delete)
        delete_result = category_service.delete_category(created_category.id)
        
        # Assert - Verificar se foi excluída
        assert delete_result is True
        
        # Act - Restaurar categoria
        restore_result = category_service.restore_category(created_category.id)
        
        # Assert - Verificar se foi restaurada
        assert restore_result is True
    
    def test_default_categories_creation(self, category_service, supabase_client):
        """Testa a criação de categorias padrão"""
        # Arrange
        user_id = "test-user-456"
        
        # Act
        default_categories = category_service.create_default_categories(user_id)
        
        # Assert
        assert len(default_categories) == 16  # 10 despesas + 6 receitas
        
        # Verificar se todas são marcadas como padrão
        for category in default_categories:
            assert category.is_default is True
        
        # Verificar se temos categorias de ambos os tipos
        expense_categories = [c for c in default_categories if c.type == "expense"]
        income_categories = [c for c in default_categories if c.type == "income"]
        
        assert len(expense_categories) == 10
        assert len(income_categories) == 6
        
        # Verificar se as categorias principais existem
        category_names = [c.name for c in default_categories]
        assert "Alimentação" in category_names
        assert "Transporte" in category_names
        assert "Salário" in category_names
        assert "Investimentos" in category_names
```

### **2. Testes de Integração com Banco de Dados**

```python
# tests/integration/test_category_database_integration.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.category import Category
from app.services.category_service import CategoryService

class TestCategoryDatabaseIntegration:
    @pytest.fixture
    def engine(self):
        # Usar banco de dados de teste
        engine = create_engine("postgresql://test:test@localhost/test_db")
        Base.metadata.create_all(bind=engine)
        yield engine
        Base.metadata.drop_all(bind=engine)
    
    @pytest.fixture
    def session(self, engine):
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        yield session
        session.close()
    
    @pytest.fixture
    def category_service(self, session):
        return CategoryService(session)
    
    def test_category_persistence(self, category_service, session):
        """Testa a persistência de categorias no banco"""
        # Arrange
        category_data = {
            "user_id": "test-user-123",
            "name": "Test Category",
            "description": "Test Description",
            "icon": "category",
            "color": "#1976d2",
            "type": "expense",
            "is_default": False
        }
        
        # Act
        category = category_service.create_category(category_data)
        
        # Assert
        assert category.id is not None
        assert category.name == "Test Category"
        
        # Verificar no banco
        db_category = session.query(Category).filter_by(id=category.id).first()
        assert db_category is not None
        assert db_category.name == "Test Category"
        assert db_category.type == "expense"
    
    def test_category_update_persistence(self, category_service, session):
        """Testa a atualização de categorias no banco"""
        # Arrange - Criar categoria primeiro
        category_data = {
            "user_id": "test-user-456",
            "name": "Original Name",
            "type": "expense"
        }
        
        category = category_service.create_category(category_data)
        
        # Act - Atualizar categoria
        update_data = {
            "name": "Updated Name",
            "description": "Updated Description"
        }
        
        updated_category = category_service.update_category(category.id, update_data)
        
        # Assert
        assert updated_category.name == "Updated Name"
        assert updated_category.description == "Updated Description"
        
        # Verificar no banco
        db_category = session.query(Category).filter_by(id=category.id).first()
        assert db_category.name == "Updated Name"
        assert db_category.description == "Updated Description"
    
    def test_category_soft_delete(self, category_service, session):
        """Testa o soft delete de categorias"""
        # Arrange - Criar categoria
        category_data = {
            "user_id": "test-user-789",
            "name": "To Delete",
            "type": "expense"
        }
        
        category = category_service.create_category(category_data)
        
        # Act - Excluir categoria
        result = category_service.delete_category(category.id)
        
        # Assert
        assert result is True
        
        # Verificar no banco que is_active = False
        db_category = session.query(Category).filter_by(id=category.id).first()
        assert db_category.is_active is False
        
        # Act - Restaurar categoria
        restore_result = category_service.restore_category(category.id)
        
        # Assert
        assert restore_result is True
        
        # Verificar no banco que is_active = True
        db_category = session.query(Category).filter_by(id=category.id).first()
        assert db_category.is_active is True
```

## 🌐 **Testes End-to-End**

### **1. Testes E2E com Playwright**

```typescript
// tests/e2e/categories.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Category Management', () => {
  test('should create new category successfully', async ({ page }) => {
    // Arrange - Login first
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'securepassword123');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/dashboard');

    // Act - Navigate to categories
    await page.click('[data-testid="categories-menu"]');
    await page.click('[data-testid="new-category-button"]');
    
    // Fill category form
    await page.fill('[data-testid="category-name-input"]', 'Test Category');
    await page.fill('[data-testid="category-description-input"]', 'Test Description');
    await page.selectOption('[data-testid="category-type-select"]', 'expense');
    await page.selectOption('[data-testid="category-icon-select"]', 'food');
    await page.selectOption('[data-testid="category-color-select"]', '#FF6B6B');
    
    await page.click('[data-testid="save-category-button"]');

    // Assert
    await expect(page.locator('[data-testid="category-name"]')).toContainText('Test Category');
    await expect(page).toHaveURL('/categories');
  });

  test('should edit existing category successfully', async ({ page }) => {
    // Arrange - Login and navigate to categories
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'securepassword123');
    await page.click('[data-testid="login-button"]');
    
    await page.click('[data-testid="categories-menu"]');

    // Act - Edit first category
    await page.click('[data-testid="edit-category-button"]');
    await page.fill('[data-testid="category-name-input"]', 'Updated Category');
    await page.click('[data-testid="save-category-button"]');

    // Assert
    await expect(page.locator('[data-testid="category-name"]')).toContainText('Updated Category');
  });

  test('should delete category successfully', async ({ page }) => {
    // Arrange - Login and navigate to categories
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'securepassword123');
    await page.click('[data-testid="login-button"]');
    
    await page.click('[data-testid="categories-menu"]');

    // Act - Delete category
    await page.click('[data-testid="delete-category-button"]');
    await page.click('[data-testid="confirm-delete-button"]');

    // Assert
    await expect(page.locator('[data-testid="success-message"]')).toContainText('Categoria excluída com sucesso');
  });

  test('should filter categories by type', async ({ page }) => {
    // Arrange - Login and navigate to categories
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'securepassword123');
    await page.click('[data-testid="login-button"]');
    
    await page.click('[data-testid="categories-menu"]');

    // Act - Filter by expense type
    await page.click('[data-testid="expense-tab"]');

    // Assert
    await expect(page.locator('[data-testid="category-type"]')).toContainText('Despesa');
    
    // Act - Filter by income type
    await page.click('[data-testid="income-tab"]');

    // Assert
    await expect(page.locator('[data-testid="category-type"]')).toContainText('Receita');
  });
});
```

### **2. Testes de API E2E**

```python
# tests/e2e/test_category_api_e2e.py
import pytest
import requests
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestCategoryAPIE2E:
    def test_complete_category_flow(self):
        """Testa o fluxo completo de gerenciamento de categorias via API"""
        # 1. Criar categoria
        category_data = {
            "name": "E2E Test Category",
            "description": "Category for E2E testing",
            "icon": "category",
            "color": "#1976d2",
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        create_response = client.post("/categories/", json=category_data, headers=headers)
        assert create_response.status_code == 201
        
        created_category = create_response.json()
        category_id = created_category["id"]
        assert created_category["name"] == "E2E Test Category"
        
        # 2. Buscar categorias
        get_response = client.get("/categories/", headers=headers)
        assert get_response.status_code == 200
        
        categories = get_response.json()
        assert any(cat["name"] == "E2E Test Category" for cat in categories)
        
        # 3. Buscar categoria específica
        get_one_response = client.get(f"/categories/{category_id}", headers=headers)
        assert get_one_response.status_code == 200
        
        category = get_one_response.json()
        assert category["name"] == "E2E Test Category"
        
        # 4. Atualizar categoria
        update_data = {
            "name": "Updated E2E Category",
            "description": "Updated description"
        }
        
        update_response = client.put(f"/categories/{category_id}", json=update_data, headers=headers)
        assert update_response.status_code == 200
        
        updated_category = update_response.json()
        assert updated_category["name"] == "Updated E2E Category"
        
        # 5. Excluir categoria
        delete_response = client.delete(f"/categories/{category_id}", headers=headers)
        assert delete_response.status_code == 204
        
        # 6. Verificar que a categoria foi excluída
        get_deleted_response = client.get(f"/categories/{category_id}", headers=headers)
        assert get_deleted_response.status_code == 404
```

## 🔒 **Testes de Validação**

### **1. Testes de Validação de Dados**

```python
# tests/validation/test_category_validation.py
import pytest
from app.utils.category_validator import CategoryValidator

class TestCategoryValidation:
    def test_valid_category_name(self):
        """Testa nome de categoria válido"""
        validator = CategoryValidator()
        result = validator.validate_name("Alimentação")
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_invalid_category_name_empty(self):
        """Testa nome de categoria vazio"""
        validator = CategoryValidator()
        result = validator.validate_name("")
        
        assert result.is_valid is False
        assert "não pode estar vazio" in result.errors[0]
    
    def test_invalid_category_name_too_long(self):
        """Testa nome de categoria muito longo"""
        validator = CategoryValidator()
        result = validator.validate_name("A" * 51)
        
        assert result.is_valid is False
        assert "máximo de 50 caracteres" in result.errors[0]
    
    def test_invalid_category_name_special_chars(self):
        """Testa nome de categoria com caracteres especiais"""
        validator = CategoryValidator()
        result = validator.validate_name("Category<script>alert('xss')</script>")
        
        assert result.is_valid is False
        assert "caracteres especiais" in result.errors[0]
    
    def test_valid_category_color(self):
        """Testa cor de categoria válida"""
        validator = CategoryValidator()
        result = validator.validate_color("#FF6B6B")
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_invalid_category_color_format(self):
        """Testa formato de cor inválido"""
        validator = CategoryValidator()
        result = validator.validate_color("invalid-color")
        
        assert result.is_valid is False
        assert "formato hexadecimal" in result.errors[0]
    
    def test_invalid_category_color_short(self):
        """Testa cor muito curta"""
        validator = CategoryValidator()
        result = validator.validate_color("#FF6")
        
        assert result.is_valid is False
        assert "formato hexadecimal" in result.errors[0]
    
    def test_valid_category_icon(self):
        """Testa ícone de categoria válido"""
        validator = CategoryValidator()
        result = validator.validate_icon("food")
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_invalid_category_icon(self):
        """Testa ícone de categoria inválido"""
        validator = CategoryValidator()
        result = validator.validate_icon("invalid-icon")
        
        assert result.is_valid is False
        assert "valores válidos" in result.errors[0]
```

### **2. Testes de Validação de Negócio**

```python
# tests/validation/test_category_business_rules.py
import pytest
from app.services.category_service import CategoryService
from app.models.category import CategoryCreate, CategoryType

class TestCategoryBusinessRules:
    @pytest.fixture
    def category_service(self):
        return CategoryService()
    
    def test_cannot_delete_default_category(self, category_service):
        """Testa que não é possível excluir categorias padrão"""
        # Arrange
        default_category_id = "default-category-123"
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            category_service.delete_category(default_category_id)
        
        assert "categoria padrão" in str(exc_info.value).lower()
    
    def test_cannot_update_default_category_name(self, category_service):
        """Testa que não é possível alterar o nome de categorias padrão"""
        # Arrange
        default_category_id = "default-category-123"
        update_data = {"name": "New Name"}
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            category_service.update_category(default_category_id, update_data)
        
        assert "categoria padrão" in str(exc_info.value).lower()
    
    def test_cannot_create_duplicate_category_name(self, category_service):
        """Testa que não é possível criar categorias com nomes duplicados"""
        # Arrange
        category_data = CategoryCreate(
            name="Duplicate Category",
            type=CategoryType.EXPENSE
        )
        
        # Criar primeira categoria
        category_service.create_category(category_data)
        
        # Act & Assert - Tentar criar segunda categoria com mesmo nome
        with pytest.raises(Exception) as exc_info:
            category_service.create_category(category_data)
        
        assert "duplicado" in str(exc_info.value).lower()
    
    def test_cannot_create_category_with_invalid_type(self, category_service):
        """Testa que não é possível criar categoria com tipo inválido"""
        # Arrange
        category_data = {
            "name": "Test Category",
            "type": "invalid_type"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            CategoryCreate(**category_data)
    
    def test_category_name_case_insensitive_duplicate(self, category_service):
        """Testa que nomes de categoria são case-insensitive para duplicatas"""
        # Arrange
        category_data1 = CategoryCreate(
            name="Test Category",
            type=CategoryType.EXPENSE
        )
        
        category_data2 = CategoryCreate(
            name="test category",  # Mesmo nome em minúsculas
            type=CategoryType.EXPENSE
        )
        
        # Criar primeira categoria
        category_service.create_category(category_data1)
        
        # Act & Assert - Tentar criar segunda categoria
        with pytest.raises(Exception) as exc_info:
            category_service.create_category(category_data2)
        
        assert "duplicado" in str(exc_info.value).lower()
```

## 📊 **Métricas de Qualidade**

### **1. Cobertura de Código**

```bash
# Executar testes com cobertura
pytest --cov=app --cov-report=html --cov-report=term-missing

# Resultado esperado:
# Name                           Stmts   Miss  Cover   Missing
# -------------------------------------------------------------
# app/services/category_service.py   45      2    96%   45-46
# app/models/category.py             32      0   100%
# app/api/category.py                28      1    96%   67
# app/utils/category_validator.py    25      0   100%
# -------------------------------------------------------------
# TOTAL                          130      3    98%
```

### **2. Métricas de Performance**

```python
# tests/performance/test_category_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCategoryPerformance:
    def test_create_category_response_time(self):
        """Testa tempo de resposta da criação de categoria"""
        category_data = {
            "name": "Performance Test Category",
            "description": "Category for performance testing",
            "icon": "category",
            "color": "#1976d2",
            "type": "expense"
        }
        
        headers = {"Authorization": "Bearer valid-token"}
        
        start_time = time.time()
        response = client.post("/categories/", json=category_data, headers=headers)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code in [201, 400]  # 201 = criado, 400 = erro de validação
        assert response_time < 1.0  # Deve responder em menos de 1 segundo
    
    def test_get_categories_response_time(self):
        """Testa tempo de resposta da busca de categorias"""
        headers = {"Authorization": "Bearer valid-token"}
        
        start_time = time.time()
        response = client.get("/categories/", headers=headers)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code in [200, 401]  # 200 = sucesso, 401 = não autorizado
        assert response_time < 0.5  # Deve responder em menos de 0.5 segundos
    
    def test_category_bulk_operations(self):
        """Testa performance de operações em lote"""
        headers = {"Authorization": "Bearer valid-token"}
        
        # Criar múltiplas categorias
        start_time = time.time()
        
        for i in range(10):
            category_data = {
                "name": f"Bulk Category {i}",
                "type": "expense"
            }
            response = client.post("/categories/", json=category_data, headers=headers)
            assert response.status_code in [201, 400]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Deve criar 10 categorias em menos de 5 segundos
        assert total_time < 5.0
        assert total_time / 10 < 0.5  # Média de 0.5s por categoria
```

## 🚀 **Automação de Testes**

### **1. GitHub Actions para Testes de Categorias**

```yaml
# .github/workflows/test-categories.yml
name: Category Tests

on:
  push:
    branches: [ main, develop ]
    paths: [ 'app/services/category_service.py', 'app/models/category.py', 'app/api/category.py' ]
  pull_request:
    branches: [ main ]
    paths: [ 'app/services/category_service.py', 'app/models/category.py', 'app/api/category.py' ]

jobs:
  test-categories:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run category unit tests
      run: |
        pytest tests/services/test_category_service.py --cov=app.services.category_service --cov-report=xml
    
    - name: Run category integration tests
      run: |
        pytest tests/integration/test_category_supabase_integration.py --cov=app.services.category_service --cov-report=xml
    
    - name: Run category validation tests
      run: |
        pytest tests/validation/ --cov=app.utils.category_validator --cov-report=xml
    
    - name: Run category performance tests
      run: |
        pytest tests/performance/test_category_performance.py -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### **2. Scripts de Teste Específicos**

```bash
#!/bin/bash
# scripts/test-categories.sh

echo "🧪 Executando testes do sistema de categorias..."

# Executar testes unitários de categorias
echo "📦 Testes Unitários de Categorias..."
pytest tests/services/test_category_service.py -v --tb=short

# Executar testes de modelos
echo "📋 Testes de Modelos de Categorias..."
pytest tests/models/test_category_models.py -v --tb=short

# Executar testes de endpoints
echo "🌐 Testes de Endpoints de Categorias..."
pytest tests/api/test_category_endpoints.py -v --tb=short

# Executar testes de integração
echo "🔗 Testes de Integração de Categorias..."
pytest tests/integration/test_category_supabase_integration.py -v --tb=short

# Executar testes de validação
echo "✅ Testes de Validação de Categorias..."
pytest tests/validation/ -v --tb=short

# Executar testes de performance
echo "⚡ Testes de Performance de Categorias..."
pytest tests/performance/test_category_performance.py -v --tb=short

# Gerar relatório de cobertura específico
echo "📊 Gerando relatório de cobertura de categorias..."
pytest --cov=app.services.category_service --cov=app.models.category --cov=app.api.category --cov-report=html --cov-report=term-missing

echo "✅ Todos os testes de categorias concluídos!"
```

Esta estratégia de testes garante que o sistema de categorias seja robusto, seguro e confiável, com cobertura abrangente de todos os cenários críticos e validações de negócio. 