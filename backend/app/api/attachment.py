from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, FileAttachment, Ticket

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.post("/{ticket_id}/upload", status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    ticket_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload file attachment to ticket."""
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    # TODO: Implement S3 upload logic
    storage_key = f"tickets/{ticket_id}/{file.filename}"

    attachment = FileAttachment(
        workspace_id=None,  # TODO: Get from ticket's workspace
        ticket_id=ticket_id,
        uploader_id=current_user.id,
        original_filename=file.filename,
        storage_key=storage_key,
        file_size=0,  # TODO: Get actual file size
        mime_type=file.content_type or "application/octet-stream",
        is_image=file.content_type.startswith("image/") if file.content_type else False,
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)

    return {
        "id": attachment.id,
        "filename": attachment.original_filename,
        "storage_key": attachment.storage_key,
        "message": "File uploaded successfully",
    }


@router.get("/{attachment_id}", response_model=dict)
async def get_attachment(
    attachment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get attachment details."""
    attachment = await db.get(FileAttachment, attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found",
        )

    return {
        "id": attachment.id,
        "filename": attachment.original_filename,
        "storage_key": attachment.storage_key,
        "file_size": attachment.file_size,
        "mime_type": attachment.mime_type,
        "created_at": attachment.created_at,
    }


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    attachment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete attachment."""
    attachment = await db.get(FileAttachment, attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found",
        )

    if attachment.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only uploader can delete attachment",
        )

    # TODO: Delete from S3
    await db.delete(attachment)
    await db.commit()
