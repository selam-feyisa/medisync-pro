from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.file_attachment import create_download_url, upload_file
from app.schemas.file_attachment import FileUploadResponse

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
    try:
        workspace_id = getattr(current_user, 'workspace_id', None)
        
        if not workspace_id:
            raise HTTPException(status_code=400, detail="Workspace not found")

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
            "download_url": f"/api/v1/attachments/{attachment.id}/download",
            "thumbnail_url": (
                f"/api/v1/attachments/{attachment.id}/thumbnail"
                if attachment.thumbnail_key
                else None
            ),
            "message": "File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/attachments/{attachment_id}/download")
async def download_attachment(
    attachment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate presigned download URL"""
    try:
        download_url = await create_download_url(
            db=db,
            attachment_id=attachment_id,
            expires=timedelta(hours=1),
        )
        return {
            "download_url": download_url,
            "expires_in": 3600
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate download link")
