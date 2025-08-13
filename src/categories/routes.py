from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user
from src.database_sqlalchemy import get_db
from src.categories.models import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryWithTransactionCount
from src.categories.services import CategoryService
from uuid import UUID
from src.auth.models import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryWithTransactionCount])
async def get_categories(
    include_inactive: bool = Query(False, description="Include inactive categories"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista todas as categorias do usuário"""
    service = CategoryService(db, current_user.id)
    return service.get_categories(include_inactive=include_inactive)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtém uma categoria específica"""
    service = CategoryService(db, current_user.id)
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova categoria"""
    service = CategoryService(db, current_user.id)
    return service.create_category(category_data)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma categoria"""
    service = CategoryService(db, current_user.id)
    category = service.update_category(category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma categoria (soft delete)"""
    service = CategoryService(db, current_user.id)
    success = service.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return {"message": "Categoria deletada com sucesso"}

@router.post("/{category_id}/restore")
async def restore_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Restaura uma categoria deletada"""
    service = CategoryService(db, current_user.id)
    category = service.restore_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category