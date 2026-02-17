from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.api.deps import require_roles
from app.core.roles import UserRole
from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
)
from app.schemas.pagination import Page

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post(
    "/",
    response_model=CategoryRead,
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await CategoryRepository.create(data.model_dump(), db)

@router.get(
    "/",
    response_model=Page[CategoryRead],
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def get_categories(
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    total, items = await CategoryRepository.get_all(db, limit, offset)
    return Page(total=total, limit=limit, offset=offset, items=items)

@router.patch(
    "/{category_id}",
    response_model=CategoryRead,
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    category = await CategoryRepository.get_by_id(category_id, db)
    if not category:
        raise HTTPException(404)
    
    return await CategoryRepository.update(
        category,
        data.model_dump(exclude_unset=True),
        db,
    )

@router.delete(
    "/{category_id}",
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    category = await CategoryRepository.get_by_id(category_id, db)
    if not category:
        raise HTTPException(404)
    
    await CategoryRepository.soft_delete(category, db)
    return {"status": "deleted"}

@router.delete(
    "/{category_id}/hard",
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def hard_delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    category = await CategoryRepository.get_by_id(category_id, db)
    if not category:
        raise HTTPException(404)
    
    await CategoryRepository.hard_delete(category, db)
    return {"status": "hard deleted"}