from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.post import Post

class PostRepository:
    @staticmethod
    async def create(data: dict, db: AsyncSession):
        post = Post(**data)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post
    
    @staticmethod
    async def get_by_id(post_id, db: AsyncSession):
        result = await db.execute(
            select(Post).where(
                Post.id == post_id,
                Post.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        limit: int,
        offset: int,
        search: str | None = None,
        category_id=None,
    ):
        query = select(Post).where(Post.is_deleted == False)
        
        if search:
            query = query.where(Post.title.ilike(f"%{search}%"))
        
        if category_id:
            query = query.where(Post.category_id == category_id)
        
        total_query = select(func.count()).select_from(query.subquery())
        total = (await db.execute(total_query)).scalar_one()
        
        result = await db.execute(
            query.limit(limit).offset(offset)
        )
        
        items = result.scalars().all()
        
        return total, items
    
    @staticmethod
    async def update(post, data: dict, db: AsyncSession):
        for key, value in data.items():
            setattr(post, key, value)
        await db.commit()
        await db.refresh(post)
        return post
    
    @staticmethod
    async def soft_delete(post, db: AsyncSession):
        post.is_deleted = True
        await db.commit()
    
    @staticmethod
    async def hard_delete(post, db: AsyncSession):
        await db.delete(post)
        await db.commit()