from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from backend.app.models.base import Base, TimestampMixin


class FileAttachment(Base, TimestampMixin):
    __tablename__ = "file_attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=True)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    original_filename = Column(String(255), nullable=False)
    storage_key = Column(String(500), nullable=False)  # MinIO path
    file_size = Column(Integer)  # bytes
    mime_type = Column(String(100))
    is_image = Column(Boolean, default=False)
    thumbnail_key = Column(String(500), nullable=True)
    version = Column(Integer, default=1)

    # Relationships
    ticket = relationship("Ticket", back_populates="attachments")
    uploader = relationship("User")

    def __repr__(self):
        return f"<FileAttachment {self.original_filename}>"