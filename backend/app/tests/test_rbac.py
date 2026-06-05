import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Workspace, WorkspaceMember, MemberRole
from app.services import RBACService


@pytest.mark.asyncio
async def test_check_workspace_access(db: AsyncSession):
    """Test checking workspace access."""
    user_id = uuid4()
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
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

    has_access = await RBACService.check_workspace_access(db, user_id, workspace.id)
    assert has_access is True


@pytest.mark.asyncio
async def test_check_workspace_permission(db: AsyncSession):
    """Test checking user workspace permission."""
    user_id = uuid4()
    workspace = Workspace(
        name="Test Workspace",
        slug="test-ws",
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

    has_permission = await RBACService.check_workspace_permission(
        db, user_id, workspace.id, MemberRole.member
    )
    assert has_permission is True
