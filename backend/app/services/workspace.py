from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import Workspace, WorkspaceMember, MemberRole
from app.schemas import WorkspaceCreate


class WorkspaceService:
    """Workspace business logic service."""

    @staticmethod
    async def create_workspace(
        db: AsyncSession, workspace_data: WorkspaceCreate, owner_id: UUID
    ) -> Workspace:
        """Create new workspace with owner."""
        workspace = Workspace(
            name=workspace_data.name,
            slug=workspace_data.slug,
            description=workspace_data.description,
            owner_id=owner_id,
        )
        db.add(workspace)
        await db.flush()

        # Add owner as workspace member
        owner_member = WorkspaceMember(
            workspace_id=workspace.id, user_id=owner_id, role=MemberRole.owner
        )
        db.add(owner_member)
        return workspace

    @staticmethod
    async def get_workspace_by_id(db: AsyncSession, workspace_id: UUID) -> Workspace | None:
        """Retrieve workspace by ID."""
        return await db.get(Workspace, workspace_id)

    @staticmethod
    async def get_user_workspaces(
        db: AsyncSession, user_id: UUID
    ) -> list[Workspace]:
        """Get all workspaces for a user."""
        stmt = (
            select(Workspace)
            .join(WorkspaceMember)
            .where(WorkspaceMember.user_id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
