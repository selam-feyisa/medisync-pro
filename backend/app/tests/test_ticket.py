import pytest
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticket, Column, Board, Project, Workspace


@pytest.mark.asyncio
async def test_create_ticket(db: AsyncSession):
    """Test ticket creation."""
    # Create nested resources
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
        name="Test Board",
    )
    db.add(board)
    await db.flush()

    column = Column(
        board_id=board.id,
        name="To Do",
        position=0,
    )
    db.add(column)
    await db.flush()

    ticket = Ticket(
        column_id=column.id,
        title="Test Ticket",
        description="A test ticket",
        priority="high",
        position=0,
    )
    db.add(ticket)
    await db.flush()

    assert ticket.title == "Test Ticket"
    assert ticket.priority == "high"


@pytest.mark.asyncio
async def test_ticket_with_due_date(db: AsyncSession):
    """Test ticket with due date."""
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
        name="Test Board",
    )
    db.add(board)
    await db.flush()

    column = Column(
        board_id=board.id,
        name="In Progress",
        position=1,
    )
    db.add(column)
    await db.flush()

    future_date = datetime.now(timezone.utc) + timedelta(days=7)
    ticket = Ticket(
        column_id=column.id,
        title="Urgent Ticket",
        priority="critical",
        due_date=future_date,
        story_points=8,
        position=0,
    )
    db.add(ticket)
    await db.flush()

    assert ticket.due_date is not None
    assert ticket.story_points == 8
