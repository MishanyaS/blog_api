from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.category import Category
from app.core.roles import UserRole
from app.core.security import hash_password
from app.core.config import settings

async def create_admin_if_not_exists(db: AsyncSession):
    result = await db.execute(
        select(User).where(User.role == UserRole.ADMIN)
    )
    admin = result.scalars().first()
    
    if admin:
        return
    
    admin = User(
        email=settings.admin_email,
        hashed_password=hash_password(settings.admin_password),
        role=UserRole.ADMIN,
    )
    
    db.add(admin)
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()

async def create_first_category_if_not_exists(db: AsyncSession):
    result = await db.execute(
        select(Category).where(Category.name == "General")
    )
    category = result.scalars().first()
    
    if category:
        return
    
    category = Category(
        name="General",
        description="Default category",
    )
    
    db.add(category)
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()