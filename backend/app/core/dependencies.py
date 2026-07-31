from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User, UserRole
from app.models.workspace_member import MemberRole
from app.core.rbac import (
    check_workspace_permission,
    is_workspace_owner,
    get_user_workspace_role,
    has_global_role
)


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def require_role(required_role: UserRole, user: User = Depends(get_current_user)) -> User:
    """
    Require the user to have a specific global role.
    """
    if not has_global_role(user, required_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Requires {required_role.value} role or higher"
        )
    return user


async def require_superadmin(user: User = Depends(get_current_user)) -> User:
    """
    Require the user to be a global admin.
    """
    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires admin role"
        )
    return user


class WorkspaceRoleChecker:
    """
    Dependency for checking workspace-specific roles.
    """
    
    def __init__(self, required_role: MemberRole):
        self.required_role = required_role
    
    async def __call__(
        self,
        workspace_id: str,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """
        Check if user has the required role in the workspace.
        """
        # Check if user is workspace owner
        owner = await is_workspace_owner(str(user.id), workspace_id, db)
        
        if owner:
            return user
        
        # Get user's workspace role
        user_role = await get_user_workspace_role(str(user.id), workspace_id, db)
        
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a member of this workspace"
            )
        
        # Check permission
        if not check_workspace_permission(user_role, self.required_role, is_owner=False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {self.required_role.value} role or higher in this workspace"
            )
        
        return user


def require_workspace_role(required_role: MemberRole) -> WorkspaceRoleChecker:
    """
    Factory function to create a workspace role dependency.
    """
    return WorkspaceRoleChecker(required_role)