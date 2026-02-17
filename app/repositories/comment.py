from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.comment import Comment

class CommentRepository:
    @staticmethod
    async def create(data: dict, db: AsyncSession):
        comment = Comment(**data)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    
    @staticmethod
    async def get_by_id(comment_id, db: AsyncSession):
        result = await db.execute(
            select(Comment).where(
                Comment.id == comment_id,
                Comment.is_deleted == False,
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_post(
        post_id,
        db: AsyncSession,
        limit: int,
        offset: int,
    ):
        query = select(Comment).where(
            Comment.post_id == post_id,
            Comment.is_deleted == False
        )
        
        total = (
            await db.execute(
                select(func.count()).select_from(query.subquery())
            )
        ).scalar_one()
        
        result = await db.execute(
            query.limit(limit).offset(offset)
        )
        
        items = result.scalars().all()
        
        return total, items
    
    @staticmethod
    async def update(comment, data: dict, db: AsyncSession):
        for key, value in data.items():
            setattr(comment, key, value)
        await db.commit()
        await db.refresh(comment)
        return comment
    
    @staticmethod
    async def soft_delete(comment, db: AsyncSession):
        comment.is_deleted = True
        await db.commit()
    
    @staticmethod
    async def hard_delete(comment, db: AsyncSession):
        await db.delete(comment)
        await db.commit()