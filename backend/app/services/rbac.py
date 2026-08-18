from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import User, Workspace, WorkspaceMember, MemberRole


from app.core.rbac import ROLE_HIERARCHY


class RBACService:
    """Role-based access control service."""

    @staticmethod
    async def check_workspace_access(
        db: AsyncSession, user_id: UUID, workspace_id: UUID
    ) -> bool:
        """Check if user has any access to workspace."""
        # Workspace owner has access
        workspace_stmt = select(Workspace).where(
            (Workspace.id == workspace_id) & (Workspace.owner_id == user_id)
        )
        workspace_result = await db.execute(workspace_stmt)
        if workspace_result.scalars().first() is not None:
            return True

        # Workspace members have access
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
        # Owner has all permissions
        workspace_stmt = select(Workspace).where(
            (Workspace.id == workspace_id) & (Workspace.owner_id == user_id)
        )
        workspace_result = await db.execute(workspace_stmt)
        if workspace_result.scalars().first() is not None:
            return True

        # Check workspace members
        stmt = select(WorkspaceMember).where(
            (WorkspaceMember.user_id == user_id)
            & (WorkspaceMember.workspace_id == workspace_id)
        )
        result = await db.execute(stmt)
        member = result.scalars().first()

        if not member:
            return False

        user_level = ROLE_HIERARCHY.get(member.role, 0)
        required_level = ROLE_HIERARCHY.get(required_role, 0)

        return user_level >= required_level

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
