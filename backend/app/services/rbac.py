from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import User, Workspace, WorkspaceMember, MemberRole


class RBACService:
    """Role-based access control service."""

    @staticmethod
    async def check_workspace_access(
        db: AsyncSession, user_id: UUID, workspace_id: UUID
    ) -> bool:
        """Check if user has any access to workspace."""
        stmt = select(WorkspaceMember).where(
            (WorkspaceMember.user_id == user_id)
            & (WorkspaceMember.workspace_id == workspace_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first() is not None

    @staticmethod
    async def check_workspace_permission(
        db: AsyncSession,
        user_id: UUID,
        workspace_id: UUID,
        required_role: MemberRole,
    ) -> bool:
        """Check if user has required role in workspace."""
        stmt = select(WorkspaceMember).where(
            (WorkspaceMember.user_id == user_id)
            & (WorkspaceMember.workspace_id == workspace_id)
        )
        result = await db.execute(stmt)
        member = result.scalars().first()

        if not member:
            return False

        # Owner has all permissions
        if member.role == MemberRole.owner:
            return True

        # Map role hierarchy
        role_hierarchy = {
            MemberRole.owner: 4,
            MemberRole.admin: 3,
            MemberRole.member: 2,
            MemberRole.viewer: 1,
        }

        return role_hierarchy[member.role] >= role_hierarchy[required_role]

    @staticmethod
    async def add_member_to_workspace(
        db: AsyncSession,
        workspace_id: UUID,
        user_id: UUID,
        role: MemberRole,
    ) -> WorkspaceMember:
        """Add user to workspace with role."""
        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )
        db.add(member)
        await db.flush()
        return member

    @staticmethod
    async def update_member_role(
        db: AsyncSession,
        workspace_id: UUID,
        user_id: UUID,
        new_role: MemberRole,
    ) -> WorkspaceMember:
        """Update member role in workspace."""
        stmt = select(WorkspaceMember).where(
            (WorkspaceMember.user_id == user_id)
            & (WorkspaceMember.workspace_id == workspace_id)
        )
        result = await db.execute(stmt)
        member = result.scalars().first()

        if member:
            member.role = new_role
            await db.flush()
        return member
