from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.category import Category

class CategoryRepository:
    @staticmethod
    async def create(data: dict, db: AsyncSession) -> Category:
        category = Category(**data)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def get_by_id(category_id, db: AsyncSession):
        result = await db.execute(
            select(Category).where(
                Category.id == category_id,
                Category.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db: AsyncSession, limit: int, offset: int):
        total_result = await db.execute(
            select(func.count()).select_from(Category).where(
                Category.is_deleted == False
            )
        )
        total = total_result.scalar_one()
        
        result = await db.execute(
            select(Category)
            .where(Category.is_deleted == False)
            .limit(limit)
            .offset(offset)
        )
        
        items = result.scalars().all()
        
        return total, items
    
    @staticmethod
    async def update(category, data: dict, db: AsyncSession):
        for key, value in data.items():
            setattr(category, key, value)
        await db.commit()
        await db.refresh(category)
        return category
    
    @staticmethod
    async def soft_delete(category, db: AsyncSession):
        category.is_deleted = True
        await db.commit()
    
    @staticmethod
    async def hard_delete(category, db: AsyncSession):
        await db.delete(category)
        await db.commit()