import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Board, Project, Workspace, BoardType


@pytest.mark.asyncio
async def test_create_kanban_board(db: AsyncSession):
    """Test creating Kanban board."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    project = Project(
        workspace_id=workspace.id,
        name="Test Project",
        slug="test-project",
    )
    db.add(project)
    await db.flush()

    board = Board(
        project_id=project.id,
        name="Kanban Board",
        board_type=BoardType.kanban,
    )
    db.add(board)
    await db.flush()

    assert board.board_type == BoardType.kanban


@pytest.mark.asyncio
async def test_create_scrum_board(db: AsyncSession):
    """Test creating Scrum board."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    project = Project(
        workspace_id=workspace.id,
        name="Test Project",
        slug="test-project",
    )
    db.add(project)
    await db.flush()

    board = Board(
        project_id=project.id,
        name="Scrum Board",
        board_type=BoardType.scrum,
    )
    db.add(board)
    await db.flush()

    assert board.board_type == BoardType.scrum
