from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models import Project, Board, Column, Ticket


class ProjectService:
    """Project business logic service."""

    @staticmethod
    async def create_project_with_boards(
        db: AsyncSession, workspace_id: UUID, name: str, slug: str
    ):
        """Create project with default boards."""
        from app.models import Project

        project = Project(
            workspace_id=workspace_id,
            name=name,
            slug=slug,
        )
        db.add(project)
        await db.flush()

        # Create default board
        board = Board(
            project_id=project.id,
            name="Backlog",
        )
        db.add(board)
        await db.flush()

        # Create default columns
        columns = [
            Column(board_id=board.id, name="To Do", position=0),
            Column(board_id=board.id, name="In Progress", position=1),
            Column(board_id=board.id, name="Done", position=2, is_done_column=True),
        ]
        for col in columns:
            db.add(col)

        return project

    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: UUID):
        """Get project with all boards and columns."""
        return await db.get(Project, project_id)

    @staticmethod
    async def get_project_tickets_by_priority(
        db: AsyncSession, project_id: UUID, priority: str
    ) -> list[Ticket]:
        """Get all tickets in project filtered by priority."""
        stmt = (
            select(Ticket)
            .join(Column)
            .join(Board)
            .where(Board.project_id == project_id)
            .where(Ticket.priority == priority)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
