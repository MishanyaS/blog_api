from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.core.roles import UserRole

class UserUpdateAdmin(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None

class UserCreateAdmin(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.ADMIN