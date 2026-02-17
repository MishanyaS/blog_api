from pydantic import BaseModel
from uuid import UUID

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class CategoryRead(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    
    model_config = {
        "from_attributes": True,
    }