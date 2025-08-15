
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

class CategoryType(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: str = "category"
    color: str = "#1976d2"
    type: CategoryType

    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Nome da categoria não pode estar vazio')
        if len(v) > 50:
            raise ValueError('Nome da categoria deve ter no máximo 50 caracteres')
        return v.strip()

    @validator('color')
    def validate_color(cls, v):
        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return v

    @validator('icon')
    def validate_icon(cls, v):
        valid_icons = [
            'category', 'home', 'restaurant', 'commute', 'shopping_cart', 
            'local_activity', 'health_and_safety', 'school', 'work', 
            'monetization_on', 'show_chart', 'card_giftcard', 'directions_car', 
            'flight', 'directions_bus', 'directions_bike', 'coffee', 
            'local_grocery_store', 'local_pharmacy', 'local_hospital', 
            'medical_services', 'fitness_center', 'sports_esports', 'movie', 
            'music_note', 'book', 'luggage', 'hotel', 'credit_card'
        ]
        if v not in valid_icons:
            raise ValueError(f'Ícone deve ser um dos valores válidos: {", ".join(valid_icons)}')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Nome da categoria não pode estar vazio')
            if len(v) > 50:
                raise ValueError('Nome da categoria deve ter no máximo 50 caracteres')
            return v.strip()
        return v

    @validator('color')
    def validate_color(cls, v):
        if v is not None:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
                raise ValueError('Cor deve estar no formato hexadecimal (#RRGGBB)')
        return v

class Category(CategoryBase):
    id: UUID
    user_id: UUID
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryWithStats(Category):
    transaction_count: int = 0
    total_amount: float = 0.0
    percentage: float = 0.0

class CategoryList(BaseModel):
    categories: list[Category]
    total: int
    page: int
    per_page: int
    total_pages: int

class CategoryResponse(CategoryBase):
    id: UUID
    user_id: UUID
    is_default: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryWithTransactionCount(CategoryResponse):
    transaction_count: int
