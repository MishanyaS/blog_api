from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.schemas.auth import TokenPair
from app.core.roles import UserRole

class AuthService:
    @staticmethod
    async def register(email: str, password: str, db: AsyncSession) -> User:
        result = await db.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.USER,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def login(email: str, password: str, db: AsyncSession) -> TokenPair:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
        )
    
    @staticmethod
    async def refresh(refresh_token: str, db: AsyncSession) -> TokenPair:
        payload = decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("sub")
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
        )