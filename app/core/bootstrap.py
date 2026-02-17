from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.category import Category
from app.core.roles import UserRole
from app.core.security import hash_password
from app.core.config import settings

async def create_admin_if_not_exists(db: AsyncSession):
    result = await db.execute(
        select(User).where(User.role == UserRole.ADMIN)
    )
    admin = result.scalar_one_or_none()
    
    if not admin:
        admin = User(
            email=settings.admin_email,
            hashed_password=hash_password(settings.admin_password),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        await db.commit()

async def create_first_category_if_not_exists(db: AsyncSession):
    result = await db.execute(
        select(Category).where(Category.is_deleted == False)
    )
    category = result.scalar_one_or_none()
    
    if not category:
        category = Category(
            name="General",
            description="Default category",
        )
        db.add(category)
        await db.commit()