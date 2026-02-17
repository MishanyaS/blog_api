from pydantic import BaseModel
from uuid import UUID

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: UUID

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: UUID | None = None

class PostRead(BaseModel):
    id: UUID
    title: str
    content: str
    author_id: UUID
    category_id: UUID
    
    model_config = {"from_attributes": True}