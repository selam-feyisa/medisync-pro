from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Workspace, WorkspaceMember, MemberRole
from app.services import RBACService

router = APIRouter(prefix="/workspaces", tags=["members"])


class AddMemberRequest(BaseModel):
    user_id: UUID
    role: str = "member"


class UpdateMemberRoleRequest(BaseModel):
    new_role: str


@router.get("/{workspace_id}/members", response_model=list[dict])
async def list_workspace_members(
    workspace_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all members in workspace."""
    has_access = await RBACService.check_workspace_access(db, current_user.id, workspace_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access workspace",
        )

    workspace = await db.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return [
        {
            "user_id": member.user_id,
            "role": member.role.value,
        }
        for member in workspace.members
    ]


@router.post("/{workspace_id}/members")
async def add_member_to_workspace(
    workspace_id: UUID,
    request: AddMemberRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add member to workspace."""
    has_permission = await RBACService.check_workspace_permission(
        db, current_user.id, workspace_id, MemberRole.admin
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can add members",
        )

    member = await RBACService.add_member_to_workspace(
        db, workspace_id, request.user_id, MemberRole(request.role)
    )
    await db.commit()

    return {
        "message": "Member added successfully",
        "user_id": member.user_id,
        "role": member.role.value,
    }


@router.patch("/{workspace_id}/members/{user_id}")
async def update_member_role(
    workspace_id: UUID,
    user_id: UUID,
    request: UpdateMemberRoleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update member role in workspace."""
    has_permission = await RBACService.check_workspace_permission(
        db, current_user.id, workspace_id, MemberRole.admin
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update member roles",
        )

    member = await RBACService.update_member_role(
        db, workspace_id, user_id, MemberRole(request.new_role)
    )
    await db.commit()

    return {
        "message": "Member role updated successfully",
        "user_id": member.user_id,
        "role": member.role.value,
    }


@router.delete("/{workspace_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    workspace_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Remove member from workspace (cannot remove owner)."""
    workspace = await db.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )
    
    if workspace.owner_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot remove workspace owner",
        )
    
    has_permission = await RBACService.check_workspace_permission(
        db, current_user.id, workspace_id, MemberRole.admin
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can remove members",
        )
    
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
    )
    member = result.scalar_one_or_none()
    if member:
        await db.delete(member)
        await db.commit()
