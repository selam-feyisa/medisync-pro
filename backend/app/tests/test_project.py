import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project, Workspace
from app.schemas import ProjectCreate


@pytest.mark.asyncio
async def test_create_project(db: AsyncSession):
    """Test project creation."""
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
        description="A test project",
    )
    db.add(project)
    await db.flush()

    assert project.name == "Test Project"
    assert project.workspace_id == workspace.id


@pytest.mark.asyncio
async def test_project_archive(db: AsyncSession):
    """Test project archiving."""
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
        owner_id=uuid4(),
    )
    db.add(workspace)
    await db.flush()

    project = Project(
        workspace_id=workspace.id,
        name="Archivable Project",
        slug="archive-project",
    )
    db.add(project)
    await db.flush()

    project.is_archived = True

    assert project.is_archived is True
