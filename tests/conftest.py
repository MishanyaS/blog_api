import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from fastapi import Request

from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

TEST_DB_NAME = settings.postgres_db + "_test"

ADMIN_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/postgres"
)

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.postgres_user}:{settings.postgres_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{TEST_DB_NAME}"
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    admin_engine = create_async_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")
    
    async with admin_engine.begin() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
        await conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    
    await admin_engine.dispose()
    
    test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    from app.models.user import User
    from app.core.roles import UserRole
    from app.core.security import hash_password
    
    SessionLocal = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )
    
    async with SessionLocal() as session:
        admin_user = User(
            email=settings.admin_email,
            hashed_password=hash_password(settings.admin_password),
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin_user)
        await session.commit()
    
    yield
    
    await test_engine.dispose()
    
    admin_engine = create_async_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")
    async with admin_engine.begin() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
    await admin_engine.dispose()

@pytest_asyncio.fixture
async def db():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)

    SessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )
    
    async with SessionLocal() as session:
        yield session
    
    await engine.dispose()

async def disable_rate_limit(request: Request):
    return

@pytest_asyncio.fixture
async def client(db):
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(autouse=True)
async def override_rate_limiter(monkeypatch):
    async def fake_rate_limiter(request):
        return
    from app.core.rate_limiter import RateLimiter
    monkeypatch.setattr(RateLimiter, "__call__", fake_rate_limiter)
