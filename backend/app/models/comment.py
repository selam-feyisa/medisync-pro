import uuid
from sqlalchemy import Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin


class Comment(Base, TimestampMixin):
    """Comment model - threaded comments on tickets."""
    __tablename__ = "comments"

    ticket_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True
    )
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship()
    replies: Mapped[list["Comment"]] = relationship(
        back_populates="parent", remote_side=[id], cascade="all, delete-orphan"
    )
    parent: Mapped["Comment | None"] = relationship(
        back_populates="replies", remote_side=[parent_id]
    )
