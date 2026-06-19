from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.services.file_attachment import upload_file
from backend.app.schemas.file_attachment import FileAttachmentResponse, FileUploadResponse

router = APIRouter()

@router.post("/tickets/{ticket_id}/attachments", 
             response_model=FileUploadResponse, 
             status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    ticket_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload file attachment to a ticket"""
    # TODO: Add workspace_id from user context later
    workspace_id = getattr(current_user, 'workspace_id', None)
    
    attachment = await upload_file(
        db=db,
        ticket_id=ticket_id,
        workspace_id=workspace_id,
        file=file,
        uploader_id=current_user.id
    )
    
    return {
        "id": attachment.id,
        "filename": attachment.original_filename,
        "download_url": f"/attachments/{attachment.id}/download",  # Will implement later
        "message": "File uploaded successfully"
    }