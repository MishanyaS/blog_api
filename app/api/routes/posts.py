from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.core.roles import UserRole
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostRead
from app.schemas.pagination import Page
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post(
    "/",
    response_model=PostRead,
    dependencies=[Depends(require_roles([UserRole.USER, UserRole.ADMIN]))]
)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post_data = data.model_dump()
    post_data["author_id"] = user.id
    
    return await PostRepository.create(post_data, db)

@router.get(
    "/",
    response_model=Page[PostRead],
)
async def get_posts(
    limit: int = Query(10, le=100),
    offset: int = 0,
    search: str | None = None,
    category_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
):
    total, items = await PostRepository.get_all(
        db,
        limit,
        offset,
        search,
        category_id,
    )
    return Page(total=total, limit=limit, offset=offset, items=items)

@router.patch(
    "/{post_id}",
    response_model=PostRead,
)
async def update_post(
    post_id: UUID,
    data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = await PostRepository.get_by_id(post_id, db)
    
    if not post:
        raise HTTPException(404)
    
    if user.role != UserRole.ADMIN and post.author_id != user.id:
        raise HTTPException(403)
    
    return await PostRepository.update(
        post,
         data.model_dump(exclude_unset=True),
         db,
    )

@router.delete(
    "/{post_id}",
)
async def delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = await PostRepository.get_by_id(post_id, db)
    
    if not post:
        raise HTTPException(404)
    
    if user.role != UserRole.ADMIN and post.author_id != user.id:
        raise HTTPException(403)
    
    await PostRepository.soft_delete(post, db)
    return {"detail": "deleted"}

@router.delete(
    "/{post_id}/hard",
    dependencies=[Depends(require_roles([UserRole.ADMIN]))],
)
async def hard_delete_post(
    post_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    post = await PostRepository.get_by_id(post_id, db)
    
    if not post:
        raise HTTPException(404)
    
    await PostRepository.hard_delete(post, db)
    return {"detail": "hard deleted"}