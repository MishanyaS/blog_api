from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import health

app = FastAPI(title=settings.app_name)

app.include_router(health.router)

@app.get("/")
async def root():
    return {"app": settings.app_name}