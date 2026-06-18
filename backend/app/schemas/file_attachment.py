from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class FileAttachmentBase(BaseModel):
    original_filename: str
    file_size: int
    mime_type: str
    is_image: bool = False


class FileAttachmentResponse(FileAttachmentBase):
    id: UUID
    ticket_id: Optional[UUID] = None
    uploader_id: UUID
    storage_key: str
    thumbnail_key: Optional[str] = None
    version: int = 1
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    id: UUID
    filename: str
    download_url: str
    thumbnail_url: Optional[str] = None
    message: str = "File uploaded successfully"