import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from app.models import User, Workspace, Project, Board, Column, Ticket
from app.models.ticket import TicketPriority, TicketStatus


@pytest.mark.asyncio
async def test_create_ticket(db: AsyncSession, client: AsyncClient):
    """Test creating a new ticket."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.flush()
    
    column = Column(board_id=board.id, name="To Do", position=0)
    db.add(column)
    await db.flush()
    
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    db.add(user)
    await db.commit()
    
    # Create ticket
    response = await client.post(
        "/api/v1/tickets",
        json={
            "title": "Test Ticket",
            "description": "Test description",
            "column_id": str(column.id),
            "priority": "medium",
            "status": "todo"
        },
        headers={"Authorization": f"Bearer test_token"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["priority"] == "medium"


@pytest.mark.asyncio
async def test_get_tickets_by_column(db: AsyncSession, client: AsyncClient):
    """Test retrieving tickets by column."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.flush()
    
    column = Column(board_id=board.id, name="To Do", position=0)
    db.add(column)
    await db.flush()
    
    ticket = Ticket(
        title="Test Ticket",
        description="Test",
        column_id=column.id,
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.TODO,
        position=0
    )
    db.add(ticket)
    await db.commit()
    
    response = await client.get(f"/api/v1/columns/{column.id}/tickets")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Ticket"


@pytest.mark.asyncio
async def test_update_ticket(db: AsyncSession, client: AsyncClient):
    """Test updating a ticket."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.flush()
    
    column = Column(board_id=board.id, name="To Do", position=0)
    db.add(column)
    await db.flush()
    
    ticket = Ticket(
        title="Test Ticket",
        description="Test",
        column_id=column.id,
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.TODO,
        position=0
    )
    db.add(ticket)
    await db.commit()
    
    response = await client.patch(
        f"/api/v1/tickets/{ticket.id}",
        json={"title": "Updated Ticket", "priority": "high"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Ticket"
    assert data["priority"] == "high"


@pytest.mark.asyncio
async def test_delete_ticket(db: AsyncSession, client: AsyncClient):
    """Test deleting a ticket."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.flush()
    
    column = Column(board_id=board.id, name="To Do", position=0)
    db.add(column)
    await db.flush()
    
    ticket = Ticket(
        title="Test Ticket",
        description="Test",
        column_id=column.id,
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.TODO,
        position=0
    )
    db.add(ticket)
    await db.commit()
    
    response = await client.delete(f"/api/v1/tickets/{ticket.id}")
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_move_ticket(db: AsyncSession, client: AsyncClient):
    """Test moving a ticket to another column."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.flush()
    
    column1 = Column(board_id=board.id, name="To Do", position=0)
    column2 = Column(board_id=board.id, name="In Progress", position=1)
    db.add_all([column1, column2])
    await db.flush()
    
    ticket = Ticket(
        title="Test Ticket",
        description="Test",
        column_id=column1.id,
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.TODO,
        position=0
    )
    db.add(ticket)
    await db.commit()
    
    response = await client.patch(
        f"/api/v1/tickets/{ticket.id}/move",
        json={"column_id": str(column2.id), "position": 1000}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert str(data["column_id"]) == str(column2.id)
