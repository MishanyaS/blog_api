from pydantic import BaseModel
from uuid import UUID

class CommentCreate(BaseModel):
    content: str
    post_id: UUID

class CommentUpdate(BaseModel):
    content: str | None = None

class CommentRead(BaseModel):
    id: UUID
    content: str
    post_id: UUID
    author_id: UUID
    
    model_config = {"from_attributes": True}