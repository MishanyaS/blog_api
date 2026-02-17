from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import TokenPair, TokenRefresh
from app.core.rate_limiter import RateLimiter

router = APIRouter(prefix="/auth", tags=["auth"])

login_limiter = RateLimiter(limit=5, window_seconds=60)
register_limiter = RateLimiter(limit=3, window_seconds=60)

@router.post(
    "/register",
    response_model=UserRead,
    dependencies=[Depends(register_limiter)],
)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await AuthService.register(data.email, data.password, db)
    return user

@router.post(
    "/login",
    response_model=TokenPair,
    dependencies=[Depends(login_limiter)],
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.login(
        form_data.username,
        form_data.password,
        db,
    )

@router.post("/refresh", response_model=TokenPair)
async def refresh(
    data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
):
    return await AuthService.refresh(data.refresh_token, db)