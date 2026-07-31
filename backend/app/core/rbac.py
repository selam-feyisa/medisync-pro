"""Role-Based Access Control (RBAC) utilities."""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from app.models.workspace_member import MemberRole
from app.models.workspace import Workspace


# Healthcare role hierarchy for workspace permissions
ROLE_HIERARCHY = {
    MemberRole.admin: 5,
    MemberRole.doctor: 4,
    MemberRole.nurse: 3,
    MemberRole.receptionist: 2,
    MemberRole.patient: 1,
}


def get_role_level(role: MemberRole) -> int:
    """Get the hierarchy level for a workspace role."""
    return ROLE_HIERARCHY.get(role, 0)


def check_workspace_permission(
    user_role: MemberRole,
    required_role: MemberRole,
    is_owner: bool = False
) -> bool:
    """
    Check if a user has the required workspace permission.
    
    Args:
        user_role: The user's role in the workspace
        required_role: The minimum role required
        is_owner: Whether the user is the workspace owner
    
    Returns:
        True if user has permission, False otherwise
    """
    # Workspace owners bypass all checks
    if is_owner:
        return True
    
    user_level = get_role_level(user_role)
    required_level = get_role_level(required_role)
    
    return user_level >= required_level


async def is_workspace_owner(
    user_id: str,
    workspace_id: str,
    db: AsyncSession
) -> bool:
    """
    Check if a user is the owner of a workspace.
    
    Args:
        user_id: The user's ID
        workspace_id: The workspace ID
        db: Database session
    
    Returns:
        True if user is the workspace owner, False otherwise
    """
    result = await db.execute(
        select(Workspace).where(
            Workspace.id == workspace_id,
            Workspace.owner_id == user_id
        )
    )
    return result.scalar_one_or_none() is not None


async def get_user_workspace_role(
    user_id: str,
    workspace_id: str,
    db: AsyncSession
) -> Optional[MemberRole]:
    """
    Get a user's role in a workspace.
    
    Args:
        user_id: The user's ID
        workspace_id: The workspace ID
        db: Database session
    
    Returns:
        The user's role or None if not a member
    """
    from app.models.workspace_member import WorkspaceMember
    
    result = await db.execute(
        select(WorkspaceMember.role).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def has_global_role(user: User, required_role: UserRole) -> bool:
    """
    Check if a user has a global role at or above the required level.
    
    Args:
        user: The user object
        required_role: The minimum required role
    
    Returns:
        True if user has sufficient global role
    """
    # Global role hierarchy
    global_hierarchy = {
        UserRole.admin: 4,
        UserRole.doctor: 3,
        UserRole.nurse: 2,
        UserRole.receptionist: 1,
        UserRole.patient: 0,
    }
    
    user_level = global_hierarchy.get(user.role, 0)
    required_level = global_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
