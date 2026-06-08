"""Seed script for demo data."""

import asyncio
from datetime import datetime, timezone, timedelta
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember, MemberRole
from app.models.project import Project, Visibility
from app.models.board import Board, BoardType
from app.models.column import Column
from app.models.sprint import Sprint, SprintStatus


async def seed_data():
    """Seed demo data for testing."""
    async with async_session_maker() as session:
        # Create demo users
        admin_user = User(
            email="admin@medisync.com",
            full_name="Admin User",
            hashed_password=hash_password("admin123"),
            role=UserRole.admin,
            timezone="UTC",
        )
        session.add(admin_user)
        await session.commit()
        await session.refresh(admin_user)

        doctor_user = User(
            email="doctor@medisync.com",
            full_name="Dr. Smith",
            hashed_password=hash_password("doctor123"),
            role=UserRole.doctor,
            timezone="America/New_York",
        )
        session.add(doctor_user)
        await session.commit()
        await session.refresh(doctor_user)

        # Create workspace
        workspace = Workspace(
            name="MediSync Clinic",
            slug="medisync-clinic",
            description="Main clinic workspace",
            plan="pro",
            owner_id=admin_user.id,
        )
        session.add(workspace)
        await session.commit()
        await session.refresh(workspace)

        # Add members to workspace
        admin_member = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=admin_user.id,
            role=MemberRole.owner,
        )
        session.add(admin_member)

        doctor_member = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=doctor_user.id,
            role=MemberRole.admin,
        )
        session.add(doctor_member)
        await session.commit()

        # Create project
        project = Project(
            workspace_id=workspace.id,
            name="Patient Management",
            slug="patient-management",
            description="Manage patient records and appointments",
            visibility=Visibility.private,
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)

        # Create Kanban board
        kanban_board = Board(
            project_id=project.id,
            name="Patient Tasks",
            board_type=BoardType.kanban,
        )
        session.add(kanban_board)
        await session.commit()
        await session.refresh(kanban_board)

        # Create columns for Kanban board
        todo_column = Column(
            board_id=kanban_board.id,
            name="To Do",
            position=0,
            is_done_column=False,
        )
        session.add(todo_column)

        in_progress_column = Column(
            board_id=kanban_board.id,
            name="In Progress",
            position=1,
            is_done_column=False,
        )
        session.add(in_progress_column)

        done_column = Column(
            board_id=kanban_board.id,
            name="Done",
            position=2,
            is_done_column=True,
        )
        session.add(done_column)
        await session.commit()

        # Create Scrum board
        scrum_board = Board(
            project_id=project.id,
            name="Sprint Board",
            board_type=BoardType.scrum,
        )
        session.add(scrum_board)
        await session.commit()
        await session.refresh(scrum_board)

        # Create columns for Scrum board
        backlog_column = Column(
            board_id=scrum_board.id,
            name="Backlog",
            position=0,
            is_done_column=False,
        )
        session.add(backlog_column)

        todo_column_scrum = Column(
            board_id=scrum_board.id,
            name="To Do",
            position=1,
            is_done_column=False,
        )
        session.add(todo_column_scrum)

        in_progress_column_scrum = Column(
            board_id=scrum_board.id,
            name="In Progress",
            position=2,
            is_done_column=False,
        )
        session.add(in_progress_column_scrum)

        done_column_scrum = Column(
            board_id=scrum_board.id,
            name="Done",
            position=3,
            is_done_column=True,
        )
        session.add(done_column_scrum)
        await session.commit()

        # Create sprint
        sprint = Sprint(
            board_id=scrum_board.id,
            name="Sprint 1",
            goal="Complete patient registration feature",
            start_date=datetime.now(timezone.utc),
            end_date=datetime.now(timezone.utc) + timedelta(days=14),
            status=SprintStatus.planning,
        )
        session.add(sprint)
        await session.commit()

        print("Demo data seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())
