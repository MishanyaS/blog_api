from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from app.models.base import BaseModel

class Comment(BaseModel):
    __tablename__ = "comments"
    
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    post_id: Mapped[UUID] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    author_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    post = relationship("Post")
    author = relationship("User")