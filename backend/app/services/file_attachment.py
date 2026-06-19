from sqlalchemy.ext.asyncio import AsyncSession
from minio import Minio
from minio.error import S3Error
from uuid import UUID, uuid4
from fastapi import UploadFile
from backend.app.core.config import settings
from backend.app.models.file_attachment import FileAttachment
from backend.app.core.exceptions import ValidationException


# MinIO Client
minio_client = Minio(
    settings.MINIO_URL,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False  # Set True in production with HTTPS
)


async def upload_file(db: AsyncSession, ticket_id: UUID, workspace_id: UUID, file: UploadFile, uploader_id: UUID):
    """Upload file to MinIO and save record"""
    
    # Validate file size (example: 10MB limit)
    if file.size > 10 * 1024 * 1024:
        raise ValidationException("File size exceeds 10MB limit")
    
    # Generate unique storage key
    file_ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    storage_key = f"workspaces/{workspace_id}/tickets/{ticket_id}/{uuid4()}.{file_ext}"
    
    # Upload to MinIO
    file_data = await file.read()
    minio_client.put_object(
        bucket_name="medisync",
        object_name=storage_key,
        data=file_data,
        length=len(file_data),
        content_type=file.content_type
    )
    
    # Save to database
    attachment = FileAttachment(
        workspace_id=workspace_id,
        ticket_id=ticket_id,
        uploader_id=uploader_id,
        original_filename=file.filename,
        storage_key=storage_key,
        file_size=len(file_data),
        mime_type=file.content_type,
        is_image=file.content_type.startswith("image/")
    )
    
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)
    
    return attachment


def ensure_bucket_exists():
    """Ensure MinIO bucket exists (call on startup)"""
    bucket_name = "medisync"
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"✅ Created MinIO bucket: {bucket_name}")
        else:
            print(f"✅ MinIO bucket '{bucket_name}' already exists")
    except S3Error as e:
        print(f"❌ MinIO bucket error: {e}")


# Run bucket check when module is imported
ensure_bucket_exists()