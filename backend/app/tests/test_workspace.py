import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Workspace, WorkspaceMember, MemberRole
from app.schemas import WorkspaceCreate
from app.services import WorkspaceService


@pytest.mark.asyncio
async def test_create_workspace(db: AsyncSession):
    """Test workspace creation."""
    owner_id = uuid4()
    workspace_data = WorkspaceCreate(
        name="Test Workspace",
        slug="test-workspace",
        description="A test workspace",
    )

    workspace = await WorkspaceService.create_workspace(db, workspace_data, owner_id)

    assert workspace.name == "Test Workspace"
    assert workspace.slug == "test-workspace"
    assert workspace.owner_id == owner_id


@pytest.mark.asyncio
async def test_get_workspace_by_id(db: AsyncSession):
    """Test retrieving workspace by ID."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    retrieved = await WorkspaceService.get_workspace_by_id(db, workspace.id)

    assert retrieved is not None
    assert retrieved.id == workspace.id


@pytest.mark.asyncio
async def test_get_user_workspaces(db: AsyncSession):
    """Test retrieving all workspaces for a user."""
    user_id = uuid4()
    workspace = Workspace(
        name="User Workspace",
        slug="user-ws",
        owner_id=user_id,
    )
    db.add(workspace)
    await db.flush()

    member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user_id,
        role=MemberRole.owner,
    )
    db.add(member)
    await db.flush()

    workspaces = await WorkspaceService.get_user_workspaces(db, user_id)

    assert len(workspaces) > 0
    assert workspaces[0].id == workspace.id
