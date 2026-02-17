from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.routes import health, auth, categories
from app.core.database import AsyncSessionLocal
from app.core.bootstrap import create_admin_if_not_exists, create_first_category_if_not_exists

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await create_admin_if_not_exists(db)
        await create_first_category_if_not_exists(db)
    
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"app": settings.app_name}