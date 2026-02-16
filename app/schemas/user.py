from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.core.roles import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    
    model_config = {"from_attributes": True}
