"""v2 OAuth endpoints for client credentials grant."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.oauth_client import OAuthClient
from app.core.crypto import hash_password, verify_password
from pydantic import BaseModel
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/oauth", tags=["OAuth v2"])
security = HTTPBasic()


class TokenResponse(BaseModel):
    """OAuth token response."""
    accessToken: str
    tokenType: str = "bearer"
    expiresIn: int
    scope: str = "all"


@router.post("/token", response_model=TokenResponse)
async def client_credentials_grant(
    credentials: HTTPBasicCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth 2.0 client credentials grant.
    
    Returns an access token for API v2 access.
    """
    # Find OAuth client
    result = await db.execute(
        select(OAuthClient).where(
            OAuthClient.client_id == credentials.username,
            OAuthClient.is_active == True
        )
    )
    client = result.scalar_one_or_none()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )
    
    # Verify client secret
    if not verify_password(credentials.password, client.client_secret_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )
    
    # Generate access token
    access_token = create_access_token(
        str(client.workspace_id),
        "service_account"
    )
    
    return TokenResponse(
        accessToken=access_token,
        expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        scope=client.scopes or "all"
    )
