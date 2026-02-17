from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.api.deps import require_roles
from app.core.roles import UserRole
from app.repositories.user import UserRepository
from app.schemas.user import UserRead
from app.schemas.user_admin import UserUpdateAdmin, UserCreateAdmin
from app.schemas.pagination import Page
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)

@router.get(
    "/",
    response_model=Page[UserRead],
)
async def get_users(
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    total, items = await UserRepository.get_all(db, limit, offset)
    return Page(total=total, limit=limit, offset=offset, items=items)

@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    user = await UserRepository.get_by_id(user_id, db)
    if not user:
        raise HTTPException(404)
    return user

@router.patch(
    "/{user_id}",
    response_model=UserRead,
)
async def update_user(
    user_id: UUID,
    data: UserUpdateAdmin,
    db: AsyncSession = Depends(get_db),
):
    user = await UserRepository.get_by_id(user_id, db)
    if not user:
        raise HTTPException(404)
    
    return await UserRepository.update(
        user,
        data.model_dump(exclude_unset=True),
        db,
    )

@router.delete(
    "/{user_id}",
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    user = await UserRepository.get_by_id(user_id, db)
    if not user:
        raise HTTPException(404)
    
    await UserRepository.soft_delete(user, db)
    return {"status": "deleted"}

@router.delete(
    "/{user_id}/hard",
)
async def hard_delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    user = await UserRepository.get_by_id(user_id, db)
    if not user:
        raise HTTPException(404)
    
    await UserRepository.hard_delete(user, db)
    return {"status": "hard deleted"}

@router.post(
    "/",
    response_model=UserRead,
)
async def create_admin(
    data: UserCreateAdmin,
    db: AsyncSession = Depends(get_db),
):
    user_data = data.model_dump()
    user_data["hashed_password"] = hash_password(data.password)
    user_data.pop("password")
    
    return await UserRepository.create(user_data, db)