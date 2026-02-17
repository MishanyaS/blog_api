from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user import User
from app.core.roles import UserRole

class UserRepository:
    @staticmethod
    async def create(data: dict, db: AsyncSession) -> User:
        user = User(**data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def get_by_id(user_id, db: AsyncSession):
        result = await db.execute(
            select(User).where(
                User.id == user_id,
                User.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(db: AsyncSession, limit: int, offset: int):
        total = (
            await db.execute(
                select(func.count()).select_from(User).where(
                    User.is_deleted == False
                )
            )
        ).scalar_one()
        
        result = await db.execute(
            select(User)
            .where(User.is_deleted == False)
            .limit(limit)
            .offset(offset)
        )
        
        items = result.scalars().all()
        return total, items
    
    @staticmethod
    async def update(user: User, data: dict, db: AsyncSession):
        for key, value in data.items():
            setattr(user, key, value)
        
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def soft_delete(user: User, db: AsyncSession):
        user.is_deleted = True
        user.is_active = False
        await db.commit()
    
    @staticmethod
    async def hard_delete(user: User, db: AsyncSession):
        await db.delete(user)
        await db.commit()