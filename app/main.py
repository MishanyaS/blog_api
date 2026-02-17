from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.routes import health, auth, categories, posts, comments, users
from app.core.database import AsyncSessionLocal
from app.core.bootstrap import create_admin_if_not_exists, create_first_category_if_not_exists
from app.core.rate_limiter import RateLimiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        await create_admin_if_not_exists(db)
        await create_first_category_if_not_exists(db)
    
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

global_limiter = RateLimiter(limit=100, window_seconds=60)

@app.middleware("http")
async def global_rate_limit(request, call_next):
    await global_limiter(request)
    response = await call_next(request)
    return response

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"app": settings.app_name}