from typing import List, Optional
from uuid import UUID
from .models import Category, CategoryCreate, CategoryUpdate
from src.database_sqlalchemy import get_supabase_client

class CategoryService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def create_category(self, category_data: CategoryCreate) -> Category:
        """Cria uma nova categoria"""
        data = category_data.dict()
        
        result = self.supabase.table('categories').insert(data).execute()
        
        if result.error:
            raise Exception(f"Erro ao criar categoria: {result.error.message}")
        
        return Category(**result.data[0])

    def get_categories_by_user(self, user_id: UUID, include_default: bool = True) -> List[Category]:
        """Busca categorias de um usuário"""
        query = self.supabase.table('categories').select('*').eq('user_id', str(user_id))
        
        if not include_default:
            query = query.eq('is_default', False)
        
        result = query.execute()
        
        if result.error:
            raise Exception(f"Erro ao buscar categorias: {result.error.message}")
        
        return [Category(**category) for category in result.data]

    def update_category(self, category_id: UUID, category_data: CategoryUpdate) -> Optional[Category]:
        """Atualiza uma categoria"""
        update_data = category_data.dict(exclude_unset=True)
        
        result = self.supabase.table('categories').update(update_data).eq('id', str(category_id)).select().single().execute()
        
        if result.error:
            raise Exception(f"Erro ao atualizar categoria: {result.error.message}")
            
        return Category(**result.data) if result.data else None

    def delete_category(self, category_id: UUID) -> bool:
        """Soft delete de uma categoria"""
        result = self.supabase.table('categories').update({'is_active': False}).eq('id', str(category_id)).execute()
        
        if result.error:
            raise Exception(f"Erro ao deletar categoria: {result.error.message}")
            
        return True

    def restore_category(self, category_id: UUID) -> bool:
        """Restaura uma categoria deletada"""
        result = self.supabase.table('categories').update({'is_active': True}).eq('id', str(category_id)).execute()
        
        if result.error:
            raise Exception(f"Erro ao restaurar categoria: {result.error.message}")
            
        return True
