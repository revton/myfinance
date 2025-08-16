
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from uuid import UUID
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryWithTransactionCount
from src.database import Category, Transaction

class CategoryService:
    def __init__(self, db: Session, user_id: UUID):
        self.db = db
        self.user_id = user_id
    
    def get_categories(self, include_inactive: bool = False, category_type: Optional[str] = None) -> List[CategoryWithTransactionCount]:
        """Lista categorias com contagem de transações"""
        query = self.db.query(
            Category,
            func.count(Transaction.id).label('transaction_count')
        ).outerjoin(Transaction, Category.id == Transaction.category_id)
        
        if not include_inactive:
            query = query.filter(Category.is_active == True)
        
        # Filtrar por tipo se especificado
        if category_type:
            query = query.filter(Category.type == category_type)
        
        query = query.filter(Category.user_id == self.user_id)
        query = query.group_by(Category.id)
        query = query.order_by(Category.name)
        
        results = query.all()
        
        categories = []
        for category, transaction_count in results:
            category_dict = category.__dict__.copy()
            category_dict['transaction_count'] = transaction_count
            categories.append(CategoryWithTransactionCount(**category_dict))
        
        return categories
    
    def get_category(self, category_id: UUID) -> Optional[Category]:
        """Obtém uma categoria específica"""
        return self.db.query(Category).filter(
            and_(
                Category.id == category_id,
                Category.user_id == self.user_id,
                Category.is_active == True
            )
        ).first()
    
    def create_category(self, category_data: CategoryCreate) -> Category:
        """Cria uma nova categoria"""
        # Verificar se já existe categoria com mesmo nome
        existing = self.db.query(Category).filter(
            and_(
                Category.name == category_data.name,
                Category.user_id == self.user_id
            )
        ).first()
        
        if existing:
            raise ValueError(f"Já existe uma categoria com o nome '{category_data.name}'")
        
        category = Category(
            user_id=self.user_id,
            **category_data.dict()
        )
        
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def update_category(self, category_id: UUID, category_data: CategoryUpdate) -> Optional[Category]:
        """Atualiza uma categoria"""
        category = self.get_category(category_id)
        if not category:
            return None
        
        # Verificar se o novo nome já existe (se estiver sendo alterado)
        if category_data.name and category_data.name != category.name:
            existing = self.db.query(Category).filter(
                and_(
                    Category.name == category_data.name,
                    Category.user_id == self.user_id,
                    Category.id != category_id
                )
            ).first()
            
            if existing:
                raise ValueError(f"Já existe uma categoria com o nome '{category_data.name}'")
        
        # Atualizar campos
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        self.db.commit()
        self.db.refresh(category)
        
        return category
    
    def delete_category(self, category_id: UUID) -> bool:
        """Soft delete de uma categoria"""
        category = self.get_category(category_id)
        if not category:
            return False
        
        # Verificar se há transações usando esta categoria
        transaction_count = self.db.query(Transaction).filter(
            Transaction.category_id == category_id
        ).count()
        
        if transaction_count > 0:
            raise ValueError(f"Não é possível deletar categoria com {transaction_count} transações")
        
        category.is_active = False
        self.db.commit()
        
        return True
    
    def restore_category(self, category_id: UUID) -> Optional[Category]:
        """Restaura uma categoria deletada"""
        category = self.db.query(Category).filter(
            and_(
                Category.id == category_id,
                Category.user_id == self.user_id
            )
        ).first()
        
        if not category:
            return None
        
        category.is_active = True
        self.db.commit()
        self.db.refresh(category)
        
        return category
