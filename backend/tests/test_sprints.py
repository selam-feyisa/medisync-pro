import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models import User, Workspace, Project, Board, Sprint
from app.models.sprint import SprintStatus


@pytest.mark.asyncio
async def test_create_sprint(db: AsyncSession, client: AsyncClient):
    """Test creating a new sprint."""
    # Create test data
    workspace = Workspace(name="Test Workspace")
    db.add(workspace)
    await db.flush()
    
    project = Project(workspace_id=workspace.id, name="Test Project", slug="test-project")
    db.add(project)
    await db.flush()
    
    board = Board(project_id=project.id, name="Test Board")
    db.add(board)
    await db.commit()
    
    response = await client.post(
        "/api/v1/sprints",
        json={
            "board_id": str(board.id),
            "name": "Sprint 1",
            "goal": "Complete initial features"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sprint 1"
    assert data["goal"] == "Complete initial features"
    assert data["status"] == "planned"


@pytest.mark.asyncio
async def test_start_sprint(db: AsyncSession, client: AsyncClient):
    """Test starting a sprint."""
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
    
    sprint = Sprint(
        board_id=board.id,
        name="Sprint 1",
        goal="Test goal",
        status=SprintStatus.planned
    )
    db.add(sprint)
    await db.commit()
    
    response = await client.post(f"/api/v1/sprints/{sprint.id}/start")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["start_date"] is not None


@pytest.mark.asyncio
async def test_complete_sprint(db: AsyncSession, client: AsyncClient):
    """Test completing a sprint."""
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
    
    sprint = Sprint(
        board_id=board.id,
        name="Sprint 1",
        goal="Test goal",
        status=SprintStatus.active,
        start_date=datetime.utcnow()
    )
    db.add(sprint)
    await db.commit()
    
    response = await client.post(f"/api/v1/sprints/{sprint.id}/complete")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["end_date"] is not None


@pytest.mark.asyncio
async def test_list_sprints(db: AsyncSession, client: AsyncClient):
    """Test listing sprints for a board."""
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
    
    sprint1 = Sprint(board_id=board.id, name="Sprint 1", goal="Goal 1", status=SprintStatus.planned)
    sprint2 = Sprint(board_id=board.id, name="Sprint 2", goal="Goal 2", status=SprintStatus.completed)
    db.add_all([sprint1, sprint2])
    await db.commit()
    
    response = await client.get(f"/api/v1/boards/{board.id}/sprints")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_start_sprint_validation(db: AsyncSession, client: AsyncClient):
    """Test that starting a second active sprint fails."""
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
    
    active_sprint = Sprint(
        board_id=board.id,
        name="Active Sprint",
        goal="Active goal",
        status=SprintStatus.active,
        start_date=datetime.utcnow()
    )
    db.add(active_sprint)
    await db.flush()
    
    new_sprint = Sprint(
        board_id=board.id,
        name="New Sprint",
        goal="New goal",
        status=SprintStatus.planned
    )
    db.add(new_sprint)
    await db.commit()
    
    response = await client.post(f"/api/v1/sprints/{new_sprint.id}/start")
    
    assert response.status_code == 400
