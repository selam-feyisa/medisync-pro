import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Comment, Ticket, Column, Board, Project, Workspace, User


@pytest.mark.asyncio
async def test_create_comment(db: AsyncSession):
    """Test creating a comment on ticket."""
    # Create nested resources
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    user = User(
        email="commenter@test.com",
        full_name="Comment Author",
        hashed_password="hashed",
    )
    db.add(user)
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
        position=0,
    )
    db.add(ticket)
    await db.flush()

    comment = Comment(
        ticket_id=ticket.id,
        author_id=user.id,
        body="This is a test comment",
    )
    db.add(comment)
    await db.flush()

    assert comment.body == "This is a test comment"
    assert comment.is_edited is False


@pytest.mark.asyncio
async def test_threaded_comments(db: AsyncSession):
    """Test creating threaded comment replies."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    user = User(
        email="test@test.com",
        full_name="Test User",
        hashed_password="hashed",
    )
    db.add(user)
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
        position=0,
    )
    db.add(ticket)
    await db.flush()

    parent_comment = Comment(
        ticket_id=ticket.id,
        author_id=user.id,
        body="Parent comment",
    )
    db.add(parent_comment)
    await db.flush()

    reply = Comment(
        ticket_id=ticket.id,
        author_id=user.id,
        body="Reply to parent",
        parent_id=parent_comment.id,
    )
    db.add(reply)
    await db.flush()

    assert reply.parent_id == parent_comment.id
