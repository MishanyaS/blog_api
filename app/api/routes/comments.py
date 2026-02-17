from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.core.roles import UserRole
from app.repositories.comment import CommentRepository
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentRead,
)
from app.schemas.pagination import Page
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post(
    "/",
    response_model=CommentRead,
    dependencies=[Depends(require_roles([UserRole.USER, UserRole.ADMIN]))]
)
async def create_comment(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment_data = data.model_dump()
    comment_data["author_id"] = user.id
    
    return await CommentRepository.create(comment_data, db)

@router.post(
    "/post/{post_id}",
    response_model=Page[CommentRead],
)
async def get_comments_for_post(
    post_id: UUID,
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    total, items = await CommentRepository.get_by_post(
        post_id,
        db,
        limit,
        offset,
    )
    
    return Page(
        total=total,
        limit=limit,
        offset=offset,
        items=items,
    )

@router.patch(
    "/{comment_id}",
    response_model=CommentRead,
)
async def update_comment(
    comment_id: UUID,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment = await CommentRepository.get_by_id(comment_id, db)
    
    if not comment:
        raise HTTPException(404)
    
    if user.role != UserRole.ADMIN and comment.author_id != user.id:
        raise HTTPException(403)
    
    return await CommentRepository.update(
        comment,
        data.model_dump(exclude_unset=True),
        db,
    )

@router.delete(
    "/{comment_id}",
)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment = await CommentRepository.get_by_id(comment_id, db)
    
    if not comment:
        raise HTTPException(404)
    
    if user.role != UserRole.ADMIN and comment.author_id != user.id:
        raise HTTPException(403)
    
    await CommentRepository.soft_delete(comment, db)
    return {"status": "deleted"}

@router.delete(
    "/{comment_id}/hard",
    dependencies=[Depends(require_roles([UserRole.USER, UserRole.ADMIN]))],
)
async def hard_delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    comment = await CommentRepository.get_by_id(comment_id, db)
    
    if not comment:
        raise HTTPException(404)
    
    await CommentRepository.hard_delete(comment, db)
    return {"status": "hard deleted"}