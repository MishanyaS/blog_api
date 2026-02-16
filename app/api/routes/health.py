from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.redis import redis_client

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception:
        return {"database": "error"}

@router.get("/redis")
async def health_redis():
    try:
        await redis_client.ping()
        return {"redis": "ok"}
    except Exception:
        return {"redis": "error"}

@router.get("/full")
async def health_full(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    redis_status = "ok"
    
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    
    try:
        await redis_client.ping()
    except Exception:
        redis_status = "error"
    
    return {
        "database": db_status,
        "redis": redis_status,
    }